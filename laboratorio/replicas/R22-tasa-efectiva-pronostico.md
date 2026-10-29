# Réplica R22: ¿qué regla pronostica mejor la tasa efectiva trimestral de impuestos?

> Laboratorio del 29-oct-2026. Fase 0: no recomienda inversiones. **Pre-registro y script en el mismo commit, antes de correr.** sha256 de `R22.py`: `3b243c1f6f5b7bb688fdfd5718d1a3208a1c9d733dff027c471b9296946adc69`.

| Campo | Valor |
|---|---|
| ID | R22 |
| Origen | Seis errores de tasa efectiva en seis reportes de la semana (AMX, BOLSA, Cemex, Visa, KOF, Walmex); propuesta de la plantilla §8 en `bitacora/decisiones-pendientes.md` (28-oct): "usar la mediana de 4 trimestres" |
| Pre-registro escrito el | 2026-10-29 17:49 UTC, antes de cualquier corrida |
| Commit | el commit que trae este archivo junto con `R22.py` |
| Responsable | orquestador (A); auditor-de-replicas (B, `auditorias/AC-29-R22/`) |
| Estado | en curso |

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
