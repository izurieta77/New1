# Post-mortem · Visa (V) · 4T fiscal 2026 (jul-sep; reportado el 27-oct-2026, después del cierre)

> Rutina de cierre, 27-oct-2026. Los pronósticos se registraron el 25-sep en `empresas/V/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado, y no se modifican. Las resoluciones están en `empresas/V/resoluciones.csv`. Sin posición: no hay decisión de cartera ni votos del comité que evaluar, solo pronósticos. No se tocaron `bitacora/pronosticos.csv` ni `competencia/calibracion-agentes.csv`.

## 1. Resultado real (fuente primaria)
**Fuente:** Visa, 8-K del 27-oct-2026, comunicado de resultados ([q42026earningsrelease.htm](https://www.sec.gov/Archives/edgar/data/0001403161/000140316126000126/q42026earningsrelease.htm)), leído por WebFetch el 27-oct a ~21:45 UTC. El trimestre cierra el 30-sep-2026.
- **Ingresos netos: US$12,139 M (+13%** nominal y en dólares constantes; 10,724 en el 4T25).
  - Servicios 5,255 (+14%); procesamiento de datos 6,245 (+16%); transacciones internacionales 4,115 (+8%); otros 1,647 (+40%).
  - Incentivos a clientes: −5,123 (+21%).
- **Volúmenes (dólares constantes):** pagos +9%; transfronterizo +14% (+14% sin intra-Europa); transacciones procesadas +10% (74.2 mil M).
- **Gastos de operación:** GAAP 4,877 (+7%), con una provisión de litigio de 474 (MDL de interchange; 469 como partida especial no-GAAP); no-GAAP 4,051 (+12%).
- **UPA:** GAAP 3.19 (+22%); **no-GAAP 3.48 (+17%**; 2.98 en el 4T25).
  - Utilidad neta no-GAAP ≈ 3.48 × 1,882 M acciones = ~6,549 M; **margen de ~53.95%** (cálculo propio).
  - Tasa efectiva GAAP 18.5%; no-GAAP 18.4%.
- **Recompras:** ~11 M acciones por US$4.0 mil M (promedio 369.12).
- **Guía:** el comunicado no trae guía cuantitativa para FY27 (va en la llamada, que no se leyó).
- **Precio:** cierre regular de 401.86 (−1.49% contra 407.92); after-hours 394.91 a las 21:37 UTC (−1.7%). P0189 (cierre del 28-oct contra el del 27-oct) resuelve mañana.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos netos (US$ M) | 12,120 (11,920-12,320) | 12,082 | 12,139 | −0.16% | −0.47% | Dentro del 80% |
| UPA no-GAAP (US$) | 3.44 (3.36-3.52) | 3.43 | 3.48 | −1.15% | −1.44% | Dentro del 80% |
| P(ingresos > 12,082) | 0.58 | — | Sí | — | — | Brier 0.1764 |
| P(UPA > 3.43) | 0.55 | — | Sí | — | — | Brier 0.2025 |

Brier promedio de los binarios: **0.1895**. Los dos puntos fueron mejores que el consenso, y los dos intervalos contuvieron el real con holgura.

## 3. Matriz y lectura
- **Ingresos: buen proceso, buen resultado.** El supuesto de "guía de +12-13% que Visa supera por 1-2 pp" dio +13.0% contra +13.2% real. El transfronterizo (+14%) siguió fuerte.
- **UPA: buen proceso, error pequeño y explicable.** El margen neto no-GAAP real fue de ~53.95% contra 53.6% supuesto: +0.35 pp ≈ +0.022 por acción. Las acciones (1,882 M contra 1,886) suman +0.007. Con los ingresos reales y nuestro margen, el modelo habría dado 3.45. **El error estuvo en el margen, no en los ingresos.** La tasa efectiva no-GAAP (18.4%) no se había anotado en la ficha.
- **Binarios: dirección correcta y poca convicción.** 0.58 y 0.55 eran coherentes con un consenso en la parte alta de la guía; el resultado lo superó por poco (0.5% en ingresos y 0.05 en UPA). Una probabilidad más alta no se justificaba con la información del 25-sep: el historial de 4 trimestres de superar el consenso era el único argumento.
- **Qué no se podía saber:** la provisión de litigio de 474 (GAAP; no afecta al no-GAAP) y el +40% de "otros ingresos".
- **Reacción:** −1.7% after-hours con un resultado arriba del consenso. [Inferencia] Lo que el precio descontaba era la guía de FY27 o el crecimiento de incentivos (+21%, más rápido que los ingresos brutos). No se verificó la llamada.

## 4. Lecciones (cada una cambia algo concreto)
1. **Margen neto en emisoras de margen estable:** usar la mediana de los últimos 4 trimestres (54.0-54.1%), no un recorte hacia la guía, salvo evidencia específica. Aquí el recorte a 53.6% costó la mayor parte del error.
2. **Tasa efectiva (lección recurrente, cuarto caso en una semana tras AMX, BOLSA y Cemex):** anotar en la §8 la tasa efectiva no-GAAP de los últimos 4 trimestres junto al supuesto.
3. **Incentivos a clientes:** crecieron +21%, contra un +13% de los ingresos netos. En la próxima ficha, modelar ingresos brutos e incentivos por separado: es la línea que mueve el precio aunque el neto cumpla.

No hay errores de hecho que registrar: el 4T25 (10,724 y 2.98) coincide con la ficha.
