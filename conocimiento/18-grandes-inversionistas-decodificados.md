# 18 — Los grandes inversionistas decodificados (y los que se hundieron)

> Nivel: experto · Actualizado: 2026-09-25 · Grado de evidencia global: **B**. Historiales de Nivel 1 (precio público o NAV diario): **A**. Mecanismo de Buffett decodificado con factores: **A/B**. Historiales privados reportados a inversionistas o prensa: **C**. Reglas de practicante atribuidas y leyendas: **D**.

Capítulos relacionados que aquí no se repiten: [01 Fundamentos](01-licenciatura-fundamentos.md) (aritmética geométrica, Bessembinder), [02 Portafolio](02-maestria-portafolio-y-asset-pricing.md) (Kelly, t ≈ IR·√T, Fama-French 2010, Barras et al.), [03 Valuación](03-maestria-valuacion-y-analisis-fundamental.md) (decaimiento de Berkshire por tamaño, fórmula mágica), cap. 06 (factores), cap. 07 (riesgo y *backtesting*), cap. 08 (sesgos), cap. 10 (practicantes y X), [14 Análisis técnico](14-analisis-tecnico-que-sobrevive.md) (CAN SLIM, Minervini, tendencia), [15 Situaciones especiales](15-eventos-corporativos-y-situaciones-especiales.md), [17 Crisis](17-crisis-burbujas-libro-de-patrones.md) (LTCM, Archegos y Melvin como crisis). Parámetros: `config/parametros.json`.

**Convenciones.** *Hecho* = dato con fuente numerada. **"Inferencia:"** = razonamiento propio. **"Regla:"** = recomendación, solo en la sección 6. **"(no verificado)"** = no confirmado en esta sesión. **"Cálculo propio"** = calculado el 25-sep-2026 con precios ajustados de Yahoo Finance (BRK-A, SPY, QQQ, ARKK, HLF, PSH.L, PSHZF, LMVTX, FMAGX, FFTY, RPAR, TAIL, DBMF, ALLW, QSPIX, QMNIX, AQMIX, NYT) y FRED (DEXUSUK) [45][46]. Los precios de fondos y ETFs son netos de sus comisiones internas, pero no de impuestos ni de costos de compraventa del inversionista.

**Nota de método.** Con la cuota de WebSearch agotada, cada cifra se confirmó por WebFetch contra la fuente primaria (cartas y comunicados de Berkshire, PDF de autores) o contra Wikipedia y su cita; los DOI, en Crossref; los rendimientos, recalculados con Yahoo y FRED. Si la única fuente es Wikipedia, el dato es Nivel 2 o 3 (sección 2.6).

---

## 1. Objetivos de dominio

Al terminar el módulo, el sistema debe poder:

1. **Descomponer** el rendimiento de cualquier gestor en mercado, factores, apalancamiento y costo de fondeo, estructura de capital, alfa y costos, y decir cuál término explica el mito.
2. **Clasificar** cada historial por auditabilidad (Nivel 1, 2 o 3) antes de usarlo como evidencia.
3. Explicar con números por qué **Buffett** es sobre todo *value* + calidad + bajo beta, apalancado 1.6 a 1 con un float que costaba menos que los T-bills, y por qué eso sí se puede imitar parcialmente.
4. Explicar por qué **Medallion** no se puede imitar: amplitud (*breadth*), horizonte, capacidad cerrada y capital propio.
5. Identificar los **mecanismos de muerte**: apalancamiento con fondeo inestable, posición grande contra la liquidez del mercado, cortos concentrados, cambio de estilo, crecimiento de activos y doblar la apuesta.
6. Separar suerte de habilidad con Denrell, Jensen, Fama-French y t ≈ IR·√T, y aplicarlo a los **rivales de la arena**, de los que solo se conocen resultados.
7. Convertir los denominadores comunes de quienes duran décadas en **reglas del sistema** coherentes con `parametros.json` (perfil `arena_agresivo` y perfil estándar).
8. Saber qué nivel de volatilidad maximiza la probabilidad de ganar una temporada de 6 meses sin quedar fuera del juego (sección 5.5).

---

## 2. Núcleo teórico / marco

### 2.1 La ecuación de descomposición

Todo historial se puede escribir como:

**R_gestor − r_f = β·(R_m − r_f) + Σ b_k·F_k + (L − 1)·(R_activos − r_fondeo) + E + α − c**

| Término | Qué captura | Ejemplo decodificado |
|---|---|---|
| β·(R_m − r_f) | Exposición al mercado | Berkshire: β ≈ 0.7 [1] |
| Σ b_k·F_k | Factores: *value*, calidad (QMJ), bajo beta (BAB), momentum, *carry*, tendencia | Buffett: BAB + QMJ hacen su alfa no significativo [1] |
| (L − 1)·(R − r_fondeo) | Apalancamiento y su costo | Berkshire ~1.6:1, float a 2.2% anual, >3 pp debajo del T-bill [1] |
| E (estructura) | Capital permanente, sin redenciones, sin *fire sales* | Berkshire cayó −44% (jun-1998 a feb-2000) mientras el mercado subía +32%, y no tuvo que vender [1] |
| α | Habilidad residual | Medallion (inferencia: no se descompone con factores públicos) |
| c | Comisiones, impacto, impuestos | Medallion cobra 5% + 44% [8] |

"Decodificar" a un inversionista quiere decir estimar cada término. El mito casi siempre atribuye a α lo que es F_k, L o E.

### 2.2 Taxonomía de ventajas (*edges*)

| Ventaja | Mecanismo económico | Ejemplos | ¿Llega a $20,000 MXN en GBM? |
|---|---|---|---|
| Analítica e informacional | Entender un negocio o un instrumento mejor que el precio | Buffett (años 60 a 80), Lynch, Burry (CDS hipotecarios), Greenblatt (situaciones especiales; no verificado) | Parcial: solo en nichos poco cubiertos |
| Estadística de alta amplitud | Miles de apuestas pequeñas casi independientes con IC diminuto | Renaissance, Thorp (*stat arb*) | No: requiere infraestructura, datos y costos institucionales |
| Estructural | Fondeo barato, capital permanente, acceso, control | Float de Berkshire, Citadel (multi-gestor), Slim (control y concesiones) | No, salvo una: el capital propio no tiene redenciones |
| Conductual y de horizonte | Comprar cuando otros *deben* vender | Marks y Oaktree 2008, Klarman, Slim 1982, Buffett | **Sí**: es la ventaja natural de una cuenta pequeña sin clientes |
| Asimetría y convexidad | Pagos donde acertar paga mucho más de lo que cuesta fallar | Soros y Druckenmiller 1992, PTJ 1987, Universa 2008 y 2020 | Parcial: el acceso a opciones en la cuenta está por verificar en GBM; stops y tamaño sí |
| **Falsa ventaja**: prima de cola vendida | Cobrar poco muchas veces y perder todo una vez | LTCM, Amaranth, Archegos y vendedores de volatilidad | Es lo que el sistema debe detectar y evitar |

### 2.3 Aritmética de supervivencia

**Recuperación necesaria** = 1/(1 − DD) − 1:

| *Drawdown* | −10% | −20% | −35% | −50% | −80.9% (ARKK 2021-22) | −92% (NYT 2002-09) |
|---|---|---|---|---|---|---|
| Alza necesaria | +11.1% | +25% | +53.8% | +100% | +423.6% | +1,150% |

**Kelly con Sharpe dado** (derivación estándar; ver cap. 02). Con exceso μ, volatilidad σ y SR = μ/σ, una fracción f del Kelly completo da crecimiento g(f) = SR²·(f − f²/2) y volatilidad f·SR:

| Fracción de Kelly | Crecimiento (% del máximo) | Volatilidad (con SR = 0.4) |
|---|---|---|
| 0.25 | 43.75% | 10% |
| 0.5 | 75% | 20% |
| 1.0 | 100% | 40% |
| 1.5 | 75% | 60% |
| 2.0 | **0%** | 80% |

Consecuencias:

- La volatilidad que maximiza el crecimiento es igual al Sharpe. Con SR = 0.4 son 40% anual.
- Sobreapostar al doble no gana nada y se cobra toda la varianza.
- Como el SR se estima con error, el Kelly "completo" casi siempre es, en realidad, más que completo.

*Inferencia:* Livermore y los fondos apalancados que quebraron operaban, en la práctica, por encima de 2× Kelly, porque el Sharpe estimado dentro de muestra suele estar inflado (cap. 07).

### 2.4 Selección, supervivencia y suerte

- **Muestreo insuficiente de fracasos.** Denrell (2003), en resumen propio: aprender de los que sobreviven sesga hacia las prácticas de riesgo alto: los que las usaron y quebraron ya no están en la muestra [35].
- **Los extremos informan poco.** Denrell y Liu (2012, PNAS) prueban que cuando el resultado extremo requiere suerte, los de mejor desempeño **no** son los de mayor habilidad esperada y "no deben ser imitados" [36].
- **Monos que tiran monedas.** Jensen lo argumentó en Columbia en 1984. Buffett respondió que los ganadores venían de la misma "aldea intelectual", Graham-and-Doddsville [5]. La réplica es buena, pero la lista la hizo él *ex post*. Frazzini, Kabiller y Pedersen (FKP) señalan ese sesgo y proponen otra prueba: factores sistemáticos [1].
- **Estadística.** t ≈ IR·√T (cap. 02). En una temporada de 6 meses, t = 2 exige un SR de 2.83. En 3 temporadas, un SR de 1.63.
- **La racha de Miller.** 15 años seguidos arriba del S&P tienen probabilidad 1/32,768 con p = 0.5 anual. Con 1,000 fondos independientes, P(al menos uno) ≈ 3% en una ventana fija; con 5,000, ≈ 14%; con ventanas móviles, más (cálculo propio). Miller lo llamó "95% suerte" [27]. *Inferencia:* el −55% de 2008 era la cola que la racha escondía.

### 2.5 Límites del arbitraje y liquidez de fondeo

- **Shleifer y Vishny (1997).** El arbitraje real requiere capital, es riesgoso y lo hacen especialistas con dinero ajeno. Cuando los precios se alejan más del valor fundamental, los clientes retiran capital y el arbitraje deja de funcionar [40].
- **Brunnermeier y Pedersen (2009).** La liquidez de mercado y la de fondeo se refuerzan entre sí en espirales [41].
- FKP resumen el genio de Buffett en una frase: aplicar apalancamiento **"without ever having to fire sale"** [1].

*Inferencia:* la variable que separa a Buffett de LTCM no es el coeficiente intelectual. Es quién puede quitarte el capital en el peor momento: acreedores de *repo* (LTCM), bancos con *swaps* (Archegos), cámaras de compensación (Amaranth) o inversionistas con redención (Melvin). Una cuenta propia sin margen elimina tres de esas cuatro amenazas. La cuarta es el propio dueño.

### 2.6 Jerarquía de auditabilidad

| Nivel | Qué es | Ejemplos | Qué **no** demuestra |
|---|---|---|---|
| **1** | Precio público diario, NAV de fondo registrado o 10-K auditado | Berkshire, Magellan, Value Trust, ARKK, PSH, fondos mutuos de AQR, FFTY, TAIL, ALLW | Que el método sea transferible, ni el rendimiento ponderado por dinero del inversionista |
| **2** | Fondo privado auditado para sus socios y reportado por prensa, cartas o LCH | Medallion, Quantum, Duquesne, Tudor, Pure Alpha, Citadel, Gotham, Scion, PNP, Universa, Melvin, Paulson | Comparabilidad: periodo, comisiones y vehículo elegidos por quien reporta |
| **3** | Autodeclarado, biográfico, concurso o anécdota | Livermore, cifras de Minervini, 20% de Klarman (Wikipedia pide cita), "la mayoría de los inversionistas de Magellan perdió dinero", anécdota de Dalio en 1982 | Casi nada. Sirve para generar hipótesis, no como evidencia |

---

## 3. Literatura y fuentes canónicas

| Autor (año) | Obra | Hallazgo cuantificado | Enlace | Grado |
|---|---|---|---|---|
| Frazzini, Kabiller y Pedersen (FAJ 74(4):35-55, 2018; WP 2013) | *Buffett's Alpha* | 1976-2011: SR 0.76 (vol 24.9%, exceso de 19.0% anual), β 0.7, IR 0.66, apalancamiento ~1.6:1, float a 2.2% (>3 pp bajo el T-bill), 36% de los pasivos es float. Alfa no significativo con BAB y QMJ. Portafolio sistemático correlacionado 75% con las acciones públicas de Berkshire. Las acciones públicas rinden más que las empresas privadas. Ganó el Graham and Dodd Award 2018 | [1] | **A** (mecanismo) |
| Berkshire Hathaway (2025) | Carta anual 2025 (firma Abel, 28-feb-2026) | 1965-2025: 19.7% vs 10.5% del S&P con dividendos. 2025: +10.9% vs +17.9%. Float de US$176 mil millones; efectivo y T-bills por más de US$370 mil millones | [3] | A (Nivel 1) |
| Buffett (1984) | *The Superinvestors of Graham-and-Doddsville* | Buffett Partnership 29.5% vs 7.4% (1957-1969); Pacific Partners 32.9% vs 7.8%. Muestra elegida *ex post* | [5] | C |
| Denrell (2003), *Org. Science* 14(3):227-243 | *Vicarious Learning, Undersampling of Failure…* | Imitar a los sobrevivientes sobreestima el valor del riesgo (resumen propio; en Crossref solo se verificaron los metadatos) | [35] | B (teoría) |
| Denrell y Liu (2012), PNAS 109(24):9331-9336 | *Top performers are not the most impressive…* | Si el extremo requiere suerte, el mejor no tiene la mayor habilidad esperada | [36] | B |
| Fama y French (2010), JF 65(5) | *Luck versus Skill…* | Pocos fondos cubren sus costos. Hay alfa bruto verdadero solo en las colas | [37] | A |
| Barras, Scaillet y Wermers (2010), JF 65(1) | *False Discoveries…* | 75% de los fondos con alfa cero neto. Los hábiles casi desaparecen hacia 2006 | [38] | A |
| Antón, Cohen y Polk (borrador 2021) | *Best Ideas* | 1983-2018: las posiciones de mayor convicción superan al mercado por 2.8-4.5% anual; el resto no. Se sostiene en *hedge funds* (13F) | [39] | B (WP, IS) |
| Shleifer y Vishny (1997), JF 52(1) | *The Limits of Arbitrage* | El arbitraje falla justo en los extremos | [40] | A (teoría con evidencia) |
| Brunnermeier y Pedersen (2009), RFS 22(6) | *Market Liquidity and Funding Liquidity* | Espirales de liquidez y de margen (resumen propio; solo metadatos verificados) | [41] | A |
| Brown, Harlow y Starks (1996), JF 51(1) | *Of Tournaments and Temptations* | 334 fondos (1976-1991): los perdedores de medio año suben la volatilidad en el segundo semestre | [42] | B |
| Chevalier y Ellison (1997), JPE 105(6) | *Risk Taking by Mutual Funds…* | Los flujos convexos incentivan a los gestores a tomar más riesgo (resumen propio; solo metadatos verificados) | [43] | B |
| Zuckerman (2019) | *The Man Who Solved the Market* | Medallion 1988-2018: 66.1% bruto y 39.1% neto anual | [8] | C (Nivel 2) |
| Lefèvre (1923) | *Reminiscences of a Stock Operator* | Biografía semificticia de Livermore | [25] | D (como evidencia) |
| Soros (1987) | *The Alchemy of Finance* | Reflexividad: percepción → precio → fundamentales | [10][11] | C (marco) |
| Kelly y Thorp | Criterio de Kelly | Fracción óptima; el sobreapuesto destruye crecimiento | [44] | A (matemática) |

---

## 4. Lo más reciente, 2023-2026

- **28-may-2023.** Muere William O'Neil [26].
- **28-nov-2023.** Muere Charlie Munger, a los 99 años [6].
- **10-may-2024.** Muere Jim Simons [8].
- **Ago-2024.** Ackman retira la OPI de Pershing Square USA: consiguió ~US$2 mil millones de una meta de US$25 mil millones [21].
- **Nov-2024.** Bill Hwang (Archegos) recibe 18 años de prisión por fraude y *racketeering* [31].
- **3-may-2025.** Buffett pide que Greg Abel lo suceda. Abel es CEO desde el 1-ene-2026 [7].
- **2025, Bridgewater.** Pure Alpha sube **+33%**, su mejor año completo. Dalio vende su última participación y sale del consejo. Los activos bajan a ~US$92 mil millones, desde ~US$162 mil millones en 2019 [14].
- **Mar-2025.** Sale el ETF ALLW (*All Weather*). Hasta el 24-sep-2026 rinde +21.9% contra +36.6% del SPY (cálculo propio).
- **May-2025.** Pershing Square sube a 47% su participación en Howard Hughes [21].
- **Nov-2025.** Burry da de baja el registro de Scion Asset Management y lanza el boletín de paga *Cassandra Unchained*. Sus 13F de 2025 mostraban *puts* sobre Nvidia y Palantir [20].
- **Dic-2025.** Según LCH, Citadel suma US$90.4 mil millones de ganancias netas desde 1990, el mayor total de la industria. Devolvió ~US$5 mil millones de ganancias de 2025 [22].
- **28-feb-2026.** Primera carta de Abel. Berkshire rinde **+10.9% en 2025 contra +17.9%** del S&P [3].
- **Mar-2026.** Gotham (Greenblatt) administra US$32.6 mil millones [19].
- **2026.** Berkshire compra OxyChem (cerrada el 2-ene-2026) y Taylor Morrison (US$8.5 mil millones; cerrada el 24-jul-2026) [4].
- **2026 al 24-sep.** BRK-A **+0.6%** contra SPY **+13.4%** (cálculo propio).
- **18-sep-2026.** Buffett pasa a presidente emérito y sigue como consejero. Howard G. Buffett es elegido presidente del consejo [4].
- **AQR resucita.** Tras −41.4% (2018-2020), QSPIX rinde +24.9% (2021), +30.8% (2022), +12.5% (2023), +21.5% (2024), +14.8% (2025) y +27.1% en 2026 (cálculo propio). Activos: US$128 mil millones en 2025 [23].
- **ARK.** ARKK subió +69.0% (2023), +8.4% (2024), +35.5% (2025) y +19.2% en 2026, y sigue **−40.5% bajo su máximo** de feb-2021 (cálculo propio).
- **Pershing Square Holdings.** −24.5% en 2026 al 23-sep (PSH.L, precio de mercado, no NAV; causa no verificada; cálculo propio).
- **Sep-2026.** Bloomberg estima la fortuna de Carlos Slim en ~US$123 mil millones (vía Wikipedia) [28].

*Inferencia:* 2023-2026 cerró la era de los fundadores (Munger, Simons, O'Neil, la salida de Dalio y la de Buffett). Berkshire se rezagó contra el índice en 2025 (último año de Buffett como CEO) y en 2026 al 24-sep (primero con Abel). Son 21 meses, demasiado pocos para concluir, pero coinciden con el decaimiento por tamaño que documenta el cap. 03.

---

## 5. Evidencia real: qué funciona, qué no y de qué tamaño

### 5.1 Tabla maestra de los grandes

| Inversionista | Cifra verificada | Nivel | Motor decodificado | Peor episodio | Grado del método transferible |
|---|---|---|---|---|---|
| **Buffett** | 19.7% vs 10.5% anual (1965-2025) [3] | 1 | *Value* + calidad + bajo β, 1.6:1 con float barato y capital permanente [1] | −48.9% (jun-1998 a mar-2000) y −51.5% (dic-2007 a mar-2009) | **A/B** vía factores QMJ y BAB; el float no se copia |
| **Munger** | 19.8% vs 5.0% del Dow (1962-1975) [6] | 2 | Concentración en calidad | −32% (1973) y −31% (1974); cerró en 1976 [6] | B (calidad) |
| **Simons** | Medallion 66.1% bruto y 39.1% neto (1988-2018); +98.2% en 2008 [8] | 2 | Amplitud estadística, horizonte corto, cerrado a externos desde 1993, 5/44 | RIEF (el fondo abierto a externos) ~−20% en 2020 y US$5 mil millones de retiros [8] | **D** (no replicable) |
| **Soros** | ~20% anual promedio en cuatro décadas; >£1,000 millones en 1992 [10][9] | 2 | Macro reflexivo, apuestas grandes con salida rápida | −US$800 millones (1987, Japón), −US$600 millones en un día (1994, yen), −US$2 mil millones (1998, Rusia) [10] | C |
| **Druckenmiller** | ~30% anual (1981-2010), sin año negativo; cerró con más de US$12 mil millones [12] | 2 | Concentración con convicción y salida rápida (caracterización propia) | Pérdidas en tecnología en 2000 (Quantum) [12] | C |
| **P. T. Jones** | +125.9% neto en 1987 [13] | 2 | Analogía con 1929 (Borish) y cortos | (sin dato verificado) | C/D |
| **Dalio** | Pure Alpha II: −18.6% (2020, a agosto) y +33% (2025) [14] | 2 | Macro sistemático; *All Weather* = paridad de riesgo | RPAR −22.8% en 2022 (cálculo propio) | C |
| **Lynch** | 29.2% vs 15.8% (1977-1990); activos de US$18 millones a US$14 mil millones [15] | 1 | GARP, cientos de posiciones, cobertura intensiva | (bajo Lynch, no verificado) | C |
| **Thorp** | PNP ~20% anual neto por ~20 años sin trimestre negativo [16] | 2 | Arbitraje de derivados y Kelly | Cierre por la investigación RICO; condenas revocadas en 1991 [16] | A (Kelly) / D (PNP) |
| **Marks** | Oaktree ~19% neto "desde el inicio" (vehículo sin especificar); fondo de deuda en problemas de US$10.9 mil millones en 2008 [17] | 2-3 | Crédito en problemas, contraciclo | (no verificado) | B (comprar cuando otros deben vender) |
| **Klarman** | "20% compuesto desde 1982" (Wikipedia pide cita); −7% a −13% en 2008 [18] | 3 | Margen de seguridad, 30-50% en efectivo | 2008 | C |
| **Greenblatt** | ~50% bruto y ~30% después de todas las comisiones (1985-1994); devolvió el capital externo en 1995 [19] | 2 | Situaciones especiales concentradas (no verificado) | (no verificado) | C (fórmula mágica, cap. 03) |
| **Burry** | Scion +489% neto acumulado (2000-2008) vs ~3% del S&P [20] | 2 | Análisis de préstamos y CDS asimétricos | Rebelión de inversionistas en 2006-2007 [20] | D (repetición) |
| **Ackman** | *Hedge* COVID: US$27 millones → US$2.6 mil millones en <1 mes [21] | 1 | Activismo concentrado | Valeant ~−US$4 mil millones; Herbalife; PSH −28%, −4.8% y −9.8% (2016-2018) | C |
| **Griffin** | Citadel +38.1% y US$16 mil millones en 2022; US$90.4 mil millones netos desde 1990 [22] | 2 | Multi-gestor con escala | −55% (2008); retiros congelados 10 meses [22] | D |
| **Asness** | QSPIX y QMNIX (Nivel 1) | 1 | Factores diversificados | −41.4% (2018-2020), luego recuperación (sección 4) | **B** |
| **Taleb y Spitznagel** | Universa +3,612% "sobre el capital invertido" (mar-2020); >100% en 2008 [24] | 2-3 | Convexidad con *puts* fuera del dinero | Pérdida continua de prima: TAIL −53.1% acumulado (cálculo propio) | D (cobertura permanente) |
| **Livermore** | ~US$100 millones en 1929; 1 millón en un día en 1907 [25] | 3 | Tendencia y piramidación | Quiebras (1915 y 1934: US$84 mil de activos vs US$2.5 millones de deuda); suicidio en 1940 [25] | D |
| **O'Neil y Minervini** | CAN SLIM, "mejor estrategia 1998-2009" según AAII (hipotética) [26]; cifras de campeonatos de Minervini (no verificado) | 3 | Crecimiento + momentum + stop de 7-8% | FFTY −59.5% (2021-23), 3.5% anual vs 13.9% del SPY (cálculo propio) | D en paquete; B en componentes (cap. 14) |
| **Bill Miller** | 15 años seguidos arriba del S&P (1991-2005) [27] | 1 | *Value* "flexible" concentrado en financieras | LMVTX −55.0% en 2008 (SPY −36.8%); −72.5% (jun-2007 a mar-2009) (cálculo propio) | D (la racha) |
| **Carlos Slim** | Compras en 1982; Telmex en 1990; préstamo de US$250 millones al NYT (ene-2009) [28] | 1 (tenencias públicas) | Contraciclo + control + rentas reguladas | — | B (comprar en crisis) / D (control) |

### 5.2 Fichas decodificadas (solo lo que agrega sobre la tabla)

**Buffett y Munger.** En 1976-2011 Berkshire tuvo el Sharpe más alto de cualquier acción o fondo con más de 30 años de historia [1]. En ese periodo sufrió −44% mientras el mercado subía +32%, un rezago de 76 pp. FKP señalan que muchos gestores no habrían sobrevivido algo así; Berkshire sí, por su reputación y por ser una corporación [1].

Por *drawdown* (cálculo propio con BRK-A) [45]:

| Episodio | Caída | Recuperación |
|---|---|---|
| Oct-1987 | −37.1% | Jul-1988 |
| Oct-1989 a oct-1990 | −37.5% | Ago-1991 |
| Jun-1998 a mar-2000 | −48.9% | Nov-2003 |
| Dic-2007 a mar-2009 | −51.5% | **Feb-2013** |
| 2020 | −30.4% | Nov-2020 |

*Inferencia:* con el límite duro de −20% del perfil estándar, el sistema habría **vendido a Buffett al menos siete veces** desde 1981 (hubo siete episodios de −25% o peor, incluidos 1981-82 con −27.1% y 2022 con −26.0%). Con el −35% del perfil arena, cuatro. El rendimiento de Buffett venía con *drawdowns* que exigen estructura, no fuerza de voluntad.

Munger perdió −32% y −31% en 1973-1974 y cerró su sociedad en 1976 [6].

Lo transferible (FKP): un portafolio sistemático *value* + calidad + bajo beta explica 57% de la varianza de las acciones públicas de Berkshire, sin costos y con retrospectiva [1]. Lo no transferible: el float a 2.2%, los tratos privados y la calificación AAA de 1989 a 2009.

**Simons y Renaissance.** Medallion ganó más de US$100 mil millones desde 1988. Los fondos de la misma firma abiertos a externos perdieron ~20% en 2020 y tuvieron US$5 mil millones de retiros (dic-2020 a feb-2021) [8]. *Inferencia:* la marca no es la ventaja. La ventaja es la capacidad cerrada, el horizonte corto, el capital de los empleados y el costo de ejecución. "Operar como Renaissance" con $20,000 MXN y datos diarios es marketing.

**Soros y Druckenmiller.** El 16-sep-1992 la tasa base subió de 10% a 12% y se prometió 15%; el Tesoro británico estimó el costo en £3.3 mil millones (revisión de 2005) [9]. La libra pasó de US$1.976 (10-sep) a 1.513 al cierre de 1992: **−23.4%** (cálculo propio con FRED DEXUSUK) [46]. Wikiquote atribuye a Soros la instrucción a Druckenmiller "go for the jugular" y a Druckenmiller la regla: "no importa si tienes razón o no, sino cuánto ganas cuando aciertas y cuánto pierdes cuando fallas" [11]. Soros: "no hay vergüenza en equivocarse, solo en no corregir" (1995) [11]. Druckenmiller se fue de Quantum en 2000 tras pérdidas grandes en tecnología [12].

*Inferencia:* el método es asimetría. Pocas apuestas enormes cuando la tesis, el precio y la política monetaria coinciden, con salida inmediata cuando no. Por eso no es un sistema replicable: depende del juicio de dos personas.

**Paul Tudor Jones.** El dato duro es el 1987: +125.9% neto [13]. Sus reglas famosas no se verificaron en fuente primaria en esta sesión: defensa primero, "no promediar pérdidas", razón de 5 a 1 y media móvil de 200 días (atribuidas a Schwager, *Market Wizards*, 1989, y entrevistas). La evidencia de la media de 200 días está en el cap. 14 (Faber: mejora el *drawdown* más que el CAGR).

**Dalio y Bridgewater.** *All Weather* (1996) es paridad de riesgo [14]. En 2022 la correlación acción-bono se volvió positiva y **RPAR cayó −22.8%**. Desde dic-2019 compone 3.6% anual contra 15.6% del SPY (cálculo propio). DBMF (tendencia) subió +21.6% en 2022 (cálculo propio). La anécdota de 1982 (predijo una depresión y se quedó sin capital) no se verificó. *Inferencia:* la paridad de riesgo depende de una correlación que cambia de signo con el régimen de inflación.

**Lynch.** "La mayoría de los inversionistas de Magellan perdió dinero" no se localizó en fuente original: es Nivel 3. Lo verificable: sin Lynch, el fondo cayó −49.4% en 2008 (FMAGX, cálculo propio).

**Thorp.** Fue escéptico de Madoff desde 1991 [16]. PNP cerró por la investigación RICO aunque las condenas se revocaron: el riesgo legal o de contraparte puede cerrar un fondo sin error de inversión. Ridgeline (1994-2002) cerró porque el *stat arb* dejó de rendir [16].

**Marks, Klarman y Greenblatt.** *Inferencia:* la ventaja de Marks y Klarman es tener pólvora cuando todos venden (Oaktree levantó US$10.9 mil millones en 2008 [17]; Klarman tiene 30-50% en efectivo [18]). En una temporada de 6 meses su costo de oportunidad es visible y el beneficio llega solo si hay crisis. Greenblatt devolvió el capital externo en 1995 [19]: limitó la capacidad para proteger el rendimiento.

**Burry.** Sus inversionistas se rebelaron en 2006-2007, antes de que la tesis pagara [20]. En 2025 apostó contra la IA con *puts* en Nvidia y Palantir y luego dio de baja el registro de su firma [20]. *Inferencia:* un acierto extremo único dice poco de la habilidad (Denrell-Liu). La lección útil es de estructura: con capital que puede irse, ni la tesis correcta sobrevive a los clientes.

**Ackman.** Herbalife: el corto de US$1 mil millones (dic-2012) se cerró en feb-2018 con pérdida [21]. HLF subió de US$18.15 a 46.05 ajustados (+154%) mientras el SPY subía +109.6%. Luego cayó −80.1% desde su máximo de 2019 (cálculo propio). Tener razón tarde es igual a no tenerla. En PSHZF (USD): −28.0% (2016), −4.8% (2017), −9.8% (2018), +56.0% (2019) y +88.6% (2020) (cálculo propio). La cobertura de marzo de 2020 es el ejemplo de manual de convexidad barata: US$27 millones de prima para una ganancia de US$2.6 mil millones [21]. *Inferencia:* Ackman es bueno comprando opcionalidad y malo con cortos concentrados de pérdida ilimitada.

**Griffin.** Citadel perdió −55% en 2008, ganó +62% en 2009 y recuperó su *high-water mark* en ene-2012 [22]. Sobrevivió porque congeló retiros 10 meses: estructura de nuevo. El modelo multi-gestor a escala no se replica con una cuenta de GBM.

**Asness y AQR.** Es el caso de libro de una prima de factor real con varianza brutal. QSPIX cayó −41.4% (2018-2020) y luego subió +239% desde el mínimo de dic-2020; hoy está +99% sobre su máximo previo (cálculo propio) [45]. Sobrevivió la firma, no todos sus clientes: los activos cayeron de US$224 mil millones a US$143 mil millones [23]. AQMIX (tendencia) ganó +35.5% en 2022 tras años planos (cálculo propio).

**Taleb y Spitznagel.** El 3,612% es sobre "capital invertido en la estrategia" [24], no sobre un portafolio total. Wikipedia cita una simulación de Universa: 3.3% en Universa + 96.7% en el S&P compuso 12.3% anual en los 10 años a feb-2018 [24]. El SPY compuso 9.6% en ese periodo (cálculo propio). CalPERS dejó a Universa en 2020 por "alternativas más baratas" [24]. La versión minorista cuesta: el ETF TAIL rinde **−7.7% anual** desde abr-2017 (−53.1% acumulado) contra +15.1% anual del SPY; en feb-mar 2020 subió solo +28.4% (cálculo propio). *Inferencia:* la convexidad funciona si es barata, táctica y pequeña. Como programa permanente para un inversionista minorista, pierde.

**Livermore.** Ganó ~US$100 millones en 1929 y se declaró en quiebra al menos dos veces más (1915 y 1934, la tercera) [25]. Su ruina no vino de un mal método de entrada, sino de apalancamiento y tamaño sin límite de pérdida total. Es la ilustración de 2× Kelly.

**O'Neil y Minervini.** El vehículo vivo más cercano, FFTY (IBD 50), compone 3.5% anual desde 2015 y cayó −59.5% [45]. Los fondos del propio O'Neil "batallaron para generar rendimientos decentes" pese a ganancias hipotéticas sobresalientes [26]. Los campeonatos son Nivel 3. Los componentes con evidencia (momentum, cercanía al máximo de 52 semanas, stop) están en el cap. 14.

**Bill Miller.** Concentró en financieras (Bear Stearns, entre otras) y perdió más de US$100 millones personales en Bear [27]. El patrón de muerte fue **promediar a la baja** una tesis de "barato" en un sector apalancado.

**Carlos Slim.** En la crisis de 1982 compró empresas mexicanas líderes a valuaciones deprimidas: minería, cobre, aluminio, llantas y comercio [28]. En 1990 compró Telmex en la privatización. Hacia 2006 controlaba ~90% de las líneas fijas y Telcel ~80% de los celulares [28]. En ene-2009 prestó US$250 millones al NYT [28], cuya acción tocó su mínimo el 19-feb-2009 con −92.1% desde 2002. Desde el 20-ene-2009 subió +120% a ene-2015 y +232% a dic-2017 (cálculo propio). *Inferencia:* hay dos ventajas distintas. Comprar a quien debe vender es transferible. El control y las rentas reguladas no lo son.

### 5.3 Los que se hundieron: mecanismo de muerte

| Caso | Antes de caer | Mecanismo | Cifras | Qué lo habría salvado |
|---|---|---|---|---|
| **LTCM** (1998; ver cap. 17) | ~21% (1994), 43% (1995) y 41% (1996) [29] | Convergencia apalancada >25:1 (US$129 mil millones de activos), US$1.25 billones de nocional. Devolvió US$2.7 mil millones a fines de 1997 y **se desvió** a volatilidad de acciones y *merger arb* [29] | −US$4.6 mil millones en <4 meses; rescate de US$3.625 mil millones [29] | Apalancamiento ≤ 5:1; límite de tamaño contra la liquidez; no cambiar de estilo |
| **Amaranth** (2006) | Máximo de US$9.2 mil millones (ago-2006) [30] | Un operador (Hunter, 32 años) con *spreads* de gas; un "multiestrategia" que en realidad era un fondo de gas | >US$6 mil millones perdidos, ~US$6.5 mil millones en una semana [30] | Límite de riesgo por libro; tamaño menor a una fracción del interés abierto |
| **Archegos** (2021) | ~US$36 mil millones de exposición en el máximo [31] | *Total return swaps* con varios bancos que no veían la exposición total; concentración (ViacomCBS, Baidu) | Bancos: >US$10 mil millones (Credit Suisse 5.5, Nomura 2.85, Morgan Stanley 0.91, UBS 0.77); 18 años de prisión [31] | Transparencia de exposición bruta; límite por emisor; historial previo (Tiger Asia, 2012) como alerta |
| **Melvin** (2021-22) | ~30% anual (2014-2020); +52% en 2020 [32] | Cortos concentrados y saturados con alto *short interest*; *squeeze* | −53% en enero de 2021; −39% en 2021; inyección de US$2.75 mil millones; cierre en 2022 [32] | Cortos pequeños o vía *puts*; límite de *crowding* |
| **John Paulson** (2011-2020) | ~US$15 mil millones de ganancia en 2007; ~US$5 mil millones personales en 2010 [33] | Pasó de la tesis de crédito a oro, bancos y Sino-Forest; exceso de confianza tras un acierto extremo | Advantage −36% y Advantage Plus −52% (2011); activos de US$38 mil millones a 9 mil millones (2018); *family office* en 2020 [33] | Tratar 2007 como evidencia débil (Denrell-Liu); mismo proceso de validación para cada tesis nueva |
| **ARK** (2021-22) | +152.7% en 2020 (cálculo propio) | Inferencia: acciones de duración larga (flujos lejanos) en un alza de tasas, con activos que crecieron hasta el máximo (el ETF activo más grande a dic-2020 [34]) | −80.9% (feb-2021 a dic-2022); desde el máximo, −8.8% anual contra +15.8% del QQQ (cálculo propio) | Filtro de valuación y de tasas; reducir cuando fluye el dinero; límite sectorial |
| **Livermore** | Fortunas en 1907 y 1929 | Apalancamiento sin límite de pérdida total | 3 quiebras; suicidio [25] | *Drawdown* máximo duro |
| **Bill Miller** | 15 años de racha | Promediar a la baja en financieras apalancadas | −55% (2008); −72.5% desde el máximo | Límite sectorial; no promediar perdedores |

### 5.4 Denominadores comunes: quién dura décadas y quién explota

| Rasgo | Los que duran (evidencia) | Los que explotan (evidencia) |
|---|---|---|
| **Fondeo** | Capital permanente o propio: Berkshire, Medallion (empleados), Soros como *family office* desde 2011 | Fondeo que se va en la crisis: LTCM (*repo*), Archegos (*swaps*), Melvin (redenciones), Amaranth (margen) |
| **Apalancamiento** | Moderado y barato: Berkshire 1.6:1 a un costo menor que el T-bill | >25:1 (LTCM); exposición oculta (Archegos) |
| **Tamaño vs liquidez** | Druckenmiller cerró en 2010; Greenblatt y Medallion limitaron la capacidad | Amaranth llegó a ser el mercado; LTCM también |
| **Error** | Soros: "corregir"; Druckenmiller: asimetría | Miller y Livermore promediaron; Ackman sostuvo Herbalife 5 años |
| **Estilo** | Constante con una ventaja que se puede explicar: Buffett (calidad), Simons (estadística) | Desvío: LTCM hacia volatilidad, Paulson hacia oro, Amaranth hacia gas |
| **Crecimiento de activos** | Devolver capital: Greenblatt 1995, Medallion 1993, Druckenmiller 2010 | Crecer en la cima: ARK en 2021, Value Trust, Magellan después de Lynch |
| **Cortos** | Cortos como cobertura con pérdida acotada: *puts* y CDS (Ackman 2020, Burry 2007) | Cortos concentrados de pérdida ilimitada: Melvin, Herbalife |
| **Humildad estadística** | Miller: "95% suerte"; Thorp detectó a Madoff por imposible | Paulson tras 2007; Hwang tras Tiger Asia |
| **Caídas sobrevividas** | Buffett (−49% y −52%), AQR (−41%), Citadel (−55%, con retiros congelados) | Los que tuvieron que vender en el mínimo |

*Inferencia (síntesis):* los que duran tienen **tres cosas**: una ventaja económica explicable, estructura que impide la venta forzada y tamaño subordinado a la liquidez. Los que explotan tienen **una**: apalancamiento o concentración que convierte una racha buena en un solo evento de ruina. El coeficiente intelectual es igual de alto en ambos grupos: dos premios Nobel en LTCM.

### 5.5 El torneo de 6 meses: volatilidad vs probabilidad de ganar (cálculo propio)

Supuestos: movimiento browniano geométrico diario, 126 días, 20,000 simulaciones, semilla 20260925, 4 rivales con volatilidad de 20% y SR de 0.4, **sin cortacircuitos**. Es una ilustración, no un pronóstico.

| Nuestra vol | P(1.º) con SR 0 | P(1.º) con SR 0.4 | Mediana con SR 0.4 | P(DD ≤ −20%) con SR 0.4 | P(DD ≤ −35%) con SR 0.4 |
|---|---|---|---|---|---|
| 10% | 6.7% | 9.3% | +1.8% | 0.1% | 0.0% |
| 20% | 14.0% | 19.7% | +3.1% | 13.8% | 0.1% |
| 30% | 20.2% | 28.3% | +4.0% | 43.8% | 4.7% |
| 45% | 25.0% | 34.0% | +4.0% | 79.3% | 25.9% |
| 60% | 27.5% | 37.2% | +3.4% | 93.7% | 50.1% |
| 80% | 27.7% | 38.2% | +0.4% | 99.1% | 75.3% |

*Inferencia:*

1. Con igual habilidad, subir la volatilidad de 20% a 30% aumenta P(1.º) en ~9 pp con un riesgo de −35% todavía bajo (~5%).
2. Arriba de ~45%, la ganancia marginal en P(1.º) es mínima y la probabilidad de tocar el límite duro se dispara.
3. La mediana se maximiza cerca de vol = SR (Kelly).
4. Sin ventaja (SR 0), la volatilidad compra probabilidad de ganar, pero a costa de mediana negativa. Es la lógica de Brown-Harlow-Starks: los perdedores de medio año apuestan la varianza [42]. Los rivales atrasados probablemente harán exactamente eso.

---

## 6. Traducción operable

**Regla 18.1. Filtro de auditabilidad.** Todo historial citado en un memo del comité lleva su Nivel (sección 2.6). El Nivel 3 no justifica ninguna posición. El Nivel 2 solo apoya hipótesis que después se prueban con datos de Nivel 1 o con *backtest* bajo `validacion_estrategias`.

**Regla 18.2. Descomponer antes de imitar.** Antes de adoptar el estilo de un gurú, regresar su serie de Nivel 1 contra mercado, *value*, calidad, bajo beta, momentum y tendencia (cap. 06). Si el alfa desaparece, **comprar el factor barato** (ETF o *screen* sistemático) en lugar de copiar a la persona.

**Regla 18.3. Estructura antes que tesis.** El sistema nunca usa fondeo que pueda retirarse en crisis:

- Sin margen, sin préstamo de valores para cortos y sin derivados con llamada de margen.
- El apalancamiento solo vía ETFs apalancados con el filtro de `filtro_apalancados` y hasta `etf_apalancado_max` = 0.5 en la arena.
- En el perfil estándar, apalancamiento bruto de 1.0 en fase 1 y 1.3 en fase 2.

**Regla 18.4. Kelly con descuento.** Volatilidad objetivo = fracción × SR estimado:

- El SR de un *backtest* se divide entre 2 antes de usarlo.
- Fracción ≤ `kelly_fraccion_max`: 0.5 en la arena, 0.25 en el estándar.
- Con SR real estimado de 0.4, la volatilidad objetivo de la arena es ≤ 20%. Solo sube a 25-30% en modo torneo atrasado (Regla 18.11).

**Regla 18.5. Cortacircuitos no negociables.** Los niveles −12%, −20%, −28% y −35% de la arena y −8%, −12%, −15% y −20% del estándar se ejecutan sin excepción. Es la regla anti-Livermore y anti-LTCM. *Inferencia:* el costo conocido es que habría sacado al sistema de Berkshire en 1987, 1990, 1998-2000 y 2008. Es un costo aceptable: el sistema no tiene la estructura de Berkshire.

**Regla 18.6. Tamaño vs liquidez.** Ninguna orden supera 5% del volumen promedio diario de 20 días del instrumento en la BMV o el SIC. Con $20,000 MXN no aplica casi nunca. Se registra para cuando se escale a fase 2.

**Regla 18.7. Concentración por convicción, no por entusiasmo.** Se permite concentrar como los "best ideas" [39] dentro de los límites:

- Arena: `accion_individual_max` 0.3 y `etf_indice_max` 0.6. Estándar: 0.10 y sector 0.25.
- La convicción se documenta *ex ante* con tesis, precio de invalidación y horizonte.
- Una posición que llega al máximo por subida de precio se recorta a la banda de rebalanceo (`banda_absoluta` 0.05).

**Regla 18.8. Nunca promediar a la baja una tesis táctica.** Solo se permite agregar a una posición perdedora si es núcleo sistemático rebalanceado por bandas. Cualquier otra adición requiere que el precio esté arriba de la entrada (piramidar ganadores, no perdedores). Es la regla anti-Miller y anti-Livermore.

**Regla 18.9. Sin cortos de pérdida ilimitada.** Las posiciones bajistas solo se toman con pérdida máxima definida: *puts*, ETFs inversos con límite de tamaño o simplemente no estar invertido. Prima total en riesgo ≤ 2% (`opciones_prima_en_riesgo_max`). Es la regla anti-Melvin y anti-Herbalife.

**Regla 18.10. Coberturas de cola solo tácticas y baratas.** No hay programa permanente de *puts* (TAIL −7.7% anual). Se compra cobertura solo si hay (a) una prima barata en términos relativos y (b) un detonador identificado. Presupuesto ≤ 2% del capital por temporada. La protección por defecto es la tendencia (media de 200 días, cap. 14) y los cortacircuitos.

**Regla 18.11. Modo torneo, calibrado con la sección 5.5.**

- Adelante del mejor rival por ≥ 5 pp (`ventaja_para_bajar_varianza_pp`): bajar la volatilidad objetivo a ~15-20%.
- Atrás por ≥ 5 pp (`desventaja_para_subir_exposicion_pp`): subir hasta 30% como máximo, **nunca 45% o más**, porque la ganancia marginal en P(1.º) es de ~6 pp contra ~20 pp más de probabilidad de tocar −35%.
- Nunca "apostar la varianza" sin SR positivo estimado. Sin ventaja, la volatilidad solo compra una lotería con mediana negativa.

**Regla 18.12. Evaluar a los rivales como Denrell-Liu.** Un rival que gana una temporada no es evidencia de habilidad (hace falta SR > 2.8 para t = 2 en 6 meses):

- No se persigue ni se imita el resultado de un rival.
- Se registra su serie en `competencia/rivales.csv` y se estima su volatilidad implícita con los reportes.
- Un rival con volatilidad muy alta y ventaja grande probablemente tomó mucha varianza. La respuesta correcta es la Regla 18.11, no copiarlo.

**Regla 18.13. Capacidad y flujos.** Si una estrategia o tema recibe flujos récord y aparece en medios (ARK 2021, Value Trust 2007), se reduce su peso táctico a la mitad hasta que el precio confirme con la tendencia. El crecimiento de activos de los gestores famosos es una señal de riesgo, no de calidad.

**Regla 18.14. Invalidación escrita (Soros).** Cada tesis táctica se registra con precio o condición de invalidación antes de entrar. Si se cumple, se sale en la siguiente sesión. Aplican las rachas de `rachas`: 3 pérdidas reducen el tamaño 50% y 5 pausan la estrategia.

**Regla 18.15. Lista de crisis precomprometida (Slim, Marks, Buffett).** Se mantiene una lista de 5 a 10 activos de calidad (índices y emisoras con balance sólido) con precio objetivo de compra. Se ejecuta en 3 tramos solo si el índice cae ≥ 20% desde su máximo **y** el propio portafolio está por encima de su nivel de cortacircuitos, dentro de los límites de concentración. *Inferencia:* el perfil arena tiene `reserva_cetes_min` = 0. Parámetro propuesto para la calibración de fin de fase 0: reserva táctica de 10-15% en CETES para este fin. **Pendiente de aprobación del dueño.**

**Regla 18.16. Checklist "¿Buffett o Livermore?"** Antes de cualquier posición ≥ 15% del capital:

1. ¿La ventaja es explicable en una frase económica, no narrativa?
2. ¿Qué factor explica la mayor parte del rendimiento esperado?
3. ¿Alguien puede obligarme a vender en el mínimo?
4. ¿La pérdida máxima está acotada y es ≤ `riesgo_por_operacion` (3% en la arena)?
5. ¿El tamaño cumple con Kelly/2 del SR descontado?
6. ¿Estoy promediando un perdedor?
7. ¿Es un corto de pérdida ilimitada?
8. ¿El tema tiene flujos récord o cobertura mediática máxima?
9. ¿Cuál es el precio de invalidación?
10. ¿Qué nivel de auditabilidad tiene la evidencia que uso?

Si 3 y 7 no pasan o 4 falla, no se opera.

---

## 7. Trampas y errores comunes

1. **Atribuir a genio lo que es factor.** Buffett es sobre todo calidad y bajo beta apalancados [1]. Imitar las acciones sin el apalancamiento, el float y la estructura da un portafolio de factores más caro.
2. **Confundir la marca con la ventaja.** Renaissance tiene Medallion y también RIEF, con −20% en 2020 [8].
3. **Tomar el rendimiento del fondo como el del inversionista.** ARKK compuso 14.5% anual desde 2014, cerca del SPY (13.8%), pero Morningstar lo ubica entre los mayores destructores de riqueza por flujos que entraron en el máximo [34].
4. **Aprender de los sobrevivientes.** Por cada Buffett hay miles de gestores *value* concentrados que no aparecen (Denrell) [35].
5. **Imitar al ganador extremo o creer en rachas.** Paulson (2007) perdió −52% en 2011 con la misma confianza [33][36]. La racha de 15 años de Miller es poco informativa con miles de fondos [27].
6. **Leer reglas de práctica sin fuente.** "5 a 1", "Regla n.º 1: no perder dinero" o "50.75% de aciertos" son Nivel 3 hasta verificarse. Lo mismo los campeonatos: cuentas pequeñas de un año, autoseleccionadas y sin GIPS.
7. **Ignorar el costo de la convexidad.** TAIL: −53% acumulado para una ganancia de +28% en el *crash* de 2020.
8. **Olvidar la estructura.** La misma tesis de Burry casi lo destruye por sus clientes. La de Buffett sobrevive a −49% porque Berkshire es una corporación.
9. **Desviarse tras el éxito.** LTCM devolvió capital y amplió estilos. Paulson pasó de crédito a oro.
10. **Tener razón demasiado pronto con un corto.** HLF +154% contra Ackman antes de caer −80% [21].
11. **Pensar que la paridad de riesgo es "todo clima".** En 2022 acciones y bonos cayeron juntos (RPAR −22.8%).
12. **Extrapolar el Berkshire de 1965-1990 al de hoy.** 2025 (último año de Buffett como CEO): +10.9% vs +17.9%; 2026 al 24-sep: +0.6% vs +13.4%. Muestra corta, pero coincide con el decaimiento por tamaño (cap. 03).
13. **Creer que el coeficiente intelectual protege.** Dos premios Nobel en LTCM [29].

---

## 8. Examen de titulación

1. **¿Cuál es el Sharpe de Berkshire en *Buffett's Alpha* y qué lo explica?**
   0.76 (1976-2011; vol 24.9%, β 0.7). Lo explican las exposiciones a BAB y QMJ con apalancamiento de ~1.6:1; el alfa deja de ser significativo [1].

2. **¿Qué ventaja de Buffett no puede copiar una cuenta de GBM?**
   El float a 2.2%, más de 3 pp bajo el T-bill (36% de los pasivos), y el capital permanente que evita la venta forzada [1].

3. **¿Cuántos *drawdowns* de más de 30% tuvo BRK-A desde 1987 y cuál fue el peor?**
   Cinco (1987, 1989-90, 1998-2000, 2007-09 y 2020). El peor fue −51.5% (dic-2007 a mar-2009), recuperado en feb-2013.

4. **Medallion: rendimiento bruto y neto y por qué no se replica.**
   66.1% bruto y 39.1% neto (1988-2018). No se replica porque exige amplitud estadística, horizonte corto, capacidad cerrada desde 1993, capital de empleados y comisiones de 5/44 [8].

5. **¿Qué dice Denrell-Liu (2012) sobre imitar a los mejores?**
   Si el extremo requiere suerte, los de mejor desempeño no tienen la mayor habilidad esperada y no deben imitarse [36].

6. **¿Cuánto SR necesita un rival para t = 2 en una temporada de 6 meses?**
   2.83, porque t ≈ SR·√0.5.

7. **Crecimiento con 2× Kelly y con ½ Kelly.**
   2×: cero. ½: 75% del máximo con la mitad de la volatilidad.

8. **Mecanismo común de LTCM, Archegos, Amaranth y Melvin.**
   Fondeo o contraparte que retira capital en el peor momento, combinado con una posición grande contra la liquidez. Límites del arbitraje [40][41].

9. **¿Por qué la cobertura de Ackman en 2020 es buena convexidad y Herbalife mala?**
   En 2020 fue una prima de US$27 millones con pérdida acotada y pago de US$2.6 mil millones. Herbalife fue un corto con pérdida ilimitada, sostenido mientras HLF subía +154% [21].

10. **Rendimiento de TAIL desde 2017 y lección.**
    −7.7% anual (−53.1% acumulado) contra +15.1% del SPY. La cobertura permanente de cola destruye crecimiento en minoristas.

11. **¿Qué pasó con la paridad de riesgo en 2022?**
    La correlación acción-bono se volvió positiva por inflación. RPAR cayó −22.8%.

12. **Cifra de Lynch y su nivel de auditabilidad.**
    29.2% contra 15.8% (1977-1990). Nivel 1: fondo mutuo registrado.

13. **¿Qué compró Slim en 1982 y qué parte de su éxito no es transferible?**
    Empresas mexicanas líderes deprimidas: minería, cobre, aluminio, llantas y comercio. No es transferible el control de Telmex y las rentas reguladas (~90% de las líneas fijas en 2006) [28].

14. **Volatilidad que maximiza P(1.º) sin disparar la ruina en 6 meses (sección 5.5).**
    ~25-30% con SR de 0.4. Arriba de 45%, la P(1.º) sube muy poco y P(DD ≤ −35%) pasa de 26%.

15. **Tres rasgos de los que duran décadas.**
    Ventaja económica explicable, estructura sin venta forzada y tamaño subordinado a la liquidez (con humildad estadística como cuarto).

---

## 9. Fuentes

1. Frazzini, A., Kabiller, D., Pedersen, L. H. (2018). "Buffett's Alpha". *Financial Analysts Journal* 74(4):35-55. DOI https://doi.org/10.2469/faj.v74.n4.3 · NBER WP 19681: https://www.nber.org/papers/w19681 · PDF del autor (borrador de nov-2013, cifras 1976-2011): http://docs.lhpedersen.com/BuffettsAlpha.pdf · AQR: https://www.aqr.com/Insights/Research/Journal-Article/Buffetts-Alpha
2. Berkshire Hathaway, carta 2024 (tabla 1965-2024: 19.9% vs 10.4%): https://www.berkshirehathaway.com/letters/2024ltr.pdf
3. Berkshire Hathaway, carta 2025 (G. Abel, 28-feb-2026; 19.7% vs 10.5%; float y efectivo): https://www.berkshirehathaway.com/letters/2025ltr.pdf
4. Berkshire Hathaway, comunicados 2026 (presidente emérito 18-sep-2026; OxyChem; Taylor Morrison): https://www.berkshirehathaway.com/news/2026news.html
5. "The Superinvestors of Graham-and-Doddsville" (Buffett, 1984): https://en.wikipedia.org/wiki/The_Superinvestors_of_Graham-and-Doddsville
6. Charlie Munger: https://en.wikipedia.org/wiki/Charlie_Munger
7. Warren Buffett: https://en.wikipedia.org/wiki/Warren_Buffett
8. Renaissance Technologies: https://en.wikipedia.org/wiki/Renaissance_Technologies · Jim Simons (cita a Zuckerman, 2019): https://en.wikipedia.org/wiki/Jim_Simons
9. Black Wednesday: https://en.wikipedia.org/wiki/Black_Wednesday
10. Soros Fund Management / Quantum: https://en.wikipedia.org/wiki/Quantum_Group_of_Funds · George Soros: https://en.wikipedia.org/wiki/George_Soros
11. Wikiquote, George Soros (incluye citas atribuidas a Druckenmiller): https://en.wikiquote.org/wiki/George_Soros
12. Stanley Druckenmiller: https://en.wikipedia.org/wiki/Stanley_Druckenmiller
13. Paul Tudor Jones: https://en.wikipedia.org/wiki/Paul_Tudor_Jones
14. Bridgewater Associates: https://en.wikipedia.org/wiki/Bridgewater_Associates · Ray Dalio: https://en.wikipedia.org/wiki/Ray_Dalio
15. Peter Lynch: https://en.wikipedia.org/wiki/Peter_Lynch
16. Edward O. Thorp: https://en.wikipedia.org/wiki/Edward_O._Thorp · Princeton Newport Partners: https://en.wikipedia.org/wiki/Princeton_Newport_Partners
17. Howard Marks: https://en.wikipedia.org/wiki/Howard_Marks_(investor)
18. Seth Klarman: https://en.wikipedia.org/wiki/Seth_Klarman
19. Joel Greenblatt: https://en.wikipedia.org/wiki/Joel_Greenblatt
20. Michael Burry: https://en.wikipedia.org/wiki/Michael_Burry
21. Bill Ackman: https://en.wikipedia.org/wiki/Bill_Ackman
22. Citadel LLC: https://en.wikipedia.org/wiki/Citadel_LLC · Kenneth C. Griffin: https://en.wikipedia.org/wiki/Kenneth_C._Griffin
23. AQR Capital Management: https://en.wikipedia.org/wiki/AQR_Capital_Management
24. Universa Investments: https://en.wikipedia.org/wiki/Universa_Investments · Mark Spitznagel: https://en.wikipedia.org/wiki/Mark_Spitznagel
25. Jesse Livermore: https://en.wikipedia.org/wiki/Jesse_Livermore
26. William O'Neil: https://en.wikipedia.org/wiki/William_O%27Neil · CAN SLIM: https://en.wikipedia.org/wiki/CAN_SLIM
27. Bill Miller: https://en.wikipedia.org/wiki/Bill_Miller_(investor) · Legg Mason: https://en.wikipedia.org/wiki/Legg_Mason
28. Carlos Slim: https://en.wikipedia.org/wiki/Carlos_Slim · The New York Times Company: https://en.wikipedia.org/wiki/The_New_York_Times_Company
29. Long-Term Capital Management: https://en.wikipedia.org/wiki/Long-Term_Capital_Management (ver además cap. 17, fuente 20: Federal Reserve History)
30. Amaranth Advisors: https://en.wikipedia.org/wiki/Amaranth_Advisors
31. Archegos Capital Management: https://en.wikipedia.org/wiki/Archegos_Capital_Management
32. Melvin Capital: https://en.wikipedia.org/wiki/Melvin_Capital
33. John Paulson: https://en.wikipedia.org/wiki/John_Paulson · Paulson & Co.: https://en.wikipedia.org/wiki/Paulson_%26_Co.
34. ARK Invest: https://en.wikipedia.org/wiki/ARK_Invest
35. Denrell, J. (2003). "Vicarious Learning, Undersampling of Failure, and the Myths of Management". *Organization Science* 14(3):227-243. https://doi.org/10.1287/orsc.14.2.227.15164
36. Denrell, J., Liu, C. (2012). "Top performers are not the most impressive when extreme performance indicates unreliability". *PNAS* 109(24):9331-9336. https://doi.org/10.1073/pnas.1116048109
37. Fama, E., French, K. (2010). "Luck versus Skill in the Cross-Section of Mutual Fund Returns". *Journal of Finance* 65(5):1915-1947. https://doi.org/10.1111/j.1540-6261.2010.01598.x
38. Barras, L., Scaillet, O., Wermers, R. (2010). "False Discoveries in Mutual Fund Performance". *Journal of Finance* 65(1):179-216. https://doi.org/10.1111/j.1540-6261.2009.01527.x
39. Antón, M., Cohen, R. B., Polk, C. "Best Ideas" (borrador de abr-2021). http://personal.lse.ac.uk/polk/research/BestIdeas.pdf
40. Shleifer, A., Vishny, R. (1997). "The Limits of Arbitrage". *Journal of Finance* 52(1):35-55. https://doi.org/10.1111/j.1540-6261.1997.tb03807.x
41. Brunnermeier, M., Pedersen, L. H. (2009). "Market Liquidity and Funding Liquidity". *Review of Financial Studies* 22(6):2201-2238. https://doi.org/10.1093/rfs/hhn098
42. Brown, K., Harlow, W., Starks, L. (1996). "Of Tournaments and Temptations". *Journal of Finance* 51(1):85-110. https://doi.org/10.1111/j.1540-6261.1996.tb05203.x
43. Chevalier, J., Ellison, G. (1997). "Risk Taking by Mutual Funds as a Response to Incentives". *Journal of Political Economy* 105(6):1167-1200. https://doi.org/10.1086/516389
44. Criterio de Kelly: https://en.wikipedia.org/wiki/Kelly_criterion (derivación de fracciones: cap. 02)
45. Yahoo Finance, API chart v8 (cálculos propios del 25-sep-2026 con `herramientas/datos_historicos.py`): https://query1.finance.yahoo.com/v8/finance/chart/BRK-A (y demás tickers de las convenciones)
46. FRED, serie DEXUSUK (USD por GBP): https://fred.stlouisfed.org/series/DEXUSUK
47. Bessembinder, H. (2018). "Do stocks outperform Treasury bills?" *Journal of Financial Economics* 129(3):440-457. https://doi.org/10.1016/j.jfineco.2018.06.004 (usada en el cap. 01; contexto del riesgo de la concentración)

### Registro de verificación (no verificado en esta sesión)

- Reglas de Paul Tudor Jones ("5 a 1", "no promediar pérdidas", media de 200 días) en fuente primaria.
- La anécdota de Dalio en 1982 (predicción de depresión y quiebra personal).
- El tamaño exacto de la posición de Soros contra la libra en 1992.
- Las cifras de Minervini en el U.S. Investing Championship.
- El 20% de Klarman desde 1982 (Wikipedia pide cita).
- El vehículo y el periodo exactos del ~19% neto de Oaktree.
- El "50.75% de aciertos" de Medallion.
- El supuesto estudio de Fidelity sobre pérdidas de los inversionistas de Magellan.
- Las cifras del Sharpe (0.79) y del apalancamiento (1.7) en la versión FAJ 2018 de *Buffett's Alpha*. El cap. 03 las usa; aquí se confirmaron 0.76 y 1.6 del borrador de 2013 con datos de 1976-2011.
- La causa de la caída de PSH en 2026.
- La composición exacta de *All Weather* después de 2009.
- Los rendimientos de Citadel en 2024 y 2025 y de Renaissance después de 2020.
