# Rutina 7 · Inteligencia (diaria: 07:05, 11:05, 15:05 y 20:05, hora del centro de México)

Sesión: "Sistema de inversión · Inteligencia y cripto". Agente: `vigia-de-informacion` (`.claude/agents/vigia-de-informacion.md`).

0. Corre `git pull --rebase --autostash`. Lee `rutinas/REGLAS-MOTOR.md` y cúmplelo: autonomía, bloqueos, latido y pendientes.
1. Lee el contexto:
   - las posiciones vigentes (`bitacora/operaciones.csv`, `bitacora/real/` y la decisión de cartera más reciente en `bitacora/decisiones/`);
   - los pronósticos abiertos (`bitacora/pronosticos.csv`);
   - la última tabla de `bitacora/inteligencia/`.
2. **Barrido.** Lánzalo con el subagente `vigia-de-informacion`. Si tu sesión no reconoce ese tipo, aplica tú el rol de su archivo.
   - Prioridad 1: lo que afecta a las posiciones abiertas y a los pronósticos abiertos.
   - Prioridad 2: macro, geopolítica y política de EUA y México.
   - Prioridad 3: academia y ensayos nuevos.
   - Prioridad 4: redes y video. Anota siempre el nivel de acceso real.
   - Profundidad según la hora:
     - 07:05: barrido completo de la noche y Asia/Europa;
     - 11:05 y 15:05: actualización de la sesión;
     - 20:05: cierre del día y lo que viene mañana, con el calendario.
3. Agrega las filas a `bitacora/inteligencia/AAAA-MM-DD.md`. Las de urgencia alta van también a `bitacora/alertas.md`.
4. En la corrida de las 20:05, registra un pronóstico binario verificable con `autor=vigia`.
5. **Cierre de la rutina:**
   - latido;
   - commit `inteligencia: AAAA-MM-DD HH:MM`, `git pull --rebase --autostash` y push, con hasta 4 reintentos;
   - respuesta final de 6 líneas o menos.
