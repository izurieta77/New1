# Empresas chicas con utilidades: método pre-registrado, evidencia y primera pantalla

> 5-oct-2026. Pedido del dueño: "empresas chicas que nadie ve, con utilidades grandes y que podrían crecer fuerte, y saber cuándo entrar y salir". Fase 0: **papel**, esto NO es una recomendación de compra real. Solo información pública (REGLAS-MOTOR §0).
> Código: `conocimiento/fichas/codigo/2026-10-05-pantalla-chicas.py`. Salidas: `arena/investigacion/pantalla-chicas-2026-10-05.csv` (+ `-operabilidad.csv`, `-backtest.csv`, `.md`).

## 0. Registro previo (escrito ANTES de correr la pantalla y el backtest)

Esta sección se escribió y se congeló antes de ver cualquier resultado de la pantalla o del backtest (solo se conocían los conteos de las listas de la BMV). Los parámetros viven en el bloque `PARAMS` del script; si cambian después de ver resultados, el cambio se anota en §9 como desviación.

**Criterios de pantalla (todos obligatorios):**
| # | Criterio | Umbral |
|---|---|---|
| F1 | Tamaño (capitalización de mercado) | USD 300 M a USD 5,000 M |
| F2 | Utilidad neta | positiva en los 3 últimos ejercicios; NI(0) ≥ 1.2 × NI(−2); UDM positiva y ≥ 0.9 × NI(0) |
| F3 | Rentabilidad | ROIC ≥ 12% (EBIT × (1−t) / capital invertido) |
| F4 | Apalancamiento | deuda neta / EBITDA ≤ 2.0 (caja neta pasa); excluye financieras (sin EBIT/EBITDA comparable) |
| F5 | Caja | FCF (flujo operativo − capex) > 0 en el último ejercicio y en UDM; FCF/NI ≥ 0.6 |
| F6 | Precio | EV/EBIT ≤ 15 y EBIT > 0 |
| F7 | Dilución | acciones(0)/acciones(−2) ≤ 1.10 |
| F8 | Liquidez operable | mediana del importe diario (60 sesiones, serie .MX) ≥ 500,000 MXN; operó ≥ 90% de las sesiones; spread estimado (Corwin-Schultz) ≤ 1.5% |
| F9 | Título | precio de 1 título ≤ 2,500 MXN (25% de 10,000; el SIC no tiene fracciones) |
| F10 | Cobertura de analistas baja | **No hay dato gratuito verificable** (Yahoo quoteSummary exige credencial: HTTP 401). No se aplica; el tamaño máximo y la poca liquidez son el sustituto, y se declara. |

**Ranking de los que pasan:** promedio de rangos de ROIC (mayor mejor), crecimiento anual compuesto de NI a 2 años (mayor mejor) y EV/EBIT (menor mejor). Se reportan ≤ 15.

**Tamaño de posición (10,000 MXN por IA):** máximo 2,500 MXN (25%) por posición; objetivo 4-6 posiciones de 1,500-2,000 MXN; títulos completos; nunca más del 2% del importe diario mediano del título.

**Entrada:** solo después de que sale un reporte (10-K/10-Q) cuyo UDM pasa los filtros; orden limitada ≤ último cierre + 0.5%; dos tramos (50% ahora, 50% a 20 sesiones salvo que el precio haya caído > 10%, caso en que se revisa la tesis en vez de promediar); no se entra en las 5 sesiones previas al siguiente reporte esperado.

**Salida y alertas (se escriben antes de entrar):**
1. Stop duro: cierre −25% contra el costo.
2. Deterioro: tras cada reporte, si UDM NI < 0.75 × UDM del año previo, o FCF UDM < 0, o deuda neta/EBITDA > 3 → vender en ≤ 5 sesiones.
3. Evento legal inmediato (8-K ítems 1.03 quiebra, 3.01 aviso de deslistado, 4.01 cambio de auditor, 4.02 no confiar en estados, 2.04/2.06 aceleración de deuda o deterioro): salir el siguiente día hábil.
4. Dilución: acciones +10% en 12 meses u oferta secundaria > 10% → revisar y, si la tesis no cambia con el nuevo número de acciones, salir.
5. Valuación: EV/EBIT > 22 → vender la mitad.
6. Liquidez: mediana del importe diario < 250,000 MXN → salir.
7. Tiempo: 24 meses máximo; revisión obligatoria a los 12.

**Criterio de refutación (sobre el backtest, costos incluidos):** el método se descarta para papel si, en las fechas de formación probadas, (a) el exceso medio anual NETO (costo de ida y vuelta supuesto 2.0%: 0.58% comisión + 1.4% spread/impacto) contra el grupo de control (empresas del mismo rango de tamaño con utilidad neta positiva, muestra aleatoria con semilla) es ≤ +2 pp, o (b) en menos de 55% de los años gana al control, o (c) el límite inferior del intervalo bootstrap de 80% (por año) del exceso neto es < 0. Forward en papel: con ≥ 12 posiciones cerradas, si el exceso neto medio es ≤ 0 contra IWM convertido a MXN, se archiva.

**Diseño del backtest:** formación el 30-jun de 2015 a 2025 (11 fechas), con el último ejercicio anual completo (período terminado ≥ 90 días antes de la formación), retención de 12 meses, equiponderado. Datos: SEC EDGAR XBRL `frames` (fundamentales) y Yahoo chart v8 (precios; rendimiento con cierre ajustado; capitalización con precio sin ajustar por splits posteriores × acciones diluidas promedio). **Sesgos declarados de antemano:** (1) supervivencia: solo hay precios de Yahoo para tickers vigentes, así que las quiebras y deslistados no aparecen; se cuantifica y se hace un análisis de sensibilidad; (2) `frames` entrega el valor más reciente presentado (reexpresiones: ligera anticipación); (3) liquidez histórica: se usa importe diario en USD ≥ 1 M (60 sesiones previas) como sustituto; (4) solo ejercicios anuales (sin UDM); (5) la muestra de control es aleatoria; (6) poder estadístico bajo (pocas fechas, rendimientos solapados).

## 1. Qué se puede comprar (datos al 5-oct-2026; FX 18.07 MXN/USD)

**Fuentes primarias:** listas en vivo de la BMV (`BmvJsonGeneric`, la misma que alimenta bmv.com.mx/es/mercados/capitales y /mercado-global), liquidez 60 sesiones por Yahoo chart de la serie `.MX` (volumen operado en México), guía de GBM ya verificada en `arena/investigacion/01-gbm-operativa-y-costos.md` (0.25% + IVA por lado; sin mínimo por orden verificado; SIC sin fracciones; Trading USA con fracciones desde 1 USD, 0.25%, spread cambiario no publicado).

| Vía | Universo hoy | En rango USD 0.3-5 mil M | Con liquidez ≥ 500 mil MXN/día (F8) | Pasan utilidad/ROIC/deuda/FCF/precio (F2-F7) |
|---|---|---|---|---|
| BMV local (series operadas) | 110 series (106 con dato) | 47 | **25** | **0** (10 fallan un solo filtro) |
| SIC (acciones operadas hoy) | 449 series, 412 con ticker de EUA, 326 con dato `.MX` | 53 | **2** (MARA y BRKB; BRKB cuesta 9,134 MXN el título) | **0** |
| Trading USA (EUA directo) | "más de 2,500 acciones" según prensa de GBM (**no verificado en fuente primaria**; gbm.com/trading no da cifra) | 48 con utilidades y deuda sanas por EDGAR | 47 (liquidez de origen ≥ 1 M USD/día) | **14** (ver §5) |

**Lectura (con cifras):**
- **BMV:** sí hay un segmento chico real (47 series, mediana de capitalización 1,962 M USD, 25 líquidas). Pero es de ~100 emisoras y ninguna pasa los 7 filtros fundamentales a la vez; las que quedan a un filtro son de §5.2.
- **SIC:** casi nada operable en lo que importa. De las 53 series chicas, solo 2 mueven ≥ 500 mil MXN/día en México (MARA y BRKB), y solo **11 de 53 tienen utilidad neta positiva tres años seguidos**; la lista de series operadas del SIC está dominada por nombres especulativos (SPCE, LCID, PLUG, QUBT, SOUN, ACHR). El SIC ejecuta contra la bolsa de origen (BMV, página de Mercado Global: "liquidez ilimitada, ya sea por el mercado local u operando contra la bolsa de origen"), así que la liquidez local subestima lo operable, pero a costa de desviaciones medidas de 0.2-1.0% (hasta 9.5%) contra el valor justo en series poco operadas (`02-universo-sic-bmv-agresivo.md`). **Ninguna de las 30 emisoras de EUA que pasan o casi pasan los filtros (§5) tiene serie `.MX` en Yahoo**, es decir, no están en el SIC o no operan.
- Criterios de admisión al SIC (Ley del Mercado de Valores art. 263 y Reglamento Interior de la BMV, Reforma en materia de SIC): valores extranjeros de mercados reconocidos por la CNBV (NYSE, Nasdaq). Los documentos accesibles no fijan un piso numérico de capitalización ni de volumen (no verificado que exista). El tamaño lo pone el interés de los intermediarios, no una regla.
- **Costo de ida y vuelta con 10,000 MXN** (comisión 0.25% + IVA × 2 = 0.58% = 58 MXN; el spread se estima, el piso es 0.30%):
  | Vía | Spread / FX | Total sobre 10,000 | Sobre una orden de 2,000 |
  |---|---|---|---|
  | BMV líquida (spread Corwin-Schultz medido 0.4-1.0%) | 0.30-1.00% | 88 a 158 MXN (0.88-1.58%) | 17.6 a 31.6 MXN |
  | SIC delgado | 0.60% típico, hasta 1% | 118 a 158 MXN | 23.6 a 31.6 MXN |
  | Trading USA (compra y venta en USD; dos conversiones de peso) | 0.3% o 1.0% por conversión (no publicado) | 118 a 258 MXN (1.18-2.58%) | 23.6 a 51.6 MXN |
  | W-8BEN para el SIC (una vez) | 75 USD + IVA | **≈ 1,572 MXN = 15.7% de 10,000** | n/a |
- Con 10,000 MXN y tope de 2,500 por posición solo caben 4 posiciones: la diversificación es mínima y cada posición pesa 25%.

## 2. Evidencia a favor y en contra

| Hallazgo | Fuente | Efecto sobre este método |
|---|---|---|
| La prima de tamaño es débil e inestable. En EUA fue 0.66% anual (t = 0.36) desde 1992; no hay relación consistente entre tamaño y rendimiento realizado en 1980-1996 | cap. 02 de `conocimiento/` (Fama-French); Horowitz-Loughran-Savin, *J. Empirical Finance* 7(2), 2000 | En contra |
| Reaparece al controlar por calidad (la "basura" chica arrastra el promedio): prima estable, no concentrada en microcaps, en 30 industrias y 24 países | Asness, Frazzini, Israel, Moskowitz, Pedersen, "Size Matters, if You Control Your Junk", *JFE* 129(3), 2018 (abstract verificado); Hou-van Dijk, *RFS* 32(7), 2019 (el efecto desaparece por choques de rentabilidad negativos en chicas) | A favor, y respalda el filtro de calidad (F2-F5) |
| La rentabilidad bruta predice rendimiento como el valor (0.31% mensual, t = 2.49); correlación de -0.57 con value | Novy-Marx, *JFE* 108(1), 2013 (cap. 03) | A favor de F3 |
| Neglected-firm: las empresas ignoradas por instituciones y analistas rinden más, también controlando por tamaño (510 empresas, 10 años) | Arbel, Carvell, Strebel, "Giraffes, Institutions and Neglected Firms", *FAJ* 39(3), 1983 (abstract verificado; el trabajo de Arbel-Strebel de 1982 no lo verifiqué) | A favor, antiguo |
| ...pero con 7,117 acciones en 1982-1995, al controlar por capitalización "no hay prima de descuido"; el efecto lo absorbe el tamaño | Beard-Sias, "Is there a neglected-firm effect?", *FAJ* 53(5), 1997 (abstract verificado) | En contra |
| Con baja cobertura el momentum rinde 1.13% mensual contra 0.72% con alta; viene de los perdedores (las malas noticias viajan lento). Empresas sin analistas: 77.3% (1976) → 36.9% (1996) | Hong-Lim-Stein, *JF* 55(1), 2000 (cap. 26) | Mixto: la lentitud castiga más al que compra una mala noticia |
| Sin los retornos de los deslistados (−55% promedio) **no hay evidencia de que haya existido** prima de tamaño en Nasdaq | Shumway-Warther, *JF* 54(6), 1999 (abstract verificado) | **En contra, y es justo el sesgo de supervivencia de nuestra prueba (§4)** |
| Las anomalías pierden 26% fuera de muestra y 58% tras publicarse; las que sobreviven viven en acciones ilíquidas y de riesgo idiosincrático alto | McLean-Pontiff (cap. 26 §2.4, cap. 01); Hou-Xue-Zhang 2020: 65% de 452 anomalías falla al quitar microcaps | En contra |
| Costos de ejecución de 20-57 pb por operación aun para institucionales; solo sobreviven netas las anomalías de rotación < 50% mensual; size, value y rentabilidad tienen la mayor capacidad | Novy-Marx-Velikov, *RFS* 29(1), 2016 (cap. 02, 03) | Neutro: nuestra rotación es baja (≈ 1 vuelta al año), pero nuestros costos son mayores |
| El "PEAD" y otras señales de chicas viven en microcaps no operables (t = 1.43 sin microcaps) | Martineau 2022; Subrahmanyam 2025 (cap. 03) | En contra de buscar el edge en lo ilíquido |

**Veredicto de la evidencia:** hay una razón académica creíble para inclinarse a **chicas con calidad** (A favor: Asness et al., Novy-Marx), no para inclinarse a chicas a secas ni a "ignoradas" por serlo (Beard-Sias, Horowitz et al., Shumway-Warther). La ventaja, de existir, está medida **bruta, long-short y en universos con microcaps**. No hay un estudio verificado de empresas chicas mexicanas con cobertura baja (cap. 26 §4.5: "no verificado").

**Qué sobrevive a los costos de GBM (cálculo propio, 1 vuelta por año; costos de §1 como porcentaje del monto):**
| Ventaja bruta supuesta (pp/año) | BMV líquida (0.88%) | BMV cara (1.58%) | Trading USA FX 0.3% (1.18%) | Trading USA FX 1% (2.58%) |
|---|---|---|---|---|
| 1.2 (la que midió nuestro backtest, §4) | 27% | **−32%** | 2% | **−115%** |
| 2 | 56% | 21% | 41% | **−29%** |
| 3 | 71% | 47% | 61% | 14% |
| 4 | 78% | 60% | 70% | 36% |

Es decir: con una ventaja bruta de 2 pp/año sobrevive entre cero y 56% según vía; con la de 1.2 pp de nuestro backtest, prácticamente nada. Y rotar dos veces al año duplica el costo.

## 3. Método (ver §0)
Lo congelado en §0 es el método. Las reglas de entrada, tamaño, salida y alertas están implementadas como filtros y como alertas 8-K en el script; el stop de precio, el deterioro y la dilución se monitorean con `herramientas/edgar.py` y `portafolio.py` cuando se registre una posición en papel.

## 4. Prueba en el pasado (backtest pre-registrado, 30-jun 2015 a 2025)

Fundamentales: SEC EDGAR `frames`; precios: Yahoo (rendimiento total ajustado a 12 meses). S = emisoras que pasan F1-F7 (con deuda y flujo del ejercicio anual; sin UDM) y liquidez histórica ≥ 1 M USD/día; C = control: muestra aleatoria (150 por año, semilla 20261005) de emisoras con utilidad neta positiva, mismo rango de tamaño y liquidez. Equiponderado. Detalle por emisora y año en `arena/investigacion/pantalla-chicas-2026-10-05-backtest.csv`.

| Año de formación | n S | n C | Ret. S | Ret. C | IWM | S − C |
|---|---|---|---|---|---|---|
| 2015 | 14 | 65 | −7.1% | −0.2% | −6.6% | −6.8 |
| 2016 | 30 | 55 | +28.2% | +33.3% | +24.4% | −5.1 |
| 2017 | 33 | 57 | +14.7% | +9.8% | +17.7% | +4.9 |
| 2018 | 30 | 61 | −2.1% | +3.9% | −3.5% | −6.1 |
| 2019 | 44 | 53 | +5.0% | −11.4% | −6.6% | +16.4 |
| 2020 | 34 | 59 | +63.3% | +62.3% | +61.9% | +1.0 |
| 2021 | 29 | 54 | −12.7% | −15.8% | −25.4% | +3.1 |
| 2022 | 47 | 51 | +23.4% | +5.6% | +12.4% | +17.8 |
| 2023 | 32 | 45 | +7.3% | +9.2% | +9.8% | −1.9 |
| 2024 | 36 | 45 | −2.6% | +8.8% | +7.6% | −11.4 |
| 2025 | 30 | 57 | +42.8% | +41.3% | +40.7% | +1.5 |
| **Media** | | | **+14.6%** | **+13.4%** | **+12.0%** | **+1.2 bruto** |

- **Exceso medio bruto contra el control: +1.2 pp/año (6 de 11 años a favor). Neto de 2.0% de costo de ida y vuelta: −0.8 pp/año (4 de 11 años a favor); intervalo bootstrap de 80%: −4.2 a +2.7 pp.** Neto contra IWM: +0.5 pp.
- **Poder estadístico:** desviación del exceso 9.2 pp, error estándar 2.8 pp; el efecto mínimo detectable con 80% de potencia es **7.8 pp/año**. Con 11 fechas solo se detectaría una ventaja enorme. Que el intervalo incluya cero no prueba que no haya ventaja.
- **Contra los criterios pre-registrados (§0):** (a) exceso neto ≤ +2 pp → se cumple la condición de refutación (−0.8); (b) ganó al control en 6/11 = 54.5% de los años (< 55%) → se cumple; (c) límite inferior del IC de 80% < 0 → se cumple. **Por el criterio escrito de antemano, el método queda refutado como fuente de ventaja neta demostrada.** No se prueba que sea inútil (poder bajo), se prueba que esta evidencia no justifica pagar sus costos.
- **Sesgo de supervivencia (declarado, no corregible con datos gratis):** solo hay precios de Yahoo para tickers vigentes. Entre los emisores con utilidad neta positiva del ejercicio de formación, **solo 50.4% (2015) a 87.9% (2025) tiene hoy un ticker vigente** (1,549 de 3,073 en 2015; 2,337 de 2,658 en 2025). Los que faltan son adquiridas, deslistadas, quebradas o renombradas, y no se observan. Shumway-Warther muestra que ignorarlas puede crear o borrar una prima de tamaño. Los niveles de rendimiento (S 14.6%, C 13.4% en promedio) están inflados por el sesgo; el exceso S−C es menos sensible porque ambos grupos pierden las mismas bajas, pero un método que selecciona por calidad pierde menos quiebras que el control, así que **el sesgo, si acaso, favorece a C en contra de S, y no se puede acotar**. No se hizo análisis de sensibilidad numérico porque los faltantes no existen en los datos.
- Otros límites: `frames` entrega el valor más reciente presentado (reexpresiones: ligera anticipación); no filtra por fecha de presentación; solo emisoras con ejercicio aproximadamente calendario; deuda no reportada se tomó como 0; liquidez de EUA (USD) no la del SIC; las 11 fechas anuales se traslapan en emisoras.
- México: **no se hizo backtest** (Yahoo solo da ~4 años de fundamentales y la BMV no ofrece XBRL gratuito automatizable).

## 5. Primera pantalla (candidatos a estudio, no recomendación)

### 5.1 Operables hoy en México (BMV y SIC) con los filtros pre-registrados: **ninguno**
Embudo (BMV + SIC, 559 series): 432 con dato → **100** en rango de tamaño → 27 con liquidez F8 → 26 con título ≤ 2,500 MXN → **0** pasan además F2-F7. Filtros que más eliminan dentro del rango: ROIC (86 de 100), deuda neta/EBITDA o falta de dato (72), EV/EBIT (72), UDM (57), FCF (59).

Candidatos *post-hoc* (solo informativos; la pantalla pre-registrada no los acepta): BMV que fallan **un** filtro, de `arena/investigacion/pantalla-chicas-2026-10-05.csv`. **Segunda fuente: ninguna** (no hay XBRL de la BMV automatizable gratis), así que **estas cifras no están verificadas dos veces** y deben revisarse a mano contra los reportes trimestrales en bmv.com.mx.
| Emisora | Operable (liquidez) | Falla | Notas y advertencias de datos |
|---|---|---|---|
| HERDEZ * | Sí (1.07 M MXN/día) | FCF UDM −415 M | NI 1,320→1,786 M; ROIC 28.7%; deuda neta/EBITDA 0.27; EV/EBIT 3.4. FCF del año fue +2,845 M y la UDM negativa: ¿capital de trabajo o inversión? |
| LAB B | Sí (44.7 M/día) | ROIC 10.9% (< 12%) | NI 1,026→1,614 M; ND/EBITDA 1.54; EV/EBIT 5.7; dilución 3.1% |
| BOLSA A | Sí (37.1 M/día) | NI crece 6% en 2 años | ROIC 23.4%; caja neta; P/U 13.1; es la propia bolsa: ¿quién vende? |
| OMA B | Sí (142 M/día) | NI crece 7% | ROIC 26%; ND/EBITDA 1.15; P/U 15.4; más grande (4.6 mil M USD) |
| GRUMA B | Sí (80 M/día) | EV/EBIT 111 | **Descartar la cifra:** Yahoo da la utilidad en USD y el precio en MXN; el cociente es inválido |
| CIE B, PINFRA L, FRAGUA B, GPROFUT, CMOCTEZ | No (liquidez < 500 mil MXN/día o spread) | varios | CIE (NI ×9) y PINFRA (NI ×2.4) casi seguro contienen ganancias extraordinarias; cifras no confiables |

Pregunta obligatoria "¿quién está del otro lado?" para el segmento BMV: el vendedor típico es el fondo local que no puede mantener posiciones de 1-4 mil M USD (tope de concentración, redenciones) y el dueño-controlador que vende poco. Aceptan "perder" por mandato, no por ignorancia: **no es una ventaja de información**, es ilíquidez y cuota de mercado. Hipótesis [I], sin evidencia verificada para México.

### 5.2 Empresas de EUA que pasan los 7 filtros (universo B) y su operabilidad
Preselección: EDGAR frames, 5,088 emisoras con 3 ejercicios de utilidad neta → 197 pasan los filtros contables con datos del ejercicio 2025 → 48 en rango de tamaño → 47 con ≥ 1 M USD/día → **14 pasan F2-F7** con datos de Yahoo (UDM, deuda y caja trimestrales). Cada cifra salió de **tres rutas**: EDGAR frames (preselección), Yahoo fundamentals-timeseries (métricas) y EDGAR companyfacts vía `herramientas/edgar.py` (utilidad neta y flujo operativo del último ejercicio: diferencia 0.0% en las 14; no son fuentes totalmente independientes porque todas descienden de los 10-K, pero sí de procesos distintos). Alertas 8-K de 180 días: ninguna de quiebra, deslistado, cambio de auditor o no-confiar-en-estados; salen salidas de directivos (ítem 5.02), que es rutinario salvo TDC (2 en 2026) y ADEA/SKY (3).

**Operabilidad:** ninguna tiene serie `.MX`: solo por Trading USA de GBM (comisión 0.25%, spread cambiario no publicado, **disponibilidad por ticker no verificada** en la app; sin órdenes stop). Costo de ida y vuelta 1.18-2.58% (§1).

| Ticker | Qué es (nombre EDGAR) | Cap. M USD | NI 2 años (M USD) | ROIC | ND/EBITDA | EV/EBIT | Hipótesis de contraparte y refutación [I] |
|---|---|---|---|---|---|---|---|
| BLBD | Blue Bird | 1,791 | 24 → 128 | 71% | 0.0 | 5.4 | NI ×5.4: el mercado descuenta pico de ciclo. Refuta si EBIT UDM cae > 25% |
| TDC | Teradata | 2,815 | 62 → 130 | 66% | −0.4 | 4.1 | Software en declive de ingresos: vende quien ve reducción de base. Refuta si FCF UDM < 0 (hoy 734 M) |
| CARG | CarGurus | 2,682 | 37 → 156 | 53% | 0.2 | 10.7 | Mercado publicitario cíclico. Refuta si NI UDM < 0.75 × año previo |
| FLXS | Flexsteel | 362 | 10 → 33 | 25% | 0.7 | 9.1 | Muy chica (362 M); cobertura baja; ganancia puede ser margen cíclico de muebles |
| TASK | TaskUs | 739 | 46 → 102 | 15% | 1.6 | 6.5 | Riesgo de IA sobre el negocio de tercerización y de concentración de clientes |
| FHI | Federated Hermes | 4,201 | 299 → 403 | 28% | −0.1 | 7.3 | Gestor de activos: flujos y comisiones; tope superior de tamaño |
| GCT | GigaCloud | 1,946 | 94 → 137 | 32% | 0.9 | 11.5 | Muebles B2B transfronterizo: riesgo arancelario y de FX |
| TILE | Interface | 2,017 | 45 → 116 | 20% | 0.9 | 11.6 | NI ×2.6, margen cíclico (construcción comercial) |
| CRCT | Cricut | 1,365 | 54 → 77 | 24% | −1.8 | 9.4 | Consumo discrecional, caja neta alta; el mercado descuenta estancamiento |
| HRMY | Harmony Biosciences | 2,304 | 129 → 159 | 18% | −1.4 | 7.5 | Concentración en un fármaco y vencimiento de patentes |
| ITRN | Ituran | 1,039 | 48 → 58 | 32% | −1.0 | 11.0 | Emisor israelí: riesgo geopolítico y descuento por país |
| CVSA | Covista | 4,270 | 137 → 252 | 14% | 1.1 | 12.4 | Cercana al tope de tamaño; revisar qué compró para duplicar NI |
| MZTI | Marzetti | 2,716 | 159 → 192 | 15% | 0.7 | 12.1 | Alimentos defensivos: el crecimiento de NI es 10% anual, no "fuerte" |
| VMD | Viemed | 348 | 10 → 15 | 12% | 0.0 | 13.0 | Muy chica (348 M), ROIC justo en el umbral, dependiente de reembolsos de Medicare |

Notas: (1) las hipótesis de contraparte son *conjeturas a falsar con los reportes*, no hechos; no leí los 10-K de estas 14 empresas. (2) Los múltiplos bajos (EV/EBIT 4-7) con utilidad que se multiplicó son la firma de "el mercado cree que es pico", no de "nadie la ve": las 14 tienen cobertura de analistas desconocida (sin dato gratis) y liquidez de 3 a 85 M USD/día, o sea, **ni son invisibles ni son ilíquidas**. (3) Orden por rango promedio de ROIC, crecimiento de NI y EV/EBIT; archivo completo con 16 emisoras que fallan un solo filtro en `arena/investigacion/pantalla-chicas-2026-10-05-universoB.csv`.

## 6. Cuándo entrar y salir (lectura para el dueño)
- **No hay un "momento" que la evidencia respalde.** El método entra tras cada reporte que pasa el filtro y no antes de los siguientes 5 días de un reporte esperado; el calendario de reportes se obtiene de EDGAR (10-Q/10-K) y de la BMV (eventos relevantes). Lo que sí está respaldado es **salir por deterioro de utilidades o por evento legal**, que son reglas objetivas y que no dependen de adivinar precios.
- El stop de −25% en empresas con volatilidad de 40-60% anual se dispara por ruido con frecuencia alta; con costos de ida y vuelta de 1-2.6%, cada stop ruidoso cuesta lo que costaba el edge. Por eso el stop duro se complementa con el stop por tesis (§0, 2-4).
- Fase 0: todo esto se registra como pronósticos en papel (`herramientas/pronosticos.py`) antes de cualquier orden; no se compra nada real.

## 7. Límites de datos y accesos
- **Bloqueado o ausente:** Yahoo `quoteSummary` (401: sin crédito; no se obtuvo número de analistas ni estimaciones → F10 no aplicado); `stooq.com` y `api.nasdaq.com` (sin conexión desde el entorno); `gbm.com` responde con redirección, y su página de trading no da cifras de instrumentos; la lista de **valores listados** en el SIC (no solo operados hoy) es una tabla dinámica que no pude extraer; no hay XBRL de la BMV automatizable gratis; 86 series del SIC no tienen datos `.MX` en Yahoo.
- La lista de "series operadas" del SIC es la de la sesión del 5-oct (hora de corte 02:20 del servidor); un título listado que no operó ese día no aparece.
- Yahoo fundamentals-timeseries: ~4 ejercicios anuales; "deuda total" incluye arrendamientos (conservador).
- SEC: `data.sec.gov` frames y companyfacts respondieron 200 con User-Agent identificado; `www.sec.gov/files/company_tickers.json` también con el correo en el User-Agent.

## 8. Reproducir
`python3 conocimiento/fichas/codigo/2026-10-05-pantalla-chicas.py todo` (stdlib; cache en `datos/cache/chicas`; primera corrida ≈ 15-20 min por las ~3,000 descargas del backtest; con cache ≈ 2 min). Subcomandos: `operabilidad`, `pantalla`, `universob`, `backtest`.

## 9. Desviaciones respecto del registro previo (honestidad)
1. **Después** de ver que la pantalla pre-registrada dejaba 0 candidatos en BMV+SIC, agregué (a) la lista "casi" (fallan un solo filtro) y (b) el universo B de EUA (Trading USA) y la liquidez de origen para el SIC. Son extensiones declaradas; no cambian ningún umbral.
2. Mi primera corrida del backtest tenía un filtro por año de accesión que eliminaba a las emisoras sobrevivientes (n ≈ 1 por año y 14% de emisores con ticker vigente); lo quité y rehice la prueba una sola vez. Los umbrales no cambiaron; el resultado de esa corrida defectuosa (exceso +14.7 pp con n ≈ 1) se descarta por no ser informativo.
3. Se añadió un piso de spread de 0.30% a la columna de costo (Corwin-Schultz da 0 en series delgadas). F8 mantiene el spread medido del registro previo.
4. Se retiró un análisis de sensibilidad a los deslistados porque los datos faltantes no existen en Yahoo.

## Fuentes
- BMV Mercado Global y series operadas: https://www.bmv.com.mx/es/mercados/mercado-global ; capitales: https://www.bmv.com.mx/es/mercados/capitales ; Reforma al RI BMV en materia de SIC: https://bmv.com.mx/docs-pub/MARCO_NORMATIVO/CTEN_MNRR/Reforma%20al%20RI%20BMV%20en%20materia%20de%20SIC.pdf
- GBM comisiones y SIC: `arena/investigacion/01-gbm-operativa-y-costos.md`, `02-universo-sic-bmv-agresivo.md` (fuentes primarias citadas ahí). Trading USA ">2,500 acciones": https://elceo.com/mercados/gbm-presiona-a-casas-de-bolsa-para-llegar-a-nuevos-inversionistas-con-trading-usa/ y https://finantres.com/gbm-acciones/ (secundarias).
- Asness et al. 2018: https://som.yale.edu/publication/size-matters-if-you-control-your-junk · Arbel-Carvell-Strebel 1983: https://rpc.cfainstitute.org/research/financial-analysts-journal/1983/giraffes-institutions-and-neglected-firms · Beard-Sias 1997: https://rpc.cfainstitute.org/research/financial-analysts-journal/1997/is-there-a-neglected-firm-effect · Shumway-Warther 1999: https://ideas.repec.org/a/bla/jfinan/v54y1999i6p2361-2379.html · Hou-van Dijk 2019: https://ideas.repec.org/a/oup/rfinst/v32y2019i7p2850-2889..html · Horowitz-Loughran-Savin 2000: https://iro.uiowa.edu/esploro/outputs/journalArticle/Three-analyses-of-the-firm-size/9984963115102771
- SEC EDGAR frames y companyfacts: https://data.sec.gov/api/xbrl/frames/ ; Yahoo chart v8 y fundamentals-timeseries (sin credencial).
