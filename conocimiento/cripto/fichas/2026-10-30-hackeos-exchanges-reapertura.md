# Ficha de avance · 30-oct-2026 · Hackeos de exchanges: cuánto tarda en reabrir el retiro, cuánto se va el cliente al reabrir y cuánto recupera

> **Por qué este tema.** La adenda del 29-oct del cap. 04 (Moore-Christin) dejó abierta una pregunta: **cuánto duran las pausas de retiro**. Es justo lo que mide el disparador "retiros en MXN o BTC suspendidos más de 24 h" de `config/parametros.json` → `cripto_binance.contingencia_contraparte`, y lo que decide O0007 a las 00:00 UTC del 31-oct. En la cola del plan (`00-plan-de-estudio.md`), los recursos 17 (*Number Go Up*: FTX) y 32/08 (Chainalysis y ZachXBT: hackeos) ya están estudiados. Las dos siguientes piezas de la cola académica (la prima electoral con los diarios del 3-4-nov y la ventana *c* del IVD, hacia el 2-dic) todavía no tienen datos. Hoy manda el evento de cola de nuestra contraparte.

## 0. Preguntas de hoy

1. Cuando un exchange solvente pausa retiros tras un hackeo, ¿cuántos días tarda en reabrir? ¿Tiene precedente la guía de "48 h" de Yi He?
2. Al reabrir, ¿qué parte de las reservas se lleva el cliente, medida con el método F (flujo neto en unidades)?
3. ¿Cuánto recupera el cliente, y cuándo, si el exchange es solvente y si no lo es?
4. ¿Dónde cae Binance (US$6.3 mil M, 29-oct-2026) en esas distribuciones?

## 1. Acceso y fuentes (declarado)

| Caso | Fuente | Grado | Acceso real |
|---|---|---|---|
| Binance 2026 | Comunicado "Security Incident Update (2026-10-30)", CMS de Binance ([API](https://www.binance.com/bapi/composite/v1/public/cms/article/detail/query?articleCode=c5a8729a97ac486d963784d96c5642d7)), publicado a las 02:23 UTC y actualizado (depósitos) | **A** | Íntegro, leído a las 14:24 UTC |
| Binance 2026 | Endpoint [getNetworkCoinAll](https://www.binance.com/bapi/capital/v1/public/capital/getNetworkCoinAll), 14:22 UTC | **A** | Íntegro: 0/990 retiros, 706 depósitos |
| Bybit, Bitget y Binance | DefiLlama `api.llama.fi/protocol/{bybit,bitget,binance-cex}` (carteras atribuidas) | **C** (atribución de DefiLlama), **A** como dato | Íntegro; foto en `2026-10-30-hackeos-exchanges-datos.json` |
| Bitget 2026 | [BleepingComputer](https://www.bleepingcomputer.com/news/security/bitget-resumes-bitcoin-withdrawals-after-3875-million-crypto-heist/) y [crypto.news](https://crypto.news/bitget-resumes-btc-withdrawals-after-usd-388m-hack/): BTC reabre el 28-sep a las 08:00 UTC; ETH el 29, USDT el 30 y fiat/P2P el 2-oct. Bloomberg ([BGOV](https://news.bgov.com/crypto/crypto-hack-spurs-463-million-in-customer-outflows-at-bitget)): US$463 M de salidas en 24 h | **B** | Titulares y resúmenes |
| Bybit 2025 | [The Block](https://www.theblock.co/post/342667/crypto-exchange-bybit-hacked-as-over-1-billion-worth-of-eth-leaves-wallets), [Khaleej Times](https://www.khaleejtimes.com/uae/dubai-bybit-operations-back-to-normal-within-24-hours-after-15-billion-crypto-hack): sin pausa; brecha de ETH cerrada el 24-feb | **B** | Resúmenes |
| Bitfinex 2016 | [CoinDesk, 10-ago-2016](https://coindesk-coindesk-prod.cdn.arcpublishing.com/markets/2016/08/10/bitfinex-exchange-to-resume-bitcoin-trading-today/) (reabre el 10-ago a las 16:00 UTC) y [Cointelegraph](https://cointelegraph.com/news/bitfinex-2016-bitcoin-hack-restitution-us-government) (recorte de 36%; BFX redimido al 100% en ~8 meses) | **B** | Resúmenes |
| Coincheck 2018 | [Finance Magnates](https://www.financemagnates.com/cryptocurrency/news/coincheck-resumes-yen-withdrawals-lawsuit-way/) (yenes el 13-feb), [ITmedia, 12-mar-2018](https://www.itmedia.co.jp/news/article/1803/12/1180312102/) (BTC y compensación de NEM a ¥88.549) | **B** | Resúmenes |
| Binance 2019 | [The Block](https://www.theblock.co/post/23501/binance-reopens-withdrawals-and-deposits-a-week-after-41-million-hack-bitcoin) (reabre el 15-may) | **B** | Titular y resumen |
| KuCoin 2020 | [Carta del CEO de KuCoin](https://www.kucoin.com/news/en-a-letter-from-kucoin-ceo-2020-2021-and-beyond) ("en una semana", reapertura gradual) e [Invezz, 7-oct-2020](https://invezz.com/news/2020/10/07/kucoin-resumes-withdrawals-and-deposits-for-btc-eth-and-usdt/) | **C** (fecha exacta sin cerrar: 4-11 días; uso 7) | Resúmenes |
| CoinEx y Poloniex 2023 | [Cointelegraph](https://cointelegraph.com/news/coinex-to-resume-services-after-70-million-hack) (CoinEx, 21-sep) y [Cointelegraph](https://cointelegraph.com/news/poloniex-resumes-withdrawals-hack) (Poloniex, gradual desde el 29/30-nov) | **B/C** | Resúmenes |
| DMM Bitcoin 2024 | [Cointelegraph](https://cointelegraph.com/news/dmm-transfer-deal-sbi-accounts-open-march): traspaso a SBI VC Trade el 8-mar-2025; BTC repuesto por el grupo DMM | **B** | Resumen |
| WazirX 2024 | [Decrypt](https://decrypt.co/345632/wazirx-to-resume-trading-and-withdrawals-more-than-a-year-after-234m-hack): reabre el 24-oct-2025 con el plan de Singapur | **B** fechas; **C** recuperación (55-85%, sin conciliar) | Resumen |
| Mt.Gox 2014 | [Axios](https://www.axios.com/2024/06/24/bitcoin-cryptocurrency-exchange-repayments-mt-gov) y [Decrypt](https://decrypt.co/346053/mt-gox-pushes-back-bitcoin-repayments-by-another-year?amp=1): pagos desde el 5-jul-2024 (142,000 BTC repartibles), plazo al 31-oct-2026 | **B** fechas; **C** recuperación (~20% en BTC, cifra de prensa sin fuente primaria) | Resúmenes |
| FTX 2022 (control: fraude, no hackeo) | Plan del capítulo 11 (cap. 04) | **B** | Ya en el cap. 04 |

**No se leyó** ninguna fuente primaria de los exchanges históricos salvo la carta de KuCoin y el comunicado de Binance de hoy. Las fechas de la tabla son de prensa B que coincide. El tamaño de la muestra (n = 11) es chico y tiene sesgo de supervivencia: los casos con cobertura en inglés son los grandes.

## 2. Ejercicio numérico (comprobado en Python)

Código: [`2026-10-30-hackeos-exchanges-reapertura.py`](2026-10-30-hackeos-exchanges-reapertura.py) (solo biblioteca estándar). Se reproduce con `python3 -I conocimiento/cripto/fichas/2026-10-30-hackeos-exchanges-reapertura.py`; con `--crudo <dir>` se rehace la foto desde los JSON de DefiLlama. **Método F** igual a la réplica `bitacora/arbitraje/2026-10-25-e1-metodo-f.py`: unidades por precio del día, solo filas de 00:00 UTC y sin token propio (BNB; MNT/BIT; BGB/BWB). La foto descarta tokens de menos de US$0.1 M por día, así que el E1 de Binance da −4.40% en vez de −4.41%.

### A. Tiempo hasta la primera reapertura (días naturales)

| | n | Días | Mediana | ≤ 2 d | ≤ 7.5 d | ≤ 14 d |
|---|---|---|---|---|---|---|
| Solventes que **pausaron** (Bitget 4, KuCoin ~7, Bitfinex 8, Binance 2019 8, CoinEx 9, Coincheck 18, Poloniex ~20) | 7 | 4-20 | **8** | **0/7** | 2/7 | 5/7 |
| Todos los que pausaron, incluidos DMM (281), WazirX (463) y Mt.Gox (nunca) | 10 | — | 13.5 | 0/10 | 2/10 | 5/10 |
| Bybit 2025: **no pausó** | 1 | 0 | — | — | — | — |

- **Ningún exchange que pausó reabrió en 48 horas.** El más rápido fue Bitget, con 4 días y solo para BTC; el resto (fiat y P2P) tardó 8 días.
- **La reapertura es por fases:** primero BTC (Bitget) o fiat (Coincheck: yenes a los 18 días y BTC a los 45).

### B. Cuánto se va el cliente (método F, DefiLlama)

| Exchange | Pérdida / reservas sin token propio | Salida de clientes, sin contar el robo | Ventana |
|---|---|---|---|
| **Bybit** (sin pausa) | 1.46 / 16.20 mil M = **9.0%** | **−4.37 mil M = −27.0%** | 22 y 23-feb-2025 (2 días) |
| **Bitget** (reabre BTC el 28-sep) | 0.388 / 6.16 mil M = **6.3%** | **−0.60 mil M = −10.2%** | 29-sep a 1-oct (3 días tras reabrir) |
| Bitget, **durante la pausa** | — | +0.02 mil M (sin corrida posible) | 26 a 28-sep |
| **Binance** (pausa desde ≈00:00 UTC del 30-oct) | 6.3 / 144.90 mil M = **4.3%** | **+0.36 mil M** (fila del 30-oct, −5.94 mil M menos el robo de 6.3, C) | 29→30-oct |

- **Reposición:** Bybit +1.08 mil M el 25-feb y Bitget +0.59 mil M el 2-oct. En una ventana de 7 días, la reposición tapa la corrida: el E1 a 7 días de Bitget pasó de −15.6% (1-oct) a **−0.9%** (2-oct).
- **Firma del robo en Binance (29→30-oct):** USDT −2.55 mil M, BTC −16.0 mil unidades (−1.23 mil M), USDC −0.77 mil M y WETH −179 mil unidades (−0.40 mil M). La salida de ETH en la clave "WETH" (−179 mil) es del orden de los 197,460 ETH que el vigía verificó en la dirección del atacante. **[I]** La salida de **BTC** (−16 mil) no estaba en el relato del robo, que era de ETH y tokens. Puede ser parte de los "additional points of breach" (Business Insider, B) o un movimiento propio. Sin verificar.

### C. Recuperación del cliente

- **Solventes (8 de 8): 100% nominal**, con matices. Bitfinex recortó 36% y pagó con BFX, que redimió en ~8 meses. Coincheck pagó NEM en yenes a ¥88.549 en ~45 días.
- **Insolventes o liquidados (3): 0.68 en promedio**, y se cobra tarde: DMM, 100% en 9 meses vía el traspaso a SBI; WazirX, ~85% (C) en 15 meses; Mt.Gox, ~20% en BTC (C) en ~125 meses.
- **FTX (control de fraude):** 119% en USD a precio de la petición, en ~30 meses. Medido en BTC es mucho menos.

## 3. Lectura para nuestra cuenta [I]

1. **O0007 / disparador de 24 h.** La tasa base de seguir pausado más de 24 horas, dado que hubo pausa, es **7/7**. La guía de 48 h de Yi He (B−) no tiene precedente en la muestra. El disparador formal empieza a contar con la evidencia fechada de BTC y MXN suspendidos (≈00:00 UTC del 30-oct, B; 02:10 UTC, A) y **se cumpliría a las 00:00-02:10 UTC del 31-oct**. A las 14:22 UTC llevaba 12-14 h. No se cumple todavía.
2. **Lo que pasa al reabrir.** Bybit y Bitget, con pérdidas relativas **más grandes** (9.0% y 6.3% contra 4.3%), pagaron todo y siguieron operando. El tamaño relativo de Binance es protector, como en Moore-Christin. **El riesgo propio de la reapertura es la cola de retiros:** Bitget perdió −10% en 3 días y Bybit −27% en 2. Para un saldo pequeño como el nuestro (0.001325 BTC y ≈3,002 MXN), eso significa salir **en la primera hora de reapertura del riel** (Lightning o SPEI), antes de que se forme la cola o se limite por montos.
3. **P0204** (BTC reabierto el 6-nov, p = 0.75, de Claude): la tasa base de ≤ 7.5 días entre solventes que pausaron es **2/7**; con ≤ 8 días, 4/7. La p de 0.75 descansa en la guía de 48 h y en el tamaño de Binance. Lo dejo anotado para la conciliación; **no la toco**.
4. **E1 hoy (−4.41%) es ÁMBAR, pero casi todo es el robo, no corrida:** sin los 6.3 mil M, el día da +0.36 mil M. Con los retiros cerrados no puede haber corrida. La prueba real de E1 es la primera semana después de reabrir. De ahí sale **P0207**.

## 4. Límites

- n = 11 casos, con fechas de prensa B o C. El caso de KuCoin tiene una fecha que va de 4 a 11 días y el de Poloniex es aproximado. Hay sesgo hacia los exchanges grandes y de habla inglesa.
- **DefiLlama solo ve las carteras que atribuye** (C). Los movimientos internos y la reposición desde carteras no rastreadas se ven como flujo. La fila del día llega con retraso.
- "Sin el robo" resta la estimación de prensa y del comunicado (6.3 mil M). El robo no se mide token por token contra la dirección del atacante.
- Las cifras de recuperación de WazirX y de Mt.Gox son C. No hay un caso comparable en tamaño absoluto (US$6.3 mil M es ~4 veces Bybit).
- No se estudió el caso de los retiros "pausados" por insolvencia sin hackeo (Celsius, Voyager); su base es otra.

## 5. Estado

**Documentado con comprobación.** Siguientes pasos:
- (a) medir en E1 la semana de reapertura de Binance (P0207);
- (b) verificar con fuente primaria la fecha de KuCoin y la recuperación de WazirX y de Mt.Gox;
- (c) agregar Zaif 2018 y Upbit 2019 para llevar n a 13.
