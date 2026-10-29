# AC-29-R22 — Ejecución B independiente de R22 (pronóstico de la tasa efectiva trimestral)

> Auditoría del 29-oct-2026. Fase 0: no recomienda inversiones. Ejecución B con código propio
> (`ac29_r22.py`, solo biblioteca estándar). Leí únicamente el PRE-REGISTRO de
> `laboratorio/replicas/R22-tasa-efectiva-pronostico.md`; `R22.py` y `R22-resultados.json` los abrí
> **después** de tener mis cifras. No modifiqué archivos de A.

## 1. Método (construcción distinta de A)
| Aspecto | A (`R22.py`) | B (`ac29_r22.py`) |
|---|---|---|
| CIK | `herramientas/edgar.cik_de_ticker` | buscador de entidades de efts.sec.gov (coincidencia exacta del ticker; respaldo con la consulta en minúsculas, porque `keysTyped=GE` devolvía error del servidor) |
| Endpoint | companyconcept, un concepto por solicitud | companyfacts completo (`data.sec.gov/api/xbrl/companyfacts/CIK##########.json`) |
| XOM | CIK de la nueva tenedora (sin historia) | tenedora 2115436 **+** predecesora Exxon Mobil Corp 34088, hechos unidos |
| Utilidad antes de impuestos | de 3 etiquetas (incluye `...Domestic`), gana **una** sola: la de más trimestres | 4 etiquetas (sin `...Domestic`, que solo es la parte doméstica; se agregan `IncomeLossBeforeIncomeTaxes` y `IncomeLossFromContinuingOperationsBeforeIncomeTaxes`); por fecha de fin manda la de más trimestres y las demás **rellenan huecos** |
| Trimestre | duración de 80 a 100 días, gana el último presentado | igual (desempate por `filed` y luego `accn`); fechas de impuesto y utilidad emparejadas a ±5 días |
| 4T | fuera | variante sin 4T (comparable con A) y variante con 4T = anual 10-K (350-380 d) − 9 meses acumulados con el mismo inicio (245-290 d), solo si no hay 4T directo |
| Filtro, objetivos y ventanas | según el pre-registro | iguales: utilidad > 0 y 0 ≤ ETR ≤ 60% (en objetivo e historia); fin entre 2022-01-01 y 2026-09-30; ≥4 válidos en los 460 días previos (se usan los 4 más recientes); ≥8 en 830 días para mediana-8 |
| Prueba de signos | aproximación normal | binomial exacta, dos colas |
| IC de la diferencia de MAE | bootstrap iid, 4000 réplicas | bootstrap iid, 10 000 réplicas (semilla 20261029) + bootstrap por emisora (conglomerados, 2000) |

Fuentes: solo data.sec.gov y efts.sec.gov, User-Agent `SistemaInversionNew1/1.0 investigacion` (sin correo), ≤ ~7 solicitudes/s. Los datos crudos se guardan en `datos/` (en .gitignore).
Universo: 49 emisoras con mercado = US sin BRK-B ni SPCX. Sin objetivos válidos: PG (no etiqueta la utilidad antes de impuestos trimestral en us-gaap), ORCL (dejó de etiquetarla en 2018), INTC, UBER, CRWD y SNDK (pérdidas o ETR fuera del filtro, o historia corta). Ninguna emisora mexicana tiene XBRL: el resultado **no** se transfiere a ellas.

## 2. Resultados de B
### 2a. Sin 4T (comparable con A): 307 objetivos, 43 emisoras
| Regla | n | MAE (pp) | Mediana del error absoluto (pp) | Error de UPA medio, \|Δτ\|/(1−τ) | Error de UPA mediano |
|---|---|---|---|---|---|
| Último trimestre | 307 | 3.535 | 2.201 | 4.47% | 2.72% |
| **Mediana de 4** | 307 | **2.987** | 2.014 | 3.80% | 2.43% |
| Media de 4 | 307 | 3.145 | 2.113 | 3.97% | 2.53% |
| Mediana de 8 | 5 | 2.981 | 3.465 | 3.66% | 4.28% |
| 21% fijo | 307 | 5.787 | 4.602 | 6.99% | 5.68% |

- Signos: la mediana de 4 gana en 174, el último en 133, sin empates; p = 0.0223 (binomial exacta, dos colas).
- Diferencia de MAE (último − mediana de 4) = 0.548 pp; IC95 iid [0.199, 0.929]; IC95 por emisora [0.195, 0.964].
- Mediana de 8: solo 5 objetivos sin 4T (casi nunca hay 8 trimestres en 830 días cuando faltan los 4T).
- **Veredicto literal:** H1 **se cumple** (2.987 < 3.535 y p = 0.022 < 0.05). H2 **se cumple** (2.987 ≤ 3.0), aunque por solo **0.013 pp**.

### 2b. Con 4T reconstruido: 657 objetivos, 45 emisoras (142 de ellos son 4T)
| Regla | n | MAE (pp) | Mediana del error absoluto (pp) | Error de UPA medio |
|---|---|---|---|---|
| Último trimestre | 657 | 4.833 | 2.885 | 6.38% |
| **Mediana de 4** | 657 | **3.589** | 2.109 | 4.82% |
| Media de 4 | 657 | 3.778 | 2.226 | 5.02% |
| Mediana de 8 | 570 | 3.477 | 2.079 | 4.74% |
| 21% fijo | 657 | 6.437 | 5.159 | 8.04% |

- Signos: 400 contra 257, p = 2.7e-8. Diferencia de MAE = 1.244 pp; IC95 iid [0.902, 1.612]; por emisora [0.848, 1.664].
- En los 142 objetivos 4T: MAE del último 5.42, de la mediana de 4 4.27, de la media de 4 4.32, del 21% 7.38. Fuera de los 4T (515 objetivos), la mediana de 4 ronda 3.40 pp (por diferencia de agregados): el 4T, que trae los ajustes anuales de impuestos, también ensucia la historia.
- En la submuestra de mediana de 8 (n = 570): mediana de 4 3.401, mediana de 8 3.477. La mediana de 8 **no** mejora a la de 4.
- **Veredicto:** H1 se cumple con holgura; H2 **no** se cumple (3.59 > 3.0).

## 3. Comparación con A
| Medida | A | B sin 4T | Δ (B − A) | B con 4T |
|---|---|---|---|---|
| Emisoras / objetivos | 29 / 194 | 43 / 307 | +14 / +113 | 45 / 657 |
| MAE último (pp) | 3.406 | 3.535 | +0.129 | 4.833 |
| MAE mediana de 4 (pp) | 3.029 | 2.987 | **−0.042** (dentro de ±0.3) | 3.589 |
| MAE media de 4 (pp) | 3.196 | 3.145 | −0.051 | 3.778 |
| MAE mediana de 8 (pp), n | 2.981 (5) | 2.981 (5) | 0 | 3.477 (570) |
| MAE 21% (pp) | 5.676 | 5.787 | +0.111 | 6.437 |
| Mediana del error abs., mediana de 4 | 2.319 | 2.014 | −0.305 | 2.109 |
| Signos (gana mediana 4 / gana último) | 109 / 85 | 174 / 133 | — | 400 / 257 |
| p de signos (dos colas) | 0.085 (normal) | 0.022 (exacta) | — | 2.7e-8 |
| IC95 de la diferencia de MAE | [0.004, 0.760] | [0.199, 0.929] | — | [0.902, 1.612] |
| Error de UPA medio, mediana de 4 | 3.88% | 3.80% | −0.08 | 4.82% |
| H1 | **no** | **sí** | discrepa | sí |
| H2 | **no** (3.029) | **sí** (2.987) | discrepa | no |

### Explicación de las diferencias
1. **Universo efectivo: 14 emisoras que A pierde (causa de casi todo).**
   - **11 emisoras por la regla "gana la etiqueta de serie más larga":** WMT, HD, JNJ, ABBV, UNH, GOOGL, NFLX, V, NVDA, MSFT y AMAT etiquetaron `...MinorityInterestAndIncomeLossFromEquityMethodInvestments` hasta mediados de 2021 (unos 40 trimestres) y después cambiaron a `...ExtraordinaryItemsNoncontrollingInterest` (unos 18). A se queda con la serie más larga, que **termina en 2021**, y por eso no tiene ningún objetivo de 2022 en adelante. Con TMO pasa lo contrario: la serie más larga es la de `...Extraordinary`, que termina en 2021-10. Es un defecto de construcción de A, no una decisión del pre-registro: el pre-registro dice "gana la de serie más larga", pero esa serie no cubre el periodo objetivo.
   - **GE:** `cik_de_ticker` falla ("Ticker GE no encontrado"). En efts, la consulta exacta `GE` también da error del servidor; B la resuelve con la consulta en minúsculas (CIK 40545).
   - **XOM:** el ticker apunta hoy a ExxonMobil Holdings Corp (CIK 2115436, con solo 2 trimestres). B une sus hechos con los de la predecesora Exxon Mobil Corp (CIK 34088).
   - **MA:** con la regla de A se usa una serie que termina en 2024-09, lo que da 6 objetivos; B, al rellenar huecos, obtiene 10.
2. **Prueba de que el cálculo de A es correcto dado su universo:** al emular en mi propia tubería la regla de A (una sola etiqueta de su lista, sin rellenar), en sus 29 emisoras obtengo **194 objetivos y MAE de 3.4063 / 3.0294 / 3.1959 / 2.9808 / 5.6761, con signos 109/85**: idéntico a A al tercer decimal. Las diferencias no vienen de la alineación, del filtro ni de las ventanas.
3. **Con los datos de B en las mismas 29 emisoras** (198 objetivos, con MA rellenada): mediana de 4 3.013, último 3.358, signos 110/88, p = 0.135, H1 no, H2 no. Es decir, en el universo de A los dos veredictos también fallan. Las 14 emisoras recuperadas (109 objetivos: mediana de 4 2.939, último 3.855) son las que mueven H1 y H2.
4. **p de signos:** A usa la aproximación normal (0.085) y B la binomial exacta; con 109/85 la exacta da 0.098. Ambas son mayores que 0.05, así que esto no cambia ningún veredicto.
5. **Mediana del error absoluto (−0.305 pp):** se explica por el cambio de muestra (las 14 emisoras recuperadas son grandes y de tasa estable).
6. **4T reconstruido:** agrega 142 objetivos 4T y habilita más objetivos de 1T y 3T (antes, sin el 4T, solo quedaban 3 trimestres en los 460 días). Sube el MAE de todas las reglas y hace que H2 falle. A no lo tiene por diseño (pre-registro: "Q4 queda fuera").

## 4. Estado propuesto
- **Criterio literal del pre-registro:** "Replicado" exige que B concuerde con A en H1 y H2, y que el MAE de la mediana de 4 quede a ±0.3 pp. El MAE concuerda (Δ = −0.042 pp), pero **H1 y H2 discrepan**, así que **no** es "Replicado".
- **Propuesta: "Replicado con diferencias"** (no "No replicado"). El cálculo de A se reproduce exactamente con su regla de etiquetas. La discrepancia de veredicto viene de un defecto de datos de A: pierde 14 de 43 emisoras con datos. Además, ambos veredictos están en el filo de su umbral: H2 por 0.013-0.029 pp y H1 con p entre 0.02 y 0.13 según el universo.
- **Lo robusto:** la mediana de 4 le gana al último trimestre en todas las variantes (diferencia de MAE de 0.35 a 1.24 pp, con IC95 > 0 en el universo corregido y con 4T). También le gana a la media de 4 y, por mucho, al 21% fijo.
- **Lo no robusto:** H2 (MAE ≤ 3.0 pp). Pasa por 0.013 pp sin 4T y falla con 4T (3.59 pp). No conviene tratar "≈3 pp" como una cota.
- **Recomendación para A:** cambiar "gana la de serie más larga" por una unión periodo a periodo (o "la de más trimestres dentro de la ventana objetivo"), quitar `...Domestic` de la lista y manejar XOM y GE. Corregir eso es una desviación del pre-registro y debe declararse como tal.

## 5. Reproducción (por resultados, no por hash)
`python3 -I laboratorio/auditorias/AC-29-R22/ac29_r22.py` descarga o lee `datos/` y escribe `resultados.json`. Cifras de control: sin 4T, 307 objetivos y 43 emisoras; MAE de la mediana de 4 2.987 y del último 3.535; signos 174/133. Con 4T, 657 objetivos y MAE de la mediana de 4 3.589. Emulación de A: 194 objetivos y MAE de la mediana de 4 3.029. Si la SEC agrega presentaciones nuevas o reexpresa cifras, los números pueden moverse en el tercer decimal.
