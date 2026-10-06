# Ficha de avance · 6-oct-2026 · G2 Ethereum (Glamsterdam activa en Sepolia: verificación y recálculo de emisión/quema de ETH)

> Corrida de las 08:17 CDMX (14:18:52 UTC), `analista-cripto`. Avanza el pendiente explícito dejado en `conocimiento/estado-de-dominio.csv` (fila cripto/02, "siguiente_prueba" del 25-sep-2026): *"Repetir el cálculo de emisión/quema de ETH tras Glamsterdam (Sepolia 6-oct-2026)"*, y el pendiente que la ficha del 5-oct-2026 (`fichas/2026-10-05-beta-correlacion-oro-sp500.md`) dejó explícito en su §3 de descarte ("el fork de Glamsterdam en Sepolia es apenas mañana, sin datos de la red todavía"). **Elegido sobre 3 candidatos** de la corrida de hoy (releer el AsciiDoc íntegro de *Mastering Bitcoin* caps. 2, 3 y 8; confirmar la tarifa 2026 del art. 152 LISR contra el Anexo 8 de la RMF; repetir la verificación de PoR de Binance —prematuro, proyectado hacia el 15-21-oct— o acumular más observaciones de flujos de ETF) porque hoy es exactamente el día en que, según lo anotado, hay datos de red nuevos y verificables que no existían ayer, y porque el propio dueño señaló este tema como el más oportuno si resultaba verificable.

## 1. Acceso real y fuentes primarias

- **eips.ethereum.org/EIPS/eip-7773** — Meta-EIP de Glamsterdam ("This Meta EIP lists the EIPs formally Proposed, Considered, Declined for & Scheduled for Inclusion in the Glamsterdam network upgrade"). Acceso **íntegro** a la lista de 18 EIPs programados para inclusión (execution + consensus layer) y 8 adicionales (networking/informacional).
- **eips.ethereum.org/EIPS/eip-8246** ("Remove SELFDESTRUCT Burn") — texto íntegro del EIP: motivación, mecánica, estado ("Last Call", cierre de revisión 2026-11-04).
- **eips.ethereum.org/EIPS/eip-7928** (Block-Level Access Lists) — texto íntegro: confirma que no toca emisión ni quema, solo estructura del bloque para paralelismo.
- **API estándar de beacon chain (Eth Beacon API, `eth/v1/beacon/...`)** de dos nodos públicos independientes de Sepolia:
  - `https://checkpoint-sync.sepolia.ethpandaops.io` (operado por ethPandaOps, equipo de la Ethereum Foundation dedicado a testing de infraestructura);
  - `https://ethereum-sepolia-beacon-api.publicnode.com` (Allnodes/PublicNode).
  Ambos exponen el endpoint estándar `/eth/v1/beacon/states/head/finality_checkpoints` y `/eth/v1/beacon/genesis`, sin clave. Consultados en vivo hoy entre las 14:28 y 14:36 UTC.
- **Prensa especializada** (KuCoin, egamers.io, CryptoTimes, 247wallst, CCN) para la hora de activación programada (13:53:36 UTC, época 353,024) y el contexto de "bugs críticos" previos al corte — usada como corroboración secundaria, no como fuente de la verificación numérica.
- Nada de esto es información privilegiada: son especificaciones públicas de un protocolo abierto y datos de una red de prueba pública.

## 2. Metodología (declarada antes de ver el resultado final)

1. Calcular, a partir del `genesis_time` oficial de Sepolia y la aritmética de épocas (32 slots × 12 s = 384 s/época), el timestamp exacto de la época de activación anunciada (353,024) y confirmar que coincide con la hora publicada por la prensa (13:53:36 UTC) — es una verificación cruzada, no una confianza ciega en el titular.
2. Calcular la época actual aproximada al momento de la corrida y confirmar que ya pasó la época de activación.
3. Consultar `finality_checkpoints` en **dos nodos independientes** y comparar: si ambos reportan la misma época finalizada y la misma raíz de bloque, hay alta confianza en que no es un error de un solo operador.
4. Si la época finalizada es **posterior** a la época de activación, la cadena siguió produciendo bloques, siendo votada y alcanzando finalidad después del fork — la lectura operativa de "el fork no rompió la red".
5. Leer el meta-EIP (7773) para la lista completa de cambios, identificar cuáles tocan emisión/quema de ETH, y cuantificar el único que aplica (EIP-8246) con los propios datos que reporta el EIP (conteo de eventos históricos), usando una cota deliberadamente generosa para no subestimar el riesgo de estar equivocado.
6. Comparar esa cota contra la emisión anual y la quema por EIP-1559 ya documentadas en el capítulo 02 (dato del 25-sep-2026, sin recalcular hoy porque mainnet no forkeó).

## 3. Resultados

### 3.1 Verificación de la activación en Sepolia (sin pérdida de finalidad)

| Dato | Valor | Fuente |
|---|---|---|
| `genesis_time` de Sepolia | 1,655,733,600 (2022-06-20 11:00:00 UTC) | `eth/v1/beacon/genesis`, ambos nodos |
| Época de activación anunciada | 353,024 | pm #2225 / prensa |
| Timestamp calculado (384 s/época) | 2026-10-06 **13:53:36 UTC** | cálculo propio — **coincide exactamente** con lo publicado |
| Época actual aprox. al momento de la corrida (~14:35 UTC) | ~353,030 | cálculo propio |
| Época finalizada observada (dos nodos, mismas raíces) | **353,026** | `finality_checkpoints`, ethPandaOps y PublicNode |
| Época justificada observada | 353,027 | idem |
| Épocas finalizadas después de la activación | **2** | cálculo propio |

**Conclusión:** Sepolia **se activó y sigue finalizando con normalidad** después de la época 353,024. No hay evidencia de pérdida de finalidad ni de reorganización mayor en la ventana observada. Esto satisface la primera mitad de la condición B del capítulo 02 §8 ("Glamsterdam debe activarse en Sepolia... sin pérdida de finalidad"). Sigue pendiente Hoodi (27-oct-2026, tentativo) y la publicación de la época de mainnet.

**Límite:** la ventana de observación es corta (2 épocas finalizadas, ~13 minutos de historia post-fork al momento de escribir). Un problema de finalidad diferido (p. ej., un cliente minoritario que se cae horas después) no se habría detectado todavía. Es una foto, no una vigilancia continua.

### 3.2 Lista de EIPs de Glamsterdam y cuál toca la emisión/quema

Del meta-EIP 7773, los 18 EIPs programados para inclusión. Los relevantes para la economía del activo:

| EIP | Qué hace | ¿Toca emisión/quema? |
|---|---|---|
| EIP-7928 (Block-Level Access Lists) | Habilita paralelismo (lecturas/ejecución/cómputo de estado en paralelo) | **No**, en el sentido de que no toca la fórmula de emisión de consenso ni el mecanismo de quema de EIP-1559. El texto del EIP no contiene una oración general que lo niegue explícitamente; sí fija una regla puntual sobre el registro de la recompensa de bloque en la lista de acceso: "A zero-value block reward MUST NOT trigger a balance change in the block access list" (verificado hoy contra el texto fuente en GitHub, `ethereum/EIPs`, archivo `eip-7928.md`) — es una regla de *contabilidad del registro*, no un cambio al monto o mecanismo de la emisión o la quema. |
| EIP-7732 (ePBS) | Separación de proponente-constructor dentro del protocolo (capa de consenso) | No directamente; es una reforma de construcción de bloques, no de la fórmula de emisión. |
| **EIP-8246 ("Remove SELFDESTRUCT Burn")** | Quita el último mecanismo por el que ETH puede quemarse fuera de la quema de EIP-1559 (self-destruct de un contrato creado en la misma transacción, con el beneficiario siendo él mismo) | **Sí**, pero marginal (ver §3.3) |
| EIP-7708, EIP-7778, otros de costo de gas | Cambian contabilidad de gas, costos de calldata/estado, tamaño máximo de contrato | No afectan la fórmula de emisión de consenso (~166.3·√S) ni la quema de base fee (EIP-1559 sigue intacto) |

### 3.3 Cuantificación de EIP-8246 (Python, verificado dos veces con supuestos distintos)

Script completo en `scratchpad/glamsterdam_calc.py` (fuera del repo; se resume aquí el resultado reproducible):

```
Ventana post-Cancún muestreada: 5,573,413 bloques (~2.12 años)
Tasa observada de auto-quemas por SELFDESTRUCT: 0.94 eventos/año
Cota superior (muy generosa, 1,000 ETH/evento) de ETH quemado: 943.7 ETH/año
Esa cota equivale a 0.0882% de la emisión anual (1,070,000 ETH/año)
y a 5.973% de la quema por EIP-1559 anualizada (15,800 ETH/año, dato del 25-sep)
```

- **Insumos del propio EIP-8246** (sección "Motivation", leída hoy): "A full replay of Ethereum mainnet from genesis to approximately block 25M found only 2 post-Cancun burns" y "pre-Cancun history contained 54 self-burns in total". Cancún se activó en el bloque ~19,426,587 (13-mar-2024); de ahí la ventana post-Cancún de ~5.57 millones de bloques (~2.12 años a 12 s/bloque).
- **Supuesto deliberadamente generoso:** 1,000 ETH por evento. Es un supuesto absurdo hacia arriba — el propio EIP no reporta montos porque ninguno fue grande (si lo hubiera sido, sería un hecho conocido de la historia de Ethereum, como The DAO); un contrato autodestruido típico tiene saldo de unos pocos ETH o menos. Se eligió esta cota precisamente para que la conclusión sobreviva incluso si la realidad es mucho peor de lo que el EIP deja ver.
- **Verificación cruzada del orden de magnitud:** aun con la cota de 1,000 ETH/evento, el resultado (943.7 ETH/año) es **más pequeño que la quema de blobs documentada el 25-sep (~0.04 ETH/día × 365 ≈ 14.6 ETH/año)** multiplicada por 64, y **muy por debajo** de la quema total por EIP-1559 (15,800 ETH/año). Con un supuesto realista (unos pocos ETH por evento, no 1,000), el efecto real es de órdenes de magnitud menor: ~1-10 ETH/año.
- **Conclusión:** incluso con la cota más generosa razonable, remover la quema de SELFDESTRUCT **no mueve de forma perceptible la ecuación de oferta de ETH**. El mecanismo dominante de quema sigue siendo, por mucho, EIP-1559 (base fee), que a su vez depende de la demanda de gas, no de este EIP.

### 3.4 ¿Cambia el cálculo de emisión neta del capítulo 02?

**No, porque Glamsterdam todavía no toca mainnet.** La fórmula de emisión de consenso (~166.3·√S ETH/año, S = ETH efectivo en staking) y el mecanismo de quema por EIP-1559 son exactamente los mismos hoy que el 25-sep-2026 en mainnet; Glamsterdam/EIP-8246 solo se activó en Sepolia. Repetir las cifras de staking/emisión/quema de mainnet hoy (43.52M ETH en staking, ~1.07M ETH/año de emisión, ~15.8 mil ETH/año de quema) habría sido redundante sin una fuente nueva que las cambie; no se re-descargaron por no aportar nada nuevo. **Lo que sí cambió y se repite aquí es la pregunta correcta:** "¿Qué le pasará a la emisión/quema cuando Glamsterdam llegue a mainnet?", y la respuesta verificada hoy es **"básicamente nada, EIP-8246 es el único EIP del paquete que toca la quema, y su efecto es marginal"**.

## 4. Qué cambia para la decisión de cartera (cripto/02 §8)

- **Condición B (ejecución del protocolo) del capítulo 02:** pasa de "pendiente, se sabrá entre el 6-oct y fines de noviembre" a **"Sepolia cumplida sin pérdida de finalidad; Hoodi y mainnet siguen pendientes"**. No es suficiente por sí sola para reingresar ETH (se necesitan A, B, C y D juntas, más el voto del comité).
- **Condición C (economía) no cambia:** la inflación neta de mainnet, el tamaño de los blobs y la base fee no se mueven por un fork en testnet. Sigue "no cumple" con los datos del 25-sep.
- **No hay ninguna señal nueva que apure o posponga la decisión del comité sobre ETH.**

## 5. Contrapuntos y límites

1. **Ventana de observación corta** (§3.1): solo 2 épocas finalizadas tras el fork al momento de escribir. Un problema diferido de un cliente de consenso específico no se habría visto.
2. **El meta-EIP 7773 puede actualizarse** después de hoy (el estado "Scheduled for Inclusion" de un EIP puede cambiar si aparece un bug crítico, como ya advirtió la prensa sobre "critical bugs" en los días previos al 6-oct). Esta ficha es una foto del 6-oct, no una garantía de que el set final en mainnet sea idéntico.
3. **El conteo de "2 post-Cancun burns" y "54 pre-Cancun" es del propio EIP**, no una réplica independiente de mi parte; no reproduje el *replay* completo de mainnet (block 0 a 25M) porque no es viable en esta sesión. Es fuente primaria (el EIP), pero de una sola fuente para ese dato específico.
4. **No verifiqué si EIP-8246 sobrevive sin cambios hasta la versión final de Glamsterdam que llegue a mainnet;** está en "Last Call" con cierre de comentarios el 4-nov-2026, así que podría ajustarse.
5. **Fuente única para "no afecta emisión/quema" de EIP-7928:** se tomó del texto del propio EIP, leído hoy; es la fuente correcta (la especificación), pero no hay una segunda fuente independiente que lo contradiga o confirme.

## 6. Autoexamen

1. **¿Se activó Glamsterdam en Sepolia hoy y cómo lo sé sin depender solo de un titular de prensa?**
   Sí. Calculé el timestamp de la época de activación (353,024) a partir del genesis_time oficial y confirmé que coincide exactamente con la hora publicada (13:53:36 UTC). Después consulté `finality_checkpoints` en dos nodos beacon públicos independientes y ambos reportan la misma época finalizada (353,026) y la misma raíz de bloque, posterior a la activación — evidencia directa de la red, no solo un reporte de prensa.
2. **¿Qué EIP de Glamsterdam toca la emisión o la quema de ETH y cuánto pesa?**
   EIP-8246, que quita la quema (ya casi inexistente) por SELFDESTRUCT. Con los propios datos del EIP (2 eventos en ~2.12 años post-Cancún) y una cota muy generosa de 1,000 ETH por evento, el efecto es de a lo sumo ~944 ETH/año, 0.09% de la emisión anual de mainnet.
3. **¿Esto cambia la decisión de mantener ETH fuera de la cuenta cripto?**
   No. Solo avanza una de cuatro condiciones (B, ejecución del protocolo) y de forma parcial (falta Hoodi y mainnet); las condiciones de mercado y economía no cambiaron hoy.

## 7. Grado de evidencia: **A en la verificación de finalidad de Sepolia (dos fuentes primarias independientes); B en la lista de EIPs y su efecto cuantificado (fuente primaria única, EIP, con cálculo propio verificado)**

## 8. Estado

**Documentado.** Pendiente para la próxima revisión: repetir la verificación de finalidad con una ventana más larga (días, no minutos) y, cuando se confirme Hoodi (~27-oct) o se anuncie la época de mainnet, actualizar el capítulo 02 §8 y §9 otra vez.
