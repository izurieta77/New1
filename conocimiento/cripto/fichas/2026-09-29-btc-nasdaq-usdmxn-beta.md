# Ficha de avance · 29-sep-2026 · G5 Mercado (BTC frente a Nasdaq, USD/MXN y tasa real, medido en MXN)

> Corrida de las 08:17 CDMX (14:17 UTC), `analista-cripto`. Toma el **tema 3** de la lista "Temas que no cubren los 35 recursos y que el torneo necesita" (`00-plan-de-estudio.md`, §"Temas que no cubren..."): *"BTC frente a tasa real, Nasdaq y USD/MXN. Betas y correlaciones, medidas en MXN"*. No tenía ficha propia todavía: el capítulo `05-mercado-on-chain-stablecoins-e-institucional.md` solo citaba correlaciones de terceros (a16z, Coinbase) en su idea #6, sin cálculo propio ni versión en MXN. Motivado además por el movimiento de hoy: BTC bajó a ~US$83,000 (−1.1 a −1.4% en 24h) mientras el rendimiento del Treasury a 10 años tocó su nivel más alto desde 2007, el dólar se fortaleció y el petróleo subió por el pesimismo renovado sobre Irán ([CoinDesk](https://www.coindesk.com/markets/2026/09/29/bitcoin-holds-usd83-000-as-zec-drops-12-and-oil-climbs-again), [Rio Times](https://www.riotimesonline.com/crypto-markets-bitcoin-majors-tuesday-september-29-2026/)).

## 1. Acceso real

- **Datos de precio:** Yahoo Finance, endpoint `chart` v8 (`query1.finance.yahoo.com/v8/finance/chart/<símbolo>?range=2y&interval=1d`), sin clave. Símbolos: `BTC-USD`, `QQQ` (proxy líquido y barato del Nasdaq-100, el mismo tipo de instrumento que ya usa este sistema para la cuenta GBM) y `MXN=X` (USD/MXN). Acceso **íntegro** a los cierres diarios de los últimos 2 años de los tres símbolos.
- **Tasa real:** FRED, serie `DFII10` (rendimiento real del Treasury a 10 años, TIPS), vía `fredgraph.csv`, sin clave. Acceso **íntegro** a toda la serie desde 2003 (5,938 observaciones).
- Nada de esto es información privilegiada: son precios de mercado público y una serie oficial de la Fed de St. Louis.

## 2. Metodología (declarada antes de ver el resultado final, salvo el primer corte exploratorio de datos)

1. Cargar cierres diarios de `BTC-USD`, `QQQ` y `MXN=X` de los últimos 2 años (rango pedido a Yahoo).
2. Quedarse con las **fechas comunes a los tres símbolos** (BTC cotiza los 7 días; QQQ y USD/MXN solo entre semana, así que el cruce fuerza a usar solo días hábiles bancarios de EUA). **Límite declarado:** esto descarta el movimiento de BTC de fin de semana, que es real y a veces grande (el filtro de tendencia de la cuenta sí lo usa). El ejercicio de hoy mide la relación entre-semana, no el movimiento de 7 días de BTC.
3. Construir versiones en MXN: `BTC_MXN = BTC_USD × USDMXN`, `QQQ_MXN = QQQ_USD × USDMXN`.
4. Calcular retornos diarios simples de las 5 series (BTC-USD, BTC-MXN, QQQ-USD, QQQ-MXN, USD/MXN).
5. Reportar: (a) correlación y beta de mínimos cuadrados (BTC como variable dependiente, Nasdaq como independiente) en la muestra completa, en USD y en MXN; (b) correlación y beta **rodantes de 90 días** para ver si el régimen se mueve, con la ventana de hoy comparada contra su mediana e historia; (c) un corte de los **últimos 30 días** para contrastar con el régimen de hoy; (d) correlación de BTC con el cambio diario del nivel de `DFII10` (tasa real), en la muestra completa y en los últimos 90 días, para acercarse al tercer eje del tema ("tasa real").
6. **Verificación doble:** el cálculo de correlación y beta se implementó con fórmulas de covarianza/varianza en Python puro (sin librerías de estadística), y se corrió dos veces con reordenamientos distintos del código para confirmar que no había un error de indexado; los números coinciden.

## 3. Resultados

### 3.1 Muestra completa (444 días hábiles comunes, 2024-09-30 a 2026-09-29)

| Par | Correlación | Beta (BTC sobre el otro activo) |
|---|---|---|
| BTC(USD) – QQQ(USD) | **0.424** | **0.886** |
| BTC(MXN) – QQQ(MXN) | **0.441** | **0.936** |
| BTC(USD) – retorno USD/MXN | **−0.066** | **−0.296** |

- Medir en MXN (en vez de en USD) sube un poco la correlación y la beta con el Nasdaq (0.424→0.441; 0.886→0.936): la variación cambiaria entre el peso y el dólar añade un poco de covarianza extra entre los dos activos, porque ambos se convierten con el mismo tipo de cambio.
- La relación entre BTC y el USD/MXN es débil en la muestra completa (correlación de solo −0.066): no hay un "acoplamiento" fuerte y estable de BTC con la fortaleza del dólar frente al peso, distinto de la correlación BTC-DXY que reportó la ficha del 28-sep-2026 como inestable pero más marcada en algunos tramos (hasta −0.90).

### 3.2 Correlación y beta rodantes de 90 días (régimen cambia, no es una constante)

| Métrica | Última ventana (29-sep-2026) | Mediana histórica | Mínimo | Máximo |
|---|---|---|---|---|
| Correlación BTC(USD)-QQQ(USD) | **0.322** | 0.491 | 0.142 (25-sep-2025) | 0.601 (15-abr-2025) |
| Beta BTC(USD) sobre QQQ(USD) | **0.602** | 1.046 | 0.293 | 1.857 |
| Correlación BTC(USD)-retorno USD/MXN | **−0.221** | −0.096 | −0.519 | +0.206 |

- **La correlación con el Nasdaq nunca fue negativa** en las 355 ventanas rodantes calculadas (mín. 0.142): a diferencia de BTC-DXY (que sí cambia de signo, según la ficha del 28-sep), BTC-Nasdaq se ha mantenido positivo todo el periodo, aunque con magnitud muy variable (de "casi nulo" a "moderado").
- Hoy la correlación (0.322) y sobre todo la beta (0.602) están **por debajo de su mediana histórica** de los últimos 2 años: BTC se está moviendo menos en sintonía con el Nasdaq que en el tramo típico de la muestra, pese a que ambos bajaron hoy por el mismo canal macro (tasas y dólar).
- La correlación con el retorno del USD/MXN se ha vuelto **más negativa que su mediana histórica** (−0.221 contra −0.096): en el tramo reciente, un peso que se deprecia (USD/MXN sube) coincide algo más con caídas de BTC que en el resto de la muestra, coherente con la lectura de hoy (dólar fuerte, BTC débil), pero la relación completa (−0.519 a +0.206) confirma que **no es un parámetro estable para apostar**.

### 3.3 Últimos 30 días (el régimen "de esta semana")

- Correlación BTC-QQQ: **0.454**; beta: **1.580** (bien por encima de la mediana de 2 años, 1.046: en las últimas semanas, cada 1% de movimiento del Nasdaq vino acompañado, en promedio, de ~1.58% de movimiento de BTC en la misma dirección — un régimen de "beta alta", no solo de correlación media).
- Correlación BTC-USD/MXN: **−0.219**, en línea con la ventana rodante de 90 días.
- Volatilidad anualizada de BTC en estos 30 días: **67.8%**, contra 56.8% de la muestra completa de 2 años y 27.2% de QQQ. BTC sigue siendo mucho más volátil que el Nasdaq incluso en los tramos donde se mueve "junto" con él.

### 3.4 Tasa real (DFII10) y BTC

- `DFII10` subió de **2.18% (19-may-2026)** a **2.83% (25-sep-2026, último dato de FRED disponible; hay 2-4 días de rezago de publicación)**, +65 puntos base en ~90 observaciones — el mismo periodo en el que la prensa de hoy reporta que el rendimiento nominal a 10 años "tocó su nivel más alto desde 2007".
- Correlación entre el **cambio diario** de `DFII10` (en puntos porcentuales) y el **retorno diario** de BTC:
  - muestra completa (497 días comunes, 2024-09-30 a 2026-09-25): **−0.005** (prácticamente nula);
  - últimos 90 días: **−0.232** (débil, negativa, consistente con "sube la tasa real, baja BTC", pero con n=90 y sin robustez fuera de esa ventana).
- **Lectura aplicada:** el canal "tasa real más alta presiona a BTC" que dominó la cobertura de prensa de hoy es **plausible y tiene el signo correcto en el tramo reciente**, pero no es una relación estable en la historia de 2 años (correlación completa ≈ 0). Es el mismo patrón de inestabilidad de régimen que ya documentó la ficha del 28-sep-2026 para BTC-DXY: el canal aparece y desaparece en ventanas de meses, no es un parámetro que se pueda fijar para el pronóstico.

## 4. Verificación numérica (script)

```python
# beta_analysis.py — verificado dos veces, mismos resultados
def load_yahoo(path):
    d = json.load(open(path)); r = d['chart']['result'][0]
    return {datetime.datetime.utcfromtimestamp(t).date(): c
            for t, c in zip(r['timestamp'], r['indicators']['quote'][0]['close']) if c is not None}

btc, qqq, usdmxn = load_yahoo('btc.json'), load_yahoo('qqq.json'), load_yahoo('usdmxn.json')
common = sorted(set(btc) & set(qqq) & set(usdmxn))          # 444 fechas
btc_mxn = {d: btc[d]*usdmxn[d] for d in common}
qqq_mxn = {d: qqq[d]*usdmxn[d] for d in common}

def rets(s, ds): return [s[ds[i]]/s[ds[i-1]] - 1 for i in range(1, len(ds))]
r_btc, r_qqq, r_fx = rets(btc, common), rets(qqq, common), rets(usdmxn, common)

def corr(a,b):
    n=len(a); ma,mb=sum(a)/n, sum(b)/n
    cov=sum((x-ma)*(y-mb) for x,y in zip(a,b))/n
    return cov/(statistics.pstdev(a)*statistics.pstdev(b))

def beta(y,x):
    n=len(x); mx,my=sum(x)/n, sum(y)/n
    cov=sum((xi-mx)*(yi-my) for xi,yi in zip(x,y))/n
    return cov/(sum((xi-mx)**2 for xi in x)/n)

print(corr(r_btc, r_qqq), beta(r_btc, r_qqq))   # 0.424  0.886
```

**Resultado de la corrida completa** (script `scratchpad/g5_beta/beta_analysis.py` de esta sesión, fuera del repo; datos crudos también en el scratchpad): reproduce exactamente los números de §3.1-§3.3. El cruce con `DFII10` está en la misma carpeta.

## 5. Contrapuntos y límites

- **n corto:** solo 2 años de datos diarios (~444-497 observaciones efectivas por par); no cubre un ciclo completo de tasas (p. ej., el periodo de tasa cero 2020-2021). Grado B para el cálculo, no A, por la ventana corta.
- **Solo días hábiles:** al forzar la intersección con QQQ y USD/MXN se pierde el ~28% de las observaciones de BTC (fines de semana), que es precisamente cuando BTC se mueve solo, sin que el Nasdaq pueda "confirmar o negar" nada. La correlación reportada es la de "cuando ambos mercados están abiertos", no la correlación de 7 días.
- **QQQ como proxy del Nasdaq:** es un ETF con su propio costo y ligero tracking error frente al índice NDX puro; para este ejercicio la diferencia es irrelevante (no se busca la cuarta cifra decimal).
- **Inestabilidad de régimen confirmada, no resuelta:** igual que con BTC-DXY (ficha del 28-sep), ninguna de estas betas o correlaciones es un parámetro fijo. El hallazgo central de este ejercicio es que **hoy, con una caída conjunta de BTC y Nasdaq y una tasa real subiendo, la correlación y la beta con el Nasdaq están de hecho por debajo de su mediana de 2 años**, mientras que la relación con la tasa real solo aparece en la ventana corta reciente. Esto es un dato en contra de narrativas simples de "todo cae junto por lo mismo": el canal más fuerte hoy no es el que domina el promedio histórico.
- **No se usa para apalancar ni para predecir el signo de mañana.** Sirve para dimensionar riesgo (BTC puede moverse 1.5-1.9× el Nasdaq en tramos de "beta alta" como el actual) y para no asumir una beta de 1.0 fija en ningún ejercicio de la cuenta `arena-claude-binance` o de la cuenta combinada.

## 6. Qué cambia para invertir

- Para el filtro de tendencia de la cuenta cripto (que solo mira el propio precio de BTC/USDT), **no cambia nada**: el filtro sigue ENCENDIDO hoy con SMA200 = 71,173.97 (ver sección de reconfirmación de esta misma corrida).
- Para leer el día de hoy: la caída de BTC (~−1.1 a −1.4%) es consistente en dirección con la caída del Nasdaq y la suba de tasas reales, pero **la magnitud de acoplamiento de hoy no está fuera de lo normal** (beta rodante de 90 días de 0.602, por debajo de la mediana); no hay evidencia de un "régimen de pánico correlacionado" excepcionalmente alto hoy.
- Para el comité: si en algún momento se considera cubrir la cuenta combinada (GBM + Binance) contra un mismo choque macro (tasas/dólar), la beta de BTC sobre el Nasdaq de los últimos 30 días (1.58) es mayor que la de 2 años (0.89): usar la beta de largo plazo subestimaría el riesgo de un episodio como el de hoy.

## 7. Autoexamen

- ¿Puedo reproducir el número sin ver la ficha? Sí: son tres descargas públicas y una covarianza/varianza estándar, documentadas en la sección 4.
- ¿Qué rompería la conclusión? Si QQQ o USD/MXN tuvieran datos faltantes sistemáticos en fechas de alta volatilidad de BTC (no verificado exhaustivamente, solo se comprobó que las 444/497 fechas comunes cubren el rango completo sin huecos visibles al inspeccionar las fechas extremas).
- **Grado: B** para el cálculo (reproducible, fuentes públicas, verificado dos veces); **grado C** para su uso como señal predictiva (el hallazgo central es precisamente que el régimen no es estable, igual que ya advertía el capítulo 05 en su idea #6).

## 8. Estado del pendiente

- Tema 3 de "Temas que no cubren los 35 recursos" (`00-plan-de-estudio.md`): **iniciado con ejercicio numérico propio y verificado.** Pendiente para una corrida futura: extender la ventana más allá de 2 años en cuanto haya presupuesto de tiempo (Yahoo permite `range=5y` o `max`), y repetir el cruce con el oro (para completar el trío BTC-Nasdaq-oro que citan a16z y Coinbase en el capítulo 05) y con el S&P 500 en vez de solo Nasdaq.
- Actualiza el capítulo de síntesis `05-mercado-on-chain-stablecoins-e-institucional.md` (adenda fechada 29-sep-2026) y `conocimiento/estado-de-dominio.csv` (fila `cripto/05`).

Script y datos crudos de esta sesión: `scratchpad/g5_beta/` (fuera del repo; si el dueño quiere conservarlos, conviene moverlos a `herramientas/`).
