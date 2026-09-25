# Módulo 21 — Industrias y ciclos sectoriales: cómo analizar cada negocio (2026)

> Nivel: maestría aplicada (analista sectorial) · Actualizado: 2026-09-25 · Grado de evidencia global: **B**. La economía de la industria (estructura, ciclo de capital, KPIs) es el mejor filtro contra errores caros (B; apoyo en Greenwood-Hanson y Cohen-Frazzini). Rotar sectores según la fase del ciclo económico: **D**. Los múltiplos de Damodaran describen (A como dato), no predicen. La lección que más dinero ahorra: **en los cíclicos, el P/U bajo aparece en el pico**. Micron cotiza a 8.7x su UPA anualizada con la guía, con margen bruto de 84.6%; en el FY2023 ese margen fue de −9.1%.

**Convenciones.** "Inferencia:" = interpretación propia. "(no verificado)" = cifra no confirmada en esta sesión. "Cálculo propio" = datos XBRL de la SEC vía `herramientas/edgar.py` o cierres ajustados de Yahoo vía `herramientas/datos.py`, descargados el 25-sep-2026. "Ficha interna" = dato de `empresas/<TICKER>/ficha.md`, que cita su fuente primaria. Los múltiplos de Damodaran son de **enero de 2026, empresas de EUA, en USD**. **Límite de la sesión:** se agotó la cuota de WebSearch (200/200). La verificación se hizo con ~50 consultas WebFetch a fuentes primarias (SEC, FDIC, EIA, Dallas Fed, WSTS, SIA, Damodaran, emisoras) y con cálculos propios. Por eso la literatura académica de 2023-2026 específica de industrias quedó sin cubrir (ver §4.0).

Capítulos relacionados: [03 valuación](03-maestria-valuacion-y-analisis-fundamental.md) (DCF, múltiplos, DCF inverso) · [06 anomalías](06-doctorado-asset-pricing-empirico-y-anomalias.md) (asset growth, momentum) · [07 riesgo](07-doctorado-riesgo-sizing-portafolio-backtesting.md) · cap. 11 México · cap. 13 estado del mercado · [16 macro y peso](16-macro-global-divisas-y-el-peso.md) (T-MEC, IED) · [17 crisis](17-crisis-burbujas-libro-de-patrones.md) (SaaSpocalypse) · [23 geopolítica](23-geopolitica-y-riesgo-politico-global.md) · [24 regulación](24-politica-publica-regulacion-y-mercados.md) (MFN, 232, OBBBA) · [25 pronóstico](25-pronostico-de-resultados-y-estados-financieros.md) (capex/D&A).

---

## 1. Objetivos de dominio

1. Clasificar cualquier empresa por su **motor de valor** (spread, commodity, capex cíclico, recurrente, inmobiliario, pipeline, minorista, regulado) y elegir el múltiplo y los KPIs correctos en 5 minutos.
2. Ubicar un sector en sus **cuatro relojes**: demanda, inventario, capital (oferta) y regulación. Distinguir un pico de márgenes de un cambio estructural.
3. Leer los KPIs de 14 sectores y saber qué número mueve el precio en cada uno.
4. Usar los múltiplos de Damodaran (ene-2026) como ancla y saber cuándo engañan.
5. Aplicar la paradoja del P/U en cíclicos: normalizar utilidades y evitar comprar el pico.
6. Auditar la economía del capex de IA: capex/ingresos, capex/flujo operativo, capex/D&A, FCF, concentración del RPO y financiamiento.
7. Analizar las emisoras mexicanas clave con sus KPIs y riesgos de 2026.
8. Correr el **checklist de 60 minutos** sobre cualquier empresa y terminar con un veredicto y un pronóstico registrable.
9. Separar qué evidencia sectorial sobrevive fuera de muestra (ciclo de capital, vínculos cliente-proveedor) de lo que es marketing (rotación por fase del ciclo).
10. Traducir todo a reglas coherentes con `config/parametros.json`.

---

## 2. Núcleo teórico / marco

### 2.1 La industria fija el techo del ROIC
El precio de una acción descuenta el ROIC futuro contra el WACC (cap. 03 §2.2). La estructura de la industria pone el techo: las cinco fuerzas de Porter (rivalidad, entrantes, sustitutos, poder de clientes y de proveedores) [52]. Dispersión actual (Damodaran, ene-2026, ROIC agregado de EUA) [3]: semiconductores 27.23%, software 29.32%, metales y minería 27.04% (en pico de precios), farmacéuticas 16.95%, telecom 12.04%, utilities 5.99%, REITs 3.20%, autos 2.25%; mercado total 8.96%. **Inferencia:** una empresa excelente en una industria de ROIC de 2-3% (autos) necesita una ventaja extraordinaria para crear valor. Una mediocre en software puede crearlo sin ella, hasta que el ciclo o un sustituto (IA agéntica) cambie la estructura.

### 2.2 Ocho motores de valor y su métrica correcta

| Motor | Sectores | Qué crea valor | Múltiplo correcto | Múltiplo que engaña |
|---|---|---|---|---|
| Spread apalancado | Bancos, aseguradoras de vida | (ROE − ke) sostenido | P/VL contra ROE; P/U | EV/EBITDA (la deuda es materia prima) |
| Suscripción + float | Aseguradoras de daños | Combined ratio < 100 + rendimiento del float | P/VL tangible, P/U normalizado | P/U en año sin catástrofes |
| Commodity (price-taker) | Petróleo, minería, acero, químicos | Posición en la curva de costos × precio de ciclo medio | EV/EBITDA y FCF a precio normalizado; P/NAV | P/U en precio pico |
| Capex cíclico | Semis, memoria, equipo, industriales, autos | Utilización y disciplina de oferta | EV/ventas y P/VL en ciclo medio; márgenes medios | P/U corriente |
| Recurrente | SaaS, telecom, bolsas, datos | Retención × margen incremental | EV/FCF menos SBC; EV/ingresos contra Rule of 40/X | P/U GAAP con SBC excluido |
| Inmobiliario | REITs, FIBRAs | NOI / valor (cap rate) contra costo de capital | P/AFFO, P/NAV, cap rate implícito | P/U (incluye revaluaciones) |
| Pipeline | Farma, biotech | Patentes × probabilidad de éxito | P/U (farma grande); rNPV y EV/ventas (biotech) | P/U con producto en LOE |
| Regulado | Utilities, aeropuertos, telecom preponderante | ROE permitido × base de activos | P/U contra crecimiento de la base; dividend yield contra bono | EV/EBITDA sin ver el régimen tarifario |

### 2.3 Los cuatro relojes del ciclo
1. **Demanda (ciclo económico).** PIB, empleo, crédito y tasas. Mueve el volumen. Es el reloj que todos miran y que el precio anticipa.
2. **Inventario (efecto látigo).** Cada eslabón amplifica los cambios de demanda del siguiente. En semis y químicos, una demanda final de −5% puede volverse −30% en pedidos al proveedor cuando el canal quema inventario. Señales: días de inventario (propios y del canal), book-to-bill, precios spot contra contrato.
3. **Capital (oferta).** Márgenes altos → capex → capacidad nueva con rezago de 1-5 años (fab, mina, barco, avión) → precios bajan → capex se corta → escasez. Es el reloj que más dinero da y el más ignorado. **Greenwood-Hanson (QJE 2015):** en fletes de granel seco, las ganancias altas elevan los precios de los barcos y la inversión, pero predicen **rendimientos futuros bajos**. La causa son dos errores: extrapolar choques temporales de demanda e ignorar la respuesta de inversión de los competidores [45]. Chancellor (*Capital Returns*, 2016) lo vuelve método: analizar la oferta, no la demanda [49].
4. **Regulación y política.** En 2026 domina en farma (MFN, 232), autos (T-MEC, 232, fin del crédito EV), utilities y semis (China) (caps. 23-24).

### 2.4 La paradoja del P/U en cíclicos
En un negocio de capex cíclico, la UPA de pico es un evento, no una tasa. Al pico el P/U se ve bajo y en el fondo alto (o negativo). **Regla de oro:** valuar con **margen de ciclo medio × ventas de tendencia**, no con la UPA corriente. Datos de Micron (XBRL de la SEC, cálculo propio) [9][11]:

| Año fiscal (ago) | Ingresos (US$ M) | Crec. | Margen bruto | Margen operativo |
|---|---|---|---|---|
| FY2018 | 30,391 | +49.5% | 58.9% | 49.3% |
| FY2019 | 23,406 | −23.0% | 45.7% | 31.5% |
| FY2023 | 15,540 | −49.5% | **−9.1%** | −37.0% |
| FY2025 | 37,378 | +48.9% | 39.8% | 26.1% |
| 3T FY26 (trim.) | 41,456 | +345.7% a/a | **84.6%** | 80.4% |

Hoy la acción está en US$1,080.53 (24-sep). La UPA GAAP de 12 meses es de US$44.18, así que el P/U es de 24.5x. Con la guía del 4T FY26 (UPA non-GAAP de US$31 ± 1, anualizada a 124), el P/U baja a **8.7x**. **Inferencia:** el mercado ya descuenta que el margen revierta. Un P/U de 8.7x sobre el margen más alto de la historia de la memoria no es "barato".

### 2.5 Tabla maestra: múltiplos, rentabilidad y costo de capital por industria (Damodaran, ene-2026, EUA, USD) [1][2][3][4][5]

| Industria | EV/EBITDA (EBITDA > 0) | P/U agregado (todas) | P/VL | ROE | Margen oper. antes de imp. | Costo de capital |
|---|---|---|---|---|---|---|
| Semiconductor | 34.75 | 77.42 | 13.31 | 31.36% | 35.33% | 10.55% |
| Semiconductor Equip | 24.74 | 35.88 | n.d. | n.d. | n.d. | n.d. |
| Software (System & App) | 24.48 | 49.13 | 9.14 | 29.62% | 32.98% | 9.34% |
| Bank (Money Center) | n.a. | 14.99 | 1.62 | 12.86% | n.a. | ke 7.34% |
| Banks (Regional) | n.a. | 14.99 | 1.14 | 9.75% | n.a. | n.d. |
| Insurance (Prop/Cas.) | 8.44 | 16.52 | 2.02 | 18.71% | 15.25% | 5.78% |
| Insurance (Life) | 12.52 | 10.17 | 1.43 | 12.87% | n.d. | n.d. |
| Oil/Gas (Integrated) | 8.16 | 15.70 | 1.71 | 9.96% | 11.25% | 5.07% |
| Oil/Gas (E&P) | 5.15 | 15.22 | n.d. | n.d. | n.d. | n.d. |
| Metals & Mining | 11.39 | 45.55 | 4.34 | 17.79% | 23.85% | 8.20% |
| Retail (General) | 17.38 | 43.04 | n.d. | n.d. | 6.80% | 7.27% |
| Retail (Grocery & Food) | 8.94 | 17.66 | 3.93 | 12.90% | 2.29% | 7.24% |
| R.E.I.T. | 19.87 | 56.11 | 1.99 | 5.04% | 24.64% | 5.32% |
| Utility (General) | 13.73 | 21.67 | 1.81 | 10.42% | 23.49% | 4.36% |
| Power | 12.38 | 23.13 | 2.28 | 12.40% | n.d. | 5.01% |
| Drugs (Pharmaceutical) | 15.25 | 58.92 | 6.64 | 24.04% | 29.54% | 7.85% |
| Drugs (Biotechnology) | 15.78 | NA | n.d. | n.d. | 8.97% | 8.49% |
| Machinery | 16.22 | 26.22 | n.d. | n.d. | 15.86% | 7.70% |
| Electrical Equipment | 24.59 | NA | n.d. | n.d. | n.d. | n.d. |
| Aerospace/Defense | 21.58 | 78.11 | n.d. | n.d. | 8.65% | 7.60% |
| Auto & Truck | 47.76 | 148.45 | 7.72 | 3.16% | 2.32% | 9.38% |
| Telecom. Services | 6.54 | 14.39 | 1.64 | 19.82% | 20.47% | 5.39% |
| Building Materials | 11.61 | 14.71 | 3.62 | 16.00% | 12.64% | 7.85% |
| **Mercado total (5,994)** | **19.73** | **34.22** | **4.61** | **17.21%** | **12.82%** | **6.96%** |

Cómo leerla: P/U agregado = capitalización total / utilidad neta total, con perdedoras incluidas (NA en biotech y equipo eléctrico). Autos está distorsionado por Tesla (47.8x con margen de 2.3%). El costo de capital de utilities (4.36%) sale de una beta de regresión de 0.24. **Inferencia:** para una utility, usar una beta bottom-up re-apalancada. Los bancos no tienen EV/EBITDA: la deuda es su insumo.

### 2.6 Fichas sectoriales: modelo, KPIs, drivers y múltiplo

**Semiconductores.** *Modelo:* fabless (NVIDIA, Broadcom), foundry (TSMC), IDM (Intel), memoria (Micron, SK hynix, Samsung: commodity con islas diferenciadas como HBM) y equipo (AMAT, Lam, KLA, ASML: venden al capex de los demás). Costo fijo altísimo y apalancamiento operativo extremo. *KPIs:* ingresos por mercado final (data center, PC, móvil, auto e industrial), margen bruto y su cambio, días de inventario propios y del canal, precios contrato DRAM/NAND t/t, bits enviados, utilización de fabs, book-to-bill del equipo y capex de la industria/ventas. *Drivers:* inventario (efecto látigo), capex del cliente final, nodos y generaciones de producto, controles de exportación. *Múltiplo:* EV/ventas y P/VL en ciclo medio; el P/U solo en fabless con ingresos recurrentes.

**Hyperscalers (economía del capex de IA).** *Modelo:* la publicidad y el software financian un capex que se convierte en ingresos de nube e IA. *KPIs:* crecimiento y margen de la nube (Azure, AWS, Google Cloud); RPO/backlog **y su concentración** (OpenAI, Anthropic); capex/ingresos; capex/flujo operativo; capex/D&A; vida útil de servidores y edificios; FCF después de arrendamientos financieros; ganancias por participaciones excluidas de la utilidad. *Drivers:* demanda de cómputo (entrenamiento contra inferencia), precio por token, oferta de GPU, memoria y energía, financiamiento de los laboratorios. *Múltiplo:* P/U y EV/FCF normalizado (capex de mantenimiento ≈ D&A), con el DCF inverso del cap. 03.

**Software/SaaS.** *Modelo:* suscripción recurrente, margen bruto de 70-90% y CAC pagado al frente. *KPIs:* ARR, **NRR** (retención neta; los mejores de la clase superan 120% y el umbral sano es de 110% o más, práctica de la industria, no verificado), GRR, cRPO, **Rule of 40** (crecimiento + margen FCF), **Rule of X** (crecimiento × 2-3 + margen FCF) [17], CAC payback y **SBC/ingresos**. *Drivers:* presupuestos de TI, cobro por asiento contra cobro por uso, sustitución por agentes de IA. *Múltiplo:* EV/ingresos NTM contra Rule of X; EV/(FCF − SBC).

**Bancos.** *Modelo:* ROE = ROA × apalancamiento; ROA = NIM − costo de riesgo − gastos + comisiones. *KPIs:* NIM y su sensibilidad a tasas, beta de depósitos y mezcla a la vista, crecimiento de cartera y depósitos, eficiencia, costo de riesgo, IMOR/NPL y **cobertura**, castigos netos, CET1/ICAP, LCR/NSFR, ROE contra ke. *Drivers:* curva de tasas, ciclo de crédito (la morosidad llega con rezago), regulación de capital. *Múltiplo:* **P/VL justificado = (ROE − g)/(ke − g)**.

**Aseguradoras.** *Modelo:* cobran la prima antes de pagar siniestros. El **float** invertido rinde, y si el **combined ratio** es menor a 100 el float cuesta menos que cero. *KPIs:* combined ratio reportado y **subyacente** (sin catástrofes ni desarrollo de reservas), desarrollo de reservas de años previos, cambio de tarifa en renovaciones contra tendencia de costo de siniestros, crecimiento de prima neta suscrita, rendimiento de la cartera y ROE. *Ciclo:* hard market (precios suben tras pérdidas) → capital nuevo → soft market. *Múltiplo:* P/VL tangible contra ROE normalizado.

**Energía (petróleo y gas).** *Modelo:* price-taker con activo que se agota; reinvertir es obligatorio. *KPIs:* producción por acción, reservas 1P y vida R/P, reemplazo de reservas, costo de hallazgo y desarrollo, **breakeven de pozo nuevo y de operación**, breakeven de FCF con dividendo, márgenes de refinación y deuda neta/EBITDA a precio medio. *Drivers:* OPEP+, inventarios, geopolítica, disciplina del shale. *Múltiplo:* EV/EBITDA y FCF yield **a precio de la curva de futuros y a precio de ciclo medio**, nunca a spot.

**Minería y materiales.** *Modelo:* price-taker; la posición en la **curva de costos** (cuartil) decide quién sobrevive al fondo. Práctica de la industria (grado C): el precio de largo plazo tiende al costo del productor marginal. *KPIs:* costo en efectivo **antes y después de créditos por subproductos**, AISC, ley del mineral, vida de la mina, capex de sostenimiento contra crecimiento, jurisdicción y regalías. Cemento: volumen × precio regional, energía por tonelada, utilización e importaciones. *Múltiplo:* EV/EBITDA a precio medio y P/NAV.

**Consumo.** *Modelo:* minorista (volumen × margen × rotación) o marca (poder de precio). *KPIs:* **mismas tiendas (SSS) = tráfico × ticket**, SSS real, aporte de aperturas, margen bruto, gastos/ventas, días de inventario, GMV y participación contra ANTAD. *Drivers:* ingreso real, empleo, remesas, crédito. *Múltiplo:* P/U y EV/EBITDA con arrendamientos (IFRS 16).

**REITs/FIBRAs.** *Modelo:* rentas con reparto obligatorio. *KPIs:* ocupación, **spread de renovación** (mark-to-market), NOI mismas propiedades, **FFO y AFFO por certificado** (el AFFO resta capex de mantenimiento, comisiones y mejoras), cap rate implícito (NOI/EV) contra cap rate de transacciones, NAV, LTV, costo y plazo de deuda, WALE, moneda de las rentas y retención. *Drivers:* tasas reales, oferta nueva, demanda (nearshoring, e-commerce). *Múltiplo:* P/AFFO, P/NAV y cap rate.

**Utilities.** *Modelo:* utilidad = ROE permitido × capital de la base tarifaria (rate base); crecer = invertir. *KPIs:* crecimiento de la base tarifaria, ROE permitido contra obtenido, rezago regulatorio, plan de capex, FFO/deuda, dilución por emisiones y demanda de carga (centros de datos). *Drivers:* tasas (bond proxy), regulador, demanda de IA. *Múltiplo:* P/U contra crecimiento de UPA y dividend yield contra bono.

**Farmacéuticas/biotech.** *Modelo:* I+D con riesgo binario y patentes que dan un monopolio temporal, seguido del precipicio (LOE). *KPIs:* ventas por producto y concentración, fecha de LOE de cada uno, pipeline por fase con probabilidad de éxito (rNPV), **precio neto contra volumen**, mezcla EUA contra resto, exposición a IRA/MFN. En biotech: caja y meses de runway, catalizadores binarios. *Múltiplo:* P/U (farma grande); rNPV y EV/ventas (biotech).

**Industriales.** *Modelo:* fabricación bajo pedido para el capex del cliente, con posventa de alto margen. *KPIs:* pedidos, backlog, **book-to-bill** (> 1 = crece), conversión del backlog, price-cost, margen incremental, servicios/ingresos, anticipos de clientes y mercado final. *Múltiplo:* EV/EBITDA y P/U en ciclo medio.

**Autos/EV.** *Modelo:* capital intensivo, bajo margen, financiera cautiva. *KPIs:* unidades, ASP, margen **sin créditos regulatorios**, incentivos, días de inventario del concesionario, garantías, margen por EV, contenido regional. *Múltiplo:* EV/EBITDA automotriz (sin financiera) en ciclo medio.

**Telecom.** *Modelo:* red de costo fijo, ingreso recurrente, madurez. *KPIs:* ARPU, churn, altas de pospago, capex/ingresos, EBITDA − capex, deuda neta/EBITDA, espectro y preponderancia (México). *Múltiplo:* EV/EBITDA y FCF yield.

**Aeropuertos (México).** *Modelo:* concesión con tarifa máxima fijada en el Programa Maestro de Desarrollo (PMD) quinquenal. Los ingresos aeronáuticos (TUA; el pasajero internacional paga más, en USD) son regulados; los comerciales no. *KPIs:* pasajeros nacionales e internacionales, ingreso comercial por pasajero, **margen EBITDA ajustado sin IFRIC 12** (los ingresos por construcción inflan ingresos sin margen), capex comprometido y deuda/EBITDA.

---

## 3. Literatura y fuentes canónicas

| Autor(es) | Año | Obra | Hallazgo cuantificado | Enlace | Grado |
|---|---|---|---|---|---|
| Porter | 2008 | "The Five Competitive Forces That Shape Strategy", HBR (ene-2008) | La competencia incluye clientes, proveedores, entrantes y sustitutos, no solo rivales. Marco sin cifras en el extracto verificado | [52] | B (herramienta) |
| Moskowitz, Grinblatt | 1999 | "Do Industries Explain Momentum?", JF 54(4) | El momentum de industria explica buena parte del momentum individual (magnitud no verificada en esta sesión) | [46] | B |
| Hong, Torous, Valkanov | 2007 | "Do Industries Lead Stock Markets?", JFE | Algunas industrias anticipan al mercado agregado (detalle no verificado en esta sesión) | [47] | C |
| Cohen, Frazzini | 2008 | "Economic Links and Predictable Returns", JF (ago-2008) | El cliente principal pesa ~20% de las ventas del proveedor. Comprar proveedores tras choques positivos del cliente y vender tras negativos rinde más allá de factores y de momentum (~150 pb/mes, no verificado) | [48] | B |
| Cooper, Gulen, Schill | 2008 | "Asset Growth and the Cross-Section of Stock Returns", JF | Las empresas que más crecen en activos rinden menos después (magnitud: ver cap. 06) | [50] | B |
| Jacobsen, Stangl, Visaltanachoti | 2009 | "Sector Rotation across the Business Cycle" (SSRN 1467457) | La rotación por fase del ciclo aporta poco aun con información favorable (magnitud no verificada en esta sesión) | [51] | D (la estrategia) |
| Greenwood, Hanson | 2015 | "Waves in Ship Prices and Investment", QJE 130(1):55-109 | Ganancias altas → precios de barcos e inversión altos → **rendimientos futuros bajos**. Se explica por extrapolación más **negligencia de la competencia** | [45] | B (una industria; el mecanismo es general) |
| Chancellor (ed.) | 2016 | *Capital Returns* (Palgrave Macmillan) | Método del ciclo de capital (Marathon): invertir donde la oferta se contrae y evitar donde se expande | [49] | C |
| Deeter, Bondy (Bessemer) | 2024 | "The Rule of X" (2-ene-2024) | Contra EV/ingresos NTM: R² de **62%** para la Rule of X y de 50% para la Rule of 40. BVP Cloud Index a fines de 2023: Rule of 40 ~31% (decil superior ~48%) | [17] | C (explica múltiplos, no rendimientos) |
| Damodaran | ene-2026 | Datasets por industria (5,994 empresas de EUA) | Múltiplos, márgenes, ROE/ROIC y costo de capital (§2.5) | [1]-[5] | A (dato descriptivo) |

---

## 4. Lo más reciente 2023-2026

### 4.0 Hueco declarado
No se verificó en esta sesión literatura académica de 2023-2026 específica de industrias: se agotó la cuota de búsqueda. Lo nuevo aquí son datos primarios de 2026. **Pendiente para la siguiente rutina:** buscar y verificar trabajos de 2023-2026 sobre momentum de industria después de su publicación, IA y márgenes de software, y ciclos de capex de IA.

### 4.1 Mapa de rendimientos 2026 (cálculo propio, cierre ajustado de Yahoo al 23/24-sep-2026, moneda local) [53]

| Sector (ETF) | YTD | 12 meses | Desde máx. 52 sem. |
|---|---|---|---|
| Semis (SOXX) | **+88.3%** | +111.0% | −13.5% |
| Energía (XLE) | +42.8% | +42.5% | −4.5% |
| Telecom (IYZ) | +23.8% | +32.3% | −9.0% |
| Biotech (XBI) | +28.1% | +60.8% | −8.0% |
| S&P 500 (SPY) | +13.4% | +17.3% | −1.1% |
| Salud (XLV) | +11.1% | +26.6% | −2.9% |
| Industriales (XLI) | +9.7% | +12.2% | −9.2% |
| Consumo básico (XLP) | +7.2% | +6.9% | −7.5% |
| Inmobiliario (XLRE) | +5.7% | +3.7% | −8.7% |
| Software (IGV) | **+1.4%** | −7.0% | −8.5% |
| Financieras (XLF) / Seguros (KIE) | +0.8% / +0.4% | +3.3% / +2.9% | −6.6% / −9.9% |
| Utilities (XLU) | −5.9% | −6.1% | −15.8% |
| Consumo discrecional (XLY) | −7.0% | −7.2% | −10.9% |
| IPC México (^MXX, precio) | −0.1% | +3.8% | −10.2% |

Materias primas (futuros, 25-sep): WTI US$92.75 (+61.5% YTD), Brent US$105.45, cobre US$6.76/lb (+42.2% a 1 año), oro US$4,304.7 y plata US$64.10 (−44.3% desde su máximo de 52 semanas). USD/MXN 17.70.

### 4.2 Semiconductores: superciclo de memoria
- **WSTS (primavera de 2026):** el mercado crecería **+90% en 2026, a US$1.51 billones**, y +27% en 2027, a ~US$1.9 billones. Memoria **~+250%, a más de US$800 mil M**; lógica +37%; analógicos +10% [6].
- **SIA:** ventas de julio de 2026 de **US$146.8 mil M** (+135.1% a/a; +6.4% m/m). Lo acumulado a julio ya supera el mayor total anual de la historia [7].
- **TrendForce (3-jul-2026):** precios contrato del 3T26 de DRAM +13-18% t/t y de NAND +10-15%. El alza se modera porque los clientes de PC y teléfonos llegan a su "límite de asequibilidad" [8]. **Inferencia:** la segunda derivada del precio ya es negativa. En el ciclo de memoria esa es la primera señal de pico.
- **Micron:** 3T FY26 con ingresos de US$41.5 mil M y margen bruto de 84.6%. Guía del 4T: US$50 ± 1 mil M con margen de ~86%. Tiene acuerdos take-or-pay por US$22 mil M (~18 mil M en depósitos de efectivo) con **techo y piso de precio** (ficha interna) [9]. Reporta el 30-sep-2026 [21].
- **NVIDIA:** 2T FY27 con ingresos de US$96.2 mil M (+106%), data center 92.5% e inventario de US$31.6 mil M (+22% t/t). Guía del 3T: US$108 mil M ±2%. La empresa espera que el margen bruto toque fondo en 71-72% en el 4T por el costo de la memoria (ficha interna) [10].
- **Equipo (XBRL, cálculo propio):** AMAT +24.8% a/a en su 3T FY26; Lam +30.0% en su 4T FY26; KLA +15.2% [11].
- **Riesgos 2026:** reversión del precio de la memoria, inventario en el canal, techos de precio en contratos, controles a China (cap. 23) y demanda concentrada en 4-5 compradores.

### 4.3 Hyperscalers: la economía del capex de IA (XBRL de la SEC, cálculo propio) [11]-[15]

| Empresa (12 m a jun-2026; MSFT = FY26) | Ingresos | Capex | Capex/ingresos | Flujo operativo | FCF | Capex 2T26 | Capex 2T25 |
|---|---|---|---|---|---|---|---|
| Microsoft | 331,839 | 115,948 | 34.9% | 182,935 | 66,987 | 35,802 | 17,079 |
| Alphabet | 445,867 | 132,402 | 29.7% | 185,675 | 53,273 | 44,924 | 22,446 |
| Amazon | 775,680 | 173,028 | 22.3% | 161,403 | −11,625 | 54,208 | 32,183 |
| Meta | 228,247 | 89,325 | 39.1% | 130,301 | 40,976 | 30,116 | 16,538 |
| **Total (US$ M)** | **1,781,633** | **510,703** | **28.7%** | **660,314** | **149,611** | **165,050** | **88,246** |

- El capex de 12 meses equivale al **77.3% del flujo operativo**. El del 2T26 creció **+87% a/a** y, anualizado, da ~US$660 mil M.
- **Guías y señales:** Meta sube su capex de 2026 a **US$130-145 mil M** (incluye arrendamientos financieros) [12]. Google Cloud creció **+82%, a US$24.8 mil M**, con utilidad operativa de US$8.8 mil M; la depreciación subió 42% a/a [13]. AWS creció +37% (US$42.2 mil M) con margen de 39.4%; el FCF de 12 meses de Amazon fue de **−US$7.6 mil M** según su definición [14].
- **Utilidades infladas por participaciones:** Alphabet registró **US$99.0 mil M** de ganancias en valores de capital en el 2T26 (utilidad neta de US$112.2 mil M) [13]. Amazon, **US$53.4 mil M** antes de impuestos, "principalmente" por Anthropic [14]. **Regla:** en hyperscalers el análisis se hace con la utilidad operativa y el FCF, no con la UPA.
- **Oracle, el caso de estrés:** en 12 meses a ago-2026, capex de US$75.7 mil M (**105% de los ingresos**) y FCF de −US$28.7 mil M. El RPO es de **US$664 mil M** y OCI crece +121% [15]. Aun así, la acción cayó −55% en 12 meses (ficha interna). **Inferencia:** el mercado castiga el capex financiado con deuda y concentrado en un cliente aunque el backlog sea récord.
- **Riesgos 2026:** monetización de la inferencia más lenta que el capex, vidas útiles más largas (edificios de Microsoft de 15 a 25 años desde el FY27, ficha interna) [16], financiamiento de los laboratorios y energía.

### 4.4 Software/SaaS: el "SaaSpocalypse" y la Rule of 40 ajustada por SBC
En feb-2026, los agentes de IA llevaron a revaluar el software cobrado por usuario. El IGV cayó **−36.6%** entre el 22-sep-2025 y el 10-abr-2026 (cap. 17) [18]. En 2026 va +1.4%, contra +35.7% de XLK. Rule of 40 con datos XBRL de 12 meses (cálculo propio) [11]:

| Empresa | Crec. ingresos | Margen FCF | Rule of 40 | SBC/ingresos | **R40 − SBC** |
|---|---|---|---|---|---|
| Datadog | 31.5% | 29.8% | 61.3 | 20.7% | 40.6 |
| Snowflake | 32.0% | 22.0% | 54.0 | 30.2% | **23.8** |
| CrowdStrike | 24.3% | 29.8% | 54.1 | 23.1% | 31.0 |
| ServiceNow | 22.2% | 31.1% | 53.3 | 14.8% | 38.5 |
| Adobe | 12.0% | 40.8% | 52.8 | 8.0% | 44.8 |
| Salesforce | 11.2% | 34.5% | 45.7 | 8.3% | 37.4 |
| Workday | 13.3% | 28.0% | 41.3 | 16.2% | **25.1** |

**Inferencia:** todas "pasan" la Rule of 40; al descontar la SBC, Snowflake y Workday quedan cerca de 25. La recompra que neutraliza la dilución (Salesforce −14.7% de acciones diluidas a/a; Workday −8.8%) es un uso de caja, no un regalo. **Riesgos 2026:** el cobro por asiento contra agentes, la compresión del NRR y la IA que baja el costo de replicar funciones.

### 4.5 Bancos
- **EUA (FDIC, 2T26):** utilidad de **US$90.1 mil M**, ROA de 1.37% y **NIM de 3.32%** (+1 pb t/t). Préstamos +1.8% t/t (+6.8% a/a) y depósitos +0.8%. Bajaron la morosidad y los castigos [19]. Damodaran: money center con P/VL de 1.62 y ROE de 12.86%; regionales con 1.14 y 9.75% [3]. KRE va +11.4% en 2026.
- **México (Banorte, 2T26):** NIM del banco de 6.9%, costo de riesgo de 1.9%, ROE de 25.7%, CET1 de 12.55%, IMOR de 1.50% (+38 pb a/a) y **cobertura de 134% (antes 158%)**. P/VL de 2.20x (ficha interna) [20]. Con ke de 13.5% y g de 4-5%, **el precio exige un ROE sostenible de 23.7-24.9%**, contra una guía de 22-24%. Banxico en 6.50%, tres pausas (cap. 16).
- **Riesgos 2026:** recortes de tasa, morosidad del consumo al alza con cobertura a la baja, soberano (S&P BBB negativa) y AML/FinCEN.

### 4.6 Aseguradoras: señales de soft market
- **Travelers 2T26:** combined ratio de **83.6%** (subyacente 84.1%). Catástrofes por US$518 M y **liberación de reservas de años previos por US$578 M**. Cambio de prima en renovaciones de Business Insurance de **4.8%**. ROE core de 24.9% [22].
- **Progressive, agosto de 2026:** combined ratio de **89.3 contra 83.1** un año antes; 87.2 en el año. Prima neta suscrita +6%, contra crecimientos de ingresos de dos dígitos en 2025 (XBRL, +14.2% en el 3T25) [23][11].
- Damodaran P&C: P/VL de 2.02 con ROE de 18.71% [3]. KIE va +0.4% en 2026.
- **Inferencia:** la rentabilidad técnica tocó su pico en 2025. Las tarifas se desaceleran y las liberaciones de reservas embellecen el resultado reportado. Es la fase del ciclo en que el P/U se ve bajo y el ROE futuro baja.

### 4.7 Energía
- **Breakevens (Dallas Fed, 1T26):** pozo nuevo, **US$66/b** en promedio (Pérmico 67; grandes 59; chicas 68); operar pozos existentes, **US$43/b** (grandes 32; chicas 46). Pronóstico de los encuestados: WTI de US$74 al cierre de 2026 [24].
- **EIA (STEO, 9-sep-2026):** Brent de ~US$90 en 2026 que **baja a US$74 en 2027**. EUA producirá 13.8 mb/d (2026) y 14.3 (2027). Inventarios globales −400 M de barriles en el año [25]. El spot sigue en WTI 92.75 y Brent 105.45 tras la guerra de Irán (cap. 16).
- Damodaran: integradas a 8.16x EV/EBITDA y E&P a 5.15x [1]. Chevron: 12.7x el P/U de 2026e; su DCF inverso descuenta un FCF entre el de Brent a 70 y el actual (ficha interna) [26].
- **Inferencia:** con el WTI ~US$27 arriba del breakeven de pozo nuevo, el reloj de capital predice más oferta en 2027, y la curva de la EIA ya lo refleja. Las acciones descuentan un precio normalizado, no el spot.

### 4.8 Minería y materiales
- **Southern Copper (Grupo México), 2T26:** cobre LME de **US$6.04/lb (+39.8%)**. Costo en efectivo antes de subproductos de **228.8¢/lb**; neto de subproductos, **4.6¢/lb** (63.1¢ un año antes). Margen EBITDA de 66.6% y capex +79.4% [27]. **Trampa:** el 4.6¢ depende del precio de la plata y el molibdeno. El costo que define la posición en la curva es el de 228.8¢.
- **Peñoles, 2T26:** plata a US$73.42/oz y oro a US$4,506/oz. Margen operativo de 44.5% (ficha interna) [28]. Hoy la plata está en US$64.10 (−44% desde el máximo).
- **Cemex, 2T26:** ventas de US$4,593 M (+12%; +7% comparable) y EBITDA de US$1,018 M (+24%) con margen de 22.2%. FCF de operación de US$637 M (se triplicó). Apalancamiento de **2.08x**. **Guía de EBITDA 2026 elevada a +16-17%**. México: cemento +7% en volumen y +6% en precio local; concreto −2% en volumen. EUA: cemento plano en volumen y −2% en precio [43]. GCC: cemento en EUA +10.8% en volumen y −3.2% en precio por importaciones (ficha interna) [44].
- Damodaran: metales y minería a 11.39x EV/EBITDA con ROE de 17.79%; materiales de construcción a 11.61x [1][3].

### 4.9 Consumo
- **ANTAD, agosto de 2026:** mismas tiendas **+1.7% nominal**, tiendas totales +4.2% y +1.5% mismas tiendas en el año [29]. Con inflación de 3.42% (cap. 16), el **real es de ≈ −1.7%**.
- **Walmex 2T26:** mismas tiendas en México +1.8% (ticket +2.9%, **tráfico −1.1%**) y margen EBITDA de 9.4%. Guía revisada por un consumo "más lento". P/U de 15.9x contra ~21.5x en 2022-2025; −18.2% en 2026 (ficha interna) [30].
- **FEMSA 2T26:** OXXO México con mismas tiendas **+9.5%** (ticket +7.4%, tráfico +2.0%) con efecto Mundial. Guía de un segundo semestre "más moderado". VE/EBITDA de 8.0x (ficha interna) [31].
- EUA: XRT −3.1% y XLY −7.0% en 2026. Damodaran: autoservicio a 8.94x y minoristas generales a 17.38x [1].

### 4.10 REITs y FIBRAs (nearshoring)
- **FIBRA Prologis, 2T26:** ocupación de **95.8% (97.7% un año antes)**, retención de **60.8% (86.0%)**, cambio de renta efectiva neta en renovación de **+40.8% (+68.0%)**, NOI en efectivo de mismas propiedades +13.1%, FFO por CBFI de US$0.0613 (+4.8%) y LTV de 24.7% [32].
- **Vesta, 2T26:** ocupación de 91.7% y estabilizada de 93.7%. Spread de renovación de 10.3% y NOI de mismas propiedades +5.9%. **El FFO creció 6.8%, pero por acción cayó −1.8%** por dilución. P/FFO de 16.3x, **cap rate implícito de 7.2%** y P/NAV de 0.97x (ficha interna) [33].
- IED del 1S-2026: récord de US$34,968 M, pero la **inversión nueva es solo 7.8%** del total (cap. 16). T-MEC con revisiones anuales.
- **Inferencia:** los contratos anteriores a 2022 aún se re-rentan con alzas fuertes, pero ocupación, retención y spread caen a la vez: ciclo que madura. Damodaran REIT: EV/EBITDA de 19.87 y costo de capital de 5.32% [1][5].

### 4.11 Utilities
EIA: consumo eléctrico récord de EUA de **4,135 TWh en 2026 y 4,211 en 2027**, por centros de datos y manufactura [25]. Aun así, XLU cae −5.9% en el año y −15.8% desde su máximo del 27-feb-2026 (cálculo propio). Duke: capex de 12 meses (a mar-2026) de US$15.0 mil M contra flujo operativo de 11.7 mil M, con **FCF negativo** (XBRL) [11]. **Inferencia:** la narrativa de demanda de IA ya se pagó en 2025. Con tasas largas altas y la necesidad de emitir capital para el capex, el sector vuelve a comportarse como bond proxy.

### 4.12 Farmacéuticas, biotech y GLP-1
- **Lilly 2T26:** ingresos de **US$23.0 mil M (+48%)**. EUA: volumen +37% y precio −3%. Fuera de EUA: volumen +113% y **precio −36%** (Mounjaro entró a la NRDL de China). Mounjaro US$9.9 mil M (+91%), Zepbound US$4.9 mil M y Foundayo (orforglipron oral) US$98 M. Margen bruto de 85.8% y guía de 2026 de US$85-87 mil M [34].
- **Política:** acuerdo MFN (6-nov-2025) en el que Medicare paga **US$245** con copago de US$50 (ficha interna, fuente Lilly/CNBC). Sección 232 con 100% a fármacos patentados desde el 31-jul-2026, con exención para firmantes MFN (cap. 24).
- **LOE en acción:** Stelara (J&J) **−41% en 2025** por biosimilares (ficha interna) [35].
- Valuación: Lilly a 24.9x la UPA de 2027e contra Novo Nordisk a 11.5x su P/U futuro (ficha interna). XBI +28.1% en 2026. Damodaran farma: EV/EBITDA de 15.25 [1].
- **Riesgos 2026:** precio neto de GLP-1, elecciones intermedias del 3-nov y aranceles 232.

### 4.13 Industriales: el backlog de la energía para IA
- **GE Vernova 2T26:** pedidos de **US$24.2 mil M (+88% orgánico)** contra ingresos de US$11.1 mil M: **book-to-bill ≈ 2.2x** (cálculo propio). Backlog de US$176 mil M; turbinas de gas de 100 a **116 GW** entre cartera y reservas de slots, con meta de 125 GW o más. FCF 2026 guiado en US$11.5-12.5 mil M [36].
- **Caterpillar 2T26:** backlog récord de **US$72.1 mil M (+92%)**, 59% entregable en 12 meses; generación eléctrica +72% (ficha interna) [37].
- Damodaran: maquinaria a 16.22x, equipo eléctrico a **24.59x** y aeroespacial/defensa a 21.58x [1].
- **Inferencia:** el backlog concentrado en un solo mercado final (centros de datos) sube la visibilidad y también el riesgo de cancelación. Un book-to-bill menor a 1 durante dos trimestres sería la señal de giro.

### 4.14 Autos/EV
XBRL de 12 meses (cálculo propio) [11]: Tesla con ingresos de US$103.6 mil M, margen operativo de 4.2% (1.4% en el 2T26) y capex del 2T26 de US$5.8 mil M con FCF trimestral de −1.1 mil M; −16.0% en 2026. GM, margen operativo de 12 meses de 1.0%. Ford, pérdida de US$11.1 mil M en el 4T25 (margen operativo de −25.2%). La OBBBA eliminó los créditos a EV (cap. 24). Sección 232 de 25% a autos; EUA pide 50% de contenido estadounidense en el T-MEC (cap. 16). **Inferencia:** es la industria de ROIC más bajo (2.25%, Damodaran), con cargos por la transición a EV y aranceles. Para México, el riesgo pasa por las reglas de origen.

### 4.15 Telecom
América Móvil 2T26: ingresos de Ps 241.1 mil M (+3.1%), margen EBITDA de 39.8%, capex de ~US$7 mil M en 2026 y meta de apalancamiento de 1.2-1.5x. **VE/EBITDA de 4.7x** y FCF yield de 8.9% (ficha interna) [38]. AT&T: capex de 17.5% de los ingresos y crecimiento de +2.6% (XBRL) [11]. IYZ va +23.8% en 2026. Damodaran: servicios a 6.54x y wireless a 8.97x [1].

### 4.16 México: tablero de emisoras clave (2T26 y agosto de 2026)

| Emisora | KPI que mueve el precio | Último dato | Lectura | Riesgo 2026 | 2026 YTD* |
|---|---|---|---|---|---|
| Banorte | NIM, costo de riesgo, ROE contra ke | NIM del banco 6.9%, CoR 1.9%, ROE 25.7%, cobertura 134% | El precio pide un ROE de 24-25% sostenido | Recortes de Banxico, consumo, soberano | +23.7% |
| Walmex | Mismas tiendas y tráfico | +1.8% (tráfico −1.1%); ANTAD ago +1.7% nominal | Consumo real negativo; P/U en mínimo de 4 años | Consumo, margen, competencia | −18.2% |
| FEMSA | Mismas tiendas de OXXO, Spin, Salud | +9.5% (Mundial) | Base alta para el 2S26 | Normalización y pérdidas de Spin | +21.0% |
| Grupo México | Precio del cobre y costo | Cu US$6.04/lb; costo bruto 228.8¢ | Cobre en pico de ciclo; primer cuartil de la curva | Reversión del cobre y la plata | +32.7% |
| Cemex | Volumen × precio y apalancamiento | EBITDA +24%, 2.08x; guía +16-17% | Mejora operativa sin premio en precio | EUA (precio −2%), obra pública | −16.3% |
| ASUR | Pasajeros internacionales en Cancún | Ago −2.1%; Cancún internacional −15.0%; EBITDA aj. 62.0% (67.6%) | Caída del internacional con capex al alza | Turismo desde EUA, PMD | −26.4% |
| GAP | Mezcla nacional/internacional | Ago +0.5%; año −3.9% (internacional −8.4%); Guadalajara +10.5% | Los destinos de playa pesan | Los Cabos, Vallarta, Jamaica | −22.9% |
| OMA | Pasajeros de negocio (norte) | Ago +4.0% (internacional +7.0%) | El mejor de los tres | Revisión del T-MEC | −6.8% |
| FIBRA Prologis / Vesta | Ocupación, retención, spread | 95.8% / 91.7%; spreads de 40.8% / 10.3% | Ciclo maduro y demanda que se enfría | T-MEC, nueva oferta | +2.2% / +5.2% |

\*Cálculo propio, cierre ajustado de Yahoo al 23-sep-2026. Fuentes: [20][29][30][31][27][43][39][40][41][42][32][33].

---

## 5. Evidencia real: qué funciona, qué no, magnitudes

### 5.1 Veredicto por idea

| Idea | Evidencia | Muestra / estado | Grado |
|---|---|---|---|
| El ciclo de capital (oferta) predice rendimientos: evitar sectores con capex y precios de activo altos | Greenwood-Hanson (QJE); asset growth (Cooper-Gulen-Schill, cap. 06); caso Micron | In-sample académico, consistente en varias industrias | **B** |
| La información fluye lento por vínculos económicos (cliente → proveedor) | Cohen-Frazzini (JF 2008) | In-sample; decaimiento posterior a la publicación no verificado | **B** |
| Momentum de industria | Moskowitz-Grinblatt (JF 1999) | Magnitud posterior a la publicación no verificada en esta sesión | **B/C** |
| Industrias que anticipan al mercado | Hong-Torous-Valkanov (JFE 2007) | Detalle no verificado | **C** |
| Rotar sectores según la fase del ciclo económico ("reloj de inversión") | Jacobsen-Stangl-Visaltanachoti (2009): gana poco | Exige fechar el ciclo en tiempo real y el mercado se adelanta | **D** |
| Rule of 40/X como filtro de calidad en SaaS | Bessemer: R² de 50-62% contra múltiplos | Explica valuación, no rendimientos futuros | **C** |
| Comprar cíclicos a P/U bajo | Micron 2018 y 2022 (§5.2) | Pierde de forma sistemática en el pico | **D (como regla)** |
| KPIs sectoriales como filtro de riesgo (cobertura, combined subyacente, costo bruto, AFFO) | Contabilidad y casos | Evita pérdidas; no genera alfa por sí solo | **B** |

### 5.2 La paradoja del cíclico, en datos (cálculo propio con Yahoo y XBRL) [11][53]
- **Micron 2018:** la acción tocó máximo el **29-may-2018** con márgenes récord (margen bruto del FY18 de 58.9%) y cayó **−53.7%** al 24-dic-2018. El margen del FY19 fue de 45.7% y el del FY20 de 30.6%.
- **Micron 2022:** máximo el 14-ene-2022 y caída de **−49.6%** al 26-sep-2022. La utilidad tocó fondo **después**: FY23 con margen bruto de −9.1%, cerrado en ago-2023. **La acción tocó fondo casi un año antes que la utilidad.**
- **Semis (SOXX):** −45.8% (dic-2021 a oct-2022) y −41.4% (jul-2024 a abr-2025). NVIDIA: **−66.3%** (nov-2021 a oct-2022).
- **Micron 2024-25:** −57.6% (jun-2024 a abr-2025), antes del superciclo actual.
- **Lección cuantificada:** en semis, una caída de 40-65% desde el pico es la norma del ciclo, no la excepción. Con `riesgo_por_operacion` de 3% en la arena, un stop a −10% en un semiconductor cíclico permite una posición de ≤30% del capital (3%/10%), el tope de `accion_individual_max`. **El stop tiene que existir:** el ciclo no avisa.

### 5.3 Caídas sectoriales de referencia (cálculo propio) [53]

| Sector | Episodio | Caída máxima | Detonador |
|---|---|---|---|
| Bancos regionales (KRE) | 14-ene-2022 → 4-may-2023 | **−52.7%** | Tasas + pérdidas no realizadas + corrida (SVB) |
| Software (IGV) | 22-sep-2025 → 10-abr-2026 | **−36.6%** | Sustitución por agentes de IA ("SaaSpocalypse") |
| Energía (XLE) | 8-jun-2022 → 14-jul-2022 | −26.0% | Reversión del crudo tras el pico de 2022 |
| Utilities (XLU) | 27-feb-2026 → 24-sep-2026 | −15.8% | Tasas largas y emisión para capex |
| Aeropuertos (ASURB) | 12 meses a sep-2026 | −34.4% (máx. de 1 año) | Tráfico internacional en Cancún |

---

## 6. Traducción operable

### 6.1 Reglas del sistema
- **R1. Clasificar antes de valuar.** Toda ficha (`skill ficha-empresa`) declara el motor de valor (§2.2) y usa su métrica correcta. Prohibido usar EV/EBITDA en bancos y P/U corriente en commodities o memoria.
- **R2. Normalizar cíclicos.** Para semis, memoria, minería, energía, acero, autos, aseguradoras y químicos: UPA normalizada = ventas de tendencia × margen mediano de 7-10 años (o de todo el ciclo disponible). Si el margen corriente está arriba del percentil 80 de su historia y el P/U corriente es menor a la mitad de su mediana, **alerta de pico: no se abren largos nuevos por valuación**; solo por tendencia, con stop. (Umbrales propios, por validar en papel.)
- **R3. Tablero de ciclo de semis (revisión mensual):** (a) precio contrato DRAM/NAND t/t (TrendForce): una desaceleración de dos trimestres seguidos es alerta; (b) SIA a/a en promedio móvil de 3 meses; (c) días de inventario de NVDA, MU y AMAT; (d) guías de capex de hyperscalers; (e) book-to-bill del equipo. **Tres de cinco en contra = reducir 50% la exposición a semis** (umbral propio, por validar), en línea con el cortacircuitos de la arena.
- **R4. Hyperscalers:** registrar cada trimestre capex/ingresos, capex/flujo operativo (hoy 77.3%), capex/D&A, FCF después de arrendamientos y la concentración del RPO. Capex/flujo operativo arriba de 90% en el agregado, o FCF agregado negativo, **sube el grado de riesgo del tema IA** en el registro de riesgos (cap. 07; umbral propio).
- **R5. SaaS:** filtro de calidad = **Rule of 40 − SBC ≥ 30**, NRR ≥ 110% cuando se revele, y dilución neta ≤ 2% a/a sin contar recompras. Excluir de la valuación la UPA "non-GAAP" que suma la SBC de regreso.
- **R6. Bancos:** calcular el ROE implícito con P/VL = (ROE − g)/(ke − g). Si el ROE implícito supera el techo de la guía y la cobertura cae dos trimestres seguidos, no se toman largos.
- **R7. Aseguradoras:** usar el combined subyacente, no el reportado. Si el cambio de tarifa en renovaciones se desacelera por 2-3 trimestres y las liberaciones de reservas superan 3-4 pp del combined (Travelers: US$578 M), tratar el ROE como de pico (umbral propio, por calibrar).
- **R8. Energía y minería:** valuar a la curva de futuros y al precio de ciclo medio. Posición en la curva con el costo **antes** de subproductos. Exigir un breakeven de FCF (con dividendo) bajo el precio de la curva a 24 meses.
- **R9. Consumo:** usar mismas tiendas **real** (nominal − INPC) y separar tráfico de ticket. Tráfico negativo dos trimestres seguidos = el margen será el siguiente en caer.
- **R10. FIBRAs y REITs:** usar AFFO por certificado, no FFO total, porque la dilución importa (Vesta: FFO +6.8% y por acción −1.8%). Comparar el cap rate implícito contra el Mbono a 10 años o el UST más la prima de la moneda de las rentas. Si ocupación, retención y spread caen a la vez, el ciclo es maduro.
- **R11. Farma:** si más de 30% de las ventas depende de productos con LOE en menos de 5 años, descontar el precipicio explícitamente (referencia: Stelara −41% en el primer año). Para GLP-1, separar precio neto de volumen cada trimestre.
- **R12. Industriales:** book-to-bill menor a 1 dos trimestres seguidos = alerta de giro. Revelar el porcentaje del backlog en un solo mercado final.
- **R13. Utilidades con participaciones:** en toda empresa con inversiones de capital relevantes (Alphabet, Amazon, Microsoft/OpenAI, NVIDIA), las proyecciones usan la utilidad operativa y el FCF.
- **R14. Concentración (de `parametros.json`):** en el patrimonio principal, `sector_max` = **25%** y `accion_individual_max` = 10%. La arena no define un límite sectorial. **Propuesta (requiere aprobación del dueño; no cambia `parametros.json`):** tope sectorial provisional de 50% en la arena, porque semis y energía tienen caídas de 40-65% en un ciclo (§5.3) y `accion_individual_max` = 30% ya permite concentrar.
- **R15. Costos y rotación de la arena:** una tesis sectorial se ejecuta con como máximo 1-2 órdenes (orden mínima de Ps 5,000; `operaciones_max_mes` = 8; rotación ≤ 1.5x) y solo con un movimiento esperado de 5% o más. Rotar sectores por fase del ciclo (grado D) **no justifica** operaciones.

### 6.2 Checklist de 60 minutos para analizar cualquier empresa

| Min. | Paso | Salida concreta |
|---|---|---|
| 0-5 | **Clasificar:** motor de valor (§2.2), industria de Damodaran y múltiplo correcto | "Es un negocio de ___; se valúa con ___" |
| 5-15 | **Economía unitaria:** cómo gana un peso (precio × volumen, spread, prima, renta, suscripción); 3 KPIs de su ficha sectorial (§2.6) con 8 trimestres | Tabla de KPIs y su tendencia |
| 15-22 | **Ciclo:** ubicar los 4 relojes. Margen actual contra percentil histórico; capex de la industria/ventas; inventarios; ¿oferta entrando? | "Fase: temprana / media / pico / contracción" y evidencia |
| 22-30 | **Estructura y ventaja:** ROIC contra WACC 5-10 años; ROIC de la industria (§2.1); 5 fuerzas en una línea cada una; posición en la curva de costos o en la cuota | ¿Moat o marea? |
| 30-38 | **Calidad del número:** FCF/UN, SBC/ingresos, dilución, ganancias no operativas, IFRIC 12, créditos de subproductos, liberación de reservas, capitalizaciones, vida útil | Utilidad "limpia" |
| 38-46 | **Balance y fondeo:** deuda neta/EBITDA a precio medio; vencimientos; CET1 o cobertura (bancos); LTV (FIBRAs); arrendamientos | ¿Sobrevive al fondo del ciclo? |
| 46-54 | **Valuación:** múltiplo correcto contra la tabla de Damodaran, contra su historia y contra pares; DCF inverso (cap. 03): ¿qué margen y crecimiento descuenta el precio? | "Descuenta ___; plausible / exigente" |
| 54-58 | **Riesgos y catalizadores:** regulación (caps. 23-24), fechas de reporte, KPI que invalidaría la tesis | Lista con fechas |
| 58-60 | **Veredicto y pronóstico:** tesis en una frase + pronóstico binario con probabilidad registrado en `pronosticos.csv` antes del siguiente reporte | Registro para Brier (`brier_objetivo` 0.20) |

### 6.3 Umbrales rápidos por sector (propios, por validar con historia antes de usarse como gatillo)
- **Semis:** alerta si el precio de la memoria sube < 5% t/t después de haber subido más de 10%, o si los días de inventario suben dos trimestres con ventas al alza.
- **SaaS:** NRR < 105% o Rule of 40 − SBC < 20 = negocio en madurez o en riesgo de sustitución.
- **Bancos:** IMOR +50 pb a/a con cobertura < 120% = el costo de riesgo va a subir.
- **Aseguradoras:** subyacente > 95% en daños = la rentabilidad técnica se agotó.
- **Energía:** WTI < breakeven de pozo nuevo (US$66) por más de 6 meses = recortes de capex y oferta, que alistan el siguiente ciclo alcista.
- **FIBRAs:** retención < 70% y ocupación a la baja por 2 trimestres = pico de rentas cercano.
- **Aeropuertos:** caída del internacional mayor a 10% dos meses seguidos en el aeropuerto principal (Cancún) = revisar las estimaciones de ingreso aeronáutico.

---

## 7. Trampas y errores comunes
1. **P/U bajo en el pico del ciclo:** Micron a 8.7x la UPA anualizada con 86% de margen guiado.
2. **EBITDA en negocios intensivos en capital:** ignora el capex (hyperscalers con capex de 28.7% de los ingresos; utilities con FCF negativo).
3. **Costo neto de subproductos:** 4.6¢/lb contra 228.8¢ antes de créditos (Southern Copper).
4. **Utilidad inflada por revaluaciones:** valores de capital (Alphabet US$99.0 mil M; Amazon US$53.4 mil M), revaluación de naves (Vesta US$49.6 M) y dilución en OpenAI (Microsoft).
5. **IFRIC 12:** ASUR creció +9.9% en ingresos, pero −0.3% sin construcción.
6. **Rule of 40 sin SBC:** Snowflake pasa de 54 a 24.
7. **Combined reportado con liberación de reservas:** embellece el año y anticipa un soft market.
8. **FFO total en lugar de FFO/AFFO por certificado:** Vesta tuvo FFO +6.8% y −1.8% por acción.
9. **Mismas tiendas nominales:** +1.7% con inflación de 3.42% es ≈ −1.7% real.
10. **Agregados de Damodaran sin contexto:** Tesla en autos, pérdidas en biotech, betas bajas en utilities.
11. **El backlog como caja:** Oracle, con RPO de US$664 mil M, FCF de −US$28.7 mil M y acción −55%.
12. **Cambios de vida útil:** mueven la UPA sin mover la caja (cap. 25).
13. **Narrativa sectorial sin flujo:** nearshoring con IED nueva de 7.8% (cap. 16); consumo eléctrico récord con XLU −15.8%.
14. **Rotación por "reloj del ciclo":** marketing, grado D.
15. **La moneda:** rentas industriales en USD (Vesta 89.3%) y mineras en USD contra un resultado del dueño medido en MXN (`moneda_base`).

---

## 8. Examen de titulación

1. **¿Por qué un P/U bajo es peligroso en un cíclico? Usa Micron.** Porque la UPA de pico no es sostenible. Micron cotiza a 8.7x la UPA anualizada con la guía (margen de ~86%), y en el FY2023 su margen bruto fue de −9.1%. La acción tocó fondo ~1 año antes que la utilidad en 2022-2023. Se valúa con margen de ciclo medio.
2. **¿Qué son el reloj de capital y el hallazgo de Greenwood-Hanson?** Márgenes altos → capex → oferta nueva → precios bajos. En fletes, las ganancias y la inversión altas predicen rendimientos futuros bajos por extrapolación y por ignorar la respuesta de los competidores.
3. **Calcula la Rule of 40 y la ajustada por SBC de Snowflake.** Crecimiento de 32.0% + margen FCF de 22.0% = 54.0; menos SBC de 30.2% = 23.8.
4. **¿Qué ROE sostenible exige el P/VL de 2.20x de Banorte con ke de 13.5% y g de 4-5%?** De 2.2 = (ROE − g)/(ke − g) sale un ROE de 23.7-24.9%. La guía es de 22-24%, así que el precio pide el tope de la guía indefinidamente.
5. **Travelers reportó un combined de 83.6% con US$578 M de liberación de reservas y renovaciones en +4.8%. ¿Qué lees?** El subyacente es de 84.1%, todavía rentable. Pero las liberaciones embellecen el resultado y las tarifas se desaceleran: son señales tempranas de soft market y de un ROE de pico.
6. **¿Qué breakevens dio el Dallas Fed y qué implican con WTI en US$92.75?** Pozo nuevo en US$66 y pozos existentes en US$43. El margen de ~US$27 por barril incentiva perforar; la EIA ya proyecta un Brent de US$74 en 2027.
7. **¿Por qué el costo de 4.6¢/lb de Southern Copper no mide su competitividad?** Porque resta los créditos por plata y molibdeno. El costo antes de subproductos (228.8¢) es el que la ubica en la curva, y el neto se evapora si caen los subproductos.
8. **ANTAD reportó +1.7% en mismas tiendas en agosto de 2026. ¿Es crecimiento?** No. Con inflación de 3.42%, el real es de ≈ −1.7%. En Walmex el tráfico cayó −1.1%.
9. **¿Qué tres datos de FIBRA Prologis indican un ciclo maduro?** Ocupación de 95.8% (antes 97.7%), retención de 60.8% (86.0%) y spread de renta de 40.8% (68.0%). Todo cae a la vez, aunque el NOI siga creciendo por el mark-to-market.
10. **Da el capex de 12 meses de los cuatro hyperscalers y su relación con el flujo operativo.** US$510.7 mil M, 77.3% del flujo operativo de US$660.3 mil M. El capex del 2T26 creció +87% a/a.
11. **¿Por qué no se usa la utilidad neta de Alphabet del 2T26?** Porque incluye US$99.0 mil M de ganancias en valores de capital. Se usa la utilidad operativa y el FCF.
12. **Calcula el book-to-bill de GE Vernova en el 2T26 y di qué riesgo implica.** US$24.2 mil M / 11.1 = ~2.2x. Crecimiento visible, pero concentrado en generación para centros de datos: riesgo de cancelación si el capex de IA se frena.
13. **ASUR reportó ingresos +9.9% en el 2T26. ¿Cuál es el dato correcto y cuál el KPI que preocupa?** Sin construcción (IFRIC 12), −0.3%. Preocupan el pasajero internacional de Cancún (−15.0% en agosto) y el margen EBITDA ajustado (62.0% contra 67.6%).
14. **Lilly: EUA con volumen +37% y precio −3%; fuera de EUA con volumen +113% y precio −36%. ¿Qué implica?** El crecimiento viene del volumen, con erosión de precio por MFN y la NRDL de China. El KPI a vigilar es el precio neto trimestral.
15. **¿Por qué la rotación sectorial por fase del ciclo es grado D?** Exige fechar el ciclo en tiempo real, el mercado se adelanta, y la evidencia (Jacobsen-Stangl-Visaltanachoti) muestra ganancias pequeñas que los costos se comen. En la arena, cada vuelta cuesta ~0.58% más spread.

---

## 9. Fuentes

1. Damodaran, EV/EBITDA por industria (enero de 2026): https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/vebitda.html
2. Damodaran, P/U por industria (enero de 2026): https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/pedata.html
3. Damodaran, P/VL, ROE y ROIC por industria (enero de 2026): https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/pbvdata.html
4. Damodaran, márgenes por industria (enero de 2026): https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/margin.html
5. Damodaran, costo de capital por industria (enero de 2026): https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/wacc.html
6. WSTS, pronóstico de primavera de 2026: https://www.wsts.org/76/Recent-News-Release
7. SIA, ventas globales de julio de 2026 (4-sep-2026): https://www.semiconductors.org/news-events/latest-news/
8. TrendForce, precios contrato del 3T26 (3-jul-2026): https://www.trendforce.com/presscenter/news/20260703-13134.html
9. Micron, comunicado del 3T FY26 (24-jun-2026): https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000013/a2026q3ex991-pressrelease.htm · ficha interna `empresas/MU/ficha.md`
10. NVIDIA, comunicado del 2T FY27 (26-ago-2026): https://www.sec.gov/Archives/edgar/data/1045810/000104581026000073/q2fy27pr.htm · ficha interna `empresas/NVDA/ficha.md`
11. SEC EDGAR XBRL companyfacts (MSFT, GOOGL, AMZN, META, ORCL, NVDA, MU, AMAT, LRCX, KLAC, CRM, NOW, ADBE, WDAY, SNOW, DDOG, CRWD, TSLA, GM, F, DUK, T, TRV, PGR), vía `herramientas/edgar.py`, 25-sep-2026: https://data.sec.gov/api/xbrl/companyfacts/
12. Meta, comunicado del 2T26 (29-jul-2026): https://www.sec.gov/Archives/edgar/data/1326801/000162828026050596/meta-06302026xexhibit991.htm
13. Alphabet, comunicado del 2T26 (22-jul-2026): https://www.sec.gov/Archives/edgar/data/1652044/000165204426000066/googexhibit991q22026.htm
14. Amazon, comunicado del 2T26 (30-jul-2026): https://www.sec.gov/Archives/edgar/data/1018724/000101872426000024/amzn-20260630xex991.htm
15. Oracle, comunicado del 1T FY27 (10-sep-2026): https://www.sec.gov/Archives/edgar/data/1341439/000119312526387905/orcl-ex99_1.htm · ficha interna `empresas/ORCL/ficha.md`
16. Microsoft, vida útil y capex (CFO Dive, 30-jul-2026; vía ficha interna, no re-verificado): https://www.cfodive.com/news/microsoft-holds-line-ai-spending-plans/826648/
17. Bessemer Venture Partners, "The Rule of X" (2-ene-2024): https://www.bvp.com/atlas/the-rule-of-x
18. Bloomberg, "SaaSpocalypse" (4-feb-2026; vía cap. 17): https://www.bloomberg.com/news/articles/2026-02-04/what-s-behind-the-saaspocalypse-plunge-in-software-stocks
19. FDIC, Quarterly Banking Profile del 2T26 (comunicado): https://www.fdic.gov/news/press-releases/2026/fdic-insured-institutions-reported-return-assets-137-percent-and-net
20. Banorte, resultados del 2T26: https://investors.banorte.com/~/media/Files/B/Banorte-IR/financial-information/quarterly-results/en/2026/2Q26/2Q26__.pdf · ficha interna `empresas/GFNORTEO.MX/ficha.md`
21. Micron IR, fecha del reporte del 4T FY26 (30-sep-2026; vía ficha interna): https://investors.micron.com/news/press-release/2026/Micron-Technology-to-Report-Fiscal-Fourth-Quarter-Results-on-September-30-2026/default.aspx
22. Travelers, comunicado del 2T26 (17-jul-2026): https://www.sec.gov/Archives/edgar/data/86312/000008631226000143/a991pressrelease63026.htm
23. Progressive, resultados de agosto de 2026 (18-sep-2026): https://www.sec.gov/Archives/edgar/data/80661/000008066126000322/pgr202608ex99earningsrelea.htm
24. Federal Reserve Bank of Dallas, Energy Survey del 1T26: https://www.dallasfed.org/research/surveys/des/2026/2601
25. EIA, Short-Term Energy Outlook (9-sep-2026): https://www.eia.gov/outlooks/steo/
26. Chevron, 8-K del 2T26 (31-jul-2026): https://www.sec.gov/Archives/edgar/data/93410/000009341026000162/a06302026ex9918-k.htm · ficha interna `empresas/CVX/ficha.md`
27. Southern Copper, resultados del 2T26 (21-jul-2026): https://www.sec.gov/Archives/edgar/data/1001838/000110465926085515/scco-20260721xex99d1.htm
28. Peñoles, Informe del Director del 2T26: https://www.penoles.com.mx/assets/files/reportes/BMV/informe/Informe_Director_2T26.pdf · ficha interna
29. ANTAD, ventas de agosto de 2026: https://antad.net/cadenas-asociadas-a-la-antad-ventas-de-agosto-2026/
30. Walmex, comunicado del 2T26: https://files.walmex.mx/upload/files/2026/EN/Quarterly/2Q26/Walmex%202Q26%20Earnings%20Release.pdf · ficha interna
31. FEMSA, 6-K de resultados del 2T26: https://www.sec.gov/Archives/edgar/data/1061736/000110465926087338/tm2621462d1_ex99-1.htm · ficha interna
32. FIBRA Prologis, resultados del 2T26 (23-jul-2026): https://d1io3yog0oux5.cloudfront.net/_dc193eb9ea2d5eb01f7d9741cddfa2f2/fibraprologis/news/2026-07-23_FIBRA_Prologis_Announces_Second_Quarter_2026_752.pdf
33. Vesta, 6-K de resultados del 2T26: https://www.sec.gov/Archives/edgar/data/1969373/000196937326000016/quarterlyreport2q2026ex-991.htm · ficha interna
34. Eli Lilly, comunicado del 2T26 (5-ago-2026): https://www.sec.gov/Archives/edgar/data/59478/000005947826000077/q226lillysalesandearningsp.htm
35. Johnson & Johnson, comunicado del 2T26: https://www.sec.gov/Archives/edgar/data/200406/000020040626000146/a2026q2exhibit991.htm · ficha interna
36. GE Vernova, comunicado del 2T26 (22-jul-2026): https://www.sec.gov/Archives/edgar/data/1996810/000199681026000147/gevpressrelease2q26.htm
37. Caterpillar, 8-K del 2T26: https://www.sec.gov/Archives/edgar/data/18230/000001823026000040/ex991toformcat2q2026earnin.htm · ficha interna
38. América Móvil, reporte del 2T26: https://s22.q4cdn.com/604986553/files/doc_financials/2026/q2/2Q26.pdf · ficha interna
39. ASUR, tráfico de agosto de 2026 (6-K, 8-sep-2026): https://www.sec.gov/Archives/edgar/data/1123452/000110465926105933/tm2625009d1_ex99-1.htm · resultados del 2T26 (6-K, 23-jul-2026): https://www.sec.gov/Archives/edgar/data/1123452/000110465926086284/tm2621230d1_ex99-1.htm
40. GAP, tráfico de agosto de 2026 (6-K): https://www.sec.gov/Archives/edgar/data/1347557/000117184326005899/f6k_090426.htm
41. OMA, tráfico de agosto de 2026 (6-K): https://www.sec.gov/Archives/edgar/data/1378239/000199937126019999/oma-6k_090726.htm
42. Precios y rendimientos de emisoras mexicanas: ver [53]
43. Cemex, resultados del 2T26 (6-K, 23-jul-2026): https://www.sec.gov/Archives/edgar/data/1076378/000119312526313194/d46310dex1.htm · https://www.sec.gov/Archives/edgar/data/1076378/000119312526313194/d46310dex2.htm
44. GCC, resultados del 2T26: https://cdn.investorcloud.net/gcc/InformacionFinanciera/InformacionTrimestral/GCC-2T2026-en.pdf · ficha interna
45. Greenwood, Hanson, "Waves in Ship Prices and Investment", QJE 130(1):55-109 (2015); NBER w19246: https://www.nber.org/papers/w19246
46. Moskowitz, Grinblatt, "Do Industries Explain Momentum?", JF (1999): https://doi.org/10.1111/0022-1082.00146
47. Hong, Torous, Valkanov, "Do Industries Lead Stock Markets?", JFE (2007): https://doi.org/10.1016/j.jfineco.2005.09.010
48. Cohen, Frazzini, "Economic Links and Predictable Returns", JF (2008): https://www.aqr.com/Insights/Research/Journal-Article/Economic-Links-and-Predictable-Returns · https://doi.org/10.1111/j.1540-6261.2008.01379.x
49. Chancellor (ed.), *Capital Returns* (Palgrave Macmillan, 2016): https://doi.org/10.1007/978-1-137-57165-6
50. Cooper, Gulen, Schill, "Asset Growth and the Cross-Section of Stock Returns" (SSRN; JF 2008): https://doi.org/10.2139/ssrn.760967
51. Jacobsen, Stangl, Visaltanachoti, "Sector Rotation across the Business Cycle" (SSRN 1467457): https://doi.org/10.2139/ssrn.1467457
52. Porter, "The Five Competitive Forces That Shape Strategy", HBR (ene-2008): https://hbr.org/2008/01/the-five-competitive-forces-that-shape-strategy
53. Yahoo Finance chart v8 (cierres ajustados; cálculo propio del 25-sep-2026 vía `herramientas/datos.py`): https://query1.finance.yahoo.com/v8/finance/chart/
54. Capítulos internos: 16 (Banxico, inflación, IED, T-MEC), 17 (SaaSpocalypse), 24 (MFN, 232, OBBBA) y 25 (capex/D&A).
