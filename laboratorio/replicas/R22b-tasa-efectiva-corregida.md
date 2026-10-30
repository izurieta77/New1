# Réplica R22b: pronóstico de la tasa efectiva con las etiquetas XBRL corregidas y el 4T reconstruido

> Laboratorio del 30-oct-2026. Fase 0: no recomienda inversiones. **Pre-registro y script en el mismo commit, antes de correr.** sha256 de `R22b.py`: `1b02352f0b205e295a2b3045fa63895a3d2e4ae7d8ea85dd0b3fa70e1110c092`.

| Campo | Valor |
|---|---|
| ID | R22b |
| Origen | R22 quedó **No replicado** porque la ejecución A tomó una etiqueta descontinuada en 12 emisoras (registro de errores, 29-oct). Pendiente anotado en `R22-tasa-efectiva-pronostico.md` y en `decisiones-pendientes.md` |
| Pre-registro escrito el | 2026-10-30 17:49 UTC, antes de correr `R22b.py` |
| Commit | el commit que trae este archivo junto con `R22b.py` |
| Responsable | orquestador (A). **B = AC-29** (`auditorias/AC-29-R22/`), ya calculada antes de este pre-registro con código independiente; se declara |
| Estado | **Replicado** (A corregida = B AC-29, que no fue ciega). H2 frágil: 2.99999 pp contra el umbral de 3.0 |

**Conocimiento previo declarado (contaminación):** **ya conozco los resultados de B (AC-29)**: sin 4T, MAE de la mediana de 4 = 2.987, signos 174/133 con p = 0.022; con 4T, 3.589 y p = 2.7e−8. Este pre-registro **no** es ciego. Lo que prueba es que A, corregida y escrita aparte, llega a lo mismo.

## PRE-REGISTRO
### 1. Hipótesis
- **H1 (sin 4T):** la mediana de 4 tiene un MAE menor que el último trimestre y la prueba de signos exacta da p < 0.05.
- **H2 (sin 4T):** el MAE de la mediana de 4 es ≤ 3.0 pp.
- **H3 (con el 4T reconstruido):** igual que H1, con p < 0.05.

### 2. Cambios contra R22 (corrección del defecto)
- Utilidad antes de impuestos: **unión periodo a periodo** de `...ExtraordinaryItemsNoncontrollingInterest` y `...MinorityInterestAndIncomeLossFromEquityMethodInvestments`. Gana la primera con dato. **Se quita `...Domestic`**.
- Datos de companyfacts completo.
- CIK fijo para GE (40545) y para XOM (34088 y 2115436, unidos).
- **4T reconstruido** = anual (350-380 días) − 9 meses (260-290 días) con el mismo inicio, para el impuesto y para la utilidad antes de impuestos.
- Prueba de signos **binomial exacta**.
- Todo lo demás es igual a R22: filtro 0-60% y utilidad > 0, ventanas de 460 y 830 días, objetivos 2022-01 a 2026-09.

### 3. Criterio
- **"Replicado"** si A y B (AC-29) coinciden en H1, H2 y H3, y los MAE de la mediana de 4 quedan a ±0.3 pp en las dos variantes.
- **Etiqueta:** no aplica.

## RESULTADOS · Ejecución A (30-oct-2026, después del commit del pre-registro `1a87a1a`)
48 emisoras con serie, sin fallidos.

| Medida | A (R22b) sin 4T | B (AC-29) sin 4T | A con 4T | B con 4T |
|---|---|---|---|---|
| Objetivos | 309 | 307 | 647 | 657 |
| MAE mediana de 4 (pp) | **3.000** (2.99999) | 2.987 | **3.620** | 3.589 |
| MAE último | 3.540 | 3.535 | 4.856 | 4.833 |
| MAE 21% fijo | 5.770 | 5.787 | 6.460 | 6.437 |
| Signos (gana / pierde), p exacta | 175/134, **0.0227** | 174/133, 0.022 | 392/255, < 1e−5 | 400/257, 2.7e−8 |
| IC95 de la diferencia de MAE | [0.192, 0.922] | [0.199, 0.929] | [0.882, 1.607] | [0.902, 1.612] |
| Error de UPA implícito | 3.81% | 3.80% | 4.87% | 4.82% |

**Veredicto con el criterio literal:** H1 sostenida en A y B; **H2 sostenida en A por 0.00001 pp** (2.99999 ≤ 3.0) y en B (2.987); H3 sostenida en A y B. MAE de la mediana de 4 dentro de ±0.3 pp en las dos variantes (0.013 y 0.031). **Estado: Replicado.** Salvedades:
- **B no fue ciego** respecto de este pre-registro (se conocía su resultado), aunque el código de A se escribió aparte del de B;
- **H2 queda en el umbral**: con el 4T (3.6 pp) no se cumpliría.

**Lectura vigente para la plantilla §8:**
- La **mediana de 4 trimestres** es la mejor regla simple. Le gana al último trimestre con significancia en las dos variantes (0.5 pp de MAE sin 4T y 1.2 pp con el 4T).
- **El 4T es el trimestre más difícil** (MAE de 3.6 pp contra 3.0): ajustes de fin de año y partidas discretas.
- Error típico de **~4-5% de UPA solo por la tasa**. Es la amplitud mínima del intervalo de la UPA por esta fuente.
- Con esto, **R22 (No replicado) queda superado** por R22b. [Nota 2026-10-30 17:50 UTC]
