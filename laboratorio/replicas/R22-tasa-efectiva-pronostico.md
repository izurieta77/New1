# Réplica R22: ¿qué regla pronostica mejor la tasa efectiva trimestral de impuestos?

> Laboratorio del 29-oct-2026. Fase 0: no recomienda inversiones. **Pre-registro y script en el mismo commit, antes de correr.** sha256 de `R22.py`: `3b243c1f6f5b7bb688fdfd5718d1a3208a1c9d733dff027c471b9296946adc69`.

| Campo | Valor |
|---|---|
| ID | R22 |
| Origen | Seis errores de tasa efectiva en seis reportes de la semana (AMX, BOLSA, Cemex, Visa, KOF, Walmex); propuesta de la plantilla §8 en `bitacora/decisiones-pendientes.md` (28-oct): "usar la mediana de 4 trimestres" |
| Pre-registro escrito el | 2026-10-29 17:49 UTC, antes de cualquier corrida |
| Commit | el commit que trae este archivo junto con `R22.py` |
| Responsable | orquestador (A); auditor-de-replicas (B, `auditorias/AC-29-R22/`) |
| Estado | **No replicado** (rige el lado más conservador, A). A y B difieren por un defecto de datos de A; ver abajo |

**Conocimiento previo declarado:** solo los seis casos anecdóticos (mexicanos en su mayoría). No he medido nada con datos de EUA. **Expectativa:** la mediana de 4 trimestres le gana al último trimestre, con un MAE de 2-4 pp.

## PRE-REGISTRO
### 1. Hipótesis
- **H1:** el MAE (puntos porcentuales) de la regla "mediana de los últimos 4 trimestres" es menor que el de "último trimestre", y la prueba de signos pareada da p < 0.05 (dos colas).
- **H2:** el MAE de la mediana de 4 es ≤ 3.0 pp.

### 2. Medidas
- MAE y mediana del error absoluto para cinco reglas: último trimestre, mediana de 4, media de 4, mediana de 8 y 21% fijo (tasa federal estatutaria).
- IC 95% de la diferencia de MAE (último − mediana de 4) por remuestreo.
- Error de UPA implícito, ≈ |Δτ| / (1 − τ).

### 3. Datos y reglas
- **Universo:** emisoras con mercado = US en `empresas/universo.csv`, sin BRK-B ni SPCX. Las emisoras mexicanas no tienen XBRL en la SEC: el resultado **no** se transfiere sin más a ellas, y se declara.
- **Datos:** SEC companyconcept (data.sec.gov, User-Agent por defecto del repo, sin correo), conceptos `IncomeTaxExpenseBenefit` y la utilidad antes de impuestos (tres etiquetas alternativas; gana la de serie más larga).
  - Trimestres = duraciones de 80-100 días; gana el último presentado.
  - Q4 casi nunca existe como duración trimestral y queda fuera.
- **Filtro:** utilidad antes de impuestos > 0 y ETR entre 0% y 60%, para objetivos y para la historia.
- **Objetivos:** trimestres con fin entre 2022-01-01 y 2026-09-30, con al menos 4 trimestres previos en los 460 días anteriores (8 en 830 días para la mediana de 8).
- **Criterio:** H1 y H2 con su umbral literal. **"Replicado"** si B, con código propio, concuerda en H1 y H2 y su MAE de la mediana de 4 queda a ±0.3 pp del de A.
- **Etiqueta:** no aplica (método de pronóstico).

## RESULTADOS · Ejecución A (29-oct-2026, después del commit del pre-registro `ba6cb83`)
- **Muestra:** 29 emisoras, 194 trimestres objetivo; GE falló (ticker no encontrado).
- **MAE (pp):** último 3.406; **mediana de 4: 3.029**; media de 4: 3.196; mediana de 8: 2.981 (n = 5); 21% fijo: 5.676.
- **Signos:** la mediana de 4 gana 109 y pierde 85; z = 1.72, **p = 0.085**. IC95 de la diferencia de MAE: [0.004, 0.760].
- **Error de UPA implícito:** 3.88%.
- **Veredicto A:** **H1 refutada** (p ≥ 0.05) y **H2 refutada** (3.029 > 3.0, por 0.029 pp).

## RESULTADOS · Ejecución B (auditor-de-replicas, `auditorias/AC-29-R22/`, 29-oct-2026)
- **Construcción propia:** companyfacts completo; etiquetas de utilidad antes de impuestos unidas periodo a periodo (sin `...Domestic`); XOM unido con su predecesora; GE resuelto (CIK 40545); prueba de signos exacta; bootstrap iid y por emisora. Variante con el 4T reconstruido (anual menos 9 meses).

| Medida | A | B sin 4T (comparable) | B con 4T |
|---|---|---|---|
| Emisoras / objetivos | 29 / 194 | 43 / 307 | 45 / 657 |
| MAE mediana de 4 | 3.029 | **2.987** | 3.589 |
| MAE último | 3.406 | 3.535 | 4.833 |
| MAE 21% fijo | 5.676 | 5.787 | 6.437 |
| Signos (gana / pierde), p | 109/85, 0.085 | **174/133, 0.022** | 400/257, 2.7e−8 |
| IC95 diferencia de MAE | [0.004, 0.760] | [0.199, 0.929] (por emisora [0.195, 0.964]) | [0.902, 1.612] |
| H1 / H2 | no / no | **sí / sí (por 0.013 pp)** | sí / no |

- **Por qué difieren:** la regla de A ("gana la etiqueta de utilidad antes de impuestos con la serie más larga") elige, en 12 emisoras (WMT, HD, JNJ, ABBV, UNH, GOOGL, NFLX, V, NVDA, MSFT, AMAT, TMO), una etiqueta que **dejó de reportarse en 2021**, así que esas emisoras se quedan sin objetivos desde 2022. Se suman GE y XOM. **Con la regla de A, B reproduce A al tercer decimal.**
- **Estado (rige el más conservador):** **No replicado.** H1 y H2 quedan refutadas en A y sostenidas en B; la discrepancia se explica por un defecto de datos de A (registro de errores), no por el método.
- **Lectura vigente** [inferencia, válida en las dos construcciones]:
  - la **mediana de 4 trimestres le gana siempre al último trimestre**, por 0.35 a 1.24 pp de MAE;
  - el 21% fijo es la peor regla (5.7-6.4 pp);
  - aun con la mejor regla, el error típico es de **~3-3.6 pp de tasa ≈ 4-5% de UPA**, y el intervalo de la UPA tiene que incluirlo.
  - H2 (≤ 3 pp) es frágil.
- **Para repetir:** R22b, con nuevo pre-registro (unión de etiquetas periodo a periodo y 4T reconstruido), para que A y B midan lo mismo.
