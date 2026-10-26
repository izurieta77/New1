# Réplica R19b: costo fiscal de la mezcla del papel con dividendos gravados y efectivo en MXN

> Trabajo continuo del 25-oct-2026 (en UTC, 26-oct). Fase 0: no recomienda inversiones. **Pre-registro y script en el mismo commit, antes de correr.** sha256 de `R19b.py`: `45200286924e27d61bf7a7cf460902568ce2114e6640ccdbf8e9797410e274c6`.

| Campo | Valor |
|---|---|
| ID | R19b |
| Origen | Auditoría W43 (`bitacora/semanal/2026-W43-abogado.md` §2) y nota del 23-oct en `R19-isr-sic-mezcla-papel.md`: el modelo de R19 omite el impuesto a los dividendos y el efectivo en MXN. La estimación del abogado es de ~1.0-1.2 pp |
| Pre-registro escrito el | 2026-10-26 01:1x UTC (25-oct en CDMX), antes de cualquier corrida |
| Commit | el commit que trae este archivo junto con `R19b.py` |
| Responsable | orquestador (A); auditor-de-replicas (B, pendiente) |
| Estado | Pendiente |

**Conocimiento previo declarado:** R19 da 0.81 pp (A) y 0.76 (B) sin dividendos gravados ni efectivo en MXN. Mi expectativa es de 1.0-1.3 pp para el caso central.

## PRE-REGISTRO
### 1. Hipótesis
- **H1b:** en el caso central (τ_div = 20%, que es 10% de EUA con W-8BEN más 10% de México; efectivo en CETES con τ_int = 20% sobre el interés nominal), el **arrastre fiscal total de la variante M es ≥ 1.0 pp por año**, 1994-2026, en MXN.
  - Arrastre total = CAGR sin ningún impuesto − CAGR con el ISR del art. 129, el impuesto a dividendos y el impuesto a intereses.
- **H2b:** en el caso central, M − F ≥ 0.3 pp.

### 2. Criterio y estado
- Sostenidas o refutadas con su umbral literal. Se reportan τ_div de 10%, 20% y 30%, y τ_int de 0% y 20%, como rango de sensibilidad.
- **Estado:** "Replicado" si B concuerda en H1b y H2b, con el central de M dentro de ±0.2 pp.
- **Etiqueta:** no aplica.

### 3. Datos
- Los de R19: cachés de R16 y R12, FRED DEXMXUS y MEXCPIALLMINMEI.
- **Nuevo:** FRED **INTGSTMXM193N** (tasa de CETES del FMI, mensual, hasta 2026-08; después se mantiene el último dato). sha256 `f8a05f13…`.
- **Dividendo diario del S&P** = r(^SP500TR) − r(^GSPC).

### 4. Reglas
- **Dividendo:** se retiene τ_div y se reinvierte el neto. El dividendo no cambia el costo fiscal de la emisora (simplificación).
- **Efectivo:** en MXN a CETES, con τ_int sobre el interés nominal. Expresado en USD dentro del modelo, cambia con el tipo de cambio.
- Todo lo demás es igual a R19, **incluidas sus desviaciones conocidas**: comisiones fuera de la base fiscal y la reentrada de F. Se mantienen para que la comparación con R19 sea limpia.
- **Sesgos declarados:**
  - QQQM se modela de precio, sin dividendos.
  - UPRO no se trata como fiscalmente distinto. Su tratamiento queda como R19c, con verificación ante GBM o el SAT.

### 5. Salida
`R19b-salida.txt` y `R19b-resultados.json`.

## Desviaciones del pre-registro
(ninguna todavía)

## Resultados · ejecución A (2026-10-26 01:12 UTC, después del commit `4755d91`)
| Variante | τ_div | τ_int | CAGR sin impuestos | CAGR con impuestos | Arrastre (pp/año) |
|---|---|---|---|---|---|
| M | 10% | 0% | 19.54% | 18.67% | 0.87 |
| M | 10% | 20% | 19.54% | 18.37% | 1.18 |
| M | 20% | 0% | 19.54% | 18.59% | 0.96 |
| **M (central)** | **20%** | **20%** | **19.54%** | **18.28%** | **1.26** |
| M | 30% | 0% | 19.54% | 18.50% | 1.04 |
| M | 30% | 20% | 19.54% | 18.19% | 1.35 |
| A | 20% | 20% | 19.98% | 18.81% | 1.17 |
| F | 20% | 20% | 19.32% | 18.38% | 0.94 |
| B (100% S&P TR) | 20% | 20% | 17.13% | 16.34% | 0.78 |
| Control R19 (M, T-bill USD, sin dividendos ni intereses gravados) | 0% | 0% | 18.75% | 17.94% | 0.81 |

- **Veredicto A:**
  - **H1b sostenida:** el arrastre central de M es **1.26 pp**, con rango de 0.87 a 1.35.
  - **H2b sostenida por poco:** M − F = 0.32 pp.
- **Lectura:**
  - El abogado del diablo tenía razón: el costo fiscal real de la mezcla con rebalanceo mensual es **~1.2-1.3 pp por año**, no ~0.8. Lo que más pesa es el impuesto a los intereses del efectivo (+0.3 pp con 20%); el impuesto a los dividendos suma +0.1-0.2 pp.
  - Con dividendos gravados, comprar y mantener el S&P también cuesta 0.78 pp por año.
  - El efectivo en CETES sube el CAGR antes de impuestos (19.54% contra 18.75%) por las tasas mexicanas altas de 1994-2008.
- **El control reproduce R19 exacto** (18.75%, 17.94% y 0.81), así que las cachés reconstruidas no cambian el resultado.

## Desviaciones del pre-registro
- **2026-10-26 01:12 UTC: cachés reconstruidas.** Esta copia del repositorio es nueva, y las cachés de R12 y R16 no están en git (`.gitignore`). R16 y R12 las volvieron a descargar el 26-oct: el sha256 combinado es `42339a50…`, contra `a4789527…` en R19.
  - El periodo es el mismo, porque el corte lo pone DEXMXUS al 16-oct, y el control reproduce R19 a dos decimales.
  - La primera ejecución falló antes de calcular nada (`FileNotFoundError`) y no produjo cifras.
- **Pendiente:** el lado B (auditor), y R19c (el tratamiento fiscal de UPRO, con verificación ante GBM o el SAT).
