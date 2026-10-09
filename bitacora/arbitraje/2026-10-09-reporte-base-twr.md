# Arbitraje · 2026-10-09 · El reporte del portafolio sigue midiendo contra la primera fila (residuo del fallo base-twr)

Origen: hallazgo 1.2 de `bitacora/revisiones/2026-10-08.md`; brief del 8-oct, L32 ("Papel GBM … +3.01% del periodo vs benchmark +1.77%").

## Posiciones
- **Brief del cierre del 8-oct (salida de `portafolio.py reporte`):** papel +3.01% y benchmark +1.77%.
- **Revisor:** según el fallo `2026-10-08-base-twr.md`, el papel lleva +2.53% (índice 102.53).

## Fuente primaria
- Fallo `bitacora/arbitraje/2026-10-08-base-twr.md`: base 100 = aportación al fondeo (`config/parametros.json` → `metrica_competencia`, "desde el fondeo").
- `bitacora/equity.csv`, fila del 8-oct: índice **102.532207**. La primera fila (28-sep) vale 99.5376.
- `herramientas/portafolio.py::metricas_curva` (antes de esta corrección): `rendimiento_total = curva[-1] / curva[0] − 1`. Da 102.532207 / 99.5376 − 1 = **+3.01%**: el día 1 queda fuera, que es justo lo que el fallo de ayer corrigió en `recalcular_indice`. El drawdown del reporte también omitía la pérdida del día 1.
- Benchmark (`serie_benchmark`, consultado el 9-oct): 99.6685 al 28-sep, 100.3062 al 30-sep y 100.9439 al 8-oct. Contra la primera fila daba +1.77% (en la corrida del 8-oct); contra 100 da **+0.94%**.

## Fallo
**Gana el revisor.** El rendimiento del periodo y el drawdown del reporte se miden desde la base 100 del fondeo, igual que el índice. El papel GBM lleva **+2.53%**, el benchmark **+0.94%** y la diferencia es de **+1.59 pp**. El drawdown máximo es −0.46% (el primer día).

## Correcciones
- `herramientas/portafolio.py`:
  - `metricas_curva(curva, rf, base=None)`: con `base`, el rendimiento es `curva[-1] / base − 1` y el drawdown incluye el punto base. Sin `base`, se comporta igual que antes.
  - `construir_reporte` pasa `base=100.0` para el portafolio y para el benchmark.
- `herramientas/tests/test_portafolio.py::test_reporte_mide_desde_el_fondeo` usa la curva real (99.5376 → 102.7057 → 102.532207) y comprueba +3.01% sin base, +2.53% con base, drawdown −0.46% y la línea del reporte.
- `python3 -m unittest discover -s herramientas/tests -q`: **326/326 OK**. `python3 herramientas/portafolio.py reporte` da "Rendimiento del periodo | +2.53% | +0.94% | +1.59%".
- `bitacora/briefs/2026-10-08.md` L32: nota fechada.
- `competencia/marcador.md`: el benchmark de septiembre pasa de +0.64% a **+0.31%**. La nota del 8-oct ("el benchmark ya incluía el primer día") era falsa: la serie sí arranca en 100, pero la cifra se medía contra su primera fila. **Error propio de la conciliación del 8-oct.**
- `bitacora/estado-rutinas.md`: no se edita la línea del cierre del 8-oct (es historia). La corrección queda en el latido de esta conciliación.
- `conocimiento/registro-de-errores.md`: dos filas.

**Salvedad:** el benchmark mide el día 1 desde el cierre anterior al 28-sep, y el papel desde la ejecución de las 14:45 UTC. Con datos diarios es la mejor alineación posible y está documentada. No es una regla nueva.
