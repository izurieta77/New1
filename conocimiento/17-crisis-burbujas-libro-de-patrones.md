# 17 — Crisis y burbujas: libro de patrones

> Nivel: experto · Actualizado: 2026-09-25 · Grado de evidencia global: **B** (magnitudes y secuencias históricas: **A**; detección de burbujas por características: **B**; *timing* del techo: **C**)

Capítulos relacionados, que aquí no se repiten: [01 Fundamentos](01-licenciatura-fundamentos.md) · cap. 04 (renta fija y macro) · cap. 05 (derivados) · cap. 07 (riesgo y *backtesting*) · cap. 08 (conductuales y pronóstico) · cap. 11 (México) · cap. 12 (alternativos y cripto) · cap. 13 (estado del mercado) · [14 Análisis técnico que sobrevive](14-analisis-tecnico-que-sobrevive.md) · [15 Eventos corporativos](15-eventos-corporativos-y-situaciones-especiales.md) · [23 Geopolítica](23-geopolitica-y-riesgo-politico-global.md). Los parámetros salen de `config/parametros.json`.

**Convenciones.** Hecho = fecha y fuente. "Inferencia:" = razonamiento propio. "Regla:" = recomendación operable (solo en la sección 6). "(no verificado)" = cifra no confirmada en esta sesión. **"Cálculo propio"** = calculado el 25-sep-2026 con cierres diarios de Yahoo Finance (^GSPC, ^SP500TR, ^MXX, MXN=X, ^VIX, ^TNX, GC=F, TLT, EWW, BTC-USD, ^N225, ^IXIC, IGV, KRE, SLV, NVDA, ARKK, GME, CX) [45]. Son índices de precio salvo que diga TR (*total return*). El IPC de Yahoo es de precio y no incluye dividendos. El tipo de cambio de Yahoo es un cierre de mercado, no el FIX.

---

## 1. Objetivos de dominio

Al terminar este módulo el sistema debe poder:

1. Clasificar cualquier crisis en uno de **7 tipos** (sección 2.5) en menos de 2 horas. Cada tipo tiene profundidad, duración y refugios distintos.
2. Separar **burbuja** (precio que se desprende de los flujos, con probabilidad alta de *crash*) de **boom racional con incertidumbre** (Pástor-Veronesi), y saber que la diferencia casi nunca es observable *ex ante*.
3. Citar de memoria las cifras de Greenwood-Shleifer-You (GSY) y Goetzmann, y saber por qué **no** se contradicen.
4. Medir la fragilidad del sistema: apalancamiento, venta de volatilidad, descalce de liquidez y descalce cambiario. Esa es la variable que convierte una caída en crisis.
5. Saber qué activo protegió en cada crisis y **cuándo falló** (bonos en 2022, oro en 2020 y 2026, bitcoin casi siempre).
6. Pensar en **MXN**. Para un inversionista mexicano el dólar es la cobertura más confiable contra crisis globales, y el IPC en dólares es de los activos con peores recuperaciones del mundo.
7. Ejecutar el *playbook* de la sección 6 dentro de los límites de `parametros.json` sin improvisar en pánico.
8. Distinguir, en cada caso, lo que es dato dentro de muestra de lo que se sostiene fuera de muestra.

---

## 2. Núcleo teórico

### 2.1 La anatomía Kindleberger-Minsky

Kindleberger (con Aliber y, en la 8.ª edición de 2023, McCauley) describe la secuencia típica de una manía en cinco etapas [8][46]:

1. **Desplazamiento (*displacement*)**: un choque real crea oportunidades de ganancia verdaderas, como los ferrocarriles, internet, la desregulación, la IA o una tasa de interés muy baja.
2. **Boom con expansión del crédito**: el dinero fluye hacia la novedad y el crédito financia la compra.
3. **Euforia**: aparece "esta vez es distinto", se valúa por narrativa y entran compradores nuevos y apalancados.
4. **Dificultad financiera (*distress*)**: los *insiders* venden, sube el costo del dinero, llega un fraude o una quiebra "idiosincrática".
5. **Repulsión y pánico (*revulsion*)**: se vende lo que se puede, no lo que se quiere. Hacia el final entra un prestamista de última instancia.

Minsky (Levy WP 74, mayo de 1992) da el motor [7]. Hay tres tipos de unidades:

- **Cobertura (*hedge*)**: sus flujos pagan intereses y principal.
- **Especulativa**: sus flujos pagan intereses pero necesita refinanciar el principal.
- **Ponzi**: sus flujos no alcanzan ni para los intereses, así que depende de vender activos o pedir prestado.

**Primer teorema**: la economía tiene regímenes de financiamiento estables y otros inestables. **Segundo teorema**: "over periods of prolonged prosperity, the economy transits from financial relations that make for a stable system to financial relations that make for an unstable system". Minsky agrega que si en ese estado la autoridad combate la inflación con restricción monetaria, las unidades especulativas se vuelven Ponzi y el patrimonio de las Ponzi "se evapora".

**Inferencia operable:** la estabilidad prolongada, con volatilidad baja y *spreads* comprimidos, no es una señal de seguridad. Es la condición que fabrica el apalancamiento. Los episodios de 1929, 2008, LDI 2022 y SVB 2023 siguen exactamente el patrón "estabilidad → apalancamiento → apretón monetario → venta forzada".

### 2.2 Reinhart-Rogoff: "esta vez es distinto" y la resaca

- *This Time Is Different* (NBER w13882) cubre ocho siglos y todas las regiones. El incumplimiento soberano serial es "a nearly universal phenomenon" en la transición de emergente a desarrollado, y los *defaults* coinciden con inflación, colapsos cambiarios y crisis bancarias [6].
- *The Aftermath of Financial Crises* (AER P&P 2009; NBER w14656) mide lo que sigue a las crisis bancarias sistémicas [5][47]:

| Variable | Magnitud promedio | Duración |
|---|---|---|
| Precio real de la vivienda | −35% pico a valle | ~6 años |
| Precio de las acciones | **−55%** | ~3.5 años |
| Desempleo | +7 pp | más de 4 años |
| PIB | −9% | más corta que la del desempleo |
| Deuda pública real | **+86%** (episodios de la posguerra) | — |

La deuda pública explota sobre todo porque se desploman los ingresos fiscales, no por el costo de los rescates. **Grado A** para el orden de magnitud (replicado en múltiples bases). **Regla derivada:** si la crisis es bancaria y sistémica, el ancla de duración es de años, no de meses.

### 2.3 El diferenciador es el crédito

Jordà, Schularick y Taylor, "Leveraged Bubbles" (NBER w21486; 17 países, 140 años), concluyen que las burbujas no son todas iguales: "When fueled by credit booms, asset price bubbles increase financial crisis risks; upon collapse they tend to be followed by deeper recessions and slower recoveries". Las burbujas inmobiliarias financiadas con crédito son las más peligrosas [9]. **Grado A/B.**

**Inferencia:** el dot-com (acciones con poco crédito bancario) destruyó el Nasdaq pero la recesión fue leve. 2008 (vivienda y bancos apalancados) destruyó el sistema. La primera pregunta ante cualquier burbuja no es "¿qué tan cara está?". Es "¿quién está apalancado contra este activo y quién le prestó?".

### 2.4 Detección de burbujas: Fama contra GSY, Goetzmann y Pástor-Veronesi

**Fama** sostiene que las alzas fuertes no predicen rendimientos bajos. **GSY, "Bubbles for Fama" (JFE 2019)**, le dan la razón en promedio y le enmiendan la plana en lo importante. Las cifras siguientes son de la versión NBER w23191 [1]:

- **Muestra:** industrias de EUA de 1926 a 2014 (40 *run-ups*) y sectores internacionales de 1985 a 2014 como prueba fuera de muestra (107 *run-ups* en 31 países; 53 terminan en *crash* y 54 no).
- **Definición de *run-up*:** rendimiento de la industria de **100% o más en 2 años**, tanto bruto como neto del mercado (ponderado por valor), o 100% bruto en 5 años.
- **Definición de *crash*:** caída de **40% o más** desde cualquier punto en los 2 años siguientes.
- **Rendimientos:** después de un *run-up* son en promedio **cercanos a cero**, así que Fama tiene razón en la media. De los 40 episodios de EUA, 21 se desploman y 19 no. Los que se desploman rinden −5% a 1 año y **−42% a 2 años** (−29% neto de mercado). Los que no, **+21% a 1 año y +46% a 2 años**.
- **Probabilidad de *crash* según la magnitud del alza (EUA):** 20% con un alza de 50% neta de mercado, **53% con 100%** y **80% con 150%** (15 episodios). En los sectores internacionales: 36%, 50% y 67% (51 episodios). La probabilidad incondicional de *crash* en 2 años es de **14%** (11% después de 1970) en EUA y de **24%** en el extranjero.
- **Timing:** aun cuando el *crash* sí llega, el precio sigue subiendo en promedio **+30% durante unos 6 meses** después de identificar el *run-up* (el *crash* empieza en promedio 5 meses después). El caso extremo fue +107% en acciones de metales preciosos a fines de los setenta. Fama recuerda que Shiller "llamó" la burbuja en dic-1996 y los precios se duplicaron después.
- **Características que distinguen los *run-ups* que se desploman:** aumento de volatilidad, **aceleración** (lo abrupto del alza), emisión de acciones, alza del CAPE del mercado y mejor desempeño de las **empresas jóvenes** frente a las viejas (*age tilt*). El *turnover* está alto en ambos grupos y **no sirve**. El crecimiento de ventas (el fundamental) tampoco distingue en EUA. Después de corregir por *false discovery rate* al 10%, en EUA sobreviven la aceleración, el *age tilt* y el cambio en volatilidad como predictores del *crash*.
- **Estrategia:** vender todo *run-up* de 100% **pierde contra comprar y mantener unos 5 pp a 1 año** (47% de falsos positivos). Condicionando además en características y **pasando a instrumentos libres de riesgo, no al mercado**, se obtiene alrededor de **+10 pp a 2 años**. Con la volatilidad como filtro el rendimiento es de 7%, 8% y 17% a 1, 2 y 4 años, un *alpha* de 0, 8 y 12 pp, significativo solo a 4 años. Los propios autores advierten poco poder estadístico (40 observaciones) y cierto *look-ahead* en los umbrales.

**Goetzmann, "Bubble Investing: Learning from History" (NBER w21693; 42 mercados, 1900-2014)** [2]:

- De 3,514 años-mercado, 58 (**1.7%**) subieron más de 100% real en un año calendario. De esos, **6.9%** cayeron más de 50% al año siguiente (incondicional: 2.1%) y otro **6.9% volvió a duplicarse**. A 5 años, la probabilidad de caer 50% fue de **17.2%** (incondicional 8.5%) y la de volver a duplicarse de **22.4%** (incondicional 16.9%).
- Con la definición amplia (duplicarse en 3 años; 346 eventos, como EUA en 1928 o 1997), la probabilidad de *crash* al año siguiente es de 4.6% (incondicional 2%) y a 5 años de 9.8% (incondicional 8.4%). En su resumen: los *crashes* "gave back prior gains only 10 percent of the time".
- Después de un año de *crash* (−50%), la probabilidad de **duplicarse en los 5 años siguientes es de 32.8%**, contra 16.9% incondicional.

**Por qué GSY y Goetzmann no se contradicen:** Goetzmann mide **mercados completos** y *crashes* de −50%. GSY miden **industrias**, *crashes* de −40% y un umbral también neto de mercado. Las burbujas son un fenómeno sectorial: la concentración y la emisión ocurren en un tema, no en todo el país. **Regla implícita:** el termómetro de burbuja se aplica a sectores y temas, no al índice amplio.

**Pástor-Veronesi.** En "Was there a Nasdaq bubble in the late 1990s?" (JFE 2006; NBER w10581) muestran que el valor de una empresa **sube con la incertidumbre sobre su rentabilidad promedio**. Con la incertidumbre de fines de los noventa y una prima de riesgo baja, las valuaciones pico del Nasdaq eran racionalizables [4]. En "Technological Revolutions and Stock Prices" (AER 2009) las "burbujas" aparecen en equilibrio durante las revoluciones tecnológicas: el riesgo de la tecnología nueva pasa de idiosincrático a **sistemático** a medida que se adopta. Son burbujas "observables *ex post* pero impredecibles *ex ante*", más pronunciadas cuando la incertidumbre es alta y la adopción rápida, con evidencia en los ferrocarriles de 1830-1861 y en internet de 1992-2005 [3].

2025-2026: Hirano, Kishi y Toda (arXiv 2501.08215, v3 de ago-2026) modelan burbujas racionales sobre acciones que **sí pagan dividendos** durante tecnologías de propósito general como la IA. El crecimiento desbalanceado hace que los precios crezcan más rápido que los dividendos, y la burbuja puede financiar I+D [11]. Wang y Chen (arXiv 2606.01575, jun-2026; sin revisión de pares) aplican cinco pilares (valuación, SADF/GSADF, LPPL, *sentiment*/emisión y *payback* del capex) a la IA. Su conclusión: "a real technological revolution with localized bubble dynamics" [12]. **Grado C** para ambos: teoría y diagnóstico sin prueba fuera de muestra.

### 2.5 Taxonomía operable: 7 tipos de crisis

| Tipo | Mecanismo | Ejemplos | Profundidad típica (S&P) | Recuperación típica | Qué protege |
|---|---|---|---|---|---|
| **A. Burbuja de valuación con poco crédito** | Narrativa, emisión, empresas jóvenes | 2000, memes 2021, ARKK, software 2026 | Sector −70% a −90%; índice amplio −25% a −50% | Sector: años o nunca. Índice TR: ~6 años (2000) | Bonos del Tesoro, efectivo, valor |
| **B. Burbuja apalancada, bancaria o inmobiliaria** | Crédito, deuda, bancos, Minsky | 1929, 2008, Japón 1990, México 1994-95 | −50% a −86% | 4 a 25 años nominal | Tesoro largo si la crisis es deflacionaria, USD, efectivo |
| **C. Choque de liquidez o microestructura** | Venta forzada mecánica: *portfolio insurance*, ETPs de volatilidad, LDI, *carry*, liquidaciones | 1987, 2010, feb-2018, LDI 2022, ago-2024, oct-2025 cripto, plata ene-2026 | −10% a −34% en días | Semanas o meses si no toca la solvencia | Liquidez, no estar apalancado, órdenes límite |
| **D. Choque de tasas o inflación** | Correlación acciones-bonos positiva | 1973-74, bonos 1994, 2022 | −20% a −48%, con bonos cayendo al mismo tiempo | 1.5 a 7.5 años | Efectivo de corto plazo (CETES/*T-bills*), *commodities*, energía |
| **E. Choque exógeno o de política** | Pandemia, aranceles, guerra (cap. 23) | 2020, abr-2025, Irán 2026 | −9% a −34% | 2 a 6 meses si la política responde | USD (para MXN), Tesoro si no es inflacionario |
| **F. Crisis emergente, cambiaria o soberana** | Tipo de cambio fijo, deuda de corto plazo en USD, *sudden stop* | México 1982 y 1994, Asia 1997, Rusia 1998, euro 2011, CNY y CHF 2015 | Mercado local −50% a −80% en USD | Años. IPC en USD: 12.8 años (2013-2026) | USD y activos fuera del país |
| **G. Apalancamiento o fraude idiosincrático con contagio** | *Prime brokers*, contrapartes, custodia | LTCM, Archegos, Terra/FTX, SVB, crédito privado 2026 | Índice −3% a −19%; contagio sectorial −50% | Índice rápido; sector lento | Custodia segregada, diversificación de contraparte |

### 2.6 Los cinco amplificadores (lo que convierte una caída en crisis)

1. **Apalancamiento con llamadas de margen.** En 1929 se compraba con 10% de enganche [14]. LTCM tenía unos 30 dólares de deuda por cada dólar de capital [20]. Archegos usaba *total return swaps*. En octubre de 2025 hubo US$19 mil millones de liquidaciones en cripto [36].
2. **Estrategias que venden cuando baja (convexidad negativa).** El *portfolio insurance* de 1987, los ETPs inversos de VIX de 2018, los fondos LDI de 2022 y los *stops* automáticos de todos al mismo nivel.
3. **Descalce de liquidez.** Depósitos a la vista contra bonos largos (SVB), BDCs no cotizados con redenciones trimestrales contra préstamos ilíquidos (2026).
4. **Descalce cambiario.** Tesobonos en 1994, deuda de corto plazo en USD en Asia 1997, empresas mexicanas vendiendo opciones sobre el dólar en 2008 [43].
5. **Posiciones concentradas y *crowding*.** El *carry* en yenes de 2024 (unos ¥40 billones o US$250 mil millones según el BIS) [32], y la concentración del índice en IA en 2025-2026.

**Inferencia:** los amplificadores explican la **forma** de la caída, que es vertical y con rebote violento. El tipo explica la **duración**. Un choque tipo C sin daño de solvencia se recupera en semanas. Un tipo B con bancos dañados tarda años.

---

## 3. Literatura y fuentes canónicas

| Obra | Hallazgo cuantificado | Enlace | Grado |
|---|---|---|---|
| Kindleberger-Aliber-McCauley, *Manias, Panics, and Crashes* (8.ª ed., 2023) | Cinco etapas; el crédito y el prestamista de última instancia como ejes. Narrativo, sin estadística | [8] | B (marco) |
| Minsky (1992), WP 74 | Cobertura, especulativa y Ponzi; dos teoremas. Pruebas empíricas formales mixtas | [7] | B/C |
| Reinhart-Rogoff (2008, 2009) | Tras crisis bancarias: acciones −55% en ~3.5 años, vivienda −35% en ~6, desempleo +7 pp, deuda +86% | [5][6] | A |
| Jordà-Schularick-Taylor (2015) | Las burbujas con crédito provocan recesiones más profundas y recuperaciones más lentas (17 países, 140 años) | [9] | A/B |
| Greenwood-Shleifer-You (JFE 2019) | Alza de 100% en 2 años → rendimiento futuro ~0 pero P(*crash* ≥40%) = 53%; con 150%, 80%. Vender con características y pasar a libre de riesgo da ~+10 pp a 2 años | [1] | B (n chica, fuera de muestra internacional confirma) |
| Goetzmann (2016) | Duplicarse en 1 año → P(−50% al año siguiente) = 6.9% contra 2.1%; a 5 años 17.2% contra 8.5%. Tras un *crash*, P(duplicarse en 5 años) = 32.8% | [2] | B |
| Pástor-Veronesi (2006, 2009) | La incertidumbre sobre la rentabilidad justifica valuaciones altas; las "burbujas" tecnológicas son racionales y solo se ven *ex post* | [3][4] | B |
| Goetzmann-Kim-Shiller, *Crash Beliefs* (NBER w22143) | 26 años de encuestas: los inversionistas **sobreestiman** la probabilidad de un *crash*; el sesgo depende de las noticias recientes (disponibilidad) y reduce los flujos a fondos | [10] | B |
| Yardeni, tablas *bull/bear* | Fechas y magnitudes oficiales de mercados bajistas y correcciones del S&P desde 1928 | [13] | A (dato) |
| BIS Bulletin 90 y 95 (2024) | *Carry* de ~¥40 billones; el pico del VIX del 5-ago-2024 se debió sobre todo a cotizaciones y *spreads* de opciones, no a ETFs | [32] | B |
| Chicago Fed Letter 480 (2023) | LDI: el bono de 30 años del Reino Unido subió +200 pb (fin de ago al 27-sep-2022); el BoE compró £19.3 mil millones | [29] | A (dato) |
| Fed OIG (2023), SVB | La supervisión no creció con el banco ni examinó el riesgo de tasa | [31] | A (dato) |
| Hirano-Kishi-Toda (2025/26) | Burbujas racionales en tecnologías de propósito general | [11] | C |
| Wang-Chen (2026) | La IA como revolución real con burbujas locales | [12] | C/D |

---

## 4. Lo más reciente, 2023-2026

**2023: SVB.** El 9-mar se retiraron **US$42 mil millones** y había **US$100 mil millones** en cola para el día siguiente (Barr, Fed) [31]. El KBW Bank Index cayó hasta 8.7% intradía el 9-mar. El S&P solo perdió −3.4% (8 al 13-mar, cálculo propio), mientras que el ETF KRE de bancos regionales acumuló **−54.2%** de ene-2022 a may-2023 y no ha recuperado (cálculo propio). En la ventana el oro subió +5.4% y bitcoin +11.4%. Lección: las corridas bancarias hoy duran horas, y el índice amplio puede ignorar una crisis sectorial muy profunda.

**Agosto de 2024: *unwind* del *carry* en yenes (tipo C).** El 5-ago el Nikkei cayó **−12.4%** (4,451 puntos, su peor día desde 1987) y al día siguiente rebotó **+10.2%** (cálculo propio). El VIX tocó alrededor de **66 en *pre-market*** (BIS 90), su mayor salto de un día. El BIS 95 lo atribuye a la ampliación de *spreads* en las cotizaciones de *puts*, porque el VIX se calcula con cotizaciones y no con operaciones. El S&P perdió −8.5% (16-jul al 5-ago) y recuperó el máximo el 19-sep, 45 días después del mínimo [32][33].

**Enero de 2025: DeepSeek.** Nvidia cayó −17% en un día (**−US$589 mil millones**, la mayor pérdida de valor de una empresa en la historia de EUA), el Nasdaq −3.07% y el S&P apenas −1.46% [34]. De máximo a mínimo Nvidia perdió −36.9% (6-ene al 4-abr-2025) y recuperó el 25-jun-2025 (cálculo propio).

**Abril de 2025: choque arancelario (tipo E, detalle en el cap. 23).** El S&P perdió **−18.9%** (19-feb al 8-abr, cierre 4,982.77), con −4.84% el 3-abr y −5.97% el 4-abr. El 9-abr subió **+9.52%** con la pausa. El VIX cerró en 52.33 el 8-abr y el S&P marcó récord el **27-jun-2025**, 80 días después del mínimo (cálculo propio; CNN [35]). **En MXN el S&P TR cayó −20.1% y no recuperó hasta el 27-oct-2025**, porque el peso se apreció (cálculo propio).

**Octubre de 2025: la mayor liquidación de la historia cripto.** El 10 y 11 de octubre, tras el anuncio de un arancel de 100% a China, se liquidaron **US$19 mil millones** en unas 24 horas y el *open interest* de perpetuos cayó 43%, de US$217 mil millones a US$123 mil millones [36]. Bitcoin pasó de un cierre máximo de 124,753 (6-oct-2025) a **58,559 (30-jun-2026), −53.1%**. Hoy está en alrededor de 84,179 (cálculo propio).

**Enero de 2026: *crash* de metales.** El 30-ene la plata cayó **−31.4%** en futuros (US$78.53), su peor día desde marzo de 1980, con −36% intradía. El oro perdió más de 12% intradía y perforó US$5,000. El detonante fue la nominación de Kevin Warsh a la Fed, que alivió el miedo a una Fed sin independencia y fortaleció el dólar [37]. El ETF SLV cayó −28.5% ese día y −52.3% del 28-ene al 16-jul. El oro (GC=F) cayó **−24.9%** del 29-ene al 16-jul (cálculo propio). Lección: un "refugio" comprado con *momentum* y apalancamiento se comporta como un activo de riesgo.

**Febrero de 2026: "SaaSpocalypse" (tipo A inverso: disrupción).** El lanzamiento de agentes de IA (Claude Cowork y Opus 4.6, según fuentes secundarias) llevó al mercado a revaluar el modelo de cobro por usuario del software (Bloomberg, 4-feb-2026) [38]. El ETF IGV perdió **−36.6%** (22-sep-2025 al 10-abr-2026) y no ha recuperado (cálculo propio). La cifra de "US$285 mil millones en 48 horas" viene de fuentes secundarias (no verificado en fuente primaria).

**Primer trimestre de 2026: crédito privado (tipo G).** Hubo cargos por fraude en Tricolor (dic-2025) y First Brands (ene-2026) [39]. Las solicitudes de redención en los 12 mayores BDCs no cotizados promediaron **12.1%** en el 1T-2026, contra compuertas de 5% (With Intelligence; cifra de fuente secundaria). Blue Owl limitó las redenciones a 5% (CNBC, 2-abr-2026). Lección: los vehículos "semilíquidos" son líquidos solo cuando nadie quiere salir.

**Febrero y marzo de 2026: guerra de Irán (tipo E/B, cap. 23).** El S&P perdió −9.1% entre cierres (27-ene: 6,978.60; 30-mar: 6,343.72; el cap. 23 reporta 6,316.91 y −9.8% con otra fuente o dato intradía) y marcó récord el 15-abr. El VIX cerró como máximo en 31.05 (27-mar). En la ventana el oro perdió −11.0% y bitcoin −25.2% (cálculo propio). La Fed **subió** la tasa el 16-sep-2026 (cap. 23). El S&P volvió a récords en agosto (CNN, 4-ago-2026) [40] y cerró en 7,704 el 24-sep.

**México en 2026.** El IPC está en **corrección de −11.5%**: del máximo de 71,601 (11-feb) a 63,376 (18-sep). En USD perdió −13.9% al mínimo del 23-mar y está en −11.5% hoy (cálculo propio). La causa no se atribuyó en esta sesión (ver cap. 11 y 13).

**Bonos largos.** El TLT (precio) está **−53.7% debajo de su máximo de ago-2020** y no ha recuperado en más de 6 años (cálculo propio; el *total return* es menos negativo por los cupones). Es el mercado bajista de "activo seguro" más largo de la era moderna. **Inferencia:** el tipo D sigue vivo.

**Debate IA 2026.** El marco académico dominante es Pástor-Veronesi y Hirano-Kishi-Toda (revolución real con burbujas locales), no "1999 otra vez" [3][11][12]. Por el termómetro GSY, la pregunta útil no es si la IA "es burbuja". Es **qué subsector cumple hoy alza de 100% o más en 2 años con aceleración, emisión, empresas jóvenes al alza y volatilidad creciente** (sección 6.1).

---

## 5. Evidencia real: casos, magnitudes y refugios

### 5.1 Fichas de casos globales

Formato: **Causa** · **Señales previas** · **Caída máxima y duración** · **Qué protegió** · **Recuperación** · **Lección operable**.

**1929-1932 (tipo B).** *Causa:* compra con margen (enganche de 10%), préstamos de corredores y una Fed que apretó (tasa de descuento de Nueva York en 6% en ago-1929) [14]. *Señales:* margen récord, manía, apretón monetario. *Caída:* Dow −89% (381.17 el 3-sep-1929 a 41.22 el 8-jul-1932). S&P −86.2% (7-sep-1929 a 1-jun-1932) [13]. Lunes y martes negros (28 y 29 de octubre): −12.9% y −10.2% en el S&P (cálculo propio). *Protegió:* el efectivo y los bonos de alta calidad, porque hubo deflación (el IPC de EUA de fines de 1936 estaba más de 18% debajo del de 1929, Hulbert) [15]. *Recuperación:* récord nominal del S&P el 22-sep-1954 (25 años). Con dividendos y deflación, el punto de equilibrio llegó a fines de 1936 [15], pero en 1937-38 hubo otro −54.5% (Yardeni). *Lección:* apalancamiento más apretón monetario igual a tipo B. Hay que medir siempre en términos reales y totales, nunca con el índice de precio nominal.

**1973-1974 (tipo D).** *Causa:* fin de Bretton Woods, choque petrolero de 1973 e inflación de 3.4% (1972) a 12.3% (1974) [16]. *Caída:* S&P −48.2% (11-ene-1973 a 3-oct-1974, 630 días) [13]. G7 −43% en términos reales y FT30 del Reino Unido **−73%** [16]. *Protegió:* efectivo a tasas cortas altas, energía y materias primas (inferencia coherente con el mecanismo; no se midió). *Recuperación:* récord nominal del S&P el 17-jul-1980 (~7.5 años). *Lección:* en un choque de inflación la cartera 60/40 no diversifica. Hay que medir duración y exposición a inflación, no solo beta.

**1987, lunes negro (tipo C).** *Causa:* el *portfolio insurance* (venta programada de futuros al bajar) y el arbitraje de índices amplificaron una caída que empezó por tasas al alza, dólar débil y déficit comercial. La Comisión Brady los señaló como amplificadores, no como origen [17]. *Caída:* S&P **−20.47%** el 19-oct (cálculo propio) y Dow −22.6%. De máximo a mínimo **−33.5%** (25-ago al 4-dic, 101 días). Hong Kong −45.8%, Australia −41.8% y Reino Unido −26.4% entre el 19 y el 26-oct. *Protegió:* los bonos, solo durante días. En la ventana ago-dic el bono a 10 años terminó más alto (8.73% a 8.94%, cálculo propio). *Recuperación:* récord el 26-jul-1989 (23 meses). *Lección:* si todos tienen la misma "cobertura" dinámica, esa cobertura es el riesgo. Un *stop* no es un *put*.

**1994: masacre de bonos (tipo D).** *Causa:* la Fed subió la tasa de 3% a 6% en unos 12 meses. El 10 años subió alrededor de 240 pb (de ~5.4% a ~7.8%) y las pérdidas contables se estimaron en más de US$1.5 billones. Orange County quebró con bonos largos financiados con reportos [18]. *Caída:* el S&P no llegó a −10% (Yardeni no registra corrección). El daño fue en duración. *Lección:* la duración apalancada más una sorpresa de la Fed es suficiente para una crisis. Además fue el contexto externo del Tequila (inferencia).

**1997, crisis asiática (tipo F).** *Causa:* tipos de cambio fijos más deuda de corto plazo en dólares. Tailandia dejó flotar el baht el 2-jul-1997. De julio de 1997 a enero de 1998 cayeron THB −56%, PHP −41%, MYR −46% e **IDR −81%**. El won coreano cayó 55% hasta su mínimo de diciembre, con paquetes del FMI [19]. *Caída:* S&P −10.8% (7 al 27-oct-1997), con récord el 5-dic. IPC **−13.34% el 27-oct-1997**, su peor día en la muestra (cálculo propio). *Lección:* el contagio no respeta fundamentales. México cayó sin tener el mismo problema.

**1998, Rusia y LTCM (tipos F y G).** *Causa:* Rusia devaluó y dejó de pagar en agosto. LTCM, con unos 30 a 1 de apalancamiento, perdió 44% en agosto y **US$4.6 mil millones** en menos de 4 meses. El 23-sep, 14 instituciones invirtieron **US$3.625 mil millones** por 90% del fondo, con la Fed de Nueva York como facilitadora y sin fondos públicos [20]. *Caída:* S&P −19.3% (17-jul al 31-ago). En la misma ventana el IPC cayó −36.0% y el EWW −43.7%. *Protegió:* el Tesoro (10 años de 5.50% a 5.03%). *Recuperación:* S&P el 23-nov-1998 (84 días desde el mínimo). IPC: −46.8% (21-oct-1997 a 10-sep-1998), recuperado el 15-abr-1999 (cálculo propio). *Lección:* el *arbitraje de convergencia* equivale a vender liquidez. En la crisis las correlaciones se van a 1 y el tamaño contra la liquidez del mercado mata.

**2000-2002, dot-com (tipo A).** *Causa:* valuaciones de internet, ola de IPOs y empresas jóvenes. GSY identifican *run-ups* en software, hardware y equipo eléctrico [1]. *Caída:* Nasdaq **−77.9%** (5,048.62 el 10-mar-2000 a 1,114.11 el 9-oct-2002). S&P −49.1% (929 días) [13][21]. *Protegió:* el Tesoro (10 años de 6.17% a 3.58%). El IPC cayó −28.8% en la ventana, bastante menos que el Nasdaq. *Recuperación:* S&P de precio 30-may-2007 (7.2 años), S&P TR 23-oct-2006 y **Nasdaq 23-abr-2015 (15 años)** (cálculo propio). *Lección:* en una burbuja de valuación sin crédito, el daño se concentra en el tema. Un índice concentrado en el tema puede tardar 15 años.

**2007-2009, crisis financiera global (tipo B).** *Causa:* vivienda y crédito, bancos apalancados (Jordà-Schularick-Taylor [9]; Reinhart-Rogoff [5]). *Caída:* S&P **−56.8%** (9-oct-2007 a 9-mar-2009, 517 días). VIX en cierre récord de la época de 80.86 (20-nov-2008) (cálculo propio). *Protegió:* oro +24.5%, TLT +17.7% y **USD/MXN +43.5%** (de 9.87 a 15.53). *Recuperación:* S&P de precio 28-mar-2013 (5.5 años) y TR 2-abr-2012. *Lección:* es el tipo B por excelencia. La magnitud de Reinhart-Rogoff se cumplió (−55% en acciones), aunque la caída del S&P duró ~1.4 años y no ~3.5. La cobertura en USD era la clave para un mexicano.

**2010, *flash crash* (tipo C).** *Causa:* el 6-may, a las 2:32 p.m. ET, durante unos 36 minutos, el Dow perdió 998.5 puntos (~9%) y se borró más de US$1 billón. SEC y CFTC atribuyen el inicio a una gran orden de venta de E-mini (Waddell & Reed), amplificada por la retirada de liquidez del HFT [22]. El S&P cerró −3.24% ese día. La corrección por Grecia fue de −16.0% (23-abr al 2-jul) y se recuperó el 4-nov-2010 (cálculo propio). *Lección:* las órdenes de mercado y los *stops* a mercado se ejecutan a precios absurdos. Hay que operar con órdenes límite.

**2011, euro y rebaja de EUA (tipos F y E).** *Causa:* contagio soberano a España e Italia y rebaja de EUA de AAA a AA+ por S&P (5 y 6 de agosto) [23]. *Caída:* S&P −6.66% el 8-ago y −19.4% en cierres (29-abr al 3-oct). *Protegió:* paradójicamente el **Tesoro rebajado**: TLT +31.9% y 10 años de 3.30% a 1.78%. También el oro (+6.4%) y el CHF. El peso se depreció fuerte (USD/MXN +22.2%). *Recuperación:* 24-feb-2012 (cálculo propio). *Lección:* el refugio lo define la liquidez en dólares, no la calificación. El peso es moneda de riesgo.

**2015: franco suizo y yuan (tipos C y F).** El 15-ene el SNB eliminó el piso de 1.20 EUR/CHF y el franco saltó entre 20% y 30% en minutos. Los clientes de FXCM quedaron con **US$225 millones** en saldos negativos y la casa necesitó unos US$300 millones de rescate [24]. El 11-ago China devaluó el fijo del yuan **1.9%**, el mayor ajuste en dos décadas. El 24-ago el Dow abrió −1,089 puntos y cerró −588, con el S&P en −3.94% [25]. Corrección del S&P: −12.4% (21-may al 25-ago-2015). Máximo a mínimo: −14.2% (21-may-2015 a 11-feb-2016), recuperado el 11-jul-2016. USD/MXN +25.7% en la ventana (cálculo propio). *Lección:* un piso o un tipo de cambio fijo es una opción vendida por el banco central, con riesgo de salto. El apalancamiento en divisas de un *broker* minorista puede dejar saldo negativo.

**Febrero de 2018, *Volmageddon* (tipo C).** El 5-feb el VIX pasó de 17.31 a 37.32 (**+116%**). XIV cayó −96% (de US$1.9 mil millones a US$63 millones) y SVXY −91%. Credit Suisse terminó XIV (último día el 15-feb). El rebalanceo diario obligaba a los productos a comprar futuros de VIX al cierre [26]. S&P −4.10% ese día y −10.2% (26-ene al 8-feb), recuperado el 24-ago. *No protegieron:* el TLT (−4.0%) y el oro (−2.6%), porque las tasas subían (cálculo propio). *Lección:* nunca tener un producto cuyo diseño lo obliga a comprar al cierre lo que está vendiendo.

**2020, COVID (tipo E).** S&P **−33.9% en 33 días** (19-feb al 23-mar). El 16-mar cayó −11.98% y el VIX cerró en **82.69**, su récord histórico (cálculo propio). *Protegió:* TLT +14.1% y **USD/MXN +33.1%** (de 18.54 a 25.34). **No protegieron** el oro (−2.5%, por liquidación) ni bitcoin (−33.4%). *Recuperación:* 18-ago-2020 (148 días desde el mínimo). **El S&P TR en MXN solo cayó −17.2% y recuperó el 26-mar-2020** (cálculo propio). *Lección:* el mercado bajista más rápido tuvo la recuperación más rápida cuando la política respondió. Rebalancear en pánico pagó.

**2021: memes y Archegos (tipos A y G).** Melvin Capital perdió **−53%** en enero por GameStop, y Citadel y Point72 le inyectaron cerca de US$3 mil millones [27]. GME cayó −88.5% (27-ene-2021 a abr-2024) y ARKK −81.1% (12-feb-2021 a 28-dic-2022); ninguno ha recuperado (cálculo propio). Archegos dejó pérdidas bancarias de **más de US$10 mil millones**: Credit Suisse US$5.5 mil millones, Nomura unos 2 mil millones, Morgan Stanley cerca de 1 mil millones y UBS 774 millones, con exposiciones escondidas en *swaps* [28]. *Lección:* la concentración apalancada detrás de derivados no aparece en los reportes de tenencias. Las posiciones cortas muy concentradas pueden sufrir un *squeeze*.

**2022: tasas, LDI y cripto (tipos D, C y G).** S&P −25.4% (3-ene al 12-oct, 282 días), recuperado el 19-ene-2024. Nasdaq −36.4%. *No protegieron:* TLT **−30.5%** (10 años de 1.63% a 3.90%), oro −6.8% y bitcoin −58.8%. El peso se **apreció** (USD/MXN −2.0%), así que el S&P TR en MXN cayó más: **−28.9%** (29-nov-2021 a 9-mar-2023), recuperado el 10-jun-2024 (cálculo propio). *LDI del Reino Unido:* el mini-presupuesto del 23-sep dejó £45 mil millones en recortes de impuestos sin financiar. El bono de 30 años subió **+200 pb** desde fin de agosto hasta el 27-sep y la libra tocó 1.03, mínimo histórico. El BoE compró **£19.3 mil millones** del 28-sep al 14-oct [29]. *Cripto:* UST (Terra) perdió la paridad en mayo, con unos US$40 mil millones destruidos. FTX se acogió al Capítulo 11 el 11-nov con un faltante de unos US$8 mil millones [30]. BTC cayó −76.6% (67,567 a 15,787) y recuperó el 4-mar-2024. *Lección:* cuando el problema es la inflación, los bonos no cubren. La cripto es un activo de riesgo apalancado. El riesgo de contraparte del *exchange* es real.

**2023 SVB, 2024 *carry*, 2025 DeepSeek y aranceles, 2026:** ver la sección 4.

### 5.2 Fichas de México

**1982: deuda, devaluación y nacionalización bancaria (tipo F).** Devaluación a inicios de 1982, moratoria de agosto de 1982 sobre una deuda de unos **US$80 mil millones**, y nacionalización bancaria con control de cambios el 1-sep-1982 [42]. La magnitud de la caída bursátil no se verificó. *Lección:* en un país emergente el riesgo político y de expropiación domina a la valuación. Los "dólares" dentro del sistema local no son dólares seguros cuando hay control de cambios (inferencia).

**1987, México.** La BMV tuvo un auge y un desplome alrededor de octubre de 1987 (magnitud no verificada; no hay datos diarios del IPC antes de nov-1991 en la fuente usada).

**1994-1995, Tequila (tipo F).** *Causa:* déficit externo, banda cambiaria y deuda de corto plazo ligada al dólar (los tesobonos pasaron de US$1.8 mil millones en 1993 a US$16.1 mil millones en 1994), en un año de choques políticos y con la Fed subiendo tasas. *Detonante:* devaluación de ~15% el 20-dic-1994 y flotación el 22-dic. El peso pasó de ~3.4 a **7.2 por dólar** en marzo de 1995 [41]. *Caída:* IPC **−49.4% en pesos** (8-feb-1994 a 27-feb-1995; cálculo propio). En USD, del orden de −70% (inferencia aritmética con el tipo de cambio; no verificado con serie diaria). PIB −6.2% en 1995, inflación de 52% y desempleo de 3.9% a 7.4%. *Rescate:* unos US$50 mil millones (EUA 20, FMI 17.8, BIS 10), pagado antes de tiempo y con ganancia para EUA de unos US$600 millones [41]. *Recuperación:* IPC nominal el 2-ene-1996, aunque en términos reales tardó mucho más por la inflación de 52% (inferencia). *Lección:* para un mexicano la cobertura es tener activos en USD **fuera** del sistema local. Un "máximo nominal" del IPC con inflación alta es una ilusión.

**2008 (tipo B importado más descalce cambiario).** IPC **−48.6%** (18-oct-2007 a 27-oct-2008), recuperado el 7-ene-2010. **En USD −64.8%** (30-may-2008 a 9-mar-2009), recuperado el 3-ene-2011. USD/MXN de 9.87 (4-ago-2008) a 15.53 (9-mar-2009), **+57%** (cálculo propio). El FMI estima pérdidas por derivados exóticos de las empresas mexicanas del orden de **US$5 mil millones** [43]. Comercial Mexicana entró a concurso mercantil tras sus pérdidas en derivados cambiarios (fecha y monto no verificados). Cemex llegó a la crisis con deuda de unos US$14 mil millones por la compra de Rinker (oferta de US$14.2 mil millones en 2007) y vendió Australia a Holcim por A$2.2 mil millones en jun-2009 [44]. El ADR CX cayó **−90%** (31.02 el 15-jun-2007 a 3.05 el 9-mar-2009), llegó a 1.63 en mar-2020 y hoy está en ~9.5 (cálculo propio): nunca recuperó. *Lección:* vender opciones sobre el dólar para "ganar el *carry*" es venta de volatilidad escondida. Una adquisición grande con deuda en el pico del ciclo puede destruir el capital de una empresa de forma permanente.

**2016, elección en EUA (tipo E).** El 9-nov el USD/MXN subió **+8.65%** en un día, de 18.55 (7-nov) a 20.74 (11-nov), con máximo de **21.92 el 19-ene-2017**. El IPC perdió −6.4% entre el 7 y el 11-nov (cálculo propio). *Lección:* el peso es el vehículo líquido con el que el mundo cubre el riesgo de México y de los emergentes. El golpe llega primero al tipo de cambio.

**2020, COVID en México.** USD/MXN de 18.54 (17-feb) a 25.34 (24-mar), +36.6%. El IPC ya venía de un máximo de 51,713 (25-jul-2017) y tocó **32,964 (23-mar-2020), −36.3%**. Recuperó el 18-ago-2021. En USD el IPC perdió **−63.9%** (11-abr-2013 a 23-mar-2020) y **recuperó hasta el 12-ene-2026, 12.8 años** (cálculo propio). El EWW (precio) tuvo el mismo patrón: −67.3% y recuperación el 27-ene-2026.

**2024: elección y reforma judicial (tipo F doméstico).** El 3-jun, tras la elección del 2-jun, el IPC perdió **−6.1%** en un día. El USD/MXN pasó de 17.01 (31-may) a 18.75 (13-jun), y de 16.31 (9-abr) a **20.65 (27-nov), +26.6%**. El IPC cayó −16.8% (7-feb a 30-dic-2024) y recuperó el 28-may-2025 (cálculo propio). *Lección:* el riesgo institucional doméstico se transmite por el peso y los bancos. Las posiciones en USD amortiguaron la caída.

### 5.3 Matriz de refugios por episodio (cálculo propio, del máximo al mínimo del S&P)

| Episodio | S&P | IPC (MXN) | Oro | TLT (precio) | USD/MXN | BTC | VIX máx. (cierre) |
|---|---|---|---|---|---|---|---|
| GFC 2007-09 | −56.8% | −46.7% | **+24.5%** | **+17.7%** | **+43.5%** | — | 80.9 |
| 2011 | −19.4% | −10.4% | +6.4% | **+31.9%** | **+22.2%** | — | 48.0 |
| 2015-16 | −14.2% | −6.1% | +3.6% | +11.1% | **+25.7%** | +61.3% | 40.7 |
| Feb-2018 | −10.2% | −6.3% | −2.6% | −4.0% | +2.1% | −26.0% | 37.3 |
| 4T-2018 | −19.8% | −16.4% | +5.1% | +3.6% | +6.2% | −37.4% | 36.1 |
| COVID 2020 | −33.9% | −26.6% | −2.5% | **+14.1%** | **+33.1%** | −33.4% | 82.7 |
| 2022 | −25.4% | −13.7% | −6.8% | **−30.5%** | −2.0% | −58.8% | 36.5 |
| Ago-2024 | −8.5% | −4.8% | −0.9% | +4.9% | **+10.2%** | −17.1% | 38.6 |
| Abr-2025 | −18.9% | −7.0% | +1.8% | +0.2% | +2.3% | −21.1% | 52.3 |
| Irán 2026 | −9.1% | −2.6% | **−11.0%** | −1.2% | +4.5% | −25.2% | 31.0 |

Lectura (**grado B**: n chica, ventanas elegidas *ex post* sobre el S&P):
- **USD/MXN**: sube en 9 de 10 episodios. La excepción es 2022, un choque de tasas con el peso apoyado en el *carry*. **Es la mejor cobertura para una cuenta en pesos.**
- **Tesoro largo**: cubre en crisis deflacionarias o de demanda (2008, 2011, 2020). **Falla** en choques de inflación o tasas (2018, 2022, 2026).
- **Oro**: cubre en 2008 y 2011. Falla en la liquidación de 2020, en 2022 y en 2026.
- **Bitcoin**: cayó más que el S&P en 6 de 8 episodios con datos, casi igual en COVID (−33.4% contra −33.9%) y solo subió en 2015-16. **No es cobertura.**
- **El IPC en pesos cae menos que el S&P en dólares** en los 10 episodios (ventanas del S&P). **Inferencia:** parte de eso es que el peso se deprecia (el IPC en USD cae más) y parte es la menor beta del IPC.

### 5.4 La lente MXN (cálculo propio, S&P 500 TR convertido a pesos)

| Episodio | S&P TR en USD | S&P TR en MXN | Recuperación en MXN |
|---|---|---|---|
| GFC | −55.3% | **−36.6%** (9-oct-2007 a 6-mar-2009) | 7-feb-2011 |
| 2018 | −19.4% | −18.3% | 2-jul-2019 |
| COVID | −33.8% | **−17.2%** | **26-mar-2020** |
| 2022 | −24.5% | **−28.9%** | 10-jun-2024 |
| 2025 | −18.7% | **−20.1%** | 27-oct-2025 |

**Conclusión (grado B, 5 episodios):** el dólar reduce la caída en los tipos B, C, E y F, que son crisis globales de aversión al riesgo. **La amplifica** cuando el choque fortalece al peso: tasas altas en México con *carry* (2022), o una debilidad del dólar originada en EUA (2025). El *benchmark* 50% S&P en MXN y 50% CETES de `parametros.json` ya tiene esta cobertura natural.

### 5.5 Qué funciona y qué no

| Idea | Evidencia | Grado |
|---|---|---|
| Comprar después de un pico de VIX. Primer cierre ≥30 tras 180 días sin tocarlo (1990-2025, n=16): S&P TR a 12 meses con mediana de **+21%**, positivo 12 de 16 veces; con ≥40 (n=9), mediana de **+23.6%**, 7 de 9 positivos. Pero en 2008 hubo otra caída de −38% a −42% | Cálculo propio, dentro de muestra, solo EUA | B |
| Tras un año de −50%, P(duplicarse en 5 años) = 32.8% (Goetzmann) | 42 mercados | B |
| Vender un sector solo porque subió 100% | Pierde ~5 pp a 1 año (GSY) | D como regla aislada |
| Vender con alza, aceleración, volatilidad, emisión y empresas jóvenes al alza, y pasar a libre de riesgo | ~+10 pp a 2 años; poco poder estadístico | B |
| Ponerse corto en una burbuja identificada | +30% promedio hasta el pico, ~6 meses (GSY) | D |
| Tesoro largo como cobertura universal | Falló en 2018, 2022 y 2026 | C |
| USD como cobertura para un inversionista en MXN | 9 de 10 episodios | A/B |
| Oro como cobertura de *crash* | Mixta; falla en liquidaciones | C |
| ETPs de volatilidad corta o *carry* apalancado | 2018: −96%; 2024: desarme en días | D (ruina) |
| Creer en las propias expectativas de *crash* | Los inversionistas las sobreestiman (Goetzmann-Kim-Shiller) | B |

---

## 6. Traducción operable

> En fase 0 estas reglas se ejecutan **en papel**. El perfil `arena_agresivo` aplica a la cuenta de competencia y el `estándar` al patrimonio principal. Ninguna regla aquí cambia `parametros.json`: los valores propuestos nuevos quedan en la sección 6.8 como **propuesta**.

### 6.1 Termómetro de burbuja (por sector o tema, no por índice)

Se calcula mensualmente para sectores GICS, ETFs temáticos y el IPC por sector.

| Señal (GSY) | Umbral | Puntos |
|---|---|---|
| *Run-up* | Rendimiento de 24 meses ≥100% **y** ≥100% neto del S&P 500 (o del IPC) | Condición de entrada |
| *Run-up* extremo | ≥150% en 24 meses | +2 |
| Aceleración | Rendimiento de los últimos 12 meses mayor que el de los 12 anteriores, con la mayor parte del alza en los últimos 6 | +1 |
| Volatilidad | Volatilidad realizada de 6 meses mayor que la de los 12-24 meses previos | +1 |
| Emisión | IPOs o colocaciones secundarias del tema en máximos de 3 años | +1 |
| Empresas jóvenes | Las empresas de menos de 5 años de listado del tema superan a las establecidas | +1 |
| Mercado caro | CAPE del mercado en el decil superior de su historia | +1 |
| Crédito (Jordà-Schularick-Taylor) | El tema se financia con deuda o margen: margen récord, *swaps*, crédito privado | +2 |

**Lectura:** con la condición de entrada y 0-1 puntos, "candidata" (P(*crash*) base ~50% en 2 años con alza de 100%). Con 2-3 puntos, "alerta". Con 4 o más, "burbuja probable" (P(*crash*) cerca de 80% si además el alza es de 150%). **Grado B** (umbrales tomados de GSY; los puntos son una simplificación propia y están pendientes de *backtest* según el cap. 07).

### 6.2 Termómetro de fragilidad (sistema)

| Indicador | Señal de fragilidad |
|---|---|
| VIX | ≥25: se desactiva el filtro de apalancados de `parametros.json`. ≥40: fase de capitulación histórica |
| Relación VIX/VIX3M | >1 (curva invertida): estrés agudo (umbral estándar de mercado; no se hizo *backtest* aquí) |
| Yen | Apreciación fuerte con caída del Nikkei (patrón de ago-2024) |
| Índice bancario regional | −20% en un mes (patrón SVB) |
| Crédito privado y BDCs | Solicitudes de redención por encima de la compuerta de 5% (patrón 2026) |
| Correlación acciones-bonos a 3 meses | Positiva: régimen tipo D, el Tesoro no cubre |
| Peso | USD/MXN +5% en una semana: choque de tipo F o de aversión global |
| Liquidaciones cripto | *Open interest* en máximos, con financiamiento positivo extremo |

### 6.3 Clasificador rápido (menos de 2 horas)

1. ¿El choque viene de **inflación o tasas**? → **D**. No usar bonos largos como cobertura.
2. ¿Hay **bancos o intermediarios** con pérdidas de solvencia (depósitos que salen, *prime brokers* con pérdidas)? → **B** o **G**. Duración de años si es sistémico.
3. ¿Es una **venta mecánica** (margen, ETP, *carry*, LDI, liquidaciones) sin daño de solvencia? → **C**. Rebote probable en días o semanas.
4. ¿Es **política, pandemia o guerra**? → **E** (cap. 23). Depende de si la política se revierte.
5. ¿Es el **tipo de cambio o la deuda de un país**? → **F**.
6. ¿Es un **tema** con termómetro de burbuja ≥2 que se desinfla? → **A**.

### 6.4 *Playbook*: señales → acciones del sistema

| # | Señal | Acción, perfil `arena_agresivo` | Acción, perfil `estándar` |
|---|---|---|---|
| 1 | Tema "candidata" (6.1) | Sin compras nuevas apalancadas en el tema. Tope del tema = `accion_individual_max` 0.30 | Tope del tema = `sector_max` 0.25 |
| 2 | Tema en "alerta" (2-3 puntos) | Recortar a la mitad la exposición al tema. **El producto va a CETES, no al índice** (GSY) | Igual, con tope de 0.125 |
| 3 | Tema en "burbuja probable" (≥4 puntos o ≥150%) | Exposición residual ≤10%, con salida por tendencia (cap. 14). **Prohibido ponerse corto** | Exposición ≤5% |
| 4 | VIX ≥25 | Aplicar `filtro_apalancados`: vender apalancados. No abrir nuevos | Sin apalancamiento (fase 1: `bruto_max` 1.0) |
| 5 | VIX ≥40 al cierre, o S&P −20% | **No vender el núcleo.** Preparar compras escalonadas en 3 tramos (hoy, +10 días hábiles, +20) con recursos de CETES, dentro de los límites de pérdida | Rebalanceo por bandas (`banda_absoluta` 0.05) hacia la asignación objetivo |
| 6 | Choque tipo C (VIX *pre-market* sin volumen, *carry*, *flash crash*) | **No operar en las primeras 2 horas.** Solo órdenes límite. No reaccionar al VIX previo a la apertura (BIS 95) | Igual |
| 7 | Tipo D (correlación acciones-bonos positiva) | El refugio es CETES, no el TLT. Revisar la exposición a *duration* | Igual; renta fija a menos de 1 año de duración |
| 8 | Estrés bancario (índice bancario −20% en un mes) | Reducir bancos y financieras. Verificar que la custodia esté segregada (GBM e Indeval, cap. 11) | Igual |
| 9 | Choque país México (USD/MXN +5% en una semana, IPC −5% en un día) | **No vender dólares en pánico.** Si la regla de bandas lo pide, rebalancear **vendiendo USD caro** | Igual |
| 10 | Choque de política reversible (tipo E) | Mantener el núcleo. **No vender en un día de −5%**: el +9.5% del 9-abr-2025 llegó 4 sesiones después | Igual |
| 11 | *Drawdown* de la cuenta | Cortacircuitos: −12% reducir 50% la táctica; −20% sin ETFs apalancados; −28% pausa de 2 semanas y *post-mortem*; −35% todo a CETES | −8%, −12%, −15% y −20% según `parametros.json` |
| 12 | Límite de pérdida del periodo | Diaria 5%, semanal 10%, mensual 18%: no se abren posiciones tácticas nuevas | 2%, 4% y 6% |
| 13 | Cripto con *open interest* récord y financiamiento extremo | Tope de 0.30 (`cripto_max`), sin margen. Reducir a la mitad si el financiamiento está en el percentil 95 | Tope de 0.05 |

**Modo torneo (`modo_torneo`).** En crisis la varianza se dispara para todos. Si la cuenta va 5 pp o más **adelante** del mejor rival cuando entra una crisis, se reduce la varianza: se cumple el paso 4 sin excepciones y no se hacen compras escalonadas con más de un tramo. Si va 5 pp o más **atrás**, las compras escalonadas del paso 5 son la forma de subir exposición con ventaja estadística (mediana de +21% a 12 meses tras un VIX de 30 o más). **Nunca** con apalancados antes de que pase el filtro.

### 6.5 Protocolo de reentrada

1. **Apalancados:** solo cuando el subyacente cierre sobre su media de 200 días y el VIX esté por debajo de 25 (`filtro_apalancados`).
2. **Tema desinflado (tipo A):** no se recompra solo porque "ya cayó 50%". En GSY, los *crashes* promedian −42% a 2 años. La recompra exige tendencia positiva (cap. 14) y valuación.
3. **Tipo B:** se asume una duración de años (Reinhart-Rogoff). La exposición se reconstruye en 4 a 6 tramos a lo largo de 6 a 12 meses, no en uno.
4. **Tipo C o E:** recompra en 1 a 3 tramos, porque el patrón histórico es de semanas (2010, 2018, 2020, 2024 y 2025).
5. **Registro:** cada decisión tomada en crisis se anota en el *ledger* de pronósticos con probabilidad y horizonte (cap. 08) para medir el Brier.

### 6.6 Tabla de *drawdowns* y recuperaciones del S&P 500 (precio)

Fuente: Yardeni [13] hasta 2022; cálculo propio para 2023-2026. "Recuperación" = primer cierre en máximo previo.

| Pico | Mínimo | Caída | Días de caída | Récord recuperado | Tiempo total |
|---|---|---|---|---|---|
| 7-sep-1929 | 1-jun-1932 | **−86.2%** | ~1,000 | 22-sep-1954 | ~25 años |
| 11-ene-1973 | 3-oct-1974 | −48.2% | 630 | 17-jul-1980 | 7.5 años |
| 25-ago-1987 | 4-dic-1987 | −33.5% | 101 | 26-jul-1989 | 23 meses |
| 16-jul-1990 | 11-oct-1990 | −19.9% | 87 | 13-feb-1991 | 7 meses |
| 17-jul-1998 | 31-ago-1998 | −19.3% | 45 | 23-nov-1998 | 4 meses |
| 24-mar-2000 | 9-oct-2002 | −49.1% | 929 | 30-may-2007 | 7.2 años |
| 9-oct-2007 | 9-mar-2009 | **−56.8%** | 517 | 28-mar-2013 | 5.5 años |
| 23-abr-2010* | 2-jul-2010 | −16.0% | 70 | 4-nov-2010 | 6 meses |
| 29-abr-2011* | 3-oct-2011 | −19.4% | 157 | 24-feb-2012 | 10 meses |
| 21-may-2015 | 11-feb-2016 | −14.2% | 266 | 11-jul-2016 | 14 meses |
| 26-ene-2018 | 8-feb-2018 | −10.2% | 13 | 24-ago-2018 | 7 meses |
| 20-sep-2018 | 24-dic-2018 | −19.8% | 95 | 23-abr-2019 | 7 meses |
| 19-feb-2020 | 23-mar-2020 | −33.9% | 33 | 18-ago-2020 | 6 meses |
| 3-ene-2022 | 12-oct-2022 | −25.4% | 282 | 19-ene-2024 | 2 años |
| 16-jul-2024 | 5-ago-2024 | −8.5% | 20 | 19-sep-2024 | 2 meses |
| 19-feb-2025 | 8-abr-2025 | −18.9% | 48 | 27-jun-2025 | 4 meses |
| 27-ene-2026 | 30-mar-2026 | −9.1% | 62 | 15-abr-2026 | 2.6 meses |

\* Pico local: el índice seguía debajo del máximo de 2007. Con dividendos (TR), 2000-2002 se recupera el 23-oct-2006 y 2007-2009 el 2-abr-2012 (cálculo propio). Nikkei de referencia: 38,915.87 (29-dic-1989) → 7,054.98 (10-mar-2009), **−81.9%**, recuperado el **22-feb-2024 (34 años)** (cálculo propio). Es la prueba de que "el índice siempre regresa" es sesgo de supervivencia de EUA.

### 6.7 Tabla de *drawdowns* y recuperaciones del IPC (precio, sin dividendos; cálculo propio)

| Pico | Mínimo | Caída en MXN | Récord recuperado (MXN) | Contexto | En USD |
|---|---|---|---|---|---|
| 1-jun-1992 | 25-sep-1992 | −34.4% | 23-ago-1993 | Corrección de 1992 | — |
| 8-feb-1994 | 27-feb-1995 | **−49.4%** | 2-ene-1996 (con inflación de 52%) | Tequila | ~−70% (inferencia) |
| 21-oct-1997 | 10-sep-1998 | −46.8% | 15-abr-1999 | Asia y Rusia | EWW −60.4% |
| 9-mar-2000 | 20-sep-2001 | −38.9% | 6-nov-2003 | Dot-com y 11-S | EWW −45.5% |
| 9-may-2006 | 13-jun-2006 | −23.7% | 20-sep-2006 | Corrección de emergentes | −27.7% |
| 18-oct-2007 | 27-oct-2008 | **−48.6%** | 7-ene-2010 | GFC | **−64.8%** (recupera 3-ene-2011) |
| 5-ene-2011 | 8-ago-2011 | −18.0% | 26-mar-2012 | Euro y EUA | −28.3% |
| 28-ene-2013 | 20-jun-2013 | −18.3% | 3-sep-2014 | *Taper tantrum* | — |
| 25-jul-2017 | 23-mar-2020 | −36.3% | 18-ago-2021 | TLCAN y COVID | **−63.9%** (desde abr-2013; recupera **12-ene-2026**) |
| 1-abr-2022 | 30-sep-2022 | −21.2% | 14-dic-2023 | Tasas | — |
| 7-feb-2024 | 30-dic-2024 | −16.8% | 28-may-2025 | Elección y reforma judicial | — |
| 11-feb-2026 | 18-sep-2026 | −11.5% (en curso) | — | 2026 | −13.9% al mínimo del 23-mar |

**Lectura:** el IPC tiene más caídas de más de 30% que el S&P en el mismo periodo, y **en dólares** sus recuperaciones son de las más largas entre los mercados relevantes para el dueño. **Regla:** el IPC es un satélite táctico o de valor, no un núcleo de protección.

### 6.8 Parámetros propuestos (para revisión, no aplicados)

```json
"crisis": {
  "termometro_burbuja": {"runup_24m": 1.0, "runup_24m_neto_mercado": 1.0, "runup_extremo": 1.5, "puntos_alerta": 2, "puntos_burbuja": 4},
  "vix_filtro_apalancados": 25,
  "vix_capitulacion": 40,
  "compras_escalonadas_tramos": 3,
  "compras_escalonadas_espaciado_dias_habiles": 10,
  "destino_salida_burbuja": "CETES",
  "no_operar_primeras_horas_choque_tipo_C": 2
}
```

---

## 7. Trampas y errores comunes

1. **Decir "burbuja" sobre un índice amplio.** Las burbujas medibles son sectoriales (GSY). Goetzmann muestra que un mercado entero duplicado rara vez se desploma.
2. **Ponerse corto en una burbuja correctamente identificada.** Hay en promedio +30% y ~6 meses hasta el pico. Shiller se adelantó más de 3 años en 1996.
3. **Salir al índice en lugar de a efectivo.** En GSY, el mercado también cae cuando cae el sector (−42% a 2 años en los episodios con *crash*).
4. **Juzgar por el índice de precio nominal.** El "25 años" de 1929 fueron unos 7 con dividendos y deflación. El "máximo del IPC" de 1996 fue nominal con 52% de inflación.
5. **Suponer que los bonos siempre cubren.** En 2022, 2018 y 2026 fallaron. Hay que revisar primero la correlación acciones-bonos.
6. **Suponer que el oro o bitcoin cubren un *crash*.** En la liquidación de 2020 el oro cayó. Bitcoin cayó más que el S&P en 6 de 8 episodios y casi igual en un séptimo.
7. **Olvidar la moneda.** Para una cuenta en MXN, el S&P cayó −17.2% y no −33.9% en 2020. En 2022 cayó más en pesos que en dólares.
8. **Reaccionar al VIX *pre-market*.** El 5-ago-2024 el 66 fue un artefacto de cotizaciones (BIS 95). El S&P recuperó en 45 días.
9. **Productos con apalancamiento diario o volatilidad inversa en crisis.** XIV −96% en una sesión.
10. **Órdenes de mercado y *stops* a mercado en choques de liquidez.** En 2010 y 2015 se ejecutaron a precios absurdos, y en CHF 2015 dejaron saldos negativos.
11. **Confundir liquidez de ventanilla con liquidez real.** SVB, los BDCs no cotizados de 2026 y los fondos LDI eran "líquidos" hasta que todos quisieron salir.
12. **Sobreestimar la probabilidad de *crash* por lo que dicen las noticias** (Goetzmann-Kim-Shiller). El costo de oportunidad de estar fuera suele superar el costo de la caída.
13. **Sesgo de supervivencia de EUA.** El Nikkei tardó 34 años. El IPC en USD tardó 12.8. "Siempre regresa" no es ley.
14. **Muestras chicas presentadas como leyes.** 40 episodios en GSY y 16 picos de VIX aquí. Todo es grado B en el mejor de los casos.
15. **Contraparte.** FTX, FXCM y Archegos: el riesgo no estaba en el activo sino en quien lo custodiaba o prestaba.

---

## 8. Examen de titulación

1. **Según GSY, ¿qué pasa con el rendimiento promedio y con la probabilidad de *crash* después de un alza de 100% en 2 años en una industria de EUA?**
   El rendimiento promedio posterior es cercano a cero. La probabilidad de una caída de 40% o más en 2 años es de 53% (80% con un alza de 150%), contra 14% incondicional.
2. **¿Por qué vender todo *run-up* de 100% pierde contra comprar y mantener a 1 año?**
   Porque 47% son falsos positivos y porque en los verdaderos el precio sube ~30% durante ~6 meses antes del pico. Pierde unos 5 pp.
3. **¿Qué características distinguen los *run-ups* que terminan en *crash*, y cuál no sirve?**
   Aceleración, aumento de volatilidad, emisión, *age tilt* hacia empresas jóvenes y CAPE alto. El *turnover* no sirve, porque es alto en ambos grupos.
4. **Goetzmann: probabilidad de que un mercado que se duplicó en un año caiga 50% al año siguiente, y a 5 años.**
   6.9% (contra 2.1% incondicional) y 17.2% (contra 8.5%).
5. **¿Cómo se reconcilian GSY y Goetzmann?**
   Goetzmann mide mercados completos con *crash* de −50%. GSY mide industrias, con −40% y alza también neta de mercado. Las burbujas son sectoriales.
6. **¿Qué dice Pástor-Veronesi sobre el Nasdaq de 1999?**
   El valor sube con la incertidumbre sobre la rentabilidad promedio. Con incertidumbre alta y prima de riesgo baja, las valuaciones eran racionalizables. Las "burbujas" tecnológicas solo se ven *ex post*.
7. **Magnitudes de Reinhart-Rogoff tras una crisis bancaria sistémica.**
   Acciones −55% en ~3.5 años, vivienda real −35% en ~6 años, desempleo +7 pp durante más de 4 años, PIB −9% y deuda pública real +86%.
8. **¿Cuál es el diferenciador clave entre una burbuja que destruye la economía y una que no?**
   El crédito (Jordà-Schularick-Taylor): las burbujas financiadas con crédito traen recesiones más profundas y recuperaciones más lentas.
9. **Los dos teoremas de Minsky.**
   (1) Hay regímenes de financiamiento estables e inestables. (2) La prosperidad prolongada mueve la economía de cobertura a especulativa y Ponzi, es decir, hacia la inestabilidad.
10. **¿Qué activo protegió al inversionista en MXN en 9 de 10 episodios, y cuál fue la excepción?**
    El dólar (USD/MXN al alza). La excepción fue 2022, un choque de tasas con el peso fuerte por *carry*.
11. **¿Por qué el Tesoro largo no cubrió en 2022, y en qué tipo de crisis sí cubre?**
    Porque el choque era de inflación y tasas (tipo D): el TLT perdió −30.5%. Cubre en crisis deflacionarias o de demanda (2008 +17.7%, 2011 +31.9%, 2020 +14.1%).
12. **Caída y recuperación del S&P en 2020 y en 2025.**
    2020: −33.9% en 33 días, récord el 18-ago-2020. 2025: −18.9% (19-feb al 8-abr), récord el 27-jun-2025.
13. **¿Qué causó el pico del VIX del 5-ago-2024 según el BIS, y qué implica?**
    Ampliación de *spreads* en cotizaciones de *puts*, porque el VIX usa cotizaciones y no operaciones. Implica no reaccionar al VIX previo a la apertura: el S&P recuperó en 45 días.
14. **¿Cuánto tardó el IPC en dólares en recuperar su máximo de 2013, y qué regla se deriva?**
    Hasta el 12-ene-2026, 12.8 años (−63.9% al mínimo de mar-2020). El IPC no es un activo de protección para el núcleo.
15. **¿Qué hace el sistema si el VIX cierra en 40 o más con la cuenta arena 5 pp atrás del mejor rival?**
    No vende el núcleo ni compra apalancados, porque el filtro exige VIX <25 y precio sobre la media de 200 días. Hace compras escalonadas en 3 tramos con recursos de CETES dentro de los límites de pérdida. Históricamente la mediana a 12 meses fue de +21% a +24%, con el riesgo de un 2008 (−38% adicional).

---

## 9. Fuentes

1. Greenwood, R., Shleifer, A. y You, Y. (2019). "Bubbles for Fama". *Journal of Financial Economics*. Cifras de la versión NBER w23191: https://www.nber.org/papers/w23191 · PDF: https://www.nber.org/system/files/working_papers/w23191/w23191.pdf · JFE: https://www.sciencedirect.com/science/article/abs/pii/S0304405X1830254X
2. Goetzmann, W. (2016). "Bubble Investing: Learning from History". NBER w21693: https://www.nber.org/papers/w21693 · PDF: https://www.nber.org/system/files/working_papers/w21693/revisions/w21693.rev1.pdf · Resumen NBER Digest: https://www.nber.org/digest/jan16/market-bubbles-what-goes-doesnt-always-come-down
3. Pástor, Ľ. y Veronesi, P. (2009). "Technological Revolutions and Stock Prices". *AER* 99(4): 1451-83. https://www.aeaweb.org/articles?id=10.1257%2Faer.99.4.1451
4. Pástor, Ľ. y Veronesi, P. (2006). "Was There a Nasdaq Bubble in the Late 1990s?". *JFE*. NBER w10581: https://www.nber.org/papers/w10581
5. Reinhart, C. y Rogoff, K. (2009). "The Aftermath of Financial Crises". NBER w14656: https://www.nber.org/papers/w14656
6. Reinhart, C. y Rogoff, K. (2008). "This Time is Different: A Panoramic View of Eight Centuries of Financial Crises". NBER w13882: https://www.nber.org/papers/w13882
7. Minsky, H. (1992). "The Financial Instability Hypothesis". Levy Institute WP 74: https://www.levyinstitute.org/pubs/wp74.pdf
8. Kindleberger, C., Aliber, R. y McCauley, R. *Manias, Panics, and Crashes* (8.ª ed.): https://www.springerprofessional.de/en/manias-panics-and-crashes/24098366
9. Jordà, Ò., Schularick, M. y Taylor, A. (2015). "Leveraged Bubbles". NBER w21486: https://www.nber.org/papers/w21486
10. Goetzmann, W., Kim, D. y Shiller, R. "Crash Beliefs from Investor Surveys". NBER w22143: https://www.nber.org/papers/w22143
11. Hirano, T., Kishi, K. y Toda, A. A. "General-Purpose Technologies and Stock Market Bubbles". arXiv 2501.08215 (v3, ago-2026): https://arxiv.org/abs/2501.08215
12. Wang, Q. y Chen, Z. (2026). "Boom, Bubble, or Buildout?". arXiv 2606.01575: https://arxiv.org/abs/2606.01575
13. Yardeni Research. *Stock Market Historical Tables: Bull & Bear Markets* (21-ene-2024): https://old.yardeni.com/wp-content/uploads/BullBearTables.pdf
14. Federal Reserve History. "Stock Market Crash of 1929": https://www.federalreservehistory.org/essays/stock-market-crash-of-1929
15. Hulbert, M. "25 Years to Bounce Back? Try 4 1/2" (History News Network): https://www.historynewsnetwork.org/article/mark-hulbert-25-years-to-bounce-back-try-4-12
16. Wikipedia. "1973–1974 stock market crash": https://en.wikipedia.org/wiki/1973%E2%80%931974_stock_market_crash
17. EBSCO Research Starters. "Black Monday stock market crash": https://www.ebsco.com/research-starters/business-and-management/black-monday-stock-market-crash
18. Wikipedia. "1994 bond market crisis": https://en.wikipedia.org/wiki/1994_bond_market_crisis · EBC: https://www.ebc.com/forex/1994-bond-massacre
19. CRS. "The 1997-98 Asian Financial Crisis": https://sgp.fas.org/crs/row/crs-asia2.htm
20. Federal Reserve History. "Near Failure of Long-Term Capital Management": https://www.federalreservehistory.org/essays/ltcm-near-failure · Wikipedia LTCM: https://en.wikipedia.org/wiki/Long-Term_Capital_Management · GAO: https://www.gao.gov/assets/ggd-00-67r.pdf
21. Wikipedia. "Dot-com bubble": https://en.wikipedia.org/wiki/Dot-com_bubble
22. Wikipedia. "2010 flash crash": https://en.wikipedia.org/wiki/2010_flash_crash · CNN (informe SEC/CFTC): https://money.cnn.com/2010/10/01/markets/SEC_CFTC_flash_crash/index.htm
23. Wikipedia. "August 2011 stock markets fall": https://en.wikipedia.org/wiki/August_2011_stock_markets_fall
24. Forbes (16-ene-2015), FXCM: https://www.forbes.com/sites/steveschaefer/2015/01/16/swiss-bank-stunner-claims-victims-currency-broker-fxcm-bludgeoned/ · Finance Magnates: https://www.financemagnates.com/forex/brokers/fxcm-publishes-data-of-snb-mishandling-of-the-swiss-franc/
25. CNN (11-ago-2015), devaluación del yuan: https://money.cnn.com/2015/08/11/investing/china-pboc-yuan-devalue-currency/index.html · CNN (24-ago-2015): https://money.cnn.com/2015/08/24/investing/stocks-markets-selloff-china-crash-dow/index.html
26. CFA Institute, FAJ (2021). "Volmageddon and the Failure of Short Volatility Products": https://rpc.cfainstitute.org/research/financial-analysts-journal/2021/volmageddon-failure-short-volatility-products · Six Figure Investing: https://www.sixfigureinvesting.com/2019/02/what-caused-the-february-5th-2018-volatility-spike-xiv-termination/
27. CNBC (31-ene-2021), Melvin Capital: https://www.cnbc.com/2021/01/31/melvin-capital-lost-more-than-50percent-after-betting-against-gamestop-wsj.html
28. Wikipedia. "Archegos Capital Management": https://en.wikipedia.org/wiki/Archegos_Capital_Management
29. Chicago Fed Letter 480 (2023), LDI: https://www.chicagofed.org/publications/chicago-fed-letter/2023/480 · FMI WP 2023/210: https://www.elibrary.imf.org/view/journals/001/2023/210/article-A001-en.xml
30. Forbes (25-may-2022), Terra: https://www.forbes.com/sites/lawrencewintermeyer/2022/05/25/from-hero-to-zero-how-terra-was-toppled-in-cryptos-darkest-hour/ · CBS, FTX: https://www.cbsnews.com/news/ftx-bankruptcy-sam-bankman-fried-resigns-cryptocurrency/
31. CNBC (28-mar-2023), testimonio de Barr: https://www.cnbc.com/2023/03/28/svb-customers-tried-to-pull-nearly-all-deposits-in-two-days-barr-says.html · Fed OIG: https://oig.federalreserve.gov/reports/board-material-loss-review-silicon-valley-bank-sep2023.htm
32. BIS Bulletin 90: https://www.bis.org/publ/bisbull90.htm · BIS Bulletin 95: https://www.bis.org/publ/bisbull95.pdf
33. CNBC (5-ago-2024), Nikkei: https://www.cnbc.com/2024/08/05/asia-markets.html
34. CNBC (27-ene-2025), Nvidia y DeepSeek: https://www.cnbc.com/2025/01/27/nvidia-sheds-almost-600-billion-in-market-cap-biggest-drop-ever.html
35. CNN (27-jun-2025), récord del S&P: https://www.cnn.com/2025/06/27/investing/stock-market-record-dow-sandp · Wikipedia. "2025 stock market crash": https://en.wikipedia.org/wiki/2025_stock_market_crash
36. CoinDesk Research. "Inside Crypto's $19 Billion Liquidation Event": https://www.coindesk.com/research/market-spotlight-the-19-billion-liquidation-that-shook-crypto
37. CNBC (30-ene-2026), plata y oro: https://www.cnbc.com/2026/01/30/silver-gold-fall-price-usd-dollar-fed-warsh-chair-trump-metals.html · Mining.com: https://www.mining.com/gold-silver-prices-plunge-as-trumps-fed-chair-pick-triggers-selloff/
38. Bloomberg (4-feb-2026). "What's Behind the 'SaaSpocalypse'": https://www.bloomberg.com/news/articles/2026-02-04/what-s-behind-the-saaspocalypse-plunge-in-software-stocks
39. CNBC (24-feb-2026), crédito privado: https://www.cnbc.com/2026/02/24/private-credit-3-trillion-boom-bankruptcies-fraud-blue-owl-redemptions-tricolor-first-brands-bdc.html · CNBC (2-abr-2026), Blue Owl: https://www.cnbc.com/2026/04/02/blue-owl-private-credit-funds-redemptions-requests.html · With Intelligence: https://www.withintelligence.com/insights/what-is-actually-going-on-in-bdc-portfolios/
40. CNN (4-ago-2026), récord del S&P: https://www.cnn.com/2026/08/04/investing/us-stock-market
41. Wikipedia. "Mexican peso crisis": https://en.wikipedia.org/wiki/Mexican_peso_crisis · Wikipedia (es). "Crisis económica de México de 1994": https://es.wikipedia.org/wiki/Crisis_econ%C3%B3mica_de_M%C3%A9xico_de_1994 · Brookings: https://www.brookings.edu/articles/mexico-in-crisis-the-u-s-to-the-rescue-the-financial-assistance-packages-of-1982-and-1995/
42. *Revista de Historia Económica* (Cambridge). "When it rains, it pours: Mexico's bank nationalisation and the debt crisis of 1982": https://www.cambridge.org/core/journals/revista-de-historia-economica-journal-of-iberian-and-latin-american-economic-history/article/when-it-rains-it-pours-mexicos-bank-nationalisation-and-the-debt-crisis-of-1982/8A85C44DE3CC18702E2229E1468B2012 · BFI, "The Case of Mexico": https://bfi.uchicago.edu/wp-content/uploads/The-Case-of-Mexico.pdf
43. Dodd, R. (2009). *Finance & Development*, FMI (derivados exóticos en emergentes): https://www.imf.org/external/pubs/ft/fandd/2009/06/dodd.htm
44. Wikipedia. "Cemex": https://en.wikipedia.org/wiki/Cemex
45. Yahoo Finance, API de gráficas (cierres diarios; ejemplo): https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC · mismo *endpoint* para ^SP500TR, ^MXX, MXN=X, ^VIX, ^TNX, GC=F, TLT, EWW, BTC-USD, ^N225, ^IXIC, IGV, KRE, SLV, NVDA, ARKK, GME y CX. Descarga del 25-sep-2026.
46. Progress.org. "Kindleberger & Aliber: Manias, Panics, and Crashes": https://www.progress.org/wiki/kindleberger-manias-panics-crashes/
47. Reinhart y Rogoff (2009), AER P&P (PDF): https://faculty.sites.iastate.edu/tesfatsi/archive/econ502/tesfatsion/AftermathOfFinancialCrisis.ReinhartRogoff.AER2009.pdf
