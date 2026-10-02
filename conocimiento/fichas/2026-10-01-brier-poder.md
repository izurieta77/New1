# Ficha de estudio: Brier, descomposición de Murphy y el poder del criterio de salida

> Laboratorio, 1-oct-2026. Fase 0. Tema "Pronóstico y puntuación Brier" (cap. 08), que estaba en Documentado. Sostiene el **criterio de salida de fase 0**: Brier ≤ 0.20 sostenido 3 meses, con 50 o más resueltos (`config/parametros.json` → `prioridad_actual.criterio_salida` y `pronosticos.brier_objetivo`).
> Código: `conocimiento/fichas/codigo/2026-10-01-brier-poder.py` (stdlib, semilla 20261001, ~5 s). Se corrió dos veces con resultados idénticos.

## 1. Pregunta
¿El umbral de Brier ≤ 0.20 mide habilidad? ¿Qué probabilidad tiene de pasarlo un pronosticador **perfectamente calibrado** con la mezcla de preguntas que de verdad registra el sistema? ¿Cuántos pronósticos hacen falta para distinguir 0.20 de 0.25?

## 2. Fuentes y acceso
| Fuente | Acceso |
|---|---|
| Brier (1950), *Monthly Weather Review* 78(1) | No releída; la definición está en el cap. 08 |
| Murphy (1973), *J. Applied Meteorology* 12(4): descomposición BS = REL − RES + UNC | No releída; la identidad se comprueba numéricamente abajo |
| `bitacora/pronosticos.csv` (47 pronósticos al 1-oct) | Íntegro |

## 3. Supuestos y derivación
- **Brier de un pronóstico:** (f − o)². Si el pronosticador está calibrado (f = q, la probabilidad verdadera), E[(q − o)²] = q(1 − q).
- **Consecuencia:** el Brier esperado de un pronosticador **perfecto en calibración** es E[q(1 − q)]. Depende solo de la **nitidez**, es decir, de qué tan lejos de 0.5 caen las preguntas. Una pregunta de 50/50 da 0.25 aunque se pronostique con perfección.
- **Murphy:** BS = REL (calibración, menor es mejor) − RES (resolución, mayor es mejor) + UNC (incertidumbre de la tasa base, que no depende del pronosticador).

## 4. Resultados
1. **Identidad de Murphy comprobada:** con 2,000 pronósticos discretos y un sesgo de +5 pp, BS = 0.177800 = REL − RES + UNC = 0.0019 − 0.0729 + 0.2488.
2. **Brier esperado con calibración perfecta y la mezcla actual de la bitácora:** con n = 47 y |p − 0.5| medio de 0.162, **E[p(1 − p)] = 0.207**.
   - **Un pronosticador perfecto, con las preguntas que hoy hacemos, queda arriba del objetivo de 0.20.**
   - Referencias: con pronósticos de 0.70/0.30 el Brier esperado es 0.210; con 0.75/0.25, 0.1875; con 0.80/0.20, 0.160.
3. **Distribución del Brier con n = 50** (20,000 simulaciones):

| Pronosticador | Brier medio | IC 90% | P(Brier ≤ 0.20) |
|---|---|---|---|
| Calibrado, mezcla actual | 0.207 | 0.171-0.245 | **0.39** |
| Calibrado, p en 0.25/0.75 | 0.188 | 0.143-0.243 | 0.64 |
| Calibrado, p en 0.15/0.85 | 0.128 | 0.079-0.191 | 0.97 |
| Sobreconfiado +10 pp, mezcla actual | 0.216 | 0.164-0.271 | 0.32 |

4. **Poder estadístico:** para distinguir un Brier de 0.20 de uno de 0.25 (una cola al 5%, poder de 80%) hacen falta **~61 pronósticos** con la mezcla actual y **~116** si las preguntas son de 0.25/0.75. Con n = 50, el error estándar del Brier es de 0.022 a 0.031.

> **Nota de verificación (2026-10-02, W40):** las cifras se reproducen con código propio (numpy, 200,000 simulaciones) sobre el CSV de 47 filas (commit `80dbe10`): E[p(1−p)] = 0.2068, P(Brier ≤ 0.20) = 0.386, IC 90% de 0.171 a 0.244, sobreconfiado P = 0.32, n ≈ 61 y ≈ 116. La mezcla ya cambió. Con las **52 filas al 2-oct**: |p − 0.5| medio de 0.156, **E[p(1−p)] = 0.210**, **P(Brier ≤ 0.20 | calibrado, n = 50) ≈ 0.33** (0.35 si se repite la mezcla fija en lugar de remuestrearla), n ≈ 58 y sobreconfiado P ≈ 0.28. La conclusión de §6 se refuerza: la mezcla se está acercando a 0.5. "Mezcla actual" quiere decir al 1-oct (47 pronósticos).

## 5. Contraejemplo y segunda comprobación
- **Contraejemplo:** un pronosticador sin ninguna habilidad puede pasar el umbral si **elige preguntas fáciles** (p cerca de 0 o 1). Con preguntas de 0.15/0.85 bien calibradas, pasa 97% de las veces. El umbral premia **elegir preguntas**, no **saber**.
- **Segunda comprobación (analítica):** E[q(1 − q)] con la mezcla actual (0.2068) coincide con la media simulada (0.2068). La identidad de Murphy cuadra al sexto decimal.

## 6. Lo que cambia para el sistema (inferencias; el cambio de parámetro es del dueño)
1. **El criterio "Brier ≤ 0.20" está mal especificado como prueba de habilidad.** Con las preguntas de hoy, un pronosticador perfecto solo lo pasa 39% de las veces, y uno sin habilidad con preguntas fáciles lo pasa casi siempre.
2. **Alternativas mejor especificadas** (propuesta en `bitacora/decisiones-pendientes.md`):
   - (a) **Brier skill score** contra una referencia externa por pregunta: el precio del mercado de predicción, el consenso o la tasa base histórica.
   - (b) **Prueba de calibración**: la Z de Spiegelhalter, o el componente REL de Murphy por debajo de un umbral.
   - (c) Mantener 0.20, pero **exigir una nitidez mínima declarada** o comparar contra el Brier esperado de un calibrado con la misma mezcla.
3. **Para la disciplina de registro:** no hay que inflar ni desinflar las probabilidades para "pasar" el umbral. Lo correcto es pronosticar la probabilidad verdadera. Así la calibración (REL) se mide limpia.

## 7. Límites
La mezcla de preguntas cambiará conforme se registren más. La simulación supone resultados independientes, pero varios pronósticos comparten el mismo factor (petróleo, tasas) y eso infla la varianza real. No se leyeron Brier (1950) ni Murphy (1973) en texto completo.

## 8. Estado nuevo
Pronóstico y puntuación Brier pasa de **Documentado** a **Comprendido con comprobación**.
