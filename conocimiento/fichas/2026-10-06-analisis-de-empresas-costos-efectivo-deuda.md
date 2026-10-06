# Ficha de estudio: análisis de empresas para invertir (costos relevantes, utilidad contra efectivo y deuda)

> Laboratorio, 6-oct-2026. Fase 0. Nace de un resumen que el dueño pegó ("Para recordar el PDF: análisis de empresas para invertir"), con la aclaración de que el tema es **inversión** y no un diagnóstico de su gasolinera. Alimenta dos áreas de los doctorados: contabilidad (C6, calidad de utilidades, y el área nueva C11, costos y contabilidad gerencial) y finanzas (F7, finanzas corporativas).
> **Acceso real:** solo el resumen del dueño, 15 puntos; **no se leyó el PDF**. Los conceptos son de libro de texto (grado A); las citas se verificaron por su referencia, no se releyeron hoy.
> Código: `conocimiento/fichas/codigo/2026-10-06-costos-relevantes-y-deuda.py` (stdlib, instantáneo). Los números son **didácticos, inventados**; no son evidencia empírica.

## 1. Pregunta
Antes de comprar una acción: ¿qué hay que entender de cómo gana dinero la empresa, de si sus ganancias son efectivo, y de su deuda, para saber qué le queda a los accionistas?

## 2. Los 15 puntos, ordenados por concepto
| Concepto | Lo que dice el resumen | Idea correcta | Ejercicio |
|---|---|---|---|
| **Modelo de negocio** | Vender mucho no es ganar mucho; revisar cuánto cuesta producir y vender | Ingreso, margen y rotación son cosas distintas; el margen de contribución importa más que el ingreso | — |
| **Asignación de gastos** | Repartir gastos entre productos puede hacer que uno parezca poco rentable; quitarlo no elimina esos gastos | Un gasto fijo repartido no desaparece si se cierra la línea: se redistribuye. La decisión se toma con el **margen de contribución**, no con la utilidad después de asignar | Ej. 1 |
| **Costo hundido** | Lo ya gastado y no recuperable no debe decidir si gastas más | Solo cuentan los flujos futuros incrementales | Ej. 2 |
| **Análisis incremental** | Para terminar un producto, compara el ingreso extra con el costo extra | Costo relevante = el que cambia con la decisión | Ej. 2 y 3 |
| **Costo de oportunidad** | También cuenta lo que dejas de ganar al ocupar esa capacidad | Con capacidad limitada, el costo de oportunidad es el margen de la mejor alternativa; con capacidad ociosa es cero | Ej. 3 |
| **Utilidad contra efectivo** | Una empresa puede tener ganancias contables y poco efectivo | La diferencia son los **devengos** (cuentas por cobrar, inventarios, capitalización de gastos); devengos altos predicen menores rendimientos (Sloan, 1996) | Ej. 4 |
| **Deuda** | Las que cotizan publican su deuda; importa cuánto deben, cuándo vence y cuánto pagan de interés; comparar esos pagos con el efectivo que generan | Cobertura de intereses, perfil de vencimientos y deuda neta contra flujo operativo | — |
| **Sobreendeudamiento** | Con deuda elevada, los dueños rechazan proyectos útiles porque el beneficio iría principalmente a los acreedores | *Debt overhang* (Myers, 1977): un proyecto con VPN positivo puede tener VPN negativo para los accionistas | Ej. 5 |
| **Idea central** | Entender ganancias, efectivo, deudas y qué queda para los accionistas | El valor del capital es lo que sobra después de acreedores, en cada escenario | — |

## 3. Resultados de los ejercicios (verificados dos veces: salida del script y cuenta a mano)
1. **Línea con "pérdida":** con A, B y C y 150 de gasto fijo repartido por ingresos, C aparece con −5 de utilidad; pero su margen de contribución es +25. Quitarla baja la utilidad total de **195 a 170** (−25), porque los 150 siguen.
2. **Costo hundido:** con 60 ya gastados y 40 por gastar, si el proyecto terminado vale 70 hay que terminar (+30 contra +10 de rescate); si vale 30 hay que abandonar (−10 contra +10), aunque ya se haya gastado 60.
3. **Capacidad:** un pedido con margen de 4 por unidad se rechaza si ocupar esa capacidad deja de ganar 6; con capacidad ociosa se acepta.
4. **Efectivo:** utilidad neta 100 con flujo operativo 20 es una conversión de 0.20 y una razón de devengos de 7.3% de los activos medios.
5. **Sobreendeudamiento:** un proyecto cuesta 10 y paga 14 seguro (VPN +4). Con deuda de 90 contra activos que valen 100 o 40, el capital pasa de 5 a 12 (+7) pero cuesta 10: **−3 para los accionistas**, y los acreedores ganan **+7**. Los dueños lo rechazan.

## 4. Lo que cambia para el sistema (inferencias)
- **Lista de seis preguntas** para todo dossier de empresa (candidatas de los radares, las 14 pequeñas, ASUR B, NVDA):
  1. ¿Cuánto del ingreso se convierte en margen de contribución, y qué parte del gasto es fija?
  2. ¿La utilidad es efectivo? Conversión CFO/NI de varios años y razón de devengos.
  3. ¿Cuánto debe, cuándo vence y cuánto interés paga? Cobertura y calendario de vencimientos.
  4. ¿Esa deuda alcanza con el flujo libre, o hay riesgo de *debt overhang*: recortes de inversión, dilución, proyectos rechazados?
  5. ¿Qué parte de los gastos de segmento es repartida y no cambia si se cierra una línea?
  6. ¿Qué le queda al accionista en el escenario malo, después de acreedores?
- **Cubierto hoy por la pantalla de empresas pequeñas:** flujo libre ≥ 0.6 × utilidad y deuda neta/EBITDA ≤ 2 (preguntas 2 y 4 parcialmente). **No cubierto:** cobertura de intereses, vencimientos, razón de devengos y la separación fijo/variable. Es el siguiente paso.
- **Los ejemplos del resumen** son del negocio que el dueño conoce; el criterio aplica igual a una emisora: el margen de una gasolinera, por ejemplo, depende de si el costo del combustible se traslada o no (como en el paquete del 5-oct con el IEPS de la gasolina), pero eso es un análisis de la emisora que se estudie, no del negocio del dueño.
- **Reglas del sistema:** el costo hundido ya está cubierto: los *stops* y las salidas del filtro se fijan por reglas futuras, no por el precio de compra.

## 5. Límites
- Es un resumen de 15 puntos, no el PDF; faltan los ejemplos y las cifras de la fuente.
- Los ejercicios usan cifras inventadas y supuestos simples (un solo periodo, sin impuestos ni costos de quiebra).
- Para *debt overhang* con evidencia empírica falta leer y replicar un estudio (por ejemplo, la medición de Myers en datos de empresas).

## 6. Estado nuevo
- Se agrega el tema **"Contabilidad gerencial: costos relevantes y utilidad contra efectivo"** en **Documentado con comprobación** (ejercicio numérico propio, sin datos empíricos) y se actualiza "Finanzas corporativas empíricas" con el ejercicio de sobreendeudamiento.
- `conocimiento/doctorados/ESTADO.md`: nueva área **C11, costos y contabilidad gerencial**, en "Parcial".
