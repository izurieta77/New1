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
