# S1: auditoría de libro cerrado del sustentante

- **Registro auditado:** `agent-aa6b1459fc26c1fee.jsonl`, del flujo `wf_e4e8e3cb-4ef`.
- **Herramientas usadas:** Bash (19), Read (10), Grep (7), StructuredOutput (1).
- **WebSearch, WebFetch y ToolSearch:** **0 usos**. Tampoco hay curl, wget ni URLs en comandos.
- **Posibles banderas revisadas (6):** cinco Grep que **excluyen** de forma explícita `conocimiento/examenes/**` y una lectura (Bash `grep`) del archivo `tool-results/toolu_01B8…txt`. Ese archivo es la salida de un Grep anterior del **propio sustentante** sobre el repositorio (se verificó su contenido: líneas de `conocimiento/16` y `conocimiento/02`). No contiene claves.
- **Dónde estaba la clave:** S1 no tiene compromiso público. Su clave vivió solo en la memoria del flujo de trabajo y se escribió en disco hasta el acta, después de las respuestas.
- **Veredicto:** sin violaciones de libro cerrado.
- **Nota de interpretación:** según el propio sustentante, 5 de 12 respuestas se apoyaron en la base del repositorio. Las demás salieron de su conocimiento sin internet. La calificación mide ambas cosas juntas.
