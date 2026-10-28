# Post-mortem · Walmart de México (WALMEX.MX) · 3T26 (reportado el 27-oct-2026; resuelto un día tarde, en el cierre del 28-oct)

> Rutina de cierre, 28-oct-2026. Los pronósticos del 25-sep (`pronosticos.csv`, §8 de la ficha) no se modifican. La fecha de resolución era el 28-oct; Walmex publicó el **27-oct** y el cierre de ese día no lo detectó (registro de errores). Sin posición.

## 1. Resultado real (comunicado en inglés, [Walmex 3Q26 Earnings Release](https://files.walmex.mx/upload/files/2026/EN/Quarterly/3Q26/Walmex%203Q26%20Earnings%20Release.pdf), PDF íntegro, 8 pp., fechado el 27-oct; sha256 `6c6e1593…`)
- **Ingresos totales: Ps 248,828 M (+3.0%).** México 206,759 (+3.1%); Centroamérica 42,069 (+2.7%; +6.0% sin tipo de cambio).
- **Utilidad de operación:** 18,683 (−1.8%; margen de 7.5%, −40 pb). EBITDA de 25,372 (+0.4%).
- **Impuestos: 5,229 (+14.2%)**, una **tasa efectiva de 32.2%** (5,229 / 16,256, cálculo propio).
- **Utilidad neta: 11,027 (−6.1%). UPA: Ps 0.642** (0.678 en el 3T25).
- **Precio:** 48.83 el 27-oct (−3.0%) y 48.40 el 28-oct (−0.9%).
- **Contraste secundario:** Vepormas (27-oct, B) da las mismas cifras.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Puntuación |
|---|---|---|---|---|---|
| Ingresos (Ps M) | 246,000 (242,000-250,000) | 250,630 | 248,828 | −1.14% | Dentro |
| UPA (Ps) | 0.715 (0.650-0.765) | 0.727 | 0.642 | **+11.4%** | **Fuera (bajo el p10)** |
| P(ingresos > 250,630) | 0.10 | — | No | — | Brier 0.01 |
| P(UPA > 0.727) | 0.38 | — | No | — | Brier 0.1444 |

## 3. Lectura y lecciones
- **Ingresos:** buen proceso y buen resultado. El binario agresivo (0.10) acertó: el consenso volvió a quedar arriba del real (4 de 6 trimestres).
- **UPA: el error es casi todo la tasa de impuestos.** Supuse 24.5% y fue 32.2%. Con 24.5% sobre la utilidad antes de impuestos real (16,256) y 17,176 M acciones, la UPA habría sido **0.7146**, igual a nuestro punto (0.715). **La parte operativa del modelo estuvo bien; la tasa la hundió.**
- **Lección (sexto caso de tasa efectiva en una semana: AMX, BOLSA, Cemex, Visa, KOF y Walmex):** la tasa supuesta sale de la mediana de 4 trimestres y se anota junto al punto. Además, cuando la tasa salta, el intervalo de la UPA debe abrirse por la tasa. Se propone volverlo regla de la plantilla de §8 (`decisiones-pendientes.md`).
