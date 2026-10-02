# Ficha de estudio: ¿un pico de riesgo geopolítico predice el mercado?

> Laboratorio, 2-oct-2026. Fase 0. Tema "Geopolítica y GPR" (cap. 23), que estaba en Documentado. El paso pendiente era replicar Caldara-Iacoviello: GPR alto → rendimiento siguiente. Se trabaja con la alerta Irán/Ormuz en ALTA desde el 1-oct.
> Código: `conocimiento/fichas/codigo/2026-10-02-gpr-rendimientos.py` (stdlib + `herramientas`, semilla 20261002, ~9 s).

## 1. Pregunta
Cuando el índice de riesgo geopolítico (GPR) da un salto, ¿el mercado de EUA rinde distinto el mes siguiente, a 3 meses o a 12 meses? ¿Sube la volatilidad? En otras palabras, ¿la noticia geopolítica deja una señal operable o ya está en el precio?

## 2. Fuentes y acceso
| Fuente | Acceso |
|---|---|
| Caldara e Iacoviello, GPR mensual (`data_gpr_export.dta`, matteoiacoviello.com), vía `herramientas/geopolitica.py` | Íntegro, 1985-2026 (último dato: 2026-09, GPR = 146.2) |
| French, `F-F_Research_Data_Factors`, mensual y diario (exceso de mercado) | Íntegro hasta ~~2026-07~~ **2026-08** (corrección 2026-10-02, verificación W40: el archivo descargado llega a 2026-08 y la muestra n = 487 lo usa como el mes siguiente del choque de 2026-07) |
| Caldara e Iacoviello (2022), *AER* 112(4) | No releído; citado en el cap. 23 |

## 3. Diseño
- **Choque:** log(GPR del mes) menos la media del log de los 12 meses previos.
- (1) **Regresión** del exceso de mercado del mes siguiente (y de la volatilidad realizada del mes siguiente, con datos diarios) sobre el choque, con t de Newey-West de 3 rezagos.
- (2) **Estudio de eventos:** meses con choque en el 5% superior (y en el 10% como robustez), comparados con todos los meses. Valor p por permutación (5,000).

## 4. Resultados (n = 487 meses de choque, 1986-01 a 2026-07; rendimientos del mes siguiente hasta 2026-08)
- **Regresión:** beta del exceso del mes siguiente de +0.68 pp por unidad de log-choque (**t = 0.88**). En volatilidad, +1.14 pp (**t = 0.80**). **Nada significativo.**
- **Eventos del 5% superior** (n = 25; incluyen Kuwait 1990-91, 11-sep-2001, Irak 2003, Ucrania 2022, Israel 2023 e Irán 2025-26):

| Ventana | Eventos | Todos | Diferencia | p (permutación) |
|---|---|---|---|---|
| **Mismo mes** | −1.02% | +0.76% | **−1.77 pp** | **0.043** |
| +1 mes | +1.87% | +0.76% | +1.11 pp | 0.22 |
| +3 meses | +2.31% | +2.25% | +0.06 pp | 0.97 |
| +12 meses | +5.77% | +9.17% | −3.40 pp | 0.30 |
| Volatilidad +1 mes | 16.9% | 15.0% | +1.9 pp | 0.29 |

- **Nota de verificación (2026-10-02, W40):** el p = 0.043 del mismo mes sale de una permutación que supone la misma varianza en los meses de evento y en el resto. Pero los meses de evento son más volátiles (desviación estándar de 6.2% contra 4.4%). Con pruebas que no suponen eso, la diferencia **no es significativa**: Welch t = −1.48 (p ≈ 0.14), regresión sobre una dummy de evento con Newey-West de 0 a 6 rezagos t = −1.51 a −1.56 (p ≈ 0.12-0.13) y Mann-Whitney p ≈ 0.14. Además, la diferencia depende de agosto de 1998 (−16.1%, la crisis rusa y LTCM, no un evento geopolítico): sin ese mes baja a −1.15 pp, y sin los dos peores a −0.72 pp. Con 5 ventanas probadas, Bonferroni lleva el p a ≈ 0.21. La cifra de −1.77 pp es correcta; su significancia, no.
- **Robustez con el 10% superior** (n = 49): mismo mes −0.67 pp (p 0.27), +1 mes +0.64 pp (p 0.30), +12 meses +0.76 pp (p 0.74). **Desaparece incluso el efecto del mismo mes.**

## 5. Lectura
1. **Nada predice lo que sigue; tampoco hay un efecto robusto en el mismo mes.** ~~El riesgo geopolítico se paga en el momento, no después. Solo los choques más extremos coinciden con un mes peor (−1.8 pp, p = 0.04)~~ (corrección 2026-10-02, W40: el −1.8 pp del mismo mes no es significativo con pruebas robustas a heterocedasticidad, con p ≈ 0.13-0.14, y depende de ago-1998; ver la nota de §4). Como mucho, el riesgo geopolítico se refleja en el momento, sin evidencia sólida de que se pague. El signo del mes siguiente es positivo (rebote), sin significancia.
2. **No hay señal operable** ni para vender después del choque ni para comprar en el rebote. Coincide con lo que el cap. 23 dice de los mercados de predicción y con Känzig-Stock-Zanotti (el daño llega por tasas).
3. **Para la alerta Irán/Ormuz en ALTA:** la evidencia respalda la decisión del decisor de **no actuar por la noticia en sí**. Solo actuar si se disparan reglas medibles (cortacircuitos, filtro, FX-1) o si cambia el canal de tasas e inflación.

**Contraste con la literatura** (agregado tras verificar el paper del día):
- Hirshleifer, Mai y Pukthuanthong (2025, *RFS* 38(2)) encuentran una **prima por riesgo de guerra**: con el GPR, +1 DE anticipa +2.5% a +7.3% anualizado de exceso al mes siguiente (t de 1.7 a 2.3; R² ≤ 1.4%).
- Nuestro signo (+0.68 pp/mes por unidad de log-choque, rebote de +1.1 pp tras los choques extremos) **va en la misma dirección**, pero no es significativo con un choque medido contra la media de 12 meses.
- Lectura conjunta: si hay algo, es una prima **a favor de mantener o comprar** tras el choque, no de vender, y es demasiado pequeña e inestable para operarla.

## 6. Contraejemplo y límites
- **Contraejemplo:** en 1990 (Kuwait) y en 2001-02, el mercado sí siguió cayendo meses después del choque. Pero esa caída se mezcla con una recesión ya en curso; el GPR no la anticipó por sí solo.
- **Límites:**
  - Los eventos están agrupados (meses consecutivos de la misma crisis), así que la permutación sobrestima la independencia.
  - Solo cubre el mercado de EUA en USD; no se probó México ni MXN.
  - El GPR mide cobertura de prensa, no daño económico.
  - Falta septiembre de 2026 en los rendimientos (French llega a ~~julio~~ agosto; corrección 2026-10-02, W40).
- **Segunda comprobación:** cambiar el umbral al 10% superior da la misma conclusión, sin predicción.

## 7. Estado nuevo
Geopolítica y GPR pasa de **Documentado** a **Comprendido con comprobación**.
