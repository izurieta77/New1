# 17 — Crisis y burbujas: libro de patrones

> Nivel: experto · Actualizado: 2026-09-25 · Grado de evidencia global: **B** (magnitudes y secuencias históricas: **A**; detección de burbujas por características: **B**; *timing* del techo: **C**)

Capítulos relacionados, que aquí no se repiten: [01 Fundamentos](01-licenciatura-fundamentos.md) · cap. 04 (renta fija) · cap. 05 (derivados) · cap. 07 (riesgo y *backtesting*) · cap. 08 (conductuales) · cap. 11 (México) · cap. 12 (alternativos y cripto) · cap. 13 (estado del mercado) · [14 Análisis técnico](14-analisis-tecnico-que-sobrevive.md) · [15 Eventos corporativos](15-eventos-corporativos-y-situaciones-especiales.md) · [23 Geopolítica](23-geopolitica-y-riesgo-politico-global.md). Los parámetros salen de `config/parametros.json`.

**Convenciones.** "Inferencia:" = razonamiento propio. "Regla:" = recomendación, solo en la sección 6. "(no verificado)" = cifra no confirmada en esta sesión. **"Cálculo propio"** = cierres diarios de Yahoo Finance descargados el 25-sep-2026 (^GSPC, ^SP500TR, ^MXX, MXN=X, ^VIX, ^TNX, GC=F, TLT, EWW, BTC-USD, ^N225, ^IXIC, IGV, KRE, SLV, NVDA, ARKK, GME, CX) [45]. Son índices de precio salvo que diga TR. El IPC no incluye dividendos. El USD/MXN de Yahoo es un cierre de mercado, no el FIX.

---

## 1. Objetivos de dominio

1. Clasificar una crisis en uno de **7 tipos** (sección 2.5) en menos de 2 horas. Cada tipo tiene profundidad, duración y refugios distintos.
2. Separar una **burbuja** de un **boom racional con incertidumbre** (Pástor-Veronesi), sabiendo que la diferencia rara vez se ve *ex ante*.
3. Dominar las cifras de Greenwood-Shleifer-You (GSY) y de Goetzmann, y explicar por qué no se contradicen.
4. Medir la fragilidad del sistema: apalancamiento, venta de volatilidad, descalce de liquidez y descalce cambiario.
5. Saber qué protegió en cada crisis y cuándo falló: bonos en 2022, oro en 2020 y 2026, bitcoin casi siempre.
6. Pensar en **MXN**: el dólar es la cobertura más confiable para un inversionista en pesos, y el IPC en USD tiene recuperaciones de más de una década.
7. Ejecutar el *playbook* de la sección 6 dentro de los límites de `parametros.json`.

---

## 2. Núcleo teórico

### 2.1 Kindleberger y Minsky

Kindleberger (con Aliber; en la 8.ª edición, también McCauley) describe cinco etapas [8][46]:

1. **Desplazamiento**: un choque real crea oportunidades de ganancia.
2. **Boom con crédito**.
3. **Euforia**: "esta vez es distinto".
4. **Dificultad financiera**: los *insiders* venden, sube el costo del dinero y aparece un fraude.
5. **Repulsión y pánico**: se vende lo que se puede. Al final entra un prestamista de última instancia.

Minsky (Levy WP 74, 1992) distingue tres tipos de unidades [7]:

- **Cobertura**: sus flujos pagan intereses y principal.
- **Especulativa**: paga intereses pero necesita refinanciar el principal.
- **Ponzi**: no le alcanza ni para los intereses, así que vende activos o pide prestado.

*Primer teorema:* hay regímenes de financiamiento estables e inestables. *Segundo:* "over periods of prolonged prosperity, the economy transits from financial relations that make for a stable system to financial relations that make for an unstable system". Si en ese estado la autoridad aprieta para combatir la inflación, las unidades especulativas se vuelven Ponzi y el patrimonio de las Ponzi "se evapora".

**Inferencia:** la volatilidad baja y los *spreads* comprimidos no son una señal de seguridad. Son la condición que fabrica el apalancamiento. 1929, 2008, LDI 2022 y SVB 2023 siguieron la secuencia estabilidad → apalancamiento → apretón monetario → venta forzada.

### 2.2 Reinhart-Rogoff

*This Time Is Different* (NBER w13882) cubre ocho siglos. El *default* soberano serial es "a nearly universal phenomenon" y coincide con inflación, colapsos cambiarios y crisis bancarias [6]. *The Aftermath of Financial Crises* (AER P&P 2009) mide lo que sigue a una crisis bancaria sistémica [5][47]:

| Variable | Promedio | Duración |
|---|---|---|
| Vivienda (real) | −35% | ~6 años |
| **Acciones** | **−55%** | ~3.5 años |
| Desempleo | +7 pp | más de 4 años |
| PIB | −9% | más corta |
| Deuda pública real | +86% (posguerra) | — |

**Grado A.** La deuda sube sobre todo porque se desploman los ingresos fiscales, no por el costo de los rescates.

### 2.3 El diferenciador es el crédito

Jordà-Schularick-Taylor, "Leveraged Bubbles" (17 países, 140 años): "When fueled by credit booms, asset price bubbles increase financial crisis risks; upon collapse they tend to be followed by deeper recessions and slower recoveries" [9]. **Grado A/B.** **Inferencia:** el dot-com (poco crédito bancario) destruyó el Nasdaq con una recesión leve, mientras que 2008 (vivienda y bancos) destruyó el sistema. La primera pregunta ante una burbuja es **quién está apalancado contra el activo y quién le prestó**.

### 2.4 Detección: GSY, Goetzmann y Pástor-Veronesi

**Greenwood-Shleifer-You, "Bubbles for Fama" (JFE 2019; cifras de NBER w23191)** [1]:

- **Definiciones.** *Run-up*: rendimiento de una industria de ≥100% en 2 años, tanto bruto como neto del mercado. *Crash*: caída de ≥40% en los 2 años siguientes.
- **Muestra.** EUA 1926-2014 (40 *run-ups*). Internacional 1985-2014 como prueba fuera de muestra (107 *run-ups* en 31 países, 53 con *crash*).
- **Fama tiene razón en la media.** Después de un *run-up* el rendimiento promedio es cercano a cero. En EUA, 21 de los 40 se desploman (−42% a 2 años, −29% neto de mercado) y 19 no (+21% a 1 año, +46% a 2 años).
- **Pero el *crash* se vuelve probable.** P(*crash*) = 20% con un alza de 50% neta de mercado, **53% con 100%** y **80% con 150%** (n=15). Internacional: 36%, 50% y 67%. Incondicional: 14% en EUA (11% después de 1970) y 24% fuera de EUA.
- **El techo no se puede cronometrar.** En los que sí se desploman, el precio sube **+30% durante ~6 meses** más desde que se identifican; el *crash* empieza a ~5 meses.
- **Qué distingue a los que se desploman:** volatilidad al alza, **aceleración**, emisión de acciones, CAPE al alza y mejor desempeño de **empresas jóvenes** sobre las viejas. El *turnover* no distingue. Las ventas tampoco (en EUA). Tras corregir por *false discovery rate* al 10%, sobreviven la aceleración, el *age tilt* y el cambio en volatilidad.
- **Estrategia.** Vender todo *run-up* de 100% **pierde ~5 pp a 1 año**, con 47% de falsos positivos. Condicionar en características y **pasar a libre de riesgo (no al índice)** da ~**+10 pp a 2 años**. Con la volatilidad como filtro el *alpha* es de 0, 8 y 12 pp a 1, 2 y 4 años, significativo solo a 4. n=40, con *look-ahead* en los umbrales.

**Goetzmann, "Bubble Investing" (42 mercados, 1900-2014)** [2]:

- De 3,514 años-mercado, 58 (1.7%) subieron más de 100% real en un año. De ellos:
  - al año siguiente **6.9%** cayeron más de 50% (incondicional 2.1%) y otro 6.9% volvió a duplicarse;
  - a 5 años, **17.2%** cayeron (incondicional 8.5%) y **22.4%** se duplicaron (incondicional 16.9%).
- Con la definición amplia (duplicarse en 3 años; 346 eventos, como EUA en 1928 o 1997) la probabilidad de *crash* es de 4.6% a 1 año (contra 2%) y de 9.8% a 5 años (contra 8.4%).
- **Tras un año de −50%, P(duplicarse en 5 años) = 32.8%.**

**Reconciliación.** Goetzmann mide mercados completos y caídas de −50%. GSY mide industrias, caídas de −40% y alzas también netas de mercado. Las burbujas son **sectoriales**. **Inferencia:** el termómetro se aplica a sectores y temas, no al índice amplio.

**Pástor-Veronesi.** En el trabajo de 2006 (JFE; NBER w10581), el valor de una empresa **sube con la incertidumbre sobre su rentabilidad promedio**. Con la incertidumbre alta y la prima de riesgo baja de 1999, el pico del Nasdaq era racionalizable [4]. En AER 2009 las "burbujas" tecnológicas surgen en equilibrio: el riesgo pasa de idiosincrático a **sistemático** al adoptarse la tecnología, son "observables *ex post* pero impredecibles *ex ante*" y fueron más fuertes con los ferrocarriles de 1830-61 y con internet en 1992-2005 [3].

**2025-2026.** Hirano-Kishi-Toda (arXiv 2501.08215, v3 de ago-2026) modelan burbujas racionales sobre acciones con dividendos en tecnologías de propósito general como la IA [11]. Wang-Chen (arXiv 2606.01575, sin revisión de pares) concluyen que la IA es "a real technological revolution with localized bubble dynamics" [12]. **Grado C.**

### 2.5 Taxonomía operable

| Tipo | Mecanismo | Ejemplos | Caída típica | Recuperación | Protege |
|---|---|---|---|---|---|
| **A** Burbuja de valuación sin crédito | Narrativa, emisión, empresas jóvenes | 2000, memes 2021, software 2026 | Sector −70% a −90%; índice −25% a −50% | Sector: años o nunca | Tesoro, efectivo |
| **B** Burbuja apalancada o bancaria | Crédito (Minsky) | 1929, 2008, Japón 1990, México 1994 | −50% a −86% | 4 a 25 años nominal | Tesoro si hay deflación, USD |
| **C** Liquidez o microestructura | Venta mecánica forzada | 1987, 2010, feb-2018, LDI, ago-2024, cripto oct-2025, plata ene-2026 | −10% a −34% en días | Semanas o meses | Liquidez, sin apalancamiento |
| **D** Tasas o inflación | Correlación acciones-bonos positiva | 1973-74, 1994, 2022 | −20% a −48%, con bonos cayendo | 1.5 a 7.5 años | CETES/*T-bills*, *commodities* |
| **E** Exógeno o de política | Pandemia, aranceles, guerra (cap. 23) | 2020, abr-2025, Irán 2026 | −9% a −34% | 2 a 6 meses | USD (en MXN) |
| **F** Emergente, cambiaria o soberana | Tipo de cambio fijo, deuda corta en USD | 1982, 1994, 1997, 1998, 2011, 2015 | Local −50% a −80% en USD | Años | USD fuera del país |
| **G** Apalancamiento o fraude idiosincrático | Contraparte, *prime broker*, custodia | LTCM, Archegos, FTX, SVB, crédito privado 2026 | Índice −3% a −19%; sector −50% | Índice rápido, sector lento | Custodia segregada |

**Amplificadores** (explican la forma de la caída; el tipo explica la duración):

1. Margen: 10% de enganche en 1929 [14]; LTCM con ~30 a 1 [20].
2. Convexidad negativa: el *portfolio insurance*, los ETPs de VIX inverso y los fondos LDI venden cuando baja.
3. Descalce de liquidez: SVB, BDCs no cotizados.
4. Descalce cambiario: tesobonos, Asia 1997, derivados de empresas mexicanas en 2008 [43].
5. *Crowding*: el *carry* en yenes (~¥40 billones o US$250 mil millones) [32].

---

## 3. Literatura y fuentes canónicas

| Obra | Hallazgo cuantificado | Enlace | Grado |
|---|---|---|---|
| Kindleberger-Aliber-McCauley, *Manias, Panics, and Crashes* | Cinco etapas; crédito y prestamista de última instancia. Narrativo | [8] | B |
| Minsky (1992), WP 74 | Cobertura, especulativa y Ponzi; dos teoremas | [7] | B/C |
| Reinhart-Rogoff (2008, 2009) | Acciones −55% en ~3.5 años, vivienda −35% en ~6, desempleo +7 pp, deuda +86% | [5][6] | A |
| Jordà-Schularick-Taylor (2015) | Las burbujas con crédito dejan recesiones más hondas y recuperaciones lentas | [9] | A/B |
| Greenwood-Shleifer-You (2019) | Con 100% en 2 años el rendimiento posterior es ~0, pero P(*crash*) = 53% (80% con 150%); salir a libre de riesgo con características da ~+10 pp a 2 años | [1] | B |
| Goetzmann (2016) | Duplicarse en 1 año lleva a P(−50%) de 6.9% al año siguiente y 17.2% a 5 años; después de un *crash*, P(duplicarse) = 32.8% | [2] | B |
| Pástor-Veronesi (2006, 2009) | La incertidumbre justifica valuaciones altas; las burbujas tecnológicas son racionales y se ven *ex post* | [3][4] | B |
| Goetzmann-Kim-Shiller, *Crash Beliefs* | 26 años de encuestas: los inversionistas sobreestiman la probabilidad de *crash*; sesgo de disponibilidad por noticias; menos flujos a fondos | [10] | B |
| Yardeni, tablas *bull/bear* | Fechas y magnitudes oficiales del S&P desde 1928 | [13] | A (dato) |
| BIS Bulletin 90 y 95 (2024) | *Carry* de ~¥40 billones; el pico del VIX del 5-ago se debió a cotizaciones de *puts*, no a ETFs | [32] | B |
| Chicago Fed Letter 480 | LDI: el gilt a 30 años subió +200 pb; el BoE compró £19.3 mil millones | [29] | A (dato) |
| Fed OIG (2023) | La supervisión de SVB no creció con el banco ni revisó el riesgo de tasa | [31] | A (dato) |
| Hirano-Kishi-Toda; Wang-Chen | Burbujas racionales en tecnologías de propósito general; IA con burbujas locales | [11][12] | C |

---

## 4. Lo más reciente, 2023-2026

- **SVB (mar-2023).** El 9-mar salieron **US$42 mil millones** y había US$100 mil millones en cola para el día siguiente (Barr) [31]. El S&P perdió −3.4% (8 al 13-mar). El KRE (bancos regionales) perdió **−54.2%** entre ene-2022 y may-2023 y no ha recuperado. En esa ventana el oro subió +5.4% (cálculo propio). Las corridas de hoy duran horas.
- ***Carry* en yenes (ago-2024).** El Nikkei perdió **−12.4%** el 5-ago (el peor día desde 1987) y rebotó **+10.2%** el 6-ago. El VIX tocó alrededor de 66 en el *pre-market*, por *spreads* de cotización según el BIS 95. El S&P perdió −8.5% y recuperó en 45 días (cálculo propio) [32][33].
- **DeepSeek (27-ene-2025).** Nvidia perdió −17% (**−US$589 mil millones**, récord), el Nasdaq −3.07% y el S&P −1.46% [34]. Nvidia cayó −36.9% al 4-abr y recuperó el 25-jun (cálculo propio).
- **Aranceles (abr-2025, tipo E).** El S&P perdió **−18.9%** (19-feb al 8-abr). El 9-abr subió **+9.52%**. El VIX cerró en 52.33 y el S&P hizo récord el 27-jun-2025 [35]. **En MXN, el S&P TR perdió −20.1% y no recuperó hasta el 27-oct-2025** (cálculo propio).
- **Cripto (10 y 11 de oct-2025).** Tras el anuncio de un arancel de 100% a China se liquidaron **US$19 mil millones** en ~24 horas, y el *open interest* cayó −43% [36]. BTC pasó de 124,753 (6-oct-2025) a **58,559 (30-jun-2026), −53.1%** (cálculo propio).
- **Metales (30-ene-2026).** La plata perdió **−31.4%** en futuros, su peor día desde 1980, y el oro perdió más de 12% intradía al nominarse Warsh a la Fed [37]. Del 29-ene al 16-jul el oro (GC=F) perdió **−24.9%** y el SLV −52.3% (cálculo propio). Un refugio comprado con *momentum* y apalancamiento se comporta como activo de riesgo.
- **"SaaSpocalypse" (feb-2026).** Los agentes de IA (Claude Cowork y Opus 4.6, según fuentes secundarias) llevaron a revaluar el software cobrado por usuario (Bloomberg, 4-feb) [38]. El IGV perdió **−36.6%** del 22-sep-2025 al 10-abr-2026 y no ha recuperado (cálculo propio).
- **Crédito privado (1T-2026, tipo G).** Hubo fraudes en Tricolor y First Brands. Las redenciones solicitadas en los 12 mayores BDCs no cotizados promediaron **12.1%**, contra compuertas de 5% (fuente secundaria). Blue Owl limitó las salidas a 5% [39]. Lo "semilíquido" es líquido solo mientras nadie quiere salir.
- **Irán (feb-mar 2026; cap. 23).** El S&P perdió −9.1% entre cierres (6,978.60 el 27-ene; 6,343.72 el 30-mar; el cap. 23 da −9.8% con otro dato) y marcó récord el 15-abr. El oro perdió −11.0% en la ventana. La Fed **subió** 25 pb el 16-sep (cap. 23). El S&P estaba en 7,704 el 24-sep [40].
- **IPC en 2026.** Corrección de **−11.5%** del 11-feb (71,601) al 18-sep (63,376); en USD perdió −13.9% al mínimo del 23-mar (cálculo propio). Causa no atribuida aquí (caps. 11 y 13).
- **Bonos largos.** El TLT (precio) sigue **−53.7%** debajo de su máximo de ago-2020, 6 años bajo el agua (cálculo propio; en TR la caída es menor). El tipo D sigue vivo.
- **IA.** El marco académico es "revolución real con burbujas locales" [3][11][12]. La pregunta útil no es si la IA es una burbuja. Es **qué subsector cumple hoy el termómetro GSY** (sección 6.1).

---

## 5. Evidencia real: casos, magnitudes y refugios

### 5.1 Casos globales

Formato: causa · señales · caída y duración · qué protegió · recuperación · **lección**.

- **1929-32 (B).** Margen de 10%, préstamos de corredores y tasa de descuento de Nueva York en 6% en ago-1929 [14]. Dow −89% (3-sep-1929 al 8-jul-1932). S&P **−86.2%** [13]; −12.9% y −10.2% los días 28 y 29 de octubre (cálculo propio). Hubo deflación (el IPC de EUA de fines de 1936 estaba más de 18% abajo del de 1929), así que el efectivo y los bonos buenos ganaron poder de compra. Récord nominal en sep-1954. Con dividendos y deflación, el punto de equilibrio fue a fines de 1936 [15], seguido de otro −54.5% en 1937-38 [13]. **Apalancamiento más apretón da el peor tipo B. Hay que medir en términos reales y totales.**
- **1973-74 (D).** Fin de Bretton Woods, choque petrolero, inflación de 3.4% a 12.3% [16]. S&P −48.2% en 630 días. G7 −43% real. FT30 **−73%**. Récord del S&P en jul-1980 (7.5 años). **En inflación, el 60/40 no diversifica.**
- **1987 (C).** El *portfolio insurance* y el arbitraje de índices amplificaron una caída que empezó por tasas, dólar y déficit (Comisión Brady) [17]. S&P **−20.47% el 19-oct**. De máximo a mínimo −33.5% en 101 días. Hong Kong −45.8%. El bono a 10 años protegió solo por días: en la ventana subió de 8.73% a 8.94%. Récord en jul-1989 (23 meses). **Si todos tienen la misma cobertura dinámica, esa cobertura es el riesgo. Un *stop* no es un *put*.**
- **1994, bonos (D).** La Fed pasó de 3% a 6% en unos 12 meses. El 10 años subió ~240 pb. Las pérdidas se estiman en más de US$1.5 billones. Orange County quebró con bonos largos financiados con reportos [18]. El S&P no llegó a −10%. **La duración apalancada ante una sorpresa de la Fed basta.** Fue el contexto externo del Tequila (inferencia).
- **1997, Asia (F).** El baht flotó el 2-jul. A enero de 1998: THB −56%, IDR **−81%**; el won llegó a −55% [19]. S&P −10.8% (récord en dic-1997). IPC **−13.34% el 27-oct-1997**, su peor día de la muestra (cálculo propio). **El contagio no respeta fundamentales.**
- **1998, Rusia y LTCM (F/G).** Rusia devaluó y dejó de pagar. LTCM (~30 a 1) perdió 44% en agosto y US$4.6 mil millones. 14 instituciones pusieron **US$3.625 mil millones** por 90% del fondo, sin dinero público [20]. S&P −19.3% en 45 días, recuperado en nov-1998. IPC −36.0% en esa ventana. El 10 años bajó de 5.50% a 5.03%. **El arbitraje de convergencia es liquidez vendida: en crisis las correlaciones van a 1.**
- **2000-02 (A).** GSY marcaron *run-ups* en software y hardware [1]. Nasdaq **−77.9%** (5,048.62 a 1,114.11), recuperado el **23-abr-2015**. S&P −49.1% en 929 días; TR recuperado en oct-2006 [13][21]. El 10 años bajó de 6.17% a 3.58%. **Una burbuja sin crédito destruye el tema: un índice concentrado tardó 15 años.**
- **2007-09 (B).** Vivienda, crédito y bancos. S&P **−56.8%** en 517 días. VIX al cierre en 80.86. Oro **+24.5%**, TLT **+17.7%**, USD/MXN **+43.5%**. Récord en mar-2013 (TR en abr-2012). **Reinhart-Rogoff se cumplió en magnitud (−55%), no en duración. El dólar era la cobertura del inversionista mexicano.**
- **2010, *flash crash* (C).** El 6-may, en unos 36 minutos, el Dow cayó 998.5 puntos (~9%) por una gran venta de E-mini agravada por la retirada del HFT (SEC/CFTC) [22]. El S&P cerró −3.24%. La corrección por Grecia fue de −16.0%, recuperada en nov-2010. **Órdenes límite, nunca *stops* a mercado.**
- **2011, euro y rebaja de EUA (F/E).** Contagio a España e Italia; EUA pasó de AAA a AA+ el 5 y 6 de agosto [23]. S&P −6.66% el 8-ago y −19.4% de máximo a mínimo. Protegió el **Tesoro rebajado** (TLT **+31.9%**), además del oro y el CHF. USD/MXN +22.2%. **El refugio es la liquidez en dólares, no la calificación.**
- **2015, CHF y CNY (C/F).** El SNB quitó el piso de 1.20 el 15-ene. El franco saltó 20-30% en minutos y los clientes de FXCM quedaron con **US$225 millones** en saldos negativos [24]. El 11-ago China devaluó el yuan 1.9%. El 24-ago el Dow abrió −1,089 puntos [25]. S&P −14.2% (may-2015 a feb-2016). USD/MXN +25.7%. **Un piso cambiario es una opción vendida por el banco central, y el salto rompe los *stops*.**
- **Feb-2018, *Volmageddon* (C).** El VIX pasó de 17.31 a 37.32 (**+116%**). XIV perdió **−96%** y lo terminaron; SVXY −91% [26]. El S&P perdió −10.2% en 13 días. **No protegieron** el TLT (−4.0%) ni el oro (−2.6%). **Nunca tener un producto que por diseño tiene que comprar al cierre lo que está vendiendo.**
- **2020, COVID (E).** S&P **−33.9% en 33 días**. −11.98% el 16-mar, con el VIX cerrando en **82.69**, récord. Protegieron el TLT (+14.1%) y el USD/MXN (**+33.1%**). **No** protegieron el oro (−2.5%) ni BTC (−33.4%). Récord el 18-ago-2020. **El S&P TR en MXN solo perdió −17.2% y recuperó el 26-mar-2020** (cálculo propio). **La crisis más rápida se recuperó rápido porque la política respondió: rebalancear en pánico pagó.**
- **2021, memes y Archegos (A/G).** Melvin perdió −53% en enero [27]. GME −88.5% y ARKK −81.1%, sin recuperar (cálculo propio). Archegos dejó pérdidas bancarias de más de US$10 mil millones (Credit Suisse 5.5, Nomura ~2) a través de *swaps* [28]. **La concentración apalancada detrás de derivados no aparece en los reportes de tenencias.**
- **2022 (D/C/G).** S&P −25.4% en 282 días, récord en ene-2024. **TLT −30.5%**, oro −6.8%, BTC −58.8%. El peso se apreció, así que **el S&P TR en MXN perdió −28.9%**, más que en USD. LDI: el mini-presupuesto del 23-sep subió el gilt a 30 años **+200 pb** y el BoE compró £19.3 mil millones [29]. Terra perdió ~US$40 mil millones en mayo. FTX quebró el 11-nov con un faltante de ~US$8 mil millones [30]. BTC −76.6%, recuperado en mar-2024. **Cuando el problema es la inflación, los bonos no cubren. La cripto es riesgo apalancado con riesgo de contraparte.**

### 5.2 México

- **1982 (F).** Moratoria de agosto sobre ~US$80 mil millones de deuda y nacionalización bancaria con control de cambios el 1-sep [42]. La caída bursátil no se verificó. **Inferencia:** con control de cambios, los dólares dentro del sistema local dejan de ser dólares seguros.
- **1987.** La BMV tuvo un auge y un desplome en octubre (magnitud no verificada; no hay datos diarios antes de 1991 en la fuente).
- **1994-95, Tequila (F).** Tesobonos de US$1.8 mil millones (1993) a US$16.1 mil millones (1994), con la Fed apretando. Devaluación el 20-dic y flotación el 22-dic. El peso pasó de ~3.4 a **7.2 por dólar** [41]. IPC **−49.4% en pesos** (8-feb-1994 a 27-feb-1995; cálculo propio); en USD ~−70% (inferencia aritmética, no verificado). PIB −6.2%, inflación de 52%, desempleo de 3.9% a 7.4%. Rescate de ~US$50 mil millones, pagado antes de tiempo [41]. El récord nominal del IPC llegó en ene-1996, pero con 52% de inflación fue una ilusión. **La cobertura es tener activos en USD fuera del sistema local.**
- **2008 (B importado con descalce cambiario).** IPC **−48.6%** (oct-2007 a oct-2008), recuperado en ene-2010. **En USD −64.8%**, recuperado en ene-2011. El USD/MXN pasó de 9.87 a 15.53 (**+57%**; cálculo propio). El FMI estima pérdidas por derivados de las empresas mexicanas en **~US$5 mil millones** [43]. Comercial Mexicana entró a concurso mercantil por derivados cambiarios (monto y fecha no verificados). Cemex compró Rinker (oferta de US$14.2 mil millones), quedó con ~US$14 mil millones de deuda y vendió Australia en 2009 [44]. El ADR CX perdió **−90%** entre jun-2007 y mar-2009 y nunca recuperó (cálculo propio). **Vender opciones sobre el dólar para "ganar *carry*" es venta de volatilidad escondida, y una compra apalancada en el pico puede ser una pérdida permanente.**
- **2016 (E).** El USD/MXN subió **+8.65%** el 9-nov y llegó a **21.92** el 19-ene-2017. El IPC perdió −6.4% en 4 días (cálculo propio). **El mundo cubre el riesgo de México vía el peso: el golpe llega primero al tipo de cambio.**
- **2020.** El USD/MXN pasó de 18.54 a 25.34 (+36.6%). El IPC perdió −36.3% desde su máximo de 2017 y recuperó en ago-2021. **En USD perdió −63.9% (abr-2013 a mar-2020) y tardó 12.8 años en recuperar (12-ene-2026)** (cálculo propio).
- **2024 (F doméstico).** El IPC perdió **−6.1%** el 3-jun, tras la elección. El USD/MXN pasó de 16.31 (abr) a **20.65 (nov), +26.6%**. El IPC perdió −16.8% (feb a dic) y recuperó en may-2025 (cálculo propio). **El riesgo institucional se transmite por el peso: el USD amortiguó.**

### 5.3 Matriz de refugios (cálculo propio, del máximo al mínimo del S&P)

| Episodio | S&P | IPC | Oro | TLT | USD/MXN | BTC | VIX máx. |
|---|---|---|---|---|---|---|---|
| GFC | −56.8% | −46.7% | **+24.5%** | **+17.7%** | **+43.5%** | — | 80.9 |
| 2011 | −19.4% | −10.4% | +6.4% | **+31.9%** | **+22.2%** | — | 48.0 |
| 2015-16 | −14.2% | −6.1% | +3.6% | +11.1% | **+25.7%** | +61.3% | 40.7 |
| Feb-2018 | −10.2% | −6.3% | −2.6% | −4.0% | +2.1% | −26.0% | 37.3 |
| 4T-2018 | −19.8% | −16.4% | +5.1% | +3.6% | +6.2% | −37.4% | 36.1 |
| COVID | −33.9% | −26.6% | −2.5% | **+14.1%** | **+33.1%** | −33.4% | 82.7 |
| 2022 | −25.4% | −13.7% | −6.8% | **−30.5%** | −2.0% | −58.8% | 36.5 |
| Ago-2024 | −8.5% | −4.8% | −0.9% | +4.9% | **+10.2%** | −17.1% | 38.6 |
| Abr-2025 | −18.9% | −7.0% | +1.8% | +0.2% | +2.3% | −21.1% | 52.3 |
| Irán 2026 | −9.1% | −2.6% | **−11.0%** | −1.2% | +4.5% | −25.2% | 31.0 |

**Grado B** (n chica, ventanas *ex post*):
- **USD/MXN** subió en 9 de 10 episodios; la excepción fue 2022, con el *carry*.
- **Tesoro largo** cubre en crisis deflacionarias y falla en choques de tasas o inflación (2018, 2022, 2026).
- **Oro** cubrió en 2008 y 2011 y falló en 2020, 2022 y 2026.
- **BTC** cayó más que el S&P en 6 de 8, igual en COVID; solo subió en 2015-16.
- **El IPC en pesos** cayó menos que el S&P en los 10 episodios, en parte porque el peso se deprecia.

### 5.4 Lente MXN: S&P 500 TR en pesos (cálculo propio)

| Episodio | TR en USD | TR en MXN | Recuperación en MXN |
|---|---|---|---|
| GFC | −55.3% | **−36.6%** | feb-2011 |
| 2018 | −19.4% | −18.3% | jul-2019 |
| COVID | −33.8% | **−17.2%** | **26-mar-2020** |
| 2022 | −24.5% | **−28.9%** | jun-2024 |
| 2025 | −18.7% | **−20.1%** | oct-2025 |

El dólar amortigua las crisis globales de aversión al riesgo (tipos B, C, E y F). La amplifica cuando el choque fortalece al peso: *carry* (2022) o debilidad del dólar originada en EUA (2025). El *benchmark* de 50% S&P en MXN y 50% CETES ya trae esta cobertura.

### 5.5 Qué funciona y qué no

| Idea | Evidencia | Grado |
|---|---|---|
| Comprar tras un pico de VIX. Primer cierre ≥30 después de 180 días sin tocarlo (1990-2025, n=16): S&P TR a 12 meses con mediana de **+21%**, positivo 12 de 16 veces. Con ≥40 (n=9): mediana de **+23.6%**, 7 de 9. En 2008 hubo otra caída de −38% a −42% | Cálculo propio, dentro de muestra, solo EUA | B |
| Comprar después de un año de −50% (P(duplicarse en 5 años) = 32.8%) | Goetzmann | B |
| Vender un sector solo porque subió 100% | −5 pp a 1 año (GSY) | D |
| Vender con características y pasar a libre de riesgo | ~+10 pp a 2 años, poco poder estadístico | B |
| Ponerse corto en una burbuja identificada | +30% promedio hasta el pico | D |
| Tesoro largo como cobertura universal | Falló en 2018, 2022 y 2026 | C |
| USD como cobertura en MXN | 9 de 10 episodios | A/B |
| Oro como cobertura de *crash* | Falla en liquidaciones | C |
| Volatilidad vendida o *carry* apalancado | −96% en un día (2018) | D (ruina) |

---

## 6. Traducción operable

> En fase 0 todo se ejecuta **en papel**. `arena_agresivo` aplica a la cuenta de competencia y `estándar` al patrimonio principal. Nada aquí modifica `parametros.json`; los valores nuevos van en 6.8 como propuesta.

### 6.1 Termómetro de burbuja (por sector o tema, mensual)

| Señal | Umbral | Puntos |
|---|---|---|
| *Run-up* | Rendimiento de 24 meses ≥100% **y** ≥100% neto del S&P (o del IPC) | Condición de entrada |
| *Run-up* extremo | ≥150% | +2 |
| Aceleración | Los últimos 12 meses rinden más que los 12 anteriores | +1 |
| Volatilidad | La de 6 meses es mayor que la de los 12-24 meses previos | +1 |
| Emisión | IPOs o colocaciones del tema en máximos de 3 años | +1 |
| Empresas jóvenes | Las de menos de 5 años de listado superan a las establecidas | +1 |
| CAPE | Decil superior de su historia | +1 |
| Crédito | Margen récord, *swaps* o crédito privado financiando el tema | +2 |

Con la condición de entrada y 0-1 puntos: **candidata** (~50% de probabilidad de *crash* a 2 años). Con 2-3: **alerta**. Con 4 o más: **burbuja probable** (~80% si además el alza es de 150%). Umbrales de GSY. Los puntos son una simplificación propia pendiente de *backtest* (cap. 07). **Grado B.**

### 6.2 Termómetro de fragilidad

- VIX ≥25 (se desactiva el filtro de apalancados).
- VIX ≥40 (capitulación histórica).
- Curva VIX/VIX3M mayor que 1.
- Yen apreciándose con el Nikkei cayendo.
- Índice bancario regional −20% en un mes.
- Redenciones de BDCs por encima de la compuerta.
- Correlación acciones-bonos a 3 meses positiva (régimen D).
- USD/MXN +5% en una semana.
- *Open interest* cripto en máximos con financiamiento extremo.

### 6.3 Clasificador en menos de 2 horas

1. ¿Inflación o tasas? → **D**.
2. ¿Solvencia de bancos o intermediarios? → **B** o **G**.
3. ¿Venta mecánica sin daño de solvencia? → **C**.
4. ¿Política, pandemia o guerra? → **E** (cap. 23).
5. ¿Tipo de cambio o deuda de un país? → **F**.
6. ¿Un tema con termómetro ≥2 que se desinfla? → **A**.

### 6.4 *Playbook*: señales → acciones

| # | Señal | `arena_agresivo` | `estándar` |
|---|---|---|---|
| 1 | Tema **candidata** | Sin compras apalancadas nuevas; tope del tema 0.30 (`accion_individual_max`) | Tope 0.25 (`sector_max`) |
| 2 | Tema en **alerta** | Recortar la exposición a la mitad; **el producto va a CETES, no al índice** (GSY) | Tope 0.125 |
| 3 | **Burbuja probable** | Residual ≤10%, con salida por tendencia (cap. 14). **Prohibido ponerse corto** | ≤5% |
| 4 | VIX ≥25 | `filtro_apalancados`: vender apalancados y no abrir nuevos | Sin apalancamiento (`bruto_max_fase_1` = 1.0) |
| 5 | VIX ≥40 al cierre, o S&P −20% | **No vender el núcleo.** Compras escalonadas en 3 tramos (hoy, +10 y +20 días hábiles) con CETES, dentro de los límites de pérdida | Rebalanceo por bandas (0.05) |
| 6 | Tipo C (VIX *pre-market*, *carry*, *flash crash*) | No operar las primeras 2 horas; solo órdenes límite | Igual |
| 7 | Tipo D | Refugio en CETES, no en el TLT | Duración menor a 1 año |
| 8 | Bancos −20% en un mes | Reducir financieras; verificar custodia segregada (GBM/Indeval, cap. 11) | Igual |
| 9 | Choque México (USD/MXN +5% en una semana o IPC −5% en un día) | **No vender dólares en pánico**; si las bandas lo piden, rebalancear **vendiendo el USD caro** | Igual |
| 10 | Choque de política reversible (E) | No vender en un día de −5%: el +9.52% de 2025 llegó 4 sesiones después | Igual |
| 11 | *Drawdown* de la cuenta | Al −12% reducir 50% la táctica; −20% sin apalancados; −28% pausa de 2 semanas y *post-mortem*; −35% todo a CETES | −8%, −12%, −15% y −20% |
| 12 | Límite de pérdida | 5% diario, 10% semanal, 18% mensual: sin tácticas nuevas | 2%, 4% y 6% |
| 13 | Cripto sobreapalancada | Tope 0.30 (`cripto_max`), sin margen; recortar a la mitad con el financiamiento en el percentil 95 | Tope 0.05 |

**Modo torneo.** Si la cuenta va **5 pp o más adelante** del mejor rival al entrar la crisis, se reduce la varianza: la regla 4 sin excepciones y un solo tramo de compra. Si va **5 pp o más atrás**, los tramos de la regla 5 son la forma de subir exposición con ventaja histórica (mediana de +21% a 12 meses). Nunca con apalancados antes de que pase el filtro.

### 6.5 Reentrada

1. **Apalancados:** solo con el subyacente sobre su media de 200 días y el VIX por debajo de 25.
2. **Tipo A:** no se recompra "porque ya cayó 50%" (en GSY los *crashes* promedian −42% a 2 años). Se exige tendencia positiva (cap. 14) y valuación.
3. **Tipo B:** se reconstruye en 4 a 6 tramos a lo largo de 6 a 12 meses (Reinhart-Rogoff).
4. **Tipos C y E:** de 1 a 3 tramos, porque la recuperación histórica fue de semanas (2010, 2018, 2020, 2024, 2025).
5. Cada decisión de crisis va al *ledger* de pronósticos con probabilidad y horizonte (cap. 08).

### 6.6 *Drawdowns* y recuperaciones del S&P 500 (precio)

Yardeni [13] hasta 2022; cálculo propio de 2023 a 2026. "Recuperación" = primer cierre en un nuevo máximo.

| Pico | Mínimo | Caída | Días | Récord | Tiempo total |
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

\* Pico local, todavía debajo del máximo de 2007. En TR, 2000-02 se recuperó el 23-oct-2006 y 2007-09 el 2-abr-2012. **Nikkei:** 38,915.87 (29-dic-1989) a 7,054.98 (10-mar-2009), **−81.9%**, con récord hasta el **22-feb-2024, 34 años después** (cálculo propio). "El índice siempre regresa" es sesgo de supervivencia de EUA.

### 6.7 *Drawdowns* y recuperaciones del IPC (precio, sin dividendos; cálculo propio)

| Pico | Mínimo | Caída en MXN | Récord en MXN | Contexto | En USD |
|---|---|---|---|---|---|
| 1-jun-1992 | 25-sep-1992 | −34.4% | 23-ago-1993 | 1992 | — |
| 8-feb-1994 | 27-feb-1995 | **−49.4%** | 2-ene-1996 (con 52% de inflación) | Tequila | ~−70% (inferencia) |
| 21-oct-1997 | 10-sep-1998 | −46.8% | 15-abr-1999 | Asia y Rusia | EWW −60.4% |
| 9-mar-2000 | 20-sep-2001 | −38.9% | 6-nov-2003 | Dot-com y 11-S | EWW −45.5% |
| 9-may-2006 | 13-jun-2006 | −23.7% | 20-sep-2006 | Emergentes | −27.7% |
| 18-oct-2007 | 27-oct-2008 | **−48.6%** | 7-ene-2010 | GFC | **−64.8%** (recupera ene-2011) |
| 5-ene-2011 | 8-ago-2011 | −18.0% | 26-mar-2012 | Euro | −28.3% |
| 28-ene-2013 | 20-jun-2013 | −18.3% | 3-sep-2014 | *Taper tantrum* | — |
| 25-jul-2017 | 23-mar-2020 | −36.3% | 18-ago-2021 | TLCAN y COVID | **−63.9%** desde abr-2013; recupera **12-ene-2026** |
| 1-abr-2022 | 30-sep-2022 | −21.2% | 14-dic-2023 | Tasas | — |
| 7-feb-2024 | 30-dic-2024 | −16.8% | 28-may-2025 | Elección y reforma judicial | — |
| 11-feb-2026 | 18-sep-2026 | −11.5% (en curso) | — | 2026 | −13.9% al mínimo |

**Regla:** en USD, el IPC tiene de las recuperaciones más largas de los mercados relevantes para el dueño. Es satélite táctico o de valor, **no núcleo de protección**.

### 6.8 Parámetros propuestos (para revisión)

```json
"crisis": {"runup_24m": 1.0, "runup_24m_neto_mercado": 1.0, "runup_extremo": 1.5,
  "puntos_alerta": 2, "puntos_burbuja": 4, "vix_capitulacion": 40,
  "compras_escalonadas_tramos": 3, "espaciado_dias_habiles": 10,
  "destino_salida_burbuja": "CETES", "pausa_horas_tipo_C": 2}
```

---

## 7. Trampas y errores comunes

1. **Llamar "burbuja" a un índice amplio.** Las burbujas medibles son sectoriales (GSY vs. Goetzmann).
2. **Ponerse corto en una burbuja bien identificada.** Hay +30% y ~6 meses hasta el pico, y Shiller se adelantó más de 3 años.
3. **Salir al índice en vez de a efectivo.** El mercado también cae cuando cae el sector (−42% a 2 años en los *crashes* de GSY).
4. **Medir con el índice nominal de precio.** El "25 años" de 1929 fueron ~7 con dividendos y deflación. El récord del IPC de 1996 venía con 52% de inflación.
5. **Suponer que los bonos siempre cubren.** Fallaron en 2018, 2022 y 2026.
6. **Suponer que el oro o bitcoin cubren un *crash*.** El oro cayó en la liquidación de 2020 y en 2026. BTC cayó más que el S&P en 6 de 8 episodios.
7. **Olvidar la moneda.** En 2020 el S&P cayó −17.2% en MXN, no −33.9%. En 2022 cayó más en pesos que en dólares.
8. **Reaccionar al VIX *pre-market*.** El 66 del 5-ago-2024 fue un artefacto de cotizaciones.
9. **Tener productos apalancados diarios o de volatilidad inversa en una crisis.** XIV −96% en un día.
10. **Usar *stops* a mercado en choques de liquidez.** 2010 y CHF 2015 (saldos negativos).
11. **Confundir la liquidez de ventanilla con liquidez real.** SVB, BDCs y LDI.
12. **Sobreestimar la probabilidad de *crash* por las noticias** (Goetzmann-Kim-Shiller). Quedarse fuera suele costar más que la caída.
13. **Sesgo de supervivencia.** Nikkei: 34 años. IPC en USD: 12.8 años.
14. **Leyes con n chica.** 40 episodios en GSY y 16 picos de VIX aquí.
15. **Contraparte.** FTX, FXCM y Archegos: el riesgo estaba en quien custodiaba o prestaba.

---

## 8. Examen de titulación

1. **GSY: ¿qué pasa después de un alza de 100% en 2 años?**
   El rendimiento promedio es ~0, pero P(*crash* ≥40%) = 53% (80% con 150%), contra 14% incondicional.
2. **¿Por qué vender todo *run-up* pierde a 1 año?**
   Porque 47% son falsos positivos y los verdaderos suben ~30% durante ~6 meses antes del pico: pierde ~5 pp.
3. **¿Qué características predicen el *crash* y cuál no sirve?**
   Aceleración, volatilidad, emisión, empresas jóvenes y CAPE. El *turnover* no sirve.
4. **Goetzmann: P(−50%) tras duplicarse en 1 año.**
   6.9% al año siguiente (contra 2.1%) y 17.2% a 5 años (contra 8.5%).
5. **¿Cómo se reconcilian GSY y Goetzmann?**
   Mercados completos con −50% contra industrias con −40% y alza neta de mercado. Las burbujas son sectoriales.
6. **¿Qué dice Pástor-Veronesi del Nasdaq de 1999?**
   La incertidumbre sobre la rentabilidad sube el valor. Con prima de riesgo baja, el pico era racionalizable y solo se vio como burbuja *ex post*.
7. **Reinhart-Rogoff después de una crisis bancaria.**
   Acciones −55% en ~3.5 años, vivienda −35% en ~6, desempleo +7 pp, PIB −9%, deuda +86%.
8. **¿Qué diferencia a una burbuja destructiva de una que no lo es?**
   El crédito (Jordà-Schularick-Taylor).
9. **Los teoremas de Minsky.**
   Hay regímenes estables e inestables, y la prosperidad prolongada lleva de cobertura a especulativa y Ponzi.
10. **¿Qué protegió a un inversionista en MXN en 9 de 10 episodios, y cuál fue la excepción?**
    El USD. La excepción fue 2022, con el peso fuerte por *carry*.
11. **¿Por qué el TLT falló en 2022 y cuándo sí cubre?**
    Porque el choque era de inflación (tipo D, −30.5%). Cubre en crisis deflacionarias: 2008 +17.7%, 2011 +31.9%, 2020 +14.1%.
12. **Caída y recuperación del S&P en 2020 y en 2025.**
    2020: −33.9% en 33 días, récord el 18-ago. 2025: −18.9% (19-feb al 8-abr), récord el 27-jun.
13. **¿Qué causó el pico del VIX del 5-ago-2024 según el BIS?**
    La ampliación de *spreads* en las cotizaciones de *puts*. No hay que operar con el VIX *pre-market*.
14. **¿Cuánto tardó el IPC en USD en recuperar su máximo de 2013?**
    Hasta el 12-ene-2026, 12.8 años (−63.9%). No es núcleo de protección.
15. **VIX al cierre ≥40 con la cuenta arena 5 pp atrás del mejor rival: ¿qué hace el sistema?**
    No vende el núcleo ni usa apalancados (el filtro exige VIX <25 y precio sobre la media de 200 días). Compra en 3 tramos con CETES dentro de los límites. La mediana histórica a 12 meses es de +21% a +24%, con el riesgo de un 2008 (−38% adicional).

---

## 9. Fuentes

1. Greenwood, Shleifer y You (2019), "Bubbles for Fama", *JFE*. NBER w23191: https://www.nber.org/papers/w23191 · PDF: https://www.nber.org/system/files/working_papers/w23191/w23191.pdf · JFE: https://www.sciencedirect.com/science/article/abs/pii/S0304405X1830254X
2. Goetzmann (2016), "Bubble Investing: Learning from History". NBER w21693: https://www.nber.org/papers/w21693 · PDF: https://www.nber.org/system/files/working_papers/w21693/revisions/w21693.rev1.pdf · NBER Digest: https://www.nber.org/digest/jan16/market-bubbles-what-goes-doesnt-always-come-down
3. Pástor y Veronesi (2009), "Technological Revolutions and Stock Prices", *AER* 99(4): https://www.aeaweb.org/articles?id=10.1257%2Faer.99.4.1451
4. Pástor y Veronesi (2006), "Was There a Nasdaq Bubble in the Late 1990s?", *JFE*. NBER w10581: https://www.nber.org/papers/w10581
5. Reinhart y Rogoff (2009), "The Aftermath of Financial Crises". NBER w14656: https://www.nber.org/papers/w14656
6. Reinhart y Rogoff (2008), "This Time is Different: A Panoramic View of Eight Centuries of Financial Crises". NBER w13882: https://www.nber.org/papers/w13882
7. Minsky (1992), "The Financial Instability Hypothesis", Levy WP 74: https://www.levyinstitute.org/pubs/wp74.pdf
8. Kindleberger, Aliber y McCauley, *Manias, Panics, and Crashes*: https://www.springerprofessional.de/en/manias-panics-and-crashes/24098366
9. Jordà, Schularick y Taylor (2015), "Leveraged Bubbles". NBER w21486: https://www.nber.org/papers/w21486
10. Goetzmann, Kim y Shiller, "Crash Beliefs from Investor Surveys". NBER w22143: https://www.nber.org/papers/w22143
11. Hirano, Kishi y Toda, "General-Purpose Technologies and Stock Market Bubbles", arXiv 2501.08215: https://arxiv.org/abs/2501.08215
12. Wang y Chen (2026), "Boom, Bubble, or Buildout?", arXiv 2606.01575: https://arxiv.org/abs/2606.01575
13. Yardeni Research, *Bull & Bear Markets* (ene-2024): https://old.yardeni.com/wp-content/uploads/BullBearTables.pdf
14. Federal Reserve History, "Stock Market Crash of 1929": https://www.federalreservehistory.org/essays/stock-market-crash-of-1929
15. Hulbert, "25 Years to Bounce Back? Try 4 1/2" (HNN): https://www.historynewsnetwork.org/article/mark-hulbert-25-years-to-bounce-back-try-4-12
16. Wikipedia, "1973–1974 stock market crash": https://en.wikipedia.org/wiki/1973%E2%80%931974_stock_market_crash
17. EBSCO, "Black Monday stock market crash": https://www.ebsco.com/research-starters/business-and-management/black-monday-stock-market-crash
18. Wikipedia, "1994 bond market crisis": https://en.wikipedia.org/wiki/1994_bond_market_crisis · EBC: https://www.ebc.com/forex/1994-bond-massacre
19. CRS, "The 1997-98 Asian Financial Crisis": https://sgp.fas.org/crs/row/crs-asia2.htm
20. Federal Reserve History, LTCM: https://www.federalreservehistory.org/essays/ltcm-near-failure · Wikipedia: https://en.wikipedia.org/wiki/Long-Term_Capital_Management · GAO: https://www.gao.gov/assets/ggd-00-67r.pdf
21. Wikipedia, "Dot-com bubble": https://en.wikipedia.org/wiki/Dot-com_bubble
22. Wikipedia, "2010 flash crash": https://en.wikipedia.org/wiki/2010_flash_crash · CNN (SEC/CFTC): https://money.cnn.com/2010/10/01/markets/SEC_CFTC_flash_crash/index.htm
23. Wikipedia, "August 2011 stock markets fall": https://en.wikipedia.org/wiki/August_2011_stock_markets_fall
24. Forbes (16-ene-2015), FXCM: https://www.forbes.com/sites/steveschaefer/2015/01/16/swiss-bank-stunner-claims-victims-currency-broker-fxcm-bludgeoned/ · Finance Magnates: https://www.financemagnates.com/forex/brokers/fxcm-publishes-data-of-snb-mishandling-of-the-swiss-franc/
25. CNN, yuan (11-ago-2015): https://money.cnn.com/2015/08/11/investing/china-pboc-yuan-devalue-currency/index.html · CNN (24-ago-2015): https://money.cnn.com/2015/08/24/investing/stocks-markets-selloff-china-crash-dow/index.html
26. CFA Institute FAJ (2021), "Volmageddon": https://rpc.cfainstitute.org/research/financial-analysts-journal/2021/volmageddon-failure-short-volatility-products · Six Figure Investing: https://www.sixfigureinvesting.com/2019/02/what-caused-the-february-5th-2018-volatility-spike-xiv-termination/
27. CNBC (31-ene-2021), Melvin: https://www.cnbc.com/2021/01/31/melvin-capital-lost-more-than-50percent-after-betting-against-gamestop-wsj.html
28. Wikipedia, Archegos: https://en.wikipedia.org/wiki/Archegos_Capital_Management
29. Chicago Fed Letter 480: https://www.chicagofed.org/publications/chicago-fed-letter/2023/480 · FMI WP 2023/210: https://www.elibrary.imf.org/view/journals/001/2023/210/article-A001-en.xml
30. Forbes, Terra: https://www.forbes.com/sites/lawrencewintermeyer/2022/05/25/from-hero-to-zero-how-terra-was-toppled-in-cryptos-darkest-hour/ · CBS, FTX: https://www.cbsnews.com/news/ftx-bankruptcy-sam-bankman-fried-resigns-cryptocurrency/
31. CNBC, Barr (28-mar-2023): https://www.cnbc.com/2023/03/28/svb-customers-tried-to-pull-nearly-all-deposits-in-two-days-barr-says.html · Fed OIG: https://oig.federalreserve.gov/reports/board-material-loss-review-silicon-valley-bank-sep2023.htm
32. BIS Bulletin 90: https://www.bis.org/publ/bisbull90.htm · BIS Bulletin 95: https://www.bis.org/publ/bisbull95.pdf
33. CNBC (5-ago-2024), Nikkei: https://www.cnbc.com/2024/08/05/asia-markets.html
34. CNBC (27-ene-2025), Nvidia: https://www.cnbc.com/2025/01/27/nvidia-sheds-almost-600-billion-in-market-cap-biggest-drop-ever.html
35. CNN (27-jun-2025): https://www.cnn.com/2025/06/27/investing/stock-market-record-dow-sandp · Wikipedia, "2025 stock market crash": https://en.wikipedia.org/wiki/2025_stock_market_crash
36. CoinDesk Research, liquidación de US$19 mil millones: https://www.coindesk.com/research/market-spotlight-the-19-billion-liquidation-that-shook-crypto
37. CNBC (30-ene-2026), metales: https://www.cnbc.com/2026/01/30/silver-gold-fall-price-usd-dollar-fed-warsh-chair-trump-metals.html · Mining.com: https://www.mining.com/gold-silver-prices-plunge-as-trumps-fed-chair-pick-triggers-selloff/
38. Bloomberg (4-feb-2026), "SaaSpocalypse": https://www.bloomberg.com/news/articles/2026-02-04/what-s-behind-the-saaspocalypse-plunge-in-software-stocks
39. CNBC (24-feb-2026), crédito privado: https://www.cnbc.com/2026/02/24/private-credit-3-trillion-boom-bankruptcies-fraud-blue-owl-redemptions-tricolor-first-brands-bdc.html · CNBC (2-abr-2026), Blue Owl: https://www.cnbc.com/2026/04/02/blue-owl-private-credit-funds-redemptions-requests.html · With Intelligence: https://www.withintelligence.com/insights/what-is-actually-going-on-in-bdc-portfolios/
40. CNN (4-ago-2026): https://www.cnn.com/2026/08/04/investing/us-stock-market
41. Wikipedia, "Mexican peso crisis": https://en.wikipedia.org/wiki/Mexican_peso_crisis · Wikipedia (es): https://es.wikipedia.org/wiki/Crisis_econ%C3%B3mica_de_M%C3%A9xico_de_1994 · Brookings: https://www.brookings.edu/articles/mexico-in-crisis-the-u-s-to-the-rescue-the-financial-assistance-packages-of-1982-and-1995/
42. *Revista de Historia Económica* (Cambridge), nacionalización bancaria de 1982: https://www.cambridge.org/core/journals/revista-de-historia-economica-journal-of-iberian-and-latin-american-economic-history/article/when-it-rains-it-pours-mexicos-bank-nationalisation-and-the-debt-crisis-of-1982/8A85C44DE3CC18702E2229E1468B2012 · BFI: https://bfi.uchicago.edu/wp-content/uploads/The-Case-of-Mexico.pdf
43. Dodd (2009), *Finance & Development*, FMI: https://www.imf.org/external/pubs/ft/fandd/2009/06/dodd.htm
44. Wikipedia, Cemex: https://en.wikipedia.org/wiki/Cemex
45. Yahoo Finance, API de gráficas (cierres diarios, descarga del 25-sep-2026): https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC (mismo *endpoint* para los demás *tickers*)
46. Progress.org, resumen de Kindleberger: https://www.progress.org/wiki/kindleberger-manias-panics-crashes/
47. Reinhart y Rogoff (2009), AER P&P (PDF): https://faculty.sites.iastate.edu/tesfatsi/archive/econ502/tesfatsion/AftermathOfFinancialCrisis.ReinhartRogoff.AER2009.pdf
