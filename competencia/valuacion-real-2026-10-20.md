# Valuación de cierre de las cuentas reales de los rivales · martes 20-oct-2026

Respaldo de las cifras de los rivales en `competencia/marcador.md` (paso 5, nota c, de `rutinas/diaria-cierre.md`).
- **Posiciones:** las que reportó el dueño (`gbm-real-2026-10-07.md` y `binance-real-2026-10-07.md`). Sin flujos nuevos.

**Insumos** (Yahoo chart v8, `regularMarketPrice`; consulta de las 21:4x UTC):

| Tipo | Activo | Precio | Hora de la cotización |
|---|---|---|---|
| Acción | NVDA | 216.47 USD | 20:00 UTC |
| Acción | GFNORTEO.MX | 204.47 MXN | 19:59 UTC |
| Acción | VISTAA.MX | 1,304.34 MXN | 19:56 UTC |
| Acción | AMKR | 41.7 USD | 20:00 UTC |
| Acción | FSLR | 174.43 USD | 20:00 UTC |
| Cripto | BTC-USD | 82,756.33 | 21:41 UTC |
| Cripto | ETH-USD | 2,448.25 | 21:41 UTC |
| Tipo de cambio | USD/MXN | 18.4156 | el de `portafolio.py valuar` en los libros GBM de Claude (el libro real de Binance usó 18.4100) |

| Cuenta | Cálculo | Valor MXN | TWR (sin flujos) |
|---|---|---:|---:|
| chatgpt-gbm | 216.47 × 18.4156 + 13 × 204.47 + 3,259.21 | 9,903.74 | -0.96% |
| grok-gbm | 3 × 1,304.34 + (3 × 41.7 + 174.43) × 18.4156 + 398.24 | 9,827.28 | -1.73% |
| chatgpt-binance | (0.00198801 × 82,756.33 + 0.030969 × 2,448.25) × 18.4156 + 502.33 | 4,928.34 | -1.43% |
| grok-binance | (0.00330974 × 82,756.33 + 0.00000843 × 2,448.25) × 18.4156 + 1.617 | 5,046.07 | +0.92% |

**Drawdown** (los picos implícitos son los del 19-oct):

| Cuenta | Drawdown actual | Drawdown máximo |
|---|---|---|
| Grok GBM | −4.12% | −4.28% (19-oct) |
| ChatGPT GBM | −1.05% | −1.63% (15-oct) |
| Grok Binance | −0.40% | −1.76% (8-oct) |
| ChatGPT Binance | — | −3.11% (8-oct) |
