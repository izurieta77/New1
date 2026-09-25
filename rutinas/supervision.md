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
