# Ficha · El Brier real contra el de un pronosticador perfectamente calibrado (contraste con 55 resueltos)

> Laboratorio del 20-oct-2026. Tema "Pronóstico y puntuación Brier" (cap. 08), en "Comprendido con comprobación". Continúa `fichas/2026-10-01-brier-poder.md`, que derivó la teoría; aquí se contrasta con los datos reales. Fase 0.

## Pregunta
El 20-oct, con n ≥ 50, el Brier global (0.2103) **no cumplió** el objetivo de ≤ 0.20. ¿Es por mala calibración, que es corregible, o por falta de nitidez (probabilidades cerca de 0.5), que es un problema de qué preguntamos?

## Fuente y acceso
- **Datos:** `bitacora/pronosticos.csv` íntegro: 55 pronósticos resueltos al 20-oct a las 18:0x UTC (29 de claude, 22 de vigía, el resto de cripto).
- **Métodos:** se citan de memoria y la implementación se comprueba con aserciones. **No se releyeron hoy.**
  - Murphy (1973), descomposición REL − RES + UNC, comprobada numéricamente en la ficha del 1-oct.
  - Prueba Z de calibración de Spiegelhalter (1986, *Statistics in Medicine* 5).

## Derivación
- **Si p es la probabilidad verdadera de cada evento,** E[(p − o)²] = p(1 − p). El Brier esperado de un pronosticador **perfectamente calibrado** con las mismas p es la media de p(1 − p).
- **Spiegelhalter:** Z = Σ(o − p)(1 − 2p) / √(Σ(1 − 2p)² p(1 − p)), que se distribuye N(0,1) bajo calibración perfecta.
- **Simulación:** 20,000 historias en las que cada evento ocurre con probabilidad p (semilla 20261020). Dan la distribución del Brier de ese pronosticador perfecto.

## Resultados (código: `fichas/codigo/2026-10-20-brier-contraste-real.py`, con aserciones)
| Grupo | n | Brier real | Esperado si estuviera calibrado | Z de Spiegelhalter | P(simulado ≥ real) | **P(calibrado ≤ 0.20)** | Frecuencia − p media |
|---|---|---|---|---|---|---|---|
| Global | 55 | 0.2102 | 0.2140 | −0.20 | 0.57 | **0.23** | +0.030 |
| claude | 29 | 0.2271 | 0.2126 | +0.51 | 0.29 | 0.35 | −0.048 |
| vigía | 22 | 0.1962 | 0.2152 | −0.74 | 0.76 | 0.29 | +0.069 |

Murphy global: REL 0.0247, RES 0.0574, UNC 0.2433. La identidad extendida, con el término de varianza dentro de la cubeta, cierra a 1e-9.

## Lectura
1. **El sistema no está mal calibrado.** El Brier global es incluso un poco mejor que el que daría la calibración perfecta con las mismas probabilidades. Z = −0.20 no rechaza la calibración.
2. **El objetivo de ≤ 0.20 es inalcanzable con las preguntas que hacemos.** Un pronosticador perfecto con nuestras p lo pasaría solo **23%** de las veces. Confirma con datos lo que la ficha del 1-oct estimó en teoría (0.207 esperado; P(pasar) = 0.39 con n = 50).
3. **Lo que lo mueve es la nitidez:** preguntas en las que tengamos información para dar 0.15 o 0.85 sin perder la calibración. Un caso: un pronóstico de 0.80 bien calibrado aporta 0.16 al esperado, contra 0.21 de uno de 0.70.
4. **claude contra vigía (n chico, no significativo):** mis eventos ocurren menos de lo que pronostico (−4.8 pp) y los del vigía, más (+6.9 pp). Ninguna Z llega a 1.

## Contraejemplo y límites
- **Bajar las preguntas difíciles no es mejorar.** Si el sistema se limita a preguntas obvias (p = 0.95), el Brier baja sin ninguna habilidad. El objetivo de ≤ 0.20 premia la facilidad de las preguntas tanto como la habilidad.
  - **Métrica que no se deja engañar:** el skill contra la tasa base, o el contraste de esta ficha (real contra calibrado con las mismas p). Hoy, con las mismas p, nuestro Brier es 0.004 mejor.
- **Las preguntas no son independientes:** P0071 y P0096 son la misma variable, y P0075 y P0095 también. Eso infla n y estrecha los intervalos. La simulación supone independencia.
- **n = 55** sigue siendo poco para separar claude de vigía.

## Error propio que corrige
El aprendizaje del brief del 19-oct (§7) decía "**subestimo** la probabilidad de que las cosas pasen", leyendo las cubetas **globales**. Por autor, el sesgo positivo es del **vigía** (+0.069); el mío es **negativo** (−0.048). Queda anotado en `registro-de-errores.md`.

## Uso en el sistema (propuesta; no cambia ninguna regla)
- **El criterio de salida de fase 0** (`config/parametros.json`: Brier ≤ 0.20 sostenido) mezcla habilidad con dificultad de las preguntas. Propuesta para el balance mensual, que decide:
  - reportar junto al Brier el **Brier esperado con calibración perfecta** y la **Z de Spiegelhalter**;
  - medir el avance como "Brier real − esperado < 0", sostenido, en vez del umbral fijo.
- **Para quien escribe pronósticos:** buscar nitidez con fundamento (σ histórica, tasas base) en vez de 0.5-0.65 por defecto.

## Segunda comprobación
- Con 0.7 y 0.4, el esperado es (0.21 + 0.24) / 2 = 0.225 (aserción).
- El Brier global de 0.2102 coincide con `pronosticos.py puntuar` (0.2103 con n = 54 en la pre-apertura; hoy hay un resuelto más).

## Estado nuevo
**"Contrastado":** la teoría del 1-oct se contrastó con los 55 resultados reales y concuerda (0.207 esperado en teoría; 0.214 con la mezcla de hoy).
