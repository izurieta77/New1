# Valuación de cierre de las cuentas reales de los rivales · martes 13-oct-2026

Respaldo de las cifras de los rivales del cierre del 13-oct en `competencia/marcador.md` (paso 5, nota c, de `rutinas/diaria-cierre.md`). Valuación del sistema con las posiciones reportadas por el dueño (`gbm-real-2026-10-07.md` y `binance-real-2026-10-07.md`); sin flujos nuevos.

**Insumos (Yahoo chart v8, cierres del 13-oct consultados ~21:45 UTC):** NVDA 228.52 USD; GFNORTEO.MX 196.56 MXN; VISTAA.MX 1,268.52 MXN; AMKR 47.61 USD; FSLR 186.60 USD; USD/MXN 18.3547 (el mismo de `portafolio.py valuar` del libro real GBM; 18.3530 para los libros cripto); BTC-USD 83,365.92; ETH-USD 2,509.71 (vela diaria en curso).

| Cuenta | Cálculo | Valor MXN | TWR (sin flujos) |
|---|---|---:|---:|
| chatgpt-gbm | 228.52 × 18.3547 + 13 × 196.56 + 3,259.21 | 10,008.91 | +0.09% |
| grok-gbm | 3 × 1,268.52 + (3 × 47.61 + 186.60) × 18.3547 + 398.24 | 10,250.39 | +2.50% |
| chatgpt-binance | (0.00198801 × 83,365.92 + 0.030969 × 2,509.71) × 18.3530 + 502.33 | 4,970.47 | −0.59% |
| grok-binance | (0.00330974 × 83,365.92 + 0.00000843 × 2,509.71) × 18.3530 + 1.617 | 5,065.96 | +1.32% |

**Drawdown máximo:** ChatGPT GBM −1.09% (12-oct); Grok GBM −0.86% (sin cambio; nuevo pico hoy); ChatGPT Binance −3.11% (8-oct); Grok Binance −1.76% (8-oct; nuevo pico hoy).

**Nota:** Yahoo revisó el cierre del USD/MXN del 12-oct a 18.4186 (la valuación de ayer usó 18.2215, último dato a las ~21:40 UTC). No se re-valúa el 12-oct; la fila de ese día queda como se registró.
