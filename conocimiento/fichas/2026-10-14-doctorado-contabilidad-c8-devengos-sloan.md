# Ficha · Doctorado en contabilidad C8: devengos y persistencia de la utilidad (Sloan, 1996)

> Laboratorio del 14-oct-2026 (miércoles: turno de doctorado, REGLAS §0d). Fase 0: no recomienda inversiones.

## Pregunta
¿Por qué la parte de la utilidad que viene de devengos (y no de flujo de efectivo) predice rendimientos menores, y sigue funcionando después de publicarse?

## Fuente y nivel de acceso
- **Sloan, R. G. (1996).** "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows about Future Earnings?" *The Accounting Review* 71(3): 289-315. PDF de 30 páginas (copia de taller, cuhk.edu.hk).
  - **Lectura de secciones:** definición de devengos, tabla 3 (persistencias) y tabla 6 (portafolios). El texto extraído tiene errores de OCR; las cifras de abajo se cotejaron en dos pasajes.
  - **Grado A** en las cifras citadas.
- **Wu, Zhang y Zhang (2010),** "The q-Theory Approach to Understanding the Accrual Anomaly", *JAR* 48: 177-223 (NBER w13525).
  - Solo resumen (página de NBER). **Grado C** para este uso.
- **Datos propios:** réplica R13 (French, `Portfolios_Formed_on_AC`, CRSP 202608).

## Hechos del artículo (A)
- **Muestra:** NYSE y AMEX, 1962-1991, 40,679 años-empresa.
- **Definición:** devengos = (ΔAC − ΔCaja) − (ΔPC − ΔDeuda CP − ΔISR por pagar) − Depreciación, todo entre activos totales promedio.
- **Persistencia (tabla 3, panel A, regresión pooled):**
  - Coeficiente de los devengos: **0.765**; del flujo de efectivo: **0.855**; F = 614.01 contra igualdad.
  - Con rangos (panel B): **0.565** contra **0.838**.
  - Persistencia promedio de la utilidad: ~0.8.
- **Rendimientos (tabla 6):** portafolio de cobertura (decil de devengos bajos menos alto), ajustado por tamaño:
  - **+10.4% (t = 4.71)** en el primer año;
  - 4.8% (t = 3.15) en el segundo;
  - 2.9% (t = 1.64) en el tercero.
  - Más de 40% del rendimiento llega en los días de anuncio de utilidades.

## Supuestos y derivación
1. La utilidad es igual a flujo de efectivo más devengos. Los devengos dependen de estimaciones (cobranza, inventario, provisiones) y se revierten.
2. Si el mercado "fija" la utilidad con una persistencia común (~0.8), sobreestima la utilidad futura de las empresas con devengos altos y subestima la de las de devengos bajos.
3. La corrección llega cuando se publica la utilidad siguiente. Por eso el rendimiento anormal se concentra en los anuncios: eso es lo que distingue el error de expectativas de una prima por riesgo.

## Ejercicio numérico (comprobado)
Código: `conocimiento/fichas/codigo/2026-10-14-c8-devengos-sloan.py` (aserciones; corre con `python3 -I`).
- **Método de balance:** ΔAC 180, Δcaja 20, ΔPC 60, Δdeuda CP 10, ΔISR 5, depreciación 40 y activos promedio 1,000. Devengos = **7.5%**.
- **Dos empresas con el mismo ROA de 10%:**

  | Empresa | Devengos | Flujo | ROA siguiente (persistencias de Sloan) | ROA siguiente (fijación, 0.8) |
  |---|---:|---:|---:|---:|
  | Devengos altos | 7.5% | 2.5% | **7.875%** | 8.000% |
  | Devengos bajos | −2.5% | 12.5% | **8.775%** | 8.000% |

  - Diferencia: 0.9 pp de ROA con la misma utilidad de hoy, que es (0.855 − 0.765) × 10 pp.
  - La fijación sobreestima a una y subestima a la otra.
- **Réplica R13 (A, French):** el largo-corto ponderado por valor rinde +0.414% al mes (t NW 3.29) en 1963-1996 y +0.163% (t NW 0.93) después; la media cae 60.6%.

## Evidencia empírica y límites
- **Lo que sostiene la evidencia:**
  - El efecto es grande y significativo en la muestra original. Con los datos de French también, aunque su definición difiere (ΔCTO/valor en libros).
  - Después de publicarse se debilita, sobre todo en grandes empresas. En R13, el ponderado por valor pierde 60.6%; el ponderado por igual pierde 36-43% y sigue en el límite de significancia (t NW 1.95-2.09).
- **Explicación rival (C):** Wu, Zhang y Zhang leen los devengos como inversión en capital de trabajo, de modo que los factores de inversión absorberían parte de la anomalía.
  - En R13, el alfa FF5 (que incluye CMA) de 1963-1996 sigue en +0.445% al mes (t NW 3.85): la explicación por inversión no la absorbe en este archivo.
- **Límites:**
  - No es operable en GBM: no hay venta en corto de acciones del SIC para persona física.
  - La pierna larga sola no se probó.
  - Las cifras de French son brutas de costos.

## Contraejemplo
Una adquisición pagada con caja sube ΔAC en 100 y ΔPC en 30 en el balance consolidado. El método de balance da **7.0%** de devengos aunque los operativos del año sean cero. El error de Hribar y Collins (2002, citado de memoria, no verificado) es esta razón para preferir el estado de flujos de efectivo cuando existe (posterior a 1988).
- **Aplicación al sistema:** en las fichas de empresas, los devengos se calculan como utilidad neta menos flujo de operación, ambos del estado de flujos. No se usa el balance.

## Segunda comprobación
- Media de A recalculada con un parser propio sobre el CSV crudo: 0.41391 y 0.16320 % al mes; coincide con `R13.py`.
- Ejecución B independiente (AC-18, OSAP oct-2025, código desde cero): VW deciles pre 0.488%/mes (t NW 3.10), post 0.107% (0.59), caída 78.0%. **Concordante: R13 Replicado.** El EW sobrevive con t ≈ 2 en French, pero no en OSAP.

## Uso en el sistema
- En la ficha de empresa (expediente de 10 puntos, calidad de utilidades), una razón devengos/activos alta debe bajar la probabilidad de "supera al consenso el próximo trimestre" respecto a la tasa base. Es una regla para pronósticos, no para la cartera.
- **Pendiente:** medir si mejora el Brier de los binarios del 4T26.

## Estado nuevo
C8 pasa de **Pendiente** a **Comprendido con comprobación**. La anomalía de devengos en sí queda **Replicada** (R13, A y B), pero el área C8 completa no: faltan relevancia de valor (Ball-Brown) y gestión de utilidades.
