# Módulo 28 — Energía, centros de datos y cómo se financian las megaempresas de IA (2026)

> Nivel: maestría aplicada (analista sectorial) · Actualizado: 2026-10-05 · Fase 0 (papel; **no recomienda inversiones reales**) · Grado de evidencia global: **B−**. Los datos primarios de gas, electricidad, balances y compromisos de las emisoras son **A** como dato. Las proyecciones de demanda eléctrica de centros de datos son **C** (rangos de 2x a 3x entre fuentes). Lo que se sabe de OpenAI y Anthropic viene de prensa y **no está auditado (D)**. La lección que más dinero ahorra: **el riesgo de esta cadena no está en los resultados del trimestre, sino en los compromisos fuera de balance** (arrendamientos que aún no empiezan, garantías, compras mínimas), que hoy suman más que el capex anual.

**Convenciones.** **Hecho** = dato con fecha y fuente [n]. **Inferencia** = razonamiento propio. **Recomendación** = regla operable para el sistema (nunca de compra). "(no verificado)" = cifra no confirmada contra la fuente primaria en esta sesión; "[solo secundaria]" = la fuente primaria no se pudo abrir y la cifra viene de prensa o de un resumen. "Cálculo propio" = datos de `herramientas/datos.py` (FRED, Yahoo chart v8) o `herramientas/edgar.py` (XBRL y texto de 10-K/10-Q de la SEC), descargados el 5-oct-2026. Cumplimiento (REGLAS-MOTOR §0): **solo información pública**; todo lo de OpenAI, Anthropic y SpaceX marcado como lo que es (prensa o presentación pública). Grados: A = dato primario o replicado; B = evidencia sólida pero con supuestos; C = proyección o inferencia con rango amplio; D = anecdótico, no auditado o sin muestra.

Capítulos relacionados (no se duplican): [16 macro y peso](16-macro-global-divisas-y-el-peso.md) · [21 industrias](21-industrias-y-ciclos-sectoriales-2026.md) (§4.2 memoria, §4.3 hyperscalers, §4.7 energía, §4.11 utilities, §4.13 industriales) · [23 geopolítica](23-geopolitica-y-riesgo-politico-global.md) · [24 política pública](24-politica-publica-regulacion-y-mercados.md) (OBBBA, aranceles, intermedias) · [25 pronóstico de resultados](25-pronostico-de-resultados-y-estados-financieros.md) · [26 radar](26-radar-de-oportunidades.md). Fichas internas: `empresas/NVDA`, `ORCL`, `GEV`, `CAT`, `SPCX`.

---

## 1. Objetivos de dominio

Quien se titula en este módulo debe poder:

1. Decir, con cifras de la EIA, dónde está el gas natural de EUA (precio, curva, inventarios, producción, GNL) y **qué descuenta** el precio y **qué lo rompería**.
2. Explicar por qué el gas pesa menos en el precio de la electricidad de un centro de datos que la capacidad, la transmisión y la distribución (§3.4).
3. Citar los rangos de demanda de centros de datos (LBNL, NERC, EIA, IEA) y por qué son tan anchos.
4. Nombrar los cuellos de botella (interconexión, turbinas, transformadores) y mapear quién captura el gasto, **marcando qué empresas ya están en `empresas/universo.csv` y cuáles no**.
5. Leer los compromisos de financiamiento de una megaempresa en su 10-K/10-Q: capex, deuda, arrendamientos que no han empezado, compras mínimas, garantías y concentración de clientes.
6. Distinguir lo auditado (10-Q) de lo no auditado (rondas privadas) y no mezclar ambos en una misma conclusión.
7. Derivar pronósticos binarios verificables y alertas pre-registrables sin recomendar compras.

---

## 2. Marco: la cadena causal

Capital (deuda, flujo propio, capital de socios) → capex y arrendamientos de centros de datos → megavatios que necesitan **interconexión** → equipos (turbinas, transformadores, interruptores) → energía (red, gas, nuclear, gas en sitio) → precio de la electricidad y de la capacidad → quién captura el margen (utilities, productores independientes, equipo eléctrico, gas).

**Inferencia (grado B):** el eslabón más escaso fija quién captura. Hoy la evidencia apunta a **equipo e interconexión** (GE Vernova con *book-to-bill* ≈ 2.2x [cap. 21 §4.13]; PJM sin cumplir su requisito de confiabilidad [12]) y no al gas como molécula (producción récord [5], inventarios sobre el promedio [2]). El gas es abundante; lo escaso es poder conectar y entregar.

---

## 3. Gas natural de EUA

### 3.1 Dónde está (hechos al 5-oct-2026)

| Variable | Dato | Fuente |
|---|---|---|
| Henry Hub spot (diario) | **US$3.18/MMBtu el 29-sep-2026**; 3.21 el 25-sep; 3.00 el 24-sep | FRED DHHNGSP (serie EIA) [8] |
| Henry Hub, promedios | 2025: 3.52 · 2026 acumulado (a 29-sep): **3.49** · 2026 sin ene-feb: **2.93** · jun-ago 2026: 2.94 (EIA: **2.93**, −6% vs 2025) · enero 2026: **7.72** | Cálculo propio sobre [8]; EIA [6] |
| Pico de 2026 | **US$30.72 el 23-ene-2026** (tormenta invernal); 25.01 el 26-ene | FRED [8] |
| Curva NYMEX (última cotización de Yahoo, 5-oct) | Nov-26 **3.08** · Dic-26 **3.37** · Ene-27 **3.74** · Feb-27 3.42 · Mar-27 2.71 · Abr-27 2.62 · Jul-27 3.04 · Oct-27 3.18 · Dic-27 4.06 · **Ene-28 4.47** · **Ene-29 4.75** | Yahoo chart v8 [9] (contratos lejanos con poco volumen; sin verificar contra CME) |
| Pronóstico EIA (STEO 9-sep) | Henry Hub **3.43 en 2026** y **3.28 en 2027** (2024: 2.19; 2025: 3.53) | EIA STEO [1] |
| Inventarios (semana al 25-sep) | **3,415 Bcf**: +64 en la semana, **−138 (−3.9%)** vs hace un año, **+79 (+2.4%)** vs promedio de 5 años (3,336). Región Sur Central −2.4% vs promedio; mina de sal −15.5% | EIA WNGSR (1-oct) [2] |
| Pronóstico de inventario | EIA: **3,969 Bcf el 31-oct-2026** (+5% vs promedio de 5 años) | EIA STEO [1] |
| Producción | Gas seco **107.64 (2025) → 111.70 (2026) → 115.90 Bcf/d (2027)**; retiros brutos récord de **137 Bcf/d en julio 2026**; Permian + Haynesville > 70% del crecimiento | EIA STEO [1]; EIA TIE 2-oct [5] |
| Consumo | 91.88 (2025) → 92.21 (2026) → 94.28 Bcf/d (2027) | EIA STEO [1] |
| Exportaciones de GNL | **17.4 Bcf/d en 1S26 (+23% a/a)**; STEO: 17.3 en 2S26 y 18.7 en 1S27; 15.1 (2025) → 17.4 (2026) → 18.6 (2027) | EIA TIE 1-sep [3]; STEO [1] |
| Capacidad nueva de GNL | Plaquemines exporta a plena capacidad; **Corpus Christi Etapa 3 completa (7 trenes, 28-ago-2026)**; ambos suman +4.0 Bcf/d nominales; **Golden Pass T1 exporta desde abr-2026** (+0.7 Bcf/d), T2 a fines de 2026; Corpus Christi Midscale (+0.4 Bcf/d) en 2028 | EIA TIE [3][4] |
| Contexto global | Cierre del estrecho de Ormuz en marzo: **20% del GNL mundial**; TTF 1S26 **US$14.74**, JKM **US$15.56** | EIA TIE [3] |
| Gas en la generación | EIA STEO: **42% (2024), 40% (2025), 40% (2026 y 2027)**. Cálculo propio sobre EPM tabla 1.1 (ene-jul 2026, escala de servicio público): gas **39.6%** (1,041 TWh, +1.8% a/a), carbón 14.8% (−10.2%), nuclear 17.5%; en **julio 2026** el gas fue 45.2% | EIA [1][7] |

**Hecho (STEO, [1]):** la generación con gas sube 2% en 2026 y 1% en 2027; el carbón cae 8% y 6%; la solar crece 21% y 18%. La capacidad solar pasa de 151 GW (2025) a 181 (2026) y 222 (2027): **+30 y +41 GW**; la eólica de 159 a 170 y 179 GW.

### 3.2 Qué descuenta el precio hoy (inferencia, grado B/C)

1. **Oferta abundante.** Producción récord y asociada al petróleo del Permian (la relación gas/petróleo subió 15% desde 2021 [1]) que no responde al precio del gas. Con el Brent EIA en US$74 en 2027, el petróleo asociado se frena, lo que sería alcista para el gas en 2027-28 (la curva ya lo insinúa: Ene-28 en 4.47 contra 3.28 del pronóstico EIA de 2027).
2. **Demanda de GNL "topada" por capacidad, no por precio.** Con TTF y JKM en US$14-16 contra Henry Hub en ~3.1-3.2, el diferencial (~US$11) ya paga cualquier terminal que exista; las exportaciones de EUA están cerca del máximo físico. **Inferencia:** una reapertura de Ormuz bajaría TTF/JKM pero movería poco a Henry Hub mientras los trenes sigan llenos; lo que mueve a HH es **capacidad nueva** (Golden Pass T2, Corpus Christi) y **clima**.
3. **Centros de datos como demanda marginal pequeña de gas.** El STEO sube el consumo total de gas solo +0.3 Bcf/d en 2026 y +2.1 en 2027 [1]; el crecimiento eléctrico lo cubre en buena parte la solar. La narrativa "los data centers disparan el gas" **no aparece en la cifra** de 2026 (grado B).
4. **Inventarios cómodos.** +2.4% sobre el promedio de 5 años.

**Verificación propia de la previsión de inventarios (inferencia, grado C, publicable como pronóstico en §7):** para llegar a 3,969 Bcf el 30-oct, el inventario debe crecer **+554 Bcf en cinco semanas** desde el 25-sep. Con datos semanales de la EIA, las acumulaciones equivalentes (del viernes más cercano al 25-sep al más cercano al 30-oct) fueron: 2016 363, 2017 309, 2018 342, 2019 412, 2020 163, 2021 441, **2022 524 (máximo)**, 2023 420, 2024 383, 2025 354 (cálculo propio sobre [2], serie histórica semanal). **554 supera todos los años desde 2016.** [Verificado 2026-10-05 con la serie semanal EIA: las diez cifras se reproducen exactamente. Matiz: la ventana semanal termina el viernes 30-oct y el STEO apunta al 31-oct; un día extra (~+5-10 Bcf) deja la necesidad en ~545, aún sobre 524. Cálculo propio sobre base estadística.] El promedio 2021-25 (~424) llevaría el inventario a ~3,840 Bcf. Las últimas seis semanas de 2026 fueron +15, +30, +40, +44, +53 y +64 Bcf (aceleración), pero las tres de septiembre sumaron solo +161, empatado con 2024 como el menor de 2021-26. **El STEO del 6-oct (próximo lanzamiento [1]) probablemente baje esa cifra.** Esto no es una predicción de precio: un inventario menor al previsto es alcista, pero el mercado ya cotiza 3.08 y no 4.

### 3.3 Qué rompería el precio (grado C)

| Dirección | Detonante | Qué ya sabemos |
|---|---|---|
| Alza | Invierno frío con inventarios medios | Precedente: spot de **30.72 el 23-ene-2026** y promedio de enero de 7.72 [8]. La curva ya paga la prima (Ene-27 3.74 vs Oct-27 3.18) |
| Alza | Capacidad de GNL que llegue antes (Golden Pass T2, CCL3 a plena carga) | +4.7 Bcf/d nominales entre Plaquemines, CCL3 y Golden Pass T1 [3] |
| Alza | Petróleo más bajo → menos gas asociado | EIA: Brent US$90 (2S26) → US$74 (2027) [1] |
| Alza | Eventos de red con picos de quema de gas (PJM 6.8 GW por debajo del requisito [12]) | Solo transmite en horas pico |
| Baja | Falla de terminales de GNL o huracán en la costa del Golfo (se pierden salidas, el gas se queda en EUA) | Sin dato propio |
| Baja | Producción que sorprende (Hugh Brinson, Permian) y clima templado | Hugh Brinson empezó flujos en junio, antes de lo esperado [1] |
| Baja | Retraso de centros de datos (pausa de Texas [13]) | Efecto pequeño sobre el gas (§3.2 punto 3) |

**Recomendación:** tratar el Henry Hub como **variable de estado** (se registra, no se opera). Gatillos en §7.2.

### 3.4 Cuánto pesa el gas en el precio de la electricidad para un centro de datos

**Hechos (EIA, julio 2026, [7]):** precio medio a clientes finales (cents/kWh, julio 2026 vs 2025): todos los sectores **14.99 vs 14.36 (+4.4%)**; comercial **14.53 vs 14.05 (+3.4%)**; industrial **9.77 vs 9.33 (+4.7%)**; residencial 18.31 vs 17.45 (+4.9%). Por estado, comercial: **Virginia 11.68 vs 10.21 (+14.4%)**, **Ohio 14.06 vs 11.50 (+22.3%)**, Texas **8.47 vs 8.85 (−4.3%)**; industrial Pensilvania 11.04 vs 9.87 (+11.9%). **Hecho [6]:** el Henry Hub de jun-ago fue 6% *más bajo* que en 2025.

**Cálculo propio (supuestos explícitos, grado C):**

| Componente | Cálculo | Resultado |
|---|---|---|
| Combustible por MWh de una central de ciclo combinado | Heat rate supuesto de ~7.0 MMBtu/MWh (no verificado contra la EIA) × HH US$3.2 | ≈ **US$22/MWh** |
| Contra el precio medio comercial (US$145/MWh) e industrial (US$98/MWh) | 22/145 y 22/98 | **15% y 23%** del precio final, como cota alta (el gas solo es marginal en parte de las horas) |
| Sensibilidad | +US$1/MMBtu | +US$7/MWh = **+4.8% (comercial) y +7.2% (industrial)** |
| Capacidad de PJM | US$325/MW-día × 365 / 8,760 h para una carga de factor 100% | ≈ **US$13.5/MWh** (~9% del precio comercial) |

**Inferencia (grado B):** las alzas fuertes de julio 2026 se concentran en estados de **PJM** (Virginia, Ohio, Pensilvania, Maryland) mientras el gas bajaba; la explicación consistente es **capacidad, transmisión y distribución**, no el combustible. Texas, con un mercado de solo energía y sin ese cargo, cayó. **Por tanto:** para un centro de datos en PJM, un movimiento de ±US$1 en el gas importa menos que el próximo remate de capacidad. Tercer remate consecutivo al tope: **US$325/MW-día** para 2028/2029, 138,318 MW comprados, **6,831 MW por debajo del requisito de confiabilidad**; sin tope habría sido US$554.72 [solo secundaria: OPIS/POWER; esa cifra **no** aparece en el comunicado de PJM [12], que sí confirma 325, 138,318 MW y 6,831 MW] [nota del verificador 2026-10-05].

**Gas y México (una línea, enlaza cap. 16):** las exportaciones por gasoducto de EUA a México promediaron 6.4 Bcf/d en 2024 y marcaron 7.5 en may-2025 (EIA, vía búsqueda; el artículo de 2026 no se abrió; **no verificado** para 2026) [32]. Un Henry Hub alto encarece el gas de CFE; el efecto en USD/MXN es de segundo orden (grado C) y no lo trato aquí.

---

## 4. Demanda eléctrica de los centros de datos y quién captura

### 4.1 Proyecciones y su incertidumbre

| Fuente | Cifra | Qué incluye / límite | Grado |
|---|---|---|---|
| **LBNL (diciembre de 2024), vía comunicado del DOE** [10] | Centros de datos: 58 TWh (2014) → **176 TWh (2023) = 4.4%** de la electricidad de EUA → **325-580 TWh en 2028 = 6.7-12%** | Proyección de EUA; rango 1.8x. El PDF de LBNL devolvió 403; cifras tomadas del comunicado oficial del DOE | B |
| **EIA STEO (9-sep-2026)** [1] | Ventas de electricidad **4,135 BkWh (2026) y 4,211 (2027)**; sector comercial +3.3% y +2.7%, **63% y 56%** del crecimiento; crecimiento total ≈ +2%/año | No aísla centros de datos; "impulsado por desarrollo de centros de datos y manufactura" | A (dato), C (atribución) |
| **EIA, Sur Central Oeste** [1] | Ventas 761 (2026) y **790 BkWh (2027) contra 829 previstas** (−4.7%) por la **pausa de Texas** | Recorte explícito al pronóstico por frenar conexiones | A |
| **NERC LTRA 2025 (enero de 2026)** [11] | Pico de verano a 10 años: **+224 GW (69% más que los +132 GW del año previo)**; pico de invierno **+245 GW**; "13 de 23 áreas" con problemas de suficiencia; **ERCOT** (no PJM): **45 GW de cargas grandes a 2030 (23 GW centros de datos)**; PJM: pico de verano **+56 GW hasta 210 GW en 2035** (invierno +62 GW), sin cifra de cargas grandes en GW en lo que revisé; MISO: 18 GW de centros de datos a 2035 [corregido por verificador 2026-10-05: el borrador atribuía a PJM los 45 GW/23 GW, que el PDF del LTRA asigna a ERCOT (sección ERCOT: "large loads totaling 45 GW by 2030, of which 23 GW are data centers"); PJM +56 GW/210 GW del mismo PDF] | Con datos de mediados de 2025. NERC avisa que ERCOT y PJM ya revisaron a la baja proyectos que "se retrasaron o no se materializaron" en el corto plazo, aunque suben las solicitudes para años posteriores | A (cita), C (proyección) |
| **ERCOT (cola de cargas grandes)** [13] | **474 GW (junio) → 498 GW en 688 solicitudes (29-jul)**, ~90% centros de datos, más de 5x el pico récord de la red | [solo secundaria] (despachos legales y prensa); casi toda la cola es especulativa | D |
| **IEA, *Energy and AI* (abr-2025)** [14] | Centros de datos del mundo **415 TWh en 2024 (1.5%)** → **945 TWh en 2030**; EUA = 45% del consumo de 2024 | [solo secundaria]: iea.org devolvió 403 | C |

**Cálculo propio (grado C):** el rango de LBNL implica un aumento de **+149 a +404 TWh** de 2023 a 2028 (30-81 TWh/año), mientras que el crecimiento de **todas** las ventas eléctricas de EUA que prevé la EIA es de ~76-80 TWh/año. **Inferencia:** el pronóstico de la EIA es compatible con la parte baja y media del rango de LBNL; el extremo alto exigiría que casi todo el crecimiento nacional fuera de centros de datos. Además, el 12% de LBNL se calculó sobre una demanda total de ~4,840 TWh en 2028, ~12% superior a la que implica el STEO; con la base de la EIA los porcentajes serían 7.6-13.5% (supuesto, no verificado).

**Por qué el rango es tan ancho:** (a) la cola de interconexión mezcla proyectos reales y especulativos (NERC [11], ERCOT [13]); (b) la eficiencia del cómputo cambia el MW por token; (c) el financiamiento condiciona el cronograma (§5); (d) las pausas regulatorias (Texas) mueven fechas. **Regla:** nunca usar una sola proyección; reportar siempre el rango y quién lo emitió.

### 4.2 Cuellos de botella

| Cuello | Hecho | Fuente | Grado |
|---|---|---|---|
| **Interconexión y suficiencia (PJM)** | Primeras subastas en la historia de PJM en que **toda la región** queda por debajo del requisito: −6.5 GW (2027/28) y **−6.83 GW (2028/29)**; PJM pedirá a la FERC un "procuramiento de respaldo" en septiembre; reserva 14.7% | PJM, 14-jul-2026 [12] | A |
| **Interconexión (Texas)** | Orden del gobernador del **3-ago-2026** para auditar cada centro de datos en la cola de ERCOT antes de avanzar; ERCOT pausó su revisión "Batch Zero"; sin fecha límite | [13] [solo secundaria]; EIA lo menciona en el STEO [1] | B |
| **Turbinas de gas** | GE Vernova: cartera + reservas de **116 GW** (2T26), pedidos US$24.2 mil M (+88%), backlog US$176 mil M [cap. 21 §4.13, comunicado de la SEC]; vende ya ranuras de **2031** [solo secundaria]; Siemens Energy 69 GW de backlog y plazos ≥3 años [solo secundaria] | GEV 8-K [30]; prensa [29] | A (GEV), C (resto) |
| **Transformadores** | Plazos de 24-30 meses antes del auge a 3-5 años para los grandes; promedio de EUA ~128 semanas | [solo secundaria] [29] | D |
| **Componentes y energía como riesgo declarado** | Microsoft: "proveedores limitados para ciertos componentes críticos... en escasez" y "asegurar recursos energéticos"; Nvidia: "tierra, energía y estructura es crucial" para el cliente | 10-K FY26 [15]; 10-Q [20] | A |

### 4.3 PPAs, nuclear y gas en sitio

- **Nuclear (hechos, [solo secundaria] ANS/prensa del 9-ene-2026 [28]):** Meta firmó con Vistra PPAs de 20 años por **2,176 MW** (Perry, Davis-Besse, Beaver Valley) más 433 MW de repotenciación; con TerraPower, 2 reactores Natrium (690 MW hacia 2032, con derechos hasta 2.1 GW más hacia 2035); con Oklo, 1.2 GW desde ~2030: **6.6 GW a 2035**. Antes: Constellation-Meta (jun-2025), **Talen-AWS 960 MW**, **Constellation-Microsoft 835 MW** (reinicio de Three Mile Island 1, préstamo del DOE de US$1 mil M en nov-2025). Grado B-: los contratos existen, pero **un PPA no es un MW nuevo en la red**: los reactores nuevos llegan en 2030+ y los existentes ya estaban en la red (efecto: precio, no oferta).
- **Gas en sitio (hecho primario, [21]):** SpaceX/xAI alimenta el centro de datos COLOSSUS II con turbinas móviles de gas; el **14-abr-2026** la NAACP presentó una demanda bajo la Clean Air Act por esas turbinas. **Inferencia:** el gas en sitio evita la cola de interconexión pero cambia el riesgo a permisos ambientales y litigio.
- **Contratos que "financian" la oferta:** Nvidia ofrece garantías de arrendamiento a sus clientes (§5.3); Meta entra en una empresa conjunta en Luisiana (§5.2). La energía y el financiamiento ya están entrelazados.

### 4.4 Mapa de quién captura (y quién ya está en el universo)

Columna "Universo" = presencia exacta del ticker en `empresas/universo.csv` (revisado el 5-oct-2026). Rendimientos de Yahoo chart v8 al 5-oct-2026 (última barra; cálculo propio, precio sin dividendos, moneda local) [27].

| Capa | Empresa (ticker) | Universo | Dato de contexto (primario salvo nota) |
|---|---|---|---|
| **Gasto (demanda)** | Microsoft (MSFT), Alphabet (GOOGL), Amazon (AMZN), Meta (META), Oracle (ORCL) | **Sí** | §5. YTD: MSFT +9.3%, GOOGL +10.9%, AMZN +8.9%, META +12.7%, **ORCL −26.2%** (−54.0% desde su máximo) |
| **Chips y red de IA** | Nvidia (NVDA), Broadcom (AVGO), AMD, Micron (MU), Dell (DELL), Arista (ANET), Cisco (CSCO), TSMC (TSM), Lam (LRCX), Applied (AMAT), Sandisk (SNDK) | **Sí** | NVDA +28.4% YTD, en su máximo de 52 sem. Ver cap. 21 §4.2 |
| **Cómputo y nubes privadas** | SpaceX/xAI (SPCX) | **Sí** (cap. USD 1.95 billones, ranking 7) | 10-Q del 2T26 [21] (§5.5) |
| **Turbinas y generación en sitio** | GE Vernova (GEV), Caterpillar (CAT) | **Sí** | GEV +51.8% YTD, CAT +49.0% |
| **Petroleras con gas** | ExxonMobil (XOM), Chevron (CVX) | **Sí** | XLE (ETF, **no** en universo) +44.7% YTD |
| **Equipo eléctrico y obra** | Eaton (ETN), Vertiv (VRT), Quanta (PWR), Bloom Energy (BE) | **No** | ETN +37.0%, VRT +56.7% (−32.6% vs máx.), PWR +62.1%, **BE +229.9%** |
| **Productores independientes (IPP)** | Vistra (VST), Constellation (CEG), NRG, Talen (TLN) | **No** | VST −9.8%, **CEG −23.9%**, **NRG −38.6%**, TLN −11.5% YTD |
| **Utilities reguladas** | NextEra (NEE), Southern (SO), Duke (DUK), AEP, ETF XLU | **No** (AEP, NEE, SO, DUK, D ausentes) | XLU −4.4% YTD, −14.5% vs máx.; AEP +6.2% |
| **Gas aguas arriba y GNL** | EQT, Cheniere (LNG), Kinder Morgan (KMI), Williams (WMB), Energy Transfer (ET) | **No** | LNG +42.4%, KMI +17.5%, WMB +20.4%, **EQT −3.8%** |
| **Nuclear y combustible** | Cameco (CCJ), Oklo (OKLO) | **No** | CCJ −4.4%, **OKLO −49.9%** YTD |
| **Fuera de EUA (no revisados)** | Siemens Energy, Schneider, ABB, Hitachi, Mitsubishi Heavy | No cotizan en el universo | No cotejados |

**Hecho:** en 2026 el **equipo y la obra** (GEV, ETN, PWR, VRT, BE) suben 37-230% y los **productores independientes y utilities** caen o quedan planos (CEG −24%, NRG −39%, XLU −4%), pese a que la demanda proyectada es la misma. **Inferencia (grado C, sin prueba):** el mercado paga la escasez de equipo y descuenta que el generador será el que cargue con **topes de precio** (PJM al cap), **presión política** por las facturas y **costos de interconexión**. Cap. 21 §4.11 llega a una lectura parecida para utilities ("bono proxy"). **No** se concluye que alguna esté barata o cara.

**Recomendación:** el universo hoy cubre **el gasto y los chips** (los que *pagan*) pero **no los generadores, las utilities, el gas ni el equipo eléctrico** (los que *cobran*). Si el trabajo continuo abre fichas nuevas (cap. 21 §6), el orden de cobertura propuesto, por poder explicativo del tema y no por atractivo, es: ETN/VRT/PWR (equipo), VST/CEG (IPP) y EQT/LNG (gas/GNL). Sin comprar nada; solo para observar.

---

## 5. Financiamiento de las megaempresas

### 5.1 Capex, flujo y guías

**Hecho (cálculo propio sobre XBRL y 10-Q/10-K de la SEC [15]-[20]; caja, no incluye arrendamientos financieros salvo nota):**

| Empresa | Capex de caja, ene-jun 2026 (US$ mil M) | vs ene-jun 2025 | Flujo operativo, ene-jun 2026 | Capex/FCO | Guía de capex 2026 |
|---|---|---|---|---|---|
| Microsoft (FY26 a jun) | **66.7** (2T cal. 35.8) | n.d. | 102.1 | 65% | Ver nota MSFT |
| Alphabet | **80.6** (2T: 44.9) | 39.6 (+103%) | 84.9 | **95%** | **US$195-205 mil M** [solo secundaria: MarketBeat/Nasdaq, antes 180-190] [22] |
| Amazon | **98.4** (2T: 54.2) | 57.2 (+72%) | 71.4 | **138%** | **~US$220 mil M** de caja [solo secundaria] [22] |
| Meta | **49.1** (incluye 2T con arrendamientos financieros: 31.08) | 29.5 (+67%) | 64.1 | 77% | **US$130-145 mil M** incl. arrendamientos financieros ([18], 10-Q) |
| **Total cuatro** | **294.8** | | **322.5** | **91%** | Alphabet + Amazon + Meta: **~US$545-570 mil M** (2 de 3 secundarias) |
| Oracle (1T FY27, a 31-ago) | **28.5** (vs 8.5) | +235% | 23.1 (incl. **11.4** de prepagos de clientes) | **123%** | "mayor que el FY26" ([19]) |
| Nvidia (1S FY27, a 26-jul) | 4.4 | n.d. | 74.4 | 6% | Capex propio mínimo; el dinero va a compromisos (§5.3) |

**Nota MSFT (discrepancia sin resolver, no verificado):** el 10-K confirma capex de caja FY26 de **US$115.9 mil M** y 4T de 35.8 [15]. Las fuentes secundarias de la llamada del 29-jul-2026 **no coinciden** sobre la guía: MarketBeat y la transcripción de Motley Fool citan "aproximadamente US$175 mil M" con un efecto de reclasificación de arrendamientos; otra fuente da **US$255-260 mil M** para el FY27. Coinciden en: capex con arrendamientos financieros del 4T FY26 de **US$41 mil M** y 1T FY27 **> US$50 mil M**, y en la ampliación de la vida útil de centros de datos de 15 a 25 años, que mueve arrendamientos de financieros a operativos (menos "capex" reportado, no menos gasto). **Recomendación:** no usar ninguna cifra de guía de Microsoft hasta leer la transcripción primaria.

**Hecho (cap. 21 §4.3, replicado):** el capex de 12 meses a jun-2026 de los cuatro fue US$510.7 mil M (77% del flujo operativo); los 2T26 crecieron +87% a/a.

**Inferencia (B):** el capex ya consume 91% del flujo operativo de los cuatro; el crecimiento que viene (guías al alza, "otro escalón en 2027" según la CFO de Alphabet [22, secundaria]) **no cabe en flujo propio sin deuda o capital externo**, y eso es lo que muestra el balance.

### 5.2 Deuda, arrendamientos y obligaciones fuera de balance

**Deuda de largo plazo (balance, US$ mil M; cálculo propio de 10-Q/10-K [15]-[20]):**

| Empresa | Dic-2025 (no corriente) | Jun-2026 (no corriente) | Cambio | Emisión reciente |
|---|---|---|---|---|
| Microsoft | 35.4 | 31.1 | −4.3 | Sin emisiones relevantes; **pasivo por arrendamientos financieros 66.6** (jun-25: 46.2) |
| Alphabet | 46.5 | **98.2** | **+51.7** | 2026: **US$20.0 mil M** en dólares (cupón 4.80%, 15 años) y **US$31.8 mil M** en divisas (£, CHF, €, C$, ¥) |
| Amazon | 65.6 | **128.9** | **+63.3** | US$67.0 mil M de ingresos por deuda en 1S26; **+US$25.0 mil M tras el 30-jun** (cupones 4.60-6.25%, vencen 2029-2066) |
| Meta | 58.7 | **83.7** | **+25.0** | **US$25.0 mil M** en mayo 2026 (seis series) |
| **Suma cuatro** | **206.4** | **341.8** | **+135.4 (+66%)** | [corregido por verificador 2026-10-05: antes 206.2 / 341.9 / +135.7, sumados con cifras ya redondeadas; XBRL exacto: 206.364 y 341.790] |
| Oracle (31-ago-26) | 129.5 (may-26) | **125.3** (7.6 corriente + 117.7) | −4.2 | **US$43.0 mil M** de notas en el FY26; **US$19.9 mil M** de capital vía programa ATM en el 1T FY27 |
| Nvidia (26-jul-26) | 8.5 (ene-26) | **33.4** (32.4 + 1.0) | **+24.9** | Primera emisión grande; también **US$39.0 mil M** de recompras en 1S FY27 |

**Compromisos que no están en el balance (hechos de las notas de los 10-Q/10-K, a la fecha indicada):**

| Empresa | Arrendamientos firmados que aún no empiezan | Otras obligaciones | Backlog / RPO |
|---|---|---|---|
| Microsoft (30-jun-26) | **US$329.1 mil M** (centros de datos; empiezan FY27-FY33; plazos 1-20 años) | **Obligaciones contractuales totales US$743.8 mil M**: arrendamientos con interés 443.5; compras mínimas **194.1**; construcción 34.6; deuda 46.1 + 25.6 de intereses | **US$684 mil M** (30% en 12 meses; **sin OpenAI, +25%** según la CFO [secundaria]) |
| Meta (30-jun-26) | **US$279.0 mil M**, más **~US$68 mil M** firmados en julio; terminan 2036 | Empresa conjunta de Luisiana: Meta 20%, ~US$27 mil M de desarrollo, arrendamientos de US$12.3 mil M desde 2029 y **garantía de valor residual de ~US$28 mil M** (sin pasivo registrado); **exposición máxima US$46.0 mil M**. Efectivo restringido de US$10.8 mil M en garantía de compras | — |
| Amazon (30-jun-26) | **US$137.2 mil M** | Compromisos totales **US$650.0 mil M**: deuda e intereses 220.3; arrendamientos operativos 116.4; **compras incondicionales 130.1**; obligaciones de financiamiento 11.1 | **US$496 mil M** de AWS, vida media restante 6.4 años |
| Alphabet (30-jun-26) | **US$85.2 mil M** (2026-2031; plazos hasta 26 años) | Arrendamientos con "VIE" de centros de datos tratados como financieros | **US$519.5 mil M** (513.9 de Cloud); algo más de 50% en 24 meses |
| Oracle (31-ago-26) | **US$288 mil M** (casi todo centros de datos; 15-19 años; empiezan 2T FY27-FY29) | — | **US$664 mil M**, solo **13% en 12 meses**; 37% de los meses 13-36 y 34% de los meses 37-60 |
| Nvidia (26-jul-26) | US$25 mil M propios + **US$20 mil M** de arrendamientos "para terceros" a reasignar | Suministro y capacidad **US$279 mil M** (el trimestre anterior: 119); acuerdos de nube 29; inversiones en capital 25 | RPO a más de un año solo US$3.2 mil M |

**Cálculo propio:** los arrendamientos aún no iniciados de Microsoft, Meta, Amazon, Alphabet y Oracle suman **~US$1.12 billones** (fechas distintas: 30-jun, y 31-ago para Oracle; Meta suma otros 68 mil M en julio). El backlog que los respalda (MSFT 684 + GOOGL 519.5 + AWS 496 + ORCL 664) suma **US$2.36 billones**. **Inferencia (B):** la mayoría de ese backlog está **a más de 12 meses** (Oracle 87%, Microsoft 70%, Alphabet algo menos de 50% a más de 24 meses), y los arrendamientos son por 15-30 años: **hay descalce de plazo** entre un cliente de IA que se compromete a 5-8 años y un arrendamiento de 20. Si el cliente final falla, el que lleva el riesgo es el hiperescalador, no el dueño del inmueble.

**Utilidad inflada por participaciones (hecho, ya en cap. 21 §4.3; cifras primarias de Amazon):** Amazon registró ajustes al alza de **US$50.5 mil M en el 2T26** (US$62.8 mil M en el semestre) sobre sus preferentes de Anthropic, con **US$15.9 mil M de gasto fiscal discreto**; el valor en libros de sus inversiones privadas pasó de **US$16.2 mil M (dic-25) a US$122.3 mil M (jun-26)**. **Regla:** en estas empresas el análisis usa utilidad operativa y flujo libre, no la UPA.

### 5.3 Acuerdos circulares proveedor-cliente (Nvidia, hechos del 10-Q del 2T FY27, [20])

| Canal | Cifra | Qué es |
|---|---|---|
| Inversión en clientes | **Inversiones de capital por US$99 mil M** y **compromisos de otros US$25 mil M** ("modelos de IA, financiadores de infraestructura y otras privadas"); valores no negociables US$51.2 mil M (ene-26: 22.3); acciones negociables US$42.8 mil M (12.9) | Nvidia financia a quienes le compran |
| Garantías de arrendamiento | **Hasta US$108.5 mil M** de exposición máxima: **US$105 mil M** firmados en agosto con SB Energy por ~**4.25 GW** de carga TI en Pike County, Ohio, para un afiliado de **OpenAI** (20 años; el sitio alojará exclusivamente cómputo de Nvidia; opción de otros ~3.8 GW); US$3.5 mil M para nubes de IA | Nvidia asume el riesgo de crédito del arrendamiento de su cliente. Las garantías terminan si OpenAI logra una calificación crediticia satisfactoria |
| Compra de capacidad a sus clientes | Acuerdos de nube **US$29 mil M** (propios) + **US$36 mil M** de "acuerdos de nubes de IA" (las nubes pueden dejar de proveer unilateralmente y vender a terceros) | Nvidia compromete gasto en las nubes que compran sus chips, con participación en ingresos si se cumplen criterios |
| Suministro | **US$279 mil M** (de 119 el trimestre anterior), sobre todo memoria | Compromisos a proveedores, parcialmente cancelables |
| Concentración | **Un cliente directo = 16% del ingreso del 2T**; en 1S: tres con 16%, 15% y 13%. **Cinco clientes directos = 70% de las cuentas por cobrar** (22%, 14%, 13%, 11%, 10%). "Una empresa de investigación y despliegue de IA aportó una cantidad significativa del ingreso al comprar nube a nuestros clientes" | Cuentas por cobrar US$63.1 mil M (ene-26: 38.5); inventario US$31.6 mil M (21.4) |
| Desempeño | Ingresos del 2T **US$96.2 mil M (+106%)**, margen bruto 75.0%, utilidad operativa US$63.7 mil M; 1S: ingresos US$177.8 mil M | [20] |

**Microsoft-OpenAI (hecho, 10-K FY26 [15]):** ingresos por acuerdos comerciales con OpenAI, incluida la participación en ingresos, **US$24.1 mil M en el FY26 (7.3% de los US$331.8 mil M)**; cuentas por cobrar de OpenAI **US$6.0 mil M**; participación de **~25%** (base convertida); compromisos de fondeo de **US$13.0 mil M**, **US$11.9 mil M ya aportados**; ganancia neta de **US$6.5 mil M** en el FY26 por la "dilución" de la recapitalización. **Amazon-OpenAI (10-Q [17]):** ampliación de **US$100 mil M a 8 años** sobre un compromiso previo de US$38 mil M; Amazon invirtió **US$15.0 mil M** en acciones Serie C y se comprometió a otros **US$35.0 mil M** (US$13.7 mil M en el 2T; los **US$21.3 mil M** restantes después del 30-jun). **Amazon-Anthropic:** compromiso de nube de **más de US$100 mil M a 10 años**; Amazon invirtió US$8.0 mil M en notas convertibles (2023-25), **US$5.0 mil M** en acciones preferentes sin voto "Serie G" en el 2T (el MD&A del mismo 10-Q dice **US$10.0 mil M** en el 2T: **no se conciló**), y abrió una línea de hasta **US$20 mil M** para Anthropic que vence 30 meses después de un evento de liquidez.

**Cálculo propio (inferencia, grado C):** los compromisos de OpenAI (38 + 100) y Anthropic (>100) con AWS suman **>US$238 mil M**, hasta ~48% del backlog de AWS de US$496 mil M **si todo estuviera incluido en él** (el 10-Q solo dice que los compromisos "incluyen" esas obligaciones; **no verificado** cuánto está en el RPO). Con la cifra de la CFO de Microsoft ("RPO +25% sin OpenAI") y el RPO de jun-2025 de US$375 mil M, el aumento atribuible a OpenAI sería de ~US$215 mil M (684 − 375×1.25), un orden de magnitud **muy aproximado**.

**Lectura (B):** el esquema es **circular y consistente con una cadena de pago de una sola raíz**: los laboratorios de IA (que pierden dinero o no han demostrado flujo, §5.4) firman compromisos de nube de cientos de miles de millones; los hiperescaladores reconocen ese backlog, se endeudan y arriendan; Nvidia vende los chips y avala los arrendamientos. Cada eslabón mide su riesgo contra el siguiente.

### 5.4 OpenAI y Anthropic (prensa; **no auditado (D)**; no hay 10-K ni 10-Q)

**Aviso de calidad:** la búsqueda devolvió agregadores y blogs (tech-insider, pinggy, Statesman, trendingtopics); **no** se obtuvo prensa de primer nivel (Bloomberg, FT, WSJ, Reuters) en esta sesión. Todas las cifras de esta sección son **[solo secundaria]** y deben leerse como "se reporta que".

| | OpenAI | Anthropic |
|---|---|---|
| Valuación y capital | Ronda de **US$122 mil M a US$852 mil M** post-dinero (cierre del 31-mar-2026); a fines de sep-2026 "en conversaciones" para **≥US$30 mil M a ~US$1.4 billones** (pre-IPO) | Serie G: **US$30 mil M a US$380 mil M** (feb-2026); Serie H: **US$65 mil M a ~US$965 mil M** (28-may-2026) |
| Ingresos | ~US$25 mil M anualizados (mar-2026); **>US$40 mil M** (ago-2026) | ~US$14 mil M (feb); ~US$30 mil M (abr); **~US$47 mil M** (fin de mayo); "esperado >US$50 mil M a fines de julio" (guía a inversionistas) |
| Compromisos de cómputo | ~**US$600 mil M** hasta 2030 (replanteados en feb-2026) | AWS **>US$100 mil M a 10 años** (10-Q de Amazon, **auditable**) |
| Deuda | Línea revolvente de ~US$4.7 mil M, sin disponer | n.d. |
| Salida a bolsa | Reportes de preparación de IPO | **S-1 confidencial presentado el 1-jun-2026** (prensa; un S-1 confidencial **no es público**: no se puede leer) |

**Hecho auditable que ancla estas cifras:** Microsoft reconoció US$24.1 mil M de ingresos de OpenAI en el FY26 [15]; Amazon marcó sus preferentes de Anthropic con un alza de US$62.8 mil M en el semestre [17] (consistente con la subida de valuación; **el 10-Q de Amazon llama "Serie G" a la ronda del 2T, mientras la prensa llama "Serie H" a la de mayo**: discrepancia de nomenclatura sin resolver). **Regla:** una valuación privada es una conversación, no un precio: se usa solo como contexto.

### 5.5 SpaceX (SPCX): **sí hay presentación pública**

SpaceX salió a bolsa en junio de 2026 (424B4 del 12-jun) y ya presenta 10-Q. **Hechos del 10-Q del 2T26 (30-jun-2026) [21]:**

| Dato | Cifra |
|---|---|
| Ingresos | 2T **US$7.81 mil M (+91.9%)**; semestre US$12.51 mil M (+53.7%) |
| Segmento IA (xAI + X) | 2T **US$2.56 mil M** (soluciones y **infraestructura de IA** US$2.19 mil M vs 0.31), con "nuevos contratos de infraestructura de IA" y arreglos de **nube con tarifas mensuales fijas** |
| Concentración | Cliente A **18.3%** del ingreso del 2T (los tres segmentos); **Cliente B 19.5%** (segmento IA); sin nombres en el 10-Q |
| Pérdida neta | 2T US$0.54 mil M; semestre **US$4.82 mil M** |
| Capex | **US$28.5 mil M en el semestre** (US$7.0 mil M en 1S25); "construcción de centros de datos" |
| Caja y deuda | Efectivo **US$93.5 mil M**; deuda **US$38.4 mil M** (notas de SpaceX por US$25.0 mil M que repagaron el préstamo puente de US$20 mil M de marzo; otros financiamientos 13.4) |
| Compromisos incondicionales | **US$27.96 mil M** (22.2 en 2027), sobre todo infraestructura de IA y capacidad de nube de terceros |
| Backlog | **US$47.5 mil M**, 56% en 12 meses |
| Litigio | Demanda de la NAACP (14-abr-2026) por turbinas de gas de COLOSSUS II |

**Inferencia (C):** SpaceX es la única de las tres "privadas" cuyo financiamiento se puede auditar, y muestra el mismo patrón: capex que sube 4x a/a, caja alta por la oferta pública y **un cliente de IA con casi una quinta parte del ingreso**.

### 5.6 Indicadores de estrés (a la fecha; el sistema los puede refrescar por API)

| Indicador | Valor | Referencia | Lectura (grado) |
|---|---|---|---|
| Spread de grado de inversión (ICE BofA, FRED BAMLC0A0CM) | **0.85 pp** (2-oct) | 12 meses: 0.73-0.94; hace un año 0.75 | Apretado (A) |
| BBB (BAMLC0A4CBBB) | 1.04 pp | 0.92-1.16 | Normal (A) |
| *High yield* (BAMLH0A0HYM2) | 3.10 pp | 2.60-3.46; hace un año 2.80 | Normal (A) |
| Treasury a 10 años (DGS10) | **5.28%** (2-oct) | máximo de 12 meses 5.29%; hace un año 4.13% | Es el costo de capital, no un spread (A) |
| VIX | 15.31 | 13.47-31.05 | Sin estrés de renta variable (A) |
| CDS a 5 años de Oracle | **203 pb** (record desde 2008; 144 pb a inicios de 2026) | FT/LSEG vía agregador, **28-jul-2026**, actualizado el 10-ago; **no es dato de hoy** [24] [solo secundaria] | Estrés específico de un emisor (C) |
| CDS de Nvidia / SpaceX | ~79 pb (récord) / spread a 30 años >200 pb | [24] [solo secundaria] | C |
| Nocional neto de CDS de tecnología | US$12.5 mil M (+500% desde 2T25); Oracle 6.5 | [24] [solo secundaria] | D |
| Notas de Oracle: valor razonable / principal | **US$105.7 mil M / US$125.0 mil M = 84.6%** (31-ago) | Mayo: 114.4 / 128.1 = 89.3% | Cotizan bajo la par; con el 10 años en 5.28% parte del descuento es **tasa**, no solo crédito (B) |
| Emisión de grado de inversión de tecnología en 2026 | "récord de US$182 mil M" | prensa [24] | D |
| FCF contra capex | **Cuatro: capex = 91% del flujo operativo**; Amazon 138%; Oracle FCF **−US$5.4 mil M** en un trimestre (**−US$16.8 mil M** sin los prepagos de clientes por 11.4 [11,363 M en el flujo operativo]: cálculo propio) [corregido por verificador 2026-10-05: antes −17.2; −5,396 − 11,363 = −16,759]; Amazon FCF de ene-jun **−US$27.0 mil M** (caja operativa − capex de caja) | 10-Q [17][19] | Estrés de flujo (A) |

**Lectura global (inferencia B):** el **crédito público no muestra estrés sistémico** (spreads en el rango de 12 meses), pero hay **estrés idiosincrático** en el eslabón más apalancado y concentrado (Oracle: capex 123% del flujo operativo, 87% del backlog a más de 12 meses, financiamiento con deuda y capital propio a la vez, **−54%** de su máximo). Los hiperescaladores con flujo grande (Microsoft, Alphabet, Meta) se financian con deuda "sin estrés"; Amazon y Oracle ya tienen FCF negativo. **Sin CDS en vivo no se puede decir si el mercado de crédito ya está cambiando.**

---

## 6. Elecciones intermedias de EUA (3-nov-2026): energía, aranceles y USD/MXN

Este apartado **no duplica** los caps. 16 (peso), 23 (probabilidades de Eurasia/Polymarket) ni 24 (OBBBA, IEEPA, 232/301/338): los enlaza y añade solo lo que afecta energía.

**Probabilidades de referencia (hecho, API de Polymarket, 5-oct-2026 [26]):** Cámara demócrata **92.5%** (volumen US$13.8 M); Senado demócrata **65.5%** (US$5.8 M). El cap. 23 midió 92.5% y 62.5% el 25-sep. **Cálculo propio (supuesto de independencia, que el mercado probablemente no hace):** ambas demócratas ~61%; Cámara D con Senado R ~32%; Cámara R con Senado D ~5%; ambas R ~3%. **Aviso:** un mercado de predicción es un precio de referencia, no un pronóstico calibrado (cap. 24 §Qué funciona).

**Qué se disputa en energía (hechos y marco):**
- **Facturas eléctricas como tema político.** Precio residencial de EUA **18.31 cents/kWh en julio 2026 (+4.9% a/a)**; STEO: 17.3 (2025) → 18.2 (2026) → 18.6 (2027) [1][7]. Capacidad de PJM al tope por tercera vez (US$325/MW-día) [12]. **Inferencia (C):** los centros de datos pasaron a ser un tema de **asignación de costos** (¿quién paga la red nueva?) en estados y comisiones, no solo de crecimiento. Texas ya actuó (SB 6 de junio de 2025 y la auditoría del 3-ago-2026 [11][13]).
- **Créditos fiscales y OBBBA.** Pierden los créditos 45Y/48E los proyectos eólicos y solares que inicien construcción desde el 4-jul-2026 (cap. 24 §4.3). Las elecciones **no** revierten una ley sin firma presidencial; el efecto es sobre el tono de supervisión y los estados.
- **Aranceles y equipo eléctrico.** El instrumento ya no es el IEEPA (anulado 6-3 el 20-feb-2026, cap. 24 §4.4) sino 232, 301 y 338. Un Congreso dividido **no** cambia esas facultades ejecutivas. **No se verificó** si hay arancel 232 específico a transformadores (no encontrado en esta sesión).
- **Permisos y gas.** Permisología para gasoductos y GNL (FERC, que devolvió 403) y la agenda de exportaciones: sin dato primario en esta sesión.

**Escenarios cualitativos para USD/MXN (grado D; no son pronósticos):** nivel de referencia **~18.06 (Yahoo, 5-oct)** y 18.19 (H.10 vía FRED, 2-oct). Enlace con FX-1 y los disparadores de REGLAS-MOTOR §7 (FIX < 17.10 / > 19.10 pendientes del comité del 9-oct).

| Escenario | Qué cambia | Efecto cualitativo sobre el peso |
|---|---|---|
| **Ambas cámaras demócratas** (el más probable, ya descontado) | Más supervisión; menor probabilidad de legislación nueva de aranceles o energía; los instrumentos 232/301/338 siguen en manos del Ejecutivo | Poca sorpresa de por sí; el riesgo es el **T-MEC y el Fed**, no el resultado (caps. 16, 24) |
| **Cámara D, Senado R** | Bloqueo en la Cámara, nombramientos y presupuesto (CR vence el 11-dic) en el Senado | Riesgo de *shutdown* en diciembre; sesgo hacia aversión al riesgo (inferencia) |
| **Cámara R** (cola de ~7.5%) | Continuidad de la política actual | **La mayor sorpresa para el mercado** (no está descontada); dirección incierta |

**Cálculo propio (grado D, n = 5):** en las intermedias de 2006, 2010, 2014, 2018 y 2022 (MXN=X de Yahoo, el último cierre antes del día de elección → +7 y +30 días calendario), el USD/MXN cambió entre **−1.1% y +1.7%** a 7 días y entre **−0.1% y +4.0%** a 30 días (2006: +0.4%/+0.8%; 2010: −0.3%/−0.1%; 2014: 0.0%/+4.0%; 2018: +1.7%/+2.5%; 2022: −1.1%/+0.5%). **Inferencia:** no hay efecto electoral estable con n = 5; la desviación a 30 días (~1.7%) es parecida a la de cualquier mes. **Recomendación:** no registrar pronósticos de FX basados en el resultado; usar FX-1 como está.

---

## 7. Puentes al sistema

### 7.1 Tres pronósticos binarios verificables (≤30 días), propuestos y **no registrados**

| # | Pregunta | Criterio de resolución y fuente | Base y prior propuesto | Fecha |
|---|---|---|---|---|
| **P1** | ¿El inventario de gas natural de EUA del informe semanal de la EIA del **29-oct-2026** (semana al 23-oct) será **≥ 3,800 Bcf**? | Cifra "Total" del WNGSR (EIA) [2]; sí = ≥3,800 | Desde 3,415 se necesitan **+385 Bcf en cuatro semanas**; en 2016-2025 solo **2022 (+417)** lo superó; 2019 y 2021 dieron +378. Prior **~15%** (base 1/10; el ritmo reciente +44, +53, +64 sube algo la probabilidad). Contraste con el STEO de 3,969 el 31-oct | 29-oct-2026 |
| **P2** | ¿El Henry Hub spot (FRED DHHNGSP) del **30-oct-2026** será **≥ US$3.00/MMBtu**? | Valor de FRED para esa fecha (o el último día hábil publicado) [8] | Spot 3.18 (29-sep); contrato noviembre en 3.08 (5-oct); prima del invierno 3.37-3.74 | 30-oct-2026 |
| **P3** | ¿**Meta** elevará **el piso o el techo** de su guía de capex 2026 (hoy **US$130-145 mil M**) en su comunicado del 3T? | Texto del comunicado de resultados en el 8-K de la SEC [18]; sí = piso >130 **o** techo >145 | Meta subió su guía de capex en el 1S26 (cap. 21 §4.3 la cita en 130-145; no se reconstruyó la serie de guías previas: no verificado); META +20% en el último mes. Reporte esperado el **28-oct** (fecha **no confirmada**; fecha de Alphabet 28-oct, Microsoft 27-oct y Amazon 29-oct también por confirmar). Prior **~60%**. Resuelve si el reporte sale ≤4-nov | ~28-oct-2026 |

**Notas:** P1 y P2 usan datos públicos de la EIA y se resuelven solos; P3 depende de una fecha corporativa pendiente de confirmar. Ninguna es una apuesta de precio de acciones. **Mañana, 6-oct,** sale el STEO de octubre: una cuarta pregunta (¿baja el pronóstico de inventarios del 31-oct de 3,969?) se resuelve en un día; no la propongo porque el aprendizaje de calibración es mínimo.

### 7.2 Alertas pre-registrables (gatillos de datos públicos; umbrales propuestos, sin calibrar)

| # | Gatillo | Fuente (frecuencia) | Umbral propuesto | Por qué importa |
|---|---|---|---|---|
| A1 | Henry Hub spot | FRED DHHNGSP (diaria) | > US$4.00 o < US$2.50 (cierre) | Fuera del rango que descuenta la curva (§3.2) |
| A2 | Inventario vs promedio de 5 años | EIA WNGSR (jueves) | Cambia de signo (de +2.4% a negativo) o supera ±8% | Señal de cambio de equilibrio antes del invierno |
| A3 | Spread de grado de inversión | FRED BAMLC0A0CM (diaria) | > 1.10 pp (el máximo de 12 meses es 0.94) | Estrés sistémico de crédito |
| A4 | Spread *high yield* | FRED BAMLH0A0HYM2 (diaria) | > 4.00 pp | Ídem |
| A5 | Treasury a 10 años | FRED DGS10 (diaria) | > 5.50% | Costo de capital del financiamiento de centros de datos |
| A6 | Guías de capex de hiperescaladores | 8-K/10-Q (trimestral) | Cualquier **recorte** de la guía de 2026-27 | Primer indicio de saturación de la demanda de IA |
| A7 | Backlog (RPO) | 10-Q (trimestral) | RPO de un hiperescalador cae q/q, o un cliente nombrado sale del backlog | La cadena depende del backlog |
| A8 | FCF/capex | Cálculo propio con XBRL (trimestral) | Capex/FCO de los cuatro > 100% | El capex ya no cabe en flujo propio |
| A9 | Compromisos de Nvidia | 10-Q (trimestral) | Garantías o inversiones nuevas > US$20 mil M, o cuentas por cobrar > 75% de un trimestre de ingresos | Circularidad creciente |
| A10 | Oracle: notas y CDS | 10-Q (trimestral); CDS **sin fuente gratuita** | Valor razonable/principal < 80%, o CDS > 250 pb (si hay fuente) | Estrés idiosincrático |
| A11 | PJM y ERCOT | Comunicados de PJM; PUCT/ERCOT (eventual) | **Procuramiento de respaldo** aprobado por la FERC; reanudación del "Batch Zero" de ERCOT; próxima subasta con precio < tope | Interconexión: el cuello de botella real |
| A12 | STEO | EIA (mensual; 6-oct) | Ventas eléctricas 2027 < 4,150 BkWh o inventario del 31-oct < 3,850 | Revisión de demanda y de gas |

**Recomendación:** registrar las alertas en `bitacora/alertas.md` solo cuando existan las piezas 1-3 del plan de cobertura (REGLAS-MOTOR §7). Cada alerta nueva debe llevar fecha de calibración y un umbral escrito **antes** de mirar el resultado.

### 7.3 Qué NO se puede concluir

1. **Que "hay una burbuja" o "no la hay".** El crédito público está tranquilo; los compromisos fuera de balance son enormes y concentrados. Ambas cosas son ciertas.
2. **Que una empresa del mapa esté barata o cara.** El módulo no valúa.
3. **Cifras de OpenAI y Anthropic como si fueran auditadas.** Son prensa de segunda línea (D).
4. **Que el gas suba por los centros de datos.** El STEO apenas sube el consumo de gas en 2026 (+0.3 Bcf/d); la solar y las exportaciones pesan más.
5. **Una proyección única de demanda.** El rango LBNL es 1.8x; el de NERC depende de proyectos que ya se retrasan.
6. **Que el resultado de las intermedias mueva al peso.** n = 5, sin patrón estable.
7. **Cuánto del backlog es de OpenAI/Anthropic.** El 10-Q de Amazon dice "incluye"; Microsoft solo da "+25% sin OpenAI". Falta una divulgación explícita.
8. **El valor presente de los arrendamientos aún no iniciados.** Las notas dan pagos sin descontar y con condiciones.
9. **Cualquier recomendación de compra o venta.** Fase 0.

---

## 8. Preguntas abiertas

1. ¿Cuánto del RPO de Microsoft, Oracle y AWS corresponde a OpenAI y Anthropic? (¿hay revelación explícita en el 10-K de Oracle del FY27?)
2. ¿Cuál es la guía correcta de capex de Microsoft (FY27): ~US$175 mil M, US$255-260 mil M o un rango con la reclasificación de arrendamientos? Falta la transcripción primaria.
3. ¿A cuánto cotiza hoy el CDS de Oracle, Nvidia y los hiperescaladores? No hay fuente gratuita verificable; el dato disponible es del 28-jul.
4. ¿Cuál fue el precio real de las notas de Oracle (rendimiento a vencimiento) en 2026? El 10-Q da solo el valor razonable agregado.
5. ¿Qué parte de los 45 GW (NERC/ERCOT a 2030) y los 498 GW (cola de ERCOT) [corregido por verificador 2026-10-05: antes "NERC/PJM"] es firme (con contrato de interconexión y garantía) y qué parte especulativa?
6. ¿La pausa de Texas y el "procuramiento de respaldo" de PJM llegan a retrasar el calendario del backlog? La EIA ya recortó la demanda de Sur Central Oeste 2027 un 4.7%.
7. ¿Cuántas de las pérdidas de generadores (CEG −24%, NRG −39%) reflejan topes de precio, política o rotación? No hay prueba.
8. ¿El ritmo de inyección de septiembre (+161 Bcf en tres semanas, tan bajo como en 2024) es un cambio de tendencia o clima? Falta el desglose de quema eléctrica semanal.
9. ¿Qué parte del precio de la electricidad de centros de datos es gas, capacidad y transmisión por región? Faltan tarifas por contrato (los PPA no son públicos).
10. ¿Cuánto del "capex" de Microsoft se saldrá del reporte al pasar arrendamientos a operativos (vida útil de 25 años)?
11. ¿Cómo se concilia la "Serie G" del 10-Q de Amazon con la "Serie H" de la prensa, y los US$5.0 mil M contra US$10.0 mil M del mismo documento?
12. ¿Hay un arancel 232 sobre transformadores o equipo eléctrico? No se encontró en esta sesión.
13. ¿Qué dice la FERC sobre la interconexión de cargas grandes? FERC devolvió 403; solo hay referencia secundaria.

---

## 9. Fuentes

Los números [n] de arriba remiten a esta tabla. "Acceso" indica qué se pudo abrir en esta sesión (5-oct-2026).

| # | Fuente | URL | Acceso / uso |
|---|---|---|---|
| 1 | EIA, Short-Term Energy Outlook, 9-sep-2026 (resumen, gas natural, electricidad; próximo 6-oct) | https://www.eia.gov/outlooks/steo/ · https://www.eia.gov/outlooks/steo/report/natgas.php · https://www.eia.gov/outlooks/steo/report/elec_coal_renew.php | Primaria, leída |
| 2 | EIA, Weekly Natural Gas Storage Report, semana al 25-sep (1-oct-2026) y serie semanal histórica | https://ir.eia.gov/ngs/ngs.html · https://www.eia.gov/dnav/ng/hist/nw2_epg0_swo_r48_bcfw.htm | Primaria, leída (la primera redirige con firma temporal) |
| 3 | EIA, Today in Energy, "U.S. LNG exports rose 23% in the first half of 2026" (1-sep-2026) | https://www.eia.gov/todayinenergy/detail.php?id=68064 | Primaria |
| 4 | EIA, Today in Energy, "Corpus Christi LNG expansion..." (15-sep-2026) | https://www.eia.gov/todayinenergy/detail.php?id=68144 | Primaria |
| 5 | EIA, Today in Energy, "U.S. natural gas production reached a record high in July 2026" (2-oct-2026) | https://www.eia.gov/todayinenergy/detail.php?id=68225 | Primaria |
| 6 | EIA, Today in Energy, "Henry Hub natural gas prices this summer were 6% lower..." (25-sep-2026) | https://www.eia.gov/todayinenergy/ | Primaria (solo el resumen de la portada) |
| 7 | EIA, Electric Power Monthly (datos de julio 2026, 24-sep-2026): tablas 1.1 y 5.6.A | https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_1_1 · https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a | Primaria |
| 8 | FRED, Henry Hub Natural Gas Spot Price (DHHNGSP) | https://fred.stlouisfed.org/series/DHHNGSP | Primaria vía `datos.py` |
| 9 | Yahoo Finance chart v8, contratos NYMEX NG (NGX26.NYM ... NGF29.NYM) | https://query1.finance.yahoo.com/v8/finance/chart/NGX26.NYM | Leída; contratos lejanos con poco volumen |
| 10 | DOE, comunicado del informe LBNL 2024 *United States Data Center Energy Usage Report* (20-dic-2024) | https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-centers | Primaria (comunicado). **PDF de LBNL: 403** (https://eta-publications.lbl.gov/sites/default/files/2024-12/lbnl-2024-united-states-data-center-energy-usage-report.pdf) |
| 11 | NERC, 2025 Long-Term Reliability Assessment (enero de 2026) | https://www.nerc.com/globalassets/our-work/assessments/nerc_ltra_2025.pdf | Primaria, leída |
| 12 | PJM, comunicado del remate de capacidad 2028/2029 (14-jul-2026) | https://www.pjm.com/-/media/DotCom/about-pjm/newsroom/2026-releases/20260714-pjm-capacity-auction-procures-138318-mw-of-generation-resources.pdf | Primaria, leída |
| 13 | Pausa de Texas a conexiones de centros de datos (3-ago-2026; cola de ERCOT) | https://www.troutman.com/insights/texas-hits-pause-on-data-center-grid-connections-amid-growing-oversight-push/ · https://www.akingump.com/en/insights/alerts/texas-pauses-data-center-interconnections-pending-statewide-audit · https://baxtel.com/news/texas-grid-audit-pauses-new-data-center-approvals-across-ercot | **Secundaria** (despachos legales, prensa); la EIA lo cita en [1] |
| 14 | IEA, *Energy and AI* (abr-2025) | https://www.iea.org/reports/energy-and-ai/executive-summary | **403**; cifras vía resúmenes de prensa (S&P, Scientific American) |
| 15 | Microsoft, 10-K del FY26 (a 30-jun-2026; presentado 29-jul-2026) | https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm | Primaria, leída |
| 16 | Alphabet, 10-Q del 2T26 (23-jul-2026) | https://www.sec.gov/Archives/edgar/data/1652044/000165204426000071/goog-20260630.htm | Primaria, leída |
| 17 | Amazon, 10-Q del 2T26 (31-jul-2026) | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm | Primaria, leída |
| 18 | Meta, 10-Q del 2T26 (30-jul-2026) | https://www.sec.gov/Archives/edgar/data/1326801/000162828026050705/meta-20260630.htm | Primaria, leída |
| 19 | Oracle, 10-Q del 1T FY27 (a 31-ago-2026; 11-sep-2026) | https://www.sec.gov/Archives/edgar/data/1341439/000119312526389274/orcl-20260831.htm | Primaria, leída |
| 20 | Nvidia, 10-Q del 2T FY27 (a 26-jul-2026; 26-ago-2026) | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm | Primaria, leída |
| 21 | SpaceX (SPCX), 10-Q del 2T26 (4-ago-2026); 424B4 del 12-jun-2026 | https://www.sec.gov/Archives/edgar/data/1181412/000162828026052535/spcx-20260630.htm | Primaria, leída |
| 22 | Guías de capex: Alphabet (llamada del 22-jul) · Amazon (30-jul) · Microsoft (29-jul) | https://www.marketbeat.com/instant-alerts/alphabet-q2-earnings-call-highlights-2026-07-22/ · https://dealroom.co/news/142839-amazon-tops-3t-market-cap-after-q2-beat-lifts-2026-capex-to-220b/ · https://www.fool.com/earnings/call-transcripts/2026/08/07/microsoft-msft-q4-2026-earnings-call-transcript/ | **Secundarias** (resúmenes de la llamada); ver nota MSFT |
| 23 | FRED: BAMLC0A0CM, BAMLC0A4CBBB, BAMLH0A0HYM2, DGS10, VIXCLS, DEXMXUS | https://fred.stlouisfed.org/ | Primaria vía `datos.py` |
| 24 | CDS de Oracle, Nvidia, Alphabet y SpaceX (FT/LSEG, vía agregador; 28-jul-2026) | https://aiweekly.co/alerts/oracle-nvidia-alphabet-spacex-cds-hit-records-on-ai-debt | **Secundaria**; no es dato de hoy |
| 25 | OpenAI y Anthropic (rondas, ingresos): agregadores de prensa | https://tech-insider.org/openai-122-billion-funding-round-852-billion-valuation-2026/ · https://tech-insider.org/anthropic-65-billion-series-h-965-billion-valuation-2026/ · https://pinggy.io/blog/openai_anthropic_funding_history/ | **Secundaria de baja calidad; no auditado (D)** |
| 26 | Polymarket, mercados de las intermedias 2026 (API Gamma, 5-oct-2026) | https://gamma-api.polymarket.com/events?slug=which-party-will-win-the-house-in-2026 · https://gamma-api.polymarket.com/events?slug=which-party-will-win-the-senate-in-2026 | Leída |
| 27 | Yahoo Finance chart v8 (precios y MXN=X; cálculo propio del 5-oct-2026 vía `herramientas/datos.py`) | https://query1.finance.yahoo.com/v8/finance/chart/ | Leída |
| 28 | Acuerdos nucleares de Meta (9-ene-2026) y de otros hiperescaladores | https://www.ans.org/news/article-7666/meta-strikes-deals-with-vistra-oklo-terrapower/ | **Secundaria** |
| 29 | Turbinas y transformadores (GE Vernova, Siemens Energy, plazos de entrega) | https://www.power-eng.com/gas/turbines/data-centers-drive-record-surge-in-ge-vernova-power-equipment-orders-as-turbine-slots-tighten-through-2030/ · https://thenextweb.com/news/us-power-companies-scramble-data-centre-equipment | **Secundaria** |
| 30 | GE Vernova, comunicado del 2T26 (22-jul-2026) | https://www.sec.gov/Archives/edgar/data/1996810/000199681026000147/gevpressrelease2q26.htm | Primaria (vía cap. 21 [36]; no re-leída en esta sesión) |
| 31 | `rutinas/REGLAS-MOTOR.md` §0 y §7 (plan de cobertura, 5-oct) | (interno) | Interno |
| 32 | EIA, exportaciones de gas natural a México | https://www.eia.gov/todayinenergy/detail.php?id=66404 | Solo el resumen de la búsqueda (2024-2025); **no verificado para 2026** |

**Huecos de acceso y no verificado (resumen):** FERC (403: sin dato primario de interconexión de cargas grandes); IEA (403) y PDF de LBNL (403): las cifras vienen de resúmenes y del comunicado del DOE; NERC LTRA sí se leyó; CME/CDS en vivo no accesibles; guías de capex de Alphabet, Amazon y Microsoft **solo por resúmenes de la llamada** (las notas del 10-Q sí confirman capex realizado); Yahoo devolvió cotizaciones de contratos lejanos con poco volumen; nomenclatura de rondas de Anthropic sin conciliar; ningún artículo de Bloomberg, FT, WSJ o Reuters pudo abrirse. Prensa de OpenAI y Anthropic: **no auditada**.

---

## 10. Registro de verificación (2026-10-05)

Cifras comprobadas **dos veces** (descarga de la fuente y recálculo o segunda ruta), todas con la fuente primaria abierta en esta sesión:

| Cifra | Primera lectura | Segunda comprobación |
|---|---|---|
| Henry Hub spot 3.18 (29-sep) y promedio jun-ago 2.93-2.94 | FRED DHHNGSP | EIA TIE 25-sep: "2.93, 6% menos" |
| Inventario 3,415 Bcf, +64, −138, +79 | WNGSR 1-oct | Serie histórica semanal EIA (3,351 → 3,415) |
| LNG 17.4 Bcf/d 1S26, +23% | TIE 1-sep | STEO (17.4 en 2026, 18.6 en 2027) |
| Gas 40% de la generación en 2026 | STEO | EPM 1.1: 39.6% ene-jul (cálculo propio) |
| Microsoft: 115.9 capex, 329.1 arrendamientos, 743.8 obligaciones, 24.1 OpenAI | XBRL (`edgar.py`) | Texto del 10-K |
| Alphabet: LP deuda 98.2, arrendamientos 85.2, RPO 519.5, capex 2T 44.9 | XBRL | Texto del 10-Q |
| Amazon: deuda 128.9 no corriente, 137.2 / 650.0 compromisos, RPO 496 | XBRL | Tabla del 10-Q |
| Meta: 130-145, 278.99 y +68, 46.03 de exposición | 10-Q | XBRL (deuda 83.7) |
| Oracle: 664 RPO (13%), 288 arrendamientos, 28.5 capex, FCF −5.4, ATM 19.9 | 10-Q | Tabla de FCF del 10-Q |
| Nvidia: 279, 99 + 25, 105 + 3.5, 16% | 10-Q | Tabla de compromisos y garantías |
| SpaceX: 7.81, 12.51, 28.5, 93.5, 38.4, 47.5 | 10-Q | Notas de deuda y de ingresos |
| NERC +224 GW / +245 GW; ERCOT 45 GW / 23 GW [corregido por verificador 2026-10-05: antes "PJM"] | PDF del LTRA | Releído íntegro por el verificador el 2026-10-05 (el "Resumen de NERC" no se usó) |
| PJM US$325, 138,318 MW, −6,831 MW | Comunicado de PJM | Prensa (APPA, OPIS) |
| Polymarket: 92.5% y 65.5% | API Gamma | Cap. 23 (92.5% / 62.5% el 25-sep) |

**Marcado como no verificado:** guías de capex de Alphabet, Amazon y Microsoft; todas las cifras de OpenAI y Anthropic; CDS de [24]; cola de ERCOT; plazos de turbinas y transformadores; acuerdos nucleares; IEA; el heat rate de ~7.0 MMBtu/MWh; la cifra de exportaciones a México de 2026.

**Efecto en el grado global:** B− (se mantiene el rango de los caps. 21 y 26). La parte de gas, electricidad, balances y compromisos es A como dato; la mitad que depende de proyecciones y de privadas baja la nota.
