# AC-02 — Auditoría ciega: factor de rentabilidad (RMW) de EUA

Estado: **ESPECIFICACIÓN PRE-REGISTRADA** (escrita el 2026-09-25, antes de descargar datos y antes de calcular nada).
Auditor: agente auditor ciego (sin acceso a `laboratorio/replicas/V01-momentum-y-rentabilidad/` ni a cifras previas del repo sobre momentum o RMW).

Esta sección no se modifica después de ver resultados. Cualquier cambio se agrega al final como **adenda fechada**.

## 1. Afirmación a auditar

> "RMW de EUA rinde ~4.5–4.8% anual desde 2000 y es significativo; no es significativo después de 2015."

Se evalúa por separado en **media ×12** (aritmética) y en **rendimiento anual compuesto**, en cada una de las tres fuentes.

## 2. Ventanas (inclusivas, meses calendario)

| Ventana | Inicio | Fin |
|---|---|---|
| W1 | 1963-07 | 1999-12 |
| W2 | 2000-01 | 2025-12 |
| W3 | 2015-01 | 2025-12 |
| W4 | 2016-01 | 2025-12 |

Si una fuente no cubre la ventana completa, se reporta la ventana efectiva (primer y último mes disponibles) y el n real; no se rellena nada.

## 3. Fuentes

- **Fuente A (oficial):** Kenneth French, `F-F_Research_Data_5_Factors_2x3` (CSV mensual), columna `RMW`, en % mensual.
- **Fuente B (reconstrucción):** Kenneth French, `6_Portfolios_ME_OP_2x3` (CSV mensual, *value-weighted*),
  `RMW_B = 1/2 (Small Robust + Big Robust) − 1/2 (Small Weak + Big Weak)`.
  Diferencia de construcción: la nota del encargo indica que el RMW oficial 2x3 "promedia también otras particiones". Hipótesis a verificar con la documentación de French (se cita textual en la sección de resultados): el componente que promedia varias particiones (B/M, OP, INV) es SMB; RMW se define con la partición tamaño × OP, pero el universo, los filtros de datos o los breakpoints usados para el factor pueden no coincidir exactamente con los del archivo `6_Portfolios_ME_OP_2x3`. No se asume el resultado: se compara mes a mes (correlación, diferencia media, desviación estándar de la diferencia, máximo |diferencia|, número de meses con |diferencia| > 0.01 pp y > 0.5 pp) y se reporta lo que salga.
- **Fuente C (independiente):**
  - C1: Hou-Xue-Zhang q-factors, factor de rentabilidad `R_ROE` (global-q.org, CSV mensual, en %).
  - C2: AQR "Quality Minus Junk: Factors, Monthly", columna `USA` (xlsx; retorno decimal, se convierte a %).
  - Si alguna no está accesible se dice explícitamente y se usa la siguiente.
  - Nota: R_ROE y QMJ **no** son el mismo constructo que RMW (ROE trimestral vs. rentabilidad operativa anual; QMJ combina rentabilidad, crecimiento, seguridad y pago). Se reportan como evidencia independiente del "premio de rentabilidad/calidad", no como réplica de RMW.
- Se reportan correlaciones mensuales entre A, B, C1 y C2 sobre los meses comunes de cada ventana.

## 4. Estadísticos por ventana y fuente

Sobre la serie mensual r_t (en %):

- `n`: número de meses.
- Media mensual (%).
- Desviación estándar muestral (divisor n−1).
- **t convencional IID** = media / (sd / √n).
- **t Newey-West** con L = 6 rezagos, kernel de Bartlett (w_j = 1 − j/(L+1)), varianza de largo plazo
  `S = γ0 + 2 Σ_{j=1..L} w_j γ_j`, con γ_j = (1/n) Σ (r_t − r̄)(r_{t−j} − r̄), multiplicada por la corrección de muestra pequeña n/(n−1).
  EE_NW = √(S · n/(n−1) / n). t_NW = media / EE_NW.
- **IC95 NW** = media ± 1.96 · EE_NW (en % mensual; también se reporta ×12).
- **Media ×12** (aritmética; etiqueta: "no es CAGR").
- **Rendimiento anual compuesto** = (Π(1 + r_t/100))^(12/n) − 1 (etiqueta: "compuesto de la serie largo-corto; no es el rendimiento de una cuenta").
- Peor mes y mejor mes (valor y fecha).

## 5. Regla de veredicto (por fuente y ventana)

- **"apoyo"**: límite inferior del IC95 NW > 0.
- **"contraria"**: límite superior del IC95 NW < 0.
- **"inconcluso"**: en otro caso.

## 6. Criterio para la afirmación compuesta

La afirmación se considera **sostenida en una fuente** sólo si en esa fuente:
1. W2 (2000–2025): media ×12 en [4.5, 4.8] % aproximadamente (se reporta el valor exacto; "~" se interpreta como ±0.5 pp alrededor del rango, es decir [4.0, 5.3] %) **y** veredicto "apoyo";
2. W3 y W4 (desde 2015 / 2016): veredicto "inconcluso" (no significativo).
Se evalúa también con el compuesto en lugar de la media ×12 para el punto 1.
Para C1/C2 el nivel no es comparable (otro constructo), así que para ellas sólo se evalúa el patrón de significancia (apoyo en W2, inconcluso en W3/W4); el nivel se reporta pero no se exige.

## 7. Datos congelados y reproducibilidad

- Cada archivo descargado se guarda sin modificar en `datos/`; `datos/SHA256SUMS.txt` en formato `sha256sum`.
- Se registra la versión/cabecera de cada archivo (p. ej. línea de copyright/fecha de CRSP en los CSV de French; fecha de actualización en AQR; año de versión en global-q).
- `auditoria.py`: Python 3.11, sólo biblioteca estándar, sin red; lee `datos/`, verifica SHA256, calcula y escribe `resultados.json`.
- Newey-West y t IID implementados desde cero en `auditoria.py` (no se importa `herramientas/estadistica.py`).

## 8. Conclusiones permitidas y NO permitidas (plantilla; se completa tras calcular)

Se completan en la sección de resultados, siguiendo estas reglas fijadas de antemano:
- Permitido: describir media, compuesto, t e IC por ventana y fuente tal como salen del código; decir si la afirmación se sostiene según el criterio de la sección 6.
- NO permitido: extrapolar a rendimientos futuros; hablar de rendimiento de una cuenta invertible (sin costos, sin préstamo de valores, largo-corto teórico); afirmar "desaparición" del factor a partir de un "inconcluso" (ausencia de significancia ≠ evidencia de cero); tratar R_ROE/QMJ como réplica de RMW.

---

## Bitácora

- 2026-09-25 05:25 UTC: especificación escrita (secciones 1–8). Antes de descargar cualquier dato, se reescribió el párrafo de la Fuente B para que dejara de dar por hecho cómo difiere su construcción (quedó como hipótesis a verificar). No se cambió ningún estadístico, ventana ni regla de veredicto.
- 05:25–05:28 UTC: descarga y congelamiento (`datos/SHA256SUMS.txt`, 8 archivos).
- 05:29 UTC: primera y única corrida de cálculo (`python3 auditoria.py`). No hubo cambios a la especificación después de ver resultados → **sin adendas**.
- Verificaciones internas del código (no alteran resultados): con L=0, el EE de Newey-West coincide con sd/√n (t NW = t IID); el EE NW con L=6 coincide con una doble suma explícita con pesos de Bartlett (0.163530 vs 0.163530 en A-W2); el compuesto coincide con el cálculo por logaritmos (4.3485% en A-W2).

## Fuentes descargadas (datos congelados)

| Archivo en `datos/` | Origen | Versión / cabecera | Cobertura mensual |
|---|---|---|---|
| `F-F_Research_Data_5_Factors_2x3_CSV.zip` | mba.tuck.dartmouth.edu/.../ftp/ | "This file was created using the 202607 CRSP database." (**CRSP 202607**); fecha interna del zip 2026-09-02 | 1963-07 a 2026-07 |
| `6_Portfolios_ME_OP_2x3_CSV.zip` | ídem | **CRSP 202607**; fecha interna del zip 2026-09-02; sección "Average Value Weighted Returns -- Monthly" | 1963-07 a 2026-07 |
| `q5_factors_monthly_2025.csv` | global-q.org/uploads/.../ | página: "Latest Release, 7/30/2026", muestra 1967-2025 | 1967-01 a 2025-12 |
| `Quality-Minus-Junk-Factors-Monthly.xlsx` | aqr.com/-/media/AQR/Documents/Insights/Data-Sets/ | sin sello de versión en el archivo ("AQR reconstructs the full history each time the portfolios are updated"); identificada por SHA256 y por su último mes | USA: 1957-07 a 2026-07 |
| `french_f-f_5_factors_2x3.html`, `french_six_portfolios_me_op.html`, `globalq_factors_page.html`, `aqr_qmj_page.html` | páginas de documentación | copia para citar construcción y versión | — |

Las cuatro fuentes estuvieron accesibles; no hizo falta usar sustitutos. Los meses 2026-01 a 2026-07 que traen A, B y C2 quedan fuera de las ventanas pre-registradas y no se usaron. En la ventana W1, C1 (R_ROE) sólo cubre desde 1967-01 (n = 396 en vez de 438). Ninguna serie tiene huecos dentro de su ventana efectiva.

## Diferencia de construcción A vs B (documentación de French, textual)

- Página del factor: *"RMW (Robust Minus Weak) is the average return on the two robust operating profitability portfolios minus the average return on the two weak operating profitability portfolios, RMW = 1/2 (Small Robust + Big Robust) - 1/2 (Small Weak + Big Weak)."* Lo que promedia tres particiones (B/M, OP, INV) es **SMB**: *"SMB = 1/3 ( SMB (B/M) + SMB (OP) + SMB (INV) )"*. Por eso la hipótesis del encargo ("el RMW oficial 2x3 promedia también otras particiones") **no aplica a RMW**; sí aplica a SMB.
- Universo del factor: *"...stocks for which we have market equity data for December of t-1 and June of t, (positive) book equity data for t-1 (for SMB, HML, and RMW), non-missing revenues and at least one of the following: cost of goods sold, selling, general and administrative expenses, or interest expense for t-1 (for SMB and RMW)..."*.
- Universo de los 6 portafolios ME/OP: *"...stocks for which we have market equity data for June of t, (positive) book equity data for t-1, non-missing revenues data for t-1, and non-missing data for at least one of the following..."*. En la documentación, la única diferencia visible es que el factor exige también el ME de diciembre de t−1. Cortes: mediana NYSE de tamaño; percentiles 30 y 70 NYSE de OP.
- Otra diferencia: RMW oficial viene con 2 decimales; los portafolios, con 4.

**Resultado de la comparación mes a mes (B − A):**

| Ventana | n | r(A,B) | Dif. media B−A %/mes | DE dif. | Máx. abs. dif. (mes) | Meses con abs. dif. > 0.01 | > 0.5 |
|---|---|---|---|---|---|---|---|
| W1 (1963-07 a 1999-12) | 438 | 1.00000 | 0.0000 | 0.0029 | 0.0050 (1983-10) | 0 | 0 |
| W2 (2000-01 a 2025-12) | 312 | 1.00000 | 0.0002 | 0.0029 | 0.0050 (2001-02) | 0 | 0 |
| W3 (2015-01 a 2025-12) | 132 | 1.00000 | -0.0002 | 0.0030 | 0.0050 (2015-03) | 0 | 0 |
| W4 (2016-01 a 2025-12) | 120 | 1.00000 | -0.0001 | 0.0029 | 0.0049 (2024-05) | 0 | 0 |
| Muestra común completa (1963-07 a 2026-07) | 757 | 1.00000 | 0.0001 | 0.0029 | 0.0050 (2001-02) | 0 | 0 |

En la versión CRSP 202607, la reconstrucción B reproduce el RMW oficial **hasta el redondeo** (máx. 0.005 pp = medio centavo del redondeo a 2 decimales; cero meses con diferencia > 0.01 pp). La diferencia de universo que describe la documentación no produce diferencias detectables. **Consecuencia:** B confirma que la aritmética del factor está bien, pero **no es evidencia independiente**, porque sale de los mismos portafolios.

## Resultados por fuente y ventana

Unidades: % mensual salvo "×12" y "compuesto". IC95 NW = media ± 1.96·EE_NW (L=6, Bartlett, n/(n−1)).
*Media ×12: media aritmética ×12; **no es CAGR**.* *Compuesto: compuesto de la serie largo-corto; **no es el rendimiento de una cuenta**.*

| Fuente | Ventana | Efectiva | n | Media %/mes | DE % | t IID | t NW(6) | IC95 NW %/mes | IC95 NW ×12 % | Media ×12 % | Compuesto anual % | Peor mes | Mejor mes | Veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A · FF5 RMW | W1 | 1963-07 a 1999-12 | 438 | 0.173 | 1.600 | 2.26 | 1.90 | [-0.005, 0.351] | [-0.06, 4.21] | 2.07 | 1.93 | -8.07 (1999-12) | 5.01 (1974-05) | inconcluso |
| A · FF5 RMW | W2 | 2000-01 a 2025-12 | 312 | 0.397 | 2.872 | 2.44 | 2.43 | [0.076, 0.717] | [0.92, 8.61] | 4.76 | 4.35 | -18.93 (2000-02) | 13.04 (2000-11) | **apoyo** |
| A · FF5 RMW | W3 | 2015-01 a 2025-12 | 132 | 0.274 | 2.129 | 1.48 | 1.59 | [-0.064, 0.611] | [-0.76, 7.33] | 3.29 | 3.06 | -5.25 (2025-10) | 7.19 (2021-11) | inconcluso |
| A · FF5 RMW | W4 | 2016-01 a 2025-12 | 120 | 0.296 | 2.197 | 1.48 | 1.57 | [-0.074, 0.666] | [-0.89, 8.00] | 3.55 | 3.32 | -5.25 (2025-10) | 7.19 (2021-11) | inconcluso |
| B · reconstr. 6P ME/OP | W1 | 1963-07 a 1999-12 | 438 | 0.173 | 1.600 | 2.26 | 1.90 | [-0.005, 0.351] | [-0.06, 4.21] | 2.07 | 1.94 | -8.07 (1999-12) | 5.01 (1974-05) | inconcluso |
| B · reconstr. 6P ME/OP | W2 | 2000-01 a 2025-12 | 312 | 0.397 | 2.872 | 2.44 | 2.43 | [0.076, 0.717] | [0.92, 8.61] | 4.76 | 4.35 | -18.93 (2000-02) | 13.04 (2000-11) | **apoyo** |
| B · reconstr. 6P ME/OP | W3 | 2015-01 a 2025-12 | 132 | 0.274 | 2.129 | 1.48 | 1.59 | [-0.064, 0.611] | [-0.77, 7.33] | 3.28 | 3.06 | -5.25 (2025-10) | 7.19 (2021-11) | inconcluso |
| B · reconstr. 6P ME/OP | W4 | 2016-01 a 2025-12 | 120 | 0.296 | 2.197 | 1.48 | 1.57 | [-0.074, 0.666] | [-0.89, 7.99] | 3.55 | 3.32 | -5.25 (2025-10) | 7.19 (2021-11) | inconcluso |
| C1 · HXZ R_ROE | W1 | 1967-01 a 1999-12 | 396 | 0.664 | 2.144 | 6.16 | 6.68 | [0.469, 0.859] | [5.63, 10.31] | 7.97 | 7.97 | -11.59 (1975-01) | 9.08 (1980-11) | **apoyo** |
| C1 · HXZ R_ROE | W2 | 2000-01 a 2025-12 | 312 | 0.336 | 3.094 | 1.92 | 1.84 | [-0.021, 0.693] | [-0.26, 8.31] | 4.03 | 3.50 | -14.33 (2020-11) | 10.37 (2000-11) | inconcluso |
| C1 · HXZ R_ROE | W3 | 2015-01 a 2025-12 | 132 | 0.362 | 2.885 | 1.44 | 1.29 | [-0.188, 0.911] | [-2.26, 10.94] | 4.34 | 3.90 | -14.33 (2020-11) | 8.39 (2021-11) | inconcluso |
| C1 · HXZ R_ROE | W4 | 2016-01 a 2025-12 | 120 | 0.320 | 2.943 | 1.19 | 1.06 | [-0.273, 0.913] | [-3.27, 10.96] | 3.84 | 3.37 | -14.33 (2020-11) | 8.39 (2021-11) | inconcluso |
| C2 · AQR QMJ USA | W1 | 1963-07 a 1999-12 | 438 | 0.336 | 1.759 | 3.99 | 3.61 | [0.154, 0.518] | [1.84, 6.21] | 4.03 | 3.91 | -5.77 (1975-01) | 7.33 (1998-08) | **apoyo** |
| C2 · AQR QMJ USA | W2 | 2000-01 a 2025-12 | 312 | 0.351 | 2.974 | 2.08 | 1.81 | [-0.029, 0.731] | [-0.35, 8.77] | 4.21 | 3.74 | -8.90 (2002-11) | 12.08 (2000-11) | inconcluso |
| C2 · AQR QMJ USA | W3 | 2015-01 a 2025-12 | 132 | 0.249 | 2.870 | 1.00 | 0.95 | [-0.266, 0.765] | [-3.20, 9.18] | 2.99 | 2.53 | -8.77 (2020-11) | 7.61 (2016-01) | inconcluso |
| C2 · AQR QMJ USA | W4 | 2016-01 a 2025-12 | 120 | 0.170 | 2.951 | 0.63 | 0.63 | [-0.357, 0.696] | [-4.29, 8.36] | 2.03 | 1.52 | -8.77 (2020-11) | 7.61 (2016-01) | inconcluso |

### Correlaciones mensuales (meses comunes de cada par)

| Par | W1 (n) | W2 (n=312) | W3 (n=132) | W4 (n=120) |
|---|---|---|---|---|
| A ~ B | 1.000 (438) | 1.000 | 1.000 | 1.000 |
| A ~ C1 (R_ROE) | 0.571 (396, desde 1967-01) | 0.721 | 0.660 | 0.679 |
| A ~ C2 (QMJ USA) | 0.603 (438) | 0.726 | 0.666 | 0.685 |
| C1 ~ C2 | 0.522 (396) | 0.781 | 0.747 | 0.749 |

(B ~ C1 y B ~ C2 son iguales a A ~ C1 y A ~ C2 a tres decimales.)

## Discrepancias entre fuentes y causas probables

1. **A vs B: sin discrepancia material.** Coinciden hasta el redondeo (ver arriba). La única diferencia visible en la tabla es la media ×12 de W3 (3.29 vs 3.28) y el compuesto de W1 (1.93 vs 1.94), y ambas vienen del redondeo a 2 decimales de A.
2. **Significancia en 2000–2025 (W2).** RMW (A/B): t NW = 2.43, límite inferior del IC > 0 → "apoyo". R_ROE (C1): t NW = 1.84, IC [-0.021, 0.693] → "inconcluso". QMJ USA (C2): t NW = 1.81, IC [-0.029, 0.731] → "inconcluso". Las tres medias puntuales son parecidas (0.34–0.40 %/mes; ×12 entre 4.03 y 4.76), pero C1 y C2 tienen mayor desviación estándar (3.09 y 2.97 contra 2.87) y medias algo menores, así que en esas dos el IC cruza cero. En C2 el veredicto cambia según el error estándar: con t IID (2.08) sería significativo y con NW (1.81) no. La regla pre-registrada es NW.
   Causas probables, no verificadas en esta auditoría: (a) constructos distintos. R_ROE ordena por ROE trimestral con reordenamiento mensual dentro de un triple orden tamaño × I/A × ROE (18 portafolios 2×3×3, según global-q.org y Hou-Xue-Zhang 2015; el documento técnico no se descargó). QMJ es un puntaje compuesto de calidad (rentabilidad, crecimiento, seguridad y pago, según Asness-Frazzini-Pedersen; ese detalle no se extrajo del archivo), no sólo rentabilidad. RMW usa OP anual reordenado cada junio. (b) Universos y ordenamientos distintos. La hoja de AQR dice: *"We do a dependent sort (first sort by size and then by metric), whereas French does an independent sort"* y *"no guarantee that the universes will be exactly the same"*. (c) Fuentes contables distintas. AQR usa Compustat/XpressFeed Global para precios domésticos desde 1998-01, según su hoja "Data Sources".
3. **1963–1999 (W1): el patrón se invierte.** RMW da 2.07% ×12 con t NW = 1.90 ("inconcluso"; con t IID = 2.26 sería significativo). R_ROE da 7.97% ×12 con t NW = 6.68, y QMJ da 4.03% ×12 con t NW = 3.61; ambas "apoyo". Causa probable: la misma diferencia de constructo. El ROE trimestral usa información contable más reciente que la OP anual con rezago de 6 a 18 meses. Queda como hipótesis; no se verificó.
4. **Nivel ×12 frente a compuesto.** En todas las fuentes el compuesto es menor que la media ×12 (A-W2: 4.35 contra 4.76) por la volatilidad (≈ σ²/2). En A-W2 el compuesto (4.35%) **queda fuera del rango literal 4.5–4.8%**, aunque dentro de la tolerancia pre-registrada [4.0, 5.3].
5. **Versión de los datos.** French y AQR reconstruyen el histórico en cada actualización, así que estas cifras valen para la versión congelada (SHA256 en `datos/SHA256SUMS.txt`). Con otra versión pueden cambiar los decimales.

## Evaluación de la afirmación (criterio de la sección 6, sin cambios)

Afirmación: *"~4.5–4.8% anual desde 2000 y significativo; no significativo después de 2015."*

| Fuente | W2 veredicto | W2 media ×12 | W2 compuesto | W3 / W4 veredicto | ¿Se sostiene con media ×12? | ¿Se sostiene con compuesto? |
|---|---|---|---|---|---|---|
| A · FF5 RMW | apoyo (t NW 2.43) | 4.76 (dentro del rango literal 4.5–4.8) | 4.35 (fuera del literal; dentro de la tolerancia 4.0–5.3) | inconcluso / inconcluso | **Sí** | **Sí según el criterio pre-registrado**; no si se exige el rango literal 4.5–4.8 |
| B · reconstrucción | apoyo (t NW 2.43) | 4.76 | 4.35 | inconcluso / inconcluso | Sí (no es independiente de A) | Sí según el criterio pre-registrado (misma salvedad que A) |
| C1 · HXZ R_ROE | **inconcluso** (t NW 1.84) | 4.03 (nivel no exigido) | 3.50 (nivel no exigido) | inconcluso / inconcluso | **No**: falla "significativo desde 2000" | **No** |
| C2 · AQR QMJ USA | **inconcluso** (t NW 1.81) | 4.21 (nivel no exigido) | 3.74 (nivel no exigido) | inconcluso / inconcluso | **No**: falla "significativo desde 2000" | **No** |

**Veredicto de la auditoría:** la afirmación **no se sostiene en las tres fuentes**.
- Se sostiene en la fuente oficial A. En media ×12 cae dentro del rango literal (4.76%). En compuesto (4.35%) sólo pasa con la tolerancia pre-registrada, no con el rango literal. B lo replica exactamente, pero no aporta independencia.
- En las dos fuentes independientes (C1 R_ROE y C2 QMJ USA), 2000–2025 da "inconcluso". El premio de rentabilidad/calidad desde 2000 **no es significativo** con NW(6) en esas medidas.
- La parte "no significativo después de 2015" coincide en las tres fuentes: todas dan "inconcluso" en W3 y W4.

## Conclusiones permitidas

- Con datos de French CRSP 202607, el RMW 2x3 de EUA tuvo en 2000-01 a 2025-12 una media de 0.397 %/mes (4.76% ×12; no es CAGR). Su compuesto fue 4.35% anual (compuesto de la serie largo-corto; no es el rendimiento de una cuenta), con t NW(6) = 2.43 e IC95 NW mensual [0.076, 0.717]. Veredicto: "apoyo".
- En 2015–2025 y 2016–2025, ese RMW no es estadísticamente distinto de cero con NW(6): t = 1.59 y 1.57.
- La media de 2000–2025 (0.397) cae dentro del IC95 de 2015–2025 ([-0.064, 0.611]). Los datos no permiten decir que el premio posterior a 2015 sea menor que el de 2000–2025; sólo que la muestra corta no alcanza para distinguirlo de cero.
- En 1963–1999, el RMW 2x3 no es significativo con NW(6) (t = 1.90); con t IID sí lo sería (2.26).
- Dos medidas independientes del premio de rentabilidad/calidad (R_ROE de HXZ y QMJ USA de AQR) tienen correlación de 0.72–0.73 con RMW en 2000–2025. Sus medias ×12 son parecidas (4.03 y 4.21), pero no son significativas en esa ventana.
- La reconstrucción con los 6 portafolios ME/OP reproduce el RMW oficial hasta el redondeo.

## Conclusiones NO permitidas

- Decir que "el factor de rentabilidad es significativo desde 2000" en general. Sólo lo es en la medida RMW de French; no en R_ROE ni en QMJ USA.
- Decir que "desapareció" o que "vale cero" después de 2015. "Inconcluso" es ausencia de significancia, no evidencia de cero, y las estimaciones puntuales de 2015–2025 siguen siendo positivas en las tres fuentes.
- Presentar 4.76% (media ×12) como rendimiento anual compuesto o CAGR. El compuesto es 4.35%.
- Presentar cualquiera de estas cifras como rendimiento alcanzable en una cuenta. Son carteras largo-corto teóricas, sin costos de transacción, préstamo de valores, impuestos ni restricciones de apalancamiento.
- Tratar R_ROE o QMJ como réplicas de RMW, o tratar la reconstrucción B como confirmación independiente de A.
- Extrapolar estas medias a rendimientos futuros.
- Citar estas cifras sin la versión de los datos (CRSP 202607; HXZ release 2026-07-30; AQR con el SHA256 de `datos/`).

## Reproducir

```
cd laboratorio/auditorias/AC-02-rentabilidad-eua
python3 auditoria.py    # sin red; verifica SHA256 y reescribe resultados.json
```
