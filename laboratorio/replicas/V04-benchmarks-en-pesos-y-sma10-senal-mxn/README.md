# V04. Benchmarks en pesos (S&P 500, IPC vía NAFTRAC, CETES) y SMA de 10 meses con señal en USD o en MXN

> Fecha: 25-sep-2026. Estado: **Replicado con diferencias**. Calificación de la afirmación recibida: **confirmada con matices**. Esto no es una recomendación ni una regla operable. Es fase 0.
>
> **Doble ejecución independiente (2026-09-25):** `independiente.py` se escribió sin leer `reproducir.py` y reproduce las 871 cifras comparadas, todas dentro de tolerancia e idénticas al redondeo impreso. No se corrigió nada. Detalle al final.
>
> Para reproducir, desde la raíz del repo: `python3 laboratorio/replicas/V04-benchmarks-en-pesos-y-sma10-senal-mxn/reproducir.py`. El script no usa red. Los datos están congelados en `datos/` y sus huellas, junto con la del pre-registro (`84aabaa6…`, fijada a las 05:40:32 UTC antes de la primera corrida), en `SHA256SUMS.txt`. La salida `resultados.json` es determinista (dos corridas dan la misma huella). El registro del motor, `V04-variantes.csv`, solo agrega filas.

## Resumen

1. **"S&P en pesos 14.5% al año, 2008-2026": depende de la fecha de inicio.** Con rendimiento total (SPY × DEXMXUS) da **13.97%** del 31-dic-2007 al 31-ago-2026 (W1, la ventana principal) y **14.47%** si se empieza el 31-ene-2008 (W2). Esa segunda ventana deja fuera enero de 2008, cuando el S&P cayó 6.0% en dólares y 6.9% en pesos. Según el mes de inicio, entre ene-2007 y dic-2009 el CAGR va de **13.4% a 17.2%**. Con ^SP500TR, FIX o MXN=X el resultado cambia 0.12 pp o menos.
2. **"IPC vía NAFTRAC 6.3%": se reproduce (6.11% en W1; 6.29% si se corta en jun-2026), pero es un piso.** Yahoo no trae **ningún dividendo de NAFTRAC en 2008-2012 ni en 2021**. Con dividendos, el IPC en MXN rindió probablemente **~6.4-6.7%**. Esa cifra es una estimación post-hoc, obtenida con EWW (MSCI México) e imputando dividendos.
3. **"CETES 6.1%": se reproduce en el borde de la tolerancia.** La subasta de CETES 28 de Banxico da **6.37%** en W1. Cualquier fecha de inicio entre 2007 y 2009 da entre 6.25% y 6.43%. Ninguna definición nuestra llega a 6.1%.
4. **"En 2008 el S&P cayó 47% en dólares, pero solo 21.6% en pesos": las dos cifras usan medidas distintas.** El 47% es la caída diaria de pico a valle **dentro de 2008** en USD (−47.6%, del 31-dic-2007 al 20-nov-2008). El 21.6% se parece al cambio **entre fechas fijas** del año calendario en MXN **sin dividendos** (−22.1%). Con la misma medida en ambas monedas, el amortiguador existe, pero es más chico:
   - Año calendario: **−36.8% en USD contra −19.9% en MXN**.
   - Caída diaria dentro de 2008: **−47.6% contra −34.9%**.
   - Caída mensual de la crisis: **−50.8% contra −31.2%**.
5. **SMA de 10 meses con señal en pesos: la dirección se confirma, pero las cifras exactas no salen en la ventana 2008-2026.** En la ventana pre-registrada de 2008-01 a 2026-08, con costos de GBM:
   - Con ejecución idealizada al mismo cierre (T0) da **15.23% contra 13.97%** de comprar y mantener, con caída máxima de **−12.2% contra −28.4%**.
   - Con ejecución al primer día hábil del mes siguiente (T1, la principal) da **15.50% contra 13.97%**, con caída de **−12.7% contra −29.5%**.
   - Las cifras recibidas (14.6% contra 13.5%, y 12% contra 31%) aparecen **solo si la evaluación empieza en 2007**. Por ejemplo, de jul-2007 a ago-2026 da 14.74% contra 13.51% y −12.2% contra −31.2%. Esta búsqueda es post-hoc. El −31% de comprar y mantener viene del pico de septiembre de 2007.
6. **La ventaja de rendimiento de la SMA no es estadísticamente distinguible de cero.** La diferencia mensual (SMA10-MXN-T1 menos comprar y mantener) da **+0.99 pp al año, con t NW(6) = 0.55**: inconcluso en 2008-2026. También es inconcluso en 1995-2007 (t = 0.34) y en 1995-2026 (t = 0.64).
7. **La señal en pesos no es mejor en todos los periodos.** En 1995-2007 la SMA10 con señal en USD rindió 20.8% y la de MXN 18.3%, con caídas de −10.8% y −19.0% (T1). En 2008-2026 fue al revés: la señal en USD **perdió** contra comprar y mantener en pesos (12.2% contra 14.0%).
8. **Lo robusto es la reducción de la caída máxima.** Las 16 variantes registradas (SMA de 6, 8, 10 y 12 meses, señal USD o MXN, T0 o T1) tienen una caída máxima menor que comprar y mantener en los dos subperiodos. En 2008-2026 va de −10.4% a −21.7%, contra −28.4% y −29.5%. En 1995-2007 va de −8.7% a −20.4%, contra −36.3% y −39.9%.
9. **Sharpe deflactado (N = 16).** SMA10-MXN-T1 da DSR = **0.997** en 2008-2026 y **0.32** en 1995-2007. El DSR contrasta el Sharpe contra cero, **no contra comprar y mantener**. Comprar y mantener tiene PSR de 0.99 en el mismo tramo de 2008-2026, así que un DSR alto ahí no prueba que la SMA agregue valor.
10. **El S&P en pesos le ganó a CETES en 2008-2026, pero no en 1995-2007.** De 2008 a 2026 el diferencial fue de +7.8 pp al año como media × 12, con t = 2.39 ("apoyo"). De 1995 a 2007, CETES rindió 18.3% anual y el S&P en MXN 18.0%, con t = 0.22.

## Por qué existe

El resumen de laboratorio recibido el 25-sep-2026 afirma, entre las "ventajas que sobreviven":

- "El S&P en pesos. Entre 2008 y 2026 rindió 14.5% al año. El IPC, medido con NAFTRAC, rindió 6.3% y CETES 6.1%. Además el peso amortigua las caídas: en 2008 el S&P cayó 47% en dólares, pero solo 21.6% en pesos."
- "La media móvil de 10 meses con la señal medida en pesos. Aplicada al S&P, rindió 14.6% contra 13.5% de solo mantener, y la peor caída fue de 12% en vez de 31%."

Regla del sistema: ninguna cifra ajena se adopta sin verificarla con datos y código propios. V04 también atiende las alertas de datos #1, #2 y #3 de `laboratorio/alertas-de-datos.md`.

---

## PRE-REGISTRO

Lo que sigue es la copia literal de `prerregistro.md`, escrito el 2026-09-25 a las 05:40 UTC. Su huella SHA-256 (`84aabaa6…`) quedó en `SHA256SUMS.txt` a las 05:40:32 UTC, antes de la primera corrida. Los encabezados bajan un nivel.

> Escrito el 2026-09-25 a las 05:40 UTC, **antes** de calcular cualquier rendimiento, CAGR, caída, media, t o Sharpe con estos datos. Su huella SHA-256 queda en `SHA256SUMS.txt` antes de la primera corrida. Cualquier cambio posterior va a "Desviaciones del pre-registro" en `README.md`; este archivo no se edita.
>
> Lo único que se miró antes de escribirlo fue la **estructura** de los archivos descargados: rango de fechas, zona horaria, número de barras sin precio, moneda y lista de eventos de dividendos (fechas y montos). No se calculó ningún rendimiento. Lo que esa revisión mostró y afecta el diseño:
>
> - `NAFTRAC.MX` en Yahoo **empieza el 2008-01-02** (el ETF existe desde 2002). Sus eventos de dividendo en Yahoo **no tienen ninguno en 2008-2012 ni en 2021**. Esto confirma estructuralmente la alerta de datos #1: el `adjclose` de NAFTRAC en Yahoo omite dividendos en al menos esos años y su rendimiento es un **piso**.
> - `SPY.MX` e `IVV.MX` (cotización del SIC en MXN) empiezan en 2008-01-02 y sus dividendos en Yahoo están en **USD hasta 2015 y en MXN desde 2016**: su `adjclose` en MXN es inconsistente antes de 2016.
> - `DEXMXUS` (FRED) va de 1993-11-08 a 2026-09-18. FIX de Banxico (SF43718) va de 1991-11-12 a 2026-09-24. `MXN=X` (Yahoo) empieza en 2003-12-01. CETES 28 de Banxico (SF43936, subasta semanal, fecha de colocación) va de 1982 a la subasta del 2026-09-24. SPY en Yahoo va de 1993-01-29 a 2026-09-24, sin barras vacías.

### 1. Afirmaciones recibidas (del resumen de laboratorio del 25-sep-2026)

- **A1.** "El S&P en pesos. Entre 2008 y 2026 rindió 14.5% al año."
- **A2.** "El IPC, medido con NAFTRAC, rindió 6.3%."
- **A3.** "CETES 6.1%."
- **A4.** "En 2008 el S&P cayó 47% en dólares, pero solo 21.6% en pesos."
- **A5.** "La media móvil de 10 meses con la señal medida en pesos. Aplicada al S&P, rindió 14.6% contra 13.5% de solo mantener, y la peor caída fue de 12% en vez de 31%."

Regla del sistema: ninguna cifra ajena se adopta sin verificarla con datos y código propios.

### 2. Hipótesis previas (con signo) y mecanismo

- **H-A (benchmarks).** Espero que A1 (≈14.5%), A2 (≈6.3%) y A3 (≈6.1%) se reproduzcan dentro de la tolerancia en al menos una ventana razonable de "2008-2026", pero con **sensibilidad alta a la fecha de inicio** en A1: arrancar antes o después de la devaluación de octubre de 2008 cambia mucho el CAGR en MXN. Espero que A2 sea un **piso** por los dividendos faltantes de NAFTRAC en Yahoo.
- **H-A4.** Espero que "47% en dólares" y "21.6% en pesos" **no** sean la misma medida: 21.6% se parece al cambio entre fechas fijas del año calendario 2008 en MXN, y 47% se parece más a una caída de pico a valle en USD. Si es así, la comparación mezcla medidas y exagera el "amortiguador" del peso.
- **H-B (SMA10).** Espero que la SMA de 10 meses **reduzca la caída máxima** en MXN frente a comprar y mantener, y que la diferencia de rendimiento medio mensual (SMA − comprar y mantener) sea **estadísticamente inconclusa** (IC95 NW que incluye 0) tanto en 2008-2026 como en 1995-2007. No tengo expectativa firme sobre el signo de la diferencia de CAGR. Espero que el Sharpe deflactado sea < 0.95.
- **Mecanismo del amortiguador.** En episodios de aversión global al riesgo el peso se deprecia contra el dólar (correlación negativa entre el S&P en USD y MXN/USD), así que un activo en USD medido en MXN cae menos. **Mecanismo de la SMA:** agrupamiento de volatilidad y tendencia (ver R01). Medir la señal en MXN mezcla la tendencia del S&P con la del tipo de cambio: la señal en MXN tiende a quedarse invertida cuando el peso se deprecia.

### 3. Datos (congelados en `datos/`, huellas en `SHA256SUMS.txt`; descargados el 2026-09-25 ≈05:37 UTC con `descargar_datos.py`)

| Serie | Archivo | Uso |
|---|---|---|
| SPY diario, `adjclose` y `close`, dividendos | `yahoo_SPY_1d.json` | **Principal** del S&P 500 con rendimiento total (ETF operable en el SIC; incluye su gasto de 0.0945% anual) |
| S&P 500 Total Return | `yahoo_SP500TR_1d.json` | Sensibilidad (índice, sin gasto) |
| S&P 500 precio | `yahoo_GSPC_1d.json` | A4 en precio y señal sobre precio |
| NAFTRAC diario, `adjclose` y `close`, dividendos | `yahoo_NAFTRAC.MX_1d.json` | **Principal** de A2 (como se afirmó) |
| IPC (precio) | `yahoo_MXX_1d.json` | Sensibilidad de A2 (sin dividendos) |
| MXN por USD, FRED `DEXMXUS` (mediodía NY) | `fred_DEXMXUS.csv` | **Principal** de conversión |
| MXN por USD, Banxico FIX `SF43718` | `banxico_CF102_fix_SF43718.csv` | Sensibilidad de conversión |
| MXN por USD, Yahoo `MXN=X` | `yahoo_MXN_X_1d.json` | Sensibilidad de conversión (desde 2003-12) |
| CETES 28 días, tasa de rendimiento de la subasta semanal, Banxico `SF43936` (fecha de colocación) | `banxico_CF107_cetes28_SF43936.csv` | **Principal** de A3 y efectivo de la SMA |
| Tasa de T-bills de México (FMI, vía FRED `INTGSTMXM193N`, mensual) | `fred_INTGSTMXM193N.csv` | Contraste de CETES |
| SPY.MX, IVV.MX, VOO.MX (SIC en MXN) | `yahoo_*.MX_1d.json` | Solo búsqueda del origen de las cifras y control de la conversión cambiaria; **no** para resultados principales |

### 4. Construcción de series (fija)

- **Cierre de mes en MXN.** E_m = último día del mes m con precio de SPY **y** tipo de cambio en la **misma fecha**. P_MXN(E_m) = P_USD(E_m) × FX(E_m). Nunca se combina un precio de un día con un tipo de cambio de otro (alerta #3). Se reporta cuántos meses tienen E_m distinto del último día hábil de SPY.
- **Cierre de mes en USD:** último día de negociación de SPY del mes.
- **NAFTRAC:** último día del mes con `adjclose` no vacío (calendario de BMV). Inicio: 2008-01-02 (primer dato de Yahoo).
- **Índice de CETES.** I(d) se acumula con interés simple entre subastas: para la colocación a_k ≤ d < a_{k+1}, I(d) = I(a_k) × (1 + y_k/100 × (d − a_k)/360), donde y_k es la tasa de la subasta con fecha de colocación a_k. El rendimiento de cualquier periodo (d0, d1] es I(d1)/I(d0) − 1. Sensibilidad: partición mensual, con la tasa de la última subasta ≤ inicio de mes, y r = y × días/360.
- **CAGR** = (V1/V0)^(1/años) − 1 con años = días calendario / 365.25. **Media × 12 no es CAGR**; ambos se reportan donde aplica.
- **Caída máxima (MDD):** de pico a valle sobre la curva (mensual y diaria por separado). **Cambio entre fechas fijas** se reporta aparte (alerta #2).
- Sin costos en A1-A4 (son rendimientos de referencia). Sin impuestos en todo V04: no se modela el ISR de 10% sobre ganancias del SIC, la retención de dividendos de EUA (30%, o 10% con W-8BEN) ni la retención sobre intereses de CETES. Como sensibilidad se calcula el S&P con dividendos netos de 30% de retención.

### 5. Ventanas para A1-A3 (lista cerrada)

| Clave | Inicio | Fin | Nota |
|---|---|---|---|
| **W1 (principal)** | 2007-12-31 | 2026-08-31 | Último mes completo. NAFTRAC arranca en 2008-01-02 (su primer dato) |
| W2 | 2008-01-31 | 2026-08-31 | Todos a cierre de mes |
| W3 (diaria) | 2008-01-02 | 2026-09-18 | Primer dato común con NAFTRAC; último dato común con DEXMXUS |
| W4 | 2007-12-31 | 2025-12-31 | Años calendario 2008-2025 completos |
| Sensibilidad de inicio | cada cierre de mes de 2007-01 a 2009-12 | 2026-08-31 | Se reporta el rango (mín., máx.) y puntos seleccionados |
| Sensibilidad de fin | 2007-12-31 | 2025-12-31, 2026-06-30, 2026-08-31, 2026-09-18 | |

**Pruebas (NW de 6 rezagos sobre diferencias mensuales, W1 y 1995-2007 donde haya datos):** S&P MXN − CETES; S&P MXN − NAFTRAC; NAFTRAC − CETES. Veredicto: "apoyo" si el límite inferior del IC95 > 0, "contraria" si el superior < 0, "inconcluso" en otro caso.

**Amortiguador (descriptivo, W1):** correlación mensual entre el rendimiento del S&P en USD y la variación de MXN/USD; variación media de MXN/USD en los meses con S&P en USD < −5%; MDD en USD frente a MDD en MXN.

### 6. A4 (2008): medidas registradas

Para SPY (rendimiento total), ^SP500TR y ^GSPC (precio), en USD y en MXN (DEXMXUS; FIX como sensibilidad):

1. Cambio entre fechas fijas del año calendario: 2007-12-31 → 2008-12-31.
2. Caída máxima **dentro de 2008** (pico y valle entre 2007-12-31 y 2008-12-31), diaria y mensual.
3. Caída máxima de la crisis (pico desde 2007-01-01, valle hasta 2009-12-31), diaria y mensual.

### 7. SMA de 10 meses (A5)

**Activo:** S&P 500 con rendimiento total en MXN = SPY `adjclose` × DEXMXUS en la misma fecha. **Efectivo:** CETES 28 (índice de §4), en MXN. Mensual, 0 o 1, sin apalancamiento ni cortos.

**Regla.** Al cierre E_{m−1}: w_m = 1 si P(E_{m−1}) > media(P(E_{m−10}), …, P(E_{m−1})); si no, 0 (empate → 0).
- **Señal USD:** P = SPY `adjclose` en USD en E. **Señal MXN:** P = SPY `adjclose` × FX en E.
- **Ejecución T0 (idealizada, Faber):** se opera al mismo cierre E_{m−1}; periodos de E a E.
- **Ejecución T1 (principal):** se opera al cierre del **primer día hábil del mes siguiente** F_{m−1} (primer día del mes m con SPY y FX); periodos de F a F. La señal sigue siendo la del cierre E_{m−1}.

**Costos GBM (por defecto):** comisión 0.25% + IVA = 0.29% por lado (hecho, Guía GBM V1025) + spread 0.05% por lado (**supuesto**), cobrados sobre |Δw| (motor `herramientas/backtest.py`). La entrada inicial también paga.

**Muestra:** evaluación de 1995-01 a 2026-08 (el primer dato de DEXMXUS es 1993-11; 12 cierres de historia en MXN antes de 1995 para todas las ventanas). Dos segmentos: **1995-2007** y **2008-2026** (esta es la ventana de la afirmación). La posición al inicio de 2008 viene del segmento anterior.

**Variantes de prueba (`es_prueba=1`, N = 16):** SMA n ∈ {6, 8, 10, 12} × señal {USD, MXN} × ejecución {T0, T1}.

**Referencias (`es_prueba=0`):** comprar y mantener (T0 y T1) y 100% CETES.

**Sensibilidades (`es_prueba=0`), para SMA10 USD y MXN y comprar y mantener:**
- Costos: sin costos; spread medio (0.29% + 0.15%); doble pierna (0.58% + 0.10%).
- Datos: ^SP500TR en lugar de SPY; FIX en lugar de DEXMXUS; MXN=X (desde 2004); señal sobre precio sin dividendos (SPY `close`); dividendos netos de 30% de retención; CETES con partición mensual.
- Corrida aislada 2008-01 a 2026-08 (entra desde cero en 2008).
- **Búsqueda de origen (no es evidencia):** (i) historia de la señal que solo empieza en 2008-01 (primera decisión a fin de oct-2008); (ii) SPY.MX `adjclose` como activo y como señal.

**Métricas:** CAGR, volatilidad anual, MDD mensual, Sharpe anual del exceso sobre CETES, tiempo invertido, cambios de señal y costo anual.

**Prueba principal:** media de la diferencia mensual de rendimientos netos (SMA10 − comprar y mantener) con NW(6), en 2008-2026, 1995-2007 y 1995-2026, para señal USD y señal MXN, T1 (principal) y T0. Veredicto como en §5.

**Sharpe deflactado:** `sharpe_deflactado_de_registro` con N = 16 en el segmento 2008-2026, para SMA10-MXN-T1 (principal), SMA10-MXN-T0 y la mejor variante; también en 1995-2007. Umbral 0.95 (`config/parametros.json`). El DSR contrasta el Sharpe contra 0 ajustado por búsqueda, **no** contra comprar y mantener.

### 8. Criterios para las afirmaciones

- **Tolerancias:** CAGR ±0.30 pp; caídas y cambios porcentuales ±1.0 pp.
- **A1-A3:** "se reproduce" si W1 cae dentro de la tolerancia; "se reproduce con otra ventana" si solo alguna ventana registrada (W2-W4 o la sensibilidad de inicio y fin) lo hace; "no se reproduce" en otro caso.
- **A4:** se reporta qué medida registrada coincide con 47% y cuál con 21.6%. Si no son la misma medida, la afirmación se califica como mezcla de medidas.
- **A5:** "se reproduce" si SMA10-MXN (T0 o T1) en 2008-2026 cae dentro de ±0.30 pp en CAGR y ±1.0 pp en MDD de 14.6%/12%, y comprar y mantener dentro de lo mismo de 13.5%/31%.
- **Calificación global de la afirmación recibida:**
  - "confirmada": A1-A5 se reproducen en su definición principal y la SMA10-MXN tiene "apoyo" en la diferencia contra comprar y mantener con DSR ≥ 0.95.
  - "confirmada con matices": las cifras se reproducen (en alguna definición registrada), pero con alguna de estas condiciones: solo con otra ventana, mezcla de medidas, dato que es piso, diferencia inconclusa, DSR < 0.95.
  - "no confirmada": las cifras centrales no se reproducen con ninguna definición registrada.

### 9. Conclusión operable (reglas fijadas de antemano)

- La SMA10 con señal en MXN solo puede pasar a candidata (papel, no dinero) si: la diferencia contra comprar y mantener tiene "apoyo" en 2008-2026 **y** no es "contraria" en 1995-2007, **y** DSR ≥ 0.95, **y** la reducción de MDD se mantiene con T1 y con costos. Si solo reduce la caída sin ventaja de rendimiento significativa, se clasifica como **control de riesgo**, no como fuente de rendimiento.
- Los benchmarks verificados se usan como **metas a superar** en MXN, con su ventana y definición explícitas.

---

## RESULTADOS (después de correr)

### Desviaciones del pre-registro

| Fecha (UTC) | Qué cambió | Por qué | ¿Invalida algo? |
|---|---|---|---|
| 2026-09-25 05:41-05:44 | Dos arranques fallidos de `reproducir.py`. El primero comparaba mal el respaldo de `close` cuando `adjclose` es nulo. El segundo dividía entre cero al calcular el Sharpe de la referencia 100% CETES, cuyo exceso es 0. Se corrigió el código. | Errores de programación | No. El método no cambió. Las filas parciales de esos arranques quedaron en `V04-variantes.csv`, que solo agrega filas. El DSR usa la última corrida de cada variante, así que N sigue siendo 16. |
| 2026-09-25 | Las pruebas NW contra NAFTRAC usan 2008-02 a 2026-08, que es el primer mes completo de NAFTRAC. | NAFTRAC empieza el 2008-01-02, y un enero parcial desalinearía un día la resta contra el S&P. | No. Es una aclaración de "donde haya datos" (§5). |
| 2026-09-25 05:48 | **POST-HOC.** Se descargó EWW (iShares MSCI Mexico, USD) y se agregó a `datos/` y a `descargar_datos.py`. Con él se estimó el IPC con dividendos. | NAFTRAC en Yahoo no trae dividendos en 6 años, y S&P DJI (IPC Total Return) respondió 403 a la consulta. | No cambia ningún veredicto. Es solo contexto. La huella del pre-registro no cambió; `SHA256SUMS.txt` se regeneró con el archivo nuevo. |
| 2026-09-25 | **POST-HOC.** Se buscó la ventana que produce las cifras recibidas de A5: 16 corridas con inicio en 2007 y fin en jun o ago de 2026, con `es_prueba=0`. | Ninguna ventana registrada reproducía 14.6/13.5/12/31. | No. No entran en N, no tienen veredicto y no son evidencia. Solo sirven para saber qué midió quien dio la cifra. |
| 2026-09-25 | Se agregaron controles cruzados (el motor contra el código de benchmarks y contra `metricas.py`), el PSR de referencia de comprar y mantener y la variación del tipo de cambio en W1. | Control de calidad y contexto | No |
| 2026-09-25 | La búsqueda de origen (ii) con SPY.MX `adjclose` resultó **inservible**. La serie de Yahoo mezcla cotizaciones en USD y en MXN hasta 2012: por ejemplo, 104.48 el 2008-08-29 y 1,083.44 el 2008-09-01, con 95 saltos mayores a 30%. | Defecto de datos | No. Sus cifras (caída de −100%, CAGR de 33%) se reportan solo como diagnóstico. |

Nota menor: el CSV de CETES se exportó desde 1990, no desde 1982 como dice el §3. Para V04 basta con datos desde 1993.

### Controles de calidad

- **Huellas.** Se verifican al inicio: datos, `descargar_datos.py` y `prerregistro.md`.
- **Parsers.** El parser propio de Yahoo coincide exactamente con `herramientas.datos_historicos.parsear_yahoo_historia` en 10 archivos: la diferencia relativa máxima es 0. El de FRED es idéntico a `herramientas.datos.parsear_fred_csv`. Los dos parsers de Banxico (partición manual y módulo `csv`) coinciden.
- **Motor contra simulador propio.** `herramientas/backtest.py` se contrastó con una simulación escrita aparte, que implementa la señal, la deriva, los costos y las métricas, en las 104 corridas (88 pre-registradas y 16 post-hoc; todas quedan en `V04-variantes.csv`). Las exposiciones son idénticas y los rendimientos netos coinciden con tolerancia de 1e-10. La diferencia máxima en CAGR, caída máxima, volatilidad y Sharpe es de **2.3e-15**.
- **Newey-West.** La herramienta coincide con la forma cuadrática de Bartlett completa: diferencia máxima de 6.1e-18.
- **Controles cruzados** (diferencia máxima de 0):
  - Comprar y mantener del motor en 2008-2026 (13.97% y −28.43%) coincide con el benchmark W1 y con la caída mensual del bloque "amortiguador".
  - CAGR y caída máxima propios coinciden con `metricas.py`.
- **Rendimiento total reconstruido.** Reconstruir SPY con cierre + dividendos brutos da 13.97% en W1, igual que `adjclose`.
- **Alineación de fechas (alerta #3).** Precio y tipo de cambio siempre se toman en la misma fecha. En 4 meses el cierre de mes usado no fue el último día de SPY, porque ese día faltaba el DEXMXUS.
- **Conversión frente al SIC** (2016 en adelante). Se comparó SPY.MX `close` contra SPY `close` × FX en la misma fecha. La mediana de la diferencia absoluta es 0.21% con DEXMXUS y 0.21% con FIX, y el percentil 90 es 0.63%. Con MXN=X la mediana es 0.33%. Esto incluye la diferencia de hora entre el cierre del SIC y la hora del tipo de cambio.

### 1. A1-A3: CAGR de referencia en MXN (sin costos ni impuestos)

| Serie | W1: 2007-12-31 a 2026-08-31 | W2: 2008-01-31 a 2026-08-31 | W3: 2008-01-02 a 2026-09-18 | W4: 2007-12-31 a 2025-12-31 |
|---|---|---|---|---|
| **S&P 500 TR en MXN: SPY `adjclose` × DEXMXUS (principal)** | **13.97%** | **14.47%** | 14.05% | 14.10% |
| SPY × FIX (Banxico) | 13.97% | 14.47% | 14.05% | 14.10% |
| SPY × MXN=X (Yahoo) | 13.99% | 14.48% | 14.02% | 14.10% |
| ^SP500TR × DEXMXUS | 14.05% | 14.55% | 14.17% | 14.18% |
| SPY con dividendos netos de 30% de retención × DEXMXUS | 13.35% | 13.85% | 13.43% | 13.47% |
| ^GSPC precio (sin dividendos) × DEXMXUS | 11.90% | 12.39% | 12.02% | 12.00% |
| S&P 500 TR en USD (SPY) | 11.29% | 11.72% | 11.29% | 10.97% |
| **NAFTRAC `adjclose` (Yahoo; desde 2008-01-02, su primer dato)** | **6.11%** | 6.13% | 5.92% | 6.15% |
| NAFTRAC `close` (sin ajuste) | 4.48% | 4.49% | 4.29% | 4.56% |
| ^MXX (IPC precio) | 4.35% | 4.52% | 4.33% | 4.42% |
| **CETES 28 (Banxico SF43936, subasta semanal)** | **6.37%** | 6.37% | 6.37% | 6.35% |
| *Post-hoc:* EWW `adjclose` × DEXMXUS (MSCI México con rendimiento total) | 6.42% | 6.56% | 6.38% | 6.32% |
| *Post-hoc:* EWW precio × DEXMXUS | 4.15% | 4.27% | 4.11% | 4.05% |

**Otras formas de calcular CETES en W1:**

- Con partición mensual (tasa de la última subasta ≤ inicio de mes): 6.36%.
- Con la tasa mensual del FMI (FRED `INTGSTMXM193N`, tasa/1200, de 2008-01 a 2026-07): 6.26%.

**Sensibilidad a la fecha de inicio (fin 2026-08-31; cada inicio es un cierre de mes).**

| Serie | Mínimo | Máximo | Inicios seleccionados |
|---|---|---|---|
| S&P TR en MXN | 13.41% (inicio 2007-01) | 17.18% (inicio 2009-02) | 2007-06: 13.53%; 2007-09: 13.53%; 2007-12: 13.97%; **2008-01: 14.47%**; 2008-02: 14.75%; 2008-03: 14.94%; 2008-04: 14.79%; 2008-06: 15.52%; 2008-12: 16.27%; 2009-03: 17.13%; 2009-12: 16.09% |
| NAFTRAC `adjclose` | 5.62% (inicio 2008-05) | 9.54% (inicio 2009-02) | 2008-01: 6.13%; 2008-06: 6.16%; 2008-12: 7.99%; 2009-06: 7.69%; 2009-12: 6.17% |
| CETES 28 | 6.25% (inicio 2009-04) | 6.43% (inicio 2007-01) | 2007-12: 6.37%; 2008-12: 6.28% |
| S&P TR en USD | 10.74% (inicio 2007-05) | 16.38% (inicio 2009-02) | 2007-12: 11.29%; 2008-12: 14.91% |

**Sensibilidad a la fecha de fin** (inicio 2007-12-31):

| Serie | 2025-12-31 | 2026-06-30 | 2026-08-31 | 2026-09-18 |
|---|---|---|---|---|
| S&P TR en MXN | 14.10% | 14.09% | 13.97% | 13.98% |
| NAFTRAC | 6.15% | **6.29%** | 6.11% | 5.92% |
| CETES | 6.35% | 6.37% | 6.37% | 6.37% |

**Dividendos de NAFTRAC en Yahoo (alerta #1).** El dividendo implícito anual se calcula como `(1 + adj) / (1 + close) − 1`. Vale **0.00% en 2008, 2009, 2010, 2011, 2012 y 2021**, y Yahoo no registra ningún evento de dividendo en esos años. En los otros años va de 0.5% a 4.3%, por ejemplo 2019 = 3.04%, 2023 = 3.43% y 2025 = 4.30%.

**Estimación post-hoc.** Se imputa en esos 6 años el dividendo implícito de EWW, que en USD fue de 2.27%, 1.60%, 0.96%, 1.40%, 1.23% y 2.19%. Así, NAFTRAC en W1 pasaría de 6.11% a **6.66%**. Es una estimación: EWW sigue al MSCI México, no al IPC.

**Contraste con BlackRock.** La página oficial de NAFTRAC, al 31-jul-2026, reporta como "NAV total return" anual de 2022 a 2025 −9.24%, 17.93%, −13.23% y 29.17%. Su "benchmark" da −9.03%, 18.41%, −13.72% y 29.88%, cifras **idénticas a las del ^MXX de precio** en nuestros datos. Ni esa página ni Yahoo sirven, entonces, como fuente del IPC con dividendos. **Pendiente:** conseguir el S&P/BMV IPC Total Return oficial (S&P DJI bloqueó el acceso).

**Pruebas Newey-West (6 rezagos) sobre diferencias mensuales en MXN:**

| Prueba | n | Media %/mes | ×12 (no es CAGR) | t NW(6) | t IID | IC95 NW (%/mes) | Veredicto |
|---|---|---|---|---|---|---|---|
| S&P MXN − CETES, 2008-01 a 2026-08 | 224 | 0.653 | 7.84% | 2.39 | 2.50 | [0.117, 1.190] | **apoyo** |
| S&P MXN − CETES, 1995-01 a 2007-12 | 156 | 0.075 | 0.90% | 0.22 | 0.21 | [−0.602, 0.753] | inconcluso |
| S&P MXN − NAFTRAC, 2008-02 a 2026-08 | 223 | 0.600 | 7.21% | 1.64 | 1.75 | [−0.119, 1.320] | inconcluso |
| NAFTRAC − CETES, 2008-02 a 2026-08 | 223 | 0.090 | 1.08% | 0.27 | 0.29 | [−0.552, 0.732] | inconcluso |

**Amortiguador del peso (descriptivo, W1, mensual):**

- La correlación entre el S&P en USD y la variación de MXN/USD es **−0.56**.
- En los 24 meses con el S&P en USD por debajo de −5% (media −7.90%), el peso se depreció en promedio **+4.54%**, y el S&P en MXN cayó en promedio −3.79%.
- La caída máxima mensual en W1 fue −48.2% en USD y **−28.4% en MXN**. La volatilidad anual fue 15.7% en USD y 13.5% en MXN.
- MXN/USD pasó de 10.92 a 17.01, un CAGR de **+2.40%**. Eso explica la diferencia de 2.7 pp entre el S&P en MXN (13.97%) y en USD (11.29%), porque 1.1129 × 1.0240 − 1 = 13.96%.
- NAFTRAC en W1 tuvo volatilidad de 16.1% y caída máxima mensual de −45.0%.

### 2. A4: 2008, medida por medida

| Medida | SPY TR USD | ^SP500TR USD | ^GSPC precio USD | SPY TR MXN (DEXMXUS) | ^SP500TR MXN | ^GSPC precio MXN | SPY TR MXN (FIX) |
|---|---|---|---|---|---|---|---|
| Cambio del 2007-12-31 al 2008-12-31 | −36.79% | −37.00% | −38.49% | −19.92% | −20.17% | **−22.06%** | −19.91% |
| Caída diaria dentro de 2008 (pico 2007-12-31, valle 2008-11-20) | **−47.58%** | **−47.71%** | −48.76% | −34.88% | −35.04% | −36.35% | −34.81% |
| Caída mensual dentro de 2008 (valle nov-2008) | −37.41% | −37.66% | −38.96% | −23.23% | −23.54% | −25.14% | −23.61% |
| Caída diaria de la crisis 2007-2009 | −55.19% (2007-10-09 a 2009-03-09) | −55.25% | −56.78% | −38.33% (2007-10-09 a 2008-11-20) | −38.27% | −39.79% | −38.32% |
| Caída mensual de la crisis 2007-2009 | −50.78% (oct-2007 a feb-2009) | −50.95% | −52.56% | −31.15% (sep-2007 a feb-2009) | −31.22% | −33.55% | −31.23% |

Coincidencias dentro de ±1.0 pp:

- **47% en USD:** solo la caída diaria dentro de 2008 (SPY −47.58% y ^SP500TR −47.71%).
- **21.6% en MXN:** solo el cambio entre fechas fijas del año calendario **sin dividendos** (^GSPC × DEXMXUS −22.06%; ^GSPC × FIX −22.05%). Con dividendos da −19.9%.

La afirmación compara una caída diaria de pico a valle en USD contra un cambio entre fechas fijas en MXN.

### 3. A5: SMA de 10 meses en MXN (costos GBM 0.29% + 0.05% por lado; efectivo en CETES 28)

**Tabla principal. 2008-2026** (segmento de la corrida 1995-2026; la posición de inicio viene de dic-2007):

| Regla | Ejecución | CAGR | Vol | Sharpe (exceso sobre CETES) | Caída máx. mensual | Tiempo invertido | Cambios de señal | Costo anual |
|---|---|---|---|---|---|---|---|---|
| Comprar y mantener | T0 | 13.97% | 13.46% | 0.579 | −28.43% | 100% | 0 | 0.000% |
| SMA10 señal USD | T0 | 12.26% | 10.78% | 0.552 | −19.87% | 78.1% | 32 | 0.583% |
| **SMA10 señal MXN** | T0 | **15.23%** | 11.21% | 0.770 | **−12.23%** | 78.6% | 18 | 0.328% |
| Comprar y mantener | T1 | 13.97% | 14.38% | 0.552 | −29.50% | 100% | 0 | 0.000% |
| SMA10 señal USD | T1 | 12.16% | 11.08% | 0.534 | −21.68% | 78.1% | 32 | 0.583% |
| **SMA10 señal MXN (principal)** | **T1** | **15.50%** | 11.55% | 0.772 | **−12.71%** | 78.6% | 18 | 0.328% |
| 100% CETES | T0 | 6.37% | 0.72% | — | 0.00% | 0% | 0 | 0 |

T0 ejecuta al mismo cierre de la señal (idealizado). T1 ejecuta al cierre del primer día hábil del mes siguiente.

**1995-2007** (fuera de la ventana de la afirmación):

| Regla | Ejecución | CAGR | Vol | Sharpe | Caída máx. | Cambios |
|---|---|---|---|---|---|---|
| Comprar y mantener | T0 | 18.01% | 15.85% | 0.058 | −39.87% | 1 |
| SMA10 señal USD | T0 | 21.22% | 13.14% | 0.256 | −8.66% | 11 |
| SMA10 señal MXN | T0 | 18.86% | 13.77% | 0.099 | −20.36% | 21 |
| Comprar y mantener | T1 | 17.02% | 14.97% | −0.006 | −36.26% | 1 |
| SMA10 señal USD | T1 | 20.83% | 12.29% | 0.239 | −10.79% | 11 |
| SMA10 señal MXN | T1 | 18.26% | 12.83% | 0.056 | −19.00% | 21 |
| 100% CETES | T0 | 18.33% | 3.88% | — | 0.00% | 0 |

**Las 16 variantes de prueba** (`es_prueba=1`; cada celda da CAGR / caída máxima / Sharpe):

| Variante | 1995-2007 | 2008-2026 | 1995-2026 (CAGR / caída máx.) |
|---|---|---|---|
| sma6_usd_T0 | 17.23% / −16.92% / −0.030 | 11.83% / −10.41% / 0.572 | 14.02% / −16.92% |
| sma8_usd_T0 | 19.28% / −8.66% / 0.124 | 13.85% / −19.87% / 0.712 | 16.05% / −19.87% |
| sma10_usd_T0 | 21.22% / −8.66% / 0.256 | 12.26% / −19.87% / 0.552 | 15.85% / −19.87% |
| sma12_usd_T0 | 22.36% / −8.66% / 0.329 | 12.95% / −13.86% / 0.615 | 16.72% / −13.86% |
| sma6_mxn_T0 | 17.69% / −20.02% / 0.020 | 13.09% / −15.10% / 0.632 | 14.96% / −20.02% |
| sma8_mxn_T0 | 20.55% / −12.85% / 0.212 | 14.98% / −11.78% / 0.761 | 17.23% / −12.85% |
| sma10_mxn_T0 | 18.86% / −20.36% / 0.099 | 15.23% / −12.23% / 0.770 | 16.71% / −20.36% |
| sma12_mxn_T0 | 20.44% / −12.73% / 0.201 | 14.76% / −13.86% / 0.724 | 17.06% / −13.86% |
| sma6_usd_T1 | 19.14% / −12.45% / 0.117 | 11.63% / −12.09% / 0.544 | 14.65% / −12.45% |
| sma8_usd_T1 | 20.52% / −10.79% / 0.217 | 13.49% / −21.68% / 0.665 | 16.32% / −21.68% |
| sma10_usd_T1 | 20.83% / −10.79% / 0.239 | 12.16% / −21.68% / 0.534 | 15.64% / −21.68% |
| sma12_usd_T1 | 21.73% / −10.79% / 0.301 | 12.59% / −14.95% / 0.576 | 16.26% / −14.95% |
| sma6_mxn_T1 | 18.10% / −15.72% / 0.045 | 13.00% / −16.71% / 0.605 | 15.07% / −16.71% |
| sma8_mxn_T1 | 20.05% / −11.09% / 0.184 | 15.27% / −12.71% / 0.761 | 17.21% / −12.71% |
| sma10_mxn_T1 | 18.26% / −19.00% / 0.056 | 15.50% / −12.71% / 0.772 | 16.63% / −19.00% |
| sma12_mxn_T1 | 19.61% / −11.25% / 0.151 | 14.85% / −13.55% / 0.715 | 16.78% / −13.55% |
| *comprar y mantener T0* | 18.01% / −39.87% / 0.058 | 13.97% / −28.43% / 0.579 | 15.61% / −39.87% |
| *comprar y mantener T1* | 17.02% / −36.26% / −0.006 | 13.97% / −29.50% / 0.552 | 15.21% / −36.26% |

- En 2008-2026, las 8 parejas USD/MXN favorecen a la señal en MXN.
- En 1995-2007 la señal en USD tuvo más CAGR en 6 de las 8 parejas: las 4 con T1, más SMA10 y SMA12 con T0.

**Prueba principal pre-registrada: diferencia mensual de rendimientos netos, SMA10 − comprar y mantener, NW(6).**

| Variante | Tramo | n | Media %/mes | ×12 | t NW(6) | IC95 (%/mes) | Veredicto |
|---|---|---|---|---|---|---|---|
| **SMA10-MXN-T1** | **2008-2026** | 224 | 0.082 | 0.99% | 0.55 | [−0.212, 0.377] | inconcluso |
| SMA10-MXN-T1 | 1995-2007 | 156 | 0.064 | 0.77% | 0.34 | [−0.300, 0.428] | inconcluso |
| SMA10-MXN-T1 | 1995-2026 | 380 | 0.075 | 0.90% | 0.64 | [−0.154, 0.303] | inconcluso |
| SMA10-MXN-T0 | 2008-2026 | 224 | 0.070 | 0.84% | 0.46 | [−0.228, 0.368] | inconcluso |
| SMA10-MXN-T0 | 1995-2007 | 156 | 0.035 | 0.42% | 0.18 | [−0.346, 0.415] | inconcluso |
| SMA10-USD-T1 | 2008-2026 | 224 | −0.169 | −2.03% | −1.01 | [−0.497, 0.159] | inconcluso |
| SMA10-USD-T1 | 1995-2007 | 156 | 0.240 | 2.88% | 1.19 | [−0.157, 0.637] | inconcluso |
| SMA10-USD-T0 | 2008-2026 | 224 | −0.154 | −1.85% | −0.93 | [−0.479, 0.171] | inconcluso |
| SMA10-USD-T0 | 1995-2007 | 156 | 0.194 | 2.33% | 0.91 | [−0.225, 0.613] | inconcluso |

**Sharpe deflactado** (`sharpe_deflactado_de_registro`, N = 16 variantes registradas, umbral 0.95):

| Tramo | Variante | Sharpe anual | SR0 anual (máximo esperado bajo H0) | PSR sin deflactar | DSR | ¿≥ 0.95? |
|---|---|---|---|---|---|---|
| 2008-2026 | **SMA10-MXN-T1 (principal; además es la mejor)** | 0.772 | 0.159 | 0.9997 | **0.9966** | sí |
| 2008-2026 | SMA10-MXN-T0 | 0.770 | 0.159 | 0.9996 | 0.9964 | sí |
| 2008-2026 | SMA10-USD-T1 | 0.534 | 0.159 | 0.9887 | 0.9453 | no |
| 2008-2026 | SMA10-MXN-T1 con N = 100 | 0.772 | 0.223 | 0.9997 | 0.9923 | sí |
| 1995-2007 | **SMA10-MXN-T1** | 0.056 | 0.185 | 0.5796 | **0.322** | no |
| 1995-2007 | SMA10-MXN-T0 | 0.099 | 0.185 | 0.6389 | 0.378 | no |
| 1995-2007 | Mejor variante (sma12_usd_T0) | 0.329 | 0.185 | 0.8823 | 0.698 | no |

Referencia sin deflactar: comprar y mantener tiene PSR de **0.993 (T0) y 0.991 (T1) en 2008-2026**, y de 0.58 y 0.49 en 1995-2007. En 2008-2026 casi cualquier exposición al S&P en MXN pasa un DSR contra cero. El DSR no mide si la SMA le gana a comprar y mantener. Eso lo mide la prueba NW, y da inconcluso.

**Sensibilidades de SMA10, 2008-2026** (CAGR / caída máxima; `es_prueba=0`):

| Escenario | Señal MXN, T1 | Señal USD, T1 | Comprar y mantener, T1 | Señal MXN, T0 | Comprar y mantener, T0 |
|---|---|---|---|---|---|
| Base (0.29% + 0.05%) | 15.50% / −12.71% | 12.16% / −21.68% | 13.97% / −29.50% | 15.23% / −12.23% | 13.97% / −28.43% |
| Sin costos | 15.88% / −12.71% | 12.81% / −20.06% | 13.97% / −29.50% | 15.61% / −12.23% | 13.97% / −28.43% |
| Spread medio (0.29% + 0.15%) | 15.39% / −12.71% | 11.97% / −22.15% | 13.97% / −29.50% | 15.12% / −12.23% | 13.97% / −28.43% |
| Doble pierna (0.58% + 0.10%) | 15.12% / −12.72% | 11.50% / −23.27% | 13.97% / −29.50% | 14.85% / −12.23% | 13.97% / −28.43% |
| ^SP500TR en vez de SPY | 15.48% / −12.70% | 12.26% / −21.69% | 14.09% / −29.55% | 15.31% / −12.15% | 14.05% / −28.76% |
| FIX en vez de DEXMXUS | 15.37% / −12.78% | 12.13% / −21.84% | 13.98% / −29.66% | 15.33% / −12.05% | 13.97% / −28.51% |
| MXN=X (muestra desde 2005) | 15.99% / −12.28% | 12.14% / −21.99% | 13.99% / −29.46% | 15.33% / −11.42% | 13.99% / −27.11% |
| Señal sobre precio sin dividendos | 15.52% / −12.71% | 12.30% / −21.68% | — | 15.72% / −11.78% | — |
| Dividendos netos de 30% de retención | 15.12% / −12.85% | 11.70% / −21.78% | 13.35% / −30.01% | 15.09% / −12.31% | 13.35% / −28.95% |
| CETES con partición por periodo | 15.49% / −12.71% | 12.16% / −21.83% | 13.97% / −29.50% | 15.22% / −12.23% | 13.97% / −28.43% |
| Corrida aislada desde 2008-01 (entra desde cero) | 15.52% / −12.71% | 12.18% / −21.68% | 13.95% / −29.74% | 15.25% / −12.23% | 13.94% / −28.68% |
| Búsqueda de origen: historia de la señal desde 2008-01 (evaluación desde nov-2008) | 15.89% / −12.71% | 12.37% / −21.68% | **16.10%** / −26.13% | 15.60% / −12.23% | **16.23%** / −25.59% |

Si la evaluación empieza después del desplome de 2008 (nov-2008), comprar y mantener **le gana** a la SMA10-MXN: 16.1% contra 15.9% en T1. La ventaja de CAGR de la SMA viene de haber esquivado 2008.

**Comparación con las cifras recibidas.** La afirmación dice SMA 14.6% / −12% y comprar y mantener 13.5% / −31%. Las tolerancias son ±0.30 pp en CAGR y ±1.0 pp en caída máxima.

| Definición | SMA10-MXN | Comprar y mantener | ¿Dentro de tolerancia? (CAGR SMA, CAGR B&H, caída SMA, caída B&H) |
|---|---|---|---|
| T0, 2008-01 a 2026-08 (pre-registrada) | 15.23% / −12.23% | 13.97% / −28.43% | no, no, **sí**, no |
| T1, 2008-01 a 2026-08 (pre-registrada, principal) | 15.50% / −12.71% | 13.97% / −29.50% | no, no, **sí**, no |
| T0 aislada desde 2008-01 | 15.25% / −12.23% | 13.94% / −28.68% | no, no, sí, no |
| T0 con historia desde 2008 (nov-2008 a ago-2026) | 15.60% / −12.23% | 16.23% / −25.59% | no, no, sí, no |
| *POST-HOC* T0, de ene-2007 a ago-2026 | 14.74% / −12.23% | 13.54% / −31.15% | **sí, sí, sí, sí** |
| *POST-HOC* T0, de jul-2007 a ago-2026 | 14.74% / −12.23% | 13.51% / −31.15% | **sí, sí, sí, sí** |
| *POST-HOC* T0, de oct-2007 a ago-2026 | 14.76% / −12.23% | 13.51% / −31.38% | **sí, sí, sí, sí** |
| *POST-HOC* T0, de ene-2007 a jun-2026 | 14.87% / −12.23% | 13.66% / −31.15% | sí, sí, sí, sí |

En la búsqueda post-hoc, 7 de las 8 ventanas que empiezan en 2007 reproducen las cuatro cifras. Todo indica que el backtest recibido **empieza en 2007**, no en 2008. El −31% de comprar y mantener es la caída del pico de septiembre de 2007 al valle de febrero de 2009.

### 4. Calificación de cada afirmación (criterios del pre-registro §8)

| Afirmación | Cifra recibida | Nuestra cifra principal | Resultado |
|---|---|---|---|
| A1: S&P en pesos, 2008-2026 | 14.5% | 13.97% (W1); 14.47% (W2) | **Se reproduce con otra ventana** (W2, con inicio a fin de ene-2008). Rango según el inicio: 13.4-17.2%. |
| A2: IPC vía NAFTRAC | 6.3% | 6.11% (W1); 6.29% con fin en jun-2026 | **Se reproduce**, pero es un **piso**: faltan dividendos de 6 años. La estimación post-hoc con dividendos es ~6.4-6.7%. |
| A3: CETES | 6.1% | 6.37% | **Se reproduce** en el límite de la tolerancia (+0.27 pp). Ninguna definición nuestra baja de 6.25%. |
| A4: 2008, −47% USD contra −21.6% MXN | −47% / −21.6% | −47.6% (caída diaria dentro de 2008, USD); −22.1% (cambio del año calendario, MXN, precio) | **Mezcla de medidas.** Con la misma medida: −36.8% contra −19.9%, o −47.6% contra −34.9%. |
| A5: SMA10 con señal en MXN | 14.6% / −12% contra 13.5% / −31% | 15.23-15.50% / −12.2 a −12.7% contra 13.97% / −28.4 a −29.5% | **No se reproduce en 2008-2026.** Sí se reproduce (post-hoc) si la evaluación empieza en 2007. La dirección y la magnitud de la reducción de la caída se confirman. La ventaja de rendimiento no es significativa (t = 0.55) y el DSR en 1995-2007 es 0.32. |

**Calificación global: "confirmada con matices"** (pre-registro §8). Las cifras salen en alguna definición registrada o con la ventana que usó quien las dio. Los matices son:

- Dependen de la ventana: A1 y A5.
- A4 mezcla medidas.
- A2 es un piso.
- La diferencia contra comprar y mantener es inconclusa.
- El DSR es menor que 0.95 fuera de 2008-2026.

### 5. Conclusión operable (reglas fijadas en el pre-registro §9)

- **La SMA10 con señal en MXN no pasa a candidata.** Le falta "apoyo" en la diferencia contra comprar y mantener en 2008-2026, donde el IC95 NW incluye el 0.
- **Se clasifica como control de riesgo, no como fuente de rendimiento.** La reducción de la caída máxima a menos de la mitad se sostiene con T1, con costos (incluida la doble pierna), con las otras fuentes de datos y en los dos subperiodos. Su "ventaja" de CAGR depende de incluir 2008 y no es significativa.
- **Metas a superar en MXN**, con su ventana explícita (del 31-dic-2007 al 31-ago-2026, antes de impuestos):
  - S&P 500 con rendimiento total vía SPY: **13.97%** anual. Con dividendos netos de 30% de retención baja a **13.35%**.
  - CETES 28: **6.37%**.
  - IPC: **al menos 6.11%**, probablemente 6.4-6.7% con dividendos.

---

## Conclusiones permitidas

- De 2007-12-31 a 2026-08-31, el S&P 500 con rendimiento total en MXN rindió **13.97%** anual antes de impuestos. Si se empieza un mes después, **14.47%**. El resultado depende mucho de la fecha de inicio: 13.4-17.2% para inicios entre 2007 y 2009.
- En 2008-2026 el S&P en MXN le ganó a CETES con significancia (t NW = 2.39). En 1995-2007 no: CETES rindió 18.3% y el S&P en MXN 18.0%.
- El peso amortiguó las caídas del S&P en esta muestra: correlación de −0.56 y caída máxima mensual de −28% en MXN contra −48% en USD en W1. Pero el contraste correcto para 2008 es **−36.8% contra −19.9%** (año calendario) o **−47.6% contra −34.9%** (caída diaria dentro del año), no −47% contra −21.6%.
- Según Yahoo, NAFTRAC rindió ≥ 6.1% anual. Esa cifra omite los dividendos de 2008-2012 y 2021.
- Los CETES 28 de Banxico rindieron 6.37% anual en W1, antes de la retención de ISR.
- La SMA10 con señal en MXN redujo la caída máxima en MXN a menos de la mitad frente a comprar y mantener, tanto en 2008-2026 como en 1995-2007, con costos de GBM y ejecución realista (T1).
- En 2008-2026, la señal en MXN funcionó mejor que la señal en USD para un inversionista que mide en pesos: las 8 parejas lo muestran. La señal en USD quedó por debajo de comprar y mantener en pesos.

## Conclusiones que NO se sostienen

- Que la SMA10 con señal en pesos **rinda más** que comprar y mantener. La diferencia es inconclusa en todos los tramos (t de 0.18 a 0.64), y desaparece si se empieza a medir después de oct-2008.
- Que la señal en MXN sea mejor que la señal en USD en general. En 1995-2007 la de USD tuvo más CAGR en 6 de las 8 parejas, y menos caída en SMA10 y SMA12.
- Que un DSR de 0.997 en 2008-2026 valide la regla. Mide el Sharpe contra cero en un tramo en el que comprar y mantener también pasa (PSR de 0.99). En 1995-2007 el DSR es 0.32.
- Que "S&P en pesos 14.5%" sea el rendimiento de "2008 a 2026" sin más. Es 13.97% desde el cierre de 2007, y 14.5% solo empezando a fin de enero de 2008.
- Que el peso reduzca las caídas de 47% a 21.6%. Esas cifras usan medidas distintas.
- Que NAFTRAC con `adjclose` de Yahoo sea el rendimiento total del IPC.
- Que alguna de estas cifras sea neta de impuestos:
  - ISR de 10% sobre ganancias del SIC.
  - Retención de dividendos de EUA: 30%, o 10% con W-8BEN, que cuesta 75 USD + IVA.
  - Retención sobre intereses de CETES.
  - Spread cambiario implícito del SIC.
- Que SPY.MX o IVV.MX de Yahoo sirvan para medir el S&P en pesos: mezclan cotizaciones en USD y MXN hasta 2012.
- Que el pasado 2008-2026, con una depreciación del peso de 2.4% anual, se repita.

## Estado

**Replicado con diferencias** (2026-09-25):

- A1 se reproduce solo con otra ventana.
- A2 y A3 se reproducen dentro de la tolerancia.
- A4 mezcla medidas.
- A5 no se reproduce en la ventana pre-registrada de 2008-2026, pero sí (post-hoc) con inicio en 2007. La dirección se confirma.

**Pendientes:**

1. S&P/BMV IPC Total Return oficial (S&P DJI) o historial de distribuciones de NAFTRAC (BlackRock o Emisnet) para 2008-2012 y 2021, que cierra la alerta #1.
2. El spread cambiario implícito del SIC en GBM.
3. La capa de impuestos (ISR de 10% SIC, W-8BEN, retención de CETES).
4. ~~Doble ejecución independiente por `auditor-de-replicas`.~~ Hecha el 2026-09-25: las 871 cifras comparadas coinciden. Ver "Doble ejecución independiente (2026-09-25)".
5. Replicar la SMA en MXN sobre el mercado de EUA de French (1926-) convertido a MXN, para tener una muestra más larga que 1995-2026. Solo es posible desde 1993 con DEXMXUS; antes, con FIX desde 1991.

**Archivos:**

- `prerregistro.md`
- `reproducir.py`
- `descargar_datos.py` (con red; no hace falta para reproducir)
- `datos/`: 15 archivos, incluida `bitacora_descarga.json`. La descarga de EWW se hizo aparte con curl a las 05:48 UTC y no está en la bitácora.
- `SHA256SUMS.txt`
- `resultados.json`
- `V04-variantes.csv`
- `independiente.py`, `independiente-comparacion.csv` e `independiente-resultados.json` (doble ejecución independiente; sin red)

**Fuentes verificadas el 2026-09-25:**

- FRED DEXMXUS: "noon buying rates in New York City for cable transfers payable in foreign currencies" (https://fred.stlouisfed.org/series/DEXMXUS).
- Banxico SIE:
  - Cuadro CF107, SF43936: "Resultados de la subasta semanal, Tasa de rendimiento Cetes a 28 días".
  - Cuadro CF102, SF43718: "Tipo de cambio para solventar obligaciones… Fecha de determinación (FIX)".
- SPY: lanzado el 22-ene-1993, gasto de 0.0945% (https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-sp-500-etf-trust-spy).
- NAFTRAC: inicio el 30-abr-2002, gasto de 0.25%, datos al 31-jul-2026 (https://www.blackrock.com/mx/intermediarios/productos/251895/ishares-naftrac-fund).
- EWW: inicio el 12-mar-1996, gasto de 0.50% (https://www.ishares.com/us/products/239670/ishares-msci-mexico-capped-etf).
- Faber (2007): ver la ficha R01.
- Costos de GBM: `arena/investigacion/01-gbm-operativa-y-costos.md`.

## Doble ejecución independiente (2026-09-25)

**Resultado: las 871 cifras comparadas están dentro de tolerancia, y las 871 son idénticas al redondeo impreso. No se corrigió nada.** Son 789 cifras numéricas y 82 categóricas: veredictos, n, fechas de pico y valle, meses de mínimos y máximos, banderas de tolerancia, listas y la copia del pre-registro. Cubren todas las tablas de RESULTADOS y las cifras que el texto cita en el Resumen, los controles, la calificación, las conclusiones y las metas. No hubo nada que anotar en `conocimiento/registro-de-errores.md`.

### Cómo se hizo

- **Qué se leyó.** El `auditor-de-replicas` escribió `independiente.py` **sin leer `reproducir.py`**. Solo leyó la sección PRE-REGISTRO de este README y los datos congelados en `datos/`. No leyó `resultados.json` ni `V04-variantes.csv`. De `herramientas/` leyó `backtest.py`, `metricas.py` y `estadistica.py`, solo para conocer las convenciones que el pre-registro cita: costos sobre |Δw| con la entrada inicial pagada, métricas y DSR de registro. Las implementó por su cuenta. Solo importa `estadistica.newey_west`, como tercera comprobación del error estándar.
- **Huellas.** Las 17 huellas de `SHA256SUMS.txt` coinciden, incluida la de `prerregistro.md` (`84aabaa6…`). La sección PRE-REGISTRO de este README es idéntica a `prerregistro.md`, con los encabezados un nivel abajo.
- **Todo el cálculo es propio (solo biblioteca estándar):**
  - **Lectores.** Yahoo JSON, con la fecha local de la bolsa según `exchangeTimezoneName` (`MXN=X` usa la hora de Londres). FRED CSV. Banxico CSV en latin-1, que omite el único `N/E` de CETES (1998-09-03).
  - **Alineación.** E_m y G_m (último y primer día del mes) se toman solo entre fechas con precio **y** tipo de cambio del mismo día.
  - **Índice de CETES.** Interés simple entre subastas y capitalización en cada colocación.
  - **Rendimiento total neto de 30%.** Se reconstruye con cierre + 0.7 × dividendo.
  - **Simulador mensual de la SMA.** T0 y T1, costos de 0.29% + 0.05% por lado sobre |Δw| y r_neto = (1 − c)(1 + r_bruto) − 1.
  - **Métricas.** CAGR con días/365.25, volatilidad muestral × √12, Sharpe del exceso sobre CETES, caída máxima contando el valor inicial como pico, tiempo invertido, cambios y costo anual.
  - **Estadística.** PSR, SR0 y DSR (Bailey y López de Prado) con la varianza muestral de los 16 Sharpe por periodo.
- **Newey-West(6) con dos fórmulas propias distintas.** (1) Autocovarianzas con pesos de Bartlett. (2) Identidad de sumas móviles: con los residuos rellenados con ceros, Σ S_t² / 7 = n·Ω. Las dos usan la corrección n/(n − 1). En las 17 pruebas, la diferencia máxima del error estándar entre las dos es de 8.0e-18. `herramientas/estadistica.newey_west` se usó solo como tercera comprobación, con diferencia de 0.
- **El README se lee de forma automática.** Cada tabla se ubica por su título y cada cifra citada en el texto por su frase. Si el texto cambia, el script falla en lugar de comparar contra otra cosa. Salidas: `independiente-comparacion.csv` (una fila por cifra, con reportado, propio, diferencia y tolerancia) e `independiente-resultados.json`. El script no usa red, y dos corridas dan archivos idénticos.
- **Alcance.** Es una doble ejecución del cálculo **con los mismos datos**, no una segunda fuente.

**Tolerancias:**

- 0.01 pp en medias mensuales y en límites de IC (%/mes).
- 0.12 pp en media × 12.
- 0.05 en t.
- 0.1 pp en CAGR, caída máxima, cambios porcentuales, volatilidad, tiempo invertido y dividendos.
- 0.01 en Sharpe anual y SR0, 0.005 en PSR y DSR y 0.01 en correlación, costo anual y niveles.
- Igualdad exacta en n, cambios de señal, conteos, fechas, meses, veredictos y listas.
- Una cifra impresa sin decimales (p. ej. "−28%") se compara con tolerancia de 0.5.

Además se revisó si la cifra propia, redondeada a los decimales impresos, es **idéntica** a la del README.

### Comparación por bloque

| Bloque del README | Cifras comparadas | Dentro de tolerancia | Idénticas al redondeo impreso | Mayor diferencia absoluta |
|---|---|---|---|---|
| 0. Estructura de los datos citada en el pre-registro (rangos de fechas, dividendos del SIC) y copia literal del pre-registro | 12 | 12 | 12 | categóricas: todas iguales |
| 1. CAGR A1-A3 (13 series × 4 ventanas, CETES por partición y FMI) | 54 | 54 | 54 | pp: 0.0050 |
| 1b. Sensibilidad a la fecha de inicio (mín., máx., mes y 18 inicios seleccionados) | 36 | 36 | 36 | pp: 0.0047 |
| 1c. Sensibilidad a la fecha de fin | 12 | 12 | 12 | pp: 0.0047 |
| 1d. Dividendos implícitos (NAFTRAC, eventos de Yahoo, EWW, imputación, ^MXX 2022-2025) | 29 | 29 | 29 | pp: 0.0125 (cifra impresa con 1 decimal) |
| 1e. Pruebas NW de benchmarks (n, media, × 12, t NW, t IID, IC, veredicto) | 32 | 32 | 32 | %/mes: 0.0005; × 12: 0.0049; t: 0.0045 |
| 1f. Amortiguador del peso | 19 | 19 | 19 | corr.: 0.0001; pp: 0.0421 (1 decimal); nivel: 0.0031 |
| 1g. Controles de datos citados (TR reconstruido, cierres E_m, SIC, SPY.MX) | 9 | 9 | 9 | pp: 0.0004; SIC: 0.0040; nivel: 0.0005 |
| 2. A4: 2008 medida por medida (35 cifras, fechas de pico y valle, coincidencias) | 57 | 57 | 57 | pp: 0.0176 (1 decimal); en la tabla, 0.0050 |
| 3a. SMA: tabla principal 2008-2026 | 48 | 48 | 48 | pp: 0.0286 (tiempo invertido, 1 decimal); Sharpe: 0.0004; costo: 0.0001 |
| 3b. SMA: tabla 1995-2007 | 34 | 34 | 34 | pp: 0.0049; Sharpe: 0.0004 |
| 3c. Las 16 variantes y las referencias (CAGR, caída máx., Sharpe; parejas y rangos) | 157 | 157 | 157 | pp: 0.0438 (rangos del Resumen, 1 decimal); Sharpe: 0.0005 |
| 3d. Prueba principal NW(6): SMA10 − comprar y mantener | 63 | 63 | 63 | %/mes: 0.0005; × 12: 0.0048; t: 0.0049 |
| 3e. Sharpe deflactado y PSR de referencia | 41 | 41 | 41 | Sharpe: 0.0005; PSR/DSR: 0.0019 |
| 3f. Sensibilidades de la SMA10 en 2008-2026 | 118 | 118 | 118 | pp: 0.0132 ("15.9%" del texto, 1 decimal); en la tabla, 0.0050 |
| 3g. Comparación con las cifras recibidas de A5 (incluye post-hoc) | 44 | 44 | 44 | pp: 0.0048 |
| 4. Cifras del texto: Resumen, calificación, conclusiones y metas | 106 | 106 | 106 | pp: 0.4342 ("−28%", impresa sin decimales); × 12: 0.0409 ("+7.8 pp"); t: 0.0049; PSR/DSR: 0.0020 |
| **Total** | **871** | **871** | **871** | |

### Cifras clave, lado a lado

| Cifra | README | Ejecución independiente |
|---|---|---|
| A1: S&P 500 TR en MXN, W1 / W2 | 13.97% / 14.47% | 13.9653% / 14.4722% |
| A2: NAFTRAC `adjclose`, W1 | 6.11% | 6.1114% |
| A3: CETES 28, W1 | 6.37% | 6.3724% |
| A4: caída diaria dentro de 2008, SPY en USD | −47.58% (2007-12-31 a 2008-11-20) | −47.5796% (2007-12-31 a 2008-11-20) |
| A4: cambio del año 2008, ^GSPC × DEXMXUS | −22.06% | −22.0599% |
| A5: SMA10-MXN-T1, 2008-2026 (CAGR / caída máx.) | 15.50% / −12.71% | 15.5039% / −12.7079% |
| A5: SMA10-MXN-T0, 2008-2026 | 15.23% / −12.23% | 15.2327% / −12.2276% |
| Comprar y mantener T0 / T1, 2008-2026 | 13.97% / −28.43% y −29.50% | 13.9653% / −28.4342% y −29.5048% |
| NW(6) SMA10-MXN-T1 − comprar y mantener, 2008-2026 | 0.082 %/mes; t 0.55; IC [−0.212, 0.377]; inconcluso | 0.0823; t 0.547; IC [−0.2125, 0.3770]; inconcluso |
| NW(6) S&P MXN − CETES, 2008-01 a 2026-08 | 0.653 %/mes; t 2.39; IC [0.117, 1.190]; apoyo | 0.6534; t 2.386; IC [0.1166, 1.1902]; apoyo |
| DSR SMA10-MXN-T1 (N = 16), 2008-2026 / 1995-2007 | 0.9966 / 0.322 | 0.99662 / 0.32201 |
| Post-hoc T0, ene-2007 a ago-2026: SMA10-MXN / comprar y mantener | 14.74% / −12.23% contra 13.54% / −31.15% | 14.7366% / −12.2276% contra 13.5388% / −31.1501% (pico 2007-09, valle 2009-02) |

### Precisiones (no son errores)

- **"En 4 meses el cierre de mes usado no fue el último día de SPY".** Los 4 son 1993-12, 2010-12, 2021-12 y 2026-09. 2026-09 es un mes incompleto. Dentro de la muestra de evaluación (1994-01 a 2026-08) solo 2010-12 y 2021-12 afectan los resultados.
- **"7 de las 8 ventanas que empiezan en 2007".** El README no dice cuáles son las 8. Con inicios trimestrales (ene, abr, jul, oct) y fin en jun o ago de 2026, la ejecución independiente obtiene 7 de 8, igual que el README. La que no reproduce es abr-2007 a jun-2026, cuyo CAGR de la SMA es 14.9005%: se sale del límite de 14.90% por 0.0005 pp. Es un resultado al filo de la tolerancia. Con los 12 inicios mensuales de 2007 y los 2 fines, reproducen 17 de 24. Sugerencia: listar las 8 ventanas en el README.
- **"En 1995-2007 la de USD tuvo [...] menos caída en SMA10 y SMA12".** Es cierto, pero se queda corto: la señal en USD tuvo menos caída máxima en **las 8 parejas** de 1995-2007, incluidas SMA6 y SMA8, con T0 y con T1. La conclusión se refuerza.
- **MXN=X "desde 2004" en el pre-registro y "muestra desde 2005" en la tabla.** No importa para las cifras reportadas: el tramo 2008-2026 da el mismo CAGR con arranque en 2004-12, 2005-01 o 2006-01 (diferencia de 0).
- **"1.1129 × 1.0240 − 1 = 13.96%".** La aritmética es correcta con los factores impresos. Con precisión completa da 13.9653%, que es el 13.97% de W1.
- **"El percentil 90 es 0.63%".** El README no dice con qué tipo de cambio. Con DEXMXUS da 0.6296% y con FIX 0.6291%; las dos redondean a 0.63%.

### Qué no cubre

- Los controles internos de `reproducir.py`: igualdad de parsers, motor contra simulador (2.3e-15), NW contra forma cuadrática (6.1e-18) y las 104 corridas del registro. Son diagnósticos de ese script.
- Las cifras de la página de BlackRock (NAV total return de NAFTRAC). No están en `datos/`. Sí se verificó que el ^MXX de precio da −9.03%, 18.41%, −13.72% y 29.88% en 2022-2025.
- La búsqueda de origen (ii) con SPY.MX `adjclose` ("caída de −100%, CAGR de 33%"). El README no define la corrida y declara la serie inservible. Sí se verificaron el defecto (104.48 y 1,083.44) y los 95 saltos mayores a 30%.
- Hechos externos (gasto de SPY, fecha de inicio de NAFTRAC, Guía GBM). La comisión de 0.25% + IVA = 0.29% por lado coincide con `arena/investigacion/01-gbm-operativa-y-costos.md` §2.1.
- No hay segunda fuente de datos. Son los mismos archivos de Yahoo, FRED y Banxico.

**Estado después de la doble ejecución:** sin cambios. Las cifras de V04 se reproducen con código independiente. El estado ("Replicado con diferencias"), la calificación ("confirmada con matices"), la conclusión operable (la SMA10 en MXN es control de riesgo, no fuente de rendimiento) y las metas en MXN quedan igual.
