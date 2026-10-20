# Réplica R17: ¿dimensionar el 3x por volatilidad objetivo, encima del filtro, protege mejor que el filtro solo?

> Laboratorio del 20-oct-2026. Fase 0: no recomienda inversiones. **Pre-registro y script en el mismo commit, antes de cualquier corrida** (plantilla del 20-oct). sha256 de `R17.py`: `8ef544ca27a5688683bb7a194bce076a4f660825998ea074c380e61a5686428c`.

**Origen.** La pregunta abierta del aprendizaje del 19-oct: si el stop fijo del UPRO es caro y casi siempre redundante (R16), ¿un tamaño por volatilidad acota mejor el riesgo? Es la idea de Moreira y Muir (2017) aplicada al 3x y encima del filtro.

**Conocimiento previo declarado:**
- **R05:** en el mercado 1x, la volatilidad gestionada no tiene alfa fuera de muestra (α post-2017 −0.75%). `vol_c1` frena las caídas con costo de CAGR (MDD −16.2% contra −24.8% fuera de muestra). AC-06 concuerda.
- **R16:** V0 (filtro vigente) en este mismo 3x tiene Sharpe 0.537 y MDD −73.7%. El stop fijo empeora las dos cosas.
- **Cap. 02 §6.1:** "vol-targeting como freno, no como fuente de alfa" (Cederburg et al.).
- **No he corrido** ninguna volatilidad objetivo sobre un 3x.
- **Expectativa propia:** mejora la MDD (el 3x es justamente donde la volatilidad se agrupa más) con un Sharpe parecido. No tengo cifra.

## PRE-REGISTRO

### 1. Hipótesis
- **H1:** VT45 (volatilidad objetivo de 45% anual, el nivel de un 3x con un índice de 15%) mejora la MDD frente a V0 en **al menos 5 pp** y **no baja el Sharpe más de 0.03**. 3x sintético del S&P 500 TR, 1990-10 a 2026-10-16.
- **H2 (informativa):** VT45 tiene un Sharpe mayor que V0.
- **Mecanismo:** la volatilidad se agrupa. Cuando la volatilidad realizada del 3x sube, la exposición baja antes de que el índice cruce la SMA200 × 0.97; el filtro tarda semanas.

### 2. Criterio y estado
- **H1 refutada** si la mejora de MDD es menor a 5 pp **o** el Sharpe baja más de 0.03.
- **Estado:** H1 sostenida, "Replicado"; H1 refutada, "No replicado". H2 no cambia el estado.
- **Consecuencia:** ninguna regla cambia en el laboratorio. Si H1 se sostiene, va como insumo al comité.

### 3. Datos
- **A:** la caché de R16 (`R16-datos/series.json`: Yahoo `^GSPC`, `^SP500TR`, `^VIX` y FRED DTB3, hasta el 16-oct-2026). Es la misma que AC-22 confirmó.
- **B:** la elige el auditor, distinta de A si es posible. Código desde cero.

### 4. Instrumento
3x diario sintético del S&P 500 TR: r3 = 3·r_TR − 2·rf − 0.91%/252, igual que R11 y R16. La parte no invertida rinde la T-bill.

### 5. Disponibilidad
- **Filtro:** señal del cierre de t−1, decisión al cierre de t (igual que R16).
- **Volatilidad realizada:** desviación estándar de los 20 rendimientos diarios del 3x previos a t (sin t), anualizada con √252.

### 6. Periodo
Desde que hay filtro y 20 días de volatilidad hasta el 16-oct-2026. Subperiodos informativos: 1990-2008 y 2009-hoy.

### 7. Limpieza
La de R16.

### 8. Reglas y variantes (N = 3 objetivos más V0)
- **V0:** filtro vigente (salida si `^GSPC` < SMA200 × 0.97 o VIX ≥ 25; entrada si `^GSPC` > SMA200 y VIX < 25). Exposición de 100% o 0%.
- **VT30, VT45 (principal) y VT60:** con el filtro encendido, la exposición es w = min(1, objetivo / volatilidad realizada a 20 días). Sin apalancamiento adicional: w ≤ 1. Con el filtro apagado, w = 0.
- **Rebalanceo:**
  - entrada y salida del filtro: al día;
  - ajuste del peso: solo los viernes y solo si |w* − w| > 10 pp.

### 9. Costos
0.10% por lado sobre el nocional que se mueve. USD, sin impuestos.

---

## RESULTADOS (se llenan después de correr)
