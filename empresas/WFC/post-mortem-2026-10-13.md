# Post-mortem · Wells Fargo (WFC) · 3T26 (reportado el 13-oct-2026, antes de la apertura)

> Rutina de Cierre, 13-oct-2026. Los pronósticos se registraron el 25-sep, en `empresas/WFC/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado. Las resoluciones están en `empresas/WFC/resoluciones.csv`. Sin posición en WFC y sin comité: no hay decisión de cartera ni votos de agentes que evaluar, solo pronósticos.

## 1. Resultado real (fuente primaria)
8-K del 13-oct-2026: ex. 99.1 ([comunicado](https://www.sec.gov/Archives/edgar/data/0000072971/000007297126000318/wfc3qer10-13x26ex991xrelea.htm)), ex. 99.2 ([suplemento](https://www.sec.gov/Archives/edgar/data/0000072971/000007297126000318/wfc3qer10-13x26ex992xsuppl.htm)) y ex. 99.3 ([presentación](https://www.sec.gov/Archives/edgar/data/0000072971/000007297126000318/ex993-wellsfargo3q26pres.htm)); las cifras coinciden en los tres:
- **Ingresos totales:** US$21,870 M (+2% a/a, −3% t/t). NII de 12,517 (+5%) y comisiones de 9,353 (−1% a/a, −9% t/t).
- **Utilidad neta:** US$5,951 M; aplicable a comunes 5,703. **UPA diluida (GAAP):** 1.87 (1.66 en el 3T25), con 3,051.5 M de acciones diluidas promedio.
- **Partidas que no se repiten:** US$170 M de beneficios fiscales discretos (≈US$0.056 por acción; tasa efectiva de 16.4%). Sin ellos, la UPA sería ~1.81 (cálculo propio).
- **Por qué cayeron las comisiones (según la empresa):** menores ganancias de trading, menor ingreso por arrendamiento tras la venta del negocio de carros de ferrocarril en el 1T26, menores ganancias de capital de riesgo (VC) y menor ingreso hipotecario. Markets de CIB −1% a/a y −17% t/t.
- **Gasto y crédito:** gasto de 13,743 M (−1%); provisión de 1,029 M; castigos netos de 0.38% (0.34% en el 2T).
- **Capital:** CET1 de **10.0%** (10.3% en el 2T); ROTCE de 16.3%; recompras de US$2.5 mil M (28.6 M de acciones).
- **Guía:** NII 2026 de ±US$50 mil M y gasto de ~55.7 mil M, ambos sin cambio; NII del 4T26 de ~13 mil M.
- **Reacción del precio:** no consultada en fuente verificable al cierre de esta rutina; no se reporta.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro | Consenso | Real | Error nuestro | Error consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos totales (punto; p10-p90) | 22,450 (21,900-23,000) | 22,340 | 21,870 | +2.65% | +2.15% | **Fuera** del intervalo de 80% (30 M abajo del p10) |
| UPA diluida GAAP (punto; p10-p90) | 1.90 (1.74-2.05) | 1.84 | 1.87 | +1.60% | −1.60% | Dentro del intervalo de 80% |
| P(ingresos > 22,340) | 0.57 | — | No | — | — | Brier 0.3249 |
| P(UPA > 1.84) | 0.63 | — | Sí | — | — | Brier 0.1369 |

Error = (pronóstico − real) / real. Brier promedio de los dos binarios: **0.231**. Con la tasa base de FactSet (0.70 ingresos y 0.78 UPA) habría sido 0.49 y 0.0484 (promedio 0.269).

## 3. Matriz y lectura
- **Ingresos: mal supuesto y mal resultado.** El NII salió casi exacto (12,517 contra 12,550). Todo el error está en comisiones: supusimos 9.9 mil M (+4% a/a) y fueron 9,353 (−1%). La venta del negocio de carros de ferrocarril (1T26) **ya estaba en la ficha** (§4.10) y no se restó del supuesto; la normalización del VC se mencionó ("con menos VC que en el 2T"), pero se subestimó. El p10 de 21,900 suponía una banda de ±2.5%, estrecha para una línea de comisiones que bajó 9% t/t.
- **UPA: buen resultado con ayuda de la suerte.** Puente aproximado de 1.90 a 1.87 (cálculo propio): ingresos −0.155; gasto menor +0.03; provisión −0.01; tasa efectiva menor (incluye los 170 M discretos) +0.05; interés minoritario de −14 M contra +170 supuestos +0.06 (en parte ligado a las menores ganancias de VC, que también restaron ingresos); acciones −0.01. El binario "UPA > 1.84" resuelve **Sí** con el criterio GAAP registrado, pero **sin el beneficio fiscal discreto (~1.81) habría sido No**. Es acierto de dirección, no evidencia de habilidad.
- **Qué se sabía el 25-sep:** la venta del negocio de carros, la volatilidad de las ganancias de VC (el 2T26 las tuvo altas), que el CFO esperaba IB y Markets a un dígito medio en el 3T, y que la UPA del 2T26 ya traía 0.04 de impuestos discretos.
- **Qué no se podía saber:** el monto y el trimestre de la resolución fiscal (170 M) ni la caída de Markets contra un 2T fuerte.
- **Escenario:** el disparador bajista era CET1 < 10.0%; salió **exactamente en 10.0%**, así que no se activa, pero queda en el límite. ROTCE de 16.3% (dentro del 16-17% del base), guía de NII y gasto sin cambio, recompras de 2.5 mil M (el base suponía ~3). Sigue el escenario **base, en vigilancia**: un CET1 abajo de 10.0% en el 4T26 lo movería al bajista.

## 4. Lecciones (cada una cambia algo concreto)
1. **Comisiones de bancos por línea, no con un % de crecimiento.** En el próximo pronóstico de WFC, construir las comisiones por componente (asesoría de inversión, depósitos, tarjetas, IB, trading, VC, arrendamiento) y **restar el ingreso de negocios vendidos** que la propia ficha documenta. Se anota para la plantilla de supuestos de `ficha-empresa` (propuesta; la skill no se modifica sin aprobación).
2. **Intervalo de ingresos de WFC más ancho:** pasar de ±2.5% a ±3.5% alrededor del punto (p10-p90), porque las comisiones se movieron −9% t/t y pesan 43% de los ingresos. Con ese ancho, el p10 habría sido ~21,670 y el dato quedaba dentro.
3. **Binarios de UPA GAAP: registrar en la resolución si una partida discreta decidió el resultado.** Aquí el 1.87 incluye ~0.056 de impuestos discretos; sin ellos el binario fallaba. Se deja asentado para que este acierto no cuente como habilidad al calibrar.
4. **Tasa base:** el 0.57 de ingresos le ganó en Brier al 0.70 de FactSet porque el resultado fue "No", y el 0.63 de UPA perdió contra 0.78. Promedio: 0.231 contra 0.269. Con n = 2 no se concluye nada; la regla de partir de la tasa base (`conocimiento/fichas/2026-10-13-pronostico-de-resultados-tasa-base.md`) sigue en pie.

No hay errores de hecho que registrar en `conocimiento/registro-de-errores.md`: las cifras de la ficha eran correctas; el error fue de supuestos (comisiones) y de ancho del intervalo. Los pronósticos se resolvieron en `empresas/WFC/resoluciones.csv`; no se ejecutó `herramientas/pronosticos.py resolver` porque esta rutina no edita `bitacora/pronosticos.csv`.
