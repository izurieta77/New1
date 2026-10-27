# Réplica R20: brecha del UPRO real contra el 3x sintético, por tramos de tasa

> Laboratorio del 27-oct-2026. Fase 0: no recomienda inversiones. **Pre-registro y script en el mismo commit, antes de correr.** sha256 de `R20.py`: `b62c6cc86cc6f0290976d2fb902ec36adc63904197311a2782adcd8bbc7408ac`.

| Campo | Valor |
|---|---|
| ID | R20 |
| Origen | `estado-de-dominio.csv` fila "Crecimiento geométrico" (siguiente prueba: "brecha de financiamiento de UPRO por tramos de tasa"); investigador vespertino del 26-oct (Bianchi y Goldberg, arXiv:2604.27287); R11-B ("el sintético rinde ~1.6 pp por año más que UPRO") |
| Pre-registro escrito el | 2026-10-27 17:52 UTC, antes de cualquier corrida |
| Commit | el commit que trae este archivo junto con `R20.py` |
| Responsable | orquestador (A); auditor-de-replicas (B, `auditorias/AC-27-R20/`) |
| Estado | en curso |

**Por qué importa:** R16, R17 y R18 (stop, volatilidad objetivo y tamaño del UPRO) usan un 3x sintético: 3 × r(^SP500TR) − 2 × DTB3/252 − 0.91%/252. Si el UPRO real rinde sistemáticamente menos, y más con tasas altas (hoy DTB3 ≈ 3.8%), esos backtests son optimistas justo en el régimen actual.

**Conocimiento previo declarado:**
- R11-B: ~1.6 pp por año de brecha (2009-hoy).
- Ficha del 29-sep: UPRO real 2.22 pp por año debajo de la fórmula.
- Mi cálculo del 26-oct (2022-2023, con fed funds por día natural): residuo de −2.0 pp por año.
- **Expectativa:** brecha total de −1.5 a −2.5 pp y mayor en tasas altas.

## PRE-REGISTRO
### 1. Hipótesis
- **H1:** la brecha aritmética (252 × media diaria de r_UPRO − r_sintético) en 2009-06-26 → 2026-10-23 es **≤ −0.5 pp por año**.
- **H2:** la brecha en el tramo de DTB3 ≥ 3% es al menos **0.5 pp por año más negativa** que en el tramo < 0.5%.
- **H3 (Bianchi-Goldberg, "timing"):** en la regresión diaria de la brecha sobre r(^SP500TR), la pendiente es negativa con **t Newey-West(6) ≤ −2**.

### 2. Medidas
- **M1:** brecha aritmética total; **M1b:** CAGR real − CAGR sintético.
- **M2:** brecha por tramos de DTB3 (< 0.5%, 0.5-3%, ≥ 3%) y por año calendario.
- **M3:** regresión de la brecha diaria sobre DTB3/252. La pendiente mide si el financiamiento efectivo escala con la tasa más allá de 2×; la constante, el diferencial fijo.
- **M4:** la regresión de H3.

### 3. Criterio y estado
- Las hipótesis se sostienen o se refutan con su umbral literal.
- **Estado "Replicado"** si B, con código propio y de preferencia otra construcción o fuente (por ejemplo, DFF o SOFR en lugar de DTB3, u otro proveedor de precios), concuerda en el signo de H1-H3 y tiene M1 dentro de ±0.3 pp.
- **Etiqueta:** no aplica, porque mide un sesgo de nuestros backtests y no busca ventaja.

### 4. Datos y reglas
- **Yahoo chart v8:** UPRO (adjclose, con distribuciones) y ^SP500TR. **FRED:** DTB3, con el último dato disponible hacia adelante. La caché va en `R20-datos/` (en .gitignore) y su sha256 se reporta.
- **Fórmula del sintético:** idéntica a `R16.py` L73, incluido el gasto fijo de 0.91% anual. La comisión real de UPRO cambió en el tiempo (≈0.92-0.95%); se declara como sesgo y no se ajusta.
- Las fechas son la intersección de las dos series de Yahoo. No se excluye ningún día.
- **Sesgos declarados:**
  - el adjclose de Yahoo reinvierte las distribuciones al cierre ex-date;
  - DTB3 no es la tasa de los swaps, y la diferencia es justo lo que mide M3;
  - UPRO aplicó splits (Yahoo los ajusta).

### 5. Salida
`R20-resultados.json`, la sección de resultados de este archivo y la fila de la tabla maestra.

## RESULTADOS · Ejecución A (27-oct-2026, después del commit del pre-registro `635e4d0`)
- **Datos:** sha256 de la caché `94226cbe…ee65`. Del 2009-06-26 al 2026-10-23, 4,358 días.
- **M1:** brecha aritmética de **−1.592 pp por año**. **M1b:** CAGR real 32.41% contra 34.22% del sintético = **−1.81 pp**.
- **M2, por tramo de DTB3:**

  | Tramo | Días | Tasa media | Brecha |
  |---|---|---|---|
  | < 0.5% | 2,389 | 0.10% | −1.31 pp |
  | 0.5-3% | 935 | 1.61% | −1.54 pp |
  | ≥ 3% | 1,034 | 4.44% | **−2.30 pp** |

- **M2, por año:** de −0.19 (2012) a −2.89 (2025). 2018-2026 en −1.1 a −2.9; 2009-2017 en −0.2 a −2.0.
- **M3:** constante de **−1.30 pp por año**, pendiente sobre la tasa de −0.20, **t NW(6) = −1.39, no significativa**.
- **M4:** pendiente de la brecha sobre r(^SP500TR) de −0.032, **t NW(6) = −6.44**. El apalancamiento efectivo diario es ≈2.97, no 3.

**Veredicto A, con el umbral literal:**
- **H1 sostenida** (−1.59 ≤ −0.5).
- **H2 sostenida** (−2.30 − (−1.31) = −0.99 ≤ −0.5).
- **H3 sostenida** (t = −6.44 ≤ −2).

**Lectura** [inferencia]:
- La brecha es sobre todo un **diferencial fijo** (~1.3 pp por año: financiamiento de los swaps sobre la T-bill, costos de rebalanceo y diferencias de precio contra NAV) más un **apalancamiento efectivo algo menor que 3**.
- Lo que separa a los tramos coincide con el periodo de tasas altas (2018-19 y 2022-26). M3 no muestra que escale con la tasa, así que H2 se sostiene como **descripción del régimen** y no como mecanismo.
- **Consecuencia para nuestros backtests:** R16, R17 y R18 sobrestiman al UPRO en ~1.6 pp por año en promedio y en ~2.3 en el régimen actual.

**Estado:** en curso, a la espera de B (AC-27).
