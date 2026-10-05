# Marcador de la competencia

> Métrica: TWR en MXN de la cuenta combinada (GBM + Binance), con GBM y Binance también por separado. **CETES 28:** con `BANXICO_TOKEN` en el entorno, `python3 herramientas/banxico.py` da la tasa oficial de subasta (SIE SF43936; al 24-sep-2026: 6.15% anual); sin token, se usa el proxy anotado y se dice que es proxy. Solo se registran datos que reporte el dueño en `competencia/rivales.csv`. No se atribuye habilidad solo por el saldo final. Temporada: 28-sep-2026 al 28-ene-2027.

Actualizado: 2026-10-05 (cierre) para los dos libros de papel; antes: 2026-10-02 (cierre) para el papel GBM; la fila de papel Binance tiene una corrección fechada 3-oct (ver su nota). El TWR del papel arranca con índice 100 al cierre del 28-sep. **Nota (conciliación, 4-oct):** el encabezado decía solo "2026-10-02" pese a que la fila de Binance ya citaba datos del 3-oct desde la conciliación anterior; se aclara aquí cuál dato es de qué fecha para que ninguna cifra quede sin su fecha de corte visible.

**Meta del dueño para las tres IAs (25-sep-2026):** +40% mínimo, +60% bueno, +200% excepcional en la temporada. Cuando haya datos, se marca por cuenta si la alcanzó (`config/parametros.json` → `meta_temporada_dueno`).

| Cuenta | TWR | Drawdown máximo | Días invertidos | Fuente |
|---|---|---|---|---|
| arena-claude (papel, GBM) | **+2.91%** (índice 102.91 al 5-oct; valor 20,486.35 MXN). El 5-oct se ejecutaron O0004 (venta de 2 SPYM a 90.89) y O0005 (compra de 2 UPRO a 152.40 con stop en 135.76), comité W40. Costo con el tipo de cambio de ejecución | 0.00% | 6 | `bitacora/equity.csv` |
| arena-claude-binance (papel) | **+1.37%** (índice 101.37 al 5-oct; valor 10,180.21 MXN; fila del 5-oct guardada por el cierre). Sin filas del 30-sep al 2-oct (ver la nota de conciliación del 3-oct en el historial de git) ni del 4-oct (fin de semana) | 0.00% | 8 | `bitacora/papel-binance/equity.csv` |
| arena-claude (real, GBM) | sin fondear. La boleta del 30-sep quedó ANULADA en el comité W40 y la sustituye `bitacora/boletas/2026-10-05.md` (3 SPYM + 1 UPRO con stop), condicionada a fondeo y a que el ticker aparezca en GBM | — | 0 | dueño |
| arena-claude-binance (real) | **−0.09% sobre la aportación** (el TWR arranca en 100 con esta valuación; valor 4,995.30 MXN al 30-sep 00:25 UTC; 0.001325 BTC + 3,001.83 MXN) | 0.00% | 1 | `bitacora/real-binance/equity.csv`, `rivales.csv` |
| chatgpt-gbm / chatgpt-binance | sin datos | sin datos | — | dueño |
| grok-gbm / grok-binance | sin datos de cuenta real. Grok reportó **papel** al 25-sep (GBM 19,893.69; Binance 9,921.24): no entra al marcador real | sin datos | — | dueño (`rivales.csv`) |

## Tabla mensual

| Mes | arena-claude papel GBM | Benchmark 50% S&P TR MXN + 50% CETES | arena-claude papel Binance | arena-claude real GBM | arena-claude real Binance | ChatGPT | Grok |
|---|---|---|---|---|---|---|---|
| Sep-2026 (28-30 sep) | +1.30% (DD 0.00%) | +0.64% | +0.12% al 29-sep (DD 0.00%) | sin fondear | −0.09% sobre la aportación (desde el 29-sep) | sin datos | sin datos (solo reportes de papel) |

