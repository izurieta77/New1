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
*(Las secciones de resultados se añaden después de ejecutar `auditoria.py`.)*
