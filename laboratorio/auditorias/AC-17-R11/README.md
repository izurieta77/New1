# AC-17-R11: ejecución B independiente de la réplica R11 (banda de −3% en el filtro del 3x)

- **Fecha:** 2026-10-13
- **Ejecutor:** auditor de réplicas (ejecución B, desde cero)
- **Insumo leído:** solo el pre-registro de `laboratorio/replicas/R11-banda-filtro-upro.md` (secciones 1 a 9). No leí el código, la salida ni los resultados de A.
- **Reproducción:** `python3 -I laboratorio/auditorias/AC-17-R11/b.py` (solo biblioteca estándar; lee `datos/`). Escribe la salida en la consola, y la guardada está en `b-salida.txt`; también genera `b-resultados.json`.

## 1. Fuentes y huellas (sha256)

Datos descargados el 2026-10-13 y guardados en `datos/` sin modificar.

| Serie | Fuente B | Archivo | sha256 |
|---|---|---|---|
| S&P 500, precio de cierre diario desde 1975 (señal y parte de precio del rendimiento) | CBOE `SPX_History.csv` (cdn-api.cboe.com) | `SPX_History_cboe.csv` | `0176fca2c4bc3ea0eced6abedc746ea3602312ee772c8f661e902cfbc8d87e08` |
| S&P 500 (contraste del tramo 2016-10 a hoy) | FRED `SP500` | `SP500_fred.csv` | `59990d549a3fc4f67993a9d8600585cf4e611081ed032a1ea095ab4fa14abeed` |
| Rendimiento por dividendo mensual del S&P 500 (para aproximar el total return) | multpl.com, tabla mensual | `multpl_sp500_dividend_yield_by_month.html` | `947bf790269bd466fb8e2fae8cdb631acaa813b89458017064ebcfa13cab984b` |
| VIX, cierre diario desde 1990-01-02 | CBOE `VIX_History.csv` (historia oficial) | `VIX_History.csv` | `965f14ae8d58079536b5491219b647e6385592be2c466e6ac849f6ace0bbe1f7` |
| T-bill a 3 meses (rf y costo de financiamiento) | FRED `DTB3` | `DTB3.csv` | `5ea29eadd254056ad0529cc92cb50a160001c7be1ef8c01e8577d4d45a893adc` |
| UPRO real (solo para la sensibilidad 2009-07 a hoy) | Yahoo chart v8, `adjclose` | `UPRO_yahoo_chart.json` | `1faa26e53f08e9d17432e055e5eac2fa960eb1367bcaa7190645acc04020ee1b` |
| Datos mensuales de Shiller, **descargados pero no usados** (los dividendos terminan en 2023-06) | datahub, `datasets/s-and-p-500` | `shiller_datahub_sp500_monthly.csv` | `3a45dffabc414afc298c12159abc84c2875f88175ff3d4473ef7417e725ecac6` |

Intenté Stooq (`^spx`), pero el proxy respondió *connection reset* tanto por https como por http, así que lo sustituí por la historia de SPX de CBOE. Tampoco encontré una fuente de total return distinta de Yahoo `^SP500TR`: CBOE devuelve AccessDenied para SPXTR y SPTR. Por eso el total return es una **aproximación de precio más dividendos** (ver la sección 2). La rf sale de la misma serie que usa A (`DTB3`), porque no hay una alternativa diaria razonable. El precio de CBOE coincide con el de FRED en 2,511 de los 2,512 días del tramo común.

## 2. Decisiones de implementación (pueden explicar diferencias con A)

1. **Total return aproximado:** `r_TR(t) = P(t)/P(t−1) − 1 + yield_mes(t)/252`. El yield de multpl es el dividendo de 12 meses entre el precio del mes al que pertenece `t`. Así los dividendos quedan repartidos de manera uniforme y no caen en las fechas ex-dividendo, de modo que la serie se parecerá a `^SP500TR`, pero no será igual. Para medir cuánto pesa esta decisión, corrí el ejercicio sin dividendos: el CAGR cae unos 5 pp en todas las reglas, pero las diferencias entre reglas casi no se mueven (ver la sección 5).
2. **3x sintético:** `r3x = 3·r_TR − 2·rf_d − 0.0091/252`, con `rf_d = DTB3(último dato anterior a t)/100/252` por día hábil. La rf es simple, no compuesta, y va rezagada un día. Con la versión compuesta `(1+y)^(1/252)−1`, el Sharpe cambia menos de 0.01.
3. **Señal y ejecución:** la señal se calcula con el cierre de t y se ejecuta al cierre de t+1. Por lo tanto, el rendimiento del día t+2 (del cierre t+1 al cierre t+2) usa la posición decidida en t. El costo de 0.10% se cobra sobre el capital al cierre del día en que se ejecuta el cambio, después del rendimiento de ese día con la posición anterior. Fuera del mercado el capital rinde `rf_d`.
4. **Histéresis:** si se está dentro, se sale con `cierre < SMA200·(1−banda)` o con `VIX ≥ 25`. Si se está fuera, se entra con `cierre > SMA200` y `VIX < 25`. Entre las dos condiciones se mantiene el estado. Cada regla arranca **fuera** y entra el primer día que cumple la condición de entrada, pagando el costo.
5. **SMA200:** media simple de los últimos 200 cierres de CBOE SPX, que incluyen el día t. Como la serie empieza en 1975, la SMA ya existe el 1990-01-02.
6. **Panel y limpieza (§7):** se usan los días que tienen SPX, SMA200 y VIX desde 1990-01-02. Se descartan 3 días con SPX pero sin VIX (1991-03-01, 1997-01-31 y 1997-11-26). En esos casos el rendimiento se mide de un cierre retenido al siguiente, así que no se pierde ningún rendimiento. Se ignoran 34 días con VIX pero sin SPX (feriados en que CBOE publicó VIX). Se corrigió un solo cierre de CBOE con FRED: 2019-02-28, de 2792.38 a 2784.49. El panel va de 1990-01-02 a 2026-10-12: tiene 9,258 días y 9,256 rendimientos, el primero del 1990-01-04.
7. **Comprar y mantener:** compra al cierre del 1990-01-03, el mismo día del primer rendimiento de las reglas, y paga un costo de entrada.
8. **Métricas:** el CAGR usa años calendario (días/365.25). La volatilidad es la desviación estándar diaria del rendimiento total por √252. El Sharpe es la media sobre la desviación estándar del exceso diario sobre `rf_d`, por √252. La MDD se mide sobre la curva diaria de capital. Las salidas son las transiciones dentro→fuera **ejecutadas** dentro del periodo. El tiempo invertido es la fracción de días con posición en el 3x.
9. **Subperiodos:** el estado de la señal no se reinicia; los subperiodos son cortes de la misma corrida completa. Van del 1990-01-04 al 2008-12-31 y del 2009-07-01 al 2026-10-12. El primer semestre de 2009 solo cuenta en el periodo completo y no tuvo salidas: 51 + 61 = 112.
10. **UPRO real:** se usa `adjclose` de Yahoo, ajustado por splits y distribuciones, con las mismas señales, y solo para 2009-07 a hoy. El último bar de Yahoo era del 2026-10-13 e intradía; quedó fuera porque el panel termina el 2026-10-12.

## 3. Resultados (netos de costos)

Abreviaturas: `sal` = salidas ejecutadas; `inv` = tiempo invertido.

### Periodo completo (1990-01-04 a 2026-10-12)

| Configuración | CAGR | Vol | Sharpe | MDD | sal | inv |
|---|---:|---:|---:|---:|---:|---:|
| **Banda −3% + VIX (principal)** | 13.77% | 32.6% | 0.48 | −73.5% | 112 | 74.2% |
| Sin banda + VIX (comparación) | 11.93% | 31.2% | 0.43 | −75.1% | 177 | 70.7% |
| Banda −3%, sin VIX (variante) | 19.25% | 36.8% | 0.59 | −58.4% | 35 | 80.1% |
| Banda −5% + VIX (variante) | 12.98% | 33.2% | 0.45 | −79.4% | 107 | 75.7% |
| Comprar y mantener 3x | 15.98% | 53.9% | 0.50 | −97.9% | 0 | 100% |
| Referencia: 1x TR aproximado | 10.88% | 18.0% | 0.51 | −55.3% | 0 | 100% |

Sharpe con más precisión: principal 0.477 y sin banda 0.431, una diferencia de **+0.045**.

Caídas máximas (de pico a valle):

- Principal y sin banda: del 1998-07-17 al 2003-04-16.
- Banda −5%: del 1998-07-17 al 2002-04-29.
- Solo SMA: del 1998-07-17 al 1998-10-27.
- Comprar y mantener 3x: del 2000-03-23 al 2009-03-09.

### 1990-2008 (3x sintético)

| Configuración | CAGR | Vol | Sharpe | MDD | sal | inv |
|---|---:|---:|---:|---:|---:|---:|
| **Banda −3% + VIX** | 10.75% | 32.0% | 0.36 | −73.5% | 51 | 70.4% |
| Sin banda + VIX | 7.55% | 30.4% | 0.26 | −75.1% | 95 | 65.5% |
| Banda −3%, sin VIX | 14.46% | 35.8% | 0.45 | −58.4% | 16 | 76.1% |
| Banda −5% + VIX | 11.69% | 32.5% | 0.38 | −79.4% | 47 | 72.9% |
| Comprar y mantener 3x | 2.16% | 54.1% | 0.24 | −96.7% | 0 | 100% |
| 1x TR aproximado | 7.19% | 18.0% | 0.26 | −50.7% | 0 | 100% |

Diferencia de Sharpe entre la regla con banda y la regla sin banda: **+0.094**.

### 2009-07 a 2026-10-12 (3x sintético)

| Configuración | CAGR | Vol | Sharpe | MDD | sal | inv |
|---|---:|---:|---:|---:|---:|---:|
| **Banda −3% + VIX** | 17.61% | 33.7% | 0.61 | −49.3% | 61 | 80.5% |
| Sin banda + VIX | 17.32% | 32.4% | 0.61 | −54.0% | 82 | 78.5% |
| Banda −3%, sin VIX | 26.00% | 38.3% | 0.76 | −55.0% | 19 | 86.4% |
| Banda −5% + VIX | 14.82% | 34.4% | 0.53 | −54.6% | 60 | 80.9% |
| Comprar y mantener 3x | 34.57% | 51.4% | 0.81 | −76.6% | 0 | 100% |
| 1x TR aproximado | 15.21% | 17.1% | 0.83 | −33.8% | 0 | 100% |

Diferencia de Sharpe entre la regla con banda y la regla sin banda: **−0.0028**.

### Sensibilidad: UPRO real (Yahoo `adjclose`), 2009-07 a 2026-10-12

| Configuración | CAGR | Vol | Sharpe | MDD | sal | inv |
|---|---:|---:|---:|---:|---:|---:|
| Banda −3% + VIX | 16.41% | 33.4% | 0.58 | −49.7% | 61 | 80.5% |
| Sin banda + VIX | 16.05% | 32.1% | 0.58 | −54.2% | 82 | 78.5% |
| Banda −3%, sin VIX | 24.93% | 38.0% | 0.74 | −55.3% | 19 | 86.4% |
| Banda −5% + VIX | 13.72% | 34.0% | 0.51 | −54.6% | 60 | 80.9% |
| Comprar y mantener UPRO | 32.99% | 51.0% | 0.79 | −76.8% | 0 | 100% |

Diferencia de Sharpe entre la regla con banda y la regla sin banda: **+0.0004**.

En 4,347 días comunes, el sintético rindió 34.65% anual y UPRO real 33.06%: el sintético rinde unos 1.6 pp por año más. Es lo esperable, porque el sintético omite el costo del swap por encima de la T-bill, los costos de rebalanceo y el error de seguimiento.

## 4. Criterio de refutación (§2)

Comparación de la regla con banda contra la regla sin banda (ambas con VIX) en el periodo completo:

| Prueba | Valor | ¿Refuta? |
|---|---|---|
| ¿La banda reduce las salidas? | 112 contra 177 (−37%) | No |
| ¿Empeora la MDD en más de 5 pp? | −73.5% contra −75.1%: mejora 1.6 pp | No |
| ¿Baja el Sharpe en más de 0.05? | 0.477 contra 0.431: sube 0.045 | No |
| ¿Se invierte el signo del efecto en Sharpe en algún subperiodo? | 1990-2008: +0.094. 2009-07 a hoy: **−0.003** con el sintético y +0.0004 con UPRO real | Sí con el sintético; no con UPRO real |

**Estado B: Replicado con diferencias.**

- **La hipótesis no se refuta.** En el periodo completo, la banda reduce las salidas en 37%, no empeora la MDD (incluso la mejora 1.6 pp) y no baja el Sharpe (sube 0.045).
- **El beneficio en Sharpe está concentrado en 1990-2008.** En 2009-07 a hoy el efecto es nulo: −0.003 con el sintético y +0.0004 con UPRO real. Ese signo no es robusto.
- **Por qué aplico la regla de "con diferencias" pese al empate.** El §2 pide "UPRO real si la fuente lo permite" para 2009-07 a hoy, y con UPRO real el signo no se invierte, lo que daría "Replicado". La instrucción de esta auditoría pide usar UPRO solo como sensibilidad. Opto por el veredicto conservador, aunque la diferencia sea prácticamente cero.
- **En 2009-07 a hoy la banda sí aporta algo:** menos salidas (61 contra 82) y una MDD menor (−49.3% contra −54.0%), con igual Sharpe.

## 5. Robustez a las decisiones de datos

| Sensibilidad | Sharpe completo con banda / sin banda | Diferencia en 1990-2008 | Diferencia en 2009-07 a hoy | Estado |
|---|---|---|---|---|
| Base (precio CBOE + dividendo multpl) | 0.477 / 0.431 | +0.094 | −0.0028 | Con diferencias |
| Solo precio, sin dividendos | 0.34 / 0.30 | +0.091 | −0.0015 | Con diferencias |
| rf compuesta | 0.48 / 0.44 | +0.094 | −0.0028 | Con diferencias |

Las salidas no cambian (112 contra 177) porque la señal no depende del rendimiento.

## 6. Hallazgos laterales (no forman parte del criterio)

- **Quitar el VIX domina a todas las demás configuraciones:** Sharpe 0.59, CAGR 19.3%, MDD −58.4% y solo 35 salidas. En este diseño, la condición de VIX ≥ 25 genera la mayor parte de las salidas, el tiempo fuera y el costo. La regla vigente del comité la incluye, así que conviene revisarla con un pre-registro propio.
- **La banda de −5% (con VIX) es peor que la de −3%:** MDD −79.4% contra −73.5%, y su Sharpe (0.45) apenas supera al de la regla sin banda (0.43). Es decir, no es cierto que más banda sea mejor.
- **Ninguna regla con VIX evita una caída de alrededor de −73% en 1998-2003.** El filtro no protegió frente a las entradas y salidas repetidas durante la burbuja y su caída. Comprar y mantener el 3x llegó a −97.9%.
- **Sesgo declarado:** el S&P 500 es un índice de sobrevivientes. Además, el sintético anterior a 2009 supone que existía un 3x con financiamiento a la T-bill.

## 7. Qué revisar al comparar con A

- **Nivel del CAGR:** A usa `^SP500TR`, con dividendos en sus fechas ex reales, y B usa el yield mensual repartido uniformemente. Espero diferencias de CAGR de unas décimas de pp, amplificadas por el 3x. Las diferencias entre reglas deberían coincidir mucho mejor que los niveles.
- **Alineación:** en B, la señal de t determina el rendimiento de t+2 y el costo se cobra el día t+1. Si A cobra el costo de otra forma, o si usa el rendimiento de t+1 en lugar del de t+2, habrá diferencias.
- **Arranque y SMA:** si A calcula la SMA200 solo con datos de Yahoo desde 1989, o si arranca en otra fecha, cambian los primeros días y la primera entrada.
- **Conteo de salidas:** B cuenta solo las salidas dentro→fuera **ejecutadas**. Si A cuenta señales o cuenta también las entradas, sus números serán distintos.
- **Datos:** la corrección del 2019-02-28 y los 3 días descartados por falta de VIX.
- **Veredicto en el filo:** el resultado depende del signo de una diferencia de Sharpe prácticamente nula en 2009-07 a hoy. Si A usó UPRO real en ese subperiodo, es posible que obtenga "Replicado". Ambas lecturas coinciden en lo sustantivo.
