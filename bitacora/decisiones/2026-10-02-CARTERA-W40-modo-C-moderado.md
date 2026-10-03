# Decisión de cartera · comité semanal W40 · viernes 2-oct-2026

> Skill `comite-de-inversion`. Preside el orquestador con el rol de `decisor`. Expediente: `bitacora/comite/2026-10-02-expediente.md`. Han pasado 5 días hábiles desde la decisión del 25-sep (REGLAS §4). Fase 0 con la excepción de la cuenta arena vigente.

## Decisión
**APROBADO: modo C moderado en GBM.** Se agrega un **27% en UPRO (3x del S&P 500) con stop obligatorio y filtro de tendencia**; el resto sigue en índices 1x. **Nunca TQQQ.** **Binance se mantiene en 40% BTC**, sin ETH. **Tipo de cambio: exposición en USD sin cobertura, como decisión explícita.**

## Tesis y cómo se refuta
- **Tesis:** dentro del mandato del dueño (modo C, máxima agresividad que permiten los topes), un 3x del S&P de tamaño moderado, con filtro y stop, sube la mediana de la temporada (+6.3% contra +4.9% de la cartera A, 1994-2026 en MXN; corregido el 3-oct, ver nota al final) sin acercar la cuenta al −20%: P(−20%) es de 0.6% con stop y 2.6% sin stop. El Nasdaq 3x queda descartado por su cola histórica (−93.6% filtrado en 2000-03).
- **Refutación (al 28-ene-2027):** la tesis falla si se cumple cualquiera de estas:
  - (a) el TWR queda debajo de la cartera A calculada en sombra menos 3 pp;
  - (b) la cuenta toca −20%;
  - (c) el stop o el filtro se activan más de 3 veces, señal de serrucho.

## Dictámenes (3 líneas cada uno)
- **Macro, C-moderado (60).** El 10a en 5.29% y la tasa real de 2.93% están en el percentil 100: es un choque estanflacionario de petróleo y el daño entra por la tasa de descuento. El Nasdaq es el activo más largo en duración, así que nada de TQQQ. Propone 25% en SPXL/UPRO, sin subir a 50% mientras el 10a esté ≥ 5% y el crédito siga en vigilancia; BTC al 40% y largo en USD sin cobertura.
- **Cuantitativo, C-moderado (60).** El 3x filtrado le gana al 1x por +14.4%/año en MXN (t = 3.35), pero con T-bill de 5% el borde esperado baja a ~8%/año y en una temporada es indistinguible de cero. Propone 35% en SPXL/UPRO, con P(−12/−20%) de 21-31 y 1.3-5.3%; con TQQQ serían 52 y 16%. Regla: ^GSPC con banda de ±3%; BTC al 40%, porque 65% no lo justifican los datos.
- **Geopolítico, C-moderado (55).** Da 52% al cese al fuego hasta el 31-oct (Polymarket 59.5%) y 35% a una ruptura después de las intermedias del 3-nov. Propone 20-25% en UPRO/SPXL, mitad ahora y mitad después del 4-nov; sin TQQQ y BTC al 40%. No cubrir el FX: el sesgo es a un peso más débil, que amortigua.
- **Cripto, 65% BTC (60).** Pasar de 40 a 65% recorta la brecha contra rivales al 90-100% con P(−20%) de 7% o menos. De 65 a 100% triplica P(−20%) sin mejorar la mediana desde 2018. ETH no: empeora la mediana. Salida del filtro en 69,219.
- **Abogado del diablo:** C-pleno **no sobrevive** (75); C-moderado **sobrevive con condiciones** (55: 25-30% UPRO/SPXL, sin TQQQ, banda de ±3%, confirmar el ticker y el fondeo, BTC al 65%); A **no sobrevive** como decisión final (65), porque incumple el mandato. Su objeción de W39 ("6 reportes de rivales antes de apalancar") cede ante el mandato. "No SPXL con 10a ≥ 5%" pasa de veto a limitar el tamaño.

## Votos y confianzas
| Agente | GBM | Confianza | Binance |
|---|---|---|---|
| analista-macro | C-moderado (25%) | 60 | 40% |
| analista-cuantitativo | C-moderado (35%) | 60 | 40% |
| analista-geopolitico | C-moderado (20-25%, escalonado) | 55 | 40% |
| analista-cripto | — | — | 65% (60) |
| abogado-del-diablo | C-moderado con condiciones | 55 | 65% |

- **GBM:** 4 de 4 a favor de C-moderado; confianza media de 57.5, arriba del mínimo de 55. El abogado dice que sobrevive, así que se aprueba.
- **Binance:** 3 a 2 por mantener 40%.

## Gestor de riesgo: APRUEBA CON CAMBIOS
- **Condición dura:** el UPRO entra **con stop registrado** (`excepcion_cuenta_arena.reglas` y riesgo por operación de 3%). **Sin stop habría veto.**
- **Papel:** vender 2 SPYM y comprar 2 UPRO, con **stop en precio de ejecución × 0.8908** (134.40 USD con 150.88), un riesgo de 598 MXN (2.93%). Queda SPYM 5 (40.2%), QQQM 1 (27.4%), UPRO 2 (26.8%) y efectivo de ≈1,120 (5.5%). Exposición nocional de 1.48x.
- **P(tocar −12/−20/−28/−35%) en 4 meses, en MXN:** con stop, 13.8/0.6/0/0% (1994-2026); sin stop, 23.5/2.6/0/0%.
- **Cola estática:** un día como el 16-mar-2020 equivale a −15% (dispararía el −12% en un día).
- **Límites:** todos cumplen. etf_apalancado 26.8%/50%, etf_indice ≤ 60%, orden mínima, 2 de 8 operaciones al mes y rotación de 0.43x.
- **Kelly** (fracción 0.5) sugeriría 0-5% en UPRO. Se anota como advertencia: prevalece el mandato del dueño.
- **Topes provisionales ratificados:** 5,000 GBM / 2,500 cripto y orden mínima de 2,500.

## Verificación
El orquestador recalculó las cifras que sostienen la decisión: pesos 40.2/27.4/26.8%, stop −10.92%, riesgo 598.06 MXN (2.93%), efectivo 1,119.96 y mínimo de UPRO para la orden mínima en 137.78 USD. Todo cuadra.
- La auditoría adversarial de la semana (`bitacora/semanal/2026-W40-verificacion.md`) confirmó al decimal las fichas del filtro y de Brier.
- Esa auditoría refutó la significancia de la ficha GPR (p ≈ 0.12-0.14 con pruebas robustas). Eso refuerza la decisión de no actuar por la noticia.

## Regla operativa del 3x (provisional hasta que el dueño ratifique `filtro_apalancados`)
- **Entrada:** ^GSPC cierra arriba de su SMA200 × 1.03 **y** VIX < 25. Hoy: 7,722.72 contra 7,442.59, y VIX 15.3, así que el filtro está encendido.
- **Salida del 100% del 3x al día siguiente:** ^GSPC cierra abajo de su SMA200 × 0.97 (7,009) **o** VIX ≥ 25, **o** se toca el stop.
- **Cada salida o reentrada consume cupo** de las 8 operaciones del mes.

## Ejecución
- **Papel:** O0004 (venta de 2 SPYM) y O0005 (compra de 2 UPRO con stop) en `bitacora/ordenes-pendientes.csv`, para el lunes 5-oct a las 14:45 UTC con la condición del filtro.
- **Real:** la boleta del 30-sep queda **ANULADA** y la reemplaza `bitacora/boletas/2026-10-05.md`: 3 SPYM + 1 UPRO con stop, solo si el dueño **confirma que UPRO (o SPXL) aparece en GBM y fondea**. Si no, solo los 3 SPYM.
- **Binance:** sin cambio (40% BTC).

## Disenso (se conserva)
- **Tamaño:** el cuantitativo quería 35% y el geopolítico 20-25% escalonado. Se eligió ~27%, que es lo que permiten los títulos enteros.
- **BTC:** el analista cripto y el abogado querían 65%; la mayoría lo dejó en 40%. Pasa a revisión el 9-oct con estos criterios: vol de 30 días ≤ 45%, cierre arriba de 87,396 y datos de rivales.
- **Tasas:** el macro y el abogado advierten que el 10a ≥ 5% sigue siendo la objeción principal. Si el 10a pasa de 5.5% o el HY OAS pasa de 3.5%, hay que volver a A.
- **Kelly:** recomienda casi nada de 3x. Se priorizó el mandato del dueño.

## Pronósticos registrados
- **P0053 (comité):** la cuenta GBM de papel toca −12% antes del 28-ene-2027, p = 0.15.
- **P0054 (geopolítico):** el cese al fuego EUA-Irán se sostiene hasta el 31-oct, p = 0.52.
- **P0055 (geopolítico):** Ormuz normalizado antes del 31-dic, p = 0.15.

## Nota de corrección (3-oct-2026, decisor vespertino, tras el hallazgo bloqueante de la revisión del 2-oct)
- **Artefacto archivado:** los scripts y datos del gestor de riesgo ahora están en `arena/modelos/comite_w40_riesgo/` (README, `sim.py`, `stop.py`, salidas y SHA256). Re-ejecutados el 3-oct, reproducen exactamente:
  - P(−12/−20/−28/−35%): 23.5/2.6/0/0% sin stop y 13.8/0.6/0/0% con stop (1994-2026, MXN); 10.5/0.2% con stop (2004-2026);
  - mediana del modo C moderado: +6.3%.
- **Error corregido:** la mediana de la cartera A en esa misma salida es **+4.9%** (1994-2026) y **+4.1%** (2004-2026), no "+5.2-5.9%". Ese rango venía del dictamen cuantitativo, con otra configuración, y se etiquetó mal. Su P(−12%) es 8.9% (1994-2026).
- **La decisión no cambia:** la brecha de mediana a favor del modo C en la historia (+1.4 pp) es mayor de lo que se citó. Pero esa historia tiene una prima de ~8%. Con una prima de ~4%, la ficha `conocimiento/fichas/2026-10-02-costo-del-apetito.md` estima que el modo C crece ~0.9 pp **menos** por temporada. El comité del 9-oct debe ver las dos cifras juntas.
