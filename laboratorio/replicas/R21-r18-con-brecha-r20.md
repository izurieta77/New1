# Réplica R21: probabilidades de cortacircuitos de R18 con el UPRO realista de R20

> Laboratorio del 28-oct-2026. Fase 0: no recomienda inversiones. **Pre-registro y script en el mismo commit, antes de correr.** sha256 de `R21.py`: `dfcb7675beea539641126a912f6e03596b0a3d0ab483f15043e8a5e7ce8ba00f`.

| Campo | Valor |
|---|---|
| ID | R21 |
| Origen | Pregunta abierta del aprendizaje del 27-oct; revisión del 27-oct §0 (a''): "R18 es optimista para el UPRO". Insumo para el comité W44 (30-oct) |
| Pre-registro escrito el | 2026-10-28 17:52 UTC, antes de cualquier corrida |
| Commit | el commit que trae este archivo junto con `R21.py` |
| Responsable | orquestador (A); auditor-de-replicas (B, `auditorias/AC-28-R21/`) |
| Estado | en curso |

**Conocimiento previo declarado:** R18 (3x sintético) y R20 (UPRO real −1.59 pp por año en total, −2.30 con DTB3 ≥ 3%; B −1.55 / −2.22). Expectativa: con el peso vigente (13.5%), la brecha casi no mueve las colas. Sería un cambio de décimas de punto en P(−12%) y de ~−0.2 pp por año en el CAGR de la mezcla.

## PRE-REGISTRO
### 1. Hipótesis (sobre el peso vigente, U13.5)
- **H1:** restar la brecha por tramos de R20-A sube P(caer −12% desde el máximo de la ventana en 126 días hábiles) en **≤ 1.0 pp** frente a R18 sin brecha.
- **H2:** el CAGR de la mezcla baja entre **−0.30 y −0.10 pp por año**.

### 2. Medidas
- P(−12%) y P(−20%) en 63 y 126 días, y CAGR. Para U13.5 y U27, en tres modos: sin brecha (R18), brecha constante (−1.59) y brecha por tramos de DTB3 (−1.31 / −1.54 / −2.30).
- La brecha **solo se resta los días en que el UPRO está invertido** (filtro V0 encendido).

### 3. Criterio y estado
- H1 y H2 se sostienen o se refutan con su umbral literal.
- **"Replicado"** si B, con código propio, concuerda en H1 y H2 y su ΔP(−12%, 126 d) queda dentro de ±0.5 pp del de A.
- **Etiqueta:** no aplica (calibración de riesgo).

### 4. Datos y reglas
- Los de R18: cachés de R16 y R12; mezcla SPYM/QQQM/UPRO/efectivo con rebalanceo mensual; QQQM 26.8% y efectivo 5.3% fijos, como en R18. Se reutilizan `R18.curva` y `R18.cargar`.
- **Métrica de toque:** la de R18, contra el máximo **de cada ventana**, no el histórico. La salvedad del 25-oct (AC-24) sigue: con el DD de hoy contra el máximo histórico, P(−12%) es mayor. Esa variante no es parte de R21.
- **Sesgos declarados:**
  - los pesos de R18 no son los del libro de hoy (el efectivo real es 18.4%, no 5.3%);
  - la brecha de R20 se midió en 2009-2026 y aquí se aplica también a 1990-2008.
