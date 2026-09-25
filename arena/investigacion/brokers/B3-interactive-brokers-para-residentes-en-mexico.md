# B3. Interactive Brokers para residentes en México

**Fecha de corte:** 2026-09-25 (todas las fuentes se consultaron ese día)
**Serie:** `arena/investigacion/brokers/`. B1 es la línea base de GBM; B2 cubre las casas de bolsa y apps mexicanas; B3 cubre el bróker extranjero, Interactive Brokers (IBKR).
**Pregunta:** ¿IBKR maximiza el rendimiento **neto** de una cuenta de ~20,000 MXN de persona física residente en México, en una competencia de rendimiento % contra IAs que se quedan en GBM?
**Relación con documentos previos:** no repito A1 (`01-gbm-operativa-y-costos.md`), A2 (`02-universo-sic-bmv-agresivo.md`) ni B1. De B1 tomo la línea base: 0.29% por lado con IVA, desviación cambiaria implícita del SIC de ~0.1%–0.25% por lado, TC de 17.71 MXN/USD del 24-sep-2026 y el patrón de operación de la cuenta (≤1–1.5 rotaciones al mes, órdenes de 5,000 a 10,000 MXN). B1 dejó abierto el régimen fiscal de una venta en NYSE/Nasdaq (§5 y §10 de B1). **Corregido en la verificación del 2026-09-25 (ver §10.2 y "Verificación"):** el criterio normativo 37/ISR/N del SAT (Anexo 7 RMF 2026) pone al 10% del art. 129 las ventas de acciones extranjeras **listadas en el SIC** aunque se vendan con un bróker extranjero. El régimen general solo queda para lo que **no** está en el SIC y, con duda, para los ETFs. `conocimiento/11-mexico` no existe en el repo. `laboratorio/replicas/V05-*` ya tiene resultados (`resultados.json`) y textos legales congelados (`datos/legal/`), y aquí se usaron. Su punto 5 (impuesto sucesorio) se responde con fuente del IRS. B4 (`B4-fiscalidad-comparada-y-otros-brokers-extranjeros.md`) cubre la fiscalidad comparada a fondo.

**Etiquetas:** **[H]** hecho con fuente oficial · **[S]** hecho con fuente solo secundaria · **[C]** cálculo propio sobre datos con fuente · **[I]** inferencia · **[R]** recomendación · **(no verificado)** sin confirmación.

**Nota de método:** las FAQ de IBKR (`ibkrguides.com/kb/...` y `interactivebrokers.com/lib/cstools/faq/#/content/<id>`) se cargan con JavaScript. Las leí con el endpoint público que usa esa misma página (`https://www.interactivebrokers.com/tws.proxy/faq/content`, POST con `question_id`). En las fuentes cito el enlace público de cada FAQ con su id. Las páginas de tarifas de IBKR dieron 403 a WebFetch; las bajé con curl y extraje el texto. El IRS, la LISR y los tarifarios de bancos se leyeron en PDF.

---

## Resumen ejecutivo

1. **[H] Un residente en México sí puede abrir cuenta en IBKR.** México está en la lista oficial de países disponibles [6]. La entidad que lo atiende es **Interactive Brokers LLC** (EUA; SEC/FINRA; SIPC): la confirmación explícita es secundaria [S][33], pero concuerda con que IB LLC publica un cargo de "Deposits – Mexico Only" [3] y con que el depósito SPEI en MXN está disponible en IBKR LLC [4]. IBKR asigna la entidad según el país de residencia legal, y el estado de cuenta la muestra en el encabezado [7]. **IBKR Lite no está disponible: es solo para residentes de EUA** [1][8]. La cuenta sería **IBKR Pro**. **No hay mínimo de apertura** [1][9].
2. **[H] El fondeo es local: SPEI en MXN a una CLABE de 18 dígitos.** Llega en "1 business day or less", se puede operar al llegar y tiene una retención de 3 días hábiles antes de poder retirar [4]. **IBKR no cobra el primer depósito del mes. Desde el segundo cobra 100 MXN** ("Deposits – Mexico Only") [3]. La FAQ de MXN dice "We do not charge for deposits" [4]; es una contradicción entre dos páginas oficiales, y aquí uso la versión conservadora. **No hace falta una transferencia internacional.** SWIFT (10–20 USD + IVA en BBVA, 0 en la app de Santander, 30 USD + IVA en Banorte [S]) y Wise (193.84 MXN por 20,000 MXN, 0.97%, cotización real de hoy) son rutas peores [25]–[29].
3. **[H] Retiros:** en MXN solo por transferencia SWIFT. **Los dos primeros retiros del mes son gratis; después, 100 MXN cada uno** [3][4]. El banco que recibe puede cobrar. El tarifario de BBVA lista "Transferencia – recepción (internacional)" en **30 USD + IVA** por evento, aunque no está verificado que eso aplique a un envío en MXN desde IBKR [26]. **Es el costo de salida más grande del esquema: ~3% de la cuenta si se cobra.**
4. **[H] Conversión MXN→USD:** **0.20 puntos base del monto, con mínimo de 2 USD por orden** [2]. En 20,000 MXN (1,129 USD), el mínimo manda: **0.18%**. **La conversión automática cobra "típicamente" un ajuste de 0.03% al tipo de cambio y no cobra comisión aparte** [2], o sea **~0.34 USD (~6 MXN)**. IBKR dice que no marca sus cotizaciones [2]. El spread adicional de las órdenes chicas ("odd lot" <25,000 USD) solo está en fuentes secundarias (1–3 pips) [S][33].
5. **[H] Comisión de acciones y ETFs de EUA (IBKR Pro):**
   - **Fija (Fixed):** 0.005 USD por acción, **mínimo 1.00 USD por orden**, máximo 1% del monto; se suman las cuotas regulatorias.
   - **Escalonada (Tiered):** 0.0035 USD por acción, **mínimo 0.35 USD**, máximo 1%; se suman bolsa, compensación (0.0002 USD/acción), cuotas de traspaso y cuotas regulatorias [1].
   - Cuotas regulatorias: SEC 0.0000206 × valor vendido; FINRA TAF 0.000195 × acciones vendidas (tope 9.79 USD); CAT 0.000003 × acciones [1]. Retirar liquidez en NYSE cuesta 0.0030 USD/acción [31].
6. **[C] Con órdenes de 5,000 MXN (patrón B1), Tiered cuesta ~0.13% por lado y Fixed ~0.36%, contra 0.39%–0.54% de GBM/SIC** (0.29% de comisión más la desviación implícita, según B1). Con órdenes de 10,000 MXN: **Tiered ~0.07%**, Fixed ~0.18%. **Con órdenes de ≤2,000 MXN, Fixed (0.89%) es peor que GBM y Tiered (0.32%) apenas lo iguala.** Hay que elegir **Tiered**. A 12 rotaciones al año con órdenes de 5,000 MXN: **Tiered ~3.1% del capital, contra ~7.0% de comisión GBM más 2.4%–6.0% de TC implícito** (§3).
7. **[H] Sin custodia, sin cuota de plataforma, sin cuota mensual de actividad y sin inactividad** (excepto cuentas ISA, TBSZ y B3 Brasil, que no aplican) [9]. **Datos en tiempo real gratis para acciones y ETFs de EUA desde Cboe One e IEX, no consolidados.** Para suscribir datos pagados se necesita un capital mínimo de **500 USD**; la cuenta lo cumple [16].
8. **[H] El efectivo no gana intereses en una cuenta de este tamaño.** IBKR paga **0% sobre los primeros 10,000 USD y sobre los primeros 200,000 MXN**. Además, con un valor neto (NAV) menor de 100,000 USD paga una fracción proporcional de la tasa [17]. En GBM el efectivo queda en Smart Cash (A1/B1). [I] Si la estrategia pasa tiempo en efectivo (por ejemplo, timing SMA10), en IBKR habría que estacionarlo en un ETF de T-bills, y cada cambio pagaría comisión.
9. **[H] El universo se abre.** Ya aparece en la tabla maestra (filas 18–28 y 36–38) y en §7:
   - Todo ETF listado en EUA: PRIIPs solo bloquea a clientes minoristas del EEE y del Reino Unido [12]. Que México no quede bloqueado es inferencia [I].
   - Fracciones: todas las cuentas individuales son elegibles, excepto residentes de Israel, RRSP/TFSA de Canadá e IBSJ [11].
   - Opciones: 0.65 USD por contrato, mínimo 1.00 USD por orden. Las compras de calls y puts requieren nivel 2 [13][14].
   - UCITS en LSE y Xetra [1] y BMV (0.1%, mínimo 60 MXN) [1]. Más de 100 tipos de orden [30].
   - **ETFs apalancados o inversos** (TQQQ, SOXL…): requieren el permiso aparte "Complex or Leveraged Exchange Traded Products", que exige requisitos financieros y experiencia que IBKR no publica [36]. **(no verificado)** que se apruebe para esta cuenta.
   - **Contratos de eventos (verificación 2026-09-25):** IBKR da acceso a **Kalshi, CME y ForecastEx** desde la misma cuenta. Kalshi cuesta 0.01 USD por contrato más 0.01 de bolsa; ForecastEx, 0.00 más 0.01. Están disponibles para "eligible clients, 21 years and older, of Interactive Brokers LLC" (y otras 4 entidades). Los contratos sobre elecciones de EUA son solo para residentes de EUA [39]. **[I]** Como la cuenta de un residente mexicano estaría en IB LLC, **podría ser la vía a Kalshi** que el dueño tiene limitada. **(no verificado)** que un residente de México sea "eligible".
   - La regla PDT de 25,000 USD está en retiro: FINRA la eliminó (vigente desde el 4-jun-2026, con implementación gradual hasta el 20-oct-2027), e IBKR dice que ya no la exige. **Pero la página de configuración de IBKR advierte que, durante la transición, las cuentas que sigan sujetas a la regla anterior necesitan 25,000 USD para hacer day trading** [15][37]. No aplica a una cuenta de efectivo.
   - **Cuenta de efectivo (verificación):** solo se puede comprar con **efectivo liquidado**. Vender antes de liquidar lo comprado con fondos no liquidados es *free riding* y deja la cuenta **90 días en "Cash Up Front"** [38]. Una cuenta de margen sí puede operar con fondos no liquidados [38]. **[C/I]** Con liquidación T+1 en EUA [40], cada rotación deja el dinero ~1 día hábil sin invertir si la cuenta es de efectivo.
10. **[H] Protección:** SIPC hasta 500,000 USD (250,000 en efectivo), más una póliza de Lloyd's de hasta 30 M USD por cliente (900,000 en efectivo) con tope agregado de 150 M USD [10]. El efectivo en MXN cuenta como "cash" si está ahí para comprar valores; si se tiene como inversión en divisa, no está protegido [10]. [I] IBKR no está supervisado por la CNBV [S][33].
11. **[H] Impuestos de EUA:**
    - El **W-8BEN es obligatorio al abrir** la cuenta, dura el año de la firma más tres años calendario, y no tiene ningún cargo publicado en Other Fees (§6) [18][3]. En el SIC de GBM cuesta 75 USD + IVA (B1).
    - La tasa del tratado sobre dividendos de EUA para residentes de México es **10%** (5% si es participación directa calificada) [20].
    - El **impuesto sucesorio de EUA** aplica a acciones de sociedades de EUA "even if... registered... in the name of a nominee", con declaración si superan **60,000 USD** [21]. **México no tiene tratado sucesorio con EUA** [22]. [I] Esto aplica igual a acciones de EUA custodiadas vía SIC/Indeval, así que no es un costo exclusivo de IBKR.
12. **[H/I] Impuestos en México. Corregido en la verificación del 2026-09-25.** Depende de qué se compre:
    - IBKR no retiene ISR mexicano ni emite constancia mexicana. Entrega Form 1042-S y un reporte anual de dividendos [19]. El cálculo de la ganancia es tuyo: el art. 129 obliga a quien opera con "entidades financieras extranjeras" a calcular su ganancia y a guardar los estados de cuenta [23].
    - **[H] Acciones extranjeras listadas en el SIC** (NVDA, MSFT, MA, LLY, AVGO, XOM, AMD, según B4): **10% definitivo (art. 129 fr. I)**, "con independencia de que su enajenación no se realice a través de un intermediario del mercado de valores mexicano" (criterio 37/ISR/N, Anexo 7 RMF 2026, DOF 09-01-2026) [35]. **Mismo impuesto que en GBM.** La versión anterior de este punto decía lo contrario y estaba mal.
    - **[I] Acciones o ETFs que no están en el SIC** (IMTM, IDMO, EEMO, PIE…): quedan fuera del art. 129. Entran al régimen general de enajenación (arts. 119–122), **acumulable a tarifa progresiva de hasta 35%** (tarifa 2026: 35% sobre el excedente de 5,107,703.93 MXN; 30% desde 668,840.15 MXN) [23][41]. Además, el art. 126 manda un **pago provisional de 20% sobre el monto total de cada venta dentro de 15 días** cuando el comprador es extranjero [23].
    - **[I] ETFs listados en el SIC y vendidos por IBKR:** hay duda. La fr. II exige que la venta sea en bolsa concesionada, y el criterio 37 solo habla de "acciones" (B4 §1.3). **(no verificado con el SAT)**
    - **[H]** Los **dividendos extranjeros se acumulan y además pagan 10% adicional definitivo a más tardar el día 17 del mes siguiente** (art. 142 fr. V). Con IBKR ese pago lo haces tú [23].
    - **Confirmar con un contador** antes de operar ETFs o acciones que no estén en el SIC.
13. **[R] Veredicto para el frente B3 (actualizado en la verificación):**
    - **Para el TWR del torneo, IBKR Pro Tiered es el bróker de menor fricción y el de mayor universo que encontré.** Baja el costo por rotación de ~0.8%–1.1% (GBM) a ~0.26% con órdenes de 5,000 MXN, y abre ETFs, fracciones y órdenes que el SIC no tiene.
    - **Para el dinero neto del dueño:**
      - **Si se limita a acciones listadas en el SIC, IBKR también gana después de impuestos.** Paga el mismo 10% que en GBM (criterio 37) y tiene menos fricción (§10.4).
      - **La ventaja se reduce o se invierte solo con instrumentos que no están en el SIC** (los ETFs de momentum que "abre" IBKR), por la tarifa progresiva y los pagos provisionales de 20% del monto bruto.
      - En cualquier caso, suma carga administrativa: el cálculo anual propio y el pago mensual del 10% por dividendos.
    - **Operativa:** en cuenta de efectivo solo se compra con efectivo liquidado (T+1). Una cuenta de margen evita esa espera (§7).
    - La decisión final se toma contra B1 y B2.

---

## 1. Tabla maestra (IBKR Pro para persona física residente en México, 2026-09-25)

| # | Concepto | IBKR (residente MX) | GBM (B1) | Tipo | Fuente |
|---|---|---|---|---|---|
| 1 | Disponibilidad para residentes de México | Sí (México en la lista de países) | Sí | H | [6] |
| 2 | Entidad | Interactive Brokers LLC (EUA) | GBM Casa de Bolsa (CNBV) | S / I | [33], [3][4][7] |
| 3 | Plan | **IBKR Pro** (Lite solo para residentes de EUA) | Única | H | [1][8] |
| 4 | Mínimo de apertura | Sin mínimo ("no... account minimums") | Sin mínimo | H | [1][9] |
| 5 | Comisión acciones/ETFs EUA, Fixed | 0.005 USD/acción; mín. 1.00 USD; máx. 1% del valor; + cuotas regulatorias | SIC: 0.25% + IVA = 0.29% | H | [1] |
| 6 | Comisión acciones/ETFs EUA, Tiered (≤300,000 acc./mes) | 0.0035 USD/acción; mín. 0.35 USD; máx. 1% en la tabla (una nota sin número dice "Tiered commissions will be capped at 0.5%"; la nota 6, "Maximum 0.5%", va con la cuota NSCC/DTC); + bolsa, compensación, traspaso, regulatorias | — | H | [1] |
| 7 | Cuotas regulatorias EUA | SEC 0.0000206 × valor vendido; FINRA TAF 0.000195 × acciones vendidas (máx. 9.79 USD); CAT 0.000003 × acciones | Implícitas en el SIC | H | [1] |
| 8 | Compensación y traspaso (Tiered) | NSCC/DTC 0.00020 USD/acción; NYSE 0.000175 × comisión; FINRA 0.00056 × comisión | — | H | [1] |
| 9 | Bolsa (Tiered, ej. NYSE) | Retirar liquidez 0.0030 USD/acción; agregar liquidez: reembolso de hasta 0.0032 | — | H | [31] |
| 10 | IVA mexicano sobre comisiones | IBKR **no aparece** en el padrón de prestadores de servicios digitales del SAT (DOF 25-jul-2025). IBKR dice que aplica IVA/GST "where applicable" | 16% incluido en el 0.29% | H (ausencia) / I | [24][1] |
| 11 | Conversión MXN→USD manual | 0.20 pb × monto; **mín. 2.00 USD** por orden | Implícita en el SIC (~0.1%–0.25%/lado, B1) | H | [2] |
| 12 | Conversión automática | IBKR "typically" suma o resta **0.03%** al TC, sin comisión aparte | — | H | [2] |
| 13 | Depósito en MXN | **SPEI a CLABE de 18 dígitos**, ≤1 día hábil, operable al llegar; retención de 3 días hábiles para retirar | SPEI, en minutos | H | [4] |
| 14 | Costo de depósito (IBKR) | 1er depósito del mes gratis; **siguientes: 100 MXN** ("Deposits – Mexico Only"). La FAQ de MXN dice "We do not charge for deposits" (contradicción) | Sin costo | H | [3][4] |
| 15 | Costo de depósito (banco emisor) | Lo fija el banco ("generally fees do apply"). SPEI por app: 0 en la mayoría [S]. El tarifario BBVA lista SPEI por banca por internet en 5.00 MXN + IVA | 0 | H / S | [4][26] |
| 16 | Retiro en MXN | Solo SWIFT. **2 retiros gratis al mes**; después **100 MXN** (USD: 10 USD por transferencia) | Días hábiles, en minutos | H | [3][4] |
| 17 | Recepción del retiro en el banco | El banco puede cobrar. BBVA: "Transferencia – recepción (internacional)" **30 USD + IVA** (tarifario; aplicación a MXN desde IBKR no verificada) | 0 | H / no verificado | [4][26] |
| 18 | Custodia, plataforma, actividad mensual, inactividad | **Ninguna** (salvo ISA, TBSZ, B3) | Ninguna | H | [9] |
| 19 | Datos de mercado | Tiempo real gratis no consolidado (Cboe One + IEX) en acciones y ETFs de EUA; 100 snapshots gratis al mes; suscripciones con capital ≥500 USD | Incluidos en la app | H | [16] |
| 20 | Intereses sobre efectivo | USD: 0% en los primeros 10,000. MXN: 0% en los primeros 200,000. Prorrateo si NAV <100,000 USD | Smart Cash (A1/B1) | H | [17] |
| 21 | ETFs de EUA | Sí. PRIIPs/KID solo bloquea a minoristas del EEE y del Reino Unido | Solo los listados en el SIC | H / I | [12] |
| 22 | Fracciones | Sí (acciones y ETFs de EUA, Canadá y Europa elegibles). Mismas tarifas, mín. 0.01 USD | SIC: no. Trading USA: sí | H | [11][1] |
| 23 | Opciones de EUA | 0.65 USD/contrato (prima ≥0.10), mín. 1.00 USD/orden, + terceros. Niveles 1–4; compras de calls y puts desde nivel 2; 2,000 USD de capital para posiciones descubiertas | No (Trading MX/SIC) | H | [13][14] |
| 24 | UCITS en LSE (USD) | Tiered 0.05%, mín. 1.70 USD (máx. 39); Fixed 0.05%, mín. 4.00 USD | Algunos UCITS en el SIC (serie N) | H | [1] |
| 25 | UCITS / acciones en Xetra (EUR) | Tiered 0.05%, mín. 1.25 EUR (máx. 29); Fixed 0.05%, mín. 3.00 EUR | — | H | [1] |
| 26 | BMV desde IBKR | Fixed 0.1% del valor, **mín. 60 MXN** (Tiered no disponible) | 0.29%, sin mínimo | H | [1] |
| 27 | Tipos de orden | "over 100 Order Types, Algos and Tools" (stop, trailing, bracket, OCA; también horario nocturno) | Trading MX: stop, OCA, OTA. Trading USA: mercado y limitada | H | [30], B1 |
| 28 | Regla PDT (25,000 USD) | En retiro (FINRA RN 26-10: vigente 4-jun-2026, implementación hasta 20-oct-2027). IBKR dice que ya no la exige, pero su página de configuración dice que las cuentas aún sujetas en la transición necesitan 25,000 USD. Margen y cortos: 2,000 USD | N/A | H | [15][37] |
| 29 | Protección | SIPC 500,000 USD (250,000 en efectivo) + Lloyd's hasta 30 M USD (900,000 en efectivo), tope agregado de 150 M | Fondo de protección de casa de bolsa (ver A1) | H | [10] |
| 30 | W-8BEN | Obligatorio al abrir; vigente el año de firma + 3 años calendario; sin costo publicado | 75 USD + IVA en el SIC | H | [18][3], B1 |
| 31 | Retención de EUA sobre dividendos | 10% por tratado (con W-8BEN); 30% sin él | 30% en el SIC (sin W-8BEN) | H | [20][18] |
| 32 | Retención de ISR mexicano | Ninguna (IBKR no es agente retenedor mexicano) | GBM retiene y da constancia | I | [19] |
| 33 | Documentos fiscales | Form 1042-S (ingresos de fuente EUA); reporte anual de dividendos; estados de actividad | Constancia fiscal mexicana | H | [19] |
| 34 | Régimen de ganancias en México | **Acciones listadas en el SIC: 10% definitivo (art. 129 fr. I), aunque se vendan por IBKR** (criterio 37/ISR/N). **Sin listado en el SIC:** régimen general, acumulable hasta 35%, pago provisional de 20% del monto en 15 días. **ETFs:** con duda | 10% definitivo (art. 129) | H (acciones SIC) / I (resto) | [35][23][41] |
| 35 | Impuesto sucesorio de EUA | Acciones de sociedades de EUA son bienes situados en EUA; declaración si >60,000 USD; sin tratado con México | Igual para acciones de EUA vía SIC (I) | H / I | [21][22] |
| 36 | Tipo de cuenta y uso de ventas no liquidadas | Efectivo: solo compra con efectivo liquidado; *free riding* → 90 días "Cash Up Front". Margen: puede usar fondos no liquidados | GBM: ver B1 | H | [38][37] |
| 37 | ETFs apalancados o inversos | Requieren el permiso "Complex or Leveraged Exchange Traded Products" (criterios no publicados) | Listados en el SIC (B1) | H | [36] |
| 38 | Contratos de eventos | Kalshi (0.01 + 0.01 USD/contrato), ForecastEx (0.00 + 0.01), CME; para clientes elegibles de IB LLC de 21 años o más; elecciones de EUA solo para residentes de EUA | No | H / (no verificado para México) | [39] |

---

## 2. Disponibilidad, entidad, plan y mínimos

- **[H] México aparece en "Available Countries and Territories"** de IB LLC [6].
- **[H] La entidad depende del país de residencia legal** y aparece en el encabezado del estado de actividad [7]. La lista oficial de entidades incluye IB LLC, IB Canada, IB UK, IB Ireland, IB Australia, IB Hong Kong, IB India, IB Securities Japan e IB Singapore [7]. **No hay entidad mexicana.**
- **[S] Mexico → IB LLC.** Lo confirma un usuario del foro Bogleheads que revisó su estado de cuenta (resumen de búsqueda; la página dio 403) [33]. **[I] Evidencia oficial que concuerda:** la página "Other Fees" de IB LLC trae una tabla de "Deposits – Mexico Only" [3], y la FAQ de MXN dice que el SPEI está disponible en "IBKR LLC, IB Canada, IB Hong Kong and IB UK" [4]. La confirmación definitiva llega con el primer estado de cuenta.
- **[H] IBKR Lite no está disponible.** "IBKR Lite is available to US residents" [1]; la FAQ lista solo residentes, asesores e *introducing brokers* de EUA [8]. **Todo lo que sigue es IBKR Pro.**
- **[H] No hay mínimo:** "Low commissions with no added spreads, ticket charges, platform fees, or account minimums" [1]. "There are no fees to open an account with IBKR" [9].
- **[S] Regulación en México:** IBKR no es una casa de bolsa autorizada por la CNBV y acepta clientes mexicanos bajo su regulación de EUA (resumen de búsqueda de BrokerChooser y TradersUnion; las páginas dieron 403) [33].

---

## 3. Comisiones de acciones y ETFs de EUA, y costo real con 20,000 MXN

### 3.1 Tarifa oficial (IBKR Pro, EUA) [1]

| Concepto | Fixed | Tiered (≤300,000 acciones/mes) |
|---|---|---|
| Por acción | 0.005 USD | 0.0035 USD (baja a 0.0020 con 300,001–3 M) |
| Mínimo por orden | **1.00 USD** | **0.35 USD** |
| Máximo por orden | 1% del valor | 1% del valor (la nota al pie dice "Tiered commissions will be capped at 0.5% of trade value") |
| Terceros que se suman | Regulatorias | Regulatorias + bolsa + compensación + traspaso |
| Fracciones | Mismas tarifas; mínimo 0.01 USD; ej. 50% de acción de 10 USD = 0.05 USD. La nota 11 añade "the greater of 1% of the trade value or USD 0.01"; la FAQ dice "Standard commission rates... apply" y "no additional fee" [11]. **[I]** El 1% solo manda cuando es menor que el mínimo (órdenes de pocos dólares) | Igual |
| Órdenes modificadas | Se tratan como nuevas (pueden volver a pagar el mínimo); las órdenes que pasan la noche cuentan como nuevas | Igual |

- **[H]** SEC: 0.0000206 × valor de venta. FINRA TAF: 0.000195 × acciones vendidas (máx. 9.79 USD). CAT: 0.000003 × acciones. NSCC/DTC: 0.00020 USD/acción. Traspasos: NYSE 0.000175 × comisión y FINRA 0.00056 × comisión [1].
- **[H]** NYSE: retirar liquidez cuesta 0.0030 USD/acción; agregar liquidez puede dar reembolsos de hasta 0.0032 [31]. IBKR advierte que el SmartRouting puede enviar a una bolsa con mejor precio pero cuota más alta [1].
- **[H] Programa NTF:** más de 150 ETFs "reimburse IBKR Pro clients for commissions paid on ETF shares held for at least 30 days" [32]. La lista se carga con JavaScript: **no verifiqué qué ETFs incluye ni si aplica a clientes fuera de EUA.**

### 3.2 Costo calculado por orden [C]

Supuestos: TC de 17.71 (B1) y cuenta de 1,129.31 USD. En Tiered supongo una orden marcable (retira liquidez a 0.0030/acción) y uso fracciones. El costo casi no depende del precio de la acción porque el mínimo domina. Script: cálculo en el scratchpad de la sesión (`costos.py`), con las tarifas de [1][31].

| Tamaño de orden | Fixed, por lado | Fixed, ida y vuelta | Tiered, por lado | Tiered, ida y vuelta | GBM/SIC por lado (B1) |
|---|---|---|---|---|---|
| 2,000 MXN (113 USD) | 0.89% | 1.78% | 0.32% | 0.64% (≈13 MXN) | 0.29% + 0.1%–0.25% implícito |
| **5,000 MXN (282 USD)** | 0.36% | 0.71% | **0.13%** | **0.26%** (≈13 MXN) | 0.39%–0.54% |
| **10,000 MXN (565 USD)** | 0.18% | 0.36% | **0.07%** | **0.13%** (≈13–14 MXN) | 0.39%–0.54% |
| 20,000 MXN (1,129 USD) | 0.09% | 0.18% | 0.04% | 0.07% (≈14–16 MXN) | 0.39%–0.54% |

**Costo anual por rotación completa de 20,000 MXN en órdenes de 5,000 MXN:**

| Rotaciones al año | IBKR Tiered | IBKR Fixed | GBM (comisión) | GBM (TC implícito) |
|---|---|---|---|---|
| 12 | **3.1%** | 8.6% | 7.0% | +2.4% a +6.0% |
| 18 | **4.7%** | 12.9% | 10.4% | +3.6% a +9.0% |

- **[C]** Con el patrón de B1, **Tiered ahorra ~0.26–0.41 puntos por lado frente a GBM**, es decir ~0.5–0.8 puntos por rotación. Con 12–18 rotaciones al año, **eso son ~6–15 puntos de TWR al año**, dentro de la cuenta.
- **[C] Fixed es una trampa en cuentas chicas:** con órdenes de ≤2,000 MXN el mínimo de 1 USD cuesta 0.89% por lado, el triple de GBM.
- **[I]** El spread de compra-venta del valor en EUA existe en los dos brókers. En el SIC se suma el spread local y la desviación del TC implícito (B1). En EUA, un ETF líquido suele tener un spread más estrecho que su réplica en el SIC. No lo medí aquí.

---

## 4. Conversión MXN→USD

- **[H]** Spot FX: **0.20 pb × monto (hasta 1,000 M USD al mes), mínimo 2.00 USD por orden**, con todas las cuotas de bolsa y regulatorias incluidas. "IBKR passes through the prices that it receives and charges a separate low commission" [2].
- **[H]** Conversión automática: "IB will typically add or subtract (at its discretion) 0.03% to the exchange rate that would otherwise apply... IB does not separately charge a commission on these auto-conversion trades" [2].
- **[S]** Las órdenes menores de 25,000 USD se enrutan como *odd lot* con un spread 1–3 pips más ancho según el par (resúmenes de foros y de MatchMyBroker). La guía de MatchMyBroker dice que a partir de ~6,667 USD la conversión manual sale más barata que la automática [33]. (no verificado en fuente oficial)
- **[C] Con 1,129 USD:** la conversión manual cuesta 2.00 USD (0.18%) y la automática ~0.34 USD (0.03%). **Para esta cuenta conviene la automática** o convertir una sola vez al inicio.
- **[I]** Una vez convertida la cuenta, las compras y ventas en USD ya no pagan TC. En el SIC, cada operación lleva la desviación del TC implícito (B1). La exposición al peso es la misma en los dos casos: un ETF del SIC en MXN también sube y baja con el USD/MXN.
- **[H] (verificación)** "Cash accounts can have multi-currency (MULT) capability and can trade non-base currency products", pero en efectivo la cuenta "must have the settled cash balance to enter trades" [37]. Se puede adjuntar una orden de FX a la compra para convertir la moneda base a la del valor [30].
- **(no verificado)** Si la conversión automática (0.03%) cubre una compra en USD con saldo solo en MXN dentro de una cuenta de efectivo, o si hay que convertir antes (2 USD mínimo). También si las ventas regresan a MXN solas o se quedan en USD. **[R]** Hacer una sola conversión manual grande al inicio (2 USD = 0.18% una vez) y operar en USD. Así no depende de esto.

---

## 5. Fondeo y retiros desde México

### 5.1 Rutas de entrada para 20,000 MXN

| Ruta | Costo de IBKR | Costo del banco o intermediario | Costo total aprox. | Tipo |
|---|---|---|---|---|
| **A. SPEI en MXN a la CLABE de IBKR, más conversión automática** | 0 (1er depósito del mes); 100 MXN desde el 2º [3] | 0 por app [S]; BBVA por banca por internet: 5.00 MXN + IVA [26] | **~6–12 MXN (0.03%–0.06%)** | H/C |
| A'. SPEI más conversión manual | igual | igual | ~35–41 MXN (0.18%–0.21%) | H/C |
| B. SWIFT en USD desde BBVA (app o portal) | 0 [5] | 10 USD según la nota de BBVA de 22-sep-2025 [25]; el tarifario (PDF modificado el 13-ago-2026) dice 20 USD + IVA [26]; más el TC de BBVA (no publicado) y bancos intermediarios | ≥177–411 MXN (0.9%–2.1%) + spread | H (contradicción entre fuentes BBVA) |
| C. SWIFT en USD desde la app de Santander | 0 | **0 de comisión** desde el 2-oct-2025 (antes 15 USD); "pueden aplicar" cargos de intermediarios; TC de Santander no publicado | spread + intermediarios (no verificado) | H [27] |
| D. SWIFT desde Banorte | 0 | 30 USD + IVA por envío [S] | ≥~616 MXN (3.1%) | S [28] |
| E. Wise, de MXN a USD por transferencia bancaria (ACH) hacia IBKR | 0 | **193.84 MXN** (0.86% + 23.51 MXN) por 20,000 MXN; recibe 1,118.09 USD al TC medio de 17.714 (cotización del 25-sep-2026). Reverificado el mismo día: la misma comisión y 1,118.97 USD al TC medio de 17.700 | **0.97%** | H [29] |

- **[H] Condiciones de la ruta A** [4]:
  - "IBKR accepts Interbank Transfers (Transferencia Interbancaria) via the SPEI network."
  - Hay que crear una notificación de depósito en el Client Portal para obtener la CLABE.
  - Se puede operar en cuanto llega el dinero; hay que esperar 3 días hábiles para retirar.
  - No se aceptan depósitos en efectivo en ventanilla. Los depósitos de terceros se rechazan en general [4][5].
  - IBKR "does not support digital banks when the bank is based on a digital wallet" y no recomienda procesadores de pago [4].
- **[R] Usar la ruta A**, con **un solo depósito al mes** para no pagar 100 MXN, desde una cuenta bancaria a nombre del titular (no de una billetera digital).

### 5.2 Salida

- **[H]** Retiro en MXN solo por "Bank Wire... via the SWIFT Network"; llega "next day" [4].
- **[H]** "IBKR allows two free withdrawal requests per calendar month." Después: **100 MXN** por transferencia en MXN y **10 USD** en USD [3]. Los cargos de bancos corresponsales o del beneficiario corren por cuenta del cliente [3].
- **[H/no verificado]** El tarifario de BBVA lista la recepción de transferencias internacionales en 30 USD + IVA por evento [26]. Leí el PDF por columnas y asigné el monto por orden, así que el mapeo es probable pero no seguro. Tampoco está verificado que un envío en MXN desde IBKR entre como transferencia internacional y no como SPEI. **[S]** Banorte: 17 USD + IVA por recibir [28].
- **[C] Peor caso de salida con 20,000 MXN:** conversión USD→MXN de 2 USD (0.18%), más la recepción de BBVA de 30 USD × 1.16 × 17.71 ≈ 616 MXN (3.1%). **Hay que confirmarlo antes de abrir la cuenta** y escoger un banco receptor que no cobre.
- **[I] Para el torneo:** si el TWR se mide sobre el valor de la cuenta, los cargos bancarios de entrada y salida quedan fuera, igual que en GBM. Para el dinero neto del dueño sí cuentan.

---

## 6. Custodia, inactividad, datos e intereses

- **[H]** "There are no custodian, trading platform or monthly activity fees for clients except for ISA and TBSZ accounts along with accounts holding positions or actively trading on the B3" [9]. En "Other Fees" no aparece ninguna cuota de inactividad ni de mantenimiento; sí aparecen cargos por eventos (órdenes por teléfono, **550 MXN**; estados de cuenta archivados, etc.) [3].
- **[H] Datos de mercado:** "IBKR clients receive free real-time streaming market data on all US-listed stocks and ETFs from Cboe One and IEX. (Non-consolidated)", 100 snapshots gratis al mes (0.01 USD cada uno en EUA después) y datos diferidos gratis [16]. Una suscripción pagada requiere un capital de 500 USD más su costo [16]. [I] Para operar la estrategia bastan los datos gratis.
- **[H] Intereses:** tabla oficial: USD "0 ≤ 10,000: 0%"; MXN "0 ≤ 200,000: 0%" y ">200,000: 2.465% (BM − 4%)" [17]. Con un NAV menor de 100,000 USD se paga una fracción proporcional [17]. **[C] Con 20,000 MXN el efectivo rinde 0.**
- **[I] Consecuencia para el torneo:** GBM pone el efectivo en Smart Cash (rendimiento y retención de 0.90% en A1/B1). En IBKR, el tiempo en efectivo cuesta el costo de oportunidad completo. Para estacionarlo hay que comprar un ETF de T-bills (por ejemplo, de la familia SGOV/BIL) con Tiered: ~0.13% ida y vuelta con órdenes de 10,000 MXN.

---

## 7. Universo y operativa

- **[H] ETFs de EUA:** PRIIPs exige un KID para "retail investors domiciled in the EEA and the UK" y, sin KID, "the PRIIP will be restricted from trading for EEA and UK retail clients" [12]. La FAQ de fracciones repite que la restricción es para "EU retail clients" [11]. **[I] Un residente mexicano puede comprar ETFs de EUA.** No encontré una restricción específica para México. Esto abre IMTM, IDMO, EEMO y PIE, que B1 no encontró en la BMV. **Costo fiscal (verificación):** al no estar en el SIC, sus ganancias salen del art. 129 (§10.2).
- **[H] Fracciones:** "All individual, standalone accounts (except those who reside in Israel, Canadian RRSP/TFSA accounts and... IBSJ) are eligible". Aplica a acciones y ETFs elegibles de EUA, Canadá y Europa (lista en `fracshare_stk.csv`) [11]. **[I]** Con 1,129 USD, esto permite ponderaciones exactas. En el SIC solo hay títulos completos (B1).
- **[H] Opciones de EUA:** IBKR Pro cobra 0.65 USD por contrato (≤10,000 contratos al mes, prima ≥0.10; menos en primas bajas), mínimo 1.00 USD por orden, más bolsa, compensación, regulatorias y transacción. Lite es solo para EUA [13].
  - Niveles: 1 (covered calls), 2 (compras de calls y puts, spreads de débito, collars), 3 (pérdida máxima limitada), 4 (todo) [14].
  - "Clients who maintain either a cash or margin type account must maintain net liquidating equity of at least USD 2,000... to establish or increase an existing uncovered options position" [14].
  - IBKR "cannot disclose its eligibility requirements" [14].
  - [I] Con 20,000 MXN solo son viables las opciones compradas y cubiertas, con nivel 2 aprobado.
- **[H] UCITS en Europa:** LSE en USD: Tiered 0.05%, mín. 1.70 USD; Fixed mín. 4.00 USD. LSE en GBP: Tiered mín. 1.00 GBP; Fixed mín. 3.00 GBP. Xetra/Alemania: Tiered 0.05%, mín. 1.25 EUR (máx. 29); Fixed mín. 3.00 EUR [1]. **[C]** Una orden de 5,000 MXN en un UCITS de LSE en USD cuesta ≥0.60% por lado en Tiered, **más caro que un ETF de EUA**. Solo tiene sentido si la cuenta crece (sucesorio, §9.3).
- **[H] BMV desde IBKR:** Fixed 0.1% del valor, **mín. 60 MXN** por orden (ej. 700 acciones a 100 MXN = 70 MXN) [1]. **[C]** Una orden de 5,000 MXN paga 60 MXN (1.2%): no conviene. **(no verificado)** si IBKR permite operar emisoras del SIC.
- **[H] Órdenes:** "Clients have access to over 100 Order Types, Algos and Tools" (bracket, OCA, stop, trailing, operación nocturna) [30].
- **[H] PDT:** FINRA RN 26-10: la SEC aprobó el 14-abr-2026, entró en vigor el 4-jun-2026 y los brókers tienen hasta el 20-oct-2027 para implementarla. Elimina el mínimo de 25,000 USD y el conteo de *day trades* [15]. IBKR: "the $25,000 minimum equity requirement for pattern day traders is no longer required... the minimum equity requirement is $2,000 to trade with leverage or execute short sales" [15]. **Matiz (verificación):** la página "Configuring Your Account" de IBKR dice que, "During the PDT rule phase-out period, accounts that remain subject to existing Pattern Day Trading regulations must maintain a minimum of USD 25,000" [37].
- **[H] Cuenta de efectivo y *free riding* (antes solo con fuente secundaria):** según la FAQ oficial, IBKR revisa en tiempo real que haya "fully settled cash" antes de aceptar cada orden. Si se cierra antes de liquidar una posición pagada con fondos no liquidados, la cuenta queda **90 días en "Cash Up Front"**. Con una cuenta de margen, "unsettled funds may be used for trading purposes but may not be withdrawn until settlement". El cambio a margen tarda de 24 a 48 horas [38]. La liquidación de acciones en EUA es T+1 desde el 28-may-2024 [40]. La página de configuración todavía dice "three business days" para la cuenta de efectivo [37]; **[I]** parece texto viejo.
  - **[C/I]** En una rotación mensual con cuenta de efectivo, el producto de la venta queda sin invertir ~1 día hábil antes de comprar lo nuevo. Son ~12 días al año fuera del mercado. El costo esperado es ≈ 12/252 × el rendimiento anual esperado: con 10%–15%, **~0.5–0.7 puntos al año**, con mucho ruido día a día. Si GBM deja comprar con ventas no liquidadas, esa diferencia va contra IBKR en efectivo (ver B1). Una cuenta de margen la elimina.
  - **(no verificado)** Si una cuenta de margen con menos de 2,000 USD de capital puede usar fondos no liquidados. La FAQ exige 2,000 USD para "trade with leverage" [15].
- **[H] ETFs apalancados o inversos:** IBKR los clasifica como "Complex or Leveraged Exchange Traded Products" y exige un permiso aparte. Para aprobarlo hay que "meet certain financial requirements, have a certain amount of prior trading experience" [36]. Si la estrategia usa TQQQ, SOXL o SPXL (réplica R06), hay que pedirlo al abrir la cuenta.
- **[H] Contratos de eventos (antes "no verificado"):** la plataforma Prediction Markets de IBKR da "unified access to three leading U.S. prediction market exchanges: Kalshi, CME Group, and ForecastEx". Comisiones: Kalshi 0.01 USD por contrato más 0.01 de bolsa; ForecastEx 0.00 más 0.01; CME 0.01 más 0.01. "Event Contracts are only available to eligible clients, 21 years and older, of Interactive Brokers LLC, Interactive Brokers Canada Inc., Interactive Brokers Hong Kong Limited, Interactive Brokers Ireland Limited and Interactive Brokers Singapore Pte. Ltd." Las elecciones de EUA son "only available to eligible US residents" [39]. **[I]** Un residente mexicano en IB LLC entra en la lista de entidades. **(no verificado)** Qué otros requisitos de elegibilidad aplican y el trato fiscal mexicano de esos contratos.

---

## 8. Protección y riesgo de contraparte

- **[H]** "Customer securities accounts at Interactive Brokers LLC are protected by... SIPC for a maximum coverage of $500,000 (with a cash sublimit of $250,000) and under... excess SIPC policy with certain underwriters at Lloyd's of London for up to an additional $30 million (with a cash sublimit of $900,000) subject to an aggregate limit of $150 million" [10].
- **[H]** Divisas: si el MXN está en la cuenta "to pay for investments that qualify as 'securities'" cuenta como efectivo protegido; si se tiene "as an investment", no [10].
- **[I]** La protección cubre la quiebra del bróker, no las pérdidas de mercado [10]. Si hubiera una disputa, se resolvería con leyes y autoridades de EUA, no ante la CONDUSEF ni la CNBV.

---

## 9. Impuestos de EUA

### 9.1 W-8BEN
- **[H]** "All non-US persons and entities are required to complete an IRS Form W-8... when opening an account." Vale "for the year in which they are signed and for the next three calendar years". Si vence, IBKR retiene 30% sobre intereses, dividendos, "gross proceeds" y pagos sustitutos [18]. Se renueva en el Client Portal [19].
- **[H/I]** No aparece ningún cargo por W-8 en "Other Fees" [3]. **En IBKR sale gratis; en el SIC de GBM cuesta 75 USD + IVA** (B1).

### 9.2 Retención sobre dividendos
- **[H]** IRS Table 1 (Rev. mayo 2023, PDF modificado en mayo de 2026): México, dividendos "Paid by U.S. Corporations — General" **10%**; "Qualifying for Direct Dividend Rate" **5%**; artículo 10(2)/2P [20].
- **[H]** IBKR: el W-8 "only allows for a reduction in the tax rate not an elimination"; los dividendos de ADR de EUA "are generally withheld at source and will not be eligible for a reduced tax rate"; las distribuciones ECI de MLP no tienen beneficio de tratado [19].
- **[C] Carga en EUA sobre un dividendo de 100 USD:** IBKR 10 USD; SIC sin W-8BEN 30 USD (B1).

### 9.3 Impuesto sucesorio (responde el punto 5 de V05)
- **[H]** Bienes situados en EUA sujetos al impuesto incluyen "Stock of corporations organized in or under U.S. law, even if the nonresident held the certificates abroad or registered the certificates in the name of a nominee". Se presenta el Form 706-NA si su valor al fallecer "exceeds $60,000" [21].
- **[H]** La lista del IRS de tratados sucesorios o de donaciones incluye Australia, Austria, Canadá, Dinamarca, Finlandia, Francia, Alemania, Grecia, Irlanda, Italia, Japón, Países Bajos, Sudáfrica, Suiza y Reino Unido. **México no está** [22].
- **[I]** "In the name of a nominee" sugiere que la custodia vía Indeval/SIC no cambia la ubicación de una acción de EUA. El riesgo existe también en GBM.
- **[I]** Los UCITS irlandeses no son "stock of corporations organized... under U.S. law", así que en principio no son bienes situados en EUA (no verificado fondo por fondo).
- **[I] Con 1,129 USD no importa.** Importa cuando la posición en acciones o ETFs de EUA pase de 60,000 USD. Las tasas del impuesto no se verificaron en esta sesión.

---

## 10. Impuestos en México y reportes

### 10.1 Qué entrega IBKR
- **[H]** Form 1042-S: "reports US source income earned by non-US persons subject to US withholding tax, including interest, dividends, substitute payments in lieu and fees"; también se envía al IRS [19]. Reporte anual de dividendos con retenciones, en la moneda base de la cuenta [19]. Estados de actividad, con 7 años disponibles [3].
- **[I]** IBKR no emite constancia mexicana ni calcula la ganancia del art. 129. El cálculo de la ganancia actualizada (INPC) y del TC queda en manos del dueño o de su contador.

### 10.2 Ganancias por venta de acciones y ETFs de EUA en NYSE/Nasdaq
- **[H]** El art. 129 (10% definitivo) cubre:
  - Fr. I, en el orden del texto: "La enajenación de acciones emitidas por sociedades mexicanas... cuando su enajenación se realice en las bolsas de valores concesionadas o mercados de derivados reconocidos en los términos de la Ley del Mercado de Valores **o de acciones emitidas por sociedades extranjeras cotizadas en dichas bolsas de valores**" [23]. **(Verificación:** la paráfrasis anterior ponía el "cuando" también sobre las acciones extranjeras. El SAT lee que para estas basta que estén cotizadas en el SIC [35].)
  - Fr. II: "títulos que representen índices accionarios enajenados en las bolsas... a que se refiere la fracción anterior".
  - Fr. III: solo acciones de **sociedades mexicanas** vendidas en mercados reconocidos de países con tratado [23].
  - La suma de ganancias se hace por intermediario, incluidas "entidades financieras extranjeras con los que tenga un contrato de intermediación" [23].
  - **[H] (verificación; la versión anterior decía que esto solo valía para la fr. III y estaba mal):** el art. 129 tiene un párrafo general para todo el primer párrafo, no solo para la fr. III: "Los contribuyentes que realicen las enajenaciones u operaciones a que se refiere el primer párrafo de este artículo, a través de contratos de intermediación que tengan con entidades financieras extranjeras que no estén autorizados conforme a la Ley del Mercado de Valores, deberán calcular la ganancia o pérdida fiscales del ejercicio y, en su caso, el impuesto que corresponda, así como tener a disposición de la autoridad fiscal los estados de cuenta" [23].
  - **[H] Criterio 37/ISR/N** (Anexo 7 RMF 2026, DOF 09-01-2026; primer antecedente 46/2014/ISR). Las ganancias por vender "acciones emitidas por sociedades extranjeras listadas en el apartado de valores autorizados para cotizar en el Sistema Internacional de Cotizaciones de la Bolsa Mexicana de Valores o de la Bolsa Institucional de Valores... están sujetas a una tasa del 10% en los términos del artículo 129, fracción I de la Ley del ISR, **con independencia de que su enajenación no se realice a través de un intermediario del mercado de valores mexicano**" [35].
- **[H] Consecuencia:** una venta en Nasdaq/NYSE por IBKR de una **acción listada en el SIC** (AAPL, NVDA, MSFT…) paga **10% definitivo** sobre la ganancia neta del año, igual que en GBM, y se declara en la anual [23][35]. No hay pago provisional.
- **[I] ETFs y acciones que no están en el SIC.** El criterio 37 solo cubre "acciones" listadas en el SIC. Una venta de un ETF que no está en el SIC (IMTM, IDMO, EEMO, PIE) o de una acción que no está en el SIC **no cabe en las fracciones I–III**. Para un ETF listado en el SIC y vendido fuera, la duda sigue abierta (B4 §1.3). Lo que no cabe va al régimen general de enajenación de bienes (Título IV, Cap. IV):
  - **Art. 120:** la ganancia se divide entre los años de tenencia (máx. 20), esa parte se acumula y el resto paga a tasa promedio. Todo se calcula con la tarifa progresiva del art. 152 [23].
  - **Art. 126:** "Tratándose de la enajenación de otros bienes, el pago provisional será por el monto que resulte de aplicar la tasa del 20% sobre el monto total de la operación... En el caso de que el adquirente no sea residente en el país... el enajenante enterará el impuesto correspondiente mediante declaración... dentro de los quince días siguientes a la obtención del ingreso" [23].
  - Si el art. 126 aplica al pie de la letra, **cada venta generaría un pago provisional en 15 días**. El Reglamento permite un pago menor ("excepto en los casos en los que el enajenante manifieste... que efectuará un pago provisional menor... requisitos que señale el Reglamento") [23]. **[I] (verificación):** en el texto, esa excepción va con la retención que hace un comprador residente en México. Para un comprador extranjero, el artículo solo dice que el vendedor entera "el impuesto correspondiente" en 15 días. **No revisé el RLISR ni la RMF 2026.**
- **[H]** La ganancia cambiaria es ingreso del Cap. IX (art. 142 fr. II) [23]. [I] Tener USD en la cuenta genera ganancia o pérdida cambiaria acumulable.
- **[H] Tarifa 2026 (art. 152, Anexo 8 RMF 2026, DOF 28-12-2025):** 30% sobre el excedente de 668,840.15 MXN, 32% desde 1,276,925.99, 34% desde 1,702,567.98 y **35% desde 5,107,703.93 MXN** [41].
- **(no verificado con el SAT ni con un contador):** el régimen exacto de los ETFs, si existe una regla miscelánea que simplifique los pagos provisionales de ventas en mercados reconocidos extranjeros, y el RLISR sobre el pago provisional menor. Pérdidas fuera del art. 129: año en curso más 3 siguientes, con los requisitos del reglamento (arts. 121–122, ver B4 §1.4).

### 10.3 Dividendos
- **[H]** Art. 142 fr. V: son ingresos "Los dividendos o utilidades distribuidos por sociedades residentes en el extranjero". La persona física, "además de acumularlos... deberán enterar de forma adicional, el impuesto... [a] la tasa del 10%, al monto... del dividendo... efectivamente distribuido por el residente en el extranjero, sin incluir el monto del impuesto retenido". Es un pago "definitivo" que se entera "a más tardar el día 17 del mes siguiente" [23]. El acreditamiento del impuesto extranjero es "en lo conducente el artículo 5" [23].
- **[I]** Cada mes con un dividendo de EUA genera una declaración de pago del 10% adicional. Además, el dividendo se acumula en la anual con crédito por el 10% retenido en EUA (art. 5).

### 10.4 Ejemplo del efecto en el dinero del dueño [C/I]
Supuestos hipotéticos: ganancia realizada de 3,000 MXN en el año (15% de 20,000) y 12 rotaciones al año con órdenes de 5,000 MXN.

Tabla corregida en la verificación. La versión anterior aplicaba la tasa progresiva a todo; ahora la primera columna de IBKR usa el criterio 37:

| | GBM/SIC | **IBKR Tiered, solo acciones listadas en el SIC** (10%, criterio 37) | IBKR Tiered, ETFs o acciones sin SIC, tasa marginal 20% (hipotética) | Ídem, tasa marginal 30% (hipotética) |
|---|---|---|---|---|
| Fricción de operación (§3.2) | 7.0% + 2.4%–6.0% = **9.4%–13.0%** | **3.1%** | **3.1%** | **3.1%** |
| ISR sobre 3,000 MXN de ganancia | 10% = 300 MXN (1.5% de la cuenta) | 10% = 300 MXN (1.5%) | ~600 MXN (3.0%) | ~900 MXN (4.5%) |
| **Total (puntos de la cuenta)** | **~10.9%–14.5%** | **~4.6%** | **~6.1%** | **~7.6%** |

- **[C/I]** Con acciones listadas en el SIC, IBKR gana por ~6–10 puntos sin castigo fiscal. Con ETFs fuera del SIC, IBKR sigue ganando con alta rotación aun con tasa marginal alta. Con rotación baja (≤4 al año) y ganancias altas, el SIC puede ganar en esos instrumentos. **Esto no incluye el costo del contador**.
- **[C] Liquidez del art. 126 (solo para lo que no está en el SIC):** con 12 rotaciones de 20,000 MXN se venden ~240,000 MXN al año. Un pago provisional de 20% del monto bruto serían **~48,000 MXN al año adelantados al SAT** (≈4,000 MXN al mes, 20% de la cuenta cada mes), contra un impuesto final de cientos de pesos. Se recupera como saldo a favor en la anual. Es la razón práctica más fuerte para quedarse en instrumentos listados en el SIC. **(no verificado)** si el RLISR o la RMF permiten un pago menor en este caso.

### 10.5 IVA
- **[H]** El listado de prestadores de servicios digitales inscritos en el RFC (Oficio 700-04-00-00-00-2025-060, DOF 25-jul-2025) **no incluye a Interactive Brokers**; sí incluye, por ejemplo, a TradingView (núm. 235) [24]. **Límite (verificación):** ese listado tiene corte al 30-jun-2025 (266 prestadores). Se publica cada bimestre. Según una fuente secundaria, hay uno más reciente, del 6º bimestre de 2025 (272 prestadores, oficio 700-04-00-00-00-2026-003), pero el PDF vigente del SAT dio 403. **(no verificado)** que IBKR siga fuera en 2026.
- **[I]** Las comisiones de corretaje no parecen servicios digitales del art. 18-B de la LIVA, así que IBKR no cobraría IVA mexicano. **(no verificado)** Queda por confirmar en el primer estado de cuenta si hay IVA en las suscripciones de datos.

---

## 11. Impacto en la competencia y ajustes a las réplicas

- **[R] Plan y configuración si se abre la cuenta (actualizado en la verificación):**
  - IBKR Pro **Tiered**, fracciones activadas y datos gratis de Cboe One/IEX.
  - **Tipo de cuenta:** pedir **margen** (sin usar apalancamiento) para poder rotar con ventas no liquidadas. En efectivo, cada rotación espera la liquidación (T+1) y una violación de *free riding* bloquea la cuenta 90 días [38]. Si con menos de 2,000 USD la cuenta de margen no permite usar fondos no liquidados, queda en efectivo y se aceptan ~0.5–0.7 puntos al año de costo esperado.
  - Pedir al abrir los permisos de "Complex or Leveraged ETPs" (si la estrategia usa apalancados) y de Prediction Markets (si se quiere Kalshi o ForecastEx) [36][39].
  - Depósito por SPEI una vez al mes.
  - Una sola conversión manual grande al inicio (2 USD) o la conversión automática (0.03%), según lo que permita la cuenta (§4).
  - Órdenes limitadas cuando se pueda (reembolso de liquidez en lugar de cuota).
  - **Universo fiscalmente limpio:** para la cuenta real del dueño, dar prioridad a acciones listadas en el SIC (10% por el criterio 37). Usar ETFs o acciones fuera del SIC solo si el rendimiento esperado compensa la tarifa progresiva y los pagos provisionales de 20% (§10.4).
- **[R] Recalcular las réplicas** (lo pidió el dueño) con:
  - Comisión Tiered: máx(0.35, 0.0035 × acciones), más ~0.0032 USD por acción de bolsa y compensación, más traspasos y regulatorias en ventas.
  - Conversión de 0.03% o 2 USD solo cuando se cambie de moneda, no en cada operación.
  - Efectivo a 0% (no Smart Cash).
  - Sin desviación del TC implícito del SIC.
- **[R] Comparabilidad:** en la bitácora, cada operación anota su costo en IBKR y el costo equivalente en GBM (0.29% + la desviación medida en B1). Así se puede separar el efecto del bróker del efecto de la estrategia frente a las IAs que siguen en GBM.
- **[I] Qué cambia en la estrategia:**
  - El universo de momentum se amplía (IMTM, IDMO, EEMO, PIE y cualquier ETF de EUA). **Pero lo que no está en el SIC paga el régimen general** (§10.2): para el TWR del torneo no cuenta, para el neto del dueño sí.
  - Las fracciones permiten ponderaciones exactas.
  - Stops y brackets se pueden usar en EUA.
  - Opciones solo compradas o cubiertas, y solo con nivel 2.
  - El efectivo ya no rinde.
- **[I] Riesgo operativo:** no busqué incidentes de caídas de IBKR en 2025-2026. Queda pendiente para comparar con los de GBM (B1 §7).

---

## 12. No verificado (pendiente)

1. **Entidad IB LLC para México:** solo hay confirmación secundaria [33] y consistencia con páginas oficiales [3][4]. Se confirma con el primer estado de cuenta.
2. **Depósitos:** "We do not charge for deposits" [4] contra "subsequent deposits... MXN 100" [3]. Supuse el caso conservador.
3. **Spread de la conversión automática y de las órdenes chicas de FX** (solo fuentes secundarias). Si la conversión automática opera con base MXN en una cuenta de efectivo y a qué moneda regresan las ventas.
4. **Costo de recibir un retiro de IBKR en MXN** en BBVA, Banorte o Santander. Si llega como SWIFT o como SPEI, y si aplica el cobro de "recepción internacional".
5. **Banorte:** la página oficial dio 403/503. Las cifras de 30 USD + IVA (envío) y 17 USD + IVA (recepción) son de resumen de búsqueda.
6. **BBVA:** la nota de prensa dice 10 USD por SWIFT digital desde abr-2025; el tarifario dice 20 USD + IVA. Además, el PDF se leyó con columnas desalineadas.
7. **Régimen fiscal mexicano de las ventas en NYSE/Nasdaq:** **resuelto para acciones listadas en el SIC** (10%, criterio 37/ISR/N) [35]. Sigue abierto para ETFs, con o sin SIC, y para acciones sin SIC: pagos provisionales (art. 126 contra lo que permita el RLISR/RMF). La tasa marginal ya está verificada (hasta 35%) [41]. **Requiere contador.**
8. **Lista de ETFs del programa NTF** y si aplica a clientes fuera de EUA.
9. **Si IBKR permite operar emisoras del SIC** en su acceso a la BMV.
10. **Contratos de eventos para residentes de México:** IBKR da acceso a Kalshi, CME y ForecastEx para clientes elegibles de IB LLC [39]. Falta confirmar los criterios de elegibilidad para México y el trato fiscal mexicano.
14. **Uso de fondos no liquidados en una cuenta de margen con menos de 2,000 USD** [15][38].
15. **Si la conversión automática cubre compras en USD con saldo en MXN** en una cuenta de efectivo [37].
16. **Aprobación del permiso de ETPs complejos o apalancados** para esta cuenta [36].
17. **Si GBM deja comprar con ventas no liquidadas** (para comparar el costo de liquidación; ver B1).
11. **Tasas del impuesto sucesorio de EUA** y el tratamiento de UCITS fondo por fondo.
12. **Incidentes operativos de IBKR 2025-2026.**
13. **IVA en suscripciones de datos** para clientes mexicanos.

---

## Verificacion (2026-09-25)

**Verificador adversarial.** Volví a bajar cada fuente oficial el 2026-09-25: páginas de tarifas de IBKR con curl, 17 FAQ de IBKR con el endpoint público, IRS, SAT (Anexos 7 y 8 de la RMF 2026), LISR (texto congelado en V05), FINRA, SEC, Wise (API en vivo) y el tarifario de BBVA. Recalculé §3.2 con un script propio.

### Qué se sostuvo (sin cambios)

| Dato | Fuente oficial releída | Estado |
|---|---|---|
| Fixed 0.005 USD/acción, mín. 1.00, máx. 1%; Tiered 0.0035, mín. 0.35 | Commissions Stocks [1] | Confirmado |
| SEC 0.0000206 × ventas; FINRA TAF 0.000195/acción (máx. 9.79); CAT 0.000003; NSCC/DTC 0.00020; traspasos NYSE 0.000175 y FINRA 0.00056 × comisión | [1] | Confirmado |
| NYSE: retirar liquidez 0.0030 USD/acción; agregar liquidez −0.0032 | [31] | Confirmado |
| FX: 0.20 pb, mín. 2.00 USD; conversión automática +/−0.03% sin comisión | [2] | Confirmado |
| 2 retiros gratis al mes; luego 100 MXN o 10 USD; "Deposits – Mexico Only" 100 MXN desde el 2º; órdenes telefónicas 550 MXN | [3] | Confirmado |
| SPEI a CLABE de 18 dígitos, ≤1 día hábil, retención de 3 días; retiro por SWIFT; "We do not charge for deposits" (sigue la contradicción con [3]) | FAQ 1146099559 [4] | Confirmado |
| México en la lista de países; sin entidad mexicana; Lite solo para EUA; sin cuota de apertura, custodia ni actividad | [6][7][8][9] | Confirmado |
| Intereses: USD 0% ≤10,000; MXN 0% ≤200,000 (>200,000: 2.465%, BM − 4%); prorrateo si NAV <100,000 USD | [17] | Confirmado |
| Datos gratis Cboe One + IEX (no consolidados); 100 snapshots; 0.01 USD por snapshot de EUA después; capital mínimo de 500 USD para suscripciones | [16] | Confirmado |
| Opciones 0.65 USD/contrato, mín. 1.00; niveles 1–4; 2,000 USD para descubiertas | [13][14] | Confirmado |
| BMV: 0.1%, mín. 60 MXN; LSE en USD: Tiered mín. 1.70 (máx. 39), Fixed 4.00; Xetra: Tiered mín. 1.25 EUR (máx. 29), Fixed 3.00 | [1] | Confirmado |
| SIPC 500,000 (250,000 en efectivo) + Lloyd's 30 M (900,000 en efectivo), tope de 150 M; divisa según la intención | [10] | Confirmado |
| PRIIPs solo bloquea a minoristas del EEE y del Reino Unido; fracciones para todas las cuentas individuales salvo Israel, RRSP/TFSA e IBSJ | [11][12] | Confirmado |
| W-8: obligatorio, vigente el año de firma + 3; 30% si vence (incluye *gross proceeds*); 1042-S | [18][19] | Confirmado |
| Tratado: dividendos 10% general, 5% participación directa (IRS Table 1, PDF modificado el 08-may-2026) | [20] | Confirmado |
| Sucesorio: "registered... in the name of a nominee", umbral de 60,000 USD (página revisada el 27-jun-2026); México fuera de la lista de tratados (revisada el 08-sep-2026) | [21][22] | Confirmado |
| Art. 126 (20% del monto total, 15 días si el comprador es extranjero) y art. 142 fr. V (10% adicional al día 17) | LISR [23] | Confirmado (texto) |
| FINRA RN 26-10: aprobación 14-abr-2026, vigencia 4-jun-2026, implementación hasta 20-oct-2027 | [15] | Confirmado |
| Wise: 193.84 MXN por 20,000 MXN | API en vivo [29] | Confirmado (TC medio de 17.700 en la re-cotización) |
| BBVA: SPEI por internet 5.00 MXN; SWIFT digital 20 USD; recepción internacional 30 USD (+IVA), con el mapeo de columnas incierto que ya se había señalado | Tarifario V.229 [26] | Confirmado con la misma salvedad |
| Santander: 0 de comisión por SWIFT en la app desde el 2-oct-2025 (antes 15 USD); asterisco sobre intermediarios | [27] | Confirmado |
| Costos de §3.2 (Tiered 0.13% por lado con 5,000 MXN; 3.1% al año con 12 rotaciones, etc.) | Recálculo propio | Reproducido a ±0.1 punto (18 rotaciones: 4.6% contra 4.7%; Fixed 12.8% contra 12.9%) |

### Qué se corrigió en sitio

1. **Régimen fiscal de ventas por IBKR (Resumen 12 y 13, tabla fila 34, §10.2, §10.4, §11, §12).** **Error decisivo.** B3 decía que ninguna venta en NYSE/Nasdaq cabe en el art. 129. El **criterio 37/ISR/N** (Anexo 7 RMF 2026, DOF 09-01-2026) dice lo contrario para las **acciones listadas en el SIC**: 10% "con independencia de que su enajenación no se realice a través de un intermediario del mercado de valores mexicano" [35]. Además, el art. 129 tiene un párrafo expreso para quien opera con "entidades financieras extranjeras" [23]. B3 lo había reducido a la fr. III. **Efecto:** con acciones listadas en el SIC, IBKR ya no tiene desventaja fiscal y gana también en el neto del dueño (~4.6% contra ~10.9%–14.5% en el ejemplo de §10.4). El castigo fiscal queda solo para ETFs y para acciones sin SIC.
2. **Tasa marginal** (antes "no verificada"): tarifa anual 2026 de hasta 35% (Anexo 8 RMF 2026) [41].
3. **Liquidez del art. 126** (nuevo cálculo): ~48,000 MXN al año de pagos provisionales si se rota en instrumentos sin SIC.
4. **Cuenta de efectivo:** B3 lo apoyaba en una fuente secundaria. Ahora es un hecho oficial (FAQ de *free riding*), con su consecuencia operativa: esperar la liquidación T+1 o pedir cuenta de margen [38][40].
5. **PDT:** "ya no existe" pasó a "en retiro"; IBKR advierte sobre las cuentas que siguen sujetas durante la transición [37].
6. **Contratos de eventos** (antes "no verificado"): IBKR da acceso a **Kalshi**, CME y ForecastEx para clientes elegibles de IB LLC [39]. Es relevante porque el dueño tiene limitado el acceso a Kalshi. La elegibilidad para México sigue sin confirmar.
7. **ETFs apalancados:** faltaba el permiso "Complex or Leveraged ETPs" [36].
8. **Tope de 0.5% en Tiered:** se aclaró cuál nota va con qué concepto (no cambia ningún cálculo; manda el mínimo).
9. **Nota de fracciones:** se añadió el texto literal de la nota 11 y la lectura de la FAQ (no cambia ningún cálculo).
10. **Listado del SAT de servicios digitales:** tiene corte al 30-jun-2025; el vigente dio 403 **(no verificado para 2026)**.
11. **Encabezado:** V05 ya no es solo un pre-registro; se añadió B4 como referencia.
12. **Título de la FAQ [15]:** corregido.
13. **Paráfrasis de la fr. I del art. 129 (§10.2):** ahora sigue el orden del texto; antes sugería que las acciones extranjeras también debían venderse en bolsa concesionada.
14. **Excepción de "pago provisional menor" del art. 126:** se precisó que, en el texto, va con la retención de un comprador residente, no con la venta a un comprador extranjero.
15. **Costo de liquidación en cuenta de efectivo** (nuevo): ~0.5–0.7 puntos al año de rendimiento esperado con rotación mensual; una cuenta de margen lo elimina (§7).

### Qué sigue sin sostenerse en fuente oficial (se queda marcado)

- La entidad IB LLC para residentes de México (solo hay fuente secundaria y consistencia con [3][4]).
- El spread de las órdenes chicas de FX (*odd lot*), y si la conversión automática cubre compras en USD con saldo en MXN en una cuenta de efectivo.
- El costo de recibir un retiro de IBKR en MXN en un banco mexicano (SWIFT o SPEI).
- Las cifras de Banorte (la página oficial no se pudo leer).
- El régimen de los ETFs, con o sin SIC, vendidos por un bróker extranjero, y si existe alivio al art. 126. **Requiere contador.**
- Si una cuenta de margen con menos de 2,000 USD puede usar fondos no liquidados.
- La elegibilidad para México de los contratos de eventos y su trato fiscal.
- El programa NTF para clientes fuera de EUA; emisoras del SIC desde el acceso de IBKR a la BMV; incidentes operativos; IVA en suscripciones.

### Veredicto del verificador

**[R]** Los datos de costo de B3 se sostienen. Su conclusión operativa (IBKR Pro Tiered es el de menor fricción) queda en pie. **Su conclusión fiscal estaba mal en contra de IBKR:** con un universo de **acciones listadas en el SIC**, IBKR maximiza el rendimiento neto también después de impuestos. Solo pierde terreno si la estrategia depende de ETFs o acciones que no están en el SIC, por la tarifa progresiva y los pagos provisionales de 20% del monto. Antes de abrir la cuenta quedan tres cosas por confirmar:

1. Si hace falta cuenta de margen para rotar sin esperar la liquidación.
2. El costo real de sacar el dinero a un banco mexicano.
3. La elegibilidad para Kalshi o ForecastEx.

---

## Fuentes

Todas se consultaron el **2026-09-25**. Las FAQ de IBKR se leyeron con el endpoint público `https://www.interactivebrokers.com/tws.proxy/faq/content`. Cito su URL pública con el id.

1. IBKR, "Commissions Stocks" (EUA Fixed, Tiered y Lite; cuotas regulatorias; México; Alemania; Reino Unido; fracciones; notas al pie). https://www.interactivebrokers.com/en/pricing/commissions-stocks.php
2. IBKR, "Commissions Spot Currencies" (0.20 pb, mín. 2 USD, conversión automática 0.03%). https://www.interactivebrokers.com/en/pricing/commissions-spot-currencies.php
3. IBKR, "Other Fees" (retiros: 2 gratis al mes, MXN 100 y USD 10; "Deposits – Mexico Only" MXN 100; órdenes telefónicas MXN 550; estados de cuenta archivados). https://www.interactivebrokers.com/en/pricing/other-fees.php
4. IBKR FAQ, "MXN Deposits and Withdrawals" (id 1146099559: SPEI, CLABE, disponibilidad por entidad, retiros SWIFT). https://www.ibkrguides.com/kb/en-us/how-to-deposit-mxn.htm → https://www.interactivebrokers.com/lib/cstools/faq/#/content/1146099559
5. IBKR, "Fund Your Account" (IBKR no responde por cargos bancarios; efectivo y terceros). https://www.interactivebrokers.com/en/support/fund-my-account.php
6. IBKR, "Available Countries and Territories" (México en la lista; aviso sobre ForecastEx). https://www.interactivebrokers.com/en/accounts/open-account-country-list.php
7. IBKR FAQ, "Which IBKR entity carries my account?" (id 38458938). https://www.interactivebrokers.com/lib/cstools/faq/#/content/38458938
8. IBKR FAQ, "Who is eligible for IBKR Lite?" (id 76129181). https://www.interactivebrokers.com/lib/cstools/faq/#/content/76129181
9. IBKR FAQ, "Is there a fee to open or maintain an account with Interactive Brokers?" (id 51679208). https://www.interactivebrokers.com/lib/cstools/faq/#/content/51679208
10. IBKR FAQ, "How is my IB LLC account protected?" (id 28214293) y "Does SIPC protection cover cash held in the account?" (id 96841841). https://www.interactivebrokers.com/lib/cstools/faq/#/content/28214293 · https://www.interactivebrokers.com/lib/cstools/faq/#/content/96841841
11. IBKR FAQ, "Fractional share trading" (id 1163260722). https://www.interactivebrokers.com/lib/cstools/faq/#/content/1163260722
12. IBKR FAQ, "PRIIPs regulation" (id 1136192471; enlazada desde ibkrguides article-2993). https://www.interactivebrokers.com/lib/cstools/faq/#/content/1136192471
13. IBKR, "Commissions Options" (EUA Pro y Lite). https://www.interactivebrokers.com/en/pricing/commissions-options.php
14. IBKR FAQ, "What are the levels of option trading permissions?" (id 1421263358) y "What are the requirements to qualify for option trading permissions?" (id 28236881). https://www.interactivebrokers.com/lib/cstools/faq/#/content/1421263358 · https://www.interactivebrokers.com/lib/cstools/faq/#/content/28236881
15. IBKR FAQ, "If the $25,000 minimum equity is no longer required for a pattern day trader, what is the minimum equity requirement?" (id 1460021712; título corregido en la verificación). https://www.interactivebrokers.com/lib/cstools/faq/#/content/1460021712 · FINRA, Regulatory Notice 26-10 (20-abr-2026). https://www.finra.org/rules-guidance/notices/26-10
16. IBKR, "Market Data Pricing" (datos gratis Cboe One/IEX, snapshots, capital mínimo de 500 USD). https://www.interactivebrokers.com/en/pricing/market-data-pricing.php
17. IBKR, "Interest Rates" (USD 0% hasta 10,000; MXN 0% hasta 200,000; >200,000 2.465%) y FAQ de intereses (id 32647026: prorrateo por NAV <100,000 USD). https://www.interactivebrokers.com/en/accounts/fees/pricing-interest-rates.php · https://www.interactivebrokers.com/lib/cstools/faq/#/content/32647026
18. IBKR, "Tax Information and Reporting – Non-US – Initial Application & Data Collection" (W-8 obligatorio, vigencia, 30% por omisión). https://www.interactivebrokers.com/en/support/tax-nonus-initial.php
19. IBKR, "Tax Information and Reporting – Year-End Tax Forms" (1042-S). https://www.interactivebrokers.com/en/support/tax-nonus-forms.php · FAQ ids 28216508 (Dividend Report), 32647192 (retención y ADR), 32666329 (actualizar el W-8BEN; MLP/ECI). https://www.interactivebrokers.com/lib/cstools/faq/#/content/28216508
20. IRS, "Table 1. Tax Rates on Income Other Than Personal Service Income..." (Rev. mayo 2023; PDF modificado el 8-may-2026): fila de México. https://www.irs.gov/pub/irs-lbi/tax-treaty-table-1.pdf
21. IRS, "Some nonresidents with U.S. assets must file estate tax returns". https://www.irs.gov/individuals/international-taxpayers/some-nonresidents-with-us-assets-must-file-estate-tax-returns · FAQ: https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-estate-taxes-for-nonresidents-not-citizens-of-the-united-states
22. IRS, "Estate & gift tax treaties (international)". https://www.irs.gov/businesses/small-businesses-self-employed/estate-gift-tax-treaties-international
23. Cámara de Diputados, *Ley del Impuesto sobre la Renta*, texto vigente, última reforma DOF 01-04-2024: arts. 119, 120, 126, 129, 140, 142 fr. II y V, y 152. https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf
24. SAT/DOF, Oficio 700-04-00-00-00-2025-060, *Listado de Prestadores de Servicios Digitales inscritos en el RFC* (DOF 25-jul-2025). http://omawww.sat.gob.mx/plataformastecnologicas/Paginas/PlataformasTecnologicas_ServiciosDigitales/documentos/Listado_de_Prestadores_de_Servicios_Digitales.pdf
25. BBVA México, "BBVA México reduce comisiones en transferencias internacionales..." (22-sep-2025). https://www.bbva.com/es/mx/innovacion/bbva-mexico-reduce-comisiones-en-transferencias-internacionales-y-elimina-cargos-por-retiros-de-efectivo-en-el-extranjero/
26. BBVA México, *Tarifas y comisiones*, tarifario general V.229 (PDF modificado el 13-ago-2026): servicios digitales (SPEI por banca por internet 5.00 MXN; SWIFT por banca móvil y por internet 20 USD; más IVA) y servicios en sucursal (recepción internacional 30 USD; más IVA). https://www.bbva.mx/content/dam/public-web/mexico/documents/tarifario-general/Tarifario.pdf
27. Santander, nota de prensa "Santander México primer banco en eliminar por completo la comisión en transferencias internacionales a través de la App" (2-oct-2025). https://www.santander.com/es/sala-de-comunicacion/notas-de-prensa/2025/10/santander-mexico-primer-banco-en-eliminar-por-completo-la-comision-en-transferencias-internacionales-a-traves-de-la-app
28. Banorte, "Envío de Transferencias Internacionales" (**403/503**; cifras de 30 USD + IVA por envío y 17 USD + IVA por recepción tomadas del resumen del buscador, **[S]**). https://www.banorte.com/Personal/Internacional/Pagos-Globales/Envio-de-Transferencias-Internacionales.html
29. Wise, API pública de precios (cotización de 20,000 MXN a USD; transferencia bancaria a transferencia bancaria: 193.84 MXN de comisión, 1,118.09 USD recibidos, TC medio 0.0564514). https://wise.com/gateway/v1/price?sourceAmount=20000&sourceCurrency=MXN&targetCurrency=USD
30. IBKR, "Order Types and Algos". https://www.interactivebrokers.com/en/trading/ordertypes.php
31. IBKR, cuotas de bolsa NYSE (Tiered). https://www.interactivebrokers.com/en/accounts/fees/NYSEstkfee.php?nhf=T
32. IBKR, "No Transaction Fee ETFs". https://www.interactivebrokers.com/en/trading/commission-free-etfs-mkt.php
33. **Secundarias:**
    - Finantres, "Comisiones de Interactive Brokers en México" (act. 16-sep-2026): 2 retiros gratis, luego 100 MXN; FX 0.20 pb con mín. 2 USD o ajuste de 0.03%. https://finantres.mx/comisiones-interactive-brokers/
    - Bogleheads, "IBKR – Regulatory Protection from outside developed countries" (usuario de México bajo IB LLC; solo resumen de búsqueda, la página dio 403). https://www.bogleheads.org/forum/viewtopic.php?t=396377
    - BrokerChooser, "Is Interactive Brokers Available to Investors in Mexico?" (403; solo resumen de búsqueda). https://brokerchooser.com/broker-reviews/interactive-brokers-review/interactive-brokers-mexico
    - TradersUnion, "Is Interactive Brokers Legal in Mexico?" (resumen de búsqueda). https://tradersunion.com/brokers/forex/view/interactive_brokers/is-regulated-in-mexico/
    - MatchMyBroker, "IBKR Currency Conversion Calculator". https://www.matchmybroker.com/articles/interactive-brokers-currency-conversion-guide
    - Financial Wisdom Forum, "Forex with IB" (odd lots de FX; resumen de búsqueda). https://www.financialwisdomforum.org/forum/viewtopic.php?t=122718
    - Resumen de búsqueda sobre *free-riding* en cuentas de efectivo (Wikipedia, "Freeriding (stocks)"). https://en.wikipedia.org/wiki/Freeriding_(stocks)
34. Internas: `arena/investigacion/brokers/B1-gbm-linea-base-.md` (línea base de GBM, TC 17.71, patrón de operación), `arena/investigacion/brokers/B2-casas-de-bolsa-y-apps-mexicanas.md`, `arena/investigacion/brokers/B4-fiscalidad-comparada-y-otros-brokers-extranjeros.md`, `arena/investigacion/01-gbm-operativa-y-costos.md`, `laboratorio/replicas/V05-spiva-y-fiscalidad-sic/` (`prerregistro.md`, `resultados.json` y `datos/legal/LISR.txt`, texto de la LISR con última reforma DOF 01-04-2024).

Fuentes añadidas en la verificación (consultadas el 2026-09-25):

35. SAT, *Anexo 7 de la Resolución Miscelánea Fiscal para 2026* (DOF 09-01-2026), criterio **37/ISR/N** "Acciones emitidas por sociedades extranjeras cotizadas en bolsas de valores concesionadas. Su enajenación está sujeta a la tasa del 10%". https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rmf/anexos/Anexo_7_RMF2026-09012026.pdf
36. IBKR FAQ, "What does the message 'Restricted: Complex or Leveraged Exchange Traded Product' mean?" (id 84620875) y la nota de la FAQ 28236881 sobre ese permiso. https://www.interactivebrokers.com/lib/cstools/faq/#/content/84620875
37. IBKR, "Configuring Your Account" (cuentas de efectivo con varias monedas; efectivo liquidado; texto sobre la transición de la regla PDT). https://www.interactivebrokers.com/en/accounts/configuring-your-account.php
38. IBKR FAQ, "Free riding rule" (id 1163245617; revisión en tiempo real de efectivo liquidado, 90 días de "Cash Up Front", cuenta de margen). https://www.interactivebrokers.com/lib/cstools/faq/#/content/1163245617
39. IBKR, "Prediction Markets" (Kalshi, CME y ForecastEx; elegibilidad por entidad y edad) y "Commissions – Prediction Markets" (Kalshi 0.01 + 0.01 USD; ForecastEx 0.00 + 0.01 USD; CME 0.01 + 0.01 USD). https://www.interactivebrokers.com/predictionmarkets/en/home.php · https://www.interactivebrokers.com/en/pricing/commissions-events.php
40. SEC, comunicado 2023-29 (15-feb-2023): acortamiento del ciclo de liquidación a T+1, con fecha de cumplimiento el 28-may-2024. https://www.sec.gov/newsroom/press-releases/2023-29
41. SAT, *Anexo 8 de la RMF 2026* (DOF 28-12-2025), sección C.II: tarifa anual 2026 de los arts. 97 y 152 LISR. https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rmf/anexos/Anexo-8-RMF-2026_DOF-28122025.pdf
