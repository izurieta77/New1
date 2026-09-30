# Rutina 1 · Pre-apertura (L-V, 06:52 hora del centro de México)

Este procedimiento escrito manda sobre el texto del disparador, que ya indica seguirlo si existe. Lo mantiene el orquestador en git.

0. Tras el `git pull --rebase --autostash`, lee `rutinas/REGLAS-MOTOR.md` y cúmplelo: autonomía, bloqueos, latido y pendientes (§7). Lee también `config/parametros.json`.
1. Corre `python3 herramientas/tablero.py --salida bitacora/briefs/AAAA-MM-DD-tablero.md` (régimen).
1b. **Tipo de cambio (regla FX-1, obligatorio):** corre `python3 herramientas/fx_alerta.py --brief`. Imprime la línea "Tipo de cambio" del brief: USD/MXN spot, Δ1, Δ10, σd, estado de FX-1 y fuente, y por cuenta (papel, real, papel-binance, real-binance) el **efecto de precio separado del efecto cambiario**, los dos sobre la misma ventana: del cierre previo de cada posición (la línea dice su fecha) a este momento, con el USD/MXN de la fecha de ese cierre como punto de partida del efecto cambiario; más el efecto por cada 1% del dólar. Si faltó el cierre de alguna posición, la línea lo dice en "Notas" (su efecto y su parte en USD no entran): cópialo al brief. Es de solo lectura: no toca `bitacora/supervision/estado-fx.json` (eso lo hace la supervisión).
   - Si el script falla, escribe la línea a mano con Yahoo `MXN=X` (chart v8, 1m) y el FIX o el cierre anterior, di la fuente y anota el fallo en `bitacora/bloqueos.md`.
   - Lee también la última línea `FX-1` de `bitacora/supervision/` (la de ayer) y las filas FX-1 abiertas de `bitacora/alertas.md`.
2. Corre `python3 herramientas/geopolitica.py` si existe (índice GPR, Polymarket/Kalshi).
3. **Pronósticos vencidos:** resuélvelos con fuente oficial y puntúa (`python3 herramientas/pronosticos.py --help`).
4. **Escaneo web con fuentes primarias** (carga WebSearch y WebFetch con ToolSearch):
   - macro de EUA y México del día;
   - geopolítica y política material de las últimas 24 h, siguiendo la cadena acontecimiento → exposición → efecto económico → estados financieros → valuación → qué descuenta el precio;
   - empresas de `empresas/universo.csv` que reportan hoy o esta semana, comparadas contra sus `pronosticos.csv`.
5. **Pronósticos nuevos:** registra 3–5 pronósticos binarios, verificables, con resolución a 30 días o menos. Varía los temas (macro, empresas, mercados, México) para que la calibración sea representativa.
6. **Portafolio de papel:** valúa y revisa cortacircuitos y rachas (`herramientas/riesgo.py`). La cartera solo cambia con la skill `comite-de-inversion` (viernes) o por un cortacircuitos (REGLAS §4).
6b. **Sala de decisiones** (agente `decisor`; si tu sesión no lo reconoce, lee `.claude/agents/decisor.md` y aplica el rol):
   - Revisa `bitacora/alertas.md`, la inteligencia y el pulso cripto de la noche y la última supervisión, incluida la línea `FX-1`.
   - **FX-1:** un AVISO (de ayer o del paso 1b) va al brief como punto propio, con el efecto por cuenta. Una ALERTA vigente va al inicio del brief con la frase para el dueño; si el paso 1b muestra una ALERTA que la supervisión aún no registró (antes de las 08:40), ponla al inicio del brief: la corrida de supervisión de las 08:40 la registra y se la avisa al dueño el mismo día. FX-1 nunca justifica por sí sola una decisión extraordinaria: informa y la revisa el comité.
   - Decide si hace falta una **decisión extraordinaria**: solo por una alerta alta confirmada, un cortacircuitos o el filtro roto. Lo normal es "sin acción"; regístralo en una línea.
   - Si hay boletas reales del día, verifica sus condiciones de validez (REGLAS §5b) y ponlas al inicio del brief.
7. **Brief:** escribe `bitacora/briefs/AAAA-MM-DD.md` con régimen; **tipo de cambio** (línea obligatoria "Tipo de cambio" del paso 1b, con el efecto de precio separado del efecto cambiario por cuenta); geopolítica y política; empresas; pronósticos nuevos y resueltos, con Brier acumulado; papel y riesgo; aprendizaje o error. Si es feriado de NYSE y BMV, basta un brief corto, pero la línea "Tipo de cambio" va siempre.
8. **Cierre de la rutina:**
   - deja el latido (REGLAS §3);
   - commit `pre-apertura: AAAA-MM-DD`, `git pull --rebase --autostash` y push, con hasta 4 reintentos;
   - respuesta final de 12 líneas o menos.
