# Rutina 1 · Pre-apertura (L-V, 06:52 hora del centro de México)

Este procedimiento escrito manda sobre el texto del disparador, que ya indica seguirlo si existe. Lo mantiene el orquestador en git.

0. Tras el `git pull --rebase --autostash`, lee `rutinas/REGLAS-MOTOR.md` y cúmplelo: autonomía, bloqueos, latido y pendientes (§7). Lee también `config/parametros.json`.
1. Corre `python3 herramientas/tablero.py --salida bitacora/briefs/AAAA-MM-DD-tablero.md` (régimen).
2. Corre `python3 herramientas/geopolitica.py` si existe (índice GPR, Polymarket/Kalshi).
3. **Pronósticos vencidos:** resuélvelos con fuente oficial y puntúa (`python3 herramientas/pronosticos.py --help`).
4. **Escaneo web con fuentes primarias** (carga WebSearch y WebFetch con ToolSearch):
   - macro de EUA y México del día;
   - geopolítica y política material de las últimas 24 h, siguiendo la cadena acontecimiento → exposición → efecto económico → estados financieros → valuación → qué descuenta el precio;
   - empresas de `empresas/universo.csv` que reportan hoy o esta semana, comparadas contra sus `pronosticos.csv`.
5. **Pronósticos nuevos:** registra 3–5 pronósticos binarios, verificables, con resolución a 30 días o menos. Varía los temas (macro, empresas, mercados, México) para que la calibración sea representativa.
6. **Portafolio de papel:** valúa y revisa cortacircuitos y rachas (`herramientas/riesgo.py`). La cartera solo cambia con la skill `comite-de-inversion` (viernes) o por un cortacircuitos (REGLAS §4).
6b. **Sala de decisiones** (agente `decisor`; si tu sesión no lo reconoce, lee `.claude/agents/decisor.md` y aplica el rol):
   - Revisa `bitacora/alertas.md`, la inteligencia y el pulso cripto de la noche y la última supervisión.
   - Decide si hace falta una **decisión extraordinaria**: solo por una alerta alta confirmada, un cortacircuitos o el filtro roto. Lo normal es "sin acción"; regístralo en una línea.
   - Si hay boletas reales del día, verifica sus condiciones de validez (REGLAS §5b) y ponlas al inicio del brief.
7. **Brief:** escribe `bitacora/briefs/AAAA-MM-DD.md` con régimen; geopolítica y política; empresas; pronósticos nuevos y resueltos, con Brier acumulado; papel y riesgo; aprendizaje o error. Si es feriado de NYSE y BMV, basta un brief corto.
8. **Cierre de la rutina:**
   - deja el latido (REGLAS §3);
   - commit `pre-apertura: AAAA-MM-DD`, `git pull --rebase --autostash` y push, con hasta 4 reintentos;
   - respuesta final de 12 líneas o menos.
