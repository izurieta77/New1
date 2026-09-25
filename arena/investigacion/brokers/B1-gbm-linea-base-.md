# B1. GBM como línea base para comparar brókers

**Fecha de corte:** 2026-09-25
**Serie:** `arena/investigacion/brokers/` (B1 = línea base; los demás B-documentos se comparan contra esta tabla)
**Pregunta de la serie:** ¿qué bróker maximiza el rendimiento **neto** de una cuenta de ~20,000 MXN de persona física residente en México, en una competencia de rendimiento % contra IAs que se quedan en GBM?
**Relación con documentos previos:** este documento **no repite** `01-gbm-operativa-y-costos.md` (A1) ni `02-universo-sic-bmv-agresivo.md` (A2). Los cita, verifica lo que cambió y agrega lo que faltaba: versión nueva de la Guía, custodia, catálogo de ETFs de momentum y UCITS, texto de ley del ISR y constancia fiscal, e incidentes de 2026. `conocimiento/11-mexico` no existe en el repo. `laboratorio/replicas/V05-spiva-y-fiscalidad-sic/` solo tiene el pre-registro (sin resultados); aquí se cierran con fuente primaria sus puntos fiscales 1, 3 y 4, y una parte del 6.

**Etiquetas:** **[H]** hecho con fuente y fecha · **[C]** cálculo propio sobre datos con fuente · **[I]** inferencia · **[R]** recomendación · **(no verificado)** sin fuente primaria que lo confirme.

---

## Resumen ejecutivo

1. **[H] La tarifa no cambió en la Guía nueva.** GBM publicó una *Guía de Servicios de Inversión* fechada "Julio 2026" (PDF creado el 23-jul-2026) que reemplaza a la V1025 de feb-2026 [1][2]. El corretaje de Trading MX (BMV, BIVA y SIC) sigue en **0.25% por operación para un monto operado de hasta 1,000,000 MXN (promedio de 3 meses)**, "la única comisión que se cobra es la de corretaje", y "se le aumentará el Impuesto al Valor Agregado" [1][3]. **Con IVA: 0.29% por lado y 0.58% por ida y vuelta.** En una cuenta de 20,000 MXN, una rotación completa cuesta 116 MXN [C].
2. **[H] No hay comisión de custodia, mantenimiento ni inactividad publicada.** La tabla de comisiones de la Guía de julio 2026 no incluye ninguna [1], y la FAQ oficial de comisiones tampoco [3]. La cifra de "129 MXN al mes por inactividad" que aparece en resúmenes de búsqueda **no tiene respaldo**: el artículo al que se atribuye (Finantres, actualizado el 16-sep-2026) dice que "GBM no publica una comisión general de mantenimiento" [27].
3. **[H] No hay comisión mínima por operación en ninguna fuente oficial** [1][3][4]. El "mínimo de 20 MXN" sigue sin respaldo (igual que en A1).
4. **[H] El tipo de cambio del SIC no es un cargo aparte.** El valor cotiza y se liquida en pesos, y el costo cambiario queda dentro del precio [21]. [C] Medido: el precio en BMV se desvía de (precio en EUA × tipo de cambio implícito) una **mediana de 0.23% en SPMO y 0.27% en MTUM** (24-jun a 24-sep-2026) [25], dentro del rango de 0.04%–0.48% que A2 midió para otros ETFs líquidos. En Trading USA la conversión MXN↔USD es explícita (Smart Cash ↔ Trading USA) y **GBM no publica el spread** [8].
5. **[H] Catálogo de momentum.** **IMTM, IDMO, EEMO y PIE no aparecen como listados en la BMV** en StockAnalysis ni en TradingView, con serie `*` ni con serie `N` [25][26]. Son agregadores y omiten valores, así que esto **no prueba** que no estén listados, pero no hay ninguna evidencia de que lo estén. Lo que **sí** cotiza en la BMV: **MTUM** (poco operado: 9 de 22 sesiones) y **SPMO** (21 de 22 sesiones, mediana de ~0.80 M MXN al día) [25]. También **dos UCITS de momentum global: IWMO/N (iShares, ISIN IE00BP3QZ825) y XDEM/N (Xtrackers, IE00BL25JP72)** [26]. Que GBM los tenga habilitados en la app: **no verificado**.
6. **[H] Los UCITS irlandeses existen en el SIC con serie `N`.** Vanguard contaba ~740 UCITS negociables en el SIC y más de 1,600 ETFs globales (abr-2024) [23]. En la BMV cotizan, entre otros, CSPX/N, VUAA/N, IWDA/N, VWRA/N, EIMI/N, CNDX/N e IB01/N [26]. El SIC está abierto a "cualquier tipo de inversionista" desde ene-2014 [21].
7. **[H] ISR: el texto de la ley confirma lo que A1 dejó abierto.** Art. 129 de la LISR: 10% definitivo sobre la ganancia en la venta de acciones extranjeras "cotizadas en dichas bolsas" (las mexicanas) y de "títulos que representen índices accionarios" [19]. En el SIC **no hay retención en la venta**; el 10% se paga en la declaración anual [14]. **Las pérdidas se compensan en el mismo ejercicio o en los diez siguientes**, solo contra ganancias del art. 129 y actualizadas por inflación [19]. El intermediario tiene que calcular la ganancia o la pérdida y entregar la constancia [19]. GBM la entrega en la app [17]. La retención sobre intereses en 2026 es de **0.90%** (LIF 2026, art. 24, DOF 07-11-2025) [20].
8. **[I] Consecuencia fiscal para comparar brókers.** Por la redacción del art. 129, el 10% solo aplica cuando la venta se hace en una bolsa mexicana (BMV o BIVA, incluido el SIC). Una venta en NYSE o Nasdaq, sea por Trading USA de GBM o por un bróker extranjero, **no entra en las fracciones I ni II** [19]. Esto es inferencia sobre el texto legal, **sin confirmar con el SAT**. Si se confirma, el régimen fiscal favorece al SIC frente a cualquier ruta directa a EUA para el rendimiento neto del dueño. **No afecta el TWR del torneo**, porque el ISR no se descuenta de la cuenta durante la temporada.
9. **[H] Incidentes.** Lo grave ya está en A1: el 7-abr-2025, más de 5 horas sin operar [30], y el 20-oct-2025, intermitencias por AWS. **En 2026 no encontré notas de prensa de caídas.** Solo hay reseñas de usuarios en App Store (3 a 20 de mayo de 2026) que hablan de fallas para operar e ingresar; son evidencia **anecdótica** [29]. Por otro lado, según prensa que cita a la CNBV, a GBM le impusieron multas de **2,886,600 MXN** por "deficiencias en sistemas automatizados de detección, monitoreo y reporte de operaciones" y de **481,100 MXN** por seguridad de la información (publicadas en ene-feb de 2026) [28]. El portal de sanciones de la CNBV respondió 503.
10. **[R] Para la competencia:** la línea base contra la que se mide a cualquier otro bróker es **0.29% por lado con IVA, sin mínimo, sin custodia, con costo cambiario implícito de ~0.1%–0.3% por lado en ETFs líquidos del SIC, sin fracciones en el SIC, con stops y OCA en Trading MX y con el 10% definitivo del art. 129.** Otro bróker solo gana dinero neto si mejora esta suma para el patrón de operación real de la cuenta (ver §9).

---

## 1. Tabla de línea base (GBM, persona física, 2026-09-25)

| # | Concepto | GBM | Tipo | Fuente |
|---|---|---|---|---|
| 1 | Documento tarifario vigente | *Guía de Servicios de Inversión*, "Julio 2026" (reemplaza a la V1025) | H | [1][2] |
| 2 | Corretaje Trading MX (BMV, BIVA, SIC), ≤1 M MXN operados (promedio de 3 meses) | **0.25%** por operación, sobre el valor operado | H | [1][3] |
| 3 | IVA | Se suma al corretaje: **0.29% por lado** | H | [1] |
| 4 | Ida y vuelta | **0.58%** del monto (116 MXN por rotación completa de 20k) | C | [1] |
| 5 | Escalones | 0.20% (1–3 M), 0.15% (3–5 M), 0.125% (5–10 M), 0.10% (>10 M) | H | [2][3] (la Guía de julio 2026 repite el renglón de 3–5 M y omite el de 5–10 M, errata irrelevante para 20k [1]) |
| 6 | Comisión mínima por operación | **No existe en fuentes oficiales** | H (ausencia) | [1][3][4] |
| 7 | Uso de la plataforma | "no tiene costo" | H | [1] |
| 8 | Custodia de valores | **Sin cargo publicado**. En Trading MX la única comisión es el corretaje | H | [1][3] |
| 9 | Mantenimiento o inactividad | **Sin cargo publicado**. El "129 MXN/mes" no tiene respaldo | H / no verificado | [3][27] |
| 10 | Trading USA (DriveWealth) | 0.25% por compra o venta. La FAQ no dice si lleva IVA | H | [4] |
| 11 | IVA en Trading USA | [I] Probable, porque la Guía dice que a "las comisiones que cobre la Casa de Bolsa" se les suma IVA [1] | I (no verificado) | [1][4] |
| 12 | Tipo de cambio en el SIC | Implícito en el precio en MXN. Desviación mediana contra el valor justo: 0.23% (SPMO) y 0.27% (MTUM). A2 midió 0.04%–0.48% en otros ETFs líquidos | H/C | [21][25], A2 §4–5 |
| 13 | Tipo de cambio en Trading USA | Conversión explícita Smart Cash ↔ Trading USA; liquidación de dólares en 1 día hábil. **Spread no publicado** | H / no verificado | [8] |
| 14 | Fracciones | **Solo en Trading USA** (desde 1 USD). En el SIC, títulos completos | H | [10][11], A1 [36] |
| 15 | Órdenes Trading MX | Mercado, limitada, MPL (mín. 100 títulos; oculto 2,000), stop, stop limitada, trailing stop, OCA, OTA | H (re-verificado) | [6] |
| 16 | Órdenes Trading USA | **Solo mercado y limitada** | H (re-verificado) | [5] |
| 17 | Vigencia máxima de la orden | 30 días; reingreso diario con folio nuevo | H | [18] |
| 18 | Filtros de precio | SIC: 5% o 10% según el sentido; locales: 3% o 6%. Por mesa: hasta 10% o 20% | H | [18] |
| 19 | Depósitos | SPEI a CLABE única, "en cualquier momento", llegan "en minutos". Sin costo publicado | H | [13] |
| 20 | Retiros | Días hábiles de 7:30 a 13:30 (CDMX), "en minutos"; después, al día hábil siguiente. Smart Cash Dólares: 2 o 3 días hábiles | H | [12] |
| 21 | Catálogo SIC (mercado) | BMV sep-2023: 1,676 acciones + 1,404 ETFs. Vanguard abr-2024: >1,600 ETFs, ~740 UCITS | H | [22][23] |
| 22 | Catálogo GBM | "Más de 5,000 instrumentos locales e internacionales" en Market y "más de 6,000" contando Trading USA. **GBM no publica la lista de emisoras SIC habilitadas** | H / no verificado | [10][11] |
| 23 | ETFs de momentum | IMTM, IDMO, EEMO, PIE: **sin evidencia de listado en la BMV**. MTUM y SPMO: sí. IWMO/N y XDEM/N (UCITS): sí | H (listado) / no verificado (habilitación en GBM) | [25][26] |
| 24 | ETFs apalancados | SOXL, TQQQ, SPXL y otros, listados y activos (A2). UPRO y SSO: sin página BMV (re-verificado) | H | A2, [25] |
| 25 | ISR por venta en el SIC | 10% definitivo sobre la ganancia neta anual, **sin retención**; se paga en la declaración anual | H | [14][19] |
| 26 | Pérdidas | Se compensan en el ejercicio o en los 10 siguientes, solo contra ganancias del art. 129 | H | [19] |
| 27 | Constancia fiscal | GBM calcula la ganancia o pérdida y emite la constancia (obligación legal del art. 129). En la app: Menú → "Estados de cuenta y constancias" → "Constancias fiscales" | H | [17][19] |
| 28 | Dividendos del SIC (EUA) | 30% en EUA (10% con W-8BEN) y luego 10% en México sobre el neto, retenido por GBM | H | [15] |
| 29 | W-8BEN para Trading MX/SIC | **75 USD + IVA**, trámite vía Indeval, confirmación en máx. 72 h. En Trading USA es gratis (A1) | H (re-verificado) | [16], A1 [24] |
| 30 | Retención sobre intereses (Smart Cash) | 0.90% anual sobre el capital en 2026 | H (primaria) | [20] |
| 31 | Tope contractual | Los montos de la Guía son "límites máximos"; GBM puede "pactar con algún cliente una comisión [...] distinta o más alta" | H | [1] |

---

## 2. Comisiones: qué cambió desde A1

- **[H] Versión nueva de la Guía.** Existe un PDF "Guía de Servicios de Inversión, Julio 2026" (metadatos: creado el 23-jul-2026; subido en `uploads/2026/08/`) [1]. A1 usaba la V1025 (12-feb-2026) [2]. Extraje y comparé el texto completo de ambas con `pypdf`:
  - El tope de "Ejecución de operaciones sobre Instrumentos de Renta Variable a través de las plataformas GBM y GBM+" sigue en **"Hasta .25%"**, con "el uso de la plataforma no tiene costo" [1].
  - La cláusula del IVA sigue igual [1].
  - La lista de "Clases de valores" ahora menciona expresamente "Acciones y fracciones de acciones en el extranjero (DriveWealth)" [1].
  - La tabla de derivados pasó de "4T25" a "2T26 Cuenta Global" [1][2]; no aplica a la cuenta.
  - Hay una **errata** en la tabla de escalones: repite "De $3,000,001 a $5,000,000 0.15%" y omite el renglón de 0.125% [1]. La V1025 [2] y la FAQ [3] traen los cinco escalones. No cambia nada para 20k.
- **[H] Custodia y mantenimiento.** Ni la Guía de julio 2026 ni la V1025 contienen las palabras "custodia" o "mantenimiento" en un concepto de cobro. Revisé el texto completo de las dos [1][2]. La FAQ oficial de comisiones solo lista corretaje, Smart Cash Dólares (1.5% + IVA anual), fondos y portafolios [3].
- **[H] Lo que no está en la tabla de retail no se cobra en retail**, salvo pacto expreso. La Guía permite "pactar con algún cliente una comisión bajo un esquema distinto o más alta", "dejando constancia del acuerdo de voluntades" [1]. [I] Una cuenta retail de la app no firma ese pacto.
- **Sin cambios en Trading USA:** 0.25% por compra o venta; "se mostrará un monto aproximado que incluye esta comisión" [4]. No dice nada del IVA ni del tipo de cambio [4].

---

## 3. Tipo de cambio

### 3.1 SIC (Trading MX)

- **[H]** La BMV dice que en el SIC se opera "en pesos" [21]. GBM no cobra una conversión cambiaria aparte en Trading MX. Su única comisión ahí es el corretaje [1][3].
- **[C] El costo cambiario es la desviación entre el precio en BMV y (precio en EUA × TC implícito).** Usé el método de A2: el TC implícito es el promedio de SPY e IVV (cierre BMV / cierre EUA) del mismo día, del 24-jun al 24-sep-2026, con cierres de StockAnalysis [25].

| ETF | Días con precio en ambos mercados | Desviación mediana | Desviación máxima |
|---|---|---|---|
| SPMO (S&P 500 Momentum) | 48 | **0.23%** | 6.55% |
| MTUM (MSCI USA Momentum) | 30 | **0.27%** | 1.36% |

  - TC implícito del 24-sep-2026: **17.75** [C][25]. A2 da el cierre de 17.71 (El Financiero) para ese día, una diferencia de 0.2%.
  - [I] En los poco operados, el "cierre" puede ser un hecho viejo o de un solo lote. La desviación mide spread más desfase. No es el spread cotizado.
- **[I]** Para el torneo, el TC es un factor común: toda posición del SIC es larga en USD. Los rivales en GBM tienen la misma exposición si también compran SIC.

### 3.2 Trading USA

- **[H]** El dinero pasa de Smart Cash a Trading USA "para adquirir dólares" y regresa a Smart Cash para venderlos. "La liquidación de dólares toma un día hábil" [8].
- **(no verificado)** El spread MXN↔USD. Ningún documento oficial de GBM lo publica [4][8]. En A1 el tipo de referencia para Smart Cash Dólares es "Valmer Spot 48 h".
- [R] Mídelo en la app: cotiza 100 USD y compáralo contra el spot del mismo minuto. Es el dato que falta para comparar con un bróker extranjero.

---

## 4. Catálogo: momentum, internacionales, apalancados y UCITS

### 4.1 Tamaño del SIC

- **[H]** BMV (sep-2023, vía Expansión, cifra del director de Promoción y Emisoras): **1,676 acciones y 1,404 ETFs** listados en el SIC [22].
- **[H]** Vanguard (abr-2024): el SIC da acceso a "more than 1,600 global ETFs" y hay "approximately 740 UCITS ETFs available to be traded on the SIC" [23].
- **[H]** La página actual de la BMV solo dice "cientos de opciones de inversión" y "desde enero de 2014, cualquier tipo de inversionista puede participar en el SIC" [21].
- **(no verificado)** Una cifra oficial de 2026. El buscador de emisoras de la BMV está detrás de protección anti-bots (F5, error 500 al consultarlo) y el portal de BIVA carga con JavaScript sin datos en el HTML. La cifra de "2,763 valores" de un resumen de búsqueda no aparece en la página de Rankia a la que se atribuye.
- **(no verificado)** Cuántas de esas emisoras tiene habilitadas GBM. GBM no publica su catálogo del SIC. Solo publica totales mezclados: ">5,000" en Market y ">6,000" con Trading USA [10][11].

### 4.2 ETFs de momentum e internacionales

Método: páginas de cotización BMV en StockAnalysis (`/quote/bmv/<ticker>/`) y TradingView (`BMV-<ticker>/` y `BMV-<ticker>/N/`), consultadas el 2026-09-25 [25][26]. Liquidez = mediana del importe diario (cierre × volumen) del 25-ago al 24-sep-2026, 22 sesiones sin el 16-sep, con 0 los días sin operación. Mismo método que A2.

| ETF | Exposición | ¿Página BMV? | Liquidez 30d (mediana MXN/día; días con operación) | Precio BMV (MXN) = % de 20k | Nota |
|---|---|---|---|---|---|
| **IMTM** | Momentum desarrollados ex-EUA | **No** (SA 404; TV 404 con `*` y con `N`) | — | — | Sin evidencia de listado |
| **IDMO** | Momentum desarrollados ex-EUA (Invesco) | **No** (SA 404; TV 404) | — | — | Sin evidencia de listado |
| **EEMO** | Momentum emergentes (Invesco) | **No** (SA 404; TV 404) | — | — | Sin evidencia de listado |
| **PIE** | Momentum emergentes (Invesco DWA) | **No** (SA 404; TV 404) | — | — | Sin evidencia de listado |
| MTUM | Momentum EUA (iShares) | **Sí** | **0** (9/22) | 5,490 (22-sep) = 27% | Muy baja liquidez |
| SPMO | S&P 500 Momentum (Invesco) | **Sí** | **~0.80 M** (21/22) | 2,701 (24-sep) = 13.5% | Baja-media |
| **IWMO/N** | MSCI World Momentum, UCITS (iShares, IE00BP3QZ825) | **Sí** (TV) | no medida | no medida | Alternativa UCITS a IMTM (incluye EUA) |
| **XDEM/N** | MSCI World Momentum, UCITS (Xtrackers, IE00BL25JP72) | **Sí** (TV) | no medida | no medida | Idem |
| EFA / VEA / EEM | Desarrollados ex-EUA / emergentes (sin factor) | **Sí** (SA) | no medida | — | Proxies sin momentum |
| MEXMTUM ISHRS | Momentum México (TRAC local de BlackRock México) | Listado local desde 2014, según un aviso de la CNBV visto solo en el listado de búsqueda | no medida | — | (parcialmente verificado) |

- **[I]** Para una estrategia de momentum internacional *ex-EUA* (IMTM/IDMO) o emergente (EEMO/PIE), el SIC vía GBM **no ofrece el instrumento exacto**. Los sustitutos listados son UCITS de momentum *global*, que incluyen EUA (IWMO/N, XDEM/N), o ETFs sin factor (EFA, VEA, EEM).
- **[I]** Trading USA da acceso a NYSE y Nasdaq [7]. Es probable que IMTM, IDMO, EEMO y PIE estén ahí, pero **no está verificado**: GBM no publica su catálogo de DriveWealth. Esa ruta tiene fracciones, pero solo órdenes a mercado y limitadas, y el spread cambiario no está publicado.

### 4.3 Apalancados

- Sin cambios respecto a A2: SOXL, TQQQ, SPXL, TECL, QLD, SPUU y otros tienen listado activo en la BMV. **UPRO y SSO siguen sin página BMV** (StockAnalysis 404, re-verificado el 2026-09-25) [25]. Una guía secundaria de sep-2026 dice que el acceso de GBM a SOXL y TQQQ "está limitado", sin fuente. No cambia la conclusión de A2: listados sí; habilitación en la app, no verificada.

### 4.4 UCITS

- **[H]** En la BMV cotizan con serie `N` (moneda MXN, bolsa BMV, ISIN irlandés): CSPX/N (IE00B5BMR087), IWDA/N (IE00B4L5Y983), EIMI/N (IE00BKM4GZ66), VWRA/N (IE00BK5BQT80), CNDX/N (IE00B53SZB19), IB01/N (IE00BGSF1X88), VUAA/N, IUSA/N, IMEU/N y MVOL/N [26].
- **[H]** WisdomTree (2019) describía el SIC como una vía para "certain institutional investors" [24]. La BMV dice que desde 2014 puede participar cualquier inversionista [21], y Vanguard dice que "institutional and retail investors have benefitted from the availability of UCITS ETFs in Mexico" [23]. [I] La restricción institucional de 2019 no es la regla actual para el SIC en general. Que GBM habilite UCITS en la app para una persona física: **no verificado**.
- **[I] Fiscal:** un UCITS de índice accionario vendido en el SIC encaja en el art. 129, fr. II ("títulos que representen índices accionarios") [19]. En las clases de acumulación no hay dividendo que retenga GBM. La retención de EUA sobre dividendos dentro del fondo irlandés (15% por tratado) **no se verificó aquí**. Es el punto 6 del pre-registro V05.

---

## 5. Impuestos y constancia (texto primario)

- **[H] Art. 129 LISR** (texto de la Cámara de Diputados, última reforma DOF 01-04-2024) [19]:
  - Fr. I: 10% definitivo sobre la ganancia en la enajenación de acciones de sociedades mexicanas "cuando su enajenación se realice en las bolsas de valores concesionadas [...] o de acciones emitidas por sociedades extranjeras cotizadas en dichas bolsas de valores".
  - Fr. II: "títulos que representen índices accionarios enajenados en las bolsas de valores [...] a que se refiere la fracción anterior".
  - Fr. III: solo acciones de **sociedades mexicanas** vendidas en mercados reconocidos de países con tratado.
  - Ganancia por emisora: precio de venta menos comisiones, menos el costo promedio de adquisición actualizado más comisiones.
  - **Pérdidas:** "podrán disminuir dicha pérdida únicamente contra el monto de la ganancia que en su caso obtenga el mismo contribuyente en el ejercicio o en los diez siguientes". Si no se aplica pudiendo hacerlo, se pierde el derecho.
  - **Intermediario:** "deberán hacer el cálculo de la ganancia o pérdida del ejercicio" y entregarlo. Si hay pérdida, "deberán emitir [...] una constancia de dicha pérdida".
- **[H] GBM:** en el SIC la venta "no tiene ninguna retención" y se paga el "ISR anual del 10% sobre las ganancias". Lo que no se vende no paga [14]. Las constancias de 2025 están en la app (Menú → "Estados de cuenta y constancias" → estrategia → "Constancias fiscales") [17].
- **[H] Dividendos:** mexicanos, 10% no acreditable (utilidades desde 2014). SIC (EUA), 30% en el extranjero (10% con W-8BEN) y luego 10% en México sobre el neto, que retiene GBM [15].
- **[H] Intereses:** LIF 2026, art. 24: "la tasa de retención anual [...] será del 0.90 por ciento" (DOF 07-11-2025) [20]. En A1 solo tenía fuente secundaria (AMCP).
- **[C] El W-8BEN en el SIC no se paga con los ahorros en una cuenta de 20k.** Cuesta 75 USD × 1.16 = 87 USD, ~1,541 MXN a 17.71, o sea **7.7% de la cuenta** [16]. Con un ETF de 1% de rendimiento por dividendo, la carga sin W-8BEN es 30% + 10% × 70% = 37% del dividendo; con W-8BEN es 10% + 10% × 90% = 19%. La diferencia es 0.18% anual sobre la posición, **~36 MXN al año** con 20k invertidos. El trámite se recuperaría en ~43 años.
- **[I] Rutas fuera de la bolsa mexicana.** Las fracciones I y II exigen que la venta ocurra en una bolsa concesionada en México, y la III solo cubre emisoras mexicanas [19]. Una venta de acciones o ETFs de EUA en NYSE o Nasdaq (Trading USA de GBM o un bróker extranjero) **no parece caber en el art. 129**. Tributaría en otro régimen, probablemente con tasa progresiva. **No verificado con el SAT ni con un especialista.** Es un punto crítico para B2 (bróker extranjero).

---

## 6. Operativa: órdenes, fracciones, depósitos y retiros

- **[H] Re-verificado hoy.** Trading MX: mercado (solo emisoras de bursatilidad media o alta e IPC), limitada, MPL activa, pasiva y con volumen oculto (mín. 100 títulos; oculto 2,000), stop, stop limitada, trailing stop, OCA y OTA [6]. Trading USA: solo mercado y limitada [5].
- **[H] Fracciones:** "Acciones completas o fracciones de empresas que cotizan en el mercado de Estados Unidos a través de Trading USA" [10]. En el SIC, títulos completos (A1).
- **[H] Folleto de órdenes:** la versión vigente sigue siendo la de `uploads/2024/11` (metadatos del PDF: 03-may-2025) [18]. El PDF "v1" de `assets.gbm.com` es de may-2020, o sea más viejo. Reglas sin cambio: vigencia ≤30 días, banda de ~0.20% en órdenes a mercado (también SIC) y filtros de 5%/10% en SIC [18].
- **[H] Novedades de la app desde A1 (feed oficial de releases)** [9]:
  - Transferencias a terceros (6-ago-2025).
  - Préstamo de valores en Trading USA (29-ago-2025).
  - Cuentas temáticas (3-sep-2025).
  - PPR (10-dic-2025).
  - "Metas" pasa a llamarse "Portafolios Recomendados" (19-dic-2025).
  - Asesoría (27-abr-2026).
  - Optimización de Portafolios Recomendados (14-jul-2026).
  - **No hay ninguna novedad de órdenes stop en Trading USA ni de fracciones en el SIC.**
- **[H] Depósitos:** SPEI a CLABE única por estrategia, "en cualquier momento", "en minutos". Sin costo ni límites publicados [13]. **Retiros:** días hábiles de 7:30 a 13:30 para que lleguen en minutos; Smart Cash Dólares en 2 o 3 días hábiles [12].

---

## 7. Incidentes y riesgo operativo (2025-2026)

| Fecha | Evento | Evidencia | Fuente |
|---|---|---|---|
| 7-abr-2025 | "Lunes negro": más de 5 horas sin poder operar | Prensa (El CEO) | [30], A1 |
| 20-oct-2025 | Intermitencias por la caída de AWS | Prensa | A1 [47] |
| 12-dic-2025 y ene-2026 (publicadas el 4-feb-2026) | Multas de la CNBV: 481,100 MXN (seguridad de la información) y 2,886,600 MXN (deficiencias en sistemas automatizados de detección, monitoreo y reporte de operaciones, art. 212 LMV). La nota dice que el total rebasa 15.8 M MXN | Prensa que cita a la CNBV. **El portal de la CNBV dio 503**, así que no está verificado en la fuente primaria | [28] |
| 3 a 20 de mayo de 2026 | Reseñas en App Store: "El 20% de los días no vas a poder operar porque se les cae el sistema", problemas con el código de acceso y con datos históricos | **Anecdótico** (reseñas, no prensa) | [29] |
| jun a sep de 2026 | No encontré notas de prensa de caídas | Ausencia de evidencia | búsquedas del 2026-09-25 |

- [I] Las multas de la CNBV son por controles internos (monitoreo de operaciones y resguardo de información). No son fallas de ejecución, pero sí son una señal de gobernanza. GBM sigue en el padrón de entidades supervisadas (resumen de búsqueda; no verificado en el padrón).
- [I] Las reseñas de mayo de 2026 no demuestran una caída sistémica, pero el patrón coincide con el historial de 2024-2025.

---

## 8. Números base para la competencia (cuenta de 20,000 MXN)

| Escenario | Costo por lado | Ida y vuelta | 1 rotación de 20k | 1 rotación al mes, 6 meses |
|---|---|---|---|---|
| SIC, ETF líquido (desviación ~0.1%–0.25% por lado) | 0.29% + ~0.1%–0.25% | ~0.78%–1.08% | ~156–216 MXN | ~4.7%–6.5% |
| SIC, solo comisión | 0.29% | 0.58% | 116 MXN | 3.5% |
| Trading USA (0.25%, IVA sin confirmar), una sola conversión por temporada | 0.25%–0.29% | 0.50%–0.58% + 2s por temporada | 100–116 MXN | 3.0%–3.5% + 2s |

[C] s = spread cambiario de Trading USA (no publicado). La desviación del SIC es la mediana medida en §3.1 y en A2.

- **[R] Regla de comparación justa:** los rivales en GBM pagan exactamente la fila 1 o 2. Si la cuenta se muda, **se recalcula todo** con los costos reales del bróker nuevo, como pidió el dueño. En la bitácora del torneo se anota la diferencia de costo por lado contra GBM para cada operación, así la comparación sigue siendo justa.

---

## 9. Qué tiene que superar otro bróker (criterios para B2 y siguientes)

Otro bróker **gana dinero neto** frente a GBM solo si, con el patrón de operación de la cuenta (≤1–1.5 rotaciones al mes, órdenes de 5,000 a 10,000 MXN, ETFs del SIC o de EUA):

1. **El costo por lado es menor que ~0.39%–0.54%** (0.29% de comisión más la desviación implícita del SIC). Hay que medirlo con la comisión, el IVA, el mínimo por orden, el spread cambiario y la frecuencia de conversión reales. Un mínimo fijo por orden (por ejemplo, 1 USD) pesa más en órdenes chicas.
2. **La custodia o la inactividad no se come la ventaja.** GBM cobra cero.
3. **Da acceso a instrumentos que GBM no tiene en el SIC** y que la estrategia necesita (IMTM, IDMO, EEMO, PIE, opciones, fracciones con stops), o a esos mismos con más liquidez.
4. **No empeora el ISR del dueño.** En GBM/SIC la tasa es 10% definitivo con constancia. Una venta fuera de bolsas mexicanas probablemente cae en otro régimen (§5, inferencia). Para el TWR del torneo no cuenta; para el dinero real del dueño sí.
5. **No suma riesgo operativo** en días de volatilidad (la referencia de GBM es el 7-abr-2025).
6. **Otra casa de bolsa mexicana** (Actinver, Banorte, BBVA, Santander, Vector, Kuspit, Flink) comparte con GBM el catálogo potencial del SIC y el régimen del art. 129. Solo cambian la comisión, la custodia, el catálogo habilitado y la calidad de ejecución. Si una cobra menos de 0.25% sin mínimo ni custodia, es mejora directa.

---

## 10. No verificado (pendiente)

- El spread cambiario MXN↔USD de Trading USA. Si la comisión de 0.25% de Trading USA lleva IVA.
- El catálogo del SIC que GBM tiene habilitado: si IWMO/N, XDEM/N, CSPX/N, VUAA/N, SPMO, MTUM y los apalancados aparecen y se pueden comprar en la app, y si piden algún perfil.
- Si IMTM, IDMO, EEMO y PIE están disponibles en Trading USA (DriveWealth).
- La cifra oficial 2026 de valores listados en el SIC (el buscador de la BMV está bloqueado por anti-bots; BIVA usa JavaScript).
- La liquidez local de IWMO/N y XDEM/N (no hay historial disponible en las fuentes consultadas).
- El régimen fiscal exacto de las ganancias vendidas en NYSE o Nasdaq (Trading USA o bróker extranjero) para una persona física residente. Lo de §5 es inferencia sobre el texto del art. 129.
- La retención de 15% sobre dividendos de EUA dentro de los UCITS irlandeses (V05, punto 6).
- Las multas de la CNBV en el portal oficial (503). Las caídas de 2026 fuera de las reseñas de App Store.
- El "mínimo de 20 MXN por operación" y el "129 MXN/mes de mantenimiento": ninguna fuente oficial los respalda.

---

## Fuentes

Todas se consultaron el **2026-09-25**.

1. GBM, *Guía de Servicios de Inversión*, "Julio 2026" (PDF creado el 23-jul-2026), págs. 17–19 (clases de valores, tabla de comisiones, escalones de Trading México). https://global.gbm.com/wp-content/uploads/2026/08/03140239/Guia-de-Servicios-GBM_v3.pdf
2. GBM, *Guía de Servicios de Inversión*, V1025 (PDF del 12-feb-2026). https://global.gbm.com/wp-content/uploads/2026/02/12141701/Guia-de-Servicios-GBM_V-1025.pdf
3. GBM, Centro de ayuda: "¿Qué comisiones cobran al invertir en GBM?". https://gbm.com/faqs/que-comisiones-cobran-al-invertir-en-gbm/
4. GBM, Centro de ayuda: "¿Existe alguna comisión por invertir en Trading USA?". https://gbm.com/faqs/existe-alguna-comision-por-invertir-en-trading-usa/
5. GBM, Centro de ayuda: "¿Con qué tipo de órdenes existen en Trading USA?". https://gbm.com/faqs/con-que-tipo-de-ordenes-existen-en-trading-usa/
6. GBM, Centro de ayuda: "¿Qué tipos de órdenes existen en Trading MX?". https://gbm.com/faqs/que-tipos-de-ordenes-existen-en-trading-mx/
7. GBM, Centro de ayuda: "¿Qué es Trading USA?". https://gbm.com/faqs/que-es-trading-usa/
8. GBM App, release "Trading USA, ahora en dólares" (31-mar-2025). https://about.appgbm.com/releases/experiencia-en-dolares-en-trading-usa/
9. GBM App, feed de releases (páginas 1 y 2; fechas de publicación del RSS). https://about.appgbm.com/releases/feed/
10. GBM, Centro de ayuda: "¿Cuáles son los instrumentos disponibles en Market?". https://gbm.com/faqs/cuales-son-los-instrumentos-disponibles-en-market/
11. GBM, "Trading en México y Estados Unidos". https://gbm.com/trading/
12. GBM, Centro de ayuda: "¿Cuál es el horario para retirar mi dinero en GBM?". https://gbm.com/faqs/cual-es-el-horario-para-retirar-mi-dinero-en-gbm-en-cuanto-tiempo-se-refleja/
13. GBM, Centro de ayuda: "¿Cuál es el horario para realizar depósitos en GBM?". https://gbm.com/faqs/cual-es-el-horario-para-realizar-depositos-en-gbm/
14. GBM, Centro de ayuda: "¿Cómo funcionan los impuestos por las acciones de empresas extranjeras en el SIC?". https://gbm.com/faqs/como-funcionan-los-impuestos-por-las-acciones-de-empresas-extranjeras-en-el-sic/
15. GBM, Centro de ayuda: "¿Cómo funcionan los impuestos sobre los dividendos en Trading MX?". https://gbm.com/faqs/como-funcionan-los-impuestos-sobre-los-dividendos-en-trading-mx/
16. GBM, Centro de ayuda: "¿Cómo registro el W8-BEN para Trading MX y SIC?". https://gbm.com/faqs/como-registro-el-w8-ben-para-trading-mx-y-sic/
17. GBM, Centro de ayuda: "¿Cómo y dónde recibo los Comprobantes Fiscales o CFDI por mis ganancias?". https://gbm.com/faqs/como-y-donde-recibo-los-comprobantes-fiscales-o-cfdi-por-mis-ganancias/
18. GBM, *Folleto Informativo del Sistema de Recepción, Registro, Ejecución de Órdenes y Asignación de Operaciones* (URL de 2024/11; metadatos del PDF: 03-may-2025). https://gbm.com/wp-content/uploads/2024/11/GBM-Folleto-Informativo.pdf . La versión antigua (may-2020) está en https://assets.gbm.com/docs/GBM-Folleto-Informativo_v1.pdf
19. Cámara de Diputados, *Ley del Impuesto sobre la Renta* (última reforma DOF 01-04-2024), art. 129, págs. 158–160. https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf
20. Cámara de Diputados, *Ley de Ingresos de la Federación para el Ejercicio Fiscal de 2026* (DOF 07-11-2025), art. 24. https://www.diputados.gob.mx/LeyesBiblio/pdf/LIF_2026.pdf
21. Grupo BMV, "Mercado Global (SIC)". https://www.bmv.com.mx/es/mercados/mercado-global
22. Expansión, "¿Qué es el SIC en la Bolsa de Valores?" (23-sep-2023; cifras de la BMV: 1,676 acciones y 1,404 ETFs). https://expansion.mx/mercados/2023/09/23/sistema-internacional-de-cotizaciones-bmv-20-anos
23. Vanguard México, "Trading UCITS ETFs in Mexico" (Expert Perspective, abr-2024). https://www.vanguardmexico.com/content/dam/intl/americas/documents/latam/en/2024/04/mx-sa-3458273-trading-ucits-etfs-in-mexico-v2.pdf
24. WisdomTree, "WisdomTree Cross-Lists 2 UCITS ETFs in Mexico" (19-sep-2019). https://ir.wisdomtree.com/news-events/press-releases/detail/139/wisdomtree-cross-lists-2-ucits-etfs-in-mexico
25. StockAnalysis (datos de S&P Global). Páginas BMV: https://stockanalysis.com/quote/bmv/MTUM/history/ , https://stockanalysis.com/quote/bmv/SPMO/history/ , https://stockanalysis.com/quote/bmv/SPY/history/ , https://stockanalysis.com/quote/bmv/IVV/history/ , más las páginas de cotización de EFA, VEA, EEM, SPXL y TQQQ (200). Páginas EUA: https://stockanalysis.com/etf/spmo/history/ (y mtum, spy, ivv). Devolvieron 404: `/quote/bmv/` IMTM, IDMO, EEMO, PIE, PDP, IMOM, QMOM, UPRO, SSO, CSPX, IWDA, VWRA.
26. TradingView, páginas de símbolo BMV: https://www.tradingview.com/symbols/BMV-IWMO/N/ , https://www.tradingview.com/symbols/BMV-XDEM/N/ , https://www.tradingview.com/symbols/BMV-CSPX/N/ , https://www.tradingview.com/symbols/BMV-IWDA/N/ , https://www.tradingview.com/symbols/BMV-EIMI/N/ , https://www.tradingview.com/symbols/BMV-VWRA/N/ , https://www.tradingview.com/symbols/BMV-CNDX/N/ , https://www.tradingview.com/symbols/BMV-VUAA/N/ , https://www.tradingview.com/symbols/BMV-IB01/N/ , https://www.tradingview.com/symbols/BMV-MTUM/ , https://www.tradingview.com/symbols/BMV-SPMO/ (200). Devolvieron 404 con `*` y con `N`: IMTM, IDMO, EEMO, PIE; con `N`: SWDA, IEMO, EMMO, XMOM.
27. Finantres, "¿Por qué GBM cobra comisión de mantenimiento?" (publicado el 13-may-2025, actualizado el 16-sep-2026; fuente secundaria). https://finantres.mx/mantenimiento-gbm/
28. El Cronista México, "La CNBV multa a GBM por fallas en controles internos y en la protección de información" (4-feb-2026; fuente secundaria que cita a la CNBV). https://www.cronista.com/mexico/finanzas-economia/la-cnbv-multa-a-gbm-por-fallas-en-controles-internos-y-en-la-proteccion-de-informacion/ . Fuente primaria intentada sin éxito (503): https://sanciones.cnbv.gob.mx/Detail/54095/0
29. MWM, perfil de la app GBM con reseñas de App Store (reseñas del 3 al 20 de mayo de 2026; evidencia anecdótica). https://mwm.ai/apps/gbm/6463154299
30. El CEO, "¿Inversionistas 'atrapados'? GBM falla en 'lunes negro'" (8-abr-2025). https://elceo.com/opinion/informacionconfidencial-inversionistas-atrapados-gbm-falla-en-lunes-negro/

Documentos internos: `arena/investigacion/01-gbm-operativa-y-costos.md` (A1) y `arena/investigacion/02-universo-sic-bmv-agresivo.md` (A2). Los números entre corchetes que se citan como "A1 [n]" o "A2 [n]" remiten a las fuentes de esos documentos.

---

## Registro de método

- Cerca de 30 búsquedas web y más de 25 consultas directas, entre páginas y PDFs. Los PDFs de la Guía (julio 2026 y V1025), del Folleto (2020 y 2024/2025), de la LISR, de la LIF 2026 y de Vanguard se descargaron y se extrajeron con `pypdf`. Los textos citados son los extraídos, no los resúmenes de búsqueda.
- El directorio de S&P DJI de ETPs listados en el SIC (jul-2026) devolvió 403, igual que el buscador de emisoras de la BMV (F5/500) y el portal de sanciones de la CNBV (503).
- La desviación y la liquidez se calcularon con cierres y volúmenes de StockAnalysis, con el mismo método de A2 (§3.1 y §4.2).
