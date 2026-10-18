# Ficha de avance · 18-oct-2026 · ETF spot de ether: ETHA sin staking frente a ETHB con staking, rendimiento realizado y riesgo de liquidez

> Corrida de las 08:17 CDMX (14:18 UTC), estudio profundo. Nivel **Maestría** (flujos de ETF spot), grupo G5 (mercado, on-chain e institucional).
>
> **Por qué este tema.** Los 35 recursos del dueño están en `estudiado` y los 6 temas del plan ya tienen ficha. El pendiente de nivel más bajo que seguía sin ficha es el punto 5 del plan de cobertura (`rutinas/REGLAS-MOTOR.md` §7): "ETFs spot de Ether: flujos, *staking* y qué dejar en spot". Hasta hoy solo existía un párrafo de prensa secundaria en `arena/investigacion/13-radar-cripto-2026-10-05.md` §8. Esta ficha lo pasa a fuente primaria (SEC) y le agrega el dato de la red.

## 0. Preguntas de hoy

1. ¿Qué cobra y qué promete ETHB, el ETF de BlackRock con staking, según su propio prospecto?
2. ¿Cuánto rindió de verdad en su primer trimestre completo, comparado con lo que daba la red?
3. ¿Qué riesgo de liquidez añade el staking, medido con la cola de validadores de hoy?
4. ¿Cambia algo para "dejar en spot" en `arena-claude-binance` o para la cuenta GBM?

## 1. Acceso y fuentes (declarado)

- **Primaria, grado A:** SEC EDGAR, iShares Staked Ethereum Trust ETF (ETHB), CIK 0002099103 ([lista de presentaciones](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0002099103)).
  - **10-Q al 30-jun-2026** (acc. 0001437749-26-027003, presentado el 11-ago-2026): estados financieros y notas 1-4. Se extrajo el texto completo y se buscaron los términos con Python. **Acceso: sección** (estados, notas y el MD&A con búsqueda dirigida; no se leyó palabra por palabra todo el documento).
  - **Prospecto 424B3 del 11-mar-2026** (acc. 0001437749-26-007771, 899 mil caracteres): comisiones, staking, Liquidity Sleeve, cola de salida y suspensión de reembolsos. **Acceso: sección** (búsqueda dirigida de 12 términos).
  - **Suplemento 424B3 del 31-jul-2026** (acc. 0001437749-26-025220): **íntegro**. Solo agrega una restricción de oferta en Abu Dhabi; no cambia comisiones ni staking.
- **Red, grado B:** [validatorqueue.com](https://www.validatorqueue.com/) (datos de beaconcha.in), con portada en vivo y el historial diario incrustado en el HTML (1,236 filas, del 21-may-2023 al 18-oct-2026). La API de beaconcha.in pide clave (401).
- **ETHA:** comisión de 0.25% y sin staking, según la página de iShares que se revisó el 5-oct (radar 13, [V]). Hoy no se volvió a verificar.
- **Flujos diarios de ETF de ether: no se consiguieron hoy.** Farside y SoSoValue dan 403, tftc.io solo tiene BTC y bitbo no tiene página de ETH. Quedan los datos de prensa del radar del 5-oct (grado C).
- **Prensa, grado C-D:** [blockeden.xyz, 14-mar-2026](https://blockeden.xyz/blog/2026/03/14/blackrock-ethb-yield-bearing-ether-etf-staking-meets-wall-street/) y [Cointelegraph](https://cointelegraph.com/news/blackrock-ishares-staked-ethereum-trust-etf-exposure-yield) daban un rendimiento neto de 1.75-2.2%. Hoy se compara contra la fuente primaria.

## 2. Lo que dice la SEC [H, grado A]

| Concepto | Dato | Documento |
|---|---|---|
| Comisión del patrocinador | 0.25% anual sobre el NAV. Exención a **0.12% por 12 meses desde el 12-mar-2026**, sobre los primeros 2.5 mil M USD | 10-Q, nota 3 |
| Parte de la recompensa que no llega al fondo | **18% de la recompensa bruta** (patrocinador más agente Coinbase Prime y validadores). El fondo retiene el 82% | Prospecto |
| Proporción stakeada | Meta de "70% - 95% under normal market circumstances". Real al 30-jun: **250,585 ETH = 86.9%** | Prospecto y 10-Q |
| Distribución | En USD, "monthly but no less frequently than quarterly", sin reinversión automática. 2T: 0.02 USD por acción | 10-Q, nota 2F |
| Tamaño al 30-jun | Activo neto de 459.4 M USD, 22.4 M de acciones, NAV de 20.51 (lanzamiento a 25.00). Rendimiento desde el inicio: −17.90% | 10-Q |
| 2T-2026 | Ingreso por staking de **1,194,785 USD**. Comisión con la parte de staking del patrocinador: 419,914, menos 179,522 exentos. NII anualizado 0.69%; gastos de 0.30% antes de la exención y 0.17% después | 10-Q |
| Salida de staking | Unos 32 minutos para salir del conjunto activo, ~27 horas de retraso obligatorio y un barrido de ~7-10 días. "The longest recorded exit queue for Ethereum was 46.5 days" | Prospecto |
| Si el colchón no alcanza | "the Trust may seek to delay settlement of redemptions with Authorized Participants until the Trust has sufficient unstaked ether". Los AP pueden cancelar o dejar de participar, y la prima o el descuento pueden abrirse | Prospecto |
| Fiscal (EUA) | La recompensa es ingreso gravable en EUA (grantor trust) | 10-Q, nota 2G |

**Confirmado contra prensa:** el 18% de la recompensa, la exención de 0.12% y el rango de 70-95% coinciden con lo que traía el radar del 5-oct. **Corrección:** el radar decía "pasa 82% de recompensas cada mes". El prospecto dice que distribuye mensualmente **pero no menos de cada trimestre**: "cada mes" es la meta, no un compromiso.

## 3. Ejercicio numérico (comprobado en Python)

Script: [`2026-10-18-etf-ether-staking.py`](2026-10-18-etf-ether-staking.py) (`python3 -I ... vq_hist.json`). Se corrió el 18-oct a las 14:2x UTC.

**[1] La cola de salida de hoy, con dos lecturas.** En la fila diaria del historial hay 928,024 ETH en la cola de salida (la portada en vivo decía 914,652). A 256 ETH por época (el tope de EIP-7251) y 225 épocas por día, la espera es de **16.11 días**, igual a lo que publica el sitio; el script lo comprueba con `assert`. La cola de entrada es de 1,269,887 ETH (22.05 días). El APR de la red es de **2.57%**, con 43.67 M de ETH stakeados (35.8% de la oferta).

**[2] Rendimiento neto teórico con el APR de hoy:** APR × fracción stakeada × 0.82 − comisión.

| Stakeado | ETHB con exención (0.12%) | ETHB sin exención (0.25%) | Ventaja sobre ETHA (−0.25%) |
|---|---|---|---|
| 70% | 1.355% | 1.225% | 1.48-1.61 pp |
| **86.9% (real al 30-jun)** | **1.711%** | **1.581%** | **1.83-1.96 pp** |
| 95% | 1.882% | 1.752% | 2.00-2.13 pp |

La prensa (1.75-2.2%) usaba un APR de 3%. Con el 2.57% de hoy, el neto cae a ~1.6-1.7%.

**[3] Rendimiento realizado en el 2T-2026 (el hallazgo de hoy).** Se calculó con dos métodos que coinciden:
- **Método 1:** el activo neto medio implícito es 419,914 / (0.30% × 91/365) = **561.4 M USD**. El ingreso por staking anualizado da 1,194,785 × 365/91 / 561.4 M = **0.854%**.
- **Método 2:** el NII anualizado más los gastos tras la exención dan 0.69% + 0.17% = **0.860%**.
- **Teórico:** el APR medio de la red en el 2T fue de 2.79% (historial diario). Con 86.9% stakeado da **2.43%**.
- **Realizado sobre teórico = 35%.** [I] La explicación más probable es la **cola de entrada**: entre el 12-mar y el 30-jun la espera media para empezar a stakear fue de **54.0 días**. El ETH que entraba al fondo por creaciones (133 M USD en especie solo en el 2T) tardaba casi dos meses en empezar a rendir. Además, el fondo arrancó el 12-mar y su staking fue escalando. El 10-Q no separa cuánto del 86.9% ya estaba activo y cuánto seguía en cola, así que esto es inferencia (grado B-C).
- **Matiz que no se pudo resolver:** el 10-Q no dice si el "staking income" ya viene neto de la parte del agente o solo de la del patrocinador. Si viniera neto de todo el 18%, el teórico comparable sería 1.99% y la razón subiría a 43%. La conclusión no cambia.

**[4] Liquidez.** Desstakear hoy toma 16.1 días de cola, 1.1 de retraso y 7.2 de barrido: **24.4 días**. El colchón sin stakear al 30-jun era de **13.1%** del fondo. El máximo histórico de espera de salida en los datos es de **46.41 días (13-sep-2025, 2,673,349 ETH)**, consistente con los "46.5 days" del prospecto (cotejo independiente).

**[5] Tasa base para el pronóstico P0141.** ¿La cola de salida a 29 días queda debajo de la de hoy?
- En todas las ventanas: 541/1,207 = 44.8%.
- Con la cola arriba de 500k: 98/149 = 65.8%.
- Con la cola arriba de 800k: **86/116 = 74.1%**. Pero son ventanas traslapadas de unos 2 episodios (ago-dic 2025), así que es grado C.
- **Dato nuevo sin explicar:** la cola pasó de 166,042 ETH (29-sep) a **850,736 (2-oct)** en un salto de un día (~685k ETH) y sigue alrededor de 0.9-1.0 M. No se identificó quién sale. Puede ser un gran operador o un custodio rebalanceando (grado D hasta tener evidencia).

## 4. Qué cambia para invertir [I/O]

1. **`arena-claude-binance`:** nada. ETH no está en el universo activo y el perfil prohíbe el staking con bloqueo. El ETH en Binance spot no rinde, y eso es una decisión, no un descuido. La ventaja de ~1.6-2.0 pp al año de un ETF con staking no alcanza para justificar la comisión de GBM (~0.29% por lado), el tipo de cambio y un universo nuevo, sobre todo cuando el rendimiento realizado del primer trimestre fue de 0.85%.
2. **Si algún día se considera ETH vía GBM:** no está verificado que ETHA o ETHB coticen en el SIC; se marca **[NV]** y no se asume. La comparación correcta es el rendimiento neto realizado (lo que muestran los 10-Q), no el APR de la red.
3. **El rendimiento del staking es una promesa con rezago:** mientras la cola de entrada sea larga (22 días hoy y 54 en promedio en mar-jun), el ETH nuevo tarda semanas en rendir. Un fondo que crece rápido rinde menos de lo que dice su folleto.
4. **El staking cambia el ETF de liquidez diaria a liquidez con colchón:** con 13% sin stakear y 24 días para desstakear, una ola de reembolsos mayor al colchón puede retrasar la liquidación con los AP y abrir el descuento. En septiembre de 2025 habrían sido 46 días. Es un riesgo de cola nuevo que ETHA no tiene.
5. **Lectura de flujos:** un reembolso de ETHB no es lo mismo que uno de ETHA. ETHB puede tener que **salir de staking**, y eso aparece en la cola de salida de la red. Esto sugiere vigilar la cola junto con los flujos [I, sin evidencia todavía de que el salto del 2-oct venga de ETF].

## 5. Contrapuntos y límites

- **n=1 trimestre** de un solo fondo. El 3T (10-Q esperado hacia el 10-13 de noviembre) dirá si la brecha se cierra cuando el staking madura. Si se cierra, el punto 3 pierde peso.
- El activo neto medio se infirió de la comisión. Coincide con el método 2, pero las dos cuentas dependen de las razones redondeadas del 10-Q.
- El APR del sitio es un promedio de la red. Los validadores de ETHB (Figment, Galaxy y Attestant, según la prensa; no se verificó en el prospecto) pueden rendir distinto.
- El historial de validatorqueue.com es de un tercero (beaconcha.in), grado B. No se cotejó con un nodo propio.
- No se revisaron ETHE ni ETH de Grayscale, que tienen staking desde oct-2025, ni FETH.

## 6. Autoexamen

1. ¿Qué parte de la recompensa bruta no llega a ETHB? → 18%.
2. ¿Por qué el rendimiento realizado del 2T fue de ~0.85% y no ~2.4%? → Cola de entrada (54 días en promedio) y arranque del staking; 35% del teórico.
3. Con una cola de salida de 928k ETH y 256 ETH por época, ¿cuántos días de espera hay? → 928,024 / 57,600 = 16.1.
4. ¿Qué puede hacer ETHB si los reembolsos superan su colchón? → Buscar retrasar la liquidación con los AP, que pueden cancelar; la prima o el descuento pueden abrirse.

## 7. Estado

- **Estado:** Documentado con comprobación (fuente primaria SEC y cálculo con dos métodos).
- **Grado:** A en comisiones y estados financieros; B en los datos de la red; B-C en la explicación de la brecha; C en la tasa base; D en quién causó el salto de la cola del 2-oct.
- **Pendientes:**
  - 10-Q del 3T-2026 de ETHB (~10-13 de noviembre): repetir el punto [3];
  - flujos diarios de ETF de ETH por una vía sin 403;
  - verificar ETHA/ETHB en el SIC de GBM;
  - identificar la salida del 2-oct (beaconcha.in con clave o rated.network);
  - ETHE de Grayscale como segundo caso.
- **Pronóstico:** P0141 (cola de salida al 16-nov < 928,024 ETH, p=0.65).

## 8. Nota corta sobre P0139 (Ledger/CryptoBilis)

Se volvió a correr `2026-10-17-ledger-cadena-suministro.py` en mempool.space, el 18-oct hacia las 14:2x UTC:
- **bc1qjqgw…:** 92.5062 BTC, sin gasto (última entrada el 16-oct 18:55 UTC).
- **bc1qqnkw…:** 111.2820 BTC, sin gasto.

Saldo conjunto: **203.7882 BTC, sin cambio frente al 17-oct**, 9 días después del robo. El umbral de P0139 es < 101.89 BTC al 16-nov; sigue en p=0.40, sin ajuste.
