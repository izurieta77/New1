# Ficha · Doctorado en contabilidad C3 · IFRS 9 (AASB 9) §5.5: pérdida esperada, etapas y efecto escalón (30-oct-2026)

**Pregunta:** ¿cómo pasa la reserva de un banco de 12 meses a toda la vida cuando sube el riesgo? ¿Cuánto mueve eso la utilidad si una parte de la cartera cambia de etapa?

**Por qué este tema:** es viernes y toca un doctorado (REGLAS §0d). La fila "C2-C3" estaba en *Documentado*, y su siguiente prueba era "leer IFRS 9 §5.5 (5.5.3, 5.5.11, 5.5.15, 5.5.17)". Además, la reserva es la línea que más mueve la UPA de los bancos del universo (GFNORTE, BBAJIO, INBURSA, BAC y JPM).

## Fuente y nivel de acceso
- **AASB 9 *Financial Instruments*, versión compilada** (Authorised Version F2026C00197, registrada el 16-mar-2026, para periodos anuales que empiezan desde el 1-ene-2026 y antes del 1-jul-2026, según su portada [Verificador W44, 30-oct-2026]), [standards.aasb.gov.au](https://standards.aasb.gov.au/sites/default/files/2026-03/AASB9_12-14_COMPfeb25_01-26.pdf), PDF de 116 pp., sha256 `083e82f1…`.
  - **Lectura íntegra de §5.5.1-5.5.20.**
  - El texto de AASB 9 reproduce IFRS 9 palabra por palabra (mismo camino que con CINIIF 12 el 26-oct; EUR-Lex da un desafío antibots).
  - **Grado A** en la letra.
- **Lo que dice la norma:**
  - **5.5.3:** reserva de **toda la vida** si el riesgo de crédito "has increased significantly since initial recognition".
  - **5.5.5:** si no subió, reserva de **12 meses**.
  - **5.5.7:** la etapa puede volver de 2 a 1.
  - **5.5.9:** el aumento se mide con el **riesgo de incumplimiento**, no con el monto de la pérdida esperada.
  - **5.5.11:** presunción refutable de aumento significativo con **más de 30 días de atraso**.
  - **5.5.15:** las cuentas por cobrar comerciales y los activos de contrato sin componente financiero significativo usan siempre toda la vida (enfoque simplificado). Con componente financiero significativo, y en los arrendamientos por cobrar, es una opción de política. [Verificador W44, 30-oct-2026: antes decía que todas las cuentas por cobrar comerciales usan siempre toda la vida; ver 5.5.15(a)(ii) y (b).]
  - **5.5.17:** la pérdida debe ser (a) "unbiased and probability-weighted", (b) con valor del dinero en el tiempo y (c) con información prospectiva.
  - **5.5.19:** el horizonte es el plazo contractual máximo.

## Supuestos y derivación
- ECL = Σ_t PD_marginal(t) · LGD · EAD(t) · DF(t), con PD_marginal(t) = S(t−1)·PD y S la supervivencia.
- La etapa 1 trunca la suma en t = 1; la etapa 2 suma hasta el vencimiento (5.5.19).
- La ponderación por escenarios (5.5.17 a) se hace **sobre las pérdidas**, no sobre los parámetros: E[ECL(PD)] ≠ ECL(E[PD]) porque la ECL de toda la vida es cóncava en la PD (la supervivencia se encoge).

## Ejercicio comprobado (`fichas/codigo/2026-10-30-c3-ifrs9-ecl-etapas.py`)
**Caso:** préstamo de 1,000 a 5 años con amortización lineal, tasa efectiva de 12%, LGD de 45%. Escenarios: base 60% (PD 2%), adverso 30% (5%), severo 10% (12%).

| Medida | Valor |
|---|---|
| ECL de 12 meses ponderada (etapa 1) | **15.67** (1.57% de la EAD) |
| ECL de toda la vida ponderada (etapa 2) | **38.02** (3.80%): **2.43×** la de 12 meses |
| ECL de toda la vida con la PD promedio (3.9%) | 39.01: la ponderación correcta da 2.5% menos (−2.52%; antes decía 2.6% [Verificador W44, 30-oct-2026]) |

**Efecto escalón en una cartera:** si 5%, 10% o 20% de los préstamos pasan a la etapa 2 sin que cambie su PD, la reserva sube **+7%, +14% y +29%**. Esa diferencia va contra el resultado (5.5.8).

**Segunda comprobación:** con Monte Carlo de 200,000 préstamos del escenario adverso, la ECL de toda la vida es 49.14, contra 49.38 de la fórmula (error de muestreo de ~0.5%).

## Evidencia empírica y límites
- **[I] Para pronosticar bancos:** el costo de riesgo trimestral no es solo PD × cartera. **Las migraciones de etapa** (que dependen de la presunción de 30 días y del juicio de "aumento significativo") y el **peso de los escenarios macro** mueven la reserva aunque no haya incumplimientos nuevos. Un cambio de pesos hacia el escenario adverso sube la reserva el mismo trimestre.
- El ejercicio supone una PD constante en el tiempo. Los bancos usan curvas de PD por plazo y LGD por garantía.
- **Lo que no se leyó:** ASC 326 (CECL de EUA, que siempre usa la pérdida de toda la vida y no tiene etapas) ni la nota de etapas del 3T26 de GFNORTE.

## Contraejemplo
- **Bajo US GAAP (CECL)** no hay escalón, porque toda la cartera reserva la vida completa desde el origen. Una migración no produce el salto de +14%, pero la reserva inicial es mayor. Comparar el costo de riesgo de BAC o JPM (CECL) con el de GFNORTE (IFRS 9) sin ajustar por esto es un error.

## Qué cambia
- **Para las fichas de bancos:** en la §8, pronosticar la **reserva por etapas** (la fracción en etapa 2 y la razón vida/12 m) además del costo de riesgo agregado. Anotar si la emisora reporta bajo IFRS 9 o CECL.
- **Ninguna regla de cartera.**

## Estado nuevo
**"Doctorado contabilidad C2-C3":** de *Documentado* a **Comprendido con comprobación**. Faltan ASC 326 en texto íntegro y la nota de etapas de un banco del universo.
