# Post-mortem · La Comer (LACOMERUBC.MX) · 3T26 (entregado a la BMV el 20-oct-2026)

> Rutina de cierre, 23-oct-2026 (~21:45 UTC). Los pronósticos se registraron el 25-sep en `empresas/LACOMERUBC.MX/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado, y no se modifican. Las resoluciones están en `empresas/LACOMERUBC.MX/resoluciones.csv`. Sin posición: no hay decisión de cartera ni votos del comité que evaluar, solo pronósticos. No se ejecutó `herramientas/pronosticos.py resolver` ni se tocaron `bitacora/pronosticos.csv` ni `competencia/calibracion-agentes.csv`.

## 1. Resultado real (fuente primaria)
**Fuente:** reporte trimestral 3T26 (IFRS, XBRL) entregado por La Comer a la BMV: [ifrsxbrl_1596544_2026-03_1.zip](https://www.bmv.com.mx/docs-pub/ifrsxbrl/ifrsxbrl_1596544_2026-03_1.zip) (sha256 `d6ce2ab4…`; archivo interno fechado 20-oct-2026 17:46), listado en [información financiera de LACOMER-32096](https://www.bmv.com.mx/es/emisoras/informacionfinanciera/LACOMER-32096-CGEN_CAPIT). El comentario de la administración del XBRL está fechado "Ciudad de México a 20 de octubre de 2026" y da los puntos relevantes del trimestre. No se identificó un evento relevante de resultados en la lista de [eventos de LACOMER-32096](https://www.bmv.com.mx/es/emisoras/eventosrelevantes/LACOMER-32096-CGEN_CAPIT), y no se buscó el PDF en el sitio de RI; se usa el XBRL, que es la presentación oficial a la BMV.

Cifras del 3T26 (Ps M; XBRL, periodo 2026-07-01 a 2026-09-30):
- **Ingresos (`Revenue`): 12,360.8** (+4.6% a/a contra 11,813.2). Comentario de la administración: "ventas totales +4.6% y ventas mismas tiendas +1.0%".
- Utilidad bruta: 3,683.0 (**margen de 29.8%**; 29.7% en el 3T25, cálculo propio).
- Gastos de venta: 2,571.9 (+11.0%). Gastos de administración: 419.6 (+9.6%). **Total: 2,991.5 (+10.8% a/a, cálculo propio).** Otros ingresos: 32.5.
- Utilidad de operación: 723.2 (−13.8%). **Margen EBITDA: 9.2%** (dato del comentario).
- Ingresos financieros: 35.8; costos financieros: 84.5. Utilidad antes de impuestos: 674.5. Impuestos: 166.9. **Tasa efectiva: 24.7%** (21.6% en el 3T25; cálculo propio: 166.859 / 674.468 y 176.103 / 816.980).
- **Utilidad neta: 507.6** (−20.8%; sin minoritario). **Margen neto: 4.1%** (5.4% en el 3T25).
- **UPA básica (XBRL `BasicEarningsLossPerShare`): Ps 0.47** (0.59 en el 3T25). Comprobación: 507.609 / 1,086 M UBC = 0.467 (cálculo propio). La utilidad básica es igual a la diluida (nota de UPA del XBRL).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos 3T26 | 12,400 (12,080-12,720) | 12,710 | 12,361 | +0.32% | +2.82% | Dentro del 80% |
| UPA 3T26 | 0.52 (0.43-0.61) | 0.56 | 0.47 | +10.64% | +19.15% | Dentro del 80% |
| P(ingresos > 12,710) | 0.10 | — | No | — | — | Brier 0.0100 |
| P(UPA > 0.56) | 0.30 | — | No | — | — | Brier 0.0900 |

Brier promedio de los binarios: **0.0500**. Los dos puntos fueron mejores que el consenso.

## 3. Matriz y lectura
- **Ingresos: buen proceso, buen resultado.** El supuesto de ventas mismas tiendas (~+2%, por ANTAD débil en julio-agosto) quedó arriba del real (+1.0%), pero el área nueva aportó más de los ~3 pp supuestos (+3.6 pp implícitos, cálculo propio). El sesgo contra el consenso (que sobreestimó el 2T26 en 2.8% y ahora en 2.8%) fue correcto y estaba fundamentado en ANTAD.
- **UPA: dirección correcta, magnitud corta.** El margen neto fue de 4.1% contra 4.5% supuesto. La causa principal fue el gasto: +10.8% a/a contra ventas de +4.6% (desapalancamiento operativo por aperturas y Sumesa). La tasa efectiva subió a 24.7% (contra 21.6% un año antes) y el resultado financiero neto empeoró (ingresos financieros de 35.8 contra 54.7). El intervalo amplio (±17%) capturó el resultado.
- **Binarios (0.10 y 0.30): buenas decisiones, buen resultado.** Ambos apostaron contra el consenso con un mecanismo nombrado (ANTAD y margen neto en caída) que se cumplió.
- **Qué se sabía el 25-sep:** ANTAD de julio y agosto, la caída del margen neto del 2T26 (−140 pb) y los gastos de Sumesa.
- **Qué no se podía saber:** la magnitud del gasto del trimestre y la tasa efectiva.
- **Escenario (§7):** las ventas mismas tiendas (+1.0%) tocan el umbral bajista (≤1%) y el gasto de venta (+11.0%) supera con mucho el umbral de 6%. Las dos señales de la §7 apuntan al **bajista**. El margen EBITDA de 9.2% ya queda debajo de 9.5%, el umbral bajista definido para 2027. Se anota en la adenda sin cambiar las probabilidades hasta la revisión de la ficha.

## 4. Lecciones (cada una cambia algo concreto)
1. **Modelar el gasto por separado de la venta en las emisoras en expansión.** El supuesto de "margen neto de ~4.5%" escondía el gasto. Checklist de la §8 para minoristas: anotar el crecimiento del gasto de venta de los últimos 4 trimestres y la tienda nueva contra mismas tiendas.
2. **Tasa efectiva:** anotar la tasa de los últimos 4 trimestres (aquí subió; en GRUMA, BOLSA y AMX bajó). La regla de usar la mediana aplica en ambos sentidos.
3. **ANTAD como señal adelantada funcionó.** Mantenerla en el checklist de los minoristas (ya está implícita; hacerla explícita en la §8).

No hay errores de hecho que registrar en `conocimiento/registro-de-errores.md`.
