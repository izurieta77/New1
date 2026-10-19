# AC-22-R16: ejecución B independiente de R16 (stop fijo del UPRO sobre el filtro)

- **Fecha:** 2026-10-19. **Insumo leído:** solo el pre-registro `laboratorio/replicas/R16-stop-fijo-upro.md` (commit c067ef6). No leí `R16.py`, su salida ni sus resultados, ni `R11.py`/`R12.py`.
- **Reproducción:** `python3 -I laboratorio/auditorias/AC-22-R16/b.py` (biblioteca estándar; lee `datos/`, escribe `salida.txt` y `b-resultados.json`). Huellas en `datos/SHA256SUMS`.

## 1. Datos (distintos de A salvo la rf)

| Uso | Fuente B | Archivo |
|---|---|---|
| Señal y precio | CBOE `SPX_History.csv` (descarga 2026-10-19, hasta 2026-10-16) | `SPX_History_cboe.csv` |
| Dividendos (TR aproximado) | multpl, yield mensual | `multpl_sp500_dividend_yield_by_month.html` |
| VIX | CBOE `VIX_History.csv` (cierre) | `VIX_History.csv` |
| rf | FRED `DTB3` copiado de AC-17 (hasta 2026-10-08) + Tesoro EE. UU., 13 semanas, tasa de descuento (2026-10-09 a 10-16) | `DTB3_fred_copia_AC17.csv`, `treasury_bill_rates_2026.csv` |
| Contraste | FRED `SP500` (copia AC-17) | `SP500_fred_copia_AC17.csv` |

- FRED no respondió el 2026-10-19 (conexión cerrada o timeout en fredgraph, alfred y /data). Por eso no hay contraste con `VIXCLS`, y la rf se completó con la serie del Tesoro, que es la misma tasa que publica DTB3; coincide en los días comunes.
- SPX CBOE coincide con FRED SP500 en 2,511 de 2,512 días. La diferencia es 2019-02-28, y no la corregí porque es un solo día y no cambia ninguna señal.
- Se descartan 3 días con SPX pero sin VIX (1991-03-01, 1997-01-31, 1997-11-26) y se ignoran 34 días con VIX pero sin SPX.

## 2. Decisiones de método (posibles causas de diferencias con A)

1. **TR aproximado:** `r_TR = P_t/P_{t-1} − 1 + yield_mes/252`. No es `^SP500TR`. En AC-17 eso movió el CAGR por nivel, pero casi nada la comparación entre reglas.
2. **3x:** `r3 = 3·r_TR − 2·rf − 0.0091/252`, con `rf = DTB3` del último dato **anterior** a t, /100/252, de forma simple.
3. **Periodo:** SMA200 sobre los cierres del panel común. Empieza en el cierre 200 (1990-10-15), y el primer rendimiento es el 1990-10-16. Termina el 2026-10-16. Subperiodos: 1990-10-16 a 2008-12-31 y 2009-01-02 a 2026-10-16, como cortes de una sola corrida.
4. **Filtro V0:** histéresis. Fuera→dentro si `SPX > SMA200` y `VIX < 25`; dentro→fuera si `SPX < 0.97·SMA200` o `VIX ≥ 25`. Se decide al cierre de t y se ejecuta al cierre de t+1. Arranca fuera.
5. **Stop:** el nivel es el valor del índice 3x al cierre de entrada × (1 − s), fijo. Se compara con el cierre del 3x de t y se sale al cierre de t (puede quedar por debajo del nivel si hay hueco). Si ese día ya estaba programada una salida del filtro, la salida cuenta como filtro, no como stop.
6. **Reentrada tras un stop:** bloqueo hasta que el filtro (estado deseado) se apague y vuelva a encender. Se entra al ejecutarse esa nueva entrada.
   - **Sensibilidad (b):** además, a los 21 días hábiles del stop se reentra al cierre si el filtro sigue encendido.
7. **Costos:** 0.10% sobre el capital en cada ejecución. Fuera del mercado se gana rf.
   - Comprar y mantener: compra al cierre del 1990-10-15 y paga un costo.
8. **Métricas:**
   - CAGR por días calendario/365.25.
   - Sharpe = media/desv. del exceso diario sobre rf × √252.
   - MDD sobre la curva diaria.
   - "sal" = todas las salidas ejecutadas; "stop" = las salidas por stop.
9. **H2:** para cada salida por stop de S10.92 el día d, se busca si V0 (corrida propia) ejecuta una salida en [d, d+21] días hábiles.

## 3. Resultados (netos)

### Periodo completo, 1990-10-16 a 2026-10-16

| Regla | CAGR | Vol | Sharpe | MDD | sal | stop |
|---|---:|---:|---:|---:|---:|---:|
| V0 | 15.11% | 32.6% | 0.516 | −73.5% | 108 | 0 |
| S8 | 9.88% | 30.1% | 0.378 | −75.9% | 108 | 24 |
| **S10.92** | 9.71% | 30.4% | 0.372 | −76.0% | 108 | 17 |
| S15 | 14.44% | 32.5% | 0.499 | −75.4% | 108 | 5 |
| S20 | 14.65% | 32.5% | 0.504 | −73.5% | 108 | 1 |
| S10.92, reentrada a 21 d (b) | 15.23% | 32.1% | 0.522 | −71.9% | 110 | 17 |
| Comprar y mantener 3x | 18.15% | 54.0% | 0.533 | −97.9% | 0 | 0 |

### Subperiodos

| Regla | 1990-2008 Sharpe | 1990-2008 MDD | 2009-hoy Sharpe | 2009-hoy MDD |
|---|---:|---:|---:|---:|
| V0 | 0.440 | −73.5% | 0.591 | −49.3% |
| S10.92 | 0.098 | −76.0% | 0.622 | −48.4% |
| S10.92 (b) | 0.418 | −71.9% | 0.626 | −48.4% |

Las tablas completas, con S8/S15/S20, CAGR, volatilidad y tiempo invertido, están en `salida.txt`.

## 4. Hipótesis y veredicto

- **H1, periodo completo (decide):** S10.92 frente a V0 da una mejora de MDD de **−2.53 pp** (empeora; el umbral es +3) y un ΔSharpe de **−0.143** (el umbral es −0.03). **Refutada** por los dos criterios.
  - En 2009-hoy, el ΔSharpe es +0.031, pero la MDD mejora solo 0.95 pp, así que también queda refutada.
- **H2 (informativa):** hubo 17 salidas por stop. En 15 de ellas (**88.2%**) V0 sale dentro de los 21 días hábiles, en general al día siguiente. **Sostenida**: el stop casi siempre se adelanta solo un día al filtro.
- **Mecanismo del costo:** las 2 salidas que no son redundantes son 1994-12-08 y 2018-03-23. En ambas, el filtro siguió encendido mucho tiempo: V0 no salió hasta 1997-09 y 2018-10, respectivamente. La regla de reentrada de reinicio completo deja a S10.92 fuera durante todo el alza de 1995-1997, y de ahí sale casi todo el costo (Sharpe 1990-2008: 0.098 contra 0.440).
  - Con la reentrada a 21 días (b), el costo desaparece (Sharpe +0.006), pero la MDD mejora solo 1.6 pp, menos que los 3 pp exigidos. H1 tampoco se sostendría con esta variante.
- **Estado según la §2:** **"No replicado"**. El stop de −10.92% no se justifica en esta prueba. Esto no cambia ninguna regla; según el pre-registro, lo decide el comité.
- **Robustez frente a la fuente:** el margen de ΔSharpe es −0.11 más allá del umbral. Es muy superior a las diferencias por TR aproximado o rf que se vieron en AC-17 (menos de 0.01 entre reglas), así que el veredicto no debería depender de la fuente.
