# Rutina 9 · Supervisión en vivo (L-V cada hora, de 08:40 a 14:40, hora del centro de México)

Sesión: "Sistema de inversión · Supervisión, conciliación y revisión". Agente: `supervisor` (`.claude/agents/supervisor.md`).

0. Corre `git pull --rebase --autostash`. Lee `rutinas/REGLAS-MOTOR.md` y cúmplelo.
1. Corre `python3 herramientas/supervision.py`. El código de salida indica el estado: 0 = OK, 1 = AVISO, 2 = ALERTA.
   - El script usa el perfil `arena_agresivo` y revisa los libros de papel y real, stops, tope, cortacircuitos, filtro de apalancados, órdenes vencidas, latidos, bloqueos y dudas.
   - Si falla, anótalo en `bitacora/bloqueos.md` y haz la revisión a mano con `python3 herramientas/portafolio.py valuar --sin-guardar` (el perfil por defecto es la arena).
2. Aplica el método del agente `supervisor`: stops, cortacircuitos, tope de 10,000 MXN, filtro de apalancados, órdenes vencidas, latidos, bloqueos y dudas abiertas.
3. **Si se dispara una regla:** boleta URGENTE al inicio de `bitacora/boletas/AAAA-MM-DD.md`, alerta alta en `bitacora/alertas.md` y órdenes de reducción según el perfil.
4. Una línea en `bitacora/supervision/AAAA-MM-DD.md`.
5. **Cierre de la rutina:**
   - latido solo si hubo AVISO o ALERTA, para no llenar el archivo de "OK";
   - commit `supervision: AAAA-MM-DD HH:MM` solo si hubo cambios;
   - pull --rebase y push;
   - respuesta final de 3 líneas o menos.
