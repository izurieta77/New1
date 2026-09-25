# V04. Pre-registro: benchmarks en pesos (S&P 500, IPC vía NAFTRAC, CETES) y SMA de 10 meses con señal en USD o en MXN

> Escrito el 2026-09-25 a las 05:40 UTC, **antes** de calcular cualquier rendimiento, CAGR, caída, media, t o Sharpe con estos datos. Su huella SHA-256 queda en `SHA256SUMS.txt` antes de la primera corrida. Cualquier cambio posterior va a "Desviaciones del pre-registro" en `README.md`; este archivo no se edita.
>
> Lo único que se miró antes de escribirlo fue la **estructura** de los archivos descargados: rango de fechas, zona horaria, número de barras sin precio, moneda y lista de eventos de dividendos (fechas y montos). No se calculó ningún rendimiento. Lo que esa revisión mostró y afecta el diseño:
>
> - `NAFTRAC.MX` en Yahoo **empieza el 2008-01-02** (el ETF existe desde 2002). Sus eventos de dividendo en Yahoo **no tienen ninguno en 2008-2012 ni en 2021**. Esto confirma estructuralmente la alerta de datos #1: el `adjclose` de NAFTRAC en Yahoo omite dividendos en al menos esos años y su rendimiento es un **piso**.
> - `SPY.MX` e `IVV.MX` (cotización del SIC en MXN) empiezan en 2008-01-02 y sus dividendos en Yahoo están en **USD hasta 2015 y en MXN desde 2016**: su `adjclose` en MXN es inconsistente antes de 2016.
> - `DEXMXUS` (FRED) va de 1993-11-08 a 2026-09-18. FIX de Banxico (SF43718) va de 1991-11-12 a 2026-09-24. `MXN=X` (Yahoo) empieza en 2003-12-01. CETES 28 de Banxico (SF43936, subasta semanal, fecha de colocación) va de 1982 a la subasta del 2026-09-24. SPY en Yahoo va de 1993-01-29 a 2026-09-24, sin barras vacías.

## 1. Afirmaciones recibidas (del resumen de laboratorio del 25-sep-2026)

- **A1.** "El S&P en pesos. Entre 2008 y 2026 rindió 14.5% al año."
- **A2.** "El IPC, medido con NAFTRAC, rindió 6.3%."
- **A3.** "CETES 6.1%."
- **A4.** "En 2008 el S&P cayó 47% en dólares, pero solo 21.6% en pesos."
- **A5.** "La media móvil de 10 meses con la señal medida en pesos. Aplicada al S&P, rindió 14.6% contra 13.5% de solo mantener, y la peor caída fue de 12% en vez de 31%."

Regla del sistema: ninguna cifra ajena se adopta sin verificarla con datos y código propios.

## 2. Hipótesis previas (con signo) y mecanismo

- **H-A (benchmarks).** Espero que A1 (≈14.5%), A2 (≈6.3%) y A3 (≈6.1%) se reproduzcan dentro de la tolerancia en al menos una ventana razonable de "2008-2026", pero con **sensibilidad alta a la fecha de inicio** en A1: arrancar antes o después de la devaluación de octubre de 2008 cambia mucho el CAGR en MXN. Espero que A2 sea un **piso** por los dividendos faltantes de NAFTRAC en Yahoo.
- **H-A4.** Espero que "47% en dólares" y "21.6% en pesos" **no** sean la misma medida: 21.6% se parece al cambio entre fechas fijas del año calendario 2008 en MXN, y 47% se parece más a una caída de pico a valle en USD. Si es así, la comparación mezcla medidas y exagera el "amortiguador" del peso.
- **H-B (SMA10).** Espero que la SMA de 10 meses **reduzca la caída máxima** en MXN frente a comprar y mantener, y que la diferencia de rendimiento medio mensual (SMA − comprar y mantener) sea **estadísticamente inconclusa** (IC95 NW que incluye 0) tanto en 2008-2026 como en 1995-2007. No tengo expectativa firme sobre el signo de la diferencia de CAGR. Espero que el Sharpe deflactado sea < 0.95.
- **Mecanismo del amortiguador.** En episodios de aversión global al riesgo el peso se deprecia contra el dólar (correlación negativa entre el S&P en USD y MXN/USD), así que un activo en USD medido en MXN cae menos. **Mecanismo de la SMA:** agrupamiento de volatilidad y tendencia (ver R01). Medir la señal en MXN mezcla la tendencia del S&P con la del tipo de cambio: la señal en MXN tiende a quedarse invertida cuando el peso se deprecia.

## 3. Datos (congelados en `datos/`, huellas en `SHA256SUMS.txt`; descargados el 2026-09-25 ≈05:37 UTC con `descargar_datos.py`)

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

## 4. Construcción de series (fija)

- **Cierre de mes en MXN.** E_m = último día del mes m con precio de SPY **y** tipo de cambio en la **misma fecha**. P_MXN(E_m) = P_USD(E_m) × FX(E_m). Nunca se combina un precio de un día con un tipo de cambio de otro (alerta #3). Se reporta cuántos meses tienen E_m distinto del último día hábil de SPY.
- **Cierre de mes en USD:** último día de negociación de SPY del mes.
- **NAFTRAC:** último día del mes con `adjclose` no vacío (calendario de BMV). Inicio: 2008-01-02 (primer dato de Yahoo).
- **Índice de CETES.** I(d) se acumula con interés simple entre subastas: para la colocación a_k ≤ d < a_{k+1}, I(d) = I(a_k) × (1 + y_k/100 × (d − a_k)/360), donde y_k es la tasa de la subasta con fecha de colocación a_k. El rendimiento de cualquier periodo (d0, d1] es I(d1)/I(d0) − 1. Sensibilidad: partición mensual, con la tasa de la última subasta ≤ inicio de mes, y r = y × días/360.
- **CAGR** = (V1/V0)^(1/años) − 1 con años = días calendario / 365.25. **Media × 12 no es CAGR**; ambos se reportan donde aplica.
- **Caída máxima (MDD):** de pico a valle sobre la curva (mensual y diaria por separado). **Cambio entre fechas fijas** se reporta aparte (alerta #2).
- Sin costos en A1-A4 (son rendimientos de referencia). Sin impuestos en todo V04: no se modela el ISR de 10% sobre ganancias del SIC, la retención de dividendos de EUA (30%, o 10% con W-8BEN) ni la retención sobre intereses de CETES. Como sensibilidad se calcula el S&P con dividendos netos de 30% de retención.

## 5. Ventanas para A1-A3 (lista cerrada)

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

## 6. A4 (2008): medidas registradas

Para SPY (rendimiento total), ^SP500TR y ^GSPC (precio), en USD y en MXN (DEXMXUS; FIX como sensibilidad):

1. Cambio entre fechas fijas del año calendario: 2007-12-31 → 2008-12-31.
2. Caída máxima **dentro de 2008** (pico y valle entre 2007-12-31 y 2008-12-31), diaria y mensual.
3. Caída máxima de la crisis (pico desde 2007-01-01, valle hasta 2009-12-31), diaria y mensual.

## 7. SMA de 10 meses (A5)

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

## 8. Criterios para las afirmaciones

- **Tolerancias:** CAGR ±0.30 pp; caídas y cambios porcentuales ±1.0 pp.
- **A1-A3:** "se reproduce" si W1 cae dentro de la tolerancia; "se reproduce con otra ventana" si solo alguna ventana registrada (W2-W4 o la sensibilidad de inicio y fin) lo hace; "no se reproduce" en otro caso.
- **A4:** se reporta qué medida registrada coincide con 47% y cuál con 21.6%. Si no son la misma medida, la afirmación se califica como mezcla de medidas.
- **A5:** "se reproduce" si SMA10-MXN (T0 o T1) en 2008-2026 cae dentro de ±0.30 pp en CAGR y ±1.0 pp en MDD de 14.6%/12%, y comprar y mantener dentro de lo mismo de 13.5%/31%.
- **Calificación global de la afirmación recibida:**
  - "confirmada": A1-A5 se reproducen en su definición principal y la SMA10-MXN tiene "apoyo" en la diferencia contra comprar y mantener con DSR ≥ 0.95.
  - "confirmada con matices": las cifras se reproducen (en alguna definición registrada), pero con alguna de estas condiciones: solo con otra ventana, mezcla de medidas, dato que es piso, diferencia inconclusa, DSR < 0.95.
  - "no confirmada": las cifras centrales no se reproducen con ninguna definición registrada.

## 9. Conclusión operable (reglas fijadas de antemano)

- La SMA10 con señal en MXN solo puede pasar a candidata (papel, no dinero) si: la diferencia contra comprar y mantener tiene "apoyo" en 2008-2026 **y** no es "contraria" en 1995-2007, **y** DSR ≥ 0.95, **y** la reducción de MDD se mantiene con T1 y con costos. Si solo reduce la caída sin ventaja de rendimiento significativa, se clasifica como **control de riesgo**, no como fuente de rendimiento.
- Los benchmarks verificados se usan como **metas a superar** en MXN, con su ventana y definición explícitas.
