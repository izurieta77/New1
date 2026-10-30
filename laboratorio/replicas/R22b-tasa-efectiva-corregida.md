# Réplica R22b: pronóstico de la tasa efectiva con las etiquetas XBRL corregidas y el 4T reconstruido

> Laboratorio del 30-oct-2026. Fase 0: no recomienda inversiones. **Pre-registro y script en el mismo commit, antes de correr.** sha256 de `R22b.py`: `1b02352f0b205e295a2b3045fa63895a3d2e4ae7d8ea85dd0b3fa70e1110c092`.

| Campo | Valor |
|---|---|
| ID | R22b |
| Origen | R22 quedó **No replicado** porque la ejecución A tomó una etiqueta descontinuada en 12 emisoras (registro de errores, 29-oct). Pendiente anotado en `R22-tasa-efectiva-pronostico.md` y en `decisiones-pendientes.md` |
| Pre-registro escrito el | 2026-10-30 17:49 UTC, antes de correr `R22b.py` |
| Commit | el commit que trae este archivo junto con `R22b.py` |
| Responsable | orquestador (A). **B = AC-29** (`auditorias/AC-29-R22/`), ya calculada antes de este pre-registro con código independiente; se declara |
| Estado | en curso |

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
