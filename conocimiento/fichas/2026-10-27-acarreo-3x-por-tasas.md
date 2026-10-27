# Ficha · Crecimiento geométrico de un 3x diario con acarreo y brecha real, por nivel de tasas (27-oct-2026)

**Pregunta:** ¿cuánto crece al año un 3x diario del S&P 500 contra el índice, según la tasa corta, una vez que se suman el acarreo (financiamiento del 2x adicional y la comisión) y la brecha real que medimos en R20? ¿Con qué rendimiento esperado del índice empata el 3x al 1x con las tasas de hoy?

## Fuente y nivel de acceso
- **Derivación:** cap. 01 §crecimiento geométrico (G ≈ A − σ²/2) y cap. 07 §2.1. Ficha previa `2026-09-29-volatility-drag.md` (L* = 2.68 con tasas cercanas a cero).
- **Brecha real:** R20 lado A (`laboratorio/replicas/R20-brecha-upro-sintetico-tasas.md`, 27-oct): −1.59 pp por año en total; −1.31 con DTB3 < 0.5%, −1.54 con 0.5-3% y **−2.30 con ≥ 3%**. El lado B está en curso.
- **Externo:** Bianchi y Goldberg (arXiv:2604.27287, lectura íntegra el 26-oct, grado C). Su "anomalía" de 2022-23 es en ≈51% acarreo omitido (adenda del 26-oct en el cap. 07).

## Supuestos y derivación
- Rebalanceo diario exacto, rendimientos log-normales y aproximación continua:
  **G(L) ≈ L·μ − (L−1)·r − c − b − L²σ²/2**
  - μ y σ: media aritmética y volatilidad anuales del índice total return;
  - r: tasa corta;
  - c: comisión (0.91%);
  - b: brecha real contra el sintético (R20).
- **Sin brecha, L\* = (μ − r)/σ².** La tasa no solo resta (L−1)·r: también **baja el apalancamiento óptimo**.
- **Supuestos ilustrativos** (no son pronóstico): μ = 8% y σ = 17%.

## Ejercicio comprobado (`fichas/codigo/2026-10-27-acarreo-3x-por-tasas.py`)
| r | G(1x) | G(3x), b = 0 | G(3x), b = 1.3 | G(3x), b = 2.3 | L\* | 3x − 1x con b = 2.3 |
|---|---|---|---|---|---|---|
| 0.1% | 6.55% | 9.88% | 8.58% | 7.58% | 2.73 | **+1.03 pp** |
| 2.0% | 6.55% | 6.08% | 4.78% | 3.78% | 2.08 | **−2.77 pp** |
| 3.8% (hoy) | 6.55% | 2.48% | 1.18% | 0.18% | 1.45 | **−6.37 pp** |

- **Segunda comprobación:** Monte Carlo diario con 400 años × 2 (variables antitéticas). Coincide con la fórmula cerrada en ±0.02 pp en las 12 celdas.
- **Empate 3x = 1x con r = 3.8%, b = 2.3% y σ = 17%:** hace falta **μ ≈ 11.2%** aritmético anual del índice total return.

## Evidencia empírica y límites
- **R20-A, por año:** la brecha real fue de −2.22 (2024), −2.89 (2025) y −2.26 (2026 a la fecha), contra −0.19 a −1.35 en 2009-2013. Es la más grande de la muestra justo en el régimen de tasas actual.
- **Lo que la tabla no incluye:**
  - **el filtro SMA200/VIX de la cartera** (R06), que reduce la exposición en las caídas. Por eso G(3x) con filtro no se lee de esta tabla;
  - μ y σ variables en el tiempo. Con σ = 12% (calma), el empate baja a μ ≈ 8.3% [misma fórmula: ((2·3.8 + 0.91 + 2.3) + 8·0.0144/2·100)/2 = 8.29]. **La volatilidad pesa tanto como la tasa.**
- **M3 de R20:** la pendiente de la brecha sobre la tasa es −0.2 con t = −1.39, **no significativa**. La brecha mayor con tasas altas puede ser de periodo (2018-2026) y no de la tasa misma. No se afirma una relación causal.

## Contraejemplo
- **2010-2013:** tasas en cero, μ realizado alto y σ baja. El 3x real superó con holgura al índice pese a la brecha: con r ≈ 0 y b ≈ 1.3, la tabla da +1 a +3 pp a favor.
- **El signo depende de μ − r**, no del apalancamiento por sí solo. La tabla no dice "el 3x siempre pierde": dice que **con r = 3.8% el umbral de μ es alto**.

## Qué cambia
- **Ninguna regla ni parámetro.** El tamaño del UPRO lo decide el comité (W43 B1 lo bajó a 1 título).
- **Insumo para el comité W44:**
  - con las tasas de hoy, el 3x necesita μ ≳ 11% para empatar al 1x antes del filtro;
  - los backtests sintéticos (R16, R18) sobrestiman al UPRO en ~2.3 pp por año en este régimen.

## Estado nuevo
**Crecimiento geométrico y matemática del compuesto:** se mantiene en *Comprendido con comprobación* mientras falte el lado B de R20. Si B concuerda, sube a **Contrastado**: tiene fórmula comprobada, la brecha medida contra datos reales y el contraste externo de Bianchi-Goldberg y R11-B.
