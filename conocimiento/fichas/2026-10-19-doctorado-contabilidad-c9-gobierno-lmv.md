# Ficha · Doctorado en contabilidad C9: gobierno corporativo y comité de auditoría de la sociedad anónima bursátil (LMV arts. 24-26, 42-43)

> Laboratorio del 19-oct-2026 (lunes: tema de doctorado, REGLAS §0d). Era el área con cobertura "Sin" en `doctorados/ESTADO.md`. Fase 0: no recomienda inversiones.

## Pregunta
¿Qué exige la ley mexicana al consejo y a los comités de una emisora del IPC, y qué se puede comprobar con su reporte anual antes de confiar en sus estados financieros?

## Fuente y nivel de acceso
- **Ley del Mercado de Valores, texto vigente, última reforma DOF 14-11-2025** (Cámara de Diputados, `diputados.gob.mx/LeyesBiblio/pdf/LMV.pdf`, 234 páginas; descargada el 19-oct-2026). **Grado A.**
  - **Acceso: sección.** Se extrajo el texto con `pypdf` y se leyeron completos los arts. 24, 25, 26 (fracciones I-IV y el inicio de la V), 42 y 43.
- **No leído:**
  - la CUAE (Disposiciones de la CNBV para emisoras que contratan auditoría externa, DOF 2018: rotación del socio, independencia del despacho);
  - la Circular Única de Emisoras (reporte anual);
  - del lado de EUA, SOX §404 y PCAOB AS 3101 (asuntos críticos de auditoría).
  - Quedan pendientes.

## Lo que dice la ley (cita literal)
| Art. | Regla |
|---|---|
| 24 | Consejo de "un máximo de veintiún consejeros, de los cuales, cuando menos, el veinticinco por ciento deberán ser independientes". No puede ser consejero quien fue **auditor externo** de la sociedad o de su grupo "durante los doce meses inmediatos anteriores" |
| 25 | Los comités de prácticas societarias y de auditoría se integran "exclusivamente con consejeros independientes y por un mínimo de tres miembros". **Excepción:** si un grupo tiene "el cincuenta por ciento o más del capital social", el de **prácticas societarias** puede integrarse "por mayoría de consejeros independientes siempre que dicha circunstancia sea revelada al público". La excepción no alcanza al de auditoría |
| 26 | No pueden ser independientes, entre otros: directivos o empleados (y quienes lo fueron en los 12 meses anteriores), quienes tienen influencia significativa o poder de mando, los accionistas del grupo de control, y los clientes, proveedores, deudores o acreedores "importantes". Importante: ventas "más del diez por ciento"; crédito "mayor al quince por ciento de los activos" de la sociedad o de su contraparte |
| 42 fr. II | El comité de auditoría evalúa al auditor externo y se reúne con él "por lo menos una vez al año"; discute los estados financieros y recomienda o no su aprobación; informa del control interno "incluyendo las irregularidades" |
| 43 | Los presidentes de ambos comités los nombra y remueve **solo la asamblea**; no pueden presidir el consejo. Su informe anual incluye las operaciones con personas relacionadas (prácticas) y el estado del control interno y la evaluación del auditor externo (auditoría) |

## Ejercicio numérico (comprobado)
Código: `conocimiento/fichas/codigo/2026-10-19-c9-gobierno-lmv.py` (aserciones; casos ilustrativos).
- **Mínimo de independientes:** ⌈0.25·n⌉. Con 8 consejeros son 2; con 12, 3; con 15, 4; con 21, 6.
  - Con 15 consejeros y 3 independientes (20%) no cumple.
- **Comités:** el de auditoría con 2 independientes de 3 no cumple. En una emisora controlada, el de prácticas societarias con 2 de 3 cumple **solo si se revela**.
- **Independencia (fr. IV):**
  - Un proveedor en el que la operación con la sociedad es 60 y sus ventas totales son 500 (12%) es importante; con 800 (7.5%), no.
  - Un crédito de 200 contra activos de 1,500 (13.3%) y de 1,200 de la contraparte (16.7%) es importante por la contraparte.
- **Exauditor:** a los 10 meses no puede ser consejero; a los 13, sí.

## Límites y contraejemplo
- **Ambigüedad del texto (inferencia):** la fr. IV dice "cuando las ventas de la sociedad representen más del diez por ciento de las ventas totales del cliente, del prestador de servicios o del proveedor". Para un **proveedor**, leído literalmente, mide las ventas de la sociedad y no las compras. El ejercicio usa "el monto de las operaciones con la sociedad". **Sin criterio de la CNBV leído, no se resuelve.**
- **El cumplimiento formal no es independencia real.** La asamblea "califica" la independencia (art. 26), y en una emisora controlada esa asamblea la domina el controlador. La ley pone el piso; la calidad se juzga por los hechos:
  - el cambio de auditor,
  - las salvedades,
  - las operaciones con relacionadas del informe del art. 43,
  - la rotación de consejeros.
- **Contraejemplo:** una emisora puede cumplir los arts. 24-26 y aun así esconder operaciones con relacionadas fuera de mercado. El caso de manual de la literatura es el *tunneling* en grupos piramidales (Johnson, La Porta, López-de-Silanes y Shleifer, 2000, *AER P&P*). Se cita de memoria y **no se verificó hoy**.

## Uso en el sistema
- **Lista de comprobación nueva para toda ficha de empresa mexicana:**
  1. ¿Cuántos consejeros y qué porcentaje son independientes (≥ 25%)?
  2. ¿El comité de auditoría es 100% independiente con ≥ 3 miembros?
  3. ¿La emisora usa la excepción del art. 25 (controlada) y la revela?
  4. ¿Qué dice el informe anual del comité (art. 43) sobre el control interno y las relacionadas?
  5. ¿Cambió de auditor externo en los últimos 3 años?
- **AMX (reporta el 20-oct):** está controlada por un grupo familiar (dato público conocido, no verificado hoy contra su reporte anual). Antes del post-mortem, revisar el art. 43 de su informe y la nota de partes relacionadas, junto con la ficha C4 del 18-oct.

## Segunda comprobación
- ⌈0.25 × 15⌉ = ⌈3.75⌉ = 4; 4/15 = 26.7% ≥ 25%.
- 60/500 = 0.12 > 0.10; 200/1,200 = 0.167 > 0.15.
- Coinciden con las aserciones.

## Estado nuevo
C9 pasa de **"Sin" a "Parcial"** en `doctorados/ESTADO.md`. Cubre el gobierno de la SAB en la LMV con texto íntegro por sección y un verificador con aserciones. Faltan:
- la CUAE (rotación e independencia del auditor);
- SOX §404 y PCAOB (asuntos críticos);
- la evidencia empírica de calidad de auditoría (por ejemplo, DeFond y Zhang, 2014);
- un caso real de una emisora del universo.
