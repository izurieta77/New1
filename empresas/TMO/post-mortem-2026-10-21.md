# Post-mortem · Thermo Fisher Scientific (TMO) · 3T26 (reportado el 21-oct-2026, antes de la apertura)

> Rutina de cierre, 21-oct-2026. Los pronósticos se registraron el 25-sep en `empresas/TMO/pronosticos.csv`, antes del resultado, y no se modifican. La fecha de resolución registrada era el 29-oct, porque la fecha del reporte no estaba confirmada. La empresa reportó el 21-oct (como estimaba Yahoo) y se resuelve hoy. Las resoluciones están en `empresas/TMO/resoluciones.csv`. Fase 0.

## 1. Resultado real (fuente primaria)
8-K del 21-oct-2026, comunicado ([SEC](https://www.sec.gov/Archives/edgar/data/0000097745/000009774526000173/q32026earnings8kex99_1.htm)). Trimestre al 26-sep-2026.

| Concepto | 3T26 | Comparación |
|---|---|---|
| **Ingresos (revenue)** | **US$12,137 M** | +9%: orgánico +6%, adquisiciones y desinversiones +3%, tipo de cambio 0%; 3T25: 11,122 |
| Margen de operación GAAP / ajustado | 18.6% / 24.5% | 17.4% / 23.3% |
| UPA diluida GAAP | 4.64 | +9% |
| **UPA ajustada** | **6.68** | +15%; 3T25: 5.79 |
| FCF | 2,115 M | 1,840 M |
| Life Sciences Solutions | 2,719 M; margen 37.6% | ≈ +5% |
| Analytical Instruments | 2,002 M; margen 26.9% | ≈ +6% |
| Specialty Diagnostics | 1,098 M; margen 31.0% | ≈ −6% (salida de microbiología) |
| Lab Products & Biopharma Services | 6,863 M; margen 15.5% | ≈ +15% (Clario) |

- **Partidas que separan la UPA GAAP de la ajustada:** amortización 1.40; reestructuración y otros 0.54 (incluye una ganancia de US$72 M por venta de un negocio y una pérdida de 244 M por activos mantenidos para venta, en las notas del año; la venta de microbiología se completó en el trimestre); costo de ventas 0.02; gastos generales −0.06 (crédito de US$20 M: costos de transacción e integración y cambios en contraprestación contingente, sin detalle); otros 0.04; impuestos 0.07; asociadas 0.02. **No hay recuperación arancelaria IEEPA** en el comunicado (revisado por la lección de RTX del 20-oct). El crédito de −0.06 queda **fuera** de la UPA ajustada, así que no la infla.
- **Guía 2026:** no está en el 8-K. La empresa dice que la actualiza en la llamada de las 7:00 ET. **No verificada en fuente primaria.** La guía previa (julio, MarketBeat) era de UPA ajustada de 24.93-25.33. Con 18.15 en nueve meses, el rango previo implica un 4T de 6.78-7.18.
- **Recompras:** US$4,000 M en nueve meses (2,963 M un año antes).
- **Reacción (Yahoo chart v8, secundaria):** abrió en 665.00 (−3.3%) y cerró en **694.02, +1.0%** contra 687.37 del 20-oct. La causa de la reversión no está verificada (probablemente la guía de la llamada).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos | 12,050 (11,850-12,250) | 11,951 | 12,137 | −0.72% | −1.53% | Dentro del 80% |
| UPA ajustada | 6.52 (6.33-6.72) | 6.408 | 6.68 | −2.40% | −4.07% | Dentro del 80%, a 0.04 del p90 |
| P(ingresos > 11,951) | 0.73 | — | Sí | — | — | Brier 0.0729 |
| P(UPA ajustada > 6.408) | 0.78 | — | Sí | — | — | Brier 0.0484 |

Brier promedio de los binarios: **0.0607**.

## 3. Matriz y lectura
- **Ingresos: buen proceso, buen resultado.** El punto suponía orgánico de ~5%, adquisiciones de ~+3.5% y divisas de +0.5-1%. Real: orgánico de 6%, M&A de +3% y divisas de 0%. Más orgánico compensó la falta de divisas. Error de la mitad del error del consenso.
- **UPA: buen proceso, buen resultado, pero el sesgo sigue.** El punto (6.52) estuvo más cerca que el consenso, pero el real quedó otra vez en la parte alta del intervalo. Margen ajustado de 24.5% (+1.2 pp). Es el **quinto trimestre seguido** en que TMO supera el consenso de UPA (ahora +4.2%; los 4 previos de la ficha: +5.3%, +1.9%, +3.8% y +5.6%). La estacionalidad 2T→3T de 2025 (+8%) fue corta: este año fue +10.8% (6.03 → 6.68).
- **Binarios bien calibrados:** 0.73 y 0.78 partían de la tasa base de la emisora (4 de 4 en la ficha). Brier promedio de 0.061, el mejor de la semana.
- **Qué se sabía el 25-sep:** la aceleración orgánica (1% → 5%), el margen de AI en alza, Clario el trimestre completo y la historia de sorpresas positivas (§4.8 de la ficha).
- **Qué no se podía saber:** la magnitud de la expansión del margen y que las divisas serían neutras.
- **Escenario:** el orgánico de 6% toca el umbral del **alcista** (≥6%) de la ficha; el umbral bajista (≤3%) queda lejos. Queda entre base y alcista hasta conocer la guía 2026 actualizada en fuente primaria y la guía 2027 (ene-2027). El DCF inverso (~11-12% anual) sigue exigente.

## 4. Lecciones (cada una cambia algo concreto)
1. **En TMO, centrar el punto de UPA ~4% sobre el consenso, no ~2%.** Cinco sorpresas seguidas promedian +4.2%; el real quedó a 0.04 del p90. Parámetro para la próxima ficha: punto = consenso × 1.04 y p90 a +7% del consenso.
2. **Registrar el crecimiento orgánico como pronóstico numérico.** Es la variable que la ficha usa para cambiar de escenario (≤3% bajista, ≥6% alcista) y no estaba en el ledger. Checklist de la próxima ficha de TMO.
3. **Cuando la guía anual se da en la llamada y no en el 8-K, dejar el post-mortem con la guía "no verificada" y sin inferirla del precio.** La reversión de −3.3% a +1.0% ocurrió durante la llamada, así que la reacción del día depende de un dato que el 8-K no trae. Regla para los post-mortems de emisoras con guía oral (TMO, entre otras): buscar la transcripción o el 10-Q antes de clasificar el escenario.
4. **Fechas no confirmadas:** la fecha de resolución registrada (29-oct) fue tardía; Yahoo (21-oct) acertó. Al registrar, usar la fecha más temprana de las fuentes como fecha de resolución.
5. **IEEPA:** se revisó el comunicado y no hay recuperación arancelaria; el crédito de −0.06 en gastos generales está excluido de la UPA ajustada.

No hay errores de hecho para `conocimiento/registro-de-errores.md`. Los binarios son del orquestador (autor claude), no votos de comité, así que no se actualiza `competencia/calibracion-agentes.csv`.
