# Valuación de cierre de las cuentas reales de los rivales · miércoles 14-oct-2026

Respaldo de las cifras de los rivales del cierre del 14-oct en `competencia/marcador.md` (paso 5, nota c, de `rutinas/diaria-cierre.md`). Es la valuación del sistema con las posiciones reportadas por el dueño (`gbm-real-2026-10-07.md` y `binance-real-2026-10-07.md`); no hubo flujos nuevos.

**Insumos:** Yahoo chart v8, `regularMarketPrice` consultado a las 21:39 UTC.

| Instrumento | Precio |
|---|---:|
| NVDA | 221.30 USD (cierre 20:00 UTC) |
| GFNORTEO.MX | 196.66 MXN |
| VISTAA.MX | 1,295.00 MXN |
| AMKR | 44.82 USD |
| FSLR | 179.08 USD |
| BTC-USD | 81,813.94 |
| ETH-USD | 2,424.54 |
| USD/MXN | 18.4710 (el mismo de `portafolio.py valuar` en los cuatro libros de Claude) |

| Cuenta | Cálculo | Valor MXN | TWR (sin flujos) |
|---|---|---:|---:|
| chatgpt-gbm | 221.30 × 18.4710 + 13 × 196.66 + 3,259.21 | 9,903.42 | −0.97% |
| grok-gbm | 3 × 1,295.00 + (3 × 44.82 + 179.08) × 18.4710 + 398.24 | 10,074.64 | +0.75% |
| chatgpt-binance | (0.00198801 × 81,813.94 + 0.030969 × 2,424.54) × 18.4710 + 502.33 | 4,893.49 | −2.13% |
| grok-binance | (0.00330974 × 81,813.94 + 0.00000843 × 2,424.54) × 18.4710 + 1.617 | 5,003.62 | +0.07% |

**Drawdown desde el pico:**

| Cuenta | Hoy | Máximo |
|---|---|---|
| Grok GBM | −1.71% desde el pico del 13-oct (10,250.39) | −1.71% (14-oct, nuevo) |
| Grok Binance | −1.23% desde el pico del 13-oct | −1.76% (8-oct) |
| ChatGPT GBM | −1.05% desde el 13-oct | −1.09% (12-oct) |
| ChatGPT Binance | | −3.11% (8-oct) |

**Nota:** los libros cripto de Claude implican BTC ≈ 81,831 (consulta de `portafolio.py` segundos antes). La diferencia contra 81,813.94 es de 0.02%, menos de 1.1 MXN por cuenta.
