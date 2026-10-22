# Valuación de cierre de las cuentas reales de los rivales · jueves 22-oct-2026

Respaldo de las cifras de los rivales en `competencia/marcador.md`.
- **Posiciones:** las registradas (`gbm-real-2026-10-07.md` y `binance-real-2026-10-07.md`), sin flujos nuevos.
- **Advertencia:** la captura del dueño del 22-oct (`datos/entrada-dueno/2026-10-22.md`) **no cuadra con lo registrado** en GBM:
  - no aparece AMKR (3 títulos de Grok);
  - VISTA A y GFNORTE O no salen en la vista SIC, así que no se sabe si siguen;
  - hay NFLX (4), UBER (3) y LULU (1) sin registro ni atribución.
  - Hasta que el dueño atribuya y confirme, las cifras de **chatgpt-gbm** y **grok-gbm** son de las posiciones registradas, **no de la cuenta real de hoy**. Las de Binance no cambian.

**Insumos** (Yahoo chart v8, `regularMarketPrice`; consulta de las 21:4x UTC):

| Tipo | Activo | Precio | Hora de la cotización |
|---|---|---|---|
| Acción | NVDA | 212.21 USD | 20:00 UTC |
| Acción | GFNORTEO.MX | 207.91 MXN | 19:59 UTC |
| Acción | VISTAA.MX | 1,321.45 MXN | 18:49 UTC |
| Acción | AMKR | 39.05 USD | 20:00 UTC |
| Acción | FSLR | 171.25 USD | 20:00 UTC |
| Cripto | BTC-USD | **81,352.68** | Es el mismo precio de los libros de Claude (`portafolio.py valuar`, ~21:40 UTC): regla del 22-oct, un solo precio. Yahoo 1m a las 21:41 marcaba 81,367.55 (diferencia 0.02%) |
| Cripto | ETH-USD | 2,390.65 | 21:41 UTC |
| Tipo de cambio | USD/MXN | 18.6890 | el de `portafolio.py valuar` en los cuatro libros de Claude |

| Cuenta | Cálculo | Valor MXN | TWR (sin flujos) |
|---|---|---:|---:|
| chatgpt-gbm | 212.21 × 18.6890 + 13 × 207.91 + 3,259.21 | 9,928.03 | −0.72% (posiciones registradas) |
| grok-gbm | 3 × 1,321.45 + (3 × 39.05 + 171.25) × 18.6890 + 398.24 | 9,752.50 | −2.48% (posiciones registradas; AMKR no aparece en la captura) |
| chatgpt-binance | (0.00198801 × 81,352.68 + 0.030969 × 2,390.65) × 18.6890 + 502.33 | 4,908.56 | −1.83% |
| grok-binance | (0.00330974 × 81,352.68 + 0.00000843 × 2,390.65) × 18.6890 + 1.617 | 5,034.12 | +0.68% |

**Drawdown:**

| Cuenta | Drawdown | Contra qué |
|---|---|---|
| Grok GBM | **−4.85%** (máximo nuevo; antes −4.28%) | pico implícito de 10,249 |
| ChatGPT GBM | −1.62% | pico del 21-oct |
| Grok Binance | −3.92% | pico del 21-oct |
| ChatGPT Binance | −3.61% | valor del 21-oct (pico no establecido) |

Día de aversión al riesgo: ^GSPC −1.21%, Nasdaq y chips abajo (NVDA −4.4%, AMKR −10.7%), BTC −3.2%. El dólar casi no se movió en el día (18.6787 → 18.6890 en Yahoo).
