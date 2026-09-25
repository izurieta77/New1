# Rutina 8 · Cripto (cada 4 horas, todos los días: 00:17, 04:17, 08:17, 12:17, 16:17 y 20:17, hora del centro de México)

Sesión: "Sistema de inversión · Inteligencia y cripto". Agente: `analista-cripto` (`.claude/agents/analista-cripto.md`).

0. Corre `git pull --rebase --autostash`. Lee `rutinas/REGLAS-MOTOR.md` y cúmplelo.
1. **Pulso** (todas las corridas). Precio y variación de 24 horas de BTC y ETH, funding, open interest, flujos de ETFs spot del día anterior, noticias materiales y régimen (tendencia sobre la SMA200 y volatilidad). Máximo 12 líneas en `bitacora/cripto/AAAA-MM-DD.md`, con fuente y hora.
2. **Estudio profundo** (solo en la corrida de las 08:17), con el subagente `analista-cripto`. Si tu sesión no lo reconoce, aplica tú el rol.
   - Avanza un tema de la carrera cripto siguiendo `conocimiento/cripto/00-plan-de-estudio.md`. Su columna vertebral son los 35 recursos del dueño (`conocimiento/cripto/recursos/00-indice.md`).
   - Toma el siguiente recurso o tema pendiente del nivel más bajo sin terminar.
   - Acceso solo por vías legales; declara el acceso real (íntegro, sección o resumen).
   - Amplía su ficha en `conocimiento/cripto/recursos/NN-*.md` y el capítulo de síntesis del grupo (01-06), con adenda fechada.
   - Actualiza `estado` y `acceso` en `conocimiento/cripto/recursos/indice.csv`.
   - Escribe la ficha en `conocimiento/cripto/fichas/AAAA-MM-DD-<tema>.md` y actualiza `conocimiento/estado-de-dominio.csv`.
3. **Pronóstico** (en la corrida de las 08:17): uno binario de cripto, verificable, a 30 días o menos, con `autor=cripto`. En las demás corridas, resuelve los pronósticos cripto vencidos.
4. **Contraparte:** una vez al día, en la corrida de las 08:17, revisa las "Señales para vigilar Binance hoy" de `conocimiento/cripto/lista-senales-de-alerta.md`. Si se cumple un disparador del plan de contingencia de `bitacora/decisiones/2026-09-25-CRIPTO-inicial.md`, genera una alerta alta.
5. **Alertas:** si una posición abierta tiene cripto y hay un movimiento de 8% o más en 4 horas, o un evento de cola (exchange, stablecoin o regulación), agrégalo a `bitacora/alertas.md`.
6. **Cierre de la rutina:**
   - latido;
   - commit `cripto: AAAA-MM-DD HH:MM`, pull --rebase y push, con hasta 4 reintentos;
   - respuesta final de 6 líneas o menos.
