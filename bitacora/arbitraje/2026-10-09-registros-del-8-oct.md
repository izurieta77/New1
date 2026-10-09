# Arbitraje · 2026-10-09 · Registros del 8-oct que contradicen fallos y fuentes previas (BMV/IBIT, P0062, pronóstico NFLX)

Origen: hallazgos 2.4, 4.3, 6.3 y 3.4 de `bitacora/revisiones/2026-10-08.md`.

## 1. Prohibición de fondos cripto en el SIC (BMV/BIVA) e IBIT vía Trading Global
- **Posiciones:**
  - `bitacora/decisiones-pendientes.md`, entrada del 8-oct, 14:28 UTC (`5ae4f66`): la prohibición "sigue sin confirmarse ni refutarse"; IBIT por Trading Global es "información útil y accionable".
  - Ficha D7, L11: "No localizada … nv".
  - Fallo `2026-10-08-bmv-fondos-cripto.md` (03:14 UTC): confirmada para la BMV.
- **Fuente primaria:** aviso de reforma de la BMV y Reglamento Interior vigente, disposición 4.019.00. La autorizó el oficio CNBV 312-2/42112/2024 del 15-abr-2024 y está en vigor desde el 17-abr-2024. La cita textual está en el fallo del 8-oct (sha256 `c8f242dc…` y `71a1e28b…`). En la búsqueda de hoy solo aparecen los documentos de la BMV: para BIVA no hay texto.
- **Fallo:** gana el fallo del 8-oct. **BMV confirmada (A); BIVA sin verificar.** Las dos afirmaciones posteriores ignoraron un fallo que ya estaba en el repo.
- **Advertencia fiscal que faltaba** (ficha D7, `conocimiento/fichas/2026-10-08-doctorado-fiscal-d7-fondos-extranjeros.md`):
  - L16: un ETF comprado en EUA no entra al 10% del art. 129 fr. I LISR y tributa con la tarifa general (grado B, inferencia de texto);
  - L30-L32: con salario, 19-30% marginal, hasta 20,000 MXN más por cada 100,000 de ganancia;
  - L17: duda del art. 176 (acumulación sin venta si el vehículo califica).

  Se agregó a la entrada de decisiones-pendientes.
- **No se decide** si se compra IBIT: eso es del comité y del dueño. La regla vigente sigue igual.

## 2. P0062 (subyacente de septiembre ≤ 3.80%)
- **Posiciones:**
  - brief del 8-oct, L21, y decisiones-pendientes (pre-apertura del 8-oct): "queda abierto, INEGI no accesible";
  - `bitacora/pronosticos.csv` L63: resuelto SÍ por el vigía a las 07:05 CDMX.
- **Fuente primaria:** boletín INEGI 619/26 del 8-oct-2026 (`inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_2q2026_10.pdf`, sha256 `9c72b5e957b9f68f…`). Página 1: subyacente anual **3.75%** y general anual 3.45%.
- **Fallo:** **SÍ** (3.75 ≤ 3.80, criterio literal). Gana el CSV y se corrigen el brief y la línea de decisiones-pendientes con nota fechada. P0036 (general ≥ 3.40%, SÍ con 3.45%) también se confirma con el mismo PDF.

## 3. Pronóstico de la ficha NFLX fuera de la bitácora central
- **Hecho:** `empresas/NFLX/pronosticos.csv`, `NFLX-guia4T26_desaceleracion-3T26` (p = 0.58), creado en `6b1de55` el 2026-10-08 a las 14:38 UTC, antes del reporte del 20-oct. No estaba en `bitacora/pronosticos.csv`.
- **Formato:** cumple. Es una pregunta binaria con probabilidad, fecha de resolución (21-oct), fuente (carta a accionistas / 8-K 2.02) y criterio literal (crecimiento a/a de la guía del 4T26 contra 12,050.8 USD M del 4T25 < 10%; el empate cuenta como NO).
- **Fallo:** se registra como **P0094** con `fecha_creacion` 2026-10-08, la real, y autor `claude` (`pronosticos.py agregar --fecha-creacion`). No es un dato retroactivo: la fecha es la del commit original.

## Correcciones
- `bitacora/decisiones-pendientes.md`: dos notas.
- `conocimiento/fichas/2026-10-08-doctorado-fiscal-d7-fondos-extranjeros.md`: L11 y L40.
- `bitacora/briefs/2026-10-08.md`: L21.
- `bitacora/pronosticos.csv`: P0094.
- `conocimiento/registro-de-errores.md`: tres filas.
