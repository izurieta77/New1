# Marcador de la competencia

> Métrica: TWR en MXN de la cuenta combinada (GBM + Binance), con GBM y Binance también por separado. **CETES 28:** con `BANXICO_TOKEN` en el entorno, `python3 herramientas/banxico.py` da la tasa oficial de subasta (SIE SF43936; al 24-sep-2026: 6.15% anual); sin token, se usa el proxy anotado y se dice que es proxy. Solo se registran datos que reporte el dueño en `competencia/rivales.csv`. No se atribuye habilidad solo por el saldo final. Temporada: 28-sep-2026 al 28-ene-2027.

Actualizado: 2026-09-28 (rutina de cierre). Día 0 de la temporada: el TWR arranca con índice 100 al cierre del 28-sep; los valores de hoy son "desde el fondeo".

**Meta del dueño para las tres IAs (25-sep-2026):** +40% mínimo, +60% bueno, +200% excepcional en la temporada. Cuando haya datos, se marca por cuenta si la alcanzó (`config/parametros.json` → `meta_temporada_dueno`).

| Cuenta | TWR | Drawdown máximo | Días invertidos | Fuente |
|---|---|---|---|---|
| arena-claude (papel, GBM) | día 0 (índice 100). Valor 19,978.62 MXN contra 20,000 aportados (−0.11%: comisiones y precio de cierre frente a la ejecución de las 08:45) | 0.0% | 0 | `bitacora/equity.csv` |
| arena-claude-binance (papel) | día 0. Valor 10,014.74 MXN contra 10,000 (+0.15%) | 0.0% | 0 | `bitacora/papel-binance/equity.csv` |
| arena-claude (real, GBM) | sin datos (el dueño aún no reporta ejecución ni valor) | sin datos | 0 | dueño (`rivales.csv`) |
| arena-claude-binance | sin datos | sin datos | 0 | dueño |
| chatgpt-gbm / chatgpt-binance | sin datos | sin datos | — | dueño |
| grok-gbm / grok-binance | sin datos de cuenta real. Grok reportó **papel** al 25-sep (GBM 19,893.69; Binance 9,921.24): no entra al marcador real | sin datos | — | dueño (`rivales.csv`) |
