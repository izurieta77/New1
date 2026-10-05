# AC-12: doble ejecución independiente (ciega) de R03 (decaimiento post-publicación McLean-Pontiff, crashes de Mom, "muerte del value")

> Fase 0, formación. Nada de esto es una recomendación de inversión. Cifras históricas, brutas, en USD, de factores largo-corto no invertibles en GBM.

| Campo | Valor |
|---|---|
| Réplica auditada (A) | `laboratorio/replicas/R03-primas-de-factores-pre-post-publicacion.md` (corrida 2026-09-25 05:56 UTC, French CRSP 202607) |
| Ejecución independiente (B) | `AC12.py` (Python 3.11, solo stdlib). De `herramientas/` usa únicamente `datos_historicos.french` para leer los zip; además un lector CSV propio verifica cada valor (dif. < 1e-12). Tramos, regresión agrupada con EE por mes, Newey-West, bootstrap de bloques, H1, H4 y H5 están escritos desde cero. No importa ni copia `R03.py` |
| Fecha | 2026-10-05 (descarga 17:49 UTC; `datos/descarga_utc.txt`) |
| Comando | `python3 laboratorio/auditorias/AC-12-R03/AC12.py` (sin red, ~25 s) → `salida.txt`, `resultados.json` |
| Semilla | 20261005 (A usó 20260925). 5,000 repeticiones, bloques móviles de 12 meses calendario |
| sha256 | `AC12.py` final `7e721afb…a7c`; versión ciega `aaf2bde3…1053`. `salida_ciega.txt` `a48129a2…049f` |

## Datos (dos vías)

| Vintage | Origen | Archivo | sha256 |
|---|---|---|---|
| **202608** (vía B principal) | descarga directa de `mba.tuck.dartmouth.edu/.../ftp/` el 2026-10-05 | F-F_Research_Data_Factors_CSV.zip | `593f4fbef03181bc0b22ff6292f217689dd1fb79355049ca905d95b262040a66` |
| | | F-F_Momentum_Factor_CSV.zip | `c06d1c2e9a5e4f6985879722f23c6bb585f46b34eaf3fcb681d4de887e353f3e` |
| | | F-F_Research_Data_5_Factors_2x3_CSV.zip | `36756c5c2559648519ac4b22913d860c6afd865cfebce920e3e8927f8e2d10b7` |
| **202607** (control, igual que A) | copias locales del repo (R01-datos/202607, C06/datos) | Factors / Momentum / 5F 2x3 | `b840dba5…f5eb` / `7ee14e89…e065` / `b8653b41…7c65807` |

Las dos vintages se recortan a 2026-07 (fin del pre-registro). Los conteos IS/OOS/POST (480/63/544, 330/18/409, 300/39/400, 606/16/135) se verifican en el script. No se reprodujo H6 (motor y archivo diario): queda fuera del alcance de esta auditoría.

## Protocolo ciego

1. De la ficha R03 leí solo el encabezado y las secciones 1 a 9. La línea "Estado" del encabezado decía "Pendiente", así que no anticipaba el veredicto.
2. Escribí `AC12.py`, lo corrí y guardé `salida_ciega.txt` (2026-10-05 17:51 UTC).
3. Después leí `R03-salida.txt` y la sección 16 de la ficha. No abrí `R03.py`. Agregué al script solo la función `conciliacion()`, que **anexa** líneas al final. Se verificó con `diff` que las primeras líneas de `salida.txt` son idénticas a `salida_ciega.txt`.

## Comparación A vs B

| Cifra | A (R03, 202607, semilla 20260925) | B 202607 | B 202608 | Dif. |
|---|---|---|---|---|
| b₂ (ee agrupado) | −0.6808 (0.3682) | −0.6808 (0.3682) | −0.6807 (0.3682) | 0 |
| **D = −b₂** | **68.1%** | **68.08%** | 68.07% | 0 |
| b₁ (ee) | 2.6832 (1.0034) | 2.6832 (1.0034) | idem | 0 |
| IC95 de D (bootstrap) | [−174.3%, 287.9%] | [−171.4%, 297.4%] | idem | +2.9 / +9.5 pp (ver 1) |
| Promedio simple de decaimientos | 64.8% | 64.83% | 64.84% | 0 |
| Decaimiento SMB / HML / Mom / RMW / CMA | 90.5 / 57.5 / 52.6 / 15.1 / 108.4% | 90.5 / 57.5 / 52.6 / 15.1 / 108.4% | 90.5 / 57.5 / 52.6 / 15.0 / 108.6% | ≤ 0.2 pp |
| IC SMB | [−511.0, 695.3] | [−480.8, 685.5] | idem | ver 1 |
| IC HML | [−143.9, 164.8] | [−124.6, 166.3] | idem | ver 1 |
| IC Mom | [−24.0, 112.4] | [−23.4, 117.5] | idem | ver 1 |
| IC RMW | [−393.8, 167.6] | [−444.0, 172.2] | idem | ver 1 |
| IC CMA | [−55.5, 288.7] | [−66.1, 296.3] | idem | ver 1 |
| Frac. rep. media IS ≤ 0 (SMB) | 0.1352 → no informativo | 0.1434 → no informativo | idem | ver 1 |
| Medias IS / POST (%/mes) | 0.157/0.015; 0.425/0.181; 0.821/0.389; 0.268/0.228; 0.324/−0.027 | idénticas | CMA post −0.028 | ≤ 0.001 pp |
| t NW de la media POST | 0.13 / 0.93 / 1.60 / 1.23 / −0.13 | 0.13 / 0.93 / 1.61 / 1.23 / −0.13 | — | Mom 0.01 (redondeo) |
| Δ POST−IS (t NW) | CMA −0.352 (−1.48) | −0.352 (−1.49) | — | 0.01 en t |
| Condición A | se cumple (0 fallas t; 4/4 magnitud con 5F) | igual | igual | 0 |
| H1 SMB (t iid IS) | 1.22 (no) | 1.22 (no) | 1.22 | 0 |
| Sens. SMB/HML 5F: D, IC | 66.1% [−95.5, 214.6] | — | 66.1% [−82.3, 225.3] | ver 1 |
| Sens. sin SMB: D, IC | 56.8% [−59.9, 122.9] | — | 56.8% [−58.0, 126.6] | ver 1 |
| Sens. fechas alternativas: D | 62.3% | — | 62.3% | 0 |
| H4 (1927-01..2026-07): oso / mkt mes > 0 / coinc. DM | 12/15, 14/15, 9/15 | 12, 14, 9 | 12, 14, 9 | 0 |
| H4 ventana DM | 13/15, 15/15, 10/15 | 13, 15, 10 | 13, 15, 10 | 0 |
| H4(d) Mom oso vs normal | −0.775% vs 0.877% (n 986) | −0.775% vs 0.883% (n 1004) | idem | 0.006 pp (ver 2) |
| H4 veredicto | confirmada | confirmada | confirmada | — |
| H5 HML 3F: pico→valle, DD | 2006-12→2020-09, −57.8% | idem | idem | 0 |
| H5 media 2007-2020 | −0.443%/mes | −0.443 | −0.443 | 0 |
| H5 valle→2026-07 / bajo el pico | +66.8% / −29.6% | +66.8 / −29.6 | +66.8 / −29.6 | 0 |
| H5 veredicto | confirmada | confirmada | confirmada | — |
| Peor mes Mom 2026-07 | −12.25% (mkt −0.27%) | −12.25 | −12.20 (mkt −0.28) | revisión de vintage (ver 3) |
| **Estado según la regla** | **Replicado con diferencias** | **Replicado con diferencias** | **Replicado con diferencias** | — |

### Diferencias explicadas

1. **Límites de los IC bootstrap (único grupo de diferencias > 0.5 pp).** Las estimaciones puntuales coinciden a 4 decimales; solo cambian los percentiles. Hay dos causas, y ninguna es un error:
   - **Semilla.** Con el panel de B, el IC de D cambia según la semilla: inferior entre −166% y −213%, superior entre 273% y 315% (6 semillas, bloque `[CONCILIACION]`). La diferencia A−B (3 y 9.5 pp) cae dentro de ese ruido de Monte Carlo. Esto pasa porque la razón r/media_IS explota cuando la media IS remuestreada de SMB se acerca a 0.
   - **Panel remuestreado.** A remuestrea 1201 meses calendario (1926-07..2026-07, incluyendo la pre-muestra sin tramo). B remuestra los 1087 meses que tienen tramo (1936-01..2026-07). El pre-registro solo dice "todo el panel". Con el panel de A, B obtiene [−157.7%, 271.7%] y P(IS SMB ≤ 0) = 0.132, contra 0.135 de A. En los IC por factor la variación es del mismo orden; el más sensible es RMW, con 135 meses POST y un IS que es pequeño frente a la volatilidad del bloque.
   - Ningún IC cambia de lado respecto a 0 ni a 0.58. Todos contienen ambos valores, salvo los de los factores individuales, que también contienen 0.
2. **H4(d), media de Mom en meses "normales": 0.883% contra 0.877%.** En la versión ciega, B contó como "normales" los 18 meses de 1927-01 a 1928-06, que no tienen 24 meses de mercado previo (el pre-registro, sección 5, dice "sin 24 meses, oso = falso"). A excluye esos meses de esta comparación. Con la ventana de A, B reproduce 0.877% y n = 986. El signo y el veredicto no cambian.
3. **Vintage 202608 contra 202607.** French revisa la historia en cada versión. Entre las dos vintages, las cifras de 1936-2026 cambian como máximo 0.001 pp/mes en las medias (CMA POST) y 0.05 pp en el último mes (Mom 2026-07). D cambia en 0.0001. **El resultado es robusto al vintage.**
4. Las demás cifras (t NW, Δ con t NW) difieren en 0.01 en t, por redondeo o por la convención del estimador NW (la de B: Bartlett con 6 rezagos y autocovarianzas divididas entre n).

## Conclusión

- **¿Coincide el estado "Replicado con diferencias"? Sí.**
  - A y B (en las dos vintages) cumplen la condición A.
  - D = 68.1% > 0 y los cinco factores tienen media POST < media IS.
  - El IC 95% de D incluye 0 con cualquier semilla o panel probado, en A y en B, así que no puede ser "Replicado".
  - D > 0 y A falla para 0 factores, así que tampoco es "No replicado".
  - La regla "rige la más conservadora de A y B" da **Replicado con diferencias** sin degradación.
- **H4 confirmada y H5 confirmada**, idénticas en A y en B. H6 no se auditó.
- Sensibilidad sin SMB (t IS < 2): D = 56.8% con IC [−58%, 127%]. También incluye 0. El 58% de McLean-Pontiff es compatible con los datos, pero el decaimiento no es estadísticamente distinto de 0 con cinco factores.
- **Etiqueta propuesta: descartada** como fuente de ventaja operable.
  - Después de publicarse, ningún factor tiene t NW ≥ 2 (de −0.13 a 1.61).
  - Los factores requieren cortos y apalancamiento que GBM no permite en fase 1.
  - El decaimiento en sí es un hallazgo descriptivo replicado con diferencias: apoya recortar μ, pero no es una oportunidad.
