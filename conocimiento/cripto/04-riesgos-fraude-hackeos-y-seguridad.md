# Capítulo 04 · Riesgos, fraude, hackeos y seguridad (grupo G4)

- **Autor:** `analista-cripto`, 25-sep-2026.
- **Base:** 6 recursos del dueño estudiados hoy (08, 17, 22, 25, 32 y 33), más fuentes primarias (tribunales, reguladores, emisores y datos on-chain) para verificar cada hecho clave.
- **Etiquetas:** [H] hecho con fuente · [I] inferencia · [O] opinión.
- **Documentos operativos que salen de este capítulo:** [`lista-senales-de-alerta.md`](lista-senales-de-alerta.md) y [`examen/banco-g4-riesgo.md`](examen/banco-g4-riesgo.md).

## 0. Por qué este capítulo manda sobre la cuenta cripto

Nuestra cuenta `arena-claude-binance`:
- opera **solo spot, con BTC**;
- está en un exchange **no supervisado en México**;
- ese exchange **se declaró culpable en 2023** de fallas de AML y sanciones;
- el DOJ lo investiga hoy por sanciones a Irán (Bloomberg, 22-sep-2026; sin cargos).

Con 10,000 MXN y un tope de pérdida de 5,000, **el riesgo de mercado lo acotan los cortacircuitos, pero el de contraparte no**. Lo dice la propia bitácora: "un congelamiento total arriesga los 10,000 MXN".

Este capítulo existe para ver venir ese riesgo con datos públicos.

## 1. Mapa del tema, de licenciatura a frontera

| Nivel | Qué hay que dominar | Recursos y fuentes | Prueba de dominio |
|---|---|---|---|
| **Licenciatura** | Taxonomía del riesgo cripto: **contraparte** (exchange o custodio), **emisor** (stablecoin), **técnico** (contrato o puente), **operativo** (llaves, firmas, personas), **fraude** (estafa, "rug pull", "pig butchering"), **regulatorio** y **físico**. Vocabulario: hot, warm y cold wallet; frase semilla; multisig; PoR; atestación frente a auditoría. Casos clásicos: FTX, Celsius, Terra y Tether 2016-2019. | Ficha 17 (Number Go Up), ficha 32 (Chainalysis), capítulo 17 de la base (crisis) | Explicar por qué a un cliente de FTX le devolvieron el 105% en USD y aun así perdió el 79% en términos de BTC |
| **Maestría** | **Medir:** flujos netos de un exchange sin el efecto precio; leer una PoR (alcance, ratio, composición, rezago); calcular el colchón de una stablecoin frente a sus activos volátiles; leer las cifras de crimen como cotas inferiores con definiciones distintas; patrones de lavado (ciclo de ~45 días de Corea del Norte). | Ficha 32; lista de señales, secciones E-G; ficha 08 (ZachXBT) | Reproducir los percentiles de flujo de Binance con la API de DefiLlama y justificar por qué se excluye BNB |
| **Doctorado** | **Clases de vulnerabilidad:** oráculos (spot, TWAP corto, reentrada de solo lectura), gobernanza con préstamo relámpago, proxies e inicialización, validar después de ejecutar, redondeo, mensajes entre cadenas; en Solana, verificaciones de firmante, dueño y PDA. **Ataques operativos:** firma a ciegas, interfaz comprometida, RPC envenenado, "durable nonces". **Resultados legales:** acusado, demandado, sentenciado, absuelto. | Fichas 25 (DVDF), 22 (Cyfrin) y 33 (Solana); Chainalysis sobre Drift y KelpDAO | Explicar qué invariante rompieron KelpDAO y el reto Withdrawal, y por qué una auditoría de contrato no lo habría detectado |
| **Frontera (2026)** | Ataques a exchanges por la **infraestructura de firma** (Bybit 2025; Bitget, 24-sep-2026). **Puentes "1 de 1"** (KelpDAO). **Administración con prefirmas** (Drift). **Cierres de exchanges por MiCA y por liquidez** (AscendEX, BitMart). Binance en la UE con **solo retiros**. **Tether auditado por KPMG** con un colchón que se redujo a la mitad. **Ataques físicos** alimentados por filtraciones de datos. **Estafas con IA** (+1,400% en suplantación). | Fichas 08, 32 y 33; la lista de señales | Llenar el tablero E1-E10 de Binance con datos del día y defender la calificación ante el comité |

## 2. Las 10 ideas que más importan para invertir

**1. Para quien tiene BTC en un exchange, el riesgo de contraparte pesa más que el técnico, y la quiebra convierte monedas en dólares.**
- [H] Los clientes de FTX recuperaron **105% nominal**, pero en USD a precios del 11-nov-2022, con BTC a US$16,871 (FTX, 17-jul-2026).
- [I] Eso es **21% en términos de BTC** frente a ~US$84,000 hoy.
- **Consecuencia:** el tope de exposición en un exchange es la pérdida máxima tolerable **total**, no la "esperada".

**2. Las señales tempranas de un exchange en problemas son públicas y se pueden medir.**
- [H] **FTX:** el balance de Alameda publicado el 2-nov-2022 estaba lleno de FTT, y la quiebra llegó 9 días después.
- [H] **Binance, dic-2022:** ~US$6 mil millones de salidas en 72 horas, y Mazars suspendió su PoR el 16-dic.
- [H] **AscendEX, 2026:** retiros sin hash, reservas −US$240 millones y el remanente concentrado en su token ASD; cerró el 1-jul-2026.
- [I] **Consecuencia:** tablero semanal E1-E10 (lista de señales) y reglas ROJA y ÁMBAR decididas **antes** del evento.

**3. Un hackeo grande no equivale a insolvencia. La diferencia se ve en los retiros de las primeras 24-72 horas.**
- [H] **Bybit** perdió US$1.46 mil millones (21-feb-2025), pero procesó el 99.994% de más de 350,000 retiros en 10 horas y repuso el ETH en dos días.
- [H] **Bitget** (24-sep-2026) suspendió retiros y dice cubrir los US$351.6 millones con un fondo de más de US$464 millones.
- [H] **FTX y AscendEX** no pagaron.
- [I] **Consecuencia:** ante un incidente en Binance hay que mirar si procesa retiros y si el SAFU cubre la pérdida (hoy 15,000 BTC), no el titular.

**4. El riesgo técnico dominante de 2025-2026 es operativo, no un bug de contrato.**
- [H] En el 1T-2025, el **88%** de las pérdidas fue por ataques a la infraestructura de llaves y firmas de servicios centralizados.
- [H] Corea del Norte hizo el **76%** de los compromisos de servicios y robó **US$2.02 mil millones** (Chainalysis).
- [H] **Casos de 2026:**
  - KelpDAO: un verificador "1 de 1" con RPC envenenados, US$292 millones;
  - Drift: multisig 2 de 5 sin timelock y prefirmas, US$285 millones;
  - Bitget: backend comprometido que falsificó transferencias.
- [I] **Consecuencia:** la pregunta de diligencia no es "¿está auditado?", sino **"¿quién puede firmar qué, con qué quórum y con qué retraso?"**.

**5. Una PoR o una atestación es una foto acotada. Valen la serie, la composición y los retiros reales.**
- [H] **Fotos maquilladas de Tether:**
  - en 2017 "verificó" efectivo depositado esa misma mañana;
  - en 2018, un día después de la carta de su banco, movió cientos de millones (NYAG);
  - Bitfinex le pasó US$382 millones antes de una revisión (CFTC).
- [H] AscendEX recibió una inyección de ~US$240 millones que se fue en semanas.
- [H] **Binance hoy:** PoR mensual con 16 días de rezago; ratio de BTC de 100.25% en agosto, es decir, un colchón de ~1,642 BTC [I].
- **Consecuencia:** la PoR se cruza con flujos (E1) y retiros (E6).

**6. El riesgo de una stablecoin ya no es solo "no hay reservas": son reservas volátiles con un colchón delgado, más el poder del emisor para congelar.**
- [H] **Tether (2T-2026):** colchón de US$4.11 mil millones, el 2.2% de los pasivos, con US$24.64 mil millones en BTC y oro. [I] Una caída conjunta de 16.7% lo borra. La auditoría de KPMG de 2025 no cambia esa sensibilidad.
- [H] USDC tuvo el 8% de sus reservas atrapado en SVB y cayó a ~US$0.87-0.88 (mar-2023).
- [H] Circle y Tether congelan fondos cuando quieren o cuando deben.
- [I] **Consecuencia:** la reserva de la cuenta en **MXN** (decisión del comité) es correcta. Si se usa USDT como puente, que sea por minutos.

**7. En Binance, el riesgo con más probabilidad de materializarse es el regulatorio, y el precedente da pocos días de aviso.**
- [H] En la UE, Binance retiró su solicitud MiCA el 24-jun-2026 y **desde el 1-jul solo permite retiros**, con ~6 días de aviso.
- [H] En México no está supervisada (bitácora).
- [H] El DOJ la investiga por Irán, **sin cargos**.
- [H] El estado de los monitores de 2023 no está confirmado.
- [I] **Consecuencia:** la contingencia en Bitso debe estar **verificada y probada antes** del evento. La bitácora la marca como pendiente del dueño para el 2-oct.

**8. Las cifras de "crimen cripto" son cotas inferiores con definiciones propias; no mezclarlas con el riesgo de fraude.**
- [H] Chainalysis revisó 2024 de US$40.9 a US$57.2 mil millones (+40%).
- [H] En 2025, el 67.5% del ilícito son flujos de **sancionados** (Rusia con A7A5, Irán).
- [H] TRM da US$158 mil millones y 1.2% del volumen, contra US$154 mil millones y "<1%" de Chainalysis.
- [I] **Consecuencia:**
  - para el riesgo de **estafa** del inversionista, la cifra relevante son las estafas (≥US$14 mil millones on-chain, suplantación +1,400%);
  - para el riesgo **regulatorio del exchange**, la relevante es la exposición a sancionados.

**9. La autocustodia quita la contraparte, pero traslada el riesgo al dueño: ingeniería social, firma a ciegas y ataques físicos.**
- [H] Las mayores pérdidas individuales fueron por falso "soporte": US$243 millones (2024), US$91.4 millones (2025) y US$282 millones (2026).
- [H] Hubo 158,000 incidentes contra carteras personales en 2025.
- [H] Los ataques físicos llegaron a un récord de US$58 millones, en parte por filtraciones de datos.
- [I] **Consecuencia práctica:**
  - nunca atender "soporte" entrante;
  - verificar en el dispositivo, no en el sitio (Cyfrin);
  - no revelar tenencias;
  - para el torneo, la ruta de salida del plan (vender a MXN y SPEI, o BTC a Bitso) es más simple que la autocustodia.

**10. Para tokens y protocolos bastan filtros rápidos: una sola falla descalifica.**
- [H] **Los filtros, con su caso:**
  - administración de umbral bajo sin timelock (Drift);
  - "1 de 1" (KelpDAO);
  - quórum concentrado (Ronin: 5 de 9);
  - oráculo en un pool delgado (Puppet, Mango, Drift);
  - gobernanza con votos del momento (Beanstalk);
  - rendimiento "garantizado" (Anchor, 19.5%);
  - oferta concentrada (M, −75%);
  - equipo que no divulga incidentes.
- [I] **Consecuencia para la cuenta:**
  - solo BTC spot;
  - nada de Earn;
  - nada de BNB o BNSOL como inversión;
  - nada de BTC envuelto o puenteado.

## 3. Contradicciones entre recursos (y cómo las resuelvo)

| # | Contradicción | Recursos | Resolución |
|---|---|---|---|
| 1 | **Tether:** el libro insinúa que las reservas no existían, pero Tether sobrevivió. En 2022 su capitalización bajó US$16 mil millones en dos meses, una señal de redenciones pagadas, y en 2026 tiene una auditoría de KPMG sin salvedades. | 17 contra CoinDesk (2022, 2026) | [I] Las **falsedades de 2016-2019** están probadas (NYAG, CFTC). **La insolvencia actual no.** El riesgo vigente es un colchón delgado con activos volátiles. |
| 2 | **"US$3.1 mil millones robados en hackeos cripto en 2022"** (Cyfrin) contra **US$3.8 mil millones** (Chainalysis) | 22 contra Chainalysis (1-feb-2023) | [H] Los 3.1 son **solo DeFi** (82.1% del total). Es un error de alcance del curso. |
| 3 | **Volumen ilícito de 2025:** Chainalysis da US$154 mil millones y "<1%"; TRM da US$158 mil millones y 1.2%. **A7A5:** 93.3 contra 72 mil millones. **Hackeos:** 3.4 contra ~3 mil millones. | 32 contra TRM (CoinDesk, 27-ene-2026) | [I] Son metodologías propietarias. Se reporta el rango y no se suman fuentes. |
| 4 | **Nobitex:** ZachXBT da US$81.7 millones y Chainalysis "más de US$90 millones" | 08 contra 32 | [I] La diferencia viene del momento de la estimación y del perímetro de carteras. Se usa "~US$80-90 millones". |
| 5 | **Hardware wallets:** ZachXBT dice que son "basura" y recomienda un iPhone dedicado; Cyfrin dice que el hardware es "la fuente de verdad" y la multisig es lo mejor; Chainalysis recomienda "custodia segura" | 08 [O] contra 22 y 32 | [I] Pesa más el consenso de dos fuentes, respaldado por casos (Bybit: verificar en el dispositivo). La opinión de ZachXBT es grado D. |
| 6 | **¿Mejora la seguridad DeFi?** Chainalysis ve pérdidas "contenidas" en 2024-2025 pese a un TVL mayor; en 2026 llegan Drift (US$285 millones) y KelpDAO (US$292 millones); ZachXBT dice que la industria está "cocinada" | 32 contra 33, 08 y Chainalysis 2026 | [I] La "fase 3" de Chainalysis describía 2024-2025. En 2026 los ataques se desplazaron a la **operación** (llaves y verificadores), no al código. Ambos tienen razón en su perímetro. |
| 7 | **Exchanges como vía de lavado:** Chainalysis ve una baja "porque pueden congelar"; ZachXBT documenta casos concretos a través de exchanges grandes (XRP, 2024, incluido Binance) y cuentas de KuCoin con KYC comprado | 32 contra 08 | [I] Es tendencia agregada contra casos. Para Binance, el riesgo relevante es **regulatorio** (sanciones), no de solvencia. |
| 8 | **Qué enseñar:** DVDF y los cursos de Cyfrin se centran en bugs de contrato (solo 1 de 18 retos es operativo), mientras las pérdidas reales de 2025-2026 fueron operativas | 25, 22 y 33 contra 32 | [I] Los recursos técnicos sirven para leer auditorías y protocolos. Para la cuenta pesan más los cursos de carteras de Cyfrin y la lista de señales. |
| 9 | **Fecha de KelpDAO:** 18-abr-2026 (Chainalysis y ZachXBT en tiempo real) contra "22-abr" (CoinDesk, 25-sep-2026) | 32 y 08 contra la prensa | [I] Se usa el **18-abr-2026**: dos fuentes independientes, una en tiempo real. |
| 10 | **Nivel y duración del curso de Solana:** la página dice "Beginner, 1 h"; el índice del dueño, "Avanzado"; el temario tiene 9 secciones | 33 | [I] Es avanzado para un inversionista, y la página es inconsistente. |
| 11 | **¿Tether está auditada?** El FMI (DP 25/09, dic-2025) dice que "not subject to a full, independent audit", y así lo recogen la ficha 30 y el capítulo 05. El 13-ago-2026, Tether anunció una opinión sin salvedades de KPMG EUA sobre sus estados de 2025, y KPMG confirmó la opinión. | 30 y cap. 05 (G5) contra 17 | [H] **El dato del FMI quedó desactualizado el 13-ago-2026.** Lo que sigue vigente es que el informe de KPMG no se ha publicado en lo que revisé y que la auditoría no elimina la sensibilidad del colchón (16.7%). El G5 debería añadir una adenda a su capítulo; no la escribo yo porque no es mi archivo. |
| 12 | **Recuperación de FTX:** "119%" (fichas 09 y cap. 06, G6) contra "105%" (ficha 17) | 09 contra 17 | [H] **Son compatibles.** El 119% es lo que el plan del 7-oct-2024 prometía al 98% de los acreedores por número (casi todos reclamos chicos de "conveniencia", hoy en 120%). El 105% es lo distribuido a jul-2026 a los reclamos de clientes grandes (clases 5A y 5B). Ambos se valúan en USD a la fecha de la petición (BTC a US$16,871). |

## 4. Implicaciones concretas para `arena-claude-binance` (propuesta para el comité y el gestor de riesgo)

1. **Tablero semanal E1-E10** de la lista de señales, en la corrida de cripto. Al 25-sep-2026 no hay ROJAS.
   - Hay ÁMBAR en **E5** (investigación del DOJ; monitores sin confirmar) y en **A9** (sin licencia en México; solo retiros en la UE).
2. **Bitso verificada y probada** con un depósito y un retiro mínimos **antes** del primer tramo grande. El precedente de la UE sugiere ~6 días de aviso.
3. **Sin saldos ociosos en USDT**, sin Earn ni colateral, y sin BNB ni BNSOL. Si se usa MXN→USDT→BTC, que sean minutos.
4. **Tras un incidente de seguridad en Binance**, se decide con E6 (¿procesa retiros?) y E4 (¿lo cubre el SAFU?). Un incidente mayor que el SAFU sin comunicado en 24 horas es ROJA y activa la contingencia.
5. **Regla de contagio:** la pausa de retiros de otro exchange grande (hoy, Bitget) sube la vigilancia de E1 a diaria mientras dure.

## 5. Enlaces a las fichas

| # | Recurso | Ficha | Acceso | Grado |
|---|---|---|---|---|
| 08 | ZachXBT (X, Telegram, Mirror) | [recursos/08-zachxbt.md](recursos/08-zachxbt.md) | Sección: Telegram completo en texto; X no | C (B en hechos confirmados; D en opiniones) |
| 17 | Number Go Up (Zeke Faux, 2023) | [recursos/17-number-go-up.md](recursos/17-number-go-up.md) | Resumen: libro no leído | B en hechos / C en la tesis sobre Tether |
| 22 | Cyfrin Updraft | [recursos/22-cyfrin-updraft.md](recursos/22-cyfrin-updraft.md) | Sección | B / C en cifras de las lecciones |
| 25 | Damn Vulnerable DeFi v4 | [recursos/25-damn-vulnerable-defi-v4.md](recursos/25-damn-vulnerable-defi-v4.md) | Íntegro: enunciados y código | A técnico / C para invertir |
| 32 | 2026 Crypto Crime Report (Chainalysis) | [recursos/32-2026-crypto-crime-report.md](recursos/32-2026-crypto-crime-report.md) | Sección: capítulos principales | B / C en agregados interanuales |
| 33 | Solana Development Course (Cyfrin) | [recursos/33-solana-development-course.md](recursos/33-solana-development-course.md) | Sección | B técnico / C en cobertura |

**Pendiente para otra sesión:**
- leer el PDF completo de Chainalysis (con registro);
- los capítulos de ransomware y darknet;
- los hilos de ZachXBT en X de 2021-2022 (sin sesión no se puede);
- los videos de Cyfrin (caso Bybit);
- las hojas 2-7 de la sentencia de SBF, que necesitan OCR.
