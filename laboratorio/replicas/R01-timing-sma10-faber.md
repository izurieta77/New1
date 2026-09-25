# Réplica R01: timing con media móvil de 10 meses (Faber) sobre el mercado accionario de EUA

| Campo | Valor |
|---|---|
| ID | `R01` (el registro de variantes es `replicas/R01-variantes.csv`; el nombre largo del archivo es `R01-timing-sma10-faber`) |
| Artículo o hallazgo | Faber, Mebane T. (2007), "A Quantitative Approach to Tactical Asset Allocation", *The Journal of Wealth Management* 9(4): 69-79, primavera de 2007, DOI 10.3905/jwm.2007.674809. Working paper en SSRN 962461. Versiones consultadas: (a) working paper de julio de 2006 (https://www.trendfollowing.com/whitepaper/CMT-Simple.pdf, 13 páginas) y (b) actualización de febrero de 2013 (https://mebfaber.com/wp-content/uploads/2016/05/SSRN-id962461.pdf, 70 páginas). La versión de la revista **no** se leyó (tiene muro de pago). |
| Fecha de publicación (primera versión pública) | Working paper de 2006 (la portada de 2013 dice "May 2006"; el PDF de 2006 dice "July 2006"). Revista: primavera de 2007. |
| Pre-registro escrito el | 2026-09-25, alrededor de las 05:21 UTC, **antes de cualquier corrida de backtest**. Antes de escribirlo solo se descargaron los datos y se revisaron metadatos (versión, rango y faltantes). No se calculó ninguna métrica de ninguna regla. |
| Responsable | Claude (laboratorio de réplicas, fase 0). Mandato: Eduardo Iván Izurieta Martínez |
| Estado | **Replicado con diferencias** (2026-09-25). Veredicto fuera de muestra: **"Se sostiene"**, con matices en la sección 14 |

---

## PRE-REGISTRO (secciones 1 a 9; no se editan después de la primera corrida)

### 1. Hipótesis previa y mecanismo

**Resultado declarado en el artículo.** Lo verifiqué hoy en los PDF, extrayendo el texto con pypdf.

*Working paper de 2006.* Tabla 2, p. 4: "S&P 500 total returns and timing total returns, 1900-2005". Datos mensuales, rendimiento total de Global Financial Data, sin impuestos, comisiones ni deslizamiento. El efectivo es papel comercial a 90 días.

| Métrica | S&P 500 | Timing (SMA de 10 meses) |
|---|---|---|
| CAGR | 9.75% | 10.66% |
| Desviación estándar | 19.91% | 15.38% |
| Sharpe (anual, rf = 4%) | 0.29 | 0.43 |
| Drawdown máximo | (83.66%) | (49.98%) |
| MAR | 0.14 | 0.23 |
| Ulcer Index | 20.33% | 11.70% |
| % del tiempo en el mercado | 100.00% | 69.77% |
| Idas y vueltas por año | – | 0.67 |
| % de operaciones positivas | – | 63% |
| Mejor año | 52.88% | 52.40% |
| Peor año | (43.86%) | (26.69%) |

Texto de las pp. 3-4 del mismo documento:

- Media aritmética anual: 11.66% (índice) contra 11.72% (timing).
- El timing queda por debajo del índice en "roughly 40%" de los años.
- La misma p. 4 dice que el drawdown bajó "from a catastrophic -83.66% to -42.24%". **Eso contradice el 49.98% de su propia Tabla 2.** Es una discrepancia interna de la fuente y no está explicada.

*Actualización de 2013.* pp. 22-24, S&P 500 de 1901 a 2012:

- Media aritmética: 11.26% contra 11.22%.
- CAGR: 9.32% contra 10.18%.
- Drawdown máximo: 83.66% contra 42.24%.
- Invertido "approximately 70%" del tiempo, con "less than one round-trip trade per year".
- Queda por debajo del índice en "roughly half of all years".
- La tabla de la Figura 7 es una imagen: no se extrajo.

*Regla del artículo.* "Buy when monthly price > 10-month SMA. Sell and move to cash when monthly price < 10-month SMA". Entrada y salida al cierre del día de la señal, el último día del mes. Series de rendimiento total.

**Hipótesis (previas a correr).**

- **H1, drawdown, efecto principal.** En el tramo que se traslapa con el artículo (1927-07 a 2005-12, sin costos), la SMA de 10 meses reduce el drawdown máximo del mercado entre 30% y 60% en términos relativos. El artículo reporta 40.3% según su Tabla 2 y 49.5% según su texto y la versión de 2013.
- **H2, CAGR.** En el mismo tramo y sin costos, el CAGR del timing supera al de comprar y mantener por 0 a 1.9 pp. El artículo reporta +0.91 pp.
- **H3, riesgo-rendimiento dentro de muestra y neto de costos GBM.** El Sharpe del timing (exceso sobre la T-bill) es mayor que el de comprar y mantener.
- **H4, fuera de muestra, 2007-01 a 2026-07, después de la publicación.** Mi expectativa previa es que la reducción del drawdown persista, sobre todo por 2008-2009, y que el CAGR neto quede **por debajo** de comprar y mantener por 0.5 a 2.5 pp. Las razones son las recuperaciones en V (2009 y 2020) y los latigazos (2011, 2015-2016, 2018 y 2022). La literatura del capítulo 14 (Zakamulin) reporta que, sin look-ahead y con costos, el rendimiento es estadísticamente indistinguible del de comprar y mantener. Sobre el Sharpe fuera de muestra no tengo expectativa direccional firme: espero algo parecido al de comprar y mantener.

**Mecanismo económico.** Hay tres candidatos, que no se excluyen entre sí:

1. **Agrupamiento de volatilidad y efecto apalancamiento.** Los meses con el índice bajo su media de 10 meses tienden a coincidir con regímenes de volatilidad alta y peor relación entre riesgo y rendimiento. Salir en esos regímenes reduce la varianza y el castigo geométrico (≈ σ²/2) más de lo que reduce la media.
2. **Subreacción y difusión lenta de la información** (tendencia de series de tiempo).
3. **Lectura de fin de ciclo.** Las grandes caídas acompañan recesiones que se desarrollan en meses, no en días.

**Por qué no se arbitra.** No es dinero gratis. Cambia potencial de subida por protección en la cola izquierda. Tiene un costo de seguimiento (queda por debajo del índice en ~40-50% de los años) y riesgo de carrera, y su pago se concentra en eventos raros.

**Hipótesis alternativa que compite.** El 10 se eligió mirando el pasado: es el equivalente mensual de la media de 200 días de Siegel, probada sobre la misma historia. Por eso se registran las longitudes vecinas y se deflacta el Sharpe.

### 2. Criterio de refutación

**Métrica principal.** Es la reducción relativa del drawdown máximo, 1 − MDD_timing / MDD_B&H, de la SMA de 10 meses contra comprar y mantener. Las métricas secundarias son:

- La diferencia de CAGR.
- El Sharpe del exceso sobre la T-bill (mensual y anualizado, métrica `sharpe` del motor).
- El tiempo invertido.
- Las idas y vueltas por año.

**Tolerancias para "Replicado".** Se evalúan en el tramo 1927-07 a 2005-12, sin costos, que es el del artículo. Deben cumplirse las cuatro:

| # | Criterio | Rango aceptado | Cifra del artículo |
|---|---|---|---|
| C1 | Reducción relativa del MDD | entre 0.30 y 0.60 | 0.403 (Tabla 2) o 0.495 (texto y 2013) |
| C2 | CAGR del timing menos CAGR de comprar y mantener | mayor que 0 y hasta +1.91 pp (+0.91 ± 1.00 pp, mismo signo) | +0.91 pp |
| C3 | Fracción del tiempo invertido | entre 0.60 y 0.80 | 0.6977 |
| C4 | Idas y vueltas por año (salidas de 1 a 0 por año) | entre 0.40 y 1.00 | 0.67 |

**Resultado que refuta la hipótesis ("No replicado").** Basta cualquiera de estas condiciones, medida en el segmento `dentro_muestra` (1927-07 a 2006-12), **neto** de los costos por defecto de GBM:

- a) La reducción relativa del MDD de la SMA de 10 meses es menor que 0.20.
- b) El Sharpe de la SMA de 10 meses es menor o igual que el de comprar y mantener.

**"Replicado con diferencias".** Aplica cuando no se cumple la refutación y C1 se cumple, pero falla alguno de C2, C3 o C4. También aplica si el efecto aparece solo en algunos subperiodos. Si falla C1 sin llegar a la refutación (reducción entre 0.20 y 0.30, o mayor que 0.60), también se clasifica como "con diferencias".

**Interpretación sobre los datos, fijada de antemano.** Usar el mercado CRSP de French (1926-) en lugar del S&P 500 de Global Financial Data (1900-) se trata como una **diferencia de datos explicada**, no como "requiere datos distintos". La regla es idéntica, el mercado es el mismo (EUA, capitalización) y el artículo afirma que la regla generaliza a más de 20 mercados. Esta decisión queda fija aquí y no se revisa después de ver resultados.

**Veredicto fuera de muestra, post-publicación.** Se mide en 2007-01 a 2026-07, neto de costos por defecto y con la SMA de 10 meses:

| Veredicto | Condición |
|---|---|
| "Se sostiene" | Reducción relativa del MDD ≥ 0.20 **y** Sharpe ≥ Sharpe de comprar y mantener |
| "Solo protección" | Reducción ≥ 0.20, pero Sharpe < el de comprar y mantener |
| "No se sostiene" | Reducción < 0.20 |

**Sharpe deflactado.** `sharpe_deflactado_de_registro("R01", segmento="dentro_muestra", variante="sma10")` usa N igual al número de variantes con `es_prueba=1` (5). Como sensibilidad se usa también N = 20, que representa la búsqueda de la literatura: el artículo de 2013 muestra longitudes de 3 a 12 meses, y se suma la familia de momentum. Umbral: 0.95 (`config/parametros.json`).

Advertencia fijada de antemano: el DSR contrasta el Sharpe del exceso sobre el efectivo contra 0, **no** contra comprar y mantener. Por eso se agrega una prueba de la diferencia mensual de rendimientos netos (SMA 10 menos comprar y mantener): media con error estándar Newey-West de 6 rezagos (`herramientas/estadistica.py`) en cada segmento.

**Cómo se traduce a la conclusión operable.** La regla afectada es R1 del capítulo 14 (`conocimiento/14-analisis-tecnico-que-sobrevive.md` §6.1): filtro de SMA de 10 meses sobre el índice total return, evaluación mensual y salida a CETES.

- **Se confirma** como filtro de riesgo si el estado es Replicado o Replicado con diferencias, el veredicto fuera de muestra es "Se sostiene" y el DSR de la SMA de 10 meses es ≥ 0.95.
- **Se modifica** si el estado es Replicado o Replicado con diferencias y el veredicto es "Solo protección". En ese caso se mantiene solo como control de drawdown o régimen, con su costo esperado en CAGR declarado, y nunca como fuente de rendimiento. Lo mismo aplica si el veredicto es "Se sostiene" pero el DSR es < 0.95.
- **Se descarta** si el estado es No replicado o el veredicto fuera de muestra es "No se sostiene".

En cualquier caso, ninguna regla pasa a dinero sin los requisitos de la sección 1 del README del laboratorio: papel durante 3 meses y 30 operaciones.

### 3. Datos y licencia

| Serie | Fuente y archivo | Versión / huella | Frecuencia | Condiciones de uso |
|---|---|---|---|---|
| Mercado (Mkt-RF + RF) y RF, **principal** | French, `F-F_Research_Data_Factors_CSV.zip`, caché de `herramientas/datos_historicos.py` | CRSP 202607, sha256 `b840dba55d319f4818fc7300e65c52eff5f64870c8d495fa58ff5d4cd749f5eb`, caché del 2026-09-25T05:11:58Z; 1926-07-31 a 2026-07-31, 1201 meses, 0 faltantes | mensual | La página dice "Copyright Eugene F. Fama and Kenneth R. French", verificado hoy. Otras condiciones: pendientes de verificar |
| Mercado y RF, vintage **2024** | French, archivo histórico "08 2024 Update", `F-F_Research_Data_Factors_CSV.zip` (formato Legacy FIZ) | CRSP 202407; sha256 se registra en la corrida; 1926-07 a 2024-07 | mensual | Igual que la anterior |
| Mercado y RF, vintage **2006** | French, archivo histórico "08 2006 Update", `F-F_Research_Data_Factors_TXT.zip` (TXT; se convierte a CSV) | CRSP 200607; sha256 se registra en la corrida; 1926-07 a 2006-07 | mensual | Igual que la anterior |
| S&P 500, índice de **precio** (solo sensibilidad de la señal) | Yahoo chart v8 `^GSPC`, diario, a través de `yahoo_historia` | Hash de la serie en la corrida | diario, llevado a cierre de mes | Pendiente de verificar |
| MXN por USD (solo sensibilidad de moneda) | FRED `DEXMXUS` | Fecha de descarga en la corrida | diario | Pendiente de verificar |
| Tasa de Cetes, aproximación (solo sensibilidad de moneda) | FRED `INTGSTMXM193N` (IMF IFS, Treasury Bill Rate de México, % anual) | Fecha de descarga en la corrida | mensual | Pendiente de verificar |

**Cambio de formato de French, verificado hoy en la Data Library.** Desde la publicación de enero de 2025, French usa los archivos CRSP Flat File Format 2.0 (CIZ) en lugar de Legacy (FIZ). Según su nota: "In the new Flat File Format (CIZ), monthly returns are compounded daily returns with dividends reinvested on their ex-dates", mientras que en FIZ se reinvertían al fin de mes. Los datos también se revisan de un vintage a otro. Por ejemplo, Mkt-RF de 1926-07 vale 2.62% en el vintage 200607, 2.96% en el 202407 y 2.89% en el 202607. Por eso se corre la sensibilidad de vintages.

### 4. Universo

Un solo activo de riesgo: el mercado accionario de EUA ponderado por capitalización, según la construcción de French con CRSP (NYSE, AMEX y NASDAQ). **No** es el S&P 500 del artículo.

- **Sesgo de supervivencia:** no hay, porque CRSP incluye las emisoras deslistadas.
- **Invertibilidad:** el portafolio de mercado no era invertible como fondo antes de los años setenta. Hoy lo aproximan ETFs de mercado total o del S&P 500 listados en el SIC.
- **Activo libre de riesgo:** RF de French (T-bill a 1 mes; Ibbotson hasta 202405 e ICE BofA desde 202406). El artículo usa papel comercial a 90 días (2006) y T-bills a 90 días (2013).

### 5. Fecha de disponibilidad

- **Estructura del motor.** La señal para el mes *t* se decide al cierre del mes *t-1* y solo ve el índice hasta *t-1*: `Historia` son vistas truncadas.
- **Ejecución.** El artículo ejecuta al cierre del mismo día de la señal. Es un supuesto optimista, porque hay que conocer el cierre para calcular la señal. El motor reproduce ese supuesto. Como cota del efecto de un retraso de ejecución se corre la sensibilidad de **rezago de 1 mes** (decidir *t* con datos hasta *t-2*). Un rezago de 1 día **no** se puede probar con datos mensuales: queda pendiente con los datos diarios de French.
- **Rezago de publicación.** French publica con 1 o 2 meses de rezago. En tiempo real, el nivel de fin de mes de un índice total return sí se conoce al cierre, así que el rezago de publicación no afecta la regla. Lo que sí la afecta son las **revisiones** de los datos, y por eso se corre la sensibilidad con el vintage 200607, disponible en agosto de 2006.
- **Series externas.** `^GSPC` (sensibilidad de la señal) y `DEXMXUS` entran como `extras` y `fx` del motor: solo son visibles las entradas con fecha ≤ la fecha de *t-1*. La tasa de Cetes solo se usa como rendimiento del efectivo, no en la señal.

### 6. Periodo

- **Periodo del artículo:** 1900-2005 (working paper de 2006) y 1901-2012 (actualización de 2013).
- **Periodo propio total:** los datos empiezan en 1926-07. Con `min_historia = 12` para **todas** las variantes (el mismo inicio para 6, 8, 10 y 12 meses), la primera decisión es para 1927-07, la curva arranca en 1927-06-30 y la última observación es 2026-07.
- **Corte:** uno, en 2006-12-31.
  - `dentro_muestra`: 1927-07 a 2006-12.
  - `fuera_muestra`: 2007-01 a 2026-07, después de la publicación (revista, primavera de 2007).
  - Las primeras ventanas de 2007 usan datos de 2006. Es legítimo y se declara.
- **Tramos de comparación con el artículo.** Se calculan sobre las series de las mismas corridas y no se registran aparte:
  - 1927-07 a 2005-12, contra la Tabla 2 de 2006.
  - 1927-07 a 2012-12, contra la versión de 2013.
  - Las estadísticas anuales usan solo años calendario completos (1928-2005).

### 7. Limpieza

- Mercado = Mkt-RF + RF (aditivo, como lo construye French). Con cualquier faltante (-99.99 o -999) o hueco de meses, el script se detiene; no se imputa.
- No se eliminan valores extremos: 1929-1933 y 1987 se quedan.
- El cambio de fuente de la T-bill en 202406 se declara, sin ajuste.
- Vintage 2006 (TXT): se convierte a CSV partiendo por espacios; el encabezado `Mkt-RF SMB HML RF` pasa a `,Mkt-RF,SMB,HML,RF`.
- `^GSPC`: el cierre de mes es el último cierre diario válido del mes. Se re-etiqueta al fin de mes calendario y se descartan los meses incompletos.
- FRED mensual: se re-etiqueta al fin de mes. El rendimiento mensual de Cetes se aproxima como tasa/1200, lo cual es un supuesto. `DEXMXUS`: se toma el último dato ≤ fin de mes con una antigüedad máxima de 10 días (regla del motor).
- Ninguna observación se elimina después de ver resultados.

### 8. Regla y variantes planeadas

**Regla exacta (pseudocódigo).**

```
I_0 = 1; I_s = I_{s-1} * (1 + Mkt_s)            # indice total return construido con Mkt-RF + RF
al cierre de t-1:  SMA_n = media(I_{t-n}, ..., I_{t-1})   # incluye el mes t-1
                   w_t = 1 si I_{t-1} > SMA_n, si no 0      # empate -> 0 (efectivo)
r_t = w_t * Mkt_t + (1 - w_t) * RF_t, menos el costo |w_t - w_pre_t| * (comision + spread)
```

Se implementa con `bt.senal_media_movil(n)` sobre `h.indice`.

**Parámetros del artículo:** n = 10 meses, evaluación mensual, 0 o 1 (sin apalancamiento ni cortos) y efectivo a tasa de corto plazo.

**Corridas planeadas.** La lista es cerrada: todo lo demás es desviación. Todas usan `id_replica="R01"`, `cortes=["2006-12-31"]` y `min_historia=12`, salvo donde se indica otra cosa.

| Bloque | Corridas | `es_prueba` | Costos |
|---|---|---|---|
| A. Principal | `sma6`, `sma8`, `sma10`, `sma12` y `mom12` (momentum absoluto de 12 meses, que es la regla sencilla de comparación) | **1** (N = 5) | Por defecto |
| B. Referencias | `comprar_y_mantener` y `efectivo` | 0 | Por defecto |
| C. Costos | {sma6, sma8, sma10, sma12, mom12, comprar_y_mantener} × {sin costos (0 y 0); spread medio (0.29% + 0.15%); spread ilíquido (0.29% + 0.30%); doble pierna (0.58% + 0.10%)} = 24 | 0 | Según el escenario |
| D. Ejecución | `sma10` con rezago de 1 mes | 0 | Por defecto |
| E. Vintages | {sma10, comprar_y_mantener} × {French 202407 (FIZ), French 200607} × {por defecto, sin costos} = 8 | 0 | Según el escenario |
| F. Señal sobre precio | Muestra común con el mercado desde 1928-01-31: {`sma10` sobre el índice TR, `sma10` sobre `^GSPC` de precio, comprar_y_mantener} = 3 | 0 | Por defecto |
| G. Moneda MXN | {sma10, comprar_y_mantener, efectivo} × {efectivo = RF en USD convertido a MXN; efectivo = Cetes (`INTGSTMXM193N`) en MXN} = 6. Rendimientos en MXN desde 1993-12, con la señal calculada en USD | 0 | Por defecto |

Notas sobre los bloques:

- **C, doble pierna:** supone que el efectivo es un instrumento comprado con comisión (por ejemplo, un ETF de T-bills en el SIC), así que cada cambio paga dos piernas.
- **G, alineación:** con Cetes como efectivo, la serie de efectivo empieza en 1986-10. La historia visible de la señal empieza ahí, y hay 7 años antes de la primera decisión en MXN.

Total planeado: 49 corridas registradas.

**Análisis sin registro adicional.** Se calculan sobre las series de las corridas anteriores:

- Los tramos del artículo.
- Las estadísticas al estilo Faber: media aritmética y desviación de años calendario, Sharpe anual con rf = 4%, mejor y peor año y % de años por debajo del índice.
- Los subperiodos por década.
- La prueba Newey-West de la diferencia contra comprar y mantener.
- El DSR.

**Exposición:** mínima 0, máxima 1 e inicial 0. Moneda USD, salvo en el bloque G.

### 9. Costos y comparación simple

**Costos por defecto:**

- Comisión GBM de 0.29% por lado. Es un hecho: 0.25% + IVA, Guía de Servicios GBM V1025, `arena/investigacion/01-gbm-operativa-y-costos.md` §2.1.
- Spread de 0.05% por lado. Es un supuesto [I] no verificado (§3).
- El costo es |Δw| × 0.34% sobre el valor de la cartera.

**No se incluye:**

- El spread cambiario, que no está publicado (§2.3).
- Los impuestos (10% sobre ganancias en el SIC, en una capa separada).
- El costo de la venta final.

Los escenarios de costos alternativos son los del bloque C.

**Reglas sencillas con idénticas condiciones:** comprar y mantener (`senal_comprar_y_mantener`), 100% efectivo (`senal_efectivo`) y momentum absoluto de 12 meses (`senal_momentum_absoluto(12)`).

---

## RESULTADOS (se llenan después de correr)

### Desviaciones del pre-registro

| Fecha | Qué cambió | Por qué | ¿Invalida el tramo de prueba? |
|---|---|---|---|
| 2026-09-25, entre 05:25 y 05:28 UTC, **antes de la primera corrida** (05:28:44 UTC) | Se operacionaliza la cláusula de la sección 2 que dice "el efecto aparece solo en algunos subperiodos". Se usan 9 ventanas dentro de muestra: 1927-07 a 1929-12, las décadas de 1930 a 1990 y 2000-01 a 2006-12. Si la reducción relativa del MDD neto de la SMA de 10 meses contra comprar y mantener es mayor que 0 en **menos de 5 de las 9**, el efecto se considera "solo en algunos subperiodos" y el estado queda como "Replicado con diferencias". | La cláusula del pre-registro no tenía un umbral. Se fija antes de ver resultados para que no haya discreción después. Referencia: Faber (2013, p. 28) dice que el timing mejora el drawdown "in all but two decades". | No: se fijó antes de cualquier corrida |
| 2026-09-25, ~05:24 UTC, antes de la primera corrida | Los tres zips de French se copiaron a `replicas/R01-datos/` (202607, 202407 y 200607), con el manifiesto `SHA256SUMS.txt`. El script los lee de ahí y se detiene si una huella no coincide. El zip 202607 es byte a byte el mismo del caché (sha256 `b840dba5…`). | Reproducibilidad: el caché `datos/cache/` está en `.gitignore`, y French publica una versión nueva cada mes. Se sigue el precedente de V01. Las condiciones de redistribución siguen pendientes de verificar. | No (mismos bytes) |
| 2026-09-25, 05:30 UTC, **después** de la corrida 1 (05:28 UTC) | (1) Se agregó a `R01.py` un **análisis post-hoc no pre-registrado**: bootstrap pareado de bloques de 12 meses (2000 repeticiones, semilla 20260925) de la diferencia de Sharpe y de la reducción del MDD de sma10 contra comprar y mantener y contra mom12. (2) Se agregó el conteo de operaciones. (3) Se volvió a correr el script completo (corrida 2). | Medir la incertidumbre de la diferencia de Sharpe, que el DSR no mide porque contrasta contra 0 y no contra comprar y mantener. | No cambia ninguna regla, variante, corte ni criterio. La corrida 2 registró otra vez las mismas 49 configuraciones (el CSV tiene 98 corridas; el DSR deduplica por variante y parámetros, así que N sigue en 5). `diff` de `R01-salida.txt` entre las corridas 1 y 2: solo cambian la marca de tiempo y las líneas agregadas; todas las demás cifras son idénticas, incluidos los datos de Yahoo y FRED. El bootstrap se reporta como post-hoc y **no** entra en el estado ni en el veredicto |
| 2026-09-25, 05:33 UTC | Se agregó `R01_verificacion.py`, una doble implementación de sma10 y de comprar y mantener sin el motor. | Auditoría del motor. | No es una variante nueva ni se registra. La diferencia máxima contra el motor es 1.28e-15 |

### 10. Variantes probadas

- **Archivo:** `replicas/R01-variantes.csv`, con 294 filas: 98 corridas × 3 segmentos (completo, `dentro_muestra` y `fuera_muestra`).
  - Corrida 1: 2026-09-25T05:28:44Z. Corrida 2: 05:30:38Z. Las dos usan las mismas 49 configuraciones (ver Desviaciones).
  - Las filas del vintage 200607 traen el segmento `fuera_muestra` vacío, porque esa serie termina en 2006-07.
- **Variantes con `es_prueba=1`:** 5 distintas (`sma6`, `sma8`, `sma10`, `sma12` y `mom12`), con costos por defecto. Cada una aparece dos veces con parámetros idénticos y el DSR la cuenta una vez.
- **Corridas con `es_prueba=0`:** 44 configuraciones por corrida:
  - Referencias: 2.
  - Costos: 24.
  - Rezago: 1.
  - Vintages: 8.
  - Señal de precio: 3.
  - MXN: 6.
- **Pruebas fuera del registro:** 0 variantes nuevas. Lo que se corrió fuera del registro no es una regla distinta:
  - `R01_verificacion.py` recalcula la misma sma10 y comprar y mantener.
  - `--prueba-sintetica` usa datos aleatorios en un directorio temporal.
  - Antes de la corrida 1 se cargaron los datos sin calcular métricas.
  - Por eso `n_pruebas` = 5. Como sensibilidad se usa N = 20.
- **Salida de `sharpe_deflactado_de_registro`**, copiada tal cual de `R01-salida.txt`:

```
sma10 dentro_muestra N=registradas             variante=sma10  DSR=0.9996 cumple(>= 0.95)=True N=5 (registradas 5) V=2.871e-04 SR=0.1363/mes (0.472 anual) SR0=0.0202/mes (0.070 anual) T=954 asim=-0.725 curt=9.038 PSR=1.0000
mejor variante dentro_muestra N=registradas    variante=mom12  DSR=0.9999 cumple(>= 0.95)=True N=5 (registradas 5) V=2.871e-04 SR=0.1492/mes (0.517 anual) SR0=0.0202/mes (0.070 anual) T=954 asim=-0.652 curt=9.633 PSR=1.0000
sma10 dentro_muestra N=20                      variante=sma10  DSR=0.9987 cumple(>= 0.95)=True N=20 (registradas 5) V=2.871e-04 SR=0.1363/mes (0.472 anual) SR0=0.0322/mes (0.112 anual) T=954 asim=-0.725 curt=9.038 PSR=1.0000
sma10 fuera_muestra N=registradas              variante=sma10  DSR=0.9953 cumple(>= 0.95)=True N=5 (registradas 5) V=4.325e-04 SR=0.2017/mes (0.699 anual) SR0=0.0248/mes (0.086 anual) T=235 asim=-0.275 curt=4.230 PSR=0.9985
sma10 completo N=registradas                   variante=sma10  DSR=1.0000 cumple(>= 0.95)=True N=5 (registradas 5) V=1.268e-04 SR=0.1473/mes (0.510 anual) SR0=0.0134/mes (0.047 anual) T=1189 asim=-0.677 curt=8.664 PSR=1.0000
```

**Lectura del DSR.**

- La variante fijada de antemano (`sma10`) tiene un DSR de 0.9996 dentro de muestra con N = 5, de 0.9987 con N = 20 y de 0.9953 fuera de muestra. Todos los casos superan el umbral de 0.95.
- **Advertencia pre-registrada.** El DSR contrasta el Sharpe del exceso sobre la T-bill contra 0. **No** contrasta contra comprar y mantener, que también tiene un Sharpe positivo (0.408 dentro y 0.645 fuera de muestra). Pasar el DSR solo dice que la regla gana una prima sobre el efectivo que no se explica por la selección entre 5 variantes. **No dice que supere al índice.** Esa comparación está en 11.5.

### 11. Resultados

#### 11.1 Resultados principales, netos de costos GBM por defecto (0.29% + 0.05% por lado)

```
--- Bloques A y B [completo] ---
variante                               inicio        fin    n    CAGR     vol  Sharpe Sortino      MDD  Calmar  invert  rot/a  costo/a  camb    PSR
sma6                               1927-06-30 2026-07-31 1189   8.60%  12.81%   0.455   0.700  -46.97%   0.183   70.6%   2.19   0.745%   217  1.000
sma8                               1927-06-30 2026-07-31 1189   8.40%  12.32%   0.454   0.663  -54.61%   0.154   71.2%   1.77   0.600%   175  1.000
sma10                              1927-06-30 2026-07-31 1189   9.22%  12.52%   0.510   0.756  -43.50%   0.212   73.0%   1.48   0.504%   147  1.000
sma12                              1927-06-30 2026-07-31 1189   9.45%  12.60%   0.525   0.785  -46.26%   0.204   73.3%   1.32   0.450%   131  1.000
mom12                              1927-06-30 2026-07-31 1189   9.61%  12.58%   0.536   0.808  -45.17%   0.213   70.6%   0.88   0.299%    87  1.000
comprar_y_mantener                 1927-06-30 2026-07-31 1189  10.26%  18.41%   0.447   0.676  -83.65%   0.123  100.0%   0.01   0.003%     1  1.000
efectivo                           1927-06-30 2026-07-31 1189   3.29%   0.86%   0.000   0.000   -0.09%  36.531    0.0%   0.00   0.000%     0     NA

--- Bloques A y B [dentro_muestra] ---
variante                               inicio        fin    n    CAGR     vol  Sharpe Sortino      MDD  Calmar  invert  rot/a  costo/a  camb    PSR
sma6                               1927-06-30 2006-12-31  954   8.49%  13.33%   0.403   0.617  -46.97%   0.181   69.6%   2.25   0.765%   179  1.000
sma8                               1927-06-30 2006-12-31  954   8.06%  12.70%   0.386   0.555  -54.61%   0.148   69.7%   1.82   0.620%   145  0.999
sma10                              1927-06-30 2006-12-31  954   9.31%  12.91%   0.472   0.694  -43.50%   0.214   71.7%   1.47   0.500%   117  1.000
sma12                              1927-06-30 2006-12-31  954   9.73%  12.92%   0.502   0.746  -46.26%   0.210   72.0%   1.30   0.440%   103  1.000
mom12                              1927-06-30 2006-12-31  954   9.82%  12.61%   0.517   0.774  -45.17%   0.217   68.4%   0.89   0.304%    71  1.000
comprar_y_mantener                 1927-06-30 2006-12-31  954  10.07%  18.98%   0.408   0.616  -83.65%   0.120  100.0%   0.01   0.004%     1  1.000
efectivo                           1927-06-30 2006-12-31  954   3.73%   0.88%   0.000   0.000   -0.09%  41.441    0.0%   0.00   0.000%     0     NA

--- Bloques A y B [fuera_muestra] ---
variante                               inicio        fin    n    CAGR     vol  Sharpe Sortino      MDD  Calmar  invert  rot/a  costo/a  camb    PSR
sma6                               2006-12-31 2026-07-31  235   9.04%  10.43%   0.737   1.177  -16.79%   0.538   74.5%   1.94   0.660%    38  0.999
sma8                               2006-12-31 2026-07-31  235   9.79%  10.64%   0.790   1.282  -13.76%   0.712   77.0%   1.53   0.521%    30  1.000
sma10                              2006-12-31 2026-07-31  235   8.85%  10.82%   0.699   1.098  -19.31%   0.458   78.3%   1.53   0.521%    30  0.998
sma12                              2006-12-31 2026-07-31  235   8.30%  11.19%   0.636   0.982  -19.31%   0.430   78.7%   1.43   0.486%    28  0.997
mom12                              2006-12-31 2026-07-31  235   8.75%  12.51%   0.615   0.952  -24.52%   0.357   79.6%   0.82   0.278%    16  0.996
comprar_y_mantener                 2006-12-31 2026-07-31  235  11.02%  15.91%   0.645   0.969  -50.31%   0.219  100.0%   0.00   0.000%     0  0.996
efectivo                           2006-12-31 2026-07-31  235   1.51%   0.54%   0.000   0.000    0.00%     inf    0.0%   0.00   0.000%     0     NA
```

Cómo leer la tabla:

- La columna `inicio` es la fecha base de la curva (valor 1.0). El primer rendimiento evaluado es el del mes siguiente: 1927-07 en `dentro_muestra` y 2007-01 en `fuera_muestra`.
- `camb` cuenta los cambios de exposición.
- `rot/a` es la rotación anual, Σ|Δw| por año.

Fechas de los drawdowns máximos, de `R01_verificacion.py` (coinciden con el motor hasta 1.28e-15):

| Serie | Segmento | Drawdown máximo | Pico | Valle |
|---|---|---|---|---|
| sma10 | dentro de muestra | −43.50% | 1929-08-31 | 1933-03-31 |
| comprar y mantener | dentro de muestra | −83.65% | 1929-08-31 | 1932-06-30 |
| sma10 | fuera de muestra | −19.31% | 2018-09-30 | 2019-08-31 |
| comprar y mantener | fuera de muestra | −50.31% | 2007-10-31 | 2009-02-28 |

Fuera de muestra, el peor drawdown de la regla no ocurre en 2008, 2020 ni 2022. Ocurre entre 2018-09 y 2019-08. *Inferencia:* fue un latigazo, porque salió después de la caída de fines de 2018 y volvió a entrar tras el rebote.

#### 11.2 Tramo del artículo, sin costos (como Faber)

```
--- 1927-07_a_2005-12 ---
variante                        CAGR media a. sd anual vol mens Sh rf4%  Sharpe      MDD    MAR   Ulcer  invert  sal/a   %op+   mejor     peor
sma6|sin_costos                9.26%   10.20%   15.93%   13.41%    0.39   0.455  -46.11%   0.20  12.88%   69.5%   1.12    53%  50.31%  -21.06%
sma8|sin_costos                8.68%    9.67%   16.35%   12.77%    0.35   0.431  -53.85%   0.16  15.31%   69.4%   0.90    50%  50.31%  -21.81%
sma10|sin_costos               9.79%   10.80%   16.35%   12.97%    0.42   0.506  -42.94%   0.23  12.67%   71.3%   0.74    47%  50.31%  -21.81%
sma12|sin_costos              10.15%   11.12%   16.13%   12.98%    0.44   0.531  -45.36%   0.22  12.88%   71.7%   0.65    48%  50.31%  -22.35%
mom12|sin_costos              10.09%   10.77%   14.03%   12.69%    0.48   0.535  -44.23%   0.23  13.15%   68.0%   0.45    81%  42.98%  -19.16%
comprar_y_mantener|sin_costo  10.01%   11.81%   20.43%   19.09%    0.38   0.404  -83.65%   0.12  23.00%  100.0%   0.00   100%  56.80%  -43.76%
anios calendario completos: (1928, 2005, 78)
sma6|sin_costos        reduccion MDD=0.4488  dif CAGR=-0.746 pp  dif media arit=-1.608 pp  % anios debajo de B&H=60.3%  operaciones=89
sma8|sin_costos        reduccion MDD=0.3563  dif CAGR=-1.332 pp  dif media arit=-2.135 pp  % anios debajo de B&H=51.3%  operaciones=72
sma10|sin_costos       reduccion MDD=0.4867  dif CAGR=-0.216 pp  dif media arit=-1.012 pp  % anios debajo de B&H=42.3%  operaciones=59
sma12|sin_costos       reduccion MDD=0.4578  dif CAGR=+0.147 pp  dif media arit=-0.685 pp  % anios debajo de B&H=41.0%  operaciones=52
mom12|sin_costos       reduccion MDD=0.4713  dif CAGR=+0.079 pp  dif media arit=-1.041 pp  % anios debajo de B&H=39.7%  operaciones=36

--- 1927-07_a_2012-12 ---
variante                        CAGR media a. sd anual vol mens Sh rf4%  Sharpe      MDD    MAR   Ulcer  invert  sal/a   %op+   mejor     peor
sma6|sin_costos                9.28%   10.18%   15.55%   13.13%    0.40   0.476  -46.11%   0.20  12.45%   69.0%   1.11    54%  50.31%  -21.06%
sma8|sin_costos                8.55%    9.49%   15.86%   12.54%    0.35   0.440  -53.85%   0.16  14.76%   69.2%   0.91    52%  50.31%  -21.81%
sma10|sin_costos               9.59%   10.55%   15.87%   12.74%    0.41   0.512  -42.94%   0.22  12.26%   71.3%   0.73    49%  50.31%  -21.81%
sma12|sin_costos               9.74%   10.66%   15.68%   12.75%    0.42   0.522  -45.36%   0.21  12.53%   71.5%   0.64    50%  50.31%  -22.35%
mom12|sin_costos               9.88%   10.53%   13.62%   12.60%    0.48   0.536  -44.23%   0.22  12.74%   68.5%   0.43    82%  42.98%  -19.16%
comprar_y_mantener|sin_costo   9.55%   11.39%   20.40%   18.92%    0.36   0.393  -83.65%   0.11  22.65%  100.0%   0.00   100%  56.80%  -43.76%
anios calendario completos: (1928, 2012, 85)
sma6|sin_costos        reduccion MDD=0.4488  dif CAGR=-0.273 pp  dif media arit=-1.214 pp  % anios debajo de B&H=60.0%  operaciones=96
sma8|sin_costos        reduccion MDD=0.3563  dif CAGR=-1.002 pp  dif media arit=-1.903 pp  % anios debajo de B&H=51.8%  operaciones=79
sma10|sin_costos       reduccion MDD=0.4867  dif CAGR=+0.044 pp  dif media arit=-0.849 pp  % anios debajo de B&H=43.5%  operaciones=63
sma12|sin_costos       reduccion MDD=0.4578  dif CAGR=+0.192 pp  dif media arit=-0.734 pp  % anios debajo de B&H=42.4%  operaciones=56
mom12|sin_costos       reduccion MDD=0.4713  dif CAGR=+0.329 pp  dif media arit=-0.867 pp  % anios debajo de B&H=38.8%  operaciones=38

Cifras del articulo, 2006 (Tabla 2, 1900-2005): CAGR 9.75% vs 10.66%; sd 19.91% vs 15.38%; Sharpe 0.29 vs 0.43; MDD 83.66% vs 49.98% (texto: 42.24%); MAR 0.14 vs 0.23; Ulcer 20.33% vs 11.70%; invertido 69.77%; 0.67 RT/anio; 63% op+; mejor 52.88% vs 52.40%; peor -43.86% vs -26.69%; media arit. 11.66% vs 11.72%; ~40% anios debajo
Cifras del articulo, 2013 (1901-2012): CAGR 9.32% vs 10.18%; media arit. 11.26% vs 11.22%; MDD 83.66% vs 42.24%; ~70% invertido; <1 RT/anio; ~50% anios debajo
```

**Comparación con la Tabla 2 del working paper de 2006.** Las cifras de la réplica son de `R01-salida.txt`, tramo 1927-07 a 2005-12. Las estadísticas anuales usan los años calendario completos 1928-2005.

| Métrica | Faber, S&P 500 (1900-2005) | Faber, timing | Réplica, comprar y mantener | Réplica, sma10 |
|---|---|---|---|---|
| CAGR | 9.75% | 10.66% | 10.01% | 9.79% |
| Timing menos índice (CAGR) | | +0.91 pp | | **−0.216 pp** |
| Media aritmética anual | 11.66% | 11.72% | 11.81% | 10.80% |
| Desviación estándar | 19.91% | 15.38% | 20.43% (años calendario) y 19.09% (mensual anualizada) | 16.35% y 12.97% |
| Sharpe (anual, rf = 4%) | 0.29 | 0.43 | 0.38 | 0.42 |
| Drawdown máximo | −83.66% | −49.98% (tabla) o −42.24% (texto) | −83.65% | −42.94% |
| Reducción relativa del MDD | | 0.403 (tabla) o 0.495 (texto) | | **0.4867** |
| MAR | 0.14 | 0.23 | 0.12 | 0.23 |
| Ulcer Index | 20.33% | 11.70% | 23.00% | 12.67% |
| % del tiempo invertido | 100% | 69.77% | 100% | 71.3% |
| Idas y vueltas por año | – | 0.67 | – | 0.74 (salidas por año) |
| % de operaciones positivas | – | 63% | – | 47% (59 operaciones) |
| Mejor año | 52.88% | 52.40% | 56.80% | 50.31% |
| Peor año | −43.86% | −26.69% | −43.76% | −21.81% |
| % de años debajo del índice | – | ~40% | – | 42.3% |

**Contra la actualización de 2013 (1901-2012).** En el tramo 1927-07 a 2012-12, sin costos, la réplica da:

| Métrica | Faber 2013 | Réplica |
|---|---|---|
| CAGR (timing contra índice) | 10.18% contra 9.32% (+0.86 pp) | 9.59% contra 9.55% (+0.044 pp) |
| Media aritmética (timing contra índice) | 11.22% contra 11.26% | 10.55% contra 11.39% (−0.849 pp) |
| Drawdown máximo (timing contra índice) | 42.24% contra 83.66% | −42.94% contra −83.65% |
| % del tiempo invertido | ~70% | 71.3% |
| % de años debajo del índice | ~50% | 43.5% |

#### 11.3 Criterios pre-registrados

La regla se aplica en el código (`R01.py`, función `analizar`). No hay juicio manual.

```
================ CRITERIOS PRE-REGISTRADOS ================
C1 reduccion relativa del MDD (1927-07..2005-12, sin costos) = 0.4867 en [0.30, 0.60]? True
C2 dif CAGR sma10 - B&H = -0.216 pp en (0, +1.91 pp]? False
C3 tiempo invertido = 0.7134 en [0.60, 0.80]? True
C4 salidas por anio = 0.7388 en [0.40, 1.00]? True
Refutacion a) dentro_muestra neto: reduccion MDD = 0.4800 < 0.20? False
Refutacion b) dentro_muestra neto: Sharpe sma10 0.4723 <= Sharpe B&H 0.4078? False
Subperiodos (adenda): reduccion MDD > 0 en 7 de 9 ventanas dentro de muestra; 'solo en algunos subperiodos' (< 5)? False
ESTADO segun reglas pre-registradas: Replicado con diferencias
Fuera de muestra (2007-01..2026-07, neto): reduccion MDD = 0.6162; Sharpe sma10 0.6987 vs B&H 0.6452 -> veredicto: Se sostiene
```

- **Se reproduce:** la reducción del drawdown (C1: 0.4867, muy cerca del 0.495 del texto de Faber), el tiempo invertido (C3) y la frecuencia de operación (C4).
- **No se reproduce:** la ventaja de CAGR (C2). Faber reporta +0.91 pp y la réplica da −0.216 pp en 1927-2005 y +0.044 pp en 1927-2012.
- **Refutación:** no se cumple. Dentro de muestra y neto, la reducción del MDD es 0.480 (≥ 0.20) y el Sharpe es 0.4723 contra 0.4078.

#### 11.4 Subperiodos: sma10 contra comprar y mantener, neto

```
--- Subperiodos: sma10 vs comprar y mantener (neto, costos por defecto) ---
ventana                   CAGR sma10  CAGR B&H Sh sma10  Sh B&H MDD sma10  MDD B&H  red MDD  invert
1927-07 a 1929-12             21.00%    15.29%     0.84    0.57   -23.71%  -33.25%    0.287     93%
1930-01 a 1939-12              2.13%    -0.26%     0.18    0.15   -29.36%  -79.37%    0.630     51%
1940-01 a 1949-12              6.21%     9.49%     0.50    0.64   -27.78%  -27.98%    0.007     67%
1950-01 a 1959-12             15.66%    18.35%     1.24    1.40   -16.73%  -14.94%   -0.120     86%
1960-01 a 1969-12              6.43%     8.26%     0.31    0.39   -14.05%  -23.07%    0.391     72%
1970-01 a 1979-12              8.21%     6.06%     0.21    0.07   -15.88%  -46.51%    0.659     65%
1980-01 a 1989-12             13.90%    16.87%     0.39    0.51   -24.84%  -29.85%    0.168     76%
1990-01 a 1999-12             12.81%    17.99%     0.63    0.93   -19.20%  -17.32%   -0.108     86%
2000-01 a 2006-12              6.08%     1.60%     0.38   -0.02   -14.33%  -44.99%    0.682     63%
2007-01 a 2009-12              9.56%    -4.85%     0.88   -0.25    -5.16%  -50.31%    0.897     53%
2010-01 a 2019-12              7.58%    13.60%     0.69    1.01   -19.31%  -17.66%   -0.093     87%
2020-01 a 2026-07             10.47%    15.02%     0.65    0.73   -13.76%  -24.84%    0.446     77%
```

- **Dentro de muestra:** la reducción del MDD es positiva en 7 de 9 ventanas; el umbral de la adenda era 5. Es negativa en los años cincuenta (−0.120) y en los noventa (−0.108). *Inferencia:* fueron mercados alcistas largos con correcciones cortas, en los que la regla sale tarde y vuelve a entrar más arriba.
- **Fuera de muestra:**
  - En 2007-2009 la reducción es de 0.897.
  - En 2010-2019 es negativa (−0.093): la regla tuvo un MDD de −19.31% contra −17.66% del índice y un CAGR de 7.58% contra 13.60%.
  - En 2020-2026-07 es de 0.446, con un CAGR de 10.47% contra 15.02%.

#### 11.5 Contra comprar y mantener y contra la regla sencilla (momentum absoluto de 12 meses)

Diferencia mensual de rendimientos netos, con error estándar Newey-West de 6 rezagos (pre-registrada):

```
--- Diferencia mensual de rendimientos netos, media y error estandar Newey-West (6 rezagos) ---
sma10 - comprar_y_mantener                         dentro_muestra  n=954   media=-0.1370%/mes (x12 -1.64%) t_NW6=-1.03 IC95=[-0.3968, +0.1228]%/mes
sma10 - comprar_y_mantener                         fuera_muestra   n=235   media=-0.2234%/mes (x12 -2.68%) t_NW6=-0.94 IC95=[-0.6873, +0.2405]%/mes
sma10 - comprar_y_mantener                         completo        n=1189  media=-0.1541%/mes (x12 -1.85%) t_NW6=-1.33 IC95=[-0.3818, +0.0737]%/mes
mom12 - comprar_y_mantener                         dentro_muestra  n=954   media=-0.1016%/mes (x12 -1.22%) t_NW6=-0.78 IC95=[-0.3580, +0.1547]%/mes
mom12 - comprar_y_mantener                         fuera_muestra   n=235   media=-0.2145%/mes (x12 -2.57%) t_NW6=-0.93 IC95=[-0.6672, +0.2381]%/mes
mom12 - comprar_y_mantener                         completo        n=1189  media=-0.1240%/mes (x12 -1.49%) t_NW6=-1.08 IC95=[-0.3483, +0.1003]%/mes
sma10 - mom12                                      dentro_muestra  n=954   media=-0.0353%/mes (x12 -0.42%) t_NW6=-0.51 IC95=[-0.1724, +0.1017]%/mes
sma10 - mom12                                      fuera_muestra   n=235   media=-0.0088%/mes (x12 -0.11%) t_NW6=-0.06 IC95=[-0.3095, +0.2918]%/mes
sma10 - mom12                                      completo        n=1189  media=-0.0301%/mes (x12 -0.36%) t_NW6=-0.47 IC95=[-0.1551, +0.0949]%/mes
sma10|sin_costos - comprar_y_mantener|sin_costos   dentro_muestra  n=954   media=-0.0954%/mes (x12 -1.14%) t_NW6=-0.73 IC95=[-0.3525, +0.1618]%/mes
sma10|sin_costos - comprar_y_mantener|sin_costos   fuera_muestra   n=235   media=-0.1798%/mes (x12 -2.16%) t_NW6=-0.78 IC95=[-0.6338, +0.2741]%/mes
sma10|sin_costos - comprar_y_mantener|sin_costos   completo        n=1189  media=-0.1121%/mes (x12 -1.34%) t_NW6=-0.98 IC95=[-0.3370, +0.1129]%/mes
```

- **Contra comprar y mantener.** La diferencia media de sma10 es **negativa y no significativa** en todos los segmentos:
  - Dentro de muestra: −0.137%/mes (t = −1.03).
  - Fuera de muestra: −0.223%/mes (t = −0.94).
  - Sin costos, dentro de muestra: −0.095%/mes (t = −0.73).
- **Lectura.** La regla no gana en rendimiento medio. Su mayor Sharpe viene de una volatilidad menor: 12.91% contra 18.98% dentro de muestra y 10.82% contra 15.91% fuera de muestra.
- **Contra la regla sencilla, mom12.**
  - Fuera de muestra, sma10 la supera en Sharpe (0.699 contra 0.615) y en MDD (−19.31% contra −24.52%).
  - Dentro de muestra, mom12 tiene mejor Sharpe (0.517 contra 0.472), con un MDD parecido (−45.17% contra −43.50%).
  - La diferencia de medias sma10 − mom12 no es significativa en ningún segmento (|t| ≤ 0.51).

**Análisis post-hoc, NO pre-registrado.** Se agregó después de la corrida 1 (ver Desviaciones) y no entra en el estado ni en el veredicto. Es un bootstrap pareado de bloques de 12 meses sobre los rendimientos realizados, sin re-simular la señal.

```
--- POST-HOC (no pre-registrado): bootstrap pareado de bloques de 12 meses, 2000 repeticiones ---
sma10 vs comprar_y_mantener    dentro_muestra  dif Sharpe obs=+0.065 IC95=[-0.134, +0.275] frac<=0=0.306 | red MDD obs=+0.480 IC95=[-0.061, +0.617] frac<0.20=0.191
sma10 vs comprar_y_mantener    fuera_muestra   dif Sharpe obs=+0.054 IC95=[-0.348, +0.523] frac<=0=0.416 | red MDD obs=+0.616 IC95=[-0.334, +0.753] frac<0.20=0.217
sma10 vs mom12                 dentro_muestra  dif Sharpe obs=-0.044 IC95=[-0.180, +0.089] frac<=0=0.749 | red MDD obs=+0.037 IC95=[-0.768, +0.269] frac<0.20=0.939
sma10 vs mom12                 fuera_muestra   dif Sharpe obs=+0.084 IC95=[-0.179, +0.412] frac<=0=0.231 | red MDD obs=+0.213 IC95=[-0.377, +0.552] frac<0.20=0.540
```

- **Diferencia de Sharpe** de sma10 contra comprar y mantener: +0.065 dentro de muestra (IC 95% de −0.134 a +0.275) y +0.054 fuera de muestra (IC de −0.348 a +0.523). **No se distingue de cero.**
- **Reducción del MDD.** El valor puntual es alto (0.480 y 0.616), pero entre 19% y 22% de los remuestreos da una reducción menor que 0.20. El efecto depende de pocos episodios: 1929-1933 y 2008-2009.
- **Límite del método.** Con bloques de 12 meses se rompen las caídas de varios años, así que esta medida es cruda.

### 12. Sensibilidad

Diferencias contra comprar y mantener en el mismo segmento y escenario. Las columnas de diferencia y de reducción relativa se calcularon de `R01-resultados.json`. Las demás cifras son las de las tablas de `R01-salida.txt`.

**dentro_muestra**

| Escenario | CAGR regla | CAGR B&H | Dif. (pp) | Sharpe regla | Sharpe B&H | Dif. | MDD regla | MDD B&H | Red. rel. MDD |
|---|---|---|---|---|---|---|---|---|---|
| sma6 (costos por defecto) | 8.49% | 10.07% | -1.58 | 0.403 | 0.408 | -0.005 | -46.97% | -83.65% | 0.438 |
| sma8 (costos por defecto) | 8.06% | 10.07% | -2.01 | 0.386 | 0.408 | -0.021 | -54.61% | -83.65% | 0.347 |
| sma10 (costos por defecto) | 9.31% | 10.07% | -0.76 | 0.472 | 0.408 | +0.065 | -43.50% | -83.65% | 0.480 |
| sma12 (costos por defecto) | 9.73% | 10.07% | -0.34 | 0.502 | 0.408 | +0.094 | -46.26% | -83.65% | 0.447 |
| mom12 (costos por defecto) | 9.82% | 10.07% | -0.25 | 0.517 | 0.408 | +0.109 | -45.17% | -83.65% | 0.460 |
| sma10, sin_costos | 9.86% | 10.07% | -0.21 | 0.512 | 0.408 | +0.104 | -42.94% | -83.65% | 0.487 |
| sma10, spread_medio | 9.15% | 10.07% | -0.92 | 0.461 | 0.408 | +0.053 | -43.67% | -83.65% | 0.478 |
| sma10, spread_iliquido | 8.91% | 10.07% | -1.16 | 0.443 | 0.408 | +0.036 | -44.43% | -83.65% | 0.469 |
| sma10, doble_pierna | 8.76% | 10.06% | -1.30 | 0.433 | 0.408 | +0.025 | -45.08% | -83.65% | 0.461 |
| sma10, rezago de 1 mes | 8.81% | 10.07% | -1.26 | 0.431 | 0.408 | +0.023 | -51.02% | -83.65% | 0.390 |
| sma10 sobre índice TR, muestra desde 1928-01 | 8.77% | 9.54% | -0.77 | 0.435 | 0.381 | +0.054 | -43.50% | -83.65% | 0.480 |
| sma10 sobre ^GSPC de precio, muestra desde 1928-01 | 9.45% | 9.54% | -0.09 | 0.508 | 0.381 | +0.127 | -46.26% | -83.65% | 0.447 |
| sma10, vintage CRSP 202407 (hasta 2024-07) | 9.30% | 10.06% | -0.76 | 0.472 | 0.407 | +0.064 | -43.52% | -83.71% | 0.480 |
| sma10, vintage CRSP 200607 (hasta 2006-07) | 9.36% | 9.92% | -0.55 | 0.477 | 0.401 | +0.076 | -43.17% | -83.72% | 0.484 |

**fuera_muestra**

| Escenario | CAGR regla | CAGR B&H | Dif. (pp) | Sharpe regla | Sharpe B&H | Dif. | MDD regla | MDD B&H | Red. rel. MDD |
|---|---|---|---|---|---|---|---|---|---|
| sma6 (costos por defecto) | 9.04% | 11.02% | -1.99 | 0.737 | 0.645 | +0.092 | -16.79% | -50.31% | 0.666 |
| sma8 (costos por defecto) | 9.79% | 11.02% | -1.23 | 0.790 | 0.645 | +0.145 | -13.76% | -50.31% | 0.727 |
| sma10 (costos por defecto) | 8.85% | 11.02% | -2.17 | 0.699 | 0.645 | +0.054 | -19.31% | -50.31% | 0.616 |
| sma12 (costos por defecto) | 8.30% | 11.02% | -2.72 | 0.636 | 0.645 | -0.009 | -19.31% | -50.31% | 0.616 |
| mom12 (costos por defecto) | 8.75% | 11.02% | -2.27 | 0.615 | 0.645 | -0.030 | -24.52% | -50.31% | 0.513 |
| sma10, sin_costos | 9.42% | 11.02% | -1.60 | 0.749 | 0.645 | +0.103 | -17.64% | -50.31% | 0.649 |
| sma10, spread_medio | 8.68% | 11.02% | -2.34 | 0.684 | 0.645 | +0.039 | -19.79% | -50.31% | 0.607 |
| sma10, spread_iliquido | 8.43% | 11.02% | -2.59 | 0.662 | 0.645 | +0.016 | -20.51% | -50.31% | 0.592 |
| sma10, doble_pierna | 8.28% | 11.02% | -2.74 | 0.648 | 0.645 | +0.003 | -20.95% | -50.31% | 0.584 |
| sma10, rezago de 1 mes | 9.45% | 11.02% | -1.57 | 0.692 | 0.645 | +0.047 | -21.53% | -50.31% | 0.572 |
| sma10 sobre índice TR, muestra desde 1928-01 | 8.85% | 11.02% | -2.17 | 0.699 | 0.645 | +0.054 | -19.31% | -50.31% | 0.616 |
| sma10 sobre ^GSPC de precio, muestra desde 1928-01 | 8.48% | 11.02% | -2.55 | 0.659 | 0.645 | +0.014 | -24.17% | -50.31% | 0.520 |
| sma10, vintage CRSP 202407 (hasta 2024-07) | 8.79% | 10.18% | -1.39 | 0.716 | 0.607 | +0.110 | -19.42% | -50.39% | 0.615 |

**Moneda MXN (señal en USD; 1993-12 a 2026-07)**

| Segmento y efectivo | CAGR regla | CAGR B&H | Dif. (pp) | Sharpe regla | Sharpe B&H | Dif. | MDD regla | MDD B&H | Red. rel. MDD |
|---|---|---|---|---|---|---|---|---|---|
| completo, efectivo rf_usd | 15.67% | 16.94% | -1.26 | 0.646 | 0.538 | +0.108 | -24.01% | -39.86% | 0.398 |
| completo, efectivo cetes | 15.75% | 16.94% | -1.19 | 0.420 | 0.395 | +0.025 | -14.31% | -39.86% | 0.641 |
| dentro_muestra, efectivo rf_usd | 22.20% | 21.90% | +0.30 | 0.620 | 0.486 | +0.134 | -13.37% | -39.86% | 0.665 |
| dentro_muestra, efectivo cetes | 20.56% | 21.90% | -1.34 | 0.204 | 0.237 | -0.033 | -13.13% | -39.86% | 0.671 |
| fuera_muestra, efectivo rf_usd | 11.51% | 13.73% | -2.23 | 0.663 | 0.569 | +0.094 | -24.01% | -29.97% | 0.199 |
| fuera_muestra, efectivo cetes | 12.64% | 13.73% | -1.09 | 0.586 | 0.562 | +0.024 | -14.31% | -29.97% | 0.523 |
| mismo periodo en USD (referencia) | 9.75% | 10.95% | -1.20 | 0.686 | 0.597 | +0.089 | -19.31% | -50.31% | 0.616 |

Notas de sensibilidad:

- **Parámetros (6, 8, 10 y 12 meses).**
  - Las cuatro longitudes reducen el MDD entre 0.347 y 0.480 dentro de muestra y entre 0.616 y 0.727 fuera de muestra.
  - Las cuatro tienen un CAGR menor que el de comprar y mantener en los dos segmentos.
  - El Sharpe supera al índice en 2 de 4 dentro de muestra (sma10 y sma12) y en 3 de 4 fuera de muestra (sma12 queda en 0.636 contra 0.645).
  - La mejor dentro de muestra, por Sharpe, es mom12; la mejor fuera de muestra es sma8. El 10 no es un óptimo en ninguno de los dos tramos, y eso es consistente con lo que dice Faber.
- **Costos.**
  - Con la comisión GBM y un spread del 0.05%, sma10 paga 0.50% al año dentro de muestra y 0.52% fuera de muestra. Con doble pierna paga 1.00% y 1.04%.
  - La ventaja de Sharpe fuera de muestra baja de +0.054 a **+0.003** con doble pierna.
  - La reducción del MDD casi no cambia: queda entre 0.584 y 0.649 fuera de muestra.
- **Ejecución con 1 mes de rezago.** La reducción del MDD cae a 0.390 dentro de muestra y a 0.572 fuera de muestra, pero se conserva. El efecto no depende de operar al cierre exacto del día de la señal.
- **Vintages de French.** El cambio de formato FIZ a CIZ (2025) y las revisiones de datos no mueven el resultado:
  - La señal sma10 del vintage 202607 contra el 202407 difiere en **0 de 1165 meses**.
  - Contra el 200607, disponible en 2006, difiere en **4 de 949 meses** (1948-10, 1953-06, 1965-08 y 2000-06).
  - En el tramo del artículo, la diferencia de CAGR es −0.216, −0.220 y −0.036 pp, y la reducción del MDD es 0.4867, 0.4867 y 0.4911 (vintages 202607, 202407 y 200607).
- **Señal sobre el índice de precio `^GSPC` (sin dividendos) en lugar del índice TR.**
  - Las señales difieren en 61 de 1171 meses.
  - Dentro de muestra, la versión de precio da mejor Sharpe (0.508 contra 0.435), pero un MDD algo mayor (−46.26% contra −43.50%) y menos tiempo invertido (65.4% contra 71.2%).
  - Fuera de muestra es peor: Sharpe 0.659 contra 0.699 y MDD −24.17% contra −19.31%.
  - No hay una ganadora estable.
- **Moneda MXN (1993-12 a 2026-07; efectivo en USD de French convertido, o Cetes aproximados con FRED `INTGSTMXM193N`/1200).**
  - Medido en MXN, el MDD de comprar y mantener es menor que en USD: −39.86% contra −50.31%, porque el peso se deprecia en las crisis y amortigua la caída.
  - **Con efectivo en USD**, el filtro reduce el MDD en MXN solo 0.199 fuera de muestra (−24.01% contra −29.97%), por debajo de 0.20. Al salir del índice, la cartera sigue expuesta al tipo de cambio: el efectivo en USD medido en MXN tuvo un MDD de −27.37%.
  - **Con Cetes como efectivo**, la reducción fuera de muestra es de 0.523 (−14.31% contra −29.97%), a cambio de −1.09 pp de CAGR.
  - **Resultado negativo.** Con Cetes, dentro de muestra (1993-12 a 2006-12, con tasas de Cetes altas), el Sharpe de la regla sobre Cetes es **menor** que el de comprar y mantener: 0.204 contra 0.237, con un CAGR de 20.56% contra 21.90%.
  - Esto confirma en lo cualitativo la inferencia del capítulo 14 (R2): el beneficio medido en MXN es menor si la salida no es a pesos.
  - El Sharpe de estas corridas mide el exceso sobre el efectivo de cada corrida en MXN, así que no es comparable entre los dos tipos de efectivo.

### 13. Diferencia frente al artículo

| Aspecto | Artículo | Réplica | ¿Explica la diferencia? |
|---|---|---|---|
| Datos / versión | S&P 500 con rendimiento total, de Global Financial Data (reconstruido antes de 1971 con el S&P Composite y dividendos de Cowles) | Mercado CRSP ponderado por valor (Mkt-RF + RF) de French, CRSP 202607 (formato CIZ); vintages 202407 (FIZ) y 200607 como control | Los vintages no mueven nada: 0 y 4 meses de señal distinta. El cambio de índice (S&P 500 contra el mercado CRSP) queda **sin medir** con datos anteriores a 1927 |
| Periodo | 1900-2005 (2006) y 1901-2012 (2013) | Traslape 1927-07 a 2005-12 y 1927-07 a 2012-12. Propio: 1927-07 a 2026-07 | **Posible explicación, no verificada**, de la diferencia de CAGR (+0.91 contra −0.22 pp): faltan 1900-1926, con caídas como las de 1907, 1917 y 1920-1921 |
| Efectivo | Papel comercial a 90 días (2006) y T-bills a 90 días (2013) | T-bill a 1 mes (Ibbotson; ICE BofA desde 202406) | Efecto no medido. Una tasa de efectivo más alta favorece al timing |
| Costos | Ninguno | 0.29% + 0.05% por lado (GBM) y escenarios de 0 a 0.68% por lado | Explica −0.55 pp de CAGR dentro de muestra (9.86% contra 9.31%) y −0.57 pp fuera de muestra (9.42% contra 8.85%) |
| Regla | SMA de 10 meses sobre el precio TR de fin de mes; ejecución al cierre | Igual; un empate va a efectivo | Sin diferencia de regla |
| Métricas | Sharpe con años calendario y rf = 4%; la desviación estándar no está especificada en 2006 | Se calcularon las dos versiones (tabla 11.2) | Sí |
| MDD del timing | 49.98% (Tabla 2) contra 42.24% (texto) | −42.94% (sin costos) | La réplica coincide con el texto. La discrepancia interna del artículo **no está explicada** |
| % de operaciones positivas | 63% | 47% (59 operaciones, 0.74 salidas por año) | **No explicada.** Hay más latigazos en el mercado CRSP que en el S&P 500 de GFD (0.74 contra 0.67 idas y vueltas por año), pero no se verificó que esa sea la causa |
| Media aritmética | El timing la iguala (11.72% contra 11.66%) | El timing queda 1.01 pp abajo (10.80% contra 11.81%) | No explicada; mismo origen probable que la diferencia de CAGR |

### 14. Conclusiones permitidas

Alcance: mercado accionario de EUA (CRSP), mensual, de 1927-07 a 2026-07, en USD salvo donde se indica, sin impuestos.

1. **La reducción del drawdown se replica.** La SMA de 10 meses sobre el índice total return reduce el drawdown máximo del mercado de EUA en ~48-49% relativo en 1927-2006, con o sin costos GBM, y en 62% después de la publicación (2007-2026). La magnitud coincide con la de Faber (0.495 según su texto) y resiste:
   - las longitudes de 6 a 12 meses;
   - los costos de hasta 0.68% por lado;
   - un mes de rezago de ejecución;
   - tres vintages de datos;
   - calcular la señal sobre el índice de precio.
2. **La ventaja de CAGR que reporta Faber (+0.9 pp, bruto) NO se replica** con datos CRSP desde 1927: −0.22 pp en 1927-2005 y +0.04 pp en 1927-2012, sin costos. Neta de costos GBM, la regla rinde **menos** que comprar y mantener: −0.76 pp al año dentro de muestra y −2.17 pp fuera de muestra.
3. **El rendimiento medio es estadísticamente indistinguible del de comprar y mantener**, con signo negativo (t de −0.73 a −1.33). El mayor Sharpe (0.472 contra 0.408 y 0.699 contra 0.645) viene de una volatilidad menor. Su diferencia no es significativa en el bootstrap post-hoc.
4. **El veredicto fuera de muestra pre-registrado es "Se sostiene"**: reducción del MDD de 0.616 y Sharpe de 0.699 contra 0.645. El margen de Sharpe es delgado: +0.003 con costos de doble pierna, y sma12 y mom12 quedan por debajo del índice fuera de muestra.
5. **En MXN, el beneficio depende del efectivo.** Salir a Cetes conserva la protección (reducción de 0.52 fuera de muestra). Salir a efectivo en USD la reduce a 0.199.
6. El DSR de la variante fijada de antemano es ≥ 0.95 con N = 5 y con N = 20. Solo contrasta el Sharpe contra 0; ver 10.

### 15. Conclusiones que NO se sostienen

- "El filtro de 10 meses mejora el rendimiento" (CAGR o media). Aquí la réplica rinde menos neto de costos, dentro y fuera de muestra.
- "Mejora el Sharpe de forma significativa" o "tiene alfa". La diferencia de Sharpe no se distingue de cero y el DSR no contrasta contra el índice.
- "El 10 es el parámetro correcto". No es el mejor en ningún tramo; su elección viene de la media de 200 días de Siegel.
- "Funciona igual en MXN". Depende de a qué efectivo se sale.
- "Protege siempre". En 2010-2019 el drawdown de la regla fue mayor que el del índice (−19.31% contra −17.66%). El drawdown máximo fuera de muestra (−19.31%) fue un latigazo en 2018-2019. En los años cincuenta y noventa también empeoró el drawdown.
- "Tiene ventaja con dinero real en GBM". No incluye impuestos: cada salida realiza la ganancia (10% en el SIC) ~0.74 veces al año, contra el diferimiento de comprar y mantener. Tampoco incluye el spread cambiario ni la comisión de un fondo o ETF, y no hay papel.
- "Funcionará en el futuro". La reducción del drawdown depende de pocos episodios (1929-1933, 2008-2009). En el bootstrap post-hoc, 19-22% de los remuestreos dan una reducción menor que 0.20.
- Cualquier conclusión sobre la regla R2 (media de 200 días **diaria** + VIX < 25 sobre apalancados). Esta réplica es mensual, sin apalancamiento y sin VIX.

### 16. Estado y reproducción

- **Estado: Replicado con diferencias**, según las reglas pre-registradas, que aplica el código:
  - C1, C3 y C4 se cumplen; **C2 (CAGR) falla**.
  - No hay refutación.
  - La reducción del MDD es positiva en 7 de 9 subperiodos.
  - **Fuera de muestra: "Se sostiene".**
- **Comandos que reproducen todo** (desde `/home/user/New1`):
  - `python3 laboratorio/replicas/R01.py`: corre las 49 configuraciones, las agrega a `R01-variantes.csv` y escribe `R01-resultados.json` y `R01-salida.txt`.
  - `python3 laboratorio/replicas/R01_verificacion.py`: hace la doble implementación. Se corre después del anterior.
  - `python3 laboratorio/replicas/R01.py --prueba-sintetica`: prueba el código sin datos reales.
- **Huellas:**
  - `huella_datos` del CSV: `e85ac74d630dff95` para los bloques A a D (French 202607). Bloque E: `7f6330f17d9d7c84` y `b3166f196d4ffb98`. Bloque F: `baac3d2ceaf0f92a`. Bloque G: `3e07a4896babbbd8` y `6f7a2f88fb30b19e`.
  - `sha256` de los zips de French:
    - 202607: `b840dba55d319f4818fc7300e65c52eff5f64870c8d495fa58ff5d4cd749f5eb`
    - 202407: `0b04328f5d25a6037281de3d7778ebd3932aebffba6fd4eb3fdfec44d4ba5a06`
    - 200607: `6e240321b8b0d53e262e1b00f9750af828a09a66b5335fad0bdcbc8e45674ebb`
    - Los tres están en `R01-datos/SHA256SUMS.txt`.
  - Huellas de las series de Yahoo y FRED: `^GSPC` `ddd4ca74000cd68c`, `DEXMXUS` `3a677532a76a7d0e` e `INTGSTMXM193N` `db8f6e0293183ed1`. Estas series no están congeladas y se vuelven a descargar.
  - sha256 del pre-registro (secciones 1-9): `679f434ac371d0a88cfc1d84933ea40b5ae8c84268a9aca27ee4b30bd0e2e936`. `R01.py` lo verifica al arrancar.
- **Fecha de la corrida final:** 2026-09-25T05:30:38Z (corrida 2; la corrida 1 da cifras idénticas).
- **Evidencia externa del orden temporal.** El guardado automático del repositorio hizo el commit `776b0ec` (2026-09-25 05:24:45 UTC). Ese commit contiene esta ficha con el pre-registro (secciones 1-9, sha256 `679f434a…`, idéntico al actual), sin resultados. También contiene `R01-datos/SHA256SUMS.txt`. Es 4 minutos anterior a la corrida 1 (05:28:44 UTC). La adenda de subperiodos no está en ese commit: aparece en `c255cf5` (05:31:37 UTC), junto con los resultados. Su orden relativo a la corrida 1 (antes) queda declarado por el responsable, no probado por git.
- **Pendientes:**
  - Datos anteriores a 1927 (S&P 500 de GFD o Shiller) para aislar el efecto del periodo 1900-1926 sobre el CAGR.
  - Rezago de 1 día con los datos diarios de French.
  - Capa de impuestos (10% sobre ganancias realizadas en el SIC).
  - Cetes oficiales de Banxico SIE en lugar de la aproximación del IMF en FRED.
  - Spread cambiario de GBM.
  - Condiciones de uso de French, Yahoo y FRED.
  - PBO (no implementado en el laboratorio).
  - Explicar el 63% contra 47% de operaciones positivas.

### Conclusión operable

La regla afectada es **R1** del capítulo 14 (`conocimiento/14-analisis-tecnico-que-sobrevive.md` §6.1): filtro de SMA de 10 meses sobre el índice total return, con evaluación mensual y salida a Cetes.

**Veredicto por la regla pre-registrada: se confirma como filtro de riesgo.**

- El estado es Replicado con diferencias.
- El veredicto fuera de muestra es "Se sostiene".
- El DSR de sma10 es 0.9996 (≥ 0.95).

**Precisiones que deja la réplica.** No cambian el veredicto, pero sí cómo se usa R1:

1. **R1 es un control de drawdown, no una fuente de rendimiento.** Su costo esperado, medido, es de 0.8 a 2.2 pp de CAGR al año frente a comprar y mantener, neto de costos GBM en USD. Fuera de muestra en MXN con Cetes, el costo es de ~1.1 pp. Se usa cuando el objetivo es limitar el drawdown, como en el `drawdown_maximo_duro` del patrimonio principal. **No** se usa para maximizar el CAGR.
   - En la cuenta arena, cuyo objetivo es el mayor rendimiento por temporada de 6 meses, el filtro **resta** rendimiento esperado en mercados alcistas. Su valor ahí es sobrevivir, no ganar.
2. **En MXN, la salida debe ser a pesos** (Cetes o un equivalente), no a efectivo en USD. Si se sale a USD, la protección fuera de muestra cae a 0.199.
3. **El parámetro 10 no tiene nada de especial.** Las longitudes de 6 a 12 meses dan lo mismo en lo cualitativo. No se optimiza. Se mantiene el 10 por ser el pre-registrado y el de la literatura.
4. **La tabla de magnitudes del capítulo 14 (§5.13) debería decir otra cosa en el CAGR.** Hoy dice "CAGR +0.9 pp (bruto)". Con datos CRSP desde 1927, el CAGR es ≈ 0 pp bruto (−0.22 pp en 1927-2005) y −0.8 a −2.2 pp neto. La reducción del drawdown se confirma: ~48% dentro de muestra y ~62% fuera de muestra. **Este documento no edita el capítulo; se deja como propuesta.**
5. **No se valida R2** (filtro de apalancados: media de 200 días diaria + VIX): queda pendiente de su propia réplica.

**Uso con dinero.** Ninguna regla pasa a dinero con esta réplica. Falta la capa de impuestos, el papel de 3 meses con 30 operaciones y la aprobación del dueño (fase 0).
