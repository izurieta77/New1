# 23 — Geopolítica y riesgo político global para inversionistas

> Nivel: experto · Actualizado 2026-09-25 · Grado global: **B** (la medición y los efectos promedio están bien documentados; el *timing* táctico alrededor de eventos es **C**)

Capítulos relacionados, que aquí no se repiten: [04 Renta fija y macro](04-renta-fija-y-macro.md) · [11 México](11-mexico.md) · [13 Estado del mercado](13-estado-del-mercado.md) · [15 Eventos corporativos](15-eventos-corporativos.md) · [16 Macro, FX y peso](16-macro-fx-peso.md) · [17 Crisis](17-crisis.md) · [22 Fuentes de datos con IA](22-fuentes-de-datos-ia.md). Los parámetros de riesgo salen de `config/parametros.json`.

**Convenciones.** Los hechos llevan fecha y fuente. "Inferencia:" marca razonamiento propio. "Regla:" marca una recomendación operable. "(no verificado)" marca una cifra que no se confirmó contra una fuente en esta sesión.

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
| **B. Oferta de energía o commodities** | 1973, Rusia 2022, Irán/Ormuz 2026 | Caída inicial moderada. El daño viene con la segunda ronda de inflación y tasas | Energía, USD, *commodities*, defensa | Oro y Treasuries a meses si suben las tasas reales. También los importadores de energía |
| **C. Política comercial originada en EUA** | "Liberation Day" abr-2025 | Caída fuerte y rápida (−10% en 2 días). Revierte si la política se revierte | CHF, JPY, oro, Bund | USD y Treasuries (abr-2025) |
| **D. Sanciones o expropiación** | Rusia 2022: MOEX cerrada y activos rusos en índices valuados a cero | Pérdida permanente en los activos expuestos | Salir antes. No promediar a la baja | Cualquier tesis de "está barato" |
| **E. Desastre de cola** | Bloqueo o invasión de Taiwán (no ha ocurrido) | Desconocida y probablemente extrema en semis y tecnología | Sólo la cobertura puesta *antes* | Reaccionar después |

---

## 3. Literatura canónica

| Estudio | Hallazgo cuantificado o central | Enlace | Grado |
|---|---|---|---|
| Caldara & Iacoviello (2022), AER 112(4):1194-1225, "Measuring Geopolitical Risk" | Índice de noticias desde 1900. Un GPR más alto anticipa menor inversión y empleo, mayor probabilidad de desastre y más riesgo a la baja. Importan tanto la amenaza como el acto. La inversión cae más en industrias expuestas | https://www.aeaweb.org/articles?id=10.1257/aer.20191823 | A (medición); B (efectos en retornos) |
| Caldara, Conlisk, Iacoviello & Penn (2026), JIE 159, "Do geopolitical risks raise or lower inflation?" | En 44 economías desde 1900, el GPR anticipa **más inflación y menor actividad**, más gasto militar, más deuda y menos comercio. Los *acts* tienen efectos mayores y más persistentes que los *threats* | https://www.matteoiacoviello.com/research_files/JIE_2026.pdf | A-/B |
| Baker, Bloom & Davis (2016), QJE, "Measuring Economic Policy Uncertainty" | Con empresas, la EPU se asocia con más volatilidad de la acción y menos inversión y empleo en sectores sensibles a la política (defensa, salud, finanzas, infraestructura). A nivel macro, las innovaciones de EPU anticipan caídas de inversión, producto y empleo (EUA y un panel de 12 países) | https://www.policyuncertainty.com/ | A (medición); B (efectos) |
| Pastor & Veronesi (2012), JF, "Uncertainty about Government Policy and Stock Prices" | Los precios caen en promedio al anunciarse cambios de política. La caída es mayor con más incertidumbre, y después suben la volatilidad y las correlaciones | https://onlinelibrary.wiley.com/journal/15406261 | B |
| Pastor & Veronesi (2013), JFE 110:520-545, "Political Uncertainty and Risk Premia" | La prima por incertidumbre política es **mayor en economías débiles**. Las acciones se vuelven más volátiles y más correlacionadas. Baja el valor del *put* implícito del gobierno | https://www.nber.org/papers/w17464 | B |
| Kelly, Pastor & Veronesi (2016), JF 71(5):2417-2480, "The Price of Political Uncertainty" | Las opciones cuya vida abarca elecciones nacionales o cumbres globales son **más caras** porque protegen contra riesgo de precio, varianza y cola. El efecto es mayor con economía débil y se contagia entre países | https://www.nber.org/papers/w19812 | A- |
| Hassan, Hollander, van Lent & Tahoun (2019), QJE 134(4):2135-2202, "Firm-Level Political Risk" | PRisk se construye con transcripciones de *earnings calls*. Las empresas con más riesgo político **recortan contratación e inversión** y hacen más *lobbying* y donaciones. La mayor parte de la varianza es idiosincrática, no agregada | https://www.nber.org/papers/w24029 · datos: https://www.firmlevelrisk.com | A- (medición) |
| Berkman, Jacobsen & Lee (2011), JFE 101(2):313-332, "Time-varying rare disaster risk and stock returns" | Con 447 crisis internacionales entre 1918 y 2006, un índice de crisis afecta la **media y la volatilidad** de los retornos mundiales. El efecto es mayor con crisis severas o con grandes potencias involucradas. El riesgo de crisis **se paga**: las industrias más sensibles rinden más en promedio | https://econpapers.repec.org/RePEc:eee:jfinec:v:101:y:2011:i:2:p:313-332 | B |
| Amiti, Redding & Weinstein (2019), JEP 33(4):187-210 | Traspaso prácticamente completo de los aranceles de 2018 a precios en EUA. A dic-2018 costaban **US$3.2 mil millones/mes** en impuestos y **US$1.4 mil millones/mes** en pérdida de eficiencia | https://www.aeaweb.org/articles?id=10.1257/jep.33.4.187 | A |
| Fajgelbaum, Goldberg, Kennedy & Khandelwal (2020), QJE 135(1):1-55 | Pérdida para compradores de importaciones de **US$51 mil millones (0.27% del PIB)**. Neto de recaudación y ganancias de productores, la pérdida agregada fue de **US$7.2 mil millones (0.04%)**. Las represalias se dirigieron a condados republicanos | https://www.nber.org/papers/w25638 | A |
| Amiti, Kong & Weinstein (2020, NBER w27114) | En 11 fechas de anuncios arancelarios EUA-China, el mercado cayó **11.5% acumulado (US$4.1 billones)**. La guerra comercial redujo el crecimiento de la inversión de las emisoras de EUA en **1.9 pp** hacia fines de 2020 | https://www.nber.org/papers/w27114 | B+ |
| Baur & Lucey (2010), Financial Review 45:217-229 | El oro cubre acciones en promedio y funciona como *safe haven* en caídas extremas, pero **sólo por unos 15 días hábiles**. Mantenerlo después de ese plazo destruyó valor en la muestra 1995-2005 | https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6288.2010.00244.x | B |
| FMI, GFSR abr-2025, cap. 2 "Geopolitical Risks: Implications for Asset Prices" | Un *shock* de GPR de un país baja las acciones alrededor de **0.3%** de forma persistente por 2 años. Un *shock* severo (≥2σ) tiene un efecto unas **7 veces mayor**. Un *shock* global produce alrededor de **−1%** por un trimestre. A nivel empresa: **−1 pp** en el mes. En emergentes, los conflictos militares internacionales producen **alrededor de −5%**. Si el socio comercial principal entra en conflicto, **hasta −2.5 pp**. En los importadores de *commodities* el CDS soberano sube más de 1% en una semana, y en los exportadores baja | https://www.imf.org/en/Publications/GFSR/Issues/2025/04/22/global-financial-stability-report-april-2025 | A- (panel amplio, identificación recursiva) |
| Deutsche Bank Research (Jim Reid, jun-2025), 32 eventos geopolíticos | Mediana del S&P 500: **−6% en 17 días hábiles** y recuperación total en **16 días más**. A 12 meses, alrededor de **+15% desde el mínimo**. Excepción, el choque petrolero de 1973: **1,475 días hábiles** para recuperar y −28% adicional a 12 meses | https://www.aol.com/stocks-risk-iran-israel-conflict-104512973.html | B (muestra chica, sin costos) |
| LPL Research (2025-2026) | Guerras y operaciones militares: *drawdown* promedio de **alrededor de 7%**, recuperado en unos **55 días**. Eventos geopolíticos en general: retroceso promedio de **4.5%** (mediana **2.9%**) | https://www.lpl.com/research/blog/iran-escalation-how-markets-have-reacted-to-geopolitical-events.html (403 al descargar; cifras tomadas del resumen indexado) | B- |
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

**Inferencia:** el GPR agregado volvió en agosto a niveles "normales altos" (alrededor de 118), aunque la guerra sigue sin resolverse y el Brent pasa de US$100. El índice mide la **atención de la prensa**, no el daño económico. Usarlo como señal de "ya pasó" en un *shock* tipo B es un error.

### 4.2 Choque arancelario de abril de 2025 (tipo C)

- 2-abr-2025: arancel base de 10% más tasas "recíprocas" para unos 60 países. En dos sesiones el S&P perdió alrededor de **10%**, el Nasdaq alrededor de 11% y se borraron **US$6.6 billones** (resumen de Wikipedia, "2025 stock market crash"). El VIX cerró en **52.33** el 8-abr y el mínimo del S&P quedó en alrededor de **4,982**.
- Lo anómalo fue que el dólar cayó y los rendimientos de los Treasuries subieron (BCE). Los refugios que funcionaron fueron CHF, JPY, oro y Bund.
- La reversión llegó con la pausa del 9-abr y la tregua con China del 12-may (BIS). El máximo previo se superó en menos de 20 semanas.
- Epílogo legal: el **20-feb-2026** la Suprema Corte anuló por 6-3 los aranceles IEEPA (*Learning Resources v. Trump*), con unos **US$166 mil millones** en reembolsos en proceso vía CBP (BDO y Norton Rose). El mismo día entró un arancel global de 10% bajo la **Sección 122**. La CIT lo declaró ilegal el 7-may-2026, pero el Circuito Federal suspendió el fallo, y el arancel **expiró por ley el 24-jul-2026** al cumplir 150 días. Ese mismo 24-jul entraron aranceles de la **Sección 301 "forced labor"**: 10% o 12.5% para 60 socios, sin fecha de expiración. México y Canadá quedaron en 10%, y los bienes que califican para el T-MEC están **exentos** (Holland & Knight, jul-2026).

**Inferencia (ventaja del dueño):** los plazos legales, como los 150 días de la Sección 122, los calendarios de la Suprema Corte y de la CIT o las revisiones anuales del T-MEC, son información pública que el mercado procesa mal. Quien entiende cómo se decide dentro del gobierno puede anticipar el **instrumento de reemplazo** (se sabía que habría un sustituto de la Sección 122 antes del 24-jul), aunque no pueda anticipar el titular.

### 4.3 La guerra de Irán de 2026 (tipo B): el caso de estudio del ciclo

Cronología verificada:
- **28-feb-2026:** ataques conjuntos de EUA e Israel ("Operation Epic Fury"). Brent previo en alrededor de US$72.5.
- **2-mar:** la Guardia Revolucionaria cierra Ormuz al tráfico de EUA y aliados.
- **18-mar:** ataque a Ras Laffan. Qatar declara *force majeure* en GNL, el TTF casi se duplica a más de €60/MWh y el GNL spot en Asia sube más de 140%.
- **31-mar:** Brent en **US$118.35** (máximo). La AIE lo llamó "la mayor interrupción de oferta en la historia del mercado petrolero".
- **8-abr:** alto al fuego mediado por Pakistán, con reapertura parcial. Iran vuelve a restringir el paso el 19-abr.
- **Junio:** memorándum de 14 puntos EUA-Irán con una ventana de negociación de 60 días (el mercado de Polymarket de "peace deal" resolvió Sí el 15-jun). El Brent baja a **US$71.57 el 1-jul**.
- **7-jul:** se reanudan los ataques. Bloqueo estadounidense e Irán atacando buques "no conformes".
- **11/12-sep:** drones hutíes golpean el oleoducto saudí Este-Oeste (Petroline), que movía de 4 a 5 millones de b/d desviados de Ormuz hacia Yanbu. Se cierra "por precaución" y queda fuera de servicio por semanas. El Brent vuelve a pasar de US$100.
- **23/24-sep:** Brent en **US$103.08** (+42% contra la preguerra, cálculo propio). Hubo un solo tránsito comercial en Ormuz el 20-sep, contra un promedio de alrededor de 85 diarios antes de la guerra, y 396 buques esperando. Irán presentó un plan de alto al fuego regional de hasta 60 días con reapertura por fases y fijó un ultimátum de "4 a 5 días" (alrededor del 27-28 de sep). Fuente: GlobalSecurity, parte del día 209.

Reacción de mercados:
- **S&P 500:** cayó 9.8% desde el máximo de enero hasta **6,316.91 (30-mar)** y marcó **récord el 15-abr (7,022.95)**, 47 días después del inicio de la guerra y a unas dos semanas del mínimo (CNN y CBS). Para fines de agosto llevaba 27 récords en 2026 y alrededor de +13% en el año (Motley Fool). La IA, casi la mitad de la capitalización, "corrió con dinámica propia".
- **Emergentes importadores de energía:** el KOSPI cayó hasta 12% intradía el 4-mar con *circuit breaker*, y el KSE-100 de Pakistán perdió 9.57%.
- **Peso mexicano:** −4.02% en marzo, con máximo de 18.13 por dólar el 27-mar (El Informador y El Financiero). Banxico recortó a 6.75% ese mes.
- **Oro:** récord de **US$5,589.38 el 28-ene-2026**, luego **US$4,369 al 1-sep (−21.8%)** y US$4,250.85 el 24-sep (CBS y Trading Economics). Cayó porque subieron las tasas reales.
- **Treasuries:** el rendimiento a 10 años llegó a 4.46% (27-mar). La **Fed subió 25 pb el 16-sep-2026 a 3.75-4.00%** (12-0), su primera alza en más de tres años, por la inflación energética. Kevin Warsh es el presidente de la Fed, y 16 de 18 miembros ven otra alza (CNBC).

**Lecciones (Inferencia):**
1. Las acciones de EUA recuperaron rápido porque las utilidades de IA dominaron el índice. El promedio de Deutsche Bank se cumplió **en el índice**, no en los emergentes importadores ni en los activos de *duration*.
2. El daño de un *shock* tipo B llega **con meses de rezago**, por inflación, luego la Fed y luego las tasas reales. Quien compró oro "por la guerra" en marzo perdía alrededor de 20% en septiembre.
3. El dólar funcionó en los primeros días (Wikipedia, sección de mercados). Para un inversionista en MXN, tener dólares amortiguó el golpe.
4. Los activos que sí cubrieron fueron energía, transporte de crudo y GNL, y los exportadores fuera del Golfo (inferencia coherente con el FMI: el *shock* de *commodities* favorece al sector energía).

### 4.4 Rusia-Ucrania: 2022 como plantilla y 2026 como estado

- **2022:** el Brent cerró en alrededor de US$127 el 8-mar-2022, con máximo intradía reportado de US$139.13 (Biblioteca de la Cámara de los Comunes; el intradía no fue verificado en fuente primaria). El níquel de la LME superó **US$100,000/t** y la bolsa **suspendió la negociación y canceló unos US$12 mil millones en operaciones** (Wikipedia LME Nickel y OFR WP 24-09). Según el FMI, las empresas con subsidiarias en Rusia o Ucrania cayeron **2.5 pp** en una semana.
- **2026:** no hay alto al fuego. Hubo treguas de 32 horas (11-abr, Pascua ortodoxa) y del 9 al 11 de mayo, y Ucrania ordenó un alto del 5 al 8 de septiembre ante la visita de Witkoff y Kushner. Rusia exige todo el Donbás. Eurasia Group (#5 "Russia's second front") y el primer ministro polaco Tusk (17-sep-2026) advierten de ataques híbridos "accidentales" contra la OTAN. Lituania reporta que la interferencia de GPS pasó de 3 a 36 estaciones.

### 4.5 EUA-China: tregua corta, chips y tierras raras

- La tregua de Busan (oct/nov-2025) se extendió en la cumbre de Pekín de mayo de 2026 y el **24-sep-2026 se extendió sólo 2 meses, hasta el 10-ene-2027** (Bessent, vía CNBC y Bloomberg). El mercado esperaba 6 meses o más.
- Aranceles vigentes: **36.5%** de EUA a China y **31%** de China a EUA (CRS jul-2026, citado por Al Jazeera). China tiene alrededor de 60% de los depósitos y alrededor de 90% del procesamiento de tierras raras. Mantiene las licencias lentas y selectivas, sancionó a la Responsible Business Alliance en agosto, y sus exportaciones de tierras raras a EUA cayeron antes de la cumbre (Chin@Strategy y Invezz, 21-sep).
- Chips: el **15-ene-2026** el BIS pasó el H200 y el MI325X a revisión caso por caso para China, con arancel de 25%, tope de 50% del volumen y pruebas de terceros. ByteDance y Tencent recibieron alrededor de 10 mil H200 cada una antes del 18-ago. Según fuente secundaria, Nvidia excluye de su guía los ingresos de centros de datos en China porque **Pekín restringió las compras**. Hay además un arancel de Sección 232 de 25% a ciertos chips avanzados que no van a la cadena de suministro de EUA. El acuerdo EUA-Taiwán de ene-2026 fija un arancel máximo de 15% y trato preferente de 232 a cambio de inversión en fábricas en EUA.
- China-Japón: tras los dichos de la primera ministra Takaichi sobre Taiwán (7-nov-2025), China prohibió en ene-2026 exportar a Japón bienes de uso dual, incluidas tierras raras. Japón dependía de China para 63% de sus importaciones de tierras raras en 2024 (CNN y CSIS).

### 4.6 Taiwán y la concentración de semiconductores

- Polymarket, "China invade Taiwan by end of 2026": **4%**, con US$42.8 millones de volumen (consultado el 25-sep-2026). EUA aprobó una venta de armas por US$11.1 mil millones en dic-2025. Trump dijo que las ventas de armas podrían entrar en la negociación con Xi, y Taiwán hizo simulacros con drones de ataque en septiembre.
- TSMC mantiene su tecnología más avanzada al menos **dos generaciones** por delante de lo que produce fuera de Taiwán, y operar en EUA cuesta **50% o más** que hacerlo en Taiwán (resumen de TSMC 20-F y prensa). **Inferencia:** un portafolio cargado en IA y semis tiene una exposición implícita a Taiwán (tipo E) que no aparece en el 10-K como "ingresos por región".

### 4.7 OPEP+, petróleo y Venezuela

- **Los EAU salieron de la OPEP y de la OPEP+ el 1-may-2026** (anuncio del 28-abr). Querían producir hacia 5 millones de b/d en 2027. La participación de la OPEP+ en la producción mundial bajó de alrededor de 46% a alrededor de 42% (EIA).
- La OPEP+ completó en septiembre el retiro de los recortes voluntarios de 2023 (+188 mil b/d) y espera mantener cuotas estables el resto de 2026 (OPEP, 2-ago-2026).
- **Venezuela, 3-ene-2026:** EUA capturó a Maduro, pero el Brent *bajó* a alrededor de US$60 porque había sobreoferta y no se dañó infraestructura (Al Jazeera y CGEP). Lección: un evento geopolítico sin pérdida de oferta, en un mercado con exceso, no mueve el precio.

### 4.8 China, Europa, India y EUA

- **China:** el pronóstico de crecimiento para 2026 va de 4.3% a 4.8% (consenso, UBS y Goldman). Los indicadores inmobiliarios siguen entre 50% y 80% debajo del pico de 2020-2021, y el PPI lleva más de 3 años en deflación. Eurasia (#7 "China's deflation trap") espera que China siga exportando deflación y que eso desate respuestas antidumping.
- **Europa:** el diferencial OAT-Bund a 10 años ronda **105 pb**, el primero arriba de 100 desde 2012 (CNBC, 24-sep-2026). La deuda francesa proyectada es de 119.3% del PIB en 2026 y la pelea presupuestal amenaza con tumbar otro gobierno. Alemania ejecuta su paquete fiscal de infraestructura y defensa. Eurasia #4: "Europe under siege".
- **India:** el acuerdo del 2-feb-2026 bajó el arancel recíproco de 25% a 18% y retiró el castigo de 25% por comprar petróleo ruso. La anulación de IEEPA y la Sección 301 cambiaron después la base; hoy India está en el grupo de 10%.
- **EUA:** Eurasia #1 es "US political revolution" y #6 "State capitalism with American characteristics", es decir, un gobierno que elige ganadores y perdedores. Elecciones intermedias del 3-nov-2026: mercados de predicción a mediados de septiembre dan a los demócratas alrededor de **89-90% para la Cámara** y **55-60% para el Senado** (CNBC y Econbrowser, sep-2026).
- **Norteamérica (detalle en el cap. 11):** en la revisión del **1-jul-2026** EUA **no** aceptó extender el T-MEC 16 años, lo que activa revisiones anuales hasta 2036 (White & Case). Eurasia #9: "Zombie USMCA". Trump dijo el 9-ene-2026 que EUA empezaría a "golpear en tierra" a los cárteles en México, y Sheinbaum lo rechaza. Eurasia #3: "Donroe Doctrine".

### 4.9 Encuestas institucionales de riesgo 2026

- **Eurasia Group Top Risks 2026** (5-ene-2026): 1 US political revolution · 2 Overpowered (China, electrones, contra EUA, moléculas) · 3 The Donroe Doctrine · 4 Europe under siege · 5 Russia's second front · 6 State capitalism with American characteristics · 7 China's deflation trap · 8 AI eats its users · 9 Zombie USMCA · 10 The water weapon. Las "red herrings" (riesgos que considera sobrevalorados): "Tariff Man", desglobalización, esferas de influencia y "sell America".
- **WEF Global Risks Report 2026** (ene-2026): **confrontación geoeconómica** es el riesgo #1 a 2 años, seguido de desinformación, polarización, clima extremo y conflicto armado entre Estados. 18% de los encuestados la señalan como el riesgo más probable de detonar una crisis global en 2026, un salto de 8 lugares.
- **BlackRock Geopolitical Risk Dashboard** (actualizado ago-2026): la fragmentación se acelera por Medio Oriente, la competencia tecnológica EUA-China y el comercio. Top 10: proteccionismo comercial, guerra regional en Medio Oriente, competencia estratégica EUA-China, desacoplamiento tecnológico, ciberataques, terrorismo, conflicto Rusia-OTAN, crisis políticas en emergentes, Corea del Norte y fragmentación europea. Subió la seguridad energética a riesgo alto y la llama la mayor crisis energética desde los años setenta (resumen indexado; no se pudieron extraer los *scores* numéricos).

---

## 5. Evidencia real: cuánto cae, cuánto tarda y qué protege

### 5.1 Magnitudes de referencia (S&P 500)

| Fuente o caso | Caída | Días al mínimo | Recuperación |
|---|---|---|---|
| Deutsche Bank, mediana de 32 eventos | −6% | 17 días hábiles | 16 días hábiles más |
| LPL, guerras y operaciones militares | −7% promedio | — | alrededor de 55 días |
| LPL, eventos geopolíticos en general | −4.5% promedio (mediana −2.9%) | menos de 1 mes | — |
| Choque petrolero de 1973 (DB) | profundo | — | **1,475 días hábiles** |
| Aranceles, abr-2025 | alrededor de −10% en 2 días (mínimo alrededor de 4,982) | ~5 días desde el anuncio | máximo previo superado en menos de 20 semanas (BIS) |
| Guerra de Irán, 2026 | −9.8% desde el máximo de enero | alrededor de 30 días desde el inicio (30-mar) | récord el 15-abr |
| Venezuela, ene-2026 | casi nula | — | — |

**Grado de esta tabla: B.** Son muestras chicas, sin costos, con sesgo de supervivencia (se mira el S&P, no el índice de un país invadido) y dominadas por un mercado cuyo peso en IA en 2026 no tiene precedente. El FMI corrige la parte internacional: en emergentes un conflicto militar internacional cuesta alrededor de **5%**, cinco veces más que el promedio.

### 5.2 Matriz de refugios

| Activo | Funciona cuando | Falla cuando | Evidencia 2022-2026 |
|---|---|---|---|
| **USD** | *Shock* global que no nace en EUA. Primeros días de un choque energético | El *shock* nace en la política de EUA | Subió en los primeros días de la guerra de Irán. Cayó más de 4% en abr-2025 y 12% contra el EUR en el año (BCE) |
| **Treasuries largos** | *Shock* de demanda o desinflacionario | Choque de oferta inflacionario o *shock* de credibilidad de EUA | +50 pb en una semana en abr-2025. El 10 años llegó a 4.46% en mar-2026 y la Fed subió tasas en sep-2026 |
| **Oro** | Los primeros ~15 días hábiles (Baur-Lucey). *Shocks* de credibilidad del USD | Suben las tasas reales o se libera liquidez. Horizontes de meses | Funcionó en abr-2025 (BCE). −21.8% entre el 28-ene y el 1-sep-2026 |
| **CHF** | Estrés europeo o global | Intervención del SNB (no verificado para 2026) | Se apreció en abr-2025 (BCE) |
| **JPY** | *Shock* de riesgo con *carry trade* desarmándose | Choque de petróleo, porque Japón importa energía (Inferencia) | Se apreció en abr-2025 (BCE). Su comportamiento en 2026 no se verificó |
| **Energía y *commodities*** | Tipo B | Tipo A con sobreoferta (Venezuela 2026) | 2022 y 2026 |
| **MXN** | Casi nunca protege. Es moneda de riesgo | — | −4% en mar-2026 |

**Regla para una cuenta en MXN:** la exposición en dólares es la cobertura natural contra el tipo A y el tipo B. Contra el tipo C originado en EUA, esa cobertura puede no funcionar, y conviene tener parte en oro o en activos no USD (el detalle está en el cap. 16).

### 5.3 Mercados de predicción: evidencia de 2026 sobre su calibración

- Kalshi, 4-may-2026: tráfico "normal" en Ormuz **antes de octubre: 62%**. Hoy Polymarket da menos de 1% para "normal al 30-sep". La probabilidad fue demasiado optimista durante meses.
- Polymarket "Russia x Ukraine ceasefire by end of 2026" **resolvió Sí** (US$14.5 millones de volumen) con una **tregua de 3 días** en mayo. El título decía "ceasefire" y la regla de resolución aceptaba una pausa temporal.
- Bloomberg documentó sospechas de *insider trading* en los mercados sobre Irán.
- **Regla:** un mercado de predicción es un *prior* útil y barato. Antes de usarlo hay que leer (1) la regla exacta de resolución, (2) el volumen y (3) si hay ventaja informativa de *insiders*. Grado para uso táctico: **C**.

---

## 6. Traducción operable

### 6.1 Árbol de clasificación (menos de 2 horas desde el evento)

1. **¿Se interrumpe un flujo físico de más de 2% de la oferta mundial** de petróleo, gas, grano, metales críticos o chips avanzados? Si es así, candidato a **tipo B** (o E si es Taiwán).
2. **¿El *shock* nace en la política de EUA** (aranceles, Fed, instituciones)? Si es así, **tipo C**: no contar con el USD ni con los Treasuries como refugio.
3. **¿Afecta derechos de propiedad o convertibilidad** (sanciones, controles de capital, *delisting*)? Si es así, **tipo D**: salir de lo expuesto y no promediar.
4. **¿Es amenaza o acto?** Una amenaza negociable es reversible. Hay que tener presente la reversión de política ("pausa del 9-abr").
5. Si ninguna de las anteriores aplica: **tipo A**.

Umbrales de confirmación para el tipo B: el Brent sube más de 25% en 10 días hábiles, la curva entra en *backwardation* fuerte, las *breakevens* de inflación suben y los futuros de Fed/Banxico dejan de descontar recortes. Umbrales de estrés: GPR mensual arriba de 200 es elevado, y arriba de 300 es extremo (6 meses desde 1985). VIX arriba de 25 apaga los ETFs apalancados (`filtro_apalancados`).

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
- **Anuales:** Eurasia Group Top Risks, el WEF Global Risks Report y el GFSR del FMI.

### 6.6 Mapa de riesgos vigente al 25-sep-2026

| Foco | Estado verificado | Mercado de predicción (25-sep-2026) | Canal principal | Qué vigilar |
|---|---|---|---|---|
| **Irán, Ormuz y Mar Rojo** | Día 209 de la guerra. Bloqueo de EUA. Un tránsito el 20-sep. Petroline fuera de servicio desde el 11/12-sep. Brent en US$103 | Ormuz normal al 31-dic: **23%**. Fin del bloqueo al 31-dic: **62%**. EUA invade Irán antes de 2027: **15%**. Caída del régimen antes de 2027: **7%**. Acuerdo nuclear final al 31-dic: **12%**. Bab el-Mandeb cerrado al 31-dic: **19%** (Polymarket) | Tipo B, en su segunda ronda (inflación y Fed) | Ultimátum iraní del 27-28 de sep, tránsitos en PortWatch, reparación de Petroline, curva del Brent |
| **EUA-China** | Tregua extendida sólo hasta el **10-ene-2027**. Aranceles de 36.5% y 31%. Tierras raras con licencias lentas | — | Tipo C/D en tecnología | Licencias de tierras raras, H200, listas del BIS y MOFCOM |
| **Taiwán** | Sin crisis militar. Taiwán teme ser moneda de cambio | Invasión antes de 2027: **4%** (US$42.8 millones) | Tipo E | Anuncios sobre venta de armas, ejercicios del EPL, lenguaje de las cumbres |
| **Rusia-Ucrania y OTAN** | Sin alto al fuego. Guerra híbrida en aumento | El mercado de alto al fuego 2026 ya resolvió Sí por una tregua de 3 días (no sirve como señal) | Tipo B en gas europeo y tipo A | Incidentes con drones en la OTAN, nuevos paquetes de sanciones de la UE |
| **Política de EUA** | Fed en 3.75-4.00% con sesgo alcista. Aranceles 301 sin fecha de fin. Elecciones intermedias el 3-nov | Cámara demócrata **alrededor de 90%**. Senado demócrata **55-60%** | Tipo C | Fallos del Circuito Federal y de la Suprema Corte, independencia de la Fed |
| **Norteamérica y México** | Revisiones anuales del T-MEC. Arancel 301 de 10% con exención T-MEC. Amenaza de ataques a cárteles | — | Tipo C para el peso y los exportadores | Rondas bilaterales con USTR (ver cap. 11) |
| **Europa** | OAT-Bund en alrededor de 105 pb. Presupuesto francés en disputa. Rearme | — | Tipo A/C para el euro | Mociones de censura, calificaciones soberanas |
| **China doméstica** | Deflación del PPI por más de 3 años. Inmobiliario en su 5º año de caída | — | Deflación exportada | Medidas antidumping de terceros países |
| **OPEP+** | Salida de los EAU. Cuotas estables el resto de 2026 | — | Oferta de crudo | Capacidad ociosa saudí, producción de los EAU |

---

## 7. Trampas

1. **Vender el titular.** La mediana histórica se recupera en semanas. Vender en el mínimo de un tipo A es el error más caro y más frecuente.
2. **Extrapolar "comprar la guerra" a un tipo B.** En 1973 la recuperación tardó 1,475 días hábiles. En 2026 el índice se recuperó, pero el oro, los bonos y los emergentes importadores no.
3. **Creer que los refugios son constantes.** En abr-2025 fallaron el USD y los Treasuries, y en 2026 falló el oro. El refugio depende del tipo de *shock*.
4. **Leer el GPR como termómetro de daño.** Mide cobertura de prensa. En agosto de 2026 estaba en 118 con Ormuz prácticamente cerrado.
5. **Comprar protección cuando ya está cara.** Kelly-Pastor-Veronesi muestran que las opciones que abarcan eventos políticos cuestan más. La cobertura se pone con VIX bajo, no con VIX en 40.
6. **Confiar en una probabilidad sin leer la regla.** "Ceasefire" resolvió Sí por una tregua de 3 días, y "Ormuz normal" depende de un umbral de tránsitos en PortWatch.
7. **Confundir el pronóstico del evento con el pronóstico de la reacción.** Acertar que habría guerra con Irán no servía para ganar con acciones de EUA, que marcaron récord 47 días después.
8. **Concentración oculta.** La exposición a IA y semis es exposición a Taiwán. El 10-K no la muestra como ingresos.
9. **Olvidar el tipo de cambio.** Para un inversionista en MXN, un *shock* global suele ser positivo en pesos si tiene dólares, y un *shock* de EUA puede no serlo.
10. **Ignorar las reversiones de política.** En 2025-2026, casi toda medida comercial extrema se pausó, se anuló en tribunales o se sustituyó. Apostar a la permanencia del titular perdió.
11. **Confundir acceso político con ventaja de mercado.** La ventaja legítima del dueño es entender procesos, plazos e incentivos. Operar con información no pública obtenida por relaciones es información privilegiada, sancionada por la Ley del Mercado de Valores y la CNBV en México y por la SEC en EUA. Ese riesgo legal es operativo y no compensa ningún rendimiento.
12. **Doble conteo.** Berkman et al. muestran que el riesgo de crisis ya se paga en precios. Los riesgos conocidos, como Taiwán, están parcialmente descontados, y la ventaja está en el cambio de probabilidad, no en su nivel.

---

## 8. Examen de titulación

**1. ¿Qué mide el GPR y cuál es su principal limitación para un inversionista?**
Mide la frecuencia de palabras sobre tensiones geopolíticas en 10 diarios, con base 1985-2019 = 100, y se divide en amenazas y actos. Su limitación es que mide atención mediática, no daño económico. En ago-2026 marcó 118 con Ormuz cerrado.

**2. Según Pastor-Veronesi (2013), ¿cuándo es mayor la prima por incertidumbre política y qué pasa con la diversificación?**
Es mayor en economías débiles. La incertidumbre política sube la volatilidad **y la correlación** entre acciones, así que la diversificación se debilita justo cuando más se necesita.

**3. ¿Qué encontraron Kelly-Pastor-Veronesi (2016) y qué implicación operativa tiene?**
Las opciones que abarcan elecciones o cumbres son más caras, sobre todo con economía débil. Comprar protección justo antes de un evento programado es pagar la prima completa. La cobertura se compra antes, cuando es barata.

**4. Da tres cifras de la tabla de Deutsche Bank y la excepción clave.**
Mediana de −6% en 17 días hábiles, recuperación total en 16 días más y alrededor de +15% a 12 meses desde el mínimo. Excepción: 1973, con 1,475 días hábiles para recuperar.

**5. ¿Por qué abril de 2025 rompió el manual de refugios?**
El *shock* nació en la política de EUA. El USD cayó (−7 pp contra el EUR después del 1-abr) y el rendimiento a 10 años subió casi 50 pb en una semana. Funcionaron CHF, JPY, oro y Bund (BCE, FSR nov-2025).

**6. En la guerra de Irán de 2026, ¿qué hizo el S&P 500 y qué hizo el oro? Explica la diferencia.**
El S&P cayó 9.8% hasta el 30-mar y marcó récord el 15-abr, impulsado por las utilidades de IA. El oro cayó 21.8% entre su récord del 28-ene y el 1-sep, porque el choque de oferta subió la inflación, luego la Fed subió tasas el 16-sep y subieron las tasas reales. Es un tipo B con segunda ronda.

**7. Cuantifica la evidencia del FMI (GFSR abr-2025) para emergentes y para la exposición por socios comerciales.**
Un conflicto militar internacional cuesta alrededor de 5% en acciones de empresas de emergentes. Si el socio comercial principal entra en conflicto, hasta −2.5 pp. Por exposición de ingresos o subsidiarias, de −0.1 a −0.25 pp adicionales, y por subsidiarias en Rusia o Ucrania en 2022, −2.5 pp en una semana.

**8. ¿Qué concluyeron Amiti-Redding-Weinstein y Fajgelbaum et al. sobre quién paga los aranceles?**
El traspaso a precios de EUA fue prácticamente completo: US$3.2 mil millones al mes en costo arancelario más US$1.4 mil millones al mes de pérdida de eficiencia a dic-2018. Fajgelbaum et al.: US$51 mil millones de pérdida para los compradores, y neto de recaudación y productores, US$7.2 mil millones (0.04% del PIB).

**9. ¿Cómo mide Hassan et al. (2019) el riesgo político de una empresa y qué hacen las empresas expuestas?**
Mide la proporción de la transcripción del *earnings call* dedicada a riesgo político, con lingüística computacional. Las empresas expuestas recortan inversión y contratación y aumentan el *lobbying* y las donaciones.

**10. Clasifica: (a) captura de Maduro en ene-2026; (b) aranceles del 2-abr-2025; (c) ataque a Ras Laffan y al Petroline en 2026; (d) exclusión de acciones rusas en 2022.**
(a) Tipo A: sin pérdida de oferta en un mercado con sobreoferta, el Brent bajó a alrededor de US$60. (b) Tipo C. (c) Tipo B. (d) Tipo D.

**11. ¿Cuánto tiempo actúa el oro como *safe haven* según Baur-Lucey (2010) y qué regla se deriva?**
Alrededor de 15 días hábiles después del *shock*. Regla: el oro táctico "por el evento" se revisa a las 3 semanas. Si suben las tasas reales, se deshace.

**12. Un mercado de Polymarket sobre "alto al fuego Rusia-Ucrania en 2026" resolvió Sí. ¿Significa que hubo paz? ¿Qué lección deja?**
No. Resolvió por una tregua de 3 días en mayo. Lección: leer la regla de resolución, el volumen y el riesgo de *insiders* antes de usar cualquier probabilidad como insumo.

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
- Berkman, Jacobsen & Lee (2011), JFE: https://econpapers.repec.org/RePEc:eee:jfinec:v:101:y:2011:i:2:p:313-332
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
- Polymarket, Irán: https://polymarket.com/iran · Ormuz: https://polymarket.com/iran/strait-of-hormuz · Taiwán: https://polymarket.com/event/will-china-invade-taiwan-before-2027 · Rusia-Ucrania: https://polymarket.com/event/russia-x-ukraine-ceasefire-before-2027
- Kalshi, Ormuz (4-may-2026): https://news.kalshi.com/p/strait-of-hormuz-recovery-odds-2026
- El Informador, peso en marzo de 2026: https://www.informador.mx/economia/el-peso-mexicano-cae-en-marzo-por-guerra-en-iran-pero-mantiene-apreciacion-trimestral-20260331-0164.html
- Al Jazeera, Venezuela (5-ene-2026): https://www.aljazeera.com/news/2026/1/5/venezuela-after-maduro-oil-power-and-the-limits-of-intervention
- CNBC, acuerdo con India (3-feb-2026): https://www.cnbc.com/2026/02/03/us-india-trade-framework-tariffs-reset-modi-trump-new-delhi-russian-oil-venezuela.html
- CSIS, tierras raras y Japón: https://www.csis.org/analysis/chinas-rare-earth-campaign-against-japan
- LME Nickel 2022: https://en.wikipedia.org/wiki/LME_Nickel
- Wikipedia, 2025 stock market crash: https://en.wikipedia.org/wiki/2025_stock_market_crash
