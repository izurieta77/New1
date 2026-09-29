# Marcador de la competencia

> Métrica: TWR en MXN de la cuenta combinada (GBM + Binance), con GBM y Binance también por separado. **CETES 28:** con `BANXICO_TOKEN` en el entorno, `python3 herramientas/banxico.py` da la tasa oficial de subasta (SIE SF43936; al 24-sep-2026: 6.15% anual); sin token, se usa el proxy anotado y se dice que es proxy. Solo se registran datos que reporte el dueño en `competencia/rivales.csv`. No se atribuye habilidad solo por el saldo final. Temporada: 28-sep-2026 al 28-ene-2027.

Actualizado: 2026-09-29 (rutina de cierre). El TWR del papel arranca con índice 100 al cierre del 28-sep.

**Meta del dueño para las tres IAs (25-sep-2026):** +40% mínimo, +60% bueno, +200% excepcional en la temporada. Cuando haya datos, se marca por cuenta si la alcanzó (`config/parametros.json` → `meta_temporada_dueno`).

| Cuenta | TWR | Drawdown máximo | Días invertidos | Fuente |
|---|---|---|---|---|
| arena-claude (papel, GBM) | **+1.28%** (índice 101.28 al 29-sep; valor 20,234.23 MXN). Casi todo por USD/MXN 17.75 → 18.03 | 0.00% (pico el 29-sep) | 1 | `bitacora/equity.csv` |
| arena-claude-binance (papel) | **+0.65%** (índice 100.65; valor 10,079.95 MXN) | 0.00% | 1 | `bitacora/papel-binance/equity.csv` |
| arena-claude (real, GBM) | sin fondear: 223.47 MXN según la captura del dueño del 28-sep; los 20,000 del torneo no se han depositado | — | 0 | dueño (`rivales.csv`) |
| arena-claude-binance | sin datos | sin datos | 0 | dueño |
| chatgpt-gbm / chatgpt-binance | sin datos | sin datos | — | dueño |
| grok-gbm / grok-binance | sin datos de cuenta real. Grok reportó **papel** al 25-sep (GBM 19,893.69; Binance 9,921.24): no entra al marcador real | sin datos | — | dueño (`rivales.csv`) |
