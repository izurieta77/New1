# Post-mortem · Micron (MU) · 4T FY26 (reportado el 30-sep-2026, después del cierre)

> Rutina de Cierre, 30-sep-2026. Los pronósticos se registraron el 25-sep, en `empresas/MU/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado. Las resoluciones están en `empresas/MU/resoluciones.csv`. Sin posición en MU: no hay decisión de cartera que evaluar, solo pronósticos.

## 1. Resultado real (fuente primaria)
Comunicado 8-K ex. 99.1 del 30-sep-2026 ([SEC](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000018/a2026q4ex991-pressrelease.htm)):
- **Ingresos:** US$54,229 M.
- **UPA:** 33.42 non-GAAP y 32.87 GAAP.
- **Margen bruto:** 87.0% non-GAAP y 86.8% GAAP.
- **Guía del 1T FY27:** ingresos de US$61.5 ± 1.5 mil M, margen bruto non-GAAP de ~86.25% y UPA non-GAAP de 38.15 ± 1.00. El consenso del 1T FY27 era de 57.4 mil M.
- **Reacción:** después del cierre, +2.1% inicial y −0.76% al corte de la inteligencia de las 15:05 CDMX. Cierre regular: US$1,065.11.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro | Consenso | Real | Error nuestro | Error consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos (punto; p10-p90) | 51,600 (49,400-57,000) | 51,200 | 54,229 | −4.85% | −5.58% | Dentro del intervalo de 80% |
| UPA non-GAAP (punto; p10-p90) | 32.10 (29.9-36.5) | 31.56 | 33.42 | −3.95% | −5.57% | Dentro del intervalo de 80% |
| P(ingresos > 51,200) | 0.56 | — | Sí | — | — | Brier 0.1936 |
| P(UPA > 31.56) | 0.58 | — | Sí | — | — | Brier 0.1764 |

## 3. Matriz y lectura
- **Buen proceso, resultado correcto pero con poca convicción.** Los dos puntos le ganaron al consenso por ~1 pp y cayeron dentro del intervalo, gracias al p90 que se amplió el 25-sep, y los dos binarios acertaron la dirección. Pero **los dos puntos salieron sesgados a la baja**, y los binarios quedaron cerca de 50% cuando la historia pedía más.
- **Qué se sabía el 25-sep:** Micron superó el punto medio de su guía en +27.6% y +23.7% de ingresos en los dos trimestres previos, y 3 de las últimas 4 sorpresas de UPA contra consenso pasaron de +20%. Esa tasa base estaba en la propia ficha.
- **Qué pasó:** hoy superó la guía por **+8.5%** (54,229 contra 50,000), más que el +3% que supusimos pero menos que los trimestres previos. **El descuento por "moderación de precios y techos de los SCA" era correcto en dirección y excesivo en tamaño.**
- **Qué no se podía saber:** la mezcla exacta del trimestre de 14 semanas y el precio realizado de HBM4.
- **Escenario:** la guía de margen del 1T FY27 (~86.25% non-GAAP) queda arriba del umbral de 86% que movía la ficha al bajista. Sigue el escenario **base**. La guía de ingresos de 61.5 mil M rebasa al consenso por +7%.

## 4. Lecciones (cada una cambia algo concreto)
1. **Binarios de "supera al consenso":** partir de la tasa base de sorpresas de la emisora y no de 50%. Para MU, con 3 de 4 sorpresas grandes, lo coherente era p ≈ 0.70-0.75, y ajustar desde ahí. Se aplica en las próximas fichas con la plantilla de `ficha-empresa`: anotar la tasa base de sorpresas antes de fijar p.
2. **Supuesto de superación de la guía:** usar la mediana de las superaciones de los últimos 4 trimestres, recortada por las causas identificadas, no un número redondo. Aquí la mediana era de ~+20%, se usó +3% y ocurrió +8.5%.
3. **Brier de estos dos binarios:** 0.185 promedio, peor que el 0.16 de un 0.60 constante. Es una muestra pequeña; no se atribuye habilidad ni torpeza con n = 2.

No hay errores de hecho que registrar en `conocimiento/registro-de-errores.md`: las cifras de la ficha eran correctas y el sesgo fue de juicio.
