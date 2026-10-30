# Valuación de cierre de las cuentas reales de los rivales · viernes 30-oct-2026

Respaldo de las cifras de los rivales en `competencia/marcador.md`. Posiciones registradas (`gbm-real-2026-10-07.md` y `binance-real-2026-10-07.md`), sin flujos nuevos. **GBM: del registro, no confirmadas. Binance: retiros cerrados desde ≈21:50 UTC del 29-oct; es valuación a mercado con riesgo de contraparte abierto.**

**Insumos** (Yahoo chart v8, `regularMarketPrice`; consulta antes del commit de este cierre):

| Tipo | Activo | Precio | Hora de la cotización |
|---|---|---|---|
| Acción | NVDA | 204.64 USD | 20:00 UTC |
| Acción | GFNORTEO.MX | 209.04 MXN | 19:59 UTC |
| Acción | VISTAA.MX | 1,340.75 MXN | 19:35 UTC (**último hecho; puede ser del 29-oct**, serie poco líquida) |
| Acción | AMKR | 39.50 USD | 20:00 UTC |
| Acción | FSLR | 174.40 USD | 20:00 UTC |
| Cripto | BTC-USD | **76,694.14** | el de los libros de Claude (implícito en `papel-binance/equity.csv`) |
| Cripto | ETH-USD | 2,237.82 | 21:39 UTC |
| Tipo de cambio | USD/MXN | 18.7435 | el de `portafolio.py valuar` |

| Cuenta | Cálculo | Valor MXN | TWR (sin flujos) |
|---|---|---:|---:|
| chatgpt-gbm | 204.64 × 18.7435 + 13 × 209.04 + 3,259.21 | 9,812.40 | −1.88% (del registro) |
| grok-gbm | 3 × 1,340.75 + (3 × 39.50 + 174.40) × 18.7435 + 398.24 | 9,910.46 | −0.90% (del registro) |
| chatgpt-binance | (0.00198801 × 76,694.14 + 0.030969 × 2,237.82) × 18.7435 + 502.33 | 4,659.11 | −6.82% |
| grok-binance | (0.00330974 × 76,694.14 + 0.00000843 × 2,237.82) × 18.7435 + 1.617 | 4,759.78 | −4.80% |

**Drawdown:**
- **Binance:** ChatGPT −8.51% y Grok −9.15% (máximos nuevos; pico del 21-oct).
- **GBM:** ChatGPT −2.86% (máximo nuevo) y Grok −3.32%, los dos del registro.
