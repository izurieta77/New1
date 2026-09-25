# GBM: operativa, costos y reglas para la cuenta arena

**Fecha de corte:** 2026-09-25
**Documento:** A1 de `arena/investigacion/`
**Alcance:** persona física operando en la app GBM (antes GBM+), productos Trading MX (BMV/BIVA + SIC), Trading USA, Smart Cash, deuda y fondos. Cuenta objetivo: `arena-claude`, 20,000 MXN.

**Convención de etiquetas:**
- **[H]** Hecho con fuente y fecha.
- **[I]** Inferencia mía a partir de hechos citados.
- **[R]** Recomendación operativa para la cuenta arena.
- **(no verificado)**: dato que aparece en fuentes secundarias o en resúmenes de búsqueda y que no confirmé en una fuente primaria.

---

## Resumen ejecutivo

1. **Comisión de corretaje en Trading MX (BMV y SIC): 0.25% por operación más IVA, o sea 0.29% por lado**, para montos de hasta 1,000,000 MXN (el escalón baja hasta 0.10% arriba de 10 MXN millones) [1][2]. La Guía de Servicios de GBM dice expresamente que a las comisiones "se le aumentará el IVA" [2]. **Ida y vuelta: 0.58% del monto operado**, antes del spread.
2. **No encontré un plan de suscripción ni un plan sin comisión vigente para personas físicas.** El mínimo de 20 MXN por operación que citan algunos sitios no aparece en la guía oficial ni en la FAQ de comisiones (no verificado). Un resumen de búsqueda del 2026-09-25 lo atribuye solo a "operaciones en corto" (no verificado). [I] Es probable que el "20 MXN" venga del monto mínimo de inversión de Trading Global en 2022 ("desde MXN$20" [11]), que no es una comisión. Sin mínimo, el costo en % es el mismo para 2,000, 5,000 o 10,000 MXN.
3. **Trading USA** (cuenta en dólares, custodia en DriveWealth) cobra 0.25% por compra o venta [3][28]. Permite **fracciones desde 1 USD** [5], pero **solo tiene órdenes a mercado y limitadas, sin stops** [9]. La conversión MXN→USD se hace aparte desde Smart Cash y tarda 1 día hábil en liquidar [6]. **El spread cambiario no está publicado** (no verificado).
4. **En el SIC solo se compran títulos completos** [36]. Trading MX tiene el menú de órdenes completo: mercado, limitada, MPL, Stop Market, Stop Limitada, Trailing Stop, OCA y OTA [8]. **La vigencia máxima de una orden es de 30 días** [10].
5. **Horario:** la BMV opera de 7:30 a 14:00 (hora CDMX) del 9 de marzo al 30 de octubre de 2026. **Regresa a 8:30–15:00 el martes 3 de noviembre de 2026**, porque el lunes 2 es inhábil [13][38]. **La liquidación en México es T+1** desde el 27 de mayo de 2024 [15].
6. **Apalancamiento:** GBM ofrece **margen intradía y venta en corto** bajo contrato y a solicitud. La venta en corto pide un mínimo de 10,000 MXN, solo en emisoras que GBM selecciona, y aparta 2 pesos de garantía por cada peso vendido [39] (parcialmente verificado). Futuros y opciones de MexDer existen en la Guía [2], pero no como función estándar de la app (no verificado). **TQQQ, SOXL y SPXL están listados con estatus ACTIVA en la BMV (SIC)** [35][43][44]. Que GBM permita comprarlos desde la app, y con qué perfil: no verificado.
7. **Liquidez ociosa:** Smart Cash paga de 4.00% a 4.75% anual según el nivel. Con menos de 300 mil MXN paga 4.00% [17][18]. En cambio, el **CETE 28 cerró en 6.15%** en la subasta del 22-sep-2026 [22] y la tasa de Banxico está en 6.50% [21]. La retención de ISR sobre intereses subió a **0.90% anual sobre el capital** en 2026 [29].
8. **Impuestos:** 10% definitivo sobre la ganancia en BMV y SIC, sin retención en la venta y pagado en la declaración anual [26]. Los dividendos del SIC pagan 30% en EUA (10% con W-8BEN) y luego 10% en México [27]. **El W-8BEN para el SIC cuesta 75 USD + IVA** (confirmado en la FAQ oficial de GBM [45]), alrededor de 7.6% de una cuenta de 20k [24][25][45]. En Trading USA es gratis [24].
9. **Protección:** GBM está supervisado por la CNBV. **El IPAB no cubre casas de bolsa** [30].
10. **Caídas registradas:** 26-jun-2024 (resuelta a las 12:30; inicio no reportado), 19-jul-2024 (CrowdStrike), dos caídas en menos de 5 días en dic-2024, **7-abr-2025 ("lunes negro" arancelario): más de 5 horas sin poder comprar ni vender en plena sesión de pánico**, y 20-oct-2025 (intermitencias por la caída de AWS) [31][32][33][46][47]. [I] La caída más larga documentada ocurrió en el día de mayor volatilidad, que es justo el escenario en el que una cuenta apalancada necesita operar. Para 2026 no encontré notas de prensa (ausencia de evidencia, no prueba de estabilidad).
11. **Implicación central:** con 0.58% por vuelta más el spread, **cada rotación completa de la cuenta cuesta de 0.7% a 1.2% del capital**. El presupuesto sano es **≤1 rotación completa al mes (~3.5% en la temporada)**. Solo conviene tomar operaciones con un movimiento esperado de **≥5%**, donde el costo se come ≤25% del edge.

---

## 1. Estructura de productos en la app GBM

| Producto | Qué es | Mercado | Moneda | Fracciones | Mínimo | Fuente |
|---|---|---|---|---|---|---|
| Trading MX | Cuenta de intermediación. Acciones BMV/BIVA, FIBRAs, ETFs locales y **SIC** | BMV/BIVA (el SIC incluido) | MXN | **No**: solo títulos completos en el SIC | Hasta 10 cuentas desde 100 MXN | [5][36] |
| Trading USA | Acceso directo a NYSE/Nasdaq. Acciones, ETFs y ADRs | EUA vía DriveWealth | **USD** (dolarizada desde el 31-mar-2025) | **Sí** | Desde 1 USD | [4][5][6][28] |
| Smart Cash | Liquidez invertida en reportos a 1 día hábil | Dinero | MXN | n/a | 100 MXN | [19][41] |
| Smart Cash Dólares | Fondo GBMDOL en instrumentos en USD | Dinero USD | USD | n/a | 100 MXN | [7][1] |
| Bonos/CETES | CETES, Bonos M, Udibonos | Deuda gubernamental | MXN | n/a | La ruta que documenta GBM para "invertir en CETES" es Smart Cash, desde 100 MXN [23][53]. GBM también ofrece "Deuda gubernamental" como cuenta gestionada, sin corretaje [54]. **Compra directa de un CETE a plazo desde la app: no verificado** | [23][53][54] |
| Fondos GBM | Fondos de renta fija y variable | Varios | MXN/USD | n/a | Varía | [1] |

[H] Trading USA dejó de operar en pesos. El dinero se pasa de Smart Cash a Trading USA para comprar dólares y regresa a Smart Cash para venderlos. **La liquidación de dólares toma 1 día hábil** [6].
[H] Tipo de cambio de referencia que declara GBM para Smart Cash Dólares: "Valmer Spot 48 h". En depósitos y transferencias se aplica "el tipo de cambio vigente al momento de la operación" [7]. No se publica un spread explícito.

---

## 2. Comisiones

### 2.1 Tabla oficial de corretaje (Trading MX: BMV, BIVA, SIC)

| Monto operado (promedio de los últimos 3 meses) | Comisión | Con IVA 16% | Fuente |
|---|---|---|---|
| De 1,000 a 1,000,000 MXN | 0.25% | **0.29%** | [1][2] |
| De 1,000,001 a 3,000,000 MXN | 0.20% | 0.232% | [1][2] |
| De 3,000,001 a 5,000,000 MXN | 0.15% | 0.174% | [1][2] |
| De 5,000,001 a 10,000,000 MXN | 0.125% | 0.145% | [1][2] |
| Más de 10,000,000 MXN | 0.10% | 0.116% | [1][2] |

- [H] La Guía de Servicios (versión V1025, publicada en feb-2026) dice: "En cada estrategia de Trading México, la única comisión que se cobra es la de corretaje y se aplica cada vez que realizas una operación de compra o venta". También dice que "el uso de la plataforma no tiene costo" y que "A las comisiones que cobre la Casa de Bolsa por sus servicios, se le aumentará el Impuesto al Valor Agregado" [2].
- [H] Los topes máximos de la Guía son 0.75% en ejecución general de renta variable y 0.25% "a través de las plataformas GBM y GBM+" [2].
- [H] **Mínimo por operación:** la Guía no menciona un mínimo en pesos [2]. Algunos resúmenes secundarios citan "20 MXN por operación" **(no verificado; no lo encontré en la fuente oficial)**.
- [H] **Planes sin comisión o por suscripción:** no hay ninguno en la FAQ oficial ni en la Guía [1][2]. Un resumen de búsqueda mencionó un "plan Smart 0.20%" **(no verificado)**. La nota de 2022 sobre "0% en fracciones" de Trading Global [11] **ya no aplica**: la FAQ vigente de Trading USA dice 0.25% por compra o venta [3].
- [H] Tanto la Guía [2] como la FAQ [1] miden el escalón por el "monto operado promedio de los últimos 3 meses" (algunos resúmenes secundarios dicen "inversión total", lo cual es incorrecto). [I] Con 20,000 MXN de capital la cuenta queda en el escalón de 0.25%: habría que operar en promedio más de 1,000,000 MXN para bajar al siguiente.

### 2.2 Otras comisiones relevantes

| Concepto | Costo | Fuente |
|---|---|---|
| Trading USA, compra o venta | 0.25% (el documento no aclara si lleva IVA) | [3] |
| Conversión MXN↔USD (Smart Cash ↔ Trading USA) | Spread no publicado. Tipo de referencia: Valmer Spot 48 h | [6][7] (spread: no verificado) |
| Smart Cash | Sin comisión | [1] |
| Smart Cash Dólares | 1.5% anual + IVA, descontado diario | [1] |
| Fondos GBM | Arancel anual de 1% a 2.75%, descontado diario | [1] |
| Fondos de renta fija | Sin corretaje (sí llevan arancel) | [1] |
| CETES/bonos gubernamentales | Sin comisión; corporativos 1% | resumen de búsqueda (no verificado) |
| W-8BEN para Trading MX/SIC | 75 USD + IVA, trámite vía Indeval, confirmación en máx. 72 h | [45] (FAQ oficial "¿Cómo registro el W8-BEN para Trading MX y SIC?"), [24][25] |
| W-8BEN para Trading USA | Gratis desde la app | [24] |
| Crédito de margen (tope) | Hasta TIIE + 10 puntos anual | [2] |
| Préstamo de valores (prestatario) | Prima base de hasta 500 MXN semanales | [2] |
| Futuros y opciones MexDer | Tabla "Cuenta Global 4T25" por vuelta sencilla | [2] |

### 2.3 El spread del SIC y la conversión cambiaria implícita

- [H] En el SIC los valores cotizan y se liquidan en pesos [36]. Una orden a mercado del SIC se ingresa "sobre los precios del mercado de origen" con una banda de protección de **~0.20% sobre la mejor postura** [10].
- [H] GBM puede ejecutar SIC como "operación por excepción": un cruce vía algoritmo cuando el precio del mercado de origen se aparta de los corros locales [10].
- [I] El precio en MXN del SIC equivale al precio en EUA por el tipo de cambio que usa el formador o el intermediario al cruzar. **La diferencia contra el spot interbancario no se publica.** Ese es el costo cambiario implícito y **no está verificado**.
- [R] Antes de la primera operación en el SIC, compara el precio que muestra la app contra (precio en NYSE/Nasdaq × USD/MXN spot) en el mismo minuto. Hazlo en 3 o 4 tickers y registra la diferencia en la bitácora. Si pasa de 0.3%, compensa usar Trading USA con una sola conversión por temporada.
- [H] Un resumen de búsqueda atribuyó a Trading USA un "spread cambiario de 3%". **No encontré la fuente primaria. Probablemente describe el esquema anterior a la dolarización de marzo de 2025 (no verificado).**

---

## 3. Costo real de ida y vuelta (Trading MX: BMV y SIC)

La fórmula es: comisión por lado = monto × 0.25% × 1.16, más el spread o slippage de ida y vuelta. El spread es una **estimación [I]**: 0.10% para ETFs y emisoras muy líquidas, 0.30% para liquidez media y 0.60% para SIC poco operado o en horas de baja liquidez.

| Monto por orden (MXN) | Comisión + IVA por lado | Comisión de ida y vuelta | % del monto | Total con spread 0.10% / 0.30% / 0.60% | % del capital de 20k (spread 0.30%) |
|---|---|---|---|---|---|
| 2,000 | 5.80 | 11.60 | 0.58% | 13.60 / 17.60 / 23.60 | 0.09% |
| 5,000 | 14.50 | 29.00 | 0.58% | 34.00 / 44.00 / 59.00 | 0.22% |
| 10,000 | 29.00 | 58.00 | 0.58% | 68.00 / 88.00 / 118.00 | 0.44% |

**Escenario con el mínimo de 20 MXN + IVA (no verificado):**

| Monto | Por lado | Ida y vuelta | % del monto |
|---|---|---|---|
| 2,000 | 23.20 | 46.40 | **2.32%** |
| 5,000 | 23.20 | 46.40 | 0.93% |
| 10,000 | 29.00 | 58.00 | 0.58% |

[I] Si el mínimo existe, el punto de equilibrio es 20 / 0.25% = **8,000 MXN por orden**. Por debajo de eso el costo porcentual se dispara.
[R] Mira el costo real en el ticket de confirmación de la primera orden y ajusta esta tabla.

**Trading USA (costo de ida y vuelta):** 2 × 0.25% (0.29% si lleva IVA) más la conversión cambiaria. [I] Si conviertes una sola vez al inicio y una al final de la temporada, el spread cambiario s se paga **una vez por temporada**, no en cada operación. En ese caso el costo por operación queda en ~0.50% a 0.58% de ida y vuelta, igual que en MX. Si conviertes en cada operación, se suma 2s: con s = 0.3% el total es ~1.1% a 1.2%, y con s = 1% es ~2.5% a 2.6%.

---

## 4. Tipos de orden

| Tipo | Trading MX (BMV/SIC) | Trading USA | Nota | Fuente |
|---|---|---|---|---|
| Mercado | Sí. Solo emisoras de liquidez media o alta e IPC | Sí | La orden entra con una banda de ~0.20% sobre la mejor postura. Fuera de horario queda en espera hasta la apertura | [8][9][10] |
| Limitada | Sí, con vigencia | Sí, con vigencia | Necesita contrapostura dentro del rango | [8][9] |
| MPL activa / pasiva / con volumen oculto | Sí. Mínimo de 100 títulos (MPVO: 2,000) | No | | [8][10] |
| Stop Market (stop loss) | Sí | **No** | Puede ejecutarse lejos del stop si hay gap | [8] |
| Stop Limitada | Sí | **No** | Protege del gap; puede quedarse sin ejecutar | [8] |
| Trailing Stop | Sí | **No** | Distancia fija o en % | [8] |
| OCA (take profit + stop) / OTA | Sí | **No** | "Posturas Cancela Postura (PCP), también conocida como stop-loss / take-profit" | [8][10] |
| Al cierre / precio promedio del día | Sí, vía mesa, con ejecución no garantizada | No | | [10] |
| Fracciones | No | Sí | En 2022 las fracciones solo aceptaban órdenes a mercado (no verificado para 2026) | [11] |

- [H] **Vigencia:** si no se indica, dura un día. **No puede pasar de 30 días.** Las órdenes no ejecutadas se reingresan cada día hábil con folio nuevo [10].
- [H] **Recepción:** las plataformas reciben órdenes 24/7. Fuera de sesión se registran al inicio de la siguiente [10].
- [H] **Filtros de precio (sin posibilidad de cambiarlos desde la plataforma):** si compras arriba o vendes abajo del último hecho, el filtro salta con una variación de 3% en emisoras locales y 5% en SIC. Si compras abajo o vendes arriba, salta con 6% en locales y 10% en SIC [10]. El folleto los define para "la plataforma GBMHomebroker" (nombre anterior); [I] que apliquen igual en la app GBM actual es inferencia (no verificado). Vía apoderado (mesa) los filtros son más amplios (hasta 10% y 20% en SIC) [10]. Esto limita las órdenes limitadas "agresivas" en mercados rápidos.
- [H] El sistema de la BMV contempla de forma nativa la "Postura Activada al Nivel" y la PCP (limitada + activada al nivel) (manual operativo BMV, visto en resumen de búsqueda [52]; parcialmente verificado). Pero las órdenes de GBM con vigencia mayor a un día se cancelan al cierre y **GBM las reingresa cada día hábil con folio nuevo** [10].

---

## 5. Horarios y calendario de la temporada (octubre 2026 a abril 2027)

| Periodo | BMV/BIVA/SIC (hora CDMX) | Trading USA (hora CDMX) | Fuente |
|---|---|---|---|
| 9-mar-2026 a 30-oct-2026 | **7:30–14:00** | 7:00–14:00 según GBM (NYSE abre a las 7:30) | [12][13] |
| Desde el mar 3-nov-2026 | **8:30–15:00** | [I] ~8:30–15:00 (NYSE 9:30–16:00 ET en horario estándar) | [13][14] |
| Desde ~16-mar-2027 | [I] 7:30–14:00 (EUA adelanta el reloj el 14-mar-2027; el lun 15-mar es inhábil en México) | [I] 7:30–14:00 | inferencia sobre la regla anual [13][14] |

- [H] México ya no cambia de horario. La BMV mueve su sesión para mantenerse alineada con Wall Street [14].
- [H] **Inhábiles en México (4T-2026):** lun 2-nov (Día de Muertos, disposición de Banxico), lun 16-nov (Revolución) y vie 25-dic. El 24 y el 31 de diciembre hay horario reducido en bancos [38].
- [I] **Inhábiles probables del 1T-2027:** 1-ene, lun 1-feb (Constitución), lun 15-mar (Juárez), jue 25 y vie 26 de marzo (Semana Santa). Fechas calculadas con la regla de "lunes", **no verificadas contra el calendario oficial de CNBV 2027**. En EUA: Thanksgiving 26-nov-2026, 25-dic, 1-ene, MLK 18-ene-2027, Presidents Day 15-feb-2027 y Good Friday 26-mar-2027 (no verificado).
- [I] Cuando la BMV abre y NYSE está cerrado (por ejemplo, Thanksgiving), el SIC opera con muy poca liquidez. Conviene evitar órdenes a mercado en SIC esos días.

### Liquidación

- [H] **México: T+1 desde el 27-may-2024.** Antes era T+2 (desde 2017) [15].
- [H] EUA también liquida en T+1 (alineación citada en [15]).
- [H] Los dólares en Trading USA ↔ Smart Cash liquidan en 1 día hábil [6].
- [H] Retiros de Smart Cash y Trading MX: se solicitan en días hábiles de 7:30 a 13:30 y llegan "en minutos". Fuera de ese horario pasan al siguiente día hábil. Smart Cash Dólares tarda 2 o 3 días hábiles [20].
- [H] **Regla de permanencia:** los depósitos a Smart Cash se invierten en reportos a 1 día hábil. Si depositas antes de las 13:30, puedes retirar al día hábil siguiente; si depositas después, a los 2 días hábiles. Ese dinero **sí se puede usar para invertir** mientras tanto [19].
- [H] Depósitos por SPEI a la CLABE única de GBM: **"en cualquier momento para que el efectivo llegue en minutos"** según la FAQ oficial [48] (la versión anterior de este documento decía "lunes a viernes de 06:00 a 18:00"; eso no se sostiene). El alta de una cuenta bancaria para retiros tarda hasta 48 h en validarse (resumen de búsqueda del centro de ayuda de GBM, **parcialmente verificado**).

---

## 6. Apalancamiento, corto y derivados

| Herramienta | Disponible para persona física | Condiciones | Fuente |
|---|---|---|---|
| Margen intradía | Sí, bajo contrato y a solicitud (correo a plus@gbm.com) | Solo intradía; la posición se cierra el mismo día. Un resumen de búsqueda menciona hasta 2.5 veces lo que se tiene en acciones y hasta 3 veces el efectivo, solo en ciertas emisoras y sin costo si se devuelve a tiempo (no verificado) | [39] (parcialmente verificado: la página oficial dio 404 al consultarla, y las páginas de GBM Academy sobre margen dieron 503 el 2026-09-25) |
| Venta en corto | Sí, con margen intradía activado | **Mínimo 10,000 MXN.** Solo emisoras que GBM selecciona. Garantía de 2 MXN por cada 1 MXN vendido | [39] (parcialmente verificado) |
| Crédito de margen (overnight) | Aparece en la Guía | Hasta TIIE + 10 | [2]. Si está disponible en la app para retail: no verificado |
| Préstamo de valores (como prestamista) | Sí, en Trading USA ("genera intereses mensuales") | Reparto del ingreso: 50% DriveWealth, 30% GBM y **20% el cliente**. Garantía del 100%; se puede vender en cualquier momento | [5] |
| Futuros/opciones MexDer | En la Guía, con tabla de comisiones 4T25 | Vía cuenta global o mesa, no como función estándar de la app | [2], [40] (no verificado) |
| ETFs apalancados en SIC | **TQQQ (ISIN US74347X8314), SOXL (US25459W4583) y SPXL (US25459W8626) están listados como TRACs extranjeros con estatus ACTIVA en la BMV** | Si GBM permite comprarlos desde la app y con qué perfil: **no verificado**. UPRO, QLD y SSO: listado en la BMV no verificado. La frase "los ETFs adquiridos en el SIC no podrán ser ni sintéticos ni apalancados" que circula en búsquedas viene del prospecto de un fondo de inversión GBM, no es una regla para personas físicas | [35][43][44] |
| Regla PDT en Trading USA | En 2022 GBM la limitaba a 3 day trades cada 5 días hábiles, con exención arriba de 25,000 USD [11]. La FAQ vigente de GBM "¿Qué es un day trade?" repite el límite de 3 en 5 días y dice que la app muestra un contador (resumen de búsqueda; la URL dio 404 el 2026-09-25, parcialmente verificado) [51] | FINRA eliminó el requisito de 25k con vigencia al 4-jun-2026. Los brokers tienen hasta el 20-oct-2027 para implementarlo, y solo aplica a cuentas de margen. Si GBM/DriveWealth ya lo cambió: **no verificado** | [11][34][51] |

[I] Para la cuenta arena, el apalancamiento práctico que se puede sostener de un día para otro son los **ETFs apalancados vía SIC**, si GBM los habilita, o vía Trading USA, sin stops. El margen de GBM es solo intradía.

---

## 7. Liquidez, CETES y fondos

| Instrumento | Tasa o costo | Fecha | Fuente |
|---|---|---|---|
| Tasa objetivo de Banxico | 6.50% (sin cambio, decisión unánime) | 24-sep-2026 | [21] |
| CETE 28 / 91 / 182 / 364 | 6.15% / 6.59% / 6.91% / 7.24% (brutas). El CETE 28 bajó 10 pb desde 6.25% | subasta del 22-sep-2026 | [22][50] (cetes.app cita SIE Banxico; Imagen Radio confirma el 6.15%; no lo verifiqué directamente en Banxico) |
| Smart Cash (<300 mil MXN) | 4.00% anual | verificado al 24-sep-2026 | [17][18] |
| Smart Cash (rango total) | 4.00%–4.75% según inversión total | vigente | [17] |
| Retención de ISR sobre intereses | 0.90% anual sobre el capital (LIF 2026, art. 24) | 2026 | [29] |

- [I] El diferencial CETE 28 − Smart Cash es de ~2.15 pp. Para dinero que vaya a quedarse quieto ≥28 días, el CETE rinde más que Smart Cash. Para dinero en espera entre operaciones, Smart Cash es la opción líquida.
- [H] **Advertencia:** no encontré en fuentes de GBM la compra directa de un CETE a plazo desde la app. GBM presenta Smart Cash como su vía para "invertir en CETES" [23][53]. Cetesdirecto es externo y exigiría sacar dinero de la cuenta arena. Que el CETE 28 esté disponible dentro de la cuenta: **no verificado**.
- [I] Neto de la retención de 0.90%, Smart Cash rinde ~3.1%, o sea ~0.26% al mes. Frente a un rival que juega a ganar, la liquidez ociosa casi no aporta al marcador.

---

## 8. Impuestos (persona física residente en México)

| Concepto | Tratamiento | Quién lo retiene o declara | Fuente |
|---|---|---|---|
| Ganancia por venta en BMV y SIC | ISR definitivo de 10% sobre la ganancia neta del año (art. 129 LISR) | **Sin retención en la venta.** Se paga en la declaración anual con la constancia de GBM | [26] |
| Ganancia en Trading USA | **Tasa no verificada.** [28] trata solo de dividendos y no menciona 10% sobre ganancias; [42] redirige a una página genérica. Que aplique el 10% del art. 129 sin intermediario mexicano: no verificado | Autodeclaración. GBM no emite CFDI por Trading USA; DriveWealth entrega la forma 1042-S "solo como guía" [27][28] | [28], [42] (no verificado) |
| Dividendos de emisoras mexicanas | Retención de 10% (utilidades desde 2014) | Emisora o intermediario | [27] |
| Dividendos SIC (fuente EUA) | 30% en EUA (10% con W-8BEN vigente) y después 10% en México sobre el neto | GBM | [27] |
| Dividendos Trading USA | 30% (10% con W-8BEN), después 10% en México | DriveWealth / GBM | [28] |
| Intereses (Smart Cash, CETES) | Retención de 0.90% anual sobre el capital | GBM | [29] |
| Compensación de pérdidas bursátiles | Las pérdidas del art. 129 se compensan contra ganancias del mismo tipo (plazo de años siguientes: **no verificado**; el portal del SAT devolvió 403) | Declaración anual | — |

- [I] Para el marcador (TWR en MXN), **el ISR de 10% sobre ganancias no afecta a la cuenta durante la temporada**, porque se paga en la declaración anual y no se descuenta de la cuenta. Las retenciones de dividendos sí restan. Por eso conviene preferir instrumentos de dividendo bajo o nulo (crecimiento, ETFs apalancados).
- [I] **El W-8BEN del SIC (75 USD + IVA, ~1,500 MXN a ~17.4 MXN/USD) cuesta ~7.6% de la cuenta de 20k.** Nunca se paga solo con los ahorros en dividendos de una cuenta de este tamaño. En Trading USA es gratis [24].

---

## 9. Protección regulatoria y riesgo de contraparte

- [H] El seguro del IPAB cubre depósitos bancarios hasta 400 mil UDIS y "No garantiza [...] las inversiones en fondos de inversión, aseguradoras y casas de bolsa" [30].
- [H] En Trading MX, los valores se custodian en S.D. Indeval a nombre del cliente [36]. [I] Si la casa de bolsa quiebra, los valores no forman parte de su patrimonio (el principio de segregación lo describen fuentes secundarias; el texto legal no lo verifiqué).
- [H] En Trading USA la custodia la lleva DriveWealth (EUA) [28][36]. DriveWealth, LLC es broker-dealer "member of FINRA and SIPC" y el 5-nov-2025 anunció cobertura Excess SIPC para "DriveWealth partners and their customers" de hasta 49 MUSD en valores y 1 MUSD en efectivo por cuenta [49]. Si la cobertura SIPC aplica a los clientes mexicanos de GBM y en qué términos: **no verificado**.
- [H] GBM aparece como casa de bolsa supervisada por la CNBV [25].

---

## 10. Caídas e incidentes operativos conocidos

| Fecha | Evento | Duración o efecto | Fuente |
|---|---|---|---|
| 26-jun-2024 | Intermitencias en GBM+ y GBM App | Nota publicada a las 11:18 y resuelta a las 12:30 CDMX; la hora de inicio no se reporta (≥ ~1 h) | [32] |
| 19-jul-2024 | Falla global de CrowdStrike/Microsoft afecta a GBM | Intermitencias por "falla global de un proveedor" | [33] |
| dic-2024 (nota del 16-dic) | Caída de la app móvil en horario de mercado, con "internal server error" | **Segunda falla en menos de 5 días** | [31] |
| **7-abr-2025** (el lunes que cita la nota del 8-abr) | "Lunes negro" por aranceles: falla de la plataforma GBM | **Más de 5 horas sin poder comprar ni vender** en una de las sesiones más volátiles en años | [46] |
| 20-oct-2025 | Caída global de AWS: "Mifel y GBM tuvieron reportes de intermitencia" | Intermitencias | [47] |
| 2026 | No encontré notas de prensa sobre caídas | — | búsquedas del 2026-09-25 |

- [I] El riesgo real para la cuenta arena es **no poder cerrar o ajustar una posición apalancada durante un movimiento fuerte**.
- [I] El 7-abr-2025 muestra que la falla más larga coincidió con el día de más volatilidad. Es el peor caso para una posición en ETF 3x.
- [R] Toda posición en Trading MX/SIC lleva un **stop o una OCA registrados en el sistema desde la entrada**, porque no dependen de que la app esté disponible en ese momento. Matiz: la BMV admite posturas activadas al nivel y PCP [52], pero una orden de varios días la reingresa GBM cada mañana [10], así que depende de los sistemas internos de GBM. **Que un stop ya registrado se haya ejecutado durante la caída del 7-abr-2025: no verificado.** En Trading USA no hay stops, así que ahí no se meten posiciones apalancadas que requieran un stop estricto. Respaldo telefónico de GBM: 55 5480 5846; WhatsApp: 55 2690 5840 [6].

---

## Implicaciones para la cuenta arena (20,000 MXN)

### A. Matemática de costos

1. **Costo fijo por vuelta (Trading MX): 0.58% del monto**, más un spread estimado de 0.10% a 0.60%. Total de **~0.7% a 1.2%** por operación completa [I, sobre 1 y 2].
2. **Costo de rotación sobre el capital:**

| Rotaciones completas de la cuenta al mes | Costo mensual (solo comisión) | Costo en la temporada de 6 meses |
|---|---|---|
| 0.5 | 58 MXN (0.29%) | 1.7% |
| **1.0** | **116 MXN (0.58%)** | **3.5%** |
| 1.5 | 174 MXN (0.87%) | 5.2% |
| 2.0 | 232 MXN (1.16%) | 7.0% |
| 3.0 | 348 MXN (1.74%) | 10.4% |

3. **El parámetro provisional `operaciones_max_mes: 8`** equivale a 8 vueltas de 10,000 MXN al mes. **Solo en comisiones cuesta 2.32% al mes y ~13.9% en la temporada.** Con 8 vueltas de 5,000 MXN cuesta 1.16% al mes y ~7% en la temporada. [R] Hay que redefinirlo como **presupuesto de rotación ≤ 1.0–1.5× el capital al mes**, que da ~4 a 6 vueltas de 5,000 o ~2 a 3 de 10,000. El costo total de la temporada queda en **≤ 3.5%–5.2%** (solo comisión).
4. **Edge mínimo por operación:** con un costo de 0.68% a 1.18%, un objetivo de movimiento de 2% pierde de 34% a 59% del edge en costos; uno de 5%, de 14% a 24%; y uno de 10%, de 7% a 12%. [R] **Solo se entra en operaciones con un movimiento esperado ≥ 5%** (swing de días a semanas). El scalping o intradía con 20k en GBM tiene un edge negativo neto de costos.
5. **Tamaño mínimo de posición:** sin comisión mínima, el costo porcentual no depende del tamaño. [R] Si se confirma un mínimo de 20 MXN, **ninguna orden va por debajo de 8,000 MXN**. Mientras no se verifique, conviene que las órdenes sean de **≥ 5,000 MXN**, con lo que hay 2 a 4 posiciones simultáneas como máximo.
6. **Granularidad del SIC:** solo títulos completos. [I] Un ETF de ~690 USD (~12,000 MXN) ocuparía el 60% de la cuenta en un solo título [36]. [R] En el SIC hay que preferir tickers con precio por título ≤ 5,000 MXN, o usar Trading USA con fracciones para los tickers caros.

### B. Elección de ruta: Trading MX/SIC contra Trading USA

| Criterio | Trading MX/SIC | Trading USA |
|---|---|---|
| Comisión por lado | 0.29% con IVA | 0.25% (IVA no confirmado) |
| Conversión cambiaria | Implícita en el precio del SIC, en cada operación (no verificado) | Explícita; se puede hacer una sola vez por temporada |
| Stops, OCA, trailing | **Sí** | **No** |
| Fracciones | No | Sí |
| ETFs apalancados | TQQQ, SOXL y SPXL listados y activos en el SIC [35][43][44]; habilitación en GBM sin verificar | Sin verificar |
| Riesgo operativo si la app se cae | Menor: el stop ya está registrado (depende de los sistemas de GBM, no de la app [10][52]) | **Alto: no hay stop** |

[R] **Ruta por defecto: Trading MX/SIC con OCA o stop limitada en cada entrada.** Trading USA solo para posiciones sin apalancamiento en tickers caros o que no están en el SIC, con **una sola conversión** de MXN a USD al inicio de la temporada.

### C. Operativa

- [R] **No hay que depositar ni retirar durante la temporada.** Cada flujo complica el TWR, y la regla de permanencia y los horarios de retiro agregan fricción.
- [R] **Horarios de ejecución:** evitar los primeros 15 minutos y el día hábil mexicano en que NYSE está cerrado (SIC sin liquidez). **Recalibrar todas las rutinas el mar 3-nov-2026**, cuando el horario cambia a 8:30–15:00.
- [R] Las órdenes limitadas en el SIC con precio más de 5% arriba del último hecho van a rebotar por el filtro de GBM [10]. Hay que usar precios realistas.
- [R] La vigencia máxima de 30 días obliga a **reponer los stops de largo plazo cada mes**. Conviene agregarlo a la rutina mensual.
- [R] La liquidez ociosa va en Smart Cash (disponible de inmediato para invertir [19]). Solo si se prevé ≥ 28 días sin operar conviene un CETE 28 (6.15% contra 4.00%), **siempre que la app permita comprarlo dentro de la cuenta (no verificado; ver sección 7)**.
- [R] **No tramitar el W-8BEN del SIC** (su costo es ~7.6% de la cuenta).

### D. Checklist que el dueño debe verificar en la app antes de fondear

1. Buscar TQQQ, SOXL, UPRO/SPXL, QLD y SSO en Trading MX (SIC): ¿se pueden comprar? ¿Pide algún perfil o carta de riesgo? (TQQQ, SOXL y SPXL ya están confirmados como listados y activos en la BMV [35][43][44]; lo que falta es la habilitación en GBM y la liquidez real del libro en pesos.)
2. Hacer una orden de prueba chica en el SIC y anotar la comisión cobrada, el IVA y si aplica un mínimo de 20 MXN.
3. En Trading USA: cotizar la compra de 100 USD y comparar el tipo de cambio que muestra contra el spot del momento. Así se obtiene el spread s real.
4. Revisar si el SIC acepta Stop Limitada y OCA para tickers extranjeros. La FAQ no distingue BMV de SIC [8].
5. Revisar si Trading USA muestra un contador de day trades (PDT).
6. Revisar si la app permite comprar un CETE 28 directo dentro de la cuenta, o si la única vía es Smart Cash.
7. En la primera operación de Trading USA, revisar si la comisión de 0.25% lleva IVA.

---

## Fuentes

Todas se consultaron el 2026-09-25, salvo que se indique otra fecha.

1. GBM, Centro de ayuda: "¿Qué comisiones cobran al invertir en GBM?". https://gbm.com/faqs/que-comisiones-cobran-al-invertir-en-gbm/
2. GBM, *Guía de Servicios de Inversión*, versión V1025 (PDF publicado en feb-2026), secciones "Comisiones" y "Tabla de Comisiones 4T25 Cuenta Global". https://global.gbm.com/wp-content/uploads/2026/02/12141701/Guia-de-Servicios-GBM_V-1025.pdf
3. GBM, Centro de ayuda: "¿Existe alguna comisión por invertir en Trading USA?". https://gbm.com/faqs/existe-alguna-comision-por-invertir-en-trading-usa/
4. GBM, Centro de ayuda: "¿Qué es Trading USA?". https://gbm.com/faqs/que-es-trading-usa/
5. GBM, "Trading en México y Estados Unidos". https://gbm.com/trading/
6. GBM App, release "Trading USA, ahora en dólares" (31-mar-2025). https://about.appgbm.com/releases/experiencia-en-dolares-en-trading-usa/
7. GBM, Centro de ayuda: "¿Qué tipo de cambio utiliza Smart Cash Dólares?". https://gbm.com/faqs/que-tipo-de-cambio-utiliza-smart-cash-dolares/
8. GBM, Centro de ayuda: "¿Qué tipos de órdenes existen en Trading MX?". https://gbm.com/faqs/que-tipos-de-ordenes-existen-en-trading-mx/
9. GBM, Centro de ayuda: "¿Con qué tipo de órdenes existen en Trading USA?". https://gbm.com/faqs/con-que-tipo-de-ordenes-existen-en-trading-usa/
10. GBM, *Folleto Informativo del Sistema de Recepción, Registro, Ejecución de Órdenes y Asignación de Operaciones* (PDF de nov-2024). https://gbm.com/wp-content/uploads/2024/11/GBM-Folleto-Informativo.pdf
11. GBM Academy, "Trading Global: ¿Qué es y cómo empezar?" (16-nov-2022). https://gbm.com/media/the-academy/trading-global-que-es-y-como-empezar/
12. GBM, Centro de ayuda: "¿Cuáles son los horarios para comprar y vender en Market?". https://gbm.com/faqs/cuales-son-los-horarios-para-comprar-y-vender-en-market/
13. Axis Negocios, "BMV adelantará inicio de operación desde el 9 de marzo por cambio de horario en EUA" (04-mar-2026). https://www.axisnegocios.com/breves.phtml?id=146701
14. Expansión, "La Bolsa Mexicana de Valores deja atrás su 'horario de verano'" (31-oct-2025). https://expansion.mx/mercados/2025/10/31/bolsa-mexicana-regresa-horario-apertura-cierre
15. Expansión, "Grupo BMV implementa el ciclo de liquidación T+1" (27-may-2024). https://expansion.mx/mercados/2024/05/27/grupo-bolsa-mexicana-valores-liquidacion-t-1
16. Blog BMV, "Revoluciona el comercio de acciones: el salto en México a la liquidación T+1" (visto en el listado de búsqueda). https://blog.bmv.com.mx/revoluciona-el-comercio-de-acciones-el-salto-en-mexico-a-la-liquidacion-t1/
17. GBM, Centro de ayuda: "¿Cuál es la tasa de rendimiento de Smart Cash?". https://gbm.com/faqs/cual-es-la-tasa-de-rendimiento-de-smart-cash/
18. De Cero al Infinito, "GBM Smart Cash vs Fintual" (dato verificado por el sitio el 24-sep-2026). https://deceroalinfinito.com/comparativas/gbm-smart-cash-vs-fintual
19. GBM, Centro de ayuda: "¿Por qué no puedo retirar el dinero que acabo de depositar a Smart Cash?". https://gbm.com/faqs/por-que-no-puedo-retirar-el-dinero-que-acabo-de-depositar-a-smart-cash/
20. GBM, Centro de ayuda: "¿Cuál es el horario para retirar mi dinero en GBM?". https://gbm.com/faqs/cual-es-el-horario-para-retirar-mi-dinero-en-gbm-en-cuanto-tiempo-se-refleja/
21. Expansión, "Banxico mantiene la tasa de interés de referencia en 6.5%, por cuarta vez consecutiva" (24-sep-2026). https://expansion.mx/economia/2026/09/24/banxico-tasa-de-interes-de-referencia-6-5-septiembre
22. cetes.app, "Tasas de CETES hoy" (subasta del 22-sep-2026, cita SIE Banxico). https://cetes.app/cetes-hoy
23. GBM Academy, "CETES: ¿Qué son, para qué sirven y cómo invertir en ellos?" (15-may-2024). https://gbm.com/media/the-academy/cetes-que-son-para-que-sirven-y-como-invertir-en-ellos-2/
24. GBM, Centro de ayuda: "¿Qué es y cómo funciona el W-8BEN para Trading MX y SIC?". https://gbm.com/faqs/que-es-y-como-funciona-el-w-8ben-para-trading-mx-y-sic/
25. Finantres, "Comisiones en GBM: análisis real de costos en México" (actualizado el 16-sep-2026). https://finantres.mx/comisiones-gbm/
26. GBM, Centro de ayuda: "¿Cómo funcionan los impuestos por las acciones de empresas extranjeras en el SIC?". https://gbm.com/faqs/como-funcionan-los-impuestos-por-las-acciones-de-empresas-extranjeras-en-el-sic/
27. GBM, Centro de ayuda: "¿Cómo funcionan los impuestos sobre los dividendos en Trading MX?". https://gbm.com/faqs/como-funcionan-los-impuestos-sobre-los-dividendos-en-trading-mx/
28. GBM, Centro de ayuda: "¿Cómo funcionan los impuestos por dividendos en Trading USA?". https://gbm.com/faqs/como-funcionan-los-impuestos-por-dividendos-en-trading-usa/
29. AMCP, "Puntos relevantes de la Ley de Ingresos de la Federación para el ejercicio fiscal 2026" (art. 24 LIF 2026). https://amcpdf.org.mx/puntos-relevantes-de-la-ley-de-ingresos-de-la-federacion-para-el-ejercicio-fiscal-2026/
30. CNBV, "IPAB, Seguro de Depósito". https://www.gob.mx/cnbv/acciones-y-programas/ipab-seguro-de-deposito
31. El CEO, "Usuarios de GBM reportan caída de aplicación móvil" (16-dic-2024). https://elceo.com/mercados/usuarios-de-gbm-reportan-caida-de-aplicacion-movil/
32. Investing.com México, "¿Eres usuario de GBM y no puedes entrar a la plataforma?" (26-jun-2024). https://mx.investing.com/news/stock-market-news/eres-usuario-de-gbm-y-no-puedes-entrar-a-la-plataforma-aqui-la-explicacion-2814358
33. SDP Noticias, "GBM advierte de intermitencias en inversiones por falla en CrowdStrike y Microsoft" (19-jul-2024; texto consultado el 2026-09-25). https://www.sdpnoticias.com/negocios/falla-en-crowdstrike-y-microsoft-afecta-inversiones-en-gbm/
34. FINRA, Regulatory Notice 26-10 (aprobación de la SEC el 14-abr-2026; vigencia 4-jun-2026; implementación hasta 20-oct-2027). https://www.finra.org/rules-guidance/notices/26-10
35. Grupo BMV, estadísticas de la emisora TQQQ * (ProShares UltraPro QQQ, TRAC extranjero, estatus ACTIVA). https://www.bmv.com.mx/es/emisoras/estadisticas/TQQQ%20*-35397
36. Asesores Inversión, "ETFs en pesos o en dólares desde México: SIC vs. cuenta en dólares" (jul-2026). https://asesoresinversion.com/academia/mercado-accionario/comprar-etf-pesos-o-dolares-mexico/
37. Finantres, "¿Se puede hacer trading en GBM? Pros y contras reales" (actualizado el 16-sep-2026). https://finantres.mx/trading-gbm/
38. Calendario de México, "Calendario bancario 2026: días inhábiles CNBV". https://calendariodemexico.com/calendario-bancario-2026/
39. GBM, Centro de ayuda: "¿Cómo funcionan las ventas en corto y margen intradía?". Contenido tomado del resumen de búsqueda; la URL devolvió 404 al consultarla. https://gbm.com/faqs/como-funcionan-las-ventas-en-corto-y-margen-intradia/
40. Finantres, "¿Se puede operar con opciones con GBM en México?" (visto en el listado de búsqueda). https://finantres.mx/opciones-gbm/
41. Rankia México, "Análisis de GBM+: apertura de cuenta, comisiones y opiniones" (10-nov-2025). https://www.rankia.mx/blog/casas-de-bolsa-de-mexico/7057487-analisis-gbm-apertura-cuenta-comisiones-opiniones
42. GBM App, Centro de ayuda: "Los impuestos por la venta de acciones en Trading USA" (redirige; contenido tomado del resumen de búsqueda). https://about.appgbm.com/faqs/impuestos-por-venta-de-acciones-en-trading-usa/
