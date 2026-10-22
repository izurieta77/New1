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

## Adenda 2026-10-22 01:15 UTC (orquestador, trabajo continuo) · perfil `arena_agresivo`
- Este informe audita contra el −8% del perfil estándar, igual que A. El papel corre con `arena_agresivo` (−12%, −20%, −28%, −35%). Ver la adenda en `replicas/R18-tamano-upro-cortacircuitos.md`.
- La columna "P ≥ 12%" de B ya es la cifra aplicable: **21.4%** con UPRO al 26.9% (A: 21.0%). P(≥ 20%) y P(≥ 28%) no los calculó B; quedan pendientes para una auditoría futura.
- El informe no se reescribe.

## Adenda 2026-10-22 · Lado B de P(≥ 20%) y P(≥ 28%) (perfil `arena_agresivo`)
- **Código:** `ac24_niveles_arena.py`, nuevo. Reutiliza las curvas de `b.py` sin modificarlo; lo ejecuta con runpy y manda su JSON a un archivo temporal, así que `b-resultados.json` no cambia. La métrica de toque y el conteo de episodios están escritos en el archivo nuevo. No se leyó `R18.py`.
- **Datos:** los mismos de la ejecución B; `datos/SHA256SUMS` verificado OK. Son 8,921 inicios con ventana traslapada (H = 63) y 142 sin traslape.
- **Control:** P(≥ 12%) reproduce exactamente las cifras previas de B (15.3 / 16.6 / 21.4 / 26.9%).

| UPRO | P≥12% B | P≥20% A | **P≥20% B** | Δ B−A | P≥28% A | **P≥28% B** | Δ B−A | P≥35% B | Sin traslape B (≥12 / ≥20 / ≥28) |
|---|---|---|---|---|---|---|---|---|---|
| 0% | 15.3% | 3.8% | **4.1%** | +0.3 | 1.2% | **1.2%** | 0.0 | 0.3% | 16.2 / 3.5 / 1.4% (23 / 5 / 2 de 142) |
| 13.5% | 16.6% | 4.2% | **4.4%** | +0.2 | 1.0% | **1.0%** | 0.0 | 0.1% | 19.0 / 2.8 / 1.4% (27 / 4 / 2) |
| **26.9% (vigente)** | 21.4% | 3.1% | **3.5%** | +0.4 | 0.2% | **0.6%** | +0.4 | 0.0% | 23.9 / 2.8 / 1.4% (34 / 4 / 2) |
| 40% | 26.9% | 4.1% | **4.5%** | +0.4 | 0.0% | **0.4%** | +0.4 | 0.0% | 28.2 / 2.8 / 0.7% (40 / 4 / 1) |

**Episodios con UPRO al 26.9% (n pequeño).** Se cuentan como bloques de inicios contiguos cuya ventana de 63 días toca el nivel:
- **≥ 20%:** 9 bloques. Por fecha de inicio: 1998, 2000-T3, 2001-T1, 2002-T2, 2008-T3, 2018-T4, 2019-12/2020-02 (COVID), 2022-T1 y 2024-12/2025-03 (aranceles).
  - Cada bloque tiene entre 16 y 60 inicios.
  - Son 8 drawdowns distintos de pico a recuperación de la curva completa.
  - Sin traslape, solo 4 de 142 trimestres.
- **≥ 28%:** 2 bloques, 2008 (−31.1%) y 2025 (−28.6%).
- **Conclusión:** la cifra de −20% descansa en unos 9 episodios y la de −28% en 2. Diferencias de ±1 pp entre variantes equivalen a 1 o 2 episodios.
- **No monotonicidad:** B también la tiene (4.1 / 4.4 / 3.5 / 4.5%), igual que A.
  - Con más UPRO aparecen más episodios cortos (6 → 9 → 9 → 11 bloques).
  - Pero V0 saca al 3x de las caídas largas, y el bloque de 2008 se acorta: 134 inicios con 0%, 60 con 26.9%.
  - Es ruido de pocos episodios, no una señal.

**Diferencias contra A, explicadas:**
- **P(≥ 28%) con UPRO al 26.9% y al 40% (+0.4 pp).** Todo viene del episodio de abril de 2025 y de un empate al filo de la regla del 0.97.
  - El 28-mar-2025, SPX/SMA200 da 0.97005 en B, que calcula la SMA sobre días comunes. B omite el 14-oct-2024 y el 11-nov-2024 porque DTB3 no tiene esos días.
  - Con todos los días de SPX, la razón es 0.96907 y V0 sale.
  - En B, el 3x sigue dentro el 3 y el 4 de abril (señal de t−2), y la curva vigente cae −28.6%. Con 40% cae −33.1%.
  - **Sensibilidad:** recalculando B con la SMA200 sobre todos los días de SPX, P(≥ 28%) baja a 0.3% (vigente) y 0.0% (40%), prácticamente igual que A (0.2 / 0.0%). P(≥ 20%) queda en 3.4% y 4.2%.
- **P(≥ 20%) (+0.2 a +0.4 pp en todas las variantes).** Hay un sesgo pequeño y uniforme por la fuente, que no cambia con la SMA:
  - El rendimiento total de B se aproxima con el dividendo mensual de multpl.
  - El NASDAQ100 viene de FRED.
  - La tasa es DTB3 con días omitidos.
  - Está muy por debajo de la tolerancia.

**Veredicto:**
- **A y B concuerdan dentro de ±1.5 pp en las 8 celdas.** La diferencia máxima es de 0.4 pp.
- **Rige la cifra más conservadora, la de B en todas las celdas.** Para la mezcla vigente:
  - **P(≥ 20%) = 3.5% por trimestre** (sin traslape: 2.8%, 4 de 142).
  - **P(≥ 28%) = 0.6%** (sin traslape: 1.4%, 2 de 142; se toma la mayor, 1.4%, si se quiere el techo).
  - Ambas cifras se apoyan en unos 9 y 2 episodios. Su error de muestreo real es del orden de su propio tamaño.
- **El veredicto sobre R18 no cambia:** sigue "No replicado" respecto de H1 literal (−8%).
- **Lectura para el comité:** la cifra aplicable es P(≥ 12%) ≈ 21%. Los niveles de −20% y −28% son raros (≈ 3-4% y ≤ 1.4% por trimestre). La regla 0.97 tiene un caso al filo en 2025 que mueve P(≥ 28%) entre 0.3% y 0.6%.
- **Salida:** la corrida está en `python3 -I ac24_niveles_arena.py datos`.
