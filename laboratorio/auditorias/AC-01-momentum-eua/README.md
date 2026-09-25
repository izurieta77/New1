# AC-01 — Auditoría ciega: factor momentum de EUA

- **Tipo:** auditoría ciega (el auditor no leyó la réplica V01 ni cifras previas de momentum/RMW del repo).
- **Especificación escrita:** 2026-09-25, **antes** de descargar datos y antes de calcular.
- **Estado:** ESPECIFICACIÓN PRE-REGISTRADA (los resultados se añaden abajo en secciones posteriores; cualquier cambio a esta especificación va como adenda fechada al final).

## 1. Pregunta

¿El factor momentum de EUA (largo ganadores / corto perdedores de los 12-2 meses previos) tiene
un rendimiento medio mensual distinto de cero en cada una de las ventanas definidas, y
coinciden las fuentes independientes?

## 2. Ventanas (inclusivas, meses calendario)

| Ventana | Inicio | Fin |
|---|---|---|
| W1 | 1984-01 | 2006-09 |
| W2 | 2006-10 | 2025-12 |
| W3 | 2006-10 | 2015-12 |
| W4 | 2016-01 | 2025-12 |

Si alguna fuente no cubre una ventana completa, se reporta con el `n` realmente disponible y se
marca como cobertura parcial; no se sustituye por otro periodo.

## 3. Fuentes

- **Fuente A (principal):** Kenneth R. French Data Library, archivo `F-F_Momentum_Factor`
  (CSV dentro de zip), sección mensual, columna `Mom`. Unidades: % mensual.
- **Fuente B (reconstrucción):** French, `6_Portfolios_ME_Prior_12_2` (CSV dentro de zip),
  sección *Average Value Weighted Returns -- Monthly*.
  `UMD_B = 1/2 (SMALL HiPRIOR + BIG HiPRIOR) - 1/2 (SMALL LoPRIOR + BIG LoPRIOR)`.
  Se compara mes a mes con A en el periodo común y en cada ventana: correlación de Pearson,
  diferencia media (B - A), máxima diferencia absoluta |B - A| y su mes.
  Además se reportan los mismos estadísticos de la sección 4 para B.
- **Fuente C (independiente, construcción distinta):** AQR Capital Management, dataset
  *Betting Against Beta: Equity Factors, Monthly* (xlsx), hoja `UMD`, columna `USA`.
  AQR expresa rendimientos en fracción decimal: se multiplican por 100 para ponerlos en % mensual.
  Se reportan los estadísticos de la sección 4 en las mismas ventanas y la correlación con A
  en el periodo común y por ventana.
  Si AQR no es accesible se dice explícitamente y se intenta la siguiente fuente: UMD de
  *Quality Minus Junk: Factors, Monthly* (AQR); si tampoco, factor R_MOM/equivalente de
  q-factors (global-q.org) si existe, declarando la diferencia de construcción.

## 4. Estadísticos por fuente y ventana

Sea `r_t` el rendimiento mensual en % y `n` el número de meses con dato en la ventana.

1. `n`
2. media mensual (%) = promedio aritmético de `r_t`
3. desviación estándar muestral (divisor n-1), % mensual
4. **t convencional IID** = media / (sd / sqrt(n))
5. **t Newey-West**, 6 rezagos, kernel de Bartlett `w_j = 1 - j/(L+1)`, L = 6:
   `S = gamma_0 + 2 * sum_{j=1..6} w_j * gamma_j`, con
   `gamma_j = (1/n) * sum_{t=j+1..n} (r_t - media)(r_{t-j} - media)`;
   se aplica corrección de muestra pequeña `S * n/(n-1)`;
   `EE_NW = sqrt(S * n/(n-1) / n)`; `t_NW = media / EE_NW`.
6. **IC95 NW** = media ± 1.96 * EE_NW (% mensual)
7. **media x12** (% anual aritmético) — etiqueta obligatoria: "no es CAGR"
8. **rendimiento anual compuesto** = `(prod(1 + r_t/100))^(12/n) - 1` — etiqueta obligatoria:
   "compuesto de la serie largo-corto; no es el rendimiento de una cuenta"
9. peor mes y mejor mes (valor y fecha)

## 5. Regla de veredicto (por fuente y ventana)

- **"apoyo"** si el límite inferior del IC95 NW > 0
- **"contraria"** si el límite superior del IC95 NW < 0
- **"inconcluso"** en otro caso

## 6. Datos congelados y reproducibilidad

- Cada archivo descargado se guarda sin modificar en `datos/`.
- `datos/SHA256SUMS.txt` en formato `sha256sum` (verificable con `sha256sum -c`).
- Se registra la versión/cabecera de cada archivo (p. ej. la línea "CRSP AAAAMM" de French,
  fecha de actualización de AQR).
- `auditoria.py`: Python 3.11, solo biblioteca estándar, sin red; lee `datos/`, verifica
  hashes, calcula y escribe `resultados.json`. Lectura de xlsx con `zipfile` + `xml.etree`.
- No se usan herramientas del repo (`herramientas/estadistica.py` no se importa).

## 7. Conclusiones permitidas / no permitidas (definidas antes de ver resultados)

- Permitido: afirmar el veredicto por ventana según la regla de la sección 5, para cada fuente;
  describir concordancia/discrepancia entre fuentes con las métricas calculadas.
- No permitido: extrapolar a rendimientos implementables (costos, impuestos, préstamo de
  acciones, capacidad no incluidos); llamar "CAGR" a la media x12; presentar el compuesto de la
  serie largo-corto como rendimiento de una cuenta; inferir causalidad sobre por qué cambió
  el rendimiento entre ventanas; usar las ventanas post-hoc para elegir otras.

---

# RESULTADOS (añadidos el 2026-09-25 tras ejecutar `python3 auditoria.py`)

Todas las cifras de esta sección son copia literal de la salida de `auditoria.py`
(también en `resultados.json`, con 6 decimales). Unidades: % mensual salvo indicación.

## 8. Fuentes efectivamente usadas y versión congelada

| Fuente | Archivo en `datos/` | Versión / cabecera | Rango disponible | SHA256 |
|---|---|---|---|---|
| A — French `Mom` | `F-F_Momentum_Factor_CSV.zip` | "created using the 202607 CRSP database" → **CRSP 202607**; HTTP Last-Modified 2026-09-04 | 1927-01 a 2026-07 (n=1195) | `7ee14e89…afe065` |
| B — French 6 carteras ME×Prior(12-2), VW | `6_Portfolios_ME_Prior_12_2_CSV.zip` | "created by using the 202607 CRSP database" → **CRSP 202607**; HTTP Last-Modified 2026-09-04 | 1927-01 a 2026-07 (n=1195) | `de721381…a90110` |
| C — AQR UMD `USA` | `Betting-Against-Beta-Equity-Factors-Monthly.xlsx` (hoja `UMD`) | último dato 2026-07; miembros del xlsx fechados 2026-09-17; HTTP Last-Modified 2026-09-17 | 1927-01 a 2026-07 (n=1195) | `b98d9ce6…164514` |

- Hashes completos en `datos/SHA256SUMS.txt`; URLs y cabeceras HTTP en `datos/PROCEDENCIA.txt`.
  `auditoria.py` aborta si algún hash no coincide.
- AQR fue accesible (descarga directa del .xlsx), así que **no** se usaron las fuentes de respaldo
  (QMJ de AQR, q-factors).
- Las cuatro ventanas tienen cobertura completa en las tres fuentes (n = 273, 231, 111, 120).

## 9. Estadísticos por fuente y ventana

"Media x12" = media aritmética mensual × 12, **no es CAGR**.
"Compuesto anual" = (∏(1+r_t))^(12/n) − 1: **compuesto de la serie largo-corto; no es el rendimiento de una cuenta**.

| Fuente | Ventana | n | Media %/mes | DE % | t IID | t NW(6) | IC95 NW % | Media x12 % (no es CAGR) | Compuesto anual % (serie L-C; no es cuenta) | Peor mes | Mejor mes | Veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A French Mom | W1 1984-01..2006-09 | 273 | 0.798 | 4.345 | 3.04 | 3.37 | [0.335, 1.262] | 9.58 | 8.76 | -25.36 (2001-01) | 18.05 (2000-02) | **apoyo** |
| A French Mom | W2 2006-10..2025-12 | 231 | 0.088 | 4.501 | 0.30 | 0.26 | [-0.566, 0.742] | 1.06 | -0.26 | -34.36 (2009-04) | 12.73 (2008-06) | inconcluso |
| A French Mom | W3 2006-10..2015-12 | 111 | 0.152 | 5.135 | 0.31 | 0.25 | [-1.051, 1.355] | 1.82 | 0.05 | -34.36 (2009-04) | 12.73 (2008-06) | inconcluso |
| A French Mom | W4 2016-01..2025-12 | 120 | 0.029 | 3.844 | 0.08 | 0.09 | [-0.578, 0.635] | 0.34 | -0.55 | -16.21 (2023-01) | 8.20 (2020-03) | inconcluso |
| B reconstrucción 6P VW | W1 1984-01..2006-09 | 273 | 0.798 | 4.345 | 3.03 | 3.37 | [0.334, 1.262] | 9.58 | 8.76 | -25.36 (2001-01) | 18.05 (2000-02) | **apoyo** |
| B reconstrucción 6P VW | W2 2006-10..2025-12 | 231 | 0.088 | 4.501 | 0.30 | 0.26 | [-0.566, 0.743] | 1.06 | -0.26 | -34.37 (2009-04) | 12.72 (2008-06) | inconcluso |
| B reconstrucción 6P VW | W3 2006-10..2015-12 | 111 | 0.152 | 5.135 | 0.31 | 0.25 | [-1.051, 1.355] | 1.83 | 0.05 | -34.37 (2009-04) | 12.72 (2008-06) | inconcluso |
| B reconstrucción 6P VW | W4 2016-01..2025-12 | 120 | 0.029 | 3.845 | 0.08 | 0.10 | [-0.577, 0.636] | 0.35 | -0.55 | -16.21 (2023-01) | 8.20 (2020-03) | inconcluso |
| C AQR UMD USA | W1 1984-01..2006-09 | 273 | 0.851 | 4.136 | 3.40 | 3.76 | [0.407, 1.295] | 10.21 | 9.56 | -25.46 (2001-01) | 17.01 (2000-02) | **apoyo** |
| C AQR UMD USA | W2 2006-10..2025-12 | 231 | 0.140 | 4.568 | 0.46 | 0.41 | [-0.525, 0.804] | 1.67 | 0.31 | -34.62 (2009-04) | 11.11 (2008-06) | inconcluso |
| C AQR UMD USA | W3 2006-10..2015-12 | 111 | 0.234 | 5.215 | 0.47 | 0.38 | [-0.985, 1.452] | 2.80 | 0.97 | -34.62 (2009-04) | 11.11 (2008-06) | inconcluso |
| C AQR UMD USA | W4 2016-01..2025-12 | 120 | 0.052 | 3.896 | 0.15 | 0.17 | [-0.570, 0.675] | 0.63 | -0.30 | -16.77 (2020-11) | 8.48 (2019-05) | inconcluso |

## 10. Comparaciones mes a mes contra A (dif = otra − A, en puntos porcentuales)

| Comparación | Tramo | Periodo | n | Correlación | Dif. media pp | Máx. \|dif\| pp (mes) | Meses con \|dif\| > 0.015 |
|---|---|---|---|---|---|---|---|
| B vs A | total común | 1927-01 a 2026-07 | 1195 | 1.0000 | -0.0000 | 0.0100 (1933-09) | 0 |
| B vs A | W1 | 1984-01 a 2006-09 | 273 | 1.0000 | -0.0003 | 0.0100 (1998-08) | 0 |
| B vs A | W2 | 2006-10 a 2025-12 | 231 | 1.0000 | 0.0005 | 0.0100 (2008-02) | 0 |
| B vs A | W3 | 2006-10 a 2015-12 | 111 | 1.0000 | 0.0002 | 0.0100 (2008-02) | 0 |
| B vs A | W4 | 2016-01 a 2025-12 | 120 | 1.0000 | 0.0007 | 0.0100 (2018-01) | 0 |
| C vs A | total común | 1927-01 a 2026-07 | 1195 | 0.9861 | 0.0438 | 4.8062 (2021-01) | 1170 |
| C vs A | W1 | 1984-01 a 2006-09 | 273 | 0.9914 | 0.0526 | 2.5408 (1999-12) | 269 |
| C vs A | W2 | 2006-10 a 2025-12 | 231 | 0.9801 | 0.0516 | 4.8062 (2021-01) | 229 |
| C vs A | W3 | 2006-10 a 2015-12 | 111 | 0.9893 | 0.0818 | 2.0618 (2008-03) | 111 |
| C vs A | W4 | 2016-01 a 2025-12 | 120 | 0.9649 | 0.0237 | 4.8062 (2021-01) | 118 |

(0.015 pp es la cota máxima de |B − A| explicable solo por redondeo a 2 decimales: ver adenda.
Para C vs A esa columna no tiene significado de redondeo; solo indica que C casi nunca coincide al centésimo.)

Meses con mayor |C − A| en W2 (salida de una comprobación auxiliar con el mismo código de lectura):
2021-01 (A 4.34, C −0.47), 2020-11 (A −12.60, C −16.77), 2020-04 (A −5.61, C −8.74),
2025-09 (A 4.62, C 2.38), 2008-03 (A 4.25, C 2.19).

## 11. Discrepancias entre fuentes y causas probables

1. **A vs B (misma base CRSP 202607):** B reproduce A dentro del redondeo. Correlación 1.0000
   (a 4 decimales), máx. |B − A| = 0.0100 pp, ningún mes supera la cota de redondeo de 0.015 pp;
   las diferencias en estadísticos aparecen solo en el 3.er decimal (p. ej. IC95 W1 0.334 vs 0.335;
   peor mes 2009-04 −34.37 vs −34.36). **Causa:** los archivos publican rendimientos redondeados a
   2 decimales; A se calcula con carteras sin redondear. No hay discrepancia de construcción.
2. **A vs C (AQR, construcción distinta):** correlación alta pero no perfecta (0.9649 a 0.9914 por
   ventana; 0.9861 en todo el periodo común). La media de C es mayor que la de A en las cuatro
   ventanas (+0.024 a +0.082 pp/mes). Las diferencias mensuales llegan a 4.81 pp (2021-01) y las
   mayores de W4 se concentran en 2020-04, 2020-11 y 2021-01, lo que explica la correlación más baja
   de W4. **Causas probables, según la documentación incluida en el propio xlsx de AQR** (hoja
   "Sources and Definitions", recuadro "Differences between AQR & Fama-French Factors", y hoja
   "Data Sources"):
   - AQR hace un ordenamiento **dependiente** (primero tamaño, luego momentum); French uno **independiente**.
   - **Universo/fuentes de datos:** AQR usa precios de EUA de CRSP hasta 1967-06, CRSP/Compustat
     combinados 1967-07 a 1997-12 y **Compustat/XpressFeed Global desde 1998-01**; French usa CRSP.
     AQR declara que filtra para acercarse al universo de French "sin garantía" de igualdad.
   - **Refrescos históricos:** ambos reconstruyen la historia en cada actualización; las versiones
     comparadas son CRSP 202607 (French) y la versión AQR con datos hasta 2026-07.
   - AQR declara que los cortes (percentiles NYSE 30/70 y mediana NYSE de tamaño) y la tasa libre
     de riesgo **no** son diferenciadores.
   - No verificado: no se puede atribuir la diferencia de un mes concreto (p. ej. 2021-01) a una de
     estas causas sin datos por acción; queda como hipótesis.
3. **Concordancia de veredictos:** las tres fuentes dan el **mismo veredicto en las cuatro
   ventanas** (W1 apoyo; W2, W3, W4 inconcluso). Ninguna fuente da "contraria" en ninguna ventana.
4. **Media aritmética vs compuesto:** en W2 y W4 la media mensual es positiva en las tres fuentes,
   pero el compuesto anual de A y B es negativo (W2 −0.26 %, W4 −0.55 %) y el de C es −0.30 % en W4.
   Es la diferencia matemática esperable entre media aritmética y geométrica de una serie con
   DE mensual de ~4-5 % y media cercana a cero; no es una discrepancia entre fuentes.

## 12. Conclusiones

**Permitidas (se desprenden directamente de la regla pre-registrada):**
- 1984-01 a 2006-09: el factor momentum de EUA tuvo media mensual positiva con IC95 NW que excluye
  el cero, en las tres fuentes (A 0.798 %/mes, IC95 [0.335, 1.262], t NW 3.37; C 0.851 %/mes,
  IC95 [0.407, 1.295], t NW 3.76). Veredicto: **apoyo**.
- 2006-10 a 2025-12, 2006-10 a 2015-12 y 2016-01 a 2025-12: veredicto **inconcluso** en las tres
  fuentes; los datos no permiten distinguir la media de cero con la regla fijada (p. ej. W2 A:
  0.088 %/mes, IC95 NW [−0.566, 0.742], t NW 0.26).
- La reconstrucción B a partir de las 6 carteras value-weighted reproduce la serie publicada A
  dentro del error de redondeo.
- Una construcción independiente (AQR) produce los mismos veredictos y correlación ≥ 0.9649 con A
  en cada ventana; la conclusión no depende de la fuente elegida.

**NO permitidas:**
- Decir que "el momentum murió", "dejó de funcionar" o que su prima es cero después de 2006:
  "inconcluso" no es evidencia de media cero (los IC95 NW de W2 llegan hasta +0.742 %/mes en A y
  +0.804 %/mes en C).
- Afirmar un cambio estructural o una diferencia estadísticamente significativa entre W1 y W2:
  no se pre-registró ni se hizo una prueba de diferencia de medias entre ventanas.
- Atribuir causas (publicación de la anomalía, saturación, crisis de 2009, etc.) al cambio entre ventanas.
- Presentar la media x12 como CAGR, o el compuesto de la serie largo-corto como rendimiento de una
  cuenta o de una estrategia implementable (no incluye costos de transacción, préstamo de acciones,
  impuestos, capacidad ni requerimientos de margen).
- Extrapolar a otros países, a otras definiciones de momentum o al futuro.
- Elegir nuevas ventanas a partir de estos resultados sin adenda fechada y justificada.

## 13. Verificaciones de la implementación

- `sha256sum -c datos/SHA256SUMS.txt` → OK para los 3 archivos (y `auditoria.py` lo re-verifica).
- Newey-West: con 0 rezagos el EE coincide con DE/√n (0.262962 en W1-A por ambas vías), y con 6
  rezagos coincide con un cálculo de doble suma directa de Σ w(|i−j|)·d_i·d_j (0.236574 en W1-A).
- Reproducir: `cd laboratorio/auditorias/AC-01-momentum-eua && python3 auditoria.py` (sin red).

## Adenda 2026-09-25 (escrita tras la primera ejecución; no altera ningún veredicto)

- Se añadió a las comparaciones una métrica descriptiva no listada en la sección 3: número de meses
  con |dif| > 0.015 pp. Justificación: A viene redondeada a ±0.005 y B combina 4 insumos redondeados
  a ±0.005 con pesos ½ (error ≤ ±0.01), así que |B − A| ≤ 0.015 es atribuible solo a redondeo.
  Esta métrica se codificó antes de la primera ejecución, pero no estaba en la especificación escrita.
- Para C vs A se reportan también diferencia media y máxima diferencia absoluta (además de la
  correlación pre-especificada), por simetría con B vs A.
- Se añadió `datos/PROCEDENCIA.txt` (URLs, cabeceras HTTP y versiones).
