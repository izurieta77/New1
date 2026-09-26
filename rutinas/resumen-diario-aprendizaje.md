# Rutina 7b · Resumen diario de aprendizaje (todos los días, 18:08 hora del centro de México)

Sesión: "Sistema de inversión · Motor de rutinas". No es un agente nuevo: lo escribe el orquestador de esa sesión, en primera persona, para el dueño.

Nace de una instrucción del dueño (25-sep-2026): quiere, cada noche, "tu resumen diario de aprendizaje" — no un reporte de mercado, sino qué aprendió el sistema hoy.

0. `git pull --rebase --autostash`. Lee `rutinas/REGLAS-MOTOR.md`.
1. **Reúne, con `git log --since="hoy 00:00" --stat` y los archivos que tocó cada commit, lo que se agregó o corrigió hoy en:**
   - `conocimiento/` (capítulos, fichas, `estado-de-dominio.csv`: qué tema subió de nivel);
   - `conocimiento/cripto/` (recursos estudiados, ideas nuevas, capítulos);
   - `laboratorio/` (réplicas, verificaciones, tabla maestra);
   - `empresas/` (fichas nuevas o actualizadas, pronósticos registrados);
   - `conocimiento/registro-de-errores.md` (errores propios corregidos hoy, con una línea cada uno: qué decía, qué es correcto).
2. **Escribe `bitacora/aprendizaje/AAAA-MM-DD.md`**, 15-25 líneas:
   - 3-5 cosas nuevas que el sistema sabe hoy que no sabía ayer, con su fuente y una cifra dura si la hay;
   - cuántos temas subieron de nivel en `estado-de-dominio.csv` y a qué nivel;
   - los errores propios corregidos hoy (nunca los de fuentes de terceros, esos viven en la ficha de cada recurso);
   - una idea que sigue sin resolverse (una pregunta abierta, no una duda operativa: esas van en `bitacora/decisiones-pendientes.md`).
3. **Añade una sección "Aprendizaje de hoy" de 6 líneas o menos** al brief del día (`bitacora/briefs/AAAA-MM-DD.md`) si existe; si no, créala solo con esa sección.
4. Nunca repitas cifras de mercado, boletas ni pronósticos: eso ya lo cubren el brief y el cierre. Esta rutina es sobre conocimiento, no sobre precios.
5. **Cierre de la rutina:**
   - latido;
   - commit `aprendizaje: AAAA-MM-DD`, `git pull --rebase --autostash` y push, con hasta 4 reintentos;
   - respuesta final de 6 líneas o menos.
