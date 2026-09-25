# 23 — Geopolítica y riesgo político global para inversionistas

> Nivel: experto · Actualizado 2026-09-25 · Grado global: **B** (la medición y los efectos promedio están bien documentados; el *timing* táctico alrededor de eventos es **C**)

Capítulos relacionados, que aquí no se repiten: [04 Renta fija y macro](04-maestria-renta-fija-tasas-macro.md) · [11 México](11-mexico-mercado-instrumentos-fiscalidad.md) · [Estado del mercado: tablero más reciente](../bitacora/briefs/) · [15 Eventos corporativos](15-eventos-corporativos-y-situaciones-especiales.md) · [16 Macro, FX y peso](16-macro-global-divisas-y-el-peso.md) · [17 Crisis](17-crisis-burbujas-libro-de-patrones.md) · [22 Fuentes de datos con IA](22-fuentes-de-datos-y-flujo-de-investigacion-con-ia.md) (11, 13 y 22 aún en redacción; verificar el nombre final del archivo). Los parámetros de riesgo salen de `config/parametros.json`.

**Convenciones.** Hecho = fecha y fuente. "Inferencia:" = razonamiento propio. "Regla:" = recomendación operable. "(no verificado)" = cifra no confirmada en esta sesión.

---

## 1. Objetivos de dominio

Al terminar este módulo el sistema debe poder:

1. Medir el riesgo geopolítico y político con índices estándar (GPR, EPU y PRisk a nivel empresa) y leer su nivel actual contra la historia.
2. Clasificar cualquier *shock* en menos de 2 horas en uno de cinco tipos, porque cada tipo tiene una reacción de mercado y un *playbook* distintos.
3. Distinguir la reacción típica, que es una caída de alrededor de 6% con recuperación en semanas, de la excepción que destruye capital: el choque de oferta de energía que cambia la política monetaria.
4. Saber qué activo protege en cada tipo de *shock* y cuándo falla. En 2025-2026 fallaron, en episodios distintos, el dólar, los Treasuries y el oro.
5. Estimar la exposición geopolítica de una empresa con datos de segmentos (10-K/20-F), cadena de suministro y reglas regulatorias. Es la "beta geopolítica".
6. Mantener un mapa de riesgos vigente con fuentes y probabilidades de mercados de predicción, sabiendo leer sus reglas de resolución.
7. Ejecutar un protocolo de 24 horas, 1 semana y 1 mes que sea coherente con los límites de `parametros.json`.
8. Convertir la ventaja comparativa del dueño (leer procesos de gobierno, calendarios legales y el comportamiento de funcionarios) en pronósticos calibrados sin cruzar la línea de la información privilegiada.

---

## 2. Marco teórico

### 2.1 Cuatro objetos distintos que se confunden

| Concepto | Qué mide | Medida estándar |
|---|---|---|
| Riesgo geopolítico | Amenazas y actos de guerra, terrorismo y tensiones entre Estados | GPR (Caldara-Iacoviello), separado en *threats* (GPRT) y *acts* (GPRA) |
| Incertidumbre de política económica | Incertidumbre sobre quién decide qué en impuestos, gasto, regulación, aranceles y política monetaria | EPU (Baker-Bloom-Davis) |
| Riesgo político a nivel empresa | La parte de la conversación de una empresa dedicada a riesgo político | PRisk (Hassan et al.), obtenido de transcripciones de *earnings calls* |
| Geoeconomía | Uso de aranceles, sanciones, controles de exportación y compras de Estado como armas | No hay un índice único. Se sigue por reglas del BIS/Commerce, USTR, MOFCOM y la OFAC |

### 2.2 Canales de transmisión a precios

1. **Tasa de descuento y prima de riesgo.** Sube la aversión al riesgo o la probabilidad percibida de desastre (*rare disasters*: Barro 2006; Berkman-Jacobsen-Lee 2011). El precio cae aunque los flujos no cambien. Este canal suele revertirse.
2. **Flujos de caja.** Los aranceles, las sanciones y la pérdida de mercados o de proveedores bajan las ventas y los márgenes. Es persistente y se concentra en empresas específicas.
3. **Commodities.** Una interrupción física de la oferta (Ormuz, Rusia, Qatar) redistribuye la riqueza de importadores a exportadores y de consumidores a productores.
4. **Reacción de política.** El *shock* de oferta sube la inflación, el banco central sube tasas y se castiga todo el *duration*, incluidos el oro y los Treasuries. Esta es la segunda ronda que destruye portafolios "defensivos".
5. **Derechos de propiedad y convertibilidad.** Las sanciones, los controles de capital y los *delistings* pueden llevar un activo a cero. No es volatilidad, es pérdida permanente.

### 2.3 Pastor-Veronesi: por qué la incertidumbre política se paga más en economías débiles

En el modelo de Pastor-Veronesi el gobierno cambia la política cuando la economía va mal. Eso funciona como un *put* implícito sobre el mercado, y la incertidumbre sobre qué hará el gobierno reduce el valor de ese *put*. Predicciones: (i) en promedio los precios caen cuando se anuncian cambios de política; (ii) la prima por incertidumbre política es mayor en economías débiles; (iii) la incertidumbre política vuelve las acciones más volátiles y más correlacionadas entre sí, lo que reduce los beneficios de diversificar justo cuando más se necesitan. Kelly-Pastor-Veronesi (2016) confirman en opciones que la protección que abarca elecciones y cumbres es más cara, y más aún con economía débil.

**Inferencia:** comprar protección *justo antes* de un evento programado (elección, cumbre, fallo judicial) significa pagar una prima que el mercado ya cobra. La protección barata se compra cuando nadie la quiere.

### 2.4 Amenaza contra acto

Caldara-Iacoviello encuentran que tanto la amenaza como la realización deprimen la inversión, y la extensión sobre inflación (2026) muestra que los actos tienen efectos mayores y más persistentes. En mercados, el patrón práctico es que la amenaza carga la prima de riesgo y el acto la descarga, salvo que el acto cambie un flujo físico. De ahí sale el refrán de "vender el rumor, comprar la invasión". El refrán funciona para los choques de incertidumbre y falla para los choques de oferta.

### 2.5 Taxonomía operable de *shocks* (núcleo del capítulo)

| Tipo | Ejemplo | Reacción típica en acciones | Qué protege | Qué falla |
|---|---|---|---|---|
| **A. Incertidumbre sin cambio de flujos** | 9/11 en su fase de mercado, Israel-Hamás oct-2023, Venezuela ene-2026 | Caída de −2% a −7%, recuperación en semanas | USD, Treasuries, CHF, JPY, oro (por días) | Vender en pánico |
| **B. Oferta de energía o commodities** | 1973, Rusia 2022, Irán/Ormuz 2026 | Caída inicial moderada. El daño viene con la segunda ronda de inflación y tasas | Energía, USD, *commodities*, defensa | Oro y Treasuries si suben las tasas reales (en 2026 el oro falló desde la tercera semana). JPY y CHF (se depreciaron contra el USD en mar-2026). También los importadores de energía |
| **C. Política comercial originada en EUA** | "Liberation Day" abr-2025 | Caída fuerte y rápida (−10% en 2 días). Revierte si la política se revierte | CHF, JPY, oro, Bund | USD y Treasuries (abr-2025) |
| **D. Sanciones o expropiación** | Rusia 2022: MOEX cerrada y activos rusos en índices valuados a cero | Pérdida permanente en los activos expuestos | Salir antes. No promediar a la baja | Cualquier tesis de "está barato" |
| **E. Desastre de cola** | Bloqueo o invasión de Taiwán (no ha ocurrido) | Desconocida y probablemente extrema en semis y tecnología | Sólo la cobertura puesta *antes* | Reaccionar después |

---

## 3. Literatura canónica

| Estudio | Hallazgo cuantificado o central | Enlace | Grado |
|---|---|---|---|
| Caldara & Iacoviello (2022), AER 112(4):1194-1225, "Measuring Geopolitical Risk" | Índice de noticias desde 1900. Un GPR más alto anticipa menor inversión y empleo, mayor probabilidad de desastre y más riesgo a la baja. Importan tanto la amenaza como el acto. La inversión cae más en industrias expuestas. **Magnitudes (adenda 2026-09-25, examen diagnóstico S5-07):** choque de 2 DE del GPR → inversión fija hasta **−1.5%** (~1 año después), horas trabajadas **−0.6%**, PIB **−0.3%** en el primer año (apéndice del artículo). Construcción: índice reciente desde 1985 con 10 periódicos (6 de EUA, 3 del RU, 1 de Canadá); histórico desde 1900 con 3 periódicos; 8 categorías de búsqueda, con las 1-5 formando el índice de amenazas (GPT) y las 6-8 el de actos (GPA); normalizado a media 100 en 1985-2019; auditoría humana de más de 7,000 artículos (correlación anual de 0.93) más un índice narrativo con 44,000 portadas del NYT. Tres picos mayores del índice reciente: Guerra del Golfo (ene-1991), 11-S (sep-2001) e invasión de Irak (mar-2003) | https://www.aeaweb.org/articles?id=10.1257/aer.20191823 | A (medición); B (efectos en retornos) |
| Caldara, Conlisk, Iacoviello & Penn (2026), JIE 159, "Do geopolitical risks raise or lower inflation?" | En 44 economías desde 1900, el GPR anticipa **más inflación y menor actividad**, más gasto militar, más deuda y menos comercio. Los *acts* tienen efectos mayores y más persistentes que los *threats* | https://www.matteoiacoviello.com/research_files/JIE_2026.pdf | A-/B |
| Baker, Bloom & Davis (2016), QJE, "Measuring Economic Policy Uncertainty" | Con empresas, la EPU se asocia con más volatilidad de la acción y menos inversión y empleo en sectores sensibles a la política (defensa, salud, finanzas, infraestructura). A nivel macro, las innovaciones de EPU anticipan caídas de inversión, producto y empleo (EUA y un panel de 12 países). **Magnitudes y probabilidad de desastre (adenda 2026-09-25, examen diagnóstico S5-07):** una innovación del tamaño del alza de 2005-06 a 2011-12 (~90 puntos) anticipa caídas de ~6% en la inversión bruta, ~1.1% en la producción industrial y ~0.35% en el empleo. +1 DE de EPU/GPR global ≈ **+18 pp** de probabilidad de desastre (especificación sin efectos fijos); el GPR por país eleva la probabilidad de inicio de un desastre de **~2.2% a ~9%**. Construcción del EPU de EUA: frecuencia de artículos en 10 periódicos grandes que contienen un término de cada grupo {economic, economy} × {uncertain, uncertainty} × {Congress, deficit, Federal Reserve, legislation, regulation, White House}; escalado por el total de artículos del mes, estandarizado a DE unitaria y normalizado a media 100 en 1985-2009; validado con auditoría humana de ~12,000 artículos (correlación 0.86 trimestral 1985-2012, 0.93 anual 1900-2010). **EPU de México (policyuncertainty.com/mexico_monthly.html):** construido con El Norte, Reforma (desde ene-1996) y Mural (desde ene-1999, con imputación previa), con la misma lógica E-U-P en español, estandarizado a DE unitaria y normalizado a media 100 en **1996-2016** | https://www.policyuncertainty.com/ | A (medición); B (efectos) |
| Pastor & Veronesi (2012), JF 67(4):1219-1264, "Uncertainty about Government Policy and Stock Prices" | Los precios caen en promedio al anunciarse cambios de política. La caída es mayor con más incertidumbre o si al cambio lo precede una recesión corta o poco profunda. Después suben la volatilidad y las correlaciones, y la prima por riesgo de salto es positiva | https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2012.01746.x | B |
| Pastor & Veronesi (2013), JFE 110(3):520-545, "Political Uncertainty and Risk Premia" | La prima por incertidumbre política es **mayor en economías débiles**. Las acciones se vuelven más volátiles y más correlacionadas. Baja el valor del *put* implícito del gobierno | https://www.nber.org/papers/w17464 | B |
| Kelly, Pastor & Veronesi (2016), JF 71(5):2417-2480, "The Price of Political Uncertainty" | Las opciones cuya vida abarca elecciones nacionales o cumbres globales son **más caras** porque protegen contra riesgo de precio, varianza y cola. El efecto es mayor con economía débil y se contagia entre países | https://www.nber.org/papers/w19812 | A- |
| Hassan, Hollander, van Lent & Tahoun (2019), QJE 134(4):2135-2202, "Firm-Level Political Risk" | PRisk se construye con transcripciones de *earnings calls*. Las empresas con más riesgo político **recortan contratación e inversión** y hacen más *lobbying* y donaciones. La mayor parte de la varianza es idiosincrática, no agregada | https://www.nber.org/papers/w24029 · datos: https://www.firmlevelrisk.com | A- (medición) |
| Berkman, Jacobsen & Lee (2011), JFE 101(2):313-332, "Time-varying rare disaster risk and stock returns" | Con 447 crisis internacionales entre 1918 y 2006 (base **International Crisis Behavior, ICB**; añadido 2026-09-25, examen diagnóstico S5-08), un índice de crisis afecta la **media y la volatilidad** de los retornos mundiales. El efecto es mayor con crisis severas o con grandes potencias involucradas. El riesgo de crisis se correlaciona con mayor E/P y dividend yield (precios bajos) y **se paga**: las industrias más sensibles rinden más en promedio. Evidencia directa de una probabilidad de desastre variable en el tiempo (Rietz; Barro; Gabaix; Wachter) | https://econpapers.repec.org/RePEc:eee:jfinec:v:101:y:2011:i:2:p:313-332 | B |
| Brogaard & Detzel (2015), Management Science 61(1):3-18, "The Asset-Pricing Implications of Government Economic Policy Uncertainty" (adenda 2026-09-25, examen diagnóstico S5-06) | El EPU predice positivamente el exceso de rendimiento del mercado: +1 DE de EPU ≈ +1.5% de rendimiento anormal esperado a 3 meses (≈6.1% anualizado), con caída contemporánea del precio. Las innovaciones de EPU tienen prima de riesgo negativa: entre los 25 portafolios de tamaño-momentum de Fama-French, el de mayor beta EPU rinde **5.53% anual menos** que el de menor beta, controlando por los 4 factores de Carhart y por volatilidad implícita/realizada | https://pubsonline.informs.org/doi/10.1287/mnsc.2014.2044 | B |
| Amiti, Redding & Weinstein (2019), JEP 33(4):187-210 | Traspaso prácticamente completo de los aranceles de 2018 a precios en EUA. Pérdida de ingreso real de **US$1.4 mil millones/mes** a fines de 2018 (confirmado en el resumen). Costo en impuestos: **alrededor de US$3 mil millones/mes** a nov-2018 según la versión NBER w25672 (Liberty Street, may-2019); la cifra de US$3.2 mil millones atribuida al texto de la revista **(no verificado)** | https://www.aeaweb.org/articles?id=10.1257/jep.33.4.187 | A |
| Fajgelbaum, Goldberg, Kennedy & Khandelwal (2020), QJE 135(1):1-55 | Pérdida para compradores de importaciones de **US$51 mil millones (0.27% del PIB)**. Neto de recaudación y ganancias de productores, la pérdida agregada fue de **US$7.2 mil millones (0.04%)**. Por las represalias, los trabajadores de sectores comerciables en condados muy republicanos fueron los más afectados | https://www.nber.org/papers/w25638 | A |
| Amiti, Kong & Weinstein (2020, NBER w27114) | Identifican 11 eventos de guerra comercial en 2018-2019. En la especificación base (ventanas de 7 días), los anuncios arancelarios de EUA y China bajaron las acciones de EUA **6.0 pp, unos US$1.7 billones** sobre una capitalización de US$28 billones. Con ventanas de 3 días la caída acumulada en los 7 eventos arancelarios fue de **9.7%**, y casi la mitad rebotó en días (sobrerreacción). La mayor parte del daño vino de los anuncios de EUA, no de las represalias chinas. Recorte de **1.9 pp** en el crecimiento de la inversión de las emisoras de EUA hacia 4T-2020 | https://www.nber.org/papers/w27114 | B+ |
| Baur & Lucey (2010), Financial Review 45(2):217-229 | El oro cubre acciones en promedio y funciona como *safe haven* en caídas extremas, pero la propiedad es de **corta duración** (resumen confirmado). La cifra de **unos 15 días hábiles** y la muestra 1995-2005 vienen del cuerpo del artículo **(no reverificado: Wiley respondió 403)** | https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6288.2010.00244.x | B |
| FMI, GFSR abr-2025, cap. 2 "Geopolitical Risks: Implications for Asset Prices" | Un *shock* de GPR de un país baja las acciones alrededor de **0.3%** de forma persistente por 2 años. Un *shock* severo (≥2σ) tiene un efecto unas **7 veces mayor**. Un *shock* global produce alrededor de **−1%** por un trimestre. A nivel empresa: **−1 pp** en el mes. En emergentes, los conflictos militares internacionales producen **alrededor de −5%**. Si el socio comercial principal entra en conflicto, **hasta −2.5 pp**. En los importadores de *commodities* el CDS soberano sube más de 1% en una semana, y en los exportadores baja | https://www.imf.org/en/Publications/GFSR/Issues/2025/04/22/global-financial-stability-report-april-2025 | A- (panel amplio, identificación recursiva) |
| Deutsche Bank Research (Jim Reid, jun-2025), 32 eventos geopolíticos | Mediana del S&P 500: **−6% en 17 días hábiles** y recuperación total en **16 días más**. A 12 meses, alrededor de **+15% desde el mínimo**. Excepción, el choque petrolero de 1973: **1,475 días hábiles** para recuperar y −28% adicional a 12 meses | https://www.aol.com/stocks-risk-iran-israel-conflict-104512973.html | B (muestra chica, sin costos) |
| LPL Research (2025-2026) | Guerras y operaciones militares: *drawdown* promedio de **alrededor de 7%**, recuperado en unos **55 días**. Eventos geopolíticos en general: retroceso promedio de **4.5%** (mediana **2.9%**) | https://www.lpl.com/research/blog/iran-escalation-how-markets-have-reacted-to-geopolitical-events.html **(no verificado: Cloudflare 403 en dos intentos y sin copia en Wayback; cifras de un resumen indexado)** | C |
| BCE, FSR nov-2025, *special feature* | En abr-2025 el USD **no funcionó como cobertura** para inversionistas no estadounidenses: cayó 12% contra el EUR en el año, 7 pp de ello después del 1-abr. El rendimiento a 10 años de EUA subió casi **50 pb** entre el 4 y el 11 de abril, la tercera mayor alza semanal desde 1986. CHF, JPY, oro y Bund sí actuaron como refugio | https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart202511_01~fdf147a04a.en.html | A- (descriptivo) |
| BIS, Quarterly Review sep-2025 | El S&P superó su máximo previo al estrés en **poco menos de 20 semanas**. Alrededor de **75%** del alza entre el mínimo del 9-abr y fines de julio se explicó por sorpresas **no arancelarias**. El minorista compró la caída y el institucional se retiró | https://www.bis.org/publications/qr-202509/understanding-swift-market-recovery-after-april-2025-tariff-shock | B+ |

---

## 4. Lo más reciente, 2023-2026

### 4.1 Lectura del GPR (dato primario descargado el 2026-09-25)

Archivo mensual oficial: https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls. Promedio 1985-2019 = 100.

| Mes | GPR | GPR *threats* | GPR *acts* |
|---|---|---|---|
| jun-2025 (guerra Israel-Irán de 12 días) | 222.6 | 288.2 | 183.7 |
| ene-2026 (Venezuela) | 168.6 | 220.2 | 100.2 |
| feb-2026 | 119.9 | 156.0 | 81.2 |
| **mar-2026 (guerra de Irán)** | **330.2** | 319.2 | **450.4** |
| abr-2026 | 250.3 | 268.6 | 305.9 |
| may-2026 | 203.6 | 233.5 | 215.2 |
| jun-2026 | 179.9 | 214.9 | 184.8 |
| jul-2026 | 167.5 | 190.9 | 180.7 |
| ago-2026 (último dato) | 117.9 | 130.7 | 120.3 |

Contexto histórico calculado con el mismo archivo: marzo de 2026 es el **6º mes más alto desde 1985**. Está por encima de mar-2022 (319.0, invasión de Ucrania) y por debajo de mar-2003 (358.7, Irak), ene-1991 (379.2, Golfo) y sep/oct-2001 (498.6/512.5). Índices por país en 2026 contra su promedio 1985-2019: Taiwán 0.529 en may-2026 contra 0.04 (unas 13 veces), México 0.261 en may-2026 contra 0.095 (unas 2.7 veces), EUA 8.68 en mar-2026 contra 2.32.

**Inferencia:** en agosto el GPR volvió a alrededor de 118 con la guerra sin resolver y Ormuz sin tráfico normal. Ese mes hubo una pausa militar (Wikipedia, "2026 Iran war"; Polymarket dio por cumplido un "effective ceasefire" de 2 semanas el 12-ago) y los futuros del Brent operaron entre US$79 y US$94; el Brent volvió a pasar de US$100 en septiembre, cuando el GPR todavía no lo registraba. El GPR mide **atención de prensa**, no daño económico ni flujos físicos; no sirve como señal de "ya pasó" en un *shock* tipo B.

### 4.2 Choque arancelario de abril de 2025 (tipo C)

- 2-abr-2025: arancel base de 10% más tasas "recíprocas" para unos 60 países. En dos sesiones el S&P perdió alrededor de **10%**, el Nasdaq alrededor de 11% y se borraron **US$6.6 billones** (resumen de Wikipedia, "2025 stock market crash"). El VIX cerró en **52.33** el 8-abr y el S&P marcó su mínimo de cierre en **4,982.77** ese mismo día (ambos confirmados en FRED). Del cierre del 2-abr (5,670.97) al del 4-abr (5,074.08) la caída fue de 10.5%.
- Lo anómalo fue que el dólar cayó y los rendimientos de los Treasuries subieron (BCE). Los refugios que funcionaron fueron CHF, JPY, oro y Bund.
- La reversión llegó con la pausa del 9-abr y la tregua con China del 12-may (BIS). El máximo previo se superó en menos de 20 semanas.
- Epílogo legal: el **20-feb-2026** la Suprema Corte anuló por 6-3 los aranceles IEEPA (*Learning Resources v. Trump*, ponencia de Roberts), con unos **US$166 mil millones** en reembolsos en proceso vía el sistema CAPE de la CBP (Greenberg Traurig, may-2026); a julio se habían pagado unos US$81 mil millones (Wikipedia). A fines de febrero entró un arancel global de 10% bajo la **Sección 122**; Wikipedia reporta que luego subió a 15%, el máximo legal **(no verificado en fuente primaria)**. La CIT lo declaró ilegal el 7-may-2026 (2-1), el Circuito Federal suspendió el fallo el 12-may, y el arancel **expiró por ley a la medianoche del 23-jul-2026** al cumplir 150 días. A las 12:01 a.m. del 24-jul entraron aranceles de la **Sección 301 "forced labor"** (investigación sobre si cada país prohíbe importar bienes hechos con trabajo forzoso): 10% para quien lo prohíbe y 12.5% para quien no, para 60 socios, sin fecha de expiración. México y Canadá quedaron en 10%, y los bienes que califican para el T-MEC están **exentos** (Holland & Knight, jul-2026).

**Inferencia (ventaja del dueño):** los plazos legales, como los 150 días de la Sección 122, los calendarios de la Suprema Corte y de la CIT o las revisiones anuales del T-MEC, son información pública que el mercado procesa mal. Quien entiende cómo se decide dentro del gobierno puede anticipar el **instrumento de reemplazo** (se sabía que habría un sustituto de la Sección 122 antes del 24-jul), aunque no pueda anticipar el titular.

### 4.3 La guerra de Irán de 2026 (tipo B): el caso de estudio del ciclo

Cronología (verificada el 2026-09-25; precios del Brent = cierre del futuro *front-month* salvo que se diga "spot"):
- **28-feb-2026:** ataques conjuntos de EUA e Israel ("Operation Epic Fury"; la israelí, "Roaring Lion"). Brent previo: **US$72.48** (cierre del 27-feb).
- **2 a 4-mar:** cierre de Ormuz. Wikipedia ("Economic impact of the 2026 Iran war") fecha el cierre el **4-mar**; el anuncio de la Guardia Revolucionaria del 2-mar dirigido a EUA y aliados **(no verificado)**. Con los buques atrapados en el Golfo, QatarEnergy declaró *force majeure* en sus contratos de GNL a inicios de marzo. El TTF casi se duplicó a más de €60/MWh hacia mediados de marzo.
- **18-mar:** Irán golpea el complejo de Ras Laffan, que ya estaba inactivo por el cierre; reducción de 17% de capacidad y el GNL spot en Asia sube más de 140% (Wikipedia).
- **31-mar:** Brent en **US$118.35**, el cierre más alto del futuro. El mercado físico estaba mucho más tenso: el Brent **spot** (EIA vía FRED) tocó **US$138.21 el 7-abr**. La AIE lo llamó "la mayor interrupción de oferta en la historia del mercado petrolero" (citado por Wikipedia).
- **8-abr:** alto al fuego de dos semanas (Polymarket resolvió "US x Iran ceasefire" ese día); las pláticas de Islamabad del 12-13 de abril fracasaron. Irán volvió a bloquear el paso el 19-abr.
- **Junio:** memorándum para terminar la guerra firmado el **17-jun** (Wikipedia); que tuviera 14 puntos y una ventana de 60 días **(no verificado)**. El mercado de Polymarket "US x Iran permanent peace deal by June 15" resolvió **Sí** (cerró el 18-jun). El Brent bajó a **US$71.57 el 1-jul**.
- **7/8-jul:** colapsa el alto al fuego (Wikipedia lo fecha el 8-jul, tras ataques iraníes a buques comerciales en Ormuz). Bloqueo naval estadounidense.
- **Agosto:** pausa militar. Polymarket dio por cumplido un "effective ceasefire" (definido como pausa de 2 semanas) el 12-ago; el mercado "US ceasefire against Iran continues through Aug 31" resolvió No el 30-ago. Otra pausa efectiva se dio por iniciada a principios de septiembre (resuelta el 15-sep).
- **11-sep (viernes):** drones atacan el oleoducto saudí Este-Oeste (Petroline), que movía de 4 a 5 millones de b/d desviados de Ormuz hacia Yanbu. **Nadie lo reivindicó**; analistas lo atribuyen a grupos proiraníes que operan desde Irak (lanzamiento desde Maysan), no a los hutíes (Al Jazeera, 12-sep). Arabia Saudita lo cerró "por precaución" sin estimar la duración ("es difícil decirlo"); la cifra de "semanas" fuera de servicio **(no verificado)**. El futuro del Brent cerró en US$104.61 el 11-sep; el spot llegó a **US$130.80 el 15-sep**.
- **23/24-sep:** el Brent cerró en **US$103.08 el 23-sep** (+42% contra la preguerra) y en **US$106.60 el 24-sep**. Hubo un solo tránsito comercial en Ormuz el 20-sep, contra un promedio de alrededor de 85 diarios antes de la guerra, y 396 buques esperando al 23-sep; funcionarios de EUA afirman, en cambio, que fluye 60-70% del petróleo previo a la guerra. Irán mantiene una pausa voluntaria (15 días sin misiles balísticos contra países anfitriones y 19 sin drones), no un alto al fuego formal; presentó un plan de alto al fuego regional de hasta 60 días con reapertura por fases y fin del bloqueo, con un ultimátum de "4 a 5 días" (vence alrededor del 27-28 de sep). Fuente: GlobalSecurity, parte del día 209 (24-sep).

Reacción de mercados:
- **S&P 500:** mínimo intradía de **6,316.91 el 30-mar** (−9.8% contra el máximo intradía de enero, Wikipedia). Al cierre, la caída fue de **−9.1%**: de 6,978.60 (27-ene) a 6,343.72 (30-mar), según FRED. Marcó **récord de cierre el 15-abr (7,022.95)**, unos 46-47 días después del inicio de la guerra y a 16 días del mínimo. En 2026 lleva **27 cierres récord** (el último, 7,798.99 el 13-ago) y cerró agosto en alrededor de +12% a +13% en el año (cálculo propio con FRED). Cerró en 7,704.13 el 24-sep. La IA, casi la mitad de la capitalización, "corrió con dinámica propia".
- **Emergentes importadores de energía:** el KOSPI cayó hasta 12% intradía el 4-mar con *circuit breaker*, y el KSE-100 de Pakistán perdió 9.57% el 2-mar (Wikipedia).
- **Peso mexicano:** −4.02% en marzo, con máximo de 18.13 por dólar el 27-mar y cierre de mes en 17.93 (El Informador, 31-mar). Banxico recortó 25 pb a 6.75% el **26-mar**; después bajó a 6.50% y ahí la mantuvo el 24-sep (Banxico).
- **Oro:** récord de **US$5,589.38 el 28-ene-2026**, luego **US$4,369.19 al 1-sep (−21.8%)** (CBS, 1-sep). El futuro COMEX cerró en US$4,298 el 24-sep; el spot de US$4,250.85 citado antes **(no verificado)**. El oro no sirvió ni en la fase aguda: el futuro cayó de US$5,311.60 (2-mar) a US$4,376.30 (26-mar), −17.6% en tres semanas. **Inferencia:** el mercado pasó de inmediato a descontar inflación, alza de tasas y dólar fuerte; CBS cita tasas y dólar como presiones, no una causa única.
- **Treasuries:** el rendimiento a 10 años llegó a 4.46% el 27-mar (Wikipedia; 4.44% en la serie de FRED) y siguió subiendo: **5.11% el 23-sep-2026** (FRED). La **Fed subió 25 pb el 16-sep-2026 a 3.75-4.00%** por unanimidad (12-0), su primera alza desde julio de 2023; el comunicado cita inflación "elevada" (FOMC, 16-sep). **Kevin Warsh** preside la Junta de Gobernadores (sitio de la Fed). Que 16 de 18 miembros vean otra alza **(no verificado: CNBC bloqueó la descarga)**.
- **Divisas refugio:** entre el 27-feb y el 27/31-mar el dólar se apreció contra el yen (156.05 a 160.16) y contra el franco suizo (0.7686 a 0.8027 CHF por USD), según FRED. En este *shock* tipo B **el USD fue el refugio y el JPY y el CHF no**. Posibles intervenciones del SNB en 2026 **(no verificado)**. El VIX tocó su máximo del año en 31.05 el 27-mar.

**Lecciones (Inferencia):**
1. Las acciones de EUA recuperaron rápido porque las utilidades de IA dominaron el índice. El promedio de Deutsche Bank se cumplió **en el índice**, no en los emergentes importadores ni en los activos de *duration*.
2. El daño de un *shock* tipo B llega **con meses de rezago**, por inflación, luego la Fed y luego las tasas reales (el 10 años pasó de 4.4% en marzo a 5.1% en septiembre). Quien compró oro "por la guerra" al inicio (alrededor de US$5,250-5,300 en futuros) perdía 18-19% al 24-sep; quien lo compró en el mínimo de marzo apenas perdía 2%.
3. El dólar funcionó en los primeros días (Wikipedia) y en todo marzo subió contra MXN, JPY y CHF (FRED). Para un inversionista en MXN, tener dólares amortiguó el golpe.
4. Los activos que sí cubrieron fueron energía, transporte de crudo y GNL, y los exportadores fuera del Golfo (inferencia coherente con el FMI: el *shock* de *commodities* favorece al sector energía).

### 4.4 Rusia-Ucrania: 2022 como plantilla y 2026 como estado

- **2022:** el futuro del Brent cerró en US$127.98 el 8-mar-2022 y el spot (EIA) en US$133.18 ese día. El máximo intradía de US$139.13 del 7-mar **(no verificado en fuente primaria**; la serie continua de Yahoo marca US$137.00). El níquel de la LME superó **US$100,000/t**; la bolsa suspendió la negociación el 8-mar y canceló entre 5,000 y 9,000 operaciones con valor de **US$3.9 a 12 mil millones** (OFR WP 24-09, Heilbron, dic-2024). Según el FMI, las empresas con subsidiarias en Rusia o Ucrania cayeron **2.5 pp** en una semana.
- **2026:** no hay alto al fuego general. El mercado de Polymarket "Russia x Ukraine ceasefire by end of 2026" resolvió Sí el 9-may, lo que es consistente con la tregua del 9 al 11 de mayo. La tregua de 32 horas de Pascua ortodoxa (11-abr), el alto ordenado por Ucrania del 5 al 8 de septiembre ante la visita de Witkoff y Kushner, la exigencia rusa de todo el Donbás, la advertencia de Tusk (17-sep-2026) sobre ataques híbridos "accidentales" contra la OTAN y el paso de 3 a 36 estaciones con interferencia de GPS en Lituania: **(no verificado en esta ronda)**. Eurasia Group sí incluye "Russia's second front" como riesgo #5 de 2026.

### 4.5 EUA-China: tregua corta, chips y tierras raras

- La tregua de Busan (30-oct-2025, cumbre APEC) se extendió en la cumbre de Pekín de mayo de 2026. El **24-sep-2026**, al llegar Xi a Washington (tercer encuentro en menos de un año), se extendió **sólo 2 meses**: la prohibición china de exportar tierras raras queda aplazada **hasta el 10-ene-2027** (Al Jazeera, 24-sep). Que el mercado esperara 6 meses o más **(no verificado)**; los analistas citados por Al Jazeera la ven como una extensión "teatral".
- Aranceles vigentes: **36.5%** de EUA a China y **31%** de China a EUA (CRS jul-2026, citado por Al Jazeera). China tiene alrededor de 60% de los depósitos y alrededor de 90% del procesamiento de tierras raras (Al Jazeera). Que mantenga licencias lentas y selectivas, haya sancionado a la Responsible Business Alliance en agosto y que sus exportaciones de tierras raras a EUA cayeran antes de la cumbre (Chin@Strategy e Invezz, 21-sep) **(no verificado en esta ronda)**.
- Chips: la regla del BIS anunciada el **13-ene-2026** y publicada en el Federal Register el **15-ene-2026** (2026-00789) pasó el H200, el MI325X y equivalentes de "presunción de negación" a **revisión caso por caso** para China y Macao, con condiciones: suministro suficiente en EUA, que los envíos a China no pasen de **50% de lo enviado a clientes en EUA**, procedimientos de seguridad y **pruebas de terceros en EUA**. El arancel de 25% **no forma parte de esa regla**; se atribuye a una medida separada de Sección 232 sobre ciertos chips avanzados **(no verificado en esta ronda)**. El 10-Q de Nvidia (26-ago-2026) confirma que desde feb-2026 EUA otorgó licencias para "pequeñas cantidades" de H200, pero **el gobierno chino restringió esas compras**; Nvidia registró un cargo de US$0.4 mil millones por inventario de H200, lo enviado es menos de 1% de sus ingresos de Data Center del trimestre y se declara "efectivamente excluida" del mercado chino de centros de datos. La cifra de alrededor de 10 mil H200 para ByteDance y Tencent cada una **(no verificado**; es difícil de conciliar con el "<1%" del 10-Q). El acuerdo EUA-Taiwán de ene-2026 con arancel máximo de 15% y trato preferente de 232 a cambio de inversión en fábricas en EUA **(no reverificado: commerce.gov respondió 403)**.
- China-Japón: tras los dichos de la primera ministra Takaichi sobre Taiwán (nov-2025), China impuso el **6-ene-2026** restricciones a la exportación a Japón de bienes de uso dual, incluidas tierras raras e imanes permanentes. Japón dependía de China para 63% de sus importaciones de tierras raras en 2024 (CSIS).

### 4.6 Taiwán y la concentración de semiconductores

- Polymarket, "Will China invade Taiwan by end of 2026?": **3.75%**, con US$42.8 millones de volumen (API de Polymarket, 25-sep-2026). La regla exige una ofensiva militar para controlar cualquier porción del territorio administrado por Taiwán, incluidas islas habitadas. "China bloquea Taiwán en 2026": 3.65%. La venta de armas de EUA por US$11.1 mil millones en dic-2025, el comentario de Trump sobre incluir las ventas de armas en la negociación con Xi y los simulacros taiwaneses con drones en septiembre **(no verificado en esta ronda)**.
- Que TSMC mantenga su tecnología más avanzada al menos **dos generaciones** por delante de lo que produce fuera de Taiwán y que operar en EUA cueste **50% o más** **(no verificado**: no aparece en el 20-F 2025 de TSMC, presentado el 16-abr-2026, que sólo habla de "mayores costos" de la expansión global). **Inferencia:** un portafolio cargado en IA y semis tiene una exposición implícita a Taiwán (tipo E) que no aparece en el 10-K como "ingresos por región".

### 4.7 OPEP+, petróleo y Venezuela

- **Los EAU salieron de la OPEP el 1-may-2026** (anuncio del 28-abr). Producían 3.4 millones de b/d en 2025; sin ellos, la participación de la OPEP+ en la producción mundial de 2025 habría sido de alrededor de 42% en vez de 46% (EIA, 23-jun-2026). Los EAU planean duplicar hacia 2027 la capacidad del oleoducto de Abu Dabi (1.8 millones de b/d), que evita Ormuz. La meta de producir 5 millones de b/d en 2027 **(no verificado)**.
- El 2-ago-2026, siete países de la OPEP+ (Arabia Saudita, Rusia, Irak, Kuwait, Kazajistán, Argelia y Omán) acordaron un ajuste de **+188 mil b/d para septiembre** a cuenta de los recortes voluntarios de abril de 2023 y mantener reuniones mensuales (la siguiente, el 6-sep). Que con eso se complete el retiro de esos recortes y que haya cuotas estables el resto de 2026 **(no verificado**: el comunicado no lo dice).
- **Venezuela, 3-ene-2026:** EUA capturó a Maduro, pero el Brent *bajó* a alrededor de US$60 (el futuro cerró en US$59.96 el 7-ene) por la sobreoferta: barriles nuevos de Brasil, Guyana, Argentina y EUA, y una AIE que proyectaba exceso de hasta 2 millones de b/d en 2026 (Al Jazeera, 5-ene). El S&P marcó récord el 6-ene. Lección: un evento geopolítico sin pérdida de oferta, en un mercado con exceso, no mueve el precio.

### 4.8 China, Europa, India y EUA

- **China:** el pronóstico de crecimiento para 2026 de 4.3% a 4.8% (consenso, UBS y Goldman), los indicadores inmobiliarios entre 50% y 80% debajo del pico de 2020-2021 y más de 3 años de deflación del PPI **(no verificado en esta ronda)**. Eurasia (#7 "China's deflation trap") espera que China siga exportando deflación y que eso desate respuestas antidumping.
- **Europa:** diferencial OAT-Bund a 10 años de alrededor de **105 pb**, el primero arriba de 100 desde 2012 (resumen de CNBC, 24-sep-2026) **(no verificado**: CNBC bloqueó la descarga; con datos mensuales de la OCDE en FRED el diferencial promedió 82 pb en ago-2026, 4.00% contra 3.18%, así que 105 pb implicaría una ampliación de más de 20 pb en septiembre). La deuda francesa proyectada de 119.3% del PIB en 2026 **(no verificado)**; la pelea presupuestal amenaza con tumbar otro gobierno. Alemania ejecuta su paquete fiscal de infraestructura y defensa. Eurasia #4: "Europe under siege".
- **India:** el acuerdo del 2-feb-2026 que bajó el arancel recíproco de 25% a 18% y retiró el castigo de 25% por petróleo ruso, y la ubicación actual de India en el grupo de 10% de la Sección 301 **(no verificado en esta ronda**: CNBC respondió 403).
- **EUA:** Eurasia #1 es "US political revolution" y #6 "State capitalism with American characteristics", es decir, un gobierno que elige ganadores y perdedores. Elecciones intermedias del 3-nov-2026: Polymarket da a los demócratas **92.5% para la Cámara** y **62.5% para el Senado** (API, 25-sep-2026); a mediados de septiembre la prensa reportaba 89-90% y 55-60% (CNBC y Econbrowser, no reverificado). "D Senado y D Cámara": 62.5%; "R Senado y D Cámara": 28.5%.
- **Norteamérica (detalle en el cap. 11):** en la revisión del **1-jul-2026** EUA **no** renovó el T-MEC, lo que activa revisiones anuales hasta su vencimiento el 1-jul-2036 (Wikipedia; la nota de White & Case respondió 403). Eurasia #9: "Zombie USMCA". Que Trump dijera el 9-ene-2026 que EUA empezaría a "golpear en tierra" a los cárteles en México **(no verificado en esta ronda)**. Eurasia #3: "The Donroe Doctrine".

### 4.9 Encuestas institucionales de riesgo 2026

- **Eurasia Group Top Risks 2026** (5-ene-2026): 1 US political revolution · 2 Overpowered (China, electrones, contra EUA, moléculas) · 3 The Donroe Doctrine · 4 Europe under siege · 5 Russia's second front · 6 State capitalism with American characteristics · 7 China's deflation trap · 8 AI eats its users · 9 Zombie USMCA · 10 The water weapon. Las "red herrings" (riesgos que considera sobrevalorados): "Tariff Man at large", desglobalización, esferas de influencia y "sell America".
- **WEF Global Risks Report 2026** (ene-2026): **confrontación geoeconómica** es el riesgo #1 por severidad a 2 años, **8 lugares arriba** del año anterior, seguido de desinformación, polarización social, clima extremo y conflicto armado entre Estados. Además, 18% de los encuestados la eligió como el riesgo más probable de detonar una crisis global material en 2026 (**2 posiciones arriba**), seguida del conflicto armado entre Estados con 14% (informe en PDF).
- **BlackRock Geopolitical Risk Dashboard** (actualizado ago-2026): "la fragmentación geopolítica se acelera" por el conflicto en Medio Oriente, la competencia tecnológica EUA-China y las tensiones comerciales, y el conflicto en Irán "ha afectado a casi todos los países y regiones" (verificado). La lista y el orden del top 10, la subida de la seguridad energética a riesgo alto y la frase "mayor crisis energética desde los setenta" **(no verificado**: la tabla es dinámica y no se pudo extraer; tampoco los valores del BGRI).

---

## 5. Evidencia real: cuánto cae, cuánto tarda y qué protege

### 5.1 Magnitudes de referencia (S&P 500)

| Fuente o caso | Caída | Días al mínimo | Recuperación |
|---|---|---|---|
| Deutsche Bank, mediana de 32 eventos | −6% | 17 días hábiles | 16 días hábiles más |
| LPL, guerras y operaciones militares (no verificado) | −7% promedio | — | alrededor de 55 días |
| LPL, eventos geopolíticos en general (no verificado) | −4.5% promedio (mediana −2.9%) | menos de 1 mes | — |
| Choque petrolero de 1973 (DB) | profundo | — | **1,475 días hábiles** |
| Aranceles, abr-2025 | −10.5% en 2 días (cierre mínimo 4,982.77 el 8-abr) | 4 sesiones desde el anuncio | máximo previo superado en menos de 20 semanas (BIS) |
| Guerra de Irán, 2026 | −9.1% al cierre (−9.8% intradía) desde el máximo de enero | 30 días desde el inicio (30-mar) | récord de cierre el 15-abr |
| Venezuela, ene-2026 | casi nula | — | — |

**Grado de esta tabla: B.** Son muestras chicas, sin costos, con sesgo de supervivencia (se mira el S&P, no el índice de un país invadido) y dominadas por un mercado cuyo peso en IA en 2026 no tiene precedente. El FMI corrige la parte internacional: en emergentes un conflicto militar internacional cuesta alrededor de **5%**, cinco veces más que el promedio.

### 5.2 Matriz de refugios

| Activo | Funciona cuando | Falla cuando | Evidencia 2022-2026 |
|---|---|---|---|
| **USD** | *Shock* global que no nace en EUA. Primeros días de un choque energético | El *shock* nace en la política de EUA | Subió en los primeros días de la guerra de Irán. Cayó más de 4% en abr-2025 y 12% contra el EUR en el año (BCE) |
| **Treasuries largos** | *Shock* de demanda o desinflacionario | Choque de oferta inflacionario o *shock* de credibilidad de EUA | +47 pb en una semana en abr-2025 (4.01% a 4.48%, FRED). El 10 años llegó a 4.44-4.46% en mar-2026 y a **5.11% el 23-sep-2026**; la Fed subió tasas en sep-2026 |
| **Oro** | Los primeros días en un *shock* tipo A o C (Baur-Lucey: efecto de corta duración). *Shocks* de credibilidad del USD | Suben las tasas reales o se fortalece el dólar. Horizontes de meses | Funcionó en abr-2025 (BCE). En la guerra de Irán cayó 17.6% en 3 semanas de marzo y −21.8% entre el 28-ene y el 1-sep-2026 |
| **CHF** | Estrés europeo o *shock* nacido en EUA | Choque global de energía en que gana el USD (2026). Intervención del SNB (no verificado para 2026) | Se apreció en abr-2025 (BCE). En mar-2026 se depreció 4.4% contra el USD (FRED) |
| **JPY** | *Shock* de riesgo con *carry trade* desarmándose | Choque de petróleo, porque Japón importa energía | Se apreció en abr-2025 (BCE). En mar-2026 se depreció alrededor de 2.6% contra el USD (156.05 a 160.16, FRED) |
| **Energía y *commodities*** | Tipo B | Tipo A con sobreoferta (Venezuela 2026) | 2022 y 2026 |
| **MXN** | Casi nunca protege. Es moneda de riesgo | — | −4.02% en mar-2026 (El Informador) |

**Regla para una cuenta en MXN:** la exposición en dólares es la cobertura natural contra el tipo A y el tipo B. Contra el tipo C originado en EUA, esa cobertura puede no funcionar, y conviene tener parte en oro o en activos no USD (el detalle está en el cap. 16).

### 5.3 Mercados de predicción: evidencia de 2026 sobre su calibración

- Kalshi, 4-may-2026: tráfico "normal" en Ormuz **antes de octubre: 62%**. Al 25-sep, Polymarket da **8.5%** a "normal al 31-oct" y **88.5%** a que el promedio diario de tránsitos al 30-sep esté entre 0 y 5. La regla de "normal" exige un promedio móvil de 7 días de al menos 60 tránsitos en IMF PortWatch. La probabilidad fue demasiado optimista durante meses.
- Polymarket "Russia x Ukraine ceasefire by end of 2026" **resolvió Sí** el 9-may (US$14.5 millones de volumen) con una **tregua de 3 días**. La regla pedía un acuerdo oficial, público y mutuo de "pausa general"; no exigía que durara.
- Polymarket "US x Iran permanent peace deal by June 15" **resolvió Sí** (18-jun) y la guerra se reanudó tres semanas después. "Permanent" en el título no garantizaba permanencia en la realidad.
- El 25-sep Polymarket da **98.3%** a "US x Iran ceasefire continues through September 25", mientras GlobalSecurity dice que no hay alto al fuego formal. No es contradicción: esa familia de mercados define el "effective ceasefire" como una **pausa de 2 semanas**, que es exactamente la pausa iraní que describe GlobalSecurity.
- Las sospechas de *insider trading* en los mercados sobre Irán documentadas por Bloomberg **(no verificado en esta ronda)**.
- **Regla:** un mercado de predicción es un *prior* útil y barato. Antes de usarlo hay que leer (1) la regla exacta de resolución, (2) el volumen y (3) si hay ventaja informativa de *insiders*. Grado para uso táctico: **C**.

---

## 6. Traducción operable

### 6.1 Árbol de clasificación (menos de 2 horas desde el evento)

1. **¿Se interrumpe un flujo físico de más de 2% de la oferta mundial** de petróleo, gas, grano, metales críticos o chips avanzados? Si es así, candidato a **tipo B** (o E si es Taiwán).
2. **¿El *shock* nace en la política de EUA** (aranceles, Fed, instituciones)? Si es así, **tipo C**: no contar con el USD ni con los Treasuries como refugio.
3. **¿Afecta derechos de propiedad o convertibilidad** (sanciones, controles de capital, *delisting*)? Si es así, **tipo D**: salir de lo expuesto y no promediar.
4. **¿Es amenaza o acto?** Una amenaza negociable es reversible. Hay que tener presente la reversión de política ("pausa del 9-abr").
5. Si ninguna de las anteriores aplica: **tipo A**.

Umbrales de confirmación para el tipo B: el Brent sube más de 25% en 10 días hábiles, la curva entra en *backwardation* fuerte, las *breakevens* de inflación suben y los futuros de Fed/Banxico dejan de descontar recortes. Umbrales de estrés: GPR mensual arriba de 200 es elevado, y arriba de 300 es extremo (8 meses desde 1985: ene y feb-1991, sep, oct y nov-2001, mar-2003, mar-2022 y mar-2026; cálculo con el archivo oficial). VIX arriba de 25 apaga los ETFs apalancados (`filtro_apalancados`).

### 6.2 Protocolo

**Primeras 24 horas**
- [ ] No enviar órdenes en los primeros 30 a 60 minutos de la apertura. Sólo órdenes limitadas.
- [ ] Clasificar el *shock* (6.1) y escribir en la bitácora el tipo y la tesis en tres líneas.
- [ ] Revisar el tablero: Brent, TTF, oro, DXY, USD/MXN, UST 10 años, VIX, CDS de México, futuros de Fed y la probabilidad en Polymarket o Kalshi (leyendo la regla).
- [ ] Listar las posiciones con exposición directa (ver 6.4) y calcular su pérdida con un escenario de −10% a −20% por nombre.
- [ ] Ante un tipo D, reducir de inmediato lo expuesto. Ante un tipo A, B o C, **no vender el núcleo por el titular**.
- [ ] Verificar los límites: cuenta arena con pérdida diaria de 5%, semanal de 10% y 3% de riesgo por operación. Perfil estándar: 2% diario y 1% por operación. Si se toca un límite, se congela la parte táctica.

**Primera semana**
- [ ] Tipo A: compra escalonada en tercios **sólo si la tesis de fondo no cambió**, en los días 3-5, 10-15 y alrededor de 20 (cerca de la mediana de DB de 17 días hábiles al mínimo). Cada tramo cuenta dentro del máximo de 8 operaciones al mes en la arena.
- [ ] Tipo B: activar el *playbook* de estanflación. Menos *duration*, nada de oro "por la guerra" si suben las tasas reales, más energía y exportadores de energía fuera de la zona de riesgo y dólar. Evitar los emergentes importadores de energía.
- [ ] Tipo C: vigilar la **reversibilidad**, es decir, el calendario de pausas, tribunales y negociaciones. La reversión ha sido la regla en 2025-2026 (pausa del 9-abr-2025, IEEPA anulado, treguas con China).
- [ ] Registrar un pronóstico calibrado (probabilidad y fecha) de la variable clave, por ejemplo "Ormuz normal al 31-dic". Se evalúa con Brier, con objetivo de 0.20 o menos según `pronosticos`.

**Primer mes**
- [ ] Revaluar los fundamentales con 8-K, prealertas de utilidades, *earnings calls* (contar menciones de "tariff", "sanction", "Hormuz" o "export control", al estilo de PRisk) y revisiones de consenso.
- [ ] Vigilar la segunda ronda: inflación, luego el banco central, luego las tasas reales. Aquí se decidió 2026.
- [ ] Hacer un *post-mortem*: ¿el tipo asignado fue correcto?, ¿funcionaron los refugios?

### 6.3 Mapeo de evento a sector (sin *tickers*)

| Evento | Presión negativa | Presión positiva | Nota México |
|---|---|---|---|
| Cierre o bloqueo de Ormuz o del Mar Rojo | Aerolíneas, química, transporte, emergentes de Asia importadores de energía, consumo discrecional | Productores de crudo y GNL fuera del Golfo, *tankers*, defensa | Pemex exporta crudo e importa refinados (no verificado en esta sesión); el peso se deprecia en *risk-off* |
| Bloqueo de Taiwán | Semiconductores, *hardware*, IA, autos (chips) | Defensa, fundidoras fuera de Taiwán (relativo), oro por días | Manufactura de electrónicos en México: ambigua |
| Alza de aranceles de EUA | Importadores y minoristas con proveeduría en Asia, autos, exportadores a EUA | Productores domésticos protegidos | T-MEC: lo que califica está exento de la 301 |
| Controles de chips o represalia con tierras raras | Diseñadores de chips con ventas a China, autos y defensa (imanes) | Minería y procesamiento de tierras raras fuera de China | — |
| Escalada Rusia-OTAN | Acciones europeas, energía europea (TTF) | Defensa europea, CHF | — |
| *Shock* institucional de EUA (Fed, tribunales) | Treasuries largos, USD | Oro, CHF | El peso puede resistir si el *shock* es del dólar (Inferencia) |

### 6.4 Beta geopolítica: cómo medirla

1. **Exposición de ingresos.** Usar la nota de segmentos y geografía del 10-K (ASC 280) o del 20-F e IFRS 8. Ejemplo real: Apple reportó ventas en **Greater China de US$64,377 millones** en su año fiscal 2025, −4% anual (10-K FY2025). Ahí se miden directamente las represalias y los boicots.
2. **Exposición de suministro.** Ubicación de proveedores críticos, fábricas y licencias. Apple declara manufactura principalmente en China, India, Japón, Corea, Taiwán y Vietnam. Esto no aparece en ingresos pero pesa igual o más.
3. **Exposición regulatoria.** Listas del BIS (*Entity List*), licencias de exportación, sanciones de la OFAC, aranceles 232 o 301 del producto y listas de control de China (MOFCOM).
4. **Beta estadística.** Regresión semanal de retornos contra el mercado y contra los *shocks* del GPR o de EPU, o *event betas* en eventos canónicos (24-feb-2022, 2-abr-2025, 2-mar-2026). El FMI calcula el costo marginal: por exposición de ingresos o subsidiarias, de −0.1 a −0.25 pp adicionales; por subsidiarias en el país en conflicto, alrededor de −2.5 pp en una semana.

**Puntaje propuesto (heurística, grado C, sin validar fuera de muestra):** `Beta_geo = 0.4·%ingresos en jurisdicción de riesgo + 0.4·%suministro crítico en jurisdicción de riesgo + 0.2·bandera regulatoria (0/1)`. **Regla propuesta, que no está en `parametros.json` y que el dueño debe aprobar:** no más de 25% del portafolio (el mismo `sector_max`) en nombres con `Beta_geo` mayor a 0.3 respecto de **una misma** jurisdicción (China, Taiwán o el Golfo).

### 6.5 Monitoreo diario (conectar con el cap. 22)

- **Índices:** GPR diario y mensual (matteoiacoviello.com/gpr.htm), EPU (policyuncertainty.com), PRisk (firmlevelrisk.com), BlackRock BGRI.
- **Probabilidades:** Polymarket y Kalshi, siempre leyendo la regla de resolución.
- **Flujos físicos:** IMF PortWatch (tránsitos por estrechos), Lloyd's List, EIA (STEO y *This Week in Petroleum*), el reporte mensual de la AIE, el MOMR de la OPEP y el TTF.
- **Reglas:** Federal Register, BIS, USTR, avisos CSMS de la CBP, OFAC, MOFCOM y el DOF.
- **Conflictos:** ISW (Rusia-Ucrania), CFR Global Conflict Tracker, ACLED y CSIS.
- **Empresas:** búsqueda de texto completo en EDGAR ("Strait of Hormuz", "export control", "rare earth") en 8-K y 10-Q.

### 6.6 Mapa de riesgos vigente al 25-sep-2026

| Foco | Estado verificado | Mercado de predicción (25-sep-2026) | Canal principal | Qué vigilar |
|---|---|---|---|---|
| **Irán, Ormuz y Mar Rojo** | Día 209 de la guerra. Bloqueo de EUA. Pausa iraní voluntaria, sin alto al fuego formal. Un tránsito el 20-sep. Petroline cerrado desde el ataque del 11-sep, sin fecha de reapertura. Brent: US$103.08 (23-sep) y US$106.60 (24-sep) | Ormuz normal al 31-dic: **22.5%**. Fin del bloqueo anunciado al 31-dic: **61.7%**. EUA invade Irán antes de 2027: **14.5%**. Caída del régimen antes de 2027: **6.5%**. Acuerdo nuclear final al 31-dic: **12.5%**. Bab el-Mandeb cerrado al 31-dic: **18.5%** (API de Polymarket, 25-sep) | Tipo B, en su segunda ronda (inflación y Fed) | Ultimátum iraní del 27-28 de sep, tránsitos en PortWatch, reparación de Petroline, curva del Brent |
| **EUA-China** | Tregua extendida sólo hasta el **10-ene-2027**. Aranceles de 36.5% y 31%. Tierras raras con licencias lentas | — | Tipo C/D en tecnología | Licencias de tierras raras, H200, listas del BIS y MOFCOM |
| **Taiwán** | Sin crisis militar. Taiwán teme ser moneda de cambio | Invasión antes de 2027: **3.75%** (US$42.8 millones). Bloqueo en 2026: 3.65% | Tipo E | Anuncios sobre venta de armas, ejercicios del EPL, lenguaje de las cumbres |
| **Rusia-Ucrania y OTAN** | Sin alto al fuego. Guerra híbrida en aumento | El mercado de alto al fuego 2026 ya resolvió Sí por una tregua de 3 días (no sirve como señal) | Tipo B en gas europeo y tipo A | Incidentes con drones en la OTAN, nuevos paquetes de sanciones de la UE |
| **Política de EUA** | Fed en 3.75-4.00%. Treasury a 10 años en 5.11% (23-sep). Aranceles 301 sin fecha de fin. Elecciones intermedias el 3-nov | Cámara demócrata **92.5%**. Senado demócrata **62.5%** (Polymarket, 25-sep) | Tipo C | Fallos del Circuito Federal y de la Suprema Corte, independencia de la Fed |
| **Norteamérica y México** | Revisiones anuales del T-MEC. Arancel 301 de 10% con exención T-MEC. Amenaza de ataques a cárteles | — | Tipo C para el peso y los exportadores | Rondas bilaterales con USTR (ver cap. 11) |
| **Europa** | OAT-Bund en alrededor de 105 pb (no verificado; 82 pb promedio en agosto). Presupuesto francés en disputa. Rearme | — | Tipo A/C para el euro | Mociones de censura, calificaciones soberanas |
| **China doméstica** | Deflación del PPI por más de 3 años. Inmobiliario en su 5º año de caída | — | Deflación exportada | Medidas antidumping de terceros países |
| **OPEP+** | Salida de los EAU (1-may). +188 mil b/d en septiembre y reuniones mensuales | — | Oferta de crudo | Capacidad ociosa saudí, producción de los EAU |

---

## 7. Trampas

1. **Vender el titular.** La mediana se recupera en semanas; vender en el mínimo de un tipo A es el error más caro y frecuente.
2. **Extrapolar "comprar la guerra" a un tipo B.** En 1973 la recuperación tardó 1,475 días hábiles. En 2026 el índice se recuperó, pero el oro, los bonos y los emergentes importadores no.
3. **Creer que los refugios son constantes.** En abr-2025 fallaron el USD y los Treasuries, y en 2026 falló el oro. El refugio depende del tipo de *shock*.
4. **Leer el GPR como termómetro de daño.** En ago-2026 marcó 118 con Ormuz prácticamente cerrado: la pausa militar bajó la atención de prensa, pero el flujo físico no se recuperó y en septiembre el Brent volvió a pasar de US$100.
5. **Comprar protección cuando ya está cara.** Kelly-Pastor-Veronesi muestran que las opciones que abarcan eventos políticos cuestan más. La cobertura se pone con VIX bajo, no con VIX en 40.
6. **Confiar en una probabilidad sin leer la regla.** "Ceasefire" Rusia-Ucrania resolvió Sí por una tregua de 3 días; "permanent peace deal" EUA-Irán resolvió Sí tres semanas antes de que se reanudara la guerra; "ceasefire continues" significa una pausa de 2 semanas; y "Ormuz normal" exige un promedio de 7 días de al menos 60 tránsitos en IMF PortWatch.
7. **Confundir el pronóstico del evento con el pronóstico de la reacción.** Acertar que habría guerra con Irán no servía para ganar con acciones de EUA, que marcaron récord de cierre 46-47 días después.
8. **Concentración oculta.** La exposición a IA y semis es exposición a Taiwán. El 10-K no la muestra como ingresos.
9. **Olvidar el tipo de cambio.** Para un inversionista en MXN, un *shock* global suele ser positivo en pesos si tiene dólares, y un *shock* de EUA puede no serlo.
10. **Ignorar las reversiones de política.** En 2025-2026, casi toda medida comercial extrema se pausó, se anuló en tribunales o se sustituyó. Apostar a la permanencia del titular perdió.
11. **Confundir acceso político con ventaja de mercado.** La ventaja legítima del dueño es entender procesos, plazos e incentivos. Operar con información no pública obtenida por relaciones es información privilegiada, sancionada por la Ley del Mercado de Valores y la CNBV en México y por la SEC en EUA. Ese riesgo legal es operativo y no compensa ningún rendimiento.
12. **Doble conteo.** Berkman et al. muestran que el riesgo de crisis ya se paga en precios. Los riesgos conocidos, como Taiwán, están parcialmente descontados, y la ventaja está en el cambio de probabilidad, no en su nivel.

---

## 8. Examen de titulación

**1. ¿Qué mide el GPR y cuál es su principal limitación para un inversionista?**
Mide la frecuencia de palabras sobre tensiones geopolíticas en 10 diarios, con base 1985-2019 = 100, y se divide en amenazas y actos. Su limitación es que mide atención mediática, no daño económico. En ago-2026 marcó 118 con Ormuz cerrado, durante una pausa militar, justo antes de que el Brent volviera a pasar de US$100.

**2. Según Pastor-Veronesi (2013), ¿cuándo es mayor la prima por incertidumbre política y qué pasa con la diversificación?**
Es mayor en economías débiles. La incertidumbre política sube la volatilidad **y la correlación** entre acciones, así que la diversificación se debilita justo cuando más se necesita.

**3. ¿Qué encontraron Kelly-Pastor-Veronesi (2016) y qué implicación operativa tiene?**
Las opciones que abarcan elecciones o cumbres son más caras, sobre todo con economía débil. Comprar protección justo antes de un evento programado es pagar la prima completa. La cobertura se compra antes, cuando es barata.

**4. Da tres cifras de la tabla de Deutsche Bank y la excepción clave.**
Mediana de −6% en 17 días hábiles, recuperación total en 16 días más y alrededor de +15% a 12 meses desde el mínimo. Excepción: 1973, con 1,475 días hábiles para recuperar.

**5. ¿Por qué abril de 2025 rompió el manual de refugios?**
El *shock* nació en la política de EUA. El USD cayó (−7 pp contra el EUR después del 1-abr) y el rendimiento a 10 años subió casi 50 pb en una semana. Funcionaron CHF, JPY, oro y Bund (BCE, FSR nov-2025).

**6. En la guerra de Irán de 2026, ¿qué hizo el S&P 500 y qué hizo el oro? Explica la diferencia.**
El S&P cayó 9.1% al cierre (9.8% intradía) hasta el 30-mar y marcó récord de cierre el 15-abr, impulsado por las utilidades de IA. El oro cayó 17.6% en tres semanas de marzo y 21.8% entre su récord del 28-ene y el 1-sep. Inferencia: el choque de oferta subió la inflación esperada, el dólar se fortaleció, la Fed terminó subiendo tasas el 16-sep y el 10 años pasó de 4.4% a 5.1%. Es un tipo B con segunda ronda.

**7. Cuantifica la evidencia del FMI (GFSR abr-2025) para emergentes y para la exposición por socios comerciales.**
Un conflicto militar internacional cuesta alrededor de 5% en acciones de empresas de emergentes. Si el socio comercial principal entra en conflicto, hasta −2.5 pp. Por exposición de ingresos o subsidiarias, de −0.1 a −0.25 pp adicionales, y por subsidiarias en Rusia o Ucrania en 2022, −2.5 pp en una semana.

**8. ¿Qué concluyeron Amiti-Redding-Weinstein y Fajgelbaum et al. sobre quién paga los aranceles?**
El traspaso a precios de EUA fue prácticamente completo: alrededor de US$3 mil millones al mes en costo arancelario (versión NBER, nov-2018) más US$1.4 mil millones al mes de pérdida de ingreso real a fines de 2018. Fajgelbaum et al.: US$51 mil millones de pérdida para los compradores, y neto de recaudación y productores, US$7.2 mil millones (0.04% del PIB).

**9. ¿Cómo mide Hassan et al. (2019) el riesgo político de una empresa y qué hacen las empresas expuestas?**
Mide la proporción de la transcripción del *earnings call* dedicada a riesgo político, con lingüística computacional. Las empresas expuestas recortan inversión y contratación y aumentan el *lobbying* y las donaciones.

**10. Clasifica: (a) captura de Maduro en ene-2026; (b) aranceles del 2-abr-2025; (c) ataque a Ras Laffan y al Petroline en 2026; (d) exclusión de acciones rusas en 2022.**
(a) Tipo A: sin pérdida de oferta en un mercado con sobreoferta, el Brent bajó a alrededor de US$60. (b) Tipo C. (c) Tipo B. (d) Tipo D.

**11. ¿Cuánto tiempo actúa el oro como *safe haven* según Baur-Lucey (2010) y qué regla se deriva?**
Poco tiempo: el resumen dice que la propiedad es "de corta duración" y el cuerpo del artículo la ubica en alrededor de 15 días hábiles (cifra no reverificada). Regla: el oro táctico "por el evento" se revisa a las 3 semanas, y se deshace antes si suben las tasas reales o el dólar. En 2026 falló desde la tercera semana.

**12. Un mercado de Polymarket sobre "alto al fuego Rusia-Ucrania en 2026" resolvió Sí. ¿Significa que hubo paz? ¿Qué lección deja?**
No. Resolvió el 9-may por una tregua de 3 días. Lo mismo pasó con "US x Iran permanent peace deal", que resolvió Sí en junio antes de que la guerra se reanudara en julio. Lección: leer la regla de resolución, el volumen y el riesgo de *insiders* antes de usar cualquier probabilidad como insumo.

**13. Tu portafolio arena tiene 40% en ETFs de IA y semiconductores. ¿Qué riesgo geopolítico no aparece en los ingresos por región y cómo lo acotas?**
Concentración en Taiwán (tipo E) por dependencia de manufactura avanzada. Se acota así: medir la beta geopolítica por suministro; respetar `etf_indice_max` 0.6 y el tope de 25% en nombres con `Beta_geo` mayor a 0.3 hacia una misma jurisdicción (propuesta); cubrir con protección comprada con VIX bajo, no después del evento.

**14. Sucede un *shock*: el Brent sube 30% en 8 días hábiles y los futuros de la Fed eliminan los recortes. ¿Qué haces en la primera semana?**
Es un tipo B confirmado. Activar el *playbook* de estanflación: bajar *duration*, no comprar oro de forma automática si suben las tasas reales, favorecer energía fuera de la zona de riesgo y el dólar, evitar los emergentes importadores de energía, respetar los límites de pérdida (5% diaria en la arena) y registrar un pronóstico con fecha sobre la reapertura del flujo.

**15. ¿Cuál es la ventaja comparativa legítima de un ex alto funcionario en este campo y cuál es la línea que no se cruza?**
Entender procesos, plazos legales e incentivos burocráticos, por ejemplo anticipar que la Sección 122 expiraba a los 150 días y que habría un instrumento sustituto, o que una revisión del T-MEC sin extensión activa revisiones anuales. La línea: nunca operar con información no pública obtenida por relaciones, que es uso de información privilegiada.

---

## 9. Fuentes

**Académicas**
- Caldara & Iacoviello (2022), AER: https://www.aeaweb.org/articles?id=10.1257/aer.20191823
- Datos del GPR (descargados el 2026-09-25): https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls · https://www.matteoiacoviello.com/gpr.htm
- Caldara, Conlisk, Iacoviello & Penn (2026), JIE: https://www.matteoiacoviello.com/research_files/JIE_2026.pdf
- Baker, Bloom & Davis, EPU: https://www.policyuncertainty.com/
- Pastor & Veronesi (2013), JFE: https://www.nber.org/papers/w17464
- Kelly, Pastor & Veronesi (2016), JF: https://www.nber.org/papers/w19812
- Hassan, Hollander, van Lent & Tahoun (2019), QJE: https://www.nber.org/papers/w24029 · https://www.firmlevelrisk.com/download
- Berkman, Jacobsen & Lee (2011), JFE: https://econpapers.repec.org/RePEc:eee:jfinec:v:101:y:2011:i:2:p:313-332 (base International Crisis Behavior, ICB)
- Brogaard & Detzel (2015), Management Science: https://pubsonline.informs.org/doi/10.1287/mnsc.2014.2044
- Amiti, Redding & Weinstein (2019), JEP: https://www.aeaweb.org/articles?id=10.1257/jep.33.4.187
- Fajgelbaum et al. (2020), QJE: https://www.nber.org/papers/w25638
- Amiti, Kong & Weinstein (2020): https://www.nber.org/papers/w27114
- Baur & Lucey (2010), Financial Review: https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6288.2010.00244.x

**Institucionales**
- FMI, GFSR abr-2025, cap. 2: https://www.imf.org/-/media/Files/Publications/GFSR/2025/April/English/ch2.ashx
- BCE, FSR nov-2025: https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart202511_01~fdf147a04a.en.html
- BIS, QR sep-2025: https://www.bis.org/publications/qr-202509/understanding-swift-market-recovery-after-april-2025-tariff-shock
- Eurasia Group, Top Risks 2026: https://www.eurasiagroup.net/issues/top-risks-2026
- WEF, Global Risks Report 2026: https://www.weforum.org/stories/2026/01/global-risks-2026-top-10-two-and-ten-year-horizon/
- BlackRock, Geopolitical Risk Dashboard: https://www.blackrock.com/corporate/insights/blackrock-investment-institute/interactive-charts/geopolitical-risk-dashboard
- EIA sobre la salida de los EAU: https://www.eia.gov/todayinenergy/detail.php?id=67804
- OPEP, 2-ago-2026: https://www.opec.org/pr-detail/1854611-2-august-2026.html
- CRS sobre IEEPA: https://www.congress.gov/crs-product/LSB11398
- Commerce, acuerdo con Taiwán: https://www.commerce.gov/news/fact-sheets/2026/01/fact-sheet-restoring-american-semiconductor-manufacturing-leadership
- BIS sobre licencias de chips: https://www.bis.gov/press-release/department-commerce-revises-license-review-policy-semiconductors-exported-china
- Apple, 10-K FY2025: https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm
- Nvidia, 10-Q del 2T FY2027 (26-ago-2026): https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm
- TSMC, 20-F 2025 (16-abr-2026): https://www.sec.gov/Archives/edgar/data/1046179/000162828026025362/tsm-20251231.htm
- Federal Register 2026-00789, regla del BIS (15-ene-2026): https://www.govinfo.gov/content/pkg/FR-2026-01-15/html/2026-00789.htm
- FOMC, comunicado del 16-sep-2026: https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm
- Banxico, anuncios de política monetaria: https://www.banxico.org.mx/publicaciones-y-prensa/anuncios-de-las-decisiones-de-politica-monetaria/anuncios-politica-monetaria-t.html
- FRED (VIXCLS, SP500, DGS10, DCOILBRENTEU, DEXMXUS, DEXJPUS, DEXSZUS, DFEDTARU, IRLTLT01FRM156N, IRLTLT01DEM156N): https://fred.stlouisfed.org/
- OFR WP 24-09, Heilbron, "Central Clearing and Trade Cancellation" (dic-2024): https://www.financialresearch.gov/working-papers/2024/12/10/central-clearing-and-trade-cancellation/
- WEF, Global Risks Report 2026 (PDF): https://reports.weforum.org/docs/WEF_Global_Risks_Report_2026.pdf
- Amiti, Redding & Weinstein, NBER w25672 y Liberty Street Economics (may-2019): https://libertystreeteconomics.newyorkfed.org/2019/05/new-china-tariffs-increase-costs-to-us-households/

**Mercado y prensa (con fecha)**
- Deutsche Bank vía AOL/Business Insider (18-jun-2025): https://www.aol.com/stocks-risk-iran-israel-conflict-104512973.html
- LPL (2026): https://www.lpl.com/research/blog/iran-escalation-how-markets-have-reacted-to-geopolitical-events.html
- Economic impact of the 2026 Iran war: https://en.wikipedia.org/wiki/Economic_impact_of_the_2026_Iran_war
- GlobalSecurity, Iran War día 209 (24-sep-2026): https://www.globalsecurity.org/military/ops/iran-war-oprep.htm
- Al Jazeera, petróleo y Ormuz (ago-2026): https://www.aljazeera.com/economy/2026/8/12/oil-prices-rise-as-attacks-dent-hopes-for-strait-of-hormuz-reopening
- Al Jazeera, Petroline (12-sep-2026): https://www.aljazeera.com/news/2026/9/12/saudi-arabia-shuts-critical-oil-pipeline-after-drone-attack-what-happened
- CNN, récord del S&P (15-abr-2026): https://www.cnn.com/2026/04/15/investing/us-stocks-iran-war
- CBS, oro (sep-2026): https://www.cbsnews.com/news/golds-price-down-by-over-21-percent-where-will-it-head-september-2026/
- CNBC, Fed (16-sep-2026): https://www.cnbc.com/2026/09/16/fed-rate-decision-september-2026.html
- CNBC, tregua con China (24-sep-2026): https://www.cnbc.com/2026/09/24/us-china-trade-truce-bessent-trump-xi.html
- Al Jazeera, "Hostile but hooked" (24-sep-2026): https://www.aljazeera.com/news-analysis/2026/9/24/hostile-but-hooked-whats-behind-the-us-china-trade-truce-extension
- Holland & Knight, Sección 301 (jul-2026): https://www.hklaw.com/en/insights/publications/2026/07/and-the-tariff-beat-goes-on
- White & Case, T-MEC (jul-2026): https://www.whitecase.com/insight-alert/usmca-2026-joint-review-united-states-declines-extend-agreement-triggering-annual
- Greenberg Traurig, Sección 122 e IEEPA (may-2026): https://www.gtlaw.com/en/insights/2026/5/us-tariff-update-section-122-duties-found-unauthorized-by-law-ieepa-refunds-under-way
- CNBC, Francia (24-sep-2026): https://www.cnbc.com/2026/09/24/france-budget-debt-deficit-government.html
- CNBC, mercados de predicción y Senado (16-sep-2026): https://www.cnbc.com/2026/09/16/prediction-markets-say-democrats-are-slightly-favored-to-win-senate.html
- Polymarket, Irán: https://polymarket.com/iran · Ormuz: https://polymarket.com/iran/strait-of-hormuz · Taiwán: https://polymarket.com/event/will-china-invade-taiwan-before-2027 · Rusia-Ucrania: https://polymarket.com/event/russia-x-ukraine-ceasefire-before-2027 · API con reglas y precios (consultada el 25-sep-2026): https://gamma-api.polymarket.com/events?slug=strait-of-hormuz-traffic-returns-to-normal-by-december-31
- Wikipedia, 2026 Iran war: https://en.wikipedia.org/wiki/2026_Iran_war · Learning Resources v. Trump: https://en.wikipedia.org/wiki/Learning_Resources,_Inc._v._Trump · T-MEC: https://en.wikipedia.org/wiki/United_States%E2%80%93Mexico%E2%80%93Canada_Agreement- Kalshi, Ormuz (4-may-2026): https://news.kalshi.com/p/strait-of-hormuz-recovery-odds-2026
- El Informador, peso en marzo de 2026: https://www.informador.mx/economia/el-peso-mexicano-cae-en-marzo-por-guerra-en-iran-pero-mantiene-apreciacion-trimestral-20260331-0164.html
- Al Jazeera, Venezuela (5-ene-2026): https://www.aljazeera.com/news/2026/1/5/venezuela-after-maduro-oil-power-and-the-limits-of-intervention
- CNBC, acuerdo con India (3-feb-2026): https://www.cnbc.com/2026/02/03/us-india-trade-framework-tariffs-reset-modi-trump-new-delhi-russian-oil-venezuela.html
- CSIS, tierras raras y Japón: https://www.csis.org/analysis/chinas-rare-earth-campaign-against-japan
- LME Nickel 2022: https://en.wikipedia.org/wiki/LME_Nickel
- Wikipedia, 2025 stock market crash: https://en.wikipedia.org/wiki/2025_stock_market_crash

---

## Registro de verificación (2026-09-25)

Verificador adversarial. Método: WebFetch a fuentes primarias (AEA, NBER, IDEAS/RePEc, Elsevier, BCE, BIS, FMI, Fed, Banxico, EIA, OPEP, SEC/EDGAR, Federal Register/GovInfo, OFR), series diarias de FRED, API pública de Polymarket (precios y reglas al 25-sep-2026) y prensa con fecha. El presupuesto de WebSearch de la sesión estaba agotado, así que todo se verificó por consulta directa. Bloqueados (403/451): CNBC, CNN, LPL, Wiley, CRS, commerce.gov, White & Case y la página de WEF (el PDF del informe sí se descargó). Revisados: 72 elementos. Confirmados: 44. Corregidos en sitio: 22. Marcados "(no verificado)": 21 (algunos elementos tienen una parte confirmada y otra no).

**Correcciones de fondo**

| # | Afirmación original | Qué dice la fuente | Fuente |
|---|---|---|---|
| 1 | AKW (2020): −11.5% acumulado, US$4.1 billones | Especificación base: −6.0 pp, US$1.7 billones; −9.7% con ventanas de 3 días en 7 eventos. No aparece 11.5% ni US$4.1 billones (tampoco en w28758) | NBER w27114, PDF |
| 2 | ARW (2019): US$3.2 mil millones/mes | Sólo US$1.4 mil millones/mes confirmado; la versión NBER dice alrededor de US$3 mil millones/mes a nov-2018 | NBER w25672; Liberty Street |
| 3 | Petroline atacado por "drones hutíes" el 11/12-sep, "fuera por semanas" | Ataque del viernes 11-sep sin reivindicación, atribuido a grupos proiraníes desde Irak; sin estimación de duración | Al Jazeera, 12-sep-2026 |
| 4 | Qatar declara *force majeure* tras el ataque a Ras Laffan del 18-mar | El *force majeure* fue a inicios de marzo por el cierre de Ormuz; Ras Laffan ya estaba inactivo al ser atacado | Wikipedia, "Economic impact of the 2026 Iran war" |
| 5 | Brent máximo de US$118.35 | Es el cierre máximo del futuro; el spot (EIA) llegó a US$138.21 el 7-abr y a US$130.80 el 15-sep | FRED DCOILBRENTEU; futuros BZ=F |
| 6 | En agosto, Brent arriba de US$100 | Futuros entre US$79 y US$94 en agosto; hubo pausa militar | Futuros BZ=F; Wikipedia; Polymarket |
| 7 | S&P −9.8% hasta 6,316.91 | Intradía. Al cierre: −9.1%, de 6,978.60 a 6,343.72 | FRED SP500 |
| 8 | GPR arriba de 300: 6 meses desde 1985 | 8 meses | Archivo oficial del GPR |
| 9 | BIS 15-ene-2026 "con arancel de 25%" | Regla anunciada el 13-ene y publicada el 15-ene; tope de 50% y pruebas de terceros confirmados; el 25% no está en la regla | Federal Register 2026-00789; BIS |
| 10 | Nvidia excluye China de su guía (fuente secundaria) | 10-Q: el gobierno chino restringió las compras de H200; cargo de US$0.4 mil millones; envíos menores a 1% de Data Center | Nvidia 10-Q, 26-ago-2026 |
| 11 | WEF: 18% y "salto de 8 lugares" | El salto de 8 lugares es del ranking a 2 años; el 18% (detonante en 2026) subió 2 posiciones | WEF GRR 2026, PDF |
| 12 | LME canceló unos US$12 mil millones | Rango de US$3.9 a 12 mil millones | OFR WP 24-09 |
| 13 | OPEP+ "completó" el retiro de recortes y "cuotas estables el resto de 2026" | El comunicado sólo acuerda +188 mil b/d para septiembre y reuniones mensuales | OPEP, 2-ago-2026 |
| 14 | Cierre de Ormuz el 2-mar | Wikipedia lo fecha el 4-mar; el 2-mar queda como no verificado | Wikipedia |
| 15 | Se reanudan ataques el 7-jul | Wikipedia: colapso del alto al fuego el 8-jul | Wikipedia, "2026 Iran war" |
| 16 | Polymarket "peace deal" resolvió el 15-jun | El mercado "by June 15" resolvió Sí, con cierre el 18-jun | API de Polymarket |
| 17 | Fajgelbaum: represalias "se dirigieron" a condados republicanos | Los trabajadores de sectores comerciables en condados muy republicanos fueron los más afectados | NBER w25638 |
| 18 | Probabilidades de Polymarket redondeadas y de mediados de septiembre | Actualizadas al 25-sep: Ormuz 22.5%, bloqueo 61.7%, invasión 14.5%, régimen 6.5%, acuerdo nuclear 12.5%, Bab el-Mandeb 18.5%, Taiwán 3.75%, Cámara D 92.5%, Senado D 62.5% | API de Polymarket |
| 19 | "Polymarket da <1% a Ormuz normal al 30-sep" | No existe ese mercado; se sustituyó por "normal al 31-oct": 8.5% | API de Polymarket |
| 20 | Oro: quien compró en marzo perdía alrededor de 20% | Depende de la fecha de compra: −18% a −19% desde el inicio de la guerra; −2% desde el mínimo de marzo | Futuros GC=F |
| 21 | Enlaces a los capítulos 04, 15, 16 y 17 rotos | Corregidos a los nombres reales de archivo | Directorio `conocimiento/` |
| 22 | Datos nuevos y relevantes que faltaban | 10 años en 5.11% (23-sep); JPY y CHF se depreciaron contra el USD en mar-2026; Banxico en 6.50%; reembolsos IEEPA pagados: US$81 mil millones | FRED; Banxico; Wikipedia |

**Confirmados (selección):** las 12 citas académicas (autores, año, revista, volumen y páginas; hallazgos centrales) salvo las dos cifras corregidas; FMI GFSR abr-2025 (todas las cifras); Deutsche Bank (32 eventos, −6%, 17+16 días, 1,475 días); BCE FSR nov-2025 (12%, 7 pp, casi 50 pb, tercera mayor alza desde 1986); BIS QR sep-2025 (<20 semanas, 75%); los 27 valores del GPR citados y el 6º lugar de mar-2026; VIX 52.33 y S&P 4,982.77 (8-abr-2025); *Learning Resources v. Trump* (20-feb-2026, 6-3); US$166 mil millones de IEEPA; CIT 7-may; expiración de la Sección 122 y entrada de la 301 (24-jul); inicio de la guerra y Brent de US$72.48; 71.57 el 1-jul; 103.08 el 23-sep; récord del S&P el 15-abr (7,022.95) y 27 récords en 2026; KOSPI y KSE-100; peso −4.02% y 18.13; Banxico 6.75% el 26-mar; oro 5,589.38 y 4,369.19; Fed +25 pb 12-0 y Warsh presidente; tregua EUA-China al 10-ene-2027; aranceles 36.5%/31%; CSIS sobre Japón (6-ene-2026, 63%); EAU fuera de la OPEP el 1-may y 46% a 42%; Venezuela y el Brent en ~US$60; Eurasia Top Risks 2026; Kalshi 62% (4-may); Polymarket Rusia-Ucrania resuelto Sí el 9-may; Apple Greater China US$64,377 millones (−4%).

**Pendientes del autor, resueltos:**
- Brent intradía de US$139.13 (7-mar-2022): sigue sin verificarse en fuente primaria. Cierre de US$127.98 el 8-mar confirmado; spot EIA de US$133.18.
- LPL: sigue sin verificarse (Cloudflare 403, sin copia en Wayback). Grado bajado a C.
- BlackRock: la frase sobre fragmentación y la fecha de actualización (ago-2026) están confirmadas; el top 10, los *scores*, el BGRI y la frase de "los setenta" no se verificaron.
- Nvidia y China: resuelto con el 10-Q (ver corrección 10).
- Pemex exporta crudo e importa refinados: no verificado en esta ronda; se mantiene la marca.
- JPY y CHF en 2026: resuelto con FRED (ambos se depreciaron contra el USD en marzo). Intervención del SNB: no verificada.
- OAT-Bund en ~105 pb: no verificado. El promedio de agosto fue de 82 pb (OCDE vía FRED).
- Taiwán en ~30% a fines de 2025: correctamente excluido; no se verificó.
- Contradicción de Polymarket sobre el alto al fuego contra GlobalSecurity: **resuelta**. Esa familia de mercados define "Effective Ceasefire" como una pausa de 2 semanas (título del evento), que es la pausa iraní que describe GlobalSecurity.

**Siguen sin verificar (marcados en el texto):** detalles 2026 de Rusia-Ucrania y OTAN (tregua de Pascua, alto del 5 al 8 de septiembre, Tusk, GPS en Lituania); 14 puntos y 60 días del memorándum de junio; 16 de 18 miembros de la Fed; oro spot a US$4,250.85; Sección 122 subida a 15%; expectativa de tregua de 6 meses; sanción a la RBA y caída de exportaciones de tierras raras; 10 mil H200 para ByteDance y Tencent; acuerdo EUA-Taiwán; venta de armas de US$11.1 mil millones; TSMC con dos generaciones y 50% de sobrecosto (no aparece en el 20-F); meta de 5 millones de b/d de los EAU; pronósticos de China; deuda francesa; acuerdo con India; frase de Trump del 9-ene sobre cárteles; sospechas de *insider trading* (Bloomberg); 15 días hábiles de Baur-Lucey.

**Nota de extensión:** el capítulo ya tenía unas 8,270 palabras antes de la verificación, arriba del rango de 3,500 a 7,000. Recorte sugerido para la próxima edición: condensar 4.8, 4.9 y la lista de fuentes de prensa.
