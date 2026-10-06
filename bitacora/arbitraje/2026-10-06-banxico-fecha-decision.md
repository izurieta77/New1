# Arbitraje · 2026-10-06 (conciliación de la noche del 5-oct) · ¿El 8-oct es una decisión de Banxico o la publicación de minutas?

## Caso

El primer paquete diario del dueño (`datos/entrada-dueno/2026-10-05.md`, entrada 1 y tabla de verificación) afirma, citando a un subgobernador de Banxico (Omar Mejía, vía SDP Noticias): **"Próxima decisión de política monetaria: 8 oct 2026."** La corrida de inteligencia que procesó el paquete marcó esto como **conflicto**: nuestra propia inteligencia (`bitacora/inteligencia/2026-09-25.md` y varias corridas posteriores) registra que Banxico **mantuvo la tasa en 6.50% el 24-sep-2026** (tercera vez consecutiva, voto unánime) y que la siguiente decisión programada era el **5-nov-2026**. La entrada quedó abierta en `bitacora/decisiones-pendientes.md` (2026-10-06 · primer paquete diario del dueño) con la nota "esperar el calendario oficial".

## Posiciones

1. **Paquete del dueño:** el 8-oct-2026 es la próxima *decisión* de política monetaria de Banxico.
2. **Inteligencia propia (24/25/26/27/29-sep, varias corridas, grado B — El Financiero, Proceso, The Rio Times, El Universal, Reuters vía agregadores):** Banxico ya decidió el 24-sep (mantuvo 6.50%); la siguiente decisión programada es el 5-nov-2026; el 8-oct sería, en su caso, la publicación de las **minutas** de la reunión del 24-sep, no una decisión nueva.

## Qué se consultó (fuente primaria)

- `www.banxico.org.mx/publicaciones-y-prensa/anuncios-de-las-decisiones-de-politica-monetaria/...` redirige (302) a `anterior.banxico.org.mx`, que devolvió 404 al intentar leer el calendario directamente en esta corrida (sin acceso de lectura exitoso al HTML del sitio oficial desde este entorno).
- Búsqueda dirigida (`WebSearch`) sobre el calendario de 2026 de anuncios de decisión de Banxico: el resultado agregado, sintetizando fuentes de mercado (BBVA Research, Monex, FXStreet, mnimarkets.com, calendarios de bancos) da las **ocho fechas de 2026**: 5-feb, 26-mar, 7-may, 25-jun, 6-ago, **24-sep**, **5-nov**, 17-dic. No hay ninguna fecha de decisión en octubre.
- Búsqueda dirigida sobre la minuta del 8-oct-2026: no se localizó el documento exacto, pero sí se confirmó el patrón de calendario de Banxico (`banxico.org.mx/publicaciones-y-prensa/minutas-de-las-decisiones-de-politica-monetaria/...`): las minutas se publican **dos jueves después** de la decisión correspondiente (ejemplo verificado: decisión 6-ago-2026 → minuta fechada 21-ago-2026, un fxstreet.com del 21-ago "Banxico minutes show split vote..."). El 24-sep-2026 es jueves; dos jueves después es el **8-oct-2026**, también jueves — coincide exactamente con el patrón.
- Esto es consistente y corrobora, por una vía independiente (búsqueda fresca de hoy), lo que la inteligencia propia ya tenía registrado desde el 25-sep (`bitacora/inteligencia/2026-09-25.md`, calendario de la semana: "la siguiente decisión programada es el 5-nov-2026") y reconfirmado el 27-sep y el 1-oct (`bitacora/inteligencia/2026-09-27.md`, `2026-10-01.md`).

## Fallo

1. **El paquete del dueño está equivocado en este punto.** El 8-oct-2026 **no** es una decisión de política monetaria de Banxico. Banxico ya decidió (mantuvo 6.50%) el **24-sep-2026**; la siguiente decisión está programada para el **5-nov-2026**. El 8-oct-2026 corresponde, con alta probabilidad (patrón de calendario verificado: dos jueves después de la decisión), a la publicación de las **minutas** de la reunión del 24-sep — consistente con lo que la lectura conservadora del vigía ya anticipaba ("lo habitual es que ~8-oct sea la publicación de las minutas").
2. **No hay, en sentido estricto, una contradicción entre fuentes primarias**: la cita del paquete no viene de una fuente primaria de Banxico (viene de una nota de prensa secundaria, SDP Noticias, parafraseando a un funcionario) ni se pudo verificar contra el calendario oficial en HTML directamente desde este entorno (404/redirect). El fallo se sostiene en la convergencia de (a) el calendario de 2026 reconstruido por múltiples fuentes de mercado coincidentes y (b) el patrón reproducible de "decisión → minuta dos jueves después" verificado con un caso concreto (6-ago → 21-ago).
3. **No se corrige ningún registro propio**: la inteligencia del 25-sep en adelante ya tenía esto bien. Se corrige únicamente la tabla de verificación del paquete del dueño (`datos/entrada-dueno/2026-10-05.md`), que había dejado la fila como "conflicto, por confirmar", y se cierra el punto en `bitacora/decisiones-pendientes.md`.
4. **Fuente de menor calidad que generó el error:** el dato original no viene de Banxico mismo sino de una paráfrasis de prensa de una declaración oral de un subgobernador; es plausible que la fuente original haya mezclado "próximo evento relevante de Banxico" (la minuta) con "próxima decisión". No se trata como mala fe ni como error grave del paquete — es el tipo de matiz (decisión vs. minuta) que confunde a cualquier cobertura de prensa que no cite el calendario oficial completo.

## Efecto

- `datos/entrada-dueno/2026-10-05.md`: fila de la tabla de verificación corregida con nota fechada (6-oct) — el conflicto queda resuelto, no solo "marcado".
- `bitacora/decisiones-pendientes.md`: la entrada "2026-10-06 · primer paquete diario del dueño" se cierra en el punto de la fecha de Banxico (el punto de P0049 y el de las cuentas de X ya estaban cerrados).
- No se registra en `conocimiento/registro-de-errores.md`: el error es del paquete externo del dueño, no de un archivo propio del sistema; nuestra propia inteligencia ya tenía el dato correcto desde el 25-sep, sin necesidad de corrección retroactiva.
- Pendiente técnico menor: si una corrida futura logra acceso de lectura directo al HTML de `banxico.org.mx` (hoy 404/redirect desde este entorno), debe confirmar con el documento oficial exacto (no solo agregadores de mercado) el calendario completo de 2026 y, si existe, el número de minuta del 8-oct.
