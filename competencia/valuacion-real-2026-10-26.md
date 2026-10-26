# Valuación de cierre de las cuentas reales de los rivales · lunes 26-oct-2026

Respaldo de las cifras de los rivales en `competencia/marcador.md`.
- **Posiciones:** las registradas (`gbm-real-2026-10-07.md` y `binance-real-2026-10-07.md`), sin flujos nuevos.
- **Las de GBM no cuadran con la captura del dueño del 22-oct** (`competencia/conciliacion-cuenta-gbm-2026-10-22.md`): son **del registro, no confirmadas**.

**Insumos** (Yahoo chart v8, `regularMarketPrice`; consulta de las 21:4x UTC):

| Tipo | Activo | Precio | Hora de la cotización |
|---|---|---|---|
| Acción | NVDA | 216.00 USD | 20:00 UTC |
| Acción | GFNORTEO.MX | 214.07 MXN | 19:59 UTC |
| Acción | VISTAA.MX | 1,350.00 MXN | 19:59 UTC |
| Acción | AMKR | 36.81 USD | 20:00 UTC |
| Acción | FSLR | 168.15 USD | 20:00 UTC |
| Cripto | BTC-USD | **79,992.31** | el mismo de los libros de Claude (`portafolio.py valuar`) |
| Cripto | ETH-USD | 2,310.65 | 21:43 UTC |
| Tipo de cambio | USD/MXN | 18.5603 | el de `portafolio.py valuar` |

| Cuenta | Cálculo | Valor MXN | TWR (sin flujos) |
|---|---|---:|---:|
| chatgpt-gbm | 216.00 × 18.5603 + 13 × 214.07 + 3,259.21 | 10,051.14 | +0.51% (del registro) |
| grok-gbm | 3 × 1,350.00 + (3 × 36.81 + 168.15) × 18.5603 + 398.24 | 9,618.77 | −3.81% (del registro) |
| chatgpt-binance | (0.00198801 × 79,992.31 + 0.030969 × 2,310.65) × 18.5603 + 502.33 | 4,782.04 | −4.36% |
| grok-binance | (0.00330974 × 79,992.31 + 0.00000843 × 2,310.65) × 18.5603 + 1.617 | 4,915.89 | −1.68% |

**Drawdown:** Grok Binance −6.17% contra el pico del 21-oct (máximo nuevo); ChatGPT Binance −6.10% contra el 21-oct. En GBM: Grok −6.15% y ChatGPT −0.40%, los dos del registro.
