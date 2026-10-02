# AC-11: segunda ejecución independiente de R07 (curva 10a−3m y recesión, Estrella-Mishkin)

> Fase 0, formación. Nada de esto es una recomendación de inversión. Todas las cifras son históricas, en USD salvo donde se indica, antes de impuestos.

| Campo | Valor |
|---|---|
| Réplica auditada (A) | `laboratorio/replicas/R07-curva-invertida-y-recesion.md` (corrida final 2026-09-25 06:37 UTC; FRED GS10, TB3MS, USREC, USRECQ, T10Y3M; French CRSP 202607) |
| Ejecución independiente (B) | `AC11.py` en esta carpeta. Python 3.11 + numpy 2.4. De `herramientas/datos.py` solo usa `parsear_fred_csv` y `parsear_yahoo_json`; del código de AC-09 solo el lector OLE2/BIFF8 del xls de Shiller. No importa ni copia `R07.py`, `R07_verificacion.py`, `herramientas/backtest.py` ni `validacion_estrategias`. El probit (Newton-Raphson con gradiente y hessiano analíticos), el sándwich de Newey-West, el pseudo R² de Estrella, las etiquetas del NBER en tiempo real, el AUC, el motor, los costos, las métricas y el DSR están escritos en `AC11.py` |
| Fecha | 2026-10-02 (descargas 17:49-17:54 UTC; `datos/descarga_utc.txt`) |
| Comando | `python3 laboratorio/auditorias/AC-11-curva-recesion/AC11.py` (sin red, ~10 s; lee `datos/` y reescribe `datos/SHA256SUMS.txt`, `salida.txt` y `resultados.json`) |
| sha256 de `AC11.py` | `a59e34a0e36c025b24d88df2bef097de2c359ee1d600a3719d56c760cad0367d` (versión ciega, antes de la conciliación: `ebf44e1a…8787`) |

## Protocolo ciego

1. De la ficha R07 leí solo el encabezado y las secciones 1 a 9 (pre-registro). La línea "Estado" del encabezado ya resumía el veredicto de A (H1/H2 replicados; H3 y H6 refutadas) y la tabla maestra lo repite; no vi ninguna cifra de resultados de A.
2. Descargué los datos, escribí `AC11.py` y generé `salida.txt` (bloques A1-A5 y H6). Guardé esa salida (sha256 `1ef24abe…59be`) a las 17:53 UTC.
3. Después leí las secciones 10 a 17 de R07. No leí `R07.py`, `R07_verificacion.py`, `R07-salida.txt`, `R07-resultados.json` ni `R07-variantes.csv`; las cifras de A salen de la ficha.

Después de leer A agregué a `AC11.py` el bloque `[CONCILIACION]` (al final de la salida), un parámetro opcional `Pmx` en `reglas` (no cambia nada si no se usa) y tres archivos de control en `datos/` (`control_fred_GS10.csv`, `control_fred_TB3MS.csv` y el zip French 202607 de A, mismo sha256 `b840dba5…f5eb`). Se verificó con `diff` que todas las líneas anteriores de `salida.txt` quedaron idénticas a la salida ciega (solo se agregan las tres huellas de control en el encabezado).

## Fuentes (B usa fuentes distintas de A)

| Serie | Uso en B | Fuente exacta | Rango usado | sha256 |
|---|---|---|---|---|
| `DGS10` | 10 años: promedio mensual de los datos diarios (A usa el promedio mensual `GS10`) | FRED, `fredgraph.csv?id=DGS10` | 1962-01 a 2026-09 | `bddfe0bd…5dca` |
| `IRLTLT01USM156N` | 10 años antes de 1962 (no hay CMT diario): rendimiento largo de EUA de la OCDE | FRED | 1953-04 a 1961-12 | `17339e70…312f` |
| `DTB3` | T-bill 3 meses diario, base descuento → BEY día por día con 365·d/(360−91·d) → promedio mensual (A convierte el promedio mensual `TB3MS`). También el efectivo: promedio mensual/1200 | FRED | 1954-01 a 2026-09 | `1e9dbca8…3e58` |
| `T10Y3M` | Control del spread, meses invertidos, racha diaria y último dato | FRED | 1982-01-04 a 2026-10-01 | `4085b93b…577d` |
| Picos y valles mensuales del NBER | Recesión mensual R_m = 1 del mes siguiente al pico al valle (A usa `USREC`) | `data.nber.org/data/cycles/business_cycle_dates.json` | 1854-2020 | `675edfab…1551` |
| Picos y valles trimestrales del NBER | Recesión trimestral: del trimestre siguiente al trimestre del pico al trimestre del valle (A usa `USRECQ`) | Tabla de la página "US Business Cycle Expansions and Contractions" (nber.org) | 1854-2020 | `13f7a42a…7eaa` |
| Anuncios del NBER | Etiquetas en tiempo real (A usa la tabla de su §3 y la comprueba con ALFRED) | Página "Business Cycle Dating Committee Announcements" (12 anuncios de 1980-2021, leídos por expresión regular) | 1980-2021 | `ef9110e9…97bc` |
| `^GSPC` + Shiller D/12; `^SP500TR` | Mercado (A5, H6): S&P 500 con rendimiento total (A usa French CRSP) | Yahoo y shillerdata.com (mismos archivos que AC-10) | 1928-01 a 2026-09 | `e1c5a167…f615f`, `044196da…89c1`, `244d8687…8f94` |
| `DEXMXUS` | MXN, último dato del mes | FRED (mismo archivo que AC-10) | 1993-11 a 2026-09 | `0b71c05f…e4b` |
| `GS10`, `TB3MS`, French 202607 | **Solo control C**, después de leer A | FRED; copia de AC-10 | — | `40323f22…13b6`, `631bc444…c08c`, `b840dba5…f5eb` |

`DGS3MO` se descargó pero no se usa. No se usó ALFRED: las etiquetas en tiempo real salen de la página de anuncios. Para 1959-1978 se aplica el supuesto pre-registrado (giro conocido 12 meses después). Condiciones de uso de FRED, NBER, Yahoo y Shiller: no verificadas.

**Control de la serie.** S_B − promedio mensual de T10Y3M (1982-02 a 2026-09): media +0.0088 pp, |máx| 0.127 pp (A: +0.0089 y 0.1345). S_B − S_A (control C, 1954-01 a 2026-08): media +0.0002 pp, |máx| 0.0097 pp. **Un solo mes cambia de signo: 2019-05** (S_B −0.005, S_A +0.00). La tabla trimestral del NBER difiere de "mayoría de meses en recesión" en 1960T2, 1980T1, 1980T3, 1981T3 y 1990T3; B usa la tabla trimestral oficial.

## Resultados de B

**A1/H1 (trimestral, orígenes 1959T1 a 1995T1−k).** k = 4: α −0.5879, β −0.7837, t MV −5.08, t NW(3) −4.72, pseudo R² **0.287** (artículo 0.296). Máximo en k = 4; k = 1: 0.061, k = 8: 0.031. Spread con P = 50%: −0.750 (ventana de origen 1959T1). Sensibilidades k = 4: NW(4) −4.97; ventana por objetivo 0.286; base descuento 0.272; solo fuentes diarias (orígenes desde 1962T1) 0.302. **H1: Replicado.**

**A2/H2 (fuera de muestra, objetivos 1971T1-1995T1).** k = 1..8: 0.041, 0.218, 0.297, **0.294**, 0.279, 0.176, −0.004, −0.216. Brier k = 4: 0.0817 contra 0.1289 de la climatología. **H2: Replicado.**

**A3 (mensual, 12 meses).** Dentro 1959-01 a 1994-03: β −0.6727, t NW(11) −4.10, pseudo R² 0.250, AUC 0.870. Completa 1959-01 a 2025-08: β −0.5531, t NW −4.54, R² 0.155. Fuera de muestra:

| Tramo | n | R² (L_c ventana) | R² (L_c recursiva) | Brier | Brier clima | AUC |
|---|---|---|---|---|---|---|
| 1970-01 a 1998-02, tiempo real | 338 | 0.278 | 0.317 | 0.0807 | 0.1232 | 0.905 |
| **1998-03 a 2025-08, tiempo real (H3)** | 330 | **−0.034** | 0.004 | **0.0900** | **0.0819** | 0.709 |
| 1998-03 a 2025-08, cronología final | 330 | −0.031 | 0.002 | 0.0899 | 0.0812 | 0.715 |
| 1998-03 a 2024-02, tiempo real | 312 | 0.005 | 0.042 | 0.0873 | 0.0858 | 0.737 |
| 1998-03 a 2025-08, coeficientes fijos 1959-1994 | 330 | −0.018 | 0.020 | 0.0910 | 0.0819 | 0.737 |

**H3: refutada** (R² ≤ 0 y Brier ≥ climatología). Con umbral 0.5: 17 señales, todas sin recesión.

**A4/H4.** S_B < 0 en 27 meses (2022-11 a 2025-04; mínimo −1.70 en 2023-05); T10Y3M mensual < 0 en 30. Racha diaria de T10Y3M < 0: 534 sesiones (2022-10-25 a 2024-12-12), mínimo −1.89 el 2023-05-04. Meses de recesión del NBER de 2022-12 a 2026-04: 0; picos posteriores a feb-2020: 0. **Falso positivo a la fecha.** Probit en tiempo real: 17 meses con P > 0.5 (2023-01 a 2024-08), máximo 0.712 en 2023-05.

**Probabilidad actual (P de recesión en los próximos 12 meses).** Con S_B de 2026-08 (+0.872): **0.105** en tiempo real (igual con la muestra completa) y 0.124 con los coeficientes de 1959-1994. Con S_B de 2026-09 (+0.952, mes completo que A no tenía): 0.098. Con el último T10Y3M diario (+1.07 el 2026-10-01): 0.087 con el modelo completo y 0.063 con los coeficientes implícitos de *Current Issues*. La calibración de esa cifra no está validada: después de 1998 el modelo no le ganó a la tasa base (H3).

**A5/H5 (S&P 500 TR).** Hay 9 inicios: 1966-01, 1968-12, 1973-06, 1978-11, 1989-06, 2000-07, 2006-08, **2019-05** y 2022-11. A 12 meses, la media es 3.91% contra 12.34% incondicional (sd 16.32%), con t aproximado de **−1.55**: **H5 se sostiene** (no es significativamente menor).

**H6 (motor, S&P 500 TR contra DTB3, costo 0.34% por lado).**

| Variante | Sharpe dentro | MDD dentro | Sharpe fuera | MDD fuera | CAGR fuera |
|---|---|---|---|---|---|
| inv1 | 0.601 | −29.6% | 0.463 | −50.9% | 7.98% |
| inv3 | 0.607 | −29.6% | 0.464 | −50.9% | 8.16% |
| inv3_medio | 0.541 | −33.1% | 0.492 | −50.9% | 8.66% |
| probit50 | 0.604 | −29.6% | 0.479 | −50.9% | 8.54% |
| probit30 | 0.597 | −29.6% | 0.429 | −50.9% | 7.61% |
| probit_cont | 0.564 | −29.4% | 0.471 | −49.9% | 7.86% |
| **inv_fuera12** (elegida) | **0.620** | −29.6% | **0.418** | −46.6% | 6.86% |
| desinv12 | 0.473 | −29.6% | 0.560 | −41.8% | 9.34% |
| comprar y mantener | 0.464 | −42.7% | **0.509** | −50.9% | 9.11% |
| SMA10 | 0.419 | −23.8% | 0.554 | −22.9% | 7.71% |

- No agrega valor frente a comprar y mantener ni frente a la SMA10. **H6 refutada.** No se refuta su uso como freno: la MDD es menor dentro y fuera de muestra.
- DSR de `inv_fuera12` fuera de muestra (V de los 8 ensayos): 0.964 con N = 8 y 0.958 con N = 16. Es contra Sharpe 0, no contra el índice.
- En bruto, ninguna regla de inversión o de probit supera a comprar y mantener fuera de muestra (la mejor llega a 0.495), salvo `desinv12` (0.567).
- Con base descuento: `inv1`, `inv3` e `inv3_medio` dan 0.471, 0.426 y 0.472 fuera de muestra.
- En MXN, fuera de muestra (CAGR / MDD): `inv_fuera12` 9.56% / −27.2%; comprar y mantener 11.86% / −40.1%; SMA10 10.43% / −31.1%.

## Comparación con A

Tolerancias: pseudo R² ± 0.01 (la tolerancia del pre-registro contra el artículo es ± 0.05); 0.05 de Sharpe; 1 pp de CAGR.

| Métrica | A | B | Dif. | ¿En tolerancia? |
|---|---|---|---|---|
| H1 k = 4: β / t NW(3) / pseudo R² | −0.7838 / −4.72 / 0.287 | −0.7837 / −4.72 / 0.287 | 0.000 | Sí |
| H1 k = 1..8, pseudo R² | 0.061 … 0.031 | idénticos a 3 decimales | ≤ 0.001 | Sí |
| H2 k = 4 (k = 5; k = 1) | 0.294 (0.280; 0.041) | 0.294 (0.279; 0.041) | ≤ 0.001 | Sí |
| A3 mensual 1959-1994: β / t NW / R² | −0.6726 / −4.10 / 0.250 | −0.6727 / −4.10 / 0.250 | 0 | Sí |
| H3: R² / Brier / clima / AUC | −0.0336 / 0.0899 / 0.0819 / 0.7092 | −0.034 / 0.0900 / 0.0819 / 0.709 | 0.0001 | Sí |
| H3 sin 2025 (orígenes a 2024-02): R² | 0.0048 | 0.005 | 0 | Sí |
| H4: meses invertidos / racha / máx. P | 27 / 534 / 0.713 (2023-05) | 27 / 534 / 0.712 (2023-05) | 0.001 | Sí |
| P actual (S de 2026-08): tiempo real / coef. 1959-94 | 0.105 / 0.124 | 0.105 / 0.124 | 0 | Sí |
| H5: inicios / media 12 m / t | 2019-**06**; 3.01% / −1.68 | 2019-**05**; 3.91% / −1.55 | +0.90 pp; +0.13 | Sí (mismo veredicto) |
| H6 elegida, Sharpe dentro | `inv_fuera12` 0.6143 | `inv_fuera12` 0.620 | +0.006 | Sí |
| H6 `inv_fuera12` fuera: Sharpe / MDD / CAGR | 0.4331 / −46.06% / 7.15% | 0.418 / −46.6% / 6.86% | −0.015; −0.29 pp | Sí |
| Comprar y mantener fuera: Sharpe / MDD / CAGR | 0.5092 / −50.31% / 9.28% | 0.509 / −50.9% / 9.11% | 0.000; −0.17 pp | Sí |
| Comprar y mantener dentro: Sharpe / MDD | 0.4676 / −46.51% | 0.464 / −42.7% | −0.004; **+3.8 pp de MDD** | Sharpe sí; MDD distinta (fuente) |
| SMA10 fuera: Sharpe / MDD | 0.5881 / −19.31% | 0.554 / −22.9% | −0.034; −3.6 pp | Sharpe sí; MDD distinta (fuente) |
| `inv1` fuera: Sharpe / CAGR | 0.4899 / 8.54% | 0.463 / 7.98% | −0.027; −0.56 pp | Sí |
| `desinv12` fuera: Sharpe / MDD | 0.5521 / −41.62% | 0.560 / −41.8% | +0.008 | Sí |
| DSR `inv_fuera12` fuera, N = 8 / 16 | 0.9728 / 0.9685 | 0.964 / 0.958 | −0.01 | Sí (contra 0 en las dos) |
| MXN fuera: `inv_fuera12` / comprar y mantener / SMA10, CAGR (MDD) | 9.85% (−29.62%) / 12.04% (−39.86%) / 10.93% (−24.01%) | 9.56% (−27.2%) / 11.86% (−40.1%) / 10.43% (−31.1%) | ≤ 0.5 pp; MDD de SMA10 −7 pp | CAGR sí; MDD de SMA10 distinta (fuente) |
| Veredictos H1 / H2 / H3 / H4 / H5 / H6 / freno | Repl. / Repl. / refutada / falso positivo / se sostiene / refutada / no refutado | iguales | — | **Concordante** |

### Explicación de las diferencias

1. **El código no es la causa.** El control C (código de B con el spread GS10 − BEY(TB3MS) y los rendimientos y la RF de French 202607) reproduce la tabla de H6 de A a cuatro decimales: `inv_fuera12` 0.6143 / 0.4331 / −46.06%, comprar y mantener 0.4676 / 0.5092 / −50.31%, SMA10 0.4123 / 0.5881 / −19.31%, `inv1` fuera 0.4899, `probit50` dentro 0.6097, y H5 3.01% con t −1.69. Toda diferencia viene de los datos.
2. **Parte A (probit): sin diferencias.** El promedio de los datos diarios DGS10 y DTB3 (BEY día por día) difiere del GS10 y TB3MS de A en menos de 0.01 pp por mes. El tramo 1959-1961 con la serie de la OCDE no mueve nada: usar solo fuentes diarias desde 1962T1 da 0.302 con k = 4. La tabla trimestral oficial del NBER produce los mismos trimestres que `USRECQ` en 1959-1995: n, β y R² coinciden. B confirma así que las diferencias de A contra el artículo en k = 5 (0.279 contra 0.155) y k = 1 (0.041 contra 0.072) no son de código ni de fuente de tasas.
3. **Un mes de señal: 2019-05.** S_B = −0.005 y S_A = +0.00. En B, la inversión de 2019 empieza en 2019-05, y no en 2019-06. Eso explica el inicio distinto de H5 y la mayor parte de la diferencia de `inv_fuera12` e `inv1` fuera de muestra. Con S_B y French, `inv_fuera12` da 0.4163 y `inv1` 0.4748; con S_A y French, 0.4331 y 0.4899. Es la misma fragilidad cerca de cero que A documenta para jun-ago 2025 (S contra T10Y3M).
4. **S&P 500 TR contra CRSP.** Pesa ≤ 0.015 de Sharpe en las reglas de curva, pero explica la caída de la SMA10 fuera de muestra (0.588 → 0.554; mismo mecanismo de cruces al filo que AC-09) y las MDD distintas: comprar y mantener dentro, −42.7% contra −46.5% (1973-74, peor en el mercado amplio), y SMA10 fuera, −22.9% contra −19.3%. Con S_A y S&P, `inv_fuera12` fuera da 0.4350 (A: 0.4331). `probit50` dentro da 0.604 en B contra 0.6097 en A. Con S_B y French da 0.598, porque un mes, 1979-02, cae del otro lado de P = 0.5. El S&P lo compensa en parte.
5. **DSR (0.964 contra 0.973) y efectivo.** B usa DTB3 (3 meses) como efectivo y A la T-bill a 1 mes de French. Además, el DSR de B usa su propia fórmula (Bailey-López de Prado, con V de los 8 Sharpe fuera de muestra). Las dos cifras quedan ≥ 0.95 contra cero y por debajo de comprar y mantener: la lectura de A ("el DSR alto no valida la regla") se sostiene.

## Veredicto de la auditoría

- **Estado pre-registrado: concordante, "Replicado".** H1 (0.287, t −4.72) y H2 (0.294) caen en la tolerancia en A y en B, con cifras iguales a tres decimales.
- **Después de la publicación: concordante.** H3 queda refutada en las dos ejecuciones (pseudo R² −0.034; Brier 0.0900 contra 0.0819). H4 es falso positivo a la fecha. H5 se sostiene (t −1.68 y −1.55). H6 queda refutada: `inv_fuera12` tiene 0.433 y 0.418 contra 0.509 de comprar y mantener, no supera a la SMA10, y su uso como freno no se refuta.
- **Diferencias fuera de tolerancia:** ninguna en Sharpe, CAGR o pseudo R². Solo difieren las MDD de comprar y mantener dentro de muestra y de la SMA10 fuera (3.6-3.8 pp, 7 pp en MXN), por la serie S&P contra CRSP, y la fecha de inicio de la inversión de 2019, por un mes con spread de −0.005. Ningún criterio cambia.
- **Estado de la doble ejecución: Replicado (confirmado).**
- **La etiqueta de R07 se sostiene: descartada.** La curva sola no da un pronóstico calibrado después de 1998 y salir del mercado por la curva no mejora el Sharpe fuera de muestra, con dos fuentes y dos códigos.
