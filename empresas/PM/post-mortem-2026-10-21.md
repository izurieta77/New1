# Post-mortem · Philip Morris International (PM) · 3T26 (reportado el 21-oct-2026, antes de la apertura)

> Rutina de cierre, 21-oct-2026. Los pronósticos se registraron el 25-sep en `empresas/PM/pronosticos.csv`, antes del resultado, y no se modifican. Las resoluciones están en `empresas/PM/resoluciones.csv`. Fase 0.

## 1. Resultado real (fuente primaria)
8-K del 21-oct-2026, comunicado ([SEC](https://www.sec.gov/Archives/edgar/data/0001413329/000162828026066596/earningsreleasepm-ex991xq3.htm)).

| Concepto | 3T26 | Comparación |
|---|---|---|
| **Ingresos netos (net revenues)** | **US$11,438 M** | +5.5%; orgánico +7.1%; 3T25: 10,845 |
| Utilidad de operación GAAP | 4,866 M (margen ≈42.5%) | +14.1% |
| Utilidad de operación ajustada | 5,117 M (margen 44.7%) | +1.6 pp |
| UPA diluida GAAP | 2.12 | −4.9% |
| **UPA ajustada** | **2.36** | +5.4%; sin tipo de cambio 2.37 (+5.8%); 3T25: 2.24 |
| Embarques de libres de humo | 48.2 mil M de unidades | +2.7% (2T26: +7.5%) |
| HTU de IQOS (embarques / IMS ajustado) | 41.5 mil M / +7.1% | embarques +1.5%; participación de IQOS de 9.9% |
| ZYN EUA (embarques) | 3.2 mil M de bolsas | +4.2% |
| Cigarros | 158.0 mil M de unidades, planos | precio de combustibles +8.9% |

- **Partidas que separan la UPA GAAP de la ajustada:** amortización de intangibles 0.13; ajuste a valor razonable de inversiones en acciones 0.06; impuesto por el financiamiento de Swedish Match 0.01; pérdida por la compra (buy-out) del plan de pensiones holandés 0.04. **No hay recuperación arancelaria IEEPA** ni otro reembolso en el comunicado (revisado por la lección de RTX del 20-oct).
- **Japón:** el IMS ajustado de HTU creció 3.4%; sin el adelanto de compras previo al alza del 1-oct, 1.3%. La empresa lo describe como "en línea con lo esperado". La cadena causal A de la ficha se confirmó, pero fue pequeña.
- **Guía 2026:** UPA ajustada de **8.29-8.44** (antes 8.35-8.50, el 8-sep); sin tipo de cambio, 8.11-8.26, +7.5-9.5%, sin cambio. Es un recorte solo por divisas. Ingresos orgánicos +5-7% ("más probable la mitad o la parte alta"); utilidad de operación orgánica +7-9% ("más probable la mitad o la parte baja"); flujo operativo de ~13.5 mil M. No hay guía explícita del 4T. Anuncia más inversión en ZYN en EUA y un costo de energía algo mayor en el 4T.
- **Reacción (Yahoo chart v8, secundaria):** abrió en 187.14 (−6.4%) y cerró en **197.46, −1.2%** contra 199.90 del 20-oct. La causa no está verificada. Candidatas: embarques de libres de humo de solo +2.7% (HTU +1.5%), guía anual recortada por divisas y más gasto en ZYN en el 4T.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos netos | 11,420 (11,120-11,720) | 11,356 | 11,438 | −0.16% | −0.72% | Dentro del 80%, casi en el centro |
| UPA ajustada | 2.39 (2.31-2.47) | 2.3425 | 2.36 | +1.27% | −0.74% | Dentro del 80% |
| P(ingresos > 11,356) | 0.58 | — | Sí | — | — | Brier 0.1764 |
| P(UPA ajustada > 2.3425) | 0.74 | — | Sí | — | — | Brier 0.0676 |

Brier promedio de los binarios: **0.1220**.

## 3. Matriz y lectura
- **Ingresos: buen proceso, buen resultado.** El punto (orgánico ~+7% con el adelanto de Japón y −2% de divisas) acertó casi exacto: el orgánico fue +7.1% y las divisas restaron ~1.6 pp. El binario en 0.58 fue tímido para un punto que ya estaba 0.6% arriba del consenso con un intervalo estrecho.
- **UPA: buen binario, punto optimista.** Superar 2.3425 salió Sí por 1.8 centavos; el 0.74 fue razonable. Pero el punto (2.39) fue el único de los cuatro números que quedó **peor que el consenso**. Lo construí suponiendo que PM volvería a superar el tope de su guía trimestral por 5-6%, como en el 1T y el 2T. Esta vez lo superó por 0.9% (2.36 contra 2.29-2.34).
- **Qué se sabía el 25-sep:**
  - que la guía del 3T ya se había elevado a mitad del trimestre (8-sep, de 2.20-2.25 en julio a 2.29-2.34), así que el "colchón" habitual ya estaba gastado en parte;
  - el USD más fuerte desde el 8-sep (§8 de la ficha) y la mayor inversión en EUA en el 2S;
  - el calendario de Japón.
- **Qué no se podía saber:** la desaceleración de los embarques de libres de humo (+2.7% contra +7.5% del 2T) y la pérdida del plan de pensiones holandés.
- **Escenario:** guía sin divisas intacta, orgánico en la mitad o parte alta de +5-7% y UPA 2026 de 8.29-8.44, un poco por debajo del rango base (8.40-8.55) solo por divisas. Sigue en el **base**, con una señal de vigilancia en el volumen de IQOS. La apertura de −6.4% muestra que el precio (P/U de ~23x, el doble que sus pares) es sensible a cualquier freno de los libres de humo.

## 4. Lecciones (cada una cambia algo concreto)
1. **Cuando la empresa actualiza la guía trimestral a mitad del trimestre, no aplicar el patrón histórico de "supera el tope por X%".** El colchón ya está consumido en parte. Regla para la próxima ficha de PM (y emisoras que actualizan guía en conferencias de septiembre): centrar el punto de UPA en el tope de la guía más ~1%, no más 5-6%.
2. **Registrar un pronóstico de embarques de libres de humo (o de HTU de IQOS)** junto con UPA e ingresos. Es la variable que sostiene la prima del múltiplo y la candidata a explicar la apertura en −6.4% aunque UPA e ingresos superaron. Checklist de la próxima ficha de PM.
3. **Binario de ingresos coherente con el punto:** si el punto queda arriba del consenso con un intervalo estrecho (±2.6%), la probabilidad debe ser ~0.62-0.65, no 0.58. Se suma a la regla propuesta de partir de la tasa base (post-mortem de GE del 20-oct).
4. **IEEPA:** se revisó el comunicado y no hay recuperación arancelaria. La pregunta se queda en el checklist de las emisoras importadoras de EUA.

No hay errores de hecho para `conocimiento/registro-de-errores.md`. Los binarios son del orquestador (autor claude), no votos de comité, así que no se actualiza `competencia/calibracion-agentes.csv`.
