# 27 — Fiscalidad 2026 y estructura del SIC (persona física residente en México)

> Nivel: especialidad (fiscal bursátil personal + estructura transfronteriza) · Actualizado 2026-09-25 · Grado global: **A en la letra de la ley** (LISR, LIF 2026, Código de EUA, instrucciones del IRS, tratados), porque cada cita se verificó mecánicamente contra el texto congelado en `laboratorio/replicas/V05-spiva-y-fiscalidad-sic/datos/legal/`. **B** en la aplicación de las reglas de *situs* al SIC/Indeval, porque no existe resolución específica. **C** en el trato fiscal mexicano de un ETF UCITS irlandés comprado en el SIC, que se infiere de la letra del art. 129 sin regla expresa del SAT. **Esto no es asesoría fiscal**: describe normas vigentes con fuente y marca lo no verificado (fase 0).

Capítulos y documentos relacionados, que aquí no se repiten: [16 Macro, divisas y el peso](16-macro-global-divisas-y-el-peso.md) (el dólar como cobertura del mexicano) · [24 Política pública y regulación](24-politica-publica-regulacion-y-mercados.md) (Paquete Económico) · `arena/investigacion/01-gbm-operativa-y-costos.md` (comisiones, W-8BEN de 75 USD + IVA, títulos completos en el SIC) · réplica [V05](../laboratorio/replicas/V05-spiva-y-fiscalidad-sic/README.md), donde están las cifras de SPIVA, los datos congelados y el código.

**Convenciones.** Hecho = lleva fuente y fecha. "**Inferencia:**" = razonamiento propio. "**Regla:**" = propuesta operable para el sistema, no para terceros. "(nv)" = no verificado en esta sesión. LISR = Ley del Impuesto sobre la Renta (texto vigente de la Cámara de Diputados, última reforma DOF 01-04-2024). LIF 2026 = Ley de Ingresos de la Federación 2026 (DOF 07-11-2025). *Situs* = lugar donde la ley de EUA considera ubicado un bien para su impuesto sucesorio. NRA = no residente y no ciudadano de EUA.

---

## 1. Objetivos de dominio

1. Calcular el ISR de una venta en BMV o SIC: base, tasa, compensación de pérdidas y quién calcula la constancia.
2. Distinguir las tres capas fiscales de un mexicano que invierte en acciones: **ganancia** (art. 129), **flujos** (dividendos e intereses) y **muerte** (*estate tax* de EUA). México no grava la herencia.
3. Saber cuánto se retiene y en qué orden sobre un dividendo del SIC, con y sin W-8BEN, y qué pasa en la declaración anual.
4. Conocer la retención de 2026 sobre intereses y su efecto en el rendimiento real de CETES o Smart Cash.
5. Medir la exposición al *estate tax* de EUA y saber qué activos del SIC la generan.
6. Evaluar ETFs UCITS irlandeses del SIC frente a ETFs de EUA: *situs*, retención de dividendos, precio por título y liquidez.
7. Leer SPIVA sin caer en sus trampas: edición, índice, supervivencia y peso fuera del índice.

---

## 2. Núcleo

### 2.1 Mapa de las tres capas

| Capa | Hecho gravado | Impuesto | Quién lo retiene o calcula | Cuándo pega |
|---|---|---|---|---|
| Ganancia | Venta de acciones o ETFs en BMV o SIC | 10% definitivo sobre la ganancia neta del año (art. 129 LISR) | El intermediario calcula; **no retiene** en la venta (FAQ de GBM) | En la declaración anual de abril |
| Flujos | Dividendos de México | 10% adicional retenido (art. 140) + acumulación con acreditamiento del ISR corporativo | Emisora o intermediario | Al pago y en la anual |
| Flujos | Dividendos extranjeros del SIC | Retención de EUA de 30% (10% con W-8BEN), luego 10% adicional en México (art. 142 fr. V) + acumulación con acreditamiento del impuesto extranjero | Agente de EUA / GBM | Al pago y en la anual |
| Flujos | Intereses (CETES, reportos, Smart Cash) | Retención de **0.90% anual sobre el capital** en 2026 (art. 24 LIF 2026; arts. 54 y 135 LISR), a cuenta del interés real acumulable | GBM | Diario / en la anual |
| Muerte | Activos con *situs* en EUA de un NRA | *Estate tax* de 18% a 40% sobre el exceso del crédito de 13,000 USD (umbral de declaración: 60,000 USD) | Albacea: Form 706-NA en 9 meses | Al fallecer |
| Muerte | Herencia recibida en México | Exenta de ISR (art. 93 fr. XXII LISR) | — | — |

### 2.2 Ganancias en bolsa: art. 129 LISR

- **Tasa y alcance.** "Las personas físicas estarán obligadas a pagar el impuesto sobre la renta, cuyo pago se considerará como definitivo, aplicando la tasa del 10% a las ganancias obtenidas en el ejercicio". Incluye (fr. I) acciones de sociedades mexicanas y "acciones emitidas por sociedades extranjeras cotizadas en dichas bolsas de valores", que es el SIC, y (fr. II) "títulos que representen índices accionarios", que son los ETFs de índices de acciones.
- **Base.** Por cada emisora: precio de venta menos comisiones, menos el **costo promedio de adquisición actualizado** por inflación hasta el mes anterior a la venta, más las comisiones de compra. Las ganancias y pérdidas de todas las emisoras se suman en el año, por intermediario.
- **Quién calcula.** El intermediario "deberá hacer el cálculo de la ganancia o pérdida del ejercicio" y entregar la información, incluida una constancia si hubo pérdida. GBM: "Tus Constancias Fiscales (o CFDI) por las ganancias del 2025 ya están disponibles en tu app GBM" (Menú → Estados de cuenta y constancias → Constancias fiscales). **No hay CFDI para Trading USA**: esa cuenta se autodeclara con los estados de DriveWealth.
- **Pérdidas.** Se restan "únicamente contra el monto de la ganancia que en su caso obtenga el mismo contribuyente en el ejercicio o en los diez siguientes", actualizadas por inflación. "Cuando el contribuyente no disminuya la pérdida fiscal durante un ejercicio pudiendo haberlo hecho […] perderá el derecho a hacerlo". No se pueden restar de sueldos ni de otros ingresos.
- **Exclusiones** (se gravan con el régimen general, no con el 10%): accionistas con 10% o más que vendan 10% o más en 24 meses, quienes vendan el control, operaciones fuera de bolsa o cruces protegidos, y acciones no colocadas entre el gran público que excedan 1% en 24 meses.
- **Inferencia:** en el SIC el precio está en pesos, así que la ganancia fiscal ya incluye el movimiento del tipo de cambio. La actualización del costo por INPC compensa solo la parte de esa ganancia que se debe a la inflación mexicana.

### 2.3 Dividendos

- **Emisoras mexicanas (art. 140).** Tasa adicional de 10% "sobre los dividendos o utilidades distribuidos por las personas morales residentes en México", retenida y definitiva. Además, el dividendo se acumula a los demás ingresos y se acredita el ISR corporativo con el factor 1.4286. GBM: el 10% aplica "solo si son utilidades del 2014 en adelante".
- **Emisoras extranjeras vía SIC (art. 142 fr. V).** Se acumulan a los demás ingresos **y**, "de forma adicional", se paga 10% "al monto al cual tengan derecho del dividendo o utilidad efectivamente distribuido por el residente en el extranjero, sin incluir el monto del impuesto retenido", como pago definitivo a más tardar el día 17 del mes siguiente. GBM lo retiene "sobre monto neto, después del impuesto retenido en el extranjero".
- **Retención de EUA.** El tratado México-EUA (art. 10) limita al **10%** del dividendo bruto en cartera (5% para sociedades con 10% o más de los votos). Sin W-8BEN, la retención es de 30%. En el SIC, el W-8BEN se tramita vía Indeval y cuesta **75 USD + IVA**; en Trading USA es gratis (doc `01`).
- **Trampa de la FAQ de GBM:** dice "Pago del ISR anual del 35%" para dividendos extranjeros. **Inferencia:** 35% es la tasa marginal máxima de la tarifa anual, no una tasa fija. El dividendo se suma al resto de ingresos y se acredita el impuesto extranjero (art. 5).

### 2.4 Intereses y la retención de 2026

- LIF 2026, art. 24: "Durante el ejercicio fiscal de 2026 la tasa de retención anual a que se refieren los artículos 54 y 135 de la Ley del Impuesto sobre la Renta será del 0.90 por ciento" (0.50% en 2025, según el doc `01`).
- Es un **pago provisional sobre el capital**, no sobre el interés. Lo que se acumula en la anual es el **interés real** (interés menos ajuste por inflación, art. 134). Quien solo tenga intereses por hasta 100,000 MXN puede tomar la retención como pago definitivo (art. 135).
- **Inferencia:** con CETE 28 en 6.15% (22-sep-2026, doc `01`), la retención de 0.90% del capital equivale a ~15% del interés nominal. Si la inflación rondara 4% (nv), sería ~40% del interés real. En la anual se recupera lo que exceda al impuesto sobre el interés real.

### 2.5 Impuesto sucesorio de EUA para no residentes

- **Umbral y crédito.** Las instrucciones del Form 706-NA (revisión 09/2025) obligan a declarar si los activos en EUA "exceeds the filing threshold of $60,000". El crédito unificado máximo es de 13,000 USD (26 USC 2102(b)(1)), igual al impuesto sobre los primeros 60,000 USD según la tarifa de 26 USC 2001(c), que sube de 18% a **40%** arriba de 1 MUSD.
- **Tratados.** Las instrucciones listan solo 15 países con tratado sucesorio: Australia, Austria, Canadá (vía el tratado de ISR), Dinamarca, Finlandia, Francia, Alemania, Grecia, Irlanda, Italia, Japón, Países Bajos, Sudáfrica, Suiza y Reino Unido. **México no está.** Y como México no grava herencias (art. 93 fr. XXII), no hay crédito que compense: el impuesto de EUA es costo puro.
- **Qué se considera situado en EUA.** "Generally, no matter where stock certificates are physically located, stock of corporations organized in or under U.S. law is property located in the United States, and all other corporate stock is property located outside the United States" (706-NA). 26 CFR 20.2104-1(a)(5): "Shares of stock issued by a domestic corporation, irrespective of the location of the certificates". Los ETFs de EUA (IVV, VOO, SPY) son sociedades de inversión reguladas (RIC) de EUA. La excepción parcial para RIC de 26 USC 2105(d) "shall not apply to estates of decedents dying after December 31, 2011".
- **Ilustración** (sin deducciones; réplica V05): 100,000 USD → 10,800 USD de impuesto (10.8%); 250,000 → 57,800 (23.1%); 1 MUSD → 332,800 (33.3%). El umbral de 60,000 USD equivale a **~1.03 millones de MXN** con el tipo de cambio de 17.25.

### 2.6 ¿Cambia el *situs* si la acción se compra en el SIC y se custodia vía Indeval?

- **Lo verificado.** La regla del IRS no depende del lugar de custodia ni de los certificados. El inversionista del SIC es dueño de la misma acción extranjera, que custodia un depósito central mexicano (Indeval) a través de custodios en el extranjero. El W-8BEN del SIC, de hecho, se tramita vía Indeval (doc `01`). Que la cadena de custodia no cambia la titularidad económica es **inferencia** sobre la estructura del SIC; no revisé el reglamento del SIC.
- **Lo que no existe.** No encontré ninguna resolución del IRS, sentencia ni guía del SAT o de la CNBV sobre el *situs* de valores del SIC.
- **Conclusión, con grado B:** la lectura dominante es que **las acciones y ETFs de EUA comprados en el SIC sí son activos con *situs* en EUA**. Así lo afirman también fuentes secundarias mexicanas (asesoresinversion.com, jul-2026). Que en la práctica la sucesión pase por Indeval sin un custodio de EUA que exija el certificado de transferencia del IRS es un **hueco de cobro, no una exención**. Apostar a él es incumplir.

### 2.7 ETFs UCITS irlandeses del SIC

- **Qué son.** ETFs de sociedades irlandesas (plc o ICAV) bajo la norma UCITS de la UE. Por la regla del IRS, "all other corporate stock is property located outside the United States": **no son activos situados en EUA**.
- **Irlanda tampoco cobra.** La s.75 de la CATCA 2003 exenta del impuesto irlandés a herencias las unidades de fondos de inversión "where the disponer and beneficiary are foreign-domiciled and foreign-resident" (Revenue, notas de guía, hasta la Finance Act 2024).
- **Dividendos.** El fondo irlandés recibe los dividendos de EUA con **15%** de retención (tratado EUA-Irlanda, art. 10(2)(b)). Un ETF de EUA en el SIC paga **10%** con W-8BEN y 30% sin él. Con un rendimiento por dividendo del S&P de ~0.99% (SPY a 12 meses), la fuga anual es de **0.15 pp** en el UCITS, contra **0.10 pp** y **0.30 pp** (réplica V05).
- **Acumulación contra distribución. Inferencia:** un UCITS de acumulación (CSPX, VUAA) no reparte dividendos, así que el mexicano no paga el 10% adicional ni acumula dividendos cada año. Paga solo al vender, con el 10% del art. 129 (fr. I o II). Esto último es inferencia de la letra: no encontré regla ni criterio del SAT específico. El régimen de REFIPRE (art. 176) solo aplica "cuando el contribuyente ejerza el control efectivo", lo que no ocurre con una participación minoritaria en un fondo público.
- **Cuáles hay en el SIC** (Yahoo, 1 año al 24-sep-2026; réplica V05):

| Ticker Yahoo | Fondo | Precio por título | Sesiones con volumen | Mediana diaria (MXN) |
|---|---|---|---|---|
| CSPXN.MX | iShares Core S&P 500 UCITS, acumulación, TER 0.07%, IE00B5BMR087 | 14,725.50 | 249/252 | 47.1 M |
| VUAAN.MX | Vanguard S&P 500 UCITS, acumulación | 2,630.00 | 251/252 | 5.3 M |
| IUSAN.MX | iShares S&P 500 UCITS, distribución, TER 0.07%, IE0031442068 | 1,304.43 | 14/213 | ~0 |
| VWRAN.MX | Vanguard FTSE All-World UCITS | 3,413.86 | 239/252 | 0.64 M |
| ISACN.MX | iShares MSCI ACWI UCITS | 2,192.08 | 199/252 | 0.67 M |
| EIMIN.MX | iShares Core MSCI EM IMI UCITS | 979.00 | 195/250 | 0.75 M |
| CNDXN.MX | iShares NASDAQ 100 UCITS | 31,040.00 | 209/252 | 4.8 M |
| IWDAN.MX | iShares Core MSCI World UCITS | 2,603.90 | 155/249 | 0.04 M |
| IVV.MX (EUA, para comparar) | iShares Core S&P 500 ETF | 13,673.23 | 250/252 | 73.8 M |

Que GBM permita comprar cada uno desde la app: (nv).

### 2.8 SPIVA como meta: qué mide y qué no

- Compara todos los fondos activos de una categoría contra el índice de la categoría, incluyendo los que cerraron. Por eso corrige el sesgo de supervivencia. Reporta el % de fondos por debajo del índice (equiponderado por conteo) y rendimientos promedio equiponderados y ponderados por activos.
- En México, el índice es el **S&P/BMV IRT**, el IPC con dividendos. Los fondos de la categoría "Mexico Equity" pueden tener valores fuera del índice, incluso ETFs extranjeros. En 2024, el cuartil superior tenía en promedio 74.3% fuera del IRT y 16.4% en fondos indexados y ETFs extranjeros.
- **Inferencia central:** si la categoría permite comprar el S&P 500, parte de "ganarle al IPC" es una apuesta de país y moneda. En 2015-2024 bastaba 13.8% en el S&P 500 para superar al IPC por 2 pp al año (réplica V05).

---

## 3. Fuentes primarias y canónicas

| Tema | Fuente primaria | Qué se usa |
|---|---|---|
| ISR bursátil, dividendos, intereses, herencias, REFIPRE | LISR, texto vigente (Cámara de Diputados) | Arts. 5, 54, 93 fr. XXII, 129, 134, 135, 140, 142 fr. V y 176 |
| Retención 2026 | LIF 2026 (DOF 07-11-2025) | Art. 24: 0.90% |
| Reglas operativas del SAT | Resolución Miscelánea Fiscal 2026 | **No consultada en esta sesión** (nv). Es donde vivirían las reglas sobre ETFs del SIC |
| *Estate tax* de no residentes | 26 USC 2001(c), 2101-2106; 26 CFR 20.2104-1 y 20.2105-1; instrucciones del Form 706-NA (09/2025) | Tarifa, crédito, *situs*, umbral y tratados |
| Retención de dividendos | Tratados EUA-México (1992, art. 10) y EUA-Irlanda (1997, art. 10) | 10% y 15% en cartera |
| Impuesto irlandés a herencias | CATCA 2003 s.75, notas de guía de Revenue (hasta la Finance Act 2024) | Exención para no domiciliados y no residentes |
| Meta de desempeño | SPIVA U.S. (Year-End 2025 y Mid-Year 2026) y SPIVA Latin America (Year-End 2024 y Primer semestre 2025) | % por debajo, supervivencia y rendimientos |
| Operativa GBM | FAQ de GBM (SIC, dividendos, W-8BEN, constancias) | Retenciones, CFDI y ruta en la app |

---

## 4. Lo más reciente (estado al 25-sep-2026)

1. **Paquete Económico 2026.** El 7-nov-2025 se publicaron la LIF 2026 y reformas al CFF, al IEPS y a la LFD. **No hubo decreto de reforma a la LISR**: el texto vigente de la Cámara sigue con última reforma del DOF 01-04-2024. Los cambios de ISR de 2026 (plataformas digitales, fintech) van en la LIF. **Para bolsa, nada cambió en 2026 salvo la retención de intereses: de 0.50% a 0.90%.**
2. **SPIVA U.S. Mid-Year 2026** (corte 30-jun-2026, PDF creado el 16-sep-2026): **83.33%** de los fondos *large-cap* por debajo del S&P 500 a 10 años. La edición de cierre de 2025 daba 85.59%.
3. **SPIVA Latin America Year-End 2025:** publicada, pero **no obtenida** (403). Según un resumen de buscador (nv): 75.6% de los fondos mexicanos por debajo del IRT a 10 años. La última cifra verificada es la del primer semestre de 2025: **73.17%**.
4. **Instrucciones del Form 706-NA, revisión 09/2025:** mantienen el umbral de 60,000 USD y el crédito de 13,000 USD para no residentes.
5. **Constancias fiscales 2025 de GBM:** disponibles en la app (FAQ vigente al 25-sep-2026).

---

## 5. Evidencia (réplica V05; cifras de PDF oficiales congelados y cálculo propio)

| Afirmación recibida | Cifra en la fuente | Edición donde aparece | Cifra más reciente | Veredicto |
|---|---|---|---|---|
| 85.6% de los *large-cap* de EUA por debajo del S&P 500 a 10 años | 85.59% | Year-End 2025 (corte 31-dic-2025) | 83.33% (Mid-Year 2026) | confirmada con matices |
| 82.9% de los fondos mexicanos por debajo de su índice a 10 años | 82.93% (contra S&P/BMV IRT) | Year-End 2024 (corte 31-dic-2024) | 73.17% (primer semestre de 2025) | confirmada con matices |
| Ganadores con cartera distinta y ETFs extranjeros | 74.3% fuera del índice; 16.4% en fondos indexados y ETFs extranjeros | Year-End 2024: **cuartil superior de 2024, a 1 año** | — | confirmada con matices |

- **Los fondos mexicanos que invierten afuera pierden más** (10 años a 2024, equiponderado): los de EUA en MXN rinden 12.65% contra 17.08% del S&P 500 (MXN), con 86.67% por debajo. Los globales en MXN rinden 7.09% contra 14.33% del S&P World (MXN), con **100%** por debajo.
- **Mecánica** (NAFTRAC y SPY × DEXMXUS, rebalanceo mensual, sin costos): de 2015 a 2024, IPC 3.53% y S&P 500 MXN 16.98%. Con 10% en el S&P, +1.45 pp al año. Diferencia mensual con t NW(6) = 1.99 (apoyo al límite). **En 2016-2025, t = 1.20 (inconcluso).**

---

## 6. Traducción operable

### 6.1 Principio rector

La ventaja fiscal y estructural es **segura y medible**: se conoce de antemano y no depende de acertar al mercado. Antes de buscar *alpha*, el sistema debe capturar la parte gratuita: menos fuga por dividendos, sin exposición sucesoria innecesaria y pérdidas bien aprovechadas.

### 6.2 Reglas para la cuenta arena (20,000 MXN, temporadas de 6 meses)

1. **Regla:** el *estate tax* es irrelevante: 1,160 USD está muy debajo de 60,000 USD.
2. **Regla:** el ISR de 10% se paga en la anual y no baja el TWR de la temporada (doc `01`). Aun así, se registra la ganancia fiscal estimada por emisora en `bitacora/operaciones.csv`.
3. **Regla:** no tramitar el W-8BEN del SIC. Cuesta 75 USD + IVA, ~7.6% de la cuenta, y el ahorro por dividendos es de 0.2 pp al año sobre el monto en ETFs de EUA.
4. **Regla:** para exposición al S&P 500 en el SIC con cuenta chica, el título de **VUAA** (~2,630 MXN, 13% de la cuenta) permite fraccionar mejor que CSPX (~14,700 MXN, 74%) o IVV (~13,700 MXN). Falta verificar que GBM lo permita.

### 6.3 Reglas para el patrimonio principal (propuesta; no modifica `config/parametros.json`)

1. **Regla:** si los activos con *situs* en EUA (acciones y ETFs de EUA en el SIC, Trading USA) superan **1,000,000 MXN**, preferir para el núcleo indexado ETFs UCITS irlandeses de acumulación con liquidez diaria (hoy CSPX y VUAA para el S&P 500; VWRA o ISAC para el mundo, con liquidez media). El costo fiscal extra por dividendos es de ~0.05 pp al año contra un ETF de EUA con W-8BEN.
2. **Regla:** las acciones individuales de EUA sí son activos situados en EUA. Su suma se vigila contra el umbral y se documenta en el tablero de riesgo.
3. **Regla:** en noviembre, antes del cierre fiscal, revisar ganancias y pérdidas del art. 129. Las pérdidas valen 10 años, pero solo contra ganancias bursátiles, y **se pierden si no se aplican cuando se puede**. Si existe una regla contra recompras inmediatas (*wash sale*) para personas físicas en México: (nv).
4. **Regla:** un fondo activo mexicano solo se compara contra **su índice y contra el S&P 500 en MXN**. Una ventaja contra el IPC con 10-20% en el S&P no cuenta como talento.

### 6.4 *Checklist* antes de comprar un ETF del SIC

| # | Pregunta | Dónde se verifica |
|---|---|---|
| 1 | ¿Domicilio del fondo (IE, US, LU)? | Página del emisor (ISIN IE… o US…) |
| 2 | ¿Acumulación o distribución? | Página del emisor ("Use of Income") |
| 3 | ¿TER? | Página del emisor |
| 4 | ¿Precio por título frente a la cuenta (solo títulos completos)? | Yahoo o la app |
| 5 | ¿Sesiones con volumen de las últimas 252 ≥ 90% y mediana diaria ≥ 20 veces la orden? | `reproducir.py` de V05, función `liquidez` |
| 6 | ¿Retención de dividendos aplicable (10%, 15% o 30%)? | Tratado y W-8BEN |
| 7 | ¿Suma a la exposición con *situs* en EUA? | Tabla 2.5 |
| 8 | ¿Es de acciones (art. 129 fr. II) o de bonos o materias primas (trato no verificado)? | Folleto; consulta fiscal |

### 6.5 Parámetros propuestos (para revisión con el dueño; no están en `parametros.json`)

| Parámetro | Valor propuesto | Justificación |
|---|---|---|
| `umbral_situs_eua_mxn` | 1,000,000 | 60,000 USD × ~17 MXN/USD, con margen |
| `preferir_ucits_si_situs_eua_supera_umbral` | true | *Estate tax* de 10.8% a 33% efectivo arriba del umbral |
| `liquidez_min_sesiones_con_volumen` | 0.90 | IUSA (14/213) quedaría fuera; CSPX y VUAA entran |
| `revision_perdidas_art129_mes` | 11 | Aplicar pérdidas antes del cierre del ejercicio |
| `w8ben_sic_min_patrimonio_eua_mxn` | 1,500,000 | Con 0.2 pp al año de ahorro, 75 USD + IVA se recuperan en ~1 año con ~750k en ETFs de EUA. Duplicado por prudencia (inferencia) |

---

## 7. Trampas

1. **Citar una edición vieja de SPIVA como vigente.** 85.6% y 82.9% ya fueron superadas: 83.33% (EUA, mitad de 2026) y 73.17% (México, mitad de 2025).
2. **Confundir supervivencia con bajo desempeño.** En la edición de mitad de 2025, 82.93% es la supervivencia a 10 años de los fondos mexicanos; el bajo desempeño es 73.17%.
3. **Medir contra el IPC de precio.** SPIVA usa el S&P/BMV IRT, con dividendos. El IPC de precio queda ~2-3 pp al año más abajo (nv) y hace ver mejores a los fondos.
4. **"Fondos grandes"** no son fondos con mucho patrimonio: son *large-cap*.
5. **Creer que comprar en el SIC y en pesos quita el *estate tax*.** La regla es "no matter where stock certificates are physically located".
6. **Creer que el UCITS irlandés siempre gana.** Con W-8BEN, un ETF de EUA pierde 10% por dividendos y el UCITS 15%. La ventaja del UCITS es sucesoria y de diferimiento, no de retención.
7. **Tratar el 10% como el único impuesto sobre dividendos extranjeros.** También se acumulan en la anual, con acreditamiento.
8. **Tomar el "35%" de la FAQ de GBM como tasa fija.** Es el tope de la tarifa progresiva.
9. **Dejar pasar una pérdida bursátil aplicable.** Si pudiendo aplicarla no se aplica, ese monto se pierde.
10. **Confundir la retención de 0.90% con una tasa sobre el interés.** Es sobre el capital y a cuenta.
11. **Comprar una emisora sin liquidez en el SIC.** IUSA tuvo volumen en 14 de 213 sesiones.
12. **Confiar en resúmenes de buscador.** Uno reportó "85.37% a 10 años" en México, atribuido a la edición de cierre de 2022. En los PDF congelados, 85.37% es el dato **ajustado por riesgo** (Report 1b) de la edición de cierre de 2023. Otro repitió 75.6% para 1 y 10 años. Solo el PDF congelado cuenta.
13. **Citar un PDF de `spglobal.com` sin congelarlo.** El sitio bloquea descargas automáticas (403) y regenera los PDF: la misma edición cambia de huella entre capturas.

---

## 8. Examen de titulación

1. **Compraste 10 títulos de VOO en el SIC a 10,000 MXN cada uno y los vendiste a 12,000 MXN, con 0.29% de comisión por lado. La inflación del periodo fue 4%. ¿Cuál es el ISR aproximado?**
   Costo actualizado ≈ (100,000 + 290) × 1.04 = 104,302. Venta neta = 120,000 − 348 = 119,652. Ganancia ≈ 15,350, e ISR (10%) ≈ **1,535 MXN**, pagado en la anual de abril. GBM no retiene en la venta.

2. **Tuviste una pérdida bursátil de 30,000 MXN en 2026 y un sueldo de 600,000 MXN. ¿Puedes restarla del sueldo?**
   No. Solo se resta de ganancias del art. 129 en 2026 o en los 10 años siguientes, actualizada por inflación. Si en un año hay ganancia y no la aplicas, pierdes ese monto.

3. **Un dividendo de 100 USD de una acción de EUA llega a tu cuenta del SIC sin W-8BEN. ¿Qué retenciones hay?**
   EUA retiene 30% (30 USD). GBM retiene 10% sobre el neto (7 USD). En la anual acumulas el dividendo y acreditas el impuesto extranjero (art. 5). Con W-8BEN, EUA retendría 10%.

4. **¿Cuánto retiene GBM en 2026 sobre 100,000 MXN en Smart Cash todo el año?**
   0.90% × 100,000 = **900 MXN**, como pago provisional (art. 24 LIF 2026). En la anual se compara contra el impuesto sobre el interés real.

5. **Un mexicano muere con 300,000 USD en acciones de EUA compradas en el SIC. ¿Hay *estate tax*?**
   Según la regla del IRS, sí: son acciones de sociedades de EUA "irrespective of the location of the certificates". Impuesto tentativo = 70,800 + 34% × 50,000 = 87,800; menos 13,000 de crédito = **74,800 USD**. México no tiene tratado sucesorio con EUA. No hay resolución sobre el SIC (grado B).

6. **¿Y si fueran 300,000 USD en CSPX?**
   CSPX es una acción de una sociedad irlandesa (iShares VII plc): no tiene *situs* en EUA. Irlanda lo exenta de su impuesto a herencias si causante y heredero no tienen domicilio ni residencia allá. *Estate tax* de EUA: 0.

7. **¿Por qué el UCITS pierde más por dividendos que un ETF de EUA con W-8BEN, y cuánto?**
   Porque el tratado EUA-Irlanda fija 15% y el de EUA-México 10%. Con un rendimiento por dividendo de ~1%, son ~0.05 pp al año de diferencia.

8. **SPIVA dice que 82.93% de los fondos mexicanos… ¿qué?**
   Depende de la edición. En Year-End 2024: quedaron por debajo del S&P/BMV IRT a 10 años. En la de mitad de 2025: **sobrevivieron** 10 años (34 de 41). Siempre se cita la edición, la fecha de corte y la tabla.

9. **Un fondo mexicano de acciones le ganó al IPC por 2 pp al año de 2015 a 2024. ¿Tiene talento?**
   No se puede saber sin ver su cartera. Con 13.8% en el S&P 500 en pesos y cero talento, se obtenía +2 pp. Hay que compararlo contra una mezcla IPC/S&P con sus mismos pesos.

10. **¿Qué cambió en 2026 en la fiscalidad bursátil de una persona física?**
    Solo la retención sobre intereses, que pasó de 0.50% a 0.90%. La LISR no se reformó: el 10%, las pérdidas a 10 años y el régimen de dividendos siguen igual.

11. **¿Por qué no conviene el W-8BEN del SIC en la cuenta arena?**
    Cuesta 75 USD + IVA (~7.6% de 20,000 MXN) y ahorra ~0.2 pp al año sobre lo invertido en ETFs de EUA: nunca se recupera en una cuenta así.

12. **¿Cuál es la conclusión operable de SPIVA para este sistema?**
    Que la meta mínima es el índice en MXN (S&P 500, IPC o el *benchmark* 50/50) neto de costos. Que 83-87% de los *large-cap* de EUA y 73-88% de los fondos mexicanos no la alcanzaron a 10 años. Y que los fondos mexicanos que invierten afuera fallan aún más (87-100%). Comprar el índice por ETF ya supera a la mayoría.

---

## 9. Fuentes

1. Ley del Impuesto sobre la Renta, texto vigente (última reforma DOF 01-04-2024), Cámara de Diputados: https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf
2. Ley de Ingresos de la Federación para el Ejercicio Fiscal de 2026 (DOF 07-11-2025), art. 24: https://www.diputados.gob.mx/LeyesBiblio/pdf/LIF_2026.pdf
3. Decretos del 7-nov-2025 (LIF, CFF, IEPS, LFD); no incluyen la LISR. Ejemplo, reforma al CFF: https://www.diputados.gob.mx/LeyesBiblio/ref/cff/CFF_ref62_07nov25.pdf · resumen: https://www.hklaw.com/en/insights/publications/2025/11/reforma-fiscal-para-2026-en-mexico · https://blog.garridolicona.com/fiscal-legal/reformas-en-materia-del-isr-para-2026
4. IRS, Instructions for Form 706-NA (Revised 09/2025): https://www.irs.gov/instructions/i706na
5. 26 CFR 20.2104-1: https://www.ecfr.gov/current/title-26/chapter-I/subchapter-B/part-20/subject-group-ECFR3cda1c0d2fca6d8/section-20.2104-1
6. 26 USC 2001 (tarifa): https://www.law.cornell.edu/uscode/text/26/2001 · 2102 (crédito): https://www.law.cornell.edu/uscode/text/26/2102 · 2105 (bienes fuera de EUA; RIC): https://www.law.cornell.edu/uscode/text/26/2105
7. IRS, Estate & gift tax treaties (international): https://www.irs.gov/businesses/small-businesses-self-employed/estate-gift-tax-treaties-international
8. Tratado EUA-México (1992) y protocolos, art. 10: https://www.irs.gov/pub/irs-trty/mexico.pdf
9. Tratado EUA-Irlanda (1997), art. 10: https://www.irs.gov/pub/irs-trty/ireland.pdf
10. Irish Revenue, Notes for Guidance CATCA 2003, Part 9 (s.75): https://www.revenue.ie/en/tax-professionals/documents/notes-for-guidance/cat/2024/part09.pdf
11. iShares Core S&P 500 UCITS ETF (Acc), CSPX: https://www.ishares.com/uk/individual/en/products/253743/ishares-sp-500-b-ucits-etf-acc-fund
12. iShares S&P 500 UCITS ETF (Dist), IUSA: https://www.ishares.com/uk/individual/en/products/251900/ishares-sp-500-ucits-etf-inc-fund
13. GBM, "¿Cómo funcionan los impuestos por las acciones de empresas extranjeras en el SIC?": https://gbm.com/faqs/como-funcionan-los-impuestos-por-las-acciones-de-empresas-extranjeras-en-el-sic/
14. GBM, "¿Cómo funcionan los impuestos sobre los dividendos en Trading MX?": https://gbm.com/faqs/como-funcionan-los-impuestos-sobre-los-dividendos-en-trading-mx/
15. GBM, "¿Qué es y cómo funciona el W-8BEN para Trading MX y SIC?": https://gbm.com/faqs/que-es-y-como-funciona-el-w-8ben-para-trading-mx-y-sic/
16. GBM, "¿Cómo y dónde recibo los Comprobantes Fiscales o CFDI por mis ganancias?": https://gbm.com/faqs/como-y-donde-recibo-los-comprobantes-fiscales-o-cfdi-por-mis-ganancias/
17. S&P DJI, SPIVA U.S. Scorecard Year-End 2025: https://www.spglobal.com/spdji/en/documents/spiva/spiva-us-year-end-2025.pdf · Mid-Year 2026: https://www.spglobal.com/spdji/en/documents/spiva/spiva-us-mid-year-2026.pdf · página: https://www.spglobal.com/spdji/en/spiva/article/spiva-us/
18. S&P DJI, SPIVA Latin America Year-End 2024: https://www.spglobal.com/spdji/en/documents/spiva/spiva-latin-america-year-end-2024.pdf · Primer semestre de 2025 (español): https://www.spglobal.com/spdji/es/documents/spiva/spiva-latin-america-mid-year-2025-es.pdf · Year-End 2025 (no obtenido): https://www.spglobal.com/spdji/en/documents/spiva/spiva-latin-america-year-end-2025.pdf
19. Fuente secundaria (solo contraste): asesoresinversion.com, "ETFs en pesos o en dólares desde México: SIC vs. cuenta en dólares" (jul-2026): https://asesoresinversion.com/academia/mercado-accionario/comprar-etf-pesos-o-dolares-mexico/
20. Réplica propia: `laboratorio/replicas/V05-spiva-y-fiscalidad-sic/` (README, `reproducir.py`, `resultados.json`, `datos/`)

### Registro de verificación (25-sep-2026)

- `reproducir.py` de V05 busca **29 frases literales** en los textos legales congelados (LISR, LIF 2026, 706-NA, eCFR, USC, tratados, Revenue y GBM) y falla si alguna falta. Las 29 están.
- La tarifa de 26 USC 2001(c) se verifica tramo por tramo contra el texto antes de usarse en la ilustración.
- No verificado: la Resolución Miscelánea Fiscal 2026 (reglas sobre ETFs del SIC), el trato de los ETFs de renta fija del SIC, que GBM permita comprar UCITS desde la app, el TER de VUAA, la existencia de una regla de *wash sale* para personas físicas y la cifra de SPIVA Latin America Year-End 2025.
