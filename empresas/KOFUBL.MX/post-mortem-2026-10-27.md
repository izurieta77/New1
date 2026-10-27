# Post-mortem · Coca-Cola FEMSA (KOFUBL.MX) · 3T26 (reportado el 26-oct-2026; resuelto un día tarde, en el cierre del 27-oct)

> Rutina de cierre, 27-oct-2026. Los pronósticos se registraron el 25-sep en `empresas/KOFUBL.MX/pronosticos.csv` y en la §8 de `ficha.md`, y no se modifican. La resolución estaba fechada el 28-oct y la emisora publicó el **26-oct**. El cierre del 26-oct no la detectó y se encontró hoy por la prensa (fila en el registro de errores). Sin posición: solo hay pronósticos que evaluar.

## 1. Resultado real (fuente primaria)
**Fuente:** 6-K del 26-oct-2026 en SEC EDGAR (CIK 910631, accession 0001292814-26-005006, [kofpr3q26_6k.htm](https://www.sec.gov/Archives/edgar/data/910631/000129281426005006/kofpr3q26_6k.htm)), leído por WebFetch el 27-oct a ~21:55 UTC.
- **Ingresos totales: Ps 79,718 M** (+10.9% contra 71,884). Netos: 79,360 (71,685).
- **Volumen:** +5.3%, a 1,089.8 M de cajas unidad.
- **Utilidad de operación:** Ps 11,874 M (10,291 en el 3T25); **margen de 14.9%** (14.3%). Según la prensa, México y Centroamérica −3.1% y Sudamérica +51.2% (El Cronista, sdpnoticias, B; no verificado por región en el 6-K).
- **Impuestos:** 33.4% sobre la utilidad antes de impuestos (30.9% en el 3T25).
- **UN mayoritaria:** Ps 6,223 M (+5.5%). **UPA: Ps 0.37 por acción** (6,223 / 16,806.7 M = 0.3703, cálculo propio); 2.96 por unidad y 29.62 por ADS.
- **Precio:** KOFUBL.MX cerró en 214.73 el 26-oct (−2.8%) y en 210.44 el 27-oct (−2.0%); −4.7% en dos sesiones (Yahoo 1d).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Puntuación |
|---|---|---|---|---|---|
| Ingresos totales (Ps M) | 75,500 (73,600-77,400) | 75,770 | 79,718 | **−5.29%** | **Fuera del 80%** |
| UPA (Ps por acción) | 0.375 (0.33-0.42) | 0.365 (base ambigua) | 0.3703 | +1.28% | Dentro del 80% |
| P(ingresos > 75,770) | 0.45 | — | Sí | — | Brier 0.3025 |
| P(margen operativo > 14.3%) | 0.62 | — | Sí (14.9%) | — | Brier 0.1444 |

Brier promedio de los binarios: **0.2235**. El binario de ingresos tuvo la dirección equivocada.

## 3. Matriz y lectura
- **Ingresos: mal resultado y proceso con un supuesto débil.** Supuse Sudamérica +9% en MXN y México y Centroamérica +2.5%. El crecimiento total fue de +10.9%, con volumen de +5.3%, así que Sudamérica creció mucho más que el supuesto. [Inferencia] La causa probable es el tipo de cambio de Brasil y Colombia y el volumen, pero no se leyó el desglose por región del 6-K. El intervalo de 80% (±2.5%) era demasiado estrecho para una emisora con más de la mitad de sus ingresos en monedas de Sudamérica.
- **UPA: buen resultado por compensación.** Los ingresos más altos se comieron con una tasa de impuestos más alta (33.4% contra 31%) y un costo financiero que no se verificó. El punto acertó, pero por razones parcialmente equivocadas.
- **Margen: buena dirección.** 0.62 con un supuesto de 14.6%; el real fue de 14.9%.
- **Precio:** −4.7% en dos días con ingresos arriba del consenso. [Inferencia] El mercado castiga la caída de México (−3.1% operativo, según la prensa) más que el crecimiento de Sudamérica.

## 4. Lecciones (cada una cambia algo concreto)
1. **Intervalos de ingresos en emisoras con mucha exposición a monedas de Sudamérica:** el p10-p90 debe incluir el escenario cambiario. Una regla de ±2.5% no basta; usar la desviación histórica de las sorpresas de 8 trimestres.
2. **Tasa efectiva (quinto caso en una semana):** 33.4% contra 31% supuesto. Se suma a la regla del post-mortem de Cemex (mediana de 4 trimestres).
3. **Proceso:** la fecha "no confirmada" del reporte (23-28 oct) debía vigilarse desde el primer día de la ventana. Se agrega la regla en el registro de errores.
