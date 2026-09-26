# Rutina 2c · Investigador permanente, corrida vespertina (todos los días, 20:12 hora del centro de México)

Sesión: "Sistema de inversión · Motor de rutinas". Agente: `investigador-academico` (`.claude/agents/investigador-academico.md`).

Nace de una instrucción del dueño (25-sep-2026): que el investigador académico no espere al laboratorio (L-V 11:47) ni al barrido trimestral: una corrida corta, todos los días, para no perder un paper importante entre trimestres.

0. `git pull --rebase --autostash`. Lee `rutinas/REGLAS-MOTOR.md`.
1. **Barrido corto** (no el barrido trimestral completo): revisa qué hay nuevo desde ayer en SSRN (Financial Economics eJournal), arXiv q-fin (cs.CE si toca cripto) y NBER, con dos o tres búsquedas dirigidas a los temas que hoy sostienen una regla del sistema (cortacircuitos, tamaño de posición, filtro de tendencia, prima cripto).
2. **Si hay un paper que cambia algo:** agrégalo al capítulo que corresponda con grado A-D y nota fechada, y anótalo en `conocimiento/registro-de-errores.md` si corrige algo nuestro. Si no hay nada que cambie algo, dilo así y no fuerces una entrada.
3. **Presupuesto:** máximo un paper por corrida, verificado de verdad (no solo el abstract), mejor que cinco por encima. El barrido profundo semestral sigue siendo el trimestral (rutina 6).
4. **Cierre de la rutina:**
   - latido;
   - commit `investigador-vespertino: AAAA-MM-DD` solo si hubo cambios, `git pull --rebase --autostash` y push, con hasta 4 reintentos;
   - respuesta final de 4 líneas o menos.
