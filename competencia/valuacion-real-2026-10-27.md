# Valuación de cierre de las cuentas reales de los rivales · martes 27-oct-2026

Respaldo de las cifras de los rivales en `competencia/marcador.md`.
- **Posiciones:** las registradas (`gbm-real-2026-10-07.md` y `binance-real-2026-10-07.md`), sin flujos nuevos.
- **Las de GBM no cuadran con la captura del dueño del 22-oct** (`competencia/conciliacion-cuenta-gbm-2026-10-22.md`): son **del registro, no confirmadas**.

**Insumos** (Yahoo chart v8, `regularMarketPrice`; consulta de ~21:5x UTC):

| Tipo | Activo | Precio | Hora de la cotización |
|---|---|---|---|
| Acción | NVDA | 217.94 USD | 20:00 UTC |
| Acción | GFNORTEO.MX | 213.64 MXN | 19:59 UTC |
| Acción | VISTAA.MX | 1,359.00 MXN | **14:40 UTC** (último hecho del día; serie poco líquida) |
| Acción | AMKR | 39.94 USD | 20:00 UTC |
| Acción | FSLR | 175.85 USD | 20:00 UTC |
| Cripto | BTC-USD | **81,103.94** | el mismo de los libros de Claude (`portafolio.py valuar`) |
| Cripto | ETH-USD | 2,352.09 | 21:41 UTC |
| Tipo de cambio | USD/MXN | 18.6500 | el de `portafolio.py valuar` |

| Cuenta | Cálculo | Valor MXN | TWR (sin flujos) |
|---|---|---:|---:|
| chatgpt-gbm | 217.94 × 18.65 + 13 × 213.64 + 3,259.21 | 10,101.11 | +1.01% (del registro) |
| grok-gbm | 3 × 1,359.00 + (3 × 39.94 + 175.85) × 18.65 + 398.24 | 9,989.49 | −0.11% (del registro) |
| chatgpt-binance | (0.00198801 × 81,103.94 + 0.030969 × 2,352.09) × 18.65 + 502.33 | 4,867.87 | −2.64% |
| grok-binance | (0.00330974 × 81,103.94 + 0.00000843 × 2,352.09) × 18.65 + 1.617 | 5,008.26 | +0.17% |

**Drawdown** (contra el máximo de los valores de cierre de `valuacion-real-*.md`):
- **Binance:** Grok −4.41% y ChatGPT −4.41%, los dos contra el pico del 21-oct.
- **GBM:** ChatGPT 0.00% (máximo nuevo, sobre el 10,091.09 del 21-oct) y Grok −2.55% (pico del 13-oct, 10,250.39). Los dos son del registro.
- **Lo que movió a Grok GBM (+3.85% en el día):** AMKR, que subió de 36.81 a 39.94.
