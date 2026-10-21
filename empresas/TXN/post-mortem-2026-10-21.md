# Post-mortem · Texas Instruments (TXN) · 3T26 (reportado el 21-oct-2026, después del cierre)

> Rutina de cierre, 21-oct-2026 (~21:40 UTC). Los pronósticos se registraron el 25-sep en `empresas/TXN/pronosticos.csv`, antes del resultado. Las resoluciones están en `empresas/TXN/resoluciones.csv`. La ficha estimaba el 27-oct (Yahoo/MarketBeat) o el 20-oct (Zacks); TI publicó el martes 21-oct. Fase 0.

## 1. Resultado real (fuente primaria)
8-K del 21-oct-2026 (ítems 2.02 y 9.01), comunicado Ex. 99 ([SEC](https://www.sec.gov/Archives/edgar/data/97476/000009747626000165/q32026txnex99-eredgar.htm)).

| Concepto | 3T26 | Comparación |
|---|---|---|
| **Ingresos** | **US$6,055 M** | +28% a/a, +11% t/t; 3T25: 4,742 |
| Analógico | 4,911 M (+32%); utilidad operativa 2,505 | — |
| Procesamiento Embebido | 858 M (+21%); utilidad operativa 227 | — |
| Otros | 286 M (−6%) | — |
| Margen bruto | 64.2% (3,887 M) | 2T26: 61.4% |
| Utilidad de operación | 2,874 M (47.5%) | +73% |
| Utilidad neta | 2,425 M | +78% |
| **UPA diluida GAAP** | **2.62** | +77%; 3T25: 1.48; 921 M acciones |
| Flujo operativo / FCF | 3,419 M / 2,956 M en el trimestre | FCF 12m: 8,422 M |
| Capex | 463 M | 12m: 2,578 M |

- **Partida no guiada:** la UPA incluye una **reducción de 1 centavo** que no estaba en la guía original.
- **Guía del 4T26:** ingresos de **US$5.80-6.30 mil M** (punto medio 6.05; consenso del 4T en la ficha: 5.72) y UPA de **2.45-2.79** (punto medio 2.62).
- **Capital:** dividendos de 1,298 M; recompras de 48 M; dividendo trimestral declarado de 1.42 (antes 1.36).
- **Reacción (provisional, Yahoo chart, secundaria):** cierre regular de US$284.65; ~US$286.64 a las 21:35 UTC, **+0.7%**, después de tocar ~292 al abrir la sesión posterior. La reacción del día se mide con el cierre del 22-oct.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos | 6,040 (5,780-6,280) | 5,907.8 | 6,055 | −0.25% | −2.43% | Dentro del 80% |
| UPA diluida GAAP | 2.49 (2.31-2.76) | 2.415 | 2.62 | −4.96% | −7.82% | Dentro del 80% |
| P(ingresos > 5,907.8) | 0.72 | — | Sí | — | — | Brier 0.0784 |
| P(UPA > 2.415) | 0.68 | — | Sí | — | — | Brier 0.1024 |

Brier promedio de los binarios: **0.0904**.

## 3. Matriz y lectura
- **Ingresos: buen proceso, buen resultado.** El método (punto medio de la guía +2.4%) dio casi exacto: la superación real fue de +2.6% sobre el punto medio (5.90). Mucho mejor que el consenso.
- **UPA: buen proceso, resultado dentro pero bajo.** La superación fue de +9.2% sobre el punto medio de la guía (2.40), en línea con el +12.0% del 2T. El margen bruto (64.2%) superó nuestro ~62.7%: el margen bruto incremental t/t fue ~90% (cálculo propio), igual o mayor que el ~87% del 2T. El p90 ampliado a 2.76 en la verificación fue la decisión correcta; el p90 original (2.68) también habría contenido el real.
- **Qué se sabía el 25-sep:** la guía del 3T, el margen incremental de ~87% del 2T, la depreciación ya estabilizada y las superaciones previas.
- **Qué no se podía saber:** la fecha exacta (TI no la había confirmado) y el tamaño de la guía del 4T.
- **Escenario:** el punto medio de la guía del 4T (6.05 mil M) cruza el umbral de > 6.0 mil M que la ficha fijó para el **alcista**. Se mueve de base a alcista para la próxima ficha, sujeto a la reacción del 22-oct y al cierre de Silicon Labs.

## 4. Lecciones (cada una cambia algo concreto)
1. **El método "punto medio de la guía + superación histórica" funcionó en ingresos (error −0.25%)**; mantenerlo para TXN. En UPA, la superación histórica (+10% a +12%) debe usarse completa, no recortada por supuestos de margen conservadores: el punto habría sido ~2.64.
2. **Fecha de reporte no confirmada:** ninguna de las dos fuentes (27-oct y 20-oct) acertó. Regla para la rutina de fichas: con fecha no confirmada, la resolución debe cubrir la ventana completa desde la fecha más temprana plausible, y revisar IR semanalmente.
3. **Registrar un pronóstico de guía del 4T** cuando la ficha fija un umbral de escenario sobre ella (aquí > 6.0 mil M). Sin pronóstico, el disparador no se puede calificar. Checklist de la próxima ficha de TXN.

No hay errores de hecho para `conocimiento/registro-de-errores.md`. Los binarios son del orquestador (autor claude), no votos de comité, así que no se actualiza `competencia/calibracion-agentes.csv`.
