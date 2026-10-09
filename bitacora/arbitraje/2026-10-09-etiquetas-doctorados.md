# Arbitraje · 2026-10-09 · Etiqueta de cobertura de D7 (y D10) en ESTADO de los doctorados

Origen: hallazgo 4.2 de `bitacora/revisiones/2026-10-08.md`. Es una regla que choca con otra: la leyenda de ESTADO contra la etiqueta usada.

## Posiciones
- `conocimiento/doctorados/ESTADO.md` L29 (commit `bb1a623`) y `estado-de-dominio.csv`, fila D7: "**Documentado con comprobación**".
- Revisor: esa etiqueta no existe en la leyenda; según la leyenda, D7 es **Parcial**.

## Fuente primaria (las reglas del propio repo)
- **Leyenda de ESTADO (L3):** "Sin = nada; **Parcial = hay material, pero no cubre el área**; Capítulo = capítulo escrito sin ficha comprobada; Comprobada = capítulo y ficha con ejercicio".
- **Área D7 (L29):** "tratados, residencia, fuente de riqueza, regímenes fiscales preferentes, FATCA/CRS". La ficha del 8-oct cubre fuente de riqueza (art. 1), el art. 129 y el 176. No cubre tratados, residencia ni FATCA/CRS, no hay capítulo y falta el criterio sobre la entidad extranjera (ficha L43).
- **Niveles de `estado-de-dominio.csv`** (`rutinas/diaria-laboratorio.md` L7): Pendiente, Localizado, Documentado, Comprendido con comprobación, Contrastado y Replicado. "Documentado con comprobación" tampoco es un nivel de esa escala: mezcla dos.
- **Mismo defecto en D10 (L32, del 9-oct):** "Localizado" es un nivel de la escala del CSV, no una cobertura de ESTADO.

## Fallo
- **ESTADO D7 → Parcial.** La única etiqueta de la leyenda que corresponde es "Parcial": hay material, pero no cubre el área.
- **ESTADO D10 → Parcial**, por la misma regla.
- **Resumen de derecho fiscal**, recontado contra la tabla: 0 Comprobada, 5 Capítulo (D2-D6), 5 Parcial (D1, D7-D10) y 1 Sin (D11). Antes decía 0/1/4/6, una cifra vieja.
- **`estado-de-dominio.csv`, D7 y D1** (D1 trae la misma etiqueta inexistente): pasan a "**Documentado**", el nivel válido inmediato inferior, que es la opción conservadora. Suben a "Comprendido con comprobación" cuando se cumpla su `siguiente_prueba`.

No se toca el mandato ni se declara ninguna graduación (REGLAS §0d).

## Correcciones
`conocimiento/doctorados/ESTADO.md` (L29, L32 y resumen, con nota fechada), `conocimiento/estado-de-dominio.csv` (dos filas, con nota en la evidencia) y `conocimiento/registro-de-errores.md`.
