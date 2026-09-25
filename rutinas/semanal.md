# Rutina 4 · Auditoría semanal (viernes, 16:47 hora del centro de México)

Este procedimiento escrito manda sobre el texto del disparador, que ya indica seguirlo si existe.

0. Tras el `git pull --rebase --autostash`, lee `rutinas/REGLAS-MOTOR.md` y cúmplelo: autonomía, bloqueos, latido y pendientes (§7).
1. **Qué se agregó en la semana** (`git log --since="7 days ago" --stat`): capítulos, fichas, réplicas, empresas, pronósticos, decisiones.
2. **Pronósticos:**
   - vencidos y calificados;
   - Brier acumulado, y por autor y tipo;
   - calibración;
   - cobertura de los intervalos de 80% en los numéricos;
   - habilidad frente a los mercados de predicción.
3. **Estado de dominio:** cuántos temas subieron de nivel, comparando `conocimiento/estado-de-dominio.csv` contra su versión de hace 7 días en git.
4. **Auditoría adversarial:** elige 3 afirmaciones importantes agregadas esta semana e intenta refutarlas con los subagentes `verificador` y `abogado-del-diablo`. Corrige y registra los errores.
5. **Portafolio de papel frente a benchmarks y rivales:**
   - benchmarks: CETES 28, S&P 500 en MXN e IPC;
   - rivales: los de `competencia/rivales.csv`;
   - métricas: TWR, drawdown y Sharpe.
6. **Comité semanal de cartera:**
   - Solo si la última decisión de cartera tiene al menos 5 días hábiles. Corre la skill `comite-de-inversion` sobre la cartera vigente: mantener, ajustar o rotar.
   - Aplica el modo torneo de `arena_agresivo`: adelante del mejor rival reportado, reducir varianza; atrás, subir exposición dentro de los límites.
   - Las órdenes van a `bitacora/ordenes-pendientes.csv` para la apertura del siguiente día hábil. Respeta `operaciones_max_mes` y `rotacion_max_mensual_x_capital`.
7. **Plan:** actualiza la sección "Avance" de `PLAN.md` con números (REGLAS §6).
8. **Radar de literatura** con el subagente `investigador-academico`: 3–5 papers de la semana, cada uno con una línea y su grado.
9. **Cierre de la rutina:**
   - escribe `bitacora/semanal/AAAA-Www.md` con el plan de la semana siguiente;
   - deja el latido;
   - commit `auditoria semanal: AAAA-Www`, pull --rebase y push;
   - respuesta final de 12 líneas o menos, con los números clave.
