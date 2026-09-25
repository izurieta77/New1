# Examen diagnóstico de titulación, 25-sep-2026

> Protocolo: `conocimiento/examenes/PROTOCOLO.md`, registrado a las 05:43:30 UTC, antes de conocer cualquier resultado. Para aprobar se exige **90% global y 85% en cada sección**.

## Resultado: APROBADO (diagnóstico)

| Sección | Examinador externo | Puntos | % | Integridad de la clave | Libro cerrado (auditoría del registro) | Respuestas apoyadas en la base |
|---|---|---|---|---|---|---|
| S1 Fundamentos y maestría (CFA I-III) | 1 | 57.50 / 60 | 95.8% | Retenida en memoria, sin compromiso público | Limpio | 5/12 |
| S2 Doctorado: asset pricing y econometría | 1 | 58.00 / 60 | 96.7% | Retenida en memoria, sin compromiso público | Limpio | 2/12 |
| S3 Evidencia empírica y réplica | 1 | 57.50 / 60 | 95.8% | Retenida en memoria, sin compromiso público | Limpio | 8/12 |
| S4 México, GBM, fiscalidad y riesgo | 1 | 57.50 / 60 | 95.8% | Retenida en memoria, sin compromiso público | Limpio | 5/12 |
| S5 Empresas, geopolítica y pronóstico | 1 | 57.00 / 60 | 95.0% | Retenida en memoria, sin compromiso público | Limpio (con 1 observación de protocolo) | 3/12 |
| S6 Laboratorio con datos crudos | 1 | 57.50 / 60 | 95.8% | **Compromiso público en GitHub** (`6c526b6`, 06:02:26 UTC), verificado de forma externa | Limpio | n/d |
| S7 Frontera: ML, microestructura, derivados | 1 | 58.75 / 60 | 97.9% | **Compromiso público en GitHub** (`2a50ca2`, 06:03:15 UTC), verificado de forma externa | Limpio | n/d |
| **Total** | **7** | **403.75 / 420** | **96.1%** | | | |

- Cada sección tuvo **dos calificadores independientes** y un árbitro. En S6 y S7 hubo además calificación automática de cifras y **defensa oral** con abogado del diablo.
- En la defensa se descontaron 2.0 puntos en S6 (preguntas 01, 02 y 04) y 0 en S7.
- Las actas por sección con enunciado, clave, fuente, respuesta, calificaciones y huecos están en `S1.md` a `S5.md` y en `S6/acta.md` y `S7/acta.md`. Las auditorías de libro cerrado están en `S*-auditoria-libro-cerrado.md` y las verificaciones externas en `S6/` y `S7/`.

## Qué NO demuestra este resultado (sin maquillar)

1. **S1 a S5 no tienen compromiso público previo.** Nada prueba desde afuera que sus claves no cambiaron. Sí lo prueban S6 y S7.
2. **Gran parte de las respuestas salió del conocimiento propio del modelo, sin internet, y no de la base.** En S2 solo 2 de 12 se apoyaron en la base. Esto mide la competencia del sustentante, no la cobertura de la base.
3. **Examinadores, sustentante y calificadores son de la misma familia de modelos.** Pueden compartir puntos ciegos. La prueba externa de verdad es el **intercambio de bancos** con otros sistemas (ver `PROTOCOLO.md` §4).
4. **La calificación automática de S6 tuvo 6 falsos negativos.** El extractor tomó el número equivocado en preguntas de varias partes. El árbitro recalculó desde los datos congelados y confirmó que las respuestas daban el valor comprometido. Corrección para la próxima ronda: el examinador define un campo numérico **por inciso**, con su nombre.
5. **Observaciones de protocolo:**
   - Una búsqueda recursiva del sustentante tocó `examenes/`, aunque filtró esas líneas antes de verlas.
   - En S6, `clave.enc` entró en un commit de sincronización (`5909c87`, 06:02:03 UTC) antes que `compromiso.json` (`6c526b6`). Los dos llegaron antes de las respuestas.
   - Corrección: durante la respuesta, la carpeta de exámenes sale del repositorio de trabajo y el compromiso va en **un solo commit**.
6. **Aprobar un examen no demuestra que se pueda ganar dinero.** Eso solo se demuestra con pronósticos calificados y con el portafolio de papel.

## Huecos a cerrar (ronda de remediación)

- **S7-02:** magnitudes exactas de Kelly-Malamud-Zhou ("virtue of complexity": mejora ≈0.47 de Sharpe, t≈3) y de sus críticas (Buncic 0.699 frente a 0.485; Elmore-Strauss 97.5%). También el hallazgo de Gu-Kelly-Xiu de que la media histórica infla el R² en ≈3 pp.
- **S7-12:** magnitudes de los efectos de las opciones 0DTE (Adams-Fontaine-Ornthanalai 60-90 pb; Amaya et al.; Brogaard-Han-Won 9.10%).
- **S6-01, S6-02, S6-04:** errores de razonamiento que exhibió la defensa oral:
  - el RF de los factores regionales de French es la T-bill de EUA a 1 mes;
  - el peso Bartlett de γ₆;
  - la dirección del sesgo del error estándar con benchmark fijo.
- **S1 a S5:** los descuentos parciales de cada acta (preguntas con 4.0 a 4.75 puntos).
