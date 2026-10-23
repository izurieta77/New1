# Investigador, corrida vespertina · 2026-10-22 (20:12 CDMX; 2026-10-23 02:13 UTC del 23-oct)

**Barrido corto, turno fiscal** (doctorados, una de cada tres). Rotación: 19-oct fiscal, 20-oct riesgo, 21-oct cripto.

## Búsquedas
1. **Gaceta Parlamentaria de Diputados (fuente primaria, HTTP 200):**
   - índice del 14-oct (Gaceta 7146), con las votaciones de la sesión del 13-oct;
   - página de votaciones `gp66_a3primero.html`;
   - índices de reservas 7145-RB y 7145-RC.
2. **Dictamen de la LIF 2027 y reservas de Morena:**
   - Descargué el dictamen (7145-IV-2, 254 pp., sha256 `ffb6b66d309a…`) y las reservas de Morena (7145-RC-1, `dd52c0f2f0c0…`). Los dos son **escaneados, sin capa de texto**. Instalé RapidOCR en el scratchpad, pero las imágenes salen mal decodificadas al extraerlas, así que no hay texto legible.
   - También descargué el dictamen de la LISR (7145-IV-1, `3532bb0c1e11…`), pero no lo procesé.
3. **Senado:** `comunicacion.senado.gob.mx`, `senado.gob.mx` e `infosen` responden 403 desde este entorno. Usé prensa: búsqueda web y Por Esto del 20-oct.
4. **DOF:** `www.dof.gob.mx` falla la verificación TLS (el certificado no coincide con el nombre del host). Sin consulta.

## Hallazgo (grado A en el trámite, fuente primaria)
**Gaceta Parlamentaria, votaciones del martes 13-oct-2026:**
- **LIF 2027:** aprobada en lo general con **331-118 el 13-oct**. En lo particular pasó en términos del dictamen, con una **modificación al artículo vigésimo transitorio** (propuesta de Monreal). Se turnó al Senado.
- **Reforma a la LISR:** aprobada con 349-118 el mismo día y turnada al Senado.
- **Senado:** al 23-oct, la página no registra su aprobación.
  - Según la prensa (C), las comisiones recibieron la minuta el 20-oct y el pleno está previsto para el 27-oct, con plazo al 31-oct.

**Corrige lo nuestro:**
- El §9.9 del cap. 33 decía 14-oct; la fecha correcta es el **13-oct**.
- El §9.10 decía que no había texto primario de la iniciativa y le daba grado C, pero el cap. 32 §2.8 ya lo había leído en el PDF primario. La mecánica es **grado A como iniciativa**.

Escribí la adenda §9.11 en el cap. 33, una adenda corta en el cap. 27 y una fila en el registro de errores.

## Qué cambia
- **Para la cartera:** nada.
  - No pude verificar si el dictamen tocó el art. 129 (SIC al 10%) o la retención sobre intereses (0.68% en la iniciativa), porque el PDF no se puede leer.
  - Ningún parámetro cambia hasta que se publique en el DOF.
- **Para la estación:** nada operativo, y la preparación del §9.10 sigue.
  - **Queda abierto:** el contenido del vigésimo transitorio modificado y si la fr. XIX del art. 25 llegó igual al dictamen. Va a decisiones pendientes.
- **Registro de errores:** una fila, por la fecha y el grado del §9.9 y §9.10, sin efecto operativo.
