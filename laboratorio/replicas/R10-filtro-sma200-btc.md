# Réplica R10: filtro de tendencia SMA200 con banda de ±3% sobre BTC (regla vigente de la cuenta Binance)

| Campo | Valor |
|---|---|
| ID | R10 |
| Artículo o hallazgo | No es un artículo: es la regla operativa del comité cripto (25-sep-2026), `config/parametros.json` → `filtro_tendencia`, y la simulación del gestor de riesgo que la justificó ("la banda baja las salidas en falso de 36-51% a 16-31%"). Antecedente académico: Faber (2007) para acciones (R01) y la literatura de tendencia en cripto (sin réplica previa en el laboratorio). |
| Fecha de publicación (primera versión pública) | Regla aprobada el 25-sep-2026 |
| Pre-registro escrito el | 2026-10-12, antes de cualquier corrida |
| Responsable | Laboratorio (A: orquestador; B: `auditor-de-replicas`, código desde cero y segunda fuente) |
| Estado | **No replicado** (hipótesis refutada en B, historia larga: mejora de MDD 19.1 pp < 25). [Corrección 13-oct-2026, conciliación, fallo `bitacora/arbitraje/2026-10-13-r10-estado.md`: decía "Replicado con diferencias (12-oct-2026, tras AC-16)"; ese estado es, según el §2, para el cambio de signo del Sharpe en un subperiodo, no para una refutación.] |

---

## PRE-REGISTRO (secciones 1 a 9; no se editan después de la primera corrida)

### 1. Hipótesis previa y mecanismo

- **Hipótesis.** Sobre BTC, la regla "salir si el cierre < SMA200 × 0.97; volver a entrar si el cierre > SMA200 × 1.03" reduce la caída máxima frente a comprar y mantener **por al menos 25 pp**, con una CAGR **no más de 15 pp menor** y un Sharpe **igual o mayor**, netos de costos.
- **Mecanismo.** Las caídas largas de BTC (2014-15, 2018, 2022) fueron tendencias persistentes; salir por debajo de la media evita la mayor parte. La banda reduce los cruces en falso (latigazos) alrededor de la media.
- **Resultado declarado.** No hay artículo. La única cifra previa es la del gestor de riesgo (salidas en falso 36-51% sin banda contra 16-31% con banda), de simulación propia, sin código en el repositorio.

### 2. Criterio de refutación

- **Métricas principales:** caída máxima (MDD), CAGR y Sharpe (rf = 0, USD) de la regla contra comprar y mantener, netos de costos; número de operaciones y fracción de salidas en falso (salida seguida de reentrada a un precio mayor dentro de 30 días).
- **Refuta la hipótesis:** MDD de la regla no al menos 25 pp mejor, **o** Sharpe de la regla menor que el de comprar y mantener en el periodo completo.
- **Subperiodos:** 2017-2020 y 2021-2026; si el signo de la mejora de Sharpe se invierte en uno, el resultado es "Replicado con diferencias".

### 3. Datos y licencia

| Serie | Fuente | Frecuencia | Uso |
|---|---|---|---|
| A: BTC/USDT | Binance `data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1d` (vela que cierra 00:00 UTC; la misma serie de la regla) | diaria | pública |
| B: BTC-USD | Segunda fuente elegida por el auditor (Yahoo `BTC-USD` chart v8 o CoinGecko), código desde cero | diaria | pública |

### 4. Universo

Un activo: BTC. Sin sesgo de supervivencia relevante (se prueba el activo que la cuenta ya tiene); el sesgo es de **selección**: BTC es el ganador ex post de los criptoactivos. Se declara.

### 5. Fecha de disponibilidad

La señal usa el cierre del día t (00:00 UTC). La operación se ejecuta al **cierre del día t+1** (aproxima "vender al día siguiente de 08:30 a 12:00 CDMX"). Sin información futura.

### 6. Periodo

A: desde que hay 200 cierres de Binance (BTCUSDT empieza el 17-ago-2017 → primera señal ~marzo-2018) hasta el último cierre disponible. B: el más largo de su fuente; se reporta también el periodo común con A.

### 7. Limpieza

Sin ajustes de precio (BTC no paga dividendos). Días faltantes: se descartan y se reporta cuántos.

### 8. Regla y variantes planeadas

- **Principal (la vigente):** banda ±3% sobre SMA200, ejecución t+1.
- **Variantes declaradas (4):** sin banda (cruce simple de SMA200); banda ±5%; SMA100 con banda ±3%; ejecución el mismo día t (para medir el costo del rezago). Total N = 5 configuraciones; no se agregan otras.

### 9. Costos y comparación simple

- Comisión Binance spot 0.10% por lado + 0.05% de deslizamiento por lado = **0.15% por lado**. Fuera del mercado, el efectivo rinde 0 (supuesto conservador; en la realidad, USDT o MXN pueden rendir algo).
- Comparación simple: **comprar y mantener BTC** en el mismo periodo.
- Moneda: USD. El efecto en MXN se discute aparte (no cambia el orden de las estrategias porque el tipo de cambio afecta igual a las dos cuando están invertidas; sí cambia el rendimiento en pesos del tramo en efectivo si se tiene en USDT).

---

## RESULTADOS (se llenan después de correr)

### Desviaciones del pre-registro

- Ninguna en la regla. El primer día con SMA, la posición inicial se fija por el lado de la media (arriba = invertido) y se paga una comisión de entrada; comprar y mantener también paga una. Los subperiodos arrancan con la posición vigente de la señal, sin costo de entrada adicional para la regla.

### 10. Variantes probadas

### 11. Resultados

**Ejecución A** (`R10.py`, Binance BTCUSDT 1d, 3,343 cierres del 17-ago-2017 al 11-oct-2026, sin huecos, sha256 `5aca7a215d622cad…`; salida completa en `R10-salida.txt` y `R10-resultados.json`). Costo 0.15% por lado; efectivo a 0%; USD.

| Periodo | Estrategia | CAGR | Vol | Sharpe | MDD | Salidas | En falso |
|---|---|---:|---:|---:|---:|---:|---:|
| 2018-03-05 → 2026-10-11 | **Regla vigente (SMA200 ±3%, t+1)** | +29.9% | 43.0% | **0.82** | **−51.6%** | 13 | 4 (31%) |
| | Comprar y mantener | +26.0% | — | 0.69 | −76.6% | — | — |
| | Sin banda | +27.9% | 43.1% | 0.79 | −55.0% | 32 | 21 (66%) |
| | Banda ±5% | +32.8% | 43.2% | 0.87 | −52.3% | 11 | 2 (18%) |
| | SMA100 ±3% (desde 2017-11-25; B&H −83.2%, Sharpe 0.72) | +49.4% | 46.5% | 1.09 | −64.0% | 21 | 7 (33%) |
| | Mismo día t | +30.6% | 42.8% | 0.84 | −52.5% | 13 | 4 (31%) |
| 2018-2020 | Regla vigente / B&H | +49.4% / +38.7% | — | 1.11 / 0.83 | −51.6% / −72.0% | 4 | 1 |
| 2021-hoy | Regla vigente / B&H | +21.0% / +19.9% | — | 0.67 / 0.60 | −47.1% / −76.6% | 9 | 3 |

- **Mejora de la MDD (regla vigente, periodo completo): 25.08 pp**, apenas encima del umbral de 25 pp del pre-registro. 2018-2020: 20.4 pp; 2021-hoy: 29.5 pp.
- **Mejora de Sharpe:** +0.14 en el periodo completo; positiva en los dos subperiodos (+0.28 y +0.06).
- **Salidas en falso:** la banda las baja de 66% a 31%. Es consistente con la cifra del gestor de riesgo (36-51% → 16-31%), en el extremo alto de su rango.

**Ejecución B** (`auditorias/AC-16-R10/`, código desde cero, Yahoo `BTC-USD` diario, 4,408 cierres del 17-sep-2014 al 11-oct-2026, sha256 `f47a8ef8…`). Periodo común con A (2018-03-04 a 2026-10-11): regla vigente CAGR +29.5%, Sharpe 0.82, MDD −50.8% contra comprar y mantener +25.9%, 0.69, −76.6%. **Mejora de MDD: 25.9 pp.** Salidas en falso: 31% con banda y 66% sin ella. Historia larga de Yahoo (desde la primera señal, 4-abr-2015): regla Sharpe 1.22 y MDD −64.3% contra 1.10 y −83.4%. **Mejora de MDD: 19.1 pp**, que no alcanza el umbral. La caída de 2017-18 la explica: la regla estaba invertida en el pico de diciembre de 2017, salió el 6-feb-2018, volvió a entrar el 10-feb y salió de nuevo el 15-mar.

### 12. Sensibilidad

- **Banda:** ±5% mejora a ±3% en Sharpe en A y en B (0.87 contra 0.82, periodo común), con menos salidas en falso (18%).
- **Media:** SMA100 ±3% domina en las dos ejecuciones desde 2017 (Sharpe 1.09-1.12). Es una de N = 5 configuraciones y no estaba en la hipótesis: **no justifica cambiar la regla**, porque es el resultado esperado de buscar entre variantes.
- **Rezago:** ejecutar el mismo día t no cambia el orden de los resultados (Sharpe 0.84-0.86 contra 0.82).
- **Inicio:** B movió el inicio del periodo común entre el 1-mar y el 1-abr de 2018 y la mejora de MDD siguió en 25.9 pp.

### 13. Diferencia frente al artículo

No hay artículo. Frente a la cifra del gestor de riesgo (salidas en falso de 36-51% sin banda y de 16-31% con banda): A y B dan **65-66% sin banda y 31-33% con ±3%**. La banda sí reduce las salidas en falso a la mitad, pero los niveles son más altos que los declarados. Diferencia A contra B en el periodo común: MDD −51.6% contra −50.8%, Sharpe 0.82 en ambas. Concordantes. La diferencia viene de la fuente (Binance BTCUSDT contra el agregado de Yahoo en USD) y del primer día (A arranca invertido según el lado de la media; B espera una señal de entrada).

### 14. Conclusiones permitidas

- Sobre BTC, la regla vigente **reduce la caída máxima entre 19 y 26 pp** y **mejora el Sharpe (+0.12 a +0.14)** sin sacrificar CAGR, en las dos fuentes y en los dos subperiodos del pre-registro.
- La banda de ±3% reduce las salidas en falso a la mitad.

### 15. Conclusiones que NO se sostienen

- Que la regla siempre recorte al menos 25 pp de caída: en la historia larga son 19 pp, y en el periodo común el margen es de solo 0.1-0.9 pp sobre el umbral.
- Que las salidas en falso con banda sean de 16-31% (cifra del gestor): A y B dan 31-33%.
- Que SMA100 sea mejor regla: es selección entre variantes.
- Que esto sea una ventaja de rendimiento: es **protección** con Sharpe algo mayor, en un solo activo elegido ex post (sesgo de selección de BTC).

### 16. Estado y reproducción

**Estado: No replicado** (rige la más conservadora de A y B: B refuta el umbral de MDD en la historia larga, que el §6 define como su periodo completo; en A el umbral se cumple por 0.08 pp). [Corrección 13-oct-2026, conciliación, fallo `bitacora/arbitraje/2026-10-13-r10-estado.md`: decía "Replicado con diferencias". `laboratorio/README.md`: "No replicado = se cumple el criterio de refutación pre-registrado". Las conclusiones permitidas del §14 no cambian: la regla reduce la caída 19-26 pp y mejora el Sharpe en las dos fuentes; lo refutado es el umbral de 25 pp.] **Etiqueta: oportunidad investigable**, con el uso de protección; la regla de la cuenta **no cambia**. Para el comité queda la propuesta de estudiar la banda de ±5% y SMA100 con un pre-registro nuevo y datos fuera de muestra. Reproducción: `python3 -I laboratorio/replicas/R10.py` (A) y `python3 -I laboratorio/auditorias/AC-16-R10/b.py` (B).
