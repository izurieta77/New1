# Ficha de estudio: ¿cuánto cuesta, en pesos, el apetito del modo C?

> Bloque de trabajo continuo, 2-oct-2026 (19:10 CDMX). Responde la pregunta abierta del resumen de aprendizaje del 2-oct: Kelly fraccional sugería casi nada de 3x, pero el comité eligió ~27% de UPRO por mandato del dueño. ¿Cuánto crecimiento esperado gana o pierde eso?
> Código: `conocimiento/fichas/codigo/2026-10-02-costo-del-apetito.py` (stdlib, semilla 20261002, ~4 s).

## 1. Supuestos
- **Cartera A:** 56% SPY + 27% QQQ + 17% efectivo. **Cartera W40:** 40% SPY + 27% QQQ + 27% UPRO + 6% efectivo.
- **Mercado:** σ S&P 16%, σ Nasdaq-100 21%, correlación 0.90. T-bill 5% (el financiamiento del UPRO cuesta 2 × r_f) y gasto del UPRO 0.91%. El efectivo rinde 7% (CETES). Prima del Nasdaq = prima del S&P + 1 pp.
- **Crecimiento:** g = media aritmética − ½σ². Temporada de 85 días hábiles.
- **Riesgo de la temporada:** Monte Carlo lognormal semanal (20,000 caminos) para P(pérdida) y P(tocar −12%).
- **Lo que no incluye:** tipo de cambio, stop ni filtro.

## 2. Resultados (temporada de 4 meses; los pesos son sobre 20,000 de papel; la cuenta real de 10,000 es la mitad)
| Prima S&P | Cartera | σ | g 4 meses | MXN esperados | P(−12%) | p10 / p50 / p90 |
|---|---|---|---|---|---|---|
| 0% | A | 14.3% | +1.56% | +312 | 7% | −8.6 / +1.5 / +12.9% |
| 0% | W40 | 24.6% | −0.19% | −39 | 31% | −16.9 / −0.2 / +19.9% |
| 2% | A | 14.3% | +2.13% | +426 | 6% | −8.2 / +2.2 / +13.7% |
| 2% | W40 | 24.6% | +0.81% | +161 | 29% | −16.0 / +0.7 / +21.1% |
| **4%** | **A** | 14.3% | **+2.70%** | **+541** | **5%** | −7.6 / +2.7 / +14.2% |
| **4%** | **W40** | 24.6% | **+1.82%** | **+364** | **27%** | −15.3 / +1.7 / **+22.4%** |
| 6% | A | 14.3% | +3.28% | +656 | 4% | −6.9 / +3.4 / +15.0% |
| 6% | W40 | 24.6% | +2.84% | +568 | 25% | −14.3 / +2.8 / +23.7% |
| 8% | A | 14.3% | +3.86% | +772 | 4% | −6.6 / +3.9 / +15.6% |
| 8% | W40 | 24.6% | +3.87% | +774 | 23% | −13.8 / +3.8 / +24.8% |

Medio Kelly sobre el S&P: L = 0.39 con prima de 2%, 0.78 con 4%, 1.17 con 6% y 1.56 con 8%. **Solo con primas de 8% o más el apalancamiento de W40 (1.48x nocional) queda cerca de medio Kelly.**

## 3. Lectura (en pesos, para el dueño)
1. **Con una prima creíble hoy (~4%, con el 10a en 5.2%), el modo C moderado cuesta unos 180 MXN de crecimiento esperado por temporada sobre 20,000 (unos 90 MXN sobre los 10,000 reales).** A cambio:
   - la probabilidad de tocar −12% sube de **5% a 27%** (con stop, el gestor la estima en ~14%);
   - el mejor 10% de las temporadas pasa de **+14% a +22%**.
   **Es una compra de cola derecha pagada con crecimiento esperado y con más probabilidad de caídas.** Es coherente con un torneo y con la meta del dueño, pero no es "más rendimiento".
2. **El punto de equilibrio está en una prima del S&P de ~8%.** Arriba de eso, W40 crece más que A. Abajo, crece menos.
3. **Con prima cero** (lo que implica el abogado del diablo para este régimen), W40 pierde dinero en expectativa (−39 MXN) y A gana +312, casi todo por los CETES y el efectivo.

## 4. Límites
- Modelo lognormal: subestima las colas reales, que en la historia del 3x son más gruesas (ver la ficha de la serie de la señal y AC-07).
- Sin el filtro ni el stop, que recortan la cola y cuestan algo de rendimiento.
- Sin tipo de cambio: el peso amortigua las caídas en MXN.
- σ y correlaciones fijas; la prima es un supuesto, no un pronóstico.

## 5. Uso
Insumo para el dueño (ver `bitacora/decisiones-pendientes.md`). No cambia la decisión W40, que respeta su mandato, pero le dice con claridad cuánto cuesta en pesos su apetito. "Crecimiento geométrico" ya estaba en Comprendido con comprobación; esta ficha amplía su evidencia con el caso de la cartera real.
