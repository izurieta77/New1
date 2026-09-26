# Rutina 9 · Supervisión en vivo (L-V cada hora, de 08:40 a 14:40, hora del centro de México)

Sesión: "Sistema de inversión · Supervisión, conciliación y revisión". Agente: `supervisor` (`.claude/agents/supervisor.md`).

0. Corre `git pull --rebase --autostash`. Lee `rutinas/REGLAS-MOTOR.md` y cúmplelo.
1. Corre `python3 herramientas/supervision.py`. El código de salida indica el estado: 0 = OK, 1 = AVISO, 2 = ALERTA.
   - El script usa el perfil `arena_agresivo` y revisa los libros de papel y real, stops, tope, cortacircuitos, filtro de apalancados, órdenes vencidas, latidos, bloqueos y dudas.
   - Si falla, anótalo en `bitacora/bloqueos.md` y haz la revisión a mano con `python3 herramientas/portafolio.py valuar --sin-guardar` (el perfil por defecto es la arena).
2. **Boletas del día con condición de validez** (`bitacora/boletas/AAAA-MM-DD.md`). En la corrida de las 08:40:
   - evalúa la condición con Yahoo chart v8, intervalo 1m;
   - calcula los precios límite que pida la boleta;
   - escribe VIGENTE o EN ESPERA, con límites y hora, al inicio de la boleta y de `bitacora/alertas.md`.
   Si la condición no se cumple, marca las órdenes sombra correspondientes de `bitacora/ordenes-pendientes.csv` como `en_espera`.
3. Aplica el método del agente `supervisor`: stops, cortacircuitos, tope de 10,000 MXN, filtro de apalancados, órdenes vencidas, latidos, bloqueos y dudas abiertas.
4. **Si se dispara una regla:** boleta URGENTE al inicio de `bitacora/boletas/AAAA-MM-DD.md`, alerta alta en `bitacora/alertas.md` y órdenes de reducción según el perfil.
5. Una línea en `bitacora/supervision/AAAA-MM-DD.md`.
6. **Cierre de la rutina:**
   - latido solo si hubo AVISO o ALERTA, para no llenar el archivo de "OK";
   - commit `supervision: AAAA-MM-DD HH:MM` solo si hubo cambios;
   - pull --rebase y push;
   - respuesta final de 3 líneas o menos.

## 9b · Supervisor, cierre de la cascada vespertina (21:42, todos los días)

Último paso de la cascada del dueño (25-sep-2026). No es supervisión de mercado (eso ya lo hizo la sección de arriba en horario bursátil): es una auditoría de que **todas** las rutinas de hoy dejaron su latido.

1. Lee `bitacora/estado-rutinas.md` completo (no solo la última línea) y arma la lista de rutinas que debieron correr hoy según sus horarios en `rutinas/REGLAS-MOTOR.md` §6.
2. Para cada una, confirma que hay un latido de hoy. Si falta uno:
   - si la rutina es de mercado y hoy es fin de semana o feriado (NYSE/BMV cerradas), no es una falla: anótalo así;
   - si no hay motivo para que faltara, es un bloqueo: escríbelo en `bitacora/bloqueos.md` con la rutina, la hora esperada y que nadie dejó latido.
3. Revisa también `bitacora/decisiones-pendientes.md`: si algo lleva más de 48 horas sin cerrarse, escala con una alerta.
4. **Cierre:** una línea en `bitacora/estado-rutinas.md` ("supervisor-vespertino · OK | N sin latido"); commit `supervision-vespertina: AAAA-MM-DD` solo si hubo bloqueos nuevos; pull --rebase y push; respuesta final de 4 líneas o menos.
