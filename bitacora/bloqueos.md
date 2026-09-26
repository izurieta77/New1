# Bloqueos de permisos

Cada rutina anota aquí el comando exacto que un permiso bloqueó (ver `rutinas/REGLAS-MOTOR.md` §2), para que el orquestador lo resuelva.

| Fecha | Rutina | Comando o herramienta | Mensaje | Estado |
|---|---|---|---|---|
| 2026-09-25 | 17. Supervisor, cierre del día | Disparador `trig_01M2QiLMduMTbtDZdqM7rGDE` (Inversión · 11 Revisión de calidad, cron 17:57 CDMX) | El disparador existe y estaba activo desde las 14:40 CDMX (antes de las 17:57), pero no dejó `last_fired_at` ni latido en `bitacora/estado-rutinas.md`; su `next_run_at` saltó directo al 26-sep, es decir se saltó la corrida de hoy sin motivo de mercado (no es rutina de mercado, no aplica la excepción de fin de semana/feriado). No hay otro bloqueo de permiso asociado. Rutinas 9 (supervisión en vivo, L-V 08:40-14:40 CDMX) tampoco dejó latido hoy, pero es explicable: su disparador se creó a las 14:40 CDMX, justo al final de esa ventana, así que ninguna corrida de hoy pudo caer dentro del horario. | Disparé `trig_01M2QiLMduMTbtDZdqM7rGDE` manualmente a las 21:44 CDMX (03:44 UTC) para que la revisión de calidad del 25-sep se haga hoy mismo. Pendiente que el orquestador revise por qué el disparador programado no se ejecutó solo, para que no se repita mañana. |
