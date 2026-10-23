# Post-mortem · Gruma (GRUMAB.MX) · 3T26 (entregado a la BMV el 21-oct-2026)

> Rutina de cierre, 23-oct-2026 (~21:45 UTC). Los pronósticos se registraron el 25-sep en `empresas/GRUMAB.MX/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado, y no se modifican. Las resoluciones están en `empresas/GRUMAB.MX/resoluciones.csv`. Sin posición: no hay decisión de cartera ni votos del comité que evaluar, solo pronósticos. No se ejecutó `herramientas/pronosticos.py resolver` ni se tocaron `bitacora/pronosticos.csv` ni `competencia/calibracion-agentes.csv`.

## 1. Resultado real (fuente primaria)
**Fuente:** reporte trimestral 3T26 (IFRS, XBRL, en dólares) entregado por Gruma a la BMV: [ifrsxbrl_1596817_2026-03_1.zip](https://www.bmv.com.mx/docs-pub/ifrsxbrl/ifrsxbrl_1596817_2026-03_1.zip) (sha256 `42bcd51e…`; archivo interno fechado 21-oct-2026 14:00), listado en [información financiera de GRUMA-5454](https://www.bmv.com.mx/es/emisoras/informacionfinanciera/GRUMA-5454-CGEN_CAPIT) junto con la constancia trimestral [constrim_1596821_2026-03_1.pdf](https://www.bmv.com.mx/docs-pub/constrim/constrim_1596821_2026-03_1.pdf). El bloque de resultados del XBRL reproduce el comunicado (consolidado y por subsidiaria; llamada el 22-oct). No hubo evento relevante de resultados en Emisnet (el último evento de GRUMA-5454 es de feb-2026). No se localizó el PDF en gruma.com (la ruta de reportes trimestrales probada da 404).

Cifras del 3T26 (US$ M; XBRL, periodo 2026-07-01 a 2026-09-30):
- **Ventas netas: 1,650.6** (+1% a/a contra 1,635.6). Volumen de 1,072 kt (−2%). El alza vino del peso fuerte y de la mezcla.
  - EUA: 838.1 (−4%; volumen −4% a 372 kt; margen UAFIRDA ajustado de 17.9% contra 21.1%).
  - GIMSA: 465.3 (−1%; volumen −2% por programas de gobierno).
  - Europa: 135.0 (estable; volumen −6%).
  - Asia y Oceanía: 79.9 (+10%).
  - Centroamérica: 107.9 (+6%; UAFIRDA +47% con una ganancia extraordinaria por seguro).
- Costo de ventas: 61.0% de las ventas (60.7%). SG&A: 26.3% (25.5%). Utilidad de operación: 218.6 (−5%). **UAFIRDA ajustado: 280.3 (margen de 17.0%, contra 17.9%).**
- Costo financiero neto: 30.2. Utilidad antes de impuestos: 188.5. Impuestos: 56.8. **Tasa efectiva: 30.1%** (33.2% en el 3T25; dato del reporte, coincide con 56.813 / 188.461).
- **Utilidad neta mayoritaria: 131.6** (−1%; minoritario de 0.014). **UPA básica y diluida (XBRL `DilutedEarningsLossPerShare`): US$0.39** (0.38 en el 3T25). Acciones implícitas: ~337.5 M (131.634 / 0.39, cálculo propio y aproximado por el redondeo).
- **Nota de definición:** el pronóstico se registró en USD convertidos desde el consenso en pesos (TC 17.22). El criterio literal es la "UPA diluida del reporte BMV 3T26 (USD, dos decimales)". El XBRL reporta en dólares, así que no hace falta conversión: **0.39**. Aquí el minoritario es casi nulo, así que no hay ambigüedad entre utilidad consolidada y controladora.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ventas 3T26 (US$ M) | 1,655 (1,615-1,695) | 1,665 | 1,650.6 | +0.27% | +0.87% | Dentro del 80% |
| UPA 3T26 (US$) | 0.36 (0.32-0.40) | 0.373 | 0.39 | −7.69% | −4.36% | Dentro del 80% |
| P(ventas > 1,665) | 0.38 | — | No | — | — | Brier 0.1444 |
| P(UPA ≥ 0.38) | 0.25 | — | Sí | — | — | Brier 0.5625 |

Brier promedio de los binarios: **0.3535**. El punto de ventas fue mejor que el consenso; el de UPA fue peor.

## 3. Matriz y lectura
- **Ventas: buen proceso, buen resultado.** El total casi exacto oculta errores que se compensaron: EUA quedó 10 M abajo del supuesto (−4% contra −3%), GIMSA 10 M abajo (−1% contra +5% en USD: el peso fuerte no compensó el menor volumen de programas de gobierno) y Europa 7 M abajo. El sesgo bajo el consenso fue correcto.
- **UPA: buen intervalo, punto sesgado a la baja.** El margen UAFIRDA (17.0%) se acertó exactamente. Los errores vinieron de abajo de la línea operativa: tasa de 30.1% contra 33% supuesta, costo financiero de 30 contra 33 y ~337 M acciones contra ~334. Con la tasa del 33% la UPA habría sido ~0.38 (inferencia: 188.5 × 0.67 / 334). Además, el punto se bajó adrede porque "el consenso quedó arriba del real en los últimos 3 trimestres"; esta vez el consenso fue más preciso.
- **Binario de UPA (p = 0.25, resultó Sí): mala decisión parcial, no solo mala suerte.** Con un punto de 0.36 y un intervalo de 0.32-0.40, la probabilidad implícita de ≥0.38 rondaba 0.3; con el consenso en 0.373, 0.25 era una apuesta fuerte contra el consenso sobre la base de un sesgo histórico de tres trimestres. Una parte es suerte (la tasa efectiva y el seguro de Centroamérica), pero la confianza fue excesiva.
- **Binario de ventas (0.38, resultó No): buena decisión, buen resultado.**
- **Qué se sabía el 25-sep:** la debilidad del canal institucional de EUA, el peso fuerte y la tasa efectiva histórica (33.2% en el 3T25).
- **Qué no se podía saber:** la ganancia por seguro en Centroamérica (~9 M en otros ingresos) y la tasa del trimestre.
- **Escenario (§7):** el volumen de EUA (−4%) toca el umbral bajista (≤−4%) y el margen UAFIRDA de EUA (17.9%) queda debajo de 19%. Las dos señales de la §7 apuntan al **bajista**, aunque el consolidado se sostiene por el resto de las regiones. Se anota en la adenda sin cambiar las probabilidades hasta la revisión de la ficha.

## 4. Lecciones (cada una cambia algo concreto)
1. **Tasa efectiva:** anotar la tasa de los últimos 4 trimestres junto al supuesto. Tercer caso en tres días (AMX el 21-oct, BOLSA el 22-oct y GRUMA hoy), siempre con la tasa real abajo del supuesto. Propuesta para el checklist de la §8: usar la mediana de los últimos 4 trimestres salvo una razón explícita.
2. **No convertir un sesgo histórico del consenso en un punto bajo sin un mecanismo.** "El consenso quedó arriba 3 trimestres" no basta. Regla: si el punto se aparta del consenso más de 3%, nombrar la partida que lo explica (margen, tasa o costo financiero).
3. **Binarios contra consenso:** la probabilidad debe salir de la distribución registrada (punto e intervalo), no fijarse aparte. Aquí la distribución daba ~0.3 y se registró 0.25.
4. **GIMSA en USD:** el supuesto de +5% en dólares "por el tipo de cambio" ignoró el volumen de los programas de gobierno. Checklist: separar el volumen y el tipo de cambio en las subsidiarias en pesos.

No hay errores de hecho que registrar en `conocimiento/registro-de-errores.md`.
