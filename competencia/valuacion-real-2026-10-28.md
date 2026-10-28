# Valuación de cierre de las cuentas reales de los rivales · miércoles 28-oct-2026

Respaldo de las cifras de los rivales en `competencia/marcador.md`. Posiciones registradas (`gbm-real-2026-10-07.md` y `binance-real-2026-10-07.md`), sin flujos nuevos. **Las de GBM no cuadran con la captura del dueño del 22-oct** (`conciliacion-cuenta-gbm-2026-10-22.md`): son del registro, no confirmadas.

**Insumos** (Yahoo chart v8, `regularMarketPrice`; consulta antes del commit de este cierre):

| Tipo | Activo | Precio | Hora de la cotización |
|---|---|---|---|
| Acción | NVDA | 215.38 USD | 20:00 UTC |
| Acción | GFNORTEO.MX | 213.09 MXN | 19:59 UTC |
| Acción | VISTAA.MX | 1,347.54 MXN | 18:59 UTC (último hecho; serie poco líquida) |
| Acción | AMKR | 42.21 USD | 20:00 UTC |
| Acción | FSLR | 176.30 USD | 20:00 UTC |
| Cripto | BTC-USD | **81,079.32** | el de los libros de Claude (`portafolio.py valuar`, implícito en `papel-binance/equity.csv`) |
| Cripto | ETH-USD | 2,358.05 | 21:42 UTC |
| Tipo de cambio | USD/MXN | 18.6284 | el de `portafolio.py valuar` |

| Cuenta | Cálculo | Valor MXN | TWR (sin flujos) |
|---|---|---:|---:|
| chatgpt-gbm | 215.38 × 18.6284 + 13 × 213.09 + 3,259.21 | 10,041.56 | +0.42% (del registro) |
| grok-gbm | 3 × 1,347.54 + (3 × 42.21 + 176.30) × 18.6284 + 398.24 | 10,083.96 | +0.84% (del registro) |
| chatgpt-binance | (0.00198801 × 81,079.32 + 0.030969 × 2,358.05) × 18.6284 + 502.33 | 4,865.34 | −2.69% |
| grok-binance | (0.00330974 × 81,079.32 + 0.00000843 × 2,358.05) × 18.6284 + 1.617 | 5,000.95 | +0.02% |

**Drawdown** (contra el máximo de los cierres de `valuacion-real-*.md`):
- **Binance:** ChatGPT −4.46% y Grok −4.55% (pico del 21-oct).
- **GBM:** ChatGPT −0.59% (pico del 27-oct) y Grok −1.62% (pico del 13-oct), los dos del registro.
