# V03. Pre-registro: anomalías de EUA en versión long-only y largo-corto

> Escrito el 2026-09-25 a las 05:24 UTC, **antes** de calcular cualquier rendimiento, media, t o intervalo con estos datos. Este archivo no se edita después de la primera corrida: su huella SHA-256 queda en `SHA256SUMS.txt`, y cualquier cambio posterior va a "Desviaciones del pre-registro" en `README.md`.
>
> Lo único que se miró antes de escribirlo fue la **estructura** de los archivos: secciones, nombres de columnas, rango de fechas, notas del preámbulo y, en NI, el NI promedio y el número de empresas por cartera, para saber cómo están armados los quintiles. No se calculó ningún rendimiento.

## 1. Preguntas y afirmaciones recibidas

1. Con los portafolios de Kenneth French para EUA, ¿el quintil "bueno" de cada anomalía le gana al mercado en versión **long-only**, que es lo único operable en GBM porque no hay cortos? ¿Y el diferencial **largo-corto** académico?
2. ¿Sobrevive después de la publicación de cada anomalía?
3. ¿Sobrevive medido en **MXN**?
4. Verificar las cifras recibidas: "rentables 4.5% anual desde 2000; recompras 5.3%; baja volatilidad 3.6% extra".

**Hipótesis previa (con signo).** Las cuatro anomalías tienen diferencial largo-corto positivo en la muestra completa. Espero que el exceso long-only sobre el mercado sea **menor** que el largo-corto, porque buena parte del premio académico suele venir de la pata corta, y que se debilite después de la publicación (McLean y Pontiff, 2016). No hay un mecanismo nuevo que probar. Se trata de medir cuánto de la cifra recibida es operable.

## 2. Datos (congelados en `datos/`, huellas en `SHA256SUMS.txt`)

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

## 3. Series (lista cerrada)

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

## 4. Ventanas

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

## 5. Método

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

## 6. Costos (sensibilidad; no entra al veredicto)

- **Comisión GBM:** 0.25% + IVA = **0.29% por lado**. Es un hecho: Guía de Servicios GBM V1025, pág. 19, "se le aumentará el Impuesto al Valor Agregado"; FAQ de GBM, escalón de 0.25% hasta 1 millón de MXN. Verificado el 2026-09-25.
- **Spread:** 0.05% por lado. Es un **supuesto**, no un hecho.
- **Qué no se sabe:** los portafolios de French no traen la rotación, así que **no se inventa**. Se reporta la **rotación de equilibrio** τ\* = (media × 12) / (2 × 0.34%), que es la rotación anual en una vía que se come toda la ventaja media. Como ilustración, se reporta también el exceso neto con τ = 100% anual, lo que resta 0.68 pp al año.
- Frente a un ETF del mercado con rotación ≈ 0, este costo es adicional.
- Tampoco se modelan el costo cambiario, los impuestos ni la imposibilidad práctica de comprar cientos de acciones con 20,000 MXN.

## 7. Criterio para las afirmaciones recibidas

Una afirmación se **reproduce** si alguna definición registrada en la sección 3, en la ventana 2000-2025 o 2000-ult, da media × 12 **o** diferencia de CAGR dentro de ±0.30 pp de la cifra. Se reporta cuál definición coincide. Las candidatas son:

- **"Rentables 4.5%":** RMW, OP-LS-VW, OP-LO-VW y OP-LS-EW.
- **"Recompras 5.3%":** NI-LS-VW, NI-LO-VW y NI-LS-EW.
- **"Baja volatilidad 3.6% extra":** VAR-LO-VW (la palabra "extra" sugiere que es sobre el mercado), VAR-LS-VW, VAR-LS-EW, RESVAR-LO-VW y RESVAR-LS-VW.

La calificación de cada afirmación queda así:

- **"confirmada":** se reproduce **y** la versión LO-VW tiene "apoyo" en 2000-2025 **y** en post.
- **"confirmada con matices":** se reproduce, pero solo como LS, o sin significancia en LO, en post o en MXN.
- **"no confirmada":** ninguna definición registrada la reproduce.

Buscar la coincidencia entre varias definiciones y ventanas es un **jardín de caminos que se bifurcan**. Solo sirve para identificar qué midió quien dio la cifra, no como prueba de la anomalía.

## 8. Número de pruebas

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

## 9. Conclusiones que se decidirán solo con estos criterios

Una ventaja se considera **operable-candidata** solo si su LO-VW tiene "apoyo" en post **y** en MXN. Aun así, **no** sería una recomendación, porque faltarían ETF concreto, costos reales, impuestos y el papel.
