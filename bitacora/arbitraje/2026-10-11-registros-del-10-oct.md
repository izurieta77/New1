# Arbitraje · 2026-10-11 · Registros del 10-oct: horas de la inteligencia 07:05, commit 221c1f7, cap. 33 y latidos

Materia: registros que no cuadran con git y pendientes de `bitacora/revisiones/2026-10-10.md`.

## 1. Horas de la inteligencia de las 07:05 (hallazgo 1.1 de la revisión)
- **Posiciones:**
  - La inteligencia dice "13:06–13:50 UTC", con filas a las 13:30–13:45, 13:35–13:50 y 13:40–13:55, y su latido dice 13:50 UTC.
  - El revisor dice que esas horas son posteriores al commit.
- **Fuente primaria:** `git show -s fd8780a`, con fecha de autor y de commit **2026-10-10 13:10:53 +0000**. Ese commit ya contiene las 23 líneas de la sección, incluida la fila "13:40–13:55", y el archivo de podcasts. La rutina se dispara a las 07:05 CDMX, que son las 13:05 UTC. Ninguna corrección posterior de la propia inteligencia tocó esas horas.
- **Fallo:** la hora real de la corrida está entre **~13:05 y 13:10:53 UTC**. Las horas de 13:11 en adelante (filas OFAC, podcasts y academia, el final de las filas "13:10–13:30", el encabezado y el latido) son imposibles. Fueron estimadas, no registradas. Los hechos de las filas no cambian. Reincide el hallazgo 2.9 del 9-oct y se agrava, porque esta vez afecta las filas. **Regla para la inteligencia:** la hora de cada fila sale de `date -u` en el momento de la consulta, y la del latido no puede ser posterior al commit.
- **Corrección:** nota fechada bajo el encabezado de `bitacora/inteligencia/2026-10-10.md` y al final de su latido en `bitacora/estado-rutinas.md`. No se borró ninguna fila.
- **Menor, reincide:** dos latidos de la noche tienen una hora posterior a su commit: inteligencia 20:05 con latido a las 02:16 y commit `78568e8` a las 02:10:38, e investigador con latido a las 02:15 y commit `4b2f44c` a las 02:13:34. Lo anoto y no corrijo esas líneas.

## 2. Commit `221c1f7` (decisor vespertino, "corrige fechas 2026-10-09")
- `git show 221c1f7 -- bitacora/estado-rutinas.md`: **+1 / −0**. Solo antepuso su propio latido.
- El `--numstat` de los 27 commits que tocaron `estado-rutinas.md` desde el 10-oct 00:00 UTC da +1 o +2 y **0 borrados** en todos.
- La "corrección de fechas":
  - creó `bitacora/decisiones/2026-10-09-decisor-vespertino.md`, con el contenido de la versión anterior del archivo del 10-oct y solo el título cambiado de fecha;
  - reescribió el del 10-oct con la corrida nueva;
  - renombró `bitacora/investigador/2026-10-10-vespertino.md` a `2026-10-09` (similitud del 94%, una línea de título).
- Ningún otro archivo cita las rutas viejas.
- **Fallo:** no hubo pérdida de escritura ni se borraron latidos ajenos, así que no hay nada que restaurar y no es una reincidencia de la pérdida del 9-oct. La fecha de cada archivo corresponde al día CDMX de la cascada, que es lo correcto.

## 3. Cap. 33, materialidad fiscal (`71f865d`)
- **Qué exige el repo:**
  - `rutinas/bloque-trabajo-continuo.md` paso 3 pide actualizar `estado-de-dominio.csv`. El commit agregó la fila: "Doctorado derecho fiscal D2-D3: materialidad…", nivel Documentado. Está bien.
  - `conocimiento/doctorados/README.md` L17 dice que el avance se mide en `ESTADO.md`. Ahí, D2 no mencionaba el cap. 33.
- **Corrección:** agregué en D2 de `ESTADO.md` la referencia al cap. 33 como "pendiente del verificador". **No cambié la cobertura** ni audité el contenido, que le toca al verificador.

## 4. Pendientes de más de 24 h
- **BIVA y la mora de GFNORTEO:** siguen abiertos y ya se anotó qué falta (ver `decisiones-pendientes.md`, entrada del 11-oct).
- **Art. 70-A CFF:** cerrado por el investigador.
- **Lo que es del dueño, del comité o del orquestador:** no se tocó.
