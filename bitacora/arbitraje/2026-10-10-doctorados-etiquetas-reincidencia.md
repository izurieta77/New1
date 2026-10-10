# Arbitraje · 2026-10-10 · Etiquetas y áreas de los doctorados: reincidencia de "Documentado con comprobación" (D8), D10/D11 mal acreditadas y fecha de ESTADO

Materia: una regla que choca con su uso. Son los hallazgos 5.1 a 5.4 de `bitacora/revisiones/2026-10-09.md` y el commit `d2bd959` de hoy. Precedente: `2026-10-09-etiquetas-doctorados.md`.

## Posiciones
- **`d2bd959`** (trabajo continuo, 10-oct 01:10 UTC): D8 pasa "de Parcial a Documentado con comprobación" en `ESTADO.md` y en la ficha del 10-oct.
- **Laboratorio** (`e56739b`): ficha PFIC, "D10 pasa ... a **Localizado con texto de EUA**". La fila D10 de `ESTADO.md` sigue diciendo "PFIC de EUA pendiente" y acredita a D10 los arts. 4-B y 176-178 LISR.
- **Revisor:** la fecha de ESTADO sigue en el 5-oct; el nivel "Localizado con texto de EUA" no existe; los arts. 176-178 son de D7; D11 sigue en "Sin" mientras el CSV agrupa "D10-D11".

## Fuente primaria (reglas del repo)
- **Leyenda de `ESTADO.md` L3:** coberturas Sin, Parcial ("hay material, pero no cubre el área"), Capítulo y Comprobada. Las filas "Sin" y "Parcial" llevan su tema en `estado-de-dominio.csv`, en "Pendiente" o "Documentado".
- **`rutinas/diaria-laboratorio.md` L7, niveles del CSV:** Pendiente, Localizado, Documentado, Comprendido con comprobación, Contrastado y Replicado.
- **Área D7:** "tratados, residencia, fuente de riqueza, **regímenes fiscales preferentes**, FATCA/CRS". **D8:** "SIC, ETFs extranjeros y apalancados, derivados, cripto". **D10:** "venta ficticia, *wash sale*, PFIC, contratos 1256". **D11:** "cláusula general antiabuso, razón de negocios".
- **Ficha D8 del 10-oct, sección Límites:** no leyó el art. 16-C CFF ni la RMF, y "la cripto ... queda sin ficha". Tiene ejercicio con código.
- **Ficha del 9-oct "D10-D11 (parcial)":** cubre los arts. 4-B y 176-178 LISR (preferentes y transparencia) y no toca el art. 5-A CFF.

## Fallo
1. **D8 → Parcial.** "Documentado con comprobación" no es una cobertura de ESTADO ni un nivel del CSV. Es la misma etiqueta que se falló el 9-oct para D7: **reincidencia**. La ficha cubre el art. 129 (SIC), pero no apalancados, derivados ni cripto, así que no cubre el área. En el CSV, D8 no tenía fila: se agrega con nivel "Documentado".
2. **Arts. 4-B y 176-178 → D7.** Se acreditan en la fila D7 de ESTADO y en el CSV. D7 sigue Parcial.
3. **D10:** la fila acredita la ficha PFIC (§§1291 y 1297 leídos) y quita "PFIC pendiente". Sigue **Parcial** en ESTADO y **Localizado** en el CSV. La ficha PFIC queda corregida: "Localizado con texto de EUA" pasa a "Localizado".
4. **D11:** sigue **Sin**. Ninguna ficha trata el art. 5-A CFF. En el CSV se separa de D10 como fila propia en "Pendiente".
5. **Fecha de ESTADO** → 2026-10-10, con nota.
6. **Resumen:** no cambia (0/5/5/1 en derecho fiscal). Con D8 en una etiqueta inválida, el resumen no cuadraba con la tabla; ahora sí.
7. **Fuera de este fallo, para el orquestador:** `estado-de-dominio.csv` tiene otras seis filas con "Documentado con comprobación" (tres de cripto, dos de ellas contadas por la W41 como "subieron de nivel"; C1; cap. 28 y contabilidad gerencial). O la escala de `diaria-laboratorio.md` se amplía o esas filas se corrigen. Es una regla de escala, así que lo dejo anotado en decisiones-pendientes y no lo cambio en bloque.

No se declara ninguna graduación y el mandato no se toca (REGLAS §0d).

## Correcciones
`conocimiento/doctorados/ESTADO.md` (L3, D7, D8 y D10), `conocimiento/estado-de-dominio.csv` (D7 con nota; D8 nueva; D10 separada; D11 nueva), `conocimiento/fichas/2026-10-09-doctorado-fiscal-d10-pfic-eua.md` L29, `conocimiento/fichas/2026-10-10-doctorado-fiscal-d8-sic-costo-y-perdidas.md` (Estado nuevo) y `conocimiento/registro-de-errores.md`.
