# Réplica R18: con UPRO al 26.9%, ¿qué tan probable es tocar el cortacircuitos de −8% en un trimestre?

> Laboratorio del 21-oct-2026. Fase 0: no recomienda inversiones. **Pre-registro y script en el mismo commit, antes de correr.** sha256 de `R18.py`: `006e6f0c5c78b0ef0c6d0d40103d674ee2673196dc7219c1b4e194b9ea1e88b9`.

**Origen.** La pregunta abierta del aprendizaje del 20-oct: R16 y R17 mostraron que el riesgo del UPRO se controla con el tamaño, no con capas rápidas. El tamaño actual (26.9% del papel, decisión W40) nunca se contrastó con los cortacircuitos de `config/parametros.json`: −8% reduce el satélite a la mitad y −12% lo deja en cero.

**Conocimiento previo declarado:**
- R16 y R17: V0 en el 3x tiene una MDD de −73.7% en 1990-2026.
- El papel lleva 22 días con una MDD de −3.35%.
- No he medido la probabilidad de toque de la mezcla.
- **Expectativa propia:** entre 15% y 30% por trimestre con la mezcla vigente, por la beta efectiva de ~1.5x (nocional de 1.48x según W40).

## PRE-REGISTRO

### 1. Hipótesis
- **H1:** con la mezcla vigente, la probabilidad de caer 8% o más bajo el máximo dentro de 63 días hábiles es **≤ 15%** en 1990-2026. La mezcla es SPYM 41.0%, QQQM 26.8%, UPRO 26.9% con filtro V0 y efectivo 5.3%, rebalanceada al inicio de cada mes.
- **H2 (informativa):** bajar UPRO a 13.5% (el resto a SPYM) reduce esa probabilidad en **≥ 5 pp**.

### 2. Criterio y estado
- **H1 refutada** si la probabilidad es mayor a 15%.
- **Estado:** H1 sostenida, "Replicado"; refutada, "No replicado".
- **Consecuencia:** ninguna regla cambia en el laboratorio. Es insumo del comité sobre el tamaño del UPRO.

### 3. Datos
- **A:** la caché de R16 (Yahoo `^GSPC`, `^SP500TR`, `^VIX` y FRED DTB3, hasta el 16-oct-2026) y `^NDX` de la caché de R12. QQQM se aproxima con `^NDX` (precio, sin dividendos) menos 0.15% de gasto anual. SPYM, con `^SP500TR` menos 0.02%.
- **B:** la elige el auditor, distinta si es posible.

### 4. Instrumentos
- UPRO = 3x sintético (3·r_TR − 2·rf − 0.91%/252) cuando el filtro V0 está encendido, y T-bill cuando está apagado (igual que R16).
- Moneda: **USD**. No incluye el tipo de cambio, aunque el papel se mide en MXN. Sesgo declarado: el peso suele depreciarse en las caídas, lo que amortigua en MXN.

### 5. Disponibilidad
Filtro como en R16: señal del cierre de t−2 aplicada al rendimiento del día t.

### 6. Periodo y métrica
- **Periodo:** desde que existen todas las series hasta el 16-oct-2026. Subperiodos informativos: 1990-2008 y 2009-hoy.
- **Métrica:** para cada día de inicio t, ¿la curva cae ≥ 8% bajo su máximo desde t, dentro de t+1..t+63? Se reporta la fracción de días de inicio. Igual para 12%.

### 7. Limpieza
Los días sin dato de alguna serie se omiten.

### 8. Variantes (N = 4)
UPRO al 0%, 13.5%, **26.9% (vigente)** y 40%. QQQM (26.8%) y el efectivo (5.3%) quedan fijos; SPYM absorbe la diferencia.

### 9. Costos
Sin costos de rebalanceo: el rebalanceo es mensual y su costo es pequeño frente a la métrica. Sin impuestos.

---

## RESULTADOS (se llenan después de correr)

### Ejecución A (orquestador): `R18.py` (sin cambios desde el pre-registro, `1e12150`), `R18-salida.txt`, `R18-resultados.json`
9,065 días con todas las series (1990-10-17 a 2026-10-16); 9,003 ventanas de 63 días.

| UPRO | P(caer ≥ 8% en 63 días) | 1990-2008 | 2009-hoy | P(≥ 12%) |
|---|---|---|---|---|
| 0% | 29.5% | 32.2% | 26.7% | 14.8% |
| 13.5% | 36.4% | 37.9% | 34.9% | 16.4% |
| **26.9% (vigente)** | **47.8%** | 49.6% | 45.9% | 21.0% |
| 40% | 55.6% | 58.0% | 53.2% | 26.5% |

### Ejecución B (auditor-de-replicas, código desde cero): `laboratorio/auditorias/AC-24-R18/`
- **Datos:** CBOE SPX + multpl, CBOE VIX, DTB3, FRED NASDAQ100 y DEXMXUS. Son copias ya guardadas, porque FRED estaba en mantenimiento.
- **Muestra:** 9,184 días, hasta el 15-oct.
- **Control:** UPRO-V0 solo da MDD −72.6%, contra −73.5% / −73.7% de R16.

| UPRO | P ≥ 8% | 1990-2008 | 2009-hoy | P ≥ 12% | P ≥ 8% en MXN, 1994-hoy (USD, mismo periodo) |
|---|---|---|---|---|---|
| 0% | 29.7% | 32.5% | 26.9% | 15.3% | 30.8% (32.6%) |
| 13.5% | 36.7% | 38.2% | 35.2% | 16.6% | 33.9% (40.0%) |
| **26.9%** | **48.0%** | 49.7% | 46.2% | 21.4% | 42.8% (50.2%) |
| 40% | 56.1% | 58.4% | 53.7% | 26.9% | 52.3% (57.6%) |

Con ventanas sin traslape, B da 49.3% para la vigente.

### Juicio
- **H1 refutada en A y en B:** con la mezcla vigente, la probabilidad de tocar el cortacircuitos de −8% en un trimestre es **~48%**, más del triple del umbral de 15%.
- **H2 sostenida:** bajar UPRO a 13.5% la reduce 11.3 pp (8.9 pp en MXN).
- **Estado (A y B concuerdan): "No replicado".**
- **Lectura:** el −8% de `config/parametros.json` está dentro del ruido trimestral de una cartera de acciones. Incluso **sin UPRO**, la mezcla lo toca en ~30% de los trimestres. Con UPRO al 26.9%, cerca de uno de cada dos.
  - Los cortacircuitos se diseñaron como freno ante algo anormal. Con esta mezcla se dispararían por volatilidad normal, y cada disparo obliga a reducir el satélite a la mitad: vender abajo, la misma mecánica que R16 midió en el stop.
- **No es una recomendación de cambio.** Es insumo para el comité: ajustar el tamaño (UPRO a ~13.5% baja 11 pp) o recalibrar los niveles a la volatilidad de la mezcla. Las dos son decisiones del comité y del dueño (los cortacircuitos los fijó el dueño el 25-sep).
- **Etiqueta:** no aplica (calibración de riesgo, no prueba de ventaja).
