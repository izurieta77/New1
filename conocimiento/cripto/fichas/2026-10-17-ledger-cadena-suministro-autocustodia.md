# Ficha de avance · 17-oct-2026 · Riesgo de autocustodia: el ataque a la cadena de suministro de Ledger vía el distribuidor CryptoBilis (oct-2026)

> Corrida de las 08:17 CDMX (14:18 UTC), estudio profundo. Grupo G4 (riesgos, fraude, hackeos y seguridad), sección D de `lista-senales-de-alerta.md` (operación propia y autocustodia).
>
> **Por qué este tema.** Quedó pendiente ayer (inteligencia del 16-oct lo dejó en grado B/D, leído solo de segunda mano vía The Hacker News). No existía ficha. Es un evento de cola nuevo de la categoría que el capítulo 04 tenía menos documentada: el riesgo **físico** del dispositivo de autocustodia, no del exchange ni del contrato.

## 0. Preguntas de hoy

1. ¿Qué dijo Ledger, con sus palabras y fechas, en sus canales oficiales?
2. ¿Qué parte de las cifras de prensa (72-100 millones de USD) se puede comprobar en la cadena?
3. ¿Qué cambia para nuestra cuenta (`arena-claude-binance`) y para la lista de señales?

## 1. Acceso y fuentes (declarado)

- **Primaria, íntegra (6 comunicados):** cuentas oficiales @Ledger_Support y @Ledger en X. x.com no se puede leer directamente; el texto completo se obtuvo del espejo público `api.fxtwitter.com/<cuenta>/status/<id>` (JSON con texto y hora). Se cotejó contra las citas literales de [The Hacker News, 12/14-oct](https://thehackernews.com/2026/10/ledger-finds-unauthorized-hardware.html) y [The Block, 13-oct](https://theblock.co/news/business/2026-10-13-ledger-confirms-hardware-implant-cryptobilis-reseller-units-mediamarkt-suspends-sales-europe-418442): coinciden palabra por palabra. Grado **A** en lo que dice Ledger (la vía es un espejo, no x.com: riesgo bajo de alteración, anotado).
  - 9-oct 13:32:12 UTC, @Ledger_Support/2108551100613714002 (primer aviso).
  - 10-oct 17:09:51 UTC, @Ledger_Support/2108968264055345381 (implante confirmado en un dispositivo).
  - 11-oct 17:13:22 UTC, @Ledger/2109331538072494364 (informe de 72 horas).
  - 13-oct 06:39:17 UTC, @Ledger/2109896739985453358 (análisis técnico del Donjon).
  - 13-oct 12:29:42 UTC, @Ledger/2109984923343782374 (MediaMarkt Saturn).
  - 13-oct 22:03:38 UTC, @Ledger/2110129361382994076 (suspensión en 7 mercados).
  - 14-oct 17:06:17 UTC, @Ledger/2110416915835338942 (inspección en Alemania).
- **No hay comunicado en ledger.com**: la búsqueda no devolvió ninguna entrada de blog. Ledger dice "We will update this post" en X. No se localizó ningún comunicado posterior al 14-oct (búsqueda web, 17-oct). Grado B en "sin novedades".
- **Cadena (primaria pública):** API de `mempool.space` sobre las 3 direcciones BTC que publicó el analista seudónimo Specter el 9-oct a las 12:24:31 UTC (@SpecterAnalyst/2108534068564373687, leído íntegro por la misma vía). La **atribución** de esas direcciones al atacante es de Specter (grado C); los saldos son grado A.
- **Secundario:** Bloomberg, vía [PYMNTS](https://www.pymnts.com/?p=4311217) (~90 millones); Bitquery, vía [braindetox/Gridinsoft](https://blog.gridinsoft.com/ledger-cryptobilis-hardware-implant/) (93.2 millones en 315 carteras); oferta de reemplazo de OneKey (The Block). Grado C-D. **No se leyeron:** el informe técnico de Tibane Labs (`tibane.net/research/ledger-nano-x-implant`) ni la página de soporte de Ledger sobre inspección del dispositivo.

## 2. Lo que dijo Ledger [H, grado A]

| Fecha (UTC) | Hecho según Ledger |
|---|---|
| 9-oct 13:32 | Investiga "reports of loss of funds" de usuarios del Sudeste Asiático que compraron a CryptoBilis. Pidió a CryptoBilis pausar ventas y envíos. A quien compró ahí **en los últimos 90 días**: no configurar; si ya lo hizo, "consider moving assets to a new Ledger signer (with new seed)". |
| 10-oct 17:09 | "One of the impacted users' devices contained an **unauthorized hardware implant**." CryptoBilis suspende **todo** su inventario de carteras de hardware. Coordina con autoridades y SEAL 911. "No indication that Ledger's security infrastructure, systems or services have been compromised." |
| 11-oct 17:13 | "The volume of impacted devices is **limited**." Todos los casos confirmados del drenaje del 9-oct vienen de CryptoBilis; canales de venta directa "unaffected". Pide a sus revendedores **no reponer producto devuelto**. Reconoce que es "an ongoing threat that doesn't just impact Ledger, but the whole ecosystem". |
| 13-oct 06:39 | **Mecanismo (Donjon):** el implante va dentro de la carcasa y **lee la pantalla**; al detectar las pantallas de la frase de 24 palabras durante la configuración, su microcontrolador las decodifica y las **transmite por LTE con una eSIM aprovisionada**. Es un componente aparte: **no modifica el Secure Element ni el sistema operativo, ni altera transacciones o firmas**. "We have **not confirmed** the total number of affected users or the total value lost. Figures circulating online come from third parties." Revisa "reports of implants in other signers and locations". |
| 13-oct 12:29 | MediaMarkt Saturn deja de vender Ledger (tiendas y en línea), con el acuerdo de Ledger, tras el reporte de un cliente en Alemania. "No loss of funds were reported." |
| 13-oct 22:03 | Pide suspender ventas y **retirar de los anaqueles** en Indonesia, Singapur, Tailandia, Filipinas, Vietnam, Malasia y Hong Kong. Los incidentes confirmados siguen limitados al Sudeste Asiático. Se investiga "who tampered with these devices and where in the distribution chain". |
| 14-oct 17:06 | En Alemania inspeccionó inventario minorista y de distribuidor: "None showed any sign of tampering. No loss of funds related to implants has been reported anywhere in Europe." No ha podido examinar los dispositivos mostrados en redes. |

**Lo que Ledger no dice (huecos):** el modelo afectado (la prensa dice Nano X; Ledger no), cuántos dispositivos, el total perdido, en qué eslabón se manipuló y si el implante del dispositivo confirmado transmitió algo. "Limited" no es una cifra.

## 3. Comprobación en la cadena [H, A en saldos; C en atribución]

Script: `conocimiento/cripto/fichas/2026-10-17-ledger-cadena-suministro.py` (paginación completa; afirma que el número de transacciones leídas = `tx_count`). Corrida 17-oct 14:2x UTC con BTC = 81,485.66 (Binance):

| Dirección (Specter) | Tx | Recibido BTC | Gastado BTC | Saldo BTC | Primera / última |
|---|---|---|---|---|---|
| bc1qjqgw…49dl | 83 | 92.5062 | 0 | 92.5062 | 9-oct 05:54 / 16-oct 18:55 |
| bc1qqnkw…jtm9 | 46 | 111.2820 | 0 | 111.2820 | 9-oct 05:54 / 9-oct 05:54 |
| bc1qgqhe…d26n | 159 | 9.9624 | 9.9624 | 0 | 7-oct 14:41 / 10-oct 00:41 |

- **Sin doble conteo:** ninguna de las tres paga a otra de la lista (0.00000000 BTC cruzados). Total recibido **213.75 BTC = 17.42 millones de USD**; **203.79 BTC (16.61 millones) siguen inmóviles** al 17-oct, ocho días después.
- **Escala:** lo visible en BTC es **20.3%** de los 86 millones de Specter y 18.7% de los 93.2 de Bitquery. El resto estaría en Ethereum y TRON (no verificado hoy). Es decir: la parte en BTC **sí cuadra con un robo de decenas de millones**, pero el total sigue sin confirmar.
- **Cronología:** la primera entrada observada es del **7-oct 14:41 UTC** (si esa dirección es del atacante desde el inicio; no se puede saber). Specter avisó **45.7 h** después y Ledger, **46.8 h** después; Ledger tardó **68 minutos** en reaccionar al aviso público. Las 46 entradas de la segunda dirección caen en un solo bloque (barrido en lote, consistente con frases ya robadas y vaciadas a la vez).
- **Pérdida media** con el dato de Bitquery: 93.2 M / 315 = **~296 mil USD por cartera** (grado D en el insumo). Víctimas de alto saldo, no minoristas pequeños: el atacante esperó a que hubiera fondos.
- **Ventana de 90 días** del aviso: compras desde el **11-jul-2026**. OneKey ofrece reemplazo a compradores de CryptoBilis del 1-mar al 13-oct (The Block, C): la ventana real de exposición podría ser mayor que la que dio Ledger.

## 4. Qué enseña (para invertir) [I]

1. **La autocustodia traslada el riesgo de contraparte del exchange a la cadena de suministro del dispositivo y al momento de generar la semilla.** El Secure Element no protege de un componente que **lee la pantalla**: la frase se muestra en claro durante la configuración. Ningún diseño que muestre la semilla en pantalla resiste un implante así; sí lo resisten la generación de semilla en un dispositivo comprado directo al fabricante, la verificación física y el multisig con fabricantes distintos.
2. **"Distribuidor autorizado" no es "canal seguro".** CryptoBilis era revendedor reconocido por Ledger, y aun así. La regla práctica: comprar **solo directo del fabricante**, nunca en mercados (Shopee, Lazada, Amazon de terceros) ni producto "abierto/devuelto".
3. **Las cifras de la primera semana son de terceros.** 72, 86, 90, 93.2 y 100 millones salen de analistas y prensa; Ledger no publicó ninguna. La cadena confirma ~17 millones solo en BTC. Para el sistema: un monto de prensa sobre un hackeo es grado C hasta que el afectado o la cadena lo respalden.
4. **Efecto en precio: nulo.** BTC −1.06% en 24 h hoy, dentro de lo normal; el BTC robado está inmóvil (una venta de 204 BTC sería ~2.0% del volumen de 24 h del par BTCUSDT de Binance, 10,171.7 BTC en un sábado; menos sobre el mercado total). El riesgo aquí es de **pérdida idiosincrática del tenedor**, no de mercado.
5. **Contraste con la lista D (Bybit, D2):** allá se alteró la interfaz de firma; aquí, el hardware. En los dos casos la defensa es la misma idea: **no confiar en un solo componente** (verificar en el dispositivo, multisig, origen controlado).

## 5. Implicación para la cuenta `arena-claude-binance` [I]

- **Exposición directa: ninguna.** El BTC de la cuenta está en custodia de Binance; no tenemos carteras de hardware, y el plan B (Bitso) también es custodia. Este incidente **no dispara** nada de `contingencia_contraparte`.
- **Lo que sí cambia:** si algún día el comité propone mover BTC a autocustodia (salida de Binance por E1-E10), el procedimiento debe incluir de antemano: compra directa al fabricante, inspección del empaque y del dispositivo, generación de semilla nueva en el dispositivo y prueba con un monto chico. Propuesta de señal nueva **D6** para la lista (pendiente de que el orquestador la acepte; va a `decisiones-pendientes.md`):
  - **D6 · Dispositivo de autocustodia de canal no directo** (revendedor, mercado en línea, devuelto o "preconfigurado"), o con señales de apertura → **ROJA**: no configurar; caso real: Ledger/CryptoBilis, oct-2026, implante con eSIM que lee la frase en pantalla.

## 6. Pronóstico de hoy

**P0139** (p = 0.40): ¿al 16-nov-2026 23:59 UTC el saldo confirmado conjunto de bc1qjqgw…49dl y bc1qqnkw…jtm9 es menor que 101.89 BTC (salió al menos la mitad de los 203.79 BTC de hoy)? Base: ocho días sin un solo gasto; la tercera dirección sí se vació en ~3 días. Los grupos sofisticados suelen lavar en semanas (Bybit-Lazarus movió casi todo en ~10 días), pero otros robos de BTC esperan meses por la vigilancia de los exchanges. p=0.40 por la inmovilidad observada. Grado C.

## 7. Límites

- La atribución de las direcciones es de un analista seudónimo (C). Si una es de un intermediario, los saldos cambian de sentido.
- Solo se vio la parte en BTC; Ethereum y TRON (y el supuesto congelamiento de ~10 millones de Tether, una sola fuente) no se revisaron.
- No hay comunicado de Ledger después del 14-oct en la búsqueda; puede existir en X sin cobertura de prensa.
- El texto oficial se leyó por un espejo (fxtwitter), cotejado con dos medios.

## 8. Estado y siguiente prueba

- **Estado:** Documentado con comprobación (fuente primaria íntegra + cadena con código).
- **Siguiente:** (a) leer el informe de Tibane Labs (variantes del implante, modelos afectados); (b) medir la parte en ETH/TRON con las direcciones de Specter (Etherscan/Tronscan); (c) revisar P0139 en cada 08:17 con el script; (d) buscar el informe final del Donjon.
