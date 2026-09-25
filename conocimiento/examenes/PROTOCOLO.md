# Protocolo de exámenes de titulación

> Registrado el 25-sep-2026, **antes** de conocer cualquier calificación del examen diagnóstico. La fecha del commit la pone GitHub. Cualquier cambio posterior se agrega como adenda fechada; este texto no se reescribe.

## 1. Criterio de aprobación (todas las secciones)

- **90% o más del puntaje global** y **85% o más en cada una de las 7 secciones (S1–S7)**.
- Este umbral de 85% por sección sustituye al 80% que tenían las secciones S1–S5 al lanzarse. Se fija antes de ver sus resultados.
- Una sección por debajo de 85% no se compensa con otra: el examen queda **no aprobado** aunque el global pase de 90%.

## 2. Integridad de la clave: qué garantiza cada sección

| Secciones | Mecanismo | Qué demuestra | Qué NO demuestra |
|---|---|---|---|
| S1–S5 | La clave vive solo en la memoria del flujo de trabajo y se escribe en disco hasta después de las respuestas | Que el sustentante no pudo leerla en disco mientras contestaba | Que la clave no se ajustó después de ver las respuestas: **no hubo compromiso público previo** |
| S6–S7 | Clave cifrada AES-256 (PBKDF2, 200,000 iteraciones) y huella SHA256 **por pregunta** y del archivo, en un commit de GitHub **antes** de contestar. La contraseña se revela al final | Que la clave no cambió: cualquiera descifra el archivo de ese commit y recalcula las huellas | Aislamiento perfecto en la máquina: se garantiza por las reglas y por la auditoría del registro de la sesión |

Consecuencia: en el reporte, las calificaciones de S1–S5 se presentan con la etiqueta **"sin compromiso público previo"**. Desde la ronda de recuperación, **todas** las secciones usan el mecanismo de S6–S7.

## 3. Libro cerrado

El sustentante (`.claude/agents/examinado.md`) no tiene herramientas web y tiene prohibido usar la red desde Bash y leer `conocimiento/examenes/`. Después de cada examen se audita el registro completo de la sesión del sustentante, buscando llamadas a WebSearch o WebFetch, curl o wget, direcciones http y lecturas de `examenes/` o de rutas fuera del repositorio. El resultado de esa auditoría se publica con el acta.

## 4. Intercambio de bancos con otros sistemas (aceptado)

Propuesta recibida el 25-sep-2026: cada sistema contesta el banco de preguntas del otro, con las mismas preguntas para ambos, y se califica con la clave de quien las escribió.

Reglas que proponemos para que el intercambio sea justo y verificable:

1. **Compromiso previo de ambos bancos.** Antes del intercambio, cada sistema publica la huella SHA256 de su banco completo (preguntas y clave) en un lugar con fecha que no controle (en nuestro caso, un commit de GitHub). Así nadie puede cambiar su clave después de ver las respuestas del otro.
2. **Se entregan solo las preguntas.** La clave se revela después de recibir las respuestas.
3. **Mismas condiciones** para los dos: libro cerrado, cada uno con su propia base, sin internet, y con auditoría del registro de la sesión.
4. **Calificación con la clave del autor**, con rúbrica publicada.
5. **Apelaciones:** si el que contesta demuestra con una fuente primaria que una clave está mal, la pregunta la resuelve un tercero neutral: el dueño o un tercer sistema acordado. La pregunta no se anula por conveniencia de nadie.
6. **Reporte simétrico:** calificación global y por sección de cada sistema en los dos bancos (el propio y el ajeno), con todas las respuestas publicadas.
7. **El dueño hace de canal.** Los bancos y las respuestas pasan por él, y conserva una copia de cada archivo con su huella.

Nuestro banco para el intercambio se publica en `conocimiento/examenes/<fecha>-diagnostico/banco-intercambio.md` (solo preguntas) y su huella en `banco-intercambio.sha256`, en cuanto termine la revelación de todas las secciones.
