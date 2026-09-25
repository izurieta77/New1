# Banco de examen G1 · Bitcoin: protocolo, dinero y autocustodia

> Creado el 25-sep-2026 por `analista-cripto`. Nivel maestría-doctorado. **Uso a libro cerrado**: se permite calculadora y los datos de entrada vienen en cada enunciado.
>
> **Estructura:**
> - **Parte A:** 8 preguntas;
> - **Parte B:** respuestas de referencia, fuentes y criterios de calificación (10 puntos por pregunta).
>
> **Fuentes:** fichas [15](../recursos/15-diplomado-en-bitcoin.md), [16](../recursos/16-mastering-bitcoin-3-a-edicion.md), [20](../recursos/20-plan-network-plan-academy.md), [28](../recursos/28-dinero-roto.md) y [29](../recursos/29-diplomado-bitcoin-edicion-2025.md), y el capítulo [01](../01-bitcoin-protocolo-dinero-y-autocustodia.md). Verifiqué todas las cifras con cálculo propio en Python o con datos públicos del 25-sep-2026.

## Parte A: preguntas

**P1. Calendario de emisión (maestría).** El 25-sep-2026 la cadena está en la altura 968,589. El subsidio sigue `GetBlockSubsidy`: 50 BTC desplazados a la derecha una vez por cada 210,000 bloques, en satoshis.
- (a) ¿Cuánta oferta teórica se ha emitido y qué porcentaje del máximo es?
- (b) ¿En qué altura es el próximo halving, cuántos bloques faltan y en qué fecha cae con bloques de 600 s y con el ritmo actual de 628.9 s?
- (c) ¿Cuál es la emisión anual antes y después de ese halving, en BTC y en porcentaje?
- (d) ¿Por qué el máximo no es exactamente 21,000,000 BTC, en qué altura el subsidio llega a cero y qué dos pasajes de *Mastering Bitcoin* se contradicen en esto?

**P2. Whitepaper §11 (doctorado).**
- (a) Escribe la probabilidad de que un atacante con fracción q del hashrate alcance a la cadena honesta desde z bloques atrás.
- (b) Calcula P para q = 0.10 con z = 2 y z = 6, y para q = 0.30 con z = 6.
- (c) ¿Cuántas confirmaciones hacen falta para P < 0.1% si q = 0.30?
- (d) ¿Qué **no** puede hacer un atacante con mayoría de hashrate?
- (e) Da dos salvedades que el apéndice B de *Mastering Bitcoin* agrega al whitepaper.

**P3. Dificultad y forks (doctorado).**
- (a) Describe la regla de ajuste de dificultad, con su error de uno y su límite.
- (b) En un hard fork contencioso que deja 80% del hashrate de un lado y 20% del otro, ¿cuánto dura el bloque promedio y cuánto tarda cada cadena en llegar a su ajuste?
- (c) Con datos reales de la prohibición china de 2021: ¿cuál fue el tiempo de bloque promedio de la época del 13-jun al 3-jul-2021, cuál el peor tramo de 144 bloques y de qué tamaño fue el ajuste?
- (d) ¿Por qué un soft fork es "compatible" y qué críticas recoge *Mastering Bitcoin*?

**P4. Presupuesto de seguridad (doctorado).** Datos del 25-sep-2026:
- subsidio de 3.125 BTC;
- 144 bloques al día;
- comisiones: 4.069 BTC en los últimos 144 bloques y 85.30 BTC en los últimos 4,320;
- precio de US$84,045.67.

Preguntas:
- (a) Calcula el subsidio diario en BTC y en USD, y la proporción de las comisiones en la recompensa en ambas ventanas.
- (b) Explica el *fee sniping*, por qué *Mastering Bitcoin* lo llama "inevitable" en cierto régimen y cómo lo mitiga Bitcoin Core.
- (c) ¿Qué cambió Bitcoin Core 29.1 (sep-2025) en la política de comisiones y por qué importa?
- (d) Tras el halving de 2028, ¿cuánto tendría que subir el precio, o cuántas veces las comisiones, para mantener el presupuesto diario en USD?

**P5. Llaves, semillas y direcciones (maestría-doctorado).**
- (a) ¿Cuántos bits de entropía y de checksum tiene una frase BIP39 de 12 palabras, y cuántos una de 24?
- (b) ¿Por qué "no existe passphrase incorrecta" es a la vez una ventaja y un riesgo?
- (c) Tu xpub de cuenta está en un servidor y se filtra una clave privada hija **no endurecida**. ¿Qué se compromete y qué lo habría evitado?
- (d) ¿Por qué un multisig en P2SH tiene ~80 bits de seguridad contra colisiones y uno en P2WSH ~128? ¿Cuánto tardaría hoy la red en hacer 2^80 hashes a 922.7 EH/s?

**P6. Lightning (doctorado).**
- (a) Bob publica un estado viejo de un canal con Alice. ¿Qué mecanismo lo castiga y qué papel juega el retraso relativo (CSV)?
- (b) ¿Por qué Alice debe vigilar la cadena y qué pasa si no lo hace?
- (c) ¿Por qué falla más un pago grande que uno chico?
- (d) ¿Qué efecto tienen comisiones on-chain altas sobre la topología de la red, según la crítica a Alden?

**P7. Custodia y contraparte aplicadas a la cuenta del torneo (maestría).** `arena-claude-binance` opera spot en un exchange que no está supervisado en México; los pesos pasan por Medá.
- (a) ¿En qué nivel de la escala de Plan ₿ está la cuenta y por qué se acepta?
- (b) ¿Qué tres riesgos de exchange enumera BTC102 y qué responde la contingencia a cada uno?
- (c) ¿Por qué, según *Dinero Roto* (cap. 6), los disparadores deben ser tempranos?
- (d) Una transacción P2WPKH de 1 entrada y 2 salidas: calcula su tamaño en vB y su costo a 2 y a 50 sat/vB.
- (e) ¿Cuántas confirmaciones esperar al depositar en Bitso y por qué no bastan 2?

**P8. La tesis de *Dinero Roto* (doctorado).**
- (a) Explica la brecha entre la velocidad de las transacciones y la de las liquidaciones, y por qué llevó a la centralización.
- (b) ¿Qué reservas encontró Jevons (1875) y qué apalancamiento implican?
- (c) Resume la "teoría del libro contable del dinero".
- (d) Da la crítica más fuerte que encontraste.
- (e) ¿Qué observaría un inversionista que refute la tesis en la práctica? ¿Qué grado de evidencia le das y por qué?

## Parte B: respuestas de referencia

### R1 · Calendario de emisión

- **(a) Oferta: 20,089,343.75 BTC = 95.66% del máximo.**
  - Son 20,089,293.75 BTC sin contar los 50 BTC de génesis, que no se pueden gastar.
  - Faltan ~910,656 BTC.
- **(b) Próximo halving: altura 1,050,000; faltan 81,411 bloques.**
  - × 600 s ≈ 565.4 días → **13-abr-2028**.
  - × 628.9 s ≈ 592.6 días → **10-may-2028**.
- **(c) Emisión anual:**
  - hoy 3.125 × 52,560 ≈ **164,250 BTC al año (0.82%)**;
  - después, ≈ **82,125 BTC al año (0.40%)**.
- **(d) Por qué no son 21 M exactos:**
  - el desplazamiento de bits trunca el subsidio al satoshi, así que el máximo es **2,099,999,997,690,000 sats = 20,999,999.9769 BTC**;
  - la época 32 (alturas 6,720,000-6,929,999) paga 1 sat y el subsidio es **0 desde la altura 6,930,000**;
  - *Mastering Bitcoin* se contradice: el cap. 6 dice "up until block 6,720,000" y el cap. 12 da las 32 reducciones y el máximo correcto.
  - Bonus: su `max_money.py`, corrido en Python 3, imprime 2.1e15 porque usa división flotante.
- **Fuentes:** MB, caps. 6 y 12; ficha 15, §4; cálculo propio.
- **Puntos:** a = 2, b = 3, c = 2, d = 3.

### R2 · Whitepaper §11

- **(a) Fórmula:** con p = 1 − q y λ = z·q/p,
  - P = 1 − Σ_{k=0}^{z} [e^(−λ)·λ^k / k!]·[1 − (q/p)^(z−k)].
- **(b) Valores:**
  - q = 0.10: z = 2 → **5.10%**; z = 6 → **0.0243%**;
  - q = 0.30: z = 6 → **13.2%**.
- **(c) z = 24.** La tabla completa para P < 0.1%:

  | q | 0.10 | 0.15 | 0.20 | 0.25 | 0.30 | 0.35 | 0.40 | 0.45 |
  |---|---|---|---|---|---|---|---|---|
  | z | 5 | 8 | 11 | 15 | 24 | 41 | 89 | 340 |

- **(d)** No puede crear monedas fuera de las reglas ni gastar monedas ajenas: los nodos validan firmas y reglas. "PoW vota solo el orden de las transacciones". Sí puede hacer doble gasto de **sus** transacciones y censurar.
- **(e) Salvedades del apéndice B:**
  - la minería egoísta es rentable con ~**30%** del hashrate, no con mayoría;
  - el **ataque Finney** funciona con cualquier número de confirmaciones si el atacante preminó un bloque;
  - también vale: "longest chain" debe leerse como cadena **con más trabajo** (cambio de jul-2010).
- **Fuentes:** whitepaper §11 reproducido en Python; MB, cap. 12 y apéndice B.
- **Puntos:** a = 2, b = 3, c = 1, d = 2, e = 2.

### R3 · Dificultad y forks

- **(a) Regla:** cada 2,016 bloques con objetivo de 20,160 min (dos semanas). El código mide **2,015** intervalos, lo que da un sesgo de +0.05% (2,016/2,015 − 1 = 0.0496%). El cambio está limitado a un factor de 4 por ajuste.
- **(b) Split 80/20:**
  - la mayoritaria mina un bloque cada **12.5 min** y llega a su ajuste en 2,016 × 12.5 min = **17.5 días**;
  - la minoritaria, cada **50 min**; tarda 2,016 × 50 min = **70 días (~10 semanas)** y tiene 1/5 de la capacidad.
- **(c) China 2021:**
  - promedio de la época: **13.9 min** por bloque;
  - peor tramo de 144 bloques: **20.2 min** (26-28-jun-2021);
  - ajuste: **−27.94%** en la altura 689,472 (3-jul-2021), el mayor de la historia.
  - Alden dijo "~18 min durante una o dos semanas": es aproximado.
- **(d) Soft fork:** solo **restringe** reglas. Los nodos viejos aceptan los bloques nuevos y la mayoría del hashrate impone la regla.
  - Críticas en MB: deuda técnica, validación degradada de los nodos no actualizados e irreversibilidad.
  - Mecanismos de activación: BIP9 (95% = 1,916 de 2,016), BIP148 (UASF), BIP8 y Speedy Trial (Taproot).
- **Fuentes:** MB, cap. 12; mempool.space (ajustes); blockstream.info (tiempos); cálculo propio.
- **Puntos:** a = 2, b = 3, c = 3, d = 2.

### R4 · Presupuesto de seguridad

- **(a) Subsidio y comisiones:**
  - subsidio: 3.125 × 144 = **450 BTC/día** ≈ **US$37.8 M/día**, ≈ US$13.8 mil M al año;
  - comisiones: 4.069 / 454.069 = **0.90%** en 144 bloques y 85.30 / 13,585.30 = **0.63%** en ~30 días, unos 2.84 BTC/día.
- **(b) Fee sniping:** un minero re-mina el bloque anterior para quedarse con sus comisiones. MB dice que hoy no es lucrativo porque el subsidio pesa mucho más que las comisiones; cuando las comisiones sean la mayor parte de la recompensa, "este escenario se vuelve inevitable".
  - Mitigación: las billeteras ponen **nLockTime = altura actual**, así que sus transacciones no caben en un bloque anterior.
- **(c) Bitcoin Core 29.1** bajó el mínimo de retransmisión y el incremental por defecto a **100 sat/kvB (0.1 sat/vB)**. El piso de comisiones en periodos tranquilos baja, y con él el ingreso por comisiones mientras no haya congestión.
- **(d) Tras el halving de 2028:**
  - hoy la recompensa diaria es 450 + 2.84 ≈ 452.8 BTC; después, el subsidio baja a 225 BTC/día;
  - para mantener US$37.8 M/día solo con precio, el precio tiene que **duplicarse** (≈ US$168 mil);
  - a precio constante, las comisiones tienen que subir de ~2.84 a ~227.8 BTC/día, **≈ 80×**.
- **Fuentes:** MB, caps. 9 y 12; notas de versión de Core 29.1; mempool.space; cálculo propio.
- **Puntos:** a = 3, b = 3, c = 2, d = 2.

### R5 · Llaves, semillas y direcciones

- **(a) BIP39:**
  - 12 palabras × 11 bits = 132 = **128 de entropía + 4 de checksum** (ENT/32);
  - 24 palabras = 264 = **256 + 8**;
  - "1 entre 2^256" es incorrecto para 12 palabras (error de Plan ₿);
  - la seguridad de una clave pública de secp256k1 ronda los **128 bits**.
- **(b) Passphrase.** Como no entra en el checksum, cada passphrase genera una billetera válida distinta. Eso da negación plausible y permite una "billetera señuelo". Pero un error de tecleo o un olvido deja fondos **irrecuperables**, y el riesgo crece con la muerte o incapacidad del dueño.
  - BIP39 usa PBKDF2 con 2,048 rondas y sal "mnemonic" + passphrase, que MB llama "débil".
- **(c) Fuga de xpub + hija no endurecida.** Con la xpub (clave pública + chain code) y **una** clave privada hija no endurecida se deriva la **clave privada extendida del padre**, y con ella **todas** las claves de la cuenta. Lo evita la **derivación endurecida** (índices ≥ 2^31).
- **(d) Colisiones:**
  - si el atacante controla parte del script (sus propias claves en un multisig), encontrar una colisión en un hash de 160 bits (HASH160) cuesta ~2^80 por la paradoja del cumpleaños; en P2WSH (SHA256, 256 bits) cuesta ~2^128;
  - MB: la red hacía ~2^80 hashes por hora a inicios de 2023, unos 335.8 EH/s; a 922.7 EH/s tarda **~21.8 min**. Es una comparación de órdenes de magnitud;
  - moraleja: multisig en P2WSH o P2TR.
- **Fuentes:** MB, caps. 4-5; ficha 20; cálculo propio.
- **Puntos:** a = 2, b = 2, c = 3, d = 3.

### R6 · Lightning

- **(a) Revocación.** Cada parte tiene su propia versión de la transacción de compromiso; la salida propia queda bloqueada por un **retraso relativo (CSV)**. Al pasar al siguiente estado, cada parte entrega el **secreto de revocación** del estado anterior.
  - Si Bob publica un estado viejo, Alice usa ese secreto para llevarse **todo** el saldo del canal mientras Bob espera el CSV.
  - El índice de estado es de 48 bits: 2^48 ≈ 2.8 × 10^14 estados.
- **(b) Vigilancia.** El castigo solo funciona si Alice (o su *watchtower*) ve la transacción **dentro del plazo del CSV**; en el ejemplo de MB, 1,000 bloques. Si no vigila, el robo de Bob se consolida.
- **(c) Pagos grandes.** La liquidez es **direccional y por salto**: cada canal de la ruta necesita saldo suficiente del lado correcto. A más monto, menos rutas viables. Los pagos multiruta ayudan en parte.
  - Alden (p. 354, según la reseña): "la liquidez es la mayor limitación de una red de canales"; la calidad de la liquidez (Bos Score) importa.
- **(d) Comisiones on-chain altas.** Abrir y cerrar canales se encarece: menos canales y más grandes, **centralización en hubs** y, en el límite, billeteras **custodiales**. Es la crítica de "Conflated" (4-sep-2024), que estima ~200 M transacciones on-chain al año; mi cálculo da ~180 M (3,420 transacciones por bloque × 52,560 bloques).
- **Fuentes:** MB, cap. 14; ficha 28; ficha 29 (cap. 7: "menos seguro").
- **Puntos:** a = 3, b = 2, c = 3, d = 2.

### R7 · Custodia y contraparte aplicadas

- **(a) Nivel 0 (custodia de terceros).** Se acepta porque es una cuenta de trading spot con filtro SMA200 y cortacircuitos que exigen vender rápido, con tope de 10,000 MXN y pérdida máxima de 5,000 MXN.
  - El exchange no está supervisado en México: no puede ser ITF sin autorización de Banxico (Ley Fintech, art. 30) y la Circular 4/2019 excluye esos servicios a clientes.
- **(b) Riesgos de BTC102 y respuesta de la contingencia:**
  - **hackeo** (Mt. Gox) → el tope de tamaño limita la pérdida;
  - **embargo o congelamiento** → disparadores definidos: aviso de Binance, SPEI caído más de 48 h, o acción de CNBV, FinCEN, OFAC o DOJ;
  - **quiebra o fraude** (FTX) → vender a MXN y retirar por SPEI, o mover BTC on-chain a Bitso;
  - un congelamiento total arriesga los 10,000 MXN.
- **(c) Disparadores tempranos.** En una corrida sobre una institución de reserva fraccionaria, **quien retira primero cobra completo** y quien llega tarde puede perderlo todo. Esperar la confirmación de insolvencia es llegar tarde.
- **(d) Tamaño y costo de la transacción:**
  - tamaño: 10.5 (base) + 68 (entrada P2WPKH) + 2 × 31 (salidas) = **140.5 vB**;
  - a 2 sat/vB = 281 sats ≈ **US$0.24**; a 50 sat/vB = 7,025 sats ≈ **US$5.90** (precio de US$84,045.67);
  - la comisión de retiro de Binance es aparte.
- **(e) 6 confirmaciones (~1 h).** Con q = 0.1 la reversión es de 0.024%, contra 5.1% con 2. El "2 bastan" del Diploma 2025 solo vale para montos pequeños.
- **Fuentes:** `bitacora/decisiones/2026-09-25-CRIPTO-inicial.md`; ficha 20 (BTC102); ficha 28 (cap. 6); MB, caps. 6, 9 y 12.
- **Puntos:** a = 2, b = 2, c = 2, d = 2, e = 2.

### R8 · La tesis de *Dinero Roto*

- **(a) La brecha.** Antes del telégrafo, la información y el valor viajaban a la misma velocidad. Desde los cables transatlánticos (años 1860), las **transacciones** viajan a la velocidad de la luz y las **liquidaciones** en oro a la velocidad de la materia.
  - Mientras tanto, el pago existe "en crédito" y alguien debe llevar el libro contable: bancos, luego bancos centrales. Los reclamos proliferaron más que el oro y los gobiernos quitaron el respaldo (Primera Guerra Mundial, 1933, 1971).
  - [O de Alden] "La única vez que el dinero más débil ganó en adopción al más fuerte."
- **(b) Jevons (1875).** Reservas del **4-5%** de los pasivos a la vista (Palgrave, 1873), es decir **20-25×**, y de **~7%** (Moxon), es decir **~14×**.
- **(c) Teoría del libro contable.** Todo dinero es un registro. La diferencia está en **quién lo mantiene**: humanos por confianza (crédito: cómodo pero se degrada), la naturaleza por la física (mercancía: duro pero lento) o los usuarios por código abierto (Bitcoin).
  - Con alta confianza domina el crédito; con baja, la mercancía. Alden concede que el crédito precede a la moneda: Smith se equivocó en el orden.
- **(d) Crítica más fuerte ("Conflated", 4-sep-2024).** El problema del oro fue la **fricción** en general, no solo la velocidad. Una capa base cara (~180-200 M transacciones al año) empuja a custodios y reclamos de papel: **repite la historia del oro**.
  - A eso se suma el conflicto de interés de la autora (consejo de Swan).
- **(e) Qué la refutaría en la práctica:**
  - que la mayoría de los BTC terminen en custodios (ETF, exchanges) con reclamos fraccionarios, igual que el oro;
  - que stablecoins o CBDC capturen la liquidación rápida con un emisor que puede congelar;
  - que el presupuesto de seguridad no aguante la transición a comisiones.
  - **Grado C como tesis** (plausible, no falsable ex ante) y **D como señal de timing**.
- **Fuentes:** *Dinero Roto*, caps. 4, 6 y 8; entrevistas de MacroVoices (19-oct-2023) y The Investor's Podcast; reseña de "Conflated".
- **Puntos:** a = 3, b = 2, c = 2, d = 2, e = 1.

## Uso

- **Examen mensual (rutina 5):** tomar 1-2 preguntas de este banco entre las 5 de cripto.
- **Aprobación:** ≥ 9/10 en cada pregunta usada, según la meta del plan de estudio (≥ 90% global).
- **Actualización:** los datos "de hoy" de P1, P4 y P7 son del 25-sep-2026. Si el banco se usa después, se recalculan con la altura y los precios del día; la fórmula y el método de la respuesta no cambian.
