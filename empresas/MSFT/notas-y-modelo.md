# MSFT: notas del 10-K FY2026 y modelo integrado de tres estados

> **FASE 0 (formación).** Nada de este documento es recomendación de compra o venta. Los escenarios son supuestos de **mecanismo**: no son pronósticos, ni guía del emisor, ni consenso. Montos en millones de USD salvo que se indique otra cosa. El ejercicio fiscal de Microsoft termina el 30 de junio.
>
> Corte: 2026-09-25. Archivos: `modelo/base.json` (transcripción), `modelo/modelo.py` (cálculo), `modelo/resultados.json` (salida), `modelo/SHA256SUMS.txt` y `modelo/datos/` (insumos congelados). Capítulos: [03 valuación](../../conocimiento/03-maestria-valuacion-y-analisis-fundamental.md), [25 pronóstico y estados financieros](../../conocimiento/25-pronostico-de-resultados-y-estados-financieros.md), [23 geopolítica](../../conocimiento/23-geopolitica-y-riesgo-politico-global.md) y [24 política pública](../../conocimiento/24-politica-publica-regulacion-y-mercados.md).

Convención de etiquetas:
- **Hecho:** cifra o texto del filing, con documento, nota o visor y fecha.
- **Cálculo:** aritmética sobre hechos.
- **Inferencia:** lectura propia. Puede estar equivocada.
- **Supuesto:** insumo de escenario elegido por el analista.

## 0. Resumen

1. **Hecho.** El pasivo por arrendamientos financieros subió de 46,172 a 66,594 (+44.2%). Además, Microsoft tiene **US$329.1 mil millones** en arrendamientos firmados que todavía no comienzan: "primarily for datacenters", "with some arrangements subject to certain contractual conditions being met", con inicio entre FY2027 y FY2033 (Nota 13). **Inferencia:** esa cifra no se suma a la deuda descontada (§2.1). Se modela como arrendamientos nuevos que entran al balance año por año (§5).
2. **Cálculo.** El FCF (CFO − capex) de FY2026 fue **66,987**, y **63,886** después de pagar 3,101 de principal de arrendamientos financieros. El margen FCF bajó de 30.2% (FY2024) a 20.2% (FY2026) porque el capex en efectivo pasó de 18.1% a 34.9% de los ingresos. Si se suman el aumento de PPE por pagar y los activos recibidos en arrendamiento financiero, la inversión devengada aproximada fue de **160,356 (48.3% de los ingresos)**.
3. **Hecho (F3).** Sin el efecto de las inversiones en OpenAI, la utilidad neta crece **22.13%** y no el 31.34% del GAAP (133,749 − 4,963 = 128,786 contra 101,832 + 3,620 = 105,452). OpenAI aportó **24.1 mil millones de ingresos (7.3% del total)** y **6.0 mil millones de cuentas por cobrar (7.4%)**.
4. **Modelo.** El motor reproduce FY2025 y FY2026 **sin diferencia** (C13: máx |modelo − reportado| = 0.0). Los 540 registros de control dan **0 FALLA** (517 OK, 19 INFO, 4 NO_APLICA). La transcripción se contrastó contra XBRL con **167 coincidencias exactas**, 2 diferencias de redondeo del emisor explicadas y 0 fallas.
5. **Escenarios de mecanismo (supuestos).** Con la política de capital fija (dividendos +10% anual y 22 mil millones de recompras al año):
   - **tensión**: requiere **28,259** de financiamiento externo en FY2027E y 2,208 en FY2028E;
   - **intermedio**: acumula 596 mil millones de FCF en 5 años;
   - **eficiencia**: acumula 796 mil millones.
6. **DCF inverso.** Datos: precio 497.93 (24-sep-2026), WACC 10.2%, g terminal 3.0% y margen FCF de 20.2% constante. El precio descuenta un crecimiento de ingresos de **21.5% anual por 10 años**. Con el margen FCF de FY2024 (30.2%) el implícito baja a 16.0%. El valor terminal pesa 68%.
7. **Sensibilidad geopolítica (mecanismo).** Un choque de suministro de 2 años sobre el escenario intermedio resta **79.8 mil millones** de FCF acumulado (−13.4%). También abre un faltante de caja de 8.7 mil millones en FY2027E.

## 1. Fuentes y método de lectura

| Id | Documento | Fecha | Uso |
|---|---|---|---|
| F1 | 10-K FY2026 (accn 0001193125-26-323660): https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm | 29-jul-2026 | Estados financieros y notas 1, 3, 4, 6, 10, 11, 12, 13, 15, 17 y 18 |
| F2 | 10-K FY2025 (accn 0000950170-25-100235) | 30-jul-2025 | Balance al 30-jun-2024 (R4) y componentes de deuda y arrendamiento de ese saldo (R72, R90) |
| F3 | 8-K del 29-jul-2026, Ex. 99.1 (comunicado FY26 Q4): https://www.sec.gov/Archives/edgar/data/789019/000119312526323632/msft-ex99_1.htm | 29-jul-2026 | Puente GAAP contra no GAAP |
| F4 | SEC companyfacts XBRL (CIK 789019) | descargado 25-sep-2026 | Segunda lectura para la doble comprobación |
| F5 | Yahoo Finance chart v8 MSFT | cierre 24-sep-2026 | Precio |
| F6 | FRED DGS10 | 23-sep-2026 | Tasa del bono a 10 años: 5.11% |
| F7 | Damodaran, *Betas by Sector (US)*, datos a enero de 2026 | descargado 25-sep-2026 | β desapalancada del software (1.25) |
| F8 | conocimiento/03 §2.3 y §6.1 (cita a Damodaran, sep-2026) | 25-sep-2026 | ERP de 4.31% y diferencial de default de EUA de 0.22% |

**Limitación de acceso.** `www.sec.gov/Archives` respondió 403 al User-Agent declarado ("SistemaInversionNew1/1.0 investigacion"), porque la SEC exige un correo para ese directorio. No se usó el correo de nadie. Por eso:
- No se descargó el htm completo del 10-K.
- La primera lectura se hizo con los **visores XBRL "R" de la SEC** (R2, R4, R6, R7 y las notas), que son renderizaciones oficiales de la misma presentación.
- La segunda lectura, automática, salió de **companyfacts XBRL** (data.sec.gov sí acepta ese User-Agent).
- **Número de página.** El índice del 10-K confirma que el Item 8 empieza en la **p. 50**. Las páginas impresas de cada nota **no se verificaron**. La tanda 2 de Maquiavelo reporta estados en pp. 50-54, Nota 3 en p. 62, Nota 6 en p. 69, Nota 13 en pp. 77-78, Nota 15 en pp. 79-80 y Nota 17 en pp. 81-82: **no verificado aquí**. Cada cifra se cita por número de nota y visor R, que es un localizador exacto dentro del filing.
- No se leyeron el MD&A (Item 7) ni la transcripción de la llamada de resultados (ver pendientes).

**Contraste con la tanda 2 (Maquiavelo, 24-sep-2026).** Cada cifra de su informe coincide con esta lectura: 66,594, 21,925, 329.1 mil millones, 3,101, 26.7 y 6.9 mil millones, 24.1 y 6.0 mil millones, 16,719, 12,405, 24.8 mil millones, 66,987 y 63,886, y 22.13% contra 31.34%. Su frase "algunos condicionados" corresponde al texto de la Nota 13 citado arriba.

## 2. Hallazgos de las notas

### 2.1 Arrendamientos (Nota 13; visores R23, R89-R93)

| Hecho (F1, 30-jun) | FY2026 | FY2025 |
|---|---|---|
| Pasivo por arrendamiento financiero (circulante / largo plazo) | 66,594 (4,290 / 62,304) | 46,172 (3,172 / 43,000) |
| Pasivo por arrendamiento operativo (circulante / largo plazo) | 21,925 (5,393 / 16,532) | 22,861 (5,424 / 17,437) |
| PPE neto por arrendamiento financiero (costo − depreciación acumulada) | 67,281 (82,712 − 15,431) | 44,015 |
| Derecho de uso obtenido: financiero / operativo | 24,608 / 4,555 | 20,511 / 7,826 |
| Principal pagado (flujo de financiamiento) | 3,101 | 2,283 |
| Interés de arrendamiento financiero (flujo operativo) | 2,547 | 1,372 |
| Plazo promedio y tasa: financiero / operativo | 13 años, 4.5% / 6 años, 3.7% | 13 años, 4.2% / 6 años, 3.5% |
| Pagos no descontados: financiero / operativo | 89,686 (interés imputado 23,092) / 24,706 (2,781) | — |
| Pagos de FY2027: financiero / operativo | 7,121 / 6,082 | — |

- **Dónde está en el balance (hecho).** El pasivo financiero está **dentro** de "Other current liabilities" y "Other long-term liabilities". El activo está dentro de "Property and equipment, net". En `base.json` el pasivo se separa en `arrendamientos_financieros` y se resta de los otros pasivos. Esa resta está en `memo` y la prueban C01 y la doble comprobación.
- **No iniciados (hecho).** "As of June 30, 2026, we had additional leases, primarily for datacenters, that had not yet commenced of $329.1 billion, with some arrangements subject to certain contractual conditions being met. These leases will commence between fiscal year 2027 and fiscal year 2033 with lease terms of 1 year to 20 years."
- **Por qué NO se suman los 329.1 mil millones a la deuda descontada (inferencia):**
  1. **Bases distintas.** Los 88,519 reconocidos (66,594 + 21,925) son **valor presente**, descontado a 4.5% y 3.7%, de pagos por activos **ya entregados**. Esos activos están en el balance. La nota no dice si los 329.1 mil millones están descontados. Su plazo de 1 a 20 años y su inicio escalonado a 7 años sugieren montos contractuales totales. Sumar un monto nominal futuro a un valor presente mezcla tiempo y tasa. Referencia: en los financieros vigentes, el VP es 74% del monto no descontado (66,594 / 89,686).
  2. **Contrato ejecutorio.** Hasta que comienza el arrendamiento, Microsoft no ha recibido el centro de datos ni debe el pago. El pasivo nace al inicio, **junto con un activo de igual monto**. Sumarlo hoy a la deuda carga el costo sin el activo ni los ingresos que ese activo generaría. Así se cuenta dos veces contra la valuación.
  3. **Hay condiciones.** "Some arrangements subject to certain contractual conditions": parte puede no materializarse.
  4. **Tratamiento correcto.** Modelarlos como flujo futuro: `nuevos_arrendamientos_financieros` de 25 a 50 mil millones al año en los escenarios. Suben el PPE y el pasivo al comenzar, y su principal y su interés reducen el FCF después de arrendamientos. En el DCF su costo entra por el margen FCF, no como deuda de hoy.
  5. **Escala.** Aun así, la cifra es **3.7 veces** el pasivo por arrendamientos reconocido y casi igual a los ingresos de FY2026 (331,839). Es la señal más clara del tamaño del compromiso de capacidad. Ninguna de estas cifras permite concluir sobre la solvencia por sí sola.
- **No se sabe (pendiente):** cuánto de los 329.1 mil millones será financiero y cuánto operativo. Tampoco su calendario por año.

### 2.2 PPE, compras por pagar y compromisos de construcción (Nota 6, R16)

- **Hecho.** Depreciación de 34.3 mil millones (FY2026), 22.0 (FY2025) y 15.2 (FY2024). "Servers, network equipment, and software" pasó de 132,836 a 215,874 a costo. Los edificios, de 137,921 a 182,749.
- **Hecho.** "Purchases of property and equipment remaining in accounts payable": **26.7 mil millones** (FY2026), 6.9 (FY2025) y 4.3 (FY2024). Compromisos de construcción: **34.6 mil millones**, "primarily related to datacenters".
- **Cálculo.** Las compras de PPE por pagar son 63% de proveedores (26,700 / 42,416). Los proveedores operativos serían ~15,716, o 54 días de costo de ventas. Los "145.5 días" que resultan del balance (C09) **no** son un DPO operativo.
- **Cálculo.** Inversión devengada aproximada = capex en efectivo + aumento de PPE por pagar + derecho de uso financiero = 115,948 + 19,800 + 24,608 = **160,356** en FY2026 (48.3% de los ingresos), contra 87,662 en FY2025. Capex en efectivo / D&A = 3.0 veces (2.2 en FY2025).
- **Inferencia.** El capex en efectivo **subestima** la inversión del año. El aumento de 19.8 mil millones en PPE por pagar difiere efectivo a FY2027: el FCF de FY2026 tiene a favor un efecto de calendario que se revierte si esas compras se pagan sin reponerse. Por eso el escenario tensión reduce ese saldo (§5).
- **Brecha del PPE (cálculo; pendiente).** La conciliación del motor deja **+7,173** no monetario en PPE en FY2026:
  - explican **+19,800** el aumento de PPE por pagar y **+4,700** la amortización de intangibles que va en D&A pero no reduce PPE (hecho XBRL);
  - quedan unos **17 mil millones** sin explicar con lo leído (bajas, transferencias u otro concepto). El 10-K no trae un roll-forward de PPE. El MD&A no se leyó.

### 2.3 OpenAI (Notas 1, 3 y 4; R11, R13, R14, R46; F3)

- **Hecho (Nota 1).** "We have an investment accounted for under the equity method that represents an approximate 25% interest on an as-converted basis." Compromisos de fondeo por 13.0 mil millones, de los que 11.9 ya se fondearon. "For fiscal year 2026, we recorded revenue from commercial arrangements with OpenAI, inclusive of revenue-sharing payments, of $24.1 billion, and accounts receivable from OpenAI as of June 30, 2026 was $6.0 billion."
- **Hecho (Nota 3).** Otros ingresos incluyen ganancias netas de OpenAI de **6.5 mil millones** en FY2026 y pérdidas de 4.8 y 1.5 mil millones en FY2025 y FY2024: "the net gains recorded for fiscal year 2026 primarily relate to the dilution gain from the OpenAI Recapitalization". Las inversiones por método de participación suman 12.0 mil millones (6.0 en FY2025, Nota 4).
- **Hecho (F3), puente no GAAP:**
  - utilidad neta 133,749 − 4,963 = **128,786** (FY2026) y 101,832 + 3,620 = **105,452** (FY2025);
  - UPA diluida 17.95 → 17.28 y 13.64 → 14.13;
  - ingresos y utilidad operativa no se ajustan. C14 prueba ambas sumas (OK).
- **Cálculo.** Crecimiento de la utilidad neta: **31.34%** GAAP contra **22.13%** sin OpenAI. OpenAI = 7.26% de los ingresos, 7.42% de las cuentas por cobrar y 3.9% de la UAI (6.5 / 165.9).
- **Inferencia:**
  - El 7.3% es la exposición **directa** informada, no todo el riesgo de IA. La dependencia también pasa por contratos futuros (las obligaciones de desempeño pendientes suman 684 mil millones; su parte de OpenAI no se leyó), por la inversión patrimonial y por la cobranza. La proporción no permite inferir una probabilidad de incumplimiento.
  - El ajuste del emisor está neto de impuestos. La ganancia de la Nota 3 está antes de impuestos. No hay que mezclarlas sin conciliar el impuesto.
  - El ajuste no elimina otras partidas no operativas: los 4,385 de inversiones y los 1,867 de derivados de la Nota 3 incluyen efectos que no son de OpenAI.

### 2.4 SBC, costo no reconocido y recompras contra retenciones (Notas 15 y 17; R25, R97, R101-R104)

| Hecho (F1) | FY2026 | FY2025 |
|---|---|---|
| Gasto por SBC (flujo y estado de variaciones) | 12,405 (3.74% de los ingresos) | 11,974 (4.25%) |
| Costo no reconocido / plazo promedio | **24.8 mil millones / 3 años** | — |
| RSU no vestidas (millones): inicial + otorgadas − vestidas − canceladas = final | 82 + 41 − 35 − 10 = **78** | 82 |
| Recompras del programa (acciones / monto) | 36 M / **16,719** | 31 M / 13,000 |
| Retenciones fiscales de empleados, **excluidas** del programa | **5.6 mil millones** | 5.4 mil millones |
| "Common stock repurchased" en el flujo / en el estado de variaciones | 22,271 / 22,286 (6,105 + 16,181) | 18,420 / 18,424 |
| Acciones en circulación: inicial + emitidas − recompradas | 7,434 + 29 − 36 = 7,427 | 7,434 |
| Programa: autorizado el 16-sep-2024 / disponible | 60.0 / 40.6 mil millones | — |

- **Cálculo.** Programa + retenciones − flujo = 16,719 + 5,600 − 22,271 = 48. El 5.6 está redondeado a 0.1 mil millones, así que el renglón del flujo equivale a programa + retenciones. Costo no reconocido / gasto anual = 2.0 años.
- **Inferencia (aproximada):**
  - Con 22.3 mil millones de efectivo, las acciones en circulación bajaron solo 7 millones (−0.09%). A 464.4 USD por acción, precio promedio del programa (cálculo), eso equivale a ~3.3 mil millones. **~85% del efectivo de recompras compensó la dilución de los planes de empleados.**
  - La SBC tiene costo económico aunque no consuma efectivo en el año. Al valuar hay que elegir **un** tratamiento: restar la SBC del FCF **o** cargar el costo de las recompras compensatorias, no ambos.
  - Aquí se reporta el FCF − SBC como variante (§2.6 y la malla del §7).

### 2.5 Segmentos, geografía y ofertas (Nota 18; R107, R109, R110)

| Hecho FY2026 (FY2025) | Ingresos | Utilidad operativa | Margen operativo (cálculo) | Crecimiento (cálculo) |
|---|---|---|---|---|
| Productivity and Business Processes | 139,996 (120,810) | 83,879 (69,773) | 59.9% | +15.9% |
| Intelligent Cloud | 137,791 (106,265) | 56,972 (44,589) | 41.3% (42.0%) | **+29.7%** |
| More Personal Computing | 54,052 (54,649) | 14,386 (14,166) | 26.6% | −1.1% |
| Total | 331,839 | 155,237 | 46.8% | +17.8% |

- **Cálculo.** El margen bruto de Intelligent Cloud bajó de 62.2% a **58.0%**: su costo de ingresos subió 44.1%. "Server products and cloud services" creció 31.5% (98,435 → 129,425). El 10-K no separa Azure.
- **Hecho.** Por geografía: Estados Unidos 170,794 (51.5%) y otros países 161,045 (48.5%). Nota al pie: "Includes billings to OEMs and certain multinational organizations...". El 10-K no desglosa China ni Taiwán.

### 2.6 FCF antes y después de principal, y calidad del CFO

| Cálculo sobre hechos (F1 R6, Nota 13) | FY2024 | FY2025 | FY2026 |
|---|---|---|---|
| CFO | 118,548 | 136,162 | 182,935 |
| Capex en efectivo | 44,477 | 64,551 | 115,948 |
| **FCF = CFO − capex** | **74,071** | **71,611** | **66,987** |
| Principal de arrendamientos financieros | 1,286 | 2,283 | 3,101 |
| **FCF después de principal** | **72,785** | **69,328** | **63,886** |
| FCF − SBC | 63,337 | 59,637 | 54,582 |
| Margen FCF / después de principal / − SBC | 30.2% / 29.7% / 25.8% | 25.4% / 24.6% / 21.2% | 20.2% / 19.3% / 16.4% |
| FCF / utilidad neta GAAP | 0.84 | **0.703** | **0.501** |
| FCF / utilidad neta sin OpenAI (F3) | — | **0.679** | **0.520** |

- **Hecho.** El interés de arrendamientos financieros (2,547) ya está **dentro** del CFO (flujo operativo, Nota 13). Restarlo otra vez cuenta dos veces el costo.
- **Hecho.** El estado de flujo no tiene renglón propio para el principal (3,101), y "Other, net" del financiamiento suma −2,839. **Inferencia:** el principal está dentro de "Other, net". En la base se separa, y el resto de "Other, net" queda en +262.
- **Regla del sistema (cálculo; conocimiento/03 §6.1, veto "FCF/UN < 0.7 dos años seguidos"):**
  - con la utilidad GAAP se cumple **un** año (FY2025 = 0.703, apenas arriba del umbral);
  - con la utilidad sin OpenAI se cumplen **dos** años (0.679 y 0.520).
  - En fase 0 esto solo se registra: no hay decisión.
- **Hecho (CFO).**
  - Los impuestos diferidos **suman +14,189** al CFO de FY2026 y restaron −7,056 en FY2025: un giro de 21.2 mil millones.
  - Las ganancias no monetarias de inversiones y derivados restan −11,047.
  - El impuesto corriente bajó de 28,851 a 17,761 (hecho XBRL). Los impuestos pagados fueron 21,188.
  - **Cálculo:** el CFO sin impuestos diferidos crece 17.8% (143,218 → 168,746), contra 34.4% reportado.
  - **Pendiente:** la causa del gasto diferido. La nota de impuestos leída no nombra ninguna ley.
- **Hecho (Nota 1):**
  - "the current portion of other receivables related to activities to facilitate the purchase of server components was $27.8 billion and $8.2 billion";
  - "restricted investments pursuant to a supplier agreement were $11.3 billion": 3.8 en inversiones de corto plazo y 7.5 en inversiones de largo plazo.
  - "Other, net" de inversión fue **−19,861** (+2,317 en FY2025).
- **Inferencia (por verificar en el MD&A):** la salida de 19.9 mil millones en "Other, net" de inversión es de magnitud parecida al aumento de 19.6 mil millones en las cuentas por cobrar por componentes de servidores. Microsoft estaría **financiando su cadena de suministro de componentes**. Si fuera así, esa salida es inversión operativa ligada al capex, y el FCF "CFO − capex" la omite.

### 2.7 Deuda, impuestos y obligaciones de desempeño

- **Deuda (Nota 10, R73-R76; hecho).**
  - Valor nominal 46,136, en libros 40,294 (menos 1,081 de descuento, 11 de cobertura y 4,750 de prima por canje) y razonable 36.5 mil millones.
  - Vencimientos de principal: 9,250 (FY2027), 0, 2,001, 0 y 500; después, 34,385.
  - Intereses pagados: 1.5 mil millones. Sin emisiones desde FY2024.
  - El roll-forward de FY2026 cierra con los componentes de la nota: 43,151 − 3,000 + 143 = 40,294. Los 143 son −70 de variación en USD de las notas en euros + 74 de descuento + 25 de cobertura + 114 de prima. Prueba C06 OK.
- **Interés (inferencia; pendiente).** El gasto por intereses (3,051, Nota 3) es apenas mayor que el interés de arrendamientos financieros (2,547, Nota 13), aunque la deuda paga ~1.5 mil millones. O parte del interés se capitaliza en construcción, o el interés de arrendamientos se presenta en otro renglón. C10 muestra 7.3% sobre deuda sola y 3.1% sobre deuda + arrendamientos.
- **Impuestos (Nota 11, R21 y R84; hecho).**
  - Tasa efectiva de 19.4% (17.6% en FY2025): "primarily due to changes in the mix of our earnings and tax expenses between the U.S. and foreign countries".
  - NOPA del IRS (años 2004-2013, precios de transferencia): "additional tax payment of $28.9 billion plus penalties and interest". Siguen en auditoría los años 2014-2017.
- **Obligaciones de desempeño pendientes (R88; hecho XBRL).** 684 mil millones, de los que ~30% se reconoce en 12 meses. Son 2.1 veces los ingresos de FY2026 (cálculo).

## 3. Base histórica y doble comprobación

La base cubre **FY2024, FY2025 y FY2026** (3 ejercicios, 2 reconciliaciones completas). Cada campo tiene su fuente en `fuentes_campos`, y el detalle de los "otros" está en `memo`.

| Hecho (F1/F2) | FY2024 | FY2025 | FY2026 |
|---|---|---|---|
| Ingresos | 245,122 | 281,724 | 331,839 |
| Utilidad bruta | 171,008 | 193,893 | 225,465 |
| Utilidad operativa | 109,433 | 128,528 | 155,237 |
| Otros ingresos (gastos), neto: interés ganado − interés pagado + otros | 3,157 − 2,935 − 1,868 | 2,647 − 2,385 − 5,163 | 3,301 − 3,051 + 10,447 |
| UAI / impuestos / utilidad neta | 107,787 / 19,651 / 88,136 | 123,627 / 21,795 / 101,832 | 165,934 / 32,185 / 133,749 |
| Caja + inversiones CP | 18,315 + 57,228 | 30,242 + 64,323 | 20,935 + 55,908 |
| Cuentas por cobrar / PPE neto | 56,924 / 135,591 | 69,905 / 204,966 | 80,876 / 313,076 |
| Activo total | 512,163 | 619,003 | 758,376 |
| Deuda / arrendamiento financiero | 51,630 / 27,145 | 43,151 / 46,172 | 40,294 / 66,594 |
| Pasivo total / capital | 243,686 / 268,477 | 275,524 / 343,479 | 315,989 / 442,387 |
| D&A y otros / SBC | 20,958 / 10,734 | 29,433 / 11,974 | 38,534 / 12,405 |
| CFO / CFI / CFF / tipo de cambio | 118,548 / −96,970 / −37,757 / −210 | 136,162 / −72,599 / −51,699 / 63 | 182,935 / −139,500 / −52,546 / −196 |
| Dividendos pagados / recompras | 21,771 / 17,254 | 24,082 / 18,420 | 26,445 / 22,271 |

**Doble comprobación.** Hay dos lecturas del mismo filing:
- **Primera:** los visores R, tecleados a `base.json`.
- **Segunda:** los hechos XBRL no dimensionales de companyfacts. El extracto está congelado en `datos/` con su SHA-256.

`modelo.py` las compara campo por campo con una tolerancia de 0.5 millones:

| Resultado | Registros |
|---|---|
| OK (diferencia 0) | **167** |
| Diferencia explicada | 2: dividendos declarados de FY2025 y FY2026 (24,677 y 27,034 en el estado de variaciones contra 24,676 y 27,035 en la Nota 15; redondeo del emisor) |
| FALLA | **0** |
| Sin contraparte XBRL | 1 (dividendos declarados FY2024) |

- Tampoco tienen contraparte en XBRL no dimensional: "D&A y otros", las ganancias del flujo, las adquisiciones y ventas de inversiones, la deuda de 90 días o menos y el reparto circulante/largo plazo del arrendamiento financiero. Esas cifras se prueban por identidad: C01-C04, C07 y C15 cierran al millón.
- **Límite:** las dos lecturas vienen del mismo XBRL del emisor. Detectan errores de transcripción, no errores del emisor.

## 4. Reconciliación del histórico (C13)

El motor corre con los drivers implícitos de cada año desde el balance reportado del año anterior. **Reproduce las 20 líneas comparadas de FY2025 y FY2026 con diferencia 0.0** (tolerancias de 2.8 y 3.3). Lo que un modelo simple de drivers no explica aparece como partida conciliatoria **nombrada**. Materiales de FY2026 (> 2% de los ingresos) y su lectura:

| Partida (FY2026) | Monto | Lectura con las notas |
|---|---|---|
| otros_ingresos (incluye ingreso financiero) | 13,748 | Hecho: 10,697 de otros ingresos netos + 3,051 de intereses que el motor separa. Incluye +6.5 mil millones de OpenAI |
| otros_inversion | −23,552 | Hecho: adquisiciones −1,743, compras −58,351, vencimientos 34,605, ventas 21,798, "Other, net" −19,861 |
| nuevos arrendamientos financieros (implícito) | 23,523 | Contra 24,608 de derecho de uso financiero obtenido (hecho). La diferencia de −1,085 (modificaciones, bajas o FX) no se revela |
| no monetario en inversiones_cp | −8,415 | Mecánica del motor: carga los flujos de inversión contra otros activos LP. Es reclasificación, no pérdida |
| no monetario en otros_activos_circulantes | 22,871 | Hecho: el saldo sube 22.9 mil millones y el flujo solo registra −2,627. Incluye +19.6 mil millones de cuentas por cobrar por componentes de servidores (§2.6) |
| no monetario en otros_activos_lp | −8,868 | Contrapartida de la reclasificación anterior |
| no monetario en ppe_neto | 7,173 | +19.8 mil millones de PPE por pagar y +4.7 de amortización de intangibles; ~17 mil millones sin explicar (§2.2) |
| no monetario en otros_pasivos_lp | 7,392 | Mecánica: el motor manda los "otros operativos" a otros pasivos LP. Incluye la contrapartida del impuesto diferido |

FY2025 tiene 5 partidas materiales del mismo tipo (tabla completa en el Anexo A). **Inferencia:** las partidas son grandes porque FY2026 combina tres cosas que un modelo de drivers no captura: financiamiento de proveedores, compras de PPE por pagar y ganancias no operativas. No indican error contable.

## 5. Escenarios de mecanismo FY2027E-FY2031E (supuestos)

La política de capital es **idéntica** en los tres escenarios para aislar el mecanismo operativo:
- dividendos de 29,700 / 32,700 / 36,000 / 39,600 / 43,500 (+10% anual sobre los 27,035 declarados en FY2026);
- recompras de 22,000 al año y emisión de acciones de 2,000;
- amortización de deuda según los vencimientos de la Nota 10: 9,250 / 0 / 2,001 / 0 / 500;
- amortización de intangibles según la Nota 9: 3,097 / 2,141 / 1,944 / 1,477 / 1,128;
- caja mínima de 20,000 (≈ caja de FY2026);
- tasas: 3.6% sobre la deuda (1.5 mil millones pagados / 41.7 promedio), 4.5% sobre arrendamientos (tasa promedio de la Nota 13) y 3.85% sobre la caja (3,301 / 85,704 promedio);
- `dias_proveedores` = (54 días de costo de ventas + PPE por pagar como % del capex) / costo de ventas × 365. La proporción es 23% del capex en FY2026 y 15% en tensión.

| Supuesto (FY2027E → FY2031E) | Tensión | Intermedio | Eficiencia | FY2026 (hecho) |
|---|---|---|---|---|
| Crecimiento de ingresos | 12% → 5% | 15% → 9% | 17% → 13% | 17.8% |
| Margen bruto | 66% → 60% | 67% → 65% | 68% | 67.9% |
| Margen operativo | 44% → 36% | 46% → 43% | 47% → 48% | 46.8% |
| D&A / ingresos | 14% → 20% | 13% → 15% | 12% → 13% | 11.6% |
| Capex / ingresos | 38% → 28% | 33% → 23% | 30% → 19% | 34.9% |
| SBC / ingresos | 4.0% | 3.7% | 3.5% | 3.7% |
| Tasa de impuestos | 21% | 19% | 18% | 19.4% |
| Días de cuentas por cobrar | 95 | 89 | 85 | 89.0 |
| Días de proveedores | 115 → 92 | 138 → 109 | 133 → 104 | 145.5 |
| Arrendamientos financieros nuevos al año | 50,000 | 35,000 | 25,000 | 23,523 (implícito) |
| Principal de arrendamientos | 4,100 → 14,000 | 4,100 → 10,500 | 4,100 → 8,000 | 3,101 |

Ancla de los supuestos:
- El principal de FY2027 (~4,100) es una inferencia: 7,121 de pagos de FY2027 menos ~3.0 mil millones de interés (4.5% × 66,594).
- Los nuevos arrendamientos por año (25 a 50 mil millones) son **supuesto**. En 5 años suman entre 125 y 250 mil millones, contra los 329.1 mil millones no iniciados (nominales, FY2027-FY2033, parte operativos).

| Resultado (modelo) | Tensión | Intermedio | Eficiencia |
|---|---|---|---|
| Ingresos FY2031E (CAGR a 5 años) | 482,448 (7.8%) | 573,913 (11.6%) | 667,194 (15.0%) |
| FCF FY2027E / FY2031E | 33,856 / 106,056 | 71,243 / 167,547 | 85,297 / 240,341 |
| FCF acumulado a 5 años (después de arrendamientos) | 361,759 (316,659) | 596,190 (559,690) | 796,178 (766,078) |
| Dividendos + recompras acumulados | 291,500 | 291,500 | 291,500 |
| **Financiamiento requerido (revolvente)** | **28,259 (FY2027E) + 2,208 (FY2028E); máximo 30,467** | 0 | 0 |
| Deuda neta FY2031E (con arrendamientos) | 199,786 | −109,645 | −359,633 |

**Lectura (inferencia):**
- **Tensión.** Con capex alto, crecimiento que se desacelera y proveedores que acortan el plazo de las compras de PPE por pagar, el FCF de FY2027E (33.9 mil millones) no cubre dividendos, recompras y vencimientos (61 mil millones). Se abre un faltante explícito de 28 mil millones.
  - El motor mantiene constantes las inversiones de corto plazo (55,908, de las que 52,108 no están restringidas). En la práctica, ese faltante podría cubrirse vendiéndolas o recortando recompras.
  - El número mide **tensión de la política de capital**, no insolvencia.
  - La deuda neta de FY2031E sube sobre todo por los arrendamientos que comienzan: son no monetarios y llegan con activo.
- **Intermedio y eficiencia.** La caja se acumula (287 y 494 mil millones en FY2031E) porque la política de capital se fijó igual en los tres escenarios. Eso es un artefacto deliberado del diseño, no una predicción de la política del emisor.
- **Mecanismo central.** La diferencia de FCF acumulado entre tensión y eficiencia (434 mil millones) viene sobre todo de capex/ingresos y del margen operativo. La depreciación que "alcanza" al capex comprime la utilidad sin mover la caja del año. Es la brecha capex/D&A de conocimiento/25 §2.7.

## 6. Controles

**540 registros: OK 517, FALLA 0, INFO 19, NO_APLICA 4.** `modelo.py` sale con código 0.

| Estado | Qué es |
|---|---|
| NO_APLICA (4) | FY2024 es el primer ejercicio: sin balance de apertura cargado no aplican C05, C06, C10 ni C13 |
| INFO C05 (2) | El 10-K no da roll-forward del PPE. Otros implícitos: 34,257 (FY2025) y 30,696 (FY2026) |
| INFO C06 (3) | Deuda FY2025: diferencia no monetaria de 483. Los componentes de F2 (visor R72) explican 464 (euro +235, descuento +72, cobertura +45, prima +112); 19 quedan sin explicar (papel comercial). Arrendamientos: nuevos + otros implícitos 21,310 y 23,523, contra 20,511 y 24,608 de derecho de uso reportado |
| INFO C08-C12 (15) | En el histórico el driver sale del mismo dato: se informa el valor (DSO 89.0, DPO 145.5, tasa efectiva 19.4%, FCF 66,987 y 63,886) |

- C01-C04, C07, C14 y C15 son **pruebas reales** en el histórico: el estado de variaciones, el puente CFO y el puente no GAAP cierran al millón. C06 de la deuda de FY2026 también, con los componentes de la Nota 10.
- En la proyección los 16 tipos se recalculan desde los estados guardados. Tensión prueba C16 con revolvente activo.
- **Auditoría del propio control (cálculo):** `mi.verificar` sobre el `resultados.json` releído reproduce 540/0/19/4. Si se altera la caja de FY2026 en +10, aparecen 10 FALLA: C01, C02 y C13 en FY2026, C02 y C10 en 2027E de los tres escenarios, y C16 en 2027E de tensión. Los controles detectan una alteración.
- La sensibilidad geopolítica (§8) corre su propio modelo: 230 registros, 0 FALLA.

## 7. DCF inverso

Insumos (hecho con fecha, cálculo o supuesto):

| Insumo | Valor | Naturaleza |
|---|---|---|
| Precio | 497.93 USD (cierre del 24-sep-2026, F5) | Hecho |
| Acciones diluidas | 7,449.5 M = 7,425.5 en portada (23-jul-2026) + 24 incrementales por SBC (Nota 2) | Hecho + cálculo |
| Capitalización | 3,709,368 | Cálculo |
| Deuda neta | **33,845** = deuda 40,294 + arrendamientos financieros 66,594 − caja 20,935 − inversiones CP no restringidas 52,108 | Cálculo |
| Ingresos base | 331,839 (FY2026) | Hecho |
| Margen FCF (FCFF = CFO − capex) | 20.19% (FY2026), constante 10 años y en el terminal | Hecho + supuesto |
| r_f ajustada | 4.89% = 5.11% (DGS10, 23-sep) − 0.22% | Hecho + supuesto del sistema |
| ERP | 4.31% (contra r_f ajustada, sep-2026, F8) | Fuente secundaria |
| β | 1.25 desapalancada (software, F7) → **1.279** reapalancada con D/E de mercado de 2.89% y t = 21% | Hecho + cálculo |
| k_e / k_d | 10.40% / 5.61% antes de impuestos (5.11% + 0.50%, supuesto) | Cálculo |
| **WACC** | **10.23% → 10.2%**. Con la β de regresión de 0.98 (dossier) saldría ~9.0%, cerca del caso −1 pp | Cálculo |
| g terminal | 3.0% (< r_f) | Supuesto |

Criterios de la deuda neta:
- Los arrendamientos operativos quedan fuera porque su costo ya está en el CFO.
- Los financieros se tratan como deuda porque su principal no está en CFO − capex.
- Su interés (2,547) ya está en el CFO: eso sesga el resultado un poco hacia arriba del crecimiento requerido.

**Resultado base.**
- **Crecimiento implícito de ingresos: 21.53% anual durante 10 años.** Los ingresos de FY2036 serían 2.33 billones, 7.0 veces los actuales.
- El valor terminal pesa 68.1% (menos de 75%, sin alerta) y equivale a un múltiplo de 14.3 veces el FCF del año 10.
- No hay alertas de g > r_f.

Malla WACC × g terminal (margen 20.19%): crecimiento implícito (peso del terminal).

| WACC \ g | 2.5% | 3.0% | 3.5% |
|---|---|---|---|
| 9.2% | 19.80% (69%) | 19.03% (70%) | 18.18% (72%) |
| **10.2%** | 22.20% (67%) | **21.53% (68%)** | 20.81% (69%) |
| 11.2% | 24.45% (65%) | 23.86% (66%) | 23.22% (67%) |

Malla WACC × margen FCF (g = 3.0%):

| WACC \ margen | 16.45% (FY2026, CFO − capex − SBC) | 20.19% (FY2026, base) | 25.42% (FY2025) | 30.22% (FY2024) |
|---|---|---|---|---|
| 9.2% | 21.79% | 19.03% | 15.95% | 13.66% |
| **10.2%** | 24.37% | **21.53%** | 18.37% | 16.01% |
| 11.2% | 26.76% | 23.86% | 20.61% | 18.20% |

Variantes con WACC de 10.2%:
- **Dilución completa** (78 M de RSU no vestidas en lugar de 24): 21.63%.
- **Restando las inversiones de largo plazo no restringidas a valor en libros** (28,848): 21.42%. La participación en OpenAI a valor de mercado no está en el 10-K. Pendiente.

Contexto (cálculo sobre hechos):
- Crecimiento de ingresos: 15.7% (FY2024), 14.9% (FY2025) y 17.8% (FY2026). CAGR FY2024-FY2026: 16.4%. El dossier reporta 14.6% de CAGR a 5 años.
- CAGR a 5 años de los escenarios: 7.8%, 11.6% y 15.0%.

**Lectura (inferencia; no es recomendación):**
- Con un margen FCF constante en el nivel deprimido de FY2026, el precio exige crecer ~21.5% al año durante una década. Es más que cualquier año reciente.
- Si el margen vuelve al 30% de FY2024, el requisito baja a ~16%, cerca del crecimiento de FY2024-FY2026.
- La variable que más mueve la expectativa es el **margen FCF**, es decir, la intensidad de capex. Pesa más que el WACC: 100 pb de WACC mueven 2.3-2.5 pp; pasar de 20% a 30% de margen mueve ~5.5 pp.
- El DCF inverso usa margen constante y los escenarios lo suben con el tiempo, así que la comparación es direccional.
- Falta contrastar con **tasas base** de crecimiento a 10 años para empresas de más de 300 mil millones de ingresos (conocimiento/03 §2.7). No están en la base de conocimiento. Pendiente.

## 8. Sensibilidad geopolítica (mecanismo, sin probabilidad)

Cadena causal (conocimiento/25 §2.9): acontecimiento → exposición → efecto económico → línea → valuación.

- **Exposición (hecho).**
  - 48.5% de los ingresos viene de fuera de EUA, sin desglose de China (Nota 18).
  - Microsoft financia directamente componentes de servidores: 27.8 mil millones en cuentas por cobrar y 11.3 mil millones en inversiones restringidas por un contrato con un proveedor (Nota 1).
  - Tiene 34.6 mil millones de compromisos de construcción y 329.1 mil millones de arrendamientos por iniciar, sobre todo centros de datos (Notas 6 y 13).
- **Acontecimientos del radar (fuente secundaria, conocimiento/23 §4.5, sin verificar aquí):**
  - la regla del BIS del 13-ene-2026 sobre chips avanzados a China;
  - la prohibición china de exportar tierras raras, aplazada solo hasta el 10-ene-2027 (extensión del 24-sep-2026);
  - el escenario de bloqueo de Taiwán (tipo E).
  - **Inferencia:** la exposición de Microsoft es sobre todo de **oferta** (GPU, memoria, energía y permisos), más que de ventas a China.
- **Choque aplicado (supuesto)** al escenario intermedio durante FY2027E-FY2028E:
  - −4 pp de crecimiento por capacidad retrasada;
  - +4 pp de capex/ingresos por componentes más caros;
  - −1 pp de margen bruto y −1 pp de margen operativo.

| Resultado (modelo) | Intermedio | Con choque | Diferencia |
|---|---|---|---|
| Ingresos FY2031E | 573,913 | 534,342 | −39,571 (−6.9%) |
| Utilidad neta acumulada a 5 años | 851,751 | 784,522 | −67,229 |
| FCF acumulado a 5 años | 596,190 | 516,411 | **−79,778 (−13.4%)** |
| Financiamiento requerido | 0 | **8,658 (FY2027E)** | +8,658 |
| Deuda neta FY2031E | −109,645 | −29,866 | +79,778 |

Otras lecturas:
- **Por la tasa.** Un riesgo geopolítico que se cobre con +1 pp de WACC sube 2.3 pp el crecimiento implícito (de 21.53% a 23.86%, §7). No se debe subir la tasa **y** recortar los flujos por el mismo riesgo (conocimiento/03 §7, trampa 3).
- **Regulación y política (conocimiento/24; hecho F1).** La NOPA del IRS por 28.9 mil millones más penalidades e intereses es el riesgo de política pública fiscal cuantificado en el filing. No se modela: no hay resolución ni probabilidad.

## 9. Qué NO demuestra este trabajo

- Los controles prueban la **consistencia aritmética** de la transcripción y del motor. No prueban valor razonable, calidad de auditoría ni ausencia de fraude.
- La doble comprobación compara dos lecturas del **mismo** XBRL del emisor: no es verificación independiente de la economía.
- Los escenarios no son pronósticos y no tienen probabilidades. La política de capital fija es un recurso de diseño.
- El modelo no captura varias cosas:
  - los arrendamientos operativos (van en otros pasivos);
  - las compras y ventas de inversiones (las inversiones de corto plazo son constantes);
  - las adquisiciones;
  - el mark-to-market de OpenAI (otros ingresos = 0 en la proyección);
  - el calendario fiscal.
  - Además, su gasto por intereses (4.5% sobre arrendamientos) queda ~2 mil millones por encima del reportado en FY2026.
- El DCF inverso no dice si el precio es "alto" o "bajo". Dice qué crecimiento hace falta bajo supuestos declarados. No sustituye a los escenarios con probabilidad ni a las tasas base.
- La brecha del PPE (~17 mil millones), la naturaleza de "Other, net" de inversión (−19.9 mil millones) y la causa del impuesto diferido (+14.2 mil millones) quedan **sin explicar** con lo leído.

## 10. Pendientes

1. Descargar el htm completo del 10-K con un `SEC_USER_AGENT` con correo, que configure el dueño.
   - Verificar la página impresa de cada nota.
   - Leer el MD&A: definición de capex con arrendamientos financieros, "Other, net" de inversión, bajas de PPE e intereses capitalizados.
2. Leer la transcripción de la llamada del 29-jul-2026. La tanda 2 reporta, sin verificar aquí:
   - que la vida útil de centros de datos y edificios pasa de 15 a 25 años desde FY2027;
   - un cambio de clasificación de los arrendamientos futuros.
   Si se confirma, la D&A de los escenarios baja y el capex "del indicador" cambia: rehacer las series `da_ventas` y `capex_ventas`.
3. Composición de los 329.1 mil millones por iniciar: financiero u operativo, nominal o descontado, calendario por año.
4. Parte de OpenAI dentro de los 684 mil millones de obligaciones de desempeño. Valor de mercado de la participación de ~25%.
5. Tasas base de crecimiento de ingresos a 10 años por tamaño (Mauboussin, *Base Rate Book*) para contrastar el 16-24% implícito.
6. Roll-forwards de FY2024: componentes de la deuda al 30-jun-2023 (10-K FY2024) para cerrar C06, y los 19 sin explicar de FY2025 (papel comercial).
7. NOPA del IRS: estado del litigio y escenario de pago.
8. Actualizar precio, DGS10 y ERP en cada revisión: `base.json` → `mercado_y_dcf`.

## 11. Reproducción y huellas

```
python3 herramientas/huellas.py verificar empresas/MSFT/modelo/datos/SHA256SUMS.txt   # insumos congelados
python3 empresas/MSFT/modelo/modelo.py                                               # codigo 0 = todo OK
cd empresas/MSFT/modelo && sha256sum -c SHA256SUMS.txt                               # base, modelo, resultados
```

- `datos/SHA256SUMS.txt` (creado con `herramientas/huellas.py`) cubre:
  - el extracto XBRL (785 hechos, con el SHA-256 del companyfacts completo: f8aae296…6bb7246f);
  - la serie de Yahoo;
  - la serie DGS10;
  - el extracto de betas de Damodaran (con el SHA-256 del HTML completo).
- `SHA256SUMS.txt` cubre `base.json`, `modelo.py`, `resultados.json` y el manifiesto de `datos/`.
- `modelo.py` se niega a correr si las huellas de los insumos no coinciden.

## Anexo A. Salida del motor (`mi.resumen_markdown`, sin edición)

Motor herramientas/modelo_integrado.py v1.0 | Microsoft Corporation | USD millones

> FASE 0 (formacion). Escenarios con supuestos explicitos: no son pronosticos, guia del emisor ni consenso, y no constituyen recomendacion de compra o venta.

**Controles:** 540 registros, OK 517, FALLA 0, INFO 19, NO_APLICA 4. Todos OK: si.

| Id | Control | OK | FALLA | INFO | NO_APLICA |
|---|---|---|---|---|---|
| C01 | Balance: activo = pasivo + capital (y totales = suma de componentes) | 54 | 0 | 0 | 0 |
| C02 | Caja: inicial + CFO + CFI + CFF + efecto cambiario = final (y sumas de CFI y CFF) | 59 | 0 | 0 | 0 |
| C03 | Capital: inicial + utilidad + SBC - dividendos - recompras + emisiones + ORI + otros = final | 18 | 0 | 0 | 0 |
| C04 | Utilidades retenidas: inicial + utilidad - dividendos - recompras imputadas + otros = final | 18 | 0 | 0 | 0 |
| C05 | PPE: inicial + capex + nuevos arrendamientos - depreciacion + otros = final | 15 | 0 | 2 | 1 |
| C06 | Deuda: inicial + emisiones - amortizaciones (+ otros) = final (deuda, arrendamientos, revolvente) | 46 | 0 | 3 | 1 |
| C07 | Puente utilidad -> CFO: utilidad + D&A + SBC + capital de trabajo + otros = CFO | 36 | 0 | 0 | 0 |
| C08 | Cuentas por cobrar = dias_cxc x ingresos / 365 | 15 | 0 | 3 | 0 |
| C09 | Inventario y proveedores = dias x costo de ventas / 365 | 30 | 0 | 3 | 0 |
| C10 | Intereses = tasa x deuda promedio; ingreso financiero = tasa x caja promedio | 30 | 0 | 2 | 1 |
| C11 | Impuestos = tasa x utilidad antes de impuestos | 15 | 0 | 3 | 0 |
| C12 | FCF = CFO - capex; FCF despues de principal de arrendamientos financieros = FCF - principal | 30 | 0 | 3 | 0 |
| C13 | Reconciliacion del historico: el motor reproduce los estados cargados con drivers implicitos | 2 | 0 | 0 | 1 |
| C14 | Conciliacion GAAP vs ajustado: cifra GAAP + ajustes = cifra ajustada | 2 | 0 | 0 | 0 |
| C15 | Aritmetica del estado de resultados (ingresos, bruta, operativa, UAI, neta) | 87 | 0 | 0 | 0 |
| C16 | Caja minima y revolvente: caja >= minimo; financiamiento requerido explicito, sin plug | 60 | 0 | 0 | 0 |

**Reconciliacion FY2025** (calculo sobre hechos; max |dif| = 0.0000, tolerancia 2.8172)

| Partida conciliatoria | Monto | % ingresos | Origen | Material |
|---|---|---|---|---|
| otros_ingresos (UAI - UO + intereses; incluye ingreso financiero) | -2,516.0 | -0.9% | implicito |  |
| otros_operativos del CFO (incluye diferencia capital de trabajo balance vs flujo) | -132.0 | -0.0% | implicito |  |
| otros_inversion (CFI + capex) | -8,048.0 | -2.9% | implicito | ALERTA |
| otros_financiamiento (CFF - componentes) | -8.0 | -0.0% | implicito |  |
| efecto_cambiario | 63.0 | 0.0% | reportado |  |
| nuevos arrendamientos financieros (saldo final - inicial + principal) | 21,310.0 | 7.6% | implicito | ALERTA |
| movimiento no monetario / no explicado en inversiones_cp | 7,095.0 | 2.5% | residuo explicito | ALERTA |
| movimiento no monetario / no explicado en otros_activos_circulantes | -298.0 | -0.1% | residuo explicito |  |
| movimiento no monetario / no explicado en otros_activos_lp | -1,980.0 | -0.7% | residuo explicito |  |
| movimiento no monetario / no explicado en ppe_neto | 12,947.0 | 4.6% | residuo explicito | ALERTA |
| movimiento no monetario / no explicado en otros_pasivos_circulantes | 15,324.0 | 5.4% | residuo explicito | ALERTA |
| movimiento no monetario / no explicado en otros_pasivos_lp | 378.0 | 0.1% | residuo explicito |  |
| movimiento no monetario / no explicado en deuda | 483.0 | 0.2% | residuo explicito |  |
| capital: ORI + otros + diferencias devengado vs pagado (del estado de variaciones) | 1,642.0 | 0.6% | derivado de movimientos_capital |  |
| utilidades retenidas: movimientos distintos de utilidad, dividendos pagados y recompras | -595.0 | -0.2% | residuo explicito |  |

**Reconciliacion FY2026** (calculo sobre hechos; max |dif| = 0.0000, tolerancia 3.3184)

| Partida conciliatoria | Monto | % ingresos | Origen | Material |
|---|---|---|---|---|
| otros_ingresos (UAI - UO + intereses; incluye ingreso financiero) | 13,748.0 | 4.1% | implicito | ALERTA |
| otros_operativos del CFO (incluye diferencia capital de trabajo balance vs flujo) | -5,015.0 | -1.5% | implicito |  |
| otros_inversion (CFI + capex) | -23,552.0 | -7.1% | implicito | ALERTA |
| otros_financiamiento (CFF - componentes) | 262.0 | 0.1% | implicito |  |
| efecto_cambiario | -196.0 | -0.1% | reportado |  |
| nuevos arrendamientos financieros (saldo final - inicial + principal) | 23,523.0 | 7.1% | implicito | ALERTA |
| movimiento no monetario / no explicado en inversiones_cp | -8,415.0 | -2.5% | residuo explicito | ALERTA |
| movimiento no monetario / no explicado en otros_activos_circulantes | 22,871.0 | 6.9% | residuo explicito | ALERTA |
| movimiento no monetario / no explicado en otros_activos_lp | -8,868.0 | -2.7% | residuo explicito | ALERTA |
| movimiento no monetario / no explicado en ppe_neto | 7,173.0 | 2.2% | residuo explicito | ALERTA |
| movimiento no monetario / no explicado en otros_pasivos_circulantes | 5,569.0 | 1.7% | residuo explicito |  |
| movimiento no monetario / no explicado en otros_pasivos_lp | 7,392.0 | 2.2% | residuo explicito | ALERTA |
| movimiento no monetario / no explicado en deuda | 143.0 | 0.0% | residuo explicito |  |
| capital: ORI + otros + diferencias devengado vs pagado (del estado de variaciones) | -539.0 | -0.2% | derivado de movimientos_capital |  |
| utilidades retenidas: movimientos distintos de utilidad, dividendos pagados y recompras | -589.0 | -0.2% | residuo explicito |  |

**Escenario tension** (supuesto de escenario; no es pronostico): Intensidad de capital sostenida con desaceleracion: el capex de IA sigue alto, la depreciacion alcanza al capex y comprime el margen, crecen los arrendamientos financieros que inician y se deshacen parcialmente las compras de PPE por pagar

| Concepto | 2027E | 2028E | 2029E | 2030E | 2031E |
|---|---|---|---|---|---|
| Ingresos | 371,659.7 | 405,109.1 | 433,466.7 | 459,474.7 | 482,448.4 |
| Utilidad operativa | 163,530.3 | 166,094.7 | 169,052.0 | 170,005.6 | 173,681.4 |
| Utilidad neta | 126,912.3 | 127,033.2 | 127,980.4 | 127,729.6 | 130,003.9 |
| CFO | 175,086.3 | 202,831.5 | 218,192.7 | 227,549.3 | 241,141.4 |
| Capex | 141,230.7 | 145,839.3 | 143,044.0 | 137,842.4 | 135,085.6 |
| FCF | 33,855.7 | 56,992.2 | 75,148.7 | 89,706.9 | 106,055.8 |
| FCF despues de arrendamientos | 29,755.7 | 50,492.2 | 66,148.7 | 78,206.9 | 92,055.8 |
| Dividendos + recompras | 51,700.0 | 54,700.0 | 58,000.0 | 61,600.0 | 65,500.0 |
| Financiamiento requerido | 28,259.3 | 2,207.8 | 0.0 | 0.0 | 0.0 |
| Caja final | 20,000.0 | 20,000.0 | 20,000.0 | 20,000.0 | 44,343.3 |
| Revolvente | 28,259.3 | 30,467.1 | 22,319.4 | 3,712.5 | 0.0 |
| Deuda neta | 95,889.3 | 141,597.1 | 172,448.4 | 192,341.5 | 199,785.7 |
- 2027E: FINANCIAMIENTO REQUERIDO 28259.3 (revolvente) para mantener caja_minima 20000
- 2028E: FINANCIAMIENTO REQUERIDO 2207.76 (revolvente) para mantener caja_minima 20000

**Escenario intermedio** (supuesto de escenario; no es pronostico): Crecimiento que se modera, capex/ventas que baja gradualmente desde el maximo de FY2026 y margen operativo que cede poco por la mayor depreciacion

| Concepto | 2027E | 2028E | 2029E | 2030E | 2031E |
|---|---|---|---|---|---|
| Ingresos | 381,614.8 | 431,224.8 | 478,659.5 | 526,525.5 | 573,912.7 |
| Utilidad operativa | 175,542.8 | 194,051.2 | 210,610.2 | 229,038.6 | 246,782.5 |
| Utilidad neta | 140,683.2 | 155,386.9 | 169,198.1 | 185,203.2 | 201,279.4 |
| CFO | 197,175.4 | 222,816.2 | 249,795.7 | 275,025.1 | 299,546.8 |
| Capex | 125,932.9 | 129,367.4 | 129,238.1 | 131,631.4 | 131,999.9 |
| FCF | 71,242.5 | 93,448.8 | 120,557.7 | 143,393.8 | 167,546.8 |
| FCF despues de arrendamientos | 67,142.5 | 87,748.8 | 113,257.7 | 134,493.8 | 157,046.8 |
| Dividendos + recompras | 51,700.0 | 54,700.0 | 58,000.0 | 61,600.0 | 65,500.0 |
| Financiamiento requerido | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Caja final | 29,127.5 | 64,176.3 | 119,433.0 | 194,326.7 | 287,373.5 |
| Revolvente | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Deuda neta | 43,502.5 | 37,753.7 | 8,196.0 | -40,597.7 | -109,644.5 |

**Escenario eficiencia** (supuesto de escenario; no es pronostico): La capacidad instalada se monetiza: crecimiento alto sostenido, capex/ventas que se normaliza rapido y margen operativo estable o al alza

| Concepto | 2027E | 2028E | 2029E | 2030E | 2031E |
|---|---|---|---|---|---|
| Ingresos | 388,251.6 | 450,371.9 | 517,927.7 | 590,437.5 | 667,194.4 |
| Utilidad operativa | 182,478.3 | 211,674.8 | 246,015.6 | 283,410.0 | 320,253.3 |
| Utilidad neta | 148,513.4 | 173,111.8 | 202,971.6 | 236,512.9 | 270,808.1 |
| CFO | 201,772.0 | 233,343.6 | 276,006.3 | 321,402.8 | 367,107.6 |
| Capex | 116,475.5 | 117,096.7 | 119,123.4 | 123,991.9 | 126,766.9 |
| FCF | 85,296.5 | 116,246.9 | 156,882.9 | 197,411.0 | 240,340.7 |
| FCF despues de arrendamientos | 81,196.5 | 111,246.9 | 150,882.9 | 190,411.0 | 232,340.7 |
| Dividendos + recompras | 51,700.0 | 54,700.0 | 58,000.0 | 61,600.0 | 65,500.0 |
| Financiamiento requerido | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Caja final | 43,181.5 | 101,728.4 | 194,610.4 | 325,421.3 | 493,762.0 |
| Revolvente | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Deuda neta | 19,448.5 | -19,098.4 | -94,981.4 | -207,792.3 | -359,633.0 |
