# AC-04: efecto Halloween, segunda ejecución independiente de R04

Estado: COMPLETADA (2026-09-25). Veredicto: **no concordante en el estado** (A: Replicado; B: Replicado con diferencias). El código concuerda; la discrepancia es de fuente de datos. Las secciones 1 y 2 se escribieron el 2026-09-25, antes de calcular cualquier rendimiento. Para escribirlas solo se leyó el pre-registro de R04 (secciones 1 a 9 de `laboratorio/replicas/R04-efecto-halloween.md`). No se leyeron `R04.py`, `R04-salida.txt`, `R04-resultados.json`, `R04-variantes.csv` ni las secciones 10 a 17 de la ficha.

## 1. Pregunta

¿La ejecución B, escrita desde cero con **otras fuentes de datos**, reproduce las conclusiones de R04 (ejecución A) sobre el efecto Halloween de Bouman y Jacobsen (2002, AER 92(5), 1618-1635)? Se aplican los mismos criterios (i) a (iv) del pre-registro de R04.

## 2. Especificación de B (fijada antes de calcular)

### 2.1 Fuentes

| Uso | Serie | Construcción |
|---|---|---|
| EUA, dentro de muestra (1926-07 a 1998-08 y 1926-07 a 2002-12) | Shiller, `ie_data.xls` (Yale, http://www.econ.yale.edu/~shiller/data/ie_data.xls), hoja `Data` | R_t = (P_t + D_t/12)/P_{t-1} − 1. P es el **promedio mensual** de cierres diarios del S&P Composite y D el dividendo anualizado (interpolado). El xls se lee con un lector OLE2/BIFF8 escrito con la biblioteca estándar |
| EUA, fuera de muestra (2003-01 a 2026-07) | Yahoo `^SP500TR` (S&P 500 Total Return), diario | Último cierre de cada mes; R_t = C_t/C_{t-1} − 1. Existe desde 1988, así que también se reporta 1988-02 a 1998-08 como contraste de la fuente |
| EUA, contraste de fuente | Shiller, fuera de muestra hasta el último mes con dividendo | Solo diagnóstico |
| México, principal | Yahoo `^MXX`, diario, índice de **precio** en MXN | Último cierre de cada mes. Ventanas 1991-12 a 2002-12 y 2003-01 a 2026-07 |
| México, segunda fuente | Yahoo `EWW` (iShares MSCI Mexico), `adjclose` diario, USD, con dividendos | Último cierre ajustado de cada mes. Ventanas 1996-05 a 2002-12 y 2003-01 a 2026-07 |
| Efectivo EUA | FRED `TB3MS` (% anual) | rf_t = TB3MS_t/1200 |
| Efectivo MXN | FRED `INTGSTMXM193N` (% anual) | rf_t = tasa_t/1200 (A usa días/360; aquí se usa /12 a propósito) |

Se usan diarios de Yahoo y no barras `1mo`, porque las barras mensuales de `^SP500TR` tienen huecos (156 barras desde 1988).

### 2.2 Estadística

- y_t = 100·ln(1 + R_t); S_t = 1 en noviembre a abril.
- MCO de y_t = μ + α₁·S_t. t MCO clásica y t Newey-West (Bartlett, 12 rezagos, corrección n/(n−2)).
- D_y (suma de nov_{y−1} a abr_y menos suma de may_y a oct_y, años completos dentro de la ventana): media, t e IC bootstrap de 95% (10,000 remuestreos iid, semilla 4, generador propio `random.Random`).
- "Significativo fuera de muestra" = t NW ≥ 2 **y** IC de D_y que excluye cero (igual que R04).

### 2.3 Estrategia (2003-01 a 2026-07)

- w_t = 1 en noviembre a abril, 0 en mayo a octubre. En w = 0 se gana rf_t.
- Costo de 0.34% (0.29% + 0.05%) por lado sobre |w_t − w_{t−1}|, cargado en el mes t. Se carga la compra inicial (w_{2002-12} = 0) tanto a la estrategia como a comprar y mantener; no hay liquidación final.
- Métricas: CAGR, volatilidad anual, Sharpe = media(R − rf)/sd·√12 con rendimientos simples netos, MDD de la riqueza a fin de mes y número de operaciones.
- Casos: EUA `^SP500TR` + TB3MS (USD); México `^MXX` + CETES (MXN); México `EWW` + TB3MS (USD).

### 2.4 Criterio de concordancia A contra B

- **Concordante** si B llega al mismo estado de R04 con la regla (i) a (iv), si los signos de α₁ coinciden en cada ventana común y si ninguna diferencia de significancia cambia una conclusión. Diferencias de magnitud se explican (fuente, promedios de Shiller, dividendos, CETES), pero no invalidan la concordancia salvo que crucen un umbral de los criterios.
- **No concordante** si el estado cambia o si un signo fuera de muestra cambia.

(Las secciones 3 en adelante se escribieron después de correr `AC04.py`; los números de B quedaron en `salida.txt` antes de leer los resultados de A.)

### 2.5 Adenda 1 (2026-09-25, después de ver las regresiones con Shiller y antes de leer cualquier resultado de A)

Con Shiller, α₁ de 1970-01 a 1998-08 sale en 0.62 (t MCO 1.63), lejos de 1.03. Sospecha concreta: el P de Shiller es un **promedio mensual** de cierres diarios, no el cierre de fin de mes. El promedio reparte cada choque entre dos meses; por ejemplo, la caída de octubre de 1987 pasa en parte a noviembre, que es mes de invierno. Además induce autocorrelación. Se agregan tres corridas, **solo como diagnóstico de la fuente**. El resultado principal de B sigue siendo el de 2.1 y no se cambia el estado por ellas:

1. **Híbrido fin de mes:** Yahoo `^GSPC` diario (último cierre del mes, desde donde exista, idealmente 1927-12) más el dividendo de Shiller/12: R_t = (P^fin_t + D_t/12)/P^fin_{t−1} − 1. Ventanas 1970-01 a 1998-08 y (inicio disponible) a 2002-12.
2. **French Mkt-RF + RF** (misma fuente que A, código de B). Separa las diferencias de código de las de datos.
3. Shiller solo precio promedio (ya incluido): aísla el efecto de los dividendos.

## 3. Fuentes exactas (consultadas el 2026-09-25)

| Serie | URL | Rango usado / disponible | sha256[:16] |
|---|---|---|---|
| Shiller `ie_data.xls`, hoja `Data` (P promedio mensual y D anualizado) | http://www.econ.yale.edu/~shiller/data/ie_data.xls (guardado por última vez el 2023-09-17) | 1871-01 a 2023-09 (D hasta 2023-06) | `0df9392b7dacf91f` |
| Yahoo `^SP500TR` diario | query1.finance.yahoo.com/v8/finance/chart, `period1=-1400000000`, `interval=1d` | 1988-01-04 a 2026-09-21 | `ced106288d62655e` |
| Yahoo `^GSPC` diario (híbrido de la adenda 1) | ídem | 1927-12-30 a 2026-09-21 | `e4cbff828f17bc27` |
| Yahoo `^MXX` diario | ídem | 1991-11-08 a 2026-09-21 | `ee0819c58ba5101f` |
| Yahoo `EWW` diario (`adjclose`) | ídem | 1996-03-18 a 2026-09-21 | `4df5ead50c25a2fa` |
| FRED `TB3MS` | fred.stlouisfed.org/graph/fredgraph.csv?id=TB3MS | 1934-01 a 2026-08 | `ebf04b1ae5bc5729` |
| FRED `INTGSTMXM193N` | ídem | 1986-10 a 2026-07 | `6ffbf4e5f6682a53` |
| French `F-F_Research_Data_Factors_CSV.zip` (solo diagnóstico, la fuente de A) | mba.tuck.dartmouth.edu | 1926-07 a 2026-07 | ver `salida.txt` |

- El xls de Shiller se leyó con un lector OLE2/BIFF8 propio (biblioteca estándar). El archivo de Yale ya no se actualiza: termina en 2023-09. Por eso el tramo fuera de muestra de EUA usa `^SP500TR`.
- Con `range=max`, Yahoo baja la granularidad a 3 meses. Se usó `period1/period2` para obtener diarios.
- Los datos crudos quedan en `datos/`. `python3 AC04.py --sin-red` reproduce todo sin red.

## 4. Resultados de B (`salida.txt`)

Regresión y = 100·ln(1+R) sobre S (nov-abr), % log mensual:

| Ventana | Fuente | n | α₁ | t MCO | t NW12 |
|---|---|---|---|---|---|
| 1970-01 a 1998-08 | Shiller (principal) | 344 | 0.6187 | 1.63 | 1.49 |
| 1970-01 a 1998-08 | Híbrido `^GSPC` fin de mes + D Shiller (diag.) | 344 | 0.9699 | 2.03 | 2.44 |
| 1926-07 a 2002-12 | Shiller (principal) | 918 | 0.3912 | 1.29 | 1.20 |
| 1928-01 a 2002-12 | Híbrido (diag.) | 900 | 0.5080 | 1.35 | 1.53 |
| 2003-01 a 2026-07 | `^SP500TR` (principal) | 283 | 0.2767 | 0.55 | 0.71 |
| 2003-01 a 2023-06 | Shiller | 246 | 0.4297 | 0.90 | 1.01 |
| México 1991-12 a 2002-12 | `^MXX` | 133 | 2.2850 | 1.45 | 1.54 |
| México 2003-01 a 2026-07 | `^MXX` | 283 | 0.7063 | 1.27 | 1.60 |
| México 1996-05 a 2002-12 | `EWW` (USD, con dividendos) | 80 | 4.8049 | 2.15 | 2.72 |
| México 2003-01 a 2026-07 | `EWW` | 283 | 1.1349 | 1.35 | 1.62 |

D_y fuera de muestra (IC bootstrap de 95%): `^SP500TR` 2.19 [−2.92, 7.14]; `^MXX` 4.86 [−0.75, 10.60]; `EWW` 7.09 [−2.95, 16.76]. Ninguno excluye el cero y ninguna t NW llega a 2: **mismo signo, no significativo** en los tres.

Estrategia 2003-01 a 2026-07, neta de 0.34% por lado:

| Caso | Regla | CAGR | Vol | Sharpe | MDD | Operaciones |
|---|---|---|---|---|---|---|
| EUA `^SP500TR`/TB3MS | nov-abr | 6.73% | 10.45% | 0.512 | −30.87% | 48 |
| | comprar y mantener | 11.58% | 14.49% | 0.714 | −50.95% | 1 |
| México `^MXX`/CETES | nov-abr | 10.11% | 12.02% | 0.337 | −21.66% | 48 |
| | comprar y mantener | 10.65% | 16.15% | 0.316 | −44.48% | 1 |
| México `EWW`/TB3MS (USD) | nov-abr | 8.89% | 17.15% | 0.487 | −39.26% | 48 |
| | comprar y mantener | 10.32% | 23.66% | 0.468 | −61.22% | 1 |

Criterios de R04 con las fuentes principales de B: (i) NO se cumple (0.62, a 0.42 pp de 1.0349, t 1.63); (ii) NO se cumple (t NW 1.20); (iii) sí; (iv) sí. **Estado B: Replicado con diferencias.** Con el híbrido de fin de mes, (i) sí se cumpliría (0.97, t MCO 2.03) y (ii) seguiría sin cumplirse (t NW 1.53). El estado sería el mismo.

## 5. Comparación A contra B

| Cifra | A (R04, French/`^MXX`) | B principal | B diag. French (código B) | Diferencia y causa |
|---|---|---|---|---|
| α₁ EUA 1970-01 a 1998-08 (t MCO) | 1.0377 (2.09) | 0.6187 (1.63) Shiller; 0.9699 (2.03) híbrido | 1.0377 (2.09) | **Fuente.** El P de Shiller es un promedio mensual: octubre de 1987 queda en −12.1% en octubre y −12.6% en noviembre (fin de mes: −21.5% y −8.2%). Pasa la caída a invierno y baja α₁ en ~0.35 pp. Con cierres de fin de mes la brecha baja a 0.07 pp (S&P 500 contra CRSP total) |
| α₁ EUA 1926-07 a 2002-12 (t NW) | 0.6819 (2.07) | 0.3912 (1.20); híbrido 1928-01: 0.5080 (1.53) | 0.6819 (2.07); French 1928-01: 0.686 (2.04) | **Fuente, tramo 1928-1969.** 1970-2002 es casi igual (híbrido 1.02, t NW 2.81; French 1.105, t NW 2.68). En 1928-1969, el S&P (90 acciones antes de 1957) con dividendos de Shiller da α₁ 0.11 y CRSP 0.36. La t de A (2.07) está justo en el umbral de 2 y no resiste el cambio de índice |
| α₁ EUA 2003-01 a 2026-07 (t NW) | 0.2886 (0.70) | 0.2767 (0.71) `^SP500TR` | 0.2886 (0.70) | < 0.02 pp: S&P 500 contra CRSP total. Concuerda |
| D_y EUA fuera de muestra, IC95 | 2.394 [−3.059, 7.500] | 2.19 [−2.92, 7.14] | 2.39 [−2.82, 7.59] | Media igual con French. El IC difiere por el generador de bootstrap (semilla 4 en otro RNG) |
| α₁ México 1991-12 a 2002-12 y 2003-01 a 2026-07 | 2.2850 (1.54); 0.7063 (1.60) | idénticos | — | Misma serie `^MXX` y mismo cálculo. Segunda fuente EWW: 1.13 (t NW 1.62), mismo signo, mayor por dividendos y tipo de cambio |
| Estrategia EUA nov-abr: CAGR / vol / Sharpe / MDD | 6.87% / 10.79% / 0.516 / −30.32% | 6.73% / 10.45% / 0.512 / −30.87% | 6.88% / 10.80% / 0.512 / −30.44% | Todas < 0.2 pp y < 0.01 de Sharpe. Causas: S&P 500 contra CRSP; TB3MS contra RF de French; B carga la compra inicial |
| EUA comprar y mantener | 11.83% / 14.95% / 0.715 / −50.31% | 11.58% / 14.49% / 0.714 / −50.95% | 11.82% / 14.95% / 0.711 / −50.31% | Ídem |
| México nov-abr | 10.20% / 12.01% / 0.3356 / −21.66% | 10.11% / 12.02% / 0.337 / −21.66% | — | CETES: A usa días/360 y B /12; B carga la compra inicial. < 0.1 pp |
| México comprar y mantener | 10.67% / 16.15% / 0.3115 / −44.48% | 10.65% / 16.15% / 0.316 / −44.48% | — | Ídem |
| Operaciones nov-abr | ~1.99 por año | 48 en 283 meses (incluye la entrada inicial) | 48 | Concuerda |
| Estado | Replicado | Replicado con diferencias | Replicado (con los datos de A) | **Fuente**: (i) y (ii) dependen de CRSP |

**Lectura:**

- El código de A es correcto. Con los mismos datos (French), B reproduce α₁, t y métricas de estrategia de A hasta el cuarto decimal o dentro de 0.01 de Sharpe.
- Las conclusiones fuera de muestra concuerdan en todo:
  - Mismo signo y no significativo en EUA y México.
  - En EUA la estrategia pierde contra comprar y mantener en CAGR y Sharpe, y gana en MDD.
  - En México gana en Sharpe y MDD por poco y pierde en CAGR. Con EWW (USD) pasa lo mismo.
- La diferencia está en la muestra histórica de EUA. La condición (ii) de A (t NW 2.07) es frágil: con un índice S&P de fin de mes y dividendos de Shiller baja a 1.53. La diferencia viene de 1928-1969. La condición (i) falla con Shiller, pero es un artefacto de los precios promedio; con cierres de fin de mes sí se cumple.

## 6. Veredicto

**No concordante en el estado, por la regla fijada en 2.4:** A = Replicado, B = Replicado con diferencias. La causa es la fuente de datos, no el código. Concordante en todo lo operable y fuera de muestra: efecto de mismo signo y no significativo; no le gana a comprar y mantener en EUA; en México solo mejora el riesgo. Recomendación para R04: pasar a **"Replicado con diferencias"**. El criterio (ii) solo se cumple con CRSP/French y no resiste un índice alternativo.

## 7. Límites

- Shiller no es una fuente de fin de mes (promedios mensuales, dividendos interpolados) y termina en 2023. El híbrido mezcla el precio de Yahoo con el dividendo de Shiller y empieza en 1928-01, no en 1926-07.
- `^SP500TR` y `^GSPC` son índices de 500 (antes de 1957, 90) acciones grandes. CRSP es el mercado total. No hay una segunda fuente de mercado total independiente de CRSP antes de 1988 con la biblioteca estándar.
- México usa la misma serie `^MXX` que A (índice de precio, sin dividendos). La segunda fuente (EWW) está en USD, así que mezcla el efecto del tipo de cambio.
- La adenda 1 (híbrido y French) se decidió después de ver el primer resultado de Shiller, aunque antes de leer A. Es diagnóstico y no cambia el estado de B.
- El bootstrap usa `random.Random(4)`, que no es el mismo generador que A: los IC difieren en ~0.2.
- No se replicaron: modelos II y Maberly-Pierce, winsorización, placebo, SMA10, variantes, DSR ni sensibilidades de costo.
