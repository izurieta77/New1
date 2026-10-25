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

## Adenda 2026-10-24 · Lado B con la métrica del cortacircuitos (máximo histórico de la cuenta)
- **Motivo:** la auditoría W43 (`bitacora/semanal/2026-W43-abogado.md` §1) señaló que R18 mide la caída contra el máximo **desde el inicio de cada ventana**, mientras que `riesgo.estado_cortacircuitos` (`herramientas/riesgo.py` L82-L89) mide DD(t) = índice(t)/max_{s≤t} índice(s) − 1, con el máximo **desde que abrió la cuenta**. El abogado calculó solo el lado A (grado C).
- **Código:** `ac24_maximo_historico.py`, nuevo. Reutiliza las curvas de `b.py` igual que la adenda del 22-oct (runpy, JSON a un temporal; `b-resultados.json` no cambia). La métrica está escrita en el archivo nuevo: el pico se actualiza con cada máximo nuevo y se toca el nivel si DD ≤ −u en algún día de t0+1..t0+H. No se leyó `R18.py` ni el código del abogado.
- **Datos:** los mismos de B (`datos/SHA256SUMS` OK). Corrida: `python3 -I ac24_maximo_historico.py datos` (~3 s).
- **Control:** la definición (a) reproduce exactamente las cifras previas de B a 63 días (P≥12% = 15.3 / 16.6 / 21.4 / 26.9%; P≥20% = 4.1 / 4.4 / 3.5 / 4.5%).

**Definiciones**
- **(a) Incondicional, cuenta nueva:** para cada t0, el pico es índice(t0) y se mide P(DD toca −u en los siguientes H días). Es la métrica de R18.
- **(b) Condicional al estado de hoy:** pico de la cuenta = max(índice[t0−L .. t0]), con L = 20, 25 o 30 días hábiles. Se toman los t0 con DD(t0) ∈ [−3.8%, −2.8%] y se mide P(DD contra ese pico, que se sigue actualizando, toque −u en t0+1..t0+H).
  - **Por qué L ≈ 20:** la cuenta de papel abrió el 28-sep-2026 y lleva ~20 sesiones al 23-oct. Su pico (104.41) fue el 9-oct, 10 sesiones antes, y hoy está en 100.97, es decir, −3.30%. Con L = 20, "pico de la cuenta" significa lo mismo que en la cuenta real: no puede venir de antes de su apertura.
  - **Sensibilidad:** L = 20 → 30 baja la P entre 1 y 4 pp. Cuanto más corto es L, más rápida fue la caída de −3.3% que se exige y más volátil es el régimen que se condiciona (agrupamiento de volatilidad). L = 63 o 126 da cifras parecidas a L = 30 con 26.9% y 40%, y menores con 0% y 13.5%.
- **(a′) Definición del lado A (abogado):** el pico es el máximo desde el inicio de la serie (1990). Se cuentan los inicios con DD(t0) > −u, y también el subconjunto con DD(t0) ∈ [−5%, −2%]. Solo sirve para cotejar con A.

**Tabla B.** Celdas (b) como L20 / L25 / L30; n ≈ 620-780 inicios condicionados (traslapados).

| UPRO | (a) −12% 63 d | (b) −12% 63 d | (a) −12% 126 d | (b) −12% 126 d | (a) −20% 63 d | (b) −20% 63 d | (a) −20% 126 d | (b) −20% 126 d |
|---|---|---|---|---|---|---|---|---|
| 0% | 15.3% | 18.5 / 16.9 / 15.9% | 26.8% | 29.1 / 26.3 / 25.4% | 4.1% | 4.4 / 3.6 / 3.3% | 9.7% | 10.8 / 9.6 / 9.7% |
| 13.5% | 16.6% | 22.3 / 20.8 / 19.8% | 30.4% | 34.1 / 32.1 / 30.9% | 4.4% | 6.3 / 5.9 / 3.7% | 12.8% | 17.5 / 16.0 / 13.9% |
| **26.9% (vigente)** | 21.4% | **28.4 / 26.1 / 24.6%** | 41.4% | **46.2 / 44.6 / 42.1%** | 3.5% | **4.9 / 5.0 / 4.1%** | 12.5% | **16.8 / 15.3 / 13.6%** |
| 40% | 26.9% | 32.2 / 30.3 / 31.3% | 50.9% | 54.6 / 52.4 / 52.5% | 4.5% | 4.7 / 4.9 / 6.1% | 15.2% | 15.7 / 13.9 / 13.5% |

- **n efectivo chico:** los inicios que tocan −12% a 126 días con 26.9% se agrupan en ~13 bloques (episodios); los de −20% a 126 días, en ~9. A 63 días, −12% se reparte en ~25 bloques y −20% en ~10.

**Cotejo con A, misma definición (a′)**

| Celda | A (abogado) | B (a′) | Δ B−A |
|---|---|---|---|
| −12% 63 d, arranca arriba de −12%: 0 / 13.5 / 26.9 / 40% | 14.1 / 20.0 / 33.3 / 37.8% | 15.4 / 20.3 / 33.3 / 38.3% | +1.3 / +0.3 / 0.0 / +0.5 |
| −12% 63 d, DD ∈ [−5, −2]%: 13.5 / 26.9% | 17.1 / 25.1% | 17.2 / 25.6% | +0.1 / +0.5 |
| −12% 126 d, DD ∈ [−5, −2]%: 13.5 / 26.9% | 29.6 / 44.7% | 29.3 / 45.6% | −0.3 / +0.9 |
| Cuenta nueva −20% 252 d: 0 / 13.5 / 26.9% | 16.6 / 25.4 / 27.1% | 16.9 / 25.9 / 27.4% | +0.3 / +0.5 / +0.3 |

- **Con la misma definición, A y B concuerdan en las 11 celdas.** Diez quedan dentro de ±1 pp. La mayor diferencia es +1.3 pp (0%, sin condicionar) y viene del mismo sesgo de fuente de B ya documentado el 22-oct (dividendo de multpl, NASDAQ100 de FRED, días omitidos por DTB3).
- **Nota sobre el "~33% sin condicionar" de A:** usa el máximo desde 1990 e incluye arranques que ya están, por ejemplo, a −10%. No describe ni una cuenta nueva (21.4%) ni la cuenta de hoy. En la nota de R18 del 23-oct, la cifra "P(−12% en 126 días) ≈ 45%" es la **condicional** (columna "Ídem, 126 d" del abogado), no la incondicional (B a′ incondicional a 126 d: 51.3%).

**Cotejo con las cifras titulares de A contra la definición pedida (b)**

| | A (DD ∈ [−5, −2]% vs máx. desde 1990) | B (b) L20 / L25 / L30 | Δ con L20 (L25) | ¿±3 pp? |
|---|---|---|---|---|
| 26.9%, −12% 63 d | ~25% (25.1) | 28.4 / 26.1 / 24.6% | +3.3 (+1.0) | Sí con L25-L30; al filo con L20 |
| 26.9%, −12% 126 d | ~45% (44.7) | 46.2 / 44.6 / 42.1% | +1.5 (−0.1) | Sí |
| 13.5%, −12% 63 d | ~17% (17.1) | 22.3 / 20.8 / 19.8% | +5.2 (+3.7) | **No** (sí con L30: +2.7) |
| 13.5%, −12% 126 d | ~30% (29.6) | 34.1 / 32.1 / 30.9% | +4.5 (+2.5) | Sí con L25-L30; no con L20 |

- **Origen de las diferencias:** es la definición, no el código. A condiciona a una banda ancha (−5 a −2%) contra un pico que puede tener años. (b) exige una caída de −3.3% desde un pico de los últimos 20-30 días, que se parece más a la cuenta real y deja una muestra de régimen más volátil. Con 13.5% el efecto es mayor.
- **La reducción por bajar UPRO de 26.9% a 13.5%** es de 6.1 pp a 63 días y 12.1 pp a 126 días con L20 (5.3 y 12.5 pp con L25), no los ~8 y ~15 pp de A. Es más que los 4.6 pp de R18 y menos que lo que estimó A.

**Veredicto**
- **El lado A se confirma.** Con su misma definición, B concuerda dentro de ±1.3 pp en las 11 celdas. Con la definición pedida (b), la cifra de 26.9% concuerda dentro de ±3 pp con L25-L30 (con L20 el desvío es +3.3 pp a 63 días). La de 13.5% queda **por encima** de A en +2.5 a +5.2 pp.
- **Rige la más conservadora (la mayor; B L20):**
  - **UPRO al 26.9%: P(tocar −12% contra el pico de la cuenta, con DD de −3.3%) ≈ 28% a 63 días y ≈ 46% a 126 días.** P(−20%) ≈ 5% a 63 días y ≈ 17% a 126 días.
  - UPRO al 13.5%: ≈ 22% / 34% para −12% y ≈ 6% / 18% para −20%.
  - Cuenta nueva sin condicionar, 26.9%: 21.4% / 41.4% para −12% y 3.5% / 12.5% para −20%.
- **Falsador C1 del abogado** ("si B da ≤ 21% con 26.9%, cae mi objeción"): B da 25.6% con su definición y 24.6-28.4% con la de hoy. **La objeción se sostiene.**
- **Lectura:** a 126 días, el primer freno se dispara en casi una de cada dos trayectorias desde el estado actual con el UPRO vigente, y en una de cada tres con 13.5%. En −20%, el tamaño del UPRO mueve poco a 63 días y nada entre 13.5% y 40% a 126 días (14-18%), lo que confirma que la cola la pone la beta sin apalancar. Los intervalos reales son anchos, porque son ~9-13 episodios por celda.
- **Sobre R18:** su estado sigue en "No replicado" respecto de H1 literal (−8%). Esta adenda solo corrige la métrica aplicable al cortacircuitos.
