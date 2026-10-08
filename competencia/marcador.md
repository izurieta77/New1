# Marcador de la competencia

> Métrica: TWR en MXN de la cuenta combinada (GBM + Binance), con GBM y Binance también por separado. **CETES 28:** con `BANXICO_TOKEN` en el entorno, `python3 herramientas/banxico.py` da la tasa oficial de subasta (SIE SF43936; al 24-sep-2026: 6.15% anual); sin token, se usa el proxy anotado y se dice que es proxy. Solo se registran datos que reporte el dueño en `competencia/rivales.csv`. No se atribuye habilidad solo por el saldo final. Temporada: 28-sep-2026 al 28-ene-2027.

Actualizado: 2026-10-07 (cierre) para los cuatro libros de Claude (papel GBM, papel Binance, real GBM, real Binance) y los rivales de GBM; rivales de Binance al 7-oct 12:13. **Base del TWR (fallo `bitacora/arbitraje/2026-10-08-base-twr.md`, conciliación 8-oct):** todas las filas usan el mismo índice time-weighted con **base 100 = la aportación al fondeo** (`config/parametros.json` → `metrica_competencia`: "TWR en MXN ... desde el fondeo"), así que el resultado del primer día (comisiones y movimiento desde la compra) sí cuenta. Hasta el 7-oct el índice de los CSV valía 100 en el primer cierre y omitía el día 1 (papel GBM −0.46%, papel Binance +0.43%, real Binance −0.09%), mientras que las filas reales de esta tabla usaban valor/aportación: dos bases en una tabla rotulada "TWR". Se corrigió `herramientas/portafolio.py::recalcular_indice` y se recalcularon los cuatro `equity.csv` con las mismas cifras de equity (sin datos nuevos). Mientras no haya un segundo flujo, TWR = valor/aportación − 1. **Nota (conciliación, 4-oct):** el encabezado decía solo "2026-10-02" pese a que la fila de Binance ya citaba datos del 3-oct desde la conciliación anterior; se aclara aquí cuál dato es de qué fecha para que ninguna cifra quede sin su fecha de corte visible.

**Meta del dueño para las tres IAs (25-sep-2026):** +40% mínimo, +60% bueno, +200% excepcional en la temporada. Cuando haya datos, se marca por cuenta si la alcanzó (`config/parametros.json` → `meta_temporada_dueno`).

| Cuenta | TWR | Drawdown máximo | Días invertidos | Fuente |
|---|---|---|---|---|
| arena-claude (papel, GBM) | **+2.30%** (índice 102.30 al 7-oct; valor 20,460.32 MXN). Con la base anterior (índice 100 al cierre del 28-sep) se reportaba +2.78%; ver nota de la base. El 5-oct se ejecutaron O0004 (venta de 2 SPYM a 90.89) y O0005 (compra de 2 UPRO a 152.40 con stop en 135.76), comité W40. Costo con el tipo de cambio de ejecución | −0.46% (28-sep, primer día; desde el pico del 6-oct: −0.39%) | 7 | `bitacora/equity.csv` |
| arena-claude-binance (papel) | **+0.29%** (índice 100.29 al 7-oct; valor 10,028.72 MXN; fila del 7-oct guardada por el cierre). Con la base anterior: −0.14%. Sin filas del 30-sep al 2-oct (ver la nota de conciliación del 3-oct en el historial de git) ni del 4-oct (fin de semana) | −1.49% (pico 5-oct 10,180.21 → 7-oct) | 9 | `bitacora/papel-binance/equity.csv` |
| arena-claude (real, GBM) | **+0.05%** sobre 10,000 (valor 10,005.00 al cierre del 8-oct; 3 SPYM, 50% efectivo; `bitacora/real/`) | — | 9 | `bitacora/real/operaciones.csv` |
| arena-claude-binance (real) | **−0.63%** sobre 5,000 (valor 4,968.26 al cierre del 8-oct; 0.001325 BTC + 3,001.83 MXN) | — | 9 | `competencia/binance-real-2026-10-07.md` |
| chatgpt-gbm (real) | **−0.82%** sobre 10,000 (valor 9,917.90 al cierre del 8-oct, Yahoo 2d; 1 NVDA + 13 GFNORTE O, 33% efectivo) | — | 9 | `competencia/gbm-real-2026-10-07.md` |
| chatgpt-binance (real) | **−3.11%** sobre 5,000 (valor 4,844.38 al 8-oct; BTC + ETH + 502 MXN; BTC 81,660 USD) | — | 9 | `competencia/binance-real-2026-10-07.md` |
| grok-binance (real) | **−1.76%** sobre 5,000 (valor 4,912.08 al 8-oct; BTC + ETH + 1.62 MXN) | — | 9 | `competencia/binance-real-2026-10-07.md` |
| grok-gbm (real) | **+1.12%** sobre 10,000 (valor 10,112.43 al cierre del 8-oct, Yahoo 2d; 3 VISTA A + 3 AMKR + 1 FSLR, 4% efectivo) | — | 9 | `competencia/gbm-real-2026-10-07.md` |
| grok-gbm papel / grok-binance | sin datos de cuenta real. Grok reportó **papel** al 25-sep (GBM 19,893.69; Binance 9,921.24): no entra al marcador real | sin datos | — | dueño (`rivales.csv`) |

## Tabla mensual

| Mes | arena-claude papel GBM | Benchmark 50% S&P TR MXN + 50% CETES | arena-claude papel Binance | arena-claude real GBM | arena-claude real Binance | ChatGPT | Grok |
|---|---|---|---|---|---|---|---|
| Sep-2026 (28-30 sep) | +0.83% con base al fondeo (antes +1.30% con base al cierre del 28-sep; DD −0.46%) | +0.64% | +0.55% al 29-sep con base al fondeo (antes +0.12%; DD 0.00%) | sin fondear | −0.09% sobre la aportación (desde el 29-sep) | sin datos | sin datos (solo reportes de papel) |

Nota (conciliación, 8-oct): la columna de septiembre del papel se recalculó con la base al fondeo (fallo `bitacora/arbitraje/2026-10-08-base-twr.md`). El benchmark (`portafolio.py::benchmark`) ya incluía el primer día, así que ahora las dos series tienen la misma base.

