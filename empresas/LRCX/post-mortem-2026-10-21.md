# Post-mortem · Lam Research (LRCX) · 1T FY27 (trimestre al 27-sep-2026; reportado el 21-oct-2026, después del cierre)

> Rutina de cierre, 21-oct-2026 (~21:40 UTC). Los pronósticos se registraron el 25-sep en `empresas/LRCX/pronosticos.csv`, antes del resultado. Las resoluciones están en `empresas/LRCX/resoluciones.csv`. La fecha de Yahoo (21-oct) fue la correcta; Zacks estimaba el 28-oct. Fase 0.

## 1. Resultado real (fuente primaria)
8-K del 21-oct-2026 (ítems 2.02 y 9.01), comunicado Ex. 99.1 ([SEC](https://www.sec.gov/Archives/edgar/data/707549/000070754926000052/lrcx_exhibitx991xq1x2027.htm)).

| Concepto | 1T FY27 (sep-2026) | Comparación |
|---|---|---|
| **Ingresos** | **US$8,219.4 M** | +22% t/t (6,722.2); +55% a/a (5.32 mil M) |
| Sistemas / soporte al cliente | 5.73 mil M / 2.49 mil M | 4T FY26: 4.25 / 2.47 |
| Margen bruto GAAP / non-GAAP | 52.3% / 52.4% | guía 52% ± 1 |
| Margen operativo GAAP / non-GAAP | 40.0% / 40.2% | guía 39.5% ± 1 |
| UPA GAAP diluida | 2.19 | 4T FY26: 1.81 |
| **UPA non-GAAP diluida** | **2.20** | 4T FY26: 1.82; guía 2.15 ± 0.15 |
| China / Corea / Taiwán | 35% / 20% / 18% | FY26: China 34% |
| Flujo operativo | 3.50 mil M | — |

- **Partidas (GAAP → non-GAAP):** amortización de intangibles (3.0 M), revaluación de compensación diferida (14.0 M en gastos, −12.9 M de ganancia en activos), amortización de descuento de notas (0.5 M) y **gasto fiscal de 11.5 M por un cambio en la ley**. Sin cargos de reestructura en el trimestre. Diferencia neta: 1 centavo.
- **Guía del trimestre de diciembre:** ingresos de **US$8.60 ± 0.40 mil M** (consenso de la ficha: 8.51), margen bruto de 52.5% ± 1, margen operativo de 40.5% ± 1 y UPA de **2.33 ± 0.15** (consenso: 2.31), con 1.253 mil M de acciones.
- **Capital:** recompras de ~1.02 mil M (0.25 en el trimestre previo); dividendo trimestral declarado sube a 0.33 (antes 0.26).
- **Reacción (provisional, Yahoo chart, secundaria):** cierre regular de US$260.81; ~US$247.50 a las 21:40 UTC, **−5.1%**. La reacción del día se mide con el cierre del 22-oct.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos | 8,300 (7,980-8,620) | 8,135 | 8,219.4 | +0.98% | −1.03% | Dentro del 80% |
| UPA non-GAAP | 2.33 (2.17-2.46) | 2.179 | 2.20 | +5.91% | −0.95% | Dentro del 80%, a 0.03 del p10 |
| P(ingresos > 8,135) | 0.74 | — | Sí | — | — | Brier 0.0676 |
| P(UPA non-GAAP ≥ 2.18) | 0.87 | — | Sí | — | — | Brier 0.0169 |

Brier promedio de los binarios: **0.0423** (el mejor de la ronda).

## 3. Matriz y lectura
- **Binarios: buen proceso, buen resultado.** La tasa base de superar al consenso funcionó.
- **Puntos: proceso optimista, ambos sobre el real.** La superación de ingresos sobre el punto medio de la guía (8.10) fue de **+1.5%**, debajo del rango histórico (+1.8% a +2.8%); la de UPA, de **+2.3%** sobre 2.15, muy debajo de +5% a +10%. El consenso estuvo más cerca que nosotros en los dos. Con un salto t/t de 22%, la superación porcentual se comprime: el margen operativo superó la guía solo en 0.7 pp.
- **Qué se sabía el 25-sep:** la guía (+20% t/t), el riesgo de aceptaciones en Japón y que la ficha misma marcaba el salto t/t como el riesgo principal.
- **Qué no se podía saber:** el gasto fiscal por cambio de ley (11.5 M) y el tono del mercado.
- **Escenario:** guía de diciembre de 8.60 (no < 8.0) y China en 35% (el disparador bajista era > 35%). Sigue en el **base**. La caída posterior al cierre (−5%) con superación y guía arriba del consenso indica que el precio ya descontaba más; dato para "qué descuenta el precio".

## 4. Lecciones (cada una cambia algo concreto)
1. **La superación histórica se aplica en dólares o se descuenta cuando la guía implica un salto t/t grande.** Regla propuesta para emisoras de equipo con guía > +15% t/t: usar la mitad inferior del rango histórico de superación (+1.8% en ingresos, +5% en UPA) en lugar de la mediana.
2. **Cuando el punto queda lejos del consenso en la misma dirección que el binario, revisar coherencia:** punto de UPA +6.9% sobre el consenso con p = 0.87 era coherente, pero el intervalo (p10 2.17) quedó a 3 centavos del real. Checklist: verificar que el real "decepcionante pero sobre consenso" quede dentro del 80%.
3. **La reacción va aparte:** superar y guiar arriba coincidió con −5.1% después del cierre (provisional). Registrar el cierre del 22-oct en la próxima ficha, sin pronóstico nuevo.

No hay errores de hecho para `conocimiento/registro-de-errores.md`. Los binarios son del orquestador (autor claude), no votos de comité, así que no se actualiza `competencia/calibracion-agentes.csv`.
