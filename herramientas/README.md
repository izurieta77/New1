# herramientas: kit cuantitativo (Python 3.11, solo biblioteca estándar)

Sin numpy/pandas y sin pip. Todos los límites de riesgo se leen de `config/parametros.json`. Ningún módulo define límites propios, y si falta una clave se lanza `KeyError`.

| Módulo | Qué hace |
|---|---|
| `parametros.py` | Carga `config/parametros.json` desde cualquier directorio (`cargar_parametros`, `obtener("kelly.fraccion_max")`). |
| `datos.py` | `fred_serie`, `yahoo_serie`, `yahoo_grafica`, `yahoo_ultimo`, `coingecko_precio`. Reintentos exponenciales, timeout y caché opcional en `datos/cache/` (excluida de git). |
| `metricas.py` | Rendimientos, CAGR, volatilidad, Sharpe, Sortino, max drawdown (pico/valle/recuperación), Calmar, hit rate, profit factor, expectancy, PSR, DSR, Brier, log score, calibración y rachas perdedoras exactas. |
| `riesgo.py` | Sizing por stop y por volatilidad objetivo, Kelly fraccional topado, cortacircuitos por drawdown, factor por rachas y `validar_orden`. |
| `tablero.py` | CLI: tablero markdown de mercado y régimen. |
| `pronosticos.py` | CLI: bitácora de pronósticos con puntuación Brier, log score y calibración. |
| `portafolio.py` | CLI: libro en papel, valuación, curva de equity y reporte vs benchmark. |

Pruebas (desde la raíz del repo): `python3 -m unittest discover -s herramientas/tests -t .`

Las CLIs funcionan desde cualquier directorio (`python3 /ruta/herramientas/tablero.py`) y también como módulo (`python3 -m herramientas.tablero`).

## Fuentes de datos (comprobadas el 2026-09-25)

- **FRED** (`fredgraph.csv?id=...&cosd=AAAA-MM-DD`): no requiere llave. **Solo responde con el User-Agent por defecto de urllib.** Con "Mozilla/5.0" corta la conexión. Los faltantes vienen como celda vacía o ".", y se ignoran. Por licencia de ICE, el spread HY (`BAMLH0A0HYM2`) solo trae unos 3 años.
- **Yahoo** (`/v8/finance/chart/TICKER`): **exige** User-Agent "Mozilla/5.0". Usa el cierre ajustado si existe. Las fechas se calculan en la hora local de la bolsa (`gmtoffset`).
- **CoinGecko** `simple/price`: sin llave.
- Stooq está bloqueado y Banxico SIE requiere token, así que no se usan. Como proxy de CETES 28d se usa FRED `INTGSTMXM193N` (T-bills México, FMI, mensual, con rezago de unos 2 meses).

## tablero.py

```
python3 herramientas/tablero.py --salida bitacora/briefs/AAAA-MM-DD-tablero.md [--cache-horas 2] [--hilos 6]
```

Series: 13 de FRED (SP500, NASDAQCOM, DGS10, DGS2, T10Y2Y, T10Y3M, DFF, DFII10, T5YIE, VIXCLS, BAMLH0A0HYM2, DEXMXUS, DCOILWTICO) y 8 de Yahoo (^GSPC, ^MXX, MXN=X, GC=F, BTC-USD, SPY, EWW, TLT). Para cada una muestra:

- último valor y fecha, marcada como "rezago" si tiene más de 5 días;
- cambio a 7, 30 y 91 días calendario (% en precios, pb en tasas, puntos en VIX);
- distancia a la SMA de 200 observaciones (solo precios);
- percentil del último valor en 5 años, o en la ventana disponible, que se indica.

Si una fuente falla, aparece en "Fuentes con error" y el tablero sigue.

Reglas de régimen (constantes al inicio de `tablero.py`):

| Dimensión | Regla | Señal |
|---|---|---|
| Tendencia | S&P 500 (FRED SP500; si falla, ^GSPC) > SMA200 | alcista +1 / bajista −1 |
| Volatilidad | VIX < 15 calma / 15-25 normal / > 25 estrés | +1 / 0 / −1 |
| Crédito | OAS HY ÷ mediana de 1 año: ≤ 1.10 benigno / ≤ 1.25 vigilancia / > 1.25 estrés | +1 / 0 / −1 |
| Curva | 10a-2a y 10a-3m: alguna < 0 = invertida; ambas ≥ 0 pero alguna < 0 en los últimos 12m = des-invertida; ambas > 0.5 pp = positiva; resto = plana | −1 / 0 / +1 / 0 |
| Dólar-peso | USD/MXN (MXN=X; si falla, DEXMXUS): +5% en 1m = depreciación rápida; < SMA200 = peso fuerte; > SMA200 = peso débil | −1 / +1 / −1 |

Diagnóstico: RISK-ON si la suma es ≥ +2, RISK-OFF si es ≤ −2, y MIXTO en otro caso. Es una descripción del estado actual, no un pronóstico.

## pronosticos.py

Archivo por defecto: `bitacora/pronosticos.csv`, con columnas `id, fecha_creacion, autor, pregunta, probabilidad, fecha_resolucion, criterio_resolucion, resultado, fecha_resuelto, notas`. Se crea con encabezado si no existe.

```
python3 herramientas/pronosticos.py agregar --pregunta "SPY > 800 el 2026-12-31?" --probabilidad 0.35 \
    --fecha-resolucion 2026-12-31 --criterio "Cierre ajustado Yahoo SPY 2026-12-31 > 800" [--autor claude] [--notas ".."]
python3 herramientas/pronosticos.py resolver P0001 --resultado si|no|1|0|anulada [--fecha AAAA-MM-DD] [--notas ".."]
python3 herramientas/pronosticos.py pendientes
python3 herramientas/pronosticos.py vencidos [--hoy AAAA-MM-DD]      # abiertos con fecha_resolucion <= hoy
python3 herramientas/pronosticos.py puntuar [--autor claude]
# opción global: --archivo RUTA
```

- La probabilidad acepta `0.65` o `65%`. Los ids se asignan solos (`P0001`, `P0002`...).
- `puntuar` reporta por grupo y por autor: n, Brier, skill vs 50% (1 − Brier/0.25), skill vs tasa base, log score (media de ln p; 0 es perfecto y −0.693 equivale a una moneda) y calibración por deciles.
- El veredicto se da contra `pronosticos.brier_objetivo` y `min_pronosticos_para_evaluar`. Los pronósticos anulados no cuentan.

## portafolio.py

Archivos por defecto: `bitacora/operaciones.csv` (`fecha, ticker, lado, cantidad, precio, moneda, comision, stop, tesis_id, estrategia, notas`) y `bitacora/equity.csv`.

```
python3 herramientas/portafolio.py registrar --fecha 2026-09-25 --lado deposito --cantidad 1000000
python3 herramientas/portafolio.py registrar --fecha 2026-09-25 --ticker SPY --lado compra --cantidad 40 \
    --precio 767.18 --moneda USD --comision 1 --stop 700 --estrategia nucleo --clase etf [--tesis-id T001] [--fase 1] [--forzar]
python3 herramientas/portafolio.py posiciones                 # a costo, sin red salvo tipo de cambio histórico
python3 herramientas/portafolio.py valuar [--reconstruir] [--sin-guardar] [--fecha AAAA-MM-DD]
python3 herramientas/portafolio.py reporte [--tasa-cetes 0.07] [--salida bitacora/briefs/AAAA-MM-DD-portafolio.md]
# opciones globales: --operaciones RUTA --equity RUTA
```

- `lado`: compra, venta, deposito o retiro. Los depósitos y retiros usan el ticker EFECTIVO y precio 1. Las monedas válidas son MXN y USD.
- El efectivo se lleva en una sola cuenta en MXN. Las operaciones en USD se convierten con el cierre de MXN=X en o antes de la fecha de la operación.
- Costo promedio ponderado con comisiones incluidas. No se admiten ventas en corto.
- **Validación previa:** cada compra o venta pasa por `riesgo.validar_orden` con el libro valuado a costo. Revisa apalancamiento bruto por fase, satélite, riesgo al stop y límites por clase. Si hay violaciones, la operación no se registra (código 2). Con `--forzar` se registra y las violaciones quedan en `notas` como "FORZADA: ...". Se considera táctica toda estrategia distinta de "" y "nucleo".
- `valuar` toma precios de Yahoo (la moneda sale de la metadata de Yahoo) y convierte USD con el MXN=X actual. Guarda la foto del día en `equity.csv`. Con `--reconstruir`, rehace la curva diaria desde la primera operación.
- `equity.csv` incluye `indice`: un índice time-weighted base 100 que no se mueve por depósitos ni retiros. Métricas y cortacircuitos se calculan sobre este índice.
- `reporte` compara contra el benchmark principal: 50% S&P 500 TR (Yahoo ^SP500TR × MXN=X) + 50% CETES. CETES devenga tasa × días/360, con el proxy FRED o `--tasa-cetes`, y se rebalancea a diario. El reporte incluye:
  - rendimiento, CAGR (solo con ≥ 1 año), volatilidad, Sharpe, Sortino (≥ 20 rendimientos), max drawdown, Calmar, tracking error e IR;
  - estado de cortacircuitos;
  - hit rate, profit factor y expectancy de las operaciones cerradas;
  - factor por rachas de cada estrategia;
  - avance contra los mínimos de paper trading.

## Uso como librería

```python
from herramientas import metricas, riesgo, datos
spy = datos.yahoo_serie("SPY", "5y")
r = metricas.rendimientos(spy)
metricas.sharpe(r, rf=0.07); metricas.max_drawdown(spy)
metricas.sharpe_probabilistico(r, sr_referencia_anual=0.5)
metricas.sharpe_deflactado(r, n_pruebas=40, varianza_sharpes=0.25, varianza_anualizada=True)  # meta >= 0.95
metricas.prob_racha_perdedora(n=100, k=6, p_ganar=0.55)
riesgo.tamano_por_stop(1_000_000, entrada=767.18, stop=740, tipo_cambio=17.7)
riesgo.estado_cortacircuitos(curva_equity); riesgo.factor_por_rachas(resultados_estrategia)
```

Referencias de fórmulas, verificadas:

- **PSR:** Bailey y López de Prado (2012), "The Sharpe Ratio Efficient Frontier", *Journal of Risk* 15(2). PSR = Φ[(SR−SR*)·√(n−1) / √(1 − γ3·SR + (γ4−1)/4·SR²)], con γ4 = curtosis cruda (3 en la normal).
- **DSR:** Bailey y López de Prado (2014), "The Deflated Sharpe Ratio", *Journal of Portfolio Management* 40(5). SR0 = √V · [(1−γ)·Φ⁻¹(1−1/N) + γ·Φ⁻¹(1−1/(N·e))], con γ = Euler-Mascheroni. Las pruebas reproducen el ejemplo del paper (DSR ≈ 0.8997, según la réplica de marti.ai, 2018).
