# AC-25-R19 · Ejecución B independiente de R19 (23-oct-2026)

**Alcance.** El código (`b.py`, biblioteca estándar) se escribió desde cero a partir del pre-registro de R19 (secciones 1-8, commit 3231990), de la ficha `conocimiento/fichas/2026-10-22-fiscalidad-sic-isr-caso-real.md` (reglas del art. 129) y de las reglas de la mezcla y de V0 en los pre-registros de R18 y R16. No se leyeron `R19.py`, `R19-salida.txt` ni `R19-resultados.json` hasta tener la tabla B (`salida.txt`). Después sí se leyeron, para explicar diferencias. El sha256 de `R19.py` coincide con el del pre-registro (`7a77728b…7d0c`).

## Datos (fuente B; sha256 en `datos/SHA256SUMS`)
| Serie | Fuente B | Fuente A |
|---|---|---|
| S&P 500 TR | CBOE `SPX` (precio) + rendimiento por dividendo mensual de multpl, devengado por día hábil (copia de AC-24: la descarga nueva de CBOE dio 307 de Cloudflare; la copia llega al 16-oct-2026) | Yahoo `^SP500TR` |
| VIX | CBOE `VIX_History` (copia de AC-24, al 16-oct) | Yahoo `^VIX` |
| Nasdaq-100 | FRED `NASDAQ100`, bajado hoy | Yahoo `^NDX` |
| Tasa | FRED `DTB3`, bajado hoy | FRED DTB3 |
| **USD/MXN** | **Banxico SIE, FIX `SF43718`**, diario, bajado hoy (exportación CSV pública del cuadro CF102, sin token) | FRED DEXMXUS |
| **INPC** | **Banxico SIE `SP1`** (INPC general de INEGI, base 2Q jul 2018), mensual de 1990 a **sep-2026**, bajado hoy (cuadro CP154). **Sin extrapolación** | OCDE MEXCPIALLMINMEI (hasta 2024-07) + 4% anual |

Control del INPC: ene, mar y ago 2026 = 143.588, 145.544 y 145.462, idénticos a la ficha (cap. 29, INEGI).

## Implementación
- **Días:** SPX ∩ VIX ∩ NDX; la tasa y el FX se arrastran con el último dato. Son 8,249 días de rendimiento, del 1994-01-03 al 2026-10-16. El FIX pasa de 3.1075 a 18.4930.
- **V0:** la SMA200 se calcula sobre todos los cierres de SPX (lección de AC-24), con histéresis. Salida si SPX < SMA×0.97 o VIX ≥ 25; entrada si SPX > SMA y VIX < 25. La exposición del día t usa el estado del cierre de t−2. La operación se ejecuta al cierre de t−1, con el FIX de ese día. V0 está encendido el 73.1% de los días.
- **Instrumentos (USD):**
  - SPYM = r_TR − 0.02%/252;
  - QQQM = r_NDX − 0.15%/252;
  - UPRO = 3·r_TR − 2·rf − 0.91%/252;
  - efectivo = rf, sin ISR;
  - en B (la variante), r_TR sin gasto.
- **Comisión:** 0.29% sobre el valor de cada compra y venta de ETF. El efectivo no paga comisión.
- **Mezcla:** SPYM 41%, QQQM 26.8%, UPRO 26.9% y efectivo 5.3%. Con V0 apagado, la manga UPRO queda en efectivo.
  - **M:** rebalanceo al cierre del primer día hábil de cada mes, con las comisiones resueltas por punto fijo.
  - **A:** rebalanceo solo el primer día hábil de enero.
  - **F:** sin rebalanceo.
  - En las tres, al salir se vende todo UPRO y la manga queda en efectivo; al entrar se recompra **con toda la manga** (lectura literal de "vender todo y recomprar"; ver diferencias).
- **ISR:**
  - **Costo promedio por emisora:** el costo en MXN al FIX de cada compra incluye la comisión de compra. Se guarda el costo nominal y el costo "real" (MXN / INPC del mes de compra − 1).
  - **Ganancia:** venta neta de comisión × FIX − max(costo nominal, costo real × INPC del mes de venta − 2). Es decir, el factor se aplica al agregado y nunca es menor a 1.
  - **Neteo y pérdidas:** neteo por año calendario; las pérdidas se arrastran 10 años sin actualizar y se aplican primero las más antiguas.
  - **Pago:** 10% el primer día hábil de mayo, con una venta pro rata de todas las posiciones (incluido el efectivo). Esa venta realiza ganancias del año en curso.
  - **Liquidación** el 16-oct-2026, con el ISR de 2026.
  - **Sin ISR:** la misma simulación, con las mismas comisiones y la misma liquidación.
- **CAGR en MXN:** 1 MXN inicial, a lo largo de 32.79 años.
- **Parte cambiaria:** 1 − Σ(ganancia USD × FIX de venta) / Σ(ganancia nominal MXN), sobre todas las ventas de la corrida con ISR. En ambas ganancias se descuentan las comisiones.

## Resultados B (`salida.txt`, `b-resultados.json`)
| Variante | CAGR MXN antes de ISR | CAGR MXN después de ISR | **Arrastre (pp/año)** | CAGR USD antes de ISR | Operaciones (con ISR) | ISR pagado / capital inicial | Parte cambiaria |
|---|---|---|---|---|---|---|---|
| **M** (vigente, mensual + filtro) | 18.76% | 17.99% | **0.76** | 12.47% | 1,344 | 21.7x | **8.2%** |
| A (anual + filtro) | 19.06% | 18.36% | 0.70 | 12.75% | 362 | 25.3x | 7.8% |
| F (solo filtro) | 18.39% | 17.82% | 0.58 | 12.12% | 245 | 23.1x | 7.1% |
| B (100% S&P TR) | 17.17% | 16.82% | 0.35 | 10.97% | 2 | 17.0x | 2.8% |

- **H1** (arrastre M ≥ 1.0 pp): **refutada** (0.76 pp).
- **H2** (M − F ≥ 0.3 pp): **refutada** (0.19 pp).
- **H3** (parte cambiaria de M ≥ 30%): **refutada** (8.2%).

**Por qué la parte cambiaria es tan baja.** La métrica de H3 solo atribuye al tipo de cambio la depreciación aplicada al costo: costo USD × (FX de venta − FX de compra). Toda la ganancia en USD se valúa al FX de la venta.
- El peso se depreció a ~5.6% anual. Las acciones subieron 11-12% anual en USD, y la mayor parte de lo realizado son ganancias en USD de lotes cuyo costo es pequeño frente al valor de venta.
- En B, el costo de 1994 (0.32 USD × 15.4 MXN de depreciación ≈ 5 MXN) es el 2.8% de ~180 MXN de ganancia.
- Además, el INPC (×10.5 de dic-1993 a ago-2026) subió más que el FX (×6.0). Por eso la actualización del costo neutraliza con creces el componente cambiario en la base gravable.
- La expectativa del pre-registro ("el peso pasó de ~3.1 a ~18.5") confundía el FX acumulado con su peso en la ganancia.

## Comparación con A (`R19-salida.txt`)
| Variante | CAGR pre A / B | CAGR post A / B | **Arrastre A / B (Δ B−A)** | Parte cambiaria A / B |
|---|---|---|---|---|
| M | 18.75% / 18.76% | 17.94% / 17.99% | **0.81 / 0.76 (−0.05)** | 6.8% / 8.2% |
| A | 19.27% / 19.06% | 18.52% / 18.36% | 0.75 / 0.70 (−0.05) | 5.7% / 7.8% |
| F | 18.80% / 18.39% | 18.15% / 17.82% | 0.65 / 0.58 (−0.07) | 5.1% / 7.1% |
| B | 17.13% / 17.17% | 16.77% / 16.82% | 0.35 / 0.35 (0.00) | 2.8% / 2.8% |
| M − F | 0.16 / 0.19 | | | |
| ISR / capital, M | 22.01x / 21.72x | | | |

### Diferencias explicadas (`sensibilidades.txt`: B con banderas que imitan cada decisión de A)
1. **Comisiones fuera de la base fiscal en A (desviación de A respecto de §4).** En `R19.py`, `Lote.compra` registra el costo **neto** de la comisión de compra, y `Lote.venta` usa la venta **bruta**, sin restar la comisión de venta. El §4 del pre-registro manda incluir ambas. Por eso A grava de más.
   - Con la bandera `comis_fuera`, el arrastre de B sube: M de 0.76 a 0.83, A de 0.70 a 0.75, F de 0.58 a 0.62.
   - Es la mayor parte de la brecha de arrastre, y explica por qué B queda debajo de A.
2. **Reentrada de UPRO.** A recompra UPRO al 26.9% **del total** (en F, con tope en el efectivo disponible). Así cada reentrada es un rebalanceo parcial de la manga. B recompra con la manga que dejó la salida (lectura literal de "sin rebalanceo").
   - Esto explica toda la diferencia de CAGR de F (bandera `reentrada_w`: 18.39% → 18.79%, contra 18.80% en A) y la de A (19.06% → 19.17%). Mueve poco el arrastre (+0.00 a +0.03).
   - En M, A no topa la compra con el efectivo disponible, así que el efectivo puede quedar negativo unos días; el efecto es despreciable.
3. **FX e INPC (segunda fuente).** Cambiar el FIX por DEXMXUS mueve el arrastre de M +0.002 pp. Cambiar el INPC por OCDE + 4% lo mueve −0.003 pp. **La extrapolación de A desde 2024-07 no importa**: B no extrapola nada (el INPC llega a sep-2026) y obtiene lo mismo.
4. **Con las cuatro decisiones de A**, B da arrastres de 0.83 / 0.76 / 0.66 / 0.35 (M / A / F / B), contra 0.81 / 0.75 / 0.65 / 0.35 de A. **Residuo ≤ 0.02 pp.** Ese residuo es de la fuente del TR (multpl contra `^SP500TR`) y del calendario: la operación de A se ejecuta antes del rendimiento del día t con el FX de t, la de B al cierre de t−1 con el FX de t−1.
5. **Parte cambiaria (+1.4 pp en M en B).** Las banderas solo la acercan a 7.8-8.2%. El residuo de ~1.4 pp no se aisló por completo; lo más probable es que venga del momento en que cada versión ejecuta las operaciones y de la fuente del TR. Es inmaterial: las dos versiones quedan a más de 20 pp del umbral de 30%.

## Veredicto
- **Concuerdan.** El arrastre de M difiere en 0.05 pp (tolerancia del §2: 0.2 pp). El veredicto de H1, H2 y H3 es el mismo en A y en B: **las tres refutadas**.
- **Rige la cifra más conservadora para el comité.** Como esto mide un costo, conservador es el arrastre mayor, el de A (0.81 pp). Con las comisiones en la base, como manda el §4, B da 0.76.
  - Rango que se debe leer: **0.75-0.85 pp por año** para la mezcla mensual.
  - **M − F = 0.16-0.20 pp**: el rebalanceo mensual cuesta en ISR menos de 0.2 pp por año.
  - **Parte cambiaria: 7-8%.**
- **Estado propuesto para R19: "Replicado"** (H1-H3 refutadas en las dos versiones).
- **Nota para la sección de resultados de R19:** A no incluyó las comisiones en la base fiscal (diferencia 1). Eso es una desviación de A respecto del §4. Sobreestima el arrastre en ~0.05 pp y no cambia ningún veredicto.

## Limitaciones
- **TR aproximado** con multpl; NDX sin dividendos (igual que A). Sin retención en EUA sobre dividendos (riesgo declarado §7).
- **Calendario:** el primer día hábil de mayo es el de EUA. No se modelan festivos mexicanos.
- **Costo promedio:** el piso de factor 1 se aplica al agregado de cada emisora, no a cada lote (es lo que fija el pre-registro).
- **Las cuatro decisiones de A** que se probaron como sensibilidad son interpretaciones, salvo la 1, que contradice el §4.

## Reproducción
- `python3 -I b.py datos b-resultados.json` (salida en `salida.txt`).
- Sensibilidades: `python3 -I b.py datos /dev/null <banderas>`, con las banderas `comis_fuera`, `reentrada_w`, `fx_dexmxus` y `cpi_ocde`. Las dos últimas leen las copias de A en `replicas/R19-datos/`. Están en `sensibilidades.txt`.
