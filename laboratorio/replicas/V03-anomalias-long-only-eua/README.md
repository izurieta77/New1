# V03. Anomalías de EUA: long-only (operable) frente a largo-corto (académico)

> Fecha: 25-sep-2026. Estado: **Replicado con diferencias** en las cifras recibidas, pero **sin versión long-only con apoyo estadístico** en 2000-2025, después de la publicación ni en MXN. No es una estrategia operable ni una recomendación.
>
> Para reproducir, desde la raíz del repo: `python3 laboratorio/replicas/V03-anomalias-long-only-eua/reproducir.py`. El script no usa red. Los datos están congelados en `datos/` y sus huellas, junto con la del pre-registro, en `SHA256SUMS.txt`. Las salidas son `resultados.json` y `variantes.csv`: 103 pruebas registradas y 8 exploratorias marcadas con `es_prueba=0`.

## Resumen

1. **Ninguna de las 16 pruebas primarias tiene apoyo:** 4 anomalías, cada una en versión LO-VW y LS-VW, en las ventanas 2000-2025 y post-publicación. Tampoco lo tiene ninguna de las 15 pruebas long-only en MXN.
2. **Lo operable (quintil bueno menos mercado, VW) paga poco.** Desde 2000 va de +0.8 a +2.1 pp al año (media × 12) y en ningún caso es significativo. Después de la publicación baja a entre +0.15 y +0.72 pp al año.
3. **"Rentables 4.5%" se reproduce, pero es el factor largo-corto RMW** (4.48% de 2000-01 a 2026-07, t = 2.28). El quintil de alta rentabilidad contra el mercado da **1.06% al año (t = 1.21)**.
4. **"Recompras 5.3%" se reproduce solo como largo-corto VW y solo si se incluye 2026:** 5.29%, t = 2.00. De 2000 a 2025 da 4.91%, con t = 1.87, y queda inconcluso. Las recompras contra el mercado dan **1.30% al año (t = 1.34)**, y después de 2008, **0.48% (t = 0.72)**.
5. **"Baja volatilidad 3.6% extra" no se reproduce** con ninguna definición registrada. Baja volatilidad contra el mercado da **0.84% al año (t = 0.52)**. Una exploración post-hoc encuentra 3.53% en el decil Lo 10 − Hi 10 (largo-corto, t = 0.50), que no es "extra sobre el mercado" ni es significativo.
6. **Lo único robusto es no operable.** NI-LS-EW (recompradores netos contra el quintil que más acciones emite, equiponderado) tiene apoyo en todas las ventanas, incluida la post-publicación: 10.7% al año, t = 2.63. Requiere vender en corto, y en la versión equiponderada el peso lo cargan las acciones pequeñas.
7. **Baja volatilidad sí redujo el riesgo** (descriptivo, sin prueba). De 2000 a 2025 tuvo volatilidad de 11.9% contra 15.7% y caída máxima de −36.5% contra −50.3% en USD. En MXN, la caída máxima fue −17.0% contra −39.9%.

## Por qué existe

El resumen de laboratorio recibido el 25-sep-2026 lista como "ventajas que sobreviven, y ahí voy a cazar": empresas muy rentables, que "en EUA pagan 4.5% al año desde 2000"; empresas que recompran, que "pagan 5.3%"; y acciones de baja volatilidad, que "dan 3.6% extra".

La regla del sistema es no adoptar una cifra ajena sin verificarla con datos y código propios. Además, en GBM no se puede ir en corto, así que lo relevante es la **pierna larga contra el mercado**, no el diferencial académico.

---

## PRE-REGISTRO

Lo que sigue es la copia literal de `prerregistro.md`, escrito a las 05:24 UTC del 2026-09-25. Su huella SHA-256 (`2d7164c3…`) quedó en `SHA256SUMS.txt` a las 05:25 UTC, antes de la primera corrida.


> Escrito el 2026-09-25 a las 05:24 UTC, **antes** de calcular cualquier rendimiento, media, t o intervalo con estos datos. Este archivo no se edita después de la primera corrida: su huella SHA-256 queda en `SHA256SUMS.txt`, y cualquier cambio posterior va a "Desviaciones del pre-registro" en `README.md`.
>
> Lo único que se miró antes de escribirlo fue la **estructura** de los archivos: secciones, nombres de columnas, rango de fechas, notas del preámbulo y, en NI, el NI promedio y el número de empresas por cartera, para saber cómo están armados los quintiles. No se calculó ningún rendimiento.

### 1. Preguntas y afirmaciones recibidas

1. Con los portafolios de Kenneth French para EUA, ¿el quintil "bueno" de cada anomalía le gana al mercado en versión **long-only**, que es lo único operable en GBM porque no hay cortos? ¿Y el diferencial **largo-corto** académico?
2. ¿Sobrevive después de la publicación de cada anomalía?
3. ¿Sobrevive medido en **MXN**?
4. Verificar las cifras recibidas: "rentables 4.5% anual desde 2000; recompras 5.3%; baja volatilidad 3.6% extra".

**Hipótesis previa (con signo).** Las cuatro anomalías tienen diferencial largo-corto positivo en la muestra completa. Espero que el exceso long-only sobre el mercado sea **menor** que el largo-corto, porque buena parte del premio académico suele venir de la pata corta, y que se debilite después de la publicación (McLean y Pontiff, 2016). No hay un mecanismo nuevo que probar. Se trata de medir cuánto de la cifra recibida es operable.

### 2. Datos (congelados en `datos/`, huellas en `SHA256SUMS.txt`)

| Serie | Archivo | Versión | Rango |
|---|---|---|---|
| Mercado (Mkt-RF + RF) | `F-F_Research_Data_Factors_CSV.zip` | CRSP 202607 | 1926-07 a 2026-07 |
| RMW, CMA | `F-F_Research_Data_5_Factors_2x3_CSV.zip` | CRSP 202607 (misma huella que V01) | 1963-07 a 2026-07 |
| Rentabilidad operativa | `Portfolios_Formed_on_OP_CSV.zip` | CRSP 202607 | 1963-07 a 2026-07 |
| Emisión neta de acciones | `Portfolios_Formed_on_NI_CSV.zip` | CRSP 202607 | 1963-07 a 2026-07 |
| Varianza total (60 días) | `Portfolios_Formed_on_VAR_CSV.zip` | CRSP 202607 | 1963-07 a 2026-07 |
| Varianza residual FF3 (60 días) | `Portfolios_Formed_on_RESVAR_CSV.zip` | CRSP 202607 | 1963-07 a 2026-07 |
| Inversión (crecimiento de activos) | `Portfolios_Formed_on_INV_CSV.zip` | CRSP 202607 | 1963-07 a 2026-07 |
| MXN por USD | FRED `DEXMXUS` (diario, mediodía NY) | descarga 2026-09-25 | 1993-11-08 a 2026-09-18 |

Todo se descargó el 2026-09-25 a las 05:22 UTC. Las series de French son rendimientos mensuales **sin costos**, en USD, antes de impuestos, e incluyen financieras y utilities.

**Construcción según French.** OP, NI e INV se arman a fin de junio con datos contables del año fiscal t-1 y breakpoints NYSE. VAR y RESVAR se arman cada mes con 60 días de rendimientos pasados. En NI, los quintiles y deciles se forman **solo con emisores positivos**: el NI promedio ponderado de "Lo 20" es positivo en todos los años revisados. Las carteras "< 0" (recompradores netos) y "ZERO" van aparte.

### 3. Series (lista cerrada)

Las carteras ponderadas por valor (VW) son las **primarias**.

| Código | Anomalía | Long-only (LO) = cartera − mercado | Largo-corto (LS) |
|---|---|---|---|
| OP | Alta rentabilidad operativa | Hi 20 − Mkt | Hi 20 − Lo 20 |
| NI | Recompras (emisión neta negativa) | "< 0" − Mkt | "< 0" − Hi 20 |
| VAR | Baja volatilidad total | Lo 20 − Mkt | Lo 20 − Hi 20 |
| INV | Baja inversión | Lo 20 − Mkt | Lo 20 − Hi 20 |

**Secundarias:**

- Mismas LS con carteras equiponderadas (EW), para las 4 anomalías. No hay LO-EW porque compararía una cartera EW contra un mercado VW y mezclaría el efecto tamaño.
- RESVAR (volatilidad idiosincrática, más cercana a Ang, Hodrick, Xing y Zhang), con LO = Lo 20 − Mkt y LS = Lo 20 − Hi 20 (VW).
- Factores RMW y CMA (2x3) como referencia y enlace con V01.

Mkt = Mkt-RF + RF (suma aritmética, como la construye French). Cada diferencia se calcula mes a mes.

### 4. Ventanas

Las fechas de publicación se verificaron con Crossref (mes del número de la revista):

| Anomalía | Artículo | Número | Primer mes post-publicación |
|---|---|---|---|
| OP (primaria) | Fama y French (2015), *JFE* 116(1), 1–22 | abril de 2015 (en línea desde oct-2014) | 2015-05 |
| OP (variante) | Novy-Marx (2013), *JFE* 108(1), 1–28 (rentabilidad **bruta**) | abril de 2013 | 2013-05 |
| NI | Pontiff y Woodgate (2008), *JF* 63(2), 921–945 | abril de 2008 | 2008-05 |
| VAR, RESVAR | Ang, Hodrick, Xing y Zhang (2006), *JF* 61(1), 259–299 | febrero de 2006 | 2006-03 |
| INV (primaria) | Cooper, Gulen y Schill (2008), *JF* 63(4), 1609–1651 | agosto de 2008 | 2008-09 |
| INV (variante) | Fama y French (2015) | abril de 2015 | 2015-05 |
| RMW, CMA | Fama y French (2015) | abril de 2015 | 2015-05 |

Ventanas por serie:

- **completo:** del inicio del archivo a 2026-07.
- **pre:** del inicio al mes de publicación.
- **2000-2025:** de 2000-01 a 2025-12.
- **2000-ult:** de 2000-01 a 2026-07. Es solo sensibilidad, para las afirmaciones "desde 2000".
- **post:** del primer mes post-publicación a 2026-07.

En MXN (solo LO, porque en GBM no hay cortos):

- **mxn-completo:** de 1994-01 a 2026-07.
- **2000-2025.**
- **post.**

### 5. Método

- **Métrica principal:** media mensual del diferencial, con error estándar **Newey-West de 6 rezagos** (Bartlett, corrección n/(n−1); `herramientas/estadistica.newey_west`) e IC95 = media ± 1.96·se. Se reporta también media × 12, que **no es CAGR**.
- **Veredicto (fijo):** "apoyo" si el límite inferior del IC95 es mayor que 0; "contraria" si el límite superior es menor que 0; "inconcluso" en cualquier otro caso.
- **Descriptivo (sin veredicto)** para LO: CAGR de la cartera y del mercado, diferencia de CAGR, volatilidad anualizada y caída máxima, en USD y en MXN.
- **MXN:** f_t = DEXMXUS(fin de mes t) / DEXMXUS(fin de mes t−1) − 1. Se usa la última observación no vacía de cada mes calendario. R_MXN = (1+R_USD)(1+f_t) − 1, y el exceso LO en MXN es R_MXN,cartera − R_MXN,Mkt = (R_cartera − R_Mkt)(1+f_t). DEXMXUS es una referencia de mediodía en Nueva York, no una cotización ejecutable en GBM.
- **Robustez (secundaria):** IC por bootstrap de bloques móviles (bloque de 12 meses, 5000 repeticiones, semilla 7) para las 8 series primarias en 2000-2025 y post.
- **Doble implementación dentro de `reproducir.py`:**
  - Un parser propio de CSV se compara contra `herramientas.datos_historicos.tabla_french`.
  - Un Newey-West escrito aparte, con la matriz de Bartlett completa, se compara contra `herramientas.estadistica`.
  - Si difieren en más de 1e-10, el script se detiene.
- **Faltantes:** -99.99 o -999 se tratan como faltante. Si una ventana tiene un faltante en alguna de sus series, se reporta y no se rellena. No se elimina ninguna observación después de ver resultados.

### 6. Costos (sensibilidad; no entra al veredicto)

- **Comisión GBM:** 0.25% + IVA = **0.29% por lado**. Es un hecho: Guía de Servicios GBM V1025, pág. 19, "se le aumentará el Impuesto al Valor Agregado"; FAQ de GBM, escalón de 0.25% hasta 1 millón de MXN. Verificado el 2026-09-25.
- **Spread:** 0.05% por lado. Es un **supuesto**, no un hecho.
- **Qué no se sabe:** los portafolios de French no traen la rotación, así que **no se inventa**. Se reporta la **rotación de equilibrio** τ\* = (media × 12) / (2 × 0.34%), que es la rotación anual en una vía que se come toda la ventaja media. Como ilustración, se reporta también el exceso neto con τ = 100% anual, lo que resta 0.68 pp al año.
- Frente a un ETF del mercado con rotación ≈ 0, este costo es adicional.
- Tampoco se modelan el costo cambiario, los impuestos ni la imposibilidad práctica de comprar cientos de acciones con 20,000 MXN.

### 7. Criterio para las afirmaciones recibidas

Una afirmación se **reproduce** si alguna definición registrada en la sección 3, en la ventana 2000-2025 o 2000-ult, da media × 12 **o** diferencia de CAGR dentro de ±0.30 pp de la cifra. Se reporta cuál definición coincide. Las candidatas son:

- **"Rentables 4.5%":** RMW, OP-LS-VW, OP-LO-VW y OP-LS-EW.
- **"Recompras 5.3%":** NI-LS-VW, NI-LO-VW y NI-LS-EW.
- **"Baja volatilidad 3.6% extra":** VAR-LO-VW (la palabra "extra" sugiere que es sobre el mercado), VAR-LS-VW, VAR-LS-EW, RESVAR-LO-VW y RESVAR-LS-VW.

La calificación de cada afirmación queda así:

- **"confirmada":** se reproduce **y** la versión LO-VW tiene "apoyo" en 2000-2025 **y** en post.
- **"confirmada con matices":** se reproduce, pero solo como LS, o sin significancia en LO, en post o en MXN.
- **"no confirmada":** ninguna definición registrada la reproduce.

Buscar la coincidencia entre varias definiciones y ventanas es un **jardín de caminos que se bifurcan**. Solo sirve para identificar qué midió quien dio la cifra, no como prueba de la anomalía.

### 8. Número de pruebas

| Grupo | Pruebas |
|---|---|
| 8 series primarias × 5 ventanas | 40 |
| 4 LS-EW × 5 ventanas | 20 |
| RESVAR, 2 series × 5 ventanas | 10 |
| RMW y CMA × 5 ventanas | 10 |
| Variantes de publicación (OP con Novy-Marx e INV con FF2015, LO y LS VW, pre y post) | 8 |
| MXN: 5 LO × 3 ventanas | 15 |
| **Total** | **≈ 103** |

Con tantas pruebas, un 5% de "apoyos" falsos es esperable si no hubiera efecto. Las **pruebas primarias** son 16: las 8 series primarias en 2000-2025 y en post.

### 9. Conclusiones que se decidirán solo con estos criterios

Una ventaja se considera **operable-candidata** solo si su LO-VW tiene "apoyo" en post **y** en MXN. Aun así, **no** sería una recomendación, porque faltarían ETF concreto, costos reales, impuestos y el papel.

---

## RESULTADOS (después de correr)

### Desviaciones del pre-registro

| Fecha | Qué cambió | Por qué | ¿Invalida algo? |
|---|---|---|---|
| 2026-09-25 | Se agregaron 8 celdas **exploratorias post-hoc**: deciles VW Lo 10 − Mkt y Lo 10 − Hi 10 de VAR y RESVAR, en 2000-2025 y 2000-ult. | Ninguna definición registrada reproducía "baja volatilidad 3.6%". Se buscaba solo el posible origen de la cifra. | No. Llevan `es_prueba=0`, no tienen veredicto y no cuentan como evidencia. |

No hubo otras desviaciones. Las ventanas, las series, el criterio de veredicto, el tratamiento en MXN, el bootstrap y el criterio para las afirmaciones son los del pre-registro.

### Controles de calidad

- **Datos.** La huella de los datos y del pre-registro se verifica al inicio (`herramientas/huellas.verificar`). Los 7 archivos de French son CRSP 202607. El archivo de 5 factores tiene la misma huella que en V01 (`b8653b41…`).
- **Parser propio contra `herramientas.datos_historicos.tabla_french`:** diferencia máxima de 5.6e-17 en las 12 tablas.
- **Newey-West.** La suma de autocovarianzas (`herramientas/estadistica.py`) se compara contra la forma cuadrática con la matriz de Bartlett completa (escrita aparte en `reproducir.py`). La diferencia máxima del error estándar es de 7.2e-16 en las 111 celdas.
- **Tercera ruta independiente** (fuera del script, con `tabla_french` + `datos.parsear_fred_csv` + `metricas.cagr/max_drawdown`). Reproduce al centésimo el CAGR, la caída máxima, la media y la t de VAR-LO 2000-2025 (USD y MXN), NI-LO post (USD y MXN) y OP-LO 2000-2025 (USD y MXN).
- **Enlace con V01.** RMW 2000-2025 da 4.76% al año y t = 2.43, y RMW 2000-01 a 2026-07 da 4.48% y t = 2.28. Son idénticos a V01.
- **Faltantes.** No hay ningún -99.99 o -999 en las series usadas.

### 1. Long-only VW: cartera "buena" menos mercado, en USD

Cada celda muestra media × 12 en % (t NW de 6 rezagos). Las celdas en **negrita** tienen veredicto "apoyo" (límite inferior del IC95 > 0). Las demás son "inconcluso"; ninguna salió "contraria".

| Serie | Definición | Último mes pre | completo | pre | 2000-2025 | 2000-ult | post |
|---|---|---|---|---|---|---|---|
| OP-LO-VW | OP Hi 20 VW − Mkt | 2015-04 | 1.06 (1.89) | 1.14 (1.82) | 1.06 (1.21) | 0.92 (1.04) | 0.72 (0.56) |
| NI-LO-VW | NI "< 0" VW − Mkt | 2008-04 | **1.97 (3.22)** | **2.58 (3.19)** | 1.30 (1.34) | 1.28 (1.35) | 0.48 (0.72) |
| VAR-LO-VW | VAR Lo 20 VW − Mkt | 2006-02 | −0.09 (−0.11) | −0.21 (−0.20) | 0.84 (0.52) | 0.85 (0.53) | 0.15 (0.09) |
| INV-LO-VW | INV Lo 20 VW − Mkt | 2008-08 | **2.39 (2.71)** | **3.11 (3.09)** | 2.09 (1.42) | 2.15 (1.49) | 0.55 (0.32) |
| RESVAR-LO-VW | RESVAR Lo 20 VW − Mkt | 2006-02 | 0.21 (0.31) | 0.24 (0.29) | 0.79 (0.68) | 0.65 (0.56) | 0.14 (0.12) |

Todas las series arrancan en 1963-07 y terminan en 2026-07.

### 2. Largo-corto VW (académico; no operable en GBM)

| Serie | Definición | Último mes pre | completo | pre | 2000-2025 | 2000-ult | post |
|---|---|---|---|---|---|---|---|
| OP-LS-VW | OP Hi 20 − Lo 20 | 2015-04 | 2.63 (1.70) | 2.50 (1.50) | 5.08 (1.89) | 4.26 (1.52) | 3.24 (0.79) |
| NI-LS-VW | NI "< 0" − Hi 20 | 2008-04 | **5.84 (4.05)** | **6.58 (4.13)** | 4.91 (1.87) | **5.29 (2.00)** | 4.04 (1.31) |
| VAR-LS-VW | VAR Lo 20 − Hi 20 | 2006-02 | 1.56 (0.51) | 2.36 (0.66) | 2.71 (0.51) | 1.70 (0.32) | −0.12 (−0.02) |
| INV-LS-VW | INV Lo 20 − Hi 20 | 2008-08 | 2.66 (1.78) | **4.10 (2.36)** | 2.50 (0.93) | 2.76 (1.05) | −0.95 (−0.33) |
| RESVAR-LS-VW | RESVAR Lo 20 − Hi 20 | 2006-02 | 2.09 (0.72) | 3.30 (0.99) | 2.76 (0.56) | 1.23 (0.24) | −0.44 (−0.08) |

### 3. Largo-corto equiponderado y factores de referencia

| Serie | Definición | Último mes pre | completo | pre | 2000-2025 | 2000-ult | post |
|---|---|---|---|---|---|---|---|
| OP-LS-EW | OP Hi 20 − Lo 20 (EW) | 2015-04 | 1.17 (0.72) | 0.45 (0.27) | 3.04 (0.99) | 3.17 (1.06) | 4.48 (0.92) |
| NI-LS-EW | NI "< 0" − Hi 20 (EW) | 2008-04 | **10.41 (5.75)** | **10.30 (5.30)** | **11.25 (3.02)** | **11.65 (3.18)** | **10.70 (2.63)** |
| VAR-LS-EW | VAR Lo 20 − Hi 20 (EW) | 2006-02 | 1.95 (0.62) | 0.11 (0.03) | 4.75 (0.85) | 4.87 (0.89) | 5.81 (0.97) |
| INV-LS-EW | INV Lo 20 − Hi 20 (EW) | 2008-08 | **8.43 (6.61)** | **9.94 (6.95)** | **7.39 (3.10)** | **7.19 (3.06)** | 4.63 (1.81) |
| RMW | Factor 2x3 (robusta − débil) | 2015-04 | **3.08 (2.86)** | **3.16 (2.59)** | **4.76 (2.43)** | **4.48 (2.28)** | 2.73 (1.23) |
| CMA | Factor 2x3 (conservadora − agresiva) | 2015-04 | **2.96 (2.88)** | **3.67 (3.34)** | 2.53 (1.41) | 2.75 (1.57) | −0.33 (−0.13) |

### 4. Detalle de las 16 pruebas primarias (IC Newey-West y bootstrap de bloques)

| Serie | Ventana | Meses | n | Media %/mes | ×12 % | t NW(6) | IC95 NW (%/mes) | IC95 bootstrap (bloques de 12) | Veredicto |
|---|---|---|---|---|---|---|---|---|---|
| OP-LO-VW | 2000-2025 | 200001–202512 | 312 | 0.089 | 1.06 | 1.21 | [−0.055, 0.232] | [−0.047, 0.255] | inconcluso |
| OP-LO-VW | post | 201505–202607 | 135 | 0.060 | 0.72 | 0.56 | [−0.150, 0.269] | [−0.137, 0.310] | inconcluso |
| OP-LS-VW | 2000-2025 | 200001–202512 | 312 | 0.423 | 5.08 | 1.89 | [−0.016, 0.862] | [0.018, 0.913] | inconcluso |
| OP-LS-VW | post | 201505–202607 | 135 | 0.270 | 3.24 | 0.79 | [−0.396, 0.936] | [−0.330, 0.977] | inconcluso |
| NI-LO-VW | 2000-2025 | 200001–202512 | 312 | 0.108 | 1.30 | 1.34 | [−0.050, 0.266] | [−0.048, 0.282] | inconcluso |
| NI-LO-VW | post | 200805–202607 | 219 | 0.040 | 0.48 | 0.72 | [−0.068, 0.148] | [−0.073, 0.128] | inconcluso |
| NI-LS-VW | 2000-2025 | 200001–202512 | 312 | 0.409 | 4.91 | 1.87 | [−0.020, 0.837] | [−0.012, 0.874] | inconcluso |
| NI-LS-VW | post | 200805–202607 | 219 | 0.337 | 4.04 | 1.31 | [−0.165, 0.839] | [−0.243, 0.660] | inconcluso |
| VAR-LO-VW | 2000-2025 | 200001–202512 | 312 | 0.070 | 0.84 | 0.52 | [−0.194, 0.334] | [−0.166, 0.356] | inconcluso |
| VAR-LO-VW | post | 200603–202607 | 245 | 0.012 | 0.15 | 0.09 | [−0.249, 0.273] | [−0.252, 0.270] | inconcluso |
| VAR-LS-VW | 2000-2025 | 200001–202512 | 312 | 0.226 | 2.71 | 0.51 | [−0.648, 1.099] | [−0.561, 1.177] | inconcluso |
| VAR-LS-VW | post | 200603–202607 | 245 | −0.010 | −0.12 | −0.02 | [−0.949, 0.929] | [−0.919, 0.968] | inconcluso |
| INV-LO-VW | 2000-2025 | 200001–202512 | 312 | 0.175 | 2.09 | 1.42 | [−0.066, 0.415] | [−0.099, 0.423] | inconcluso |
| INV-LO-VW | post | 200809–202607 | 215 | 0.046 | 0.55 | 0.32 | [−0.237, 0.329] | [−0.232, 0.367] | inconcluso |
| INV-LS-VW | 2000-2025 | 200001–202512 | 312 | 0.208 | 2.50 | 0.93 | [−0.228, 0.644] | [−0.297, 0.686] | inconcluso |
| INV-LS-VW | post | 200809–202607 | 215 | −0.079 | −0.95 | −0.33 | [−0.548, 0.390] | [−0.583, 0.432] | inconcluso |

**Discrepancia registrada.** En OP-LS-VW 2000-2025, el bootstrap excluye el cero y Newey-West no. El veredicto pre-registrado es el de Newey-West, así que la prueba queda **inconclusa**. El bootstrap era solo robustez secundaria.

### 5. Variantes de fecha de publicación

| Serie | Corte | Ventana | Meses | ×12 % | t NW(6) | IC95 (%/mes) | Veredicto |
|---|---|---|---|---|---|---|---|
| OP-LO-VW | Novy-Marx 2013 (abr-2013) | pre | 196307–201304 | 1.14 | 1.77 | [−0.010, 0.200] | inconcluso |
| OP-LO-VW | Novy-Marx 2013 | post | 201305–202607 | 0.76 | 0.69 | [−0.117, 0.245] | inconcluso |
| OP-LS-VW | Novy-Marx 2013 | pre | 196307–201304 | 2.66 | 1.54 | [−0.060, 0.503] | inconcluso |
| OP-LS-VW | Novy-Marx 2013 | post | 201305–202607 | 2.53 | 0.72 | [−0.367, 0.790] | inconcluso |
| INV-LO-VW | Fama-French 2015 (abr-2015) | pre | 196307–201504 | 3.10 | 3.32 | [0.106, 0.410] | apoyo |
| INV-LO-VW | Fama-French 2015 | post | 201505–202607 | −0.89 | −0.39 | [−0.447, 0.299] | inconcluso |
| INV-LS-VW | Fama-French 2015 | pre | 196307–201504 | 3.80 | 2.42 | [0.060, 0.573] | apoyo |
| INV-LS-VW | Fama-French 2015 | post | 201505–202607 | −2.58 | −0.63 | [−0.880, 0.450] | inconcluso |

### 6. Exceso long-only sobre el mercado en MXN

Ambas piernas se convierten con DEXMXUS de fin de mes, así que el exceso en MXN es (R_cartera − R_Mkt)(1 + f).

| Serie | Ventana | Meses | n | Media %/mes | ×12 % | t NW(6) | IC95 (%/mes) | Veredicto |
|---|---|---|---|---|---|---|---|---|
| OP-LO-VW | mxn-completo | 199401–202607 | 391 | 0.087 | 1.04 | 1.28 | [−0.046, 0.220] | inconcluso |
| OP-LO-VW | 2000-2025 | 200001–202512 | 312 | 0.097 | 1.16 | 1.30 | [−0.049, 0.243] | inconcluso |
| OP-LO-VW | post | 201505–202607 | 135 | 0.069 | 0.83 | 0.63 | [−0.145, 0.284] | inconcluso |
| NI-LO-VW | mxn-completo | 199401–202607 | 391 | 0.125 | 1.50 | 1.68 | [−0.021, 0.271] | inconcluso |
| NI-LO-VW | 2000-2025 | 200001–202512 | 312 | 0.114 | 1.37 | 1.41 | [−0.045, 0.273] | inconcluso |
| NI-LO-VW | post | 200805–202607 | 219 | 0.045 | 0.54 | 0.81 | [−0.065, 0.155] | inconcluso |
| VAR-LO-VW | mxn-completo | 199401–202607 | 391 | 0.007 | 0.08 | 0.05 | [−0.231, 0.244] | inconcluso |
| VAR-LO-VW | 2000-2025 | 200001–202512 | 312 | 0.090 | 1.09 | 0.67 | [−0.176, 0.357] | inconcluso |
| VAR-LO-VW | post | 200603–202607 | 245 | 0.034 | 0.40 | 0.25 | [−0.232, 0.299] | inconcluso |
| INV-LO-VW | mxn-completo | 199401–202607 | 391 | 0.131 | 1.57 | 1.27 | [−0.071, 0.333] | inconcluso |
| INV-LO-VW | 2000-2025 | 200001–202512 | 312 | 0.174 | 2.09 | 1.42 | [−0.067, 0.416] | inconcluso |
| INV-LO-VW | post | 200809–202607 | 215 | 0.045 | 0.54 | 0.31 | [−0.239, 0.329] | inconcluso |
| RESVAR-LO-VW | mxn-completo | 199401–202607 | 391 | 0.056 | 0.67 | 0.65 | [−0.111, 0.223] | inconcluso |
| RESVAR-LO-VW | 2000-2025 | 200001–202512 | 312 | 0.079 | 0.95 | 0.80 | [−0.114, 0.272] | inconcluso |
| RESVAR-LO-VW | post | 200603–202607 | 245 | 0.028 | 0.33 | 0.28 | [−0.167, 0.222] | inconcluso |

Medir en MXN casi no cambia el exceso, porque el tipo de cambio multiplica ambas piernas por igual. Lo que sí cambia es el nivel de rendimiento y las caídas (tabla 7).

### 7. Descriptivo long-only (sin prueba estadística)

El CAGR es geométrico. La diferencia de CAGR **no** es la media × 12: con menor volatilidad, la diferencia de CAGR supera a la media × 12.

| Serie | Ventana | Moneda | CAGR cartera | CAGR mercado | Dif. CAGR (pp) | Vol. cartera | Vol. mercado | Caída máx. cartera | Caída máx. mercado |
|---|---|---|---|---|---|---|---|---|---|
| OP-LO-VW | completo | USD | 12.02% | 10.85% | +1.17 | 15.4% | 15.4% | −50.0% | −50.3% |
| OP-LO-VW | 2000-2025 | USD | 9.60% | 8.27% | +1.33 | 14.6% | 15.7% | −42.5% | −50.3% |
| OP-LO-VW | post | USD | 14.55% | 13.70% | +0.86 | 15.4% | 15.6% | −23.7% | −24.8% |
| NI-LO-VW | completo | USD | 13.18% | 10.85% | +2.32 | 14.6% | 15.4% | −48.3% | −50.3% |
| NI-LO-VW | 2000-2025 | USD | 9.91% | 8.27% | +1.64 | 14.2% | 15.7% | −48.3% | −50.3% |
| NI-LO-VW | post | USD | 12.54% | 11.86% | +0.68 | 15.4% | 16.2% | −43.2% | −45.9% |
| VAR-LO-VW | completo | USD | 11.26% | 10.85% | +0.41 | 12.1% | 15.4% | −42.3% | −50.3% |
| VAR-LO-VW | 2000-2025 | USD | 9.76% | 8.27% | +1.49 | 11.9% | 15.7% | −36.5% | −50.3% |
| VAR-LO-VW | post | USD | 11.83% | 11.14% | +0.69 | 12.3% | 15.6% | −36.5% | −50.3% |
| INV-LO-VW | completo | USD | 13.28% | 10.85% | +2.42 | 16.7% | 15.4% | −53.5% | −50.3% |
| INV-LO-VW | 2000-2025 | USD | 10.31% | 8.27% | +2.04 | 17.0% | 15.7% | −53.5% | −50.3% |
| INV-LO-VW | post | USD | 12.77% | 12.44% | +0.33 | 17.7% | 16.2% | −45.3% | −41.6% |
| RESVAR-LO-VW | 2000-2025 | USD | 9.54% | 8.27% | +1.27 | 13.1% | 15.7% | −38.3% | −50.3% |
| OP-LO-VW | 2000-2025 | MXN | 12.33% | 10.98% | +1.36 | 13.4% | 13.9% | −32.4% | −39.9% |
| OP-LO-VW | post | MXN | 15.77% | 14.90% | +0.86 | 15.6% | 15.1% | −25.2% | −27.2% |
| NI-LO-VW | 2000-2025 | MXN | 12.66% | 10.98% | +1.68 | 12.8% | 13.9% | −27.9% | −39.9% |
| NI-LO-VW | post | MXN | 15.66% | 14.97% | +0.70 | 13.3% | 13.8% | −24.6% | −27.2% |
| VAR-LO-VW | 2000-2025 | MXN | 12.50% | 10.98% | +1.52 | 11.6% | 13.9% | −17.0% | −39.9% |
| VAR-LO-VW | post | MXN | 14.63% | 13.93% | +0.70 | 11.7% | 13.5% | −17.0% | −30.0% |
| INV-LO-VW | 2000-2025 | MXN | 13.07% | 10.98% | +2.09 | 15.4% | 13.9% | −34.5% | −39.9% |
| INV-LO-VW | post | MXN | 16.09% | 15.75% | +0.34 | 15.4% | 13.7% | −21.3% | −27.2% |

Las filas completas, incluidas mxn-completo y RESVAR, están en `resultados.json` y en la salida del script. "Mercado" es el mercado CRSP VW de French (Mkt-RF + RF), **no** el S&P 500.

### 8. Costos (sensibilidad, no entra al veredicto)

- **Comisión GBM:** 0.25% + IVA = 0.29% por lado, confirmada el 2026-09-25 en la Guía de Servicios V1025, pág. 19, y en la FAQ de comisiones.
- **Spread:** 0.05% por lado, **supuesto**.
- **Rotación:** French no publica la rotación de estas carteras, así que no se inventa.
- τ\* es la rotación anual (en una vía) que se come toda la ventaja media.

| Serie | Ventana | ×12 bruto % | τ\* | ×12 neto con τ = 100% |
|---|---|---|---|---|
| OP-LO-VW | 2000-2025 | 1.06 | 156% | 0.38 |
| OP-LO-VW | post | 0.72 | 105% | 0.04 |
| NI-LO-VW | 2000-2025 | 1.30 | 191% | 0.62 |
| NI-LO-VW | post | 0.48 | 70% | −0.20 |
| VAR-LO-VW | 2000-2025 | 0.84 | 123% | 0.16 |
| VAR-LO-VW | post | 0.15 | 22% | −0.53 |
| INV-LO-VW | 2000-2025 | 2.09 | 308% | 1.41 |
| INV-LO-VW | post | 0.55 | 82% | −0.13 |
| OP-LO-VW, MXN | post | 0.83 | 122% | 0.15 |
| NI-LO-VW, MXN | post | 0.54 | 80% | −0.14 |
| VAR-LO-VW, MXN | post | 0.40 | 59% | −0.28 |
| INV-LO-VW, MXN | post | 0.54 | 79% | −0.14 |

Después de la publicación, con una sola rotación completa al año, NI, VAR e INV quedan en negativo y OP en ≈ 0. VAR se rearma **cada mes**, así que su rotación real muy probablemente supera el 22% anual que se come su ventaja. Esto es una inferencia: la rotación no está medida.

### 9. Afirmaciones recibidas

El criterio pre-registrado es ±0.30 pp en media × 12 o en diferencia de CAGR, en las ventanas 2000-2025 o 2000-ult.

**"Rentables 4.5% anual desde 2000"**

- **Se reproduce** como RMW: 4.76% en 2000-2025 (t = 2.43, apoyo) y 4.48% en 2000-ult (t = 2.28, apoyo). También como OP-LS-VW 2000-ult: 4.26% (t = 1.52, inconcluso).
- **Pero la versión operable no paga eso.** OP-LO-VW da 1.06% en 2000-2025 (t = 1.21) y 0.72% en post (t = 0.56). En MXN post da 0.83% (t = 0.63). RMW post-2015 da 2.73% (t = 1.23), inconcluso.
- **Calificación: confirmada con matices.** La cifra existe, pero es el diferencial largo-corto académico. El quintil rentable contra el mercado da cerca de una cuarta parte y no es significativo.

**"Recompras 5.3%"**

- **Se reproduce solo** como NI-LS-VW 2000-ult: 5.29% (t = 2.00, apoyo al límite: IC95 [0.010, 0.872]). Con 2000-2025 da 4.91% (t = 1.87, inconcluso). O sea, la significancia depende de 7 meses de 2026.
- **La versión operable no la sostiene.** NI-LO-VW da 1.30% en 2000-2025 (t = 1.34) y 0.48% en post (t = 0.72). En MXN post da 0.54% (t = 0.81).
- NI-LS-EW sí es fuerte en todas las ventanas (11.25% en 2000-2025, 10.70% en post), pero es otra cosa: largo-corto, equiponderado y cargado a acciones pequeñas.
- **Calificación: confirmada con matices.**

**"Baja volatilidad 3.6% extra"**

- **Ninguna de las 20 comparaciones registradas coincide.**
  - VAR-LO-VW: 0.84% en 2000-2025 (t = 0.52); diferencia de CAGR 1.49.
  - VAR-LS-VW: 2.71%.
  - VAR-LS-EW: 4.75%.
  - RESVAR-LO-VW: 0.79%.
  - RESVAR-LS-VW: 2.76%.
- **Exploratorio post-hoc (no es prueba):**

  | Serie | Ventana | n | ×12 % | Dif. CAGR | t NW(6) | IC95 (%/mes) |
  |---|---|---|---|---|---|---|
  | VAR Lo 10 − Mkt | 2000-2025 | 312 | 0.39 | 1.07 | 0.18 | [−0.318, 0.384] |
  | VAR Lo 10 − Mkt | 2000-ult | 319 | −0.07 | 0.57 | −0.03 | [−0.360, 0.348] |
  | VAR Lo 10 − Hi 10 | 2000-2025 | 312 | 6.02 | 12.35 | 0.89 | [−0.602, 1.606] |
  | VAR Lo 10 − Hi 10 | 2000-ult | 319 | **3.53** | 10.26 | 0.50 | [−0.857, 1.446] |
  | RESVAR Lo 10 − Mkt | 2000-2025 | 312 | 1.79 | 2.38 | 1.07 | [−0.125, 0.423] |
  | RESVAR Lo 10 − Mkt | 2000-ult | 319 | 1.36 | 1.92 | 0.79 | [−0.167, 0.393] |
  | RESVAR Lo 10 − Hi 10 | 2000-2025 | 312 | 6.26 | 12.10 | 0.98 | [−0.523, 1.567] |
  | RESVAR Lo 10 − Hi 10 | 2000-ult | 319 | 4.65 | 10.76 | 0.72 | [−0.673, 1.447] |

  El único valor cercano a 3.6 es un largo-corto de deciles (t = 0.50). No es un "extra" sobre el mercado y su t es de 0.50. Pasar de 2000-2025 a 2000-ult lo mueve de 6.02 a 3.53: es una cifra muy inestable.
- **Calificación: no confirmada.** El origen de la cifra no está identificado.

### 10. Recuento

- **Pruebas registradas:** 103.
- **Con "apoyo":** 25. Todas están en ventanas completas o pre-publicación, o en RMW desde 2000, NI-LS-VW 2000-ult y las LS equiponderadas. Solo **una** está en post-publicación: NI-LS-EW.
- **Pruebas primarias con apoyo:** 0 de 16.
- **Pruebas en MXN con apoyo:** 0 de 15.

---

## Conclusiones permitidas

Todas valen para EUA, carteras de French CRSP 202607, sin costos salvo que se indique, antes de impuestos y medidas contra el mercado CRSP VW.

1. **En toda la muestra 1963-2026, dos versiones long-only VW le ganaron al mercado con significancia:**
   - Recompradores netos: +1.97 pp al año (t = 3.22).
   - Baja inversión: +2.39 pp al año (t = 2.71).
   
   **Alta rentabilidad** (+1.06, t = 1.89) y **baja volatilidad** (−0.09, t = −0.11) no lo hicieron.
2. **Después de la publicación, ninguna versión long-only VW tiene apoyo**, ni en USD ni en MXN. Los excesos medios caen a +0.15 / +0.48 / +0.55 / +0.72 pp al año (VAR / NI / INV / OP). Es consistente con el debilitamiento post-publicación que documentan McLean y Pontiff (2016). Esta réplica no prueba la causa.
3. **Desde 2000, ninguna versión long-only VW tiene apoyo** (t entre 0.52 y 1.42). Tampoco en MXN.
4. **La cifra de "rentables 4.5%" es real, pero es el factor largo-corto RMW** (V01 y V03 coinciden). La mayor parte de ese diferencial no está disponible sin cortos: el quintil alto contra el mercado da cerca de 1% al año.
5. **"Recompras 5.3%" corresponde al largo-corto VW de 2000-01 a 2026-07**, con significancia al límite y frágil ante la ventana.
6. **"Baja volatilidad 3.6% extra" no se reproduce** con ninguna definición registrada.
7. **Descriptivo, sin inferencia:** la cartera de baja volatilidad (VAR Lo 20 VW) tuvo menor volatilidad y menores caídas que el mercado.
   - 2000-2025, USD: volatilidad 11.9% contra 15.7%; caída máxima −36.5% contra −50.3%.
   - 2000-2025, MXN: caída máxima −17.0% contra −39.9%.
   
   Su diferencia de CAGR fue +1.49 pp en USD, pero la diferencia de medias no es significativa. Su valor, si existe, está en **reducir el riesgo**, no en un rendimiento extra demostrado.
8. **Lo único que sobrevive después de la publicación es NI-LS-EW** (+10.70 pp al año, t = 2.63), que no es operable en GBM porque requiere cortos y depende de acciones pequeñas.

## Conclusiones que NO se sostienen

- Que "las empresas muy rentables pagan 4.5% al año" **para quien solo puede comprar**. Lo medido long-only es cerca de 1% al año y no es significativo.
- Que las recompras paguen 5.3% al año comprándolas. Long-only, desde 2008, es 0.48% al año (t = 0.72).
- Que la baja volatilidad dé "3.6% extra".
- Que alguna de estas cuatro anomalías sea "una ventaja que sobrevive" en versión long-only después de su publicación, en USD o en MXN.
- Que "la ventaja está en elegir bien qué empresas comprar" con estas cuatro características. En su versión operable no hay evidencia estadística de que eso agregue rendimiento desde 2000.
- Que el exceso sobreviva a los costos de GBM. Con una rotación completa al año, la ventaja post-publicación de NI, VAR e INV se vuelve negativa y la de OP queda en ≈ 0. La rotación real no está medida.
- Que medir en pesos "crea" una ventaja. El tipo de cambio multiplica por igual la cartera y el mercado, así que no cambia el exceso de forma relevante. Solo cambia el nivel de rendimiento y las caídas.
- Que estos resultados se trasladen a ETFs concretos del SIC (calidad, recompras, baja volatilidad). No se probaron. Tienen otras reglas, costos de administración y otros periodos.
- Que la media × 12 sea un CAGR o lo que obtendría un inversionista.

## Estado

- **Replicado con diferencias** en las cifras recibidas:
  - "Rentables 4.5%": sí, como RMW largo-corto.
  - "Recompras 5.3%": sí, como NI-LS-VW 2000-ult, al límite.
  - "Baja volatilidad 3.6%": no.
- **No replicado** como ventaja long-only operable: 0 de 8 pruebas long-only primarias y 0 de 15 en MXN tienen apoyo.

**Pendiente:**

1. Rotación real de las carteras, para medir el costo neto.
2. ETFs concretos disponibles en el SIC para cada estilo. La disponibilidad no está verificada. Habría que medir su historia real en MXN con costos de GBM.
3. Costo cambiario de GBM (no publicado).
4. Impuestos (10% sobre la ganancia en el SIC y retención de dividendos).
5. Ejecución por el `auditor-de-replicas`.

## Fuentes

- **Kenneth R. French Data Library.** Archivos `Portfolios_Formed_on_{OP,NI,VAR,RESVAR,INV}_CSV.zip`, `F-F_Research_Data_Factors_CSV.zip` y `F-F_Research_Data_5_Factors_2x3_CSV.zip` (CRSP 202607), descargados el 2026-09-25. Las descripciones de construcción están en `Data_Library/det_port_form_{ni,op,var,resvar,inv}.html`. https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
- **FRED, serie `DEXMXUS`** (Mexican Pesos to One U.S. Dollar), descargada el 2026-09-25. https://fred.stlouisfed.org/series/DEXMXUS
- **Fechas de publicación, verificadas con la API de Crossref** el 2026-09-25:
  - Novy-Marx, R. (2013). "The other side of value: The gross profitability premium". *Journal of Financial Economics* 108(1), 1–28, abril de 2013. doi:10.1016/j.jfineco.2013.01.003
  - Fama, E. F. y French, K. R. (2015). "A five-factor asset pricing model". *Journal of Financial Economics* 116(1), 1–22, abril de 2015 (registro en Crossref del 29-oct-2014). doi:10.1016/j.jfineco.2014.10.010
  - Pontiff, J. y Woodgate, A. (2008). "Share Issuance and Cross-sectional Returns". *Journal of Finance* 63(2), 921–945, abril de 2008. doi:10.1111/j.1540-6261.2008.01335.x
  - Ang, A., Hodrick, R. J., Xing, Y. y Zhang, X. (2006). "The Cross-Section of Volatility and Expected Returns". *Journal of Finance* 61(1), 259–299, febrero de 2006 (en línea desde el 20-ene-2006). doi:10.1111/j.1540-6261.2006.00836.x
  - Cooper, M. J., Gulen, H. y Schill, M. J. (2008). "Asset Growth and the Cross-Section of Stock Returns". *Journal of Finance* 63(4), 1609–1651, agosto de 2008 (en línea desde el 19-jul-2008). doi:10.1111/j.1540-6261.2008.01370.x
- **GBM.**
  - *Guía de Servicios de Inversión* V1025, pág. 19: tabla de corretaje (0.25% hasta 1 millón de MXN) y "A las comisiones que cobre la Casa de Bolsa por sus servicios, se le aumentará el Impuesto al Valor Agregado". https://global.gbm.com/wp-content/uploads/2026/02/12141701/Guia-de-Servicios-GBM_V-1025.pdf
  - FAQ de comisiones. https://gbm.com/faqs/que-comisiones-cobran-al-invertir-en-gbm/
  - Ambas consultadas el 2026-09-25.
- **McLean, R. D. y Pontiff, J. (2016).** "Does Academic Research Destroy Stock Return Predictability?", *Journal of Finance*. Solo se cita como contexto; no se verificó en esta réplica.
