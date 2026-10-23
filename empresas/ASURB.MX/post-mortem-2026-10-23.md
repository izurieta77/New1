# Post-mortem · Grupo Aeroportuario del Sureste (ASURB.MX) · 3T26 (reportado el 22-oct-2026)

> Rutina de cierre, 23-oct-2026 (~21:45 UTC). Los pronósticos se registraron el 25-sep en `empresas/ASURB.MX/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado, y no se modifican. Las resoluciones están en `empresas/ASURB.MX/resoluciones.csv`. Sin posición: no hay decisión de cartera ni votos del comité que evaluar, solo pronósticos. No se ejecutó `herramientas/pronosticos.py resolver` ni se tocaron `bitacora/pronosticos.csv` ni `competencia/calibracion-agentes.csv`.

## 1. Resultado real (fuente primaria)
**Fuente:** BMV, evento relevante del 22-10-2026 a las 14:30, "ASUR ANUNCIA RESULTADOS 3T26" (español): [eventemi_1597192_1.pdf](https://www.bmv.com.mx/docs-pub/eventemi/eventemi_1597192_1.pdf) (38 pp., sha256 `8455bccc…`), listado en [eventos relevantes de ASUR-6001](https://www.bmv.com.mx/es/emisoras/eventosrelevantes/ASUR-6001-CGEN_CAPIT). Cotejado con:
- el XBRL IFRS del trimestre entregado a la BMV el 22-oct a las 14:32: [ifrsxbrl_1597194_2026-03_1.zip](https://www.bmv.com.mx/docs-pub/ifrsxbrl/ifrsxbrl_1597194_2026-03_1.zip) (sha256 `5776b155…`; `Revenue` 3T26 = 10,420,538 miles; `ProfitLossAttributableToOwnersOfParent` = 2,158,798 miles; `Basic/DilutedEarningsLossPerShare` = 7.196);
- el comunicado completo en inglés del sitio de RI ([Earnings-Release-3Q26.pdf](https://www.asur.com.mx/media/Informes%20Financieros/2026/3/ASUR-Airport-Cancun-Mexico-Earnings-Release-3Q26.pdf), 33 pp., sha256 `c913f9d6…`);
- y el 6-K ante la SEC ([ex-99.1](https://www.sec.gov/Archives/edgar/data/1123452/000110465926118175/tm2628145d1_ex99-1.htm), versión resumida).

Las cuatro fuentes dan las mismas cifras.

Estado de resultados 3T26 (Ps miles en el comunicado; aquí en Ps M):
- **Ingresos totales: 10,420.5** (+18.9% a/a contra 8,765.5).
  - Sin construcción: 7,829.4 (+12.6%). Construcción (IFRIC 12): 2,591.1 (+43.0%).
  - Por región: México 6,679.8 (sin construcción 4,518.8, −6.8%), San Juan 1,270.9, Colombia 1,172.2 (incluye 137.3 de construcción), EUA 456.4 y Brasil y otros (solo septiembre) 841.2 (sin construcción 676.4).
- Pasajeros: −1.2% total; México −4.6% (internacional −11.8%, nacional +1.6%).
- EBITDA: 4,719.3 (+1.7%). Margen EBITDA ajustado: **60.3%** (66.7% un año antes). Utilidad de operación: 3,889.8, así que D&A ≈ 829.5 (cálculo propio).
- RIF: −718.7. Se compone de pérdida cambiaria de −803.5, ganancia realizada de +719.2 en tres *forwards* de cobertura, intereses pagados de −871.7 e intereses ganados de +237.3.
- Utilidad antes de impuestos: 3,215.5. Impuestos: 907.6 (corriente 863.6 y diferido 44.0). **Tasa efectiva: 28.2%** (31.3% en el 3T25; cálculo propio con el estado de resultados).
- Minoritario: 149.1. **Utilidad neta mayoritaria: 2,158.8 M** (+2.1%).
- **UPA: Ps 7.1960** (7.0486 en el 3T25). Es la mayoritaria entre ~300.0 M acciones (cálculo propio: 2,158.8 / 7.196). El XBRL da la misma cifra (7.196), así que aquí no hay ambigüedad con el minoritario.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos totales 3T26 (con construcción y CPC) | 9,450 (8,300-10,700) | 9,140 | 10,420.5 | −9.31% | −12.29% | Dentro del 80% |
| UPA 3T26 (mayoritaria, Ps) | 6.60 (5.30-8.00) | 7.94 | 7.1960 | −8.28% | +10.34% | Dentro del 80% |
| P(ingresos > 9,140) | 0.58 | — | Sí | — | — | Brier 0.1764 |
| P(UPA > 7.94) | 0.12 | — | No | — | — | Brier 0.0144 |

Brier promedio de los binarios: **0.0954**. En ingresos, el punto fue mejor que el consenso; en UPA, el error absoluto fue menor que el del consenso (8.3% contra 10.3%), pero el sesgo fue el opuesto.

## 3. Matriz y lectura
- **Ingresos: buen proceso, buen resultado, y el error se explica casi todo por construcción.**
  - Supuestos contra real: orgánico sin construcción ~6,500 contra 6,696.6 (México + San Juan + Colombia, cálculo propio); EUA ~440 contra 456.4; CPC en septiembre ~700 contra 676.4; construcción ~1,800 contra **2,591.1**.
  - Construcción explica ~790 de los ~970 M de error. Cayó dentro de nuestro rango (700-3,200), pero arriba del punto. El orgánico explica ~200 M: el peso y Colombia salieron algo mejor de lo supuesto.
  - Sin construcción, el error habría sido ~−2.4% (7,640 contra 7,829; cálculo propio).
  - Lección: la línea de construcción (IFRIC 12) es ruido de capex, no de operación. Pesa mucho en el punto de "ingresos totales" y no se puede predecir con la información operativa.
- **UPA: buen resultado dentro del intervalo, con dos supuestos rotos a favor.**
  - EBITDA: 4,719 contra ~4,600.
  - D&A: 830 contra ~880.
  - RIF: −719 contra −830. Los *forwards* de +719 compensaron casi toda la pérdida cambiaria; esa ganancia no estaba en el modelo.
  - Tasa: 28.2% contra 30%.
  - Minoritario: 149 contra ~100, que va en contra.
  - El punto apostó por una caída más fuerte que el consenso. El signo del binario de UPA (p = 0.12 de superar 7.94) fue correcto, pero el punto quedó del lado bajo.
  - Inferencia: sin los *forwards* (≈ +0.7 mil M antes de impuestos), la UPA habría salido cerca de Ps 5.5-5.6, más cerca de nuestro punto que del consenso. Lo que movió el resultado fue una cobertura cambiaria que la ficha no conocía. Fue **suerte**, no proceso.
- **Binarios.** Ingresos > 9,140 con p = 0.58: buena decisión y buen resultado, aunque con poca convicción; con el punto en 9,450 y un intervalo sesgado, la probabilidad pudo ser ~0.62-0.65. UPA > 7.94 con p = 0.12: buena decisión y buen resultado.
- **Qué se sabía el 25-sep:** el tráfico de julio y agosto, el cierre de CPC el 1-sep y la deuda puente de Motiva. Las coberturas cambiarias pudieron intuirse por la deuda nueva en MXN y USD, pero no se revelaron antes.
- **Qué no se podía saber:** el monto de construcción del trimestre, los *forwards* (se revelaron con el reporte) y la tasa efectiva.
- **Escenario (§7):** el margen EBITDA ajustado de 60.3% queda entre los umbrales (≤ 60% bajista, ≥ 64% alcista), pegado al bajista. El tráfico internacional de México del trimestre fue de −11.8%, cerca del umbral bajista de Cancún (≤ −12%; el umbral se mide con sep-nov y no con el trimestre). Lectura (inferencia): señal inclinada al bajista. Se anota en la adenda sin cambiar las probabilidades.

## 4. Lecciones (cada una cambia algo concreto)
1. **Pronosticar ingresos sin construcción como variable principal en aeropuertos.** Checklist de la §8 para ASUR, OMA y GAP: registrar un pronóstico de ingresos sin construcción (o los dos), porque la construcción IFRIC 12 domina el error del total (aquí 80% del error).
2. **Coberturas cambiarias en el RIF.** Antes de fijar el RIF, revisar en el último 20-F o 6-K si hay *forwards* o derivados vigentes, sobre todo cuando hubo deuda nueva en otra moneda. El modelo de UPA debe separar la pérdida cambiaria de la cobertura.
3. **Tasa efectiva:** 28.2% contra 30% supuesto. Es el tercer caso esta semana (AMX, BOLSA y ahora ASUR) en que la tasa supuesta quedó arriba de la real. Regla propuesta: usar la mediana de la tasa de los últimos 4 trimestres en lugar de una tasa redonda.

No hay errores de hecho que registrar en `conocimiento/registro-de-errores.md`: las cifras del 3T25 de la ficha coinciden con la columna comparativa del comunicado (ingresos de 8,765.5 y UPA de 7.0486).
