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

### Ejecución A (orquestador): `R17.py` (sha256 8ef544ca…, sin cambios desde el pre-registro), `R17-salida.txt`, `R17-resultados.json`
Datos de la caché de R16: 9,266 días, de 1990-01-02 al 2026-10-16.

| Variante (1990-10-17 a 2026-10-16) | CAGR | Vol | Sharpe | MDD | Exposición media | Cambios |
|---|---|---|---|---|---|---|
| V0 filtro vigente | +15.2% | 32.6% | 0.537 | −73.7% | 0.75 | 217 |
| VT30 | +12.9% | 25.9% | 0.519 | −61.5% | 0.62 | 520 |
| **VT45** | **+14.5%** | 30.7% | **0.530** | **−71.9%** | 0.72 | 303 |
| VT60 | +15.4% | 32.2% | 0.545 | −73.4% | 0.74 | 236 |

Subperiodos, VT45 contra V0:
- 1990-2008: MDD −71.9% contra −73.7%; Sharpe 0.448 contra 0.457.
- 2009-hoy: MDD −45.3% contra −49.3%; Sharpe 0.610 contra 0.616.

### Ejecución B (auditor-de-replicas, código desde cero): `laboratorio/auditorias/AC-23-R17/`
Datos: CBOE SPX y VIX, multpl y DTB3 (los de AC-22, con sha256 iguales). Evaluación desde el 1990-10-01.

| Variante | CAGR | Vol | Sharpe | MDD | Exposición media | Cambios |
|---|---|---|---|---|---|---|
| V0 | 15.15% | 32.6% | 0.516 | −73.5% | 0.75 | 217 |
| VT30 | 12.91% | 25.9% | 0.498 | −60.8% | 0.62 | 522 |
| **VT45** | **14.44%** | 30.7% | **0.509** | **−72.0%** | 0.71 | 304 |
| VT60 | 15.38% | 32.1% | 0.525 | −73.0% | 0.74 | 235 |

- **Sensibilidad (peso que deriva entre ajustes):** ΔMDD +1.9 pp y ΔSharpe −0.006.
- **Por qué casi no mejora (B):** la MDD de V0 y la de VT45 caen en el mismo episodio, de 1998-07 a 2003-04. Fue un mercado bajista lento, con rebotes de volatilidad baja en los que el filtro volvía a entrar con exposición casi completa.

### Juicio
- **H1 refutada en A y en B:** con VT45, ΔMDD es +1.7 pp (A) y +1.5 pp (B), lejos del umbral de ≥ 5 pp; ΔSharpe −0.008 en las dos.
- **H2 refutada.**
- **Estado (A y B concuerdan): "No replicado".**
- **Lo informativo (no decide, por pruebas múltiples):** VT30 baja la MDD 12-13 pp a cambio de 2.3 pp de CAGR y −0.018 de Sharpe. Es el mismo trade-off de "freno con costo" que R05 encontró en el 1x. Parece más una reducción de exposición (media 0.62 contra 0.75) que una mejor regla.
- **Lectura conjunta con R16:** ni el stop fijo ni la volatilidad objetivo de 45% mejoran al filtro vigente en caídas lentas (2000-2002), que es donde está la MDD. La palanca que sí mueve la MDD es la **exposición media**. Esa decisión es de tamaño de la posición, y la toma el comité.
- **Etiqueta:** descartada como mejora del filtro.
