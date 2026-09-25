---
name: post-mortem
description: Evalúa una decisión, pronóstico o reporte trimestral ya resuelto; separa calidad de decisión de suerte, califica a cada agente del comité y registra lecciones y errores.
---
# Post-mortem

1. **Recupera lo registrado antes del resultado.** No reconstruyas de memoria: usa la tesis, los dictámenes, los votos y los pronósticos originales que están en `bitacora/decisiones/` y en los ledgers.
2. **Resultado real** con fuente primaria. Resuelve los pronósticos con `python3 herramientas/pronosticos.py resolver ...`.
3. **Matriz decisión × resultado:** buena decisión y buen resultado, buena decisión y mal resultado (mala suerte), mala decisión y buen resultado (suerte), o mala decisión y mal resultado.
4. **Qué se sabía y qué no se podía saber** en la fecha de la decisión.
5. **Calificación por agente.** Indica si su voto y su confianza fueron correctos y actualiza `competencia/calibracion-agentes.csv` con estas columnas: fecha, decisión, agente, voto, confianza, correcto (1/0).
6. **Lecciones.** Cada una debe cambiar algo concreto: una regla, un parámetro propuesto, un capítulo o un checklist. Los errores de hecho van a `conocimiento/registro-de-errores.md`.
7. **Escribe** `empresas/<TICKER>/post-mortem-AAAA-MM-DD.md` o `bitacora/decisiones/<...>-post-mortem.md`.
