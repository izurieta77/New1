# B2. Casas de bolsa y apps mexicanas contra GBM: costo neto para la cuenta arena

**Fecha de corte:** 2026-09-25 (todas las fuentes se consultaron ese día, salvo que se indique otra fecha).
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
   - **Vector ya no es opción.** La CNBV revocó su autorización como casa de bolsa el 16-dic-2025, a petición de la propia Vector, y la puso en liquidación. Sus clientes locales pasaron a Finamex y los internacionales a Insigneo [19][20].
   - **Flink ya no existe como marca.** Desde abril de 2025 es **Webull México** (Vifaru Casa de Bolsa para pesos y Webull Financial LLC para EUA) [22][24].
   - **Hapi no es casa de bolsa mexicana.** Es Hapi Securities LLC, un broker-dealer de EUA registrado en la SEC, que liquida con Apex [26][27].
2. **[H] Las casas mexicanas no retienen ISR cuando vendes acciones del SIC o de la BMV.** El intermediario **calcula** la ganancia o pérdida del año y **entrega la constancia**, y tú pagas el 10% definitivo en la declaración anual (art. 129 LISR). Si hay pérdida, la puedes restar de ganancias del mismo tipo en ese año o en los **10 siguientes** [33]. Lo que sí retienen es ISR sobre dividendos (B1). **[I]** Por eso cambiar de GBM a otra casa mexicana no cambia en nada tu régimen fiscal.
3. **[H] Comisión por operación publicada en fuente oficial (persona física, monto chico):**

   | Bróker | Comisión por lado | Con IVA | Fuente |
   |---|---|---|---|
   | GBM (referencia) | 0.25% | **0.29%** | [36] |
   | Actinver Trade | 0.25% (0 a 1 MDP operado en 30 días) | **0.29%** | [1][2] |
   | Kuspit | **0.20%** | 0.232% si lleva IVA (**no verificado**) | [6] |
   | Finamex Trading | **0.06%** "sin importar el monto" | 0.0696% si lleva IVA | [9] |
   | BBVA Trader | 0.23% "incluyen IVA" | 0.23% | [10] |

   **Pero:** Finamex cobra **86 MXN + IVA al mes** por información de mercado y **2% anual** de administración en contratos menores a 1 MDP [9]. BBVA Trader **solo acepta clientes de Banca Patrimonial y Privada** [10].
4. **[C] Costo de comisiones en la temporada de 6 meses para 20,000 MXN** (R = idas y vueltas completas de la cuenta; §3):

   | R | GBM | Actinver Trade (con el mes gratis) | Kuspit (con IVA) | Finamex Trading |
   |---|---|---|---|---|
   | 6 (1 al mes) | 696 (3.48%) | 580 (2.90%) | **557 (2.78%)** | 998 (4.99%) |
   | 9 (1.5 al mes) | 1,044 (5.22%) | 870 (4.35%) | **835 (4.18%)** | 1,081 (5.41%) |
   | 12 (2 al mes) | 1,392 (6.96%) | 1,160 (5.80%) | 1,114 (5.57%) | 1,165 (5.82%) |
   | 18 (3 al mes) | 2,088 (10.4%) | 1,740 (8.70%) | 1,670 (8.35%) | **1,332 (6.66%)** |

   **[I] La ventaja máxima contra GBM con el ritmo presupuestado (R = 6 a 9) es de ~0.6 a 1.0 puntos porcentuales en toda la temporada.** Es real, pero chica: un solo buen o mal trade la borra. Finamex solo le gana a GBM a partir de ~9.4 idas y vueltas, y a Kuspit a partir de ~12.8.
5. **[H] Actinver Trade da "un mes sin comisiones en el mercado de capitales" si el primer depósito es de más de 10,000 MXN, y el W-8BEN es gratis** [2][3]. En GBM el W-8BEN del SIC cuesta 75 USD + IVA (B1). La custodia y la administración cuestan 0 [1].
6. **[H] Kuspit cobra 0.20% por operación y no cobra el mantenimiento de un mes si la rotación del portafolio de capitales en ese mes supera el valor del portafolio** [6]. Según fuentes secundarias, ese mantenimiento es de 0.99% anual [7] (**el monto no está verificado en fuente oficial**). **Qué tiene Kuspit en su catálogo del SIC** (por ejemplo, TQQQ, SOXL o SPXL) **y qué tipos de órdenes permite** (stop, OCA): **no verificado**. Es justo lo que decide si sirve para la estrategia.
7. **[H] Calidad de servicio (CONDUSEF, IDATU 4T-2025, publicado el 17-abr-2026):** el promedio del sector fue 8.9. Las tres peores fueron **GBM (7.00)**, Finamex (7.48) y BBVA México Casa de Bolsa (7.93). Casa de Bolsa Banorte sacó 10 [32]. Actinver y Kuspit no aparecen en el comunicado.
8. **[H] Descartadas para 20k:**
   - **BBVA Trader:** exige ser cliente patrimonial. El umbral de ~5 MDP solo sale en fuentes secundarias (no verificado) [10][13].
   - **Monex Trader:** está en la sección de Banca Privada. La guía dice "hasta 1.70%" por operación (visto en un resumen de búsqueda; el sitio dio 403) [17][18].
   - **Santander:** no publica tarifa; se pacta en el contrato [15]. Su guía dio 403 [16].
   - **Banorte BeTrading:** la comisión solo aparece en el panel de confirmación, y la profundidad de libro cuesta 700 MXN + IVA al mes [14]. El sitio dio 503.
   - **Vector:** revocada [19].
   - **Hey X:** su lanzamiento, previsto para el 15-jun-2026, quedó pospuesto por observaciones de la CNBV [31].
9. **[I] Webull México, Hapi y Revolut son en realidad la ruta del "bróker extranjero"**: compras directas en NYSE/Nasdaq, con custodia en EUA y conversión MXN→USD. Según una fuente secundaria, Webull México hoy no permite comprar acciones mexicanas [25]. Ninguna de las tres publica su margen cambiario, y ninguna es la vía SIC. Ese análisis corresponde al frente de brókers extranjeros, no a este.
10. **[R] Veredicto de B2** (condicionado a tres verificaciones en la app; §6):
    - **Primera opción, Kuspit.** Es la comisión oficial más baja sin cargos fijos cuando la cuenta rota ≥1 vez al mes. Solo sirve si tiene habilitados los ETFs del SIC que usa la estrategia y si acepta órdenes stop.
    - **Segunda opción, Actinver Trade.** Cobra lo mismo que GBM, pero da un mes gratis, el W-8BEN gratis y la custodia en 0, y es un grupo financiero grande. **Es la opción más segura si Kuspit falla la verificación.**
    - **Finamex** solo tiene sentido si la cuenta va a rotar más de ~10 veces en la temporada. Eso va contra el presupuesto de rotación de A1.
    - **[I] Ninguna casa mexicana cambia el juego.** Ganan ≤1 punto por temporada con el ritmo presupuestado, así que la decisión se define por catálogo, tipos de orden y estabilidad, no por comisión.

---

## 1. Quién es quién (entidad, regulación y estado en 2026)

| Nombre comercial | Entidad que presta el servicio | Tipo | Estado al 2026-09-25 | Fuente |
|---|---|---|---|---|
| GBM | GBM Casa de Bolsa | Casa de bolsa (CNBV) | Activa. Línea base | B1 |
| **Actinver Trade** (antes Bursanet) | "Actinver Trade Casa de Bolsa" dentro de Grupo Financiero Actinver. La guía clasifica a Bursanet como "Servicios de inversión no asesorados" | Casa de bolsa (CNBV, SHCP, Banxico según su FAQ). La cuenta bancaria integrada tiene IPAB; los valores no | Activa. Cambió de nombre el 26-ago-2025 | [1][2][5] |
| **Kuspit** | Kuspit Casa de Bolsa, S.A. de C.V. Autorizada por la SHCP (DOF 31-ene-2011), supervisada por la CNBV. No da asesoría: solo ejecución | Casa de bolsa (CNBV) | Activa | [6] |
| **Finamex Trading** | Casa de Bolsa Finamex | Casa de bolsa (CNBV) | Activa. Absorbió ~30,000 cuentas de Vector (nota de oct-2025) | [9][21] |
| **BBVA Trader** | BBVA México (Casa de Bolsa BBVA México en el ranking de CONDUSEF) | Banco / casa de bolsa | Activa, **solo para Banca Patrimonial y Privada** | [10][11][32] |
| **Banorte BeTrading** | Casa de Bolsa Banorte | Casa de bolsa (CNBV) | Activa | [14][32] |
| **Santander** (SuperNet / SuperTrader) | Casa de Bolsa Santander | Casa de bolsa (CNBV) | Activa; tarifa no pública | [15] |
| **Monex Trader** | Monex Casa de Bolsa | Casa de bolsa (CNBV) | Activa; en la sección de Banca Privada | [17][18] |
| **Vector / e-Vector** | Vector Casa de Bolsa | — | **Autorización revocada el 16-dic-2025**, en liquidación | [19][20] |
| **Webull México** (antes Flink) | Vifaru, S.A. de C.V., Casa de Bolsa (operaciones en pesos) + Webull Financial LLC (EUA; SEC, FINRA, SIPC) | Mixta: casa de bolsa mexicana + broker-dealer de EUA | Activa. Su oferta visible es acciones, opciones, ETFs y futuros **de EUA** | [22][24][25] |
| **Hapi** | Hapi Securities LLC (SEC, FINRA CRD #311868, SIPC); liquidación con Apex Clearing | **Broker-dealer extranjero**, sin autorización de casa de bolsa en México | Activa | [26][27] |
| **Revolut México** | Revolut Bank, S.A., Institución de Banca Múltiple. Según el resumen de su página oficial, la ejecución la hace "Revolut Securities Singapore Pte" | Banco mexicano + ejecutor extranjero | Activa (acciones de EUA) (detalle no verificado; el sitio dio 403) | [28][30] |
| **Hey X** (Hey Banco) | Hey Banco. Se iba a operar con Apex Fintech y referenciación de Admino | Banco | **No lanzado**: pospuesto tras observaciones de la CNBV (jun-2026) | [31] |

**Qué implica cada tipo [I]:**
- **Casa de bolsa mexicana (CNBV):** custodia en Indeval, acceso al SIC en pesos, régimen del art. 129 con constancia anual [33]. **El IPAB no cubre casas de bolsa** (A1 §9). Los valores están a nombre del cliente en Indeval.
- **Broker-dealer extranjero (Hapi, la parte de EUA de Webull, y aparentemente Revolut):** custodia fuera de México, protección SIPC hasta los límites de EUA [26], sin constancia mexicana del art. 129 (no verificado para cada uno) y con W-8BEN. **La fracción I del art. 129 exige que la venta se haga en bolsas concesionadas conforme a la LMV** [33], así que la venta directa en NYSE/Nasdaq probablemente no entra ahí (inferencia; lo trata el frente de brókers extranjeros).

---

## 2. Tabla comparativa (persona física, cuenta de ~20,000 MXN)

| Bróker | Comisión por lado (fuente oficial) | Mínimo por orden | Custodia y cuotas fijas | Apertura mínima | SIC (catálogo declarado) | Fracciones | W-8BEN | Órdenes stop/OCA | Verificación |
|---|---|---|---|---|---|---|---|---|---|
| **GBM** (B1) | 0.25% + IVA = 0.29% | Ninguno oficial | 0 | 100 MXN | No publica catálogo del SIC; totales ">5,000"/">6,000" mezclados | No en el SIC | 75 USD + IVA | **Sí** (Stop, Stop limitada, Trailing, OCA, OTA) | Oficial (B1, A1) |
| **Actinver Trade** | 0.25% (0–1 MDP en 30 días), 0.20%, 0.15% y 0.10% arriba; + IVA [1][2] | La guía lista "Comisiones mínimas por compraventa de acciones" como un beneficio, sin cifra [1] (**ambiguo; no verificado**) | **0**: "Custodia INDEVAL $0.00", "Administración de cuenta $0.00", sin anualidad [1][2] | Primer depósito de 1,000 MXN. La cuenta abierta desde la app (Nivel 2) tiene un tope de depósitos de 3,000 UDIS al mes [2] | "Cientos de Acciones de empresas nacionales e internacionales (SIC)" [2]; "más de 3,000 acciones nacionales e internacionales" (El Financiero) [5] | No: "puedes comprar desde una sola Acción" [2] | **Gratis** [2] | No verificado | Oficial (guía 25.2.3 y FAQ) |
| **Kuspit** | **0.20%** "Mercado de capitales = 0.20% por operación" [6] | "Sin importar el monto" [6] | "No cobra ninguna comisión por administración y custodia" [6]. **Mantenimiento: no se cobra el mes en que la rotación supera el valor del portafolio** [6]. Su tasa (0.99% anual) solo sale en fuentes secundarias [7] | 100 MXN [6] | No publica catálogo (la API pide token). Acceso al SIC según fuentes secundarias [7] | No verificado | No verificado | No verificado | Oficial (texto de comisiones de kuspit.com) + secundaria |
| **Finamex Trading** | **0.06%** "sin importar el monto que operes" [9] | Ninguno mencionado | **86 MXN + IVA al mes** (información de mercado) + administración de **2% anual** (contratos < 1 MDP; 1% arriba) [9] | **10,000 MXN** [9] | "Más de 2,200 acciones y ETF's", BMV + SIC [9] | No verificado | No verificado | No verificado | Oficial (FAQ de Finamex Trading) |
| **BBVA Trader** | 0.23% (< 1 MDP), 0.18% y 0.10% arriba; "incluyen IVA" [10] | No publicado | La guía del banco menciona "supervisión y custodia" de **200 MXN + IVA al mes**, "en su caso", y custodia de 0.105 al millar [12] (vigencia de la guía no verificada) | **Cliente de Banca Patrimonial y Privada** [10] | "Más de 4,700 instrumentos a nivel global" [11] | No verificado | No verificado | No verificado | Oficial (requisito y tarifa); cuotas ambiguas |
| **Banorte BeTrading** | "Sólo se cobra una comisión de corretaje", visible en el panel de confirmación [14] | No publicado | Contratación sin costo; profundidad de libro 700 MXN + IVA al mes [14] | No publicado | Nacional + SIC [14] | No verificado | No verificado | No verificado | Solo el resumen del buscador de la página oficial (el sitio dio 503) |
| **Santander** | "Se pactan en el contrato"; no hay tarifa pública [15] | — | — | — | — | — | — | — | Secundaria; guía oficial con 403 [16] |
| **Monex Trader** | "Hasta 1.70% por operación más IVA" (guía V.4, citada en un resumen de búsqueda) [17] | — | — | Enfoque de banca privada [18] | Nacional + SIC [18] | — | — | — | No verificado (403) |
| **Vector** | — | — | — | — | — | — | — | — | **Revocada** [19] |
| **Webull México** | "Cero comisiones" en acciones y ETFs de EUA; pueden aplicar cargos regulatorios y de cambio [22][24] | — | Sin depósito mínimo [22] | "Cualquier cantidad" [22] | **No es vía SIC.** Según Rankia, no permite comprar acciones mexicanas [25] (no verificado) | "Cuando estén disponibles" [24] | Aplica (EUA) [24] | No verificado | Oficial (portada) + secundaria |
| **Hapi** | 0 de comisión, más una "clearing house fee" de 0.10 USD por trade de títulos completos y 0.15 USD por fracciones (usuarios regulares); 2.99 USD fuera de horario [27] | Implícito en la cuota fija | Inactividad de 4.99 USD al mes si el saldo es < 100 USD; Prime a 9.99 USD al mes [27] | — | **No es vía SIC** (EUA directo) | **Sí** [26] | EUA | No verificado | Oficial (fee schedule, PDF del 29-abr-2026) |
| **Revolut México** | Plan Estándar: "1 operación sin comisión por mes"; la comisión después no está verificada [28] | — | Custodia 0 (resumen) [28] | — | **No es vía SIC** (EUA directo) | Sí (secundaria) [30] | — | No verificado | Resumen del buscador de la página oficial (403) |

**Tipo de cambio en el SIC [H/I]:**
- **[H]** En el SIC todo cotiza y se liquida en pesos. El precio en MXN equivale a (precio en EUA × tipo de cambio) más la desviación del libro local, que se mide en B1 §3.1 y A2 §9.
- **[I]** Las casas mexicanas **no cobran un margen cambiario aparte** en el SIC. El costo cambiario está metido en la desviación del libro, y el libro es el mismo para todos los intermediarios (BMV/BIVA). Ninguna de las guías que revisé publica un margen cambiario para el SIC [1][9][12].
- **(no verificado)** Si alguna ejecuta el SIC "por excepción" contra su propio precio, como documenta GBM (A1 §2.3), y si eso mejora o empeora la ejecución.
- **[H]** En Actinver Trade, los dividendos de emisoras del SIC normalmente se pagan en USD y quedan en el apartado de efectivo en dólares [2].

**Catálogo del SIC [I]:** B1 §4.1 tiene el tamaño del SIC en la BMV (1,676 acciones y 1,404 ETFs, sep-2023). Un valor listado en el SIC lo puede operar cualquier inversionista a través de un intermediario [35]. Ninguna de estas casas publica qué emisoras tiene **habilitadas** en su app (Actinver dice "cientos" [2], Finamex ">2,200" [9], BBVA ">4,700 instrumentos" [11], y Kuspit no publica). **La diferencia real de catálogo solo se puede medir buscando los tickers en cada app** (§6).

---

## 3. Costo de la temporada para la cuenta de 20,000 MXN [C]

**Supuestos:**
- Capital de 20,000 MXN. Temporada de 6 meses.
- R = número de idas y vueltas completas del capital. El volumen total operado es 2 × 20,000 × R.
- IVA de 16% sobre toda comisión, salvo en BBVA, que ya lo incluye.
- La desviación del libro del SIC es igual en todos, así que no cambia la comparación y no se incluye.

**Fórmulas:**
- **GBM:** 0.29% × volumen.
- **Actinver Trade:** igual que GBM, pero con el primer mes gratis. Con actividad uniforme, eso son 5/6 del costo de GBM.
- **Kuspit:** 0.232% × volumen si lleva IVA; 0.20% si no. Sin mantenimiento, porque con R ≥ 6 la rotación mensual (compras + ventas) supera al portafolio [6].
- **Finamex:** 0.0696% × volumen + 86 × 1.16 × 6 = 598.56 de información + 2% × 20,000 × 0.5 × 1.16 = 232 de administración. Son **830.56 MXN fijos (4.15% del capital)**.

| R en la temporada | GBM | Actinver Trade (con el mes gratis) | Kuspit (con IVA) | Kuspit (sin IVA) | Finamex | BBVA Trader* |
|---|---|---|---|---|---|---|
| 3 | 348 (1.74%) | 290 (1.45%) | 278 (1.39%) | 240 (1.20%) | 914 (4.57%) | 276 (1.38%) |
| **6** | **696 (3.48%)** | 580 (2.90%) | 557 (2.78%) | 480 (2.40%) | 998 (4.99%) | 552 (2.76%) |
| 9 | 1,044 (5.22%) | 870 (4.35%) | 835 (4.18%) | 720 (3.60%) | 1,081 (5.41%) | 828 (4.14%) |
| 12 | 1,392 (6.96%) | 1,160 (5.80%) | 1,114 (5.57%) | 960 (4.80%) | 1,165 (5.82%) | 1,104 (5.52%) |
| 18 | 2,088 (10.44%) | 1,740 (8.70%) | 1,670 (8.35%) | 1,440 (7.20%) | 1,332 (6.66%) | 1,656 (8.28%) |

\* **BBVA Trader no es accesible con 20k.** Además, si aplicara la cuota de supervisión de 200 MXN + IVA al mes, sumaría **1,392 MXN (6.96%) en la temporada** [12].

**Puntos de equilibrio [C]:**
- **Finamex contra GBM:** R = 830.56 / (40,000 × (0.0029 − 0.000696)) = **9.4 idas y vueltas**.
- **Finamex contra Kuspit con IVA:** **12.8**. Contra Kuspit sin IVA: **15.9**.
- **Kuspit contra GBM con R = 6:** ahorra **139 MXN = 0.70 pp** de rendimiento en la temporada. Con R = 12 ahorra 1.39 pp.
- **Kuspit con mantenimiento:** si la rotación de un mes no supera el portafolio y se cobra el 0.99% anual (secundario), la temporada suma hasta 99 MXN (115 con IVA) = 0.57%. Con R ≤ 3 casi borra la ventaja contra GBM.

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
- **[I] Consecuencia para la decisión:** Actinver Trade, Kuspit, Finamex, Banorte, BBVA y Santander tienen el mismo régimen que GBM. Ninguna retiene ISR en la venta. Todas deben calcular y entregar la constancia, y retienen el ISR de los dividendos (B1 §5). Si la cuenta arena se abre en otra casa mexicana, el dueño tendrá **dos constancias** (GBM y la nueva) y suma ambos resultados en su declaración [33].
- **(no verificado)** Reformas al art. 129 posteriores al 01-04-2024 (la copia consultada llega hasta esa fecha).
- **[H] W-8BEN:** gratis en Actinver Trade [2] y 75 USD + IVA en GBM para el SIC (B1). **[C]** Con 20k no se paga solo en GBM (B1 §5). En Actinver Trade sí conviene, porque cuesta 0 y baja la retención de EUA sobre dividendos del SIC de 30% a 10% (esa tasa es de B1; que Actinver la aplique así: no verificado).

---

## 5. Calidad de la app, servicio e incidentes

| Bróker | Evidencia | Tipo | Fuente |
|---|---|---|---|
| GBM | IDATU 4T-2025: **7.00**, el más bajo del sector. Caídas documentadas en 2024-2025 y multas de la CNBV (B1 §7) | Oficial (CONDUSEF) | [32], B1 |
| Finamex | IDATU 4T-2025: **7.48** (segundo más bajo) | Oficial | [32] |
| BBVA México Casa de Bolsa | IDATU 4T-2025: **7.93** | Oficial | [32] |
| Casa de Bolsa Banorte | IDATU 4T-2025: **10** (entre las mejores) | Oficial | [32] |
| Actinver Trade | 4.2 en Google Play; reseñas de caídas y lentitud en la app (sin fechas precisas) | Secundaria / anecdótica | [23] |
| Kuspit | Una falla del portal web en 2018 (en X); no encontré notas de prensa de 2025-2026. Finantres la califica de "interfaz desactualizada" y con "herramientas limitadas para traders activos" | Anecdótica / secundaria | búsqueda del 2026-09-25, [37] |
| Vector, Intercam, CIBanco | Señalados por FinCEN el 25-jun-2025. Vector: licencia revocada (16-dic-2025). Intercam: operaciones vendidas a Kapital Bank (anuncio de la CNBV del 19-ago-2025, según resumen de búsqueda; no verificado en la fuente primaria) | Prensa | [19][20] |
| Hey X | La CNBV frenó el lanzamiento (jun-2026) | Prensa | [31] |

- **[I]** El IDATU mide la atención a reclamaciones, no la disponibilidad de la plataforma. Aun así, **GBM tiene la peor calificación del sector**, y una alternativa no queda en desventaja por servicio. De Actinver y Kuspit no hay dato de IDATU en el comunicado.
- **(no verificado)** No existe ningún registro público de caídas de Actinver Trade ni de Kuspit comparable con las de GBM del 7-abr-2025.

---

## 6. Veredicto y qué verificar antes de mover dinero

### 6.1 Ranking de B2 para "ganar más dinero neto" [R]

1. **Kuspit**, si pasa la verificación. Tiene la comisión oficial más baja sin cargos fijos (0.20%), no cobra mantenimiento si la cuenta rota más que su valor en el mes y abre desde 100 MXN. Ahorra ~0.7 pp contra GBM con R = 6. **Riesgos:** catálogo del SIC, tipos de orden y robustez para operar activamente, todos sin verificar.
2. **Actinver Trade**, la opción más segura. Tiene la misma tarifa que GBM, con 30 días sin comisiones (primer depósito > 10,000 MXN), W-8BEN gratis, custodia en 0, dividendos del SIC en USD y respaldo de un grupo financiero con banco. Ahorra ~0.6 pp contra GBM con R = 6, casi todo por el mes gratis. **Ojo: la cuenta debe ser Actinver Trade, no Casa de Bolsa Actinver con asesor.** En la asesorada, la guía marca corretaje de 0.75% con saldo < 500 mil, **mínimo de 200 MXN + IVA por operación**, custodia de 50 MXN + IVA al mes y 100 MXN al mes con saldo < 5,000 [1].
3. **Finamex Trading**, solo si la cuenta va a rotar más de ~10 veces en la temporada. Con el presupuesto de A1 pierde contra GBM.
4. **Descartadas para 20k:** BBVA Trader (requisito patrimonial), Monex, Santander y Banorte (sin tarifa pública verificable), Vector (revocada) y Hey X (no lanzado).
5. **Fuera de B2:** Webull México, Hapi y Revolut. Operan EUA directo con custodia extranjera y pertenecen al frente del bróker extranjero, junto con Interactive Brokers.

**[I] Mensaje central para el dueño:** entre las casas mexicanas, cambiar de GBM rinde a lo mucho ~1 punto por temporada con la operación presupuestada. Es dinero de verdad, pero **no compensa quedarse sin los ETFs del SIC que usa la estrategia ni sin órdenes stop**. Por eso el orden final depende de la verificación de abajo.

### 6.2 Verificación en la app antes de fondear (por bróker candidato)

1. **Catálogo:** buscar TQQQ, SOXL, SPXL, QLD, SMH, SOXX, QQQM, SPLG/SPYM, GLD, IAU y EWW. Anotar si aparecen, si se pueden comprar y si la app pide un perfil o una carta.
2. **Órdenes:** revisar si la app acepta stop, stop limitada, trailing y OCA en valores del SIC, y qué vigencia máxima tienen.
3. **Costo real:** poner una orden de prueba de ~2,000 MXN y leer en la confirmación la comisión, el IVA y si hay algún mínimo.
   - En **Kuspit:** confirmar si el 0.20% lleva IVA y cómo calcula la "rotación" que exenta el mantenimiento (¿compras + ventas, o un solo lado?).
   - En **Actinver Trade:** confirmar que no hay comisión mínima y que la promoción de 30 días aplica con un depósito de 20,000 MXN.
4. **Límite de la cuenta:** en Actinver Trade, la cuenta abierta desde la app (Nivel 2) tiene un tope de depósitos de 3,000 UDIS al mes [2]. Con la UDI en ~8.5–8.7 MXN serían ~26 mil MXN (valor de la UDI no verificado). Si se quiere margen, conviene abrir la Nivel 4 desde el sitio web.
5. **Constancia:** confirmar en la FAQ o por chat que entregan la constancia anual del art. 129 por contrato.

### 6.3 Comparabilidad en la competencia [R]

- Todas las réplicas y pruebas actuales usan **0.29% por lado (GBM)**. Si la cuenta se muda:
  - **Kuspit:** recalcular con **0.232%** por lado (0.20% si se confirma que no lleva IVA), más el mantenimiento en los meses sin rotación.
  - **Actinver Trade:** 0.29%, con **0% el primer mes**.
- En la bitácora del torneo se anota, **por operación**, la diferencia de costo contra GBM (por ejemplo, Kuspit: −0.058 pp por lado; Actinver en el mes gratis: −0.29 pp por lado). Así el marcador se puede reportar también "a costos de GBM" y la comparación con las IAs que siguen en GBM sigue siendo justa.
- La desviación del libro del SIC no cambia entre casas mexicanas (§2), así que no hace falta ajustarla.

---

## 7. No verificado (lista consolidada)

- **Kuspit:** si el 0.20% lleva IVA; el monto oficial del mantenimiento (0.99% anual solo sale en fuentes secundarias); la definición exacta de "rotación"; el catálogo del SIC; los tipos de orden; las fracciones; el costo del W-8BEN.
- **Actinver Trade:** qué significa "Comisiones mínimas por compraventa de acciones" en la guía 25.2.3 (¿hay un mínimo en pesos?); los tipos de orden (stop, OCA); el catálogo exacto del SIC; la vigencia de la promoción de 30 días a la fecha de apertura.
- **Finamex:** si el 0.06% y el 2% anual llevan IVA; los tipos de orden; el catálogo real.
- **BBVA:** el umbral de Banca Patrimonial (5 MDP según una fuente secundaria); si la cuota de 200 MXN + IVA al mes aplica a BBVA Trader; la fecha de vigencia de la guía (su ruta dice "18-sep").
- **Banorte BeTrading, Santander y Monex:** tarifas (sitios con 503 o 403). El "hasta 1.70%" de Monex solo viene de un resumen de búsqueda.
- **Webull México:** si todavía ofrece BMV/SIC en pesos vía Vifaru; su margen cambiario MXN→USD; su tratamiento fiscal en México.
- **Hapi:** el costo de depósito y la conversión desde México ("se muestran en la app").
- **Revolut México:** la comisión después de la operación gratis del plan Estándar; la conversión; quién custodia.
- **Intercam:** el destino de su casa de bolsa (solo prensa y resúmenes).
- **Art. 129 LISR:** reformas posteriores al 01-04-2024.
- **Todos:** la calidad de ejecución en el SIC (cruces "por excepción") y el historial de caídas fuera de GBM.

---

## Fuentes

Todas se consultaron el 2026-09-25.

1. Grupo Financiero Actinver, *Guía de Servicios de Inversión*, clave 1-PV-GR-007, versión 25.2.3 (liberación 24-jun-2025; las páginas internas dicen 25.2.2). Secciones 3.2 "Servicios de Inversión no asesorados (Bursanet)", 6.2 (Casa de Bolsa asesorada) y 6.4 (Bursanet por Internet). Texto extraído con pypdf. https://actinver.com/documents/74160/86943/NosotrosPracticasdeVentaGuiaserviciosdeinversion.pdf/6eab44ee-edff-0cc9-c819-1db19618416a?version=2.1&t=1756925715237&download=false
2. Actinver Trade, "Preguntas frecuentes": comisiones de 0.10% a 0.25%, primer depósito mínimo de 1,000 MXN, cuenta Nivel 2 con tope de 3,000 UDIS al mes, W-8BEN gratuito, "desde una sola Acción", "Actinver Trade Casa de Bolsa está regulada y supervisada por la CNBV, la SHCP y Banxico", dividendos del SIC en USD y "un mes sin comisiones [...] al realizar tu primer depósito mayor a $10,[000]". https://actinvertrade.actinver.com/preguntas-frecuentes.html
3. Actinver Trade, página de inicio: "30 días de trades gratis con tu primer depósito. *Válido a partir de $10,000 MXN". https://actinvertrade.actinver.com/
4. Bursanet (Grupo Financiero Actinver), "En Bursanet nuestra misión es cubrir tus necesidades al menor costo" (PDF; título interno "Bursanet_Comisiones_Landing_2021"). Escalones de 0.25% a 0.10%, W-8BEN $0, custodia Indeval $0; contacto bursanet@actinver.com.mx. https://www.actinver.com/documents/74160/1977463/Bursanet+Comisiones.pdf/cb157f61-2c31-83ae-abf3-f74fbf8ec4f8?t=1636471970934
5. El Financiero, "Actinver evoluciona Bursanet a Actinver Trade y refuerza su apuesta digital" (26-ago-2025). https://www.elfinanciero.com.mx/mundo-empresa/2025/08/26/actinver-evoluciona-bursanet-a-actinver-trade-y-refuerza-su-apuesta-digital/
6. Kuspit Casa de Bolsa, contenido oficial del pie de página de kuspit.com ("Comisiones", "Preguntas frecuentes", "Protección de tu inversión"), servido por su API pública https://ok2.kuspit.com/OpenKuspit/api/k2/generales/footer (campo `comisionReal: 0.002`). Textos: "Mercado de capitales = 0.20% por operación"; "Kuspit no cobra ninguna comisión por administración y custodia"; "En caso de que tu portafolio de mercado de capitales [...] presente en un mes una rotación mayor al valor del portafolio no te cobraremos la comisión por mantenimiento en ese mes"; autorización de la SHCP (DOF 31-ene-2011). Portal: https://www.kuspit.com/
7. Rankia México, "Kuspit Casa de Bolsa: productos, comisiones, apertura y alternativas" (actualizado el 01-abr-2026). Fuente del mantenimiento de 0.99% anual (secundaria). https://www.rankia.mx/blog/casas-de-bolsa-de-mexico/7057514-analisis-kuspit-productos-comisiones-como-abrir-cuenta-alternativas
8. Kuspit en X (@Kuspit1): "Comisión Mantenimiento = 0% / Comisión por Operación = 0.20%" (visto solo en el listado de búsqueda; fecha no verificada). https://x.com/Kuspit1/status/1770216462776471888
9. Casa de Bolsa Finamex, "Finamex Trading" (FAQ: "86 pesos más IVA al mes", "costo por operación es de .06% sin importar el monto", administración "mayor a 1 mdp será de 1% anual, en caso contrario 2% anual", "desde 10 mil pesos", "más de 2,200 acciones y ETF's"). HTML descargado y leído. https://www.finamex.com.mx/general/finamex-trading/
10. BBVA México, "BBVA Trader" (comisiones de 0.23%, 0.18% y 0.10% que "incluyen IVA"; requisito: "persona física cliente de Banca Patrimonial y Privada"; contrato de Ejecución de Operaciones; BMV, BIVA y SIC). https://www.bbva.mx/personas/productos/patrimonial-y-privada/inversiones/trader.html
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

---

## Registro de método

- **Búsquedas:** 41 consultas web (WebSearch) el 2026-09-25, más lectura directa de fuentes primarias. Guías en PDF de Actinver, BBVA, Hapi y Revolut, extraídas con pypdf. HTML de Finamex Trading y Actinver Trade, descargado y leído. JSON público del pie de página de Kuspit. Art. 129 LISR, desde la copia local.
- **Sitios bloqueados:** Banorte (503 o conexión cortada), Santander (403), Monex (403) y Revolut (403). De esos solo hay resúmenes del buscador, marcados como tales.
- **Cálculos (§3):** script en Python con los supuestos listados. Las cifras se redondean a pesos y a centésimas de punto.
