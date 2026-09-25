# 24 — Política pública, regulación y mercados (EUA y México)

> Nivel: experto · Actualizado 2026-09-25 · Grado global: **B**. La reacción de los precios a las sorpresas de política y el valor de las conexiones políticas están medidos con rigor. Las reglas de *trading* que salen de esa literatura, como la deriva pre-FOMC, el "presidential puzzle" o copiar al Congreso, son **C o D**. Donde hay ventaja operable es en anticipar el **instrumento**, el **plazo** y la **sorpresa contra lo que ya descuenta el precio**.

Capítulos relacionados que aquí no se repiten: [04 Renta fija y macro](04-renta-fija-y-macro.md) · [11 México](11-mexico.md) · [13 Estado del mercado](13-estado-del-mercado.md) · [15 Eventos corporativos](15-eventos-corporativos-y-situaciones-especiales.md) · [16 Macro, FX y peso](16-macro-fx-peso.md) · [17 Crisis](17-crisis.md) · [22 Fuentes de datos con IA](22-fuentes-de-datos-ia.md) · [23 Geopolítica](23-geopolitica-y-riesgo-politico-global.md). Los parámetros de riesgo salen de `config/parametros.json` y los pronósticos se registran en `bitacora/pronosticos.csv` con `herramientas/pronosticos.py`.

**Convenciones.** Un **hecho** lleva fecha y fuente. "**Inferencia:**" marca un razonamiento propio. "**Regla:**" marca una recomendación operable. "(no verificado)" marca un dato que no se confirmó en esta sesión. El grado de evidencia va de A a D: A es un resultado replicado y robusto fuera de muestra, neto de costos; D es evidencia débil o marketing.

---

## 1. Objetivos de dominio

Al terminar este módulo el sistema debe poder:

1. Leer la **función de reacción** de la Fed y de Banxico en sus documentos (comunicado, SEP y *dot plot*, minutas, discursos, conferencia) y convertirla en probabilidades para cada reunión. Esas probabilidades se comparan contra los futuros de fondos federales, OIS y swaps de TIIE.
2. Medir una decisión de política como **sorpresa**, es decir, la decisión menos lo que el mercado ya descontaba, y no como un nivel.
3. Clasificar cualquier medida de gobierno por la **durabilidad de su instrumento** (constitución, ley, reglamento, orden ejecutiva, declaración) y por su **riesgo judicial**. En 2025-2026 este fue el mejor predictor de si una medida iba a sobrevivir.
4. Mantener al día el estado de la política en EUA y México al 25-sep-2026: la Fed de Warsh, el Tesoro, el Congreso, los aranceles, el antimonopolio, la FDA, la SEC, la política industrial, el Paquete Económico 2027, Banxico, las reformas, la revisión del T-MEC y las calificadoras.
5. Anticipar la política con un método explícito: incentivos de los actores, jugadores con veto, calendario legal, señales costosas contra declaraciones baratas, precios de mercados de predicción y una lectura de ganadores y perdedores.
6. Convertir la experiencia de gobierno del dueño en una **ventaja medible**. Para eso cada pronóstico político se registra en el *ledger* y se califica contra el mercado, no contra una moneda al aire, sin cruzar nunca la línea de la información privilegiada.
7. Aplicar a cada empresa un **checklist de riesgo regulatorio** que termine en una cifra: un descuento de valoración o un límite de posición coherente con `parametros.json`.
8. Operar con un **calendario político-regulatorio** que tenga fechas duras y reglas de tamaño alrededor de eventos binarios.

---

## 2. Marco teórico

### 2.1 Cuatro canales por los que la política llega a los precios

| Canal | Mecanismo | Ejemplo 2025-2026 | Persistencia |
|---|---|---|---|
| **Tasa de descuento** | Tasa corta esperada, prima por plazo y prima de riesgo accionario | La Fed sube 25 pb el 16-sep-2026 | Alta mientras no cambie la función de reacción |
| **Flujos de caja** | Impuestos, aranceles, subsidios, precios regulados, compras de gobierno | La OBBBA hace permanente la depreciación inmediata de 100%; aranceles 232 a fármacos | Depende del instrumento (ver 2.4) |
| **Estructura de mercado** | Fusiones permitidas o bloqueadas, concesiones, licencias, reguladores | Paramount-WBD, remedios contra Google, CRT y Comisión Antimonopolio en México | Alta: cambia los márgenes de largo plazo |
| **Derechos de propiedad y *enforcement*** | Tribunales, amparo, sanciones, cobro fiscal, intervención bancaria | Nueva SCJN contra Elektra; FinCEN contra CIBanco, Intercam y Vector | Puede ser permanente (pérdida de valor, no volatilidad) |

### 2.2 El precio reacciona a la sorpresa, no a la noticia

Bernanke-Kuttner (2005) separan la parte anticipada de la no anticipada de cada decisión de la Fed usando futuros de fondos federales. Un recorte **no anticipado** de 25 pb se asocia con un alza de alrededor de **1%** en los índices amplios, y la parte anticipada casi no mueve precios. La mayor parte de la respuesta pasa por la prima de riesgo esperada, no por dividendos o tasas reales. Gürkaynak-Sack-Swanson (2005) muestran que las decisiones tienen dos dimensiones: el "*target*" (la tasa de hoy) y el "*path*" (la guía sobre la trayectoria). La segunda explica la mayor parte del movimiento de los plazos largos. Nakamura-Steinsson (2018) agregan el "*information effect*": un alza puede leerse como "la Fed sabe que la economía está fuerte". Bauer-Swanson (2023) lo matizan: buena parte de ese efecto es la reacción de la Fed a noticias públicas que el mercado todavía no había incorporado.

**Regla:** toda decisión de política se registra como el par (decisión, expectativa previa medida en precio). Sin la expectativa, el evento no se puede interpretar.

### 2.3 Función de reacción: qué mirar en cada documento

- **Comunicado:** los cambios de palabras contra el anterior. Se hace un *diff* literal.
- **SEP y *dot plot*:** mediana, dispersión y número de participantes en cada nivel. La mediana no es un compromiso. En dic-2021 la mediana para fin de 2022 era **0.9%** y la tasa terminó 2022 en **4.25-4.50%**. Sirve para medir el sesgo del comité, no para pronosticar el nivel.
- **Minutas** (tres semanas después): el balance de riesgos y cuántos participantes piensan qué.
- **Discursos:** pesan más los del presidente, el vicepresidente y el presidente de la Fed de Nueva York. Durante el *blackout*, que empieza el segundo sábado antes de la reunión, no hay señales oficiales.
- **Conferencia:** respuestas no guionadas que sirven para identificar la variable que domina la función de reacción.

**Inferencia (régimen Warsh):** en septiembre de 2026 Warsh **no entregó punto** en el *dot plot*. Eso, junto con su frase "*independence is a two-way street... we stay in our lane*", indica menos guía futura y más peso del comunicado y la conferencia. Con menos guía hay más sorpresa por reunión, y conviene esperar más volatilidad en el día de la decisión.

### 2.4 Durabilidad del instrumento: el concepto operable central

| Instrumento | Quién lo revierte | Vida media empírica 2025-2026 (Inferencia) | Ejemplo |
|---|---|---|---|
| Constitución (MX) | Mayoría calificada y congresos locales | Años | Reforma judicial de 2024, extinción de órganos autónomos |
| Ley federal | Congreso y control judicial | Años | OBBBA, GENIUS Act, leyes secundarias de energía en MX |
| Acción administrativa con base estatutaria clara | Tribunales; la agencia misma | Meses a años | Sección 232 (acero 50%, autos 25%, fármacos 100%), Sección 301 |
| Acción con base estatutaria dudosa | Tribunales | Meses | Aranceles IEEPA, anulados 6-3 el 20-feb-2026 |
| Instrumento con plazo legal | El propio calendario | Días fijos | Sección 122: 150 días, expiró el 24-jul-2026 |
| Declaración, *post* o mañanera | Nadie: no obliga a nada | Horas a semanas | Amenazas arancelarias con fecha que luego se pospone |

**Regla:** antes de reaccionar a una medida, se escribe su instrumento jurídico, su vía de impugnación y su fecha de caducidad. Si el instrumento está en la mitad baja de la tabla, la posición se dimensiona para una reversión y no para la permanencia.

### 2.5 Economía política: quién decide y por qué

- **Grupos concentrados contra difusos** (Olson; Stigler, captura regulatoria; Grossman-Helpman 1994, "*Protection for Sale*"). La protección y la regulación favorecen a quien concentra beneficios y reparte costos. Un arancel lo pagan millones de consumidores y lo cobran pocas industrias. **Inferencia:** el sesgo de largo plazo de la política comercial favorece a los sectores organizados con empleo geográficamente concentrado, como acero, autos o agro de estados clave.
- **Jugadores con veto** (Tsebelis). Entre más actores deben estar de acuerdo, más estable es el *statu quo*. En México la mayoría calificada depende de PT y PVEM, y el 11-mar-2026 votaron **en contra** de la reforma electoral: 259 a favor, 234 en contra, se necesitaban 334. La coalición no es un bloque.
- **Ciclo electoral.** Antes de una elección el gobierno evita medidas con costo concentrado y visible, y después de la elección se abre una ventana para medidas impopulares. Las intermedias de EUA son el **3-nov-2026** y las de México el **primer domingo de junio de 2027** (por regla, el 6-jun-2027).
- **Pastor-Veronesi (2012, 2020).** Los cambios de política bajan precios en promedio, sobre todo cuando la economía es débil, y la incertidumbre política sube la correlación entre acciones (ver cap. 23). Su modelo de 2020 explica la prima demócrata por el cambio de la aversión al riesgo del electorado, no por la política misma.

### 2.6 Conexiones políticas: renta y riesgo

Una conexión política vale porque da acceso a contratos, rescates y regulación favorable (Faccio 2006; Faccio-Masulis-McConnell 2006; Goldman-Rocholl-So 2009 y 2013). También es un pasivo contingente: cuando cambia el poder, la renta se invierte. El caso Elektra en 2025-2026 muestra el lado negativo en México (sección 4.9). Para un inversionista externo la conexión no es una estrategia. Es un **factor de riesgo** que se mide y se cubre.

---

## 3. Literatura canónica

| Estudio | Hallazgo cuantificado | Enlace | Grado |
|---|---|---|---|
| Bernanke-Kuttner (2005, JF) | Recorte sorpresa de 25 pb: alrededor de **+1%** en índices amplios; la parte anticipada casi no mueve precios | https://www.nber.org/papers/w10402 | **A** |
| Gürkaynak-Sack-Swanson (2005, IJCB) | Dos factores (*target* y *path*); el *path* domina los plazos largos | https://www.federalreserve.gov/pubs/feds/2004/200466/200466pap.pdf | **A** |
| Nakamura-Steinsson (2018, QJE); Bauer-Swanson (2023) | *Information effect* de la Fed; lo discute la explicación de "respuesta a noticias" | https://www.nber.org/papers/w19260 | **B** (en debate) |
| Lucca-Moench (2015, JF) | S&P +**49 pb** en las 24 h previas al FOMC (sep-1994 a mar-2011), alrededor de **80%** del exceso anual | https://www.newyorkfed.org/research/staff_reports/sr512.html | B en muestra; **D** hoy |
| Kurov-Wolfe-Gilbert (2021, FRL) | La deriva pre-FOMC **desapareció después de 2015**, con y sin conferencia (muestra hasta dic-2019) | https://pmc.ncbi.nlm.nih.gov/articles/PMC7525326/ | **B** |
| Cieslak-Morse-Vissing-Jorgensen (2019, JF) | Desde 1994 la prima accionaria se gana en las semanas **0, 2, 4 y 6** del ciclo FOMC; el canal es la comunicación informal de la Fed | https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12818 | B en muestra; **C** como estrategia (no verificado fuera de muestra) |
| Santa-Clara-Valkanov (2003, JF) | Exceso de retorno mayor con presidentes demócratas: **9 pp** (ponderado por valor) y **16 pp** (equiponderado) al año | https://ideas.repec.org/a/bla/jfinan/v58y2003i5p1841-1872.html | B como hecho; **D** para operar (N pequeño; "Is the presidential premium spurious?", JEF 2020) |
| Pastor-Veronesi (2020, JPE) | Explica la prima demócrata por la aversión al riesgo que cambia en el tiempo | https://www.nber.org/papers/w24453 | B |
| Snowberg-Wolfers-Zitzewitz (2007, QJE) | Con mercados de predicción el día de la elección: un triunfo republicano sube las acciones **2-3%** | https://www.nber.org/papers/w12073 | **A-/B** |
| Wagner-Zeckhauser-Ziegler (2018, JFE) | Elección de 2016: ganan las empresas de impuestos altos y las domésticas y pierden las internacionales; lo **fácil de evaluar se priceó más rápido** que lo complejo | https://www.nber.org/papers/w23152 | **B** |
| Faccio (2006, AER) | 47 países: las conexiones son más frecuentes con más corrupción y barreras; **anunciar una conexión nueva sube el valor** | https://www.aeaweb.org/articles?id=10.1257%2F000282806776157704 | **A** |
| Faccio-Masulis-McConnell (2006, JF) | Las empresas conectadas tienen más probabilidad de ser rescatadas | https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2006.01000.x | B |
| Goldman-Rocholl-So (2009, RFS) | S&P 500: nombrar un consejero conectado genera retorno anormal positivo. Tras la elección de 2000 suben las empresas conectadas con republicanos y bajan las conectadas con demócratas | https://academic.oup.com/rfs/article-abstract/22/6/2331/1592075 | **B** |
| Goldman-Rocholl-So (2013, RoF) | Los consejos conectados con el partido ganador reciben más contratos de gobierno | https://academic.oup.com/rof/article-abstract/17/5/1617/1582382 | B |
| Acemoglu et al. (2016, JFE) | La nominación de Geithner (nov-2008) da a las financieras conectadas un retorno anormal de alrededor de **6%** en el primer día y alrededor de **12%** en 10 días | https://www.nber.org/papers/w19701 | **B** |
| Cooper-Gulen-Ovtchinnikov (2010, JF) | El número de candidatos apoyados predice retornos anormales futuros; es más fuerte cuando el candidato puede ayudar a la empresa (magnitud no verificada) | https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2009.01548.x | **C** |
| Chen-Parsley-Yang (2015, **J. Business Finance & Accounting**, no JFQA) | Los portafolios de mayor intensidad de *lobbying* superan su *benchmark* en los 3 años siguientes | https://onlinelibrary.wiley.com/doi/10.1111/jbfa.12109 | **C** |
| Eggers-Hainmueller (2013, JOP) | El inversionista promedio del Congreso quedó **2-3% al año por debajo** del mercado en 2004-2008 | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1762019 | **B** |
| Belmont-Sacerdote et al. (2022, JPubE) | Sin desempeño superior en 2012-2020. Lo que compran los diputados rinde **−26 pb** a 6 meses | https://www.nber.org/papers/w26975 | **B**; la estrategia de copiar al Congreso es **D** |
| Cohen-Coval-Malloy (2011, JPE) | Cuando llega un presidente de comité poderoso, las empresas de su estado **recortan** inversión porque el gasto público las desplaza | https://www.nber.org/papers/w14504 | B |
| Wolfers-Zitzewitz (2004, JEP) | Los mercados de predicción agregan información bien, con sesgo *favorite-longshot* | https://www.aeaweb.org/articles?id=10.1257/089533004323015025 | B |

**Lectura del panel.** La academia dice tres cosas útiles. (1) La **sorpresa** se puede medir y mueve precios de forma predecible (A). (2) Las conexiones y la política redistribuyen valor **entre empresas** más que mover el índice (B). (3) Casi todas las anomalías de calendario político se degradaron o nunca fueron operables (D). La ventaja está en el corte transversal y en el instrumento, no en el calendario.

---

## 4. Lo más reciente, 2023-2026 (estado al 25-sep-2026)

### 4.1 La Fed: Warsh, primera alza desde 2023 y la independencia en tribunales

- **Liderazgo.** El Senado confirmó a Kevin Warsh como gobernador el 12-may-2026 y como presidente el 13-may por **54-45**. Fue la votación más dividida para un presidente de la Fed; sólo Fetterman cruzó la línea partidista. Juró el **22-may-2026** (CNN, CNBC, Spectrum). Powell sigue como **gobernador**, con periodo hasta 2028, mientras continúe la investigación del DOJ sobre la remodelación de la sede.
- **Última decisión (16-sep-2026).** Alza de 25 pb a **3.75-4.00%** por **12-0**, sin disensos. Es la primera alza desde julio de 2023. El comunicado dice que "*inflation remains elevated*" y habla de una "*timelier return*" a 2% (comunicado de la Fed). Del *dot plot*: Warsh no entregó punto; 16 de 18 participantes ven otra alza en 2026 y 4 ven dos; la mediana de 2026 es **4.125%** y la de 2027 sube de 3.6% a **4.1%** (TheStreet, TradingKey, Bondsavvy). Según Warsh, la inflación ha estado "*too high... for too long*".
- **Presión política.** Trump dijo que le recomendó a Warsh "*you might as well vote with the board because it's not going to matter*" y llamó al Consejo "*very hostile, very political*" (CNBC, 16-sep-2026). **Inferencia:** el costo político de subir tasas ya se pagó una vez. Una segunda alza el 28-oct o el 9-dic pondría a prueba la relación con la Casa Blanca antes y después de las intermedias.
- ***Trump v. Cook* (29-jun-2026).** Por **5-4**, la Suprema Corte negó suspender el amparo que impide destituir a la gobernadora Lisa Cook. La ley exige "*for cause*" con aviso y oportunidad de responder. En agosto de 2026 Trump notificó a Cook que "considera" destituirla, esta vez con el procedimiento (SCOTUSblog). **La independencia está protegida por procedimiento, no por inmunidad.**
- ***Trump v. Slaughter* (29-jun-2026).** Por **6-3**, la Corte revocó *Humphrey's Executor*: el presidente puede remover a voluntad a los comisionados de agencias independientes (FTC y, por extensión, SEC, FCC, etc.), **excepto la Fed**. **Inferencia:** la regulación y el antimonopolio en EUA ahora son política del Ejecutivo. Ganan valor el riesgo de "cambio de administración" y la negociación transaccional de fusiones.
- **Calendario restante:** 27-28 de octubre y 8-9 de diciembre (con SEP). En 2027: 26-27 ene, 16-17 mar\*, 27-28 abr, 8-9 jun\*, 27-28 jul, 14-15 sep\*, 26-27 oct y 7-8 dic\* (\* con SEP; Fed).

### 4.2 Tesoro: *refunding*, TGA y techo de deuda

- ***Refunding* del 5-ago-2026.** US$125 mil millones: 3 años por 58, 10 años por 42 y 30 años por 25. Refinancia US$96.3 mil millones y levanta US$28.7 mil millones nuevos. La guía mantiene los tamaños de cupones "*for at least the next several quarters*", con recompras de hasta US$38 mil millones en el trimestre. El Tesoro supone una **TGA de US$950 mil millones al cierre de septiembre y alrededor de US$1.05 billones a fines de octubre**. El próximo anuncio es el **4-nov-2026**, al día siguiente de las intermedias (Tesoro, comunicado sb0590).
- **Por qué importa.** Si la TGA sube, drena reservas bancarias y liquidez. Si cambian los tamaños de cupones, cambia la prima por plazo. Una sorpresa al alza en cupones es un *shock* de *duration*. **Regla:** en cada *refunding* se revisan tres cosas: los tamaños y la frase "*several quarters*", la TGA proyectada y la mezcla entre *bills* y cupones.
- **Techo de deuda.** La OBBBA lo subió **US$5 billones, a US$41.1 billones** (sin suspensión). El BPC estima que se alcanzará **entre finales del invierno y mediados del verano de 2027**, con medidas extraordinarias de 6 a 9 meses, lo que pone el *X-date* entre finales de 2027 y principios de 2028. Ya se usó más de la mitad del aumento.

### 4.3 Congreso: OBBBA, presupuesto y cripto

- **OBBBA (firmada el 4-jul-2025).** Según la CBO, sube el déficit **US$3.4 billones en 10 años**, o US$4.1 billones con intereses. Hace **permanente la depreciación inmediata de 100%** para bienes adquiridos después del 19-ene-2025. Recorta el IRA: se pierden los créditos 45Y y 48E para proyectos eólicos y solares que **inicien construcción desde el 4-jul-2026** y entren en servicio después de 2027. Elimina los créditos de vehículos eléctricos y varios de eficiencia (Sidley, CRFB, BPC). **Inferencia:** el calendario del IRA adelanta arranques de obra a 2025-2026 y deja un precipicio de demanda en 2028 para desarrolladores de renovables en EUA.
- **Año fiscal 2027.** La resolución continua (CR, H.R. 6500) extiende los niveles de 2026 **hasta el 11-dic-2026**. Pasó el Senado 90-6 el 8-ago, la Cámara 370-48 el 1-sep y se firmó el 2-sep (FedTools). Se evitó el cierre del 1-oct y el siguiente precipicio cae en la **sesión *lame duck*** posterior a las intermedias.
- **Cripto.** La GENIUS Act (stablecoins) es ley desde julio de 2025. La CLARITY Act (estructura de mercado) **fracasó en la votación de cloture 49-50 el 15-sep-2026**, y la senadora Lummis advierte que la próxima oportunidad realista podría ser 2030 (CNBC, DWT).
- **Intermedias del 3-nov-2026.** Probabilidad de Senado demócrata: **55% en Kalshi** y **59% en Polymarket**. Según Kalshi, el resultado más probable es control demócrata de ambas cámaras (**46%**), seguido de Senado republicano con Cámara demócrata (38%) (CNBC, 16-sep-2026). Antes de la guerra con Irán los republicanos tenían alrededor de 60% de probabilidad de retener el Senado.

### 4.4 Aranceles: de IEEPA a 122, 301 y 232

- **IEEPA.** El 20-feb-2026 la Suprema Corte decidió por 6-3 que IEEPA no autoriza aranceles (*Learning Resources v. Trump*). La CBP abrió CAPE (fase 1 el 20-abr, fase 2 el 29-jun). A fines de julio había **US$128.68 mil millones** en reembolsos aceptados para trámite, y el DOJ apeló la orden de reembolso universal de la CIT (Holland & Knight, Skadden). **Inferencia:** los reembolsos son ganancias no recurrentes en los 10-Q de 2026 de importadores y minoristas, y deben excluirse de las utilidades normalizadas.
- **Sección 122.** 10% global del 20-feb al 24-jul-2026, fecha en que expiró por ley a los 150 días (ver cap. 23).
- **Sección 301 "*forced labor*" (desde el 24-jul-2026).** 10% o 12.5% a 60 economías. **México 10%**, pero están **exentos los bienes que entran libres de arancel bajo el T-MEC** y los bienes bajo programas 232 (Global Trade Alert, Honigman, BBVA Research). **Inferencia:** para México, la tasa de cumplimiento de reglas de origen del T-MEC es hoy la variable arancelaria más importante.
- **Sección 232.** Autos y autopartes 25%; los vehículos que cumplen el T-MEC pagan sólo sobre el contenido no estadounidense. Camiones medianos y pesados 25% y autobuses 10% desde el 1-nov-2025. Acero y aluminio 50%. **Fármacos patentados y sus ingredientes activos 100%**, vigente desde el **31-jul-2026** para empresas grandes y el **29-sep-2026** para las pequeñas. Quedan exentas las empresas con acuerdo de precios MFN firmado antes del 2-abr-2026 (Crowell, Foley Hoag). Al 4-sep-2026 había acuerdos MFN con **26 empresas, alrededor de 89% del mercado de marca** (Duane Morris, Casa Blanca).

### 4.5 Antimonopolio, SEC, CFTC y FDA

- **Google.** El 2-sep-2026 la jueza Brinkema **rechazó** obligar a vender AdX y DFP y ordenó sólo remedios de conducta, como interoperar con Prebid (CNBC, DOJ). Es el segundo caso de Google, después del de búsqueda en 2025, en que no hay ruptura estructural.
- **Paramount-WBD.** El plazo HSR expiró el 19-feb-2026 sin demanda del DOJ. Doce estados demandaron el 13-jul y obtuvieron una orden temporal el 20-jul. El **21-sep-2026** hubo un acuerdo con compromisos de conducta: 30 películas al año en cines y un consejo de independencia editorial para CBS News y CNN. El cierre se espera "a más tardar a principios de octubre", pero un juez admitió una moción contra el acuerdo (CNN, Variety, Deadline). **Inferencia:** el antimonopolio federal se volvió negociable y los estados son hoy el jugador con veto relevante.
- **SEC.** El 5-may-2026 propuso el informe semestral **opcional** (Formulario 10-S en lugar de tres 10-Q), con comentarios hasta el 6-jul-2026. Si se aprueba, habrá menos datos duros por empresa y los trimestres 1 y 3 quedarían en comunicados 8-K. **Regla:** en una empresa que se cambie al régimen semestral, se sube el descuento por incertidumbre informativa y se reduce el tamaño de la posición alrededor de sus reportes.
- **CFTC y mercados de predicción.** Propuesta de regla del 10-jun-2026: prohíbe apuestas sobre guerras y asesinatos y legaliza las deportivas. Hay litigio con estados (Tercer Circuito a favor de Kalshi el 7-abr-2026; Nevada en el Noveno Circuito) y acciones contra *insider trading* en contratos de eventos (abr-2026).
- **FDA.** El Commissioner's National Priority Voucher promete revisiones de **1 a 2 meses** en vez de 10 a 12. Tuvo su séptima aprobación el 8-may-2026 y decide un comité de altos funcionarios encabezado por Prasad. Richard Pazdur cuestiona su legalidad y su seguridad (FDA, BioSpace, PBS). **Inferencia:** la aprobación regulatoria incorpora criterios de política como la relocalización y el precio. Una empresa con acuerdo MFN tiene, de hecho, un canal preferente.

### 4.6 Política industrial: el Estado como accionista

- **Intel:** el gobierno compró **433.3 millones de acciones a US$20.47 (9.9%)**, pagadas con US$5.7 mil millones de CHIPS no desembolsados y US$3.2 mil millones de Secure Enclave. Las acciones no dan asiento en el consejo y su voto es limitado (Intel, ago-2025).
- **MP Materials:** 15% en manos del DoD, que es el mayor accionista. En ene-2026 el gobierno entró también en USA Rare Earth (Fortune). En opinión del Washington Post (ago-2026), el Departamento de Comercio ha gastado alrededor de US$4 mil millones en participaciones "desde diciembre". Una encuesta de CNBC de jul-2026 encontró que 49% de los votantes considera inapropiadas esas participaciones y 19% las apoya.
- **Inferencia:** una empresa con el gobierno como accionista tiene un **piso implícito**, porque el gobierno no la deja caer. Pero tiene un **techo político**: precios, clientes y asignación de capital quedan sujetos a presión, y el apoyo se revierte si cambia el Congreso. Se modela como una opción con dos colas, no como un respaldo gratuito.

### 4.7 México: Paquete Económico 2027 (entregado el 8-sep-2026)

Lo entregó el secretario de Hacienda Édgar Amador (comunicado SHCP 71; Expansión; Investing; adn40):

| Variable | Paquete 2027 | Nota |
|---|---|---|
| PIB 2027 | **1.5-2.5%** (puntual 2.0%) | Antes 1.9-2.9%. PIB 2026: 1-2% |
| RFSP 2027 | **3.9% del PIB** | 4.1% estimado para 2026. En Pre-Criterios se planteaba 3.5% |
| Balance primario | alrededor de 1.1% del PIB (Investing) | (no verificado en fuente primaria) |
| Deuda (SHRFSP) | alrededor de 55% del PIB (Investing) | (no verificado en fuente primaria) |
| Ingresos tributarios | **15.9% del PIB**, "máximo histórico" | Sin impuestos nuevos. Más control de IEPS a combustibles y retenciones de IVA e ISR a plataformas digitales |
| Costo financiero | MXN 1.575 billones, **17.2% de los ingresos presupuestarios**, el más alto desde 1999 (Investing) | La restricción fiscal que vigila Moody's |
| Gasto neto | MXN 10.636 billones | Salud MXN 1.1 billones (+10.9%) |
| Apoyo a Pemex | cae a **MXN 81.1 mil millones (−70%)** (Investing) | Expansión (24-sep): Pemex seguirá necesitando hasta US$10 mil millones anuales |
| Tipo de cambio | 17.9 (adn40) o 18.0 (Investing) | Discrepancia entre fuentes secundarias |
| Inflación y tasa | 3.0% al cierre de 2027; tasa de 6.0% al cierre de 2027 | Implica que Hacienda supone 50 pb más de recortes de Banxico |

**Calendario legal:** la Ley de Ingresos debe aprobarse en Diputados a más tardar el **20-oct** y en el Senado el **31-oct**. El Presupuesto de Egresos se aprueba en Diputados a más tardar el **15-nov**. **Inferencia:** con mayoría holgada no hay riesgo de que no se apruebe. Lo que vale la pena pronosticar es si el RFSP aprobado se desvía de 3.9%, si se agregan medidas recaudatorias en comisiones y cómo se ejerce el apoyo a Pemex.

### 4.8 Banxico

- **Trayectoria:** 7.00% (pausa del 5-feb-2026), luego **6.75%** (26-mar) y **6.50%** (7-may). Después mantuvo la tasa el 25-jun, el 6-ago y el **24-sep-2026**, este último por unanimidad (listado de anuncios de Banxico). Es la **tercera** pausa consecutiva. Expansión dice "cuarta", pero el listado oficial la contradice.
- **Mensaje:** prevé que la inflación llegue a la meta en el **4T-2027**. Destaca la "ausencia de presiones de demanda" y que la política mexicana **no seguirá mecánicamente a la Fed** (Proceso, Investing).
- **Diferencial:** 6.50% contra el techo de la Fed de 4.00% da **250 pb**, contra más de 600 pb en 2023. **Inferencia:** el colchón de *carry* del peso es el más delgado en años. Si la Fed sube otra vez y Banxico no se mueve, el diferencial baja a alrededor de 225 pb, y la sensibilidad del peso a *shocks* de riesgo sube (ver cap. 16).
- **Calendario restante 2026:** decisiones el **5-nov** y el **17-dic**; minutas el 8-oct y el 19-nov; Informe Trimestral el 26-nov (calendario oficial de Banxico). La minuta de diciembre se publica el 7-ene-2027.

### 4.9 Reformas y Estado de derecho en México

- **Reforma judicial (2024).** Tras la elección del 2-jun-2024 y el apoyo a la reforma, el peso cayó **4.3% en días** (de 16.97 a 17.70), alrededor de **16%** hasta inicios de septiembre, rozó 20 con la aprobación en Diputados y cerró 2024 con **−22.5%** (El Financiero, Infobae, CNN/EFE). Es el caso de referencia del **riesgo institucional mexicano**. La nueva SCJN entró en funciones en sep-2025. En may-2026 se aprobó aplazar la **segunda elección judicial de 2027 a 2028** (Senado 29-may; Diputados 26-may) (La Jornada, MVS).
- **Nueva SCJN y cobro fiscal: el caso Elektra.** La Corte resolvió que Elektra y TV Azteca deben pagar **MXN 48.3 mil millones** (ISR de 2008-2013). Elektra reconoció un adeudo de MXN 32.1 mil millones, pagó MXN 13.98 mil millones y liquida el resto en parcialidades hasta **jul-2027**. En el 4T reportó una pérdida de casi MXN 20 mil millones (Bloomberg Línea, La Silla Rota, El Imparcial). **Lección:** un litigio fiscal que antes era una contingencia de probabilidad baja pasó a ser un **pasivo cierto**.
- **Reforma a la Ley de Amparo** (DOF 16-oct-2025, en vigor el 17-oct). El interés legítimo exige una afectación "real, actual y diferenciada". En materia fiscal, la suspensión sólo procede con **garantía** del interés fiscal. El amparo contra el cobro sólo procede hasta la convocatoria de remate. Y la reforma **aplica a juicios en trámite** (DLA Piper, GT). **Regla:** cualquier emisora mexicana con créditos fiscales relevantes en litigio lleva en el modelo la probabilidad de pagar el 100% más accesorios, y no la de "litigar indefinidamente".
- **Órganos autónomos.** Cofece e IFT desaparecen. La competencia económica pasa a la **Comisión Nacional Antimonopolio**, organismo descentralizado sectorizado a la Secretaría de Economía (Senado jun-2025, Diputados jul-2025). La regulación de telecomunicaciones pasa a la **Comisión Reguladora de Telecomunicaciones (CRT)**, instalada el 17-oct-2025. **Inferencia:** los reguladores ya no son independientes del Ejecutivo, y los resultados en telecomunicaciones, concentraciones y preponderancia se deben pronosticar como decisiones políticas.
- **Energía.** Las leyes secundarias están en vigor desde el **19-mar-2025**. Pemex y CFE son "empresas públicas del Estado" y la **Comisión Nacional de Energía**, desconcentrada de SENER, sustituye a la CRE y a la CNH. En 2025 el gobierno inyectó alrededor de US$35 mil millones a Pemex (1.9% del PIB, según Moody's) y hubo **P-Caps por US$12 mil millones** en jul-2025. Moody's ratificó a Pemex en **B1 estable** (may-2026).
- **Límite de la coalición.** La reforma electoral fracasó el 11-mar-2026 porque PT y PVEM votaron en contra. Hay que pronosticar los votos de los aliados, no los de Morena.

### 4.10 Calificación soberana

| Agencia | Calificación | Perspectiva | Fecha de la última acción |
|---|---|---|---|
| Moody's | **Baa3** (bajó de Baa2) | Estable | 20-may-2026 |
| S&P | BBB | **Negativa** | 12-may-2026 |
| Fitch | BBB- | Estable | mar-2026 |

Moody's citó el deterioro fiscal, la base de ingresos limitada, el gasto rígido y el apoyo a Pemex en un entorno de bajo crecimiento. Al pasar de perspectiva negativa a estable, no espera cambios en 18 meses. **Inferencia (índices):** con la regla de "calificación intermedia" que usan índices de grado de inversión como el Bloomberg Agg (no verificada en esta sesión), hoy la calificación intermedia es **BBB-**. Para que México salga del grado de inversión en índices, **dos agencias** tendrían que bajarlo a especulativo. El riesgo inmediato es que S&P baje a BBB-, lo que no provoca ventas forzadas pero deja a las tres agencias en el último escalón.

### 4.11 T-MEC, aranceles y seguridad

- **Revisión conjunta del 1-jul-2026:** EUA **no aceptó** extender el tratado. Su vigencia sigue hasta el 1-jul-2036, con **revisiones anuales** (USTR, White & Case). Hubo rondas bilaterales con México: 29-may (CDMX), junio (Washington) y 21 al 23 de julio (CDMX). La cuarta está anunciada para Washington en septiembre, con fecha tentativa del **28-29 de sep** sin confirmar al 23-sep (El Heraldo). Canadá no participa en las bilaterales.
- **Lo que está en juego:** EUA exige que **50% del valor de cada vehículo sea estadounidense**. México pide bajar el 232 a autos (25%) y a acero y aluminio (50%) antes de conceder otras cosas. Los analistas esperan una prolongación "dolorosa" hasta fines de 2026 o 2027 (TLC Magazine, UC Davis MexAg).
- **Aranceles mexicanos:** desde el 1-ene-2026 hay aranceles de **5% a 50%** en **1,463 fracciones** a países sin tratado (China, India, Corea, entre otros), con meta de recaudar más de MXN 70 mil millones (DOF, prensa). **Inferencia:** México se alineó con la agenda de EUA frente a China como moneda de cambio en la revisión.
- **Plan México** (ene-2025): meta de inversión de más de 25% del PIB desde 2026 y 28% en 2030. Hay 14 Polos de Desarrollo para el Bienestar aprobados entre jun-2025 y jun-2026, y 6 con desarrollador y alrededor de **US$17.49 mil millones comprometidos** (Segundo Informe).
- **Seguridad y finanzas.** El 25-jun-2025 FinCEN emitió órdenes contra **CIBanco, Intercam y Vector** y la CNBV los intervino. Los fideicomisos de CIBanco pasaron a Multiva y parte de Intercam a Kapital (Mayer Brown, Federal Register). El 23-sep-2026 El Financiero, citando al NYT, reportó que Trump **frenó planes de ataques aéreos** contra cárteles por el endurecimiento del gobierno de Sheinbaum. Ella rechaza operaciones conjuntas en territorio mexicano. **Inferencia:** el riesgo de seguridad llega a los precios por el sistema financiero (FinCEN, OFAC, cárteles designados como FTO) antes que por la violencia misma.

---

## 5. Evidencia real

### 5.1 Eventos de política y reacción medida

| Evento | Tipo de instrumento | Reacción | Lección |
|---|---|---|---|
| Elección de 2000 en EUA | Elección | Suben las empresas conectadas con republicanos y bajan las conectadas con demócratas (Goldman-Rocholl-So) | El valor político es transversal |
| Nominación de Geithner (2008) | Nombramiento | Financieras conectadas: +6% el primer día y +12% en 10 días (Acemoglu et al.) | Los nombramientos son eventos operables en el corte transversal |
| Elección de 2016 en EUA | Elección | Ganan domésticas y de impuestos altos; lo complejo se priceó con rezago (Wagner et al.) | Hay ventaja en analizar lo complejo |
| Elección de México del 2-jun-2024 | Elección más reforma constitucional | Peso −4.3% en días y −22.5% en 2024 | La mayoría calificada es un evento de régimen, no de ciclo |
| Aranceles del 2-abr-2025 | IEEPA | S&P −10% en 2 sesiones y reversión con la pausa (cap. 23) | Instrumento frágil, reversión probable |
| Suprema Corte e IEEPA (20-feb-2026) | Judicial | Reembolsos por US$128.68 mil millones aceptados a julio; sustituto inmediato (122 y luego 301) | Se anticipa el **instrumento sustituto** |
| Rebaja de Moody's (20-may-2026) | Calificación | Anunciada y "sin sobresaltos" (El Financiero) | La calificación va detrás del mercado; importa la **segunda** rebaja |
| Alza de la Fed (16-sep-2026) | Política monetaria | Primera alza desde 2023; mediana de 2027 sube a 4.1% | La sorpresa estuvo en el *path*, no sólo en el *target* |

### 5.2 Qué funciona y qué no (panel)

- **Funciona (A/B):** medir la sorpresa contra futuros; anticipar sustitutos de un instrumento que caduca o que va a ser anulado; analizar ganadores y perdedores en el corte transversal (impuestos, exposición internacional, contenido regional); usar mercados de predicción como precio de referencia.
- **Ya no funciona (D):** la deriva pre-FOMC. Desapareció después de 2015 (Kurov et al.), y en el régimen Warsh, con menos guía, la varianza del día del anuncio es mayor. Tampoco el "presidential puzzle" como regla (N de alrededor de 20 presidencias). Tampoco copiar las compras del Congreso: el promedio **pierde** contra el mercado.
- **Dudoso (C):** comprar empresas con mucho *lobbying* o muchas contribuciones. En muestra hay retorno, pero puede ser un factor de tamaño o rentabilidad y hay costos de implementación.
- **Evidencia del propio ciclo:** en 2025-2026 casi todas las medidas extremas basadas en **declaración u orden ejecutiva frágil** se pausaron, se anularon o se reemplazaron. Las basadas en **ley o en 232** persistieron (acero 50%, autos 25%, depreciación de 100%, fin de créditos del IRA).

### 5.3 Mercados de predicción como *benchmark*

Sirven para tres cosas: (1) medir la probabilidad implícita de eventos que no tienen futuros financieros, como elecciones, confirmaciones o votaciones de cloture; (2) servir de **línea base** para calificar los pronósticos del dueño; (3) detectar cambios bruscos de probabilidad. Los límites: el sesgo *favorite-longshot*, las reglas de resolución (cap. 23, trampa 6), la liquidez y el riesgo regulatorio de la plataforma (CFTC y estados en 2026).

---

## 6. Traducción operable

### 6.1 Método de 8 pasos para anticipar una decisión de política

1. **Pregunta resoluble.** Qué, quién, cuándo y con qué criterio se resuelve, y en qué fuente (DOF, Federal Register, comunicado).
2. **Instrumento y durabilidad** (tabla 2.4): vía de impugnación y caducidad.
3. **Calendario legal:** plazos constitucionales, reglamentarios y judiciales. Ejemplos: la Ley de Ingresos el 20-oct, la CR el 11-dic, la 122 a los 150 días, la iniciativa preferente del 1-feb en México.
4. **Mapa de actores:** qué gana cada uno (voto, presupuesto, carrera, relación con EUA) y quién tiene veto (PT y PVEM, el Senado de EUA con 60 votos, la SCJN, los estados en EUA, las calificadoras).
5. **Señales.** Una **señal costosa** es un presupuesto asignado, una publicación en el DOF, un nombramiento o un gasto de capital político. Una **señal barata** es una declaración, un *post* o una mañanera. La señal costosa pesa de 3 a 5 veces más (Inferencia de panel, a calibrar con el *ledger*).
6. **Precio implícito:** futuros, OIS, TIIE-IRS, CDS, Kalshi y Polymarket leyendo la regla, y *spreads* de fusiones.
7. **Pronóstico** con probabilidad, horizonte y criterio, registrado **antes** del evento.
8. **Cadena causal** hasta el precio: acontecimiento → exposición → efecto económico → estado financiero → valoración → diferencia contra lo que descuenta el precio (ideas adoptadas, punto 9).

### 6.2 Protocolo para la ventaja del ex funcionario (verificable)

**Dónde está la ventaja legítima:** conocer los procesos (cómo se redacta un decreto, quién firma, cuánto tarda una publicación en el DOF, cómo negocia Hacienda con Energía, qué significa que un tema salga o no en la mañanera) y **leer incentivos**. **Dónde no está:** en la información no pública obtenida por relaciones. Operar con ella es uso de información privilegiada, sancionado por la Ley del Mercado de Valores y la CNBV en México y por la Regla 10b-5 de la SEC en EUA, incluso bajo la teoría de la apropiación indebida. Es un límite duro, no una preferencia.

**Registro en el *ledger*** (`herramientas/pronosticos.py agregar`):
- `autor`: `dueno` o `claude`, para calificar a cada uno por separado.
- `pregunta` y `criterio_resolucion`: un enunciado binario con fuente de resolución.
- `notas`: `tipo=[timing|contenido|magnitud|reaccion]; ventaja=[proceso|incentivos|calendario|lectura_publica]; p_mercado=0.xx (plataforma, regla)`.

**Cómo se califica:** el Brier propio contra el objetivo de config (**≤ 0.20**, con un mínimo de **50** pronósticos) y además la **habilidad sobre el mercado** = Brier(p_mercado) − Brier(propio). Si la habilidad es mayor que 0 con 50 o más pronósticos, hay ventaja demostrada. Si no, la experiencia no se traduce en precio. Se separa por `tipo`: lo típico es acertar en *contenido* y *timing* y fallar en *reacción* (cap. 23, trampa 7).

**Regla:** sólo los tipos de pregunta en que el dueño muestre habilidad positiva sobre el mercado con N ≥ 30 pueden usarse para dimensionar posiciones del satélite.

### 6.3 Calendario político-regulatorio (25-sep-2026 a jul-2027)

| Fecha | Evento | Instrumento de mercado | Qué pronosticar |
|---|---|---|---|
| 28-29 sep (tentativo) | Cuarta ronda T-MEC en Washington | USD/MXN, autopartes, acero | ¿Hay alivio del 232 o contenido estadounidense de 50%? |
| 29 sep | Arancel 232 a fármacos para empresas pequeñas | Farmacéuticas medianas | ¿Más acuerdos MFN? |
| 5 oct | Inicia el periodo de la Suprema Corte de EUA (1er lunes de octubre) | Sectores con litigio pendiente | Admisiones y órdenes |
| 8 oct | Minuta de Banxico | TIIE-IRS | ¿Disensos o sesgo? |
| 20 oct / 31 oct | Ley de Ingresos 2027 en Diputados / Senado | Bonos M, Udibonos | Cambios contra la iniciativa |
| 27-28 oct | FOMC (sin SEP) | Fondos federales, Treasuries, dólar | ¿Segunda alza? |
| 3 nov | Intermedias en EUA | Sectores sensibles (6.5) | Control de las cámaras (Kalshi/Polymarket) |
| 4 nov | *Refunding* del Tesoro | Plazos largos | ¿Cambia "*several quarters*"? |
| 5 nov | Banxico | Peso, TIIE | ¿Pausa o recorte? |
| 15 nov | Presupuesto de Egresos 2027 | Emisoras con contratos de gobierno | Reasignaciones |
| 19 / 26 nov | Minuta de Banxico / Informe Trimestral | TIIE | Pronósticos de inflación |
| 8-9 dic | FOMC con SEP | Todo | *Dots* de 2027 |
| 11 dic | Vence la CR en la sesión *lame duck* | Contratistas, defensa | ¿Nueva CR, *omnibus* o cierre? |
| 17 dic | Banxico | Peso | Última de 2026 |
| 10 ene 2027 | Vence la tregua EUA-China (cap. 23) | Tecnología | ¿Extensión? |
| Fin de invierno a mediados de 2027 | Se alcanza el techo de deuda (BPC) | *Bills*, CDS de EUA | Negociación con un Congreso posiblemente dividido |
| 6 jun 2027 | Elecciones intermedias en México | Peso, emisoras reguladas | ¿Morena y aliados conservan la mayoría calificada? |
| 1 jul 2027 | Segunda revisión anual del T-MEC | Exportadores | ¿Extensión? |
| jul 2027 | Última parcialidad de Elektra al SAT | — | Cumplimiento |
| 31 ene 2028 | Vence el periodo de Powell como gobernador | Fed | ¿Otra vacante? |

**Regla:** este calendario se revisa cada lunes. Cada evento binario abre una entrada en el *ledger* con al menos 5 días hábiles de anticipación.

### 6.4 Checklist de riesgo regulatorio por empresa (0 a 3 puntos por renglón)

| # | Dimensión | 0 | 3 |
|---|---|---|---|
| 1 | % de ingresos que dependen del gobierno (contratos, subsidios, precios regulados) | <5% | >40% |
| 2 | Concesión o licencia necesaria para operar y su plazo | No aplica | Renovación en menos de 3 años o discrecional |
| 3 | Exposición arancelaria: origen de insumos y ventas, % que cumple el T-MEC | Doméstica o cumple | Más de 30% de ventas expuesto a 232 o 301 sin exención |
| 4 | Antimonopolio: participación de mercado y operaciones pendientes | Sin operaciones y baja participación | Fusión pendiente o preponderancia |
| 5 | Fiscal: créditos en litigio sobre capital contable | 0 | >10% del capital (post reforma al amparo, sin colchón) |
| 6 | Política industrial: beneficiario, gobierno accionista o blanco | Neutral | El gobierno es accionista o el precio depende de un subsidio con fecha |
| 7 | Regulador sectorial (FDA, CNE, CRT, CNBV, FERC) con decisión en 12 meses | No | Decisión binaria material |
| 8 | Seguridad y AML: FinCEN, OFAC, FTO, contrapartes en zonas de riesgo | Sin exposición | Antecedentes o clientes en sectores señalados |
| 9 | Conexiones políticas y partes relacionadas | Sin conexiones | El control depende de una relación con el gobierno en turno |
| 10 | Durabilidad del marco que sostiene la tesis | Ley o constitución | Orden ejecutiva, declaración o litigio abierto |
| 11 | Evento binario de política dentro del horizonte de la posición | No | Sí, en menos de 30 días |
| 12 | Riesgo soberano indirecto (calificación, transferencias, Pemex y CFE como contraparte) | Bajo | Proveedor o acreedor relevante de Pemex o CFE |

**Traducción a acción (Regla):**
- **0 a 8 puntos:** tamaño normal según config.
- **9 a 16:** descuento de valoración de al menos 10% sobre el valor intrínseco y máximo la mitad del límite por emisora (0.05 del capital en el perfil estándar y 0.15 en arena).
- **17 o más:** sólo como posición de evento con tesis escrita sobre el resultado regulatorio, con riesgo ≤ `max_riesgo_pct_capital` (0.01 estándar, 0.005 en fase de prueba, 0.03 en arena) y fecha de salida atada al evento.
- **Renglones 5 u 8 en 3:** veto automático hasta revisión del dueño. Es el tipo de riesgo que termina en pérdida permanente.

### 6.5 Sectores y emisoras sensibles a la política (ejemplos de exposición, no recomendaciones)

**EUA**

| Sector | Palanca | Estado al 25-sep-2026 | Qué vigilar |
|---|---|---|---|
| Farmacéuticas | 232 al 100%, acuerdos MFN, vouchers de la FDA | 26 empresas con MFN (alrededor de 89% del mercado de marca) | Quién queda fuera de los acuerdos; legalidad del CNPV |
| Semiconductores | Participaciones CHIPS, controles de exportación, 232 | Intel con 9.9% del gobierno | Condiciones de futuros apoyos; China (cap. 23) |
| Minerales críticos | Participaciones del DoD | MP Materials 15%; USA Rare Earth | Si el Congreso cambia, revisión de apoyos |
| Renovables | OBBBA | Sin créditos para obras iniciadas desde el 4-jul-2026 | Precipicio en entradas en servicio de 2028 |
| Autos y camiones | 232 (25%) y T-MEC | Demanda de 50% de contenido estadounidense | Resultado de las rondas con México |
| Medios y tecnología | Antimonopolio politizado | Paramount-WBD con acuerdo; Google sin ruptura | Estados como jugador con veto |
| Importadores y minoristas | 301 de 10-12.5%; reembolsos IEEPA | US$128.68 mil millones aceptados | Ganancias no recurrentes y apelación del DOJ |
| Cripto e intermediarios | GENIUS (ley), CLARITY (frenada) | Cloture 49-50 | Horizonte legislativo hasta 2030 |
| Contratistas y defensa | CR hasta el 11-dic | Niveles de 2026 | Cierre en la sesión *lame duck* |

**México**

| Sector | Palanca | Estado | Qué vigilar |
|---|---|---|---|
| Bancos | Banxico, FinCEN, CNBV | Tasa de 6.50%; precedente CIBanco, Intercam y Vector | Fin del ciclo de recortes; márgenes; AML |
| Energía (Pemex, CFE, generadores privados) | Leyes de 2025, PEF 2027 | Apoyo a Pemex −70% en 2027 (Investing) | Ejecución del apoyo; pagos a proveedores |
| Telecom y radiodifusión | CRT y Comisión Antimonopolio (Ejecutivo) | Reguladores nuevos | Preponderancia, espectro, concesiones |
| Exportadores y autopartes | T-MEC, 232, 301 | Exentos de la 301 si cumplen el T-MEC | Contenido estadounidense de 50%, rondas |
| Acero y metales | 232 al 50% | Sin alivio | Negociación; protección vía aranceles a Asia |
| Grupos con litigios fiscales | Nueva SCJN, amparo | Elektra paga MXN 32.1 mil millones en parcialidades | Otros grandes contribuyentes |
| Construcción, cemento, parques industriales | Plan México, Polos de Bienestar | US$17.49 mil millones comprometidos en 6 polos | Asignaciones del PEF 2027 |
| Consumo (bebidas, tabaco, plataformas) | IEPS, retenciones | Sin impuestos nuevos en 2027; control de plataformas | Cambios en comisiones de la Cámara |

### 6.6 Protocolo ante un evento de política no programado

- **T+0 (menos de 2 horas):** (1) se identifica el instrumento y su durabilidad; (2) se mide la reacción contra la probabilidad previa (mercado de predicción o precio); (3) se clasifican ganadores y perdedores por canal (2.1); (4) si el instrumento es frágil, se **prohíbe vender en pánico** posiciones perdedoras sólo por el titular.
- **T+1 día:** se busca la ruta de impugnación (tribunal, plazo, precedente) y el instrumento sustituto probable. Se abre la entrada en el *ledger*: "¿seguirá vigente en 90 días?".
- **T+1 semana:** cadena causal completa hasta el estado financiero de cada emisora expuesta. Sólo con esa cadena se opera, y dentro de los límites de pérdida del periodo.
- **Siempre:** ningún tamaño supera `max_riesgo_pct_capital` del perfil. Si el evento toca un límite diario, semanal o mensual, no se abren posiciones tácticas nuevas.

### 6.7 Parámetros propuestos (a integrar en `parametros.json`; no se modifica aquí)

```json
"politica": {
  "evento_binario_riesgo_max_estandar": 0.01,
  "evento_binario_riesgo_max_arena": 0.03,
  "checklist_regulatorio_umbral_medio": 9,
  "checklist_regulatorio_umbral_alto": 17,
  "descuento_valoracion_riesgo_medio": 0.10,
  "habilidad_min_para_dimensionar": 0.0,
  "n_min_pronosticos_por_tipo": 30,
  "prohibido": ["operar deriva pre-FOMC", "copiar operaciones del Congreso", "informacion no publica"]
}
```

Son coherentes con `riesgo_por_operacion` (0.01 y 0.03 en arena), `pronosticos.brier_objetivo` (0.20) y `min_pronosticos_para_evaluar` (50).

### 6.8 Fuentes primarias a monitorear (automatización en el cap. 22)

- **EUA:** federalreserve.gov (comunicados, SEP, minutas, calendario); treasury.gov (*refunding*, subastas); federalregister.gov; congress.gov (texto y CRS); ustr.gov; cbp.gov (mensajes CSMS); supremecourt.gov (opiniones y órdenes); sec.gov (EDGAR 8-K); fda.gov; CFTC.
- **México:** dof.gob.mx (edición matutina y vespertina; la vigencia está en los transitorios); Gaceta Parlamentaria de Diputados y Gaceta del Senado; finanzaspublicas.hacienda.gob.mx (Criterios, Pre-Criterios, informes trimestrales); banxico.org.mx; CNBV; SAT (Resolución Miscelánea Fiscal); SE (T-MEC); comunicados de las calificadoras.

---

## 7. Trampas

1. **Reaccionar a la noticia y no a la sorpresa.** Si ya estaba en el precio, no hay nada que operar (Bernanke-Kuttner).
2. **Confundir declaración con instrumento.** Una declaración cuesta cero y se revierte a costo cero. Lo que cuenta es lo que se publica en el DOF o el Federal Register, lo que se presupuesta y lo que se firma.
3. **Suponer permanencia de instrumentos frágiles.** IEEPA cayó, la 122 caducó y la 301 las sustituyó. Quien apostó al titular original perdió dos veces.
4. **Suponer que un instrumento anulado significa que la política terminó.** El Ejecutivo busca un sustituto. Hay que pronosticar el **instrumento siguiente**.
5. **Operar la deriva pre-FOMC o el ciclo presidencial.** Una desapareció y el otro tiene N de alrededor de 20. Es D.
6. **Copiar al Congreso.** El promedio pierde contra el mercado (Eggers-Hainmueller; Belmont et al.). Los ETFs que lo replican venden una narrativa, no una ventaja.
7. **Tratar la mayoría legislativa como un bloque.** En México los aliados tumbaron la reforma electoral y en EUA la cloture de la CLARITY Act perdió 49-50.
8. **Leer el *dot plot* como pronóstico.** La mediana de 2022 en dic-2021 fue 0.9% y la tasa terminó en 4.25-4.50%. Con Warsh sin punto, el *dot plot* informa aún menos sobre el presidente.
9. **Ignorar el nuevo régimen legal mexicano.** Después de la reforma al amparo, la suspensión fiscal exige garantía y la reforma aplica a juicios en trámite. Un litigio fiscal ya no es una opción gratuita.
10. **Ver a un gobierno accionista como una garantía.** Da piso, pero también pone techo y un riesgo de reversión si cambia el Congreso.
11. **Confundir acierto de *timing* o contenido con acierto de reacción.** Se califican por separado en el *ledger*.
12. **Usar una sola fuente secundaria para cifras fiscales.** En esta sesión dos fuentes dieron tipos de cambio distintos (17.9 contra 18.0) y otra dio mal el número de pausas de Banxico. La fuente primaria manda.
13. **Cruzar la línea de la información privilegiada.** El riesgo legal y reputacional no compensa ningún rendimiento y destruye el activo principal del dueño.
14. **Olvidar el tipo de cambio.** Un evento de política de EUA medido en MXN puede tener el signo contrario (cap. 16).

---

## 8. Examen de titulación

**1. La Fed sube 25 pb y el S&P cae 1.5% ese día. ¿Qué dato falta para interpretarlo?**
La expectativa previa: la probabilidad implícita en los futuros de fondos federales y el *path* esperado. Si el alza estaba descontada al 100%, la caída vino del *path* o de la conferencia (el factor de Gürkaynak-Sack-Swanson), no del *target*.

**2. ¿Quién preside la Fed al 25-sep-2026 y cuál fue la última decisión?**
Kevin Warsh: confirmado 54-45 el 13-may-2026 y juramentado el 22-may. El 16-sep-2026 la Fed subió 25 pb a 3.75-4.00% por 12-0, la primera alza desde jul-2023. Warsh no entregó punto, y la mediana de 2026 es 4.125% y la de 2027, 4.1%.

**3. ¿Qué resolvieron *Trump v. Cook* y *Trump v. Slaughter*, y qué implican para el mercado?**
En *Cook* (5-4, 29-jun-2026) la gobernadora sigue en el cargo porque la destitución "*for cause*" exige debido proceso. En *Slaughter* (6-3, el mismo día) se revocó *Humphrey's Executor*: el presidente puede remover a comisionados de agencias independientes, salvo la Fed. Implicación: la regulación (FTC, SEC y demás) es política del Ejecutivo, y la Fed está protegida por procedimiento, no por inmunidad. La amenaza a Cook sigue viva (aviso de ago-2026).

**4. Ordena por durabilidad y justifica: arancel 232, arancel IEEPA, depreciación de 100% de la OBBBA, arancel 122.**
OBBBA (ley) > 232 (base estatutaria clara, históricamente sostenida) > 122 (legal pero con caducidad de 150 días) > IEEPA (base dudosa, anulada 6-3).

**5. ¿Cuál es el estado del T-MEC y qué variable arancelaria domina para México?**
El 1-jul-2026 EUA no aceptó extenderlo, así que hay revisiones anuales hasta 2036. Hay rondas bilaterales, con la cuarta tentativa el 28-29 de sep. La 301 impone 10% a México pero exenta lo que entra libre bajo el T-MEC, así que la **tasa de cumplimiento de reglas de origen** es la variable clave. Los pendientes son el 232 de autos (25%) y de acero (50%) y la demanda de 50% de contenido estadounidense.

**6. Da las cifras clave del Paquete Económico 2027 y el calendario de aprobación.**
Se entregó el 8-sep-2026. PIB de 1.5-2.5% (2.0% puntual), RFSP de 3.9% (4.1% en 2026), ingresos tributarios de 15.9% del PIB y sin impuestos nuevos. El costo financiero es 17.2% de los ingresos, el más alto desde 1999, y el apoyo a Pemex cae alrededor de 70%. La Ley de Ingresos se aprueba a más tardar el 20-oct en Diputados y el 31-oct en el Senado, y el Presupuesto de Egresos el 15-nov.

**7. ¿Dónde está Banxico y por qué importa el diferencial con la Fed?**
En 6.50%, con tres pausas desde el recorte del 7-may. La inflación llegaría a la meta en el 4T-2027 y Banxico dice que no seguirá mecánicamente a la Fed. El diferencial contra el techo de la Fed es de 250 pb, el más delgado en años, así que el peso tiene menos colchón de *carry* ante *shocks*.

**8. Moody's pone a México en Baa3 estable, S&P en BBB negativa y Fitch en BBB-. ¿Hay riesgo inminente de salida de índices de grado de inversión?**
No es inminente. Con la regla de calificación intermedia (no verificada en esta sesión), hoy la intermedia es BBB-, y hacen falta dos agencias en especulativo. El riesgo relevante es que S&P baje a BBB-, porque las tres quedarían en el último escalón y cualquier rebaja siguiente sería decisiva. Moody's no espera cambios en 18 meses.

**9. ¿Por qué el caso Elektra es una lección de modelado y no una anécdota?**
Porque muestra que la nueva SCJN y la reforma al amparo (suspensión fiscal sólo con garantía y aplicación a juicios en trámite) convierten contingencias fiscales de probabilidad baja en pasivos ciertos: MXN 48.3 mil millones resueltos y pérdida en el 4T. Todo litigio fiscal material se modela ahora con pago cercano al 100%.

**10. ¿Qué dice la evidencia sobre la deriva pre-FOMC y qué regla se deriva?**
Lucca-Moench encontraron +49 pb en las 24 horas previas (1994-2011), alrededor de 80% del exceso anual. Kurov et al. muestran que desapareció después de 2015. Regla: no se opera (grado D). En el régimen Warsh, con menos guía, conviene reducir tamaño alrededor del anuncio en lugar de apostar a la deriva.

**11. ¿Cómo se demuestra que la experiencia de gobierno del dueño es una ventaja?**
Con pronósticos binarios registrados antes del evento en `bitacora/pronosticos.csv`, cada uno con su tipo y la probabilidad del mercado en `notas`. La ventaja existe si Brier(mercado) − Brier(dueño) es mayor que 0 con N ≥ 50 (≥ 30 por tipo para dimensionar), y además el Brier propio es ≤ 0.20. Nunca con información no pública.

**12. ¿Qué evidencia académica hay de que las conexiones políticas valen, y cómo se usa sin tenerlas?**
Faccio (2006): anunciar una conexión sube el valor. Goldman-Rocholl-So (2009): la elección de 2000 redistribuyó valor por la afiliación del consejo. Acemoglu et al.: Geithner dio +6% el primer día y +12% en 10 días. Se usa como **evento transversal**: cuando cambia el poder o hay un nombramiento, se identifica qué empresas ganan o pierden la renta. También como **riesgo**: la conexión con el gobierno en turno es un pasivo contingente si cambia el gobierno.

**13. Aplica el método de 8 pasos a esta pregunta: "¿Habrá cierre de gobierno en EUA después del 11-dic-2026?"**
(1) Criterio: lapso de fondos más allá de las 00:01 del 12-dic según la OMB. (2) Instrumento: CR u *omnibus*. (3) Calendario: la sesión *lame duck* después del 3-nov. (4) Actores: la mayoría saliente quiere cerrar el año y la entrante, si es demócrata, prefiere negociar en enero; el Senado requiere 60 votos. (5) Señales: la CR anterior pasó 90-6 y 370-48, es decir, con amplio apoyo bipartidista. (6) Precio: mercados de predicción de *shutdown*. (7) Probabilidad registrada. (8) Cadena causal: contratistas, datos económicos retrasados, *bills*.

**14. ¿Qué sectores de México se vuelven más "políticos" con la desaparición de Cofece e IFT y por qué?**
Telecomunicaciones y radiodifusión (CRT), las concentraciones de cualquier sector (Comisión Nacional Antimonopolio, sectorizada a Economía) y energía (CNE desconcentrada de SENER). Los reguladores ya no son independientes del Ejecutivo, así que los resultados deben pronosticarse con los incentivos del gobierno y no con la jurisprudencia técnica previa.

**15. Ocurre un anuncio arancelario sorpresa por *post* un viernes por la noche. ¿Qué haces el lunes?**
Aplico T+0: identifico el instrumento. Si es sólo un *post* sin orden publicada, es de baja durabilidad y no vendo en pánico. Mido la reacción contra la probabilidad previa, mapeo ganadores y perdedores y veo si hay exención T-MEC. En T+1 busco la vía legal (232, 301 o 122) y su plazo, y registro "¿vigente en 90 días?" en el *ledger*. Todo dentro de los límites de pérdida del periodo.

---

## 9. Fuentes

**Fed y política monetaria**
- Comunicado FOMC 16-sep-2026: https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm
- Calendario FOMC: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
- CNBC, decisión de sep-2026: https://www.cnbc.com/2026/09/16/fed-rate-decision-september-2026.html
- TheStreet, *dot plot*: https://www.thestreet.com/fed/fed-rate-hike-warsh-dot-plot-inflation
- TradingKey, *dot plot*: https://www.tradingkey.com/analysis/stocks/us-stocks/262172696-fed-rate-hike-october-dot-plot-median-one-more-2026-tradingkey
- Bondsavvy, *dot plot*: https://www.bondsavvy.com/fixed-income-investments-blog/fed-dot-plot
- CNBC, Trump y Warsh: https://www.cnbc.com/2026/09/16/trump-fed-interest-rate-warsh.html
- CNN, confirmación de Warsh: https://www.cnn.com/2026/05/13/economy/kevin-warsh-confirmation-trump-fed-chair
- Al Jazeera, juramento: https://www.aljazeera.com/economy/2026/5/22/kevin-warsh-sworn-in-as-new-us-fed-chair
- Spectrum, voto 54-45 y Powell: https://spectrumlocalnews.com/us/snplus/politics/2026/05/22/kevin-warsh-sworn-in-jerome-powell-trump-white-house-ceremony-clarence-thomas
- *Trump v. Cook* (opinión): https://www.supremecourt.gov/opinions/25pdf/25a312_5468.pdf
- SCOTUSblog, aviso a Cook (ago-2026): https://www.scotusblog.com/2026/08/trump-informs-lisa-cook-that-he-is-considering-her-removal/
- SCOTUSblog, *Slaughter*: https://www.scotusblog.com/2026/06/court-allows-trump-to-fire-ftc-commissioner-and-overturns-major-restraint-on-presidential-power/
- CRS sobre *Slaughter*: https://www.congress.gov/crs-product/LSB11448

**Tesoro, Congreso y aranceles**
- *Refunding* del 5-ago-2026: https://home.treasury.gov/news/press-releases/sb0590
- BPC, techo de deuda: https://bipartisanpolicy.org/article/when-will-we-reach-the-debt-limit-again/
- CRFB, OBBBA: https://www.crfb.org/blogs/whats-one-big-beautiful-bill-act
- BPC, costo de la OBBBA: https://bipartisanpolicy.org/explainer/what-does-the-one-big-beautiful-bill-cost/
- Sidley, OBBBA y energía: https://www.sidley.com/en/insights/newsupdates/2025/07/the-one-big-beautiful-bill-act-navigating-the-new-energy-landscape
- FedTools, CR del año fiscal 2027: https://www.fedtools.com/blog/government-shutdown-october-2026
- CNBC, mercados de predicción y Senado: https://www.cnbc.com/2026/09/16/prediction-markets-say-democrats-are-slightly-favored-to-win-senate.html
- DWT, CLARITY Act: https://www.dwt.com/blogs/financial-services-law-advisor/2026/09/clarity-act-crypto-market-structure-bill-stalled
- CNBC, cripto en septiembre: https://www.cnbc.com/2026/09/01/crypto-enters-september-with-policy-gamble-hanging-by-a-thread.html
- Holland & Knight, reembolsos IEEPA: https://www.hklaw.com/en/insights/publications/2026/06/ieepa-tariff-refund-update-government-appeals
- Skadden, CAPE: https://www.skadden.com/insights/publications/2026/03/tariff-refund-mechanism-takes-shape
- Global Trade Alert, 301: https://globaltradealert.org/blog/forced-labour-section-301-final-action
- Holland & Knight, México y 301: https://www.hklaw.com/en/insights/publications/2026/07/mexico-mantiene-acceso-preferencial-bajo-el-tmec
- BBVA Research, 301 y México: https://www.bbvaresearch.com/en/publicaciones/mexico-favorable-position-on-new-us-tariffs-under-section-301-for-forced-labor/
- CRS, 232 autos: https://www.congress.gov/crs-product/IN12545
- Crowell, 232 fármacos: https://www.crowell.com/en/insights/client-alerts/trump-administration-imposes-section-232-tariffs-on-patented-pharmaceutical-imports-tiered-rate-structure-takes-effect-beginning-july-31-2026
- Duane Morris, acuerdos MFN: https://www.duanemorris.com/alerts/most_favored_nation_drug_pricing_agreements_expanded_nine_additional_pharmaceutical_0926.html

**Antimonopolio, SEC, CFTC, FDA y política industrial**
- CNBC, remedios de Google: https://www.cnbc.com/2026/09/02/google-defeats-us-bid-to-force-ad-tech-sale.html
- CNN, acuerdo de Paramount con los estados: https://www.cnn.com/2026/09/21/media/paramount-wbd-settlement-cnn-ellison-bonta-lawsuit
- Deadline, moción contra el acuerdo: https://deadline.com/2026/09/paramount-merger-delayed-settlement-challenge-1237112480/
- SEC, informe semestral: https://www.sec.gov/newsroom/press-releases/2026-42-sec-proposes-amendments-permit-optional-semiannual-reporting-public-companies
- Federal Register, CFTC y mercados de predicción: https://www.federalregister.gov/documents/2026/06/12/2026-11854/prediction-markets-public-interest-determinations
- FDA, CNPV: https://www.fda.gov/news-events/press-announcements/fda-grants-seventh-approval-under-national-priority-voucher-pilot-program
- BioSpace, Pazdur: https://www.biospace.com/fda/pazdur-questions-legality-safety-of-fdas-expedited-drug-approvals-programs
- Intel, acuerdo con el gobierno: https://www.intc.com/news-events/press-releases/detail/1748/intel-and-trump-administration-reach-historic-agreement-to
- CSIS, participaciones federales: https://www.csis.org/analysis/understanding-federal-equity-investments-strategic-companies
- Fortune, USA Rare Earth: https://fortune.com/2026/01/26/trump-admin-buys-stake-usa-rare-earth-wave-deals-critical-minerals/

**México**
- SHCP, comunicado 71 (Paquete 2027): https://www.gob.mx/shcp/prensa/comunicado-no-71-la-secretaria-de-hacienda-y-credito-publico-entrega-el-paquete-economico-2027-al-h-congreso-de-la-union
- Expansión, Paquete 2027: https://expansion.mx/economia/2026/09/08/entrega-paquete-economico-2027-mensaje-secretario-hacienda
- Investing, Paquete 2027: https://mx.investing.com/news/economy-news/hacienda-recorta-pib-a-2-en-paquete-economico-2027-y-busca-deficit-de-35-3759177
- adn40, Paquete 2027: https://www.adn40.mx/finanzas/2026-09-08/paquete-economico-2027-hacienda-recorta-crecimiento-de-mexico-y-revela-que-pasara-con-los-impuestos/
- Banxico, anuncios de política monetaria: https://www.banxico.org.mx/publicaciones-y-prensa/anuncios-de-las-decisiones-de-politica-monetaria/anuncios-politica-monetaria-t.html
- Banxico, calendario 2026: https://www.banxico.org.mx/monetary-policy/d/%7B0C35369C-BF8F-E5A8-7710-FD5A6716474F%7D.pdf
- Expansión, Banxico 24-sep-2026: https://expansion.mx/economia/2026/09/24/banxico-tasa-de-interes-de-referencia-6-5-septiembre
- Proceso, Banxico y la Fed: https://www.proceso.com.mx/economia/2026/9/24/banxico-se-desmarca-de-la-fed-congela-la-tasa-e-insiste-en-que-mexico-no-tiene-que-seguir-a-eu-380590.html
- USTR, revisión del T-MEC: https://ustr.gov/about/policy-offices/press-office/press-releases/2026/july/ambassador-greer-issues-statement-usmca-joint-review
- White & Case, T-MEC: https://www.whitecase.com/insight-alert/usmca-2026-joint-review-united-states-declines-extend-agreement-triggering-annual
- El Heraldo, rondas del T-MEC: https://heraldodemexico.com.mx/nacional/2026/9/23/cuando-es-la-negociacion-del-t-mec-que-se-discute-fechas-893607.html
- TLC Magazine, cuarta ronda: https://tlcmagazinemexico.com/secciones/people-of-trade/la-cuarta-ronda-que-llego-sin-texto-firmado-y-con-un-reloj-que-ya-rebaso-su-propia-fecha/index.html
- Bloomberg Línea, Moody's y Fitch: https://www.bloomberglinea.com/latinoamerica/mexico/mexico-queda-en-el-ultimo-escalon-de-grado-de-inversion-con-moodys-y-fitch/
- El Financiero, Moody's: https://www.elfinanciero.com.mx/economia/2026/05/21/moodys-baja-nota-crediticia-a-mexico-por-debilidad-fiscal/
- La Jornada, Pemex B1: https://www.jornada.com.mx/noticia/2026/05/22/economia/moodys-ratifica-calificacion-de-pemex-con-perspectiva-estable
- Expansión, apoyos a Pemex: https://expansion.mx/empresas/2026/09/24/pemex-llegara-apoyos-gobierno-pese-meta-autosuficiencia
- CIEP, Pemex: https://ciep.mx/pemex-y-su-plan-estrategico-rumbo-al-paquete-economico-2026/
- El Financiero, reforma electoral rechazada: https://www.elfinanciero.com.mx/nacional/2026/03/11/reforma-electoral-va-rumbo-a-la-guillotina-sin-apoyo-del-verde-y-pt-sigue-la-sesion-en-vivo/
- La Jornada, elección judicial en 2028: https://www.jornada.com.mx/noticia/2026/05/29/politica/avala-senado-la-reforma-que-pospone-de-2027-a-2028-la-eleccion-judicial
- Bloomberg Línea, SCJN y Elektra: https://www.bloomberglinea.com/latinoamerica/mexico/nueva-suprema-corte-resuelve-que-elektra-de-salinas-pliego-debe-pagar-al-sat/
- La Silla Rota, pago de Elektra: https://lasillarota.com/negocios/2026/5/25/grupo-elektra-liquida-primera-parte-de-deuda-fiscal-por-32-mil-mdp-ante-sat-588858-amp.html
- DLA Piper, reforma al amparo: https://www.dlapiper.com/es-mx/insights/publications/2025/10/mexico-reforms-the-amparo-law
- LatinUS, extinción de Cofece: https://latinus.us/mexico/2025/7/1/diputados-extinguen-la-cofece-avalan-la-creacion-de-la-comision-nacional-antimonopolio-145754.html
- Diputados, leyes secundarias de energía en el DOF: https://comunicacionsocial.diputados.gob.mx/index.php/notilegis/publica-dof-leyes-secundarias-de-la-reforma-constitucional-en-materia-energetica
- Aranceles a Asia (DOF): https://www.diariodemexico.com/mi-nacion/publican-en-el-dof-decreto-sobre-aranceles-productos-asiaticos
- Polos de Bienestar: https://es-us.noticias.yahoo.com/polos-bienestar-atraer%C3%ADan-17-491-150000390.html
- Mayer Brown, FinCEN y CIBanco: https://www.mayerbrown.com/en/insights/publications/2025/09/ongoing-developments-related-to-fincens-cibanco-order
- El Financiero, Trump frena ataques: https://www.elfinanciero.com.mx/nacional/2026/09/23/trump-freno-ataques-aereos-contra-mexico-por-endurecimiento-contra-carteles-de-sheinbaum-segun-nyt/
- El Financiero, peso tras la elección de 2024: https://www.elfinanciero.com.mx/economia/2024/06/07/por-que-el-peso-y-los-mercados-enloquecieron-despues-de-las-elecciones-2024/
- CNN/EFE, peso en 2024: https://cnnespanol.cnn.com/2025/01/01/mexico/fin-superpeso-moneda-mexicana-se-deprecia-efe

**Literatura académica**: los enlaces están en la tabla de la sección 3.

---

### Registro de verificación (25-sep-2026)

- **Corrección:** Chen-Parsley-Yang (2015) se publicó en el *Journal of Business Finance & Accounting*, no en el JFQA.
- **Corrección:** Expansión dice que la pausa de Banxico del 24-sep fue la "cuarta" consecutiva. El listado oficial muestra la **tercera** (jun, ago, sep), después de los recortes de marzo y mayo.
- **Discrepancia:** el tipo de cambio del Paquete 2027 aparece como 17.9 (adn40) y como 18.0 (Investing). El comunicado de la SHCP no lo trae, así que queda pendiente de revisar en los Criterios Generales.
- **Discrepancia:** una fuente fecha la aprobación de la Comisión Nacional Antimonopolio en Diputados el 31-mar-2026. La prensa de 2025 la ubica en jul-2025, que es la fecha que se adopta aquí.
- **Calendario de Banxico:** una fuente secundaria listaba el "19-nov" como decisión. En el calendario oficial esa fecha es de minuta; las decisiones son el 5-nov y el 17-dic.
- **Sin verificar en esta sesión:** la regla de calificación intermedia del Bloomberg Agg; el balance primario y la SHRFSP del Paquete en fuente primaria; la magnitud de los retornos en Cooper-Gulen-Ovtchinnikov.
