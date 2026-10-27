# Marcador de la competencia

> Métrica: TWR en MXN de la cuenta combinada (GBM + Binance), con GBM y Binance también por separado. **CETES 28:** con `BANXICO_TOKEN` en el entorno, `python3 herramientas/banxico.py` da la tasa oficial de subasta (SIE SF43936; al 24-sep-2026: 6.15% anual); sin token, se usa el proxy anotado y se dice que es proxy. Solo se registran datos que reporte el dueño en `competencia/rivales.csv`. No se atribuye habilidad solo por el saldo final. Temporada: 28-sep-2026 al 28-ene-2027.

Actualizado: **2026-10-27 (cierre)** para los cuatro libros de Claude (fila del 27-oct de cada `equity.csv`; sin órdenes nuevas) y para los cuatro rivales (posiciones **registradas**; precios en `competencia/valuacion-real-2026-10-27.md`). **Ojo:** la cuenta GBM compartida no cuadra (`competencia/conciliacion-cuenta-gbm-2026-10-22.md`). USD/MXN 18.6500.

**Meta del dueño para las tres IAs (25-sep-2026):** +40% mínimo, +60% bueno, +200% excepcional en la temporada. Cuando haya datos, se marca por cuenta si la alcanzó (`config/parametros.json` → `meta_temporada_dueno`).

| Cuenta | TWR | Drawdown máximo | Días invertidos | Fuente |
|---|---|---|---|---|
| arena-claude (papel, GBM) | **+2.87%** (índice 102.87 al 27-oct; valor 20,574.91 MXN: 5 SPYM + 1 QQQM + 1 UPRO + 3,799.05 de efectivo). Sin órdenes nuevas (O0006 se ejecutó el 26-oct) | −3.35% (del pico del 9-oct al 16-oct); hoy −1.48% (siguiente nivel −12%) | 22 | `bitacora/equity.csv` |
| arena-claude-binance (papel) | **+0.77%** (índice 100.77 al 27-oct; valor 10,077.41 MXN: 0.002698 BTC a 81,103.94 + 5,996.44 MXN) | −2.55% (26-oct; pico del 21-oct, 102.64); hoy −1.82% | 30 | `bitacora/papel-binance/equity.csv` |
| arena-claude (real, GBM) | **+1.09%** (índice 101.09 al 27-oct; valor 10,109.23 MXN: 3 SPYM + **efectivo 5,040.16 registrado; última confirmación del dueño el 7-oct; en duda desde la captura del 22-oct (la cuenta compartida no cuadra)**). VT: 0, conocido; boleta caducada | −0.91% (23-oct); hoy −0.27% | 17 | `bitacora/real/equity.csv` |
| arena-claude-binance (real) | **+0.12%** (índice 100.12 al 27-oct; valor 5,006.01 MXN: 0.001325 BTC + 3,001.83 MXN) | −2.53% (26-oct; pico del 21-oct, 101.96); hoy −1.80% | 29 | `bitacora/real-binance/equity.csv`; saldo confirmado en `competencia/binance-real-2026-10-07.md` |
| chatgpt-gbm (real) | **+1.01%** sobre 10,000 (valor 10,101.11 al cierre del 27-oct con las posiciones **registradas**: 1 NVDA + 13 GFNORTE O + efectivo). Sin flujos | −1.63% (15-oct); hoy 0.00% (**máximo nuevo**), **del registro, no confirmado** | 17 | posiciones: `competencia/gbm-real-2026-10-07.md`; valuación: `competencia/valuacion-real-2026-10-27.md` |
| chatgpt-binance (real) | **−2.64%** sobre 5,000 (valor 4,867.87 al cierre del 27-oct; BTC + ETH + 502 MXN) | −6.10% (26-oct, contra el 21-oct); hoy −4.41% | 29 | posiciones: `competencia/binance-real-2026-10-07.md`; valuación: `competencia/valuacion-real-2026-10-27.md` |
| grok-binance (real) | **+0.17%** sobre 5,000 (valor 5,008.26 al cierre del 27-oct; BTC + 1.62 MXN + polvo de ETH) | −6.17% (26-oct; pico del 21-oct); hoy −4.41% | 29 | posiciones: `competencia/binance-real-2026-10-07.md`; valuación: `competencia/valuacion-real-2026-10-27.md` |
| grok-gbm (real) | **−0.11%** sobre 10,000 (valor 9,989.49 al cierre del 27-oct con las posiciones **registradas**: 3 VISTA A + 3 AMKR + 1 FSLR, 4% efectivo; **AMKR no aparece en la captura del 22-oct**). Sin flujos | −6.15% (26-oct); hoy −2.55%, **del registro, no confirmado** | 17 | posiciones: `competencia/gbm-real-2026-10-07.md`; valuación: `competencia/valuacion-real-2026-10-27.md` |
| grok-gbm papel / grok-binance | sin datos de cuenta real. Grok reportó **papel** al 25-sep (GBM 19,893.69; Binance 9,921.24): no entra al marcador real | sin datos | — | dueño (`rivales.csv`) |

## Tabla mensual

| Mes | arena-claude papel GBM | Benchmark 50% S&P TR MXN + 50% CETES | arena-claude papel Binance | arena-claude real GBM | arena-claude real Binance | ChatGPT | Grok |
|---|---|---|---|---|---|---|---|
| Sep-2026 (28-30 sep) | +0.83% con base al fondeo (antes +1.30% con base al cierre del 28-sep; DD −0.46%) | +0.31% con base 100 al fondeo (antes +0.64%, medido desde el cierre del 28-sep; nota del 9-oct) | +0.55% al 29-sep con base al fondeo (antes +0.12%; DD 0.00%) | sin fondear | −0.09% sobre la aportación (desde el 29-sep) | sin datos | sin datos (solo reportes de papel) |

Nota (conciliación, 8-oct): la columna de septiembre del papel se recalculó con la base al fondeo (fallo `bitacora/arbitraje/2026-10-08-base-twr.md`). El benchmark (`portafolio.py::benchmark`) ya incluía el primer día, así que ahora las dos series tienen la misma base. **[Corregido 9-oct-2026, conciliación, fallo `bitacora/arbitraje/2026-10-09-reporte-base-twr.md`]:** la última frase era falsa. La serie del benchmark (`serie_benchmark`) sí vale 100 antes del primer día (99.67 al 28-sep), pero el +0.64% se midió contra su primera fila, igual que el papel. Con base 100 queda en **+0.31%** al 30-sep: 100.3062, con Yahoo ^SP500TR, MXN=X y el proxy FRED de CETES consultados el 9-oct. `portafolio.py reporte` ya mide las dos series desde 100.

