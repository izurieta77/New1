# AC-24-R18 · Ejecución B independiente de R18 (21-oct-2026)

**Alcance.** El código se escribió desde cero (`b.py`, biblioteca estándar) a partir del pre-registro de R18 (commit 1e12150) y de la definición de V0 en el `.md` de R16. No se leyeron `R18.py`, `R16.py`, `R12.py` ni sus salidas.

## Datos (fuente B; sha256 en `datos/SHA256SUMS`, carpeta fuera de git)
- **S&P 500:** CBOE `SPX` (precio) más el rendimiento por dividendo mensual de multpl, devengado por día hábil. Es un rendimiento total aproximado, no `^SP500TR`.
- **VIX:** CBOE `VIX_History`.
- **Tasa:** FRED DTB3 (copia de AC-21, hasta el 15-oct). El 16-oct se completa con el 13 semanas del Tesoro.
- **Nasdaq-100:** FRED `NASDAQ100` (precio), copia de AC-21-R12.
- **MXN:** FRED `DEXMXUS`, copia de R15-datos, hasta el 9-oct; se arrastra el último valor.
- **FRED en mantenimiento el 21-oct:** las descargas nuevas fallaron, por eso se usan copias de FRED ya guardadas.
- **Fin efectivo de la muestra: 15-oct-2026,** porque NASDAQ100 no tiene el 16-oct. Por la regla §7, ese día se omite.

## Implementación
- **Días:** la intersección de SPX, VIX, NDX y tasa: 9,184 días, de 1990-01-02 a 2026-10-15.
- **Devengo:** el dividendo, la tasa y los gastos se devengan por los días hábiles entre dos días comunes.
- **V0:**
  - SMA200 sobre cierres comunes.
  - Salida si SPX < SMA200×0.97 o VIX ≥ 25; entrada si SPX > SMA200 y VIX < 25; con histéresis.
  - Estado del cierre de t−2 aplicado al rendimiento de t.
  - La curva empieza el 1990-10-18.
- **Instrumentos:**
  - UPRO encendido: 3·r_TR − 2·rf − 0.91%/252; apagado: rf.
  - SPYM: r_TR − 0.02%/252.
  - QQQM: r_NDX(precio) − 0.15%/252.
  - Efectivo: rf.
- **Rebalanceo:** a pesos objetivo antes del primer rendimiento de cada mes; dentro del mes, los pesos derivan.
- **Métrica:** para cada inicio t con ventana completa, el peor V_s/max(V_t..V_s) − 1 para s en t+1..t+63. Se reporta la fracción de inicios con ≤ −8% (y ≤ −12%). Los subperiodos se asignan por la fecha de inicio.
- **Control de cordura:** UPRO-V0 solo da CAGR 14.9%, MDD −72.6% y 74.7% de días encendido, contra R16 (A: 15.2%, −73.7%, 75%; B: 15.1%, −73.5%). El S&P TR solo da P(≥8%) = 27.9%.

## Resultados (USD; P = fracción de días de inicio)
| UPRO | SPYM | CAGR | Vol | MDD | P≥8% completo | 1990-2008 | 2009-hoy | P≥12% completo | P≥8% MXN 94-hoy (USD 94-hoy) |
|---|---|---|---|---|---|---|---|---|---|
| 0% | 67.9% | 12.33% | 18.6% | −58.3% | 29.7% | 32.5% | 26.9% | 15.3% | 30.8% (32.6%) |
| 13.5% | 54.4% | 13.15% | 19.2% | −57.0% | 36.7% | 38.2% | 35.2% | 16.6% | 33.9% (40.0%) |
| **26.9% (vigente)** | 41.0% | 13.86% | 20.4% | −55.8% | **48.0%** | 49.7% | 46.2% | 21.4% | 42.8% (50.2%) |
| 40% | 27.9% | 14.44% | 22.1% | −54.6% | 56.1% | 58.4% | 53.7% | 26.9% | 52.3% (57.6%) |

Con ventanas sin traslape (142 trimestres de 63 días), la mezcla vigente da 49.3% para ≥ 8% y 23.9% para ≥ 12%. Las cifras completas están en `salida.txt` y `b-resultados.json`.

## Veredicto (§2)
- **H1 refutada.** La probabilidad vigente es 48.0%, más de 3 veces el umbral de 15%. Se mantiene en los dos subperiodos (49.7% y 46.2%), en MXN (42.8%) y con ventanas sin traslape.
  - Incluso sin UPRO (0%), la mezcla rebasa el 15% (29.7%): el −8% está dentro del ruido trimestral normal de la renta variable.
  - Con −12%, la mezcla vigente da 21.4%.
- **H2 sostenida.** Bajar a 13.5% reduce la probabilidad 11.3 pp (48.0% → 36.7%). En 1990-2008 la reducción es de 11.5 pp y en 2009-hoy de 11.0 pp. En MXN es de 8.9 pp.
- **Estado según B: "No replicado"** (H1 refutada). La expectativa previa del autor (15-30%) también subestima la cifra.
- **MXN:** amortigua 5-7 pp, como se había anticipado, pero no cambia el veredicto.
- **Insumo para el comité:** con los cortacircuitos actuales, el satélite se recortaría a la mitad en aproximadamente uno de cada dos trimestres. Esto es esperable para cualquier peso de UPRO, porque el umbral está por debajo del ruido base de la mezcla sin UPRO.

## Limitaciones
- **Rendimiento total aproximado:** el TR viene de multpl (mensual), no de un índice TR oficial.
- **NDX sin dividendos,** como en A, lo que subestima levemente el rendimiento de QQQM y no afecta la métrica de caída.
- **Las ventanas traslapadas no son independientes.** Por eso se agrega la cifra con ventanas sin traslape.
