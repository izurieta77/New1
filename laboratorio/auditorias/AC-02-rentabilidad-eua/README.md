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

## RESULTADOS

(pendiente — se completa después de descargar, congelar y calcular)
