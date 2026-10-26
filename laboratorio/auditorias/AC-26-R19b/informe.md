# AC-26-R19b · Ejecución B independiente de R19b (26-oct-2026)

**Alcance.** `b.py` (biblioteca estándar, sha256 `cb9ec1bb…61e2`) parte de mi propio `AC-25-R19/b.py`. Solo leí el pre-registro de R19b (§1-5, commit 4755d91) y la nota del investigador (τ_div real = t_m + 9 pp con W-8BEN). No leí `R19b.py`, `R19b-salida.txt` ni la tabla de A hasta tener la tabla B (`salida.txt`). Las cifras centrales de A sí venían en la instrucción del orquestador. El sha256 de `R19b.py` coincide con el del pre-registro (`45200286…74c6`).

## Datos (fuente B; sha256 en `datos/SHA256SUMS`)
| Serie | Fuente B | Fuente A |
|---|---|---|
| S&P 500 TR y dividendo | CBOE SPX (precio) + dividend yield mensual de multpl, devengado por día hábil (promedio de 1.88% al año) | dividendo = r(^SP500TR) − r(^GSPC) |
| **CETES** | **Banxico SIE SF43936**: tasa de la subasta semanal de CETES a 28 días, bajada hoy (26-oct, último dato 22-oct-2026, sin extrapolar). Se usa la tasa vigente al cierre de t−1, con devengo de tasa/360 × días naturales | FRED INTGSTMXM193N (FMI, mensual hasta 2026-08 y después constante), /252 por fila |
| USD/MXN | Banxico FIX SF43718 | FRED DEXMXUS |
| INPC | Banxico SP1 | OCDE + 4% |
| VIX, NDX, DTB3 | CBOE, FRED, FRED (igual que en AC-25) | Yahoo, Yahoo, FRED |

## Implementación (lo que se agrega a AC-25)
- **Dividendo:** se aplica a SPYM y a la variante B (100% S&P). El rendimiento del día es precio + dividendo × (1 − τ_div) − gasto. El neto se reinvierte sin comisión y **sin cambiar el costo fiscal** (§4).
  - QQQM no paga dividendo y UPRO tampoco se grava, como sesgo declarado.
  - El financiamiento de UPRO sigue a DTB3.
- **Efectivo:** incluye el 5.3% del núcleo y la manga UPRO cuando V0 está apagado. Está en MXN y, en USD, se multiplica cada día por (1 + i_CETES·(1 − τ_int)) × FIX(t−1)/FIX(t). τ_int grava el interés nominal en MXN al momento de devengarse.
- **Arrastre total:** CAGR en MXN sin ningún impuesto (CETES bruto y dividendo bruto) − CAGR con ISR art. 129 + τ_div + τ_int.
- **Convenciones de R19:** el §4 de R19b manda conservar las desviaciones de A en R19. Por eso la corrida principal usa las banderas `comis_fuera,reentrada_w` (comisiones fuera de la base fiscal; al reentrar, UPRO se compra al 26.9% del total).
  - También se reporta la corrida con mis convenciones de AC-25, que siguen literalmente el §4 de R19 (`salida-conv-ac25.txt`).
- **Control:** con `caja_usd` y τ = 0, B reproduce exacto AC-25: M da 18.758% → 17.994%, un arrastre de 0.764 (`control-r19.txt`).

## Tabla B (`salida.txt`, convención del pre-registro)
| Variante | τ_div | τ_int | CAGR sin imp. | CAGR con imp. | **Arrastre B** | Arrastre A | Δ B−A | Ops |
|---|---|---|---|---|---|---|---|---|
| M | 10% | 0% | 19.54% | 18.65% | 0.89 | 0.87 | +0.02 | 1,347 |
| M | 10% | 20% | 19.54% | 18.34% | 1.20 | 1.18 | +0.02 | 1,347 |
| M | 20% | 0% | 19.54% | 18.57% | 0.98 | 0.96 | +0.02 | 1,347 |
| **M central** | **20%** | **20%** | **19.54%** | **18.26%** | **1.29** | **1.26** | **+0.03** | 1,347 |
| M | 30% | 0% | 19.54% | 18.48% | 1.06 | 1.04 | +0.02 | 1,347 |
| M | 30% | 20% | 19.54% | 18.17% | 1.37 | 1.35 | +0.02 | 1,347 |
| A | 20% | 20% | 19.87% | 18.68% | 1.19 | 1.17 | +0.02 | 365 |
| F | 20% | 20% | 19.29% | 18.34% | 0.96 | 0.94 | +0.02 | 247 |
| B (100% S&P) | 20% | 20% | 17.17% | 16.38% | 0.79 | 0.78 | +0.01 | 2 |
| **M − F** | | | | | **0.33** | 0.32 | +0.01 | |
| Sensibilidad: M, τ_div 44% | 44% | 20% | 19.54% | 18.04% | **1.50** | (sin corrida A; la estimación lineal da 1.43-1.47) | | |
| Sensibilidad: F, τ_div 44% | 44% | 20% | 19.29% | 18.18% | 1.11 | | | |

**Descomposición de M** (convención del pre-registro):
- Solo ISR: 0.80 pp.
- Con τ_div 20%: +0.18 pp.
- Con τ_int 20%: +0.31 pp.
- Todo: 1.29 pp.

El impuesto a los intereses pesa más que el impuesto a los dividendos, igual que en A.

## Diferencias con A (todas ≤ 0.03 pp; tolerancia de 0.2 pp)
1. **El residuo heredado de R19 (+0.02 pp)** viene de la fuente del TR (multpl contra ^SP500TR) y de la hora de ejecución (B al cierre de t−1 con el FIX de t−1). AC-25 ya lo había medido: con las convenciones de A, B daba 0.83 contra 0.81.
2. **Fuente de CETES:** con la serie de FRED de A (bandera `cetes_fred`), M sube +0.007 pp. **FX DEXMXUS:** +0.002 pp. **FRED + DEXMXUS + INPC OCDE juntos:** 1.291 pp. El dato no explica la brecha; el residuo es el punto 1.
3. **El CAGR de A (variante) antes de impuestos** es 19.87% en B contra 19.98% en A, por el mismo efecto de calendario y TR de AC-25. El arrastre no cambia.

## Sensibilidades adicionales (`sensibilidades.txt`, `salida-conv-ac25.txt`)
- **Convenciones literales del §4 de R19** (comisiones dentro de la base y reentrada con la manga):
  - M central: **1.23 pp** (rango 0.82-1.31).
  - F: 0.96.
  - **M − F = 0.27, por debajo de 0.3.**
  - τ_div 44%: M 1.44.
- **UPRO con el dividendo 1× gravado:** M central 1.37 y M − F 0.37 (cota superior razonable del sesgo declarado).

## Veredicto
- **H1b sostenida en B:** M central = 1.29 pp ≥ 1.0. El rango de M es 0.89-1.37, contra 0.87-1.35 en A. Se sostiene en todas las sensibilidades, con un mínimo de 1.23.
- **H2b sostenida en B por poco:** M − F = 0.33 pp ≥ 0.3, contra 0.32 en A.
  - **Es frágil.** Con las comisiones dentro de la base fiscal, como manda el §4 de R19, da 0.27 y quedaría refutada.
  - Se sostiene porque el pre-registro de R19b mantuvo a propósito la desviación de A. Hay que leerla como "M − F ≈ 0.27-0.37 pp", no como un umbral superado con holgura.
- **Concordancia:** el central de M difiere en +0.03 pp (tolerancia de ±0.2) y el veredicto de H1b y H2b coincide. **Estado propuesto para R19b: "Replicado"**, con la nota de fragilidad de H2b.
- **Cifra para el comité:** el arrastre total de la mezcla mensual es **~1.25-1.30 pp por año** con τ_div de 20%.
  - Con la τ_div real de un dueño con t_m de 35% (44%), el arrastre es **~1.45-1.50 pp por año** (corrida B, no estimación).

## Limitaciones
- **τ_int sobre el interés nominal y retenido al devengarse.** La LISR grava el interés real en la declaración anual, así que esto sobreestima el arrastre cuando la inflación es alta (1995-1999).
- **TR aproximado:** el dividendo es mensual de multpl y no se modela el calendario real de pago. La reinversión no paga comisión.
- **Sin costo cambiario** al pasar entre MXN y USD.

## Reproducción
- Principal: `python3 -I b.py datos b-resultados.json comis_fuera,reentrada_w` (salida en `salida.txt`).
- Convención de AC-25: `python3 -I b.py datos b-resultados-conv-ac25.json ""`.
- Control: `python3 -I b.py datos /dev/null caja_usd`.
- Sensibilidades: banderas `cetes_fred`, `upro_div`, `fx_dexmxus` y `cpi_ocde`. Las de A leen `replicas/R19-datos/`.
- CETES: POST a `banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarSeries`, con `idCuadro=CF107&sector=22&series=SF43936&formatoCSV.x=10`, sin token.
