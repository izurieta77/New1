# V01. Verificación independiente: momentum (MOM) y rentabilidad (RMW)

> Fecha: 25-sep-2026. Estado: **Replicado** en lo estadístico (factor académico). **No** es una estrategia operable en GBM.
> Reproducir desde la raíz del repo: `python3 laboratorio/replicas/V01-momentum-y-rentabilidad/reproducir.py`. No usa red: los datos están congelados en `datos/` y sus huellas en `SHA256SUMS.txt`.

## Por qué existe

Revisamos dos cifras aportadas por otros sistemas antes de usarlas:

1. El factor MOM de Kenneth French pagó 0.80%/mes entre 1984 y 2006 y casi nada después (reportado en el LAB-003 de ChatGPT).
2. RMW (empresas muy rentables menos poco rentables) paga ~4.5% anual desde 2000 y es significativo (reportado por otro rival).

Regla del sistema: no se usa ninguna cifra ajena sin verificarla con datos y código propios.

## Datos

- **Fuente:** Kenneth French Data Library, archivos `F-F_Momentum_Factor_CSV.zip` y `F-F_Research_Data_5_Factors_2x3_CSV.zip`, versión "CRSP 202607".
- **Huella del zip de momentum:** `7ee14e89…`. Es idéntica a la del paquete del rival, así que ambos usamos la misma versión de los datos.
- **Qué son estas series:** diferenciales largo-corto académicos de EUA, **sin costos**, antes de impuestos y en USD.

## Método

- **Inferencia:** media mensual, error estándar Newey-West con 6 rezagos (kernel de Bartlett y corrección n/(n−1)) e intervalo de confianza al 95%, calculados con `herramientas/estadistica.py`.
- **Doble implementación del error estándar:** la suma de autocovarianzas se comparó contra la matriz de Bartlett completa (`herramientas/tests/test_estadistica.py`).
- **Veredicto pre-definido:** "apoyo" si el límite inferior del intervalo es mayor que 0, "contraria" si el límite superior es menor que 0, "inconcluso" en cualquier otro caso.

## Resultados

| Factor | Ventana | n (meses) | Media %/mes | ×12 (no es CAGR) | t NW(6) | IC 95% | Veredicto |
|---|---|---|---|---|---|---|---|
| MOM | 1984-01 a 2006-09 | 273 | 0.798 | 9.58% | 3.37 | [0.335, 1.262] | apoyo |
| MOM | 2006-10 a 2025-12 | 231 | 0.088 | 1.06% | 0.26 | [−0.566, 0.742] | inconcluso |
| MOM | 2006-10 a 2015-12 | 111 | 0.152 | 1.82% | 0.25 | [−1.051, 1.355] | inconcluso |
| MOM | 2016-01 a 2025-12 | 120 | 0.029 | 0.34% | 0.09 | [−0.578, 0.635] | inconcluso |
| RMW | 1963-07 a 1999-12 | 438 | 0.173 | 2.07% | 1.90 | [−0.005, 0.351] | inconcluso |
| RMW | 2000-01 a 2025-12 | 312 | 0.397 | 4.76% | 2.43 | [0.076, 0.717] | apoyo |
| RMW | 2015-01 a 2025-12 | 132 | 0.274 | 3.29% | 1.59 | [−0.064, 0.611] | inconcluso |
| RMW | 2016-01 a 2025-12 | 120 | 0.296 | 3.55% | 1.57 | [−0.074, 0.666] | inconcluso |

Con la serie hasta julio de 2026, RMW desde 2000 da 4.48% anual y t = 2.28. Eso implica que en 2026 el factor ha tenido meses negativos.

## Conclusiones permitidas

- **MOM:** las cifras publicadas por el rival se reproducen exactamente, con la misma media, la misma t y el mismo intervalo. Desde octubre de 2006 no hay evidencia estadística de una media positiva del factor MOM de EUA. Eso **no prueba** que el efecto haya desaparecido: el intervalo es amplio.
- **RMW:** se **confirma** que desde 2000 paga ~4.5–4.8% anual con significancia (t ≈ 2.3–2.4). **Matiz decisivo:** después de su publicación (Fama-French, 2015) baja a ~3.3–3.6% anual y **deja de ser significativo** (t ≈ 1.6). Antes de 2000 también fue débil.

## Conclusiones que NO se sostienen

- Que momentum o rentabilidad sean estrategias rentables en GBM. Estas series son largo-corto, sin costos y en USD, y con 20,000 MXN no se puede ir en corto.
- Que RMW sea una ventaja segura hacia adelante. La evidencia posterior a su publicación es inconclusa.
- Que una media multiplicada por 12 sea un CAGR o la riqueza que obtendría un inversionista.

## Siguiente prueba (pendiente)

1. Momentum y rentabilidad **fuera de EUA** con los factores internacionales de French (Developed, Europe, Japan, Asia Pacific ex Japan y Emerging), antes y después de su publicación.
2. **Versiones implementables** vía ETFs disponibles en el SIC (por ejemplo, ETFs de momentum y de calidad frente al mercado), en MXN y con costos de GBM.
3. Doble ejecución independiente de este archivo por el subagente `auditor-de-replicas`.
