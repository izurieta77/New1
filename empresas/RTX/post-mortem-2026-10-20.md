# Post-mortem · RTX Corporation (RTX) · 3T26 (reportado el 20-oct-2026, antes de la apertura)

> Rutina de cierre, 20-oct-2026. Los pronósticos se registraron el 25-sep en `empresas/RTX/pronosticos.csv`, antes del resultado. Las resoluciones están en `empresas/RTX/resoluciones.csv`. Fase 0.

## 1. Resultado real (fuente primaria)
8-K del 20-oct-2026, anexo 99 ([SEC](https://www.sec.gov/Archives/edgar/data/0000101829/000010182926000030/a2026-10x208xkerexhibit99.htm)).

| Concepto | 3T26 | Comparación |
|---|---|---|
| **Ventas** | **US$24,965 M** (ajustadas iguales) | +11%; +12% orgánico; 3T25: 22,478 |
| Collins | 8,382 | — |
| Pratt & Whitney | 9,231 | — |
| Raytheon | 8,031 | — |
| **UPA ajustada** | **2.26** | 3T25: 1.70 |
| UPA GAAP | 1.89 | — |
| FCF | 2.1 mil M | — |
| Cartera de pedidos | 340 mil M (récord) | — |

- **La UPA ajustada incluye 0.25 por acción de recuperación de costos arancelarios (IEEPA).** Fueron ~0.4 mil M en utilidad de segmento: ~250 M en Collins y ~160 M en P&W. No hubo efecto en ventas. **Sin esa partida, la UPA comparable es ≈ 2.01.**
- **Guía 2026:** ventas ajustadas de 97.0-97.5 mil M (antes 95.0-96.0); UPA ajustada de 7.65-7.75 (antes 7.10-7.25); FCF de 9.0-9.2 mil M (antes 8.50-8.75).
- **Reacción (Yahoo, secundaria):** cerró en 193.34, +0.6% contra 192.11.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ventas | 24,100 (23,300-25,300) | 24,013 | 24,965 | −3.46% | −3.81% | Dentro del 80% |
| UPA ajustada | 1.84 (1.72-2.10) | 1.77 | 2.26 | −18.58% | −21.68% | **Fuera del 80%**. Sin la partida arancelaria (2.01): −8.5%, dentro |
| P(UPA ajustada > 1.77) | 0.72 | — | Sí | — | — | Brier 0.0784 |
| P(ventas > 24,013) | 0.55 | — | Sí | — | — | Brier 0.2025 |

Brier promedio de los binarios: **0.1405**.

## 3. Matriz y lectura
- **UPA: proceso razonable, resultado fuera del rango por una partida única.** La UPA comparable (2.01) habría caído dentro del intervalo, cerca del p90. El sesgo es el mismo que el consenso: los dos quedaron debajo.
  - La ficha (L45) documentaba que RTX superó el consenso de UPA en los últimos 4 trimestres, por 5% a 21%. Nuestro punto estaba solo +4% sobre el consenso: tímido frente a esa historia.
- **Ventas: igual que GE.** Un binario en 0.55 con impulso documentado (cartera, posventa); el resultado superó.
- **Qué se sabía el 25-sep:**
  - la historia de sorpresas (L45);
  - que la Corte Suprema había invalidado los aranceles IEEPA y había reembolsos en curso. GE ya había recibido US$100 M en el 2T.
- **Qué no se podía saber:** cuánto y en qué trimestre se reconocería la recuperación de RTX.
- **Escenario:** guía elevada por tercera vez en el año y cartera récord. Pasa del **base** hacia el **alcista** de la ficha (25%).

## 4. Lecciones (cada una cambia algo concreto)
1. **Recuperaciones arancelarias IEEPA: una partida que se repite en industriales** (GE en el 2T, RTX en el 3T). Checklist de las fichas de industriales e importadores de EUA (PM, PG, TMO esta semana): preguntar si hay reembolsos IEEPA pendientes y ensanchar el p90 de UPA si los hay.
2. **Cuando una emisora supera en UPA de forma sistemática (4 de 4 trimestres, 5-21%), el punto debe ir al menos a la mediana histórica de sorpresa,** no a +4%. Es la misma regla de tasa base, aplicada al punto.
3. **Separar en la tabla la UPA comparable de la reportada** cuando hay partidas únicas. Se puntúa contra la cifra del criterio (2.26), pero el aprendizaje del modelo sale de la comparable (2.01).

No hay errores de hecho. Los binarios son del autor claude, no votos de comité, así que no se actualiza `competencia/calibracion-agentes.csv`.
