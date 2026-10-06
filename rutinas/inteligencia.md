# Rutina 7 · Inteligencia (diaria: 07:05, 11:05, 15:05 y 20:05, hora del centro de México)

Sesión: "Sistema de inversión · Inteligencia y cripto". Agente: `vigia-de-informacion` (`.claude/agents/vigia-de-informacion.md`).

0. Corre `git pull --rebase --autostash`. Lee `rutinas/REGLAS-MOTOR.md` y cúmplelo: autonomía, bloqueos, latido y pendientes.
1. Lee el contexto:
   - las posiciones vigentes (`bitacora/operaciones.csv`, `bitacora/real/` y la decisión de cartera más reciente en `bitacora/decisiones/`);
   - los pronósticos abiertos (`bitacora/pronosticos.csv`);
   - la última tabla de `bitacora/inteligencia/`;
   - el tipo de cambio y la regla FX-1: `python3 herramientas/fx_alerta.py` (solo lectura) y la última línea `FX-1` de `bitacora/supervision/`.
1b. **Entradas del dueño (REGLAS §0e):** lee lo que el dueño pegó en `datos/entrada-dueno/` (últimas 48 h) y `datos/fuentes-del-dueno.csv`. Procésalo primero: califícalo de A a D (lo de redes empieza en D), verifícalo con fuente primaria, agrégalo a la tabla del día y anota la fuente en el marcador de fuentes. Lo que diga ser información privilegiada se descarta por cumplimiento.
1c. **Podcasts (herramienta propia):** corre `python3 herramientas/podcasts.py --dias 2 --salida bitacora/inteligencia/podcasts-AAAA-MM-DD.md`. Lista los episodios nuevos de `datos/podcasts-feeds.csv`, baja las transcripciones que el feed publica (Odd Lots, Columbia Energy Exchange, Bankless; quedan en `datos/cache/podcasts/`, fuera de git) y cuenta palabras clave. Lee las transcripciones de los episodios que toquen posiciones, pronósticos abiertos, la lista de vigilancia o los doctorados, extrae tesis y datos, **verifica cada dato contra fuente primaria**, y anota en el marcador de fuentes (`datos/fuentes-del-dueno.csv`) los datos verificados y los que no. Los programas sin transcripción en el feed (Norte Económico, Expansión Daily, Unchained, Capital Allocators) solo traen notas: el dueño pega lo que escuche.
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
   - **Umbral de urgencia alta por precio:** un movimiento de más de 2% en el **valor en pesos** de una posición abierta (precio en USD × USD/MXN), no en su precio en dólares. Ejemplo: SPYM −1.5% en dólares con el peso apreciándose 0.8% es −2.3% en pesos y sí es urgencia alta.
   - **Un AVISO o una ALERTA de FX-1 cuenta como urgencia alta.** Busca la causa (Banxico, Fed, datos, flujos, política) con fuente primaria y di qué posiciones toca. Si la supervisión ya abrió la fila en `bitacora/alertas.md`, agrega tu actualización en esa fila; no abras otra.
4. En la corrida de las 20:05, registra un pronóstico binario verificable con `autor=vigia`.
5. **Cierre de la rutina:**
   - latido;
   - commit `inteligencia: AAAA-MM-DD HH:MM`, `git pull --rebase --autostash` y push, con hasta 4 reintentos;
   - respuesta final de 6 líneas o menos.
