# Rutina 8 · Cripto (cada 4 horas, todos los días: 00:17, 04:17, 08:17, 12:17, 16:17 y 20:17, hora del centro de México)

Sesión: "Sistema de inversión · Inteligencia y cripto". Agente: `analista-cripto` (`.claude/agents/analista-cripto.md`).

0. Corre `git pull --rebase --autostash`. Lee `rutinas/REGLAS-MOTOR.md` y cúmplelo.
1. **Pulso** (todas las corridas). Precio y variación de 24 horas de BTC y ETH, funding, open interest, flujos de ETFs spot del día anterior, noticias materiales y régimen (tendencia sobre la SMA200 y volatilidad). Máximo 12 líneas en `bitacora/cripto/AAAA-MM-DD.md`, con fuente y hora.
2. **Estudio profundo** (solo en la corrida de las 08:17), con el subagente `analista-cripto`. Si tu sesión no lo reconoce, aplica tú el rol.
   - Avanza un tema de la carrera cripto.
   - Si no existe, crea `conocimiento/cripto/00-plan-de-estudio.md` con la ruta licenciatura → maestría → doctorado → frontera.
   - Escribe la ficha en `conocimiento/cripto/fichas/AAAA-MM-DD-<tema>.md` y actualiza `conocimiento/estado-de-dominio.csv`.
3. **Pronóstico** (en la corrida de las 08:17): uno binario de cripto, verificable, a 30 días o menos, con `autor=cripto`. En las demás corridas, resuelve los pronósticos cripto vencidos.
4. **Alertas:** si una posición abierta tiene cripto y hay un movimiento de 8% o más en 4 horas, o un evento de cola (exchange, stablecoin o regulación), agrégalo a `bitacora/alertas.md`.
5. **Cierre de la rutina:**
   - latido;
   - commit `cripto: AAAA-MM-DD HH:MM`, pull --rebase y push, con hasta 4 reintentos;
   - respuesta final de 6 líneas o menos.
