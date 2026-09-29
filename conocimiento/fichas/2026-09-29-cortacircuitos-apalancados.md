# Ficha de estudio (continuación): cortacircuitos de la arena con apalancamiento, para el comité del 2-oct

> Bloque de trabajo continuo, 29-sep-2026 (01:10 UTC). Fase 0, no es recomendación. Continúa `2026-09-28-cortacircuitos-arena.md`, que dejó como siguiente prueba repetir el cálculo con 3x y filtro SMA200. Es insumo directo del comité del 2-oct (modo C: hasta 50% en ETF 3x con `filtro_apalancados`).
> Código: `conocimiento/fichas/codigo/2026-09-29-cortacircuitos-apalancados.py` (~3 s).

## 1. Pregunta
¿Cuánto cambia la probabilidad de tocar cada cortacircuitos de `arena_agresivo` (−12/−20/−28/−35%, y −50% = tope de 10,000 MXN), y la distribución del rendimiento de temporada, al pasar de la cartera A (beta 1x) a las candidatas del modo C?

## 2. Método y supuestos
- **Datos:** Yahoo `^SP500TR`, `^GSPC` y `^VIX` (rango 30y), FRED `DEXMXUS` y `DTB3`. Días de 1997-07 a 2026-09 (n = 7,346). Temporadas de 85 días hábiles, una cada 5 días (1,453, traslapadas).
- **Simulador de R06** (reproduce UPRO/TQQQ reales con ρ ≥ 0.9956 y sobreestima el CAGR 0.7-1.6 pp/año): r_L = L·r − (L−1)·rf − 0.9%/año, re-apalancado diario.
- **Filtro** (`filtro_apalancados`): si el ^GSPC cierra debajo de su SMA200 en t, el sleeve 3x está en efectivo (rf) en t+1. Variante: además, ^VIX < 25.
- Sin costos de transacción de GBM, sin spread cambiario ni impuestos, y **sin las acciones de los cortacircuitos**, que recortarían exposición después de −12%. Por eso las probabilidades de −20% y más son una cota superior.
- Subyacente: S&P 500. El TQQQ (Nasdaq-100) tiene más volatilidad; sus colas serían más gruesas que las de aquí (inferencia, no calculado).

## 3. Resultados (en MXN)
| Cartera | −12% | −20% | −28% | −35% | −50% | p10 | Mediana | p90 | P(> +40%) |
|---|---|---|---|---|---|---|---|---|---|
| A actual: 100% 1x | 0.171 | 0.028 | 0.000 | 0.000 | 0.000 | −6.5% | +4.8% | +14.3% | 0.000 |
| C1: 50% 3x **sin** filtro + 50% 1x | 0.483 | 0.227 | 0.138 | 0.066 | **0.008** | −15.2% | +7.5% | +25.2% | 0.021 |
| C2: 50% 3x con SMA200 + 50% 1x | 0.289 | 0.065 | 0.000 | 0.000 | 0.000 | −9.2% | +5.2% | +21.3% | 0.004 |
| C3: 50% 3x con SMA200 y VIX + 50% 1x | 0.277 | 0.046 | 0.000 | 0.000 | 0.000 | −9.5% | +5.2% | +20.2% | 0.001 |
| C4: 100% 3x con SMA200 | 0.636 | 0.268 | 0.090 | 0.036 | 0.000 | −16.9% | +5.9% | +31.4% | 0.041 |

## 4. Lectura
1. **El filtro es la diferencia entre sobrevivir y no.** Sin filtro, el 50% en 3x toca el tope del dueño en 0.8% de las temporadas y la pausa de −28% en 13.8%. Con filtro, ninguna temporada desde 1997 pasa de −28%. Confirma R06 ("solo protección") en la métrica que importa para la arena.
2. **El apalancamiento filtrado no sube la mediana, sube la cola derecha.** C2 contra A: la mediana va de +4.8% a +5.2%, pero el p90 de +14.3% a +21.3%. El costo es el doble de probabilidad de tocar −12% (0.29 contra 0.17) y un p10 de −9.2% contra −6.5%. En un torneo con pocos participantes, comprar cola derecha puede ser racional; en crecimiento esperado casi no cambia nada.
3. **El VIX < 25 casi no aporta** (C3 contra C2: −20% baja de 6.5% a 4.6%, a cambio de algo de p90). Coincide con R06, que propone quitarlo o dejarlo como opcional.
4. **La meta del dueño (+40% mínimo) está fuera de la distribución histórica** de cualquier candidata razonable: P(> +40%) de 0% a 4% en 4 meses, y la más alta (C4) exige aceptar 64% de probabilidad de tocar −12% y 27% de −20%. Es un dato duro para la conversación con el dueño: la meta, tal como está, solo se alcanza con suerte o con más riesgo del que permiten sus propios cortacircuitos.

## 5. Límites y contraejemplo
- Temporadas traslapadas: pocos episodios independientes (2000-02, 2008, 2011, 2015-16, 2018, 2020, 2022) dominan las colas.
- El filtro reacciona con un día de rezago y al cierre. Un salto como el del 16-mar-2020 o el de agosto de 2024 entra antes de que el filtro actúe. La simulación sí los incluye, porque son datos diarios reales.
- **Contraejemplo:** en un mercado lateral con cruces repetidos de la SMA200 (2015-16), el filtro entra y sale; el costo de esas vueltas en GBM (0.58% por vuelta + spread) no está en la simulación.

## 6. Estado
El tema "Cortacircuitos de drawdown y rachas" sigue en **Comprendido con comprobación**. Esta ficha agrega la dimensión de apalancamiento. Para llegar a "Contrastado" falta una segunda implementación independiente, que puede hacer el `auditor-de-replicas`, con costos de GBM y con TQQQ real desde 2010.
