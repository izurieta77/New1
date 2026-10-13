# Post-mortem · Goldman Sachs (GS) · 3T26 (reportado el 13-oct-2026, antes de la apertura)

> Rutina de Cierre, 13-oct-2026. Los pronósticos se registraron el 25-sep, en `empresas/GS/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado. Las resoluciones están en `empresas/GS/resoluciones.csv`. Sin posición en GS: no hay decisión de cartera ni votos del comité que evaluar, solo pronósticos. No se ejecutó `herramientas/pronosticos.py resolver` ni se tocó `bitacora/pronosticos.csv` ni `competencia/calibracion-agentes.csv` (fuera del alcance de esta tarea).

## 1. Resultado real (fuente primaria)
8-K del 13-oct-2026 (items 2.02, 7.01 y 9.01). Ex. 99.1, comunicado ([SEC](https://www.sec.gov/Archives/edgar/data/886982/000088698226000529/a3q26gsearningsresults.htm)), y ex. 99.2, presentación ([SEC](https://www.sec.gov/Archives/edgar/data/886982/000088698226000529/a3q26gsearningsresultspr.htm)):
- **Net revenues:** US$18,679 M (+23% a/a; −8% t/t). Es el segundo trimestre más alto de su historia.
- **UPA diluida GAAP:** US$17.01, contra 12.25 del 3T25 y 20.98 del 2T26. Las donaciones a Goldman Sachs Gives la redujeron en "aproximadamente US$1.00" (ex. 99.2). ROE anualizado de 18.7% y ROTE de 20.5%.
- **Segmentos:** GBM 13,458: banca de inversión 3,224 (asesoría récord, 1,654), FICC 3,471, Equities 6,441 y otros 322. AWM 5,051 (comisiones de incentivo 587 e inversiones 50). Platform Solutions 170.
- **Gastos e impuestos:** provisiones de 368 M; compensación de 5,122 M (27.4% de los ingresos; 29.6% en el acumulado del año); gasto no de compensación de 6,186 M ("otros gastos" 1,098, contra 559 en el 2T); tasa efectiva de 24.4% en el trimestre (20.4% en el año). Acciones diluidas promedio: 301.1 M.
- **Capital:** CET1 estandarizado de **12.4%** (12.9% en el 2T). Recompras de 3.0 mil M y dividendo de US$5.00. El *backlog* de banca de inversión bajó contra el 2T.
- **Reacción (Yahoo, fuente secundaria):** abrió en 923.00 (+3.2% contra el cierre del 12-oct, 893.95) y cerró en 891.91 (−0.2%).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro | Consenso | Real | Error nuestro | Error consenso | Puntuación |
|---|---|---|---|---|---|---|
| Net revenues (punto; p10-p90) | 17,900 (16,400-19,400) | 17,590 | 18,679 | −4.17% | −5.83% | Dentro del intervalo de 80% |
| UPA diluida GAAP (punto; p10-p90) | 15.00 (12.60-17.60) | 15.73 | 17.01 | −11.82% | −7.52% | Dentro del intervalo de 80% |
| P(net revenues > 17,590) | 0.58 | — | Sí | — | — | Brier 0.1764 |
| P(UPA > 15.73) | 0.38 | — | Sí | — | — | Brier 0.3844 |

Brier promedio de los dos binarios: **0.2804**. Con la tasa base de FactSet (0.70 para ingresos y 0.78 para UPA) habría sido de 0.0692 (0.0900 y 0.0484).

## 3. Matriz y lectura
- **Ingresos: buen resultado, con convicción insuficiente.** El punto le ganó al consenso por 1.7 pp y cayó dentro del intervalo, pero quedó sesgado a la baja, como en MU. Por línea (supuesto contra real): banca de inversión 3.0 contra 3.22, FICC 4.0 contra 3.47, Equities 6.0 contra 6.44, otros 0.15 contra 0.32, AWM 4.4 contra 5.05 y Platform 0.3 contra 0.17. **La única línea sobreestimada fue FICC**, justo la que Solomon había anticipado como "*softer*". Las demás se recortaron más de lo que pedía la guía.
- **UPA: mal pronóstico, con un resultado que lo exhibe.** El punto (15.00) quedó **por debajo del consenso** y el binario se fijó en 0.38, contra la tasa base de 0.78 y contra la historia de la propia emisora (superó el consenso en los 4 trimestres previos, por 7-45%). Puente (cálculo propio): con el ingreso real y nuestros demás supuestos, el modelo daba ~16.47; los ingresos explican ~1.47 de los 2.01 de error. El resto: la compensación fue 27.4% y no 30% (≈ +1.27 por acción), compensado en parte por una tasa fiscal de 24.4% y no 21.5% (≈ −0.67) y por preferentes menores (+0.19).
- **Qué se sabía el 25-sep:** (i) el consenso ya había bajado de 16.43 a 15.73 en 7 días tras la conferencia de Barclays, así que la guía de gasto ya estaba en buena parte en el consenso; restarla otra vez fue **doble descuento**; (ii) el gasto no de compensación sí salió como se pronosticó (6.19 contra 6.1 mil M), con donaciones de ~US$1 por acción; (iii) la tasa base de sorpresas de GS y del S&P 500 estaba disponible.
- **Qué no se podía saber:** el ajuste a la baja del índice de compensación en el 3T (GS lo acumula por año y lo corrige en el trimestre: 30.7% en el 1S y 27.4% en el 3T), el monto de las comisiones de incentivo (587 M por distribuciones de fondos) y las marcas negativas en Platform por Apple Card.
- **Matriz:** ingresos, buen proceso y buen resultado (con sesgo). UPA, **mal proceso** (se ignoró la tasa base y se descontó dos veces la guía) y resultado contrario al binario; el punto quedó dentro del intervalo solo porque éste era amplio.
- **Escenario:** Equities +72% a/a contra el umbral de 3,736 M y FICC prácticamente igual (3,471). Pero el **CET1 de 12.4% cruza el umbral de 12.5%** que la ficha marcaba como señal bajista (colchón de ~100 pb sobre el 11.4% requerido), y el *backlog* bajó contra el 2T. Sigue el escenario **base**, con la señal de capital activada.

## 4. Lecciones (cada una cambia algo concreto)
1. **Binarios de "supera al consenso": partir de la tasa base (0.70 ingresos, 0.78 UPA) y anotar por escrito qué información específica justifica alejarse.** Aquí 0.38 en UPA costó 0.34 de Brier contra la tasa base. Es la misma lección de MU (30-sep) y la regla propuesta en `conocimiento/fichas/2026-10-13-pronostico-de-resultados-tasa-base.md` §7; con dos casos más en la misma dirección, se refuerza la propuesta al comité para la plantilla de `ficha-empresa`.
2. **No descontar dos veces una guía que el consenso ya incorporó.** Checklist para la §8 de las fichas: si el consenso se revisó después de la guía (aquí 16.43 → 15.73), el punto parte del consenso revisado y no resta otra vez el efecto.
3. **Bancos de inversión: modelar el índice de compensación como meta del año, no como porcentaje fijo del trimestre.** Parámetro para GS: el índice del 3T es el que lleva el acumulado a la meta anual (aquí ~29.6%), con sensibilidad de ±2 pp sobre la UPA (≈ ±1.0 por acción) en la ficha.
4. **Ingresos por línea: recortar solo la línea que la empresa guió a la baja.** En este caso, FICC; las demás al ritmo del trimestre anterior ajustado por estacionalidad.

**Dato a revisar (no se registra como error de hecho):** la ficha usaba FICC del 3T25 de 3,472 M (presentación del 3T25); la presentación del 3T26 muestra 3,493 M para el 3T25, probablemente por reclasificación. No se modifica la ficha original; se anota en la adenda.
