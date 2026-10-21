# Valuación de cierre de las cuentas reales de los rivales · miércoles 21-oct-2026

Respaldo de las cifras de los rivales en `competencia/marcador.md`.
- **Posiciones:** las que reportó el dueño (`gbm-real-2026-10-07.md` y `binance-real-2026-10-07.md`). Sin flujos nuevos.

**Insumos** (Yahoo chart v8, `regularMarketPrice`; consulta de las 21:4x UTC):

| Tipo | Activo | Precio | Hora de la cotización |
|---|---|---|---|
| Acción | NVDA | 221.97 USD | 20:00 UTC |
| Acción | GFNORTEO.MX | 206.76 MXN | 19:59 UTC |
| Acción | VISTAA.MX | 1,330.57 MXN | 16:03 UTC |
| Acción | AMKR | 43.73 USD | 20:00 UTC |
| Acción | FSLR | 174.82 USD | 20:00 UTC |
| Cripto | BTC-USD | 84,759.57 | 21:39 UTC |
| Cripto | ETH-USD | 2,498.11 | 21:39 UTC |
| Tipo de cambio | USD/MXN | 18.6692 | el de `portafolio.py valuar` en los cuatro libros de Claude |

| Cuenta | Cálculo | Valor MXN | TWR (sin flujos) |
|---|---|---:|---:|
| chatgpt-gbm | 221.97 × 18.6692 + 13 × 206.76 + 3,259.21 | 10,091.09 | +0.91% |
| grok-gbm | 3 × 1,330.57 + (3 × 43.73 + 174.82) × 18.6692 + 398.24 | 10,102.91 | +1.03% |
| chatgpt-binance | (0.00198801 × 84,759.57 + 0.030969 × 2,498.11) × 18.6692 + 502.33 | 5,092.47 | +1.85% |
| grok-binance | (0.00330974 × 84,759.57 + 0.00000843 × 2,498.11) × 18.6692 + 1.617 | 5,239.32 | +4.79% |

**Drawdown** (los picos implícitos son los del 19-oct; si un valor supera su pico, es pico nuevo):

| Cuenta | Drawdown actual |
|---|---|
| Grok GBM | −1.43% |
| ChatGPT GBM | +0.00% |
| Grok Binance | +0.00% |

El peso perdió 1.39% en el día (18.4142 → 18.6692): eso sube el valor en MXN de todo lo que está en dólares.
