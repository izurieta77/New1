# Banco de examen G4: riesgo, fraude, hackeos y seguridad

- **Autor:** `analista-cripto`, 25-sep-2026.
- **Base:** fichas 08, 17, 22, 25, 32 y 33, el capítulo 04 y `lista-senales-de-alerta.md`.
- **Formato:** examen a libro cerrado, salvo que la pregunta pida calcular. Cada respuesta de referencia trae su fuente.
- **Criterio de calificación:**
  - **completa:** todos los puntos clave y la cifra correcta, con ±2% de tolerancia en los cálculos;
  - **parcial:** la idea correcta, pero sin cifra o sin distinción clave;
  - **incorrecta:** confunde conceptos (por ejemplo, atestación con auditoría, o acusado con sentenciado).

---

## Pregunta 1 (stablecoin, cálculo)

La atestación de Tether al 30-jun-2026 reporta:
- activos: US$187,751,426,411;
- pasivos: US$183,641,897,215;
- tenencias de BTC: US$5.80 mil millones;
- tenencias de oro: US$18.84 mil millones.

En ago-2026, Tether anunció una opinión sin salvedades de KPMG sobre sus estados de 2025.

**(a)** Calcula el excedente como % de los pasivos y la caída conjunta de BTC y oro que lo borraría.
**(b)** Explica por qué la auditoría de KPMG no invalida ese cálculo.
**(c)** Di qué otra información necesitarías para juzgar el riesgo de una corrida.

**Respuesta de referencia**

(a) Excedente y caída que lo borra:
- excedente = US$4,109,529,196, es decir **2.2% de los pasivos**;
- BTC y oro = US$24.64 mil millones; 4.11 / 24.64 = **16.7%**;
- solo oro: 21.8%; solo BTC: 70.9%.

(b) **Atestación y auditoría miden cosas distintas:**
- la atestación de BDO confirma la composición de reservas en una fecha;
- la auditoría de KPMG da una opinión sobre los estados de todo 2025 (excedente de US$6.814 mil millones al 31-dic-2025).
- **Ninguna elimina la volatilidad de BTC y oro después de esas fechas.** El colchón bajó de ~US$8.23 a US$4.11 mil millones en un trimestre, sobre todo por la caída de valor del oro y del BTC.

(c) Faltaría conocer:
- la liquidez y el plazo de los bonos del Tesoro y reportos, ~80% de las reservas según la cobertura;
- los préstamos garantizados, que bajaron US$2.38 mil millones (−15%). Eso implica ~US$13.5 mil millones restantes (cálculo propio, no reportado);
- las condiciones de redención: quién puede redimir y con qué mínimo;
- la concentración de contrapartes.

**Fuentes:** Tether (atestación del 2T-2026); CoinDesk (31-jul y 13-ago-2026); ficha 17.

---

## Pregunta 2 (exchange, método y datos)

Describe cómo medir el **flujo neto semanal** de Binance con datos públicos sin que el precio contamine la medida.

**(a)** Explica por qué se excluye BNB.
**(b)** Da los umbrales ÁMBAR y ROJA propuestos con su base estadística.
**(c)** Da la lectura al 25-sep-2026, incluidos los 3 días posteriores al reporte de Bloomberg sobre el DOJ.
**(d)** Menciona dos límites del método.

**Respuesta de referencia**

**Método:** con la API de DefiLlama `protocol/binance-cex`, se calcula el flujo = Σ por token (unidades_t − unidades_{t−7}) × precio_t. Al usar el cambio en unidades, se separa la entrada o salida real del efecto precio.

(a) **Por qué se excluye BNB:**
- las "salidas" extremas de abr-2024 y oct-2024 fueron **casi solo BNB** (−US$13.25 y −US$9.67 mil millones): reclasificaciones de carteras, no corridas;
- además, el token propio no mide la confianza de los clientes. Es la lección de FTT.

(b) **Umbrales**, sobre 1,405 ventanas sin BNB:
- ÁMBAR: < −2.1% en 7 días, el percentil 5;
- ROJA: < −5.3%, el percentil 1;
- referencia: −13.5%, la peor semana (18-dic-2022, tras FTX y la salida de Mazars).

(c) **Lectura al 25-sep-2026:**
- **+0.46%** en 7 días;
- **−0.55%** en 3 días desde el 22-sep;
- **+1.18%** en 30 días.
- **No hay señal de corrida.**

(d) **Límites:**
- DefiLlama solo ve las carteras que conoce, y las reasignaciones crean saltos;
- no ve pasivos, así que se complementa con la PoR y con retiros reales.

**Fuentes:** lista de señales (secciones E y F); cálculo propio (`scratchpad/g4/calc/flujos_binance_defillama.py`); CoinDesk (13-dic-2022) para la corrida de dic-2022.

---

## Pregunta 3 (quiebra, cálculo)

A los clientes de FTX se les ha distribuido **105% acumulado** de sus reclamos (5.ª distribución, 31-jul-2026).

**(a)** ¿Cuánto recuperó en USD un cliente que tenía 1 BTC en FTX el día de la quiebra, y qué fracción es de 1 BTC a US$84,000?
**(b)** Explica qué lección deja para la autocustodia y por qué, aun así, **no** se recomienda para la cuenta del torneo.

**Respuesta de referencia**

(a) **Recuperación:**
- los reclamos se valuaron en USD al 11-nov-2022, con BTC a US$16,871;
- 1.05 × 16,871 = **US$17,715**, el **21.1%** de US$84,000.
- Perdió ~79% en términos de BTC, aunque "recuperó 105%".

(b) **Lección:**
- en una quiebra, el cliente de un exchange pasa a ser acreedor en dólares y pierde la exposición al activo y la liquidez durante años;
- la autocustodia evita eso.

**Por qué no para el torneo:**
- traslada el riesgo operativo al dueño: los mayores robos individuales fueron por falso "soporte" (US$243, 91.4 y 282 millones);
- con 10,000 MXN y una salida vía MXN/SPEI o Bitso ya definida, la contingencia es más simple y rápida que retirar a una cartera propia.

**Fuentes:** FTX (17-jul-2026); Protos (1-feb-2024): el juez de quiebras aceptó valuar los reclamos a la fecha de la petición, con BTC a US$16,871; fichas 08, 17 y 32; bitácora del 25-sep-2026.

---

## Pregunta 4 (clasificar incidentes)

Clasifica cada caso según su naturaleza:
- **Bybit** (21-feb-2025);
- **Bitget** (24-sep-2026);
- **AscendEX** (jun-jul-2026);
- **FTX** (nov-2022).

Las categorías son: hackeo con solvencia y retiros operando; hackeo con retiros suspendidos y fondo de protección; falla de liquidez que termina en cierre; fraude con insolvencia.

Para cada uno, di **qué dato público de las primeras 24-72 horas** lo distingue y **qué harías con nuestra cuenta** si el caso fuera Binance.

**Respuesta de referencia**

**Bybit: hackeo con solvencia.**
- Perdió US$1.46 mil millones, pero procesó el 99.994% de más de 350,000 retiros en 10 horas y reunió US$1.23 mil millones en ETH en 2 días.
- **Qué harías:** vigilar y **no** activar la contingencia si los retiros fluyen.

**Bitget: hackeo con retiros suspendidos.**
- Perdió US$351.6 millones en hot y warm wallets, con retiros suspendidos "hasta revisión". Su fondo de más de US$464 millones lo cubre, 1.32 veces.
- **Qué harías:** ÁMBAR. Si pasa en Binance, comparar con el SAFU (15,000 BTC, ~US$1.26 mil millones). Activar la contingencia si los retiros no vuelven en 48 horas, que es el disparador de la bitácora.

**AscendEX: falla de liquidez.**
- Retiros sin hash durante semanas, mientras aceptaba depósitos.
- Reservas −US$240 millones el 20-jun-2026 y remanente en su token ASD.
- Cierre el 1-jul-2026, con aviso 5 días después.
- **Qué harías:** ROJA desde el primer retiro atorado. Salir.

**FTX: fraude.**
- Balance de la afiliada lleno de su token propio (2-nov-2022).
- Congelamiento de retiros y quiebra el 11-nov-2022.
- Fundador **sentenciado** a 25 años.
- **Qué harías:** ROJA. Salir antes de que se congelen los retiros.

**Fuentes:** cronología de Bybit; CoinDesk (25-sep-2026); Cointelegraph y TechTimes (jul-2026); CoinDesk (2-nov-2022); sentencia de SBF; lista de señales A2, A6 y A11.

---

## Pregunta 5 (cifras de crimen)

Chainalysis estima **US$154 mil millones** ilícitos en 2025, "<1%" del volumen; TRM estima **US$158 mil millones**, 1.2%.

**(a)** Explica dos razones de la diferencia y por qué las cifras cambian con el tiempo, con un ejemplo cuantitativo.
**(b)** Di qué parte del total es irrelevante para el riesgo de **estafa** de un inversionista pero relevante para el riesgo **regulatorio** de su exchange, con la cifra.
**(c)** Da el dato de estafas que sí importa.

**Respuesta de referencia**

(a) **Por qué difieren:**
- cada empresa usa **metodologías y atribuciones propietarias** (qué direcciones cuentan como ilícitas);
- los **denominadores** son distintos: Chainalysis usa las entradas a servicios conocidos.
- **Son cotas inferiores que se revisan:** Chainalysis subió 2024 de US$40.9 a US$57.2 mil millones (+40%). También difieren en A7A5: 93.3 frente a 72 mil millones.

(b) **Los flujos de sancionados:** US$104 mil millones, el 67.5% del total de Chainalysis (+694%), sobre todo Rusia (A7A5) e Irán.
- No son fraude contra minoristas.
- Sí son riesgo para los exchanges que los procesan. Ejemplo: la investigación del DOJ a Binance por Irán.

(c) **Estafas:** al menos **US$14 mil millones** on-chain, con una proyección de más de US$17 mil millones.
- Pago promedio de **US$2,764** (+253%).
- **Suplantación +1,400%**; con IA, 4.5 veces más rentables.

**Fuentes:** Chainalysis (introducción, 8-ene-2026; sanciones, 5-mar-2026; estafas, 13-ene-2026); CoinDesk sobre TRM (27-ene-2026); ficha 32.

---

## Pregunta 6 (puentes, técnica e inversión)

Compara el reto **Withdrawal** de Damn Vulnerable DeFi v4 con los hackeos de **KelpDAO** (18-abr-2026) y **Ronin** (mar-2022).

**(a)** Di qué invariante se rompe en los tres.
**(b)** Explica por qué una auditoría de contratos no habría detectado KelpDAO.
**(c)** Di qué diseño de quórum o de monitoreo lo habría mitigado.
**(d)** Explica qué implica para mantener BTC "envuelto" (por ejemplo, BTCB) en lugar de BTC nativo.

**Respuesta de referencia**

(a) **El invariante:** "lo liberado en el destino = lo quemado o bloqueado en el origen".
- En Withdrawal, el operador puede finalizar sin prueba Merkle, y un retiro fallido queda marcado como finalizado.
- En KelpDAO se liberaron 116,500 rsETH (~US$292 millones) contra una quema que nunca ocurrió.
- En Ronin se comprometieron 5 de 9 llaves de validadores, justo el umbral (~US$625 millones).

(b) **No fue un fallo de contrato.** Un solo verificador (LayerZero Labs DVN) leía de nodos RPC que el atacante comprometió, mientras tumbaba con DDoS los nodos externos. Cada transacción on-chain era "válida".

(c) **Mitigación:**
- varios verificadores independientes, no "1 de 1";
- un quórum repartido entre organizaciones (Ronin anunció subir a 8 de 9);
- monitoreo de invariantes entre cadenas, con pausa automática. En KelpDAO, la pausa evitó un segundo intento de US$95 millones.

(d) **BTC envuelto:** suma el riesgo del puente o del custodio al del BTC. Para la cuenta, **solo BTC nativo** en spot.

**Fuentes:** `src/withdrawal/L1Gateway.sol` (DVDF); Chainalysis (23-abr-2026); post-mortem de Ronin; fichas 25 y 33.

---

## Pregunta 7 (estatus legal y escritura responsable)

Da el **estatus legal exacto** al 25-sep-2026 (acusado, demandado, investigado, sentenciado, indultado o absuelto) de:
1. SBF;
2. CZ;
3. Binance como empresa;
4. el acusado principal del robo de US$243 millones al acreedor de Genesis;
5. el operador del ataque a Mango Markets;
6. el presidente de Prince Group;
7. LayerZero frente a KelpDAO;
8. Binance frente a la pesquisa sobre Irán.

Explica por qué la distinción importa en nuestros documentos y en el umbral E5.

**Respuesta de referencia**

1. **SBF:** **sentenciado**. Culpable de 7 cargos (2-nov-2023), 25 años (28-mar-2024). El 2.º Circuito confirmó (12-jun-2026) y pidió revisión a la Suprema Corte (sep-2026).
2. **CZ:** se **declaró culpable** en 2023 (AML), fue **sentenciado** a 4 meses, que cumplió en 2024, e **indultado** el 23-oct-2025.
3. **Binance:** **se declaró culpable** y pagó US$4.3 mil millones, con monitores (nov-2023). Hoy está **investigada** por el DOJ por Irán, **sin cargos**.
4. **Acusado principal del caso Genesis:** **se declaró culpable** de conspiración RICO el 8-sep-2026 y **espera sentencia**. Hay 18 acusados y 3 coacusados ya sentenciados.
5. **Operador de Mango Markets:** un jurado lo había declarado culpable, pero **el 23-may-2025 el juez anuló las condenas** por fraude y manipulación y lo **absolvió** de un tercer cargo.
6. **Presidente de Prince Group:** **acusado** en EUA y **designado** por OFAC. Fue arrestado en Camboya y **extraditado a China** (ene-2026). No tiene sentencia en EUA.
7. **LayerZero:** **demandado** en un proceso civil en Columbia Británica (25-sep-2026). LayerZero dice que la demanda "no tiene mérito".
8. **Binance frente a Irán:** es una **investigación reportada por la prensa** (Bloomberg, 22-sep-2026). No hay acusación ni fuente primaria del DOJ.

**Por qué importa:**
- afirmar culpabilidad sin sentencia es riesgo de difamación y es un error factual;
- en E5, **"investigado"** vale ÁMBAR y **"cargos penales contra la entidad"** vale ROJA. Confundirlos dispararía la contingencia sin causa.

**Fuentes:** sentencia ECF 424 (hoja 1), Al Jazeera y CNN; CNN y PBS (indulto); Tesoro (21-nov-2023); CoinDesk (22-sep-2026); Fortune y Cryptonomist (sep-2026); TRM Labs (may-2025); Chainalysis (estafas); CoinDesk (25-sep-2026).

---

## Pregunta 8 (prueba de reservas)

El 45.º reporte de PoR de Binance (foto del 1-ago-2026) muestra ~657,000 BTC de usuarios con un **ratio de 100.25%**. El 46.º (foto del 1-sep, publicado el 17-sep) muestra ~682,000 BTC y un ratio "≥1:1". Binance tiene un SAFU de **15,000 BTC** y se compromete a reponerlo si baja de US$800 millones.

**(a)** Calcula el excedente de BTC implícito en el 100.25% y el precio de BTC al que el SAFU toca US$800 millones.
**(b)** Enumera cinco cosas que una PoR **no** prueba, con un caso real para al menos tres.
**(c)** Da tu calificación de E3 y E4 para Binance hoy.

**Respuesta de referencia**

(a) **Cálculos:**
- 0.25% × 657,000 = **~1,642 BTC** de excedente;
- 800,000,000 / 15,000 = **US$53,333** por BTC.
- [I] El SAFU en BTC es **procíclico**: se encoge justo cuando el mercado cae y aumentan la tensión y los retiros.

(b) **Lo que una PoR no prueba:**
1. **Otros pasivos** del exchange, fuera de los saldos de clientes: deuda y préstamos.
2. **Que los activos no estén comprometidos** o prestados, ni que se puedan vender sin impacto.
3. **Que no haya una inyección temporal** en la fecha de la foto. Casos: la "verificación" de Tether de 2017 con dinero depositado esa mañana (NYAG); Bitfinex transfirió US$382 millones antes de una revisión (CFTC); la inyección de ~US$240 millones de AscendEX que se fue en semanas.
4. **Seguridad operativa y cumplimiento.** Caso: la PoR no detecta llaves comprometidas como en Bybit, ni exposición a sanciones como la investigación del DOJ.
5. **Que los retiros funcionen hoy.** El rezago es de 16 días. Caso: Mazars se retiró en dic-2022 porque el público no entendía esos reportes, y Binance tuvo ~US$6 mil millones de salidas en 72 horas.

(c) **Calificación:**
- **E3: LIMPIA.** El ratio es ≥100%, el reporte es mensual y el rezago es menor a 30 días. Delgado en BTC, pero sin alerta.
- **E4: LIMPIA.** Con BTC a ~US$84,000, el SAFU vale ~US$1.26 mil millones, arriba del umbral de US$800 millones. Vigilar si BTC baja de ~US$53,333.

**Fuentes:** PANews (17-sep-2026); CoinAlert y crypto.news (19-ago-2026); CoinDesk (12-feb-2026); NYAG (23-feb-2021); CFTC (15-oct-2021); TechTimes (12-jul-2026); CoinDesk (13 y 16-dic-2022); lista de señales (secciones E y G).
