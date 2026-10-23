# Réplica R19: ¿cuánto le quita el ISR del SIC (10%) a la mezcla de papel en pesos, y cuánto de la ganancia gravable es solo tipo de cambio?

> Laboratorio del 23-oct-2026. Fase 0: no recomienda inversiones. **Pre-registro y script en el mismo commit, antes de correr.** sha256 de `R19.py`: `7a77728b9beefa5850cf47fd12cf7520b35b45564ad4057b3a6ad4c36f727d0c`.

| Campo | Valor |
|---|---|
| ID | R19 |
| Hallazgo | Propio. Cierra el hueco 5 de `tabla-maestra.md` ("Resultados después de impuestos: ninguna prueba incluye el ISR de 10%"). La mecánica fiscal sale de LISR art. 129 (ficha `conocimiento/fichas/2026-10-22-fiscalidad-sic-isr-caso-real.md`, grado A) y del art. 17-A CFF (cap. 29) |
| Pre-registro escrito el | 2026-10-23, antes de cualquier corrida |
| Commit del pre-registro y del código | el commit que trae este archivo junto con `R19.py` (sha256 arriba). El script corre solo después de ese commit |
| Responsable | orquestador (A); auditor-de-replicas (B) |
| Estado | Pendiente |

**Conocimiento previo declarado:**
- R18 mide el riesgo de la mezcla en USD, sin impuestos ni tipo de cambio.
- Ayer, en el caso real, la ganancia fiscal de SPYM fue 100% cambiaria.
- No he corrido ninguna simulación fiscal.
- **Expectativa propia:** un arrastre de 0.5-1.5 pp por año con rebalanceo mensual. El tipo de cambio sería una parte grande de la ganancia nominal (el peso pasó de ~3.1 a ~18.5 desde 1994).

## PRE-REGISTRO (no se edita después de la primera corrida)

### 1. Hipótesis
- **H1:** con la mezcla vigente (SPYM 41%, QQQM 26.8%, UPRO 26.9% con filtro V0, efectivo 5.3%; rebalanceo mensual) y el ISR del art. 129, el **arrastre fiscal es ≥ 1.0 pp por año**, en MXN, de 1994 a 2026.
  - Arrastre = CAGR antes de ISR − CAGR después de ISR. Las dos se miden con la liquidación final y con las mismas comisiones.
- **H2:** el rebalanceo mensual aumenta el arrastre en **≥ 0.3 pp por año** frente a solo el filtro, sin rebalanceo (variante F).
- **H3:** más del **30%** de la ganancia nominal realizada en MXN (sin INPC) de la variante mensual es efecto cambiario. Se mide como 1 − (ganancia en USD × tipo de cambio de la venta) / (ganancia nominal en MXN).

### 2. Criterio y estado
- Cada hipótesis se sostiene o se refuta con su umbral literal.
- **Estado:** "Replicado" si A y B concuerdan en el veredicto de H1-H3 y el arrastre de M difiere en ≤ 0.2 pp. Si no, "Replicado con diferencias" o "No replicado".
- **Etiqueta:** no aplica (es medición de costo fiscal, no de ventaja).
- **Consecuencia:** ninguna regla cambia en el laboratorio. Es insumo del comité sobre la frecuencia de rebalanceo y sobre la expectativa de rendimiento neto en MXN.

### 3. Datos
- **A:** las cachés de R16 y R12 (Yahoo `^GSPC`, `^SP500TR`, `^VIX` y `^NDX`; FRED DTB3), las mismas de R18. Además, en `R19-datos/`:
  - **FRED DEXMXUS:** USD/MXN diario, 1993-11 a 2026-10-16; sha256 `60c8c775…7738`;
  - **FRED MEXCPIALLMINMEI:** IPC de México de la OCDE, que se usa como **proxy del INPC**. Llega solo hasta 2024-07; sha256 `afc67b02…b34e`. Después se extrapola con 4% anual, con sensibilidad a 0% y 8%.
- **B:** la elige el auditor, distinta si es posible (por ejemplo, el FIX de Banxico o INEGI para el INPC).

### 4. Reglas fiscales modeladas (LISR art. 129 y CFF art. 17-A)
- **Costo promedio por emisora** (SPYM, QQQM y UPRO), en MXN al tipo de cambio de cada compra, con las comisiones de compra.
- **Actualización del costo:** factor = INPC(mes de venta − 2) / INPC(mes de compra − 1). Se aplica al agregado de compras y nunca es menor a 1.
- **Ganancia:** venta en MXN, menos la comisión, menos el costo actualizado.
- **Neteo entre emisoras** dentro del año calendario.
- **Pérdidas:** se arrastran hasta 10 años, sin actualizar (simplificación declarada).
- **Pago:** 10% de la base positiva, el primer día hábil de mayo del año siguiente, con una venta pro rata que a su vez realiza ganancias. Al final se liquida todo y se paga el impuesto pendiente.
- **Comisión de GBM:** 0.25% + IVA = 0.29% por operación.
- **Efectivo:** sigue como en R18 (T-bill en USD) y **no causa ISR** en este modelo. Es una simplificación: en GBM el efectivo está en MXN y sus intereses tienen otra retención.

### 5. Variantes (4, todas registradas aquí)
- **M:** la vigente, con rebalanceo al inicio de cada mes y el filtro (vender todo UPRO al salir y recomprar al entrar).
- **A:** igual, pero con rebalanceo solo el primer día hábil de enero.
- **F:** solo el filtro, sin rebalanceo.
- **B:** 100% S&P 500 TR, comprar y mantener (referencia).

### 6. Periodo
Del 1994-01-03 al último día común de los datos (DEXMXUS al 16-oct-2026).

### 7. Riesgos de sesgo declarados
- El INPC es un proxy de la OCDE.
- El efectivo no paga impuesto.
- Las pérdidas no se actualizan.
- No hay retención en EUA sobre dividendos: el TR los reinvierte completos, lo que sobreestima ligeramente el antes y el después de ISR.
- El SIC no siempre listó estos ETF (QQQM y SPYM son recientes). Es un ejercicio sintético de mecánica fiscal, no un rendimiento histórico alcanzable.

### 8. Salida
`R19-salida.txt` y `R19-resultados.json`.

## Desviaciones del pre-registro
(ninguna todavía)

## Resultados · ejecución A (2026-10-23, después del commit `3231990`)
Periodo del 1994-01-03 al 2026-10-16, 8,253 días (`R19-salida.txt`, `R19-resultados.json`).

| Variante | CAGR MXN antes de ISR | CAGR después de ISR | Arrastre (pp/año) | Parte cambiaria de la ganancia nominal realizada |
|---|---|---|---|---|
| M: vigente, rebalanceo mensual + filtro | 18.75% | 17.94% | **0.81** | **6.8%** |
| A: rebalanceo anual + filtro | 19.27% | 18.52% | 0.75 | 5.7% |
| F: solo filtro | 18.80% | 18.15% | 0.65 | 5.1% |
| B: 100% S&P TR, comprar y mantener | 17.13% | 16.77% | 0.35 | 2.8% |

- **Sensibilidad a la inflación extrapolada después de 2024-07 (M):** 0.83 pp con 0% y 0.80 pp con 8%. No cambia nada.
- **Veredicto A:**
  - **H1 refutada:** el arrastre de 0.81 pp es menor a 1.0.
  - **H2 refutada:** M − F = 0.16 pp, menos de 0.3.
  - **H3 refutada:** 6.8%, menos de 30%.
- **Lectura preliminar (pendiente de B):**
  - El ISR del SIC cuesta ~0.8 pp por año con la mezcla vigente. Más de la mitad viene del **filtro** del 3x (salidas y reentradas), no del rebalanceo mensual. El rebalanceo anual quita 0.06 pp de impuesto, y además rinde más antes de impuestos en esta muestra.
  - **En plazos largos, la parte cambiaria de la ganancia gravable es chica (~7%).** El 100% cambiario del caso real de SPYM (ficha del 22-oct) es un efecto de **plazo corto**: con dos semanas, el tipo de cambio domina, y con décadas, domina el rendimiento en dólares.
  - El costo fiscal es la mitad del de comprar y mantener todo en el S&P, que difiere el impuesto hasta el final (0.35 pp).
