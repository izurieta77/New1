# Rutina 2 · Laboratorio de estudio (L-V, 11:47 hora del centro de México)

Este procedimiento escrito manda sobre el texto del disparador, que ya indica seguirlo si existe.

0. Tras el `git pull --rebase --autostash`, lee `rutinas/REGLAS-MOTOR.md` y cúmplelo: autonomía, bloqueos, latido y pendientes (§7).
   - **Objetivo:** subir de nivel los temas de `conocimiento/estado-de-dominio.csv`.
   - **Niveles:** Pendiente, Localizado, Documentado, Comprendido con comprobación, Contrastado, Replicado.
1. Si no existe `conocimiento/estado-de-dominio.csv`, créalo con las columnas `tema,capitulo,estado,evidencia,fecha,siguiente_prueba` y los temas principales de `conocimiento/`.
2. **Elige un tema:** el de mayor valor con el estado más bajo. Da prioridad a los que sostienen reglas de riesgo o la cartera de papel vigente.
3. **Escribe `conocimiento/fichas/AAAA-MM-DD-<tema>.md`** con:
   - pregunta;
   - fuente y versión, con el nivel de acceso real (lectura íntegra, sección o resumen);
   - supuestos y derivación;
   - ejercicio numérico comprobado en Python;
   - evidencia empírica y límites;
   - contraejemplo y segunda comprobación;
   - estado nuevo.
4. **Avanza UNA réplica.** Puede ser nueva o la doble ejecución independiente de una existente, con el subagente `auditor-de-replicas`: código desde cero e, idealmente, una segunda fuente de datos.
   - Actualiza `laboratorio/tabla-maestra.md` con periodo, instrumento, benchmark, dividendos, moneda, FX, costos, impuestos y resultados A y B.
   - Etiqueta: descartada, oportunidad investigable o ventaja demostrada.
   - **Estado de la réplica:** rige la más conservadora de A y B.
5. Si detectas errores, corrígelos y anótalos en `conocimiento/registro-de-errores.md`.
6. Verifica un paper reciente pendiente y agrégalo al capítulo que corresponda, con grado A–D.
7. **Cierre de la rutina:**
   - deja el latido (REGLAS §3);
   - commit `laboratorio: AAAA-MM-DD`, pull --rebase y push;
   - respuesta final de 8 líneas o menos.
