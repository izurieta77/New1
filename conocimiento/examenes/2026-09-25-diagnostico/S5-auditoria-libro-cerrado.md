# S5: auditoría de libro cerrado del sustentante

- **Registro auditado:** `agent-ac00d28501e72e8db.jsonl` del flujo `wf_c811d0cd-ef0`.
- **Herramientas usadas:** Bash 46 veces, Read 8 veces y StructuredOutput 1 vez.
- **Acceso a internet:** **0 usos** de WebSearch, WebFetch, ToolSearch, curl, wget o URLs.
- **Única bandera, revisada a mano:**
  - Comando: `grep -rn ... conocimiento/ --include=*.md | grep -v "/examenes/" | head -20`.
  - Lo que hizo: el `grep` recorrió `conocimiento/` completo, pero su salida pasó por `grep -v "/examenes/"`, así que el sustentante no vio ninguna línea de `examenes/`.
  - La clave de S5 no pudo filtrarse: no estaba en disco, sino en la memoria del flujo hasta el acta.
  - Lo que había en `examenes/` en ese momento no era de S5: actas de otras secciones y claves cifradas de S6 y S7.
- **Veredicto:** sin violaciones.
- **Lección para el protocolo:** en la ronda formal, la carpeta de exámenes sale del repositorio de trabajo mientras se contesta, para que ni siquiera una búsqueda recursiva la toque.
- **Nota:** según el propio sustentante, 3 de 12 respuestas se apoyaron en la base del repositorio.
