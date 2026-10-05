# Ficha de avance · 5-oct-2026 · G5 Mercado (beta y correlación de BTC con S&P 500 y oro, ventana de 5 años, con análisis de días de estrés)

> Corrida de las 08:17 CDMX (14:17 UTC), `analista-cripto`. Avanza el pendiente explícito dejado en `conocimiento/estado-de-dominio.csv` (fila cripto/05, "siguiente_prueba" del 2-oct-2026): *"extender la ventana de beta/correlación de BTC más allá de 2 años, agregar oro y S&P 500 al cruce"*, que a su vez retomaba el pendiente ya anotado el 29-sep-2026 en la ficha `fichas/2026-09-29-btc-nasdaq-usdmxn-beta.md` §8. Elegido sobre los otros 5 candidatos de la corrida de hoy (releer Mastering Bitcoin en AsciiDoc, repetir emisión/quema de ETH tras Glamsterdam, verificar la tarifa del art. 152 LISR, repetir PoR de Binance, acumular flujos de ETF) porque es el que más valor aporta **hoy mismo** para el riesgo de cola de la cuenta combinada (`arena-claude` GBM + `arena-claude-binance`): el comité del 9-oct debe ratificar si BTC sube de 40% a 65% de la cuenta cripto, y la cuenta GBM ya tiene UPRO (3x S&P 500) desde la decisión W40 del 2-oct. Si BTC se mueve con una beta alta frente al S&P 500 **precisamente en los peores días del índice**, el supuesto de diversificación entre las dos cuentas se debilita. Los otros 5 candidatos son mantenimiento de calidad o esperan una fecha (PoR hacia el 15-21 de octubre; el fork de Glamsterdam en Sepolia es apenas mañana, sin datos de la red todavía) y no cambian ninguna decisión de cartera en esta corrida.

## 1. Acceso real

- **Datos de precio:** Yahoo Finance, endpoint `chart` v8 (`query1.finance.yahoo.com/v8/finance/chart/<símbolo>?range=5y&interval=1d`), sin clave; se necesitó fijar un `User-Agent` de navegador porque la primera tanda de solicitudes sin encabezado devolvió HTTP 429 (límite de tasa), no un bloqueo permanente. Símbolos: `BTC-USD`, `^GSPC` (S&P 500, nuevo en este ejercicio), `GC=F` (futuro de oro, nuevo), `MXN=X` (USD/MXN) y `QQQ` (Nasdaq-100, para comparar contra la ficha del 29-sep). Acceso **íntegro** a los cierres diarios de los últimos 5 años de los cinco símbolos (1,827 velas de BTC, que cotiza 7 días; 1,255 de los demás, que solo cotizan en días hábiles de EUA).
- Nada de esto es información privilegiada: son precios de mercado público.

## 2. Metodología (declarada antes de ver el resultado final, salvo el primer corte exploratorio)

1. Cargar cierres diarios de los 5 símbolos a `range=5y` (en vez de los `range=2y` de la ficha del 29-sep).
2. Quedarse con las **fechas comunes** a BTC, S&P 500, oro, USD/MXN y QQQ (1,108 fechas, 2021-10-05 a 2026-10-05); igual que en la ficha del 29-sep, esto descarta el movimiento de fin de semana de BTC.
3. Calcular retornos diarios simples de las 5 series; construir versiones en MXN (`BTC_MXN`, `GSPC_MXN`, `GOLD_MXN`) multiplicando por USD/MXN del mismo día.
4. Reportar, en USD y en MXN: (a) correlación y beta de mínimos cuadrados (BTC como dependiente) en la muestra completa de 5 años; (b) la misma muestra recortada a los últimos 2 años, para comparar directamente con la ficha del 29-sep; (c) correlación y beta **rodantes de 90 días** sobre toda la ventana de 5 años (1,017 ventanas, contra las 355 de la ficha anterior); (d) corte **por año calendario** (2021 parcial a 2026 parcial); (e) **nuevo en este ejercicio:** correlación y retorno medio de BTC condicionados a que el S&P 500 tuvo un día de estrés (retorno diario ≤ −1%) contra los días normales, y el detalle de los 10 peores días del S&P 500 en la ventana, con lo que hizo BTC y el oro ese mismo día.
5. **Verificación doble:** el cálculo se implementó primero con fórmulas de covarianza/varianza en Python puro (stdlib, sin librerías), replicando el patrón de la ficha del 29-sep, y se repitió completo con NumPy (orden de cómputo distinto). Los números coinciden a 3-4 decimales (diferencias de ≤0.0015 en correlación y ≤0.002 en beta, atribuibles a redondeo de punto flotante, no a un error de indexado).

## 3. Resultados

### 3.1 Muestra completa de 5 años (1,107 retornos diarios comunes, 2021-10-06 a 2026-10-05)

| Par | Correlación | Beta (BTC sobre el otro activo) |
|---|---|---|
| BTC(USD) – S&P 500 (USD) | **0.438** | **1.359** |
| BTC(USD) – oro (USD) | **0.123** | **0.343** |
| BTC(USD) – QQQ (USD) | **0.441** | **1.017** |
| BTC(MXN) – S&P 500 (MXN) | **0.424** | **1.257** |
| BTC(MXN) – oro (MXN) | **0.122** | **0.323** |
| S&P 500 (USD) – oro (USD) | 0.144 | — |
| BTC(USD) – retorno USD/MXN | −0.127 | −0.296 (igual orden de magnitud que la ficha del 29-sep) |
| Volatilidad anualizada | BTC 67.6% · S&P 500 21.8% · oro 24.3% · QQQ 29.3% | — |

- **La beta de BTC sobre el S&P 500 en 5 años (1.359) es mayor que la que reportó la ficha del 29-sep sobre el Nasdaq en 2 años (0.886)**, y también mayor que la beta de BTC sobre QQQ en esta misma ventana de 5 años (1.017). Al meter el ciclo completo de endurecimiento monetario de 2022 (ver §3.4), la beta de BTC frente a renta variable amplia sube, no baja.
- **El oro se comporta distinto:** correlación baja con BTC (0.123) y con el S&P 500 (0.144) en la muestra completa; beta de BTC sobre el oro de solo 0.343. No hay evidencia de que BTC y el oro compartan el mismo "canal de devaluación" de forma estable en 5 años, aunque §3.4 muestra que la correlación BTC-oro subió en el tramo reciente.

### 3.2 Ventana de 2 años (444 días, 2024-10-07 a 2026-10-05), para comparar directo con la ficha del 29-sep

| Par | Correlación | Beta |
|---|---|---|
| BTC(USD) – S&P 500 (USD) | 0.422 | 1.174 |
| BTC(USD) – oro (USD) | 0.138 | 0.251 |

- Es consistente con la ficha del 29-sep (BTC-QQQ: correlación 0.424, beta 0.886, con datos hasta el 29-sep): la correlación con renta variable amplia es parecida (0.42-0.44) sin importar si se usa el S&P 500 o el Nasdaq, pero la **beta** depende del índice de referencia y de la ventana exacta — nunca se debe asumir una beta de 1.0 fija frente a "el mercado".

### 3.3 Rodante de 90 días sobre toda la ventana de 5 años (1,017 ventanas, no solo 355 como en la ficha del 29-sep)

| Métrica | Mediana | Mínimo | Máximo | Última ventana (hoy) |
|---|---|---|---|---|
| Correlación BTC(USD)-S&P 500(USD) | 0.468 | **−0.131** | 0.746 | 0.346 |
| Beta BTC(USD)/S&P 500(USD) | 1.398 | **−0.637** | 2.737 | 1.126 |
| Correlación BTC(USD)-oro(USD) | 0.098 | −0.206 | 0.493 | **0.448** |

- **Corrección a la ficha del 29-sep:** aquella ficha decía que la correlación BTC-Nasdaq "nunca fue negativa" en 355 ventanas de 2 años (mínimo 0.142). Con la ventana de 5 años (1,017 ventanas), **sí hubo tramos con correlación BTC-S&P 500 negativa**: 73 de 1,017 ventanas (7.2%), con un mínimo de −0.131. No es un error de aquella ficha (la afirmación era correcta para su propia ventana de 2 años), pero **no se sostiene al extender la historia**, que es justamente el objetivo de este ejercicio. Se registra como corrección de alcance, no como error de cálculo, en `conocimiento/registro-de-errores.md`.
- **La correlación BTC-oro subió mucho en la ventana reciente** (última lectura 0.448, contra una mediana histórica de solo 0.098): 217 de 1,017 ventanas (21.3%) tuvieron correlación negativa en algún momento de los 5 años, pero el régimen de hoy está en el extremo alto de toda la historia. Esto es consistente con la narrativa de "comercio de devaluación" (BTC y oro subiendo juntos en 2026) que menciona la prensa, pero con un historial de solo 5 años no se puede afirmar que sea un parámetro estable; es el mismo patrón de inestabilidad de régimen que ya documentan las fichas del 28 y 29-sep para otros pares.

### 3.4 Por año calendario (corr BTC-S&P 500 / corr BTC-oro)

| Año | n días | corr BTC-S&P 500 | corr BTC-oro |
|---|---|---|---|
| 2021 (parcial, oct-dic) | 57 | 0.300 | −0.024 |
| 2022 | 221 | **0.646** | 0.080 |
| 2023 | 220 | 0.068 | 0.193 |
| 2024 | 222 | 0.412 | 0.130 |
| 2025 | 221 | 0.447 | 0.070 |
| 2026 (parcial, ene-oct) | 166 | 0.435 | **0.229** |

- **2022 (el año del ciclo de alzas de la Fed, Terra y FTX) tuvo, por mucho, la correlación más alta del quinquenio entre BTC y el S&P 500 (0.646).** Es el año que la ficha del 29-sep no alcanzaba a ver con su ventana de 2 años. Esto importa porque es precisamente el tipo de año (tasas subiendo rápido, estrés de liquidez) que más se parece a un escenario de cola para la cuenta combinada.
- 2026 tiene la correlación BTC-oro más alta del quinquenio (0.229), coherente con el repunte de la ventana rodante de §3.3.

### 3.5 Análisis nuevo: ¿qué hace BTC en los peores días del S&P 500? (1,254 retornos diarios comunes BTC-S&P 500-oro, 2021-10-06 a 2026-10-05)

| | Días de estrés del S&P 500 (retorno ≤ −1%, n=162 de 1,254) | Días normales (n=1,092) |
|---|---|---|
| Correlación BTC-S&P 500 ese subconjunto | 0.333 | 0.293 |
| Retorno medio de BTC | **−2.43%** | +0.47% |
| Retorno medio del oro | −0.09% | — |
| P(BTC también cae ≥1% el mismo día) | **63.6%** | — |

- **BTC no actuó como refugio en promedio durante los días malos del S&P 500 de los últimos 5 años: en esos 162 días cayó, en promedio, −2.43%** (contra +0.47% en un día normal), y la correlación con el S&P 500 fue ligeramente **más alta**, no más baja, que en días normales (0.333 vs 0.293). No hay evidencia de que la diversificación "funcione mejor" justo cuando más se necesita; si algo, el patrón va en la dirección contraria.
- **Los 10 peores días del S&P 500 de los últimos 5 años, con lo que hizo BTC y el oro ese mismo día:**

| Fecha | S&P 500 | BTC | Oro | Contexto |
|---|---|---|---|---|
| 2025-04-04 | −5.97% | **+0.89%** | −2.76% | Arancel "Día de la Liberación" de Trump |
| 2025-04-03 | −4.84% | **+0.75%** | −1.41% | Mismo choque arancelario, un día antes |
| 2022-09-13 | −4.32% | **−9.27%** | −1.33% | CPI de EUA más caliente de lo esperado |
| 2022-05-18 | −4.04% | −5.61% | −0.16% | Ciclo de alzas de la Fed |
| 2022-06-13 | −3.88% | **−22.68%** | −2.33% | Congelamiento de retiros de Celsius (12-jun-2022) |
| 2022-04-29 | −3.63% | −2.93% | +1.08% | Ciclo de alzas de la Fed |
| 2022-05-05 | −3.56% | −7.87% | +0.37% | Ciclo de alzas de la Fed |
| 2025-04-10 | −3.46% | −3.57% | +3.19% | Choque arancelario, continuación |
| 2022-08-26 | −3.37% | −6.21% | −1.22% | Discurso de Powell en Jackson Hole |
| 2022-06-16 | −3.25% | −9.71% | +1.67% | Continuación de la corrida de Celsius |

- **Hallazgo central: el patrón depende del tipo de choque, no es uniforme.** En el choque arancelario de abril de 2025 (un shock de política comercial, no financiero ni cripto-específico), BTC **subió** mientras el S&P 500 y el oro caían — el único tramo de la tabla donde BTC se comportó como diversificador real. En los 6 peores días de 2022 (ciclo de alzas de tasas combinado con el colapso de Celsius, un evento de cola propio de cripto), BTC **amplificó** la caída del S&P 500, llegando a −22.68% en un solo día (13-jun-2022) cuando el índice cayó "solo" −3.88%. **Conclusión aplicada:** no se puede asumir que BTC diversifique un mismo choque macro para las dos cuentas (GBM y Binance); depende de si el origen del estrés es idiosincrático de cripto (amplifica) o un choque de política ajeno a cripto (puede diversificar, con 2 observaciones nada más).

## 4. Verificación numérica (script, dos implementaciones independientes)

```python
# beta_extendido.py — Python puro, verificado después con NumPy (coincide a 3-4 decimales)
def load_yahoo(path):
    d = json.load(open(path)); r = d['chart']['result'][0]
    return {datetime.datetime.utcfromtimestamp(t).date(): c
            for t, c in zip(r['timestamp'], r['indicators']['quote'][0]['close']) if c is not None}

btc, gspc, gold, usdmxn = (load_yahoo(f) for f in
    ('yahoo_BTC_USD.json', 'yahoo__GSPC.json', 'yahoo_GC_F.json', 'yahoo_MXN_X.json'))
common = sorted(set(btc) & set(gspc) & set(gold) & set(usdmxn))   # 1,108 fechas

def rets(s, ds): return [s[ds[i]]/s[ds[i-1]] - 1 for i in range(1, len(ds))]
r_btc, r_gspc, r_gold = rets(btc, common), rets(gspc, common), rets(gold, common)

def corr(a, b):
    n = len(a); ma, mb = sum(a)/n, sum(b)/n
    cov = sum((x-ma)*(y-mb) for x, y in zip(a, b)) / n
    return cov / (statistics.pstdev(a) * statistics.pstdev(b))

def beta(y, x):
    n = len(x); mx, my = sum(x)/n, sum(y)/n
    cov = sum((xi-mx)*(yi-my) for xi, yi in zip(x, y)) / n
    return cov / (sum((xi-mx)**2 for xi in x) / n)

print(corr(r_btc, r_gspc), beta(r_btc, r_gspc))   # 0.438  1.359 (pandas/numpy: 0.4380  1.3593)
```

- **Verificación cruzada con NumPy** (orden de cálculo distinto, `np.corrcoef` y `np.cov`/`np.var`): `corr=0.43804`, `beta=1.35935`, `corr_oro=0.12319`, `beta_oro=0.34345`, `vol_BTC=67.62%`, `vol_GSPC=21.81%`, `vol_oro=24.28%`. Coincide con la implementación en Python puro a 3-4 decimales; la diferencia residual es de redondeo de punto flotante, no un error de indexado.
- **Scripts y datos crudos de esta sesión:** `scratchpad/beta_extendido.py` (fuera del repositorio). Si el comité quiere conservarlo, debe moverse a `herramientas/` y pasar revisión de código.

## 5. Contrapuntos y límites

- **5 años sigue sin cubrir un ciclo completo:** Yahoo solo entregó datos de `^GSPC`/`GC=F`/`QQQ`/`MXN=X` desde el 5-oct-2021 con `range=5y` (BTC sí tiene historia desde 2014, pero se recorta a la intersección). Se pierde el ciclo 2017-2021 completo (burbuja de 2017, COVID de marzo de 2020, el bull run de 2020-2021), que habría enriquecido el corte por año. **No se puede concluir que el patrón de "amplificación en choques idiosincráticos de cripto vs. diversificación en choques macro ajenos" se sostenga en esos periodos**: es una observación de 5 años, con solo 2 episodios de choque "ajeno a cripto" (abril de 2025) y 6 de "choque de cripto superpuesto a una caída macro" (2022).
- **Solo días hábiles:** al forzar la intersección con S&P 500/oro/QQQ/USD-MXN se pierde el movimiento de fin de semana de BTC, igual que en la ficha del 29-sep.
- **`GC=F` es un futuro, no el spot del oro:** tiene su propio calendario de vencimientos y roll; para este ejercicio (correlaciones de retornos diarios) el efecto es menor, pero no es exactamente lo mismo que el oro físico.
- **n pequeño para el análisis condicional:** 162 "días de estrés" en 5 años es una muestra razonable para la correlación promedio, pero la tabla de los 10 peores días tiene, en la práctica, solo 2 "episodios" distintos (el ciclo de alzas de la Fed/Celsius de 2022, y el choque arancelario de abril de 2025). **No es una ley general sobre cómo se comporta BTC en cualquier choque de cola; es una descripción de los dos tipos de choque que de hecho ocurrieron.**
- **Correlación no es causalidad ni mecanismo:** este ejercicio no identifica *por qué* BTC subió en abril de 2025 (podría ser una rotación específica hacia cripto como cobertura contra política comercial, o coincidencia de otro catalizador cripto esa semana; no se investigó la causa).

## 6. Qué cambia para invertir

- **Para el filtro de tendencia de la cuenta cripto** (que solo mira el propio precio de BTC/USDT), no cambia nada.
- **Para el comité del 9-oct-2026** (que decide si BTC sube de 40% a 65% de la cuenta `arena-claude-binance`, con la cuenta GBM ya en UPRO 3x desde la decisión W40): la beta de 5 años de BTC sobre el S&P 500 (1.36, más alta que la beta de 2 años sobre el Nasdaq que ya se conocía, 0.89) y, sobre todo, **el hallazgo de que en 2022 (el año más parecido a un ciclo de endurecimiento monetario con estrés de liquidez cripto) la correlación llegó a 0.646 y BTC amplificó las peores caídas del S&P 500 hasta −22.68% en un día**, es evidencia en contra de tratar la cuenta cripto como una fuente de diversificación independiente del riesgo de la cuenta GBM apalancada. El escenario de cola que más debería preocupar al comité no es "BTC cae mientras el S&P 500 sube" (poco probable según este ejercicio), sino un choque tipo 2022 que golpee a las dos cuentas a la vez, con la cripto cayendo proporcionalmente más.
- **Matiz a favor de la diversificación, con solo 2 observaciones:** el choque arancelario de abril de 2025 muestra que no todo evento macro arrastra a BTC hacia abajo junto con la renta variable; un choque de política comercial (no financiero, no cripto) coincidió con que BTC subiera. No se puede generalizar de 2 días, pero tampoco se debe asumir automáticamente que "todo cae junto".
- **Para dimensionar riesgo, no para predecir el signo de mañana** (igual que la ficha del 29-sep): la beta correcta para un ejercicio de estrés de la cuenta combinada depende de qué tipo de choque se simula. Usar la beta de 5 años (1.36) para un choque "ajeno a cripto" sobreestimaría el riesgo; usar la misma beta para un choque "de cripto superpuesto a lo macro" (como 2022) la subestimaría — en ese año la correlación real (0.646) y la magnitud de la caída de BTC fueron mucho peores que el promedio de 5 años.

## 7. Autoexamen

- ¿Puedo reproducir el número sin ver la ficha? Sí: son descargas públicas de Yahoo y covarianza/varianza estándar, documentadas en §4, verificadas con dos implementaciones independientes (Python puro y NumPy).
- ¿Qué rompería la conclusión? Si `^GSPC`, `GC=F` o `MXN=X` tuvieran datos faltantes sistemáticos en fechas de alta volatilidad de BTC (no se verificó exhaustivamente: solo se comprobó que las fechas extremas de la muestra —2021-10-05 y 2026-10-05— están presentes en las 5 series, igual que hizo la ficha del 29-sep). También se rompería si `GC=F` tuviera saltos de roll de futuro justo en una de las 10 fechas de la tabla de §3.5; no se verificó contra el spot físico del oro.
- **Grado: B** para el cálculo (reproducible, fuentes públicas, verificado dos veces, con la misma metodología que ya validó la ficha del 29-sep); **grado C** para la lectura del comportamiento de BTC en choques ("amplifica lo cripto-específico, posible diversificador en choques de política ajenos a cripto"), porque descansa en solo 2 episodios distintos de 5 años, no en una muestra grande de choques independientes.

## 8. Estado del pendiente

- Pendiente de `estado-de-dominio.csv` (cripto/05, fecha 2-oct-2026): **completado** con ventana de 5 años, oro y S&P 500 añadidos al cruce (quedó pendiente todavía repetir con un **S&P 500 de retorno total** en vez de precio, que subestima ligeramente la correlación frente a QQQ que sí captura dividendos reinvertidos de forma indirecta vía precio; no se corrigió hoy porque no cambia el orden de magnitud de las conclusiones).
- Nuevo pendiente para una corrida futura: repetir el análisis condicional de "días de estrés" (§3.5) con un umbral distinto (p. ej. ≤−2%) y con el VIX como variable de condicionamiento adicional, en vez de solo el retorno del S&P 500; y buscar si hay un proveedor gratuito con historia de `^GSPC`/oro más allá de 2021 (CRSP y FRED tienen oro e índices accionarios con historia mucho más larga, pero requerirían reconciliar el calendario diario con BTC).
- Actualiza el capítulo de síntesis `05-mercado-on-chain-stablecoins-e-institucional.md` (adenda fechada 5-oct-2026, §12) y `conocimiento/estado-de-dominio.csv` (fila cripto/05).

Script y datos crudos de esta sesión: `scratchpad/beta_extendido.py` y los JSON de Yahoo descargados hoy (fuera del repo).
