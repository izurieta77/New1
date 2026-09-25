# Módulo 19 — Biblioteca esencial: 40 libros y sus lecciones operables

> Nivel: licenciatura → doctorado + práctica · Actualizado: 2026-09-25 · Grado de evidencia global: **B (bimodal)**. Lo que el canon enseña como **aritmética o teorema** (Kelly, costos, p = E(mx), sesgo de supervivencia) o como **historia replicada con datos** (DMS, Reinhart-Rogoff, Kindleberger, LTCM) es **A**. El **método de practicante** (margen de seguridad, ciclos, reflexividad) es **B/C**. La **anécdota de ganadores** (Market Wizards, Lefèvre) es **D**: solo genera hipótesis.

No se repiten aquí: [01](01-licenciatura-fundamentos.md) (Kelly fraccional, DMS, Bessembinder, SPIVA), [02](02-maestria-portafolio-y-asset-pricing.md) (factores y su decaimiento), [03](03-maestria-valuacion-y-analisis-fundamental.md) (Graham, fórmula mágica, decaimiento de Berkshire), [05](05-maestria-derivados-y-volatilidad.md) (tail hedging), cap. 07 (backtesting), cap. 08 (sesgos), [15](15-eventos-corporativos-y-situaciones-especiales.md), [16](16-macro-global-divisas-y-el-peso.md) (Dalio, Reinhart-Rogoff), [17](17-crisis-burbujas-libro-de-patrones.md) (Kindleberger-Minsky), [18](18-grandes-inversionistas-decodificados.md) (historiales de los autores). Parámetros: `config/parametros.json`.

**Convenciones.** [n] = fuente de §9. **"Inferencia:"** = interpretación propia. **"Regla:"** = recomendación (solo en §6). **"(no verificado)"** = no confirmado en esta sesión. El grado de un libro es el **mínimo** entre la calidad de su evidencia y su aplicabilidad a una cuenta de MXN 20,000 operada a mano en GBM.

---

## 1. Objetivos de dominio

1. Citar de los 40 libros el autor, el año, la edición vigente, la tesis, 3 lecciones operables y la crítica principal.
2. Ubicar cada libro en su estante (A decisión · B negocio y valuación · C tamaño y supervivencia · D mercados y rendimientos esperados · E crisis y ciclos · F cuantitativo · G practicantes) y en su nivel.
3. Separar en cada libro teorema, dato replicado, historial y anécdota, y resolver con evidencia los desacuerdos del canon.
4. Convertir cada lección en una regla atada a un parámetro.
5. Seguir la ruta de lectura e incorporar lo publicado en 2023-2026.

## 2. Núcleo teórico / marco

### 2.1 Jerarquía de evidencia de un libro

| Nivel | Afirmación | Ejemplos | Grado máx. |
|---|---|---|---|
| 1 | Identidad o teorema | Kelly, aritmética de costos (Bogle), p = E(mx) | A |
| 2 | Datos públicos replicados | DMS, Reinhart-Rogoff, SPIVA | A/B |
| 3 | Historial público del autor | Berkshire, Magellan | B (selección) |
| 4 | Historial privado reportado | Baupost, Gotham, Medallion, Quantum | C |
| 5 | Anécdota, entrevista o novela | Lefèvre, Schwager, Housel | D |

**Inferencia:** una biblioteca de inversión es una muestra de sobrevivientes: el practicante escribe después de ganar. Por eso valen doble los libros sobre fracasos (*When Genius Failed*, Livermore, *The Missing Billionaires*), y el canon sobrerrepresenta la concentración y la convicción.

### 2.2 Ocho convergencias que sobreviven a la evidencia

1. **Sobrevivir primero** (Buffett, Marks, Taleb, Thorp, Housel): la ruina es absorbente.
2. **Los costos deciden** (Bogle, Malkiel, Swensen, Carver).
3. **Precio contra valor: qué descuenta el precio** (Graham, Klarman, Rappaport-Mauboussin, Damodaran).
4. **El tamaño importa tanto como la dirección** (Thorp, Poundstone, Haghani-White, Chan, Carver).
5. **Proceso sobre resultado** (Duke, Mauboussin, Tetlock, Taleb).
6. **Los ciclos existen; el timing es difícil** (Marks, Kindleberger, Shiller, Reinhart-Rogoff, Dalio, Soros).
7. **Los backtests mienten por defecto** (López de Prado, Carver, Chan; McLean-Pontiff, cap. 03).
8. **Apalancamiento más iliquidez mata** (LTCM, Kindleberger, Pedersen).

### 2.3 Desacuerdos reales y su resolución

| Debate | Bando 1 | Bando 2 | Resolución |
|---|---|---|---|
| ¿Se le gana al mercado? | Graham, Buffett, Lynch | Malkiel, Bogle | "Eficientemente ineficiente" (Pedersen, Lo): la mayoría pierde neto de costos (A); las primas existen y decaen al publicarse |
| ¿Concentrar? | Munger, Fisher | Bogle, Swensen | La mediana de una acción pierde contra T-bills (Bessembinder). Solo con ventaja demostrada y con topes |
| ¿Kelly completo? | Kelly (1956) | Samuelson | El error de estimación manda: Kelly fraccional |
| ¿Timing del ciclo? | Marks, Shiller, Dalio | Bogle | La valuación predice a 10 años con ruido; no es gatillo. Ajustar dentro de bandas |
| ¿Cobertura de cola permanente? | Taleb | Ilmanen/AQR | El put continuo cuesta más de lo que protege (cap. 05) |

## 3. Literatura y fuentes canónicas

### 3.1 Tabla maestra

Nivel: Lic = licenciatura, Maes = maestría, Doc = doctorado, Práct = práctica.

| # | Libro · autor · año (edición vigente verificada) | Est. · nivel | Hallazgo cuantificado | Grado | [n] |
|---|---|---|---|---|---|
| 1 | *Thinking, Fast and Slow* · Kahneman · 2011 (+ *Noise*, 2021) | A · Lic/Maes | El capítulo de priming tiene un R-index de 14 | B | [15] |
| 2 | *Superforecasting* · Tetlock y Gardner · Crown 2015 | A · Lic/Maes | GJP: 35-72% más preciso que los otros equipos de IARPA; ~30% mejor que analistas con información clasificada | A geopolítica / C precios | [16] |
| 3 | *Thinking in Bets* · Duke · Portfolio 2018 (+ *Quit*, 2022) | A · Lic | Marco de decisión, sin métrica | B | [17] |
| 4 | *Fooled by Randomness* (2001; 2.ª ed. 2004) y *The Black Swan* (2007; ampl. 2010) · Taleb | A · Maes | Colas gruesas: hecho. Universa +3,612% sobre la prima (mar-2020), contra el costo continuo de la cobertura (cap. 05) | A hecho / D cobertura permanente | [14] |
| 5 | *More Than You Know* (Columbia UP 2006) y *The Success Equation* (HBR Press 2012) · Mauboussin | A · Maes | Marco de suerte contra habilidad | B | [10] |
| 6 | *Poor Charlie's Almanack* · Munger · 2005; ampl. 2008; Stripe Press 2023 | A · Lic | Wheeler Munger: 19.8% contra 5.0% del Dow (1962-1975) | B/C | [43] |
| 7 | *The Psychology of Money* · Housel · Harriman 2020 (+ *Same as Ever*, 2023) | A · Lic | Anecdótico | C | [41] |
| 8 | *Against the Gods* · P. L. Bernstein · Wiley 1996 | A · Lic | Historia de las ideas de riesgo | A | [26] |
| 9 | *The Intelligent Investor* (1949; 4.ª ed. rev. 1973; 3.ª ed. revisada con Zweig, Harper Business 2024) y *Security Analysis*, con Dodd (1934; 7.ª ed., McGraw-Hill, 27-jun-2023) · Graham | B · Lic/Maes | HML −57.8% (dic-2006 a sep-2020; cap. 03) | B | [1][2] |
| 10 | *Common Stocks and Uncommon Profits* · Fisher · 1958 | B · Lic | Motorola, de 1955 hasta su muerte: un caso, no una muestra | C | [3] |
| 11 | *The Essays of Warren Buffett* · Cunningham · 1997; ediciones revisadas hasta 2019; Wiley 2021 | B · Lic/Maes | Berkshire 19.7% contra 10.5% (1965-2025); 13.0% contra 14.1% (2011-2025) | B | [4][46] |
| 12 | *One Up on Wall Street* · Lynch · 1989 | B · Lic | Magellan 29.2% contra 15.8% (1977-1990) | C/D | [5] |
| 13 | *Margin of Safety* · Klarman · HarperBusiness 1991 | B · Maes | "20% compuesto desde 1982" (sin cita); −7% a −13% en 2008 | B/C | [7] |
| 14 | *The Little Book That (Still) Beats the Market* (Wiley 2005/2010) y *You Can Be a Stock Market Genius* (1997) · Greenblatt | B · Lic/Maes | Réplica EUA 2003-2015: 11.4% contra 8.7% del S&P, lejos del ~30% del libro | C | [8] |
| 15 | *Investment Valuation* (Wiley, 4.ª ed. 2024) y *Narrative and Numbers* (Columbia UP 2017) · Damodaran | B · Maes | Herramienta; no hay alfa atribuible | A herramienta / C alfa | [9] |
| 16 | *Expectations Investing* · Rappaport y Mauboussin · 2001; ed. rev. 2021 | B · Maes | Método (DCF inverso) | B | [10] |
| 17 | *The Most Important Thing* (Columbia UP 2011) y *Mastering the Market Cycle* (2018) · Marks | C · Lic/Maes | Oaktree levantó US$10.9 mil millones en 2008, el mayor fondo de deuda en problemas de la historia | B riesgo / C timing | [6] |
| 18 | *A Man for All Markets* · Thorp · Random House 2017 | C · Lic | Reportó 20% anual en 28.5 años (1998). Ridgeline cerró en 2002 | A Kelly / D replicar | [11] |
| 19 | *Fortune's Formula* · Poundstone · Hill and Wang 2005 | C · Lic | Con ventaja de 60/40, el 28% de los participantes quebró (Haghani-Dewey) | A | [12][13] |
| 20 | *When Genius Failed* · Lowenstein · Random House 2000 | C · Lic | LTCM: más de 25:1; −US$4.6 mil millones en menos de 4 meses; rescate de US$3.625 mil millones | A | [40] |
| 21 | *A Random Walk Down Wall Street* · Malkiel · 1973; 13.ª ed. 2023 | D · Lic | SPIVA EUA 2025: 79% de los activos large-cap pierde | A | [27][47] |
| 22 | *The Little Book of Common Sense Investing* · Bogle · Wiley 2007; ed. 2017 | D · Lic | SPIVA México: 75.6% pierde a 10 años (cap. 01) | A | [25][47] |
| 23 | *Stocks for the Long Run* · Siegel · 1994; 6.ª ed. McGraw-Hill 2022 | D · Lic | ~6.5-7% real anual en 200 años; McQuarrie: acciones ≈ bonos en 1797-1942 | B | [28] |
| 24 | *Triumph of the Optimists* · Dimson, Marsh y Staunton · Princeton UP 2002 | D · Maes | 16 países y 101 años. Yearbook 2026: 35 mercados y 126 años; EUA 6.6% real | A | [29] |
| 25 | *Pioneering Portfolio Management* (2000; rev. 2009) y *Unconventional Success* (2005) · Swensen | D · Maes | Yale: 12.4% anual en los 30 años a 2020; −24.6% en 2008 | B individuos / C endowment | [24] |
| 26 | *Expected Returns* (Wiley 2011) e *Investing Amid Low Expected Returns* (Wiley, abr-2022) · Ilmanen | D · Doc | Factores de EUA 2016-2025 ≈ 0 bruto (cap. 02) | B | [22] |
| 27 | *Efficiently Inefficient* · Pedersen · Princeton UP 2015 | D · Maes/Doc | Primas por liquidez e información | B | [23] |
| 28 | *Adaptive Markets* · Lo · Princeton UP 2017 | D · Maes | Consistente con −58% post-publicación | C | [30] |
| 29 | *Asset Pricing* · Cochrane · 2001; rev. 2005 | D · Doc | "Discount Rates" (JF 2011): la variación de P/D es variación de la tasa de descuento | A | [42] |
| 30 | *Irrational Exuberance* · Shiller · Princeton UP 2000; 3.ª ed. 2015 | E · Lic/Maes | Salió el mes del pico del Nasdaq, que luego cayó más de 80% en dos años | B/C | [31] |
| 31 | *Manias, Panics, and Crashes* · Kindleberger (1978); 8.ª ed. con Aliber y McCauley, Springer 2023 | E · Maes | Patrón de 5 etapas (cap. 17) | B | [32] |
| 32 | *This Time Is Different* · Reinhart y Rogoff · Princeton UP 2009 | E · Maes | 66 países y 8 siglos; la vivienda real cae ~35% en ~6 años tras una crisis bancaria | B | [33] |
| 33 | *Principles* (2017) y *Big Debt Crises* (2018) · Dalio | E · Lic/Maes | Pure Alpha II: −18.6% (2020, a agosto) y +33% (2025) (cap. 18) | B proceso / D reloj | [21] |
| 34 | *The Alchemy of Finance* · Soros · 1987; reed. 2003 | E · Maes | Quantum: más de 20% compuesto; más de US$1,000 millones en 1992 | C | [18] |
| 35 | *Advances in Financial Machine Learning* · López de Prado · Wiley 2018 | F · Doc | El DSR (JPM 2014) corrige la selección y la no normalidad | A validación / C alfa | [34][36] |
| 36 | *Systematic Trading* · Carver · Harriman 2015 (+ AFTS, abr-2023) | F · Práct | Marco sin historial auditado público | B | [37] |
| 37 | *Quantitative Trading* (2008; 2.ª ed. 2021) y *Algorithmic Trading* (2013) · Chan · Wiley | F · Práct | Backtests dentro de muestra | C | [38] |
| 38 | *The Man Who Solved the Market* · Zuckerman · Portfolio 2019 | F · Lic | Medallion: 66% bruto y 39% neto (1988-2018) | A hecho / D transferir | [39] |
| 39 | *Reminiscences of a Stock Operator* · Lefèvre · 1923; anotada Wiley 2009 | G · Práct | Livermore quebró varias veces; se suicidó en 1940 | D | [19] |
| 40 | *Market Wizards* · Schwager · 1989 (serie hasta 2020) | G · Práct | Sin grupo de control | C/D | [20] |

### 3.2 Fichas: tesis, lecciones y contra

**A — Decisión e incertidumbre**

**1. Kahneman.** *Tesis:* la intuición (Sistema 1) comete errores sistemáticos; en la teoría prospectiva las pérdidas pesan más que las ganancias. *Lecciones:* (1) partir de la tasa base; (2) escribir la probabilidad antes de ver el resultado; (3) revisar el portafolio con menos frecuencia para no vender en pánico. *Contra:* el capítulo de priming no replica, y Kahneman admitió "I placed too much faith in underpowered studies" [15].

**2. Tetlock y Gardner.** *Tesis:* el pronóstico es medible con Brier, entrenable y agregable. *Lecciones:* (1) cada tesis es una pregunta con fecha y probabilidad; (2) descomponer y partir de la tasa base; (3) actualizar poco y seguido, y ponderar a cada quien por su historial. *Contra:* en mercados el precio ya agrega pronósticos: la ventaja tiene que ser contra el precio.

> **Adenda 2026-09-25 (examen diagnóstico S5-10, ficha `conocimiento/fichas/2026-09-25-examen-S1-S5-huecos.md`).** Ficha técnica ampliada, con una **corrección importante** a una cifra que circulaba en el examen (no en este capítulo):
> - **Tetlock, *Expert Political Judgment* (2005):** 284 expertos, ~28,000 predicciones (también reportado como 82,361 juicios de probabilidad en otras fuentes), proyecto de 1984 a 2003. Los expertos fueron apenas mejores que el azar y casi siempre peores que algoritmos simples de extrapolación. Los "zorros" (eclécticos) superaron a los "erizos" (una sola gran teoría).
> - **Good Judgment Project (torneo ACE de IARPA):** superó al grupo de control por más de 50-60% en Brier; los *superforecasters* son el 2% superior de los participantes, con persistencia de ~70% año con año. Mellers et al. (2014), *Psychological Science*, identifican tres factores de precisión: entrenamiento breve en razonamiento probabilístico, trabajo en equipo y seguimiento (agrupar a los mejores en equipos de élite). https://journals.sagepub.com/doi/10.1177/0956797614524255
> - **Extremización (Baron et al., *Decision Analysis*, 2014):** conviene extremizar el promedio de varios pronósticos cuando la información es parcialmente independiente (cada uno tiene solo una parte) y cuando los juicios individuales están comprimidos hacia 0.5 por ruido.
> - **Mercados de predicción (Berg, Nelson y Rietz, *International Journal of Forecasting*, 2008):** en 964 comparaciones simultáneas con encuestas, en cinco elecciones presidenciales de EUA (1988-2004), el Iowa Electronic Market estuvo más cerca del resultado final **74%** de las veces, con ventaja mayor a horizontes largos.
> - **Halawi et al. (2024, NeurIPS):** el sistema LLM con recuperación de noticias obtuvo Brier de **0.179** contra **0.149** del agregado de la comunidad; el promedio de ambos dio **0.146**, mejor que cualquiera de los dos por separado.
> - **ForecastBench (Karger et al., 2025, ICLR) — cifras corregidas tras verificar el PDF publicado (arXiv 2409.19839, Tabla 2, subconjunto de 200 preguntas estándar) con `pypdf`:** superforecaster (mediana) **Brier = 0.096** [IC 0.076-0.116]; público general (mediana) **0.121** [0.101-0.141]; mejor LLM (Claude-3-5-Sonnet-20240620, valores congelados, *prompt* "scratchpad") **0.122** [0.099-0.146]. *(Nota: una versión previa de esta cifra, que circuló en un examen interno como 0.093/0.107/0.111, no coincide con el texto del artículo publicado; se corrige aquí y se registra en `conocimiento/registro-de-errores.md`.)* https://arxiv.org/abs/2409.19839
> - **Implicación para usar un LLM como pronosticador en inversión:** tratarlo como un insumo más dentro de un ensamble con la multitud o el precio (así es como mejora en Halawi), evaluarlo solo con preguntas posteriores a su fecha de corte para evitar fuga de información, y exigir habilidad medible (Brier del LLM mejor que el del mercado, con N ≥ 30-50 por tipo de pregunta) antes de confiar en él.

**3. Duke.** *Tesis:* decidir es apostar; juzgar una decisión por su resultado (*resulting*) es el error central. *Lecciones:* (1) en el post-mortem, separar la calidad de la decisión de la suerte; (2) pre-mortem antes de entrar; (3) criterios de abandono fijados de antemano (*Quit*). *Contra:* el póker da retroalimentación rápida; la inversión, muestras chicas.

**4. Taleb.** *Tesis:* confundimos suerte con habilidad y subestimamos los extremos. *Lecciones:* (1) desconfiar de historiales cortos con sesgo negativo; (2) dimensionar por la pérdida máxima plausible, no por la σ gaussiana; (3) barbell: núcleo seguro y satélite convexo de pérdida acotada. *Contra:* no da reglas de entrada, y la cobertura de cola permanente pierde (cap. 05).

**5. Mauboussin (ensayos y suerte-habilidad).** *Tesis:* con mucha suerte en juego, la habilidad se mide con muestras grandes. Paradoja de la habilidad: cuando todos son hábiles, decide la suerte. *Lecciones:* (1) ubicar la actividad en el continuo suerte-habilidad antes de juzgar a alguien (rivales incluidos); (2) tasas base para crecimiento y márgenes; (3) no extrapolar el mejor semestre. *Contra:* son ensayos, no pruebas.

**6. Munger.** *Tesis:* un enrejado de modelos mentales, la inversión del problema y 25 sesgos que se combinan ("lollapalooza") [43]. *Lecciones:* (1) listar cómo fracasaría la tesis; (2) checklist multidisciplinario; (3) pocas decisiones y un círculo de competencia explícito. *Contra:* su sociedad cayó −32% en 1973 y −31% en 1974 (cap. 18); esa concentración choca con los cortacircuitos del sistema.

**7. Housel.** *Tesis:* la conducta pesa más que la inteligencia. Hay que sobrevivir con margen de error y dejar que operen las colas. *Lecciones:* (1) margen de error en cada plan; (2) "razonable" le gana a "racional"; (3) definir qué es "suficiente". *Contra:* anécdotas elegidas; lo cuantificable ya está en Bessembinder y DMS.

**8. Bernstein.** *Tesis:* historia del riesgo, de Pascal y Fermat a Bernoulli, Galton, Markowitz y Kahneman-Tversky. *Lecciones:* (1) distinguir riesgo medible de incertidumbre (Knight); (2) la regresión a la media engaña si la media cambia; (3) utilidad no es valor esperado (Bernoulli), y de ahí sale Kelly. *Contra:* se publicó antes de LTCM, 2008 y los factores.

**B — Negocio y valuación**

**9. Graham.** *Tesis:* una acción es parte de un negocio, el "Señor Mercado" ofrece precios de ánimo cambiante, y se compra con margen de seguridad. *Lecciones:* (1) el valor es un rango conservador; (2) el margen protege contra el error propio; (3) el inversionista defensivo diversifica con reglas mecánicas. *Contra:* el propio Graham, en los años 70: "I doubt whether in most cases such extensive efforts will generate sufficiently superior selections to justify their cost" [2].

**10. Fisher.** *Tesis:* pocas empresas excepcionales, investigadas por *scuttlebutt*; el mejor momento para vender es "almost never" [3]. *Lecciones:* (1) investigar en campo con clientes, proveedores y competidores; (2) juzgar la calidad de la administración y de su reinversión; (3) no vender por una sobrevaluación leve. *Contra:* sesgo de supervivencia; como la mayoría de las acciones pierde contra T-bills, "casi nunca vender" exige atinarle a los pocos ganadores.

**11. Cunningham / Buffett.** *Tesis:* las cartas ordenadas por tema: asignación de capital, valor intrínseco contra contable, recompras debajo del valor y el float de seguros. *Lecciones:* (1) medir un negocio por su rentabilidad sin apalancamiento excesivo; (2) recomprar solo debajo del valor conservador; (3) no usar un apalancamiento que obligue a vender. *Contra:* su motor es value, calidad y beta baja apalancados ~1.6-1.7× con float barato (caps. 03 y 18), y no se copia.

**12. Lynch.** *Tesis:* el individuo ve primero a ciertas empresas y luego valida los fundamentales. Seis tipos: crecimiento lento, *stalwarts*, crecimiento rápido, cíclicas, *turnarounds* y *asset plays* [5]. *Lecciones:* (1) clasificar la acción antes de valuarla; (2) explicar la tesis en dos minutos; (3) en una cíclica, un P/U bajo en el pico de utilidades es una trampa. *Contra:* Lynch tenía cientos de acciones y un equipo de análisis. "Invierte en lo que conoces" coincide con el sesgo de familiaridad de Huberman (RFS 2001) [45].

**13. Klarman.** *Tesis:* rendimiento absoluto con aversión al riesgo, descuento sobre un valor conservador y aprovechamiento de las restricciones institucionales de otros. *Lecciones:* (1) medir la pérdida permanente, no el rezago contra el índice; (2) el efectivo es una opción (llegó a 30-50%); (3) buscar vendedores forzados y un catalizador. *Contra:* el efectivo tiene costo de oportunidad y el historial no está auditado.

**14. Greenblatt.** *Tesis:* comprar "buenas empresas baratas" (EBIT/EV y ROC altos), 20-30 acciones con rebalanceo anual. En *Genius*: situaciones especiales con vendedores no económicos. *Lecciones:* (1) combinar calidad con valor; (2) mantener la disciplina en los años de rezago; (3) una regla simple le gana al juicio ruidoso. *Contra:* rezago en 2007-2011; un estudio de 2024 lo atribuye a factores conocidos [8]; los spin-offs decayeron (cap. 15).

**15. Damodaran.** *Tesis:* una valuación es una historia convertida en números coherentes (flujos, crecimiento, riesgo). *Lecciones:* (1) crecimiento = reinversión × ROIC, y la tasa en la moneda de los flujos (MXN o USD); (2) ir de la historia a las variables, al valor y de vuelta a la historia; (3) que algo esté barato no garantiza que el precio converja. *Contra:* el DCF es muy sensible a sus supuestos y no es una regla de trading.

**16. Rappaport y Mauboussin.** *Tesis:* no pronosticar el valor, sino leer las expectativas implícitas en el precio (DCF inverso) y apostar a su revisión. *Lecciones:* (1) calcular qué crecimiento, margen y duración de la ventaja descuenta el precio; (2) identificar el disparador de valor de más impacto; (3) comprar solo con brecha grande y catalizador. *Contra:* exige pronosticar mejor que el consenso (cap. 25).

**C — Tamaño y supervivencia**

**17. Marks.** *Tesis:* pensamiento de segundo nivel. El riesgo es la pérdida permanente, y los ciclos oscilan como un péndulo: se sabe "dónde estamos", no "a dónde vamos". *Lecciones:* (1) preguntar qué descuenta el consenso; (2) medir la temperatura con síntomas (crédito fácil, emisiones basura, "esta vez es distinto"); (3) ajustar la agresividad dentro de límites. *Contra:* sin reglas cuantitativas; el ciclo se diagnostica fácil a posteriori.

**18. Thorp.** *Tesis:* primero la ventaja medible y después el tamaño disciplinado, en el blackjack y en el mercado. *Lecciones:* (1) sin ventaja cuantificada no hay apuesta; (2) Kelly fraccional; (3) detectar el fraude por su imposibilidad estadística (dudó de Madoff desde 1991) [11]. *Contra:* sus oportunidades de los años 60 a 80 ya fueron arbitradas.

**19. Poundstone.** *Tesis:* la historia de Kelly (Shannon, Thorp) y su pleito con Samuelson. *Lecciones:* (1) maximizar el log de la riqueza equivale a maximizar el CAGR, la función objetivo del sistema; (2) apostar el doble de Kelly baja el crecimiento a la tasa libre de riesgo (cap. 01); (3) una fracción de Kelly recorta mucho la volatilidad y poco el crecimiento. *Contra:* Samuelson: "When you lose — and you sure can lose — with N large, you can lose real big" [12]. En un torneo de 6 meses el objetivo no es logarítmico (cap. 18).

**20. Lowenstein.** *Tesis:* LTCM: premios Nobel, convergencia y apalancamiento. *Lecciones:* (1) en una fuga hacia la liquidez, las posiciones "diversificadas" se mueven juntas; (2) el apalancamiento vuelve permanente una pérdida temporal: la prima de Royal Dutch sobre Shell pasó de 8-10% a ~22% [40]; (3) devolver capital sin reducir posiciones sube el apalancamiento. *Contra:* periodismo, sin probabilidades ex ante.

**D — Mercados y rendimientos esperados**

**21. Malkiel.** *Tesis:* los precios siguen aproximadamente una caminata aleatoria; ni el análisis técnico ni el fundamental le ganan al índice neto de costos. *Lecciones:* (1) un núcleo indexado barato; (2) rebalancear y diversificar entre países; (3) no elegir fondos por su pasado. *Contra:* las anomalías existen dentro de muestra, pero decaen al publicarse.

**22. Bogle.** *Tesis:* los inversionistas en conjunto obtienen el mercado menos costos. *Lecciones:* (1) minimizar comisiones, rotación e impuestos; (2) rendimiento a 10 años ≈ dividendo + crecimiento + cambio de P/U; (3) al menos 20% en bonos para la mayoría [25]. *Contra:* en un torneo, indexar asegura la mediana, no el primer lugar.

**23. Siegel.** *Tesis:* desde 1802, las acciones de EUA rinden 6.5-7% real y a plazos largos son menos riesgosas que los bonos. *Lecciones:* (1) el horizonte cambia qué riesgo importa; (2) valuaciones altas anticipan rendimientos menores. *Contra:* McQuarrie encontró que Siegel subestimó los bonos del siglo XIX en ~1.5 pp, y que en 1797-1942 acciones y bonos rindieron casi lo mismo [28].

**24. Dimson, Marsh y Staunton.** *Tesis:* 101 años en 16 países: las acciones ganan, pero los índices con sobrevivientes y los datos de EUA inflan la prima esperada [29]. *Lecciones:* (1) usar evidencia global; (2) esperar una prima menor que la histórica de EUA; (3) actualizar cada año con el Yearbook. *Contra:* Inferencia: aun con 35 mercados, la muestra favorece a los países que sobrevivieron.

**25. Swensen.** *Tesis:* para la institución perpetua: diversificar, sesgarse a renta variable y aprovechar lo ilíquido. Para el individuo: seis clases de activo (EUA, desarrolladas, emergentes, REITs, Treasuries y TIPS), rebalanceo e índices baratos [24]. *Lecciones:* (1) la asignación pesa más que la selección; (2) rebalancear con disciplina; (3) la iliquidez es un costo que solo conviene a quien puede cargarlo. *Contra:* Ellis: el modelo es difícil de replicar y las primas alternativas se comprimen.

**26. Ilmanen.** *Tesis:* estimar rendimientos esperados desde las clases de activo, los estilos, los factores y su variación en el tiempo. En 2022, tras décadas de revaluación, eran mínimos [22]. *Lecciones:* (1) separar yield + crecimiento + revaluación y no proyectar la revaluación; (2) diversificar entre primas de estilo; (3) timing solo en dosis pequeñas, porque el costo es el alfa más seguro. *Contra:* los estilos long-short tuvieron una década pobre (cap. 02).

**27. Pedersen.** *Tesis:* los mercados son lo bastante ineficientes para pagarles a los activos sus costos y su riesgo de liquidez, y no más. Explica las estrategias de hedge funds con entrevistas. *Lecciones:* (1) toda ganancia es el pago por un servicio: liquidez, riesgo o información; (2) preguntar quién está del otro lado (cap. 26); (3) la liquidez de mercado y la de fondeo se refuerzan en espiral. *Contra:* las primas concretas decayeron.

**28. Lo.** *Tesis:* la eficiencia cambia con el entorno; las estrategias nacen, se saturan y mueren como especies. *Lecciones:* (1) toda ventaja caduca, hay que vigilar su vida útil; (2) las primas dependen del régimen; (3) diversificar entre "ecologías". *Contra:* difícil de falsar.

**29. Cochrane.** *Tesis:* todo precio es p = E(mx). *Lecciones:* (1) toda anomalía es riesgo o precio equivocado: preguntar en qué estados del mundo paga mal; (2) los rendimientos esperados varían y la valuación los predice a plazos largos [42]; (3) dominar GMM y las pruebas de factores. *Contra:* es técnico, y a corto plazo el R² es bajo (Inferencia).

**E — Crisis y ciclos**

**30. Shiller.** *Tesis:* las burbujas son retroalimentación entre precio y narrativa; un CAPE alto anticipa rendimientos bajos a 10 años. La 2.ª edición advirtió de la burbuja inmobiliaria. *Lecciones:* (1) ante una valuación alta, bajar la expectativa de rendimiento; (2) identificar los amplificadores: medios, "nueva era", crédito; (3) la vivienda real rinde menos de 1% anual a largo plazo [31]. *Contra:* Fama: "consistently pessimistic" [31].

**31. Kindleberger.** *Tesis:* el patrón de Minsky: desplazamiento → auge con crédito → euforia → dificultad financiera → pánico, con el prestamista de última instancia como árbitro. La 8.ª edición agrega cripto y a la Fed como prestamista global [32]. *Lecciones:* (1) fechar la etapa por el crédito y no por el precio; (2) el fraude aparece al final; (3) el contagio viaja por los flujos. *Contra:* no da timing.

**32. Reinhart y Rogoff.** *Tesis:* los defaults, las crisis bancarias, la inflación y los colapsos cambiarios se repiten en todas partes. *Lecciones:* (1) "esta vez es distinto" es la frase de alarma; (2) deuda externa con tipo de cambio fijo es fragilidad; (3) la recuperación tras una crisis bancaria es larga. *Contra:* el error de Excel estaba en otro trabajo, *Growth in a Time of Debt* (2010): con deuda de más de 90% del PIB reportaron −0.1% de crecimiento, y corregido daba 2.2% [33].

**33. Dalio.** *Tesis:* aprender de los errores con reflexión escrita, decidir con transparencia radical y conocer los arquetipos de crisis de deuda (deflacionaria o inflacionaria). *Lecciones:* (1) registrar decisiones y principios; (2) ponderar opiniones por historial, como el Brier del comité; (3) diversificar entre flujos no correlacionados. *Contra:* *The Fund* (Copeland, nov-2023) describe una cultura de vigilancia, algo que Dalio niega [21]. Como reloj, sin señales fechadas (cap. 16).

**34. Soros.** *Tesis:* reflexividad: las percepciones sesgadas cambian los fundamentales (crédito ↔ colateral) y producen auges y quiebras. *Lecciones:* (1) buscar los circuitos que se refuerzan solos; (2) posición grande con tesis fuerte y salida rápida si falla; (3) asumir la propia falibilidad. *Contra:* poco falsable; el propio Soros: "I have a record of crying wolf" [18].

**F — Cuantitativo**

**35. López de Prado.** *Tesis:* la mayoría de los descubrimientos cuantitativos son falsos por sobreajuste y pruebas múltiples. *Causal Factor Investing* (2023) agrega que los factores son asociaciones sin causa probada [35]. *Lecciones:* (1) usar el Deflated Sharpe Ratio y la PBO; (2) validación cruzada purgada y con embargo; (3) registrar cuántas pruebas se corrieron. *Contra:* hay poca evidencia pública de alfa neto obtenido con estos métodos.

**36. Carver.** *Tesis:* pronósticos escalados y combinados, volatilidad objetivo, costos controlados, y la expectativa de que el Sharpe real sea menor que el del backtest. *Lecciones:* (1) dimensionar por volatilidad; (2) pronósticos continuos en vez de binarios; (3) un presupuesto de costos por rotación. *Contra:* pensado para futuros diversificados; no se replica a mano con MXN 20,000.

**37. Chan.** *Tesis:* un individuo puede operar estrategias cuantitativas simples (reversión, pares, momentum) con backtests honestos. *Lecciones:* (1) revisar el look-ahead, la supervivencia y los costos; (2) probar la cointegración antes de operar pares; (3) la capacidad define la estrategia. *Contra:* rotación alta, con resultados dentro de muestra.

**38. Zuckerman.** *Tesis:* Renaissance: científicos, datos limpios y miles de señales pequeñas. *Lecciones:* (1) muchas apuestas con ventaja leve; (2) investigación industrial y reproducible; (3) limitar la capacidad protege la ventaja. *Contra:* el fondo para externos (RIEF) quedó muy por debajo de Medallion [39]; no se puede replicar.

**G — Practicantes**

**39. Lefèvre.** *Tesis:* novela en clave sobre Livermore: leer la tendencia, esperar y dejar correr las ganancias [19]. *Lecciones:* (1) cortar pérdidas rápido; (2) no operar por tips; (3) el mismo apalancamiento que lo enriqueció lo quebró varias veces. *Contra:* no tiene estadística.

**40. Schwager.** *Tesis:* los traders excepcionales coinciden en control de riesgo, disciplina y un método ajustado a su personalidad. *Lecciones:* (1) riesgo por operación pequeño y fijo; (2) un método que calce con el horizonte propio; (3) reducir el tamaño en rachas perdedoras. *Contra:* supervivencia extrema, sin grupo de control.

## 4. Lo más reciente 2023-2026

| Fecha | Novedad | Qué cambia |
|---|---|---|
| 2023 | *Security Analysis*, 7.ª ed. (27-jun); Malkiel, 13.ª ed.; Kindleberger, 8.ª ed. con McCauley [2][27][32] | Ediciones vigentes |
| abr-2023 | Carver, *Advanced Futures Trading Strategies* [37] | Versión actual de su marco |
| 2023 | López de Prado, *Causal Factor Investing* [35] | Sobreajuste (tipo A) contra confusores (tipo B) |
| sep-2023 | Haghani y White, *The Missing Billionaires* (Wiley) [44] | Las fortunas se pierden por tamaño y gasto, no por selección |
| nov-2023 | Copeland, *The Fund* [21] | Contrapunto a Dalio |
| 28-nov-2023 | Muere Munger; Stripe Press reedita su *Almanack* [43] | — |
| 2023-2024 | Jensen-Kelly-Pedersen (la mayoría de los factores replica; cap. 02); McQuarrie, FAJ 2024 [28] | Factores: sí dentro de muestra; Siegel matizado |
| 2024 | *The Intelligent Investor*, 3.ª ed. revisada (Harper Business) [1]; Damodaran, 4.ª ed. y *The Corporate Life Cycle* [9] | Ediciones vigentes |
| 2024 | Mueren Kahneman (27-mar) y Simons [15][39] | — |
| 2024 | Estudio de cuatro fórmulas en EUA 1963-2022 [8] | Rinden por factores; ninguna domina |
| 2025 | Dalio, *How Countries Go Broke*; Housel, *The Art of Spending Money* [21][41] | — |
| 31-dic-2025 | Buffett deja de ser CEO; Abel firma la carta de 2025 (cap. 03) [46] | Las *Essays* quedan como corpus cerrado |
| mar-2026 | Yearbook 2026 de DMS (cap. 01) [29] | 35 mercados, 126 años |

**Haghani-Dewey (2016), base de *The Missing Billionaires*:** 61 participantes, US$25, moneda con 60% de cara, tope de US$250. El 28% quebró, el 21% llegó al tope, el pago promedio fue de US$91; Kelly indicaba 20% por tiro [12]. **Inferencia:** aun con la ventaja a la vista, el error dominante fue el tamaño.

## 5. Evidencia real: qué funciona, qué no, magnitudes

### 5.1 Tesis del canon contra evidencia independiente

| Tesis (fichas) | Evidencia y magnitud | Grado |
|---|---|---|
| El índice barato le gana a la mayoría (21, 22, 25) | SPIVA: 79% pierde en EUA (2025); 75.6% pierde en México a 10 años | **A** |
| Las acciones le ganan a los bonos a largo plazo (23, 24) | EUA 6.6% real en 1900-2025, pero hay periodos multidecenales de empate (McQuarrie) | **B** |
| Margen de seguridad y valor (9, 13, 14) | HML −57.8% (2006-2020); fórmula mágica 11.4% contra 8.7% | **B/C** |
| Calidad + valor + beta baja apalancados (11) | Sharpe ≈0.76-0.79; 2011-2025: 13.0% contra 14.1% | **A** mecanismo / **C** alfa futuro |
| Colas gruesas (4) | Hecho; la cobertura permanente se desangra (cap. 05) | **A** / **D** cobertura |
| Ciclos y crisis (30-34, 17) | Vivienda −35% y desempleo +7 pp tras crisis bancarias (cap. 16) | **B** descriptivo / **D** timing |
| Apalancamiento + iliquidez (20) | LTCM: de US$4.7 mil millones (inicio de 1998) a US$400 millones (25-sep-1998); apalancamiento efectivo de más de 250:1 | **A** |
| Los backtests se sobreajustan (35-37) | −26% fuera de muestra y −58% post-publicación | **A** |
| "Invierte en lo que conoces" (12) | Sesgo de familiaridad (Huberman 2001) | **D** |
| Modelo endowment (25) | Yale −24.6% en 2008; difícil de replicar | **C** |
| Reflexividad y mercados adaptativos (34, 28) | Poco falsables | **C** |

### 5.2 Qué envejeció bien y qué mal

- **Bien:** Bogle, Malkiel, Thorp, Poundstone, Lowenstein, Reinhart-Rogoff, Kindleberger, DMS, Cochrane, Tetlock, López de Prado (validación).
- **Mal:** Siegel ("siempre acciones"), el ~30% de Greenblatt, el priming de Kahneman, Swensen para individuos, Dalio como reloj, la regla de Lynch.
- **Inferencia:** envejecen mejor la aritmética, la historia y la validación; peor, los métodos de selección con backtest propio, porque publicarlos erosiona la ventaja.

## 6. Traducción operable

### 6.1 Ruta de lectura por nivel

| Nivel | Orden (número de ficha) | Para qué |
|---|---|---|
| 1. Licenciatura | 22 → 21 → 7 → 9a (*Intelligent Investor*) → 3 → 8 → 12 → 10 → 11 → 17a (*Most Important Thing*) → 20 → 38 → 6 | Indexar, margen de seguridad, cómo muere un fondo |
| 2. Maestría | 23 → 24 → 1 → 2 → 4 → 5 → 16 → 15 → 13 → 14 → 18 → 19 → 17b (*Market Cycle*) → 25 → 30 → 31 → 32 → 33 → 34 | Contrastar con datos; valuar, dimensionar, leer el ciclo |
| 3. Doctorado | 29 → 26 → 27 → 28 → 35 → 9b (*Security Analysis*, 7.ª) | Origen de las primas; validación |
| 4. Práctica | 36 → 37 → 39 → 40 | Sistema operable y psicología |

Satélites 2023-2026, cada uno después de su libro madre: *The Missing Billionaires* (19), *Causal Factor Investing* (35), *The Corporate Life Cycle* (15), *The Fund* (33), *Noise* (1), AFTS (36).

### 6.2 Reglas: del libro al parámetro

| # | Regla | Fichas | Parámetro |
|---|---|---|---|
| R1 | **Regla:** la supervivencia manda. Ninguna estrategia apalancada con sesgo negativo | 4, 7, 17, 20 | `drawdown_maximo_duro` 0.20 (arena −0.35); `bruto_max_fase_1` 1.0 |
| R2 | **Regla:** tamaño = mín(fracción × Kelly con la ventaja recortada 50%, tope de concentración) | 18, 19, 37 | `kelly.fraccion_max` 0.25 (arena 0.5); riesgo por operación 1% (arena 3%; 0.5% en prueba) |
| R3 | **Regla:** costos primero. Una idea satélite entra solo si su ventaja supera varias veces el costo de ida y vuelta (~0.58% en el SIC, cap. 15) | 21, 22, 25, 36 | `nucleo_min` 0.70 (estándar) |
| R4 | **Regla:** toda compra discrecional lleva valor conservador, escenario bajista y DCF inverso | 9, 13, 15, 16 | Plantilla de ficha-empresa |
| R5 | **Regla:** toda tesis con probabilidad y fecha, calificada con Brier | 1, 2, 3, 5 | `brier_objetivo` 0.20; `min_pronosticos_para_evaluar` 50 |
| R6 | **Regla:** ninguna estrategia se juzga por su resultado antes de tener muestra | 3, 5, 40 | 3 meses y 30 operaciones en papel; rachas: 3 pérdidas → ×0.5, 5 → pausa |
| R7 | **Regla:** backtest de ≥10 años con costos, DSR ≥ 0.95 y PBO ≤ 0.25; el Sharpe se recorta antes de dimensionar | 35-37 | `validacion_estrategias` |
| R8 | **Regla:** el termómetro de ciclo mueve la exposición táctica dentro de bandas, nunca a todo o nada | 17, 30-34 | Bandas de 5 pp y 25%; `satelite_max` 0.30 |
| R9 | **Regla:** ETFs apalancados solo con tendencia a favor y sin promediar a la baja | 36, 39, 40 | `filtro_apalancados` (MA200 y VIX < 25); `etf_apalancado_max` 0.5 |
| R10 | **Regla:** concentrar solo con ventaja documentada | 6, 10, 11 frente a 22, 24 | Acción individual ≤ 0.10 (arena 0.30); `sector_max` 0.25 |
| R11 | **Regla:** en 6 meses domina la suerte; la varianza es palanca de torneo, no sustituto de la ventaja | 5, 18, 19 | `modo_torneo` (±5 pp contra el mejor rival) |
| R12 | **Regla:** toda ventaja caduca; revisarla tras 5 pérdidas seguidas | 14, 18, 28 | `perdedoras_para_pausa` 5 |

### 6.3 Checklist del canon antes de operar (en papel o en real)

1. ¿Qué descuenta el precio y en qué difiero del consenso? (16, 17)
2. ¿Cuál es la tasa base? (1, 2, 5)
3. ¿Qué probabilidad y qué fecha le pongo? (2, 3)
4. ¿Cómo fracasaría? (3, 6)
5. ¿La pérdida máxima plausible cabe en el riesgo por operación? (4, 20)
6. ¿El tamaño sale de Kelly fraccional con la ventaja recortada? (18, 19)
7. ¿Quién está del otro lado? (13, 27)
8. ¿Algo me obligaría a vender en el peor momento? (20, 31)
9. ¿Sobrevive a los costos de GBM y al tipo de cambio? (22, 36)
10. ¿Qué evidencia me haría salir? (3, 39)

### 6.4 Cómo incorporar un libro nuevo

(a) Tesis como hipótesis falsable; (b) mejor evidencia independiente, con grado; (c) regla candidata; (d) parámetro que toca; (e) 3 meses en papel. Sin (b) y (e) no se vuelve regla.

## 7. Trampas y errores comunes

1. Leer a los ganadores como si fueran una muestra: los que quebraron no escribieron libro.
2. Tomar un backtest publicado como resultado fuera de muestra (el ~30% de Greenblatt).
3. Trasladar consejo institucional (Swensen, Carver, el float de Buffett) a MXN 20,000.
4. Usar a Taleb para justificar la compra permanente de puts.
5. Usar a Lefèvre o a Schwager para justificar piramidar con apalancamiento.
6. Usar a Dalio, Shiller o Marks como reloj.
7. Citar a Kahneman sin la fe de erratas del priming.
8. Confundir el error del paper de Reinhart-Rogoff de 2010 con el libro de 2009.
9. Leer ediciones viejas (ver §4).
10. Usar Kelly completo con una ventaja estimada: eso es sobreapostar.

## 8. Examen de titulación

1. **¿Cuál es la edición vigente de los dos libros de Graham?** *The Intelligent Investor*: 3.ª ed. revisada con Zweig (Harper Business, 2024), sobre la 4.ª de 1973. *Security Analysis*: 7.ª ed. (McGraw-Hill, 27-jun-2023, con Klarman).
2. **¿Qué pensaba Graham en los años 70 del análisis extenso?** Dudaba de que produjera selecciones lo bastante superiores para justificar su costo.
3. **Experimento de Haghani y Dewey.** 61 personas, US$25, 60% de cara, tope de US$250. El 28% quebró, el 21% llegó al tope, el pago promedio fue de US$91; Kelly indicaba 20% por tiro.
4. **¿Por qué Kelly fraccional?** Porque la ventaja se estima con error y el doble de Kelly baja el crecimiento a la tasa libre de riesgo. Un cuarto de Kelly da 43.75% del crecimiento máximo con 25% de la volatilidad (cap. 01).
5. **Cifras de LTCM.** Más de 25:1 (inicio de 1998); −US$4.6 mil millones en menos de 4 meses; recapitalización de US$3.625 mil millones con 14 instituciones.
6. **¿Qué no replicó de *Thinking, Fast and Slow*?** El capítulo de priming (R-index de 14), y Kahneman lo admitió.
7. **¿Qué logró el GJP?** Ganó las dos temporadas de IARPA-ACE con 35-72% más precisión que los otros equipos; sus mejores pronosticadores fueron ~30% mejores que analistas con información clasificada; todo medido con Brier.
8. **¿Qué encontró McQuarrie sobre Siegel?** Que en 1797-1942 acciones y bonos rindieron casi lo mismo, y que Siegel subestimó los bonos del siglo XIX en ~1.5 pp.
9. **¿Dónde estuvo el error de Reinhart-Rogoff?** En *Growth in a Time of Debt* (2010): con deuda de más de 90% del PIB, el −0.1% reportado era 2.2% corregido (Herndon-Ash-Pollin, 2013).
10. **¿Qué dice la evidencia independiente de la fórmula mágica?** 11.4% contra 8.7% en EUA 2003-2015, con rezago en 2007-2011; un estudio de 2024 la explica sobre todo por factores; el ~30% del libro era un backtest del autor.
11. **Medallion: cifras y por qué no se transfiere.** 66% bruto y 39% neto (1988-2018). RIEF quedó muy por debajo. Capacidad cerrada, horizonte corto e infraestructura imposible de copiar.
12. **¿Qué corrige el DSR y qué umbrales usa el sistema?** La selección entre muchas pruebas y la no normalidad (Bailey y López de Prado, 2014). Umbrales: DSR ≥ 0.95 y PBO ≤ 0.25.
13. **Lynch: rendimiento y crítica.** 29.2% contra 15.8% (1977-1990). Su regla coincide con el sesgo de familiaridad (Huberman 2001), y él tenía cientos de acciones y un equipo.
14. **Kindleberger: etapas y novedad de la 8.ª edición.** Desplazamiento → auge con crédito → euforia → dificultad → pánico. Agrega cripto y a la Fed como prestamista global.
15. **¿Por qué el grado es el mínimo entre evidencia y aplicabilidad?** Porque una verdad inaplicable a MXN 20,000 operados a mano en GBM (el float de Buffett, los ilíquidos de Swensen) no rinde en esta cuenta.

## 9. Fuentes

1. Wikipedia, *The Intelligent Investor*: https://en.wikipedia.org/wiki/The_Intelligent_Investor
2. Wikipedia, *Security Analysis*: https://en.wikipedia.org/wiki/Security_Analysis_(book)
3. Wikipedia, Philip Fisher: https://en.wikipedia.org/wiki/Common_Stocks_and_Uncommon_Profits
4. Open Library, *The Essays of Warren Buffett*: https://openlibrary.org/works/OL18072192W · https://openlibrary.org/works/OL20374816W
5. Wikipedia, *One Up on Wall Street* y Peter Lynch: https://en.wikipedia.org/wiki/One_Up_on_Wall_Street · https://en.wikipedia.org/wiki/Peter_Lynch
6. Wikipedia, Howard Marks: https://en.wikipedia.org/wiki/Howard_Marks_(investor)
7. Wikipedia, Seth Klarman: https://en.wikipedia.org/wiki/Seth_Klarman
8. Wikipedia, Joel Greenblatt y Magic formula investing: https://en.wikipedia.org/wiki/Joel_Greenblatt · https://en.wikipedia.org/wiki/Magic_formula_investing
9. Damodaran, libros: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm · https://openlibrary.org/works/OL21035837W
10. Wikipedia, Michael J. Mauboussin: https://en.wikipedia.org/wiki/Michael_J._Mauboussin · https://openlibrary.org/search?q=expectations+investing+mauboussin
11. Wikipedia, Edward O. Thorp: https://en.wikipedia.org/wiki/Edward_O._Thorp
12. Wikipedia, Kelly criterion: https://en.wikipedia.org/wiki/Kelly_criterion
13. Open Library, *Fortune's Formula*: https://openlibrary.org/search?q=fortune%27s+formula+poundstone
14. Wikipedia, *Fooled by Randomness* y *The Black Swan*: https://en.wikipedia.org/wiki/Fooled_by_Randomness · https://en.wikipedia.org/wiki/The_Black_Swan:_The_Impact_of_the_Highly_Improbable
15. Wikipedia, *Thinking, Fast and Slow* y Daniel Kahneman: https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow · https://en.wikipedia.org/wiki/Daniel_Kahneman
16. Wikipedia, Good Judgment Project: https://en.wikipedia.org/wiki/Good_Judgment_Project
17. Wikipedia, Annie Duke: https://en.wikipedia.org/wiki/Annie_Duke
18. Wikipedia, George Soros: https://en.wikipedia.org/wiki/George_Soros
19. Wikipedia, *Reminiscences of a Stock Operator*: https://en.wikipedia.org/wiki/Reminiscences_of_a_Stock_Operator
20. Wikipedia, Jack D. Schwager: https://en.wikipedia.org/wiki/Jack_D._Schwager
21. Wikipedia, Ray Dalio y *Principles*: https://en.wikipedia.org/wiki/Ray_Dalio · https://en.wikipedia.org/wiki/Principles_(Dalio_book)
22. Wiley, *Investing Amid Low Expected Returns* (abr-2022): https://www.wiley.com/en-us/Investing+Amid+Low+Expected+Returns%3A+Making+the+Most+When+Markets+Offer+the+Least-p-9781119860198
23. Wikipedia, Lasse Heje Pedersen: https://en.wikipedia.org/wiki/Lasse_Heje_Pedersen
24. Wikipedia, David F. Swensen: https://en.wikipedia.org/wiki/David_F._Swensen
25. Wikipedia, John C. Bogle: https://en.wikipedia.org/wiki/John_C._Bogle
26. Open Library, *Against the Gods*: https://openlibrary.org/search?q=against+the+gods+bernstein
27. Wikipedia, *A Random Walk Down Wall Street*: https://en.wikipedia.org/wiki/A_Random_Walk_Down_Wall_Street
28. Wikipedia, *Stocks for the Long Run*: https://en.wikipedia.org/wiki/Stocks_for_the_Long_Run · McQuarrie (2024), FAJ 80(1): https://www.tandfonline.com/doi/abs/10.1080/0015198X.2023.2268556
29. Princeton UP, *Triumph of the Optimists*: https://press.princeton.edu/books/hardcover/9780691091945/triumph-of-the-optimists · UBS Yearbook 2026: https://www.ubs.com/content/dam/assets/wm/static/cio/documents/giry2026-summary-public.pdf
30. Wikipedia, Andrew Lo y AMH: https://en.wikipedia.org/wiki/Andrew_Lo · https://en.wikipedia.org/wiki/Adaptive_market_hypothesis
31. Wikipedia, *Irrational Exuberance*: https://en.wikipedia.org/wiki/Irrational_Exuberance_(book)
32. Springer, *Manias, Panics, and Crashes*, 8.ª ed. (2023): https://www.springerprofessional.de/en/manias-panics-and-crashes/24098366
33. Wikipedia, *Growth in a Time of Debt*: https://en.wikipedia.org/wiki/Growth_in_a_Time_of_Debt · https://press.princeton.edu/books/paperback/9780691152646/this-time-is-different
34. Bailey y López de Prado (2014), "The Deflated Sharpe Ratio", JPM: https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf
35. López de Prado (2023), *Causal Factor Investing*: https://doi.org/10.1017/9781009397315
36. Open Library, *Advances in Financial Machine Learning*: https://openlibrary.org/search?q=advances+in+financial+machine+learning
37. Blog de Carver: https://qoppac.blogspot.com/
38. Open Library, *Quantitative Trading*, 2.ª ed.: https://openlibrary.org/works/OL25274055W
39. Wikipedia, Renaissance Technologies: https://en.wikipedia.org/wiki/Renaissance_Technologies
40. Wikipedia, *When Genius Failed* y LTCM: https://en.wikipedia.org/wiki/When_Genius_Failed · https://en.wikipedia.org/wiki/Long-Term_Capital_Management
41. Open Library, obras de Housel: https://openlibrary.org/search?q=morgan+housel
42. NBER w16972, Cochrane, "Discount Rates": https://www.nber.org/papers/w16972 · https://en.wikipedia.org/wiki/John_H._Cochrane
43. Wikipedia, *Poor Charlie's Almanack* y Charlie Munger: https://en.wikipedia.org/wiki/Poor_Charlie%27s_Almanack · https://en.wikipedia.org/wiki/Charlie_Munger
44. Wiley, *The Missing Billionaires* (sep-2023): https://www.wiley.com/en-us/The+Missing+Billionaires%3A+A+Guide+to+Better+Financial+Decisions-p-9781119747918
45. Huberman (2001), RFS 14(3): https://academic.oup.com/rfs/article-abstract/14/3/659/1578906
46. Berkshire Hathaway, carta de 2025: https://www.berkshirehathaway.com/letters/2025ltr.pdf
47. S&P DJI, SPIVA: https://www.spglobal.com/spdji/en/spiva/article/spiva-us/
48. Open Library, API: https://openlibrary.org/developers/api

**Registro de verificación (2026-09-25).** Sin WebSearch (cuota agotada): ~30 lecturas con WebFetch, ~60 extractos de Wikipedia y ~90 consultas a Open Library. **No verificado:** el número de la edición de 2019 de las *Essays* y si hay ediciones posteriores a la de Wiley de 2021; el título del artículo de Samuelson de 1979; el contenido del libro de Carver anunciado para dic-2026; la fecha exacta de la muerte de Simons.
