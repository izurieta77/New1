# Valuación de cierre de las cuentas reales de los rivales · viernes 16-oct-2026

Respaldo de las cifras de los rivales en `competencia/marcador.md` (paso 5, nota c, de `rutinas/diaria-cierre.md`). La valuación usa las posiciones que reportó el dueño (`gbm-real-2026-10-07.md` y `binance-real-2026-10-07.md`). No hubo flujos nuevos.

**Insumos** (Yahoo chart v8, `regularMarketPrice` consultado a las 21:39 UTC):
- **Acciones:** NVDA 214.13 USD; GFNORTEO.MX 205.02 MXN; VISTAA.MX 1,337.00 MXN; AMKR 41.82 USD; FSLR 172.64 USD.
- **Cripto:** BTC-USD 81,615.84; ETH-USD 2,415.02.
- **Tipo de cambio:** USD/MXN 18.4790, el mismo que usó `portafolio.py valuar` en los cuatro libros de Claude.

| Cuenta | Cálculo | Valor MXN | TWR (sin flujos) |
|---|---|---:|---:|
| chatgpt-gbm | 214.13 × 18.4790 + 13 × 205.02 + 3,259.21 | 9,881.38 | −1.19% |
| grok-gbm | 3 × 1,337.00 + (3 × 41.82 + 172.64) × 18.4790 + 398.24 | 9,917.83 | −0.82% |
| chatgpt-binance | (0.00198801 × 81,615.84 + 0.030969 × 2,415.02) × 18.4790 + 502.33 | 4,882.66 | −2.35% |
| grok-binance | (0.00330974 × 81,615.84 + 0.00000843 × 2,415.02) × 18.4790 + 1.617 | 4,993.67 | −0.13% |

**Drawdown desde el pico:**

| Cuenta | Drawdown actual | Drawdown máximo |
|---|---|---|
| Grok GBM | −3.24% desde el pico del 13-oct | −3.24% (nuevo) |
| ChatGPT GBM | −1.27% | −1.63% (15-oct) |
| Grok Binance | −1.43% | −1.76% (8-oct) |
| ChatGPT Binance | — | −3.11% (8-oct) |
