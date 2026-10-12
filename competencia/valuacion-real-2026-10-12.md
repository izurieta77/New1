# Valuación de cierre de las cuentas reales de los rivales · lunes 12-oct-2026

Respaldo de las cifras de los rivales que el cierre del 12-oct escribe en `competencia/marcador.md` (paso 5, nota c, de `rutinas/diaria-cierre.md`). Es una **valuación del sistema**, no un reporte del dueño. Las posiciones son las mismas que reportó el dueño (`gbm-real-2026-10-07.md` y `binance-real-2026-10-07.md`); sin flujos nuevos reportados.

**Insumos (consultados el 12-oct ~21:45 UTC, Yahoo chart v8, último dato del día):** NVDA 226.32 USD; GFNORTEO.MX 192.90 MXN; VISTAA.MX 1,268.00 MXN; AMKR 48.11 USD; FSLR 179.72 USD; USD/MXN 18.2215 (MXN=X, el mismo que usó `portafolio.py valuar`); BTC-USD 82,804.84; ETH-USD 2,507.34. Cuentas de Claude: SPYM 91.58, QQQM 307.19, UPRO 155.46 USD.

| Cuenta | Cálculo | Valor MXN | TWR (sin flujos) |
|---|---|---:|---:|
| chatgpt-gbm | 226.32 × 18.2215 + 13 × 192.90 + 3,259.21 | 9,890.80 | −1.09% |
| grok-gbm | 3 × 1,268.00 + (3 × 48.11 + 179.72) × 18.2215 + 398.24 | 10,106.92 | +1.07% |
| chatgpt-binance | (0.00198801 × 82,804.84 + 0.030969 × 2,507.34) × 18.2215 + 502.33 | 4,916.79 | −1.66% |
| grok-binance | (0.00330974 × 82,804.84 + 0.00000843 × 2,507.34) × 18.2215 + 1.617 | 4,995.83 | −0.08% |

**Drawdown máximo (pico contra valle, base 100 = aportación):** ChatGPT GBM **−1.09%** (nuevo mínimo, 12-oct); Grok GBM −0.86% (sin cambio; hoy a −0.05% de su pico de 10,112.43); ChatGPT Binance −3.11% (8-oct); Grok Binance −1.76% (8-oct).

**Límite:** BTC-USD y ETH-USD de Yahoo son el último dato de la vela diaria en curso a la hora de la consulta, no un cierre de las 00:00 UTC. Las cuentas cripto de Claude se valuaron con el mismo dato (BTC implícito en `bitacora/papel-binance/equity.csv`: 4,070.89 / 0.002698 / 18.2215 = 82,808).
