# Valuación de cierre de las cuentas reales de los rivales · lunes 19-oct-2026

Respaldo de las cifras de los rivales en `competencia/marcador.md` (paso 5, nota c, de `rutinas/diaria-cierre.md`).
- **Posiciones:** las que reportó el dueño (`gbm-real-2026-10-07.md` y `binance-real-2026-10-07.md`). No hubo flujos nuevos.

**Insumos** (Yahoo chart v8, `regularMarketPrice`; consulta de las 21:4x UTC):

| Tipo | Activo | Precio | Hora de la cotización |
|---|---|---|---|
| Acción | NVDA | 217.09 USD | 20:00 UTC |
| Acción | GFNORTEO.MX | 204.85 MXN | 19:59 UTC |
| Acción | VISTAA.MX | 1,312.32 MXN | 19:56 UTC |
| Acción | AMKR | 41.89 USD | 20:00 UTC |
| Acción | FSLR | 171.80 USD | 20:00 UTC |
| Cripto | BTC-USD | 81,947.19 | 21:39 UTC |
| Cripto | ETH-USD | 2,400.35 | 21:39 UTC |
| Tipo de cambio | USD/MXN | 18.4097 | el mismo que usó `portafolio.py valuar` en los cuatro libros de Claude |

| Cuenta | Cálculo | Valor MXN | TWR (sin flujos) |
|---|---|---:|---:|
| chatgpt-gbm | 217.09 × 18.4097 + 13 × 204.85 + 3,259.21 | 9,918.82 | −0.81% |
| grok-gbm | 3 × 1,312.32 + (3 × 41.89 + 171.80) × 18.4097 + 398.24 | 9,811.53 | −1.88% |
| chatgpt-binance | (0.00198801 × 81,947.19 + 0.030969 × 2,400.35) × 18.4097 + 502.33 | 4,870.00 | −2.60% |
| grok-binance | (0.00330974 × 81,947.19 + 0.00000843 × 2,400.35) × 18.4097 + 1.617 | 4,995.14 | −0.10% |

**Drawdown desde el pico.** El pico se reconstruye con el drawdown del 16-oct: pico = valor del 16-oct / (1 + drawdown del 16-oct).

| Cuenta | Pico implícito | Drawdown actual | Drawdown máximo |
|---|---|---|---|
| Grok GBM | ≈10,249.9 | **−4.28%** | −4.28% (nuevo máximo) |
| ChatGPT GBM | ≈10,008.5 | −0.90% | −1.63% (15-oct) |
| Grok Binance | ≈5,066.1 | −1.40% | −1.76% (8-oct) |
| ChatGPT Binance | — | — | −3.11% (8-oct) |
