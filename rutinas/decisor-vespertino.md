# Rutina 3b · Decisor, corrida vespertina (todos los días, 19:27 hora del centro de México)

Sesión: "Sistema de inversión · Motor de rutinas". Agente: `decisor` (`.claude/agents/decisor.md`).

Nace de una instrucción del dueño (25-sep-2026): una corrida diaria del decisor, no solo la del comité semanal, con la cartera de **papel**.

0. `git pull --rebase --autostash`. Lee `rutinas/REGLAS-MOTOR.md`.
1. **No es un comité ni un rebalanceo.** REGLAS §4 solo permite cambiar la cartera de papel el viernes, con la skill `comite-de-inversion`, y con al menos 5 días hábiles desde la última decisión. Esta corrida NUNCA genera una orden nueva fuera de esa regla.
2. **Tu pregunta única, como dice tu ficha: ¿alguna alerta de hoy amerita actuar antes del viernes?** Revisa:
   - `bitacora/alertas.md` (altas del día);
   - `bitacora/cripto/AAAA-MM-DD.md` y `bitacora/inteligencia/AAAA-MM-DD.md`;
   - el resultado de la supervisión del día (cortacircuitos, stops, tope) y sus líneas `FX-1` en `bitacora/supervision/AAAA-MM-DD.md`;
   - la lectura de la noche del tipo de cambio: `python3 herramientas/fx_alerta.py` (solo lectura; no toca el estado de supresión). Usa la fecha de la Ciudad de México: a las 19:27 sigue siendo hoy aunque en UTC ya sea mañana.
2b. **Regla FX-1 (alerta cambiaria).** Informa y pide revisión; por sí sola nunca amerita una orden antes del viernes.
   - **AVISO de hoy** (o de la lectura de la noche): una línea en tu archivo del día con Δ1, Δ10, σd, fuente y el efecto por cuenta por cada 1% del dólar, y "sin acción; va al brief de mañana". Si hoy también hubo AVISO ayer en la misma dirección, dilo: es candidato a punto del comité.
   - **ALERTA de hoy:** confirma que el dueño ya recibió hoy la frase clara (fila Alta en `bitacora/alertas.md` a su nombre). Si no la recibió, o la lectura de la noche da una ALERTA nueva que la supervisión no alcanzó a registrar, corre `python3 herramientas/fx_alerta.py --registrar` (imprime la línea y al final guarda la supresión para que la supervisión de mañana no la repita) y escríbela tú ahora como alerta Alta para el dueño, copiando la frase que imprime ("el dólar subió 5.1% en 10 días; a tu dinero le suma unos X MXN; hoy tienes unos Y MXN en dólares: cada 1% del dólar les mueve unos Z MXN; no hay que hacer nada hoy, lo revisa el comité del viernes"). X es el efecto real (lo comprado con el dólar ya arriba casi no suma): no lo recalcules con la parte en USD de hoy. Asegura el punto automático del siguiente comité en `bitacora/decisiones-pendientes.md` ("Comité del viernes AAAA-MM-DD: revisar FX-1 ALERTA del AAAA-MM-DD"); si la supervisión ya lo dejó, no lo dupliques.
3. **Si nada amerita actuar antes del viernes:** dilo en una línea en `bitacora/decisiones/AAAA-MM-DD-decisor-vespertino.md` (o añade una entrada si el archivo del día ya existe) y termina. Es el resultado normal casi todos los días.
4. **Si algo sí amerita actuar antes del viernes** (por ejemplo, un cortacircuitos que la regla ya dispara, o una alerta de contraparte con disparador cumplido): no es una decisión de comité, es una regla. Prepara la boleta (papel y, si aplica, real) según la regla que se disparó, dilo en el mismo archivo con el porqué, y avisa con una alerta alta.
5. **Cierre de la rutina:**
   - latido;
   - commit `decisor-vespertino: AAAA-MM-DD`, `git pull --rebase --autostash` y push, con hasta 4 reintentos;
   - respuesta final de 4 líneas o menos.
