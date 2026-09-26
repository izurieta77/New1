# Rutina 2b · Bloque de trabajo continuo (todos los días, 19:09 hora del centro de México)

Sesión: "Sistema de inversión · Motor de rutinas". La ejecuta el orquestador de esa sesión, con los subagentes que hagan falta.

Nace de una instrucción del dueño (25-sep-2026): un bloque diario que **sigue con la cola de tareas del plan**, para que el trabajo de fondo (que no depende del calendario de mercado) no espere a que alguien lo pida.

0. `git pull --rebase --autostash`. Lee `rutinas/REGLAS-MOTOR.md`.
1. **Elige UNA tarea** de la cola, en este orden de prioridad:
   - tareas del sistema de tareas (`TaskList`) marcadas `in_progress` que no avanzaron en las últimas 24 horas;
   - huecos que la auditoría semanal o la revisión de calidad hayan dejado anotados como pendientes;
   - la tarea de mayor valor de `estado-de-dominio.csv` en el nivel más bajo (igual que el laboratorio, pero sin limitarse a un tema del laboratorio: puede ser una ficha de empresa, un capítulo de conocimiento, una réplica o una pregunta del banco de examen).
2. **Avánzala de verdad en esta corrida**, no solo la anotes: un capítulo, una ficha, una réplica, una verificación. Verifica dos veces cualquier cifra antes de escribirla.
3. **Actualiza el sistema de tareas** (`TaskUpdate`) y `estado-de-dominio.csv` si aplica.
4. **No toques** nada de mercado (boletas, cortacircuitos, cartera): eso es de las otras rutinas. Si encuentras algo urgente de mercado, anótalo en `bitacora/decisiones-pendientes.md` y sigue con tu tarea.
5. **Presupuesto:** una tarea por corrida, bien hecha, mejor que varias a medias. Si la tarea es grande, dilo y dónde la dejaste, para continuar mañana.
6. **Cierre de la rutina:**
   - latido;
   - commit `trabajo-continuo: AAAA-MM-DD` con el nombre de la tarea, `git pull --rebase --autostash` y push, con hasta 4 reintentos;
   - respuesta final de 6 líneas o menos: qué tarea, qué avanzó, qué falta.
