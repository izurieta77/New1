# Horarios de agentes de la competencia (registro de inteligencia)

**Fecha del registro:** 25-sep-2026, sesión principal. **Fuente:** el dueño describió de memoria un patrón de horarios que observó correr en un rival, sin nombrarlo explícitamente (confirmó "ambas cosas" cuando se le preguntó si venía de un rival y si quería que lo adoptáramos). No es una cita textual del rival ni un documento suyo: es lo que el dueño reportó haber visto.

## Lo reportado

Secuencia observada, hora del centro de México (asumida; el dueño no precisó zona horaria, pero coincide con la nuestra):

| Hora | Paso, según el dueño |
|---|---|
| 5:57 pm | El revisor, en su primera corrida. Revisa los hallazgos pendientes del investigador y del agente cripto |
| 6:08 pm | Resumen diario de aprendizaje |
| 6:42 pm | El agente cripto |
| 7:09 pm | El bloque de trabajo continuo, que sigue con la cola de tareas del plan |
| 7:27 pm | El agente de decisiones, en su primera corrida, con la cartera de papel |
| 8:12 pm | El investigador permanente |
| 8:57 pm | El agente de arbitraje, en su primera corrida |
| 9:42 pm | El agente de supervisión, en su primera corrida. Revisa que todos hayan cumplido |

## Qué es hecho, qué es inferencia

- **[H]** El dueño reportó esta secuencia y confirmó que la vio correr en un rival.
- **[I]** Cuál rival (ChatGPT, Grok o Barebone AI) no quedó especificado. Sin ese dato no se puede verificar de forma independiente (no hay un panel público de ninguno de los tres que hayamos podido auditar hasta ahora).
- **[I]** Los minutos no redondos (57, 08, 42, 09, 27, 12, 57, 42) son compatibles con una práctica común de jitter para evitar que varias tareas disparen a la misma hora en punto; no prueban ni descartan que sea de un rival real, porque es la misma práctica que ya usábamos nosotros antes de este registro.
- **[I]** Los pasos "primera corrida" (revisor, decisor, arbitraje, supervisor) sugieren un arranque diario de una secuencia, no necesariamente una operación continua 24/7 como la nuestra en cripto e inteligencia.

## Qué adoptamos y qué no

Adoptamos la **secuencia y el espaciamiento** (una cascada vespertina de 8 pasos, de 17:57 a 21:42, todos los días), mapeada a nuestros propios agentes existentes (`rutinas/REGLAS-MOTOR.md` §0b). No adoptamos a ciegas:

- no movimos la supervisión de mercado (rutina 9, L-V 08:40-14:40): esa vigilancia tiene que ocurrir durante el horario bursátil, no una vez en la noche, porque un cortacircuito o un stop se dispara en vivo;
- no comprimimos el estudio de cripto en un solo bloque nocturno: mantuvimos el pulso cada 4 horas (rutina 8) y solo movimos su último pulso del día para que caiga dentro de la cascada;
- no le dimos al decisor vespertino poder de rebalancear: sigue rigiendo la regla de `REGLAS-MOTOR.md` §4 (solo el viernes, con 5 días hábiles de por medio).

## Pendiente

[I] Podría ser ChatGPT: su protocolo (`08-chatgpt-protocolo-maquiavelo.md`) dice "rutinas activas" desde la versión 1.1. No confirmado.

Si el dueño precisa cuál rival mostró este patrón, se agrega aquí y se compara contra lo que ya sabemos de él en `06-barebone-ai-competidor.md` o en `competencia/rivales.csv`.
