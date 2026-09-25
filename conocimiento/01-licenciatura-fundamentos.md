# Módulo 01 — Fundamentos de finanzas e inversión: la matemática del compuesto y los hechos duros del mercado

> Nivel: licenciatura · Actualizado: 2026-09-25 · Grado de evidencia global: **A** — el núcleo son identidades matemáticas (valor del dinero en el tiempo, volatility drag, recuperación de drawdowns) y hechos empíricos replicados en 35 mercados y más de 125 años (prima de renta variable en portafolios diversificados, asimetría extrema de las acciones individuales, costos que destruyen rendimiento). Lo disputado (magnitud futura de la prima, señales contables publicadas) se marca C en su lugar.

---

## 1. Objetivos de dominio (qué debe saber hacer quien "se titula" en este módulo)

Quien apruebe este módulo debe poder, sin ayuda y con números:

1. Valuar cualquier flujo: VP, VF, anualidades (vencidas y anticipadas), perpetuidades (constantes y crecientes), VPN y TIR, y detectar cuándo la TIR engaña (múltiples TIR, escala, supuesto de reinversión).
2. Convertir entre tasa nominal, efectiva, continua y real; calcular el precio y el rendimiento efectivo de un CETE (convención de 360 días).
3. Leer los tres estados financieros y calcular liquidez, apalancamiento, cobertura, ROE, ROIC, la descomposición DuPont y el flujo libre (FCFF y FCFE); saber cuándo cada ratio miente.
4. Explicar la mecánica de acciones, bonos (precio-rendimiento, duración, convexidad), fondos y ETFs; los tipos de orden; bid-ask, profundidad e impacto; la custodia y la liquidación (T+1 en EUA, México y Canadá desde mayo de 2024).
5. Calcular media, varianza, covarianza, correlación y varianza de portafolio; separar el rendimiento aritmético del geométrico y cuantificar el volatility drag.
6. Explicar por qué los rendimientos tienen colas gruesas y por qué las correlaciones suben en las caídas, y qué implica eso para stops, VaR y dimensionamiento.
7. Citar con cifras exactas la evidencia de largo plazo (Dimson-Marsh-Staunton 2026, Siegel, Bessembinder 2018, 2023 y 2026, Anarkulova-Cederburg-O'Doherty 2022, McQuarrie 2024).
8. Medir todo en MXN, netear costos e impuestos, y compararlo contra el benchmark del sistema (50% S&P 500 TR en MXN + 50% CETES 28).
9. Aplicar la matemática del compuesto a las reglas de riesgo de `config/parametros.json`: cortacircuitos, rachas, Kelly fraccional y bandas de rebalanceo.

---

## 2. Núcleo teórico

### 2.1 Valor del dinero en el tiempo

**Valor futuro y presente (tasa por periodo *r*, *n* periodos):**
- VF = VP · (1 + r)^n ; VP = VF / (1 + r)^n

**Anualidad vencida (pago *C* al final de cada periodo):**
- VP = C · [1 − (1 + r)^(−n)] / r ; VF = C · [(1 + r)^n − 1] / r
- Anualidad anticipada: multiplicar por (1 + r).
- Ejemplo: $10,000 MXN mensuales durante 20 años al 8% nominal anual capitalizable mensualmente (r = 0.667%, n = 240) acumulan VF ≈ **$5.89 millones**, contra $2.4 millones aportados. La diferencia es puro compuesto.

**Perpetuidades:**
- Constante: VP = C / r
- Creciente a tasa g < r: VP = C₁ / (r − g). Es el modelo de Gordon: P₀ = D₁ / (r − g). Con D₁ = 5, r = 9% y g = 4%, P₀ = 100. Si g sube a 5%, P₀ = 125 (+25%). **Intuición económica:** el precio de un activo de larga duración es hipersensible a (r − g). De ahí la volatilidad de las acciones de "crecimiento" ante cambios en tasas.

**VPN y TIR:**
- VPN = Σ CF_t / (1 + r)^t. Regla: se acepta si VPN > 0 al costo de capital correcto.
- La TIR resuelve VPN = 0. Ejemplo: flujos (−1000, 300, 400, 500): VPN al 10% = −21.0; TIR = 8.90%.
- Fallas de la TIR: (i) con flujos que cambian de signo más de una vez puede haber varias TIR o ninguna; (ii) no mide escala (una TIR de 50% sobre $1,000 vale menos que una de 15% sobre $10 millones); (iii) supone implícitamente reinversión a la propia TIR. **Para decidir entre proyectos o estrategias manda el VPN; la TIR solo sirve como resumen.** La MIRR corrige (iii) porque reinvierte al costo de capital.

**Tasas nominal, efectiva, continua y real:**
- Efectiva anual: EAR = (1 + APR/m)^m − 1. 12% capitalizable mensual → 12.68%; continua → e^0.12 − 1 = 12.75%.
- Continua: VF = VP · e^(rT); tasa continua equivalente = ln(1 + r_efectiva).
- **Fisher (exacta):** (1 + i) = (1 + r_real)(1 + π) → r_real = (1 + i)/(1 + π) − 1. Con 10% nominal y 4% de inflación, la tasa real es 5.77%, no 6%.
- Regla del 72: el tiempo para duplicar es ≈ 72/r(%). La versión exacta es ln 2 / ln(1 + r). Al 6.6% real (acciones de EUA desde 1900, ver §3) el poder de compra se duplica cada 10.8 años.

**CETES (México), convención de 360 días:**
- Precio = VN / (1 + r · d/360). Con r = 6.15% y d = 28 días (tasa de la subasta del 22-sep-2026, según fuente secundaria [34]), por cada $10 de valor nominal se pagan $9.9524.
- Rendimiento del periodo: 6.15% × 28/360 = 0.4783%. Si se reinvierte, la tasa efectiva anual es (1.004783)^(365/28) − 1 = **6.42%**. Comparar una tasa de CETES "de subasta" contra una tasa efectiva de otro instrumento sin convertirla es un error de principiante.

### 2.2 Estados financieros y ratios

Los tres estados: **resultados** (devengado: ingresos − costos = utilidad), **balance** (activos = pasivos + capital) y **flujo de efectivo** (operación, inversión y financiamiento). La utilidad es una opinión contable y el efectivo es un hecho. Cuando divergen de forma persistente (utilidad alta, flujo de operación bajo), la calidad de las utilidades es baja.

| Familia | Ratio | Fórmula | Lectura |
|---|---|---|---|
| Liquidez | Circulante | Activo circulante / Pasivo circulante | Cobertura de obligaciones de corto plazo |
| Liquidez | Prueba ácida | (AC − Inventarios) / PC | Sin depender de vender inventario |
| Apalancamiento | Deuda neta / EBITDA | (Deuda − Caja) / EBITDA | Años de EBITDA para pagar la deuda |
| Apalancamiento | D/E | Deuda / Capital contable | Riesgo financiero; amplifica ROE |
| Cobertura | Intereses | EBIT / Gasto por intereses | Holgura antes de impago |
| Rentabilidad | ROA | Utilidad neta / Activos | Eficiencia total |
| Rentabilidad | ROE | Utilidad neta / Capital | Rendimiento al accionista (contaminado por apalancamiento) |
| Rentabilidad | ROIC | NOPAT / Capital invertido; NOPAT = EBIT(1 − t) | Rendimiento del negocio operativo, sin importar cómo se financia |
| Eficiencia | Rotación de activos | Ventas / Activos | Intensidad de capital |
| Eficiencia | Ciclo de conversión de efectivo | Días inventario + Días cobro − Días pago | Capital de trabajo atrapado |
| Flujo | FCFF | EBIT(1 − t) + D&A − Capex − ΔCTN | Efectivo para todos los proveedores de capital |
| Flujo | FCFE | FCFF − Intereses(1 − t) + Endeudamiento neto | Efectivo disponible para el accionista |

**DuPont:**
- 3 factores: ROE = (UN/Ventas) × (Ventas/Activos) × (Activos/Capital) = margen × rotación × apalancamiento.
- 5 factores: ROE = (UN/UAI) × (UAI/EBIT) × (EBIT/Ventas) × (Ventas/Activos) × (Activos/Capital), es decir, carga fiscal × carga de intereses × margen operativo × rotación × multiplicador.
- **Regla de oro:** un ROE alto que viene del multiplicador de capital (apalancamiento o recompras que reducen el capital contable) no es un ROE de calidad. Hay que mirar el ROIC.
- Creación de valor: una empresa crea valor solo si ROIC > WACC. Crecer con ROIC < WACC destruye valor aunque la utilidad suba.

**Evidencia académica sobre ratios:**
- Nissim y Penman (2001) formalizan el análisis de ratios como pronóstico de pagos futuros al accionista, separando lo operativo de lo financiero [20].
- Soliman (2008) muestra que los componentes DuPont (sobre todo el cambio en rotación de activos) predicen utilidades futuras y que el mercado y los analistas reaccionan de forma incompleta [21].
- Altman (1968) construye el Z-score con 66 manufactureras (la mitad en quiebra) para predecir la quiebra a dos años [18].
- Piotroski (2000), con 9 señales contables binarias (F-score) dentro de acciones de alto book-to-market, reporta que seleccionar a las financieramente fuertes sube el rendimiento medio al menos 7.5% anual, y que comprar ganadoras y vender perdedoras esperadas dio 23% anual en 1976-1996. Es **in-sample y previo a la publicación** [19].
- Novy-Marx (2013): la utilidad bruta sobre activos tiene aproximadamente el mismo poder que el book-to-market para explicar la sección cruzada de rendimientos [22].

### 2.3 Instrumentos, mercados y microestructura

**Acciones:** son un derecho residual con responsabilidad limitada. La pérdida máxima es −100% y la ganancia no tiene techo. Esa asimetría es la raíz de la asimetría positiva documentada por Bessembinder (§3 y §5).

**Bonos:** P = Σ C/(1 + y)^t + F/(1 + y)^T.
- Duración de Macaulay: D = Σ t · VP(CF_t) / P. Duración modificada: D* = D/(1 + y).
- ΔP/P ≈ −D* · Δy + ½ · Convexidad · (Δy)².
- Ejemplo: bono a 10 años, cupón de 8% y rendimiento de 9% → P = 93.58, D = 7.15, D* = 6.56. Si la tasa sube 100 pb, la duración estima −6.56% y el cambio real es −6.27%. La diferencia es la convexidad, que juega a favor del tenedor.
- En México: CETES (cupón cero, descuento), Bonos M (tasa fija), Udibonos (indexados a UDIS, es decir, reales) y deuda corporativa.
- Riesgos: tasa, crédito (spread), liquidez, inflación y, para el inversionista en MXN, tipo de cambio si el bono está en USD.

**Fondos y ETFs:** un fondo abierto (en México, fondos de inversión) se valúa al NAV del día. Un ETF cotiza intradía y su precio se ancla al NAV mediante creación y redención por participantes autorizados. Lo que importa: TER (expense ratio), tracking difference (lo que realmente pierdes contra el índice, no solo el TER), spread de compraventa y liquidez del subyacente. Costo promedio ponderado por activos que pagaron los inversionistas de fondos en EUA: **0.32% en 2025** (0.34% en 2024 y 0.80% hace dos décadas; Morningstar 2026) [25].

**Tipos de orden:**

| Orden | Qué garantiza | Qué no garantiza | Uso correcto |
|---|---|---|---|
| Mercado | Ejecución | Precio | Solo en activos muy líquidos, en tamaño pequeño y fuera de la apertura y el cierre |
| Límite | Precio máximo o mínimo | Ejecución | Predeterminada para el sistema |
| Stop (a mercado) | Se dispara al tocar el precio | Precio de salida (gaps) | Salida de emergencia; la pérdida real puede exceder la planeada |
| Stop-límite | Precio mínimo de salida | Salida (puede quedar sin ejecutar en un desplome) | Cuando el deslizamiento es peor que no salir |
| MOC/LOC | Precio de cierre o límite en el cierre | — | Rebalanceos contra benchmarks de cierre |
| Vigencia: Day, GTC, IOC, FOK | Tiempo y parcialidad | — | IOC/FOK para evitar ejecuciones parciales indeseadas |

**Bid-ask y liquidez:**
- Spread cotizado = ask − bid. Spread efectivo = 2 · |P_ejecución − medio|. El costo de ida y vuelta de una orden a mercado es aproximadamente el spread efectivo, más el impacto si el tamaño consume la profundidad.
- "Comisión cero" no significa costo cero. Schwarz, Barber, Huang, Jorion y Odean (JF, 2025) enviaron unas 85,000 órdenes simultáneas idénticas por seis cuentas en cinco brokers (dic-2021 a jun-2022). El costo medio de ida y vuelta por cuenta fue de **0.07% a 0.46%**, sin comisiones, y el PFOF no explica la dispersión: los mayoristas dan precios distintos a distintos brokers [24].
- Cambio regulatorio en EUA: el 18-sep-2024 la SEC aprobó un tick de $0.005 para acciones de $1 o más con spread promedio ponderado por tiempo de 1.5 centavos o menos, y bajó el tope de access fee de 30 a 10 mils. La Corte de Apelaciones del Circuito de D.C. confirmó la regla el 14-oct-2025. La fecha de cumplimiento se prorrogó por exención al **primer día hábil de noviembre de 2026** [30][31].

**Custodia y liquidación:**
- EUA pasó de T+2 a **T+1 el 28-may-2024**. **México y Canadá lo hicieron el 27-may-2024**, porque el 27 fue feriado solo en EUA (Memorial Day) [27][28].
- La UE y el Reino Unido planean T+1 para el **11-oct-2027** [29].
- Custodio central en México: Indeval. En EUA: DTC.
- Implicación operativa: la conversión MXN/USD y la disponibilidad de fondos deben alinearse con T+1. Vender y recomprar con fondos no liquidados puede violar reglas de cuenta de efectivo.

### 2.4 Riesgo y rendimiento

**Rendimientos:** simple R = P₁/P₀ − 1 (se agrega entre activos) y logarítmico r = ln(1 + R) (se agrega en el tiempo).

**Media aritmética vs. geométrica:**
- Aritmética A = (1/T) Σ R_t: es el mejor estimador del rendimiento esperado de un periodo.
- Geométrica G = [Π(1 + R_t)]^(1/T) − 1: es lo que realmente compone tu riqueza.
- Aproximación: **G ≈ A − σ²/2**. Esa diferencia es el **volatility drag**.
- Ejemplo: +50% y luego −50% da A = 0% y G = −13.4%.
- Drag anual: σ = 16% → 1.28 pp; σ = 20% → 2.0 pp; σ = 40% → 8.0 pp.
- **Consecuencia para un sistema cuyo objetivo es el CAGR:** reducir volatilidad sin reducir la media aumenta el crecimiento. Es la base matemática de la diversificación y del rebalanceo.
- Para proyectar riqueza terminal, compuestar a la media aritmética histórica sesga el pronóstico hacia arriba. Jacquier, Kane y Marcus (2003) muestran que el estimador insesgado es un promedio ponderado entre la media aritmética y la geométrica, y que el peso de la geométrica crece con el horizonte relativo al tamaño de la muestra [15].

**Apalancamiento y crecimiento:**
- Con exposición L a un activo de exceso esperado μ y volatilidad σ: g(L) ≈ r_f + L·μ − L²·σ²/2.
- El crecimiento se maximiza en L* = μ/σ² (Kelly continuo; Kelly 1956 [16]) y cae a r_f en 2L*.
- Con fracción k de Kelly se obtiene (2k − k²) del crecimiento excedente máximo. Con k = 0.25 (el tope de `parametros.json`) se logra **43.75% del crecimiento máximo con 25% de la volatilidad** del Kelly completo.
- Los ETFs apalancados diarios sufren este drag de forma mecánica.

**Varianza de portafolio:**
- σ_p² = Σ_i Σ_j w_i w_j σ_ij = wᵀΣw. Correlación ρ_ij = σ_ij/(σ_i σ_j).
- Con N activos igualmente ponderados: σ_p² = σ̄²/N + (1 − 1/N)·cov̄. El primer término (riesgo idiosincrático) se diversifica; el segundo (riesgo sistemático) no.
- Ejemplo (Inferencia, parámetros ilustrativos: σ = 30% y ρ = 0.25): 1 acción → 30%; 10 → 17.1%; 30 → 15.7%; 50 → 15.4%; límite → 15%.
- Statman (1987) calculó 30 acciones (inversionista que se endeuda) y 40 (inversionista que presta) [11].
- Campbell, Lettau, Malkiel y Xu (2001) documentan que la volatilidad idiosincrática subió de 1962 a 1997. En 1986-1997 se necesitaban **cerca de 50 acciones** para lograr lo que 20 lograban antes [12]. Su revisión de 2023 muestra que esa volatilidad bajó después de 2000 y repuntó en 2008-09 y 2020-21 [13].

**Sharpe:** S = (R_p − R_f)/σ_p. Para este sistema, R_f es CETES 28 (MXN).

**Colas gruesas y dependencia en crisis:**
- Mandelbrot (1963) documenta colas mucho más gruesas que la normal en precios especulativos [9].
- Cont (2001) sistematiza los "hechos estilizados": colas pesadas, agrupamiento de volatilidad, asimetría de ganancias y pérdidas y colas que se adelgazan al agregar horizontes [10].
- El 19-oct-1987 el S&P 500 cayó **20.47%** y el Dow **22.6%** en un día [32]. Inferencia: con volatilidad diaria del orden de 1%, eso es un evento de unas 20 desviaciones estándar, con probabilidad ~3×10⁻⁸⁹ bajo normalidad. Los modelos gaussianos no sirven para dimensionar pérdidas extremas.
- Longin y Solnik (2001): la correlación entre mercados accionarios internacionales **aumenta en mercados bajistas extremos**; se rechaza la normalidad en la cola negativa, pero no en la positiva [14]. La diversificación funciona peor justo cuando más se necesita.

**Asimetría por compuesto:**
- Farago y Hjalmarsson (2023, Review of Finance) muestran que el compuesto multiplicativo induce asimetría positiva fuerte en horizontes largos, y que su magnitud depende sobre todo de la volatilidad de corto plazo. La media del rendimiento compuesto es mala guía del resultado típico [17].
- Es la mecánica que explica a Bessembinder: media alta, mediana pobre.

**Aritmética del drawdown:** una pérdida L exige una ganancia L/(1 − L) para recuperarse.

| Drawdown | Ganancia necesaria para recuperar |
|---|---|
| −8% | +8.7% |
| −12% | +13.6% |
| −15% | +17.6% |
| −20% | +25.0% |
| −50% | +100% |

### 2.5 Inflación, moneda e interés compuesto en MXN

- Rendimiento real = (1 + nominal)/(1 + inflación) − 1.
- México hoy: Banxico mantuvo el objetivo en **6.50%** el 24-sep-2026 [35]. La inflación anual de la 1a quincena de septiembre de 2026 fue **3.42%** (subyacente 3.79%) [36]. Inferencia: CETES 28 al 6.15% implica un rendimiento real ex ante antes de impuestos de ≈ **2.6%**.
- Impuestos (MX, 2026):
  - Retención provisional de ISR sobre intereses de **0.90% anual sobre el capital** (0.50% en 2025; LIF 2026) [37]. El impuesto definitivo se calcula sobre el interés real en la declaración anual.
  - La ganancia en venta de acciones en bolsa concesionada paga **10%** (art. 129 LISR), calculada sobre la ganancia con costo actualizado por inflación [38].
- **Moneda:** R_MXN = (1 + R_USD)(1 + ΔUSDMXN) − 1. Ejemplo: S&P 500 +10% en USD con el peso apreciándose 5% da +4.5% en MXN.
  - El benchmark del sistema es R_b = 0.5·[(1 + R_SPX)(1 + Δs) − 1] + 0.5·R_CETES. En el ejemplo, con CETES al 6.5%: 5.5%.
  - DMS 2026: el riesgo cambiario añadió en promedio **~6 puntos porcentuales** a la volatilidad total, tanto en acciones como en bonos [1].
- **Las acciones no son cobertura de inflación de corto plazo:**
  - En los 8 regímenes inflacionarios de EUA desde 1926 (inflación anual acelerando y de 5% o más), las acciones rindieron ≈ **−7% real anualizado**, el bono a 10 años −5% y el 60/40 −6%. Las materias primas rindieron **+14%** real anualizado y fueron positivas en los 8 episodios (Neville, Draaisma, Funnell, Harvey y Van Hemert, 2021) [23][39].
  - El oro tuvo rendimiento negativo en **13 de los 28 años** con inflación de EUA arriba de 3%. Su rendimiento real anualizado desde 1900 es **1.3%** (DMS 2026) [1].

---

## 3. Literatura canónica

| Autores | Año | Título | Revista/Editorial | Hallazgo clave cuantificado | Enlace/DOI | Grado |
|---|---|---|---|---|---|---|
| Bodie, Kane, Marcus | 2024 | *Investments*, 13a ed. | McGraw Hill | Texto de referencia; alineado al currículo CFA; tesis central: mercados "casi eficientes" | ISBN 978-1-264-41266-2 | Texto |
| Brealey, Myers, Allen, Edmans | 2023 | *Principles of Corporate Finance*, 14a ed. | McGraw Hill | VPN, costo de capital y estructura de capital; Edmans se suma como coautor | ISBN 978-1-264-08094-6 | Texto |
| Berk, DeMarzo | 2023 | *Corporate Finance*, 6a ed. | Pearson | Marco unificado en la Ley de Un Precio | ISBN 978-0-13-784502-6 | Texto |
| Graham (comentarios de J. Zweig; intro de Buffett) | 2024 | *The Intelligent Investor*, 3a ed. revisada | HarperBusiness | Margen de seguridad; "Mr. Market"; texto original intacto con comentario nuevo | ISBN 978-0-06-335673-3 | Texto |
| Malkiel | 2023 | *A Random Walk Down Wall Street*, 13a ed. (50 aniversario) | W. W. Norton | Indexación diversificada de bajo costo; crítica de cripto, NFT y meme stocks | ISBN 978-1-324-05113-8 | Texto |
| Siegel | 2022 | *Stocks for the Long Run*, 6a ed. (datos a 2021) | McGraw Hill | Gráfica 1802-2023 (reales): acciones **6.8%**, bonos 3.3%, bills 2.5%, oro 0.6%, dólar −1.4% | CFA RF brief [7] | B (datos del s. XIX disputados) |
| Dimson, Marsh, Staunton | 2026 | *UBS Global Investment Returns Yearbook 2026* | UBS / LBS | EUA 1900-2025: acciones **9.8%** nominal y **6.6% real**; bonos 1.6% real; bills 0.5% real; inflación 2.9%. Acciones: mejor activo en los 21 países con historia continua | [1][2] | A |
| Bessembinder | 2018 | "Do stocks outperform Treasury bills?" | *JFE* 129(3):440-457 | Solo **42.6%** de las acciones de CRSP (1926-2016) supera a los T-bills en toda su vida; más de la mitad tiene rendimiento de vida negativo; resultado modal −100%; **1,092 empresas (~4%)** explican toda la creación neta de riqueza (~US$35 billones); 90 empresas, más de la mitad | doi:10.1016/j.jfineco.2018.06.004 [3] | A |
| Bessembinder, Chen, Choi, Wei | 2023 | "Long-Term Shareholder Returns: Evidence from 64,000 Global Stocks" | *FAJ* 79(3):33-63 | 1990-2020: **55.2%** (EUA) y **57.4%** (fuera de EUA) rinden menos que los T-bills a un mes; el **2.4%** de las firmas explica los **US$75.7 billones** de riqueza neta global | doi:10.1080/0015198X.2023.2188870 [4] | A |
| Anarkulova, Cederburg, O'Doherty | 2022 | "Stocks for the long run? Evidence from a broad sample of developed markets" | *JFE* 143(1):409-433 | 39 países desarrollados, 1841-2019: **12%** de probabilidad de perder contra la inflación en un horizonte de 30 años | doi:10.1016/j.jfineco.2021.06.040 [6] | A |
| McQuarrie | 2024 | "Stocks for the Long Run? Sometimes Yes, Sometimes No" | *FAJ* 80(1) | Con datos rehechos desde 1793: hay periodos multidecenales en que los bonos superan a las acciones; la prima de renta variable es por regímenes | doi:10.1080/0015198X.2023.2268556 [8] | B |
| Mandelbrot | 1963 | "The Variation of Certain Speculative Prices" | *J. of Business* 36:394-419 | Colas gruesas; propone distribuciones estables (Pareto-Lévy) | JSTOR 2350970 | A |
| Cont | 2001 | "Empirical properties of asset returns: stylized facts and statistical issues" | *Quantitative Finance* 1:223-236 | Colas pesadas, agrupamiento de volatilidad, asimetría ganancia-pérdida | doi:10.1080/713665670 | A |
| Statman | 1987 | "How Many Stocks Make a Diversified Portfolio?" | *JFQA* 22(3):353-363 | 30 acciones (inversionista que se endeuda) y 40 (que presta) | [11] | B |
| Campbell, Lettau, Malkiel, Xu | 2001 | "Have Individual Stocks Become More Volatile?" | *JF* 56(1):1-43 | La volatilidad idiosincrática sube de 1962 a 1997; ~50 acciones en 1986-97 contra 20 antes | doi:10.1111/0022-1082.00318 | B |
| Longin, Solnik | 2001 | "Extreme Correlation of International Equity Markets" | *JF* 56(2):649-676 | La correlación sube en mercados bajistas; se rechaza la normalidad en la cola negativa | doi:10.1111/0022-1082.00340 | A |
| Barber, Odean | 2000 | "Trading Is Hazardous to Your Wealth" | *JF* 55(2):773-806 | 66,465 hogares, 1991-96: quienes más operan ganan **11.4%** contra 17.9% del mercado; rotación promedio de 75% al año | doi:10.1111/0022-1082.00226 | A |
| Altman | 1968 | "Financial Ratios, Discriminant Analysis and the Prediction of Corporate Bankruptcy" | *JF* 23(4):589-609 | Z-score con 66 manufactureras; predicción de quiebra a 2 años | doi:10.1111/j.1540-6261.1968.tb00843.x | B |
| Piotroski | 2000 | "Value Investing: The Use of Historical Financial Statement Information…" | *JAR* 38:1-41 | +7.5% anual al filtrar alto B/M por solidez; long/short **23% anual** en 1976-96 (in-sample) | [19] | C (post-publicación) |
| Nissim, Penman | 2001 | "Ratio Analysis and Equity Valuation" | *RAS* 6:109-154 | Marco de ratios operativos vs. financieros para pronosticar pagos | doi:10.1023/A:1011338221623 | B |
| Soliman | 2008 | "The Use of DuPont Analysis by Market Participants" | *TAR* 83(3):823-853 | El cambio en rotación de activos predice utilidades y retornos anormales futuros | [21] | B/C |
| Novy-Marx | 2013 | "The other side of value: The gross profitability premium" | *JFE* 108(1):1-28 | La utilidad bruta sobre activos predice rendimientos con fuerza similar a B/M | doi:10.1016/j.jfineco.2013.01.003 | B |
| Jacquier, Kane, Marcus | 2003 | "Geometric or Arithmetic Mean: A Reconsideration" | *FAJ* 59(6) | Compuestar a la media aritmética sesga al alza el pronóstico de riqueza terminal | doi:10.2469/faj.v59.n6.2574 | A (matemático) |
| Kelly | 1956 | "A New Interpretation of Information Rate" | *Bell System Tech. J.* 35(4):917-926 | Tasa máxima de crecimiento exponencial del capital | doi:10.1002/j.1538-7305.1956.tb03809.x | A (matemático) |
| McLean, Pontiff | 2016 | "Does Academic Research Destroy Stock Return Predictability?" | *JF* 71(1):5-32 | 97 anomalías: rendimiento **26% menor fuera de muestra** y **58% menor tras la publicación** | doi:10.1111/jofi.12365 | A |
| Neville, Draaisma, Funnell, Harvey, Van Hemert | 2021 | "The Best Strategies for Inflationary Times" | *JPM* 47(8) | 8 regímenes inflacionarios en EUA: acciones ≈ −7% real anualizado, materias primas +14%; momentum 8% contra 4% en tiempos normales | [23][39] | B |

(DOIs confirmados por búsqueda en las páginas de la revista, RePEc o ResearchGate durante la verificación.)

---

## 4. Lo más reciente 2023-2026

| Fecha | Hallazgo o dato | Relevancia |
|---|---|---|
| 18-mar-2026 | **Bessembinder, "One Hundred Years in the U.S. Stock Markets"** (SSRN 6438198): 29,754 acciones, 1926-2025. Riqueza creada: **US$91 billones**. Casi **60%** de las acciones redujo la riqueza de sus tenedores de largo plazo. Rendimiento buy-and-hold **medio >30,000%** y **mediano −6.9%**. Solo **46 empresas** explican la mitad de los US$91 billones; en 2016 se necesitaban 90. Mercado ponderado por valor: **10.1% anual** (1,504,057% acumulado) [5][40] | La concentración de la creación de riqueza se aceleró. Elegir acciones al azar o con poca diversificación tiene mediana negativa |
| 3-mar-2026 | **UBS Global Investment Returns Yearbook 2026** (DMS): 35 mercados, 126 años. EUA pesa **62%** del mercado accionario mundial. La concentración del mercado de EUA a fines de 2025 es la **más alta en al menos 100 años**. Acciones y bonos han perdido más de 70% real en varias ocasiones, pero un 60:40 **nunca cayó más de 50%**. Mercados desarrollados 8.5% anual contra emergentes 6.9% (1900-2025; 1960-2025: emergentes 10.9% contra desarrollados 9.6%). Con cobertura cambiaria, invertir global en vez de doméstico mejoró el Sharpe en la gran mayoría de los 32 mercados (1974-2025). 22% de las combinaciones país-década tuvieron prima de factor negativa [1] | Evidencia base del núcleo del sistema: diversificación global, 60/40 como ancla de drawdown |
| 2025 (WP; premio ICPM 2025) | **Anarkulova, Cederburg, O'Doherty, "Beyond the Status Quo"**: 39 países, 1890-2023. 50% acciones domésticas + 50% internacionales toda la vida supera a las estrategias de ciclo de vida acciones/bonos en riqueza, consumo, preservación de capital y herencia [41] | Disputa la regla "más bonos con la edad". No es aplicable directamente con drawdown duro de 20% (ver §6) |
| oct-2025 | **Schwarz et al., JF 80(5):2507-2541**: costo de ida y vuelta de 0.07% a 0.46% según el broker, sin relación con el PFOF [24] | Elegir broker es una decisión de alfa |
| 14-oct-2025 | La Corte del Circuito de D.C. confirma la regla de tick de $0.005 y el tope de access fee de 10 mils; cumplimiento prorrogado a nov-2026 [30][31] | Spreads más finos en acciones muy líquidas de EUA |
| 2026 | **Morningstar US Fund Fee Study**: costo promedio ponderado por activos de **0.32%** en 2025 (−5.6% contra 2024) [25] | Referencia de costos para el núcleo |
| 2026 | **SPIVA EUA cierre 2025**: **79%** de los fondos activos large-cap perdió contra el S&P 500 en 2025 (el S&P 500 subió 18%). A 20 años, 93% (según resumen de TKer) [26][42] | La gestión activa promedio pierde neto de costos |
| 2026 | **SPIVA Latinoamérica cierre 2025, México**: el S&P/BMV IRT subió **35.2%** en 2025. Fondos activos de acciones mexicanas que perdieron contra el índice: **75.6%** a 1 año, **69.8%** a 3, **77.3%** a 5 y **75.6%** a 10. Rezago mediano: 3.0% en 2025 y 3.1% anual a 10 años [43] | En México también pierde la mayoría de los gestores activos |
| 2024 | **McQuarrie, FAJ 80(1)** + brief del CFA Research Foundation (McCaffrey, prólogo de L. Siegel): la gráfica de Siegel extendida a 2023 da acciones 6.8% real [7][8] | Los datos del s. XIX debilitan la tesis "siempre acciones" |
| 2023 | **Bessembinder, Cooper, Zhang, JFE 147:132-158**: pérdida agregada de riqueza de **US$1.02 billones** para inversionistas en fondos mutuos a 30 años contra el SPY ajustado por beta. El % de fondos que supera al SPY cae conforme se alarga el horizonte de medición [44] | El alfa mensual positivo puede convivir con riqueza destruida a largo plazo |
| 2023 | **Farago y Hjalmarsson, RoF 27(2):495-538**: asimetría positiva extrema de largo plazo inducida por el compuesto [17] | Media ≠ resultado típico |
| 2023 | **Campbell, Lettau, Malkiel, Xu, Critical Finance Review 12:203-223**: la volatilidad idiosincrática bajó después de 2000 con picos en 2008-09 y 2020-21 [13] | El número de acciones "suficientes" varía con el régimen |
| 27/28-may-2024 | T+1 en México y Canadá (27) y en EUA (28). UE y Reino Unido: 11-oct-2027 [27][28][29] | Liquidación y fondeo |
| 2026 | México: retención de ISR sobre intereses de 0.90% sobre capital [37]. Banxico en 6.50% (24-sep-2026) [35]. Inflación de 3.42% (1a quincena de sep-2026) [36] | Hurdle real en MXN |

---

## 5. Evidencia real: qué funciona, qué no, magnitudes netas y decaimiento

| Afirmación | Evidencia (muestra; in/out-of-sample) | Magnitud | Grado |
|---|---|---|---|
| La renta variable diversificada supera a bills y bonos a largo plazo | DMS: 21 países con historia continua, 1900-2025. Out-of-sample respecto de estudios previos (Ibbotson-Sinquefield y Siegel, centrados en EUA) | EUA: 6.6% real contra 0.5% (bills) → prima geométrica ≈ 6 pp/año. Pero ACO (2022): 12% de probabilidad de perder en términos reales a 30 años en 39 países | **A** en existencia. **B** en magnitud futura: EUA es el ganador ex post y pesa 62% del índice mundial |
| Elegir pocas acciones individuales es apostar contra la mediana | Bessembinder 2018 (EUA), 2023 (global, 64,000 acciones) y 2026 (100 años). Replicado dentro y fuera de EUA | 57.4% de las acciones no estadounidenses y 55.2% de las estadounidenses pierden contra T-bills (1990-2020). Una estrategia de 1 acción al azar perdió contra el mercado en **96%** de las simulaciones y contra T-bills en **73%** (1926-2016) | **A** |
| La gestión activa promedio pierde neto de costos | SPIVA (EUA, México, global); Bessembinder-Cooper-Zhang 2023 | EUA 2025: 79% pierde. México 10 años: 75.6% pierde, con rezago mediano de 3.1% anual | **A** |
| Los costos visibles e invisibles importan tanto como la selección | Morningstar 2026; Schwarz et al. 2025 | TER promedio de 0.32%. Dispersión de ejecución de 0.07% a 0.46% por ida y vuelta: con 20 viajes redondos al año sobre el capital completo, el costo va de 1.4% a 9.2% (diferencia de ~7.8 pp) (Inferencia) | **A** |
| Operar mucho destruye rendimiento | Barber-Odean 2000 (1991-96) | 11.4% contra 17.9% del mercado; hogar promedio 16.4% | **A** |
| La diversificación reduce riesgo, pero falla en las colas | Statman 1987; Campbell et al. 2001; Longin-Solnik 2001; DMS 2026 | 30-50 acciones para eliminar la mayor parte del riesgo idiosincrático; la correlación sube en caídas | **A** |
| La mezcla de acciones y bonos acota drawdowns | DMS 2026 | Acciones y bonos por separado cayeron más de 70% real en ocasiones; 60:40 nunca más de 50% | **A** (histórico) |
| Las acciones protegen de la inflación | Neville et al. 2021; DMS 2026 | −7% real anualizado en regímenes de inflación alta y creciente en EUA | **D** (falso en el corto plazo) |
| El oro protege de la inflación | DMS 2026; brief CFA 2024 | Negativo en 13 de 28 años con inflación >3%; 1.3% real anual desde 1900 | **C** |
| Las señales contables (F-score, DuPont, rentabilidad) dan alfa | Piotroski 2000 (in-sample 1976-96); Soliman 2008; Novy-Marx 2013 | 23% L/S in-sample. Decaimiento genérico post-publicación de −58% (McLean-Pontiff) | **B** (rentabilidad) / **C** (F-score como fuente de alfa hoy). Útiles como filtro de riesgo |
| La volatilidad resta crecimiento compuesto | Identidad matemática | G ≈ A − σ²/2 | **A** |

**Decaimiento post-publicación.** McLean y Pontiff (2016), con 97 predictores, estiman que los rendimientos caen **26% fuera de muestra** (sesgo estadístico) y **58% después de publicarse**. El 32% de diferencia se atribuye a que los inversionistas operan la anomalía una vez publicada [45]. Inferencia operable: cualquier ventaja tomada de un paper publicado entra al sistema con un recorte de al menos 50% de su rendimiento bruto in-sample antes de restar costos.

**Bruto vs. neto.** Casi todas las cifras académicas de §3 son brutas de costos e impuestos. Las de SPIVA y Bessembinder-Cooper-Zhang son netas de comisiones de fondos. Las de DMS y Siegel son índices sin costos. Inferencia: un inversionista mexicano que replica el S&P 500 vía ETF paga TER, spread, conversión cambiaria e impuestos. Su rendimiento en MXN será menor que el índice en USD incluso sin error de selección.

**EUA vs. global vs. México.**
- EUA es el caso ganador (6.6% real, 1900-2025).
- ACO (2022) con 39 países da una distribución más ancha y peor.
- Para México, la evidencia de gestores (SPIVA) coincide con EUA: la mayoría de los activos pierde.
- DMS incluye a México entre sus mercados, pero su resumen público no reporta el rendimiento real histórico mexicano: **no verificado aquí**.

---

## 6. Traducción operable (cómo lo usa el sistema para ganar dinero)

Todas las cifras de riesgo vienen de `config/parametros.json`. Este módulo no crea límites nuevos; donde propongo un criterio de selección lo marco como tal.

**R1. Función objetivo = crecimiento geométrico en MXN.**
- Toda estrategia se evalúa por su CAGR neto en MXN (después de TER, spread, comisión, conversión cambiaria e impuestos), no por su media aritmética.
- Prueba mínima: g_neto ≈ μ_neto − σ²/2 > g del benchmark. Una estrategia con mayor media y mucha más volatilidad puede perder en crecimiento.

**R2. Benchmark y hurdle.**
- Calcular cada mes R_b = 0.5·[(1 + R_SPX TR, USD)(1 + ΔUSDMXN) − 1] + 0.5·R_CETES28.
- El satélite solo justifica su existencia si supera a R_b ajustado por riesgo (Sharpe contra CETES) durante la validación de `validacion_estrategias`.

**R3. Núcleo ≥ 70%: diversificado, sistemático y barato.**
- Base empírica: Bessembinder (la mediana de una acción pierde), SPIVA (el activo promedio pierde), DMS (global > doméstico en Sharpe con cobertura; 60:40 acota drawdowns).
- Criterio de selección (no es límite de riesgo): entre vehículos equivalentes, preferir el menor tracking difference observado, no solo el menor TER.

**R4. Satélite ≤ 30% y concentración.**
- Acción individual ≤ 10%, sector ≤ 25%, cripto ≤ 5%, prima de opciones en riesgo ≤ 2%, emisor de deuda privada ≤ 5%.
- Justificación cuantitativa: con probabilidad de ~57% de que una acción individual pierda contra T-bills, concentrar sin ventaja validada es jugar contra la mediana.

**R5. Dimensionamiento por riesgo, no por monto.**
- Acciones = ⌊(0.01 × Capital) / |Entrada − Stop|⌋. En fase de prueba se usa 0.005 en lugar de 0.01.
- Tope adicional: el nocional no puede superar el 10% del capital (acción individual) ni la holgura de sector.
- Verificación de gap: como el stop no garantiza el precio (colas gruesas; −20.47% en un día en 1987), si Nocional × (peor movimiento diario histórico del activo) > 2% del capital (el límite diario), reducir el tamaño hasta cumplirlo.

**R6. Cortacircuitos: la aritmética de la recuperación.**

| Nivel | Acción | Ganancia necesaria para volver al máximo |
|---|---|---|
| −8% | Reducir 50% el riesgo del satélite | +8.7% |
| −12% | Satélite a cero; solo núcleo; revisión completa | +13.6% |
| −15% | Pausa táctica de 30 días + post-mortem; núcleo defensivo | +17.6% |
| −20% | Des-riesgo a perfil de preservación hasta revisar con el dueño | +25.0% |

- Inferencia: con CETES en ~6.2% nominal, recuperar un −20% solo con el componente libre de riesgo toma (ln 1.25 / ln 1.0642) ≈ **3.6 años** a la tasa efectiva de hoy. Ese costo de oportunidad es la razón de ser del límite duro.

**R7. Rachas y límites de periodo.**
- Límites de pérdida: 2% diario, 4% semanal y 6% mensual.
- Con 1% de riesgo por operación, 5 pérdidas seguidas suman −4.9%. Por lo tanto, **el límite semanal de 4% se activa antes que la pausa por 5 pérdidas** si ocurren en la misma semana.
- Protocolo: 3 pérdidas → riesgo × 0.5; 2 ganancias → restaurar; 5 pérdidas → pausa y revisión de si el edge sigue vivo.

**R8. Kelly fraccional ≤ 0.25.**
- Con fracción k de Kelly se captura (2k − k²) del crecimiento máximo; con k = 0.25, el 43.75%.
- Ejemplo ilustrativo (Inferencia): exceso de 5% y σ = 18% → Kelly completo 1.54×; un cuarto de Kelly, 0.39× en ese activo.
- Además, `apalancamiento.bruto_max_fase_1 = 1.0` impide cualquier apalancamiento hasta cumplir el requisito de fase 2: 12 meses reales con Sharpe > 0.7 y drawdown dentro del objetivo.
- La estimación de μ tiene error enorme. Si μ está sobreestimado al doble, el Kelly "completo" es en realidad 2L*, donde el crecimiento cae al nivel de r_f. Por eso el tope es fraccional.

**R9. Rebalanceo por bandas (5% absoluta / 25% relativa, revisión mensual).**
- Peso objetivo de 50%: la banda relativa daría ±12.5 pp y la absoluta ±5 pp, así que manda la absoluta: rebalancear fuera de 45%-55%.
- Peso objetivo de 10%: la relativa (±2.5 pp) es más estrecha que la absoluta (±5 pp), así que el rango es 7.5%-12.5%.
- Inferencia: se toma como disparador la banda más estrecha; confirmar esa interpretación en el módulo de rebalanceo.
- Racional: el rebalanceo recorta varianza (volatility drag) y mantiene el riesgo que el sistema aceptó.

**R10. Medición en MXN y descomposición cambiaria.**
- Reportar cada posición en USD como R_MXN = (1 + R_USD)(1 + Δs) − 1, separando el efecto activo del efecto cambiario.
- DMS: el tipo de cambio añade ~6 pp de volatilidad. La decisión de cubrir o no se toma en el módulo de divisas, no aquí.

**R11. Efectivo y CETES.**
- Calcular siempre la tasa efectiva anual (convención 360 días, reinversión) y la real (Fisher).
- La reserva de 6 meses de gastos va fuera del portafolio (`liquidez`).
- La retención de ISR de 0.90% sobre capital es provisional. Estimar el impuesto definitivo sobre el interés real para el rendimiento neto.

**R12. Ejecución.**
- Órdenes límite por defecto. Órdenes a mercado solo en instrumentos muy líquidos y fuera de la subasta de apertura.
- Medir el implementation shortfall de cada orden contra el punto medio al momento de la decisión.
- Comparar brokers con órdenes espejo pequeñas cada trimestre (el método de Schwarz et al.).
- Alinear la conversión MXN/USD con la liquidación T+1.

**R13. Filtro contable para cualquier acción del satélite (filtro de riesgo, no de alfa).**
- Revisar: ROIC contra costo de capital y su tendencia; cobertura de intereses; deuda neta/EBITDA; FCF/utilidad neta (conversión de caja); utilidad contra flujo de operación (devengos); y DuPont para detectar ROE inflado por apalancamiento.
- En manufactura, Z de Altman < 1.81 es zona de peligro según Altman (1968).
- F-score de Piotroski: el paper original trata como "altos" los puntajes de 8-9 y como "bajos" los de 0-1.
- Una señal publicada entra con recorte de ≥50% de su ventaja in-sample (R16).

**R14. Validación antes de arriesgar dinero.**
- Backtest de ≥10 años con costos y slippage.
- Deflated Sharpe con probabilidad ≥0.95 y PBO ≤0.25.
- Paper trading de ≥3 meses y ≥30 operaciones.
- Arranque con 25% del capital asignado a la estrategia.
- Fases: 0 (papel, 0-3 meses), 1 (25% real, 3-12 meses), 2 (100%, 12+ meses con requisito).

**R15. Pronósticos.** Registrar cada pronóstico con probabilidad y evaluarlo con Brier (objetivo ≤0.20) solo después de acumular ≥50 pronósticos.

**R16. Recorte por publicación.** Esperanza de rendimiento para una anomalía publicada = rendimiento in-sample × (1 − 0.58), menos costos. Si el resultado no supera al benchmark, no entra.

**Rutinas derivadas de este módulo:**

| Frecuencia | Tarea | Métrica |
|---|---|---|
| Diaria | P&L en MXN contra el límite de 2%; revisar gaps y riesgo abierto por posición (≤1%) | Pérdida del día; riesgo abierto total |
| Semanal | P&L contra el límite de 4%; conteo de rachas por estrategia | Racha actual; factor de riesgo vigente |
| Mensual | P&L contra el límite de 6%; drawdown contra cortacircuitos; revisión de bandas de rebalanceo; R_b del benchmark; CAGR, σ, Sharpe contra CETES y máximo drawdown | Desviación de pesos; CAGR neto contra R_b |
| Trimestral | Auditoría de ejecución (shortfall, comparación de brokers); tracking difference del núcleo | pb de costo por ida y vuelta |
| Anual | Impuestos (retenciones contra ISR definitivo); actualizar DMS, SPIVA y fee study | Rendimiento neto después de impuestos |

---

## 7. Trampas y errores comunes

1. **Proyectar con la media aritmética.** Sobreestima la riqueza terminal (Jacquier-Kane-Marcus). Con σ = 20% el sesgo es de ~2 pp por año.
2. **Ignorar el volatility drag del apalancamiento.** Por encima de L* el crecimiento cae aunque el rendimiento esperado suba. Los ETFs apalancados diarios pierden en mercados laterales volátiles.
3. **Mezclar convenciones de tasa.** Tasa de descuento, rendimiento, 360 vs. 365 días, nominal vs. efectiva. En CETES, 6.15% de subasta equivale a 6.42% efectiva anual.
4. **Usar la TIR para elegir entre proyectos de distinta escala** o con flujos que cambian de signo.
5. **Sesgo de supervivencia y de "datos fáciles".** EUA es el ganador ex post. ACO (2022) con 39 países y McQuarrie (2024) con datos del s. XIX muestran distribuciones peores.
6. **Suponer normalidad.** El VaR gaussiano subestima las colas. Un stop no es una pérdida máxima garantizada.
7. **Contar con correlaciones de tiempos tranquilos.** En caídas extremas suben (Longin-Solnik). DMS 2026 reporta además más correlación entre acciones y bonos y entre mercados desarrollados y emergentes.
8. **Creer que "comisión cero" es costo cero.** Hay de 0.07% a 0.46% por ida y vuelta según el broker, además del spread cambiario.
9. **Confundir ROE con calidad.** El apalancamiento y las recompras inflan el ROE. El capital contable negativo lo vuelve inútil. Hay que usar ROIC.
10. **Tratar el EBITDA como efectivo.** Ignora capex, capital de trabajo e impuestos. Lo que cuenta es el FCF.
11. **Perseguir anomalías publicadas sin recorte.** En promedio pierden 58% tras publicarse.
12. **Sobre-operar.** Barber-Odean: 6.5 pp por año de rezago para los que más operan.
13. **Extrapolar el último año.** En 2025 el S&P/BMV IRT subió 35.2% y el S&P 500 18%. Un año no es evidencia de ventaja.
14. **Tratar al oro o a las acciones como cobertura de inflación automática.** La evidencia (−7% real en regímenes inflacionarios; oro negativo en 13 de 28 años inflacionarios) lo contradice en el corto plazo.
15. **Medir en USD cuando la base es MXN.** Un año bueno en USD puede ser malo en MXN si el peso se aprecia.
16. **Confundir T+1 con liquidez inmediata.** Vender y usar los fondos antes de la liquidación puede infringir las reglas de la cuenta.

---

## 8. Examen de titulación

1. **¿Qué tasa efectiva anual corresponde a CETES 28 días al 6.15% (convención 360) reinvertidos todo el año (365 días)?**
   (1 + 0.0615 × 28/360)^(365/28) − 1 = **6.42%**.

2. **Con inflación de 3.42%, ¿cuál es la tasa real ex ante de CETES al 6.15%?**
   1.0615/1.0342 − 1 = **2.64%** (antes de impuestos).

3. **Un activo rinde +50% y luego −50%. ¿Cuáles son su media aritmética y su rendimiento geométrico?**
   Aritmética 0%; geométrica √(1.5 × 0.5) − 1 = **−13.4%**.

4. **Media aritmética de 10% y σ = 20%. ¿Qué CAGR aproximado se espera?**
   G ≈ 10% − 0.2²/2 = **8%**.

5. **¿Qué ganancia se necesita para recuperar un drawdown de 20%?**
   0.20/0.80 = **25%**.

6. **Según Bessembinder (2018), ¿qué fracción de las acciones de CRSP (1926-2016) superó a los T-bills en toda su vida, y cuántas empresas explican toda la creación neta de riqueza?**
   **42.6%**; **1,092 empresas (~4%)** explican los ~US$35 billones.

7. **En la versión global (FAJ 2023), ¿qué porcentaje de acciones fuera de EUA perdió contra los T-bills y qué fracción de firmas explica la riqueza neta?**
   **57.4%** fuera de EUA (55.2% en EUA); **2.4%** de las firmas explica los US$75.7 billones (1990-2020).

8. **Rendimiento real anualizado de las acciones de EUA 1900-2025 según DMS 2026, y el de los bills.**
   **6.6%** y **0.5%**.

9. **¿Qué probabilidad estiman Anarkulova, Cederburg y O'Doherty (2022) de perder contra la inflación con 30 años en acciones diversificadas?**
   **12%** (39 países desarrollados, 1841-2019).

10. **Bono a 10 años, cupón 8% y rendimiento 9%, con duración modificada de 6.56. Estima el cambio de precio si la tasa sube 100 pb y explica la diferencia con el −6.27% real.**
    −6.56% por duración. La diferencia es la convexidad positiva.

11. **ROE = 20% con margen neto de 5%, rotación de 1.0 y multiplicador de capital de 4. ¿Es un ROE de calidad?**
    No necesariamente: viene del apalancamiento (4×). ROA = 5%. Hay que revisar ROIC y cobertura.

12. **¿Cuánto cae en promedio el rendimiento de una anomalía después de publicarse (McLean y Pontiff, 2016)?**
    **58%** (26% fuera de muestra, por sesgo estadístico).

13. **¿Cuándo pasaron EUA y México a T+1?**
    EUA el **28-may-2024**; México y Canadá el **27-may-2024**.

14. **¿Qué fracción del crecimiento máximo se obtiene con un cuarto de Kelly, y con qué volatilidad relativa?**
    2(0.25) − 0.25² = **43.75%** del crecimiento excedente máximo, con 25% de la volatilidad.

15. **Con 1% de riesgo por operación, ¿qué se activa primero: el límite semanal o la pausa por 5 pérdidas seguidas en la misma semana?**
    El límite semanal de 4%: 4 pérdidas suman −3.94% y la 5a llevaría a −4.9%.

---

## 9. Fuentes

1. UBS / Dimson, Marsh, Staunton — *Global Investment Returns Yearbook 2026, Public summary edition*: https://www.ubs.com/content/dam/assets/wm/static/cio/documents/giry2026-summary-public.pdf
2. UBS — Comunicado del Yearbook 2026 (3-mar-2026): https://www.ubs.com/global/en/media/display-page-ndp/en-20260303-global-investment-returns-yearbook-2026.html
3. Bessembinder (2018), JFE — ScienceDirect: https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301521 ; versión de autor: https://www.zeninvestor.org/wp-content/uploads/2025/11/Do-stocks-outperform-T-bills.pdf
4. Bessembinder, Chen, Choi, Wei (2023), FAJ 79(3): https://www.tandfonline.com/doi/abs/10.1080/0015198X.2023.2188870 ; CFA: https://rpc.cfainstitute.org/research/financial-analysts-journal/2023/long-term-shareholder-returns-evidence-from-64000-global-stocks
5. Bessembinder (2026), "One Hundred Years in the U.S. Stock Markets", SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6438198
6. Anarkulova, Cederburg, O'Doherty (2022), JFE 143(1): https://www.sciencedirect.com/science/article/abs/pii/S0304405X2100310X ; https://sites.google.com/site/cederburg/research
7. McCaffrey / CFA Institute Research Foundation (2024), *Stocks for the Long Run? New Evidence, Old Debates*: https://rpc.cfainstitute.org/sites/default/files/docs/research-reports/mccaffrey_rf_brief_stocksforthelongrun_online.pdf
8. McQuarrie (2024), FAJ 80(1): https://www.tandfonline.com/doi/abs/10.1080/0015198X.2023.2268556
9. Mandelbrot (1963), J. of Business 36: https://econpapers.repec.org/RePEc:ucp:jnlbus:v:36:y:1963:p:394
10. Cont (2001), Quantitative Finance 1(2): https://www.tandfonline.com/doi/abs/10.1080/713665670
11. Statman (1987), JFQA 22(3): https://www.semanticscholar.org/paper/How-Many-Stocks-Make-a-Diversified-Portfolio-Statman/206231eea16cd8714d192e02005d293484d4163a
12. Campbell, Lettau, Malkiel, Xu (2001), JF 56(1): https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00318
13. Campbell, Lettau, Malkiel, Xu (2023), Critical Finance Review 12: https://www.nber.org/papers/w29916
14. Longin, Solnik (2001), JF 56(2): https://onlinelibrary.wiley.com/doi/10.1111/0022-1082.00340
15. Jacquier, Kane, Marcus (2003), FAJ 59(6): https://www.tandfonline.com/doi/abs/10.2469/faj.v59.n6.2574
16. Kelly (1956), Bell System Technical Journal 35(4): https://onlinelibrary.wiley.com/doi/abs/10.1002/j.1538-7305.1956.tb03809.x
17. Farago, Hjalmarsson (2023), Review of Finance 27(2): https://ideas.repec.org/a/oup/revfin/v27y2023i2p495-538..html
18. Altman (1968), JF 23(4): https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1968.tb00843.x
19. Piotroski (2000), JAR 38: https://www.ivey.uwo.ca/media/3775523/value_investing_the_use_of_historical_financial_statement_information.pdf
20. Nissim, Penman (2001), RAS 6: https://link.springer.com/article/10.1023/A:1011338221623
21. Soliman (2008), The Accounting Review 83(3): https://publications.aaahq.org/accounting-review/article-pdf/83/3/823/19603/accr_2008_83_3_823.pdf
22. Novy-Marx (2013), JFE 108(1): https://www.sciencedirect.com/science/article/abs/pii/S0304405X13000044
23. Neville, Draaisma, Funnell, Harvey, Van Hemert (2021), JPM 47(8): https://people.duke.edu/~charvey/Research/Published_Papers/P154_The_best_strategies.pdf
24. Schwarz, Barber, Huang, Jorion, Odean (2025), JF 80(5): https://onlinelibrary.wiley.com/doi/full/10.1111/jofi.13467
25. Morningstar — Annual US Fund Fee Study (2026): https://www.morningstar.com/business/insights/research/annual-us-fund-fee-study
26. S&P DJI — SPIVA U.S. Year-End 2025: https://www.spglobal.com/spdji/en/spiva/article/spiva-us/
27. SEC — Implementación de T+1: https://www.sec.gov/newsroom/press-releases/2024-62
28. HSBC — T+1 en EUA, Canadá y México: https://www.business.hsbc.com/en-gb/financial-regulations/tplus1-settlement-cycle/us-canada-mexico
29. ESMA — T+1 para octubre de 2027: https://www.esma.europa.eu/press-news/esma-news/esma-proposes-move-t1-october-2027
30. SEC — Fact sheet, tick sizes y access fees: https://www.sec.gov/files/34-101070-fact-sheet.pdf ; exención de cumplimiento: https://www.sec.gov/newsroom/press-releases/2025-130-sec-issues-exemptive-order-regarding-compliance-certain-rules-under-regulation-nms
31. Sidley — La Corte del Circuito de D.C. confirma la regla (oct-2025): https://www.sidley.com/en/insights/newsupdates/2025/10/dc-circuit-upholds-sec-tick-size-fee-cap-rule
32. Federal Reserve History — Stock Market Crash of 1987: https://www.federalreservehistory.org/essays/stock-market-crash-of-1987 ; Goldman Sachs: https://www.goldmansachs.com/our-firm/history/moments/1987-black-monday
33. Barber, Odean (2000), JF 55(2): https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00226
34. cetes.app — Tasas de CETES, sep-2026 (fuente secundaria; confirmar en Banxico): https://cetes.app/cetes-hoy ; Banxico, resultados de subasta: https://www.banxico.org.mx/apps/dao-web/4/54/4/resultadosgubernamental.html
35. Expansión — Banxico mantiene la tasa en 6.5% (24-sep-2026): https://expansion.mx/economia/2026/09/24/banxico-tasa-de-interes-de-referencia-6-5-septiembre
36. El Financiero — Inflación de 3.42% en la 1a quincena de septiembre de 2026: https://www.elfinanciero.com.mx/economia/2026/09/24/inflacion-acelera-a-342-en-primera-quincena-de-septiembre-que-alimentos-subieron-mas-de-precio/
37. Russell Bedford México — Retención sobre intereses 2026: https://russellbedford.mx/fiscal/aumento-en-la-tasa-de-retencion-por-intereses-en-el-ejercicio-2026/
38. Justia México — Art. 129 LISR: https://mexico.justia.com/federales/leyes/ley-del-impuesto-sobre-la-renta/titulo-iv/capitulo-iv/seccion-ii/
39. Man Group — What Works When Inflation Hits?: https://www.man.com/insights/when-inflation-hits
40. Larry Swedroe — Resumen de Bessembinder (2026): https://larryswedroe.substack.com/p/a-century-of-stock-market-winnersand ; M. Mauboussin en X: https://x.com/mjmauboussin/status/2034439690829631902
41. Anarkulova, Cederburg, O'Doherty — "Beyond the Status Quo" (SSRN WP): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4590406
42. TKer — Resumen de SPIVA 2025: https://www.tker.co/p/spiva-2025-active-manager-vs-benchmark
43. S&P DJI — SPIVA Latin America Year-End 2025: https://www.spglobal.com/spdji/en/documents/spiva/spiva-latin-america-year-end-2025.pdf
44. Bessembinder, Cooper, Zhang (2023), JFE 147: https://www.sciencedirect.com/science/article/abs/pii/S0304405X22002264
45. McLean, Pontiff (2016), JF 71(1): https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12365
46. Barber, Huang, Odean, Schwarz (2022), JF 77(6), "Attention-Induced Trading and Returns: Evidence from Robinhood Users": https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.13183
47. Libros de texto (editoriales): BKM 13e https://www.mheducation.com/highered/product/investments-bodie.html ; Brealey-Myers-Allen-Edmans 14e https://www.mheducation.com/highered/product/principles-corporate-finance-brealey-myers/1265434476.html ; Berk-DeMarzo 6e https://www.pearson.com/en-us/subject-catalog/p/corporate-finance/P200000009791/9780137844906 ; Graham-Zweig 3a ed. https://jasonzweig.com/books/the-intelligent-investor/ ; Malkiel 13a ed. https://en.wikipedia.org/wiki/A_Random_Walk_Down_Wall_Street

**Sin verificar o con verificación parcial en este módulo:** el rendimiento real histórico del mercado accionario mexicano en DMS (no está en el resumen público); el % de fondos large-cap de EUA que pierde a 20 años (93%, tomado de un resumen secundario, no del PDF de S&P); la tasa exacta de CETES del 22-sep-2026 (fuente secundaria); el decaimiento específico del F-score después de 2000 (solo hay evidencia de practicantes, no académica verificada).
