# Valuación de cierre de las cuentas reales de los rivales · viernes 23-oct-2026

Respaldo de las cifras de los rivales en `competencia/marcador.md`.
- **Posiciones:** las registradas (`gbm-real-2026-10-07.md` y `binance-real-2026-10-07.md`), sin flujos nuevos.
- **Las de GBM siguen sin cuadrar con la captura del dueño del 22-oct** (`competencia/conciliacion-cuenta-gbm-2026-10-22.md`): falta AMKR, y NFLX, UBER y LULU no tienen registro. Las cifras de chatgpt-gbm y grok-gbm son **del registro, no confirmadas**.

**Insumos** (Yahoo chart v8, `regularMarketPrice`; consulta de las 21:4x UTC):

| Tipo | Activo | Precio | Hora de la cotización |
|---|---|---|---|
| Acción | NVDA | 210.96 USD | 20:00 UTC |
| Acción | GFNORTEO.MX | 213.46 MXN | 19:59 UTC |
| Acción | VISTAA.MX | 1,398.55 MXN | 19:58 UTC |
| Acción | AMKR | 39.30 USD | 20:00 UTC |
| Acción | FSLR | 171.99 USD | 20:00 UTC |
| Cripto | BTC-USD | **81,294.23** | el mismo precio de los libros de Claude (`portafolio.py valuar`, ~21:40 UTC) |
| Cripto | ETH-USD | 2,397.54 | 21:40 UTC |
| Tipo de cambio | USD/MXN | 18.6480 | el de `portafolio.py valuar` |

| Cuenta | Cálculo | Valor MXN | TWR (sin flujos) |
|---|---|---:|---:|
| chatgpt-gbm | 210.96 × 18.6480 + 13 × 213.46 + 3,259.21 | 9,968.17 | −0.32% (del registro) |
| grok-gbm | 3 × 1,398.55 + (3 × 39.30 + 171.99) × 18.6480 + 398.24 | 9,999.76 | −0.00% (del registro; AMKR no aparece en la captura) |
| chatgpt-binance | (0.00198801 × 81,294.23 + 0.030969 × 2,397.54) × 18.6480 + 502.33 | 4,900.71 | −1.99% |
| grok-binance | (0.00330974 × 81,294.23 + 0.00000843 × 2,397.54) × 18.6480 + 1.617 | 5,019.48 | +0.39% |

**Drawdown:**

| Cuenta | Drawdown | Contra qué |
|---|---|---|
| Grok GBM | −2.44% | pico implícito de 10,249; del registro |
| ChatGPT GBM | −1.22% | 21-oct; del registro |
| Grok Binance | −4.20% | 21-oct: **máximo nuevo** |
| ChatGPT Binance | −3.77% | valor del 21-oct |
