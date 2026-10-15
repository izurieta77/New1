# Ficha · Crisis y burbujas: tres casos medidos y qué hizo el filtro de la SMA200

> Laboratorio del 15-oct-2026 (jueves: tema de mayor valor con el nivel más bajo; "Crisis y burbujas" estaba en Documentado con la prueba pendiente "ficha de patrones con 3 casos medidos"). Fase 0: no recomienda inversiones.

## Pregunta
En las tres caídas grandes más recientes de los índices de EUA, ¿cuánto cayeron, cuánto duraron y qué parte de la caída habría evitado la regla de salida vigente del sistema (cierre < SMA200 × 0.97, ejecutando al cierre siguiente)?

## Fuente y nivel de acceso
- **Datos:** cierres diarios de Yahoo chart v8 (`^IXIC`, `^GSPC`), los mismos que descarga `laboratorio/replicas/R14.py` (sha256 en `R14-salida.txt`). Índices de precio, sin dividendos. Lectura íntegra de la serie.
- **Capítulo:** `conocimiento/17-crisis-burbujas-libro-de-patrones.md`.

## Supuestos
- Índice 1x, sin costos. Solo la **primera** salida del filtro después del pico; no se cuentan reentradas ni latigazos posteriores (eso lo midieron R06 y R11 con la estrategia completa).
- "Fracción evitada" = (precio de salida − valle) / (pico − valle).

## Ejercicio numérico (comprobado)
Código: `conocimiento/fichas/codigo/2026-10-15-crisis-tres-casos.py` (aserciones; `python3 -I … laboratorio/replicas/R14-datos`).

| Caso | Pico | Valle | Caída máxima | Días hábiles al valle | Días para recuperar el pico | Primera salida del filtro | Caída al salir | Fracción de la caída evitada |
|---|---|---|---:|---:|---:|---|---:|---:|
| Nasdaq, punto com | 10-mar-2000 (5,048.62) | 9-oct-2002 (1,114.11) | **−77.9%** | 647 | 3,802 (~15 años) | 17-abr-2000 (3,539.16) | −29.9% | 61.6% |
| S&P 500, crisis financiera | 9-oct-2007 (1,565.15) | 9-mar-2009 (676.53) | **−56.8%** | 355 | 1,376 (~5.5 años) | 20-nov-2007 (1,439.70) | −8.0% | 85.9% |
| Nasdaq, alza de tasas | 19-nov-2021 (16,057.44) | 28-dic-2022 (10,213.29) | **−36.4%** | 277 | 570 (~2.3 años) | 21-ene-2022 (13,768.92) | −14.3% | 60.8% |

## Patrones (inferencia sobre tres casos; no es estadística)
1. **La salida llega después de un golpe ya sufrido**, de 8% a 30% en el 1x. En un 3x, ese primer golpe se multiplica: el −29.9% del Nasdaq entre el pico y la salida del 17-abr-2000 es **−70.4%** en un 3x diario sintético sin costos (calculado con la misma serie, rendimiento diario × 3). Es la razón de fondo del stop del UPRO (135.76), que está **antes** que el filtro.
2. **La caída más rápida es la que el filtro protege peor:** el Nasdaq 2000 perdió 30% en cinco semanas antes de la señal. Coincide con arXiv:2607.00883 (la tendencia llega tarde al primer choque; cap. 07, adenda del 15-oct).
3. **Lo que más cuesta es la duración:** recuperar el pico tomó 2.3, 5.5 y 15 años. Para un plan de cuatro meses (la temporada termina el 28-ene-2027), no hay "esperar a que se recupere".
4. Las tres caídas empezaron con el índice **arriba** de su SMA200 y con valuaciones concentradas en un sector (internet en 2000, financieras y vivienda en 2007, tecnología de larga duración en 2021). Hoy, la concentración en IA es el paralelo a vigilar (cap. 17; arXiv:2606.01575).

## Límites
- Tres casos elegidos por ser los más grandes: hay sesgo de selección. No mide los latigazos: R06 y R11 muestran que, con reentradas, el 3x con filtro aun así cayó cerca de −73% en 1998-2003.
- Índices de precio, sin dividendos; el 1x no es el UPRO.

## Contraejemplo
En la caída de **feb-mar 2020** (−34% del S&P 500 en 23 días hábiles, de memoria, no calculado aquí), la salida por SMA200 × 0.97 llega cuando ya se perdió la mayor parte, y la reentrada llega después del rebote: el filtro casi no ayuda en un desplome en V. No se calculó aquí; queda como siguiente prueba.

## Segunda comprobación
- Picos y valles conocidos que coinciden con la historia publicada: Nasdaq 5,048.62 el 10-mar-2000 y 1,114.11 el 9-oct-2002; S&P 500 1,565.15 el 9-oct-2007 y 676.53 el 9-mar-2009.
- Las aserciones del código revisan que la caída al salir sea menor que la máxima y que la fracción evitada esté entre 0 y 1.

## Estado nuevo
"Crisis y burbujas" pasa de **Documentado** a **Comprendido con comprobación**: tres casos medidos con código. Siguiente prueba: el caso de 2020 (desplome en V) y la trayectoria exacta de un 3x sintético en los tres casos.
