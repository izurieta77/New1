# Ficha · Doctorado en finanzas F11 · Riesgo sistémico: ΔCoVaR de Adrian y Brunnermeier con datos públicos (29-oct-2026)

**Pregunta:** ¿cuánto empeora el VaR del sistema financiero cuando un banco cae a su propio VaR? ¿Cómo se estima sin datos de balance, y qué tan estable es la estimación en la cola del 1%?

**Por qué este tema:** F11 (intermediación, banca y riesgo sistémico) era el área en **Localizado**, la más baja del estado de dominio con F7. El riesgo de contraparte (Binance E1-E10, GBM) y el contagio a la cartera pasan por estos canales.

## Fuente y nivel de acceso
- **Adrian y Brunnermeier, "CoVaR"**, NBER WP 17454 (*American Economic Review* 106(7), 2016). **Lectura íntegra de §1-§3.1** (definiciones, ec. 2-5 y estimación por regresión cuantílica). Grado **A** en la definición.
- **Definición 1:** CoVaR_q^{j|i} es el VaR_q del sistema j condicionado a que la institución i esté en su VaR_q, y **ΔCoVaR_q^i = CoVaR_q^{j|X_i=VaR_q} − CoVaR_q^{j|X_i=Mediana}**.
- **Con regresión cuantílica** (ec. 5): ΔCoVaR_q^i = β̂_q (VaR_q^i − VaR_50^i).
- **Datos:** Yahoo, cierres ajustados semanales, 2005-2026 (1,138 semanas). [Nota orquestador 2026-10-30 01:11 UTC, revisión del 29-oct m6: consulta del 29-oct-2026 entre las 17:51 y las 17:53 UTC (laboratorio; el commit `4acc431` es de las 17:53). Las barras semanales llegan a la semana del 26-oct-2026, y Yahoo puede reescribir la última.] Sistema: XLF para EUA e ^MXX para México.

## Supuestos y derivación
- La regresión cuantílica ŷ_q = α̂_q + β̂_q x da el cuantil condicional del sistema; al evaluarla en x = VaR_q^i se obtiene CoVaR. La resta contra x = mediana deja solo la pendiente por la distancia entre cola y mediana.
- **Diferencia con el paper** (declarada): ellos usan el **crecimiento de los activos totales a valor de mercado** (patrimonio de mercado × apalancamiento contable) y un portafolio de todas las instituciones. Aquí se usan **rendimientos de la acción** y un índice (XLF o ^MXX) como sistema. Por eso las cifras no son comparables con su figura 1 (2006Q4).

## Ejercicio comprobado (`fichas/codigo/2026-10-29-f11-delta-covar.py`)
| Institución | β (1%) | VaR 1% semanal | **ΔCoVaR 1%** | β (5%) | ΔCoVaR 5% |
|---|---|---|---|---|---|
| JPM | 0.652 | −10.35% | **−7.00 pp** | 0.706 | −4.73 |
| BAC | 0.453 | −14.83% | −6.82 | 0.491 | −3.79 |
| C | 0.309 | −15.86% | −4.96 | 0.468 | −4.01 |
| WFC | 0.610 | −14.04% | **−8.72** | 0.570 | −4.32 |
| GS | 0.674 | −11.90% | −8.27 | 0.661 | −4.63 |
| MS | 0.167 | −13.33% | **−2.26** | 0.484 | −3.74 |
| GFNORTE O (contra ^MXX) | 0.369 | −11.30% | −4.20 | 0.357 | −2.27 |
| GFINBUR O (contra ^MXX) | 0.393 | −10.04% | −3.99 | 0.355 | −2.19 |

- **Segunda comprobación:**
  - **calibración:** la fracción de semanas con el sistema bajo la recta cuantílica es 0.011 al 1% y 0.050 al 5% en todas las filas;
  - **la pendiente por rejilla exhaustiva** (paso 0.005) coincide con la búsqueda ternaria en todas, con ≤ 0.005 de diferencia.
- **BBAJIO O:** sin fechas semanales comunes con ^MXX en Yahoo (serie desde 2017 con otro calendario); queda fuera.

## Evidencia empírica y límites
- **El VaR propio no ordena el riesgo sistémico** (es el hallazgo central del paper): C tiene el peor VaR (−15.9%), pero un ΔCoVaR al 1% menor que el de JPM, WFC o GS.
- **La cola del 1% es inestable:** con 1,138 semanas solo hay ~11 observaciones en la cola. MS pasa de β 0.167 (1%) a 0.484 (5%). **Para usarlo, el 5% es más robusto**; el paper agrega variables de estado y errores por bootstrap, que aquí no se hicieron.
- XLF contiene a estas mismas instituciones (JPM ~10%), así que hay un **sesgo mecánico** de pendiente al alza para las grandes. El paper construye el sistema sin la institución evaluada.
- **Bancos mexicanos:** un ΔCoVaR al 5% de ~2.2 pp contra el IPC, menos de la mitad que en EUA. [Inferencia] El IPC pesa menos en financieras y el sistema bancario mexicano está más concentrado en filiales extranjeras, que no cotizan aquí.

## Contraejemplo
- **El ΔCoVaR es correlación en la cola, no causalidad.** Una institución pequeña que solo refleja choques comunes puede tener ΔCoVaR alto sin causar nada. El paper lo reconoce y propone el *forward ΔCoVaR* con características rezagadas (tamaño, apalancamiento, desfase de vencimientos), que aquí no se estimó.

## Qué cambia
- **Ninguna regla.** Es una herramienta para el riesgo de contraparte: el mismo procedimiento puede medir cuánto empeora la cola de BTC cuando Binance (sin acción cotizada; proxy BNB) está en su VaR. Queda como siguiente prueba.

## Estado nuevo
**F11:** de *Localizado* a **Documentado (con comprobación de ΔCoVaR)**. Falta Diamond-Dybvig, SRISK y el ΔCoVaR condicional con variables de estado.
