# Rutina 10 · Conciliación y arbitraje (diaria, 20:57 hora del centro de México)

Séptimo paso de la cascada vespertina del dueño (25-sep-2026, ver `rutinas/REGLAS-MOTOR.md` §6b): corre después del decisor y del investigador vespertino, para resolver cualquier desacuerdo que hayan dejado.

Sesión: "Sistema de inversión · Supervisión, conciliación y revisión". Agente: `conciliador-arbitro` (`.claude/agents/conciliador-arbitro.md`).

0. Corre `git pull --rebase --autostash`. Lee `rutinas/REGLAS-MOTOR.md` y cúmplelo.
1. **Conciliación del día**, con el subagente `conciliador-arbitro`. Si tu sesión no lo reconoce, aplica tú el rol.
   - Cuadra órdenes, ejecuciones, reporte real, valuación, pronósticos y cifras repetidas.
   - Escribe `bitacora/conciliacion/AAAA-MM-DD.md` con: OK por rubro, diferencias y su explicación, y correcciones con una nota fechada.
2. **Arbitraje:**
   - resuelve cada punto abierto de `bitacora/decisiones-pendientes.md` que sea de hechos, registros o reglas, con su fallo en `bitacora/arbitraje/`;
   - lo que toque la dirección de una inversión o los parámetros se escala: al decisor o al dueño, según corresponda.
3. **Errores:** los que encuentres van a `conocimiento/registro-de-errores.md`.
4. **Cierre de la rutina:**
   - latido;
   - commit `conciliacion: AAAA-MM-DD`, pull --rebase y push;
   - respuesta final de 6 líneas o menos.
