# Réplica R21: probabilidades de cortacircuitos de R18 con el UPRO realista de R20

> Laboratorio del 28-oct-2026. Fase 0: no recomienda inversiones. **Pre-registro y script en el mismo commit, antes de correr.** sha256 de `R21.py`: `dfcb7675beea539641126a912f6e03596b0a3d0ab483f15043e8a5e7ce8ba00f`.

| Campo | Valor |
|---|---|
| ID | R21 |
| Origen | Pregunta abierta del aprendizaje del 27-oct; revisión del 27-oct §0 (a''): "R18 es optimista para el UPRO". Insumo para el comité W44 (30-oct) |
| Pre-registro escrito el | 2026-10-28 17:52 UTC, antes de cualquier corrida |
| Commit | el commit que trae este archivo junto con `R21.py` |
| Responsable | orquestador (A); auditor-de-replicas (B, `auditorias/AC-28-R21/`) |
| Estado | **Replicado** (B AC-28, 28-oct-2026) |

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

## RESULTADOS · Ejecución A (28-oct-2026, después del commit del pre-registro `1554d62`)
Datos: sha256 de la caché de R16 `42339a50…466b`; del 1990-10-17 al 2026-10-16, 9,065 días.

| Peso | Modo | P(−12%) 63 d / 126 d | P(−20%) 63 d / 126 d | CAGR |
|---|---|---|---|---|
| U13.5 | sin brecha | 16.43 / 30.12 | 4.19 / 12.59 | 13.297% |
| U13.5 | constante (−1.59) | 16.45 / 30.13 | 4.25 / 12.60 | 13.114% |
| U13.5 | tramos | 16.45 / **30.43** | 4.25 / 12.60 | **13.083%** |
| U27 | sin brecha | 21.02 / 40.91 | 3.05 / 12.00 | 14.125% |
| U27 | tramos | 21.28 / 42.16 | 3.05 / 12.12 | 13.698% |

- **H1 sostenida:** ΔP(−12%, 126 d) = **+0.31 pp** ≤ 1.0.
- **H2 sostenida:** ΔCAGR = **−0.214 pp por año**, dentro de [−0.30, −0.10].
- Con U27: +1.25 pp y −0.43 pp por año.

## RESULTADOS · Ejecución B (auditor-de-replicas, `auditorias/AC-28-R21/`, 28-oct-2026)
- **Método:** código desde cero, sin importar R16/R18/R21. Yahoo descargado hoy; DTB3 copiado de AC-27, porque FRED no respondió.
- **Variante con otra fuente** (FRED NASDAQ100 y CBOE VIX): todas las celdas a ≤ 0.03 pp.
- **Sin brecha, B reproduce R18.** Las 30 celdas coinciden con A a ≤ 0.01 pp y el CAGR al milésimo.
- **Una diferencia de A:** `prob` de `R21.py` omite la última ventana completa (8,939 en vez de 8,940). Es menor y no cambia los veredictos.
- **Veredicto B:** H1 (+0.31 pp) y H2 (−0.214) sostenidas.
- **Estado: Replicado.** La independencia es de código y de las series del NDX y del VIX, no del proveedor del S&P TR (Yahoo en las dos).

**Lectura para el comité W44:**
- Con el UPRO en 13.5%, la brecha de R20 **no cambia las colas** de R18: +0.3 pp en P(−12%). Cuesta ~0.2 pp por año de CAGR.
- Con el 27% de antes de B1, la brecha sí pesaba: +1.25 pp y −0.43 pp por año.
- **Las probabilidades de R18 siguen siendo válidas para el libro vigente**, con la salvedad del 25-oct (métrica contra el máximo de la ventana, no contra el histórico).

## Nota exploratoria (trabajo continuo, 2026-10-29 01:11 UTC; revisión del 28-oct C3): contra la mezcla **sin** UPRO
**No es parte del pre-registro ni del estado "Replicado".** Es un cálculo exploratorio con las mismas funciones de `R21.py` y `R18.py` y los mismos datos (1990-10-17 a 2026-10-16). En U0 el peso del UPRO pasa a SPYM.

| Mezcla | CAGR | P(−12%, 126 d) | P(−20%, 126 d) | MDD | Vol anual |
|---|---|---|---|---|---|
| U0 (sin UPRO) | 12.36% | 25.46% | 9.37% | −58.3% | 18.56% |
| U13.5, sin brecha | 13.30% | 30.12% | 12.59% | −56.9% | 19.10% |
| **U13.5, con la brecha de R20** | **13.08%** | **30.43%** | **12.60%** | −57.0% | 19.10% |

- **Lectura** [inferencia]: con la brecha, el 13.5% de UPRO aporta **+0.73 pp por año de CAGR** frente a no tenerlo. Lo paga con **+5.0 pp de probabilidad de tocar −12%** y **+3.2 pp de tocar −20%** en 126 días; la MDD no empeora, por el filtro.
- **Por eso "las probabilidades de R18 siguen siendo válidas" no es un respaldo del 3x.** Dice solo que la brecha no cambia el costo en colas del UPRO, que ya era de ~5 pp en P(−12%).
- **Límite:** es una muestra (1990-2026) con un S&P fuerte. El rendimiento extra del 3x depende de μ − r (ficha del 27-oct: con r = 3.8% y σ = 17%, el empate es μ ≈ 11.2%).
- Es **insumo para el comité W44**, no una decisión.
