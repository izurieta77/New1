# Post-mortem · Morgan Stanley (MS) · 3T26 (reportado el 14-oct-2026, antes de la apertura)

> Rutina de Cierre, 14-oct-2026. Los pronósticos se registraron el 25-sep en `empresas/MS/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado. Las resoluciones están en `empresas/MS/resoluciones.csv`. No hay posición en MS ni pasó por comité, así que no hay decisión de cartera ni votos de agentes que evaluar: solo pronósticos.

## 1. Resultado real (fuente primaria)
8-K del 14-oct-2026, ex. 99.1 ([comunicado](https://www.sec.gov/Archives/edgar/data/895421/000089542126000288/a3q26msearningsrelease.htm)); el ex. 99.2 es el [suplemento](https://www.sec.gov/Archives/edgar/data/895421/000089542126000288/a3q26msfinancialsupplement.htm). Las cifras se verificaron dos veces en la fuente: en la tabla y en el titular.
- **Ingresos netos (*net revenues*):** US$20,338 M, contra 18,224 en el 3T25 (+11.6%) y 21,348 en el 2T26 (−4.7%).
- **Utilidad neta aplicable a MS:** US$4,909 M. **UPA diluida:** 3.03, contra 2.80 en el 3T25 y 3.46 en el 2T26, con 1,566 M de acciones diluidas promedio. El comunicado no presenta UPA sin partidas.
- **Margen y rentabilidad:** margen antes de impuestos de 32%, contra 34% en el 2T y 33% en el 3T25. ROTCE de 22.6%, tasa efectiva de 23.3% y eficiencia de 67%.
- **Gasto:** compensación de 7,997 M y gasto no ligado a compensación de 5,715 M, igual que en el 2T y +20% a/a. Provisión de 148 M, con 105 M de castigos en ISG sobre préstamos corporativos y de bienes raíces comerciales (CRE).
- **Segmentos:**
  - **ISG:** 10,029 M. Banca de inversión 2,159, Equity 5,799 (+41% a/a) y renta fija 2,011 (−7%).
  - **WM:** 9,065 M, récord. Margen de 30.4%; comisiones de gestión de activos de 5,544 M, transaccional de 1,166 y NII de 2,228. Activos nuevos netos (NNA) de **US$232.4 mil M** y flujos *fee-based* de 80.5 mil M.
  - **IM:** 1,459 M, contra 1,651 en el 3T25 (−12%).
- **Capital:** CET1 estandarizado de 14.9%. Recompras de 1,540 M (~7 M de acciones a 212.74 en promedio). Dividendo de US$1.15.
- **Reacción del precio (Yahoo, fuente secundaria):** cerró en 181.51, contra 186.64 el 13-oct (**−2.75%**).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro | Consenso | Real | Error nuestro | Error consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos netos (punto; p10-p90) | 20,900 (19,700-22,100) | 20,840 | 20,338 | +2.76% | +2.47% | Dentro del intervalo de 80% |
| UPA diluida GAAP (punto; p10-p90) | 3.32 (3.00-3.64) | 3.16 | 3.03 | +9.57% | +4.29% | Dentro del intervalo de 80%, a 0.03 del p10 |
| P(ingresos > 20,840) | 0.53 | — | No | — | — | Brier 0.2809 |
| P(UPA > 3.16) | 0.72 | — | No | — | — | Brier 0.5184 |

El error es (pronóstico − real) / real. El Brier promedio de nuestros dos binarios es **0.3997**. Con la tasa base de FactSet (0.70 en ingresos y 0.78 en UPA) habría sido 0.49 y 0.6084 (promedio 0.549). Con 0.50 constante habría sido 0.25.

Con el consenso de Zacks, el resultado cambia: 20,338 supera los ingresos de 19,880 (+2.3%) y empata en la práctica con su UPA de 3.06 (−1%). Los binarios se registraron contra Yahoo, así que resuelven No.

## 3. Matriz y lectura
- **Decisión mediocre y resultado malo en UPA.** El punto de 3.32 quedó por encima del consenso de Yahoo (3.16) y del de Zacks (3.06). El p = 0.72 se apoyaba sobre todo en el historial de 4 sorpresas positivas de 11-35%. Era un argumento de *momentum* de sorpresas, no un dato del trimestre. Además, la ficha registraba en contra la frase de Simkowitz del 15-sep, "*3Q is no 2Q*", que era la versión de MS de la guía de BAC. Con BAC la usamos para movernos contra el consenso; con MS la ignoramos.
- **Puente aproximado de UPA, de 3.32 a 3.03** (cálculo propio):

  | Componente | Efecto en UPA |
  |---|---|
  | Ingresos 562 M abajo (al 34% de margen y 77% después de impuestos) | ≈ −0.09 |
  | Margen de 31.9% contra 34%: gasto no ligado a compensación de 5.7 mil M, +20% a/a | ≈ −0.21 |
  | Preferentes de 158 contra 145 y acciones de 1,566 contra 1,563 | ≈ −0.01 |
  | **Suma** | **≈ 3.01**, contra 3.03 real |

  **El error principal fue de margen y gasto, no de ingresos.**
- **Ingresos, por componente:**

  | Componente | Modelado | Real |
  |---|---|---|
  | Equity | 5.5 | 5.80 |
  | Banca de inversión | 2.3 | 2.16 |
  | Renta fija | 2.3 | 2.01 |
  | WM | 9.3 | 9.07 |
  | IM | 1.7 | 1.46 |

  El error de IM (−0.24) es el más grande en proporción y no tenía señal en la ficha. Que se deba a comisiones de desempeño o a inversiones es inferencia sin verificar en el suplemento.
- **Suerte contra calidad.** El binario de ingresos (p = 0.53) era en la práctica una moneda al aire, y el real quedó 2.4% abajo: es un resultado neutral sin mucha información. El binario de UPA perdió con razón: el p = 0.72 era más alto que lo que justificaba el modelo, cuyo punto estaba 5% sobre el consenso pero con un intervalo de ±10%, y que la evidencia fechada en contra.
- **Qué se sabía el 25-sep:**
  - La frase "*3Q is no 2Q*".
  - El NII de WM guiado a "*modest sequential increase*", que se cumplió con 2,228.
  - Que MS no mueve sus metas durante el año (margen de WM de 30%, que se cumplió con 30.4%).
  - Que el 2T26 tuvo un margen excepcional de 34.4%, que tomamos como base del 3T.
- **Qué no se podía saber:** el salto del gasto no ligado a compensación (+20% a/a), sin detalle verificado aquí, y la caída de IM.
- **Escenario:** los NNA de 232.4 mil M (récord) y los flujos *fee-based* de 80.5 mil M rebasan con mucho lo que la ficha usaba para distinguir escenarios. Equity sube 41% a/a. Sigue el **base**, con sesgo hacia el alcista en WM. Matiz: falta separar cuánto de los NNA vino otra vez de OPIs del canal Workplace; en el 2T fue "*just over half*". El ROTCE de 22.6% está dentro del rango base de 22-25%.

## 4. Lecciones (cada una cambia algo concreto)
1. **Simetría en el uso de la guía intratrimestral.** Si una guía de conferencia (BAC el 14-sep, MS el 15-sep) mueve el binario de una empresa, debe moverlo también en sus pares con guía equivalente. Regla propuesta para la §8 de `ficha-empresa`: listar las guías intratrimestrales y declarar explícitamente en qué dirección mueven cada binario.
2. **Margen: no extrapolar el pico del trimestre anterior.** En bancos de inversión, el margen antes de impuestos del pronóstico se toma como el promedio de los últimos 4 trimestres, no el último. Aquí habría sido ~32-33% contra el 34% usado, y el punto habría quedado en ~3.15.
3. **Las rachas de sorpresas no justifican p > 0.70 por sí solas.** La tasa base de FactSet (78% en UPA) ya incorpora que las empresas superan el consenso con frecuencia. Subir arriba de ella exige un dato del trimestre. Hoy el 0.72 perdió 0.52 de Brier.
4. **Sesgo optimista en puntos de UPA:** 3 de 3 en el lote de bancos (ver el post-mortem de BAC, lección 3). Se propone el mismo descuento de 3%.

Acumulado del 13 y 14-oct (JPM, BAC y MS):
- **Binarios:** nuestro Brier promedio es **0.256** (6 binarios), contra 0.549 de la tasa base y 0.25 de 0.50 constante. Los 6 resolvieron No. n = 6 sigue siendo poco para concluir.
- **Intervalos numéricos:** 5 de 6 cayeron dentro del p10-p90, contra 80% esperado. Están bien calibrados, aunque todos los puntos quedaron arriba del real.

No hay errores de hecho que registrar en `conocimiento/registro-de-errores.md`: los errores fueron de supuestos (margen, IM) y de juicio en el binario de UPA. Los pronósticos se resolvieron en `empresas/MS/resoluciones.csv`. No se ejecutó `herramientas/pronosticos.py resolver` porque esta rutina no edita `bitacora/pronosticos.csv`. Como no hubo comité, no se actualiza `competencia/calibracion-agentes.csv`.
