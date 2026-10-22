# Post-mortem · Quálitas Controladora (Q.MX) · 3T26 (reportado el 20-oct-2026, después del cierre)

> Rutina de cierre, 22-oct-2026 (~21:45 UTC). Los pronósticos se registraron el 25-sep en `empresas/Q.MX/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado, y no se modifican. Las resoluciones están en `empresas/Q.MX/resoluciones.csv`. Sin posición en Q: no hay decisión de cartera ni votos del comité que evaluar, solo pronósticos del orquestador. No se ejecutó `herramientas/pronosticos.py resolver` ni se tocaron `bitacora/pronosticos.csv` ni `competencia/calibracion-agentes.csv` (fuera del alcance de esta tarea). Fase 0.

## 1. Resultado real (fuente primaria)
- **BMV, evento relevante del 20-10-2026 a las 17:05 (CDMX):** "Q*- Reporte Trimestral 3T26" (español): [eventemi_1596530_1.pdf](https://www.bmv.com.mx/docs-pub/eventemi/eventemi_1596530_1.pdf) (sha256 `1bcb70c7…`). La versión en inglés ("Earnings Results 3Q26", 17:01) es [eventemi_1596528_1.pdf](https://www.bmv.com.mx/docs-pub/eventemi/eventemi_1596528_1.pdf) y da las mismas cifras.
- **Cotejo con la información financiera trimestral de la BMV** (formato de aseguradoras, cifras acumuladas al 30-sep, enviada el 20-oct a las 16:44): [infinasg_1596511_2026-03_1.pdf](https://www.bmv.com.mx/docs-pub/infinasg/infinasg_1596511_2026-03_1.pdf) (sha256 `3e7a31e0…`).
  - Acumulado 9M26: primas emitidas de 57,685.2 M; primas de retención devengadas de 54,391.5 M; RIF de 3,644.0 M; utilidad del ejercicio de 4,713.7 M (controladora: 4,716.9 M).
  - Coincide con el reporte. El RIF trimestral (1,307) más el del 1S26 de la ficha (2,337) da 3,644, igual al acumulado.

| Concepto | 3T26 | Comparación |
|---|---|---|
| **Prima emitida** | **Ps 18,663 M** | +7.7% contra 17,335 del 3T25 |
| **Prima devengada** | **Ps 18,200 M** | +2.2%. Se constituyeron 279 M de reservas; la mezcla de pólizas anuales y multianuales subió de 22.5% a 26.0% |
| **RIF** | **Ps 1,307 M** | RSI de 8.3%; portafolio de 54,754 M |
| **Ingresos según el criterio (devengada + RIF)** | **Ps 19,507 M** (18,200 + 1,307, cálculo propio) | 2T26: 18,553 |
| Índice de siniestralidad | 63.4% (México: 61.5%) | ya refleja el IVA. La frecuencia bajó, hubo menos robo y lluvias menos intensas |
| Índice combinado | 92.7% (México: 89.8%) | 2T26: 95.7%; 3T25: 93.0% |
| Tasa impositiva | 30.5% | supuesto: 30% |
| **Utilidad neta (resultado neto)** | **Ps 1,770 M** | +2.1% (+36.3 M) contra 1,734 |
| **UPA según el criterio (resultado neto / 400 M acciones)** | **Ps 4.425** (cálculo propio) | 2T26: 3.47 con la misma convención. La "UPA" de $11.3 de la portada es de 12 meses |
| Unidades aseguradas | 6.2 M (récord) | +86.8 mil a/a |
| Índice de solvencia | 357% | — |

- **Definición de ingresos.** La fila del pronóstico advierte que la definición del proveedor de consenso no es homogénea. Se aplicó literal el criterio registrado: Prima Devengada + RIF del reporte trimestral. No se intentó reconstruir la definición de TradingView o Yahoo.
- **Reacción del precio (Yahoo chart v8, secundaria):** 171.11 (20-oct) → 179.86 (21-oct, +5.1%) → 190.87 (22-oct, +6.1%). La causa no está verificada.

## 2. Pronósticos contra resultado
El error es (punto − real) / real, con la misma convención que `empresas/AMXB.MX/resoluciones.csv`.

| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos (devengada + RIF) | 19,700 (18,900-20,350) | 19,220 (no homogéneo) | 19,507 | +0.99% | −1.47% | Dentro del 80% |
| Prima emitida | 17,850 (17,000-18,800) | — | 18,663 | −4.36% | — | Dentro, cerca del p90 |
| UPA (resultado neto / 400 M) | 3.35 (2.75-3.95) | 3.53 | 4.425 | −24.3% | −20.2% | **Fuera** del 80% (arriba del p90) |
| P(ingresos > 19,220) | 0.70 | — | Sí | — | — | Brier 0.0900 |
| P(UPA > 3.53) | 0.37 | — | Sí | — | — | Brier 0.3969 |

Brier promedio de los dos binarios: **0.2435**, apenas mejor que una moneda al aire (0.25).

## 3. Matriz y lectura
- **Ingresos: buen resultado, con errores que se compensaron.**
  - El supuesto de devengada (~18,550) quedó alto, porque el real fue 18,200: la empresa constituyó más reservas por la mezcla multianual.
  - El supuesto de RIF (~1,150) quedó bajo, porque el real fue 1,307, con RSI de 8.3%.
  - Los dos errores se compensaron. El punto y el binario acertaron, pero en parte por suerte.
- **Binario de ingresos (0.70): buena decisión, buen resultado.** El punto estaba 2.5% arriba del consenso y el 2T26 había quedado debajo del consenso por una definición distinta. Era razonable no ir más allá de 0.70.
- **Prima emitida: punto pesimista.** El supuesto de +3% a/a extrapolaba la emisión plana del 2T26 (−0.5%) y la guerra de precios. El real fue +7.7%, igual al ritmo de 9M (+7.7%). Quedó dentro del intervalo, pero en el borde alto.
- **UPA: mal proceso, mal resultado.** Real 4.425 contra 3.35, fuera del p90.
  - Descomposición aproximada (inferencia, porque el índice combinado de la emisora mezcla denominadores):
    - El combinado fue de 92.7% contra ~95.8% supuesto: ~3.1 pp sobre ~18.2 mil M de devengada son ~560 M antes de impuestos, ~390 M después.
    - El RIF quedó +157 M arriba del supuesto: ~110 M después de impuestos.
    - La devengada más baja restó poco.
    - Total: ~+500 M contra los +430 M observados (1,770 contra ~1,340).
  - **Causa principal: la siniestralidad.** Se sumaron ~330 pb por IVA a la base del 3T25 (62.4%), lo que daba ~65.7%. El real fue 63.4%: la frecuencia bajó, el robo bajó, llovió menos y el costo medio se contuvo.
  - En la práctica, el supuesto extrapolaba el 2T26 (combinado de 95.7%). El promedio de 1T26-2T26 (90.2% y 95.7%, ~93%) habría quedado casi exacto.
- **Binario de UPA (0.37): mala decisión, mal resultado.** Brier 0.3969. La probabilidad era coherente con el punto (debajo del consenso), pero el punto venía del mismo supuesto de siniestralidad. Fue un solo error contado dos veces.
- **Qué se sabía el 25-sep:**
  - la volatilidad trimestral del combinado (88-103% en 8 trimestres);
  - que el 1S26 ya traía el efecto del IVA (~320-340 pb) y aun así el 1T26 cerró en 90.2%;
  - la tendencia favorable de robos y frecuencia que la propia empresa reportó en el 2T26.
- **Qué no se podía saber:** la intensidad de las lluvias del trimestre y el RSI de 8.3%, que dependió de la valuación de la renta variable.
- **Escenario.** La ficha definió los disparadores:
  - Prima emitida del 3T26 de +5% o más: **alcista. Se cumplió (+7.7%).**
  - Siniestralidad mayor a 67%: bajista. No se cumplió (63.4%).
  - El alcista también pedía un combinado menor a 92%, y el real fue 92.7%, a 0.7 pp.
  - **Lectura:** el disparador de emisión apunta al alcista. El ROE de 12 meses (17.2%) sigue debajo del base (19-21%), y la devengada creció solo 2.2%. Se mantiene el **base con sesgo alcista**. No se reasignan las probabilidades de la §7 (25-sep), que quedan para la próxima revisión de la ficha.
  - El precio ya subió ~11.5% en dos sesiones (Yahoo, secundaria), así que parte de esto ya lo descuenta.

## 4. Lecciones (cada una cambia algo concreto)
1. **Siniestralidad de aseguradoras: no apilar un choque regulatorio sobre la base del año anterior si los trimestres posteriores al choque ya lo muestran.** Usar el promedio móvil de los últimos dos trimestres (ya con el choque) más la estacionalidad documentada. Checklist de la §8 en las fichas de aseguradoras: anotar la siniestralidad y el combinado de los últimos 4 trimestres junto al supuesto.
2. **Un mismo supuesto no debe mover el punto y el binario en la misma dirección sin decirlo.** Cuando el binario de UPA depende del mismo supuesto que el punto, la §8 debe nombrarlo y calcular la probabilidad con la dispersión histórica del combinado (88-103%), no solo con la distancia del punto al umbral. Con esa dispersión, P(UPA > 3.53) habría estado cerca de 0.45-0.50.
3. **Intervalo de UPA de aseguradoras más ancho.** ±18% (2.75-3.95) es estrecho para una variable que en 8 trimestres fue de −0.48 a 5.36. Propuesta de parámetro (no aplicado): un intervalo de 80% de al menos ±30% del punto, mientras el combinado trimestral tenga un rango de más de 10 pp.
4. **Prima emitida:** no extrapolar un trimestre plano cuando el acumulado del año corre a otro ritmo. Usar el ritmo de 9M o del 1S (+7.7%) como supuesto central, y la guerra de precios como riesgo del intervalo.

No hay errores de hecho para `conocimiento/registro-de-errores.md`: las cifras del 1S26 de la ficha (RIF de 2,337) cuadran con el acumulado de la BMV. Una nota menor: el reporte dice "al cierre del segundo trimestre" para las ~7.7 M acciones en tesorería, dentro del texto del 3T26. Parece una errata de la emisora; no afecta el criterio (400 M acciones).
