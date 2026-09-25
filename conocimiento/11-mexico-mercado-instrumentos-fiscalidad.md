# 11 — México: mercado, instrumentos, fiscalidad y operación

> Nivel: aplicado · Actualizado: 2026-09-25 · Grado de evidencia global: **B**. Las cifras vigentes (Banxico, SIE, FIX, subastas, LISR, LIF 2026, UMA, calificaciones) se tomaron de la fuente primaria o de una nota con fecha y tienen grado A como dato. Las conclusiones de inversión (IPC contra S&P 500, *carry* del peso, cobertura cambiaria, FIBRAs) salen de cálculos propios *in-sample*, brutos y sin costos: grado B. Los temas interpretativos (broker extranjero y art. 129, *situs* del SIC, REFIPRE en ETFs) tienen grado C.

**Convenciones.** "Hecho" lleva fuente y fecha. "**Inferencia:**" es razonamiento propio. "**Regla:**" es una propuesta operable para el sistema y vive en la sección 6. "(nv)" = no verificado en esta sesión. Los números entre corchetes remiten a la sección 9. Cálculos propios: Yahoo Finance (chart v8) y FRED, corte 18-sep-2026 salvo que se diga otra cosa; son brutos, sin impuestos ni costos, e *in-sample*.

**Nota de método (honestidad del proceso):** esta sesión agotó su presupuesto de la herramienta WebSearch antes de empezar. Las búsquedas se hicieron con Google News RSS (≈30 consultas, con los enlaces resueltos al medio original), con las fuentes primarias consultadas directamente (Banxico SIE, FRED, Yahoo, cetesdirecto, gob.mx y el texto de la LISR y la LIF congelado en `laboratorio/replicas/V05-…/datos/legal/`) y con Crossref para confirmar las citas académicas (≈25 consultas).

Capítulos relacionados, que aquí no se repiten: [27 Fiscalidad 2026 y estructura del SIC](27-fiscalidad-2026-y-estructura-sic.md) (*estate tax* de EUA, UCITS irlandeses, SPIVA) · [16 Macro, divisas y el peso](16-macro-global-divisas-y-el-peso.md) · [04 Renta fija, tasas y macro](04-maestria-renta-fija-tasas-macro.md) · `arena/investigacion/01-gbm-operativa-y-costos.md` (comisiones y operativa de GBM).

---

## 1. Objetivos de dominio

Quien "se titula" en este módulo debe poder:

1. **Leer el tablero México en 5 minutos:** tasa objetivo, TIIE de Fondeo, curva de CETES, Bonos M y UDIBONOS, *breakeven*, FIX, inflación general y subyacente. Y decir qué descuenta el mercado.
2. **Comparar bien el IPC contra el S&P 500:** con dividendos, en la misma moneda y en el mismo periodo, y contra CETES como tasa libre de riesgo local.
3. **Elegir instrumento y canal:** BMV/BIVA, SIC, cetesdirecto, broker de EUA, Afore/PPR. Con costo total (comisión + IVA + *spread* + impuesto) y con el riesgo de contraparte correcto (Indeval, IPAB, SIPC).
4. **Calcular el impuesto** de cada flujo: ganancia bursátil al 10%, dividendos (10% adicional + acumulación), intereses reales, distribuciones de FIBRA, deducción de PPR.
5. **Decidir si cubrir el tipo de cambio,** con números: correlación del peso con el S&P 500, diferencial de tasas y costo real del ETF cubierto.
6. **Mapear los riesgos país vigentes:** calificación a un escalón del grado especulativo, Pemex, revisiones anuales del T-MEC, remesas, nearshoring y riesgo institucional. Y traducirlos a disparadores operables.
7. **Operar sin errores de calendario:** horario de la BMV frente a NYSE, días inhábiles, liquidación T+1 y liquidez del SIC.

---

## 2. Núcleo teórico

### 2.1 Tasa libre de riesgo local y tasa real después de impuestos

- **Rendimiento de un CETE** (descuento, base 360): precio $P = \frac{10}{1 + r \cdot d/360}$, con valor nominal de 10 pesos. La "tasa de rendimiento" de la subasta es $r$.
- **Tasa real ex ante:** $r_{real} \approx r_{nominal} - \pi^e$. **Después de impuestos** para una persona física: el ISR se causa sobre el **interés real** (art. 134 LISR), acumulado a la tasa marginal (hasta 35%). $r_{real,neta} \approx (r - \pi)(1 - t_{marg})$.
- **Ejemplo con datos vigentes:** CETE 28 en 6.15% [3], inflación de 3.42% [2] y $t_{marg}$ = 35% → real bruta ≈ 2.73% → real neta ≈ **1.8%**. **Inferencia:** para el dueño, en el tramo alto, el "6%" de CETES rinde menos de 2% real neto.
- La **retención provisional de 0.90% anual se aplica sobre el capital**, no sobre el interés (art. 24 LIF 2026; art. 135 LISR) [8][9]. Equivale a ~15% del interés nominal de un CETE a 6.15%. En la declaración anual se compara contra el impuesto sobre el interés real.

### 2.2 Paridad de tasas, *carry* y *peso problem*

- **Paridad cubierta:** $F/S = (1 + i_{MXN})/(1 + i_{USD})$. Por eso cubrir dólares a pesos "paga" aproximadamente el diferencial $i_{MXN} - i_{USD}$. Es la fuente del rendimiento extra de un ETF del S&P 500 cubierto a pesos.
- **Paridad descubierta (UIP):** predice que la moneda de tasa alta se deprecia en el diferencial. Empíricamente falla: Fama (1984) documenta el sesgo de la prima *forward* [45], y el *carry* (largo en la moneda de tasa alta) gana en promedio.
- **Exceso de retorno del *carry* MXN, en USD:** $rx_{t+1} = (1 + i_{MXN,t})\frac{S_t}{S_{t+1}} - (1 + i_{USD,t})$, con $S$ en MXN por USD.
- **Peso problem:** el término nació con el peso mexicano. Krasker (1980) [46] mostró que una probabilidad pequeña de devaluación grande sesga las pruebas de eficiencia del *forward*. El *carry* gana poco a poco y pierde de golpe: tiene sesgo negativo (Brunnermeier, Nagel y Pedersen, 2008 [48]).
- **Por qué el *carry* paga:** es compensación por riesgo sistemático, porque las monedas de tasa alta pierden cuando sube la volatilidad cambiaria global (Menkhoff, Sarno, Schmeling y Schrimpf, 2012 [49]). Lustig, Roussanov y Verdelhan (2011) [50] lo resumen en un factor global (HML_FX).

### 2.3 Cobertura cambiaria desde la óptica de un inversionista en pesos

- Rendimiento en MXN de un activo en USD: $(1 + R_{USD})(1 + \Delta S) - 1$. La varianza depende de $\rho(R_{USD}, \Delta S)$.
- Si el dólar sube cuando las bolsas caen ($\rho(R_{S\&P}, \Delta USDMXN) < 0$), **no cubrir reduce la varianza en pesos**. Campbell, Serfaty-de Medeiros y Viceira (2010) [51] documentan que el USD, el euro y el franco suizo se mueven contra las bolsas mundiales, y que al inversionista global en bonos le conviene casi la cobertura completa.
- **Inferencia:** para un mexicano, el S&P 500 sin cobertura es un activo de riesgo que trae su propio seguro (el dólar). El ETF cubierto cambia ese seguro por el diferencial de tasas.

### 2.4 Riesgo soberano en moneda local

- Du y Schreger (2016) [52]: el *spread* de crédito en moneda local (bono local contra la tasa libre de riesgo sintética vía *cross-currency swaps*) es "positive and sizable". Tiene menor media, menor correlación entre países y menor sensibilidad global que el *spread* en moneda extranjera.
- Hofmann, Shim y Shin (2020) [53]: en emergentes, la apreciación de la moneda comprime los *spreads* soberanos, **incluso en moneda local**, por la vía de la prima de crédito. El tipo de cambio que importa es el **bilateral contra el USD**.
- **Inferencia para México:** peso fuerte, Bonos M que suben y spreads que se comprimen son el mismo trade. Cuando se revierte, pegan juntos. Un portafolio "diversificado" en IPC + Bonos M + peso es, en crisis, una sola apuesta.

### 2.5 Régimen fiscal: fórmulas clave (LISR vigente, última reforma DOF 01-04-2024 [8])

| Flujo | Regla | Artículo |
|---|---|---|
| Ganancia en acciones y ETFs de BMV/BIVA y SIC | 10% definitivo sobre (precio de venta − comisiones) − (costo promedio **actualizado por INPC** + comisiones), neteado por emisora y año | 129 |
| Pérdida bursátil | Solo contra ganancias del art. 129 del mismo año o de los **10 siguientes**; se pierde si pudiendo aplicarse no se aplica | 129 |
| Dividendo de emisora mexicana | 10% adicional retenido + acumulación con acreditamiento del ISR corporativo | 140 |
| Dividendo extranjero (SIC o broker) | Acumulación + 10% adicional; retención de EUA de 10% con W-8BEN (tratado) o 30% sin él | 142-V; tratado art. 10 |
| Intereses | Se acumula el **interés real**; la retención de 0.90% sobre el capital es provisional; con ingresos por intereses ≤ 100,000 MXN se puede tomar la retención como definitiva; la pérdida real se aplica contra otros ingresos (no contra sueldos ni actividad empresarial) hasta 5 años | 134, 135; LIF 2026 art. 24 |
| FIBRA: distribución del resultado fiscal | Retención de 30% (tasa del art. 9); el tenedor acumula y acredita | 188-IV, V |
| FIBRA: reembolso de capital | No es ingreso; reduce el costo fiscal | 188-IX |
| FIBRA: ganancia en venta por bolsa | **Exenta** para personas físicas residentes | 188-X |
| PPR y aportaciones complementarias | Deducibles hasta 10% de los ingresos acumulables, tope de 5 UMA anuales. **No** cuentan para el tope global de deducciones personales | 151-V y último párrafo |
| Cuentas personales especiales de ahorro | Diferimiento hasta $152,000 por año | 185 |
| Ventas vía entidad financiera extranjera | El contribuyente calcula la ganancia y conserva los estados de cuenta | 129 (párrafo sobre entidades extranjeras) |

---

## 3. Literatura canónica

| Autores | Año | Título | Revista/Editorial | Hallazgo clave cuantificado | Enlace/DOI | Grado |
|---|---|---|---|---|---|---|
| Krasker | 1980 | The 'peso problem' in testing the efficiency of forward exchange markets | Journal of Monetary Economics | Una devaluación poco probable pero grande sesga las pruebas de eficiencia del *forward*. El caso es el peso mexicano | 10.1016/0304-3932(80)90031-8 | B |
| Fama | 1984 | Forward and spot exchange rates | Journal of Monetary Economics | La prima *forward* no predice la depreciación con pendiente 1: sesgo de la prima *forward* (cualitativo aquí) | 10.1016/0304-3932(84)90046-1 | A |
| Brunnermeier, Nagel, Pedersen | 2008 | Carry Trades and Currency Crashes | NBER Macroeconomics Annual | El *carry* tiene sesgo negativo y se desarma cuando se seca la liquidez de fondeo (cualitativo) | 10.1086/593088 | A |
| Burnside, Eichenbaum, Kleshchelski, Rebelo | 2011 | Do Peso Problems Explain the Returns to the Carry Trade? | Review of Financial Studies 24 | El *carry* cubierto con opciones sigue siendo rentable: el premio no se explica solo por pérdidas raras; refleja el valor del factor de descuento en esos estados (cualitativo) | 10.1093/rfs/hhq138 | B |
| Lustig, Roussanov, Verdelhan | 2011 | Common Risk Factors in Currency Markets | Review of Financial Studies 24 | Un factor global HML_FX explica el corte transversal de portafolios de divisas ordenados por tasa (cualitativo) | 10.1093/rfs/hhr068 | A |
| Menkhoff, Sarno, Schmeling, Schrimpf | 2012 | Carry Trades and Global Foreign Exchange Volatility | Journal of Finance | Las monedas de tasa alta rinden poco cuando la volatilidad cambiaria global sube por sorpresa; ese riesgo domina al de liquidez | 10.1111/j.1540-6261.2012.01728.x | A |
| Koijen, Moskowitz, Pedersen, Vrugt | 2018 | Carry | Journal of Financial Economics 127 | El *carry* predice rendimientos en todas las clases de activos (cualitativo) | 10.1016/j.jfineco.2017.11.002 | B |
| Du, Schreger | 2016 | Local Currency Sovereign Risk | Journal of Finance 71 | El *spread* de crédito en moneda local es positivo y considerable, con menor media y menor beta global que el de moneda extranjera | 10.1111/jofi.12389 | B |
| Hofmann, Shim, Shin | 2020 | Bond Risk Premia and the Exchange Rate | Journal of Money, Credit and Banking | La apreciación contra el USD comprime *spreads* soberanos de emergentes, incluso en moneda local | 10.1111/jmcb.12760 | B |
| Harvey | 1995 | Predictable Risk and Returns in Emerging Markets | Review of Financial Studies 8 | Rendimientos de emergentes altos, volátiles y más predecibles que los desarrollados (cualitativo) | 10.1093/rfs/8.3.773 | B (decae con la integración) |
| Bekaert, Harvey | 2000 | Foreign Speculators and Emerging Equity Markets | Journal of Finance 55 | La liberalización baja el costo de capital **entre 5 y 75 pb** | 10.1111/0022-1082.00220 | B |
| Rouwenhorst | 1999 | Local Return Factors and Turnover in Emerging Stock Markets | Journal of Finance 54 | En emergentes hay *momentum*, tamaño y valor; beta alta no rinde más | 10.1111/0022-1082.00151 | B |
| Bekaert, Harvey, Lundblad | 2007 | Liquidity and Expected Returns: Lessons from Emerging Markets | Review of Financial Studies 20 | La iliquidez está preciada en emergentes (cualitativo) | 10.1093/rfs/hhm030 | B |
| Campbell, Serfaty-de Medeiros, Viceira | 2010 | Global Currency Hedging | Journal of Finance 65 | 1975-2005: USD, euro y franco suizo se mueven contra las bolsas. En bonos conviene casi la cobertura completa | 10.1111/j.1540-6261.2009.01524.x | A/B |
| Perold, Schulman | 1988 | The Free Lunch in Currency Hedging | Financial Analysts Journal | Sostiene que cubrir reduce el riesgo sin costo esperado. Inferencia: para el inversionista en MXN no aplica (ver 5.4) | 10.2469/faj.v44.n3.45 | C |
| French, Poterba | 1991 | Investor Diversification and International Equity Markets | AER P&P (NBER w3609) | Sesgo local: los inversionistas concentran en su país más de lo que justifica la diversificación (cualitativo) | 10.3386/w3609 | A |
| Calvo, Reinhart | 2002 | Fear of Floating | Quarterly Journal of Economics 117 | Muchos "flotadores" declarados intervienen y temen a la flotación (cualitativo) | 10.1162/003355302753650274 | B |
| Calvo, Mendoza | 1996 | Mexico's balance-of-payments crisis: a chronicle of a death foretold | Journal of International Economics 41 | Anatomía de la crisis de 1994-95: deuda corta dolarizada (Tesobonos) y fragilidad bancaria | 10.1016/S0022-1996(96)01436-5 | B (histórico) |
| Sachs, Tornell, Velasco | 1996 | Financial Crises in Emerging Markets: The Lessons from 1995 | Brookings Papers on Economic Activity | Contagio del "tequila" según fundamentales (tipo de cambio real, auge crediticio, reservas) | 10.2307/2534648 | B (histórico) |
| Miranda-Agrippino, Rey | 2020 | U.S. Monetary Policy and the Global Financial Cycle | Review of Economic Studies 87 | La política monetaria de EUA mueve el ciclo financiero global de activos de riesgo y de crédito (cualitativo) | 10.1093/restud/rdaa019 | A/B |
| Asness, Moskowitz, Pedersen | 2013 | Value and Momentum Everywhere | Journal of Finance 68 | Valor y *momentum* en 8 clases de activos, incluidas divisas, con correlación negativa entre sí | 10.1111/jofi.12021 | A |

---

## 4. Lo más reciente 2023-2026 (fecha de cada dato)

### 4.1 Política monetaria, inflación y tasas (a 25-sep-2026)

- **Banxico mantuvo la tasa objetivo en 6.50%** el 24-sep-2026, **por unanimidad**. Fue la tercera pausa seguida (25-jun, 6-ago y 24-sep) [1][2]. El comunicado dice: "la política monetaria no tendría que reaccionar de manera mecánica ante los ajustes previstos a la tasa de fondos federales" [2].
- **Trayectoria** (listado oficial [1]):

| Fecha | Acción | Nivel |
|---|---|---|
| 8-feb-2024 | Pausa | 11.25% |
| 21-mar, 8-ago, 26-sep, 14-nov y 19-dic-2024 | −25 pb cada una | 10.00% al cierre de 2024 |
| 6-feb, 27-mar, 15-may y 26-jun-2025 | −50 pb cada una | 8.00% |
| 7-ago, 25-sep, 6-nov y 18-dic-2025 | −25 pb cada una | 7.00% al cierre de 2025 |
| 5-feb-2026 | Pausa | 7.00% |
| 26-mar y 7-may-2026 | −25 pb cada una | 6.50% |
| 25-jun, 6-ago y 24-sep-2026 | Pausa | 6.50% |

  Total del ciclo: **−475 pb** desde marzo de 2024. Las fechas de las decisiones restantes de 2026: (nv).
- **Inflación** (INEGI, citada por Banxico [2]): la general pasó de 3.10% a **3.42%** entre la 1a quincena de julio y la 1a de septiembre de 2026, por la no subyacente. La subyacente bajó de 3.95% a **3.79%**. Banxico espera converger a la meta de 3% en el **4T-2027** y ve el balance de riesgos "con sesgo al alza".
- **Contexto externo:** la Fed **subió 25 pb** en septiembre de 2026, a un rango de **3.75%-4.00%** (FRED DFEDTARL/DFEDTARU, 24-sep) [2][6]. El Treasury a 10 años está en **5.11%** (23-sep; 4.47% el 1-jun) y el Brent en **114.89 USD** (22-sep) [6]. El VIX está en 14.21 (22-sep) [6].
- **TIIE de Fondeo a un día:** **6.53%** (24-sep-2026). La TIIE 28 se sigue publicando: 6.7860% el 25-sep [4].
- **Curva gubernamental** (subastas primarias de Banxico, SIE CF107, fecha de colocación [3]):

| Instrumento | Rendimiento | Subasta |
|---|---|---|
| CETE 28 d | 6.15% | 22-sep-2026 |
| CETE 91 d | 6.59% | 22-sep-2026 |
| CETE 182 d | 6.91% | 22-sep-2026 |
| CETE 364 d | 7.24% | 15-sep-2026 |
| CETE 728 d | 8.01% | 22-sep-2026 |
| Bono M 3 años | 8.24% | 8-sep-2026 |
| Bono M 5 años | 9.00% | 15-sep-2026 |
| Bono M 10 años | 9.35% | 22-sep-2026 |
| UDIBONO 3 años | 4.00% real | 22-sep-2026 |
| UDIBONO 10 años | 4.75% real | 8-sep-2026 |
| UDIBONO 30 años | 4.90% real | 15-sep-2026 |
| BONDES F 1, 3 y 7 años | Precio 99.935, 99.537 y 98.809 | 22-sep-2026 |

  **Inferencia:** la curva está muy empinada: +320 pb entre el CETE 28 y el Bono M a 10 años. El *breakeven* aproximado a 10 años es (1.0935/1.0475) − 1 ≈ **4.4%** (fechas de subasta distintas), por arriba de la meta de 3%. El mercado cobra prima por inflación, por plazo y fiscal. BONDES F debajo de 100 = sobretasa positiva sobre la TIIE de Fondeo.
- **BONDES G y Bono S** (sostenibles): el 14-may-2026 se colocaron 35 mil millones de pesos, con demanda de 2.62 veces. Los BONDES G son "de tasa flotante, referenciados a la TIIE de Fondeo", con sobretasas de 0.147% (2 años) a 0.208% (5 años). El Bono S a 10 años tiene cupón de 8% y rindió 9.24% [33].

### 4.2 Peso y sus *drivers*

- **Nivel:** FRED DEXMXUS **17.2454** (18-sep-2026) [6]. **FIX de Banxico 17.6425** y cierre de 17.7148 (24-sep-2026) [5]. Rango de 12 meses: 16.863 (4-sep-2026) a 18.620 (6-nov-2025) [6]. **Inferencia:** el peso se depreció ~2.7% en una semana: Fed al alza, Treasuries arriba de 5% y petróleo arriba de 110 USD.
- ***Carry*:** diferencial de política de 250 pb (6.50% contra 4.00%). CETE 28 menos T-bill 3m (4.04%, 23-sep) = **2.1 pp** [3][6]. La volatilidad realizada del USD/MXN es de 5.2% (21 días), 6.3% (63 días) y 7.6% (252 días) [6]. **Inferencia:** *carry*/volatilidad ≈ 0.33, bajo contra el promedio de 5.1-5.5 pp de diferencial en 2021-2026 (cálculo propio con IR3TIB01MXM156N − TB3MS [6]). El colchón que protegía al peso es la mitad del de 2023.
- **Remesas:** en 2025 cayeron **4.6%**, a **61,791 millones de USD**, la primera caída desde 2013 [19]. En enero-julio de 2026 suben **3.1%** (36,349 millones de USD) y julio sumó 5,571 millones, +3.0% [20]. Desde el 1-ene-2026 EUA cobra un **impuesto de 1%** a los envíos en efectivo [21]. Benavides Perales y Borrego-Salcido (2026, REMEF) [54] estiman con un VECM que las remesas tienen un "limited effect" sobre el tipo de cambio: domina la cuenta corriente.
- **Nearshoring:** la IED fue **récord en 2025, 40,871 millones de USD** [23]. En el 1S-2026 sumó 34,968 millones (+2.1%), pero **88.5% fueron reinversión de utilidades y solo 7.8% (2,726 millones) inversión nueva**. EUA aportó 48.2% [22]. En la literatura: Alfaro y Chor (2023, NBER w31661) documentan una "great reallocation": baja el abasto directo de EUA desde China y ganan Vietnam y **México** [55]. Freund, Mattoo, Mulabdic y Ruta (2024, JIE) [56] estudian si los aranceles de EUA reconfiguran las cadenas (no se extrajeron cifras). **Inferencia:** la narrativa de nearshoring es real en comercio, pero no en capital nuevo. Solo 1 de cada 13 dólares de IED en 2026 es proyecto nuevo.
- **T-MEC:** el 1-jul-2026, en la revisión conjunta, **EUA no extendió el acuerdo**. Se abre un ciclo de **revisiones anuales hasta el vencimiento en 2036** (Ebrard: "las revisiones son anuales, durante la vigencia del tratado que es hasta 2036") [17]. La cuarta ronda bilateral (aranceles de acero, aluminio y autos, más ~12 temas mexicanos frente a 54 demandas de EUA) **se aplazó a octubre de 2026** [18].
- **Riesgo institucional:** reforma judicial de 2024 con elección de jueces en 2025 (nv en esta sesión; ver capítulo 23). Moody's justifica su rebaja por el "debilitamiento sostenido de la solidez fiscal" y el apoyo a Pemex [11][12]. No la atribuye explícitamente a la reforma judicial en las notas revisadas.

### 4.3 Calificaciones (a 25-sep-2026)

| Emisor | S&P | Moody's | Fitch |
|---|---|---|---|
| México (soberano, moneda extranjera) | **BBB, negativa** (12-may-2026) [13][14] | **Baa3, estable** (20-may-2026, desde Baa2 negativa) [12] | **BBB-, estable** (ratificada en abr-2026) [11] |
| Pemex | **BBB, negativa** (13-may-2026) [14] | **B1** (pie de foto de El Financiero del 24-sep-2026; confirmar) [16] | **BB+, estable** (ratificada ~24-sep-2026; perfil individual "ccc"; dos escalones debajo del soberano) [15] |

- México queda **a un escalón del grado especulativo** con Moody's y Fitch [11]. Moody's recortó su pronóstico de PIB a menos de 1.0% en 2026 y 1.3% en 2027 [12]. Estima que Pemex necesitará **al menos 10,000 millones de USD al año del gobierno durante 5 años** [16].
- **Inferencia:** si una segunda agencia baja a México a grado especulativo, habrá ventas forzadas de mandatos que exigen grado de inversión. La regla de salida de índices como el WGBI: (nv). Es el principal riesgo de cola de 2026-2027 para Bonos M y para el peso.

### 4.4 Mercado accionario, SIC, FIBRAs, Afores

- **Rebalanceo del IPC:** S&P DJI publicó el 5-sep-2026 los resultados preliminares. Televisa salió (cayó 10% el 7-sep) y **Alpek entró**, con efecto el **21-sep-2026**. Ese día Televisa subió 8.75%, Alpek cayó 1.66% y el IPC cerró en 63,536.96 [29][30]. Televisa ocupaba la posición 33 de 36 [30].
- **SIC:** más de **2,100 emisoras internacionales** (El CEO, 3-sep-2026). **SpaceX quedó disponible en el SIC el 14-sep-2026**, al cumplir tres meses de su salida a bolsa [27]. Cumplió 20 años en 2023 (creado en jun-2003) y entonces representaba **42%** del importe operado en la BMV [28].
- **Afores:** comisión promedio de 2026 de **0.538%** (desde 0.547%): nueve Afores en 0.54% y PensionISSSTE en 0.52% [34]. Plusvalías de enero-agosto de 2026: 475,433 millones de pesos, −37% anual [35]. Composición: 51.3% deuda gubernamental local, 13.7% renta variable internacional, 11.3% deuda privada local, 7.8% estructurados, 6.8% renta variable local, 3.1% FIBRAs [35]. **Inferencia:** activos ≈ 8.9 billones de pesos, porque las plusvalías acumuladas de 4.90 billones son "55% de los activos" [35].
- **SIEFOREs generacionales:** en la migración quinquenal del 26-ago-2024 se creó la SIEFORE Básica 95-99 (240,678 millones de pesos desde la Inicial) y la 55-59 pasó a Pensiones (121,340 millones). Hoy hay **8 generacionales + Inicial + Pensiones** [36].
- **CKDs/CERPIs:** régimen de inversión de las Afores con tope de **30% en estructurados** (20% original + 10% adicional de oct-2025). La exposición a CKDs + CERPIs bajó de 8.9% (dic-2024) a **8.3%** (abr-2026) por el vencimiento de CKDs de la década pasada [37].

### 4.5 Intermediarios y regulación

- **Caso Vector (2025):** la CNBV intervino Vector Casa de Bolsa el 2-jul-2025, tras los señalamientos del Tesoro de EUA por presunto lavado de dinero [38]. La cartera pasó a **Finamex** (oct-2025) [39]. La lección de la interventora: los valores están "bajo custodia del Instituto para el Depósito de Valores". Pero **el IPAB excluye a las casas de bolsa**, y el efectivo es lo vulnerable [38].
- **Horario:** la BMV y BIVA operan de **7:30 a 14:00 (CDMX) del 9-mar al 30-oct-2026**, y regresan a **8:30-15:00 el martes 3-nov-2026** (el 2-nov es inhábil) [24][25]. Así se mantienen alineadas con NYSE (9:30-16:00 ET) porque México eliminó el horario de verano en 2022 (el Senado aprobó la Ley de los Husos Horarios el 26-oct-2022) [26]. BIVA replica el ajuste [25]; opera desde el 25-jul-2018 [42].

### 4.6 Papers y datos nuevos de interés

- **BIS Bulletin 90** (Aquilina, Lombardi, Schrimpf y Sushko, 27-ago-2024): el desarme de *carry* de agosto de 2024 golpeó fuerte a los *carry trades* de divisas. La posición en yenes se estimó en ~40 billones de yenes (250 mil millones de USD) [57]. El boletín no da cifras específicas del peso (en la versión revisada).
- **SPIVA Latin America** (primer semestre de 2025): 73.17% de los fondos mexicanos de renta variable quedaron debajo del S&P/BMV IRT a 10 años (capítulo 27, réplica V05) [44].

---

## 5. Evidencia real: qué funciona, qué no y con qué magnitud

### 5.1 IPC contra S&P 500 contra CETES (cálculo propio; corte 18-sep-2026; bruto, *in-sample*)

| Serie (anualizado) | 1 año | 3 años | 5 años | 10 años |
|---|---|---|---|---|
| IPC precio, MXN | 3.35% | 7.03% | 4.32% | 3.27% |
| IPC precio, USD | 10.09% | 6.76% | 7.44% | 4.41% |
| NAFTRAC ajustado (aprox. IPC con dividendos, neto de TER), MXN | 6.40% | 10.92% | 7.59% | **5.77%** |
| NAFTRAC ajustado, USD | 13.34% | 10.63% | 10.81% | 6.93% |
| S&P 500 TR, USD | 16.71% | 21.35% | 13.14% | 15.49% |
| S&P 500 TR, MXN | 9.56% | 21.66% | 9.85% | **13.98%** |
| CETES (FRED INTGSTMXM193N, capitalización mensual, aprox.) | — | — | ~9.1% | **~7.8%** |
| USD/MXN (+ = peso se deprecia) | — | — | −2.9%/año | −1.3%/año |

Fuentes: Yahoo (^MXX, NAFTRAC.MX, ^SP500TR) y FRED (DEXMXUS, INTGSTMXM193N) [6][7]. Años calendario: en **2025**, IPC +29.9% en MXN (+50.4% en USD) y S&P 500 TR +17.9% en USD (+1.8% en MXN). En **2026 al 18-sep**, IPC −1.5% en MXN y S&P 500 TR +12.7% en USD (+8.0% en MXN).

**Lectura:**
1. **A 10 años, la bolsa mexicana con dividendos (~5.8%) rindió menos que CETES (~7.8%)**: prima de riesgo accionario ex post **negativa** en pesos. A 5 años también (7.6% contra 9.1%). El S&P 500 en pesos rindió 14.0%, casi el doble que CETES. Esto es *in-sample* y antes de impuestos; y el ISR de 10% sobre la ganancia real castiga menos a la bolsa que la tasa marginal sobre intereses. Aun así, la brecha es enorme.
2. **La moneda de medición cambia el veredicto:** en 2025 el IPC en USD (+50%) aplastó al S&P 500. En MXN, el S&P 500 apenas ganó 1.8% porque el peso se apreció de 20.86 a 18.01.
3. **Inferencia:** el sesgo local (French y Poterba, 1991) le costó al inversionista mexicano ~8 pp al año durante una década. El caso a favor del IPC es táctico (valuación, flujos, 2025), no estructural.

### 5.2 El *carry* del peso (cálculo propio, mensual, fin de mes; largo MXN fondeado en USD; interbancaria MX 3m contra T-bill 3m; sin costos)

| Periodo | Exceso anual (media aritmética) | Volatilidad | Sharpe | Sesgo | Drawdown máximo | Peor mes |
|---|---|---|---|---|---|---|
| 1997-2026 | 4.94% | 10.55% | 0.47 | −0.94 | −33.0% | −15.5% |
| 2010-2026 | 4.02% | 11.31% | 0.36 | −0.84 | −33.0% | −15.5% |
| 2016-2026 | 6.14% | 11.70% | 0.52 | −1.00 | −20.0% | −15.5% |
| 2021-2026 | 8.21% | 8.40% | 0.98 | −0.51 | −16.9% | −6.5% |
| 2008 | −15.65% | 15.42% | — | — | −25.1% | −13.1% |
| 2024 | −14.35% | 8.96% | — | — | −16.9% | −6.5% |
| 2025 | +19.89% | 4.72% | — | — | −0.8% | −0.8% |
| 2026 (a sep) | +9.58% | 8.12% | — | — | −4.2% | −4.2% |

Fuentes: FRED DEXMXUS, IR3TIB01MXM156N, TB3MS [6].

- **Funciona:** el *carry* MXN tiene prima positiva a largo plazo (Sharpe de 0.36-0.52). Es consistente con la literatura (grado A en el cruce de países, B para una sola moneda).
- **No funciona como "ingreso seguro":** sesgo negativo, un peor mes de −15.5% y un drawdown de −33%. Un año malo (2008, 2024) borra 2-3 años de *carry*. El Sharpe de 0.98 de 2021-2026 es un régimen, no una constante: coincidió con diferenciales de 5-7 pp que hoy son de 2.1 pp.

### 5.3 FIBRAs: rendimiento por distribución (Yahoo, 12 meses a 23-sep-2026; calidad de datos media)

| FIBRA | Precio | Distribución 12m | Rendimiento | Precio a 1 año |
|---|---|---|---|---|
| FUNO11 | 29.34 | 2.53 | ~8.6% | +12.0% |
| FIBRAMQ12 | 44.01 | 3.68 | ~8.4% (fechas irregulares en la fuente) | +54.7% (causa: nv) |
| FMTY14 | 14.18 | 1.07 | ~7.5% | +5.5% |
| DANHOS13 | 29.30 | 1.80 | ~6.1% | +12.0% |
| FIBRAPL14 | 74.88 | 2.83 | ~3.8% | +8.4% |

Referencia: NAFTRAC con dividendo de ~3.6% [7].

- **Inferencia fiscal:** la parte de "resultado fiscal" se acumula a la tasa marginal (hasta 35%) con acreditamiento del 30% retenido. Para el dueño, esa parte de la distribución paga ~35%. El "reembolso de capital" no paga hoy, pero baja el costo, y la ganancia en bolsa está **exenta** (art. 188-X). El rendimiento que se anuncia no es el neto.

### 5.4 ¿Cubrir el dólar? (cálculo propio, S&P 500 TR mensual)

| Periodo | Versión | CAGR | Volatilidad | Drawdown máximo |
|---|---|---|---|---|
| 2000-2026 | USD | 8.32% | 15.13% | −50.9% |
| 2000-2026 | **MXN sin cobertura** | 10.77% | **13.36%** | **−40.1%** |
| 2000-2026 | MXN cubierto (aprox. teórica: USD + diferencial) | 14.58% | 15.06% | −46.2% |
| 2008-2009 | USD | −10.74% | 23.01% | −48.5% |
| 2008-2009 | **MXN sin cobertura** | −2.38% | 15.62% | **−28.8%** |
| 2008-2009 | MXN cubierto (aprox. teórica) | −4.77% | 22.89% | −43.9% |
| 2020 | USD | 18.40% | 24.84% | −19.6% |
| 2020 | **MXN sin cobertura** | 24.88% | 19.57% | **−8.9%** |
| 2020 | MXN cubierto (aprox. teórica) | 24.93% | 24.84% | −18.7% |

Correlación del S&P 500 (USD) con el USD/MXN: **−0.51** en 2000-2026 y en 2010-2026, −0.75 en 2008-09, −0.66 en 2020 [6][7].

- **Resultado:** sin cobertura, el S&P 500 en pesos tuvo **menor volatilidad y ~11 pp menos drawdown** que en dólares. El dólar funciona como seguro de crisis para el mexicano, como predice Campbell et al. (2010). Cubrir cobra el diferencial (+3.8 pp/año teóricos en 2000-2026), pero **quita el seguro justo cuando más se necesita**.
- **Brecha de implementación:** el ETF real **IVVPESO** (iShares S&P 500 Peso Hedged TRAC) rindió 14.60% anual a 5 años. La aproximación teórica da ~18.6% (S&P 500 TR en USD 13.14% + diferencial medio de 5.5 pp). A 1 año: 14.26% contra ~20.3%. **La brecha es de 3-6 pp por año.** Causas: (nv). Posiblemente la serie de Yahoo sin distribuciones, el TER, el costo de los *forwards* y la base. **No hay que suponer que el ETF cubierto entrega todo el diferencial.**

### 5.5 Costos reales de acceso (hechos)

- **GBM (Trading MX: BMV, BIVA, SIC):** 0.25% + IVA = **0.29% por lado**, 0.58% por vuelta completa, hasta 1 millón de MXN operados en promedio de 3 meses. El W-8BEN del SIC cuesta 75 USD + IVA. Smart Cash paga 4.00% con menos de 300 mil MXN (doc `01`) [43].
- **Interactive Brokers:** acciones de EUA en IBKR Pro Fixed a **0.005 USD por acción, mínimo 1.00 USD** y máximo 1% del valor; IBKR Lite es solo para residentes de EUA. En la **BMV cobra 0.1% del valor, mínimo 60 MXN** [41]. **Inferencia:** para una orden de 5,000 MXN en la BMV, el mínimo de 60 MXN equivale a 1.2%, peor que GBM (0.29%). Para acciones de EUA de 5,000 USD, la comisión es ~0.02-0.1%, muy abajo de GBM.
- **Hapi:** sin comisión de broker, con cargos de ejecución de ~0.10 USD (títulos completos) o 0.15 USD (fracciones). Registrada ante la SEC, miembro de FINRA y SIPC, liquida con Apex; desde 5 USD [40]. *Spread* cambiario: (nv).
- **cetesdirecto:** desde 100 MXN, "No pagas ningún tipo de comisión"; es de Nacional Financiera. Ofrece CETES a 28, 91, 182 y 364 días, Bonos (3-30 años), UDIBONOS, BONDES F y BONDDIA [32].
- **Actinver, Kuspit, Bursanet, Flink:** comisiones vigentes (nv). Sus sitios no mostraron tarifas en la consulta.

---

## 6. Traducción operable (coherente con `config/parametros.json`)

### 6.1 Marco

- **Objetivo del sistema:** CAGR en MXN con drawdown acotado. Benchmark principal: **50% S&P 500 TR en MXN + 50% CETES 28** (`objetivo.benchmark_principal`). Cada idea de México se mide contra ese benchmark, no contra el IPC.
- **Cuenta arena** (`cuentas[0]`): 20,000 MXN en GBM, TWR en MXN por temporadas de 6 meses. `orden_minima_mxn` = 5,000. `operaciones_max_mes` = 8. `rotacion_max_mensual_x_capital` = 1.5. Riesgo por operación de 3%. `concentracion.accion_individual_max` = 30%. `etf_apalancado_max` = 50%, con el filtro de SMA200 y VIX < 25.
- **Fase 0** (`prioridad_actual`): nada de lo siguiente se ejecuta con dinero real antes de aprobar el examen y la validación en papel. Toda regla táctica nueva pasa por `validacion_estrategias`: backtest de 10 años o más, con costos, DSR ≥ 0.95, PBO ≤ 0.25 y 3 meses o 30 operaciones en papel.

### 6.2 Reglas de asignación y moneda

1. **Regla (núcleo, patrimonio principal): la exposición accionaria de EUA va sin cobertura cambiaria por omisión.** Evidencia: la tabla 5.4 muestra −11 pp de drawdown máximo y −1.8 pp de volatilidad en MXN, con ρ = −0.51. El IPC es satélite, no núcleo (tabla 5.1).
2. **Regla (arena, táctica; requiere validación):** el ETF cubierto (IVVPESO) solo se considera si se cumplen las tres condiciones: (a) CETE 28 − T-bill 3m ≥ 4.0 pp; (b) VIX < 20; (c) USD/MXN debajo de su SMA de 200 días. **Hoy falla (a): el diferencial es de 2.1 pp → sin cobertura.** El costo de implementación observado (5.4) obliga a descontar al menos 3 pp del diferencial teórico.
3. **Regla:** el *carry* MXN no se usa como fuente de rendimiento del satélite mientras *carry*/volatilidad sea < 0.5. Hoy está en ~0.33.
4. **Regla (disparador soberano):** si una segunda agencia (Moody's o Fitch) baja a México a grado especulativo, en el patrimonio principal se lleva la duración en Bonos M a ≤ 3 años y se revisa el peso dentro de 24 horas. En la arena se aplica `cortacircuitos_drawdown` sin excepciones. Moody's y Fitch se revisan cada semana.
5. **Regla (T-MEC):** el mes de cada ronda o revisión anual (la próxima es en oct-2026) es un **evento de alto riesgo** para autos, acero y el peso. No se abren posiciones tácticas en esas emisoras en los 3 días hábiles previos al anuncio.

### 6.3 Reglas de liquidez y renta fija

6. **Regla:** el efectivo que no se usará en 5 días hábiles o más va a instrumentos gubernamentales. En el patrimonio principal: cetesdirecto o CETES directos (6.15% contra 4.00% de Smart Cash con menos de 300 mil). En la arena: Smart Cash, porque sacar el dinero de GBM rompe la operación y la diferencia en 6 meses, aun con los 20 mil completos en efectivo, es de ~215 MXN (2.15 pp × 20,000 × 0.5; inferencia). Si GBM permite comprar un CETE directo desde la app: (nv, verificar).
7. **Regla:** la tasa real neta se calcula siempre (2.1). Con el dueño en el tramo de 35%, CETES rinde ~1.8% real neto. Solo "gana" contra una alternativa si esta rinde más después del 10% del art. 129.
8. **Regla:** duración en pesos (Bonos M) solo en el patrimonio principal, nunca en la arena. Tamaño con la misma regla de concentración del emisor soberano. Pemex no se compra como deuda privada (`emisor_deuda_privada_max` = 5% como techo, y la preferencia es 0% por su perfil individual "ccc" [15]).

### 6.4 Reglas fiscales

9. **Regla (PPR):** en el patrimonio principal, aportar cada año a un PPR hasta el menor de 10% de los ingresos acumulables o **5 UMA anuales = 213,973.20 MXN en 2026** (5 × 42,794.64 [10]). Con tasa marginal de 35%, la deducción equivale a ~74,900 MXN de ISR diferido: el rendimiento libre de riesgo más alto disponible. El retiro antes de los 65 años se acumula (art. 151-V). Tope exento al retiro: (nv).
10. **Regla (FIBRAs):** para el dueño, las FIBRAs se tienen por su ganancia de capital exenta y por su diversificación, no por su "rendimiento" bruto. La parte de resultado fiscal paga ~35% efectivo (5.3).
11. **Regla (pérdidas, art. 129):** en noviembre, cosechar pérdidas contra ganancias del año (capítulo 27). Registrar por emisora el costo actualizado en `bitacora/operaciones.csv`.
12. **Regla (broker extranjero):** por ahora no se abre cuenta en IBKR para operar acciones de EUA con la expectativa del 10%. El art. 129 fr. I exige, para acciones extranjeras, que la venta sea "en las bolsas de valores concesionadas" de México. El párrafo sobre "entidades financieras extranjeras" obliga al contribuyente a calcular él mismo. La aplicación del 10% a ventas en NYSE vía un broker extranjero tiene **grado C**; la postura conservadora es el régimen general, hasta 35%. **Consulta con contador antes de usar un broker extranjero.**
13. **Regla (REFIPRE):** un ETF o fondo extranjero minoritario no activa REFIPRE, porque el capítulo "sólo será aplicable cuando el contribuyente ejerza el control efectivo" (art. 176). Pero la ley **presume** el control salvo prueba en contrario. Conservar la evidencia de participación minoritaria (estado de cuenta y número de acciones en circulación).

### 6.5 Checklist operativo (antes de cada orden en México)

| # | Verificación | Umbral |
|---|---|---|
| 1 | ¿Día hábil en México y en EUA? | Si la BMV cierra y NYSE abre, no dejar órdenes del SIC abiertas (riesgo de *gap*) |
| 2 | Horario | 7:30-14:00 CDMX hasta el 30-oct-2026; 8:30-15:00 desde el 3-nov-2026 |
| 3 | Liquidez del SIC | ≥ 90% de sesiones con volumen y mediana diaria ≥ 20 veces la orden (capítulo 27) |
| 4 | Tipo de orden | Limitada en el SIC; no a mercado en la apertura |
| 5 | Costo por vuelta | 0.58% + *spread* ≤ 25% del movimiento esperado → movimiento ≥ 5% (`nota_rotacion`) |
| 6 | Impuesto | ¿Art. 129 (10%), dividendos (10% + acumulación) o intereses (real)? |
| 7 | Riesgo de evento | ¿Banxico, Fed, INEGI, T-MEC o calificadora en las próximas 48 horas? |
| 8 | Límites | `limites_perdida` del perfil activo y cortacircuitos vigentes |

---

## 7. Trampas y errores comunes

1. **Comparar el IPC de precio contra el S&P 500 con dividendos**, o en monedas distintas. A 10 años, el IPC de precio rinde 3.3% y con dividendos 5.8%: la diferencia es de 2.5 pp por año.
2. **Declarar "México barato, entonces compro"** sin ver que en 10 años el IPC con dividendos no le ganó a CETES. La prima accionaria local no está garantizada.
3. **Leer el 6.15% de CETES como ganancia.** Después de inflación e ISR marginal es ~1.8% real para el tramo alto. Y la retención de 0.90% es sobre el capital: con tasas de 6%, se come 15% del interés nominal en flujo.
4. **Tomar el "rendimiento" de una FIBRA como neto:** mezcla resultado fiscal (retención de 30%) con reembolso de capital (baja el costo fiscal).
5. **Creer que el IPAB protege en una casa de bolsa.** No lo hace. Los valores en Indeval sí están segregados. El efectivo y los reportos dependen de la solvencia y de la operación del intermediario (caso Vector, 2025).
6. **Usar listas viejas de apps:** Vector ya no opera; su cartera pasó a Finamex.
7. **Cubrir el dólar por reflejo** "para no tener riesgo cambiario". Para el inversionista en pesos, el dólar reduce el drawdown en crisis (−28.8% contra −48.5% en 2008-09). Cubrirlo convierte un seguro en una apuesta de *carry*.
8. **Suponer que el ETF cubierto entrega todo el diferencial.** IVVPESO quedó 3-6 pp por año debajo de la aproximación teórica.
9. **Tratar el *carry* como renta fija:** sesgo de −0.9, peor mes de −15.5% y 2024 en −14%. El Sharpe de 2021-2026 (0.98) es de régimen.
10. **Confundir la TIIE 28 con la TIIE de Fondeo:** los BONDES F y G usan la de Fondeo (6.53%). La TIIE 28 (6.79%) sigue publicándose, pero es otra tasa.
11. **Leer la "calificación BBB" de S&P como holgada:** Moody's y Fitch ya están a un escalón del grado especulativo, y S&P tiene perspectiva negativa.
12. **Leer la IED récord como nearshoring nuevo:** 88.5% es reinversión de utilidades y solo 7.8% es inversión nueva (1S-2026).
13. **Suponer que el 10% aplica a todo lo bursátil:** vender acciones de EUA en NYSE con un broker extranjero es interpretativo (grado C). Las pérdidas del art. 129 no se restan de sueldos ni de intereses.
14. **Olvidar el calendario:** hay días en que la BMV cierra y NYSE abre. Una posición del SIC queda congelada mientras el subyacente se mueve.
15. **Comprar en el SIC con orden a mercado en la apertura o en emisoras sin volumen:** *spreads* amplios; IUSA tuvo volumen en 14 de 213 sesiones (capítulo 27).
16. **Pensar que las remesas sostienen al peso:** cayeron 4.6% en 2025 y el peso se apreció igual. La evidencia VECM (2026) les da un efecto limitado.

---

## 8. Examen de titulación

1. **¿Cuál es la tasa objetivo de Banxico al 25-sep-2026 y cuánto se ha recortado desde marzo de 2024?**
   6.50% (decisión unánime del 24-sep-2026). Desde 11.25% son −475 pb, con pausas el 25-jun, el 6-ago y el 24-sep-2026.

2. **Con CETE 28 en 6.15%, inflación de 3.42% y tasa marginal de 35%, ¿cuál es la tasa real neta aproximada?**
   (6.15 − 3.42) × (1 − 0.35) ≈ **1.8%**. Se grava el interés real (art. 134), y la retención de 0.90% sobre el capital es solo un pago provisional.

3. **¿Qué rindió más en 10 años al 18-sep-2026 en pesos: IPC con dividendos, CETES o S&P 500 TR?**
   S&P 500 TR en MXN ~14.0% > CETES ~7.8% > NAFTRAC (IPC con dividendos) ~5.8%.

4. **¿Por qué en 2025 el IPC "le ganó" al S&P 500 y en pesos el S&P 500 apenas subió?**
   El IPC subió 29.9% en MXN y 50.4% en USD porque el peso se apreció de 20.86 a 18.01. El S&P 500 TR subió 17.9% en USD, pero solo 1.8% en MXN.

5. **¿Por qué, históricamente, un mexicano no debería cubrir el dólar del S&P 500 por omisión?**
   Porque ρ(S&P 500, USD/MXN) ≈ −0.5: el dólar sube cuando la bolsa cae. En 2000-2026, sin cobertura, la volatilidad fue de 13.4% contra 15.1% y el drawdown de −40% contra −51%. Cubrir cobra el diferencial, pero quita ese seguro.

6. **Menciona tres rasgos del *carry* MXN de 1997-2026.**
   Exceso de ~4.9% anual, Sharpe de ~0.47, sesgo de −0.94, drawdown máximo de −33% y peor mes de −15.5%. Además, hoy el diferencial es de solo 2.1 pp.

7. **¿Cómo tributa la distribución de una FIBRA y la venta de sus CBFIs en bolsa para una persona física?**
   El resultado fiscal tiene retención de 30%, se acumula y se acredita (art. 188-IV y V). El reembolso de capital reduce el costo. La ganancia en venta por bolsa está exenta (art. 188-X).

8. **¿Cuál es el tope de deducción de un PPR en 2026?**
   El menor de 10% de los ingresos acumulables y 5 UMA anuales: 5 × 42,794.64 = 213,973.20 MXN. No entra en el tope global de 15% o 5 UMA (último párrafo del art. 151).

9. **Tienes 50,000 MXN de pérdida bursátil en 2026 y 1 millón de sueldo. ¿Qué haces con la pérdida?**
   Solo se resta de ganancias del art. 129 de 2026 o de los 10 años siguientes, actualizada. No se resta del sueldo, y se pierde si pudiendo aplicarse no se aplica.

10. **¿Qué protege y qué no protege a un cliente de casa de bolsa en México?**
    Protege la custodia segregada de valores en Indeval, con supervisión de la CNBV. No lo protege el IPAB, que excluye a las casas de bolsa. Ejemplo: Vector (intervenida el 2-jul-2025; su cartera pasó a Finamex).

11. **¿A qué hora abre la BMV el 28-oct-2026 y el 4-nov-2026 (hora CDMX), y por qué cambia?**
    7:30 el 28-oct y 8:30 el 4-nov. La BMV sigue el horario de verano de EUA para abrir con NYSE, porque México eliminó el suyo en 2022.

12. **¿Calificación soberana de México por agencia al 25-sep-2026?**
    S&P BBB con perspectiva negativa, Moody's Baa3 estable (rebaja del 20-may-2026) y Fitch BBB- estable. Moody's y Fitch están a un escalón del grado especulativo.

13. **¿Qué pasó con el T-MEC el 1-jul-2026 y qué implica?**
    EUA no extendió el acuerdo. Hay revisiones anuales hasta el vencimiento en 2036, y la cuarta ronda se aplazó a octubre de 2026. Es riesgo de evento recurrente para autos, acero y el peso.

14. **¿La IED récord prueba el nearshoring?**
    No por sí sola. En el 1S-2026, de 34,968 millones de USD, 88.5% fue reinversión de utilidades y solo 7.8% inversión nueva.

15. **¿Qué BONDES referencian la TIIE de Fondeo y qué sobretasa pagaron los BONDES G en mayo de 2026?**
    BONDES F y BONDES G. Los BONDES G pagaron de 0.147% (2 años) a 0.208% (5 años) sobre la TIIE de Fondeo, con demanda de 2.62 veces.

---

## 9. Fuentes

**Banxico, datos de mercado y cálculos propios**
1. Banxico, "Anuncios de las decisiones de política monetaria" (listado 2024-2026, consultado el 25-sep-2026). https://www.banxico.org.mx/publicaciones-y-prensa/anuncios-de-las-decisiones-de-politica-monetaria/anuncios-politica-monetaria-t.html
2. Banxico, comunicado de política monetaria del 24-sep-2026 (PDF): https://www.banxico.org.mx/publicaciones-y-prensa/anuncios-de-las-decisiones-de-politica-monetaria/%7B7D0BDB6E-E519-9C69-04AA-ABD4D31E4850%7D.pdf
3. Banxico SIE, cuadro CF107 "Valores Gubernamentales. Resultados de la subasta semanal" (observaciones al 24-sep-2026): https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?sector=22&accion=consultarCuadro&idCuadro=CF107&locale=es
4. Banxico SIE, cuadro CF101 "Tasas de interés en el mercado de dinero" (TIIE de Fondeo, TIIE 28, al 25-sep-2026): https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?sector=18&accion=consultarCuadro&idCuadro=CF101&locale=es
5. Banxico, Mercado cambiario, FIX y cierre de jornada (24-sep-2026): https://www.banxico.org.mx/tipcamb/llenarTiposCambioAction.do?idioma=sp
6. FRED (St. Louis Fed): DEXMXUS, IR3TIB01MXM156N, TB3MS, DTB3, INTGSTMXM193N, DFEDTARU/DFEDTARL, DGS10, DGS2, VIXCLS, DCOILBRENTEU, T10YIE. https://fred.stlouisfed.org/series/DEXMXUS
7. Yahoo Finance chart API vía `herramientas/datos.py` (^MXX, NAFTRAC.MX, ^GSPC, ^SP500TR, EWW, IVVPESO.MX, VOO.MX, CSPXN.MX, FUNO11.MX, FIBRAPL14.MX, FMTY14.MX, DANHOS13.MX, FIBRAMQ12.MX). Scripts en el *scratchpad* de la sesión (m11_hedge.py, carry.py, ipc2.py). https://finance.yahoo.com/quote/%5EMXX/

**Leyes, fiscalidad y previsión social**

8. Ley del Impuesto sobre la Renta, texto vigente (última reforma DOF 01-04-2024), arts. 129, 134, 135, 140, 142, 151, 176, 185, 187 y 188: https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf (copia congelada en `laboratorio/replicas/V05-spiva-y-fiscalidad-sic/datos/legal/LISR.txt`)
9. Ley de Ingresos de la Federación 2026, art. 24 (0.90%): https://www.diputados.gob.mx/LeyesBiblio/pdf/LIF_2026.pdf
10. KPMG México, "Flash Inegi: valor de la UMA para 2026" (8-ene-2026): https://kpmg.com/mx/es/tendencias/2026/01/flash-inegi-valor-de-la-uma-para-2026.html

**Calificaciones y Pemex**

11. Bloomberg Línea, "México queda en el último escalón de grado de inversión con Moody's y Fitch" (21-may-2026): https://www.bloomberglinea.com/latinoamerica/mexico/mexico-queda-en-el-ultimo-escalon-de-grado-de-inversion-con-moodys-y-fitch/
12. El Financiero, "Moody's Ratings rebaja la calificación de México a 'Baa3'" (20-may-2026): https://www.elfinanciero.com.mx/economia/2026/05/20/moodys-ratings-rebaja-la-calificacion-de-mexico-a-baa3/
13. UnoTV, "S&P ratifica calificación BBB a México, pero cambia perspectiva a negativa" (12-may-2026; titular): https://www.unotv.com/negocios/sp-ratifica-calificacion-crediticia-de-mexico-en-bbb-pero-baja-perspectiva-a-negativa/
14. Bloomberg Línea, "S&P extiende perspectiva negativa de México a las estatales Pemex y CFE" (13-may-2026): https://www.bloomberglinea.com/latinoamerica/mexico/sp-extiende-perspectiva-negativa-de-mexico-a-las-estatales-pemex-y-cfe/
15. Revista Fortuna, "Refrenda Fitch nota internacional de Pemex en 'BB+' con perspectiva estable" (24-sep-2026): https://revistafortuna.com.mx/2026/09/24/refrenda-fitch-nota-internacional-de-pemex-en-bb-con-perspectiva-estable/
16. El Financiero, "Moody's trae un pronóstico gris para Pemex: necesitará 10 mil mdd al año del gobierno por 5 años" (24-sep-2026): https://www.elfinanciero.com.mx/economia/2026/09/24/moodys-trae-un-pronostico-gris-para-pemex-necesitara-10-mil-mdd-al-ano-del-gobierno-por-5-anos/

**Macro, comercio, remesas e IED**

17. Excélsior, "T-MEC tendrá revisión anual hasta 2036; 20 de julio, próxima reunión" (2-jul-2026): https://www.excelsior.com.mx/nacional/t-mec-tendra-revision-anual-hasta-2036-20-julio-proxima-reunion
18. El Universal, "México y Estados Unidos aplazan cuarta ronda del T-MEC" (24-sep-2026): https://www.eluniversal.com.mx/cartera/mexico-y-estados-unidos-aplazan-cuarta-ronda-del-t-mec-negociacion-sobre-aranceles-de-acero-aluminio-y-autos-continua/
19. El CEO, "Remesas a México caen en 2025 por primera vez desde 2013" (3-feb-2026): https://elceo.com/economia/remesas-a-mexico-caen-en-2025-por-primera-vez-desde-2013/
20. Forbes México, "Remesas a México hilan en julio seis meses con incrementos" (1-sep-2026): https://forbes.com.mx/remesas-a-mexico-hilan-en-julio-seis-mes-con-incrementos/
21. Univision, "Qué efectos tendrá el impuesto a las remesas… que entra en vigor este 1 de enero" (1-ene-2026): https://www.univision.com/noticias/dinero/impacto-impuesto-remesas-ley-fiscal-trump-entrada-en-vigor-2026
22. Secretaría de Economía, "México registra un máximo histórico de IED para un primer semestre: 34 mil 968 millones de dólares en 2026" (24-ago-2026): https://www.gob.mx/se/prensa/mexico-registra-un-maximo-historico-de-inversion-extranjera-directa-ied-para-un-primer-semestre-34-mil-968-millones-de-dolares-en-2026
23. El Financiero, "Inversión Extranjera Directa en México logra cifra histórica en 2025 con 40,871 mdd" (25-feb-2026; titular): https://www.elfinanciero.com.mx/economia/2026/02/25/mexico-logra-historica-cifra-de-inversion-extranjera-directa-en-2025/

**Mercado, horario e instrumentos**

24. Axis Negocios, "BMV adelantará inicio de operación desde el 9 de marzo por cambio de horario en EUA" (4-mar-2026): https://www.axisnegocios.com/breves.phtml?id=146701
25. Expansión, "La Bolsa Mexicana de Valores deja atrás su 'horario de verano'" (31-oct-2025): https://expansion.mx/mercados/2025/10/31/bolsa-mexicana-regresa-horario-apertura-cierre
26. Senado de la República, "Pleno del Senado aprueba dictamen para expedir Ley de los Husos Horarios en México" (26-oct-2022; titular): https://comunicacionsocial.senado.gob.mx/informacion/comunicados/4104-pleno-del-senado-aprueba-dictamen-para-expedir-ley-de-los-husos-horarios-en-mexico
27. El CEO, "Así puedes invertir en Disney y Apple a través del SIC de la BMV; SpaceX estará disponible el 14 de septiembre" (3-sep-2026): https://elceo.com/mercados/asi-puedes-invertir-en-el-sic-de-la-bmv-donde-puedes-acceder-a-valores-de-disney-nvidia-y-apple/
28. Expansión, "¿Qué es el SIC en la Bolsa de Valores?" (23-sep-2023): https://expansion.mx/mercados/2023/09/23/sistema-internacional-de-cotizaciones-bmv-20-anos
29. El CEO, "Acciones de Televisa suben 8.75% en su primera sesión fuera del IPC; Alpek cae en su regreso" (21-sep-2026): https://elceo.com/mercados/acciones-de-televisa-suben-8-75-en-su-primera-sesion-fuera-del-ipc-de-la-bmv-alpek-cae-en-su-regreso/
30. El Cronista, "Golpe histórico a Televisa: se hunde 10% en la bolsa tras perfilarse su reemplazo en el IPC por Alpek" (7-sep-2026): https://www.cronista.com/mexico/finanzas-economia/golpe-historico-a-televisa-se-hunde-10-en-la-bolsa-tras-perfilarse-su-reemplazo-en-el-ipc-por-alpek/
31. Milenio, "Seis empresas concentran 60% de la muestra del IPC: BMV" (3-ene-2023; solo titular; los pesos vigentes a sep-2026 no se verificaron): https://www.milenio.com/negocios/empresas-concentran-60-muestra-ipc-bmv
32. cetesdirecto (Nafin), portal: https://www.cetesdirecto.com/sites/portal/inicio
33. Hoja de Ruta Digital, "Hacienda celebra la segunda subasta simultánea de Bondes G y Bono S de 2026" (16-may-2026): https://hojaderutadigital.mx/hacienda-celebra-la-segunda-subasta-simultanea-de-bondes-g-y-bono-s-de-2026/

**Afores, CKDs y CERPIs**

34. El CEO, "Consar aprueba nuevas comisiones para las Afores; esto es lo que cobrarán en 2026" (21-nov-2025): https://elceo.com/economia/estos-seran-los-nuevos-cobros-de-las-afores-en-2026/
35. Yahoo Noticias, "Plusvalías de los ahorros en las Afores registran caída de 37% anual hasta agosto" (15-sep-2026): https://es-us.noticias.yahoo.com/plusval%C3%ADas-ahorros-afores-registran-ca%C3%ADda-161445244.html
36. CONSAR, "Se llevó a cabo la migración quinquenal de Siefores Generacionales" (2024): https://www.gob.mx/consar/articulos/se-llevo-a-cabo-la-migracion-quinquenal-de-siefores-generacionales
37. Funds Society, "AFOREs: el reto en inversiones alternativas ahora es la oferta local" (4-jun-2026): https://www.fundssociety.com/es/opinion/afores-el-reto-en-inversiones-alternativas-ahora-es-la-oferta-local/

**Intermediarios**

38. El CEO, "Tras intervención a Vector, ¿qué tan protegidos están sus clientes?" (2-jul-2025): https://elceo.com/mercados/tras-intervencion-a-vector-que-tan-protegidos-estan-sus-clientes/
39. El Economista, "Vector transfiere cartera a Finamex" (2-oct-2025; titular): https://www.eleconomista.com.mx/opinion/vector-transfiere-cartera-finamex-20251002-779693.html
40. Hapi, sitio oficial (comisiones, SEC/FINRA/SIPC, Apex): https://hapi.trade/es
41. Interactive Brokers, "Commissions: Stocks, ETFs and Warrants" (EUA y México): https://www.interactivebrokers.com/en/pricing/commissions-stocks.php
42. CNBV, "48/2018, Inicio de Operaciones Bolsa Institucional de Valores" (25-jul-2018; titular): https://www.gob.mx/cnbv/prensa/48-2018-inicio-de-operaciones-bolsa-institucional-de-valores
43. Documento interno `arena/investigacion/01-gbm-operativa-y-costos.md` (comisiones GBM 0.25% + IVA, W-8BEN de 75 USD + IVA, Smart Cash, T+1), con fuentes oficiales de GBM ahí citadas: https://gbm.com/faqs/
44. Capítulo interno `conocimiento/27-fiscalidad-2026-y-estructura-sic.md` y réplica V05 (SPIVA Latin America; *estate tax*; UCITS). SPIVA LatAm: https://www.spglobal.com/spdji/es/documents/spiva/spiva-latin-america-mid-year-2025-es.pdf

**Literatura académica** (verificada en Crossref el 25-sep-2026)

45. Fama (1984), JME: https://doi.org/10.1016/0304-3932(84)90046-1
46. Krasker (1980), JME: https://doi.org/10.1016/0304-3932(80)90031-8
47. Burnside, Eichenbaum, Kleshchelski, Rebelo (2011), RFS 24: https://doi.org/10.1093/rfs/hhq138
48. Brunnermeier, Nagel, Pedersen (2008), NBER Macroeconomics Annual: https://doi.org/10.1086/593088
49. Menkhoff, Sarno, Schmeling, Schrimpf (2012), JF: https://doi.org/10.1111/j.1540-6261.2012.01728.x
50. Lustig, Roussanov, Verdelhan (2011), RFS 24: https://doi.org/10.1093/rfs/hhr068
51. Campbell, Serfaty-de Medeiros, Viceira (2010), JF 65: https://doi.org/10.1111/j.1540-6261.2009.01524.x
52. Du, Schreger (2016), JF 71: https://doi.org/10.1111/jofi.12389
53. Hofmann, Shim, Shin (2020), JMCB: https://doi.org/10.1111/jmcb.12760
54. Benavides Perales, Borrego-Salcido (2026), "The Medium-Run Equilibrium Exchange Rate, Remittances, and External Adjustment in Mexico", REMEF: https://doi.org/10.21919/remef.v21i2.1543
55. Alfaro, Chor (2023), "Global Supply Chains: The Looming 'Great Reallocation'", NBER w31661: https://www.nber.org/papers/w31661
56. Freund, Mattoo, Mulabdic, Ruta (2024), "Is US trade policy reshaping global supply chains?", JIE 152: https://doi.org/10.1016/j.jinteco.2024.104011
57. Aquilina, Lombardi, Schrimpf, Sushko (2024), BIS Bulletin 90: https://www.bis.org/publ/bisbull90.htm
58. Koijen, Moskowitz, Pedersen, Vrugt (2018), JFE 127: https://doi.org/10.1016/j.jfineco.2017.11.002
59. Harvey (1995), RFS 8: https://doi.org/10.1093/rfs/8.3.773
60. Bekaert, Harvey (2000), JF 55: https://doi.org/10.1111/0022-1082.00220
61. Rouwenhorst (1999), JF 54: https://doi.org/10.1111/0022-1082.00151
62. Bekaert, Harvey, Lundblad (2007), RFS 20: https://doi.org/10.1093/rfs/hhm030
63. Perold, Schulman (1988), FAJ: https://doi.org/10.2469/faj.v44.n3.45
64. French, Poterba (1991), NBER w3609 / AER P&P: https://doi.org/10.3386/w3609
65. Calvo, Reinhart (2002), QJE 117: https://doi.org/10.1162/003355302753650274
66. Calvo, Mendoza (1996), JIE 41: https://doi.org/10.1016/S0022-1996(96)01436-5
67. Sachs, Tornell, Velasco (1996), BPEA: https://doi.org/10.2307/2534648
68. Miranda-Agrippino, Rey (2020), REStud 87: https://doi.org/10.1093/restud/rdaa019
69. Asness, Moskowitz, Pedersen (2013), JF 68: https://doi.org/10.1111/jofi.12021


### Registro de verificación (25-sep-2026)

- **Verificado en fuente primaria:** decisiones de Banxico 2024-2026 y comunicado del 24-sep; subastas de CF107; TIIE de Fondeo y TIIE 28 de CF101; FIX; series de FRED; art. 24 de la LIF 2026; arts. 129, 134, 135, 151, 176, 185, 187 y 188 de la LISR (texto congelado); cetesdirecto; IED de la SE; comisiones de IBKR y Hapi; migración de SIEFOREs de CONSAR.
- **Verificado en nota de prensa con fecha:** calificaciones soberanas y de Pemex (salvo Moody's-Pemex B1, que solo aparece en un pie de foto), T-MEC, remesas, rebalanceo del IPC, SIC y SpaceX, Afores, Vector y Finamex, horario de la BMV, BONDES G y Bono S.
- **No verificado:** pesos vigentes de las emisoras del IPC y su regla de topes; comisiones de Actinver, Kuspit, Bursanet y Flink; fechas de Banxico de nov-dic de 2026; tope exento del retiro del PPR a los 65 años; criterios de salida del WGBI; causa del +54.7% de FIBRAMQ; causas de la brecha de IVVPESO; si GBM permite comprar un CETE directo; reglas de la RMF 2026 sobre ventas vía broker extranjero; vigencia del W-8BEN (3 años naturales según las instrucciones del IRS, no consultadas aquí); detalles de la reforma judicial.
