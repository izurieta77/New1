# Valuación de cierre de las cuentas reales de los rivales · viernes 9-oct-2026

Respaldo de las cifras de los rivales que el cierre del 9-oct escribió en `competencia/marcador.md` (paso 5, nota c, de `rutinas/diaria-cierre.md`). Es una **valuación del sistema**, no un reporte del dueño, y por eso no va en `competencia/rivales.csv` (REGLAS §5). Las posiciones son las que reportó el dueño y no cambiaron desde el 7-oct. La corrida de cierre (~21:39 UTC) solo dejó "Yahoo 2d, USD/MXN 18.36" en el brief (L33); los insumos los reconstruyó la conciliación del 10-oct (fallo `bitacora/arbitraje/2026-10-10-marcador-tercera-noche.md`) con datos públicos que se pueden volver a consultar.

**Insumos (consultados el 10-oct ~03:00 UTC):**
- **Cierres Yahoo chart v8 (1d) del 9-oct:** NVDA 229.28 USD; GFNORTEO.MX 189.95 MXN; VISTAA.MX 1,219.00 MXN; AMKR 49.12 USD; FSLR 177.82 USD. Cuentas de Claude: SPYM 91.64, QQQM 309.39, UPRO 155.72 USD.
- **USD/MXN:** 18.36, cierre 1d de Yahoo MXN=X del 9-oct (último dato, vela de las 21:00-21:04 UTC; es el mismo spot que imprimió `fx_alerta.py`). La vela de 15m de las 20:45 UTC cerró en 18.393: con ese tipo de cambio las cuentas en USD subirían ~0.18% en su parte en dólares.
- **Cripto:** Yahoo 15m, vela de las 21:45 UTC: BTC 82,465.54 USD y ETH 2,482.88 USD. El BTC implícito de los dos libros de Claude (4,084.97 / 0.002698 y 2,006.15 / 0.001325, ÷ 18.36) es 82,466.

| Cuenta | Posiciones (fuente) | Cálculo | Reproducido | Registrado por el cierre | Diferencia |
|---|---|---|---|---|---|
| chatgpt-gbm | 1 NVDA + 13 GFNORTE O + 3,259.21 MXN (`gbm-real-2026-10-07.md`) | 229.28 × 18.36 + 13 × 189.95 + 3,259.21 | 9,938.14 | 9,938.14 | 0.000% |
| grok-gbm | 3 VISTA A + 3 AMKR + 1 FSLR + 398.24 MXN (`gbm-real-2026-10-07.md`) | 3 × 1,219.00 + (3 × 49.12 + 177.82) × 18.36 + 398.24 | 10,025.54 | 10,025.54 | 0.000% |
| chatgpt-binance | 0.00198801 BTC + 0.030969 ETH + 502.33 MXN (`binance-real-2026-10-07.md`) | (0.00198801 × 82,465.54 + 0.030969 × 2,482.88) × 18.36 + 502.33 | 4,924.05 | 4,923.40 | −0.013% |
| grok-binance | 0.00330974 BTC + 1.617 MXN + 0.00000843 ETH (`binance-real-2026-10-07.md`) | (0.00330974 × 82,465.54 + 0.00000843 × 2,482.88) × 18.36 + 1.617 | 5,013.17 | 5,013.19 | +0.000% |

Las cuatro quedan dentro de la tolerancia de 0.1%; el marcador conserva las cifras del cierre. Sin flujos, el TWR es valor/aportación − 1: ChatGPT GBM −0.62%, Grok GBM +0.26%, ChatGPT Binance −1.53% y Grok Binance +0.26%.

**Drawdown máximo (pico contra valle, base 100 = aportación; valuaciones del 7, 8 y 9-oct):** ChatGPT GBM −0.82% (8-oct); Grok GBM **−0.86%** (del pico de 10,112.43 del 8-oct a 10,025.54 del 9-oct; la conciliación del 9-oct puso −0.38% porque medía el mínimo contra la aportación, no contra el pico); ChatGPT Binance −3.11% (8-oct); Grok Binance −1.76% (8-oct).
