# AC-16-R10: ejecución B (independiente, segunda fuente) del filtro SMA200 ±3% sobre BTC

- Fecha: 2026-10-12. Auditor: `auditor-de-replicas` (ejecución B).
- Pre-registro respetado: `laboratorio/replicas/R10-filtro-sma200-btc.md`, secciones 1 a 9. No se leyó código ni resultados de la ejecución A.
- Código: `b.py` (solo biblioteca estándar). Reproducción: `python3 -I laboratorio/auditorias/AC-16-R10/b.py`. Salida: `salida_b.txt` y `resultados_b.json`.

## Fuente y huellas

| Archivo | Fuente | sha256 |
|---|---|---|
| `datos/yahoo_BTC-USD_1d.json` | Yahoo Finance chart v8, `query2.finance.yahoo.com/v8/finance/chart/BTC-USD?interval=1d&period1=1410912000&period2=1791763200&includeAdjustedClose=true`, User-Agent de navegador, descargado el 2026-10-12 17:50 UTC | `f47a8ef862642bb9947a3a0ea99ecb2926cfd519cf4ff9bf048443c0f02445a8` |

- `range=max` devuelve barras **mensuales** aunque se pida `interval=1d`, por eso se pidió el rango explícito con `period1` y `period2`. `query1` respondió 429 en el primer intento.
- 4,409 barras diarias, del 2014-09-17 al 2026-10-12. La barra del 2026-10-12 está incompleta (intradía) y se descarta. Quedan 4,408 cierres hasta el **2026-10-11**.
- Nulos: 0. Días faltantes en el calendario: **0** (no hubo que descartar nada, §7).
- Las barras de Yahoo son días UTC (00:00 a 23:59:59). El cierre del día t equivale al de la vela Binance con apertura t, que cierra a las 00:00 UTC de t+1.
- De Binance solo se consultaron las **fechas** de las primeras 210 velas BTCUSDT 1d, para fijar el inicio común. No se usó ningún precio de Binance. La primera vela es la del 2017-08-17 y no hay huecos, así que el cierre 200 es el del **2018-03-04**.

## Decisiones de implementación (pueden explicar diferencias con A)

1. **SMA**: media simple de los N cierres que terminan en t, incluido el de t.
2. **Primer día**: el día de la primera señal válida (`i0`) la cartera está en efectivo. Se entra solo con una señal de **entrada**: cierre > SMA × 1.03. No se entra por estar "dentro de la banda". Con ejecución t+1, la primera compra posible ocurre al cierre de `i0+1`.
3. **Histéresis**: invertido y cierre < SMA × (1 − b) → salir. Fuera y cierre > SMA × (1 + b) → entrar. Las desigualdades son estrictas y la banda no se redondea (0.97 y 1.03 exactos). Sin banda, b = 0.
4. **Ejecución t+1**: la orden decidida con el cierre de t se ejecuta al cierre de t+1. El rendimiento del día t+1 lo recibe la posición anterior. En la variante "mismo día", la orden se ejecuta al cierre de t.
5. **Costos**: 0.15% por lado, que multiplica la equidad en cada compra o venta. El efectivo rinde 0. No se liquida la posición al final (se valúa a mercado). Comprar y mantener paga una compra de 0.15% el día de inicio.
6. **Periodo completo (a)**: todas las configuraciones, incluida SMA100, arrancan en efectivo el día de la primera señal válida de **SMA200** en Yahoo (2015-04-04), igual que comprar y mantener. Así todas cubren el mismo periodo.
7. **Periodo común (b)**: se reinicia la simulación en efectivo el 2018-03-04. La SMA usa la historia de Yahoo, pero los 200 cierres que terminan ese día son exactamente las mismas fechas que tiene Binance, así que la señal del primer día es comparable. La primera compra se ejecuta el 2018-03-05 a 11,573.
8. **Subperiodos**: son cortes de la corrida continua, no reinicios. El valor inicial es la equidad al cierre del último día anterior al corte. Se reportan los del pre-registro (2017-2020 y 2021-hoy, sobre la corrida completa) y los pedidos para el periodo común (2018-03-04 a 2020 y 2021-hoy).
9. **Métricas**:
   - CAGR con días calendario / 365.
   - Volatilidad: desviación estándar muestral diaria × √365.
   - Sharpe: media diaria × 365 / volatilidad (rf = 0).
   - MDD sobre la equidad diaria, incluido el valor inicial.
   - "Viajes" = ventas ejecutadas en la ventana.
   - Salida en falso: una venta seguida de la siguiente compra en ≤ 30 días calendario y a un precio de ejecución mayor. El porcentaje es sobre las ventas.

## Resultados (netos de 0.15% por lado, USD)

### (b) Periodo común con Binance: 2018-03-04 a 2026-10-11

| Configuración | CAGR | Vol | Sharpe | MDD | Viajes | Salidas en falso |
|---|---:|---:|---:|---:|---:|---:|
| Comprar y mantener | 25.9% | 61.5% | 0.69 | -76.6% | - | - |
| **Principal SMA200 ±3%, t+1** | **29.5%** | **42.7%** | **0.82** | **-50.8%** | **13** | **4/13 (31%)** |
| Sin banda SMA200, t+1 | 27.8% | 42.8% | 0.79 | -55.3% | 32 | 21/32 (66%) |
| SMA200 ±5%, t+1 | 32.5% | 42.9% | 0.87 | -51.9% | 11 | 2/11 (18%) |
| SMA100 ±3%, t+1 | 46.7% | 42.2% | 1.12 | -38.8% | 20 | 7/20 (35%) |
| SMA200 ±3%, mismo día t | 31.8% | 42.5% | 0.86 | -52.1% | 13 | 4/13 (31%) |

Subperiodo 2018-03-04 a 2020-12-31:

| Configuración | CAGR | Vol | Sharpe | MDD | Viajes | Falsas |
|---|---:|---:|---:|---:|---:|---:|
| Comprar y mantener | 38.6% | 69.9% | 0.83 | -72.0% | - | - |
| Principal | 49.2% | 45.3% | 1.11 | -50.8% | 4 | 1/4 (25%) |
| Sin banda | 50.0% | 45.1% | 1.12 | -51.8% | 6 | 2/6 (33%) |
| Banda ±5% | 50.9% | 45.4% | 1.13 | -49.7% | 4 | 1/4 (25%) |
| SMA100 ±3% | 76.2% | 45.9% | 1.46 | -38.8% | 7 | 2/7 (29%) |
| Mismo día | 50.9% | 45.3% | 1.13 | -50.2% | 4 | 1/4 (25%) |

Subperiodo 2021-01-01 a 2026-10-11 (es el mismo en (a) y en (b)):

| Configuración | CAGR | Vol | Sharpe | MDD | Viajes | Falsas |
|---|---:|---:|---:|---:|---:|---:|
| Comprar y mantener | 20.1% | 56.9% | 0.61 | -76.6% | - | - |
| Principal | 20.8% | 41.4% | 0.66 | -46.9% | 9 | 3/9 (33%) |
| Sin banda | 18.1% | 41.6% | 0.61 | -55.3% | 26 | 19/26 (73%) |
| Banda ±5% | 24.3% | 41.7% | 0.73 | -51.9% | 7 | 1/7 (14%) |
| SMA100 ±3% | 34.1% | 40.3% | 0.93 | -35.1% | 13 | 5/13 (38%) |
| Mismo día | 23.3% | 41.1% | 0.71 | -52.1% | 9 | 3/9 (33%) |

### (a) Periodo completo Yahoo: 2015-04-04 (primera señal SMA200) a 2026-10-11

| Configuración | CAGR | Vol | Sharpe | MDD | Viajes | Salidas en falso |
|---|---:|---:|---:|---:|---:|---:|
| Comprar y mantener | 65.4% | 65.2% | 1.10 | -83.4% | - | - |
| **Principal SMA200 ±3%, t+1** | **64.9%** | **52.4%** | **1.22** | **-64.3%** | **15** | **5/15 (33%)** |
| Sin banda SMA200, t+1 | 64.0% | 52.4% | 1.21 | -64.3% | 37 | 24/37 (65%) |
| SMA200 ±5%, t+1 | 66.8% | 52.5% | 1.24 | -64.3% | 13 | 3/13 (23%) |
| SMA100 ±3%, t+1 | 76.0% | 50.8% | 1.37 | -63.6% | 26 | 10/26 (38%) |
| SMA200 ±3%, mismo día t | 64.4% | 52.1% | 1.21 | -66.9% | 15 | 5/15 (33%) |

Subperiodo del pre-registro 2017-01-01 a 2020-12-31 (corrida completa):

| Configuración | CAGR | Vol | Sharpe | MDD | Viajes | Falsas |
|---|---:|---:|---:|---:|---:|---:|
| Comprar y mantener | 134.1% | 80.1% | 1.47 | -83.4% | - | - |
| Principal | 140.3% | 66.3% | 1.65 | -64.3% | 5 | 2/5 (40%) |
| Sin banda | 142.6% | 66.2% | 1.67 | -64.3% | 8 | 3/8 (38%) |
| Banda ±5% | 142.3% | 66.3% | 1.67 | -64.3% | 5 | 2/5 (40%) |
| SMA100 ±3% | 161.3% | 63.9% | 1.82 | -63.6% | 10 | 4/10 (40%) |
| Mismo día | 134.6% | 66.1% | 1.62 | -66.9% | 5 | 2/5 (40%) |

El tramo 2015-04 a 2016, que no estaba en el pre-registro y se reporta solo como información, va en contra de la regla. Comprar y mantener tuvo Sharpe 1.75 y la regla principal 1.62, con el mismo MDD (-32%). Ver `salida_b.txt`.

## Criterio de refutación (§2): regla principal contra comprar y mantener

| Ventana | Mejora de MDD (pp) | Dif. CAGR (pp) | Dif. Sharpe | ¿Refuta? |
|---|---:|---:|---:|---|
| Común con Binance, 2018-03-04 a 2026-10-11 | **25.9** | +3.6 | +0.13 | No, por un margen de 0.9 pp |
| Completo Yahoo, 2015-04-04 a 2026-10-11 | **19.1** | -0.5 | +0.12 | **Sí** (MDD < 25 pp) |
| 2017-2020 (completo) | 19.1 | +6.3 | +0.19 | MDD < 25 pp; el Sharpe mejora |
| 2018-03 a 2020 (común) | 21.3 | +10.6 | +0.28 | MDD < 25 pp; el Sharpe mejora |
| 2021-hoy | 29.8 | +0.7 | +0.06 | No |

- **Signo del Sharpe**: la mejora es positiva en los dos subperiodos del pre-registro, tanto en la corrida completa como en la común. No se invierte en ninguno.
- **CAGR**: la regla nunca queda más de 15 pp por debajo de comprar y mantener. Esa parte de la hipótesis se cumple en todas las ventanas.
- **Sensibilidad del inicio común**: se movió el inicio entre el 2018-03-01 y el 2018-04-01. La mejora de MDD sigue en 25.9 pp, porque el MDD de comprar y mantener es el de nov-2021 a nov-2022 (-76.6%) y el de la regla va del 2019-06-26 al 2020-05-11 (-50.8%). El Sharpe de la regla queda entre 0.82 y 0.92 y el de comprar y mantener entre 0.68 y 0.79. Si la simulación corre de forma continua desde 2015 y no se reinicia, el resultado en el periodo común es el mismo: -50.8%, 0.82 y 29.6%.
- **Por qué falla en el periodo largo**: en la caída de 2017-2018, la regla estaba invertida en el pico de diciembre de 2017. Vendió el 2018-02-06 a 7,754, recompró el 2018-02-10 a 8,622 (una salida en falso) y volvió a vender el 2018-03-15 a 8,300. Su MDD fue -64.3%, contra -83.4% de comprar y mantener: solo 19.1 pp de mejora. Ese tramo queda fuera de la ventana de Binance, porque BTCUSDT empieza en agosto de 2017 y no tiene 200 cierres hasta marzo de 2018.

## Afirmación del gestor de riesgo (salidas en falso de 36-51% sin banda y 16-31% con banda)

- Con la ventana a 30 días, B obtiene 66% sin banda y 31% con ±3% en el periodo común. En el completo, 65% y 33%. Por subperiodo, sin banda va de 33% a 73% y con ±3% de 25% a 40%.
- La banda sí reduce mucho las salidas en falso, y también los viajes: de 32 a 13 en el periodo común.
- El nivel con banda (31-33%) está en el extremo alto del rango del gestor o por encima.
- El nivel sin banda (65-66%) es mayor que el 36-51% declarado.
- No hay código del gestor, así que no se puede saber si definió "salida en falso" igual.

## Veredicto de B

**Replicado con diferencias.**

- En el periodo comparable con la serie de la regla (Binance, desde marzo de 2018), con una segunda fuente y código independiente, la hipótesis **no se refuta**. La regla mejora el MDD en 25.9 pp, gana 3.6 pp de CAGR y 0.13 de Sharpe, y la mejora de Sharpe tiene el mismo signo en los dos subperiodos.
- El margen en MDD es de solo 0.9 pp sobre el umbral de 25 pp. Diferencias de nivel entre fuentes (Yahoo agregado contra Binance BTCUSDT) del orden de 1-2% en un cierre clave podrían cambiar el resultado.
- En la historia más larga disponible (2015-2026), el criterio del pre-registro **sí refuta** la hipótesis por el MDD (19.1 pp de mejora). Lo mismo pasa en 2017-2020 y en 2018-2020: la caída de 2018 no se evita lo suficiente.
- Lo robusto es que la regla reduce la volatilidad unos 20 pp, mejora el Sharpe 0.06-0.28 en casi todas las ventanas y no cuesta CAGR de forma relevante.
- La afirmación "reduce la caída máxima por al menos 25 pp" depende de la muestra y está en el límite.
- Con datos de Yahoo, la variante SMA100 ±3% domina a la regla vigente en todas las ventanas desde 2017. Es una de 5 configuraciones probadas (N = 5), así que no es evidencia para cambiar la regla sin una corrección por pruebas múltiples.

No se editó ningún otro archivo del repositorio ni se hizo commit.
