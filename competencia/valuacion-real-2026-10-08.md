# Valuación de cierre de las cuentas reales de los rivales · jueves 8-oct-2026

Respaldo de las cifras de los rivales que el cierre del 8-oct escribió en `competencia/marcador.md` (paso 5, nota c, de `rutinas/diaria-cierre.md`). Es una **valuación del sistema**, no un reporte del dueño, y por eso no va en `competencia/rivales.csv` (REGLAS §5). Las posiciones son las que reportó el dueño. La corrida de cierre (~21:37 UTC) no archivó sus insumos; los reconstruyó la conciliación del 9-oct (fallo `bitacora/arbitraje/2026-10-09-marcador-cierre-reincidencia.md`) con datos públicos que se pueden volver a consultar.

**Insumos:**
- **Cierres Yahoo chart v8 (1d) del 8-oct:** NVDA 230.48 USD; GFNORTEO.MX 190.12 MXN; VISTAA.MX 1,228.49 MXN; AMKR 51.00 USD; FSLR 178.85 USD.
- **USD/MXN:** 18.17, el que cita el brief del 8-oct, L35. Yahoo MXN=X 5m entre 21:10 y 21:35 UTC: 18.158-18.176.
- **Cripto:** BTC 81,660 USD y ETH 2,476 USD (brief del 8-oct, L36). Yahoo 5m de 21:30-21:35 UTC: BTC 81,603-81,670 y ETH 2,472-2,476.

| Cuenta | Posiciones (fuente) | Cálculo | Reproducido | Registrado por el cierre | Diferencia |
|---|---|---|---|---|---|
| chatgpt-gbm | 1 NVDA + 13 GFNORTE O + 3,259.21 MXN (`gbm-real-2026-10-07.md`) | 230.48 × 18.17 + 13 × 190.12 + 3,259.21 | 9,918.59 | 9,917.90 | +0.007% |
| grok-gbm | 3 VISTA A + 3 AMKR + 1 FSLR + 398.24 MXN (`gbm-real-2026-10-07.md`) | 3 × 1,228.49 + (3 × 51.00 + 178.85) × 18.17 + 398.24 | 10,113.42 | 10,112.43 | +0.010% |
| chatgpt-binance | 0.00198801 BTC + 0.030969 ETH + 502.33 MXN (`binance-real-2026-10-07.md`) | (0.00198801 × 81,660 + 0.030969 × 2,476) × 18.17 + 502.33 | 4,845.33 | 4,844.38 | +0.020% |
| grok-binance | 0.00330974 BTC + 1.617 MXN + 0.00000843 ETH (`binance-real-2026-10-07.md`) | (0.00330974 × 81,660 + 0.00000843 × 2,476) × 18.17 + 1.617 | 4,912.86 | 4,912.08 | +0.016% |

Las cuatro quedan dentro de la tolerancia de 0.1%. El marcador conserva las cifras del cierre. Sin flujos, el TWR es valor/aportación − 1: ChatGPT GBM −0.82%, Grok GBM +1.12%, ChatGPT Binance −3.11% y Grok Binance −1.76%.
