# Arbitraje · 2026-10-13 · Registros del 12-oct: PDF del Formato 47/CFF, stop y filtro del UPRO en el cierre, horas de latido y pendientes de más de 24 h

Materia: hallazgos 1.3, 2.3 y 5.5 de `bitacora/revisiones/2026-10-12.md`, y los pendientes de hechos de `bitacora/decisiones-pendientes.md`.

## 1. PDF del Formato 47/CFF (`13e60cd`, hallazgo 1.3)
- **Fuente primaria:** `sha256sum` del archivo = `f0300b42b89466f5941e83fa1d35676a4feaf27ee54ddd07808b0feae4b42e8b` (coincide con el revisor). Metadatos: solo `/Producer: pypdf`; 3 páginas, cabecera "Viernes 17 de julio de 2026 DIARIO OFICIAL" y "9. Formato de Solicitud de trámite 47/CFF ... del Anexo 2". El commit no trae URL ni latido.
- **Origen probable, no confirmado:** el índice del DOF del 17-jul-2026 (`dof.gob.mx/index.php?year=2026&month=07&day=17&edicion=MAT`) publica "Anexo 1 de la Primera Resolución de Modificaciones a la Resolución Miscelánea Fiscal para 2026, publicada el 9 de julio de 2026" (`nota_detalle.php?codigo=5793857&fecha=17/07/2026`), además del Anexo 2 (5793858) y los Anexos 3, 9, 14, 15, 21, 22 y 29 (5793859). La página de la nota no devolvió el cuerpo ni un PDF descargable desde aquí, así que **no pude cotejar bytes ni páginas**: la URL exacta y las páginas de origen siguen sin determinarse.
- **Fallo:** sha256 y procedencia quedan anotados en el memo (nota del 13-oct en L37), con la advertencia de que es un extracto de pypdf y no la edición del DOF. El latido de `13e60cd` se da por cubierto con la mención en la línea de esta conciliación (precedente de `55987a6`, 12-oct). El cotejo con el DOF queda para el verificador.

## 2. Stop y filtro del UPRO de papel en el cierre (`13c8880`, hallazgo 2.3)
- **Qué pide la regla:** `rutinas/diaria-cierre.md` **no lo dice**: su paso 3 solo pide "límites y cortacircuitos" del perfil. La obligación está en `rutinas/REGLAS-MOTOR.md` §7, nota del 5-oct (que manda sobre la rutina): "el cierre revisa cada día el stop de UPRO (135.76 USD, al cierre en papel) y la salida del filtro (^GSPC < SMA200 × 0.97 o VIX ≥ 25)".
- **Conteo, con la sección Cierre de cada brief** (la sección de Revisión y la de Aprendizaje no cuentan):

| Cierre | Stop 135.76 | Filtro | Señalado por |
|---|---|---|---|
| 5-oct | sí | sí | — |
| 6-oct | sí | sí | — |
| 7-oct | **no** | sí | nadie (no se había notado) |
| 8-oct | **no** | sí | revisión 8-oct 1.6 |
| 9-oct | **no** | sí | revisión 9-oct 2.6 (reincide) |
| 12-oct | **no** | **no** | revisión 12-oct 2.3 (reincide) |

- **Fallo:** son **cuatro cierres seguidos** sin el stop (7, 8, 9 y 12-oct); el 12-oct es el primero que también omite el filtro. Contando solo lo señalado, es la segunda reincidencia; contando los hechos, la tercera. Por el precedente (3 y 10-oct) se escala como mecanismo y no se refuerza el texto. **Riesgo real hoy: bajo.** La supervisión sí revisó los dos (UPRO 155.46, 14.5% sobre el stop; ^GSPC 7,807.24 contra la salida 7,037.46 = SMA200 7,255.12 × 0.97; VIX 15.21; recalculado aquí con Yahoo).
- **Opciones (para el dueño, porque es diseño de la cascada; ninguna implementada):** (a) llevar la línea de REGLAS §7 al paso 3 de `diaria-cierre.md`, que hoy no la tiene (la parte de redacción la puede hacer el orquestador); (b) un chequeo en `herramientas/riesgo.py` o en la valuación que imprima stop y filtro del UPRO, para que el cierre solo lo copie; (c) dejarlo formalmente a la supervisión, que ya lo hace.

## 3. Horas de latido posteriores al commit (hallazgo 5.5)
- **Fuente primaria:** `git log --format="%h %ci"`. La revisión contó **7 de 22** hasta `db32887`. Después hubo 7 commits más: `9c531fb` (revisión, orquestador: latido 00:25, commit 00:06, **+19 min**) y `35cb19f` (inteligencia 20:05: latido 02:15, commit 02:12, **+3 min**); los otros 5 (`9cd3546`, `0553159`, `e1af7fc`, `12d9b74` y `b8f4a35`) cuadran.
- **Fallo:** el 12-oct CDMX quedan **9 de 29** commits con una hora de latido posterior a la del commit, y uno sin latido (`13e60cd`). Es la cuarta jornada seguida (9, 10, 11 y 12-oct). Ya está escalado al dueño (12-oct); solo se actualiza el conteo en la alerta.

## 4. Pendientes de hechos de más de 24 h
- **Metaplanet: cerrado.** El 13-oct a las 03:04 UTC TDnet respondió 200 (antes 403) y EDINET (`disclosure2`) también 200. El aviso del 5-oct (`release.tdnet.info/inbs/140120261005546273.pdf`, sha256 `77430f97…`) dice que la tenencia al 30-sep-2026 es de **44,000 BTC**, con 11,000 comprados y 10,000 vendidos en el 3T. La adenda está en `conocimiento/cripto/fichas/2026-10-12-indebtedness-no-definido-y-metaplanet-bloqueado.md`.
- **BIVA (prohibición en el SIC de fondos con cripto): abierto.** `biva.mx/empresas/marco_normativo` da 200, pero es una aplicación de una sola página (igual que el 11 y el 12-oct). Falta el reglamento o un comunicado.
- **Mora automotriz de GFNORTEO: abierto.** `portafolioinfo.cnbv.gob.mx` falla en TLS (código 000, 03:04 UTC), y el SIE pide token. Falta un acceso alterno (el reporte trimestral de Banorte).

## Correcciones
`datos/asunto-fiscal-sgm/memo-multa-2026-10-06.md` (L37), `bitacora/alertas.md` (conteo de latidos y fila nueva del stop), la ficha de cripto del 12-oct (adenda), `bitacora/decisiones-pendientes.md` y `conocimiento/registro-de-errores.md`.
