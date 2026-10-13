# Post-mortem · Johnson & Johnson (JNJ) · 3T26 (reportado el 13-oct-2026, antes de la apertura)

> Rutina de Cierre, 13-oct-2026. Los pronósticos se registraron el 25-sep, en `empresas/JNJ/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado. Las resoluciones están en `empresas/JNJ/resoluciones.csv`. Sin posición en JNJ: no hay decisión de cartera ni votos del comité que evaluar, solo pronósticos. No se ejecutó `herramientas/pronosticos.py resolver` ni se tocó `bitacora/pronosticos.csv` ni `competencia/calibracion-agentes.csv` (fuera del alcance de esta tarea).

## 1. Resultado real (fuente primaria)
8-K del 13-oct-2026 (items 2.02 y 9.01). Ex. 99.1, comunicado ([SEC](https://www.sec.gov/Archives/edgar/data/200406/000020040626000189/a2026q3exhibit991.htm)), y ex. 99.2, tablas complementarias ([SEC](https://www.sec.gov/Archives/edgar/data/200406/000020040626000189/a2026q3exhibit992.htm)):
- **Reported sales:** US$25,399 M (+5.9%; +6.0% operacional; divisas −0.1 pp; +6.1% operacional ajustado). EUA 14,959 (+9.1%) e internacional 10,440 (+1.8% operacional).
- **Segmentos:** Innovative Medicine 16,757 (+7.9% operacional; Stelara resta ~690 pb). MedTech 8,642 (+2.5% operacional, contra +3.6% en el 2T).
- **Adjusted EPS (diluted):** US$2.59 (−7.5% a/a). El comunicado dice que "también refleja el impacto" de Firefly y Sail. Tasa efectiva ajustada de 17.4% (19.4% un año antes). Acciones diluidas: 2,448.6 M.
- **UPA GAAP:** US$0.09, por un cargo de litigio de 5,519 M antes de impuestos (resolución propuesta del talco de ovario), además de 339 M de deterioros de IPR&D, que también se excluyen de la ajustada.
- **Guía 2026:** ventas reportadas de 101.0-101.4 mil M (punto medio 101.2; antes 101.1) y UPA ajustada de 11.05-11.15 (punto medio 11.10, +0.06). FCF del año a la fecha de ~US$15.1 mil M.
- **Reacción (Yahoo, fuente secundaria):** abrió en 254.56 (−3.5% contra el cierre del 12-oct, 263.73) y cerró en 248.61 (**−5.7%**). La causa no está verificada.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro | Consenso | Real | Error nuestro | Error consenso | Puntuación |
|---|---|---|---|---|---|---|
| Reported sales (punto; p10-p90) | 25,550 (25,050-26,050) | 25,291 | 25,399 | +0.59% | −0.43% | Dentro del intervalo de 80% |
| Adjusted EPS diluted (punto; p10-p90) | 2.46 (2.32-2.60) | 2.45 | 2.59 | −5.02% | −5.41% | Dentro del intervalo de 80%, a 0.01 del p90 |
| P(ventas > 25,291) | 0.72 | — | Sí | — | — | Brier 0.0784 |
| P(UPA ajustada > 2.45) | 0.55 | — | Sí | — | — | Brier 0.2025 |

Brier promedio de los dos binarios: **0.1405**. Con la tasa base de FactSet (0.70 y 0.78) habría sido de 0.0692 (0.0900 y 0.0484).

## 3. Matriz y lectura
- **Ventas: buen proceso y buen resultado, pero por errores que se compensaron.** El punto quedó a 0.6% del real. Supusimos +7% operacional y −0.5% de divisas (≈ 25,553 M); ocurrió +6.0% operacional y −0.1% de divisas. El crecimiento operacional se sobreestimó en ~1 pp (MedTech se desaceleró) y el efecto cambiario se sobreestimó en contra. El binario en 0.72, ya cerca de la tasa base, fue el mejor de los cuatro de esta jornada (GS y JNJ).
- **UPA ajustada: proceso razonable, sesgo a la baja.** El punto quedó por debajo del real igual que el consenso (−5.0% contra −5.4%), y el real tocó casi el p90. La ficha restaba ~0.57 por Firefly y Sail en el 3T (inferencia propia). El comunicado no separa el monto del IPR&D adquirido dentro de I+D (que subió 980 M a/a, a 4,652 M), así que **no se puede verificar en fuente primaria cuánto de la diferencia vino del reparto 3T/4T de Sail y cuánto del negocio subyacente.** Sí se puede medir la tasa fiscal: con la tasa ajustada del 3T25 (19.4%), la UPA habría sido ~2.53 (cálculo propio), así que ~0.06 de la sorpresa vino de impuestos.
- **Binario de UPA en 0.55:** la tasa base era 0.78 y la ficha documentaba que JNJ superó el consenso de UPA en 3 de los 4 trimestres previos. Partir de ~0.75 era lo coherente; 0.55 costó 0.15 de Brier contra la tasa base.
- **Qué se sabía el 25-sep:** el cargo GAAP por el talco en el 3T26 (la ficha lo anticipó en la cadena causal A: se confirmó, 5,519 M), el IPR&D de Firefly en el 3T y la historia de sorpresas de UPA.
- **Qué no se podía saber:** el reparto exacto del costo de Sail entre trimestres, la tasa fiscal del trimestre y la desaceleración de MedTech internacional (+0.1% operacional).
- **Matriz:** ventas, buen proceso y buen resultado (con algo de suerte por compensación de errores). UPA, proceso razonable en el punto y débil en el binario; el resultado fue favorable.
- **Escenario:** Innovative Medicine creció 7.9% operacional, arriba del umbral de 5% que movía la ficha al bajista, y la guía subió. Sigue el escenario **base**. La caída de −5.7% en el día con resultados arriba del consenso indica que el precio (P/U ajustada de ~25x) ya descontaba más; la desaceleración de MedTech es la hipótesis más visible, sin verificar.

## 4. Lecciones (cada una cambia algo concreto)
1. **Binarios de "supera al consenso": partir de la tasa base (0.70 ventas, 0.78 UPA)** y ajustar con la historia de la emisora escrita en la ficha. Mismo patrón que MU y GS; refuerza la regla propuesta en `conocimiento/fichas/2026-10-13-pronostico-de-resultados-tasa-base.md` §7.
2. **Cuando el punto dependa del calendario de un cargo (IPR&D, pagos iniciales), sesgar el intervalo hacia el lado donde caería si el cargo se difiere.** Aquí el real quedó a 0.01 del p90. Checklist de la §8: indicar en qué trimestre cae cada cargo y qué pasa con la UPA si se mueve al siguiente.
3. **Separar en el supuesto de ventas el crecimiento operacional y el de divisas, y puntuar cada uno.** Un acierto del total con errores compensados no es evidencia de calibración. En la próxima ficha de JNJ: supuesto operacional por segmento (IM y MedTech) más divisas, cada uno con su real.
4. **Registrar la reacción del precio aparte del binario.** Superar el consenso no implica subir: aquí −5.7%. Se anota como dato para el tema de "qué descuenta el precio", sin pronóstico nuevo.

No hay errores de hecho que registrar en `conocimiento/registro-de-errores.md`: las cifras de la ficha eran correctas y el sesgo fue de juicio.
