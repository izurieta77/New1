# Marcador de la competencia

> Métrica: TWR en MXN de la cuenta combinada (GBM + Binance), con GBM y Binance también por separado. **CETES 28:** con `BANXICO_TOKEN` en el entorno, `python3 herramientas/banxico.py` da la tasa oficial de subasta (SIE SF43936; al 24-sep-2026: 6.15% anual); sin token, se usa el proxy anotado y se dice que es proxy. Solo se registran datos que reporte el dueño en `competencia/rivales.csv`. No se atribuye habilidad solo por el saldo final. Temporada: 28-sep-2026 al 28-ene-2027.

Actualizado: **2026-10-21 (cierre)** para los cuatro libros de Claude (fila del 21-oct de cada `equity.csv`) y para los cuatro rivales (valuación de cierre del 21-oct con las posiciones reportadas por el dueño; precios y tipo de cambio en `competencia/valuacion-real-2026-10-21.md`). El peso perdió 1.39% en el día [Conciliación 22-oct-2026 03:0x UTC, `bitacora/arbitraje/2026-10-21.md` §6: el dólar subió **1.38%** y el peso perdió **1.37%**] (USD/MXN 18.6692), lo que sube el valor en MXN de todo lo que está en dólares.

**Meta del dueño para las tres IAs (25-sep-2026):** +40% mínimo, +60% bueno, +200% excepcional en la temporada. Cuando haya datos, se marca por cuenta si la alcanzó (`config/parametros.json` → `meta_temporada_dueno`).

| Cuenta | TWR | Drawdown máximo | Días invertidos | Fuente |
|---|---|---|---|---|
| arena-claude (papel, GBM) | **+4.08%** (índice 104.08 al 21-oct; valor 20,816.73 MXN: 5 SPYM + 1 QQQM + 2 UPRO + 1,071.96 de efectivo). Sin órdenes nuevas desde O0004 y O0005 (5-oct). Benchmark: `reporte` dio n/d hoy (FRED en mantenimiento) | −3.35% (del pico del 9-oct, índice 104.41, al 16-oct); hoy −0.32% | 18 | `bitacora/equity.csv` |
| arena-claude-binance (papel) | **+2.64%** (índice 102.64 al 21-oct, **pico nuevo**; valor 10,264.28 MXN: 0.002698 BTC + 5,996.44 MXN) | −1.76% (del pico del 5-oct al 8-oct); hoy 0.00% | 24 | `bitacora/papel-binance/equity.csv` |
| arena-claude (real, GBM) | **+1.36%** (índice 101.36 al 21-oct, **pico nuevo**; valor 10,136.30 MXN: 3 SPYM + efectivo 5,040.16; ~50% efectivo). Boleta VT del 19-oct: EN ESPERA hasta que el dueño confirme. El dueño reportó el 20-oct que VT no aparece al buscar "vanguard" (`datos/entrada-dueno/2026-10-20.md`) | −0.67% (del pico del 9-oct al 16-oct); hoy 0.00% | 11 | `bitacora/real/equity.csv` |
| arena-claude-binance (real) | **+1.96%** (índice 101.96 al 21-oct, **pico nuevo**; valor 5,097.79 MXN: 0.001325 BTC + 3,001.83 MXN) | −0.63% (8-oct); hoy 0.00% | 23 | `bitacora/real-binance/equity.csv`; saldo confirmado en `competencia/binance-real-2026-10-07.md` |
| chatgpt-gbm (real) | **+0.91%** sobre 10,000 (valor 10,091.09 al cierre del 21-oct; 1 NVDA + 13 GFNORTE O, 33% efectivo). Sin flujos: TWR = valor/aportación − 1 | −1.63% (15-oct); hoy, pico nuevo | 11 | posiciones: `competencia/gbm-real-2026-10-07.md`; valuación: `competencia/valuacion-real-2026-10-21.md` |
| chatgpt-binance (real) | **+1.85%** sobre 5,000 (valor 5,092.47 al cierre del 21-oct; BTC + ETH + 502 MXN) | −3.11% (8-oct) | 23 | posiciones: `competencia/binance-real-2026-10-07.md`; valuación: `competencia/valuacion-real-2026-10-21.md` |
| grok-binance (real) | **+4.79%** sobre 5,000 (valor 5,239.32 al cierre del 21-oct; BTC + 1.62 MXN + polvo de ETH) | −1.76% (8-oct); hoy, pico nuevo | 23 | posiciones: `competencia/binance-real-2026-10-07.md`; valuación: `competencia/valuacion-real-2026-10-21.md` |
| grok-gbm (real) | **+1.03%** sobre 10,000 (valor 10,102.91 al cierre del 21-oct; 3 VISTA A + 3 AMKR + 1 FSLR, 4% efectivo). Sin flujos: TWR = valor/aportación − 1 | −4.28% (19-oct); hoy −1.43% | 11 | posiciones: `competencia/gbm-real-2026-10-07.md`; valuación: `competencia/valuacion-real-2026-10-21.md` |
| grok-gbm papel / grok-binance | sin datos de cuenta real. Grok reportó **papel** al 25-sep (GBM 19,893.69; Binance 9,921.24): no entra al marcador real | sin datos | — | dueño (`rivales.csv`) |

## Tabla mensual

| Mes | arena-claude papel GBM | Benchmark 50% S&P TR MXN + 50% CETES | arena-claude papel Binance | arena-claude real GBM | arena-claude real Binance | ChatGPT | Grok |
|---|---|---|---|---|---|---|---|
| Sep-2026 (28-30 sep) | +0.83% con base al fondeo (antes +1.30% con base al cierre del 28-sep; DD −0.46%) | +0.31% con base 100 al fondeo (antes +0.64%, medido desde el cierre del 28-sep; nota del 9-oct) | +0.55% al 29-sep con base al fondeo (antes +0.12%; DD 0.00%) | sin fondear | −0.09% sobre la aportación (desde el 29-sep) | sin datos | sin datos (solo reportes de papel) |

Nota (conciliación, 8-oct): la columna de septiembre del papel se recalculó con la base al fondeo (fallo `bitacora/arbitraje/2026-10-08-base-twr.md`). El benchmark (`portafolio.py::benchmark`) ya incluía el primer día, así que ahora las dos series tienen la misma base. **[Corregido 9-oct-2026, conciliación, fallo `bitacora/arbitraje/2026-10-09-reporte-base-twr.md`]:** la última frase era falsa. La serie del benchmark (`serie_benchmark`) sí vale 100 antes del primer día (99.67 al 28-sep), pero el +0.64% se midió contra su primera fila, igual que el papel. Con base 100 queda en **+0.31%** al 30-sep: 100.3062, con Yahoo ^SP500TR, MXN=X y el proxy FRED de CETES consultados el 9-oct. `portafolio.py reporte` ya mide las dos series desde 100.

