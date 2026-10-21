# Ficha · Doctorado en derecho fiscal D1: proporcionalidad tributaria aplicada al IEPS por diferencias de litros

> Laboratorio del 21-oct-2026 (miércoles: tema de doctorado). D1 estaba en "Parcial", el área fiscal más débil. Continúa la ficha del 7-oct. Fase 0. **No es asesoría: cualquier medio de defensa lo decide el dueño con su abogado y su contador.**

## Pregunta
El IEPS por diferencias de litros (LIF 2027, iniciativa) grava la diferencia positiva mensual entre litros vendidos y adquiridos, sin acreditamiento ni traslado (cap. 33 §9.10, grado C). ¿Qué dice el principio de proporcionalidad y en qué caso concreto la medida podría gravar algo que no es capacidad contributiva?

## Fuentes y acceso
- **Constitución, art. 31 fr. IV** (texto vigente, última reforma DOF 07-10-2026; `diputados.gob.mx/LeyesBiblio/pdf/CPEUM.pdf`, descargado el 21-oct). **Íntegro en lo pertinente, grado A.** Dice: "Contribuir para los gastos públicos, así de la Federación, como de los Estados, de la Ciudad de México y del Municipio en que residan, de la manera **proporcional y equitativa** que dispongan las leyes".
- **SCJN, Primera Sala, Amparo en Revisión 1292/2017** (proyecto publicado en scjn.gob.mx, 14 páginas). **Sección, grado A** como fuente de la Corte. Párrafos 22-25:
  - el gravamen debe tener "congruencia entre el mismo y la capacidad contributiva de los causantes; entendida ésta como la potencialidad real de contribuir al gasto público";
  - cita la jurisprudencia **P./J. 10/2003** ("PROPORCIONALIDAD TRIBUTARIA. DEBE EXISTIR CONGRUENCIA ENTRE EL TRIBUTO Y LA CAPACIDAD CONTRIBUTIVA DE LOS CAUSANTES"; SJF y su Gaceta, Novena Época, t. XVII, mayo de 2003, p. 144, **registro 184291**) y la **P./J. 53/2014 (10a.)**.
  - El Semanario Judicial (sjf2.scjn.gob.mx) bloqueó la consulta automática (Incapsula), así que la tesis se cita por su reproducción en la sentencia, no por su ficha oficial.
- **IEPS por diferencias de litros:** iniciativa de LIF 2027, art. 25 fr. XIX, según facturando.mx. **Grado C**: falta el texto aprobado (cap. 33 §9.10).

## Derivación
1. **Proporcionalidad (P./J. 10/2003):** el impuesto debe medirse por una manifestación real de riqueza del contribuyente.
2. **Hecho que se grava:** "litros vendidos − litros adquiridos > 0" en el mes. Si existe una venta sin origen documentado (el objetivo de la medida), esa diferencia sí revela una riqueza (un ingreso no declarado), y el gravamen tiene conexión con la capacidad.
3. **Riesgo constitucional (inferencia):** la diferencia mensual también aparece **sin ninguna irregularidad**, por puro calendario de inventarios. Si el texto final no reconoce el inventario inicial y final (el blog dice que no prevé una fórmula), grava un movimiento de inventario, que no es riqueza.

## Ejercicio numérico (comprobado)
Código: `fichas/codigo/2026-10-21-d1-ieps-diferencias-proporcionalidad.py`. **Cuota de 6.00 MXN/l y margen de 1.40 MXN/l: supuestos ilustrativos, no datos.**

| Caso | Hechos | IEPS por diferencias | % del margen bruto del mes |
|---|---|---|---|
| 1. Solo calendario | Mes 1: compra 520 mil l, vende 480 mil. Mes 2: compra 460 mil, vende 500 mil. En el bimestre, compras = ventas = 980 mil | Mes 1: 0. **Mes 2: 240,000 MXN** | **34.3%** |
| 2. Inventario reconocido | Igual, pero la base es vendidos − (compras + inventario inicial − inventario final) | 0 | 0% |
| 3. Huachicol | 2,500 l vendidos sin compra ni inventario que los explique | 15,000 MXN | 2.1% |

**Lectura:** el caso 1 cobra más de un tercio del margen del mes a una estación que no vendió ni un litro irregular. El caso 3, que es el objetivo, cobra 2.1%. La desproporción no está en la cuota, sino en **no reconocer el inventario**.

## Límites y contraejemplo
- **Todo depende del texto final.** Si el dictamen o el Senado agregaron el reconocimiento de inventarios, o una tolerancia de merma, el caso 1 desaparece y el argumento se debilita. El blog es grado C.
- **Contraejemplo de la Corte (inferencia general):** la SCJN suele validar medidas contra la evasión, como las presunciones del CFF, si admiten **prueba en contrario**. Si la ley permite "justificar" diferencias con controles volumétricos, inventarios y CFDI (lo que el blog sugiere), la autoridad dirá que el caso 1 se justifica con el inventario y que no hay desproporción. **El argumento solo se sostiene si la ley no deja probar el inventario.**
- **Equidad:** la medida excluye a fabricantes, productores e importadores. Tratar distinto a quien sí está en la misma situación de vender combustible es otro ángulo, que no se estudió hoy.

## Uso para el dueño (preparación, no litigio)
1. **Medir desde ya, con datos de 2026,** la diferencia mensual (ventas − compras) de la estación por producto, y cuánto de ella explica el inventario. Si en algún mes sale positiva solo por calendario, ese es el riesgo exacto.
2. **Leer el texto final** (Gaceta del Senado o DOF, a más tardar a finales de 2026) **antes** de decidir nada. Lo que hay que buscar: si reconoce el inventario o la merma y cómo se prueba.
3. **Si el texto final no reconoce el inventario:** el plazo para un amparo contra la ley suele contarse desde que entra en vigor o desde el primer acto de aplicación. Lo define el abogado.

## Segunda comprobación
- 40,000 l × 6.00 = 240,000.
- 500,000 × 1.40 = 700,000; 240,000 / 700,000 = 34.29%.
- 2,500 × 6 = 15,000; 15,000 / (502,500 × 1.40) = 2.13%.
- Coinciden con las aserciones.

## Estado nuevo
D1 sigue en **"Parcial"** en `doctorados/ESTADO.md`, con evidencia nueva: el art. 31 fr. IV vigente y la tesis 184291 reproducida por la SCJN. En el estado de dominio, la fila D1 pasa de "Documentado" a **"Comprendido con comprobación"**. Faltan:
- legalidad (reserva de ley) y destino al gasto público;
- jurisprudencia de equidad;
- la ficha oficial de la tesis en el Semanario Judicial.
