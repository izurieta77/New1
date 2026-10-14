# AC-18-R13: ejecución B independiente de R13 (devengos, Sloan 1996)

- **Auditor:** `auditor-de-replicas` (ejecución B). Fecha: 2026-10-14 (UTC).
- **Independencia:** solo se leyó el pre-registro (§1-9) de `laboratorio/replicas/R13-devengos-sloan.md`. No se leyeron `R13.py` ni `R13-salida.txt`. Código propio: `b.py` (stdlib; `python3 -I b.py`). Salida completa: `salida.txt`.

## 1. Fuentes (segunda construcción de la señal, distinta de French)

| Archivo (en `datos/`) | Origen | Descargado | sha256 |
|---|---|---|---|
| PredictorAltPorts_DecilesVW.zip | OSAP, Drive id `1_1WWZqilrt1gleeyAFwjv5aobd0QRbS3` | 2026-10-14 17:51 UTC | d1790e831b621069379d5584d3114292ac52e8cdc36e44e302e880bd0c972b7c |
| PredictorAltPorts_DecilesEW.zip | OSAP, id `1pFBX0LTyoSwH7i8mT4kPCS_3QghlbODD` | ídem | b49364d5ddaa3ffa789b67b0757e3e38bc4291473510751593cae3273e5ee103 |
| PredictorAltPorts_QuintilesVW.zip | OSAP, id `1ef905SSlCDyh1KU9W1tJs5sfBFz0HPUt` | ídem | 03c2358f223670b6ce21853f2f9d86404012f6cea9a14e76d116ca05f20d5070 |
| PredictorAltPorts_QuintilesEW.zip | OSAP, id `1KjptjrRi96ko_tR8zFjXCyYfNlyiHGiI` | ídem | 2be3c54459f5de8ee1bf4a474b9a3ea7a74cb3d37b8c690ade0dff773b77a0c6 |
| PredictorPortsFull.csv (construcción del artículo original, chequeo) | OSAP, id `1g7w-yQ6Cg2qbMEkER9Q3vgns4JszXQo6` | 17:50 UTC | 6cdaf0ff051222b813e6f8404d7a30b94e146b421625f202bd04473fe97a1817 |
| PredictorLSretWide.csv (no se usa en los cálculos) | OSAP, id `10sOryk_ddjkXagaajTKUk1nwJs2ZLRiI` | 17:50 UTC | 79aa0896d79924e1efa83f9afe51a3b4ce94137adfd2c5c3fd2d5d350532ee18 |
| SignalDoc.csv (definición de la señal) | OSAP, id `1Sev9s6cPFUGgxp1pFiej0lGzpsMqJCI2` | 17:50 UTC | 590a308e40483fa87c0cbb95f73c010d09a61e22a3e2059627d2b3de9b77e0d9 |
| F-F_Research_Data_5_Factors_2x3_CSV.zip | mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/ | 17:51 UTC | 36756c5c2559648519ac4b22913d860c6afd865cfebce920e3e8927f8e2d10b7 |
| Portfolios_Formed_on_AC_CSV.zip (cotejo: misma fuente que A, código independiente) | ídem | 17:51 UTC | 6710cd881e625f48b39d48d4cf77cb11a6deef3e67e4b091551289b9005a413e |

URL de descarga de Drive: `https://drive.usercontent.google.com/download?id=<id>&export=download&confirm=t`. Página índice: https://www.openassetpricing.com/data/

- **Versión OSAP:** release de octubre de 2025 (v2.0.0, primera generada con código Python). Portafolios de 1952-07 a **2024-12**.
- **French:** archivos generados con CRSP 202608. AC de 1963-07 a **2026-08**.
- **Señal OSAP "Accruals"** (SignalDoc): textualmente, según SignalDoc: "Δact − Δche − Δlct − Δdlc − Δtxp, dividido entre el promedio de at de este año y el anterior; excluye abs(prc) < 5". Es decir, devengos de balance escalados por activos totales promedio, como en Sloan. No verifiqué en el código de OSAP los signos de dlc y txp. En el artículo original: EW, deciles, mantenimiento de 12 meses y arranque en junio. Diferencias frente a Sloan: OSAP no resta la depreciación. Frente a French: este divide AC/B entre el capital contable y no aplica filtro de precio.
- **Orientación (verificada con los datos):** OSAP guarda la señal firmada (Sign = −1, por lo que `signallag` = −devengos). El puerto 10 (5 en quintiles) es el de devengos **bajos**, y `LS` = p10 − p01 (máx. |dif| ≈ 1e-13 en los 5 archivos). Por eso Lo−Hi = p10 − p01 (p05 − p01 en quintiles). *Nota de transparencia:* mi primera corrida tomó p01 − p10 y dio signos invertidos. El chequeo contra la columna LS lo detectó y lo corregí antes del veredicto.
- **Faltantes** (−99.99, −999 o NA) en las series usadas: 0.
- **Correlación mensual** del Lo−Hi VW de deciles entre OSAP y French (1963-07 a 2024-12): **0.40**. Son construcciones bastante distintas.

## 2. Resultados (largo-corto Lo−Hi, % mensual, bruto; t NW con 6 rezagos y pesos de Bartlett)

| Serie | Media pre 63-07..96-06 | t / t NW | Media post 96-07..fin | t / t NW | Caída | 2001+ media (t NW) | Veredicto §2 |
|---|---|---|---|---|---|---|---|
| **OSAP VW deciles (principal B)**, fin 2024-12 | **0.488** | 2.95 / **3.10** | **0.107** | 0.59 / **0.59** | **78.0%** | 0.024 (0.13) | **Replicado** |
| OSAP EW deciles | 0.666 | 7.05 / 6.23 | 0.103 | 1.04 / 0.89 | 84.6% | −0.004 (−0.04) | Replicado |
| OSAP VW quintiles | 0.265 | 2.08 / 2.02 | 0.159 | 1.02 / 1.00 | 40.1% | 0.168 (1.14) | Con diferencias (caída < 50%) |
| OSAP EW quintiles | 0.456 | 6.01 / 4.97 | 0.084 | 1.03 / 0.85 | 81.5% | 0.016 (0.16) | Replicado |
| French VW deciles (cotejo), fin 2026-08 | 0.414 | 3.15 / 3.30 | 0.163 | 0.96 / 0.93 | 60.6% | 0.062 (0.34) | Replicado |
| French VW deciles, periodo común hasta 2024-12 | 0.414 | 3.15 / 3.30 | 0.146 | 0.86 / 0.81 | 64.7% | 0.034 (0.18) | Replicado |
| French EW deciles, fin 2026-08 | 0.416 | 5.28 / 4.91 | 0.266 | 2.37 / 1.96 | 36.0% | 0.181 (1.28) | Con diferencias |
| French VW quintiles, fin 2026-08 | 0.382 | 3.58 / 3.62 | 0.167 | 1.23 / 1.20 | 56.3% | 0.109 (0.80) | Replicado |
| French EW quintiles, fin 2026-08 | 0.368 | 5.89 / 5.19 | 0.211 | 2.52 / 2.09 | 42.7% | 0.139 (1.34) | Con diferencias |

**Con un costo de 1% anual** (0.0833 pp al mes), principal OSAP: pre 0.405 (t NW 2.57) y post 0.024 (t NW 0.13), con 2001+ en −0.059. French VW deciles: pre 0.331 (2.63) y post 0.080 (0.45).

**Alfas de la principal OSAP (VW deciles), % mensual (t NW6):**

| Tramo | α CAPM | α FF5 |
|---|---|---|
| 1963-07..1996-06 | 0.621 (4.30), β = −0.29 | 0.439 (2.83) |
| 1996-07..2024-12 | 0.066 (0.34) | 0.170 (0.91) |
| 2001-01..2024-12 | −0.024 (−0.13) | 0.075 (0.39) |

French VW deciles: α CAPM pre 0.472 (3.80) y post 0.178 (1.04); α FF5 pre 0.445 (3.64) y post 0.118 (0.69).

**Comparación simple (Mkt−RF):** pre 0.467 (t NW 2.05). Post hasta 2024-12: 0.725 (2.88). Post hasta 2026-08: 0.749 (3.12).

## 3. Veredicto (criterio del §2, serie principal VW Lo10−Hi10)

- **H1 se sostiene en ambas fuentes:** OSAP 0.488%/mes con t NW 3.10; French 0.414% con t NW 3.30.
- **H2 se sostiene en ambas:** caída de 78% en OSAP y de 61% en French (65% en el periodo común). La media posterior no es significativa (t NW 0.59 y 0.93).
- **Estado B: Replicado.** Las conclusiones no dependen de la fuente. Dos construcciones distintas de la señal, con correlación mensual de solo 0.40, llevan al mismo veredicto en la serie principal.
- **Matices (variantes, no cambian el veredicto):**
  - La caída es menor a 50% en OSAP VW quintiles (40%), French EW deciles (36%) y French EW quintiles (43%). Las dos variantes EW de French conservan t ≈ 2 después de 1996, y en el periodo común hasta 2024-12 superan 2.0. La anomalía sobrevive más en las ponderadas por igual, es decir, en las acciones pequeñas.
  - En OSAP, la versión VW de quintiles apenas pasa H1 (t NW 2.02).
  - Desde 2001, ninguna serie VW tiene media significativa, y la principal es negativa una vez descontado el costo.
