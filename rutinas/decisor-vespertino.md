# Rutina 3b · Decisor, corrida vespertina (todos los días, 19:27 hora del centro de México)

Sesión: "Sistema de inversión · Motor de rutinas". Agente: `decisor` (`.claude/agents/decisor.md`).

Nace de una instrucción del dueño (25-sep-2026): una corrida diaria del decisor, no solo la del comité semanal, con la cartera de **papel**.

0. `git pull --rebase --autostash`. Lee `rutinas/REGLAS-MOTOR.md`.
1. **No es un comité ni un rebalanceo.** REGLAS §4 solo permite cambiar la cartera de papel el viernes, con la skill `comite-de-inversion`, y con al menos 5 días hábiles desde la última decisión. Esta corrida NUNCA genera una orden nueva fuera de esa regla.
2. **Tu pregunta única, como dice tu ficha: ¿alguna alerta de hoy amerita actuar antes del viernes?** Revisa:
   - `bitacora/alertas.md` (altas del día);
   - `bitacora/cripto/AAAA-MM-DD.md` y `bitacora/inteligencia/AAAA-MM-DD.md`;
   - el resultado de la supervisión del día (cortacircuitos, stops, tope).
3. **Si nada amerita actuar antes del viernes:** dilo en una línea en `bitacora/decisiones/AAAA-MM-DD-decisor-vespertino.md` (o añade una entrada si el archivo del día ya existe) y termina. Es el resultado normal casi todos los días.
4. **Si algo sí amerita actuar antes del viernes** (por ejemplo, un cortacircuitos que la regla ya dispara, o una alerta de contraparte con disparador cumplido): no es una decisión de comité, es una regla. Prepara la boleta (papel y, si aplica, real) según la regla que se disparó, dilo en el mismo archivo con el porqué, y avisa con una alerta alta.
5. **Cierre de la rutina:**
   - latido;
   - commit `decisor-vespertino: AAAA-MM-DD`, `git pull --rebase --autostash` y push, con hasta 4 reintentos;
   - respuesta final de 4 líneas o menos.
