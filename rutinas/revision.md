# Rutina 11 · Revisión de calidad (diaria, 17:57 hora del centro de México)

Primer paso de la cascada vespertina del dueño (25-sep-2026): revisor → resumen de aprendizaje → cripto → bloque de trabajo continuo → decisor → investigador → conciliación y arbitraje → supervisor. Revisa lo acumulado hasta ahora (pre-apertura, laboratorio, cierre de hoy, y lo que quedó pendiente de la noche anterior), antes de que el resto de la cascada añada trabajo nuevo esta noche.

Sesión: "Sistema de inversión · Supervisión, conciliación y revisión". Agente: `revisor` (`.claude/agents/revisor.md`).

0. Corre `git pull --rebase --autostash`. Lee `rutinas/REGLAS-MOTOR.md` y cúmplelo.
1. Lista los entregables del día: `git log --since="24 hours ago" --name-only`.
2. Con el subagente `revisor`, aplica la lista de revisión completa a:
   - las decisiones y boletas del día;
   - los briefs;
   - `PLAN.md`, si cambió;
   - una muestra de 3 fichas o réplicas del día.
   Si tu sesión no reconoce al revisor, aplica tú el rol.
3. Escribe `bitacora/revisiones/AAAA-MM-DD.md`. Los hallazgos bloqueantes van también a `bitacora/alertas.md`.
4. **Resumen para el dueño:** agrega al final del brief del día (`bitacora/briefs/AAAA-MM-DD.md`) una sección "Revisión" de 5 líneas o menos con lo que el dueño debe saber.
5. **Cierre de la rutina:**
   - latido;
   - commit `revision: AAAA-MM-DD`, pull --rebase y push;
   - respuesta final de 6 líneas o menos.
