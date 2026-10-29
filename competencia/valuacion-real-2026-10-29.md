# Valuación de cierre de las cuentas reales de los rivales · jueves 29-oct-2026

Respaldo de las cifras de los rivales en `competencia/marcador.md`. Posiciones registradas (`gbm-real-2026-10-07.md` y `binance-real-2026-10-07.md`), sin flujos nuevos. **Las de GBM no cuadran con la captura del dueño del 22-oct**: son del registro, no confirmadas.

**Insumos** (Yahoo chart v8, `regularMarketPrice`; consulta antes del commit de este cierre):

| Tipo | Activo | Precio | Hora de la cotización |
|---|---|---|---|
| Acción | NVDA | 213.66 USD | 20:00 UTC |
| Acción | GFNORTEO.MX | 210.99 MXN | 19:59 UTC |
| Acción | VISTAA.MX | 1,340.75 MXN | 19:35 UTC (último hecho) |
| Acción | AMKR | 41.21 USD | 20:00 UTC |
| Acción | FSLR | 176.89 USD | 20:00 UTC |
| Cripto | BTC-USD | **79,409.75** | el de los libros de Claude (implícito en `papel-binance/equity.csv`) |
| Cripto | ETH-USD | 2,283.95 | 21:40 UTC |
| Tipo de cambio | USD/MXN | 18.8405 | el de `portafolio.py valuar` |

| Cuenta | Cálculo | Valor MXN | TWR (sin flujos) |
|---|---|---:|---:|
| chatgpt-gbm | 213.66 × 18.8405 + 13 × 210.99 + 3,259.21 | 10,027.54 | +0.28% (del registro) |
| grok-gbm | 3 × 1,340.75 + (3 × 41.21 + 176.89) × 18.8405 + 398.24 | 10,082.44 | +0.82% (del registro) |
| chatgpt-binance | (0.00198801 × 79,409.75 + 0.030969 × 2,283.95) × 18.8405 + 502.33 | 4,809.25 | −3.82% |
| grok-binance | (0.00330974 × 79,409.75 + 0.00000843 × 2,283.95) × 18.8405 + 1.617 | 4,953.75 | −0.93% |

**Drawdown:**
- **Binance:** ChatGPT −5.56% y Grok −5.45% (pico del 21-oct).
- **GBM:** ChatGPT −0.73% y Grok −1.64%, los dos del registro.
