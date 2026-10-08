# AC-15 / R04: auditoría con tercera fuente del efecto Halloween (EUA)

Fecha de ejecución: 2026-10-08. Pregunta: ¿el estado de R04 (efecto Halloween: noviembre a abril contra mayo a octubre) se sostiene con una tercera fuente de EUA distinta de French CRSP y de Yahoo `^GSPC` (usada en AC-04)? ¿Dentro y fuera de muestra? ¿En qué periodo cambia la conclusión?

Respuesta corta: **no se pudo verificar con tercera fuente**. La única serie mensual de EUA con dividendos que cubre 1926 (hoja de Shiller) calcula el precio como promedio mensual, no como cierre de fin de mes. Eso mezcla meses calendario y la hace inválida para una prueba de estacionalidad mensual. Las otras fuentes de FRED que probé son más cortas (2016 en adelante) o tienen el mismo problema. Lo que sí se pudo hacer: un control de código con la misma lógica sobre French reproduce las cifras del original, y con Shiller el efecto tiene el mismo signo que el original fuera de muestra pero no es significativo.

## Archivos

| Archivo | Qué es |
|---|---|
| `convertir_shiller_xls.py` | Paso de preparación (no estadístico). Convierte `ie_data.xls` a CSV. Usa `xlrd` (fuera de la biblioteca estándar); se corrió con `xlrd` instalado en un directorio temporal. Verifica que el código año.mes coincida con la fecha fraccional de Shiller (0 discrepancias). |
| `ac15_r04_independiente.py` | Réplica independiente. Solo biblioteca estándar. Escrita desde la sección de pre-registro (secciones 1 a 9 de `laboratorio/replicas/R04-efecto-halloween.md`). No se abrió `R04.py`. |
| `salida.txt` | Salida completa de `python3 -I ac15_r04_independiente.py`. |
| `resultados_independiente.json` | Cifras clave (efecto, alineación, ventanas móviles, estrategias, control). |
| `datos_crudos/` | Datos crudos con hash (ver abajo). |

Reproducción: `python3 convertir_shiller_xls.py` (requiere `xlrd`), luego `python3 -I ac15_r04_independiente.py > salida.txt`.

## Fuentes evaluadas

| Fuente | Cobertura | Resultado |
|---|---|---|
| Shiller `ie_data.xls` (S&P Composite; P y D) | Precio mensual 1871-01 a 2023-09; dividendo D hasta 2023-06 | **Usada como tercera fuente de EUA, pero no es válida para el calendario.** Ver control de alineación. |
| FRED `SPASTT01USM661N` (OECD, índice de precio de EUA) | 1957-01 a 2026-08 | Probada como alternativa. Mismo patrón de promedio mensual (corr. en rezago 0 y +1 de 0.70 y 0.58; rezago -1 de 0.04). **No válida.** |
| FRED `SP500` | 2016-10-10 a 2026-10 | **No alcanza 1988** (la petición lo suponía). Insuficiente. |
| FRED `DJIA` | 2016-10-10 a 2026-10 | Insuficiente (mismo recorte). |
| FRED `TB3MS` (T-bill 3 meses) | 1934-01 a 2026-09 | Usada solo como efectivo. **Antes de 1934-01 no hay efectivo**, así que las pruebas con efectivo y las estrategias empiezan en 1934-01. |
| French F-F factores (CRSP) | 1926-07 a 2026-08 | Solo control: verificación de alineación (crac de octubre de 1987: −23.19%) y control de código (misma lógica que el original). No es la serie probada. |
| Yahoo `^GSPC` | — | No usada: ya la usó AC-04, y el criterio pide una tercera fuente. |
| Yahoo `^MXX` (México) | — | **No re-ejecutado.** Yahoo respondió HTTP 429 en el intento; además es la misma fuente que el original, así que no sería una tercera fuente. Criterio (iv) sin evaluar. |
| Stooq | — | Conexión reiniciada; no disponible. |

## Control de alineación (el hallazgo principal)

Correlación mensual entre el rendimiento total de Shiller en el mes `t+k` y el de French en el mes `t`:

| Rezago k | 1926-1959 | 1960-1989 | 1990-2023 | Todo 1926-2023 |
|---|---|---|---|---|
| −1 | 0.067 | 0.032 | −0.007 | 0.045 |
| 0 | 0.671 | 0.700 | 0.645 | 0.672 |
| +1 | 0.655 | 0.571 | 0.545 | 0.611 |

Con cierre de fin de mes, la correlación en rezago 0 debería ser de 0.95 o más. El patrón observado coincide con un **promedio de dos meses**: si el precio de la fila `t` es el promedio del mes, el rendimiento de la fila `t` mezcla medio mes de `t` y medio de `t−1`. La correlación teórica en rezago 0 y +1 es sqrt(0.5) = 0.707, y en rezago −1 es 0. Shiller reproduce ese patrón en los tres subperiodos. La hoja de Shiller misma indica en su última fila que el precio del mes es el "1st close", así que la convención no es uniforme. OECD muestra el mismo patrón.

**Consecuencia:** con esta fuente, la estacionalidad mensual no se mide por mes calendario. La prueba de Shiller no es una réplica válida de R04.

## Prueba de contaminación (diagnóstico)

Se mezcló el French real de la misma forma (log-rendimiento de `t` promediado con el de `t−1`) y se corrió la misma regresión:

| Ventana | French (real) α₁ (t NW) | French mezclado α₁ (t NW) | Shiller α₁ (t NW) |
|---|---|---|---|
| Dentro 1926-07 a 2002-12 | 0.682 (2.07) | 0.540 (1.63) | 0.391 (1.20) |
| Artículo 1970-01 a 1998-08 | 1.038 (2.32) | 0.804 (1.83) | 0.619 (1.49) |
| Fuera 2003-01 a 2023-06 | 0.406 (1.01) | 0.243 (0.51) | 0.430 (1.01) |

El promedio mensual explica **una parte** de la reducción de α₁ (dentro: de 0.68 a 0.54 contra 0.39 de Shiller). El resto (~0.15 en dentro y ~0.19 en el artículo) viene de la composición de la serie (S&P Composite contra CRSP VW, con 90 acciones antes de 1957). Fuera de muestra, Shiller da un α₁ mayor que el French mezclado, así que el promedio no explica todo. Esta prueba no separa las dos causas del todo.

## Control de código (validación de la réplica)

Misma lógica (regresión, Newey-West, estrategias, costos) aplicada a French, con las fechas del original:

| Métrica | Original (R04 md, sección 11) | Réplica independiente sobre French |
|---|---|---|
| α₁ 1926-07 a 2002-12 (t NW) | 0.6819 (2.07) | 0.6819 (2.07) |
| α₁ 2003-01 a 2026-07 (t NW) | 0.2886 (0.70) | 0.2886 (0.70) |
| α₁ 1970-01 a 1998-08 (t NW) | 1.0377 (2.32) | 1.038 (2.32) |
| US_nov_abr dentro, CAGR / vol / Sharpe / MDD | 8.21% / 12.53% / 0.3962 / −57.60% | 8.22% / 12.54% / 0.3965 / −57.63% |
| US_nov_abr fuera, CAGR / vol / Sharpe / MDD | 6.87% / 10.79% / 0.5161 / −30.32% | 6.88% / 10.80% / 0.5167 / −30.35% |
| Comprar y mantener dentro, CAGR / vol / Sharpe / MDD | 9.80% / 19.36% / 0.3874 / −83.65% | 9.80% / 19.36% / 0.3876 / −83.65% |

Las diferencias son de 0.0003 en CAGR, 0.0006 en Sharpe y 0.0003 en MDD: redondeo. **El código reproduce al original.** Por tanto, las diferencias con Shiller se deben a la fuente y no al código.

## Tabla comparativa (EUA)

Efecto (α₁ en puntos porcentuales log por mes; t Newey-West de 12 rezagos):

| Ventana | Original (French) | Réplica sobre French (control) | Réplica sobre Shiller |
|---|---|---|---|
| Artículo 1970-01 a 1998-08 | 1.0377 (2.32) | 1.038 (2.32) | **0.619 (1.49)** |
| Dentro 1926-07 a 2002-12 | 0.6819 (2.07) | 0.6819 (2.07) | **0.391 (1.20)** |
| Fuera 2003-01 a 2026-07 (Shiller: a 2023-06) | 0.2886 (0.70) | 0.2886 (0.70) | **0.430 (1.01)** |
| Pre-artículo 1926-07 a 1969-12 | 0.3603 (0.75) | no corrido | **−0.019 (−0.04)** |
| Completo | 0.5895 (2.18) | no corrido | 0.399 (1.47) (a 2023-06) |
| Contraste Jacobsen-Zhang 1998-09 a 2011-07 | 0.9300 (1.63) | no corrido | 1.205 (1.88) |

Estrategias EUA, costos por defecto (0.34% por lado), efectivo T-bill:

| Ventana y variante | CAGR | Vol. | Sharpe | MDD | Ops/año |
|---|---|---|---|---|---|
| Dentro 1927-05 a 2002-12, Halloween (original) | 8.21% | 12.53% | 0.396 | −57.6% | 2.00 |
| Dentro 1927-05 a 2002-12, Halloween (control French) | 8.22% | 12.54% | 0.397 | −57.6% | 2.00 |
| Dentro 1934-01 a 2002-12, Halloween (Shiller) | 8.50% | 8.58% | 0.530 | −51.5% | 2.00 |
| Dentro 1934-01 a 2002-12, comprar y mantener (Shiller) | 11.09% | 12.94% | 0.569 | −41.6% | 0 |
| Fuera 2003-01 a 2026-07, Halloween (original) | 6.87% | 10.79% | 0.516 | −30.3% | 1.99 |
| Fuera 2003-01 a 2023-06, Halloween (Shiller) | 6.29% | 9.05% | 0.577 | −29.0% | 2.00 |
| Fuera 2003-01 a 2023-06, comprar y mantener (Shiller) | 10.08% | 12.59% | 0.726 | −49.0% | 0 |
| Fuera 2003-01 a 2023-06, SMA10 (Shiller) | 10.03% | 9.31% | 0.937 | −19.2% | 1.02 |

Nota sobre la comparación de estrategias: las ventanas de Shiller empiezan en 1934 (por TB3MS), así que el MDD de comprar y mantener dentro (−41.6%) no es comparable con el −83.6% de 1927 (que incluye la caída de 1929-32).

## Diferencias y explicación

1. **Alineación de la fuente (mayor).** El precio de Shiller es un promedio mensual. Mezcla meses calendario y reduce α₁ de forma sistemática. Explica parte de la diferencia (ver prueba de contaminación), no toda.
2. **Composición de la serie.** S&P Composite (90 acciones antes de 1957) contra CRSP VW. Explica el resto de la diferencia en α₁ dentro y en el artículo. No se pudo aislar del efecto de alineación.
3. **Dividendos.** No es la causa. Con precio solo (PR) el α₁ dentro es 0.390 contra 0.391 con dividendos. La aproximación D/12 no mueve el resultado.
4. **Ventanas.** Shiller termina en 2023-06 (su D termina ahí; el archivo termina en 2023-09 sin D). El original llega a 2026-07. Las estrategias con efectivo empiezan en 1934-01 (TB3MS). Las diferencias de estrategias de la tabla no son solo de fuente.
5. **Código.** Ninguna diferencia atribuible al código: el control con French coincide con el original.

## Periodo donde la conclusión cambia (Shiller)

- **Ventana creciente desde 1926-07.** α₁ es negativo hasta 1970 (−0.75 en 1950 con t −1.02; −0.35 en 1960 con t −0.64; −0.01 en 1970 con t −0.02), positivo desde ~1975 (0.19), y el t NW nunca llega a 2 (máximo 1.53).
- **Ventanas de 20 años.** De 78 ventanas, 58 tienen t NW < 2. Las que llegan a t ≥ 2 empiezan en 1948-1960 (terminan 1967-1979), en 1983-1986 (terminan 2002-2005) y en 1995-1998 (terminan 2014-2017).
- **Décadas (diagnóstico).** 1950s: 0.52 (t 1.51); 1960s: 1.17 (t 1.84); 1970s: 1.16 (t 1.65); 1980s: 0.13 (t 0.19); 1990s: 1.17 (t 1.45); 2000s: 0.48 (t 0.69); 2010s: 1.09 (t 2.33); 2020-2023: −0.26 (t −0.15).
- **Donde cambia la conclusión entre fuentes:** en 1926-1969 (French 0.36 contra Shiller −0.02) y en el artículo 1970-1998 (1.04 contra 0.62). Ahí se pierde el criterio (i) y el (ii) con Shiller.

## Estado de los criterios pre-registrados (EUA, con Shiller)

| Criterio | Condición | Shiller | Resultado |
|---|---|---|---|
| (i) | 1970-01 a 1998-08: α₁ > 0, \|α₁ − 1.0349\| ≤ 0.20, t MCO ≥ 1.96 | α₁ 0.619, diferencia 0.416, t MCO 1.63 | **No cumple** |
| (ii) | 1926-07 a 2002-12: α₁ > 0 y t NW ≥ 2 | α₁ 0.391, t NW 1.20 | **No cumple** |
| (iii) | 2003-01 a fin: α₁ > 0 | α₁ 0.430 (t NW 1.01) | Cumple (solo signo) |
| (iv) | México 2003-01 a fin: α₁ > 0 | no re-ejecutado | Sin evaluar |

Regla pre-registrada (sección 2 de la ficha): "No replicado" exige α₁ ≤ 0 en 1970-1998 o fuera de muestra en ambos mercados. Ninguna se cumple con Shiller. "Replicado con diferencias" exige α₁ > 0 en el artículo y al menos (iii) o (iv): se cumple por signo. Por tanto, **por la regla, el estado de R04 se mantiene en "Replicado con diferencias"**. Pero la significancia que la ficha asocia a "mismo signo, no significativo" tampoco se sostiene aquí dentro de muestra con esta fuente. Fuera de muestra, la significancia (t NW ≥ 2 y IC bootstrap sin cero) no se cumple con ninguna de las dos fuentes de EUA.

## Limitaciones

1. **No hay tercera fuente válida de 1926-2002 con cierre de fin de mes.** Shiller y OECD promedian el mes. FRED SP500 y DJIA empiezan en 2016. Yahoo `^GSPC` ya lo usó AC-04. Esta es la limitación que impide confirmar o refutar el estado con una fuente independiente.
2. **Shiller es un promedio mensual**, así que la prueba de Shiller no es una réplica del calendario. Los números de Shiller se reportan como diagnóstico y no como evidencia de replicación o de refutación.
3. **Sin México.** Criterio (iv) no evaluado (Yahoo 429; misma fuente que el original).
4. **Efectivo desde 1934.** Las estrategias y las pruebas de exceso sobre efectivo no cubren 1926-1933.
5. **Dividendos aproximados.** D/12 mensual; el efecto es nulo en α₁, pero no se validó contra un índice de retorno total.
6. **Mezcla de dos meses como modelo.** La prueba de contaminación es un modelo simple (promedio de logs de `t` y `t−1`). Sirve para mostrar que el promedio explica parte del efecto, no para corregirlo.
7. **Shiller termina en 2023-06** (D). Fuera de muestra de Shiller: 2003-01 a 2023-06 (246 meses), no 2026-07.
8. **Datos no redistribuibles.** `datos_crudos/` contiene datos de Shiller, FRED y French; el hash está en `salida.txt`. Verificar la licencia antes de compartir.

## Hashes de datos crudos (sha256)

- `shiller_ie_data.xls`: 0df9392b7dacf91f756e92c8db508ad903c4588b43f3253680eec3dd8b40db68
- `shiller_mensual.csv` (generado): b0fe4bc0bd01908d41df9b345f2023411fa713740f499585a6c6c6b3b082bee9
- `french_factors_csv.zip`: 593f4fbef03181bc (ver `salida.txt`; completo en el archivo)
- `fred_TB3MS.csv`: 631bc444a8c5370c (completo en `salida.txt`)
- `fred_SP500.csv`: bcec17353c6f5556f8e8849a9c3215ae0aa506fc2463da8ad772b7d9d0155747 (evidencia del recorte 2016)
- `fred_SPASTT01USM661N.csv`, `fred_DJIA.csv`: evidencia de fuentes descartadas
