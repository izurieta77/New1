# 24 — Política pública, regulación y mercados (EUA y México)

> Nivel: experto · Actualizado 2026-09-25 · Grado global: **B**. Está medido con rigor cómo reaccionan los precios a las sorpresas de política y cuánto valen las conexiones políticas. Las reglas de *trading* derivadas, como la deriva pre-FOMC, el ciclo presidencial o copiar al Congreso, son **C o D**. La ventaja operable está en anticipar el **instrumento**, el **plazo** y la **sorpresa contra lo que ya está en el precio**.

Capítulos relacionados, que aquí no se repiten: [04 Renta fija y macro](04-maestria-renta-fija-tasas-macro.md) · [11 México](11-mexico-mercado-instrumentos-fiscalidad.md) · [Estado del mercado: tablero más reciente](../bitacora/briefs/) · [15 Eventos corporativos](15-eventos-corporativos-y-situaciones-especiales.md) · [16 Macro, FX y peso](16-macro-global-divisas-y-el-peso.md) · [17 Crisis](17-crisis-burbujas-libro-de-patrones.md) · [22 Fuentes de datos con IA](22-fuentes-de-datos-y-flujo-de-investigacion-con-ia.md) · [23 Geopolítica](23-geopolitica-y-riesgo-politico-global.md). Los parámetros de riesgo están en `config/parametros.json`. Los pronósticos se registran en `bitacora/pronosticos.csv` con `herramientas/pronosticos.py`.

**Convenciones.** Hecho = lleva fecha y fuente. "**Inferencia:**" = razonamiento propio. "**Regla:**" = recomendación operable. "(no verificado)" = no se confirmó en esta sesión. Grados de evidencia: A = replicado y robusto fuera de muestra y neto de costos. D = débil o marketing.

---

## 1. Objetivos de dominio

1. Leer la **función de reacción** de la Fed y de Banxico (comunicado, SEP y *dot plot*, minutas, discursos, conferencia) y convertirla en probabilidades por reunión, para contrastarlas con futuros de fondos federales, OIS y swaps de TIIE.
2. Medir cada decisión como **sorpresa**: lo que se decidió menos lo que el precio ya descontaba.
3. Clasificar toda medida por la **durabilidad de su instrumento** y su riesgo judicial. En 2025-2026 este fue el mejor predictor de supervivencia de una medida.
4. Conocer el estado vigente de la política en EUA y México al 25-sep-2026.
5. Anticipar la política con un método explícito: incentivos, jugadores con veto, calendario legal, señales costosas, mercados de predicción y el mapa de quién gana y quién pierde.
6. Convertir la experiencia de gobierno del dueño en **ventaja medible** en el *ledger*, calificada contra el mercado y sin tocar información privilegiada.
7. Aplicar un **checklist de riesgo regulatorio** por empresa que produzca un descuento de valoración o un límite de posición coherente con `parametros.json`.

---

## 2. Marco teórico

### 2.1 Cuatro canales de transmisión

| Canal | Mecanismo | Ejemplo 2025-2026 | Persistencia |
|---|---|---|---|
| **Tasa de descuento** | Tasa corta esperada, prima por plazo, prima accionaria | La Fed sube 25 pb el 16-sep-2026 | Alta mientras no cambie la función de reacción |
| **Flujos de caja** | Impuestos, aranceles, subsidios, precios regulados, compras públicas | OBBBA: depreciación de 100% permanente. Sección 232 a fármacos | Depende del instrumento (2.4) |
| **Estructura de mercado** | Fusiones, concesiones, reguladores | Paramount-WBD; remedios contra Google; en México, CRT y Comisión Antimonopolio | Alta: cambia márgenes de largo plazo |
| **Derechos de propiedad y *enforcement*** | Tribunales, amparo, sanciones, cobro fiscal | SCJN contra Elektra; FinCEN contra CIBanco, Intercam y Vector | Puede ser pérdida permanente |

### 2.2 El precio reacciona a la sorpresa

Bernanke-Kuttner (2005) separan con futuros de fondos federales la parte anticipada de cada decisión de la no anticipada. Un recorte sorpresa de 25 pb se asocia con alrededor de **+1%** en los índices amplios. La parte anticipada casi no mueve precios y el grueso del efecto pasa por la prima de riesgo esperada. Gürkaynak-Sack-Swanson (2005) separan dos factores: *target* (la tasa de hoy) y *path* (la guía). El *path* domina los plazos largos. Nakamura-Steinsson (2018) proponen el *information effect*: un alza se lee como "la Fed ve fuerte la economía". Bauer-Swanson (2023) lo reinterpretan como la respuesta de la Fed a noticias públicas.

**Regla:** toda decisión se registra como el par (decisión, expectativa previa medida en precio).

### 2.3 Función de reacción: qué leer

- **Comunicado:** comparar palabra por palabra contra el anterior.
- ***Dot plot*:** mide el sesgo del comité, no pronostica niveles. En dic-2021 la mediana para fin de 2022 era **0.9%** y la tasa cerró 2022 en **4.25-4.50%**.
- **Minutas:** el balance de riesgos y el conteo de posturas.
- **Discursos:** pesan más presidente, vicepresidente y NY Fed. Durante el *blackout* no hay señales.
- **Conferencia:** qué variable domina la función de reacción.

**Inferencia (régimen Warsh):** Warsh **no entregó punto** en septiembre de 2026 y dice que "*independence is a two-way street... we stay in our lane*" (cita no verificada en esta sesión). Eso apunta a menos guía futura, más peso del comunicado y la conferencia y, por lo tanto, más sorpresa y volatilidad el día del anuncio.

### 2.4 Durabilidad del instrumento: el concepto operable central

| Instrumento | Quién lo revierte | Vida media 2025-2026 (Inferencia) | Ejemplo |
|---|---|---|---|
| Constitución (MX) | Mayoría calificada y congresos locales | Años | Reforma judicial, extinción de autónomos |
| Ley | Congreso, tribunales | Años | OBBBA, GENIUS Act, leyes de energía MX |
| Acción administrativa con base estatutaria clara | Tribunales, la propia agencia | Meses a años | 232 (acero 50%, autos 25%, fármacos 100%), 301 |
| Acción con base dudosa | Tribunales | Meses | IEEPA, anulado 6-3 el 20-feb-2026 |
| Instrumento con plazo legal | El calendario | Fecha fija | Sección 122, expiró a los 150 días (24-jul-2026) |
| Estatuto antiguo casi sin uso | Negociación, tribunales | Semanas a meses; puede escalar | Sección 338 contra Canadá: aranceles del 22-ago y veto a importaciones desde el 29-sep-2026 |
| Declaración, *post*, mañanera | Nadie: no obliga | Horas a semanas | Amenazas arancelarias pospuestas |

**Regla:** antes de reaccionar se anotan el instrumento, la vía de impugnación y la fecha de caducidad. Si el instrumento está en la mitad baja de la tabla, la posición se dimensiona para una reversión.

### 2.5 Economía política

- **Concentrados contra difusos** (Olson; Stigler; Grossman-Helpman 1994, *Protection for Sale*). Gana quien concentra beneficios y reparte costos. **Inferencia:** a largo plazo la política comercial favorece a sectores organizados con empleo concentrado geográficamente (acero, autos, agro de estados clave).
- **Jugadores con veto** (Tsebelis). En México la mayoría calificada depende de PT y PVEM. El 11-mar-2026 votaron **contra** la reforma electoral: 259 a favor, 234 en contra, cuando se necesitaban 334. La coalición no es un bloque.
- **Ciclo electoral.** Antes de una elección se evitan costos visibles y después se abre una ventana para medidas impopulares. Intermedias de EUA: **3-nov-2026**. Intermedias de México: **6-jun-2027**, primer domingo de junio según la LGIPE; Proceso Electoral Federal 2026-2027 con 500 diputaciones y 17 gubernaturas (Wikipedia; calendario del INE no consultado).
- **Pastor-Veronesi (2012, 2020).** Los cambios de política bajan precios en promedio, más cuando la economía es débil (cap. 23). La prima demócrata se explica por la aversión al riesgo del electorado.

### 2.6 Conexiones: renta y pasivo contingente

Las conexiones valen porque dan acceso a contratos, rescates y regulación favorable (Faccio 2006; Faccio-Masulis-McConnell 2006; Goldman-Rocholl-So 2009 y 2013). Cuando cambia el poder, la renta se invierte (caso Elektra, 4.9). Para el inversionista externo la conexión no es una estrategia: es un **factor de riesgo** que se mide.

---

## 3. Literatura canónica

| Estudio | Hallazgo cuantificado | Enlace | Grado |
|---|---|---|---|
| Bernanke-Kuttner (2005, JF) | Recorte sorpresa de 25 pb: alrededor de **+1%** en índices. La parte anticipada casi no mueve precios | https://www.nber.org/papers/w10402 | **A** |
| Gürkaynak-Sack-Swanson (2005, IJCB) | Factores *target* y *path*. El *path* domina los plazos largos | https://www.federalreserve.gov/pubs/feds/2004/200466/200466pap.pdf | **A** |
| Nakamura-Steinsson (2018, QJE) | *Information effect* de la Fed (en debate con Bauer-Swanson 2023) | https://www.nber.org/papers/w19260 | **B** |
| Lucca-Moench (2015, JF) | +**49 pb** en las 24 h previas al FOMC (sep-1994 a mar-2011), alrededor de **80%** del exceso anual | https://www.newyorkfed.org/research/staff_reports/sr512.html | B en muestra, **D** hoy |
| Kurov-Wolfe-Gilbert (2021, FRL; en línea 2020) | La deriva **desapareció después de 2015**, con y sin conferencia (muestra hasta dic-2019) | https://pmc.ncbi.nlm.nih.gov/articles/PMC7525326/ | **B** |
| Cieslak-Morse-Vissing-Jorgensen (2019, JF) | Desde 1994 la prima accionaria se gana en las semanas **0, 2, 4 y 6** del ciclo FOMC, por comunicación informal de la Fed | https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12818 | B / **C** como estrategia |
| Santa-Clara-Valkanov (2003, JF) | Exceso de retorno con presidentes demócratas: **+9 pp** ponderado por valor y **+16 pp** equiponderado | https://ideas.repec.org/a/bla/jfinan/v58y2003i5p1841-1872.html | B como hecho, **D** para operar (N≈20) |
| Pastor-Veronesi (2020, JPE) | Explica la prima demócrata por aversión al riesgo variable | https://www.nber.org/papers/w23184 | B |
| Snowberg-Wolfers-Zitzewitz (2007, QJE) | Un triunfo republicano sube las acciones **2-3%** (mercados de predicción el día de la elección) | https://www.nber.org/papers/w12073 | **A-** |
| Wagner-Zeckhauser-Ziegler (2018, JFE) | En 2016 ganan las empresas domésticas y con impuestos altos. Lo **fácil de evaluar se incorporó más rápido** que lo complejo | https://www.nber.org/papers/w23152 | **B** |
| Faccio (2006, AER) | En 47 países las conexiones abundan donde hay más corrupción. **Anunciar una conexión sube el valor** | https://www.aeaweb.org/articles?id=10.1257%2F000282806776157704 | **A** |
| Faccio-Masulis-McConnell (2006, JF) | Las conectadas tienen más probabilidad de ser rescatadas | https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2006.01000.x | B |
| Goldman-Rocholl-So (2009, RFS) | Nombrar un consejero conectado da retorno anormal positivo. En 2000 subieron las ligadas a republicanos y cayeron las ligadas a demócratas | https://academic.oup.com/rfs/article-abstract/22/6/2331/1592075 | **B** |
| Goldman-Rocholl-So (2013, RoF) | Los consejos conectados con el partido ganador reciben más contratos | https://academic.oup.com/rof/article-abstract/17/5/1617/1582382 | B |
| Acemoglu et al. (2016, JFE) | Nominación de Geithner: las financieras conectadas ganan **~6%** el primer día y **~12%** en 10 días | https://www.nber.org/papers/w19701 | **B** |
| Cohen-Coval-Malloy (2011, JPE) | Cuando llega un presidente de comité poderoso, las empresas de su estado **recortan** inversión y empleo | https://www.nber.org/papers/w15839 | B |
| Cooper-Gulen-Ovtchinnikov (2010, JF 65(2)) | Con donaciones 1979-2004, las medidas de contribución se correlacionan positivamente con retornos futuros. El efecto es mayor con muchos candidatos del estado sede, de la Cámara y demócratas. El resumen no da magnitud (no verificado) | https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2009.01548.x | **C** |
| Chen-Parsley-Yang (2015, **J. Business Finance & Accounting**, no JFQA) | Los portafolios con más *lobbying* superan su *benchmark* durante 3 años | https://onlinelibrary.wiley.com/doi/10.1111/jbfa.12109 | **C** |
| Eggers-Hainmueller (2013, JOP) | El Congreso promedio quedó **2-3% anual por debajo** del mercado (2004-2008) (resumen no consultado en esta sesión) | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1762019 | **B** |
| Belmont-Sacerdote et al. (2022, JPubE) | Sin desempeño superior entre 2012 y 2020. Lo que compra la Cámara rinde **−26 pb** a 6 meses | https://www.nber.org/papers/w26975 | B. Copiar al Congreso: **D** |
| Wolfers-Zitzewitz (2004, JEP) | Los mercados de predicción agregan bien la información, con sesgo *favorite-longshot* | https://www.aeaweb.org/articles?id=10.1257/0895330041371321 | B |

**Lectura del panel.** (1) La sorpresa se mide y mueve precios de forma predecible (A). (2) La política redistribuye valor **entre empresas** más que mover el índice (B). (3) Las anomalías de calendario político se degradaron o nunca fueron operables (D).

---

## 4. Lo más reciente (estado al 25-sep-2026)

### 4.1 Fed: Warsh, primera alza desde 2023, independencia en tribunales

- **Liderazgo.** El Senado confirmó a Warsh como presidente el 13-may-2026 por **54-45**, la votación más dividida para ese cargo. Juró el **22-may** ante el juez Clarence Thomas. Powell sigue como **gobernador** (periodo hasta 2028) mientras dure la investigación del DOJ sobre la remodelación de la sede (Wikipedia, Spectrum).
- **16-sep-2026.** Alza de 25 pb a **3.75-4.00%**, votación 12-0 sin disensos. Es la primera alza desde jul-2023. El comunicado dice "*inflation remains elevated*" y busca "*a timelier return*" a 2% (Fed). En el *dot plot*, Warsh no entregó punto (lo dijo él mismo, según Wikipedia). El SEP lo firman **18** participantes. Para fin de 2026, 12 ven una alza más (4.125%), 4 ven dos (4.375%) y 2 ninguna. La mediana de 2026 sube de 3.8% a **4.1%**, la de 2027 de 3.6% a **4.1%**, la de 2028 queda en 3.9% y la de largo plazo en 3.2% (SEP de la Fed; TradingKey).
- **Presión.** Según CNBC, Trump dijo que le recomendó a Warsh "*you might as well vote with the board because it's not going to matter*" y llamó al Consejo "*very hostile, very political*" (no verificado: CNBC bloqueó el acceso en esta sesión). **Inferencia:** una segunda alza (28-oct o 9-dic) pone a prueba la relación en plena ventana electoral.
- ***Trump v. Cook* (29-jun-2026).** Por 5-4 (Roberts, con Sotomayor, Kagan, Kavanaugh y Jackson; disienten Thomas, Alito, Gorsuch y Barrett) la Corte negó suspender la medida que impide destituir a Lisa Cook. Una remoción "*for cause*" exige aviso y oportunidad de responder. El 7-ago-2026 Trump le notificó que "considera" destituirla por presunto fraude hipotecario y le dio 21 días para responder (SCOTUSblog). La independencia depende del procedimiento, no es inmunidad.
- ***Trump v. Slaughter* (29-jun-2026).** Por 6-3 (Roberts; disienten Sotomayor, Kagan y Jackson) se revoca *Humphrey's Executor*. El presidente puede remover a voluntad a comisionados de agencias independientes (FTC y análogas). **La Corte no resolvió el caso de la Fed**: dejó abierta la cuestión y citó la "*distinct historical tradition*" de los Bancos Primero y Segundo (SCOTUSblog). **Inferencia:** regulación y antimonopolio pasan a ser política del Ejecutivo y sube el riesgo de cambio con cada administración.
- **Calendario:** 27-28 oct y 8-9 dic (con SEP). En 2027: 26-27 ene, 16-17 mar\*, 27-28 abr, 8-9 jun\*, 27-28 jul, 14-15 sep\*, 26-27 oct, 7-8 dic\*. (\* = con SEP.)

### 4.2 Tesoro y techo de deuda

- ***Refunding* del 5-ago-2026:** US$125 mil millones en tres emisiones: 58 a 3 años, 42 a 10 años y 25 a 30 años. Levanta US$28.7 mil millones de efectivo nuevo. Los cupones se mantienen "*for at least the next several quarters*", con recompras de hasta US$38 mil millones. Supuesto de **TGA: US$950 mil millones a fin de septiembre y ~US$1.05 billones a fines de octubre.** Próximo anuncio: **4-nov-2026**, un día después de las intermedias (Tesoro).
- **Regla:** en cada *refunding* se revisan tres cosas: la frase "*several quarters*", la TGA proyectada y la mezcla entre *bills* y cupones. Un alza sorpresa en cupones equivale a un *shock* de *duration*, y una TGA al alza drena reservas.
- **Techo de deuda.** La OBBBA lo subió **US$5 billones, a US$41.1 billones**. Según el BPC se alcanzaría entre finales del invierno y mediados del verano de 2027. Con 6 a 9 meses de medidas extraordinarias, el *X-date* caería entre finales de 2027 y principios de 2028.

### 4.3 Congreso

- **OBBBA (4-jul-2025).** La CBO estima **+US$3.4 billones** de déficit a 10 años, o +4.1 con intereses. La depreciación de 100% queda permanente para bienes adquiridos después del 19-ene-2025. Pierden los créditos 45Y/48E los proyectos eólicos y solares que **inicien construcción desde el 4-jul-2026** y entren en servicio después de 2027. Se eliminan los créditos a vehículos eléctricos (Sidley, CRFB). **Inferencia:** se adelantan obras a 2025-2026 y se crea un precipicio de demanda para renovables de EUA en 2028.
- **Año fiscal 2027.** Hay una resolución continua (CR) **hasta el 11-dic-2026**: Senado 90-6 el 8-ago, Cámara 370-48 el 1-sep, firma el 2-sep (FedTools). El siguiente precipicio cae en la sesión *lame duck*.
- **Cripto.** La GENIUS Act es ley desde jul-2025. La CLARITY Act **no llegó al pleno del Senado**: las negociaciones se estancaron el 13-sep-2026 y la Casa Blanca aceptó cláusulas de ética el 14-sep. Según Lummis, no habrá ley de estructura de mercado "*probably until at least 2030*" (DWT, 21-sep). La votación de cloture 49-50 del 15-sep que aparecía en una versión previa **no se confirmó** (no verificado).
- **Intermedias.** Probabilidad de Senado demócrata según CNBC (16-sep): **55%** en Kalshi y **59%** en Polymarket. El escenario más probable en Kalshi era control demócrata de ambas cámaras (46%), seguido de Senado republicano con Cámara demócrata (38%). No se verificó directamente porque CNBC y Kalshi bloquearon el acceso. **Consulta directa a Polymarket el 25-sep-2026: 63% demócrata y 38% republicano** (volumen de US$5.25 millones).

### 4.4 Aranceles

- **IEEPA:** anulada 6-3 el 20-feb-2026 (*Learning Resources v. Trump*). La recaudación sujeta a reembolso es de ~US$166 mil millones de más de 330 mil importadores (Skadden). CAPE arrancó el 20-abr. Al 9-jun había ~US$23 mil millones aprobados y más de US$95 mil millones en cola (Holland & Knight), y hacia julio ~US$81 mil millones distribuidos (Wikipedia). El 3-jun el DOJ apeló las órdenes de reembolso universal ante el Circuito Federal. La cifra de US$128.68 mil millones "aceptados" que aparecía antes **no se confirmó** (no verificado). **Inferencia:** los reembolsos son ganancias extraordinarias en los 10-Q de 2026 de importadores y minoristas y deben excluirse de la utilidad normalizada.
- **Sección 122:** 10% global, anunciada el 20-feb y vigente del **24-feb** al 24-jul-2026 (150 días). Se anunció un alza a 15%, pero no se verificó que se aplicara (cap. 23).
- **Sección 338 (Tariff Act de 1930) contra Canadá:** es un instrumento casi inédito. Las Proclamaciones 11046-11048 (20-jul-2026) impusieron hasta **50%** a lácteos, bebidas alcohólicas y vehículos de Canadá. Se suspendieron tres días (Proclamación 11056, 18-ago) y entraron en vigor el **22-ago**, después de que, según el texto, Canadá "*reneged*". La Proclamación 11063 (8-sep) **prohíbe la importación** de ciertos productos canadienses desde el **29-sep-2026** (Federal Register). **Inferencia:** México compite con Canadá en autos. Una escalada de este tipo reasigna producción norteamericana y muestra que EUA está dispuesto a usar instrumentos estatutarios poco probados contra un socio del T-MEC.
- **Sección 301 "*forced labor*" (desde el 24-jul-2026):** 10-12.5% a 60 economías. **México 10%, con exención para lo que entra libre bajo el T-MEC** y para bienes con 232 (Global Trade Alert, BBVA Research). **Inferencia:** para México, la variable arancelaria clave es la tasa de cumplimiento de reglas de origen.
- **Sección 232:** autos 25% (si cumplen el T-MEC, sólo sobre el contenido no estadounidense). Camiones 25% y autobuses 10% desde el 1-nov-2025 (no verificado: CRS bloqueó el acceso). Acero y aluminio 50%. **Fármacos patentados: 100%** según la Proclamación 11020 (2-abr-2026), desde el 31-jul-2026 para las empresas del Anexo III y desde el **29-sep-2026** para las demás. Hay tasas reducidas: 15% para la UE, Japón, Corea y Suiza; 10% para el Reino Unido (bajada a 0% en ago-2026); 20% con plan de relocalización aprobado (sube a 100% el 2-abr-2030); y **0% hasta el 20-ene-2029** para empresas con acuerdo de precios MFN (Federal Register). No se confirmó una fecha de corte "antes del 2-abr" para los acuerdos (no verificado). Al **31-ago** había acuerdos MFN con **26 empresas, ~89% del mercado de marca** (Duane Morris).

### 4.5 Antimonopolio, SEC, CFTC, FDA

- **Google (2-sep-2026):** la jueza Brinkema **rechazó** la venta de AdX y DFP y ordenó sólo remedios de conducta (Wikipedia; CNBC). Es el segundo caso de Google sin ruptura estructural.
- **Paramount-WBD:** el plazo HSR se cumplió sin demanda del DOJ (Paramount lo anunció el 20-feb). California y otros 11 estados demandaron el 13-jul y obtuvieron una orden temporal de dos semanas el 20-jul (jueza Martínez-Olguín). **Acuerdo del 21-sep** con California y el WGA: 30 películas al año por dos años y luego 32, un consejo editorial para CBS News y CNN y US$1.5 mil millones de producción en EUA. No se confirmó la adhesión de los otros 11 estados. El 24-sep la corte admitió *amicus* de *Block the Merger* contra el acuerdo. Ellison espera cerrar hacia el 5-oct; al 25-sep **no había cerrado** (Wikipedia). **Inferencia:** el antimonopolio federal se volvió negociable y los estados son el jugador con veto.
- **SEC:** el 5-may-2026 propuso un **informe semestral opcional** (Formulario 10-S en lugar de los 10-Q). **Regla:** en una empresa que lo adopte, sube el descuento por incertidumbre informativa.
- **CFTC:** propuesta de regla publicada el **12-jun-2026** en el Federal Register (comentarios hasta el 27-jul). **No prohíbe por categoría**: enumera terrorismo, asesinato, guerra y *gaming* como actividades que la Comisión "*may determine*" contrarias al interés público. Dice que los contratos deportivos con utilidad comercial "*are not contrary to the public interest*" y presume contrarios los juegos de azar puro. El litigio con estados y las acciones contra *insider trading* (abr-2026) no se verificaron.
- **FDA:** el Commissioner's National Priority Voucher (CNPV) busca revisiones de **1-2 meses** en vez de 10-12 (BioSpace). Su séptima aprobación fue Bizengri, el 8-may-2026 (FDA). La FDA habla de un "*CNPV review council*". Que lo encabece Prasad no está verificado. Pazdur cuestionó la seguridad y la legalidad de los programas acelerados (BioSpace, nov-2025). **Inferencia:** la aprobación regulatoria ya incorpora criterios de relocalización y precio.

### 4.6 Política industrial: el Estado accionista

El gobierno compró **433.3 millones de acciones de Intel a US$20.47 (9.9%, US$8.9 mil millones)**, pagadas con US$5.7 mil millones de subvenciones CHIPS pendientes y US$3.2 mil millones del programa Secure Enclave (Intel, ago-2025). **El DoD tiene 15% de MP Materials** (CSIS). El 26-ene-2026 el gobierno anunció US$1.6 mil millones para USA Rare Earth, con una participación de 8% a 16% según los *warrants* (Fortune). Según una encuesta de CNBC (jul-2026), **49%** de los votantes considera inapropiadas estas participaciones y **19%** las apoya (no verificado). **Inferencia:** el gobierno como accionista da **piso** (no deja caer a la empresa) pero pone **techo** (precios, clientes y capital bajo presión política) y crea riesgo de reversión si cambia el Congreso. Debe modelarse como opción con dos colas.

### 4.7 México: Paquete Económico 2027 (8-sep-2026)

| Variable | Paquete 2027 | Nota |
|---|---|---|
| PIB 2027 | **1.5-2.5%** (2.0% puntual) | Antes 1.9-2.9%. PIB 2026: 1-2% |
| RFSP | **3.9% del PIB** | 4.1% en 2026. Pre-Criterios planteaban 3.5% |
| Balance primario / SHRFSP | Superávit primario ~1.1% (Investing) / SHRFSP ~55% del PIB (Investing y adn40) | Dos fuentes secundarias coinciden en la SHRFSP. Ninguna cifra está confirmada en los Criterios Generales (portal de Hacienda caído, 503) |
| Tributarios | **15.9% del PIB**, sin impuestos nuevos | Control de IEPS a combustibles, retenciones a plataformas |
| Costo financiero | **17.2% de los ingresos**, el más alto desde 1999 (Investing) | Es la restricción que señala Moody's |
| Apoyo a Pemex | **MXN 81.1 mil millones (−70%)** (Investing). Meta de superávit financiero de Pemex: MXN 95 mil millones (Expansión) | Moody's (Roxana Muñoz, Expansión, 24-sep) espera "**al menos** 10,000 millones de dólares de transferencia cada año por un periodo de cinco años" |
| Tipo de cambio | **18.00 por dólar** (Investing) | La nota de adn40 no contiene "17.9" ni ninguna cifra de tipo de cambio. Fuente única y secundaria |
| Inflación y tasa | 3.0% y 6.0% al cierre de 2027 | Hacienda supone ~50 pb más de recortes de Banxico |

Fuentes: SHCP comunicado 71, Expansión, Investing, adn40. Presentó el secretario Édgar Amador. **Calendario legal:** Ley de Ingresos a más tardar el **20-oct** en Diputados y el **31-oct** en el Senado. Presupuesto de Egresos a más tardar el **15-nov**. **Inferencia:** la aprobación es segura. Lo que sí se pronostica es la desviación del RFSP, las medidas que se agreguen en comisiones y cómo se ejerza el apoyo a Pemex.

### 4.8 Banxico

- Mantuvo 7.00% el 5-feb. Bajó a **6.75%** el 26-mar y a **6.50%** el 7-may. Pausas el 25-jun, el 6-ago y el **24-sep** (unánime). Son **tres** pausas consecutivas según el listado oficial y Proceso (Expansión dice "cuarta").
- El comunicado del 24-sep "sigue anticipando que la inflación general converja a la meta en el **cuarto trimestre de 2027**", menciona "la ausencia de presiones de demanda" y dice que "la política monetaria **no tendría que reaccionar de manera mecánica** ante los ajustes previstos a la tasa de fondos federales" (Banxico).
- **Diferencial contra el techo de la Fed: 250 pb.** **Inferencia:** es el colchón de *carry* más delgado en años y aumenta la sensibilidad del peso a *shocks* (cap. 16).
- **Calendario oficial:** decisiones el **5-nov** y el **17-dic**; minutas el 8-oct y el 19-nov; Informe Trimestral el 26-nov.

### 4.9 Reformas y Estado de derecho

- **Reforma judicial.** Tras la elección del 2-jun-2024 el peso llegó a **18.36** el 7-jun. Ese día perdió 2.65% (desde 17.88) cuando AMLO insistió en la reforma judicial (El Financiero). Las cifras de −4.3% el primer día (16.97 a 17.70), ~16% hasta septiembre y −22.5% en 2024 vienen de CNN/EFE, que bloqueó el acceso en esta sesión (no verificado). Es el caso de referencia del riesgo institucional mexicano. La nueva SCJN funciona desde sep-2025. La segunda elección judicial se **aplazó de 2027 a 2028** (may-2026).
- **Elektra.** El 13-nov-2025 la SCJN resolvió por unanimidad que Elektra (43.3) y TV Azteca (5.1) deben pagar **MXN 48.3 mil millones** (ISR de 2008-2010, 2012 y 2013). Elektra reconoce MXN 32.1 mil millones, ya pagó 13.98 y cubrirá el resto en parcialidades hasta **jul-2027** (Bloomberg Línea, La Silla Rota). Una contingencia de probabilidad baja se volvió un **pasivo cierto**.
- **Ley de Amparo** (DOF 16-oct-2025, vigente el 17-oct). El interés legítimo exige una lesión "real y diferenciada que concurra más allá de lo hipotético". La suspensión no procede cuando obstruye el cobro de créditos fiscales por el Estado. Que la suspensión fiscal exija **garantía** no se confirmó en DLA Piper (no verificado). La reforma aplica a juicios con etapas en trámite (DLA Piper). **Regla:** un crédito fiscal material en litigio se modela con probabilidad de pago cercana a 100% más accesorios.
- **Autónomos.** Cofece e IFT se sustituyen por la **Comisión Nacional Antimonopolio**, aprobada en Diputados el **1-jul-2025** por 323 a 125 (LatinUS), y por la **CRT**, instalada el 17-oct-2025. La sectorización de la Comisión a Economía y la fecha de instalación de la CRT no se verificaron en esta sesión. **Inferencia:** telecomunicaciones, concentraciones y preponderancia se pronostican ahora como decisiones políticas.
- **Energía.** Las leyes secundarias están vigentes desde el **19-mar-2025**. Pemex y CFE son "empresas públicas del Estado" y la CNE sustituye a CRE y CNH. En 2025 hubo apoyo a Pemex de ~US$35 mil millones (1.9% del PIB, según Moody's; no verificado) y P-Caps por US$12 mil millones. Moody's ratificó a Pemex con perspectiva estable (may-2026). El nivel B1 no se verificó porque La Jornada bloqueó el acceso.

### 4.10 Calificación soberana

| Agencia | Nota | Perspectiva | Última acción |
|---|---|---|---|
| Moody's | **Baa3** (antes Baa2) | Estable | 20-may-2026 |
| S&P | BBB | **Negativa** | 12-may-2026 |
| Fitch | BBB- | Estable | abr-2026 (ratificación, según Bloomberg Línea) |

Moody's citó el debilitamiento fiscal acelerado desde 2024, el gasto inflexible, la base de ingresos reducida y el apoyo a Pemex. Los "18 meses" sin cambios son la lectura de un analista (Carlos López Jones, en El Financiero) sobre la perspectiva estable, no una frase de Moody's.

**Regla de índices (verificada):** Bloomberg (metodología del 8-ene-2026) usa la **calificación intermedia** de Moody's, S&P y Fitch, en la práctica una regla de "dos de tres". Si sólo hay dos calificaciones, usa la más baja. Para los bonos soberanos en moneda local del Global Aggregate usa la calificación soberana de largo plazo en moneda local, y para seguir en el índice exige al menos Baa3/BBB-/BBB-. **Inferencia:** hoy la intermedia es BBB- (Baa3 / BBB / BBB-). Para salir de los índices de grado de inversión de Bloomberg harían falta **dos** agencias en especulativo. El riesgo cercano es que S&P baje a BBB- y deje a las tres en el último escalón. La calificación en moneda local puede diferir de la de moneda extranjera; se revisa antes de concluir sobre los Mbonos.

### 4.11 T-MEC, aranceles y seguridad

- **1-jul-2026:** "*The United States did not agree to renew the USMCA in its current form*" (USTR). Sigue vigente mientras se negocia; por el artículo 34.7 corre hasta 2036 con **revisiones anuales** (White & Case). Rondas bilaterales: 29-may (CDMX), junio (Washington) y 21-23 jul (CDMX). La cuarta, en Washington, tiene fecha tentativa **28-29 sep**, que Economía pidió tratar como provisional (El Heraldo, 23-sep). Canadá queda fuera de las bilaterales y enfrenta la Sección 338 (4.4).
- **Nudo:** EUA exige **50% de contenido estadounidense** por vehículo. México pide primero alivio de la 232 (autos 25%, acero 50%). Se espera una prolongación hasta fines de 2026 o 2027 (TLC Magazine).
- **Aranceles mexicanos** (DOF 29-dic-2025, vigentes desde el 1-ene-2026): **5-50%** sobre **1,463 fracciones** a países sin tratado, con meta de más de MXN 70 mil millones de recaudación (Diario de México; el número de fracciones no aparece en esa nota). **Plan México:** inversión de más de 25% del PIB desde 2026. Seis Polos de Bienestar tienen **US$17.49 mil millones comprometidos** (Segundo Informe).
- **Seguridad-finanzas:** FinCEN emitió órdenes contra **CIBanco, Intercam y Vector** el 25-jun-2025, y la CNBV intervino al día siguiente (Mayer Brown). El 23-sep-2026, según El Financiero citando al NYT, Trump **frenó planes de ataques aéreos** por el endurecimiento de Sheinbaum contra los cárteles. **Inferencia:** el riesgo de seguridad llega a los precios primero por el sistema financiero (FinCEN, OFAC, cárteles designados FTO).

---

## 5. Evidencia real

| Evento | Instrumento | Reacción | Lección |
|---|---|---|---|
| Elección EUA 2000 | Elección | Ganan las conectadas a republicanos y pierden las conectadas a demócratas | El valor político es transversal |
| Geithner (2008) | Nombramiento | +6% el primer día y +12% a 10 días en las conectadas | Los nombramientos son eventos operables |
| Elección EUA 2016 | Elección | Ganan domésticas y con impuestos altos. Lo complejo se incorporó al precio con rezago | La ventaja está en analizar lo complejo |
| Elección MX, 2-jun-2024 | Elección y constitución | Peso en 18.36 el 7-jun (−2.65% ese día). El −22.5% anual no está verificado | La mayoría calificada es un evento de régimen |
| Aranceles, abr-2025 | IEEPA | S&P −10% en 2 sesiones, luego reversión (cap. 23) | Instrumento frágil, reversión probable |
| SCOTUS e IEEPA, feb-2026 | Judicial | ~US$166 mil millones sujetos a reembolso, ~US$81 mil millones distribuidos hacia julio. Sustitutos: la 122, después la 301 y la 338 contra Canadá | Se pronostica el **instrumento sustituto** |
| Moody's, may-2026 | Calificación | "Ajuste anunciado y sin sobresaltos" (El Financiero) | Lo que importa es la **segunda** rebaja |
| Fed, 16-sep-2026 | Monetaria | La mediana de 2027 sube a 4.1% | La sorpresa estuvo en el *path* |

**Qué funciona (A/B):** medir la sorpresa contra los futuros, anticipar sustitutos, el análisis transversal de ganadores y perdedores y usar mercados de predicción como precio de referencia. **Qué ya no (D):** la deriva pre-FOMC, el ciclo presidencial como regla y copiar al Congreso. **Dudoso (C):** comprar empresas con mucho *lobbying* o muchas contribuciones, por posible confusión con factores y por costos. **Evidencia del ciclo 2025-2026:** casi toda medida extrema basada en declaración o en una orden frágil se pausó, se anuló o se sustituyó. Persistió lo que tenía base en ley o en la 232.

**Mercados de predicción.** Sirven como probabilidad implícita para eventos sin futuros (elecciones, votos de cloture), como **línea base** para calificar al dueño y para detectar cambios bruscos. Sus límites: el sesgo *favorite-longshot*, las reglas de resolución (cap. 23), la liquidez y el riesgo regulatorio de las plataformas.

---

## 6. Traducción operable

### 6.1 Método de 8 pasos para anticipar una decisión

1. **Pregunta resoluble:** qué, quién, cuándo, con qué criterio y en qué fuente (DOF, Federal Register).
2. **Instrumento:** su durabilidad y su vía de impugnación (2.4).
3. **Calendario legal:** plazos constitucionales, reglamentarios y judiciales.
4. **Actores y vetos:** qué gana cada uno (voto, presupuesto, carrera, relación con EUA) y quién puede bloquear (PT y PVEM, los 60 votos del Senado de EUA, la SCJN, los estados de EUA, las calificadoras).
5. **Señales:** las **costosas** (presupuesto, DOF, nombramiento, capital político) pesan más que las **baratas** (declaración, mañanera). El peso relativo se calibra con el *ledger*.
6. **Precio implícito:** futuros, OIS, TIIE-IRS, CDS, Kalshi y Polymarket (leyendo la regla), *spreads* de fusión.
7. **Pronóstico** con probabilidad, horizonte y criterio, registrado **antes** del evento.
8. **Cadena causal:** evento → exposición → efecto económico → estado financiero → valoración → diferencia contra lo que ya está en el precio.

### 6.2 La ventaja del ex funcionario, verificable

**Legítima:** conocer procesos (cómo se redacta y firma un decreto, cuánto tarda en publicarse en el DOF, cómo negocian Hacienda y Energía, qué significa que un tema entre o no a la mañanera) y leer incentivos. **Prohibida:** usar información no pública obtenida por relaciones. En México la sanciona la Ley del Mercado de Valores; en EUA, la Regla 10b-5 de la SEC, incluida la teoría de apropiación indebida. Es un límite duro.

**Registro** (`herramientas/pronosticos.py agregar`):
- `autor` = `dueno` o `claude`.
- `pregunta` y `criterio_resolucion`: binarios y con la fuente de resolución.
- `notas` = `tipo=[timing|contenido|magnitud|reaccion]; ventaja=[proceso|incentivos|calendario|lectura_publica]; p_mercado=0.xx (plataforma, regla)`.

**Calificación:** Brier propio ≤ **0.20** con N ≥ **50** (config). Además, **habilidad sobre el mercado** = Brier(p_mercado) − Brier(propio), calculada por `tipo`. **Regla:** sólo los tipos de pregunta con habilidad > 0 y N ≥ 30 pueden usarse para dimensionar el satélite.

### 6.3 Calendario político-regulatorio

| Fecha | Evento | Qué pronosticar |
|---|---|---|
| 28-29 sep (tentativa) | 4ª ronda del T-MEC en Washington | ¿Alivio de la 232? ¿50% de contenido estadounidense? |
| 29 sep | Sección 232 a fármacos para las empresas fuera del Anexo III. Veto de la 338 a productos canadienses | ¿Más acuerdos MFN? ¿Represalia de Canadá, desvío hacia México? |
| ~5 oct | Cierre esperado de Paramount-WBD (según Ellison) | ¿Retrasos por los *amicus* o por los otros 11 estados? |
| 8 oct | Minuta de Banxico | ¿Disensos o sesgo? |
| 20 / 31 oct | Ley de Ingresos 2027: Diputados / Senado | Cambios contra la iniciativa |
| 27-28 oct | FOMC | ¿Segunda alza? |
| 3 nov | Intermedias de EUA | Control de las cámaras |
| 4 nov | *Refunding* del Tesoro | ¿Se mantiene "*several quarters*"? |
| 5 nov | Banxico | ¿Pausa o recorte? |
| 15 nov | Presupuesto de Egresos 2027 | Reasignaciones |
| 19 / 26 nov | Minuta de Banxico / Informe Trimestral | Pronósticos de inflación |
| 8-9 dic | FOMC con SEP | *Dots* de 2027 |
| 11 dic | Vence la CR (*lame duck*) | ¿Nueva CR, ómnibus o cierre? |
| 17 dic | Banxico | Última decisión del año |
| 10 ene 2027 | Vence la tregua EUA-China (cap. 23) | ¿Extensión? |
| Fin del invierno a verano de 2027 | Se alcanza el techo de deuda (BPC) | Negociación con un Congreso posiblemente dividido |
| jun 2027 | Intermedias de México | ¿Morena y aliados conservan la mayoría calificada? |
| 1 jul 2027 | Revisión anual del T-MEC | ¿Extensión? |
| 31 ene 2028 | Vence el periodo de Powell como gobernador | ¿Nueva vacante? |

**Regla:** el calendario se revisa cada lunes. Cada evento binario se registra en el *ledger* al menos 5 días hábiles antes.

### 6.4 Checklist de riesgo regulatorio por empresa (0 a 3 puntos cada renglón)

| # | Dimensión | 0 puntos | 3 puntos |
|---|---|---|---|
| 1 | Ingresos que dependen del gobierno (contratos, subsidios, precios regulados) | <5% | >40% |
| 2 | Concesión o licencia | No aplica | Renovación discrecional en menos de 3 años |
| 3 | Exposición arancelaria y cumplimiento del T-MEC | Doméstica o cumple | >30% de las ventas expuesto a 232 o 301 sin exención |
| 4 | Antimonopolio | Sin operaciones pendientes | Fusión pendiente o preponderancia |
| 5 | Créditos fiscales en litigio / capital | 0 | >10% |
| 6 | Política industrial | Neutral | Gobierno accionista o subsidio con fecha de vencimiento |
| 7 | Decisión de un regulador sectorial (FDA, CNE, CRT, CNBV) en 12 meses | No | Binaria y material |
| 8 | Seguridad y AML (FinCEN, OFAC, FTO) | Sin exposición | Antecedentes o clientes en sectores señalados |
| 9 | Conexiones y partes relacionadas | Ninguna | El control depende del gobierno en turno |
| 10 | Durabilidad del marco que sostiene la tesis | Ley o constitución | Orden ejecutiva, declaración o litigio abierto |
| 11 | Evento binario dentro del horizonte | No | Sí, en menos de 30 días |
| 12 | Exposición soberana indirecta (Pemex o CFE como contraparte) | Baja | Proveedor o acreedor relevante |

**Traducción (Regla):**
- **0-8 puntos:** tamaño normal.
- **9-16 puntos:** descuento de valoración de al menos 10% y máximo la mitad del límite por emisora (0.05 en el perfil estándar, 0.15 en arena).
- **17 o más:** sólo como posición de evento con tesis escrita, riesgo ≤ `max_riesgo_pct_capital` (0.01 estándar, 0.005 en fase de prueba, 0.03 en arena) y salida atada al evento.
- **3 puntos en el renglón 5 o en el 8:** veto hasta revisión con el dueño.

### 6.5 Sectores y emisoras sensibles (ejemplos de exposición, no recomendaciones)

| País | Sector | Palanca y estado al 25-sep-2026 | Qué vigilar |
|---|---|---|---|
| EUA | Farmacéuticas | 232 al 100%; 26 acuerdos MFN; vouchers de la FDA | Quién queda fuera de los acuerdos |
| EUA | Semiconductores y minerales críticos | Gobierno accionista (Intel 9.9%, MP 15%) | Condiciones de nuevos apoyos; cambio de Congreso |
| EUA | Renovables | Fin de créditos para obras iniciadas desde el 4-jul-2026 | Precipicio de 2028 |
| EUA | Autos y camiones | 232 al 25% y contenido estadounidense | Rondas con México |
| EUA | Medios y tecnología | Antimonopolio negociable; estados con veto | Cierre de Paramount-WBD |
| EUA | Importadores | 301 de 10-12.5%; reembolsos IEEPA | Ingresos extraordinarios; apelación del DOJ |
| EUA | Contratistas | CR hasta el 11-dic | Cierre en la *lame duck* |
| MX | Bancos | Tasa de 6.50%; precedente de FinCEN | Fin de los recortes; AML |
| MX | Energía (Pemex, CFE, privados) | Apoyo −70% en 2027 | Pagos a proveedores |
| MX | Telecomunicaciones | CRT y Comisión Antimonopolio | Preponderancia, espectro |
| MX | Exportadores y acero | 301 exenta con T-MEC; 232 sin alivio | Rondas del T-MEC |
| MX | Grupos con litigios fiscales | SCJN y amparo (Elektra) | Otros grandes contribuyentes |
| MX | Construcción, cemento, parques industriales | Plan México, Polos de Bienestar | Asignaciones del Presupuesto 2027 |

### 6.6 Protocolo ante un evento no programado

- **T+0 (menos de 2 horas):** identificar el instrumento y su durabilidad. Medir la reacción contra la probabilidad previa. Mapear ganadores y perdedores por canal. Si el instrumento es frágil, **no vender en pánico**.
- **T+1 día:** vía de impugnación, plazo y sustituto probable. Registrar en el *ledger*: "¿seguirá vigente en 90 días?".
- **T+1 semana:** cadena causal hasta los estados financieros. Se opera sólo con ella y dentro de los límites de pérdida del periodo. Si se toca un límite, no se abren posiciones tácticas nuevas.

### 6.7 Parámetros propuestos (a integrar en `parametros.json`; aquí no se modifica)

```json
"politica": {
  "evento_binario_riesgo_max_estandar": 0.01,
  "evento_binario_riesgo_max_arena": 0.03,
  "checklist_regulatorio_umbral_medio": 9,
  "checklist_regulatorio_umbral_alto": 17,
  "descuento_valoracion_riesgo_medio": 0.10,
  "n_min_pronosticos_por_tipo": 30,
  "prohibido": ["deriva pre-FOMC", "copiar al Congreso", "informacion no publica"]
}
```

Estos valores son coherentes con `riesgo_por_operacion`, `brier_objetivo` (0.20) y `min_pronosticos_para_evaluar` (50).

**Fuentes primarias a monitorear** (automatización: cap. 22). **EUA:** federalreserve.gov, treasury.gov, federalregister.gov, congress.gov (con los reportes del CRS), ustr.gov, cbp.gov (CSMS), supremecourt.gov, EDGAR 8-K, fda.gov, CFTC. **México:** dof.gob.mx (ediciones matutina y vespertina; la vigencia está en los transitorios), Gaceta Parlamentaria y del Senado, finanzaspublicas.hacienda.gob.mx, banxico.org.mx, CNBV, SAT (RMF), SE, comunicados de las calificadoras.

---

## 7. Trampas

1. **Reaccionar a la noticia y no a la sorpresa.** Lo que ya estaba en el precio no se opera.
2. **Confundir declaración con instrumento.** Sólo cuenta lo que se publica, se presupuesta o se firma.
3. **Suponer que un instrumento frágil es permanente.** IEEPA fue anulada, la 122 caducó y la 301 las sustituyó.
4. **Creer que la política terminó cuando se anula su instrumento.** Hay que pronosticar el sustituto.
5. **Operar la deriva pre-FOMC o el ciclo presidencial.** La primera murió y el segundo tiene N≈20.
6. **Copiar al Congreso.** En promedio pierde contra el mercado.
7. **Tratar una mayoría como un bloque.** PT y PVEM tumbaron la reforma electoral (259-234-1, cuando se necesitaban 334). La CLARITY no llegó al pleno aunque el partido del presidente controla el Senado.
8. **Leer el *dot plot* como pronóstico.** La mediana para 2022 era 0.9% y la tasa terminó en 4.25-4.50%. Hoy además el presidente de la Fed no entrega punto.
9. **Tratar el litigio fiscal mexicano como una opción gratis.** Después de la reforma al amparo la suspensión exige garantía.
10. **Ver a un gobierno accionista como garantía.** Da piso, pero también techo y riesgo de reversión.
11. **Confundir acertar el contenido con acertar la reacción del mercado.** Se califican por separado.
12. **Usar una sola fuente secundaria para cifras fiscales o de actualidad.** En la verificación, un tipo de cambio atribuido a adn40 no estaba en la nota, había un conteo de pausas equivocado, una votación de cloture no se sostuvo y una cifra de reembolsos IEEPA no se encontró.
13. **Cruzar la línea de la información privilegiada.** Destruye el activo principal del dueño.
14. **Olvidar el tipo de cambio.** Medido en MXN, el signo puede invertirse (cap. 16).

---

## 8. Examen de titulación

**1. La Fed sube 25 pb y el S&P cae 1.5%. ¿Qué falta para interpretarlo?**
La expectativa previa en futuros, tanto del *target* como del *path*. Si el alza estaba descontada, la caída vino de la guía o de la conferencia.

**2. ¿Quién preside la Fed y cuál fue la última decisión?**
Kevin Warsh, confirmado 54-45 el 13-may-2026. El 16-sep subió la tasa a 3.75-4.00% con votación 12-0. Es la primera alza desde jul-2023. La mediana de 2026 es 4.125% y la de 2027, 4.1%.

**3. ¿Qué implican *Trump v. Cook* y *Trump v. Slaughter*?**
Cook (5-4): destituir a un gobernador de la Fed exige causa y debido proceso. Slaughter (6-3): se revoca *Humphrey's Executor* y el presidente puede remover comisionados de agencias independientes, salvo en la Fed. En consecuencia, la regulación es política del Ejecutivo y la protección de la Fed es de procedimiento, no inmunidad. La amenaza contra Cook sigue viva desde agosto.

**4. Ordena por durabilidad: 232, IEEPA, depreciación de 100% de la OBBBA, 122.**
OBBBA (es ley) > 232 (base estatutaria clara) > 122 (legal pero caduca a los 150 días) > IEEPA (anulada).

**5. ¿Cuál es el estado del T-MEC y qué variable domina para México?**
EUA no aceptó extenderlo el 1-jul-2026, así que hay revisiones anuales hasta 2036 y rondas bilaterales (la 4ª, tentativa el 28-29 sep). Domina el cumplimiento de reglas de origen, porque la 301 exenta lo que entra bajo el T-MEC. Quedan pendientes la 232 (autos 25%, acero 50%) y la exigencia de 50% de contenido estadounidense.

**6. ¿Cuáles son las cifras clave del Paquete 2027 y sus plazos?**
PIB de 1.5-2.5%, RFSP de 3.9%, tributarios de 15.9% del PIB, sin impuestos nuevos, costo financiero de 17.2% de los ingresos y apoyo a Pemex −70%. Ley de Ingresos: 20 y 31 de octubre. Presupuesto de Egresos: 15 de noviembre.

**7. ¿Dónde está Banxico y por qué importa el diferencial?**
En 6.50%, con tres pausas y la inflación en meta hasta el 4T-2027. El diferencial con el techo de la Fed es de 250 pb, el colchón de *carry* más delgado en años, así que el peso queda más expuesto a *shocks*.

**8. Con Moody's en Baa3, S&P en BBB negativa y Fitch en BBB-, ¿hay salida inminente de los índices de grado de inversión?**
No. Bloomberg usa la calificación intermedia de las tres ("dos de tres"; metodología de ene-2026), así que hacen falta dos agencias en especulativo. El riesgo es que S&P baje a BBB- y deje a las tres en el último escalón. Para los Mbonos se revisa además la calificación en moneda local.

**9. ¿Qué enseña el caso Elektra?**
Que la nueva SCJN y la reforma al amparo convierten las contingencias fiscales en pasivos ciertos: MXN 48.3 mil millones resueltos y pagos en parcialidades hasta 2027. Un litigio fiscal material se modela con pago cercano a 100%.

**10. ¿Qué dice la evidencia sobre la deriva pre-FOMC?**
Hubo +49 pb en las 24 horas previas entre 1994 y 2011 (~80% del exceso anual), y desapareció después de 2015. Es D. En el régimen Warsh conviene reducir el tamaño alrededor del anuncio.

**11. ¿Cómo se demuestra la ventaja del ex funcionario?**
Con pronósticos binarios registrados antes del evento y la probabilidad del mercado anotada en `notas`. La ventaja existe si Brier(mercado) − Brier(dueño) > 0 con N ≥ 50 (≥30 por tipo para dimensionar) y un Brier ≤ 0.20. Nunca con información no pública.

**12. ¿Cómo se usa la evidencia sobre conexiones sin tenerlas?**
Como evento transversal y como riesgo. Faccio: anunciar una conexión sube el valor. Goldman-Rocholl-So: en 2000 el valor se redistribuyó según la afiliación del consejo. Geithner: +6% el primer día y +12% a 10 días. Ante un cambio de poder o un nombramiento, se identifica quién gana y quién pierde la renta.

**13. Aplica el método a: "¿Habrá cierre de gobierno en EUA después del 11-dic-2026?"**
Criterio: falta de fondos a las 00:01 del 12-dic, según la OMB. Instrumento: CR u ómnibus. Calendario: *lame duck*. Actores: la mayoría saliente quiere cerrar el año; el Senado necesita 60 votos. Señal: la CR anterior pasó 90-6 y 370-48. Precio: mercados de predicción. Se registra la probabilidad. Cadena causal: contratistas, datos económicos retrasados, *bills*.

**14. Un *post* anuncia un arancel sorpresa el viernes por la noche. ¿Qué haces el lunes?**
T+0: si no hay orden publicada, el instrumento es frágil y no se vende en pánico. Medir la reacción contra la probabilidad previa, mapear ganadores y perdedores y revisar la exención del T-MEC. T+1: identificar la vía legal probable (232, 301 o 122) y su plazo, y registrar "¿vigente en 90 días?". Todo dentro de los límites de pérdida.

---

## 9. Fuentes

**Fed y política monetaria**
- Comunicado FOMC, 16-sep-2026: https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm
- Calendario FOMC: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
- CNBC, decisión: https://www.cnbc.com/2026/09/16/fed-rate-decision-september-2026.html
- TheStreet, *dot plot*: https://www.thestreet.com/fed/fed-rate-hike-warsh-dot-plot-inflation
- TradingKey, *dot plot*: https://www.tradingkey.com/analysis/stocks/us-stocks/262172696-fed-rate-hike-october-dot-plot-median-one-more-2026-tradingkey
- CNBC, Trump y Warsh: https://www.cnbc.com/2026/09/16/trump-fed-interest-rate-warsh.html
- CNN, confirmación: https://www.cnn.com/2026/05/13/economy/kevin-warsh-confirmation-trump-fed-chair
- Spectrum, juramento y Powell: https://spectrumlocalnews.com/us/snplus/politics/2026/05/22/kevin-warsh-sworn-in-jerome-powell-trump-white-house-ceremony-clarence-thomas
- *Trump v. Cook*: https://www.supremecourt.gov/opinions/25pdf/25a312_5468.pdf
- SCOTUSblog, Cook (ago-2026): https://www.scotusblog.com/2026/08/trump-informs-lisa-cook-that-he-is-considering-her-removal/
- SCOTUSblog, *Slaughter*: https://www.scotusblog.com/2026/06/court-allows-trump-to-fire-ftc-commissioner-and-overturns-major-restraint-on-presidential-power/

**Tesoro, Congreso y aranceles**
- Tesoro, *refunding* 5-ago-2026: https://home.treasury.gov/news/press-releases/sb0590
- BPC, techo de deuda: https://bipartisanpolicy.org/article/when-will-we-reach-the-debt-limit-again/
- CRFB, OBBBA: https://www.crfb.org/blogs/whats-one-big-beautiful-bill-act
- Sidley, OBBBA y energía: https://www.sidley.com/en/insights/newsupdates/2025/07/the-one-big-beautiful-bill-act-navigating-the-new-energy-landscape
- FedTools, CR año fiscal 2027: https://www.fedtools.com/blog/government-shutdown-october-2026
- CNBC, mercados de predicción y Senado: https://www.cnbc.com/2026/09/16/prediction-markets-say-democrats-are-slightly-favored-to-win-senate.html
- DWT, CLARITY: https://www.dwt.com/blogs/financial-services-law-advisor/2026/09/clarity-act-crypto-market-structure-bill-stalled
- CNBC, cripto: https://www.cnbc.com/2026/09/01/crypto-enters-september-with-policy-gamble-hanging-by-a-thread.html
- Holland & Knight, reembolsos IEEPA: https://www.hklaw.com/en/insights/publications/2026/06/ieepa-tariff-refund-update-government-appeals
- Skadden, CAPE: https://www.skadden.com/insights/publications/2026/03/tariff-refund-mechanism-takes-shape
- Global Trade Alert, 301: https://globaltradealert.org/blog/forced-labour-section-301-final-action
- BBVA Research, 301 y México: https://www.bbvaresearch.com/en/publicaciones/mexico-favorable-position-on-new-us-tariffs-under-section-301-for-forced-labor/
- CRS, 232 autos: https://www.congress.gov/crs-product/IN12545
- Crowell, 232 fármacos: https://www.crowell.com/en/insights/client-alerts/trump-administration-imposes-section-232-tariffs-on-patented-pharmaceutical-imports-tiered-rate-structure-takes-effect-beginning-july-31-2026
- Duane Morris, MFN: https://www.duanemorris.com/alerts/most_favored_nation_drug_pricing_agreements_expanded_nine_additional_pharmaceutical_0926.html

**Antimonopolio, reguladores y política industrial**
- CNBC, Google ad tech: https://www.cnbc.com/2026/09/02/google-defeats-us-bid-to-force-ad-tech-sale.html
- CNN, Paramount y los estados: https://www.cnn.com/2026/09/21/media/paramount-wbd-settlement-cnn-ellison-bonta-lawsuit
- Deadline, moción contra el acuerdo: https://deadline.com/2026/09/paramount-merger-delayed-settlement-challenge-1237112480/
- SEC, informe semestral: https://www.sec.gov/newsroom/press-releases/2026-42-sec-proposes-amendments-permit-optional-semiannual-reporting-public-companies
- Federal Register, CFTC: https://www.federalregister.gov/documents/2026/06/12/2026-11854/prediction-markets-public-interest-determinations
- FDA, CNPV: https://www.fda.gov/news-events/press-announcements/fda-grants-seventh-approval-under-national-priority-voucher-pilot-program
- BioSpace, Pazdur: https://www.biospace.com/fda/pazdur-questions-legality-safety-of-fdas-expedited-drug-approvals-programs
- Intel, acuerdo con el gobierno: https://www.intc.com/news-events/press-releases/detail/1748/intel-and-trump-administration-reach-historic-agreement-to
- CSIS, participaciones federales: https://www.csis.org/analysis/understanding-federal-equity-investments-strategic-companies
- Fortune, USA Rare Earth: https://fortune.com/2026/01/26/trump-admin-buys-stake-usa-rare-earth-wave-deals-critical-minerals/

**México**
- SHCP, comunicado 71: https://www.gob.mx/shcp/prensa/comunicado-no-71-la-secretaria-de-hacienda-y-credito-publico-entrega-el-paquete-economico-2027-al-h-congreso-de-la-union
- Expansión, Paquete 2027: https://expansion.mx/economia/2026/09/08/entrega-paquete-economico-2027-mensaje-secretario-hacienda
- Investing, Paquete 2027: https://mx.investing.com/news/economy-news/hacienda-recorta-pib-a-2-en-paquete-economico-2027-y-busca-deficit-de-35-3759177
- adn40, Paquete 2027: https://www.adn40.mx/finanzas/2026-09-08/paquete-economico-2027-hacienda-recorta-crecimiento-de-mexico-y-revela-que-pasara-con-los-impuestos/
- Banxico, anuncios: https://www.banxico.org.mx/publicaciones-y-prensa/anuncios-de-las-decisiones-de-politica-monetaria/anuncios-politica-monetaria-t.html
- Banxico, calendario 2026: https://www.banxico.org.mx/monetary-policy/d/%7B0C35369C-BF8F-E5A8-7710-FD5A6716474F%7D.pdf
- Proceso, Banxico: https://www.proceso.com.mx/economia/2026/9/24/banxico-se-desmarca-de-la-fed-congela-la-tasa-e-insiste-en-que-mexico-no-tiene-que-seguir-a-eu-380590.html
- USTR, revisión del T-MEC: https://ustr.gov/about/policy-offices/press-office/press-releases/2026/july/ambassador-greer-issues-statement-usmca-joint-review
- White & Case, T-MEC: https://www.whitecase.com/insight-alert/usmca-2026-joint-review-united-states-declines-extend-agreement-triggering-annual
- El Heraldo, rondas: https://heraldodemexico.com.mx/nacional/2026/9/23/cuando-es-la-negociacion-del-t-mec-que-se-discute-fechas-893607.html
- TLC Magazine: https://tlcmagazinemexico.com/secciones/people-of-trade/la-cuarta-ronda-que-llego-sin-texto-firmado-y-con-un-reloj-que-ya-rebaso-su-propia-fecha/index.html
- Bloomberg Línea, calificaciones: https://www.bloomberglinea.com/latinoamerica/mexico/mexico-queda-en-el-ultimo-escalon-de-grado-de-inversion-con-moodys-y-fitch/
- El Financiero, Moody's: https://www.elfinanciero.com.mx/economia/2026/05/21/moodys-baja-nota-crediticia-a-mexico-por-debilidad-fiscal/
- La Jornada, Pemex B1: https://www.jornada.com.mx/noticia/2026/05/22/economia/moodys-ratifica-calificacion-de-pemex-con-perspectiva-estable
- Expansión, apoyos a Pemex: https://expansion.mx/empresas/2026/09/24/pemex-llegara-apoyos-gobierno-pese-meta-autosuficiencia
- El Financiero, reforma electoral: https://www.elfinanciero.com.mx/nacional/2026/03/11/reforma-electoral-va-rumbo-a-la-guillotina-sin-apoyo-del-verde-y-pt-sigue-la-sesion-en-vivo/
- La Jornada, elección judicial en 2028: https://www.jornada.com.mx/noticia/2026/05/29/politica/avala-senado-la-reforma-que-pospone-de-2027-a-2028-la-eleccion-judicial
- Bloomberg Línea, Elektra: https://www.bloomberglinea.com/latinoamerica/mexico/nueva-suprema-corte-resuelve-que-elektra-de-salinas-pliego-debe-pagar-al-sat/
- La Silla Rota, pago de Elektra: https://lasillarota.com/negocios/2026/5/25/grupo-elektra-liquida-primera-parte-de-deuda-fiscal-por-32-mil-mdp-ante-sat-588858-amp.html
- DLA Piper, amparo: https://www.dlapiper.com/es-mx/insights/publications/2025/10/mexico-reforms-the-amparo-law
- LatinUS, Cofece: https://latinus.us/mexico/2025/7/1/diputados-extinguen-la-cofece-avalan-la-creacion-de-la-comision-nacional-antimonopolio-145754.html
- Diputados, leyes de energía en el DOF: https://comunicacionsocial.diputados.gob.mx/index.php/notilegis/publica-dof-leyes-secundarias-de-la-reforma-constitucional-en-materia-energetica
- Aranceles a Asia: https://www.diariodemexico.com/mi-nacion/publican-en-el-dof-decreto-sobre-aranceles-productos-asiaticos
- Polos de Bienestar: https://es-us.noticias.yahoo.com/polos-bienestar-atraer%C3%ADan-17-491-150000390.html
- Mayer Brown, FinCEN: https://www.mayerbrown.com/en/insights/publications/2025/09/ongoing-developments-related-to-fincens-cibanco-order
- El Financiero, ataques frenados: https://www.elfinanciero.com.mx/nacional/2026/09/23/trump-freno-ataques-aereos-contra-mexico-por-endurecimiento-contra-carteles-de-sheinbaum-segun-nyt/
- El Financiero, peso en 2024: https://www.elfinanciero.com.mx/economia/2024/06/07/por-que-el-peso-y-los-mercados-enloquecieron-despues-de-las-elecciones-2024/
- CNN/EFE, peso en 2024: https://cnnespanol.cnn.com/2025/01/01/mexico/fin-superpeso-moneda-mexicana-se-deprecia-efe

**Agregadas en la verificación (2026-09-25)**
- Bloomberg, *Fixed Income Index Methodology* (8-ene-2026): https://assets.bbhub.io/professional/sites/10/Bloomberg-Index-Publications-Fixed-Income-Index-Methodology.pdf
- Fed, SEP 16-sep-2026: https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm
- Wikipedia, Kevin Warsh: https://en.wikipedia.org/wiki/Kevin_Warsh
- Federal Register, Proclamación 11020 (fármacos): https://www.federalregister.gov/documents/full_text/text/2026/04/09/2026-06956.txt
- Federal Register, Proclamaciones 11056 y 11063 (Sección 338, Canadá): https://www.federalregister.gov/documents/full_text/text/2026/08/24/2026-17294.txt y https://www.federalregister.gov/documents/full_text/text/2026/09/14/2026-18837.txt
- Federal Register, propuesta CFTC (texto): https://www.federalregister.gov/documents/full_text/text/2026/06/12/2026-11854.txt
- Wikipedia, *Learning Resources v. Trump*: https://en.wikipedia.org/wiki/Learning_Resources_v._Trump
- Wikipedia, Google ad tech: https://en.wikipedia.org/wiki/United_States_v._Google_LLC_(2023)
- Wikipedia, Paramount-WBD: https://en.wikipedia.org/wiki/Acquisition_of_Warner_Bros._Discovery_by_Paramount_Skydance
- Polymarket, Senado 2026 (consulta 25-sep-2026): https://polymarket.com/event/which-party-will-win-the-senate-in-2026
- Banxico, comunicado del 24-sep-2026: https://www.banxico.org.mx/publicaciones-y-prensa/anuncios-de-las-decisiones-de-politica-monetaria/%7B7D0BDB6E-E519-9C69-04AA-ABD4D31E4850%7D.pdf
- Wikipedia, elecciones federales de México de 2027: https://es.wikipedia.org/wiki/Elecciones_federales_de_M%C3%A9xico_de_2027
- La Silla Rota, pagos de Elektra: https://lasillarota.com/negocios/2026/5/25/grupo-elektra-liquida-primera-parte-de-deuda-fiscal-por-32-mil-mdp-ante-sat-588858.html
- Belmont et al. (JPubE 2022): https://ideas.repec.org/a/eee/pubeco/v207y2022ics0047272722000044.html
- Cooper-Gulen-Ovtchinnikov (JF 2010): https://ideas.repec.org/a/bla/jfinan/v65y2010i2p687-724.html

**Literatura académica:** los enlaces están en la tabla de la sección 3.

---

## Registro de verificación (2026-09-25)

**Método.** Verificador adversarial. El presupuesto de WebSearch de la sesión ya estaba agotado (200/200), así que todo se contrastó con **WebFetch** directo a fuentes primarias (Fed, Tesoro, Federal Register, SEC, FDA, USTR, Banxico, SHCP, opinión de la SCOTUS, metodología de Bloomberg) o a prensa y bases académicas con fecha: unas 75 consultas y **58 elementos** revisados. No se pudo acceder a CNBC, CNN, Crowell, SSRN, Wiley, La Jornada, el portal de Hacienda ni Kalshi (403, 451 o 503).

**Confirmados.**
- **Fuente primaria:** decisión y SEP de la Fed del 16-sep, *Trump v. Cook*, calendario FOMC, *refunding* del 5-ago, Proclamación 11020, SEC 10-S, FDA CNPV, USTR 1-jul, Intel 9.9% y Banxico (decisiones de 2026, calendario y comunicado del 24-sep).
- **Prensa o secundaria con fecha:** Warsh 54-45 y sin punto; *Slaughter* 6-3; CR al 11-dic; IEEPA 6-3; Sección 301; 26 acuerdos MFN; remedios de Google; Paquete 2027 (PIB, RFSP, tributarios, 17.2%, Pemex −70%); rondas del T-MEC; exigencia de 50% de contenido; reforma electoral 259-234-1; elección judicial en 2028; FinCEN; freno a los ataques aéreos (NYT, 23-sep); Polos de Bienestar; aranceles mexicanos; Elektra; Moody's y S&P.
- **Literatura (resumen o texto consultado):** Bernanke-Kuttner, Lucca-Moench (49 pb, ~80%), Kurov-Wolfe-Gilbert, Cieslak et al., Santa-Clara-Valkanov, Pastor-Veronesi, Snowberg et al., Wagner et al., Faccio, Goldman-Rocholl-So, Acemoglu et al., Cohen-Coval-Malloy, Chen-Parsley-Yang, Belmont et al. y Nakamura-Steinsson.

**Corregidos en sitio.**
1. **Regla de índices:** se confirmó la calificación intermedia ("dos de tres") en la metodología de Bloomberg. Se añadió el umbral Baa3/BBB-/BBB- y la advertencia de moneda local.
2. **Tipo de cambio del Paquete 2027:** queda 18.00 (Investing). La nota de adn40 no contiene 17.9 ni ninguna cifra de tipo de cambio.
3. **Balance primario y SHRFSP:** la SHRFSP (~55%) coincide en dos fuentes secundarias (Investing y adn40). Sigue sin fuente primaria.
4. **Pemex:** decía "hasta US$10 mil millones al año". Moody's dice "**al menos**" US$10 mil millones al año durante cinco años.
5. **CLARITY:** la votación de cloture 49-50 del 15-sep no se sostiene. DWT dice que no llegó al pleno tras el estancamiento del 13-sep.
6. **Reembolsos IEEPA:** los US$128.68 mil millones no aparecen en las fuentes citadas. Se sustituyeron por US$166 mil millones sujetos a reembolso, US$23 mil millones aprobados más US$95 mil millones en cola al 9-jun y ~US$81 mil millones distribuidos hacia julio.
7. **Sección 122:** entró en vigor el 24-feb, no el 20-feb.
8. **Fármacos 232:** el corte no es por tamaño. Aplica desde el 31-jul a las empresas del Anexo III y desde el 29-sep a las demás. Se añadieron las tasas diferenciadas y el 0% hasta el 20-ene-2029 para acuerdos MFN. La fecha de corte "antes del 2-abr" no se sostiene. MFN al 31-ago, no al 4-sep.
9. ***Slaughter*:** no excluye a la Fed; reserva la cuestión.
10. **CFTC:** no prohíbe por categoría; enumera actividades que la Comisión "*may determine*". Publicada el 12-jun.
11. **Paramount-WBD:** el acuerdo es con California y el WGA; no se confirmó que se sumaran los 11 estados restantes. La "moción" fue una emergencia de *Block the Merger* admitida el 24-sep para presentar *amicus*. Cierre esperado hacia el 5-oct según Ellison; no había cerrado al 25-sep.
12. **Comisión Antimonopolio:** la discrepancia se resolvió a favor del 1-jul-2025 (323-125).
13. **Fitch:** última acción en abr-2026 (Bloomberg Línea), no en mar-2026.
14. **Moody's "18 meses":** es la lectura de un analista, no un texto de Moody's.
15. **Peso 2024:** la fuente citada sólo sostiene 17.88 → 18.36 (−2.65%) el 7-jun. El resto queda como no verificado.
16. **Intel:** el pago incluye US$3.2 mil millones de Secure Enclave, no sólo CHIPS. USA Rare Earth: US$1.6 mil millones, participación de 8% a 16%.
17. **FDA:** que Prasad encabece el comité queda sin verificar. Pazdur habló en nov-2025.
18. **Elektra:** se precisaron los ejercicios (2008-2010, 2012, 2013), la fecha (13-nov-2025) y la unanimidad.
19. **Amparo:** la redacción es "real y diferenciada". La garantía para la suspensión fiscal queda como no verificada.
20. **SEP:** el texto decía "16 esperan otra alza y 4 esperan dos". Se reemplazó por el reparto exacto: 12 ven una alza más, 4 ven dos y 2 ninguna.
21. **Omisión relevante añadida:** la **Sección 338 contra Canadá** (aranceles de hasta 50% vigentes desde el 22-ago y veto a importaciones desde el 29-sep-2026). Se reflejó en 2.4, 4.4, 4.11 y 6.3.
22. **Intermedias de México:** el 6-jun-2027 se confirmó con la regla de la LGIPE y con fuente secundaria (500 diputaciones y 17 gubernaturas).
23. **4ª ronda del T-MEC:** se confirmó que sigue siendo tentativa. Economía pidió tratar la fecha como provisional.
24. **Polymarket:** 63% de Senado demócrata en la consulta directa del 25-sep-2026. El 55% de Kalshi y el 59% de Polymarket del 16-sep se atribuyen a CNBC sin verificación directa.

**Sigue sin verificar:** balance primario y SHRFSP en los Criterios Generales; la magnitud de Cooper-Gulen-Ovtchinnikov (el resumen no la da); el resumen de Eggers-Hainmueller; la cita de Trump a Warsh (CNBC); la cita "*two-way street*" de Warsh; la encuesta de CNBC (49/19); el nivel B1 de Pemex y el apoyo de ~US$35 mil millones en 2025; la instalación de la CRT el 17-oct-2025 y la sectorización de la Comisión Antimonopolio; los datos del peso en 2024 de CNN/EFE; el número de 1,463 fracciones; el litigio de la CFTC con estados; el calendario del INE.

**Inferencias que no se pueden verificar:** la ponderación entre señal costosa y señal barata (6.1, paso 5) y las vidas medias de la tabla 2.4 son inferencias del panel. Se calibran con el *ledger* (N ≥ 30 por tipo) y no son hechos.
