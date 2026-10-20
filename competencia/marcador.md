# Marcador de la competencia

> Métrica: TWR en MXN de la cuenta combinada (GBM + Binance), con GBM y Binance también por separado. **CETES 28:** con `BANXICO_TOKEN` en el entorno, `python3 herramientas/banxico.py` da la tasa oficial de subasta (SIE SF43936; al 24-sep-2026: 6.15% anual); sin token, se usa el proxy anotado y se dice que es proxy. Solo se registran datos que reporte el dueño en `competencia/rivales.csv`. No se atribuye habilidad solo por el saldo final. Temporada: 28-sep-2026 al 28-ene-2027.

Actualizado: **2026-10-19 (cierre)** para los cuatro libros de Claude (fila del 19-oct de cada `equity.csv`) y para los cuatro rivales (valuación de cierre del 19-oct con las posiciones reportadas por el dueño; precios y tipo de cambio en `competencia/valuacion-real-2026-10-19.md`).

**Meta del dueño para las tres IAs (25-sep-2026):** +40% mínimo, +60% bueno, +200% excepcional en la temporada. Cuando haya datos, se marca por cuenta si la alcanzó (`config/parametros.json` → `meta_temporada_dueno`).

| Cuenta | TWR | Drawdown máximo | Días invertidos | Fuente |
|---|---|---|---|---|
| arena-claude (papel, GBM) | **+1.41%** (índice 101.41 al 19-oct; valor 20,281.93 MXN: 5 SPYM + 1 QQQM + 2 UPRO + 1,071.96 de efectivo; benchmark 50/50 +1.78% en el periodo, el papel sigue debajo del benchmark por 0.37 pp). Sin órdenes nuevas desde O0004 y O0005 (5-oct) | −3.35% (del pico del 9-oct, índice 104.41, al 16-oct); hoy −2.88% | 16 | `bitacora/equity.csv` |
| arena-claude-binance (papel) | **+0.67%** (índice 100.67 al 19-oct; valor 10,066.76 MXN: 0.002698 BTC + 5,996.44 MXN) | −1.76% (del pico del 5-oct, índice 101.80, al 8-oct); hoy −1.11% | 22 | `bitacora/papel-binance/equity.csv` |
| arena-claude (real, GBM) | **+0.23%** (índice 100.23 al 19-oct; valor 10,023.48 MXN: 3 SPYM + efectivo 5,040.16; ~50% efectivo). Boleta del 5-oct cerrada el 7-oct (G1 ejecutada, G2 cancelada). Boleta VT del 19-oct: **VENCIDA** sin reporte del dueño (fue VIGENTE desde las 14:42 UTC, límite 2,908.15 MXN); no entra al libro; EN ESPERA hasta que el dueño confirme si compró [conciliación 20-oct-2026, `bitacora/arbitraje/2026-10-19.md` §1] | −0.67% (del pico del 9-oct al 16-oct); hoy −0.64% | 9 | `bitacora/real/equity.csv` |
| arena-claude-binance (real) | **+0.02%** (índice 100.02 al 19-oct; valor 5,000.76 MXN: 0.001325 BTC + 3,001.83 MXN) | −0.63% (8-oct); hoy −0.56% | 21 | `bitacora/real-binance/equity.csv`; saldo confirmado en `competencia/binance-real-2026-10-07.md` |
| chatgpt-gbm (real) | **−0.81%** sobre 10,000 (valor 9,918.82 al cierre del 19-oct; 1 NVDA + 13 GFNORTE O, 33% efectivo). Sin flujos: TWR = valor/aportación − 1 | −1.63% (15-oct); hoy −0.90% | 9 | posiciones: `competencia/gbm-real-2026-10-07.md`; valuación: `competencia/valuacion-real-2026-10-19.md` |
| chatgpt-binance (real) | **−2.60%** sobre 5,000 (valor 4,870.00 al cierre del 19-oct; BTC + ETH + 502 MXN) | −3.11% (8-oct) | 21 | posiciones: `competencia/binance-real-2026-10-07.md`; valuación: `competencia/valuacion-real-2026-10-19.md` |
| grok-binance (real) | **−0.10%** sobre 5,000 (valor 4,995.14 al cierre del 19-oct; BTC + 1.62 MXN + polvo de ETH) | −1.76% (8-oct); hoy −1.40% | 21 | posiciones: `competencia/binance-real-2026-10-07.md`; valuación: `competencia/valuacion-real-2026-10-19.md` |
| grok-gbm (real) | **−1.88%** sobre 10,000 (valor 9,811.53 al cierre del 19-oct; 3 VISTA A + 3 AMKR + 1 FSLR, 4% efectivo). Sin flujos: TWR = valor/aportación − 1 | **−4.28%** (del pico del 13-oct al 19-oct; nuevo máximo) | 9 | posiciones: `competencia/gbm-real-2026-10-07.md`; valuación: `competencia/valuacion-real-2026-10-19.md` |
| grok-gbm papel / grok-binance | sin datos de cuenta real. Grok reportó **papel** al 25-sep (GBM 19,893.69; Binance 9,921.24): no entra al marcador real | sin datos | — | dueño (`rivales.csv`) |

## Tabla mensual

| Mes | arena-claude papel GBM | Benchmark 50% S&P TR MXN + 50% CETES | arena-claude papel Binance | arena-claude real GBM | arena-claude real Binance | ChatGPT | Grok |
|---|---|---|---|---|---|---|---|
| Sep-2026 (28-30 sep) | +0.83% con base al fondeo (antes +1.30% con base al cierre del 28-sep; DD −0.46%) | +0.31% con base 100 al fondeo (antes +0.64%, medido desde el cierre del 28-sep; nota del 9-oct) | +0.55% al 29-sep con base al fondeo (antes +0.12%; DD 0.00%) | sin fondear | −0.09% sobre la aportación (desde el 29-sep) | sin datos | sin datos (solo reportes de papel) |

Nota (conciliación, 8-oct): la columna de septiembre del papel se recalculó con la base al fondeo (fallo `bitacora/arbitraje/2026-10-08-base-twr.md`). El benchmark (`portafolio.py::benchmark`) ya incluía el primer día, así que ahora las dos series tienen la misma base. **[Corregido 9-oct-2026, conciliación, fallo `bitacora/arbitraje/2026-10-09-reporte-base-twr.md`]:** la última frase era falsa. La serie del benchmark (`serie_benchmark`) sí vale 100 antes del primer día (99.67 al 28-sep), pero el +0.64% se midió contra su primera fila, igual que el papel. Con base 100 queda en **+0.31%** al 30-sep: 100.3062, con Yahoo ^SP500TR, MXN=X y el proxy FRED de CETES consultados el 9-oct. `portafolio.py reporte` ya mide las dos series desde 100.

