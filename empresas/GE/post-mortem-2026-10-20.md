# Post-mortem · GE Aerospace (GE) · 3T26 (reportado el 20-oct-2026, antes de la apertura)

> Rutina de cierre, 20-oct-2026. Los pronósticos se registraron el 25-sep en `empresas/GE/pronosticos.csv`, antes del resultado. Las resoluciones están en `empresas/GE/resoluciones.csv`. Fase 0.

## 1. Resultado real (fuente primaria)
8-K del 20-oct-2026, comunicado ([SEC](https://www.sec.gov/Archives/edgar/data/0000040545/000004054526000063/ge3q2026earningsrelease.htm)).

| Concepto | 3T26 | Comparación |
|---|---|---|
| Ingreso total GAAP | US$14,118 M | +16% |
| **Ingreso ajustado** | **13,285 M** | +18%; 3T25: 11,305 |
| CES (Commercial Engines & Services) | ingreso 10,342; utilidad 2,887 | — |
| DPT (Defense & Propulsion Technologies) | ingreso 3,469; utilidad 475 | — |
| Utilidad ajustada | 2,988 | — |
| **UPA ajustada** | **2.25** | +36%; 3T25: 1.66 |
| UPA GAAP continua | 2.32 | — |
| Órdenes | 19.0 mil M | +49% |
| FCF | 2,042 M | −14% |

- **Guía 2026:** UPA ajustada de 8.00-8.10 (antes 7.65-7.85); ingreso ajustado ~19-20% (antes "high teens"); FCF de 9.1-9.4 mil M (antes 8.9-9.2).
- **Reacción (Yahoo, secundaria):** abrió en 302.23 y cerró en 299.87, **−3.7%** contra 311.28 del 19-oct. La causa no está verificada. La caída del FCF (−14%) es una candidata.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingreso ajustado | 12,850 (12,350-13,800) | 12,829 | 13,285 | −3.27% | −3.43% | Dentro del 80% |
| UPA ajustada | 2.06 (1.92-2.32) | 1.99 | 2.25 | −8.44% | −11.56% | Dentro del 80%, a 0.07 del p90 |
| P(ingreso ajustado > 12,829) | 0.53 | — | Sí | — | — | Brier 0.2209 |
| P(UPA ajustada > 1.99) | 0.70 | — | Sí | — | — | Brier 0.0900 |

Brier promedio de los binarios: **0.1555**.

## 3. Matriz y lectura
- **UPA: buen proceso, buen resultado.** El punto estuvo más cerca que el consenso (−8.4% contra −11.6%) y el binario en 0.70 era coherente con la historia de sorpresas. El real quedó en la parte alta del intervalo.
- **Ingreso: proceso tímido.** El 0.53 estaba casi en 50/50, cuando la ficha documentaba entregas de LEAP +24% y servicios de taller +25% en el 2T. El punto quedó debajo, igual que el consenso.
- **Qué se sabía el 25-sep:**
  - el impulso de servicios y entregas (§1 de la ficha, L14);
  - la guía ya elevada en julio;
  - el reembolso arancelario del 2T (US$100 M, L51).
- **Qué no se podía saber:** la magnitud del salto de órdenes (+49%) y la caída del FCF.
- **Escenario:** servicios con crecimiento de doble dígito y guía elevada otra vez. Sigue en el **base/alcista**. La caída del precio con resultados arriba confirma que el precio ya descontaba mucho (DCF inverso de la ficha: 12.9% anual por 10 años).

## 4. Lecciones (cada una cambia algo concreto)
1. **En las emisoras con impulso documentado (entregas y servicios > 20%), los binarios de ingreso deben partir de la tasa base de "supera al consenso" (~0.70), no de 0.53.** Es el mismo patrón que JNJ, GS y MU. Se suma a la regla propuesta de partir de la tasa base.
2. **Registrar el FCF y su variación como pronóstico** cuando el precio descuenta crecimiento alto. Superar en UPA no basta si el flujo decepciona (aquí −14%). Checklist de la próxima ficha de GE: agregar un pronóstico de FCF trimestral.
3. **La reacción va aparte:** superar y subir la guía coincidió con −3.7%. Es dato para "qué descuenta el precio", sin pronóstico nuevo.

No hay errores de hecho para `conocimiento/registro-de-errores.md`. Los binarios son del orquestador (autor claude), no votos de comité, así que no se actualiza `competencia/calibracion-agentes.csv`.
