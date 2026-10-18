# AC-21-R12: ejecución B independiente de R12 (condición VIX ≥ 25 en el filtro del 3x, Nasdaq-100)

> Fase 0: formación. No recomienda inversiones. La auditoría se hizo el 2026-10-18. Solo leí el pre-registro de R12 (§1-9) y la convención t+1 de R11. **No** leí `R12.py`, `R12-salida.txt` ni `R11.py`.

## 1. Datos (fuente distinta de A)

Todo se descargó el 2026-10-18 a las 01:13 UTC desde `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIE>`, sin encabezados especiales. Los sha256 están en `datos/SHA256SUMS`. La carpeta pesa 1.2 MB, menos de 5 MB.

| Serie | Uso | Rango | sha256 |
|---|---|---|---|
| FRED `NASDAQ100` | precio NDX (señal y rendimiento) | 1986-01-02 a 2026-10-15, diario | `cacdccbf…` |
| FRED `VIXCLS` | VIX | 1990-01-02 a 2026-10-15 | `90b0099e…` |
| FRED `DTB3` | rf diaria | 1954 a 2026-10-15 | `d9392b1d…` |
| FRED `VXOCLS` | VXO (prueba secundaria) | 1986-01-02 a 2021-09-23 | `3ab3e522…` |
| CBOE `SPX_History.csv` (copia de `AC-17-R11/datos`) | S&P 500 1986-1989 (secundaria) | desde 1975 | `0176fca2…` |
| FRED `SP500` | descargada, pero sin uso: solo cubre 10 años | 2016 a 2026 | `312d9c82…` |

- FRED `NASDAQ100` tiene datos diarios **desde 1986-01-02**, así que cubre todo el periodo pre-registrado y no hace falta recortarlo.
- **Limitación:** FRED todavía no publica el 2026-10-16. El último cierre común es el **2026-10-15**, un día antes del fin pre-registrado.
- Limpieza (§7): el panel tiene 9,261 días comunes NDX∩VIX. Se descartan 6 días con NDX y sin VIX (1991-03-01, 1997-01-31, 1997-11-26, 1998-07-03, 2001-01-01 y 2019-04-19) y 35 con VIX y sin NDX (feriados de 2022 en adelante en los que VIXCLS publica valor, más 2002-01-29 y 2004-06-11). En los días descartados, el rendimiento se mide de un cierre retenido al siguiente.

## 2. Implementación (`b.py`, stdlib, `python3 -I b.py`)

- **3x sintético:** 3·r_NDX(d) − 2·rf(d) − 0.95%/252. rf(d) es el DTB3 del día hábil previo dividido entre 100 y entre 252 (si falta, se rellena hacia adelante).
- **SMA200:** media de los últimos 200 cierres del panel común, incluido t, como dice §6. El primer rendimiento evaluado es del **1990-10-17**.
- **Ejecución:** señal al cierre t y ejecución al cierre t+1. El rendimiento del día t+2 ya corresponde a la nueva posición.
- **Costos:** 0.10% por lado, cargado el día del cambio. Fuera del mercado se gana rf. B&H paga una sola entrada.
- **Estado inicial:** fuera del mercado. Se entra cuando se cumple la regla de entrada.
- **Variantes:**
  - V0: salida si < SMA·0.97 o VIX ≥ 25; entrada si > SMA·1.03 y VIX < 25.
  - V1: igual, pero sin VIX.
  - V2: el VIX ≥ 25 debe darse en t y en t−1 para salir; la entrada es igual a V0.
  - V3: umbral 30, tanto en la salida como en la entrada.
- **Métricas:**
  - CAGR con 252 días por año.
  - Sharpe = media del exceso diario sobre rf ÷ desviación × √252.
  - MDD sobre la curva diaria.
  - Salidas = transiciones de invertido a fuera de la posición ejecutada.
  - % invertido = proporción de días invertidos.

## 3. Resultados: periodo completo (1990-10-17 a 2026-10-15, 9,060 días)

| Variante | CAGR | Sharpe | MDD | Salidas | % invertido |
|---|---|---|---|---|---|
| V0 vigente (VIX ≥ 25) | 19.64% | 0.560 | −73.7% | 108 | 68.7% |
| V1 solo SMA200 ±3% | 25.13% | 0.635 | **−90.7%** | 30 | 76.1% |
| V2 VIX ≥ 25 dos cierres | 19.28% | 0.553 | −87.8% | 75 | 69.7% |
| V3 VIX ≥ 30 | 21.83% | 0.590 | −92.1% | 67 | 73.6% |
| B&H 3x | 17.04% | 0.565 | −100.0% | 0 | 100% |

**Subperiodos (informativos)**

| Variante | 1990-2008: CAGR / Sharpe / MDD / salidas | 2009-hoy: CAGR / Sharpe / MDD / salidas |
|---|---|---|
| V0 | 15.98% / 0.477 / −73.7% / 55 | 23.51% / 0.685 / −63.2% / 53 |
| V1 | 19.88% / 0.548 / −90.7% / 17 | 30.74% / 0.768 / −62.8% / 13 |
| V2 | 12.32% / 0.424 / −86.7% / 40 | 26.86% / 0.744 / −62.8% / 35 |
| V3 | 18.20% / 0.521 / −92.0% / 30 | 25.68% / 0.707 / −62.8% / 37 |
| B&H | −4.68% / 0.374 / −100% / 0 | 44.46% / 0.878 / −81.8% / 0 |

**Ventanas de la MDD**
- V0: del 2000-01-03 al 2002-01-16.
- V1: del 2000-03-27 al 2003-04-11.
- V2: del 2000-03-27 al 2010-02-04.
- V3: del 2000-03-27 al 2009-07-07.

En la burbuja punto-com, la banda sola deja al 3x dentro de varios rebotes bajistas de 2000 a 2002. El VIX ≥ 25 lo sacaba antes y lo mantenía fuera.

## 4. Veredicto según §2 (V1 contra V0, periodo completo)

- **H1, Sharpe:** V1 0.635 > V0 0.560. La condición se cumple.
- **H1, MDD:** V1 −90.7% contra V0 −73.7%, es decir, **17.0 pp peor**. Rebasa el límite de 3 pp, así que **H1 queda REFUTADA**.
- **H2:** las salidas bajan 72% (30 contra 108), más que el 40% exigido. **H2 se sostiene.**
- **Estado según §2:** H1 refutada → **"No replicado". La condición de VIX se queda.**
- **Subperiodos:**
  - En 2009-hoy, H1 y H2 se sostienen: Sharpe +0.083 y MDD +0.4 pp.
  - En 1990-2008, H1 se refuta por la MDD.
  - El resultado depende de que la muestra incluya el estallido de 2000-2002, que es justo el caso que R11 (S&P) no castigó tanto.
- **Sensibilidad (no pre-registrada):** si la SMA200 se calcula con la historia de NDX desde 1986 (la señal existe desde el 1990-01-04), sale lo mismo. V1 tiene Sharpe 0.596 contra 0.515 de V0 y MDD −90.7% contra −73.7%.

## 5. Prueba secundaria (informativa): S&P 500 con VXO, 1986-1989

Se usaron CBOE SPX y FRED VXOCLS: 1,010 días comunes, con 1 descartado (1986-05-15). Las métricas van del 1986-10-20 al 1989-12-29.

| Variante | CAGR | Sharpe | MDD | Salidas |
|---|---|---|---|---|
| V0 (VXO ≥ 25) | 26.50% | 0.666 | −48.9% | 9 |
| V1 solo SMA ±3% | −7.71% | 0.067 | −82.2% | 1 |
| V2 | 17.97% | 0.455 | −57.0% | 7 |
| V3 (VXO ≥ 30) | −10.97% | −0.003 | −82.2% | 3 |
| B&H 3x | 3.32% | 0.349 | −80.8% | 0 |

El crash de octubre de 1987 domina la muestra: la condición de volatilidad saca a V0 antes del 19-oct, y la banda sola no. Esto también va contra H1. Los datos son informativos y la muestra es muy corta: un solo episodio.

## 6. Limitaciones

- NDX es un índice de precio, sin dividendos, igual que en A. El efecto es similar en todas las variantes.
- El 3x es sintético: no incluye el costo de financiamiento por encima de la T-bill ni el tracking real de TQQQ. No hice la sensibilidad con TQQQ real.
- El fin real es el 2026-10-15, no el 16, porque FRED tiene un día de rezago.
- El estado inicial (fuera) y la forma de contar las salidas (sobre la posición ejecutada) son elecciones de B. Si A empieza invertido, puede haber diferencias de ±1 salida.
- Después del juicio pre-registrado, las variantes V2 y V3 y los subperiodos son informativos.

Archivos: `b.py`, `salida.txt` (salida completa), `b-resultados.json`, `datos/`.
