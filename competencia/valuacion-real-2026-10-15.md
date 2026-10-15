# Valuación de cierre de las cuentas reales de los rivales · jueves 15-oct-2026

Respaldo de las cifras de los rivales en `competencia/marcador.md` (paso 5, nota c, de `rutinas/diaria-cierre.md`). Es una valuación del sistema con las posiciones que reportó el dueño (`gbm-real-2026-10-07.md` y `binance-real-2026-10-07.md`); no hubo flujos nuevos.

**Insumos** (Yahoo chart v8, `regularMarketPrice` a las 21:38 UTC):
- **Acciones:** NVDA 217.23 USD; GFNORTEO.MX 199.25 MXN; VISTAA.MX 1,293.54 MXN; AMKR 44.05 USD; FSLR 178.81 USD.
- **Cripto:** BTC-USD 82,208.49; ETH-USD 2,458.20.
- **USD/MXN:** 18.3957 para GBM y 18.3880 para cripto, los mismos que usó `portafolio.py valuar` en los libros de Claude.

| Cuenta | Cálculo | Valor MXN | TWR (sin flujos) |
|---|---|---:|---:|
| chatgpt-gbm | 217.23 × 18.3957 + 13 × 199.25 + 3,259.21 | 9,845.56 | −1.54% |
| grok-gbm | 3 × 1,293.54 + (3 × 44.05 + 178.81) × 18.3957 + 398.24 | 9,999.19 | −0.01% |
| chatgpt-binance | (0.00198801 × 82,208.49 + 0.030969 × 2,458.20) × 18.3880 + 502.33 | 4,907.35 | −1.85% |
| grok-binance | (0.00330974 × 82,208.49 + 0.00000843 × 2,458.20) × 18.3880 + 1.617 | 5,005.17 | +0.10% |

**Drawdown desde el pico:**

| Cuenta | Hoy | Máximo |
|---|---|---|
| Grok GBM | −2.45% desde el pico del 13-oct | −2.45% (nuevo) |
| ChatGPT GBM | −1.63% desde el 13-oct | −1.63% (nuevo) |
| Grok Binance | −1.20% | −1.76% (8-oct) |
| ChatGPT Binance | | −3.11% (8-oct) |
