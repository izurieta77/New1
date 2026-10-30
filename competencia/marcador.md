# Marcador de la competencia

> Métrica: TWR en MXN de la cuenta combinada (GBM + Binance), con GBM y Binance también por separado. **CETES 28:** con `BANXICO_TOKEN` en el entorno, `python3 herramientas/banxico.py` da la tasa oficial de subasta (SIE SF43936; al 24-sep-2026: 6.15% anual); sin token, se usa el proxy anotado y se dice que es proxy. Solo se registran datos que reporte el dueño en `competencia/rivales.csv`. No se atribuye habilidad solo por el saldo final. Temporada: 28-sep-2026 al 28-ene-2027.

Actualizado: **2026-10-30 (cierre)** para los cuatro libros de Claude (fila del 30-oct de cada `equity.csv`; sin órdenes nuevas en GBM; O0007 condicional en papel Binance) y para los cuatro rivales (posiciones **registradas**; precios en `competencia/valuacion-real-2026-10-30.md`). **Ojo:** la cuenta GBM compartida no cuadra; **Binance con retiros cerrados desde ≈21:50 UTC del 29-oct: los saldos de Binance son valuación a mercado con riesgo de contraparte abierto.** USD/MXN 18.7435.

**Meta del dueño para las tres IAs (25-sep-2026):** +40% mínimo, +60% bueno, +200% excepcional en la temporada. Cuando haya datos, se marca por cuenta si la alcanzó (`config/parametros.json` → `meta_temporada_dueno`).

| Cuenta | TWR | Drawdown máximo | Días invertidos | Fuente |
|---|---|---|---|---|
| arena-claude (papel, GBM) | **+0.56%** (índice 100.56 al 30-oct; valor 20,111.52 MXN: 5 SPYM + 1 QQQM + 1 UPRO + 3,799.05 de efectivo). Sin órdenes nuevas | −3.69% (**máximo nuevo**, 30-oct; pico del 9-oct) (siguiente nivel −12%) | 25 | `bitacora/equity.csv` |
| arena-claude-binance (papel) | **−1.25%** (índice 98.75 al 30-oct; valor 9,874.86 MXN: 0.002698 BTC a 76,694.14 + 5,996.44 MXN). O0007 condicional | −3.79% (**máximo nuevo**, 30-oct; pico del 21-oct) | 33 | `bitacora/papel-binance/equity.csv` |
| arena-claude (real, GBM) | **+0.42%** (índice 100.42 al 30-oct; valor 10,041.86 MXN: 3 SPYM + **efectivo 5,040.16 registrado; última confirmación del dueño el 7-oct; en duda desde la captura del 22-oct (la cuenta compartida no cuadra)**). VT: 0, conocido; boleta caducada | −1.17% (30-oct, máximo nuevo; pico del 29-oct) | 20 | `bitacora/real/equity.csv` |
| arena-claude-binance (real) | **−1.87%** (índice 98.13 al 30-oct; valor 4,906.54 MXN a mercado: 0.001325 BTC + 3,001.83 MXN; **retiros cerrados**) | −3.75% (**máximo nuevo**, 30-oct; pico del 21-oct) | 32 | `bitacora/real-binance/equity.csv`; saldo confirmado en `competencia/binance-real-2026-10-07.md` |
| chatgpt-gbm (real) | **−1.88%** sobre 10,000 (valor 9,812.40 al cierre del 30-oct con las posiciones **registradas**: 1 NVDA + 13 GFNORTE O + efectivo). Sin flujos | −2.86% (**máximo nuevo**, 30-oct; pico del 27-oct), **del registro, no confirmado** | 20 | posiciones: `competencia/gbm-real-2026-10-07.md`; valuación: `competencia/valuacion-real-2026-10-30.md` |
| chatgpt-binance (real) | **−6.82%** sobre 5,000 (valor 4,659.11 al cierre del 30-oct; BTC + ETH + 502 MXN; **retiros cerrados**) | −8.51% (**máximo nuevo**, 30-oct; pico del 21-oct) | 32 | posiciones: `competencia/binance-real-2026-10-07.md`; valuación: `competencia/valuacion-real-2026-10-30.md` |
| grok-binance (real) | **−4.80%** sobre 5,000 (valor 4,759.78 al cierre del 30-oct; BTC + 1.62 MXN + polvo de ETH; **retiros cerrados**) | −9.15% (**máximo nuevo**, 30-oct; pico del 21-oct) | 32 | posiciones: `competencia/binance-real-2026-10-07.md`; valuación: `competencia/valuacion-real-2026-10-30.md` |
| grok-gbm (real) | **−0.90%** sobre 10,000 (valor 9,910.46 al cierre del 30-oct con las posiciones **registradas**: 3 VISTA A + 3 AMKR + 1 FSLR, 4% efectivo; **AMKR no aparece en la captura del 22-oct**). Sin flujos | −6.15% (26-oct); hoy −3.32%, **del registro, no confirmado** | 20 | posiciones: `competencia/gbm-real-2026-10-07.md`; valuación: `competencia/valuacion-real-2026-10-30.md` |
| grok-gbm papel / grok-binance | sin datos de cuenta real. Grok reportó **papel** al 25-sep (GBM 19,893.69; Binance 9,921.24): no entra al marcador real | sin datos | — | dueño (`rivales.csv`) |

## Tabla mensual

| Mes | arena-claude papel GBM | Benchmark 50% S&P TR MXN + 50% CETES | arena-claude papel Binance | arena-claude real GBM | arena-claude real Binance | ChatGPT | Grok |
|---|---|---|---|---|---|---|---|
| Sep-2026 (28-30 sep) | +0.83% con base al fondeo (antes +1.30% con base al cierre del 28-sep; DD −0.46%) | +0.31% con base 100 al fondeo (antes +0.64%, medido desde el cierre del 28-sep; nota del 9-oct) | +0.55% al 29-sep con base al fondeo (antes +0.12%; DD 0.00%) | sin fondear | −0.09% sobre la aportación (desde el 29-sep) | sin datos | sin datos (solo reportes de papel) |

Nota (conciliación, 8-oct): la columna de septiembre del papel se recalculó con la base al fondeo (fallo `bitacora/arbitraje/2026-10-08-base-twr.md`). El benchmark (`portafolio.py::benchmark`) ya incluía el primer día, así que ahora las dos series tienen la misma base. **[Corregido 9-oct-2026, conciliación, fallo `bitacora/arbitraje/2026-10-09-reporte-base-twr.md`]:** la última frase era falsa. La serie del benchmark (`serie_benchmark`) sí vale 100 antes del primer día (99.67 al 28-sep), pero el +0.64% se midió contra su primera fila, igual que el papel. Con base 100 queda en **+0.31%** al 30-sep: 100.3062, con Yahoo ^SP500TR, MXN=X y el proxy FRED de CETES consultados el 9-oct. `portafolio.py reporte` ya mide las dos series desde 100.

