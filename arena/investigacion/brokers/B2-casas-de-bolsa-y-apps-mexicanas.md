# B2. Casas de bolsa y apps mexicanas contra GBM: costo neto para la cuenta arena

**Fecha de corte:** 2026-09-25 (todas las fuentes se consultaron ese día, salvo que se indique otra fecha).
**Verificación adversarial:** 2026-09-25. Correcciones hechas en el texto; el detalle está en "## Verificacion (2026-09-25)" al final.
**Frente:** B2 de `arena/investigacion/brokers/`. La línea base de GBM está en `B1-gbm-linea-base-.md` y en `../01-gbm-operativa-y-costos.md`. Aquí no se repite; solo se cita.
**Pregunta:** ¿qué casa de bolsa o app mexicana maximiza el rendimiento **neto** de una cuenta de ~20,000 MXN que compite en % contra IAs que se quedan en GBM?
**Alcance:** Actinver Trade (antes Bursanet), Kuspit, Finamex, BBVA, Banorte, Santander, Monex, Vector, Flink (hoy Webull México), Hapi, Revolut México y Hey X. También cubre el marco fiscal común (art. 129 LISR) y la calidad de servicio según la CONDUSEF.

**Etiquetas:**
- **[H]** Hecho con fuente y fecha.
- **[C]** Cálculo propio sobre hechos citados. El método está a la vista.
- **[I]** Inferencia.
- **[R]** Recomendación para la cuenta arena.
- **(no verificado)**: no lo confirmé en una fuente oficial, o solo aparece en fuentes secundarias o en resúmenes del buscador.

---

## Resumen ejecutivo

1. **[H] Correcciones a la premisa.**
   - **Bursanet no es de Monex.** Es la plataforma de Grupo Financiero Actinver y desde el 26-ago-2025 se llama **Actinver Trade** [1][4][5].
   - **Vector ya no es opción.** La Junta de Gobierno de la CNBV revocó su autorización como casa de bolsa en la sesión del 12-dic-2025, a petición de la propia Vector, y la puso en liquidación. Se hizo público el 16-dic-2025 [19][20][38]. Antes de eso, sus clientes locales habían pasado a Finamex (oct-2025) y la cartera internacional (VectorGlobal) a Insigneo [21][39].
   - **Flink ya no existe como marca.** Desde abril de 2025 es **Webull México** (Vifaru Casa de Bolsa para pesos y Webull Financial LLC para EUA) [22][24].
   - **Hapi no es casa de bolsa mexicana.** Es Hapi Securities LLC, un broker-dealer de EUA registrado en la SEC, que liquida con Apex [26][27].
2. **[H] Las casas mexicanas no retienen ISR cuando vendes acciones del SIC o de la BMV.** El art. 129 LISR no contiene ninguna obligación de retener en la venta (revisé el artículo completo). El intermediario **calcula** la ganancia o pérdida del año y **entrega la constancia**, y tú pagas el 10% definitivo en la declaración anual. Si hay pérdida, la puedes restar de ganancias del mismo tipo en ese año o en los **10 siguientes** [33]. La FAQ de Actinver Trade lo confirma para su caso: las ganancias "se declaran en el SAT y corresponden al 10%" [2]. **Dividendos:** en los mexicanos, la ley obliga a retener a la emisora (art. 140). En los del SIC, el art. 142 fr. V pone el 10% adicional **a cargo de la persona física** (entero a más tardar el día 17 del mes siguiente). GBM lo retiene según su FAQ (B1). Que Actinver, Kuspit o Finamex también lo retengan: **no verificado**. **[I]** Por eso cambiar de GBM a otra casa mexicana no cambia tu régimen fiscal.
3. **[H] Comisión por operación publicada en fuente oficial (persona física, monto chico):**

   | Bróker | Comisión por lado | Con IVA | Fuente |
   |---|---|---|---|
   | GBM (referencia) | 0.25% | **0.29%** | [36] |
   | Actinver Trade | 0.25% (0 a 1 MDP operado en 30 días) | **0.29%** | [1][2] |
   | Kuspit | **0.20%** | 0.232% si lleva IVA. La fuente oficial no dice si lleva IVA; **[I]** muy probable, porque la LIVA grava las comisiones de intermediación | [6][40] |
   | Finamex Trading | **0.06%** "sin importar el monto" | 0.0696% si lleva IVA | [9] |
   | BBVA Trader | 0.23% "*Comisión más IVA" (**corregido**; antes decía "incluyen IVA") | **0.267%** | [10] |

   **Pero:** Finamex cobra **86 MXN + IVA al mes** por información de mercado y **2% anual** de administración en contratos menores a 1 MDP [9]. BBVA Trader **solo acepta clientes de Banca Patrimonial y Privada** [10].
4. **[C] Costo de comisiones en la temporada de 6 meses para 20,000 MXN** (R = idas y vueltas completas de la cuenta; §3):

   | R | GBM | Actinver Trade (con el mes gratis) | Kuspit (con IVA) | Finamex Trading |
   |---|---|---|---|---|
   | 6 (1 al mes) | 696 (3.48%) | 580 (2.90%) | **557 (2.78%)** | 998 (4.99%) |
   | 9 (1.5 al mes) | 1,044 (5.22%) | 870 (4.35%) | **835 (4.18%)** | 1,081 (5.41%) |
   | 12 (2 al mes) | 1,392 (6.96%) | 1,160 (5.80%) | 1,114 (5.57%) | 1,165 (5.82%) |
   | 18 (3 al mes) | 2,088 (10.4%) | 1,740 (8.70%) | 1,670 (8.35%) | **1,332 (6.66%)** |

   **[I] La ventaja máxima contra GBM con el ritmo presupuestado (R = 6 a 9) es de ~0.6 a 1.0 puntos porcentuales en toda la temporada.** Es real, pero chica: un solo buen o mal trade la borra. Finamex solo le gana a GBM a partir de ~9.4 idas y vueltas, y a Kuspit a partir de ~12.8.
5. **[H] Actinver Trade da "un mes sin comisiones en el mercado de capitales" si el primer depósito es de más de 10,000 MXN, y el W-8BEN es gratis** [2][3]. Según los términos de la edición 2024 (los de 2026 no están publicados): el depósito debe ir **al contrato de Casa de Bolsa, no al de Banco**, en una sola exhibición y dentro de los 90 días posteriores a la apertura. Son **30 días naturales** contados desde el correo de confirmación, con un tope de 1,000 operaciones, y solo para clientes nuevos [41]. En GBM el W-8BEN del SIC cuesta 75 USD + IVA (B1). La custodia y la administración cuestan 0 según la guía vigente, versión 26.1.3, en vigor desde el 22-jul-2026 [1].
6. **[H] Kuspit cobra 0.20% por operación y no cobra el mantenimiento de un mes si la rotación del portafolio de capitales en ese mes supera el valor del portafolio** [6]. **El monto del mantenimiento no está en ninguna tarifa oficial accesible.** La guía de servicios de Kuspit (`G_Serv_Inv_Kuspit.pdf`) está en un puerto que no se pudo alcanzar. La cuenta oficial de Kuspit en X dijo "0.99% anual del valor de tu portafolio", cobrado cada mes (feb-2018) [42]. En mar-2024, la misma cuenta anunció "Comisión Mantenimiento = 0%" [8]. Rankia (abr-2026) sigue citando 0.99% [7]. **Hay contradicción entre canales oficiales; supuesto prudente: 0.99% anual en los meses sin rotación.** En la ficha oficial de la App Store, Kuspit Casa de Bolsa dice "más de 3,500 opciones" [43]. **[I]** Eso solo cuadra si incluye el SIC. Aun así, **qué ETFs concretos tiene (TQQQ, SOXL o SPXL) y qué tipos de órdenes permite (stop, OCA): no verificado**. Es justo lo que decide si sirve para la estrategia.
7. **[H] Calidad de servicio (CONDUSEF, IDATU 4T-2025, publicado el 17-abr-2026):** el promedio del sector fue 8.9. Las tres peores fueron **GBM (7.00)**, Finamex (7.48) y BBVA México Casa de Bolsa (7.93). Casa de Bolsa Banorte sacó 10 [32]. Actinver y Kuspit no aparecen en el comunicado.
8. **[H] Descartadas para 20k:**
   - **BBVA Trader:** exige ser cliente patrimonial. El umbral de ~5 MDP solo sale en fuentes secundarias (no verificado) [10][13].
   - **Monex Trader:** está en la sección de Banca Privada. La guía dice "hasta 1.70%" por operación (visto en un resumen de búsqueda; el sitio dio 403) [17][18].
   - **Santander:** no publica tarifa; se pacta en el contrato [15]. Su guía dio 403 [16].
   - **Banorte BeTrading:** la comisión solo aparece en el panel de confirmación, y la profundidad de libro cuesta 700 MXN + IVA al mes [14]. El sitio dio 503.
   - **Vector:** revocada [19][38].
   - **Hey X:** su lanzamiento, previsto para el 15-jun-2026, quedó pospuesto por observaciones de la CNBV. El comunicado oficial de Hey Banco (5-jun-2026) no da nueva fecha [31][44]. No encontré que haya lanzado al 25-sep-2026.
   - **AcciTrade (Banamex/Accival), agregada en la verificación:** 0.35% + IVA por operación y apertura mínima de 100,000 MXN, según fuentes secundarias (Finantres, sep-2026; Rankia). La página oficial de requisitos no devolvió contenido: **no verificado** [45]. Es más cara que GBM de todos modos.
9. **[I] Webull México, Hapi y Revolut son en realidad la ruta del "bróker extranjero"**: compras directas en NYSE/Nasdaq, con custodia en EUA y conversión MXN→USD. **[H]** La portada oficial de Webull México (consultada el 25-sep-2026) dice que con Vifaru Casa de Bolsa "depositas tu dinero en pesos [...] y operas reportos o bien, compras dólares", y que la compraventa de valores de EUA la hace Webull Financial LLC [22]. **[I]** No ofrece acciones de la BMV ni del SIC, lo cual coincide con Rankia [25]. Ninguna de las tres publica su margen cambiario, y ninguna es la vía SIC. Ese análisis corresponde al frente de brókers extranjeros, no a este.
10. **[R] Veredicto de B2** (condicionado a tres verificaciones en la app; §6):
    - **Primera opción, Kuspit.** Es la comisión oficial más baja sin cargos fijos cuando la cuenta rota ≥1 vez al mes. Solo sirve si tiene habilitados los ETFs del SIC que usa la estrategia y si acepta órdenes stop. **Verificación:** en la primera temporada, su ventaja sobre Actinver es de solo ~0.12 pp (R = 6), y se invierte si cobra el mantenimiento de 0.99% (§3). Sin confirmación escrita del IVA, el mantenimiento y las órdenes, gana Actinver.
    - **Segunda opción, Actinver Trade.** Cobra lo mismo que GBM, pero da un mes gratis, el W-8BEN gratis y la custodia en 0, y es un grupo financiero grande. **Es la opción más segura si Kuspit falla la verificación.**
    - **Finamex** solo tiene sentido si la cuenta va a rotar más de ~10 veces en la temporada. Eso va contra el presupuesto de rotación de A1.
    - **[I] Ninguna casa mexicana cambia el juego.** Ganan ≤1 punto por temporada con el ritmo presupuestado, así que la decisión se define por catálogo, tipos de orden y estabilidad, no por comisión.

---

## 1. Quién es quién (entidad, regulación y estado en 2026)

| Nombre comercial | Entidad que presta el servicio | Tipo | Estado al 2026-09-25 | Fuente |
|---|---|---|---|---|
| GBM | GBM Casa de Bolsa | Casa de bolsa (CNBV) | Activa. Línea base | B1 |
| **Actinver Trade** (antes Bursanet) | "Actinver Trade Casa de Bolsa" dentro de Grupo Financiero Actinver. La guía clasifica a Bursanet como "Servicios de inversión no asesorados" | Casa de bolsa (CNBV, SHCP, Banxico según su FAQ). La cuenta bancaria integrada tiene IPAB; los valores no | Activa. Cambió de nombre el 26-ago-2025 | [1][2][5] |
| **Kuspit** | Kuspit Casa de Bolsa, S.A. de C.V. Autorizada por la CNBV con el oficio 210-90283/2010, publicado en el DOF el 31-ene-2011 (**corregido**: antes decía "por la SHCP"). No da asesoría: solo ejecución | Casa de bolsa (CNBV) | Activa. La app de iOS se actualizó por última vez en sep-2026 (v1.3.28) [43] | [6] |
| **Finamex Trading** | Casa de Bolsa Finamex | Casa de bolsa (CNBV) | Activa. Absorbió ~30,000 cuentas de Vector (nota de oct-2025) | [9][21] |
| **BBVA Trader** | BBVA México (Casa de Bolsa BBVA México en el ranking de CONDUSEF) | Banco / casa de bolsa | Activa, **solo para Banca Patrimonial y Privada** | [10][11][32] |
| **Banorte BeTrading** | Casa de Bolsa Banorte | Casa de bolsa (CNBV) | Activa | [14][32] |
| **Santander** (SuperNet / SuperTrader) | Casa de Bolsa Santander | Casa de bolsa (CNBV) | Activa; tarifa no pública | [15] |
| **Monex Trader** | Monex Casa de Bolsa | Casa de bolsa (CNBV) | Activa; en la sección de Banca Privada | [17][18] |
| **Vector / e-Vector** | Vector Casa de Bolsa | — | **Autorización revocada** (sesión de la Junta de Gobierno de la CNBV del 12-dic-2025; pública el 16-dic-2025), en liquidación | [19][20][38] |
| **Webull México** (antes Flink) | Vifaru, S.A. de C.V., Casa de Bolsa (operaciones en pesos) + Webull Financial LLC (EUA; SEC, FINRA, SIPC) | Mixta: casa de bolsa mexicana + broker-dealer de EUA | Activa. Su oferta visible es acciones, opciones, ETFs y futuros **de EUA** | [22][24][25] |
| **Hapi** | Hapi Securities LLC (SEC, FINRA CRD #311868, SIPC); liquidación con Apex Clearing | **Broker-dealer extranjero**, sin autorización de casa de bolsa en México | Activa | [26][27] |
| **Revolut México** | Revolut Bank, S.A., Institución de Banca Múltiple. Según el resumen de su página oficial, la ejecución la hace "Revolut Securities Singapore Pte" | Banco mexicano + ejecutor extranjero | Activa (acciones de EUA) (detalle no verificado; el sitio dio 403) | [28][30] |
| **Hey X** (Hey Banco) | Hey Banco. Se iba a operar con Apex Fintech y referenciación de Admino | Banco | **No lanzado**: pospuesto tras observaciones de la CNBV (jun-2026) | [31] |

**Qué implica cada tipo [I]:**
- **Casa de bolsa mexicana (CNBV):** custodia en Indeval, acceso al SIC en pesos, régimen del art. 129 con constancia anual [33]. **El IPAB no cubre casas de bolsa** (A1 §9). Los valores están a nombre del cliente en Indeval.
- **Broker-dealer extranjero (Hapi, la parte de EUA de Webull, y aparentemente Revolut):** custodia fuera de México, protección SIPC hasta los límites de EUA [26], sin constancia mexicana del art. 129 (no verificado para cada uno) y con W-8BEN. ~~La fracción I del art. 129 exige que la venta se haga en bolsas concesionadas conforme a la LMV [33], así que la venta directa en NYSE/Nasdaq probablemente no entra ahí (inferencia; lo trata el frente de brókers extranjeros).~~ **Corregido el 2026-09-25 (ver B4 §1.2 y `../05-comparativa-brokers.md`):** para **acciones extranjeras listadas en el SIC**, el criterio normativo 37/ISR/N (Anexo 7 RMF 2026, DOF 09-01-2026) aplica el 10% del art. 129 fr. I "con independencia de que su enajenación no se realice a través de un intermediario del mercado de valores mexicano". Siguen abiertos los ETFs vendidos fuera de México y los valores no listados en el SIC (B4 §1.3–1.4).

---

## 2. Tabla comparativa (persona física, cuenta de ~20,000 MXN)

| Bróker | Comisión por lado (fuente oficial) | Mínimo por orden | Custodia y cuotas fijas | Apertura mínima | SIC (catálogo declarado) | Fracciones | W-8BEN | Órdenes stop/OCA | Verificación |
|---|---|---|---|---|---|---|---|---|---|
| **GBM** (B1) | 0.25% + IVA = 0.29% | Ninguno oficial | 0 | 100 MXN | No publica catálogo del SIC; totales ">5,000"/">6,000" mezclados | No en el SIC | 75 USD + IVA | **Sí** (Stop, Stop limitada, Trailing, OCA, OTA) | Oficial (B1, A1) |
| **Actinver Trade** | 0.25% (0–1 MDP en 30 días), 0.20%, 0.15% y 0.10% arriba; "A todos los cobros [...] se les agrega el importe calculado de I.V.A." [1][2] | La guía vigente (26.1.3) sigue listando "Comisiones mínimas por compraventa de acciones" como un beneficio, sin cifra [1] (**ambiguo; no verificado**) | **0**: "Custodia INDEVAL $0.00", "Administración de cuenta $0.00", "Información en línea de BMV $0.00", sin anualidad. SPEI sin costo; transferencia internacional de 6 USD [1][2] | Primer depósito de 1,000 MXN. La cuenta abierta desde la app (Nivel 2) tiene un tope de depósitos **y transferencias** de 3,000 UDIS al mes (~26,500 MXN con la UDI de ~8.85 [46]). SPEI nocturno o de fin de semana: máximo 1,500 UDIS por operación [2] | "Cientos de Acciones de empresas nacionales e internacionales (SIC)" [2]; "más de 3,000 acciones nacionales e internacionales" (El Financiero) [5] | No: "puedes comprar desde una sola Acción" [2] | **Gratis**, pero hay que entregar el original en Montes Urales 620, CDMX [2] | Stop loss: la cuenta oficial en X (feb-2022, como Bursanet) explicaba "cómo colocar un stop loss en tus órdenes de compra" [47]. OCA y trailing: no verificado | Oficial (guía 26.1.3, en vigor desde el 22-jul-2026, y FAQ) |
| **Kuspit** | **0.20%** "Mercado de capitales = 0.20% por operación" [6]; "0.20% en todas tus operaciones" (App Store) [43]. IVA no indicado | "Sin importar el monto" [6] | "No cobra ninguna comisión por administración y custodia" [6]. **Mantenimiento: no se cobra el mes en que la rotación supera el valor del portafolio** [6]. Su tasa: 0.99% anual según Kuspit en X (2018) [42] y Rankia (2026) [7], pero "0%" según Kuspit en X (2024) [8]; **contradictorio** | 100 MXN [6]. Apertura gratis y fondeo por SPEI [6]; costo de retiro no publicado | "Más de 3,500 opciones" (App Store oficial) [43]. **[I]** Incluye el SIC. Los tickers concretos no están verificados (la API pide token) | No verificado | No verificado | No verificado (las enumeraciones de stop del código web son de la librería de gráficos TradingView, no de órdenes de Kuspit) | Oficial (kuspit.com y App Store) + secundaria |
| **Finamex Trading** | **0.06%** "sin importar el monto que operes" [9] | Ninguno mencionado | **86 MXN + IVA al mes** (información de mercado) + administración de **2% anual** (contratos < 1 MDP; 1% arriba) [9] | **10,000 MXN** [9] | "Más de 2,200 acciones y ETF's", BMV + SIC [9] | No verificado | No verificado | No verificado | Oficial (FAQ de Finamex Trading) |
| **BBVA Trader** | 0.23% (< 1 MDP), 0.18% y 0.10% arriba; "*Comisión más IVA" [10] (**corregido**: antes decía "incluyen IVA"; queda en 0.267% con IVA) | No publicado | La guía del banco menciona "supervisión y custodia" de **200 MXN + IVA al mes**, "en su caso", y custodia de 0.105 al millar [12] (vigencia de la guía no verificada) | **Cliente de Banca Patrimonial y Privada** [10] | "Más de 4,700 instrumentos a nivel global" [11] | No verificado | No verificado | No verificado | Oficial (requisito y tarifa); cuotas ambiguas |
| **Banorte BeTrading** | "Sólo se cobra una comisión de corretaje", visible en el panel de confirmación [14] | No publicado | Contratación sin costo; profundidad de libro 700 MXN + IVA al mes [14] | No publicado | Nacional + SIC [14] | No verificado | No verificado | No verificado | Solo el resumen del buscador de la página oficial (el sitio dio 503) |
| **Santander** | "Se pactan en el contrato"; no hay tarifa pública [15] | — | — | — | — | — | — | — | Secundaria; guía oficial con 403 [16] |
| **Monex Trader** | "Hasta 1.70% por operación más IVA" (guía V.4, citada en un resumen de búsqueda) [17] | — | — | Enfoque de banca privada [18] | Nacional + SIC [18] | — | — | — | No verificado (403) |
| **Vector** | — | — | — | — | — | — | — | — | **Revocada** [19] |
| **Webull México** | "Cero comisiones" en acciones y ETFs de EUA; pueden aplicar cargos regulatorios y de cambio [22][24] | — | Sin depósito mínimo [22] | "Cualquier cantidad" [22] | **No es vía SIC.** Según Rankia, no permite comprar acciones mexicanas [25] (no verificado) | "Cuando estén disponibles" [24] | Aplica (EUA) [24] | No verificado | Oficial (portada) + secundaria |
| **Hapi** | 0 de comisión, más una "clearing house fee" de 0.10 USD por trade de títulos completos y 0.15 USD por fracciones (usuarios regulares); 2.99 USD en horario extendido o nocturno [27] | Implícito en la cuota fija | Inactividad de 4.99 USD al mes, solo en cuentas con 60 días sin actividad y saldo de más de 0 y menos de 100 USD; Prime a 9.99 USD al mes. El costo de depósito "se muestra en la app" [27]. FINRA BrokerCheck: CRD 311868, activa [48] | — | **No es vía SIC** (EUA directo) | **Sí** [26] | EUA | No verificado | Oficial (fee schedule, PDF del 29-abr-2026) |
| **Revolut México** | Plan Estándar: "1 operación sin comisión por mes"; la comisión después no está verificada [28] | — | Custodia 0 (resumen) [28] | — | **No es vía SIC** (EUA directo) | Sí (secundaria) [30] | — | No verificado | Resumen del buscador de la página oficial (403) |

**Tipo de cambio en el SIC [H/I]:**
- **[H]** En el SIC todo cotiza y se liquida en pesos. El precio en MXN equivale a (precio en EUA × tipo de cambio) más la desviación del libro local, que se mide en B1 §3.1 y A2 §9.
- **[I]** Las casas mexicanas **no cobran un margen cambiario aparte** en el SIC. El costo cambiario está metido en la desviación del libro, y el libro es el mismo para todos los intermediarios (BMV/BIVA). Ninguna de las guías que revisé publica un margen cambiario para el SIC [1][9][12].
- **(no verificado)** Si alguna ejecuta el SIC "por excepción" contra su propio precio, como documenta GBM (A1 §2.3), y si eso mejora o empeora la ejecución.
- **[H]** En Actinver Trade, los dividendos de emisoras del SIC normalmente se pagan en USD y quedan en el apartado de efectivo en dólares. Para disponer de ellos hay que llamar al centro de atención [2]. La compraventa de divisas "no aplica el pago de ningún tipo de comisión" [2], pero **el diferencial cambiario no está publicado (no verificado)**.
- **[H]** En Actinver Trade, lo que entra por una venta de acciones se invierte automáticamente en el fondo ACTIREN. Para retirar por SPEI hay que vender el fondo antes de las 13:30 [2]. **[I]** El efectivo ocioso rinde algo, pero agrega un paso para retirar. La comisión de ese fondo no está verificada.
- **[H]** Finamex Trading incluye la "operación de tipo de cambio peso-dólar" en su oferta [9]. Su diferencial: no verificado.

**Catálogo del SIC [I]:** B1 §4.1 tiene el tamaño del SIC en la BMV (1,676 acciones y 1,404 ETFs, sep-2023). Un valor listado en el SIC lo puede operar cualquier inversionista a través de un intermediario [35]. Ninguna de estas casas publica qué emisoras tiene **habilitadas** en su app (Actinver dice "cientos" [2], Finamex ">2,200" [9], BBVA ">4,700 instrumentos" [11], y Kuspit no publica). **La diferencia real de catálogo solo se puede medir buscando los tickers en cada app** (§6).

---

## 3. Costo de la temporada para la cuenta de 20,000 MXN [C]

**Supuestos:**
- Capital de 20,000 MXN. Temporada de 6 meses.
- R = número de idas y vueltas completas del capital. El volumen total operado es 2 × 20,000 × R.
- IVA de 16% sobre toda comisión, BBVA incluida (**corregido en la verificación**: su página dice "*Comisión más IVA").
- La desviación del libro del SIC es igual en todos, así que no cambia la comparación y no se incluye.

**Fórmulas:**
- **GBM:** 0.29% × volumen.
- **Actinver Trade:** igual que GBM, pero con el primer mes gratis. Con actividad uniforme, eso son 5/6 del costo de GBM.
- **Kuspit:** 0.232% × volumen si lleva IVA; 0.20% si no. Sin mantenimiento, porque con R ≥ 6 la rotación mensual (compras + ventas) supera al portafolio [6].
- **Finamex:** 0.0696% × volumen + 86 × 1.16 × 6 = 598.56 de información + 2% × 20,000 × 0.5 × 1.16 = 232 de administración. Son **830.56 MXN fijos (4.15% del capital)**.

| R en la temporada | GBM | Actinver Trade (con el mes gratis) | Kuspit (con IVA) | Kuspit (sin IVA) | Finamex | BBVA Trader* (0.267%, corregido) |
|---|---|---|---|---|---|---|
| 3 | 348 (1.74%) | 290 (1.45%) | 278 (1.39%) | 240 (1.20%) | 914 (4.57%) | 320 (1.60%) |
| **6** | **696 (3.48%)** | 580 (2.90%) | 557 (2.78%) | 480 (2.40%) | 998 (4.99%) | 640 (3.20%) |
| 9 | 1,044 (5.22%) | 870 (4.35%) | 835 (4.18%) | 720 (3.60%) | 1,081 (5.41%) | 960 (4.80%) |
| 12 | 1,392 (6.96%) | 1,160 (5.80%) | 1,114 (5.57%) | 960 (4.80%) | 1,165 (5.82%) | 1,281 (6.40%) |
| 18 | 2,088 (10.44%) | 1,740 (8.70%) | 1,670 (8.35%) | 1,440 (7.20%) | 1,332 (6.66%) | 1,921 (9.60%) |

\* **BBVA Trader no es accesible con 20k.** Además, si aplicara la cuota de supervisión de 200 MXN + IVA al mes, sumaría **1,392 MXN (6.96%) en la temporada** [12]. La columna se recalculó en la verificación con 0.23% × 1.16. Antes decía 0.23% "con IVA incluido" (276 / 552 / 828 / 1,104 / 1,656). Las otras columnas se recalcularon y cuadran al peso.

**Puntos de equilibrio [C]:**
- **Finamex contra GBM:** R = 830.56 / (40,000 × (0.0029 − 0.000696)) = **9.4 idas y vueltas**.
- **Finamex contra Kuspit con IVA:** **12.8**. Contra Kuspit sin IVA: **15.9**.
- **Kuspit contra GBM con R = 6:** ahorra **139 MXN = 0.70 pp** de rendimiento en la temporada. Con R = 12 ahorra 1.39 pp.
- **Kuspit con mantenimiento:** si la rotación de un mes no supera el portafolio y se cobra el 0.99% anual (Kuspit en X, 2018; Rankia, 2026), la temporada suma hasta 99 MXN (115 con IVA) = 0.57%. Con R ≤ 3 casi borra la ventaja contra GBM. **Ojo con la definición de "rotación":** si Kuspit la mide con un solo lado (solo ventas o solo compras), una ida y vuelta al mes da una rotación de 1.0× y **no** es "mayor al valor del portafolio". Entonces se cobraría el mantenimiento aun con R = 6 (**[I]**; la definición no está verificada).

- **[C] Kuspit contra Actinver Trade (agregado en la verificación).** Kuspit con IVA cuesta 92.8 × R MXN por temporada; Actinver con el mes gratis cuesta 96.7 × R.
  - **Sin mantenimiento**, Kuspit ahorra apenas **3.9 × R MXN** en la primera temporada: 23 MXN (**0.12 pp**) con R = 6 y 35 MXN (0.17 pp) con R = 9.
  - **Si se cobra el mantenimiento los 6 meses** (+114.84 MXN), Actinver sale más barato para cualquier R < ~30 en la primera temporada: 580 contra 672 con R = 6, y 870 contra 950 con R = 9. Aun así, Kuspit le gana a GBM (672 contra 696).
  - **A partir de la segunda temporada**, Actinver ya no tiene mes gratis y cuesta lo mismo que GBM. Kuspit le ahorra 0.12 pp (con mantenimiento) a 0.70 pp (sin mantenimiento) con R = 6.

**[I] Lectura:**
- Con el presupuesto de rotación de A1 (≤ 1–1.5 idas y vueltas al mes, R = 6 a 9), **Kuspit y Actinver Trade le ahorran a la cuenta ~0.6 a 1.0 pp por temporada frente a GBM.** Finamex sale más caro.
- Todos los números son **solo comisión**. La desviación del libro del SIC (~0.1%–0.25% por lado en ETFs líquidos, B1) pesa igual o más que la diferencia de comisiones y no cambia entre casas mexicanas.

---

## 4. Impuestos, retención y constancia (igual para todas las casas mexicanas)

- **[H] Art. 129 LISR** (texto de la Cámara de Diputados, última reforma DOF 01-04-2024) [33]:
  - El 10% definitivo aplica a la enajenación de acciones mexicanas "o de acciones emitidas por sociedades extranjeras cotizadas en dichas bolsas de valores" (fr. I) y de títulos que representen índices accionarios (fr. II), siempre que se vendan en bolsas concesionadas conforme a la LMV.
  - La ganancia o pérdida se suma por cada intermediario del mercado de valores "con los que opere o entidades financieras extranjeras con los que tenga un contrato de intermediación".
  - "Las entidades financieras autorizadas conforme a la Ley del Mercado de Valores para actuar como intermediarios [...] deberán hacer el cálculo de la ganancia o pérdida del ejercicio" y entregarlo al contribuyente. Si hay pérdida, "deberán emitir [...] una constancia de dicha pérdida".
  - Si el cliente cambia de intermediario, el anterior entrega al nuevo el costo promedio actualizado.
  - Las pérdidas se restan "contra el monto de la ganancia [...] en el ejercicio o en los diez siguientes".
- **[H] El art. 129 no tiene ninguna disposición de retención** (revisé el artículo completo en la copia local, del "Artículo 129." al "Artículo 130."). Solo obliga al intermediario a calcular y a expedir constancias "por contrato de intermediación" [33].
- **[I] Consecuencia para la decisión:** Actinver Trade, Kuspit, Finamex, Banorte, BBVA y Santander tienen el mismo régimen que GBM. Ninguna retiene ISR en la venta y todas deben calcular y entregar la constancia. Actinver Trade la entrega en el portal ("Estados de Cuenta" → "Constancia Fiscal") [2]. **Dividendos:** los mexicanos los retiene la emisora (art. 140). En los del SIC, el art. 142 fr. V obliga a la **persona física** a enterar el 10% adicional a más tardar el día 17 del mes siguiente. GBM lo retiene por el cliente (B1 §5). Que las otras casas hagan lo mismo: **no verificado**. Si alguna no lo hace, la obligación mensual queda a cargo del dueño. Si la cuenta arena se abre en otra casa mexicana, el dueño tendrá **dos constancias** (GBM y la nueva) y suma ambos resultados en su declaración [33].
- **[H] (verificado en la revisión)** La LISR no tiene reformas posteriores al 01-04-2024. La página de la Cámara de Diputados, consultada el 25-sep-2026, dice "Última reforma publicada en el Diario Oficial de la Federación el 1 de abril de 2024" [49]. Coincide con `conocimiento/27-fiscalidad-2026-y-estructura-sic.md` (el Paquete 2026 no reformó la LISR).
- **[H] W-8BEN:** gratis en Actinver Trade, pero "debe entregarse el original en Montes Urales 620" (CDMX), lo que implica mensajería o ir en persona [2]. En GBM cuesta 75 USD + IVA para el SIC (B1). **[C]** Con 20k no se paga solo en GBM (B1 §5). En Actinver Trade sí conviene, porque cuesta 0 y baja la retención de EUA sobre dividendos del SIC de 30% a 10% (esa tasa es de B1; que Actinver la aplique así: no verificado).

---

## 5. Calidad de la app, servicio e incidentes

| Bróker | Evidencia | Tipo | Fuente |
|---|---|---|---|
| GBM | IDATU 4T-2025: **7.00**, el más bajo del sector. Caídas documentadas en 2024-2025 y multas de la CNBV (B1 §7) | Oficial (CONDUSEF) | [32], B1 |
| Finamex | IDATU 4T-2025: **7.48** (segundo más bajo) | Oficial | [32] |
| BBVA México Casa de Bolsa | IDATU 4T-2025: **7.93** | Oficial | [32] |
| Casa de Bolsa Banorte | IDATU 4T-2025: **10** (entre las mejores, junto con Merrill Lynch y Goldman Sachs; Multiva 9.89, Morgan Stanley 9.86). Todas las cifras de la CONDUSEF se re-verificaron el 25-sep-2026 | Oficial | [32] |
| Actinver Trade | 4.2 en Google Play; reseñas de caídas y lentitud en la app (sin fechas precisas) | Secundaria / anecdótica | [23] |
| Kuspit | Una falla del portal web en 2018 (en X); no encontré notas de prensa de 2025-2026. Finantres la califica de "interfaz desactualizada" y con "herramientas limitadas para traders activos" | Anecdótica / secundaria | búsqueda del 2026-09-25, [37] |
| Vector, Intercam, CIBanco | Señalados por FinCEN el 25-jun-2025. Vector: licencia revocada (16-dic-2025). Intercam: operaciones vendidas a Kapital Bank (anuncio de la CNBV del 19-ago-2025, según resumen de búsqueda; no verificado en la fuente primaria) | Prensa | [19][20] |
| Hey X | La CNBV frenó el lanzamiento (jun-2026) | Prensa | [31] |

- **[I]** El IDATU mide la atención a reclamaciones, no la disponibilidad de la plataforma. Aun así, **GBM tiene la peor calificación del sector**, y una alternativa no queda en desventaja por servicio. De Actinver y Kuspit no hay dato de IDATU en el comunicado.
- **(no verificado)** No existe ningún registro público de caídas de Actinver Trade ni de Kuspit comparable con las de GBM del 7-abr-2025.

---

## 6. Veredicto y qué verificar antes de mover dinero

### 6.1 Ranking de B2 para "ganar más dinero neto" [R]

1. **Kuspit**, si pasa la verificación. Tiene la comisión oficial más baja sin cargos fijos (0.20%), no cobra mantenimiento si la cuenta rota más que su valor en el mes y abre desde 100 MXN. Ahorra ~0.7 pp contra GBM con R = 6. **Riesgos:** catálogo del SIC, tipos de orden y robustez para operar activamente, todos sin verificar. **Matiz de la verificación [C]:** en la primera temporada, su ventaja sobre Actinver Trade es de solo ~0.12 pp con R = 6, y **se invierte** si Kuspit cobra el mantenimiento (monto y definición de "rotación" contradictorios en sus canales oficiales; §3). **[R]** Si en la app Kuspit no confirma por escrito el IVA, el mantenimiento y los tipos de orden, **Actinver Trade pasa a primer lugar** para la primera temporada.
2. **Actinver Trade**, la opción más segura. Tiene la misma tarifa que GBM, con 30 días naturales sin comisiones (primer depósito ≥ 10,000 MXN **al contrato de Casa de Bolsa**, en una sola exhibición [41]), W-8BEN gratis (hay que entregar el original en CDMX), custodia en 0, dividendos del SIC en USD y respaldo de un grupo financiero con banco. Ahorra ~0.6 pp contra GBM con R = 6, casi todo por el mes gratis. Tiene stop loss según su cuenta oficial (2022) [47]. **Ojo: la cuenta debe ser Actinver Trade, no Casa de Bolsa Actinver con asesor.** En la asesorada, la guía vigente (26.1.3) marca corretaje de 0.75% con saldo < 500 mil, **mínimo de 200 MXN + IVA por operación**, custodia de 50 MXN + IVA al mes, 100 MXN al mes con saldo < 5,000 y **anualidad de 2,100 MXN + IVA** (Banca Patrimonial) [1].
3. **Finamex Trading**, solo si la cuenta va a rotar más de ~10 veces en la temporada. Con el presupuesto de A1 pierde contra GBM.
4. **Descartadas para 20k:** BBVA Trader (requisito patrimonial), Monex, Santander y Banorte (sin tarifa pública verificable), Vector (revocada) y Hey X (no lanzado).
5. **Fuera de B2:** Webull México, Hapi y Revolut. Operan EUA directo con custodia extranjera y pertenecen al frente del bróker extranjero, junto con Interactive Brokers.

**[I] Mensaje central para el dueño:** entre las casas mexicanas, cambiar de GBM rinde a lo mucho ~1 punto por temporada con la operación presupuestada. Es dinero de verdad, pero **no compensa quedarse sin los ETFs del SIC que usa la estrategia ni sin órdenes stop**. Por eso el orden final depende de la verificación de abajo.

### 6.2 Verificación en la app antes de fondear (por bróker candidato)

1. **Catálogo:** buscar TQQQ, SOXL, SPXL, QLD, SMH, SOXX, QQQM, SPLG/SPYM, GLD, IAU y EWW. Anotar si aparecen, si se pueden comprar y si la app pide un perfil o una carta.
2. **Órdenes:** revisar si la app acepta stop, stop limitada, trailing y OCA en valores del SIC, y qué vigencia máxima tienen.
3. **Costo real:** poner una orden de prueba de ~2,000 MXN y leer en la confirmación la comisión, el IVA y si hay algún mínimo.
   - En **Kuspit:** confirmar si el 0.20% lleva IVA, si el mantenimiento existe hoy (0.99% o 0%; los canales oficiales se contradicen) y cómo calcula la "rotación" que lo exenta (¿compras + ventas, o un solo lado?). Pedir la guía de servicios vigente (`G_Serv_Inv_Kuspit.pdf`), que no se pudo descargar.
   - En **Actinver Trade:** confirmar que no hay comisión mínima, que la promoción de 30 días sigue vigente en 2026 (solo se localizaron los términos de 2024) y que el depósito de 20,000 MXN se aplica **al contrato de Casa de Bolsa** en una sola exhibición [41].
4. **Límite de la cuenta:** en Actinver Trade, la cuenta abierta desde la app (Nivel 2) tiene un tope de depósitos y transferencias de 3,000 UDIS al mes [2]. Con la UDI en ~8.85 MXN (Banxico SIE, 8-10 oct 2026: 8.8496–8.8535 [46]) son **~26,500 MXN**. Los 20,000 caben, pero con poco margen para aportar más en el mismo mes. Entre 17:31 y 05:59 y en fines de semana, el SPEI tiene un tope de 1,500 UDIS (~13,300 MXN) por operación: conviene fondear en horario hábil [2]. Si se quiere margen, conviene abrir la Nivel 4 desde el sitio web (el cambio de nivel no tiene costo [2]).
5. **Constancia:** confirmar en la FAQ o por chat que entregan la constancia anual del art. 129 por contrato.

### 6.3 Comparabilidad en la competencia [R]

- Todas las réplicas y pruebas actuales usan **0.29% por lado (GBM)**. Si la cuenta se muda:
  - **Kuspit:** recalcular con **0.232%** por lado (0.20% si se confirma que no lleva IVA), más el mantenimiento en los meses sin rotación.
  - **Actinver Trade:** 0.29%, con **0% el primer mes**.
- En la bitácora del torneo se anota, **por operación**, la diferencia de costo contra GBM (por ejemplo, Kuspit: −0.058 pp por lado; Actinver en el mes gratis: −0.29 pp por lado). Así el marcador se puede reportar también "a costos de GBM" y la comparación con las IAs que siguen en GBM sigue siendo justa.
- La desviación del libro del SIC no cambia entre casas mexicanas (§2), así que no hace falta ajustarla.

---

## 7. No verificado (lista consolidada)

- **Kuspit:** si el 0.20% lleva IVA (**[I]** probable); el monto vigente del mantenimiento (0.99% anual en X 2018 y Rankia 2026, contra "0%" en X 2024; la guía oficial no se pudo descargar); la definición exacta de "rotación"; qué tickers del SIC tiene (el total de "más de 3,500 opciones" sí es oficial); los tipos de orden; las fracciones; el costo del W-8BEN; el costo de retiro; la retención del 10% sobre dividendos del SIC.
- **Actinver Trade:** qué significa "Comisiones mínimas por compraventa de acciones" en la guía 26.1.3 (¿hay un mínimo en pesos?); OCA y trailing (el stop loss sí aparece en su cuenta oficial, 2022); el catálogo exacto del SIC; los términos 2026 de la promoción de 30 días (solo se localizaron los de 2024); el diferencial cambiario al convertir dividendos en USD; la comisión del fondo ACTIREN; la retención del 10% sobre dividendos del SIC.
- **Finamex:** si el 0.06% y el 2% anual llevan IVA; los tipos de orden; el catálogo real; el diferencial cambiario.
- **BBVA:** el umbral de Banca Patrimonial (5 MDP según una fuente secundaria); si la cuota de 200 MXN + IVA al mes aplica a BBVA Trader; la fecha de vigencia de la guía (su ruta dice "18-sep"). (Que la comisión lleva IVA ya se verificó.)
- **AcciTrade (Banamex):** 0.35% + IVA y 100,000 MXN mínimos, solo en fuentes secundarias.
- **Banorte BeTrading, Santander y Monex:** tarifas (sitios con 503 o 403). El "hasta 1.70%" de Monex solo viene de un resumen de búsqueda.
- **Webull México:** su margen cambiario MXN→USD y su tratamiento fiscal en México. (Que Vifaru solo ofrece reportos y compra de dólares, sin BMV ni SIC, ya se verificó en la portada oficial.)
- **Hapi:** el costo de depósito y la conversión desde México ("se muestran en la app").
- **Revolut México:** la comisión después de la operación gratis del plan Estándar; la conversión; quién custodia.
- **Intercam:** el destino de su casa de bolsa (solo prensa y resúmenes).
- ~~**Art. 129 LISR:** reformas posteriores al 01-04-2024.~~ Verificado: no hay (Cámara de Diputados, 25-sep-2026) [49].
- **Todos:** la calidad de ejecución en el SIC (cruces "por excepción") y el historial de caídas fuera de GBM.

---

## Fuentes

Todas se consultaron el 2026-09-25.

1. Grupo Financiero Actinver, *Guía de Servicios de Inversión*, clave 1-PV-GR-007. **Versión vigente (verificada): 26.1.3**, actualizada el 01-jun-2026, aprobada el 21-jul-2026 y en vigor desde el 22-jul-2026. Es la que enlaza hoy el pie de página de Actinver Trade: https://www.actinver.com/documents/d/actinver/guia-de-servicios-de-inversion. La sección 6.4, "Actinver Trade por Internet" (0.25%/0.20%/0.15%/0.10%, custodia y administración en $0, nota de IVA), no cambió en sustancia. Versión citada originalmente: 25.2.3 (liberación 24-jun-2025; las páginas internas dicen 25.2.2). Secciones 3.2 "Servicios de Inversión no asesorados (Bursanet)", 6.2 (Casa de Bolsa asesorada) y 6.4 (Bursanet por Internet). Texto extraído con pypdf. https://actinver.com/documents/74160/86943/NosotrosPracticasdeVentaGuiaserviciosdeinversion.pdf/6eab44ee-edff-0cc9-c819-1db19618416a?version=2.1&t=1756925715237&download=false
2. Actinver Trade, "Preguntas frecuentes": comisiones de 0.10% a 0.25%, primer depósito mínimo de 1,000 MXN, cuenta Nivel 2 con tope de 3,000 UDIS al mes, W-8BEN gratuito, "desde una sola Acción", "Actinver Trade Casa de Bolsa está regulada y supervisada por la CNBV, la SHCP y Banxico", dividendos del SIC en USD y "un mes sin comisiones [...] al realizar tu primer depósito mayor a $10,[000]". https://actinvertrade.actinver.com/preguntas-frecuentes.html
3. Actinver Trade, página de inicio: "30 días de trades gratis con tu primer depósito. *Válido a partir de $10,000 MXN". https://actinvertrade.actinver.com/
4. Bursanet (Grupo Financiero Actinver), "En Bursanet nuestra misión es cubrir tus necesidades al menor costo" (PDF; título interno "Bursanet_Comisiones_Landing_2021"). Escalones de 0.25% a 0.10%, W-8BEN $0, custodia Indeval $0; contacto bursanet@actinver.com.mx. https://www.actinver.com/documents/74160/1977463/Bursanet+Comisiones.pdf/cb157f61-2c31-83ae-abf3-f74fbf8ec4f8?t=1636471970934
5. El Financiero, "Actinver evoluciona Bursanet a Actinver Trade y refuerza su apuesta digital" (26-ago-2025). https://www.elfinanciero.com.mx/mundo-empresa/2025/08/26/actinver-evoluciona-bursanet-a-actinver-trade-y-refuerza-su-apuesta-digital/
6. Kuspit Casa de Bolsa, contenido oficial del pie de página de kuspit.com ("Comisiones", "Preguntas frecuentes", "Protección de tu inversión"), servido por su API pública https://ok2.kuspit.com/OpenKuspit/api/k2/generales/footer (campo `comisionReal: 0.002`). Textos: "Mercado de capitales = 0.20% por operación"; "Kuspit no cobra ninguna comisión por administración y custodia"; "En caso de que tu portafolio de mercado de capitales [...] presente en un mes una rotación mayor al valor del portafolio no te cobraremos la comisión por mantenimiento en ese mes"; autorización de la SHCP (DOF 31-ene-2011). Portal: https://www.kuspit.com/
7. Rankia México, "Kuspit Casa de Bolsa: productos, comisiones, apertura y alternativas" (actualizado el 01-abr-2026). Fuente del mantenimiento de 0.99% anual (secundaria). https://www.rankia.mx/blog/casas-de-bolsa-de-mexico/7057514-analisis-kuspit-productos-comisiones-como-abrir-cuenta-alternativas
8. Kuspit en X (@Kuspit1): "¡La combinación ganadora para operar con la comisión más baja de México! 1. Comisión Mantenimiento = 0% 2. Comisión por Operación = 0.20%". Fecha: **19-mar-2024**, calculada del ID del tuit (snowflake). Texto visto en el listado de búsqueda; X devolvió 402. https://x.com/Kuspit1/status/1770216462776471888
9. Casa de Bolsa Finamex, "Finamex Trading" (FAQ: "86 pesos más IVA al mes", "costo por operación es de .06% sin importar el monto", administración "mayor a 1 mdp será de 1% anual, en caso contrario 2% anual", "desde 10 mil pesos", "más de 2,200 acciones y ETF's"). HTML descargado y leído. https://www.finamex.com.mx/general/finamex-trading/
10. BBVA México, "BBVA Trader". Re-descargada el 25-sep-2026: "En operaciones de menos de 1,000,000 MXN es de 0.23%. De 1,000,001 a 5,000,000 MXN es de 0.18%. [...] a partir de 5,000,001 MXN es de 0.10%. **\*Comisión más IVA**." Requisito: "Ser persona física y cliente de la Banca Patrimonial y Privada de BBVA"; contrato de Ejecución de Operaciones; BMV, BIVA y SIC. **Corrección:** la versión anterior de este documento decía "incluyen IVA". https://www.bbva.mx/personas/productos/patrimonial-y-privada/inversiones/trader.html
11. BBVA Noticias, "BBVA Trader transforma la inversión en México al unificar operaciones de bolsa y banca en un solo lugar" (17-dic-2025; "más de 4,700 instrumentos"). https://www.bbva.com/es/mx/innovacion/bbva-trader-transforma-la-inversion-en-mexico-al-unificar-operaciones-de-bolsa-y-banca-en-un-solo-lugar/
12. BBVA México (Institución de Banca Múltiple), *Guía de Servicios de inversión* (PDF sin fecha visible; ruta "18-sep/bpp"). Custodia de 0.105 al millar, compraventa "Máximo 1.7%", supervisión y custodia de "$200.00 [...] por mes más el IVA", "en su caso". https://www.bbva.mx/content/dam/public-web/mexico/documents/18-sep/bpp/guia-de-servicios-de-inversiones.pdf
13. Resumen de búsqueda sobre el mínimo de 5,000,000 MXN para Banca Patrimonial BBVA (sin fuente primaria; **no verificado**). Página de referencia: https://www.bbva.mx/personas/banca-patrimonial-y-privada.html
14. Banorte, "BeTrading" y sus preguntas frecuentes (contenido tomado del resumen del buscador; el sitio respondió 503 a WebFetch y cortó la conexión con curl). https://www.banorte.com/Casa-de-Bolsa/BeTrading.html
15. Rankia México, "Santander Casa de Bolsa México: comisiones, funciones y cómo invertir" (22-sep-2026; secundaria). https://www.rankia.mx/blog/forex-mexico/5940004-analisis-santander-casa-bolsa
16. Santander México, *Guía de servicios de inversión 2024* (PDF; 403 al consultarlo). https://www.santander.com.mx/PDF/personas/guia-de-servicios-de-inversion-2024.pdf
17. Monex Casa de Bolsa, *Guía de Servicios de Inversión V.4* (PDF; 403 al consultarlo; el "hasta 1.70%" viene del resumen del buscador). https://www.monex.com.mx/portal/download/noticias/Guia-Servicios-de-Inversion-Casa-de-Bolsa.pdf
18. Monex, "Monex Trader" y "Monex Trader móvil" (sección de Banca Privada; 403 al consultarlo; datos del listado de búsqueda). https://www.monex.com.mx/portal/banca-privada/canales-digitales/monex-trader
19. Expansión, "CNBV revoca licencia de Vector Casa de Bolsa tras señalamientos de lavado de dinero" (16-dic-2025). https://expansion.mx/economia/2025/12/16/cnbv-revoca-licencia-de-vector-casa-de-bolsa
20. La Jornada, "CNBV revoca a Vector licencias como casa de bolsa y operadora de fondos" (16-dic-2025; visto en el listado de búsqueda, junto con el resumen: solicitud del 1-dic-2025, Junta de Gobierno del 12-dic-2025, liquidador designado). https://www.jornada.com.mx/noticia/2025/12/16/economia/cnbv-revoca-a-vector-licencias-como-casa-de-bolsa-y-operadora-de-fondos
21. Expansión, "¿Quién es dueño de Finamex, la casa de bolsa que tomó los clientes de inversión de Vector?" (2-oct-2025; visto en el listado de búsqueda, con la cifra de ~30,000 clientes y 90,000 MDP en el resumen). https://expansion.mx/economia/2025/10/02/quien-es-dueno-de-finamex-la-casa-de-bolsa
22. Webull México, página de inicio (entidades: Vifaru, S.A. de C.V., Casa de Bolsa, "regulada por CNBV y Banco de México", para operaciones en pesos; Webull Financial LLC, miembro de SEC, FINRA y SIPC, para operaciones en dólares; "cero comisiones"; sin depósito mínimo). https://www.webull.com.mx/ (la página /pricing redirige con 301 a https://www.webull.com/pricing, la de EUA).
23. Finantres, "Actinver opiniones: seguridad, comisiones y si conviene" (Google Play 4.2; secundaria). https://finantres.mx/actinver/
24. Finantres, "Webull opiniones México" (actualizado el 16-sep-2026; entidades Webull Asesor de Inversiones S.C., Vifaru y Webull Financial LLC; FINRA CRD #289063; secundaria). https://finantres.mx/webull-opiniones/
25. Rankia México, "GBM+ vs Flink (Webull México): ¿Cuál te conviene para invertir en México?" (dice que no permite comprar acciones mexicanas "por el momento"; visto en el listado de búsqueda; secundaria). https://www.rankia.mx/blog/casas-de-bolsa-de-mexico/7188607-gbm-vs-flink-webull-mexico-cual-conviene-para-invertir
26. Hapi, sitio oficial (Hapi Securities LLC, FINRA CRD #311868, SIPC, Apex Clearing; fracciones). https://hapi.trade/en
27. Hapi, *Fee Schedule* (PDF creado el 29-abr-2026). https://hapi-public-documents.s3.us-east-1.amazonaws.com/hapi-fees-schedule.pdf
28. Revolut México, "Acciones y ETF de EE. UU." (403 al consultarlo; datos del resumen del buscador: plan Estándar con "1 operación sin comisión por mes", "Revolut Securities Singapore Pte", "Revolut Bank, S.A., Institución de Banca Múltiple"). https://www.revolut.com/es-MX/stock-trading/
29. Revolut México, *Anexo de Comisiones de Productos* (PDF; solo cubre cuentas, tarjetas y transferencias; no incluye inversiones). https://cdn.revolut.com/terms_and_conditions/pdf/consulta_los_costos_y_comisiones_de_nuestros_productos_bd276606_1.0.0_1773759339_es.pdf
30. Rankia México, "Revolut en México: ¿cómo impacta a inversionistas y traders en 2026?" (6-feb-2026; lanzamiento el 27-ene-2026; secundaria). https://www.rankia.mx/blog/forex-mexico/7185707-revolut-mexico-inversiones-trading-guia
31. Expansión, "La CNBV frena lanzamiento de nueva plataforma de inversión de Hey Banco" (5-jun-2026). https://expansion.mx/economia/2026/06/05/cnbv-frena-lanzamiento-nueva-plataforma-inversion-hey-banco
32. CONDUSEF, "Nuevos resultados del desempeño en la atención a usuarios del sector casas de bolsa, al 4º trimestre de 2025" (17-abr-2026). https://www.gob.mx/condusef/prensa/nuevos-resultados-del-desempeno-en-la-atencion-a-usuarios-del-sector-casas-de-bolsa-al-4-trimestre-de-2025-consultalos-antes-de-decidir
33. Ley del Impuesto sobre la Renta, art. 129 (Cámara de Diputados, texto vigente con última reforma DOF 01-04-2024; copia local ya descargada en esta investigación). https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf
34. Grupo BMV, boletín "El Sistema Internacional de Cotizaciones de la BMV permite a los mexicanos invertir en Amazon, Apple o Tesla" (11-nov-2020; 2,411 valores listados en oct-2020; referencia histórica, B1 trae una cifra más reciente). https://www.bmv.com.mx/docs-pub/SALA_PRENSA/CTEN_BOLE/El%20SIC%20de%20la%20BMV%20permite%20invertir%20en%20acciones%20como%20Tesla,%20Apple%20o%20Amazon%20.pdf
35. Grupo BMV, "Mercado Global" (SIC): "Desde enero de 2014, cualquier tipo de inversionista puede participar en el SIC"; operación en pesos. https://www.bmv.com.mx/es/mercados/mercado-global
36. Documentos internos: `../01-gbm-operativa-y-costos.md` (A1), `../02-universo-sic-bmv-agresivo.md` (A2) y `B1-gbm-linea-base-.md` (línea base de GBM: 0.29% por lado, W-8BEN de 75 USD + IVA, IDATU, caídas).
37. Finantres, "Kuspit opiniones 2026" (secundaria). https://finantres.mx/kuspit-opiniones/
38. CNBV, "Comunicado de Prensa, Revocación de licencia a Vector Casa de Bolsa" (gob.mx; sesión de la Junta de Gobierno del 12-dic-2025; revocación a solicitud de la propia entidad y sin relación con FinCEN). Leído con WebFetch; curl devolvió una página de verificación anti-bots. https://www.gob.mx/cnbv/prensa/comunicado-de-prensa-revocacion-de-licencia-a-vector-casa-bolsa?idiom=es
39. Insigneo, comunicado "Insigneo adquirirá las cuentas de VectorGlobal" (GlobeNewswire, 21-oct-2025; visto en el listado de búsqueda) y El Universal, "Finamex se queda con clientes y activos de Vector Casa de Bolsa" (secundaria). https://www.globenewswire.com/news-release/2025/10/21/3170322/0/es/Insigneo-adquirir%C3%A1-las-cuentas-de-VectorGlobal-fortaleciendo-su-presencia-en-Am%C3%A9rica-Latina.html
40. Inferencia fiscal: la Ley del IVA grava la prestación de servicios (art. 14) y ninguna exención cubre las comisiones de intermediación bursátil. Actinver [1] y GBM (B1) cobran IVA sobre el corretaje. Que Kuspit lo cobre: **no verificado** en su tarifa.
41. Actinver (Bursanet), "Promoción 30 Días de Trades Gratis 2024", términos y condiciones (PDF, vigencia del 1-ene al 31-dic-2024): primer fondeo mínimo de 10,000 MXN "a su contrato de Casa de Bolsa, no contrato de Banco", "en una sola exhibición" y dentro de los 90 días de la apertura; "30 días naturales sin comisiones de compra o venta en el mercado de capitales"; tope de 1,000 operaciones; solo clientes nuevos. **Los términos 2026 no se localizaron**; la portada actual sigue anunciando la promoción [3]. https://www.actinver.com/documents/74160/597710/Bursanet+-+Promoci%C3%B3n+30+Trades+Gratis+(Social+Media).pdf/3cb95675-c7e7-9f55-903d-fef3673f11ad?t=1628607848753
42. Kuspit en X (@Kuspit1), respuesta a un cliente: "comisión de Mantenimiento de Portafolio [...] es del 0.99% anual del valor de tu portafolio y la cobramos de manera mensual". Fecha: **2-feb-2018**, calculada del ID del tuit. Texto del listado de búsqueda. https://twitter.com/Kuspit1/status/959550246035644418
43. Apple App Store, "Kuspit" (vendedor: Kuspit Casa de Bolsa SA de CV): "Contamos con más de 3,500 opciones", "Bajamos la comisión a 0.20% en todas tus operaciones", gráficos de TradingView; versión 1.3.28 de sep-2026. Leído con WebFetch. https://apps.apple.com/us/app/kuspit/id1568546658
44. Hey Banco, "Hey Banco informa actualización sobre el lanzamiento de Hey X" (5-jun-2026): pospone el lanzamiento "con el objetivo de incorporar las recomendaciones emitidas por la autoridad" y no da nueva fecha. https://banco.hey.inc/blog-hey/articulos/sala-de-prensa/Hey-Banco-informa-actualizacion-sobre-el-lanzamiento-de-Hey-X
45. Finantres, "AcciTrade opiniones" (actualizado el 16-sep-2026; 0.35% + IVA y apertura de 100,000 MXN; secundaria) y Rankia, "Accival Casa de Bolsa [...] Accitrade" (secundaria). La página oficial de requisitos de Banamex no devolvió contenido. https://finantres.mx/accitrade-opiniones/ ; https://www.banamex.com/es/personas/inversiones/accitrade/requisitos_condiciones.htm
46. Banco de México, SIE, cuadro CP150 "Valor de UDIS": 8.849589 (08-oct-2026), 8.851528 (09-oct-2026) y 8.853467 (10-oct-2026). Banxico publica la UDI por adelantado; el valor del 25-sep no se extrajo. https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?sector=8&accion=consultarCuadro&idCuadro=CP150&locale=es
47. Actinver Trade (antes Bursanet) en X (@BursanetMX): "Si aún no sabes cómo colocar un stop loss en tus órdenes de compra, da clic aquí". Fecha: **17-feb-2022**, calculada del ID del tuit. Texto del listado de búsqueda; que la app actual lo conserve: no verificado. https://x.com/BursanetMX/status/1494417855261118477
48. FINRA BrokerCheck, API pública de búsqueda: "HAPI SECURITIES LLC", firm_source_id 311868, SEC 8-70646, firm_scope "ACTIVE". https://api.brokercheck.finra.org/search/firm?query=hapi%20securities
49. Cámara de Diputados, "Ley del Impuesto sobre la Renta", página de reformas: "Última reforma publicada en el Diario Oficial de la Federación el 1 de abril de 2024" (consultada el 25-sep-2026). https://www.diputados.gob.mx/LeyesBiblio/ref/lisr.htm

---

## Registro de método

- **Búsquedas:** 41 consultas web (WebSearch) el 2026-09-25, más lectura directa de fuentes primarias. Guías en PDF de Actinver, BBVA, Hapi y Revolut, extraídas con pypdf. HTML de Finamex Trading y Actinver Trade, descargado y leído. JSON público del pie de página de Kuspit. Art. 129 LISR, desde la copia local.
- **Sitios bloqueados:** Banorte (503 o conexión cortada), Santander (403), Monex (403) y Revolut (403). De esos solo hay resúmenes del buscador, marcados como tales.
- **Cálculos (§3):** script en Python con los supuestos listados. Las cifras se redondean a pesos y a centésimas de punto.

---

## Verificacion (2026-09-25)

**Método.** Revisé cada afirmación que decide la elección contra la fuente oficial, descargada el mismo día: HTML con curl, PDF con pypdf, JSON público de Kuspit, la copia local de la LISR y WebFetch cuando curl estaba bloqueado. Recalculé con un script propio todas las cifras de §3 y los puntos de equilibrio. Estados: **Confirmado** (la fuente oficial dice lo mismo), **Corregido** (se cambió en el texto) y **No verificado** (la fuente oficial no se pudo leer o no lo dice).

### Qué decide la elección

| # | Afirmación | Fuente revisada | Estado |
|---|---|---|---|
| 1 | Kuspit cobra 0.20% por operación | JSON oficial `generales/footer` (`comisionReal: 0.002`; "Mercado de capitales = 0.20% por operación") + ficha de la App Store ("0.20% en todas tus operaciones") [6][43] | **Confirmado** |
| 2 | Kuspit no cobra custodia ni administración, y exenta el mantenimiento en el mes con rotación mayor al portafolio | JSON oficial [6] | **Confirmado** (texto literal) |
| 3 | El mantenimiento de Kuspit es de 0.99% anual | Kuspit en X, 2-feb-2018: 0.99% [42]. Kuspit en X, 19-mar-2024: "Mantenimiento = 0%" [8]. Rankia, abr-2026: 0.99% [7]. La guía oficial `G_Serv_Inv_Kuspit.pdf` (en api.kuspit.com:8080) no respondió: conexión rechazada o reiniciada | **No verificado**, y los canales oficiales se contradicen. Se agregó el peor caso a §3 |
| 4 | El 0.20% de Kuspit lleva IVA | Ninguna fuente de Kuspit lo dice | **No verificado**. **[I]** Probable por la LIVA [40] |
| 5 | Kuspit tiene acceso al SIC | App Store oficial: "más de 3,500 opciones" [43] | **Inferencia reforzada**: el total es oficial; los tickers no (la API pide token) |
| 6 | Actinver Trade: 0.25% / 0.20% / 0.15% / 0.10% + IVA; custodia, administración e información de la BMV en $0 | Guía **26.1.3 (en vigor desde el 22-jul-2026)**, sección 6.4, y FAQ [1][2] | **Confirmado**; la fuente se actualizó a la versión vigente |
| 7 | Actinver Trade: 30 días sin comisiones con depósito > 10,000 MXN | Portada y FAQ, hoy [2][3]. Términos 2024 [41] | **Confirmado**, con condiciones nuevas: el depósito va al contrato de Casa de Bolsa, en una exhibición y dentro de 90 días; 30 días naturales desde el correo; tope de 1,000 operaciones. Los términos 2026 no se localizaron |
| 8 | Actinver Trade: W-8BEN gratis | FAQ [2] y hoja de comisiones de Bursanet [4] | **Confirmado**, pero exige entregar el original en CDMX |
| 9 | Actinver Trade: Nivel 2 con tope de 3,000 UDIS al mes | FAQ [2] + UDI de Banxico ~8.85 [46] | **Confirmado**: ~26,500 MXN; los 20k caben. SPEI fuera de horario: tope de 1,500 UDIS por operación |
| 10 | Actinver Trade: "Comisiones mínimas por compraventa de acciones" | Guía 26.1.3 [1] | **Sigue ambiguo** (no da cifra) |
| 11 | Actinver Trade: órdenes stop | Cuenta oficial en X, 2022 [47] | **Parcial**: el stop loss existía en 2022; OCA y trailing no verificados |
| 12 | Finamex: 0.06%, 86 MXN + IVA al mes, 2% anual de administración (< 1 MDP), desde 10,000 MXN, >2,200 valores BMV + SIC | HTML oficial de Finamex Trading, re-descargado [9] | **Confirmado** (texto literal). Si el 0.06% y el 2% llevan IVA: no verificado |
| 13 | BBVA Trader: 0.23% "incluyen IVA" | Página oficial, re-descargada: "*Comisión más IVA" [10] | **Corregido**: 0.23% + IVA = 0.267%. Se recalculó la columna de §3. No cambia nada, porque BBVA sigue exigiendo ser cliente de Banca Patrimonial y Privada |
| 14 | Las casas mexicanas no retienen ISR en la venta; calculan y dan constancia; pérdidas compensables por 10 años | Art. 129 LISR completo (copia local, sin ninguna palabra "reten-") [33]. FAQ de Actinver [2] | **Confirmado** |
| 15 | "Retienen el ISR de los dividendos" | Arts. 140 y 142 fr. V LISR [33] | **Corregido/matizado**: en el SIC la ley pone el 10% a cargo de la persona física. Que retengan GBM (B1) sí; Actinver, Kuspit y Finamex: no verificado |
| 16 | Reformas a la LISR después del 01-04-2024 | Cámara de Diputados, 25-sep-2026 [49] | **Confirmado: no hay**. Se quitó de la lista de no verificados |
| 17 | IDATU 4T-2025: sector 8.9; GBM 7.00, Finamex 7.48, BBVA 7.93, Banorte 10 | Comunicado de la CONDUSEF del 17-abr-2026 [32] | **Confirmado**; Actinver y Kuspit no aparecen |

### Contexto (no decide la elección)

| # | Afirmación | Estado |
|---|---|---|
| 18 | Kuspit "autorizada por la SHCP" | **Corregido**: la autorización es de la CNBV (oficio 210-90283/2010, DOF 31-ene-2011) [6] |
| 19 | Vector revocada "el 16-dic-2025" | **Matizado**: sesión de la Junta de Gobierno del 12-dic-2025, pública el 16-dic [38]. Traspaso de clientes a Finamex e Insigneo: prensa y comunicado de Insigneo [21][39] |
| 20 | Webull México no ofrece acciones mexicanas | **Reforzado con fuente oficial**: Vifaru solo ofrece "reportos o bien, compras dólares"; los valores de EUA van por Webull Financial LLC [22] |
| 21 | Hapi: cargos de 0.10/0.15 USD, 2.99 USD, 4.99 USD de inactividad, CRD 311868 | **Confirmado** (PDF del 29-abr-2026 y FINRA BrokerCheck [27][48]). Inactividad matizada: 60 días sin actividad y saldo de 0 a 100 USD |
| 22 | Hey X pospuesto | **Confirmado** con el comunicado oficial de Hey Banco (5-jun-2026) [44]; sin fecha nueva |
| 23 | Banorte BeTrading, Santander, Monex y Revolut | **Siguen sin verificar**: Banorte dio 503 y cortó HTTP/2, Revolut dio 403 |
| 24 | AcciTrade (Banamex) | **Agregado**: 0.35% + IVA y 100k mínimos (secundario). Descartado |
| 25 | Aritmética de §3 (GBM, Actinver, Kuspit con y sin IVA, Finamex, puntos de equilibrio 9.4 / 12.8 / 15.9, ahorro de 139 MXN y mantenimiento de 99/115 MXN) | **Confirmado** al peso con un script propio |

### Impacto en el veredicto

- **[C] Hallazgo nuevo que decide:** la ventaja de Kuspit sobre Actinver Trade en la **primera** temporada es de solo **0.12 pp con R = 6** (23 MXN), y **se invierte** si Kuspit cobra el mantenimiento de 0.99% (672 contra 580 MXN). Desde la segunda temporada, sin el mes gratis de Actinver, Kuspit gana entre 0.12 y 0.70 pp.
- **[R] Orden corregido:** Kuspit sigue primero **solo** si confirma por escrito, antes de fondear, cuatro cosas: el IVA, que no cobra mantenimiento con una ida y vuelta al mes, el catálogo del SIC y las órdenes stop. Si no, **Actinver Trade queda primero**. Tiene tarifa vigente verificada, custodia en 0, W-8BEN gratis, stop loss (según su cuenta oficial, 2022) y el respaldo de un grupo financiero con banco. No aparece en el IDATU. Finamex, BBVA y AcciTrade siguen sin convenir para 20k.
- **[I] Sin cambio de fondo:** ninguna casa mexicana ahorra más de ~1 pp por temporada frente a GBM con la rotación presupuestada. La decisión B2 se define por catálogo, órdenes y certeza de costos, no por comisión.

### Lo que sigue sin fuente oficial (bloquea la cifra final)

1. La tarifa completa de Kuspit (guía de servicios inaccesible desde aquí): IVA, mantenimiento y definición de "rotación".
2. Los tickers concretos del SIC habilitados en Kuspit y en Actinver Trade.
3. La retención del 10% sobre dividendos del SIC en Actinver, Kuspit y Finamex.
4. Los términos 2026 de la promoción de 30 días de Actinver.
5. Las tarifas de Banorte BeTrading, Santander y Monex.
