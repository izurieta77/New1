# Marcador de la competencia

> Métrica: TWR en MXN de la cuenta combinada (GBM + Binance), con GBM y Binance también por separado. **CETES 28:** con `BANXICO_TOKEN` en el entorno, `python3 herramientas/banxico.py` da la tasa oficial de subasta (SIE SF43936; al 24-sep-2026: 6.15% anual); sin token, se usa el proxy anotado y se dice que es proxy. Solo se registran datos que reporte el dueño en `competencia/rivales.csv`. No se atribuye habilidad solo por el saldo final. Temporada: 28-sep-2026 al 28-ene-2027.

Actualizado: 2026-10-01 (cierre). El TWR del papel arranca con índice 100 al cierre del 28-sep.

**Meta del dueño para las tres IAs (25-sep-2026):** +40% mínimo, +60% bueno, +200% excepcional en la temporada. Cuando haya datos, se marca por cuenta si la alcanzó (`config/parametros.json` → `meta_temporada_dueno`).

| Cuenta | TWR | Drawdown máximo | Días invertidos | Fuente |
|---|---|---|---|---|
| arena-claude (papel, GBM) | **+2.65%** (índice 102.65 al 1-oct; valor 20,435.20 MXN; benchmark 50% S&P TR MXN + 50% CETES +1.44%). Casi todo por USD/MXN 17.825 → 18.291; en USD, SPYM −0.4% y QQQM +0.9% sobre costo. Costo con el tipo de cambio de ejecución (`bitacora/arbitraje/2026-09-30.md`) | 0.00% (pico el 1-oct) | 3 | `bitacora/equity.csv` |
| arena-claude-binance (papel) | **+0.12%** (índice 100.12 al 29-sep; valor 10,055.01 MXN, serie re-expresada por la rutina cripto) | 0.00% | 1 | `bitacora/papel-binance/equity.csv` |
| arena-claude (real, GBM) | sin fondear todavía: capital nuevo de 10,000 MXN (dueño, 29-sep); boleta VIGENTE el 30-sep y el 1-oct, sin depósito ni llenados reportados; pasa al comité del 2-oct | — | 0 | dueño |
| arena-claude-binance (real) | **−0.09% sobre la aportación** (el TWR arranca en 100 con esta valuación; valor 4,995.30 MXN al 30-sep 00:25 UTC; 0.001325 BTC + 3,001.83 MXN) | 0.00% | 1 | `bitacora/real-binance/equity.csv`, `rivales.csv` |
| chatgpt-gbm / chatgpt-binance | sin datos | sin datos | — | dueño |
| grok-gbm / grok-binance | sin datos de cuenta real. Grok reportó **papel** al 25-sep (GBM 19,893.69; Binance 9,921.24): no entra al marcador real | sin datos | — | dueño (`rivales.csv`) |

## Tabla mensual

| Mes | arena-claude papel GBM | Benchmark 50% S&P TR MXN + 50% CETES | arena-claude papel Binance | arena-claude real GBM | arena-claude real Binance | ChatGPT | Grok |
|---|---|---|---|---|---|---|---|
| Sep-2026 (28-30 sep) | +1.30% (DD 0.00%) | +0.64% | +0.12% al 29-sep (DD 0.00%) | sin fondear | −0.09% sobre la aportación (desde el 29-sep) | sin datos | sin datos (solo reportes de papel) |

