# Ficha de avance · 28-sep-2026 · G1 Bitcoin (Mastering Bitcoin, caps. 2, 3 y 8; correlación BTC-petróleo del día)

> Corrida de las 08:17 CDMX (14:18 UTC), `analista-cripto`. Continúa el pendiente dejado el 27-sep-2026 en [2026-09-27-reversion-btc-eth-ventanas.md](2026-09-27-reversion-btc-eth-ventanas.md) y en `estado-de-dominio.csv` (fila `cripto/01`): "Mastering Bitcoin caps. 2, 3 y 8 (MuSig2/FROST) a detalle". Añade una sección aparte sobre si el salto del petróleo de hoy (Irán/Ormuz, WTI +4%) tiene un efecto documentado sobre cripto, pedida explícitamente para esta corrida.

## 1. Acceso real

- **Fuente:** repo oficial `https://github.com/bitcoinbook/bitcoinbook` (CC BY-SA 4.0, gratis), rama `develop`. Archivos leídos vía `raw.githubusercontent.com`: `ch02_overview.adoc`, `ch03_bitcoin-core.adoc`, `ch08_signatures.adoc`.
- **Nivel de acceso: sección.** El texto se procesó con la herramienta de recuperación web de esta sesión (que resume en el acto lo que trae la página), no lo pegué ni lo leí carácter por carácter yo mismo en esta corrida — a diferencia de la lectura íntegra en AsciiDoc del 25-sep-2026 para los caps. 4-14. Por eso el grado de esta ficha es más bajo (B, no A) hasta que se relea el AsciiDoc completo de estos tres capítulos en una corrida futura con más tiempo. Verifiqué los datos numéricos citados abajo por mi cuenta contra `mempool.space` (API pública), no contra el libro.
- No cité más de un par de frases textuales por capítulo; el resto es paráfrasis y verificación propia.

## 2. Lo esencial, con etiquetas

### Cap. 2 — Panorama de Bitcoin

- **[H]** El sistema no exige confiar en terceros: "cada usuario puede correr software en su propia computadora para verificar cada aspecto del sistema". Tres piezas: usuarios con billeteras (llaves), transacciones que se propagan por la red, y mineros que producen la cadena de consenso.
- **[H]** Una transacción es como una partida de contabilidad de doble entrada: entradas que gastan, salidas que reciben; la diferencia es la comisión. Las transacciones se encadenan (una salida se vuelve la entrada de otra).
- **[H]** El cambio ("vuelto") va a una dirección nueva de la propia billetera por privacidad; no tiene que ser la misma dirección de la entrada.
- **[H]** Minar es "una lotería descentralizada": cada minero arma su propio "boleto" (bloque candidato) y prueba hashes. Crear un bloque válido cuesta mucho cómputo; verificarlo cuesta poco — la asimetría central de la prueba de trabajo.
- **[H]** Confirmaciones: "por convención, cualquier bloque con más de 6 confirmaciones se considera muy difícil de cambiar". Coincide con el cálculo propio del whitepaper §11 que ya está en la ficha del recurso 16 (25-sep-2026): con un atacante de 10% del hashrate, 6 confirmaciones bajan la probabilidad de reversión a 0.024%.
- **Sin novedad frente a lo ya estudiado** el 25-sep (caps. 4-14): este capítulo es la introducción de alto nivel; no cambia ninguna cifra operativa de la cuenta `arena-claude-binance`.

### Cap. 3 — Bitcoin Core

- **[H]** Requisitos de un nodo completo (cifras del libro, 2023): más de 500 GB de almacenamiento inicial, ~400 MB/día de descarga continua, se recomienda 1 TB para operar con margen. Ejemplo de nodo: altura ~775,072, ~1,000 millones de transacciones acumuladas, ~563 GB de tamaño de cadena.
- **[H] Verificación propia (mempool.space, 28-sep-2026 14:18 UTC):** altura actual = **969,006** (193,934 bloques más que el ejemplo del libro, ≈3.7 años de crecimiento a ~144 bloques/día). No tengo una cifra pública instantánea del tamaño exacto en GB hoy, pero con una tasa de crecimiento de ~150-160 GB/año reportada por trackers de la cadena, la cifra de 2023 (~563 GB) hoy debe rondar **850 GB-1 TB**, lo cual hace más relevante, no menos, la recomendación del libro de podar (`prune=`) en un nodo con disco limitado. **[I, nuestra]**: no verifiqué esta proyección con una fuente que dé el tamaño exacto hoy; queda como estimación, no como dato duro.
- **[H]** Opciones de configuración citadas en el libro y su función: `txindex=1` (indexa todas las transacciones, necesario para `getrawtransaction` de transacciones viejas), `prune=<MB>` (borra bloques antiguos, incompatible con `txindex`), `dbcache` (caché de UTXO en RAM), `blocksonly=1` (ahorra ancho de banda, no participa en el relevo de transacciones no confirmadas), `maxmempool`.
- **[H]** `bitcoin-cli getblockchaininfo`, `getrawtransaction`, `decoderawtransaction`, `getblockhash`/`getblock`: la RPC en JSON escucha por defecto en `127.0.0.1:8332`.
- **Para la cuenta de torneo:** no operamos un nodo propio (la cuenta es spot en Binance), así que este capítulo es cultura general de la carrera, no algo que cambie una decisión de la cuenta. Sí es relevante para la "vacuna" de custodia: entender que verificar un saldo propio con un nodo completo (en vez de confiar en el explorador de un tercero) es técnicamente accesible con ~1 TB de disco y algunas horas de sincronización, lo cual respalda por qué el libro (cap. 13, ya leído el 25-sep) insiste en "don't outsource validation".

### Cap. 8 — Firmas: Schnorr, MuSig2 y FROST

- **[H]** Firma Schnorr (Claus Schnorr, 1989; estandarizada para secp256k1 en **BIP340**, parte del soft fork Taproot de nov-2021): una firma son dos valores de 32 bytes, `(R, s)`, con `R` la coordenada x de un punto nonce y `s` un escalar. Se verifica con `sG = R + H(R‖P‖m)·P`. Ocupa 64 bytes (65 si se fija el `SIGHASH` explícitamente) contra 69-71 bytes típicos de una firma ECDSA en formato DER.
- **[H] Propiedad clave: la linealidad.** A diferencia de ECDSA, las firmas Schnorr se pueden sumar algebraicamente, lo que habilita la verificación por lotes (más barata) y las multifirmas "sin script" (donde el árbol de Script no necesita listar cada llave; la cadena solo ve una llave y una firma).
- **[H] MuSig1 (3 rondas de comunicación) → MuSig2 (2 rondas, BIP327) → MuSig-DN (nonce determinístico, evita el problema de sesiones repetidas, a costa de más cómputo).** El libro recomienda MuSig2 como la opción práctica hoy.
- **[H] El problema que resuelven y el ataque que evitan (rogue-key / cancelación de claves):** en una suma ingenua de llaves públicas (`P_agg = ΣP_i`), un participante que **no** necesita conocer la llave privada de nadie puede publicar una "llave pública" `P_C` maliciosa, calculada como `P_C = P_objetivo − ΣP_i(honestos)`, de modo que la suma total termine siendo `P_objetivo`, una llave que el atacante controla por completo. El atacante puede entonces firmar solo, sin que los demás participen, y la firma se ve válida "para el grupo". **MuSig2 lo evita con coeficientes de agregación `a_i = H(L, P_i)`** (BIP327 §2.4, donde `L` es la lista ordenada de todas las llaves): como cada coeficiente depende del hash de la llave de todos, el atacante no puede despejar `P_C` sin resolver un problema de logaritmo discreto, que se considera intratable.
- **[H] Firmas de umbral sin script (`t`-de-`k`):** combinan las multifirmas Schnorr con el esquema de Shamir de reparto verificable de secretos (VSSS). El libro documenta dos límites: **no dan "rendición de cuentas"** (no se puede probar después quién firmó, porque el firmante final es indistinguible del resto) y son **vulnerables si los participantes se coluden bilateralmente**. Ningún protocolo de este tipo tenía BIP asignado al cierre de la edición consultada.
- **[H]** El nonce debe ser criptográficamente aleatorio; reutilizarlo con la misma llave expone la clave privada (esto ya estaba en la ficha del 25-sep, cap. 8 "por encabezados"; ahora está verificado con la ecuación completa, no solo mencionado).

## 3. Ejercicio numérico verificado en Python: el ataque de cancelación de claves

Implementé la aritmética **real** de secp256k1 (mismos parámetros `p`, `n`, `G` que usa Bitcoin) en Python puro, sin librerías de terceros, para: (1) firmar y verificar una firma Schnorr individual con la ecuación de BIP340 simplificada; (2) simular una "multifirma ingenua" honesta de dos partes A y B; (3) reproducir el ataque de cancelación de claves descrito en el cap. 8, en el que un atacante C, **sin conocer la llave privada de A**, construye una llave pública que cancela la de A y firma solo, produciendo una firma que se verifica como si fuera de {A, C}.

```python
# secp256k1 real: p, n, G tomados de la especificación
p  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
n  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G  = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
      0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
# ... point_add, point_mul y sha256int con aritmética modular estándar ...

d_A, P_A = 0xA1, point_mul(0xA1, G)          # llave de la víctima A
d_target = 0xE5; P_target = point_mul(d_target, G)   # llave que el atacante SÍ controla
P_C = point_add(P_target, (P_A[0], (p - P_A[1]) % p))  # P_C = P_target - P_A

P_agg_rogue = point_add(P_A, P_C)            # "llave conjunta" de {A, C}
assert P_agg_rogue == P_target                # el atacante ya controla la llave agregada

k_atk = 0xF6; R_atk = point_mul(k_atk, G)
h_atk = sha256int(P_agg_rogue... )  # reto de Schnorr sobre la llave agregada
s_atk = (k_atk + h_atk * d_target) % n       # el atacante firma SOLO, con su propia llave

# Verificación: s_atk*G == R_atk + h_atk*P_agg_rogue  ->  True
```

**Resultado de la corrida** (script completo en `scratchpad/g1_musig/musig_toy.py` de esta sesión, fuera del repo):

```
1) Firma individual A valida: True
2) Multifirma ingenua (A+B honestos) valida: True
3) P_A + P_C == P_target (el atacante controla la llave agregada): True
4) Firma falsificada por el atacante, SIN participacion de A, valida bajo P_agg_rogue: True
```

- **Lo que prueba:** con la suma ingenua de llaves públicas que describen MuSig1/2 como el problema a resolver, un atacante que nunca vio la llave privada de A puede producir una firma que **pasa la verificación** como si fuera una firma conjunta de A y del atacante, sin que A haya firmado nada. Es una demostración concreta, no solo una cita del libro, de por qué el cap. 8 insiste en que la suma directa de llaves es insegura y de por qué existe el coeficiente `a_i = H(L, P_i)` de BIP327.
- **Límite del ejercicio:** es un juguete didáctico, no una implementación de producción — omite el hash "tagged" exacto de BIP340, la normalización de paridad de `y`, y no reproduce por qué el coeficiente de MuSig2 sí bloquea el ataque (eso exige una reducción de seguridad criptográfica, no un experimento numérico; lo doy como cita del BIP, [H] pero no verificado por mí con matemáticas de reducción). **Grado B** para la demostración del ataque (reproducible, con la curva real); **grado H-citado, no verificado por mí** para la prueba de que MuSig2 lo arregla.

## 4. Datos de red verificados hoy (mempool.space, 28-sep-2026 ~14:18-14:20 UTC), para contrastar con el 25-sep-2026

| Dato | 25-sep-2026 (ficha del recurso 16) | 28-sep-2026 (hoy) | Cambio |
|---|---|---|---|
| Altura | 968,589 | 969,006 | +417 bloques (~2.9 días a 144/día, consistente) |
| Dificultad | 132,757,073,449,487.5 | 132,757,073,449,487.5 (sin cambio; mismo periodo de 2,016 bloques) | Sin ajuste todavía |
| Próximo ajuste estimado | altura 969,696, **−4.49%** | altura 969,696, **−0.92%** (65.8% del periodo transcurrido) | La estimación de baja se moderó de −4.49% a −0.92% en 3 días: el hashrate se recuperó parcialmente dentro del mismo periodo |
| Hashrate (3 días) | ~922.7 EH/s | ~947.2 EH/s | +2.7% |

- **[I, nuestra]** Los últimos 26 ajustes de dificultad (≈ último año, API `mempool.space/api/v1/mining/difficulty-adjustments`) tuvieron **14 bajas de 26 (53.8%)**, muy por encima de la tasa histórica completa desde 2009 (**110 de 466, 23.6%**) y de los últimos ~2 años (**19 de 52, 36.5%**). El hashrate de BTC ha estado más "picudo" en el último año que en su historia completa. **Grado B** (cálculo propio, reproducible, con la API pública).

## 5. ¿El salto del petróleo de hoy (+4%, Irán/Ormuz) tiene un efecto documentado sobre cripto?

Pedido explícito de esta corrida. Busqué evidencia académica y de prensa especializada, sin especular donde no la encontré.

### 5.1 Lo que sí está documentado (revisado por pares)

- **[H] Salisu, Ndako y Vo, "Oil price and the Bitcoin market", *Resource Policy* 82 (2023), 103437** ([SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4261825), [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0301420723001459)): con datos del 27-ene-2017 al 3-jun-2022, encuentran que el petróleo **no predice el nivel del retorno de BTC de forma directa**, sino que **mejora el pronóstico de la volatilidad realizada de BTC** frente a un modelo de caminata aleatoria, y que esto opera por un canal específico: **el petróleo es un insumo de la minería (energía)**, así que un petróleo más caro sube el costo de minar, lo que a su vez se asocia con menor retorno y menor volatilidad de BTC en el mediano plazo (no de un día para otro).
- **[I, nuestra]** Este es el canal de "costo de producción", no un canal de "activo de riesgo que sube o baja junto con el petróleo por sentimiento". Es coherente con el hallazgo del punto 4 de esta ficha: la tasa de ajustes de dificultad negativos ya venía elevada (53.8% en el último año) antes del salto de hoy, lo cual podría ser congruente con presión de costos energéticos acumulada — pero **esto es una hipótesis nuestra, no algo que el paper mida con datos de 2026**, y no puedo aislar el petróleo de otras causas (precio de la electricidad regional, eficiencia de los ASIC, clima).

### 5.2 Lo que está documentado pero es inestable, no una constante

- **[H]** La correlación rodante BTC-DXY (índice del dólar) ha sido reportada como negativa la mayor parte de la historia de BTC (entre −0.40 y −0.80 desde 2014), pero la prensa especializada (no un paper revisado por pares) documenta que **en 2025-2026 esa correlación se ha invertido y vuelto a invertir varias veces en semanas** — de negativa a positiva a fines de 2025/inicios de 2026, y de vuelta a fuertemente negativa (≈−0.90) hacia abril de 2026 ([Coincub](https://coincub.com/blog/bitcoin-dollar-index/); [24/7 Wall St.](https://247wallst.com/investing/2026/03/06/bitcoins-12-year-relationship-with-the-dollar-just-broke/); [CME Group](https://www.cmegroup.com/insights/economic-research/2025/why-is-bitcoin-moving-in-tandem-with-equities.html)). La correlación BTC-Nasdaq a 30 días también saltó de 92% a 69% y luego de −0.68 a +0.72 en semanas, según la misma cobertura.
- **[I, nuestra]** Con una relación que cambia de signo en cuestión de semanas, **no hay un número único y estable que aplicar hoy**. No encontré un estudio revisado por pares (2025-2026) que mida la transmisión de un shock petrolero geopolítico puntual (como el de Ormuz de hoy) al precio de BTC en el mismo día. Lo que sí es consistente con la evidencia: el canal más sólido y verificado (Salisu et al.) es de **costo de minería sobre volatilidad de mediano plazo**, no de "activo de riesgo que reacciona el mismo día al petróleo".

### 5.3 Conclusión aplicada a hoy

- **No especulo un vínculo mecánico de corto plazo entre el +4% del petróleo de hoy y el movimiento de BTC de esta mañana** (BTC bajó ~1.5-2% en 24h, pero ese movimiento ya traía ese sesgo desde antes de la escalada de Ormuz, según los pulsos de 00:17-05:41 de hoy). **Declarado explícitamente: no encontré evidencia sólida de una transmisión mecánica del mismo día; lo que existe es un canal de costo de minería sobre horizontes de semanas (grado B, un paper) y una correlación BTC-DXY/Nasdaq documentada pero inestable (grado C, solo prensa especializada, sin paper 2026).**
- **Para el pronóstico de hoy** (sección 6), uso este hallazgo del canal de costo de minería como base para una pregunta verificable a 30 días sobre dificultad de minado, en vez de intentar predecir el precio de BTC a partir del petróleo, que la evidencia no respalda con ese nivel de precisión.

## 6. Estado del pendiente de `cripto/01`

- **Mastering Bitcoin caps. 2, 3 y 8: hecho (sección, no lectura íntegra del AsciiDoc completo; ver §1).** Cierra la mitad de este pendiente que no depende de una compra.
- **Nuevo pendiente:** releer el AsciiDoc completo de los caps. 2, 3 y 8 palabra por palabra (no solo vía resumen de la herramienta web) en una corrida con más presupuesto de tiempo, para subir el grado de A a la par del resto del libro; y, si el dueño confirma acceso, buscar un paper 2025-2026 revisado por pares que sí mida la transmisión de shocks petroleros geopolíticos puntuales a BTC (no solo el canal de costo de minería de mediano plazo de Salisu et al. 2023).
- **Dinero Roto caps. 9-30:** sigue bloqueado, sin vía legal gratuita (cuarto intento acumulado sin éxito desde el 25-sep; no se reintenta hoy porque no hay señal nueva de que algo cambió). Depende de que el dueño compre el ebook.

Script y datos de esta sesión: `scratchpad/g1_musig/musig_toy.py` (fuera del repo; si el dueño quiere conservarlo, conviene moverlo a `herramientas/`).
