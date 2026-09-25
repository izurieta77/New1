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
| 2026-09-25, ~05:30 UTC, **antes de la primera corrida** | Se operacionaliza la cláusula de la sección 2 que dice "el efecto aparece solo en algunos subperiodos". Se usan 9 ventanas dentro de muestra: 1927-07 a 1929-12, las décadas de 1930 a 1990 y 2000-01 a 2006-12. Si la reducción relativa del MDD neto de la SMA de 10 meses contra comprar y mantener es mayor que 0 en **menos de 5 de las 9**, el efecto se considera "solo en algunos subperiodos" y el estado queda como "Replicado con diferencias". | La cláusula del pre-registro no tenía un umbral. Se fija antes de ver resultados para que no haya discreción después. Referencia: Faber (2013, p. 28) dice que el timing mejora el drawdown "in all but two decades". | No: se fijó antes de cualquier corrida |
| 2026-09-25, 05:25 UTC, antes de la primera corrida | Los tres zips de French se copiaron a `replicas/R01-datos/` (202607, 202407 y 200607), con el manifiesto `SHA256SUMS.txt`. El script los lee de ahí y se detiene si una huella no coincide. El zip 202607 es byte a byte el mismo del caché (sha256 `b840dba5…`). | Reproducibilidad: el caché `datos/cache/` está en `.gitignore`, y French publica una versión nueva cada mes. Se sigue el precedente de V01. Las condiciones de redistribución siguen pendientes de verificar. | No (mismos bytes) |
| 2026-09-25, 05:30 UTC, **después** de la corrida 1 (05:28 UTC) | (1) Se agregó a `R01.py` un **análisis post-hoc no pre-registrado**: bootstrap pareado de bloques de 12 meses (2000 repeticiones, semilla 20260925) de la diferencia de Sharpe y de la reducción del MDD de sma10 contra comprar y mantener y contra mom12. (2) Se agregó el conteo de operaciones. (3) Se volvió a correr el script completo (corrida 2). | Medir la incertidumbre de la diferencia de Sharpe, que el DSR no mide porque contrasta contra 0 y no contra comprar y mantener. | No cambia ninguna regla, variante, corte ni criterio. La corrida 2 registró otra vez las mismas 49 configuraciones (el CSV tiene 98 corridas; el DSR deduplica por variante y parámetros, así que N sigue en 5). `diff` de `R01-salida.txt` entre las corridas 1 y 2: solo cambian la marca de tiempo y las líneas agregadas; todas las demás cifras son idénticas, incluidos los datos de Yahoo y FRED. El bootstrap se reporta como post-hoc y **no** entra en el estado ni en el veredicto |
| 2026-09-25, 05:33 UTC | Se agregó `R01_verificacion.py`, una doble implementación de sma10 y de comprar y mantener sin el motor. | Auditoría del motor. | No es una variante nueva ni se registra. La diferencia máxima contra el motor es 1.28e-15 |

### 10. Variantes probadas

### 11. Resultados

### 12. Sensibilidad

### 13. Diferencia frente al artículo

### 14. Conclusiones permitidas

### 15. Conclusiones que NO se sostienen

### 16. Estado y reproducción
