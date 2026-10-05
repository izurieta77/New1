# Arbitraje · 2026-10-05 (conciliación de la noche del 4-oct) · Flujo neto de ETF spot BTC del 1-oct-2026: +103M o +676M

## Caso

El analista-cripto (cascada vespertina, 4-oct 18:42 CDMX) encontró que el flujo neto de los ETF spot de bitcoin en EUA para el **1-oct-2026** está registrado en `bitacora/cripto/2026-10-01.md` (vía el ejercicio de `bitacora/cripto/2026-10-02.md`, línea 27) y en las notas de los pronósticos **P0052** y **P0059** (`bitacora/pronosticos.csv`) como **+103M USD** (atribuido a SoSoValue, citado por un resumen de búsqueda), mientras que una búsqueda nueva del 4-oct devolvió, para la misma fecha, **+676M USD** (IBIT +405M, FBTC +179M), de un resumen de búsqueda sin verificar contra fuente primaria. El analista-cripto, correctamente, no tocó el registro existente y dejó la duda abierta en `bitacora/decisiones-pendientes.md` (entrada del 4-oct 18:42).

## Posiciones

1. **+103M USD** (registrado): citado en `bitacora/cripto/2026-10-01.md`/`2026-10-02.md` y en P0052/P0059, atribuido a "SoSoValue vía KuCoin" sin acceso directo a `sosovalue.com` (403 documentado desde el 25-sep).
2. **+676M USD** (candidato nuevo): IBIT +405M, FBTC +179M, de una búsqueda dirigida del 4-oct que el propio analista-cripto marcó como sospechosa de mala atribución de fecha (mezclaba cifras de 6, 14 y 24-oct con la del 1-oct).

## Qué se consultó

- **`sosovalue.com/assets/etf/us-btc-spot`** y **`farside.co.uk/btc/`**: ambos devuelven **HTTP 403** tanto por `curl` directo como por `WebFetch` en esta corrida. Verificado contra `/__agentproxy/status`: sin fallas de política de egreso recientes (`recentRelayFailures: []`), así que el 403 es del propio sitio (protección anti-bot), no un bloqueo de la sesión. Esto es consistente con el mismo hallazgo ya documentado el 25-sep y el 2-oct en `bitacora/cripto/2026-10-02.md` ("Farside/SoSoValue siguen en 403").
- Búsquedas dirigidas repetidas sobre el origen exacto de la cifra de **+676M USD** (con IBIT +405M y FBTC +179M) llevaron a un artículo identificable: **coinfomania.com**, "Bitcoin Spot ETFs Log $676M Inflows In 3 Days, IBIT Tops At $405M". Se leyó el artículo completo con `WebFetch`:
  - **Fecha de publicación: 2 de octubre de 2025** (no 2026).
  - Los **$676M** son el acumulado de **tres días de operación**, no el flujo de un solo día.
  - El día con el inflow más alto de IBIT (**$405M**) fue el **1 de octubre de 2025**.
  - El artículo no menciona octubre de 2026 en ningún lugar (las únicas referencias a "2026" son enlaces a notas relacionadas, no distintas, publicadas en esa fecha, no parte del cuerpo de la noticia).
- Segunda búsqueda, sobre un tercer candidato que apareció al indagar ("$300M de salida neta del 1 al 3-oct-2026"): no se encontró ningún artículo específico que respalde esa cifra con fecha de publicación verificable; es, igual que el candidato de +676M, un resumen de búsqueda sin fuente citable identificada. No se incorpora como candidato serio por falta de trazabilidad.

## Fallo

1. **La cifra de +676M USD no es válida para el 1-oct-2026.** Corresponde al **1-oct-2025** (confirmado con fecha de publicación del artículo fuente, 2-oct-2025, y con el propio texto del artículo que la describe como un acumulado de 3 días, no el dato de un único día). El motor de búsqueda que la produjo mezcló el año incorrectamente al resumir resultados — el mismo patrón de mala atribución que el analista-cripto ya había señalado como sospechoso ("mezcló... cifras de fechas muy posteriores... con el dato del 1-oct") se confirma aquí como un error de **año**, no solo de mes.
2. **No hay discrepancia real que arbitrar entre +103M y +676M para el 1-oct-2026**: el segundo valor sencillamente no es un dato de esa fecha. No se cambia ningún registro (`bitacora/cripto/2026-10-01.md`, `bitacora/cripto/2026-10-02.md`, P0052, P0059 quedan como están).
3. **El valor de +103M USD sigue sin verificación directa contra fuente primaria** (SoSoValue y Farside inaccesibles por 403 en esta sesión, igual que en todas las corridas previas desde el 25-sep). No se encontró, en esta corrida, ninguna fuente de prensa alternativa con fecha de publicación verificable que confirme o contradiga +103M para el 1-oct-2026 específicamente. Se mantiene como el único valor con algún respaldo (aunque de calidad media) para esa fecha, por no tener ningún competidor creíble.
4. **No se fabrica ni se elige arbitrariamente ninguna cifra.** Si una corrida futura logra acceso directo a `sosovalue.com` o `farside.co.uk` (p. ej. si cambia la protección anti-bot del sitio, o si el dueño puede compartir una captura), debe verificar +103M contra la fuente primaria y corregir si procede.

## Efecto

- `bitacora/decisiones-pendientes.md`: la entrada del 4-oct 18:42 CDMX se cierra con este fallo.
- No se registra ninguna corrección en `conocimiento/registro-de-errores.md` para este punto específico: ningún registro propio estaba mal; el "error" vivía enteramente en un resultado de búsqueda externo que nunca se incorporó a ningún archivo del sistema.
- Pendiente técnico (bajo, para quien use búsquedas web en corridas de cripto futuras): los resúmenes de búsqueda pueden mezclar artículos de años distintos bajo la misma fecha de calendario ("1 de octubre") sin decirlo; conviene, ante cualquier cifra que no cuadre con el registro existente, pedir explícitamente el año de publicación del artículo fuente antes de tratarla como un candidato real, como se hizo en este fallo.
