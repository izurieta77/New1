# Módulo 03 — Valuación y análisis fundamental: DCF, costo de capital, múltiplos, calidad de utilidades y qué sobrevive fuera de muestra

> Nivel: maestría · Actualizado: 2026-09-25 · Grado de evidencia global: **B**. Como herramienta, la valuación es aritmética correcta (DCF, residual income y ROIC contra WACC son identidades, grado A). Como fuente de alfa, las señales fundamentales publicadas decayeron en EUA. Value (HML) cayó **−57.8%** entre dic-2006 y sep-2020 y en jul-2026 seguía **30%** debajo de su pico. El PEAD no existe en emisoras grandes desde 2006. Accruals y F-score no rinden en EUA después de publicarse. Sobreviven mejor fuera de EUA, combinadas (value + rentabilidad) y como filtros para evitar pérdidas.

---

## 1. Objetivos de dominio (qué debe saber hacer quien "se titula" en este módulo)

1. Construir un DCF de FCFF y otro de FCFE coherentes: flujo, tasa, moneda e inflación alineados. Reconciliar ambos con el puente de deuda neta.
2. Estimar el costo de capital con insumos vigentes: tasa libre de riesgo ajustada por default, ERP implícita de Damodaran del mes, beta bottom-up, prima país ponderada por exposición (λ), costo de deuda por calificación sintética y tasa marginal de impuestos. Convertir de USD a MXN por diferencial de inflación.
3. Modelar el valor terminal sin sus trampas: g ≤ tasa libre de riesgo nominal, reinversión consistente (g = tasa de reinversión × RONIC), convergencia de RONIC a WACC salvo moat documentado, y peso del valor terminal reportado.
4. Usar múltiplos como DCF comprimidos: derivar P/E, P/B y EV/EBITDA justificados y saber cuándo cada uno engaña.
5. Aplicar residual income (Ohlson) y leer el P/B como valor presente del ROE en exceso.
6. Hacer un DCF inverso (Mauboussin-Rappaport): qué crecimiento, margen y ROIC descuenta el precio, y compararlo con tasas base históricas.
7. Diagnosticar ventaja competitiva (ROIC − WACC, persistencia, fuentes del moat) y calificar la asignación de capital, incluidas recompras y dilución por compensación en acciones.
8. Auditar la calidad de utilidades: accruals (Sloan), F-score (Piotroski), rentabilidad bruta (Novy-Marx), QMJ (Asness-Frazzini-Pedersen) y M-score (Beneish), con sus umbrales y tasas de error.
9. Citar con números qué señales fundamentales sobrevivieron a su publicación y cuáles no. Separar in-sample de out-of-sample, bruto de neto y EUA de global y de México.
10. Convertir todo lo anterior en reglas del sistema coherentes con `config/parametros.json`: filtro, veto, dimensionamiento y registro de pronósticos.

---

## 2. Núcleo teórico

### 2.1 Principio único
Valor = VP de los flujos esperados a una tasa que refleja su riesgo. Toda la disciplina es consistencia:
- **Flujo a la firma (FCFF)** se descuenta al **WACC** y da el valor operativo. **Flujo al accionista (FCFE)** se descuenta al **costo de capital propio (k_e)** y da el valor del capital.
- **Moneda y tasa:** flujos en MXN se descuentan a tasa en MXN. Flujos nominales van con tasa nominal y flujos reales con tasa real.
- **Valor del capital por acción** = (valor operativo + caja y activos no operativos − deuda − minoritarios − otros derechos como arrendamientos y pensiones − valor de opciones y RSU vivas) / acciones en circulación.

### 2.2 Flujos
- FCFF = EBIT·(1 − t) + D&A − CapEx − ΔCapital de trabajo = NOPAT − Reinversión neta.
- FCFE = FCFF − Intereses·(1 − t) + (Deuda nueva − Amortizaciones).
- Tasa de reinversión RR = Reinversión neta / NOPAT. **Crecimiento sostenible del NOPAT: g = RR × RONIC** (RONIC = retorno sobre el capital nuevo).
- **Fórmula del value driver (McKinsey):** V₀ = NOPAT₁ · (1 − g/RONIC) / (WACC − g).
  - Ejemplo: NOPAT₁ = 100, g = 4%, WACC = 10%. Con RONIC = 15%: V = 100·(1 − 0.267)/0.06 = **1,222**. Con RONIC = 10% = WACC: V = 1,000 = NOPAT/WACC, y **el crecimiento no agrega nada**. Con RONIC = 8%: V = **833**, y **el crecimiento destruye valor**.
  - Intuición: el crecimiento solo vale si RONIC > WACC. Esa es la definición operativa de moat.

### 2.3 Costo de capital
**CAPM:** k_e = r_f + β·ERP + λ·CRP.

**Tasa libre de riesgo.** El T-bond a 10 años ya no es estrictamente libre de riesgo. Moody's bajó a EUA de Aaa a Aa1 el 16-may-2025. Desde entonces Damodaran reporta dos ERP: una contra el T-bond, para comparar con su serie histórica, y otra contra una r_f ajustada (T-bond − diferencial de default de Aa1 ≈ 0.22%) [2].

**ERP implícita del S&P 500 (Damodaran).** Es la TIR que iguala el precio del índice con los dividendos y recompras esperados. Supone crecimiento de consenso a 5 años y después crecimiento estable igual a r_f. Valores de 2026, tomados de sus hojas mensuales [1][2][3]:

| Inicio de mes | S&P 500 | T-bond 10a | Crec. 5 años (consenso top-down) | E(R) acciones | ERP vs T-bond | ERP vs r_f ajustada |
|---|---|---|---|---|---|---|
| ene-2026 | 6,845.5 | 4.18% | 10.50% | 8.41% | **4.23%** | 4.46% |
| jul-2026 | 7,499.4 | 4.45% | 13.69% | 8.62% | 4.17% | 4.39% |
| ago-2026 | 7,489.7 | 4.74% | 14.26% | 8.97% | 4.23% | 4.45% |
| sep-2026 | 7,686.1 | 4.75% | 13.99% | 8.84% | **4.09%** | 4.31% |

Referencias de la misma hoja: promedio 1960-actual de **4.25%**, promedio de la última década de **5.08%** y máximo histórico de **6.45%**. El rendimiento en efectivo (dividendos + recompras de 12 meses / índice) era de **2.63%** en septiembre, con un payout total de ~74% de las utilidades [2].
*Inferencia:* la ERP de septiembre de 2026 está en su promedio de largo plazo. Pero se sostiene con un crecimiento esperado de utilidades de ~14% anual, que subió desde 10.5% en enero. El riesgo de la valuación agregada está en que ese optimismo revierta (§2.12, sesgos de analistas).

**Prima país (México), actualización de Damodaran del 1-jul-2026 [4][5]:**
- La prima de mercado maduro es de **4.20%** (ERP de EUA de 4.42% menos el diferencial de default de EUA). El multiplicador de volatilidad relativa acciones/bonos es de **1.55**.
- México tiene calificación Moody's **Baa3**:
  - Por calificación: diferencial de default de 1.75%, **CRP de 2.72%** y **ERP total de 6.92%**.
  - Por CDS neto de Suiza: diferencial de 1.46%, CRP de 2.27% y ERP total de 6.47%.
- La tasa marginal de impuestos que usa la hoja para México es de 30%.
- **λ (exposición de la empresa al riesgo país):** usa la fracción de ingresos de la empresa que viene de México, no el país de su sede. Una emisora de la BMV con 70% de ingresos en EUA no debe cargar el CRP completo.

**Beta bottom-up.** Toma la beta desapalancada promedio del sector (β_u), reapalanca con β_L = β_u·[1 + (1 − t)·D/E] y ajusta por el efectivo. Evita la beta de regresión de una sola acción: su error estándar es enorme.

**Costo de deuda.** k_d = r_f + diferencial por calificación (o calificación sintética por cobertura de intereses) + diferencial país si aplica. Se usa k_d·(1 − t_marginal).

**WACC** = E/(D+E)·k_e + D/(D+E)·k_d·(1 − t), con pesos a valor de mercado y pesos objetivo de largo plazo.

**Conversión USD → MXN:** (1 + k_MXN) = (1 + k_USD)·(1 + π_MX)/(1 + π_US).
- Ejemplo ilustrativo para una emisora mexicana 100% doméstica con β = 1:
  - k_USD = 4.53% (r_f ajustada de sep-2026) + 4.20% + 2.72% = **11.45%**.
  - Con π_MX = 3.5% y π_US = 2.5% (supuestos, no datos): k_MXN = **12.54%**.
  - Contexto: Banxico mantuvo el objetivo en 6.50% el 24-sep-2026 [62].

### 2.4 Valor terminal y sus trampas
Fórmula de Gordon: VT_n = FCFF_{n+1}/(WACC − g) con FCFF_{n+1} = NOPAT_{n+1}·(1 − g/RONIC).

**Cuánto pesa.** En la hoja de Damodaran de sep-2026, el VP del valor terminal es **~86%** del valor intrínseco del S&P 500 (6,359 de 7,398; cálculo propio con sus celdas) [2]. Lo mismo pasa en casi cualquier empresa en marcha: el DCF es sobre todo un supuesto de largo plazo.

**Sensibilidad.** Cálculo propio: réplica del modelo implícito de sep-2026 con tiempos anuales. La réplica da E(R) = 8.83% contra 8.84% de la hoja.
- ±50 pb en la tasa de descuento mueven el valor del índice **+14.3% / −11.2%**. ±100 pb lo mueven **+33.3% / −20.2%**.
- Si el crecimiento a 5 años fuera de 7% en vez de 14%, el valor caería **25.6%**.
- A la ERP promedio de la última década (5.08%), el índice valdría **20%** menos. Para justificar el precio con esa ERP haría falta un crecimiento de **~19.6%** anual por 5 años.

**Reglas del valor terminal:**
1. g ≤ r_f nominal de la moneda del flujo. Ninguna empresa crece más que la economía para siempre.
2. En el terminal, RONIC tiende a WACC (crecimiento sin valor), salvo que haya un moat documentado. En ese caso, RONIC > WACC con una prima decreciente.
3. La reinversión debe ser consistente con g. El error clásico es g alto con CapEx igual a la depreciación.
4. Reporta el % del valor que viene del terminal. Si pasa de 75%, la tesis depende del largo plazo y exige un margen de seguridad mayor.
5. Calcula el múltiplo de salida implícito (VT/EBITDA_n) y compáralo con el historial del sector. Un múltiplo de salida no sustituye al Gordon: es un DCF escondido con los supuestos de otro.

### 2.5 Múltiplos: DCF comprimidos
- **P/E forward justificado** = payout/(k_e − g), con payout = 1 − g/ROE. Ejemplo con ROE 15%, g 4% y k_e 10%: payout = 73.3% y P/E = **12.2x**.
- **P/B justificado** = (ROE − g)/(k_e − g) → con los mismos datos, **1.83x**. Un P/B alto es correcto si ROE > k_e de forma persistente.
- **EV/EBITDA** = f(ROIC, g, WACC, t, intensidad de CapEx). Sirve para comparar entre estructuras de capital. Engaña con CapEx y arrendamientos distintos, y cuando la compensación en acciones (SBC) se suma de regreso.
- **EV/Sales** es para empresas sin utilidad. Implícitamente supone un margen objetivo: exige declararlo.
- **Coherencia de numerador y denominador:** EV con EBITDA, EBIT o ventas. Precio con utilidad neta o valor en libros. Mezclarlos es error de examen.
- **Pares.** Un múltiplo relativo solo dice "más barato que sus pares", no "barato". Bartram-Grinblatt (2018) muestran que un valor "de pares" estimado estadísticamente con estados contables sí predice rendimientos (hasta ~10% anual ajustado por riesgo, convergencia en ~34 meses) [53].

### 2.6 Residual income (Ohlson)
- V₀ = B₀ + Σ_t (ROE_t − k_e)·B_{t−1}/(1 + k_e)^t. Requiere contabilidad de *clean surplus*.
- Ohlson (1995) formaliza el valor como función del libro, las utilidades anormales y la "otra información" con dinámica lineal [54].
- **Ventaja práctica:** el valor terminal pesa menos que en un DCF porque el libro ya está en V₀. Es útil en bancos y aseguradoras, donde el FCFF no tiene sentido.
- Frankel-Lee (1998) usan residual income con pronósticos de I/B/E/S: la razón V/P predice rendimientos transversales hasta por **3 años** [55]. Haboub, Kartsaklas y Sarafidis (arXiv, may-2025) reportan que en EUA los portafolios de V/P alto superan a los de V/P bajo en horizontes de 1 a 3 años [60] (working paper, grado C).

### 2.7 DCF inverso (Expectations Investing)
Mauboussin y Rappaport (2021, edición revisada) proponen partir del precio y preguntar qué flujos implica. El precio es el dato con menos error [10]:
1. Fija el costo de capital y el horizonte de ventaja competitiva (CAP).
2. Resuelve el crecimiento de ventas, el margen operativo y la reinversión que igualan el DCF al precio.
3. Identifica el disparador de valor que más mueve el valor (ventas, costos o inversión).
4. Compara las expectativas implícitas con las **tasas base** (qué fracción histórica de empresas de ese tamaño logró ese crecimiento) y con tu pronóstico.
5. Solo hay oportunidad si tu escenario difiere del implícito y tienes una razón fechada y verificable.
- La herramienta `herramientas/dossier.py` ya calcula una valuación inversa (`--tasas`, `--crecimiento-terminal`). Las tasas deben venir de §2.3, no de los valores por defecto.

### 2.8 ROIC contra WACC y moats
- ROIC = NOPAT / capital invertido (capital de trabajo operativo + activo fijo neto + intangibles adquiridos; ajustar por arrendamientos y por I+D capitalizado). **Se crea valor solo si ROIC > WACC**, y el valor se amplifica con crecimiento y duración (CAP).
- **Reversión a la media:** el ROIC regresa hacia el costo de capital en todos los periodos estudiados. Pero hay más persistencia en los extremos de la que el azar explicaría (Mauboussin y Callahan, Counterpoint Global) [11][12]. *No verificado en esta sesión:* las cifras exactas de transición entre quintiles del reporte, porque el PDF de Morgan Stanley bloqueó la descarga (403).
- **Measuring the Moat (Mauboussin y Callahan, Morgan Stanley):**
  - Primero el mapa y la estructura de la industria: rentabilidad del sector, barreras de entrada, rivalidad, poder de proveedores y clientes, sustitutos, disrupción.
  - Después las fuentes de la ventaja de la firma:
    - Del lado de la producción: escala, costos y know-how.
    - Del lado del consumidor: costos de cambio, efectos de red, hábito y marca.
    - Externas: regulación y licencias.
  - Al final, la interacción estratégica y la gestión.
  - El producto es un ROIC − WACC esperado **y su duración**.
- **Buffett** en la práctica: Frazzini, Kabiller y Pedersen (2018) encuentran un Sharpe de **0.79** para Berkshire. Su alfa deja de ser significativo al controlar por BAB y QMJ. El apalancamiento promedio fue de ~**1.7 a 1**. Conclusión de los autores: acciones baratas, seguras y de calidad, apalancadas [27].

### 2.9 Asignación de capital y recompras
- Una recompra crea valor para el accionista que se queda solo si **precio < valor intrínseco**. A precio justo es neutral y a precio alto transfiere riqueza a quien vende.
- Berkshire formaliza esa regla en su carta de 2025: compra "below our estimate of intrinsic value, conservatively determined". La firma Gregory E. Abel el 28-feb-2026; Buffett dejó de ser CEO el 31-dic-2025 [26].
- Mide la **recompra neta**: recompras − emisión por SBC. Una empresa que "recompra" 3% y emite 3% en RSU no reduce su conteo de acciones.
- Evidencia de eventos:
  - Ikenberry, Lakonishok y Vermaelen (1995), EUA 1980-1990: rendimiento anormal buy-and-hold de **12.1% a 4 años** tras el anuncio, y **45.3%** en empresas value [56].
  - Fu y Huang (2016): ese rendimiento anormal **desaparece** en los eventos de 2003-2012 [57].
  - Manconi, Peyer y Vermaelen (2019): en 31 países fuera de EUA (más de 9,000 anuncios) hay excesos positivos de corto y largo plazo, mayores donde la subvaluación es probable y el mercado es menos eficiente [58].
  - (No verificado en esta sesión: el impuesto federal de 1% sobre recompras netas en EUA desde 2023.)

### 2.10 Calidad de utilidades: las cinco herramientas
1. **Accruals (Sloan 1996):**
   - Utilidad = flujo de caja + accruals. Los accruals son menos persistentes y el mercado los sobrevalora.
   - Medida de balance: ΔActivo circulante − ΔCaja − (ΔPasivo circulante − ΔDeuda de corto plazo − ΔImpuestos por pagar) − Depreciación, entre activo total promedio. Hoy se usa la versión de flujos: (Utilidad neta − CFO)/Activo.
   - La cobertura bajo menos alto rindió **~10-12% anual** in-sample (cifra de fuentes secundarias [13]; el original no se consultó).
2. **F-score (Piotroski 2000).** Nueve señales binarias:
   - Rentabilidad: ROA > 0; CFO > 0; ΔROA > 0; CFO > utilidad neta (accrual).
   - Apalancamiento y liquidez: ΔApalancamiento < 0; ΔRazón circulante > 0; sin emisión de acciones.
   - Eficiencia: ΔMargen bruto > 0; ΔRotación de activos > 0.
   - Aplicado **solo al quintil de alto book-to-market** de EUA en 1976-1996, subió el rendimiento del inversionista value en **≥ 7.5% anual**. La cobertura de ganadores menos perdedores rindió **23% anual**. El efecto se concentra en empresas chicas, poco líquidas y sin cobertura de analistas [16].
3. **Rentabilidad bruta (Novy-Marx 2013).** GP/A = (Ventas − Costo de ventas)/Activo total. Tiene casi el mismo poder predictivo que el B/M. Resultados de jul-1963 a dic-2010, sin financieras [19]:
   - El diferencial rentable menos no rentable es de **0.31% mensual** (t = 2.49). Su alfa FF3 es de **0.52% mensual** (t = 4.49).
   - Su correlación con value es de **−0.57**. Combinadas, las dos estrategias dan 0.71% mensual con la misma volatilidad que cada una por separado.
4. **QMJ (Asness-Frazzini-Pedersen 2019).** La calidad se compone de rentabilidad, crecimiento, seguridad y payout (buena administración). Las acciones de calidad cotizan más caras, pero no lo suficiente: el factor largo calidad y corto basura tiene alfa significativo en EUA y en 24 países [20].
5. **M-score (Beneish 1999).**
   - M = −4.84 + 0.920·DSRI + 0.528·GMI + 0.404·AQI + 0.892·SGI + 0.115·DEPI − 0.172·SGAI + 4.679·TATA − 0.327·LVGI [24].
   - Umbral: M > **−1.78** señala posible manipulador.
   - En la muestra de control 1989-1992 identificó al **50%** de los manipuladores antes de que se descubrieran, con **7.2%** de falsos positivos [22].
   - Beneish, Lee y Nichols (2013): un M-score alto predice **menores rendimientos** en cada decil de tamaño, B/M, momentum, accruals e interés en corto. El efecto es más fuerte en acciones de accruals bajos, que en apariencia son de "alta calidad" [23].

### 2.11 Graham y Dodd, intangibles y el libro contable
- **Graham y Dodd** (1934; 7a ed., McGraw Hill, 2023, con Seth Klarman [25]):
  - El valor intrínseco es un rango, no un punto.
  - El margen de seguridad protege contra el error de estimación.
  - Se prefiere el poder de ganancia normalizado de varios años a la utilidad de un solo año.
  - Hay que distinguir inversión de especulación.
- **Intangibles.** La contabilidad (US GAAP y, en general, IFRS) lleva a gasto la mayor parte de la I+D, la publicidad y el capital organizacional. Eso rompe el B/M como medida de valor. Correcciones:
  - Capitalizar la I+D con vida útil sectorial (Damodaran).
  - Capitalizar el SG&A con el método de inventario perpetuo, como en Eisfeldt, Kim y Papanikolaou (2022) [32].
- *Inferencia:* en una economía donde el capital es intangible, el P/B sin ajuste mide mal la contabilidad antes que el valor.

### 2.12 Sesgos de expectativas (analistas)
- **La Porta (1996):** las acciones con el menor crecimiento esperado por analistas rinden **~20% más al año** que las de mayor crecimiento esperado. Las expectativas son demasiado extremas [40].
- **Bordalo, Gennaioli, La Porta y Shleifer (2019):** lo explican con expectativas diagnósticas. Los analistas sobrerreaccionan a buenas noticias de crecimiento: "fast earnings growth predicts future Googles but not as many as analysts believe" [41].
- **Bouchaud, Krüger, Landier y Thesmar (2019):** con expectativas pegajosas, los analistas son demasiado pesimistas con las empresas de alta rentabilidad. Eso explica la anomalía de rentabilidad [42].
- **Uso:** el consenso de crecimiento a largo plazo es un insumo sesgado. Si el precio descuenta el LTG de consenso (§2.7), se asume ese sesgo.

---

## 3. Literatura canónica

| Autores | Año | Título | Revista/Editorial | Hallazgo clave cuantificado | Enlace/DOI | Grado |
|---|---|---|---|---|---|---|
| Graham, Dodd (7a ed. con Klarman) | 1934/2023 | Security Analysis | McGraw Hill | Margen de seguridad, poder de ganancia normalizado | ISBN 9781264932405 [25] | A (marco) |
| Ohlson | 1995 | Earnings, Book Values, and Dividends in Equity Valuation | CAR 11:661-687 | Valor = libro + VP de utilidades anormales | 10.1111/j.1911-3846.1995.tb00461.x | A (teoría) |
| Frankel, Lee | 1998 | Accounting valuation, market expectation, and cross-sectional stock returns | JAE 25(3):283-319 | V/P con residual income predice rendimientos hasta 3 años | sciencedirect S0165410198000263 | B |
| Sloan | 1996 | Do stock prices fully reflect information in accruals and cash flows about future earnings? | TAR 71:289-315 | Cobertura de accruals ~10-12% anual in-sample (fuente secundaria) | [13] | B antes / D EUA post-2000 |
| Green, Hand, Soliman | 2011 | Going, Going, Gone? The Apparent Demise of the Accruals Anomaly | Mgmt Sci 57(5):797-816 | Las coberturas de accruals en EUA ya no son confiablemente positivas; causa: capital de hedge funds | 10.1287/mnsc.1110.1320 | A (del decaimiento) |
| Pincus, Rajgopal, Venkatachalam | 2007 | The Accrual Anomaly: International Evidence | TAR 82(1):169 | La anomalía aparece fuera de EUA (el detalle por país no se verificó) | [15] | C |
| Piotroski | 2000 | Value Investing: The Use of Historical Financial Statement Information… | JAR 38:1-41 | +7.5% anual para value; cobertura de 23% anual en 1976-1996 | SSRN 249455 | C en EUA post-publicación / B internacional |
| Walkshäusl | 2020 | Piotroski's FSCORE: international evidence | J. Asset Mgmt 21:106-118 | F alto menos F bajo ≈ +10% anual en 2000-2018 fuera de EUA (desarrollados y emergentes) | 10.1057/s41260-020-00157-2 | B |
| Novy-Marx | 2013 | The other side of value: The gross profitability premium | JFE 108(1):1-28 | 0.31%/mes (t = 2.49); alfa FF3 de 0.52%/mes; correlación de −0.57 con value | S0304405X13000044 | B |
| Asness, Frazzini, Pedersen | 2019 | Quality minus junk | RAST 24(1):34-112 | QMJ con alfa significativo en EUA y 24 países | 10.1007/s11142-018-9470-2 | B |
| Beneish | 1999 | The Detection of Earnings Manipulation | FAJ 55:24-36 | Detecta 50% de manipuladores con 7.2% de falsos positivos (umbral de −1.78) | [22] | B (filtro) |
| Beneish, Lee, Nichols | 2013 | Earnings Manipulation and Expected Returns | FAJ 69(2):57-82 | M-score alto → menor rendimiento en todos los deciles de control | 10.2469/faj.v69.n2.1 | B |
| Bernard, Thomas | 1989 | Post-Earnings-Announcement Drift: Delayed Price Response or Risk Premium? | JAR 27:1-36 | Drift en la dirección de la sorpresa; no se explica por riesgo | [36] | D en grandes hoy |
| Martineau | 2022 | Rest in Peace Post-Earnings Announcement Drift | CFR 11(3-4):613-646 | Sin PEAD en emisoras grandes desde 2006; en microcaps desapareció después | [37] | A (del decaimiento) |
| La Porta | 1996 | Expectations and the Cross-Section of Stock Returns | JF 51:1715-1742 | LTG bajo supera a LTG alto por ~20% anual | [40] | B |
| Bordalo, Gennaioli, La Porta, Shleifer | 2019 | Diagnostic Expectations and Stock Returns | JF 74(6):2839-2874 | La sobrerreacción del LTG explica la reversión | 10.1111/jofi.12833 | B |
| Bouchaud, Krüger, Landier, Thesmar | 2019 | Sticky Expectations and the Profitability Anomaly | JF 74(2):639-674 | Pesimismo de analistas con las empresas rentables | 10.1111/jofi.12734 | B |
| Ikenberry, Lakonishok, Vermaelen | 1995 | Market Underreaction to Open Market Share Repurchases | JFE 39:181-208 | +12.1% a 4 años; +45.3% en value | [56] | C en EUA hoy |
| Fu, Huang | 2016 | The Persistence of Long-Run Abnormal Returns Following Stock Repurchases and Offerings | Mgmt Sci 62(4):964-984 | El drift post-recompra desaparece en 2003-2012 | [57] | A (del decaimiento) |
| Manconi, Peyer, Vermaelen | 2019 | Are Buybacks Good for Long-Term Shareholder Value? Evidence from Buybacks around the World | JFQA 54(5):1899-1935 | >9,000 anuncios en 31 países: excesos positivos | [58] | B (fuera de EUA) |
| Frazzini, Kabiller, Pedersen | 2018 | Buffett's Alpha | FAJ 74(4):35-55 | Sharpe de 0.79; apalancamiento ~1.7x; alfa explicado por BAB + QMJ | 10.2469/faj.v74.n4.3 | A |
| Bartram, Grinblatt | 2018 | Agnostic fundamental analysis works | JFE 128(1):125-147 | Valor de pares vs. precio: hasta ~10% anual ajustado por riesgo | 10.1016/j.jfineco.2016.11.008 | B |
| Fama, French | 2021 | The Value Premium | RAPS 11(1):105-121 | Premio value mucho menor en 1991-2019, pero no se rechaza que sea igual | [30] | A (del hecho) |
| Arnott, Harvey, Kalesnik, Linnainmaa | 2021 | Reports of Value's Death May Be Greatly Exaggerated | FAJ 77(1) | Drawdown de HML de 55% a mediados de 2020; lo explican los intangibles y el abaratamiento relativo | 10.1080/0015198X.2020.1842704 | B |
| Israel, Laursen, Richardson | 2021 | Is (Systematic) Value Investing Dead? | JPM 47(2):38-62 | "Muerte" prematura; los fundamentales siguen importando | [31] | B |
| Eisfeldt, Kim, Papanikolaou | 2022 | Intangible Value | CFR 11(2):299-332 | HML_INT (con SG&A capitalizado) rinde más que HML, también en las décadas malas | NBER w28056 | B |
| Lev, Srivastava | 2022 | Explaining the Recent Failure of Value Investing | CFR 11(2):333-360 | Value no ganó en ~30 años salvo tras el dotcom; causas: contabilidad de intangibles y menor reversión | [33] | B |
| McLean, Pontiff | 2016 | Does Academic Research Destroy Stock Return Predictability? | JF 71(1):5-32 | 97 predictores: −26% fuera de muestra y −58% post-publicación | 10.1111/jofi.12365 | A |
| Hou, Xue, Zhang | 2020 | Replicating Anomalies | RFS 33(5):2019-2133 | 65% de 452 anomalías no pasa t = 1.96 (ponderado por valor, sin microcaps); 82% no pasa t = 2.78 | [49] | A |
| Novy-Marx, Velikov | 2016 | A Taxonomy of Anomalies and Their Trading Costs | RFS 29(1):104-147 | Con turnover < 50% mensual sobreviven netas; size, value y rentabilidad tienen más capacidad | [52] | A |
| Damodaran | 2025 | Investment Valuation, 4a ed. | Wiley (ene-2025) | Texto de referencia; datos a 2023; secciones nuevas sobre bitcoin y oro | ISBN 9781394254606 [8] | A (herramienta) |
| Koller, Goedhart, Wessels (McKinsey) | 2025 | Valuation, 8a ed. | Wiley (may-2025) | Value driver, ROIC, alto crecimiento y activos digitales | ISBN 9781394279418 [9] | A (herramienta) |
| Mauboussin, Rappaport | 2021 | Expectations Investing (revisado) | Columbia Business School Publishing | DCF inverso y expectativas implícitas en el precio | [10] | A (herramienta) |
| Greenblatt | 2005 | The Little Book That Beats the Market | Wiley | ~30% anual según el libro, backtest propio del autor (periodo 1988-2004 tomado de fuentes secundarias) | [28] | C |

---

## 4. Lo más reciente 2023-2026 (con fecha)

**Datos y manuales**
- **Damodaran, ERP 2026 Edition** (SSRN 6361419, 2026) y hojas mensuales. ERP de **4.23%** el 1-ene-2026 y de **4.09%** el 1-sep-2026, con E(R) de 8.84% [1][2][6].
- **Damodaran, país, 1-jul-2026** (corregida el 9-jul). Prima madura de 4.20%. México Baa3: CRP de 2.72% y ERP de 6.92% por calificación; 6.47% por CDS [4].
- **Libros:** Damodaran, *Investment Valuation* 4a ed. (Wiley, 10-ene-2025) [8]. McKinsey, *Valuation* 8a ed. (Wiley, mayo de 2025) [9]. Graham-Dodd 7a ed. (2023) [25].
- **Carta de Berkshire de 2025** (28-feb-2026, G. Abel). CAGR 1965-2025 de **19.7%** contra 10.5% del S&P 500. En 2025, Berkshire subió **10.9%** y el S&P 17.9% [26].

**Valor y calidad, datos al 31-jul-2026 (French, AQR; cálculo propio)**
- **HML (value) por año:**

| Año | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (ene-jul) |
|---|---|---|---|---|---|---|---|
| HML | −30.7% | +22.2% | +31.7% | −11.1% | −7.0% | +6.6% | +12.3% |

  - Desde el mínimo de sep-2020 acumula **+66.8%**, pero sigue **−29.6%** respecto de su pico de dic-2006 [34].
- **Rentabilidad y calidad en 2025-2026:**
  - RMW (rentabilidad operativa de FF) perdió **−10.2%** en 2025 y **−5.8%** en ene-jul 2026 [34].
  - QMJ de EUA (AQR) perdió **−11.2%** en 2025 y QMJ global −9.8% [21].
  - *Inferencia:* 2025 fue un año de "basura sobre calidad". La calidad no es cobertura garantizada en todos los regímenes.
- **Diferencial de valuación (AQR, nov-2025):** percentil **75-80** histórico, amplio pero no extremo [35].

**Anomalías fundamentales**
- **PEAD, 2025-2026.** Dickerson-Julliard-Mueller y Hirshleifer-Peng-Wang (2025) reportan drift "vivo" (t ≈ 2.2 y ≈ 14) [38]. Subrahmanyam (SSRN 2025; *Journal of Investment and Management* 2026) replica: sin microcaps, t = 1.43. **El PEAD existe solo en microcaps**, lo que reconcilia esos resultados con Martineau [38][39].
- **Yu, Liu, Zhang y He** (arXiv, 29-jun-2026), S&P 1500 2022-2025 [61]:
  - La sorpresa numérica se elimina antes de la siguiente apertura.
  - El tono de la llamada de resultados tiene su máximo al día siguiente y sería operable.
  - Es un working paper (grado C).
- **Intangibles.** Lin Li (arXiv, may-2025): la inversión en intangibles casi no predice rendimientos en 1963-1992 y los predice con fuerza en 1993-2022, por encima de HML y RMW [59] (working paper, grado C).

**Aprendizaje automático, LLMs y verificabilidad (crítico para un sistema de IA)**
- **Cao, Jiang, Wang y Yang (JFE 160, 2024):**
  - Un "analista IA" supera a la mayoría de los analistas humanos cuando la información es transparente pero voluminosa.
  - Los humanos ganan cuando importa el conocimiento institucional (intangibles, estrés financiero).
  - "Humano + máquina" reduce los errores extremos [45].
- **van Binsbergen, Han y Lopez-Lira (RFS 36(6), 2023)** construyen un pronóstico de utilidades con ML y encuentran que el sesgo de los analistas predice rendimientos negativos [43].
  - Zhang, Zhu y Linnainmaa ("Man versus Machine Learning Revisited", RFS 38(12), dic-2025) atribuyen el resultado a **look-ahead bias**: al quitarlo, **el alfa desaparece**, y los modelos lineales pronostican igual de bien [44].
  - La RFS publicó una **Expression of Concern** sobre el artículo original (vol. 39(5), mayo de 2026) [43].
- **Kim, Muhn y Nikolaev, "Financial Statement Analysis with Large Language Models"** (arXiv 2407.17866) afirmaba que GPT-4 supera a los analistas prediciendo la dirección de las utilidades. **Fue retirado el 20-feb-2025** porque un coautor encontró inconsistencias de datos al replicarlo. Otro trabajo de los mismos autores ("Bloated Disclosures") también se retiró [46].
- **Lopez-Lira, Tang y Zhu (abr-2025)** [47]:
  - Los LLMs **memorizan** datos económicos y financieros previos a su fecha de corte.
  - Pedirles que "no usen el futuro" no lo evita, y enmascarar nombres tampoco, porque reconstruyen la entidad y la fecha con muy poco contexto.
  - Consecuencia: el desempeño de un LLM dentro de su periodo de entrenamiento **no está identificado**.

---

## 5. Evidencia real: qué funciona, qué no, magnitudes netas y decaimiento

### 5.1 Factores fundamentales antes y después de su publicación (EUA, long-short, brutos, en USD; cálculo propio con French y AQR a jul-2026)

| Factor | Antes | Rend. geom. anual / Sharpe | Después | Rend. geom. anual / Sharpe |
|---|---|---|---|---|
| HML (value; FF 1992) | 1963-07 a 1991-12 | 4.23% / 0.52 (t = 2.75) | 1992-01 a 2026-07 | 2.19% / 0.25 (t = 1.45) |
| HML, subperiodo | 1992-2006 | 7.61% / 0.72 | 2007-2020 | **−5.67%**; DD máx. de −57.8% |
| RMW (rentabilidad; FF 2015) | 1963-07 a 2013-12 | 2.95% / 0.41 (t = 2.94) | 2014-01 a 2026-07 | 2.23% / 0.30 (t = 1.08) |
| CMA (inversión) | 1963-07 a 2013-12 | 3.72% / 0.56 | 2014-01 a 2026-07 | **−1.10%** / −0.10 |
| QMJ EUA (AFP 2013) | 1957-07 a 2012-12 | 3.96% / 0.56 | 2013-01 a 2026-07 | 2.53% / 0.29 |
| QMJ global ex-EUA | 1989-07 a 2012-12 | 6.12% / 0.85 | 2013-01 a 2026-07 | **4.82% / 0.86** |

Lectura:
1. En EUA, todas las primas fundamentales se debilitaron después de publicarse, en línea con McLean-Pontiff (−58%) [48].
2. **QMJ fuera de EUA mantuvo su Sharpe.** El F-score internacional también sobrevivió, con ~+10% anual en 2000-2018 [17]. *Inferencia:* la ventaja fundamental sobrevive donde hay menos arbitraje y cobertura de analistas. Esto es relevante para México, pero no hay una réplica verificada del F-score o de QMJ en la BMV.
3. Son cifras **brutas** y long-short. Una implementación long-only minorista en GBM captura solo la pata larga, con toda la beta. Novy-Marx y Velikov (2016) estiman costos de ejecución de **20-57 pb** por operación para anomalías de turnover medio [52].

### 5.2 Veredicto por señal

| Señal | Evidencia post-publicación | Magnitud neta realista | Grado |
|---|---|---|---|
| Value B/M clásico | −57.8% de 2006 a 2020; recuperación parcial desde 2021; 2026 positivo | EUA: ~0-2% anual long-short bruto desde 1992 | C (EUA) / B (global) |
| Value con intangibles (HML_INT) | Supera a HML también en las décadas malas (EKP 2022; Arnott et al. 2021) | Mejor que HML, pero con la misma familia de riesgos | B |
| Rentabilidad bruta / RMW / QMJ | Decae en EUA, se mantiene fuera; −10% en 2025 | 2-3% anual bruto en EUA; ~5% ex-EUA | B |
| Value + rentabilidad combinados | Correlación de −0.57 (Novy-Marx): diversificación real | Mejor Sharpe que cada uno solo | B |
| F-score | EUA: practicantes reportan que se invirtió (Portfolio123 2021: pérdidas en 2001-2020) [18]; internacional ~+10% anual [17] | En EUA solo sirve como filtro de riesgo | C (EUA) / B (intl.) |
| Accruals (Sloan) | Desapareció en EUA (Green-Hand-Soliman 2011) | ~0 como alfa en EUA | D (alfa) / B (filtro) |
| M-score | Predice menores rendimientos fuera de muestra (BLN 2013); detecta 50% con 7.2% de falsos positivos | Valor en **evitar** pérdidas | B (veto) |
| PEAD | Muerto en grandes desde 2006; solo en microcaps no operables | ~0 en lo operable | D |
| Drift post-recompra (EUA) | Desaparece en 2003-2012 (Fu-Huang) | ~0 | D (EUA) / B (intl.) |
| Magic formula (Greenblatt) | Réplicas académicas mixtas y mayormente internacionales (Wikipedia recopila 8); reportes de rezago en EUA en los 2010s | Incierta; con alta volatilidad y periodos largos de rezago | C |
| V/P de residual income | Frankel-Lee; Haboub et al. 2025 (WP) | Horizonte de 1-3 años | C |
| LLM "lee estados financieros y gana" | Estudio insignia retirado; problema de memorización; ML con look-ahead | Sin evidencia limpia | D |

### 5.3 Buffett: el mejor caso real también decae con el tamaño (cálculo propio con la tabla de la carta de 2025; diferencia de redondeo de ±0.1 pp)

| Periodo | Berkshire (valor de mercado por acción) | S&P 500 con dividendos |
|---|---|---|
| 1965-1989 | 30.0% | 10.2% |
| 1990-2025 | 13.2% | 10.8% |
| 2011-2025 | **13.0%** | **14.1%** |
| 2016-2025 | 14.3% | 14.8% |

*Inferencia:* 15 años sin exceso de rendimiento para el inversionista fundamental más exitoso documentado. La causa es la escala más la competencia por las mismas ideas. Una cuenta de $20,000 MXN no tiene el problema de escala, pero tampoco tiene el float, el acceso a operaciones privadas ni la información de Berkshire.

### 5.4 La "muerte del value" 2007-2020 y su recuperación: diagnóstico con números
- **Hecho:** HML cayó −57.8% del pico de dic-2006 al valle de sep-2020 (French). Arnott et al. midieron 55% a mediados de 2020 [29][34].
- **Explicaciones con evidencia:**
  - **Contracción del múltiplo relativo.** Arnott et al. encuentran que la caída del diferencial de valuación entre value y growth explica **todo el drawdown**, con holgura. Es una revaluación, no una pérdida de fundamentales.
  - **Intangibles mal medidos:** EKP y Lev-Srivastava [32][33].
  - **Menor reversión** de ganadores y perdedores (Lev-Srivastava).
  - **Estadística:** Fama-French no pueden rechazar que el premio esperado sea igual en ambas mitades de la muestra, porque la volatilidad es demasiado alta [30].
- **Recuperación:** +66.8% de sep-2020 a jul-2026, pero con dos años negativos (2023-2024). En nov-2025 el diferencial seguía en el percentil 75-80 [35].
- *Inferencia:* value es una prima de alta varianza y de horizonte de décadas. Esa varianza no cabe en una temporada de 6 meses.

---

## 6. Traducción operable (cómo lo usa el sistema para ganar)

Toda cifra de riesgo viene de `config/parametros.json`. En **fase 0** (`prioridad_actual.fase = 0`) el sistema no propone operaciones reales: las reglas se aplican al portafolio de papel y a los pronósticos registrados.

### 6.1 Reglas
1. **La valuación entra primero como filtro y veto, y solo después como fuente de alfa.** Los usos con mejor evidencia neta, en orden:
   - (a) **vetar** pérdidas previsibles (M-score, accruals extremos, F-score bajo en nombres value, dilución);
   - (b) **no pagar de más**: el DCF inverso contra las tasas base;
   - (c) **inclinar** el satélite hacia value + rentabilidad combinados, nunca value puro.
2. **Vetos duros** para comprar cualquier acción individual (papel o real):
   - M-score > −1.78.
   - Accruals totales / activo en el decil más alto del universo.
   - F-score ≤ 2 si la acción es value (P/B en el quintil más bajo).
   - Dilución neta > 3% anual.
   - FCF/utilidad neta < 0.7 por 2 años seguidos.
   - SBC > 10% de ingresos sin descontarlo del FCF.
   - Estos umbrales son heurísticos (los tres últimos son los de `herramientas/dossier.py`). Cualquier excepción se escribe con su razón.
3. **Costo de capital estándar del sistema:**
   - ERP = la más reciente de Damodaran, actualizada el día 1 de cada mes (hoy: 4.09% vs T-bond y 4.31% vs r_f ajustada).
   - r_f = T-bond − diferencial de default de EUA.
   - Para emisoras con ingresos en México: CRP de 2.72%, ponderado por λ = fracción de ingresos en México.
   - Conversión a MXN por diferencial de inflación (§2.3).
   - La tasa se reporta con su rango. El `--tasas` de `dossier.py` se fija en ±150 pb alrededor del WACC calculado.
4. **Valor terminal:**
   - g ≤ r_f nominal de la moneda.
   - RONIC terminal = WACC, salvo un moat documentado con 3 fuentes (§2.8).
   - Si el VT pesa más de 75% del valor, se exige un margen de seguridad de 30% en lugar de 20%.
5. **Regla de compra por valuación (papel en fase 0; real desde la fase 1):**
   - Precio ≤ 0.8 × valor del escenario base, y valor ponderado por probabilidad (3 escenarios que suman 100%) > precio.
   - El crecimiento implícito del DCF inverso debe ser ≤ al percentil 75 de las tasas base del sector y tamaño.
   - Venta: si el precio supera el valor ponderado o la tesis se invalida por un dato fechado.
6. **Dimensionamiento:**
   - Riesgo por operación ≤ `riesgo_por_operacion.max_riesgo_pct_capital` = 1%, y 0.5% en fase de prueba.
   - Acción individual ≤ `concentracion.accion_individual_max` = 10%; sector ≤ 25%; núcleo ≥ 70% indexado.
   - En la cuenta `arena-claude` (perfil `arena_agresivo`): riesgo por operación de 3%, acción ≤ 30% y ≤ 8 operaciones al mes.
   - Kelly fraccional ≤ 0.25 (estándar) o 0.5 (arena), sobre una ventaja **recortada 50%** respecto del backtest (McLean-Pontiff).
7. **El horizonte manda.** Las señales fundamentales convergen en 1-3 años (Frankel-Lee; Bartram-Grinblatt: ~34 meses). Una tesis de valuación sin catalizador fechado **no justifica** exposición táctica en una temporada de 6 meses (`temporada_meses`). En la arena, el análisis fundamental se usa como veto y para elegir el vehículo; la exposición la definen el régimen y la tendencia (módulos de momentum y riesgo).
8. **Temporada de reportes:**
   - No se opera PEAD en emisoras grandes: no existe desde 2006.
   - Se pronostica: antes de cada reporte se registran punto e intervalo de 80% para ingresos y UPA, más probabilidades binarias, con `herramientas/pronosticos.py` (objetivo Brier ≤ 0.20, mínimo 50 pronósticos).
   - La señal del tono de la llamada (Yu et al. 2026) queda en observación, sin capital, hasta replicarla con los criterios de `validacion_estrategias`.
9. **Recompras:** se premia la recompra neta (descontada la SBC) a precio menor que el valor. En EUA, un anuncio de recompra **no** es señal de compra (Fu-Huang). En México y otros mercados menos eficientes, puede ser un factor de desempate (Manconi et al.).
10. **Higiene de IA** (el sistema es un LLM):
    - Nunca usar la memoria del modelo para cifras financieras históricas: cada dato se descarga con fecha y fuente.
    - Ningún backtest que use juicio de LLM cuenta como evidencia si su periodo cae antes de la fecha de corte del modelo (Lopez-Lira et al. 2025).
    - Todo modelo de ML de utilidades se prueba con datos *point-in-time* para evitar el look-ahead (Zhang-Zhu-Linnainmaa 2025).
11. **Admisión de un factor fundamental al satélite:**
    - Backtest ≥ 10 años con costos y slippage.
    - Deflated Sharpe ≥ 0.95 y PBO ≤ 0.25.
    - Papel ≥ 3 meses y ≥ 30 operaciones.
    - Arranque con 25% del capital asignado (`validacion_estrategias`).
    - Evidencia de grado ≥ B en al menos 2 regiones después de su publicación (§5.2).
12. **Rachas y cortacircuitos:** si 3 tesis fundamentales seguidas pierden, el tamaño baja 50%. Con 5, se pausa la estrategia y se revisa si la ventaja sigue viva (`rachas`). Los cortacircuitos de drawdown siempre dominan a cualquier convicción de valuación.

### 6.2 Checklist del expediente de valuación (se integra en `empresas/<TICKER>/ficha.md` mediante la skill `ficha-empresa`)
- [ ] Datos primarios con fecha: 10-K/10-Q o reporte BMV/Emisnet; precio y conteo de acciones diluido.
- [ ] Cadena causal: acontecimiento → exposición → efecto económico → estado financiero → valuación → precio.
- [ ] Ajustes: arrendamientos, I+D capitalizado, SBC como gasto, partidas no recurrentes, minoritarios, pensiones.
- [ ] ROIC contra WACC en 5-10 años; fuentes del moat; CAP estimado.
- [ ] FCFF y FCFE con 3 escenarios que suman 100%; % del valor en el terminal; múltiplo de salida implícito.
- [ ] DCF inverso: crecimiento, margen y ROIC implícitos contra las tasas base.
- [ ] Múltiplos justificados contra pares y contra su propia historia.
- [ ] Calidad: M-score, accruals, F-score, GP/A, conversión de caja, dilución neta.
- [ ] Historial de promesas de la dirección contra resultados, partes relacionadas, y vencimientos y moneda de la deuda.
- [ ] Pronóstico registrado antes del próximo reporte; revisión fechada, sin sobrescribir.

---

## 7. Trampas y errores comunes
1. **Tasa y flujo incoherentes:** FCFF descontado a k_e, flujos en MXN a tasa en USD, o flujos nominales a tasa real.
2. **g terminal > r_f**, o g alto sin reinversión. Es crecimiento gratis, que no existe.
3. **Doble conteo del riesgo:** subir la tasa *y* recortar los flujos por el mismo riesgo país. O cargar el CRP completo a una empresa que vende en EUA.
4. **Beta de regresión de una sola acción,** con error estándar alto. Se usa la beta sectorial (bottom-up).
5. **Ignorar la SBC** ("EBITDA ajustado") y las opciones y RSU vivas en el conteo de acciones.
6. **Tratar el múltiplo de salida como independiente del DCF.** Importa el error del mercado de hoy al año terminal.
7. **P/B bajo = barato.** En la era de intangibles, un P/B bajo a menudo refleja libros inflados o negocios en declive (Lev-Srivastava).
8. **Aplicar el F-score a todo el universo.** Se diseñó para el quintil de alto B/M y su efecto está en chicas sin cobertura. En grandes de EUA, post-publicación, no aporta alfa.
9. **Tomar el M-score como veredicto.** Con 7.2% de falsos positivos, en un universo de 500 empresas marca ~36 honestas. Es un veto de compra, no una tesis para vender en corto.
10. **Confiar en el LTG de consenso.** Los analistas sobreextrapolan (La Porta; BGLS). A sep-2026 el índice descuenta ~14% de crecimiento anual en 5 años.
11. **Backtests in-sample de anomalías publicadas** usados como expectativa. Hay que restar el decaimiento (−26% fuera de muestra y −58% post-publicación) y los costos.
12. **Confundir "value ganó en 2022" con "value regresó".** Una prima de Sharpe ~0.25 necesita décadas para distinguirse de cero (t = 1.45 en 34 años).
13. **LLM como analista con resultados in-sample.** El estudio insignia se retiró y el problema de memorización está documentado.
14. **Recompra = buena noticia.** Solo si el precio es menor que el valor y la recompra neta es positiva.
15. **Anclarse a un valor puntual.** El valor es una distribución. Un DCF sin escenarios ni rangos es falsa precisión.

---

## 8. Examen de titulación

1. **¿A qué tasa se descuenta el FCFF y a cuál el FCFE?** El FCFF al WACC, lo que da el valor operativo. El FCFE a k_e, lo que da el valor del capital.
2. **Con NOPAT₁ = 100, g = 4% y WACC = 10%, ¿cuánto vale la empresa si RONIC = 10%? ¿Por qué?** 1,000 = NOPAT/WACC. Si RONIC = WACC, el crecimiento no crea valor.
3. **¿Cuál era la ERP implícita de Damodaran el 1-sep-2026 y con qué E(R)?** 4.09% sobre el T-bond de 4.75%, con E(R) de 8.84%. Contra la r_f ajustada por default (4.53%), 4.31%.
4. **Calcula el k_e en USD de una emisora mexicana 100% doméstica con β = 1 (jul/sep-2026).** 4.53% + 4.20% + 2.72% ≈ 11.45%.
5. **¿Cuánto pesa el valor terminal en el modelo del S&P de Damodaran de sep-2026 y qué implica?** ~86% del valor. El resultado depende casi todo de los supuestos de largo plazo, así que hay que reportar sensibilidades (±50 pb ≈ +14%/−11%).
6. **P/B justificado con ROE 15%, g 4% y k_e 10%.** (0.15 − 0.04)/(0.10 − 0.04) = 1.83x.
7. **¿Qué hace un DCF inverso y qué se compara al final?** Resuelve el crecimiento, el margen y el ROIC implícitos en el precio, y los compara con las tasas base y con el escenario propio.
8. **Resultados de Piotroski (2000) y su estado actual.** +7.5% anual para value y cobertura de 23% en 1976-1996. En EUA post-publicación no rinde (evidencia de practicantes). Fuera de EUA, ~+10% anual en 2000-2018 (Walkshäusl 2020).
9. **¿Qué mide GP/A y por qué combina bien con value?** (Ventas − COGS)/activo. Rinde 0.31%/mes con alfa FF3 de 0.52% y tiene correlación de −0.57 con value. Juntos mejoran el Sharpe.
10. **Umbral y tasas de error del M-score.** −1.78. En la muestra de control detecta 50% de los manipuladores con 7.2% de falsos positivos.
11. **¿Qué dice Martineau (2022) y cómo se concilia con los papers de 2025?** No hay PEAD en emisoras grandes desde 2006. Los papers de 2025 incluyen microcaps. Sin ellas, el t cae a 1.43 (Subrahmanyam).
12. **Tamaño y fechas de la "muerte del value".** HML −57.8% de dic-2006 a sep-2020. Desde entonces, +66.8%, aún −29.6% bajo el pico (jul-2026).
13. **¿Qué explica el alfa de Buffett según Frazzini-Kabiller-Pedersen?** Exposición a BAB y QMJ con apalancamiento de ~1.7x: acciones baratas, seguras y de calidad, apalancadas. Sharpe de 0.79.
14. **¿Por qué el sistema no confía en un backtest de un LLM sobre 2015-2024?** Porque el LLM memorizó esos datos (Lopez-Lira et al. 2025). Además, estudios clave sufrieron look-ahead o se retiraron (Kim-Muhn-Nikolaev; Zhang-Zhu-Linnainmaa).
15. **¿Cuánto decae en promedio una anomalía publicada?** 26% fuera de muestra y 58% post-publicación (McLean-Pontiff 2016, 97 predictores).

---

## 9. Fuentes

1. Damodaran, "Data Update 2 for 2026" (enero de 2026): https://aswathdamodaran.blogspot.com/2026/01/
2. Damodaran, hoja de ERP implícita de septiembre de 2026: https://pages.stern.nyu.edu/~adamodar/pc/implprem/ERPSept26.xlsx
3. Hojas de ago, jul y ene 2026: https://pages.stern.nyu.edu/~adamodar/pc/implprem/ERPAug26.xlsx ; https://pages.stern.nyu.edu/~adamodar/pc/implprem/ERPJuly26.xlsx ; https://pages.stern.nyu.edu/~adamodar/pc/implprem/ERPJan26.xlsx
4. Damodaran, primas por país (1-jul-2026): https://pages.stern.nyu.edu/~adamodar/pc/datasets/ctrypremJuly26.xlsx
5. Damodaran, "Equity Risk Premiums, by country – July 2026 Update": https://www.linkedin.com/pulse/equity-risk-premiums-country-july-2026-update-aswath-damodaran-zti8c
6. Damodaran, ERP 2026 Edition (SSRN): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6361419
7. Damodaran, "Data Update 4 for 2026": https://aswathdamodaran.substack.com/p/data-update-4-for-2026-a-risk-journey
8. Damodaran, *Investment Valuation* 4a ed. (Wiley): https://www.wiley.com/en-us/shop/general-finance-investments/investment-valuation-university-edition-tools-and-techniques-for-determining-the-value-of-any-asset-4th-edition-p-9781394262731
9. Koller, Goedhart, Wessels, *Valuation* 8a ed.: https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/valuation-measuring-and-managing-the-value-of-companies
10. Mauboussin, Rappaport, *Expectations Investing* (2021): https://cup.columbia.edu/book/expectations-investing/9780231554848/ ; https://www.expectationsinvesting.com/
11. Mauboussin, Callahan, "Measuring the Moat": https://www.morganstanley.com/im/publication/insights/articles/article_measuringthemoat.pdf
12. Mauboussin, Callahan, "ROIC and the Investment Process" (2023): https://www.morganstanley.com/im/publication/insights/articles/article_roicandtheinvestmentprocess.pdf
13. Dechow, Khimich, Sloan, "The Accrual Anomaly" (síntesis): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1793364
14. Green, Hand, Soliman (2011): https://pubsonline.informs.org/doi/abs/10.1287/mnsc.1110.1320
15. Pincus, Rajgopal, Venkatachalam (2007), TAR: https://publications.aaahq.org/accounting-review/article/82/1/169/2913/The-Accrual-Anomaly-International-Evidence
16. Piotroski (2000): https://www.gsb.stanford.edu/faculty-research/publications/value-investing-use-historical-financial-statement-information ; https://papers.ssrn.com/sol3/papers.cfm?abstract_id=249455
17. Walkshäusl (2020): https://link.springer.com/article/10.1057/s41260-020-00157-2
18. Taylor (Portfolio123, feb-2021), "Why Piotroski's F-Score No Longer Works": https://blog.portfolio123.com/why-piotroskis-f-score-no-longer-works/
19. Novy-Marx (2013): https://www.sciencedirect.com/science/article/abs/pii/S0304405X13000044 ; https://mysimon.rochester.edu/novy-marx/research/OSoV.pdf
20. Asness, Frazzini, Pedersen (2019): https://link.springer.com/article/10.1007/s11142-018-9470-2
21. AQR, datos mensuales de QMJ: https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Quality-Minus-Junk-Factors-Monthly.xlsx
22. Beneish (1999): https://www.calctopia.com/papers/beneish1999.pdf
23. Beneish, Lee, Nichols (2013): https://rpc.cfainstitute.org/research/financial-analysts-journal/2013/earnings-manipulation-and-expected-returns
24. Fórmula del M-score: https://en.wikipedia.org/wiki/Beneish_M-score
25. Graham, Dodd, *Security Analysis* 7a ed.: https://www.mheducation.com/highered/mhp/product/security-analysis-seventh-edition-principles-techniques.html
26. Berkshire Hathaway, carta de 2025: https://www.berkshirehathaway.com/letters/2025ltr.pdf
27. Frazzini, Kabiller, Pedersen (2018): https://rpc.cfainstitute.org/research/financial-analysts-journal/2018/faj-v74-n4-3
28. Magic formula, recopilación de réplicas: https://en.wikipedia.org/wiki/Magic_formula_investing
29. Arnott, Harvey, Kalesnik, Linnainmaa (2021): https://www.tandfonline.com/doi/full/10.1080/0015198X.2020.1842704
30. Fama, French (2021): https://academic.oup.com/raps/article-abstract/11/1/105/6033665
31. Israel, Laursen, Richardson (2021): https://www.aqr.com/Insights/Research/Journal-Article/Is-Systematic-Value-Investing-Dead
32. Eisfeldt, Kim, Papanikolaou (2022): https://www.nber.org/papers/w28056 ; https://www.nowpublishers.com/article/Details/CFR-0113
33. Lev, Srivastava (2022): https://www.nowpublishers.com/article/Details/CFR-0115 ; https://cfr.ivo-welch.org/published/papers/lev2021explaining.pdf
34. Kenneth French Data Library (factores FF3 y FF5, archivo CRSP 202607): https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
35. Hedgeweek, "US stocks expensive but not in bubble territory, says AQR boss" (nov-2025): https://www.hedgeweek.com/us-stocks-expensive-but-not-in-bubble-territory-says-aqr-boss/
36. Bernard, Thomas (1989): https://ideas.repec.org/a/bla/joares/v27y1989ip1-36.html
37. Martineau (2022): https://www.nowpublishers.com/article/Details/CFR-0122
38. UCLA Anderson Review, "Is Post-Earnings Announcement Drift a Thing? Again?": https://anderson-review.ucla.edu/is-post-earnings-announcement-drift-a-thing-again/
39. Subrahmanyam, "Keeping it Simple…": https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5930255 ; https://www.sciencepublishinggroup.com/article/10.11648/j.jim.20261501.11
40. La Porta (1996): https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1996.tb05223.x
41. Bordalo, Gennaioli, La Porta, Shleifer (2019): https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12833 ; https://www.nber.org/papers/w23863
42. Bouchaud, Krüger, Landier, Thesmar (2019): https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12734
43. van Binsbergen, Han, Lopez-Lira (2023) y Expression of Concern (2026): https://academic.oup.com/rfs/article/36/6/2361/6782974 ; https://academic.oup.com/rfs/article/39/5/1555/8502599
44. Zhang, Zhu, Linnainmaa (2025): https://academic.oup.com/rfs/article-abstract/38/12/3768/8246070 ; https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4899584
45. Cao, Jiang, Wang, Yang (2024): https://www.sciencedirect.com/science/article/abs/pii/S0304405X24001338
46. Kim, Muhn, Nikolaev (retirado): https://arxiv.org/abs/2407.17866 ; https://faculty.chicagobooth.edu/valeri-nikolaev/ongoing-research-projects
47. Lopez-Lira, Tang, Zhu (2025): https://arxiv.org/abs/2504.14765
48. McLean, Pontiff (2016): https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12365
49. Hou, Xue, Zhang (2020): https://academic.oup.com/rfs/article-abstract/33/5/2019/5236964
50. Jensen, Kelly, Pedersen (2023), JF 78(5):2465-2518: https://onlinelibrary.wiley.com/doi/full/10.1111/jofi.13249
51. Chen, Zimmermann (2022), CFR 11(2): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3604626 ; https://www.openassetpricing.com/
52. Novy-Marx, Velikov (2016): https://academic.oup.com/rfs/article-abstract/29/1/104/1844518
53. Bartram, Grinblatt (2018): https://www.sciencedirect.com/science/article/abs/pii/S0304405X1730315X
54. Ohlson (1995): https://onlinelibrary.wiley.com/doi/10.1111/j.1911-3846.1995.tb00461.x
55. Frankel, Lee (1998): https://www.sciencedirect.com/science/article/pii/S0165410198000263
56. Ikenberry, Lakonishok, Vermaelen (1995): https://www.sciencedirect.com/science/article/abs/pii/0304405X9500826Z
57. Fu, Huang (2016): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1936187
58. Manconi, Peyer, Vermaelen (2019): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2330807
59. Lin Li (2025), arXiv 2505.16336: https://arxiv.org/abs/2505.16336
60. Haboub, Kartsaklas, Sarafidis (2025), arXiv 2506.00206: https://arxiv.org/abs/2506.00206
61. Yu, Liu, Zhang, He (2026), arXiv 2606.29734: https://arxiv.org/abs/2606.29734
62. Expansión, "Banxico mantiene la tasa en 6.5%" (24-sep-2026): https://expansion.mx/economia/2026/09/24/banxico-tasa-de-interes-de-referencia-6-5-septiembre

**Contexto adicional:** Jensen-Kelly-Pedersen (2023) [50] y Chen-Zimmermann (2022) [51] muestran que la mayoría de los factores se replica **en muestra** (98% de los 161 predictores claramente significativos, con t > 1.96, según Chen-Zimmermann). Eso no contradice el decaimiento post-publicación: replicar el pasado no es lo mismo que rendir en el futuro.

**Sin verificar o con verificación parcial en este módulo:**
- La magnitud exacta de la cobertura de Sloan (1996). Hay un rango de 10-12% en fuentes secundarias; el original no se consultó.
- La magnitud del drift en Bernard-Thomas (1989).
- Las cifras de transición de ROIC entre quintiles y la fecha exacta de la versión vigente de "Measuring the Moat" (Morgan Stanley bloqueó la descarga).
- El periodo muestral exacto de "Buffett's Alpha" en la versión de la FAJ.
- El impuesto de 1% a recompras en EUA.
- El rendimiento del bono M a 10 años de septiembre de 2026, por lo que no se usa en los ejemplos.
- El desempeño post-publicación de la magic formula en EUA: solo hay evidencia de practicantes y réplicas internacionales de calidad heterogénea.
- La réplica de F-score, QMJ o value en la BMV.
