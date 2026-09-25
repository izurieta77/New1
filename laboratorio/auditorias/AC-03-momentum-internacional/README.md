# AC-03 — Momentum internacional (auditoria ciega)

Estado: COMPLETADA. Secciones 1-2 (especificacion) escritas antes de descargar y calcular; adenda 1
escrita antes de calcular; adenda 2 posterior y solo descriptiva.
Fecha de registro de la especificacion: 2026-09-25.
Auditor: agente auditor ciego. No se leyo ningun archivo de
`laboratorio/replicas/V01-momentum-y-rentabilidad/` ni cifras previas de momentum/RMW del repo.

## 1. Pregunta

Se afirma (afirmacion bajo auditoria, recibida como texto, sin ver su codigo):

- "Momentum en emergentes: 9.6% anual desde 2000 y 12.3% desde 2010."
- "Japon y Norteamerica: inconclusos."

Esta auditoria verifica si esas afirmaciones se sostienen con (A) los factores MOM/WML
regionales de Kenneth French, (B) una reconstruccion independiente a partir de los
portafolios 2x3 de tamano y momentum regionales de French, y (C) los factores UMD
regionales/por pais de AQR.

## 2. Especificacion (no se cambia despues de ver resultados; cambios = adenda fechada)

### 2.1 Series

- Fuente A: French, `<Region>_MOM_Factor` (CSV dentro de zip), columna WML, mensual, en %
  (rendimientos en USD, segun la Data Library). Regiones: Emerging, Developed_ex_US, Europe,
  Asia_Pacific_ex_Japan, Japan, North_America.
- Fuente B (reconstruccion): French, `<Region>_6_Portfolios_ME_Prior_12_2` (o el nombre
  equivalente de la Data Library), bloque de rendimientos mensuales ponderados por valor.
  WML reconstruido = 1/2 (Small High + Big High) - 1/2 (Small Low + Big Low).
  Minimo: Emerging, Europe, Japan; si estan disponibles, tambien las demas regiones de A.
  Se reporta ademas la diferencia contra A (media de la diferencia, correlacion, max |dif|).
- Fuente C (independiente): AQR, "Betting Against Beta: Equity Factors, Monthly" (hoja UMD),
  columnas por pais y regionales disponibles (Europe, Pacific, Global ex USA, Japon,
  Norteamerica si existe, y paises). Rendimientos en decimales -> se convierten a %.
  AQR no publica una serie "Emerging" en ese archivo (si la publicara, se usaria).
  Si una fuente no esta accesible, se documenta y se usa la siguiente.

### 2.2 Ventanas

- V1: 2000-01 a ultimo mes disponible en cada serie.
- V2: 2010-01 a ultimo mes disponible en cada serie.
- V3: 2016-01 a 2025-12.
Se usan solo meses con dato valido (se reportan n y meses faltantes). El "ultimo mes
disponible" se reporta por serie.

### 2.3 Estadisticos por ventana (r_t en % mensual)

- n
- media mensual (%)
- desviacion estandar muestral (n-1)
- t convencional IID = media / (sd / sqrt(n))
- t Newey-West con L = 6 rezagos, kernel de Bartlett w_j = 1 - j/(L+1),
  varianza de largo plazo S = gamma_0 + 2 sum_{j=1..L} w_j gamma_j con
  gamma_j = (1/n) sum (r_t - m)(r_{t-j} - m); correccion de muestra finita S * n/(n-1);
  EE_NW = sqrt(S * n/(n-1) / n); t_NW = media / EE_NW
- IC95 NW = media +/- 1.96 * EE_NW
- media x12 (aritmetica) — etiquetada "no es CAGR"
- rendimiento anual COMPUESTO = (prod(1 + r_t/100))^(12/n) - 1 — etiquetado
  "compuesto de la serie largo-corto; no es el rendimiento de una cuenta"
- peor mes y mejor mes (valor y fecha)

### 2.4 Veredicto por serie y ventana

- "apoyo" si limite inferior IC95 NW > 0
- "contraria" si limite superior IC95 NW < 0
- "inconcluso" en otro caso

### 2.5 Criterios para juzgar las afirmaciones

- "Emergentes 9.6% anual desde 2000 / 12.3% desde 2010": se compara contra media x12 y contra
  el compuesto de las series de emergentes (A y B; C no tiene emergentes). Se considera que la
  cifra "se reproduce" si la media x12 redondeada a 0.1 coincide (tolerancia +/- 0.15 pp); se
  reporta tambien si la cifra corresponde en realidad al compuesto. La afirmacion cualitativa
  (momentum emergente positivo y distinto de cero) se juzga por el veredicto NW.
- "Japon y Norteamerica inconclusos": se sostiene en una fuente si el veredicto NW es
  "inconcluso" para esa region en las ventanas V1 y V2 (se reporta V3 aparte).
  Para C, Japon = columna JPN; Norteamerica = no existe en AQR BAB como tal: se usara USA y
  CAN por separado (y se dira que no es la misma definicion).

### 2.6 Datos congelados y reproducibilidad

- Cada archivo descargado se guarda en `datos/` sin modificar; `datos/SHA256SUMS.txt` en
  formato `sha256sum`. Se registra la version/cabecera de cada archivo.
- `auditoria.py` (Python 3.11, solo biblioteca estandar; xlsx leido con zipfile +
  xml.etree) recalcula todo sin red desde `datos/` y escribe `resultados.json`.

### 2.7 Adenda 1 (2026-09-25, despues de descargar y ANTES de calcular cualquier estadistico)

Al inspeccionar solo cabeceras y rangos de fechas de los archivos descargados:

1. La hoja UMD de AQR SI tiene columna "North America" (ademas de USA y CAN). Por 2.1
   ("Norteamerica si existe") se usa "North America" como comparable de North_America de
   French; USA y CAN se reportan aparte como complemento. Esto sustituye la frase de 2.5 que
   suponia que no existia.
2. Los archivos de French (base "202608 Bloomberg") terminan en 2026-08; el archivo de AQR
   termina en 2026-07. Las ventanas V1/V2 terminan, por especificacion, en el ultimo mes de
   cada serie. Diagnostico adicional (no cambia veredictos): para comparar fuentes se reporta
   la media x12 de A, B y C sobre los meses comunes (interseccion de fechas) de cada par
   comparable, y las metricas de concordancia (correlacion mensual, media de la diferencia,
   max |dif|).
3. Diagnostico de sensibilidad del final de ventana (no cambia veredictos): para Emerging (A y B)
   se reporta media x12 y compuesto desde 2000-01 y 2010-01 terminando en 2025-12, 2026-07 y
   2026-08, para poder explicar una posible diferencia con las cifras afirmadas.
4. Pares comparables A/B vs C (definiciones no identicas): Europe-Europe, Japan-JPN,
   North_America-North America, Developed_ex_US-"Global Ex USA",
   Asia_Pacific_ex_Japan-"Pacific" (AQR Pacific incluye Japon; French no: NO equivalentes).

## 3. Fuentes y datos congelados (descargados el 2026-09-25)

| archivo en `datos/` | URL de origen | version / cabecera | rango mensual |
|---|---|---|---|
| `<Region>_MOM_Factor_CSV.zip` (6 archivos: Emerging, Developed_ex_US, Europe, Asia_Pacific_ex_Japan, Japan, North_America) | `https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/<Region>_MOM_Factor_CSV.zip` | "This file was created using the 202608 Bloomberg database." | Emerging 1990-01 a 2026-08; resto 1990-11 a 2026-08 |
| `<Region>_6_Portfolios_ME_Prior_12_2_CSV.zip` (6 archivos; para emergentes el nombre es `Emerging_Markets_6_Portfolios_ME_Prior_12_2_CSV.zip`) | `https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/<archivo>` (nombres tomados de `data_library.html`) | "This file was created using the 202608 Bloomberg database. It contains value- and equal-weighted returns for the intersections of 2 ME portfolios and 3 prior return portfolios ... Prior return is from -12 to - 2." | Emerging_Markets 1990-01 a 2026-08; resto 1990-11 a 2026-08 |
| `AQR_Betting-Against-Beta-Equity-Factors-Monthly.xlsx` (hoja `UMD`) | pagina `https://www.aqr.com/Insights/Datasets/Betting-Against-Beta-Equity-Factors-Monthly` -> `https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Betting-Against-Beta-Equity-Factors-Monthly.xlsx` | Sin sello de version en el archivo ("This file contains monthly self-financing returns of equity Up Minus Down (UMD) factors ... AQR reconstructs the full history each time the portfolios are updated."). Version = su SHA256 (`b98d9ce6...4514`) + ultimo mes 2026-07. | USA 1927-01; demas paises 1985-1996 segun columna; todos hasta 2026-07 |

Las sumas SHA256 completas estan en `datos/SHA256SUMS.txt`; `auditoria.py` las verifica antes de
calcular y aborta si alguna no coincide.

Fuentes no usadas: q-factors de Hou-Xue-Zhang (`global-q.org/factors.html`) — accesible, pero solo
publica factores de EUA y no tiene factor de momentum ni series internacionales, por lo que no
aplica a esta pregunta. No hay, entre las fuentes accesibles, una segunda fuente independiente de
momentum de emergentes: AQR BAB/UMD cubre solo mercados desarrollados (+ ISR).

Adenda 2 (2026-09-25, POST-resultados, solo descriptiva, no cambia ningun veredicto): se agregaron
correlaciones para documentar la composicion de los agregados AQR (seccion 5.4).

## 4. Resultados por fuente (salida exacta de `auditoria.py`, redondeada para la tabla)

Unidades: % mensual en USD. "media x12" = media aritmetica x12, NO es CAGR. "compuesto" =
(prod(1+r_t))^(12/n)-1 de la serie largo-corto; NO es el rendimiento de una cuenta (ignora costos,
financiamiento de la pata corta, restricciones de venta en corto, impuestos). t NW con 6 rezagos
Bartlett y correccion n/(n-1). Veredicto segun IC95 NW. Las ventanas V1/V2 de French terminan en
2026-08 y las de AQR en 2026-07 (ultimo mes de cada archivo).

#### Fuente A

| serie | V | periodo | n | media %/mes | DE | t IID | t NW(6) | IC95 NW %/mes | media x12 % (no es CAGR) | compuesto anual % (serie L-C; no es rendimiento de cuenta) | peor mes | mejor mes | veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A:Emerging | V1 | 2000-01–2026-08 | 320 | 0.799 | 3.10 | 4.60 | 4.21 | [0.427, 1.171] | 9.59 | 9.37 | -16.84 (2026-07) | 12.84 (2026-04) | apoyo |
| A:Emerging | V2 | 2010-01–2026-08 | 200 | 1.025 | 3.02 | 4.80 | 5.47 | [0.658, 1.391] | 12.30 | 12.40 | -16.84 (2026-07) | 12.84 (2026-04) | apoyo |
| A:Emerging | V3 | 2016-01–2025-12 | 120 | 0.860 | 2.52 | 3.74 | 3.76 | [0.412, 1.309] | 10.32 | 10.41 | -9.15 (2022-11) | 7.03 (2021-01) | apoyo |
| A:Developed_ex_US | V1 | 2000-01–2026-08 | 320 | 0.584 | 3.51 | 2.98 | 2.59 | [0.141, 1.028] | 7.01 | 6.43 | -22.52 (2009-04) | 10.06 (2000-02) | apoyo |
| A:Developed_ex_US | V2 | 2010-01–2026-08 | 200 | 0.708 | 2.73 | 3.67 | 4.22 | [0.379, 1.038] | 8.50 | 8.35 | -12.31 (2020-11) | 7.21 (2020-03) | apoyo |
| A:Developed_ex_US | V3 | 2016-01–2025-12 | 120 | 0.479 | 2.57 | 2.04 | 2.27 | [0.064, 0.893] | 5.75 | 5.48 | -12.31 (2020-11) | 7.21 (2020-03) | apoyo |
| A:Europe | V1 | 2000-01–2026-08 | 320 | 0.749 | 4.08 | 3.28 | 3.05 | [0.267, 1.230] | 8.99 | 8.25 | -26.09 (2009-04) | 13.65 (2002-09) | apoyo |
| A:Europe | V2 | 2010-01–2026-08 | 200 | 0.851 | 3.08 | 3.90 | 4.77 | [0.501, 1.200] | 10.21 | 10.06 | -18.39 (2020-11) | 8.94 (2012-04) | apoyo |
| A:Europe | V3 | 2016-01–2025-12 | 120 | 0.618 | 3.08 | 2.20 | 2.69 | [0.168, 1.067] | 7.41 | 7.05 | -18.39 (2020-11) | 8.50 (2019-05) | apoyo |
| A:Asia_Pacific_ex_Japan | V1 | 2000-01–2026-08 | 320 | 0.889 | 3.51 | 4.53 | 3.66 | [0.413, 1.365] | 10.67 | 10.38 | -18.03 (2009-05) | 7.99 (2013-04) | apoyo |
| A:Asia_Pacific_ex_Japan | V2 | 2010-01–2026-08 | 200 | 1.040 | 3.05 | 4.82 | 4.99 | [0.631, 1.448] | 12.48 | 12.60 | -8.37 (2020-11) | 7.99 (2013-04) | apoyo |
| A:Asia_Pacific_ex_Japan | V3 | 2016-01–2025-12 | 120 | 0.751 | 2.86 | 2.88 | 3.41 | [0.319, 1.183] | 9.02 | 8.87 | -8.37 (2020-11) | 7.65 (2020-07) | apoyo |
| A:Japan | V1 | 2000-01–2026-08 | 320 | -0.020 | 3.96 | -0.09 | -0.09 | [-0.481, 0.440] | -0.24 | -1.19 | -18.28 (2026-07) | 14.80 (2000-02) | inconcluso |
| A:Japan | V2 | 2010-01–2026-08 | 200 | 0.082 | 3.40 | 0.34 | 0.40 | [-0.324, 0.488] | 0.98 | 0.28 | -18.28 (2026-07) | 14.30 (2026-04) | inconcluso |
| A:Japan | V3 | 2016-01–2025-12 | 120 | -0.090 | 2.89 | -0.34 | -0.37 | [-0.570, 0.391] | -1.08 | -1.57 | -8.50 (2016-08) | 8.44 (2016-06) | inconcluso |
| A:North_America | V1 | 2000-01–2026-08 | 320 | 0.248 | 4.93 | 0.90 | 1.00 | [-0.239, 0.735] | 2.97 | 1.51 | -25.00 (2009-04) | 29.32 (2000-02) | inconcluso |
| A:North_America | V2 | 2010-01–2026-08 | 200 | 0.348 | 3.29 | 1.50 | 1.74 | [-0.044, 0.740] | 4.18 | 3.58 | -12.98 (2026-07) | 11.35 (2026-04) | inconcluso |
| A:North_America | V3 | 2016-01–2025-12 | 120 | 0.164 | 3.32 | 0.54 | 0.58 | [-0.389, 0.718] | 1.97 | 1.32 | -12.72 (2023-01) | 6.94 (2020-03) | inconcluso |

#### Fuente B

| serie | V | periodo | n | media %/mes | DE | t IID | t NW(6) | IC95 NW %/mes | media x12 % (no es CAGR) | compuesto anual % (serie L-C; no es rendimiento de cuenta) | peor mes | mejor mes | veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B:Emerging | V1 | 2000-01–2026-08 | 320 | 0.799 | 3.10 | 4.60 | 4.21 | [0.427, 1.170] | 9.58 | 9.37 | -16.84 (2026-07) | 12.84 (2026-04) | apoyo |
| B:Emerging | V2 | 2010-01–2026-08 | 200 | 1.024 | 3.02 | 4.79 | 5.48 | [0.658, 1.390] | 12.29 | 12.39 | -16.84 (2026-07) | 12.84 (2026-04) | apoyo |
| B:Emerging | V3 | 2016-01–2025-12 | 120 | 0.860 | 2.52 | 3.74 | 3.76 | [0.412, 1.309] | 10.32 | 10.41 | -9.15 (2022-11) | 7.02 (2021-01) | apoyo |
| B:Developed_ex_US | V1 | 2000-01–2026-08 | 320 | 0.583 | 3.51 | 2.97 | 2.58 | [0.140, 1.026] | 7.00 | 6.42 | -22.52 (2009-04) | 10.05 (2000-02) | apoyo |
| B:Developed_ex_US | V2 | 2010-01–2026-08 | 200 | 0.707 | 2.73 | 3.67 | 4.21 | [0.378, 1.036] | 8.49 | 8.34 | -12.31 (2020-11) | 7.21 (2020-03) | apoyo |
| B:Developed_ex_US | V3 | 2016-01–2025-12 | 120 | 0.478 | 2.57 | 2.04 | 2.26 | [0.064, 0.892] | 5.74 | 5.47 | -12.31 (2020-11) | 7.21 (2020-03) | apoyo |
| B:Europe | V1 | 2000-01–2026-08 | 320 | 0.749 | 4.08 | 3.28 | 3.05 | [0.267, 1.230] | 8.98 | 8.24 | -26.09 (2009-04) | 13.65 (2002-09) | apoyo |
| B:Europe | V2 | 2010-01–2026-08 | 200 | 0.850 | 3.08 | 3.90 | 4.77 | [0.501, 1.199] | 10.20 | 10.06 | -18.39 (2020-11) | 8.93 (2012-04) | apoyo |
| B:Europe | V3 | 2016-01–2025-12 | 120 | 0.617 | 3.08 | 2.20 | 2.69 | [0.168, 1.067] | 7.41 | 7.04 | -18.39 (2020-11) | 8.49 (2019-05) | apoyo |
| B:Asia_Pacific_ex_Japan | V1 | 2000-01–2026-08 | 320 | 0.888 | 3.51 | 4.53 | 3.65 | [0.412, 1.364] | 10.66 | 10.37 | -18.02 (2009-05) | 7.99 (2013-04) | apoyo |
| B:Asia_Pacific_ex_Japan | V2 | 2010-01–2026-08 | 200 | 1.039 | 3.05 | 4.82 | 4.99 | [0.631, 1.447] | 12.47 | 12.59 | -8.38 (2020-11) | 7.99 (2013-04) | apoyo |
| B:Asia_Pacific_ex_Japan | V3 | 2016-01–2025-12 | 120 | 0.750 | 2.86 | 2.88 | 3.41 | [0.319, 1.182] | 9.01 | 8.86 | -8.38 (2020-11) | 7.63 (2020-07) | apoyo |
| B:Japan | V1 | 2000-01–2026-08 | 320 | -0.021 | 3.96 | -0.09 | -0.09 | [-0.481, 0.439] | -0.25 | -1.20 | -18.27 (2026-07) | 14.79 (2000-02) | inconcluso |
| B:Japan | V2 | 2010-01–2026-08 | 200 | 0.082 | 3.40 | 0.34 | 0.39 | [-0.324, 0.487] | 0.98 | 0.28 | -18.27 (2026-07) | 14.29 (2026-04) | inconcluso |
| B:Japan | V3 | 2016-01–2025-12 | 120 | -0.090 | 2.89 | -0.34 | -0.37 | [-0.570, 0.390] | -1.08 | -1.57 | -8.49 (2016-08) | 8.43 (2016-06) | inconcluso |
| B:North_America | V1 | 2000-01–2026-08 | 320 | 0.247 | 4.92 | 0.90 | 1.00 | [-0.240, 0.734] | 2.97 | 1.50 | -25.00 (2009-04) | 29.32 (2000-02) | inconcluso |
| B:North_America | V2 | 2010-01–2026-08 | 200 | 0.348 | 3.29 | 1.50 | 1.74 | [-0.044, 0.740] | 4.17 | 3.58 | -12.97 (2026-07) | 11.36 (2026-04) | inconcluso |
| B:North_America | V3 | 2016-01–2025-12 | 120 | 0.165 | 3.32 | 0.54 | 0.58 | [-0.389, 0.718] | 1.98 | 1.32 | -12.72 (2023-01) | 6.95 (2020-03) | inconcluso |

#### Fuente C — agregados AQR y comparables directos

| serie | V | periodo | n | media %/mes | DE | t IID | t NW(6) | IC95 NW %/mes | media x12 % (no es CAGR) | compuesto anual % (serie L-C; no es rendimiento de cuenta) | peor mes | mejor mes | veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C:Global Ex USA | V1 | 2000-01–2026-07 | 319 | 0.838 | 3.61 | 4.15 | 3.50 | [0.369, 1.308] | 10.06 | 9.66 | -23.53 (2009-04) | 11.09 (2000-02) | apoyo |
| C:Global Ex USA | V2 | 2010-01–2026-07 | 199 | 0.953 | 2.64 | 5.10 | 5.82 | [0.632, 1.274] | 11.43 | 11.59 | -12.06 (2020-11) | 6.92 (2019-05) | apoyo |
| C:Global Ex USA | V3 | 2016-01–2025-12 | 120 | 0.721 | 2.57 | 3.07 | 3.50 | [0.317, 1.126] | 8.66 | 8.58 | -12.06 (2020-11) | 6.92 (2019-05) | apoyo |
| C:Europe | V1 | 2000-01–2026-07 | 319 | 1.006 | 4.22 | 4.26 | 3.85 | [0.494, 1.519] | 12.08 | 11.53 | -27.06 (2009-04) | 14.62 (2002-09) | apoyo |
| C:Europe | V2 | 2010-01–2026-07 | 199 | 1.123 | 2.93 | 5.41 | 6.66 | [0.792, 1.454] | 13.48 | 13.74 | -18.88 (2020-11) | 8.61 (2019-05) | apoyo |
| C:Europe | V3 | 2016-01–2025-12 | 120 | 0.855 | 2.99 | 3.13 | 3.98 | [0.433, 1.276] | 10.25 | 10.14 | -18.88 (2020-11) | 8.61 (2019-05) | apoyo |
| C:Pacific | V1 | 2000-01–2026-07 | 319 | 0.485 | 3.39 | 2.55 | 2.14 | [0.040, 0.929] | 5.81 | 5.23 | -17.47 (2009-04) | 11.42 (2000-02) | apoyo |
| C:Pacific | V2 | 2010-01–2026-07 | 199 | 0.617 | 2.78 | 3.13 | 3.38 | [0.260, 0.974] | 7.40 | 7.16 | -10.74 (2026-07) | 8.36 (2026-04) | apoyo |
| C:Pacific | V3 | 2016-01–2025-12 | 120 | 0.454 | 2.54 | 1.96 | 2.07 | [0.024, 0.883] | 5.44 | 5.18 | -7.46 (2024-09) | 7.84 (2024-01) | apoyo |
| C:JPN | V1 | 2000-01–2026-07 | 319 | 0.087 | 3.85 | 0.40 | 0.37 | [-0.369, 0.543] | 1.04 | 0.14 | -17.49 (2009-04) | 11.92 (2004-03) | inconcluso |
| C:JPN | V2 | 2010-01–2026-07 | 199 | 0.114 | 3.23 | 0.50 | 0.57 | [-0.278, 0.507] | 1.37 | 0.74 | -14.41 (2026-07) | 11.55 (2026-04) | inconcluso |
| C:JPN | V3 | 2016-01–2025-12 | 120 | -0.056 | 2.91 | -0.21 | -0.22 | [-0.544, 0.432] | -0.67 | -1.17 | -8.76 (2021-02) | 8.72 (2016-06) | inconcluso |
| C:North America | V1 | 2000-01–2026-07 | 319 | 0.343 | 5.01 | 1.22 | 1.22 | [-0.207, 0.893] | 4.12 | 2.54 | -34.16 (2009-04) | 16.65 (2000-02) | inconcluso |
| C:North America | V2 | 2010-01–2026-07 | 199 | 0.460 | 3.70 | 1.76 | 2.01 | [0.010, 0.909] | 5.52 | 4.78 | -16.88 (2020-11) | 10.77 (2015-07) | apoyo |
| C:North America | V3 | 2016-01–2025-12 | 120 | 0.110 | 3.89 | 0.31 | 0.35 | [-0.514, 0.734] | 1.32 | 0.39 | -16.88 (2020-11) | 8.48 (2019-05) | inconcluso |
| C:USA | V1 | 2000-01–2026-07 | 319 | 0.275 | 5.05 | 0.97 | 0.98 | [-0.272, 0.822] | 3.30 | 1.68 | -34.62 (2009-04) | 17.01 (2000-02) | inconcluso |
| C:USA | V2 | 2010-01–2026-07 | 199 | 0.386 | 3.70 | 1.47 | 1.69 | [-0.062, 0.833] | 4.63 | 3.86 | -16.77 (2020-11) | 10.40 (2015-07) | inconcluso |
| C:USA | V3 | 2016-01–2025-12 | 120 | 0.052 | 3.90 | 0.15 | 0.17 | [-0.570, 0.675] | 0.63 | -0.30 | -16.77 (2020-11) | 8.48 (2019-05) | inconcluso |
| C:CAN | V1 | 2000-01–2026-07 | 319 | 1.320 | 5.85 | 4.03 | 3.44 | [0.568, 2.072] | 15.84 | 14.63 | -29.32 (2009-04) | 22.57 (2001-02) | apoyo |
| C:CAN | V2 | 2010-01–2026-07 | 199 | 1.453 | 5.18 | 3.96 | 3.89 | [0.720, 2.186] | 17.44 | 17.02 | -19.00 (2020-11) | 16.05 (2015-07) | apoyo |
| C:CAN | V3 | 2016-01–2025-12 | 120 | 1.116 | 4.96 | 2.46 | 2.26 | [0.149, 2.083] | 13.39 | 12.56 | -19.00 (2020-11) | 12.76 (2020-03) | apoyo |
| C:Global | V1 | 2000-01–2026-07 | 319 | 0.551 | 4.17 | 2.36 | 2.24 | [0.069, 1.033] | 6.61 | 5.66 | -28.48 (2009-04) | 14.16 (2000-02) | apoyo |
| C:Global | V2 | 2010-01–2026-07 | 199 | 0.649 | 3.08 | 2.97 | 3.46 | [0.282, 1.016] | 7.78 | 7.45 | -14.72 (2020-11) | 7.77 (2019-05) | apoyo |
| C:Global | V3 | 2016-01–2025-12 | 120 | 0.337 | 3.18 | 1.16 | 1.32 | [-0.162, 0.837] | 4.05 | 3.48 | -14.72 (2020-11) | 7.77 (2019-05) | inconcluso |

#### Fuente C — paises AQR

| serie | V | periodo | n | media %/mes | DE | t IID | t NW(6) | IC95 NW %/mes | media x12 % (no es CAGR) | compuesto anual % (serie L-C; no es rendimiento de cuenta) | peor mes | mejor mes | veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C:AUS | V1 | 2000-01–2026-07 | 319 | 1.449 | 4.31 | 6.01 | 5.44 | [0.927, 1.971] | 17.39 | 17.54 | -17.19 (2000-04) | 14.79 (2013-04) | apoyo |
| C:AUS | V2 | 2010-01–2026-07 | 199 | 1.383 | 3.79 | 5.14 | 5.88 | [0.922, 1.843] | 16.59 | 16.92 | -13.48 (2020-11) | 14.79 (2013-04) | apoyo |
| C:AUS | V3 | 2016-01–2025-12 | 120 | 0.953 | 3.38 | 3.09 | 4.86 | [0.568, 1.338] | 11.44 | 11.30 | -13.48 (2020-11) | 9.28 (2020-03) | apoyo |
| C:AUT | V1 | 2000-01–2026-07 | 319 | 0.571 | 5.76 | 1.77 | 1.40 | [-0.230, 1.372] | 6.85 | 4.81 | -39.69 (2009-04) | 21.56 (2008-11) | inconcluso |
| C:AUT | V2 | 2010-01–2026-07 | 199 | 0.625 | 4.87 | 1.81 | 1.56 | [-0.160, 1.409] | 7.50 | 6.23 | -23.06 (2020-11) | 16.10 (2026-05) | inconcluso |
| C:AUT | V3 | 2016-01–2025-12 | 120 | -0.017 | 4.53 | -0.04 | -0.04 | [-0.944, 0.909] | -0.21 | -1.47 | -23.06 (2020-11) | 7.69 (2025-05) | inconcluso |
| C:BEL | V1 | 2000-01–2026-07 | 319 | 0.735 | 5.14 | 2.56 | 2.25 | [0.096, 1.375] | 8.83 | 7.42 | -30.98 (2009-04) | 19.34 (2008-10) | apoyo |
| C:BEL | V2 | 2010-01–2026-07 | 199 | 0.613 | 4.26 | 2.03 | 2.36 | [0.105, 1.122] | 7.36 | 6.44 | -19.03 (2020-11) | 12.80 (2012-04) | apoyo |
| C:BEL | V3 | 2016-01–2025-12 | 120 | 0.343 | 4.05 | 0.93 | 0.95 | [-0.366, 1.051] | 4.11 | 3.15 | -19.03 (2020-11) | 12.58 (2018-01) | inconcluso |
| C:CHE | V1 | 2000-01–2026-07 | 319 | 0.780 | 4.68 | 2.98 | 2.94 | [0.260, 1.300] | 9.36 | 8.32 | -25.28 (2009-04) | 22.69 (2001-09) | apoyo |
| C:CHE | V2 | 2010-01–2026-07 | 199 | 0.722 | 3.38 | 3.02 | 3.93 | [0.361, 1.082] | 8.66 | 8.27 | -16.67 (2020-11) | 9.47 (2020-03) | apoyo |
| C:CHE | V3 | 2016-01–2025-12 | 120 | 0.516 | 3.51 | 1.61 | 2.12 | [0.040, 0.993] | 6.19 | 5.58 | -16.67 (2020-11) | 9.47 (2020-03) | apoyo |
| C:DEU | V1 | 2000-01–2026-07 | 319 | 1.425 | 5.59 | 4.56 | 4.33 | [0.780, 2.071] | 17.10 | 16.30 | -23.21 (2009-08) | 26.89 (2008-10) | apoyo |
| C:DEU | V2 | 2010-01–2026-07 | 199 | 1.399 | 3.53 | 5.60 | 5.86 | [0.931, 1.866] | 16.79 | 17.27 | -15.15 (2020-11) | 11.29 (2026-01) | apoyo |
| C:DEU | V3 | 2016-01–2025-12 | 120 | 0.958 | 3.66 | 2.87 | 3.38 | [0.402, 1.515] | 11.50 | 11.23 | -15.15 (2020-11) | 11.13 (2019-05) | apoyo |
| C:DNK | V1 | 2000-01–2026-07 | 319 | 1.441 | 4.93 | 5.22 | 5.19 | [0.897, 1.986] | 17.30 | 17.03 | -22.25 (2009-04) | 14.15 (2022-04) | apoyo |
| C:DNK | V2 | 2010-01–2026-07 | 199 | 1.554 | 4.65 | 4.71 | 5.09 | [0.956, 2.152] | 18.65 | 18.82 | -14.63 (2022-05) | 14.15 (2022-04) | apoyo |
| C:DNK | V3 | 2016-01–2025-12 | 120 | 1.293 | 5.00 | 2.83 | 2.98 | [0.442, 2.144] | 15.51 | 14.97 | -14.63 (2022-05) | 14.15 (2022-04) | apoyo |
| C:ESP | V1 | 2000-01–2026-07 | 319 | 0.825 | 5.33 | 2.76 | 2.68 | [0.221, 1.428] | 9.90 | 8.42 | -28.87 (2020-11) | 14.89 (2020-07) | apoyo |
| C:ESP | V2 | 2010-01–2026-07 | 199 | 1.166 | 5.30 | 3.10 | 3.03 | [0.411, 1.920] | 13.99 | 12.96 | -28.87 (2020-11) | 14.89 (2020-07) | apoyo |
| C:ESP | V3 | 2016-01–2025-12 | 120 | 0.854 | 4.91 | 1.91 | 1.87 | [-0.040, 1.748] | 10.25 | 9.09 | -28.87 (2020-11) | 14.89 (2020-07) | inconcluso |
| C:FIN | V1 | 2000-01–2026-07 | 319 | 0.858 | 5.27 | 2.91 | 3.29 | [0.347, 1.370] | 10.30 | 9.00 | -19.06 (2001-10) | 26.09 (2001-08) | apoyo |
| C:FIN | V2 | 2010-01–2026-07 | 199 | 0.883 | 3.86 | 3.23 | 3.50 | [0.389, 1.378] | 10.60 | 10.16 | -10.09 (2026-07) | 13.10 (2012-04) | apoyo |
| C:FIN | V3 | 2016-01–2025-12 | 120 | 0.543 | 3.30 | 1.80 | 2.33 | [0.086, 1.000] | 6.51 | 6.03 | -8.20 (2025-07) | 11.84 (2019-05) | apoyo |
| C:FRA | V1 | 2000-01–2026-07 | 319 | 0.887 | 4.90 | 3.23 | 3.25 | [0.352, 1.421] | 10.64 | 9.56 | -26.67 (2009-04) | 20.66 (2002-09) | apoyo |
| C:FRA | V2 | 2010-01–2026-07 | 199 | 0.935 | 3.40 | 3.88 | 5.41 | [0.596, 1.274] | 11.22 | 11.03 | -21.28 (2020-11) | 8.00 (2019-05) | apoyo |
| C:FRA | V3 | 2016-01–2025-12 | 120 | 0.814 | 3.59 | 2.48 | 3.53 | [0.362, 1.266] | 9.76 | 9.34 | -21.28 (2020-11) | 8.00 (2019-05) | apoyo |
| C:GBR | V1 | 2000-01–2026-07 | 319 | 1.016 | 5.00 | 3.63 | 3.08 | [0.370, 1.662] | 12.19 | 11.11 | -34.19 (2009-04) | 12.46 (2000-02) | apoyo |
| C:GBR | V2 | 2010-01–2026-07 | 199 | 1.171 | 3.89 | 4.25 | 4.23 | [0.628, 1.714] | 14.06 | 13.92 | -26.21 (2020-11) | 10.85 (2020-07) | apoyo |
| C:GBR | V3 | 2016-01–2025-12 | 120 | 0.755 | 3.99 | 2.07 | 2.12 | [0.057, 1.453] | 9.06 | 8.34 | -26.21 (2020-11) | 10.85 (2020-07) | apoyo |
| C:GRC | V1 | 2000-01–2026-07 | 319 | 0.518 | 7.50 | 1.23 | 1.21 | [-0.321, 1.358] | 6.22 | 2.65 | -35.93 (2012-01) | 35.15 (2015-08) | inconcluso |
| C:GRC | V2 | 2010-01–2026-07 | 199 | 0.759 | 7.97 | 1.34 | 1.42 | [-0.289, 1.807] | 9.11 | 5.24 | -35.93 (2012-01) | 35.15 (2015-08) | inconcluso |
| C:GRC | V3 | 2016-01–2025-12 | 120 | 0.046 | 5.53 | 0.09 | 0.09 | [-0.930, 1.021] | 0.55 | -1.34 | -25.06 (2020-11) | 17.45 (2016-06) | inconcluso |
| C:HKG | V1 | 2000-01–2026-07 | 319 | 0.802 | 5.46 | 2.62 | 2.48 | [0.169, 1.435] | 9.63 | 8.02 | -28.43 (2009-05) | 20.72 (2000-02) | apoyo |
| C:HKG | V2 | 2010-01–2026-07 | 199 | 0.927 | 4.67 | 2.80 | 3.35 | [0.385, 1.470] | 11.13 | 10.22 | -22.09 (2024-09) | 12.07 (2024-01) | apoyo |
| C:HKG | V3 | 2016-01–2025-12 | 120 | 0.870 | 4.85 | 1.96 | 2.47 | [0.179, 1.561] | 10.44 | 9.34 | -22.09 (2024-09) | 12.07 (2024-01) | apoyo |
| C:IRL | V1 | 2000-01–2026-07 | 319 | 0.713 | 10.56 | 1.21 | 1.20 | [-0.453, 1.878] | 8.55 | 0.96 | -59.46 (2011-10) | 37.56 (2009-02) | inconcluso |
| C:IRL | V2 | 2010-01–2026-07 | 199 | 0.742 | 9.73 | 1.07 | 1.22 | [-0.452, 1.935] | 8.90 | 2.29 | -59.46 (2011-10) | 30.76 (2014-01) | inconcluso |
| C:IRL | V3 | 2016-01–2025-12 | 120 | -0.234 | 7.13 | -0.36 | -0.45 | [-1.263, 0.795] | -2.81 | -5.82 | -28.51 (2020-11) | 20.41 (2016-05) | inconcluso |
| C:ISR | V1 | 2000-01–2026-07 | 319 | 1.373 | 4.85 | 5.05 | 4.64 | [0.793, 1.952] | 16.47 | 16.10 | -24.66 (2009-04) | 13.00 (2008-06) | apoyo |
| C:ISR | V2 | 2010-01–2026-07 | 199 | 1.612 | 4.31 | 5.27 | 4.91 | [0.968, 2.255] | 19.34 | 19.82 | -18.62 (2020-11) | 12.10 (2017-08) | apoyo |
| C:ISR | V3 | 2016-01–2025-12 | 120 | 1.426 | 4.12 | 3.79 | 3.24 | [0.563, 2.289] | 17.11 | 17.33 | -18.62 (2020-11) | 12.10 (2017-08) | apoyo |
| C:ITA | V1 | 2000-01–2026-07 | 319 | 1.009 | 5.06 | 3.56 | 3.59 | [0.459, 1.560] | 12.11 | 11.09 | -21.12 (2009-03) | 20.09 (2000-02) | apoyo |
| C:ITA | V2 | 2010-01–2026-07 | 199 | 1.351 | 4.46 | 4.28 | 5.22 | [0.844, 1.858] | 16.21 | 16.09 | -18.88 (2020-11) | 14.89 (2010-11) | apoyo |
| C:ITA | V3 | 2016-01–2025-12 | 120 | 1.530 | 4.36 | 3.84 | 4.44 | [0.855, 2.204] | 18.36 | 18.63 | -18.88 (2020-11) | 12.68 (2016-06) | apoyo |
| C:NLD | V1 | 2000-01–2026-07 | 319 | 0.486 | 5.72 | 1.52 | 1.49 | [-0.153, 1.125] | 5.83 | 3.87 | -31.17 (2009-04) | 17.88 (2013-02) | inconcluso |
| C:NLD | V2 | 2010-01–2026-07 | 199 | 0.645 | 4.93 | 1.85 | 1.96 | [-0.000, 1.291] | 7.74 | 6.46 | -21.39 (2020-11) | 17.88 (2013-02) | inconcluso |
| C:NLD | V3 | 2016-01–2025-12 | 120 | 0.618 | 4.88 | 1.39 | 1.34 | [-0.286, 1.523] | 7.42 | 6.12 | -21.39 (2020-11) | 12.00 (2019-05) | inconcluso |
| C:NOR | V1 | 2000-01–2026-07 | 319 | 1.553 | 5.63 | 4.92 | 4.79 | [0.918, 2.189] | 18.64 | 18.08 | -22.44 (2001-11) | 20.12 (2002-12) | apoyo |
| C:NOR | V2 | 2010-01–2026-07 | 199 | 1.480 | 4.68 | 4.46 | 4.18 | [0.786, 2.174] | 17.76 | 17.73 | -19.98 (2020-11) | 16.22 (2020-03) | apoyo |
| C:NOR | V3 | 2016-01–2025-12 | 120 | 1.527 | 4.63 | 3.61 | 3.34 | [0.632, 2.422] | 18.33 | 18.43 | -19.98 (2020-11) | 16.22 (2020-03) | apoyo |
| C:NZL | V1 | 2000-01–2026-07 | 319 | 1.240 | 3.52 | 6.29 | 6.66 | [0.875, 1.605] | 14.88 | 15.10 | -11.10 (2014-04) | 13.96 (2001-09) | apoyo |
| C:NZL | V2 | 2010-01–2026-07 | 199 | 1.299 | 3.52 | 5.21 | 5.54 | [0.840, 1.758] | 15.59 | 15.91 | -11.10 (2014-04) | 11.10 (2020-12) | apoyo |
| C:NZL | V3 | 2016-01–2025-12 | 120 | 1.247 | 3.74 | 3.65 | 4.30 | [0.679, 1.815] | 14.96 | 15.10 | -9.43 (2020-11) | 11.10 (2020-12) | apoyo |
| C:PRT | V1 | 2000-01–2026-07 | 319 | 0.972 | 6.13 | 2.83 | 3.03 | [0.342, 1.602] | 11.67 | 9.80 | -23.97 (2020-11) | 18.02 (2011-10) | apoyo |
| C:PRT | V2 | 2010-01–2026-07 | 199 | 1.086 | 6.48 | 2.37 | 2.67 | [0.289, 1.883] | 13.03 | 11.02 | -23.97 (2020-11) | 18.02 (2011-10) | apoyo |
| C:PRT | V3 | 2016-01–2025-12 | 120 | 0.595 | 6.61 | 0.98 | 1.22 | [-0.358, 1.547] | 7.13 | 4.57 | -23.97 (2020-11) | 16.38 (2020-03) | inconcluso |
| C:SGP | V1 | 2000-01–2026-07 | 319 | 0.851 | 4.34 | 3.50 | 3.01 | [0.297, 1.406] | 10.22 | 9.40 | -31.70 (2009-05) | 14.52 (2020-07) | apoyo |
| C:SGP | V2 | 2010-01–2026-07 | 199 | 1.027 | 3.24 | 4.47 | 5.36 | [0.652, 1.402] | 12.33 | 12.35 | -9.07 (2013-10) | 14.52 (2020-07) | apoyo |
| C:SGP | V3 | 2016-01–2025-12 | 120 | 0.907 | 3.22 | 3.09 | 3.94 | [0.456, 1.359] | 10.89 | 10.78 | -9.00 (2016-03) | 14.52 (2020-07) | apoyo |
| C:SWE | V1 | 2000-01–2026-07 | 319 | 1.057 | 5.79 | 3.26 | 3.26 | [0.421, 1.693] | 12.68 | 11.13 | -29.43 (2009-04) | 22.36 (2000-02) | apoyo |
| C:SWE | V2 | 2010-01–2026-07 | 199 | 1.205 | 3.27 | 5.19 | 6.99 | [0.868, 1.543] | 14.46 | 14.74 | -10.63 (2012-01) | 13.16 (2021-07) | apoyo |
| C:SWE | V3 | 2016-01–2025-12 | 120 | 1.000 | 3.38 | 3.25 | 4.77 | [0.589, 1.411] | 12.00 | 11.95 | -7.18 (2022-01) | 13.16 (2021-07) | apoyo |

Resumen de veredictos de los 21 paises AQR restantes (excluye JPN, USA, CAN que estan arriba):
V1 = 17 apoyo, 4 inconcluso (AUT, GRC, IRL, NLD); V2 = 17 apoyo, 4 inconcluso (AUT, GRC, IRL, NLD);
V3 = 14 apoyo, 7 inconcluso (AUT, BEL, ESP, GRC, IRL, NLD, PRT). Ninguna serie de ninguna fuente
obtuvo veredicto "contraria".

## 5. Diagnosticos

### 5.1 Fuente A vs fuente B (reconstruccion desde portafolios 2x3 VW)

| region | n comun (historia completa) | corr A-B | dif. media mensual A-B (pp) | max abs dif (pp) |
|---|---|---|---|---|
| Emerging | 440 (1990-01–2026-08) | 1.00000 | 0.0004 | 0.020 |
| Developed_ex_US | 430 (1990-11–2026-08) | 1.00000 | 0.0010 | 0.020 |
| Europe | 430 (1990-11–2026-08) | 1.00000 | 0.0007 | 0.015 |
| Asia_Pacific_ex_Japan | 430 (1990-11–2026-08) | 1.00000 | 0.0008 | 0.020 |
| Japan | 430 (1990-11–2026-08) | 1.00000 | 0.0004 | 0.015 |
| North_America | 430 (1990-11–2026-08) | 1.00000 | 0.0007 | 0.020 |

### 5.2 French (A) vs AQR (C) en meses comunes

| par (French ~ AQR) | V | meses comunes | n | corr A-C | media x12 A % | media x12 C % | dif. media mensual A-C (pp) | max abs dif mensual (pp) |
|---|---|---|---|---|---|---|---|---|
| Europe~Europe | V1 | 2000-01–2026-07 | 319 | 0.971 | 9.04 | 12.08 | -0.253 | 3.35 |
| Europe~Europe | V2 | 2010-01–2026-07 | 199 | 0.949 | 10.30 | 13.48 | -0.265 | 3.32 |
| Europe~Europe | V3 | 2016-01–2025-12 | 120 | 0.959 | 7.41 | 10.25 | -0.237 | 3.32 |
| Japan~JPN | V1 | 2000-01–2026-07 | 319 | 0.980 | -0.24 | 1.04 | -0.107 | 3.87 |
| Japan~JPN | V2 | 2010-01–2026-07 | 199 | 0.986 | 0.99 | 1.37 | -0.032 | 3.87 |
| Japan~JPN | V3 | 2016-01–2025-12 | 120 | 0.986 | -1.08 | -0.67 | -0.034 | 1.64 |
| North_America~North America | V1 | 2000-01–2026-07 | 319 | 0.935 | 3.18 | 4.12 | -0.078 | 12.67 |
| North_America~North America | V2 | 2010-01–2026-07 | 199 | 0.919 | 4.51 | 5.52 | -0.084 | 9.80 |
| North_America~North America | V3 | 2016-01–2025-12 | 120 | 0.899 | 1.97 | 1.32 | 0.054 | 9.80 |
| Developed_ex_US~Global Ex USA | V1 | 2000-01–2026-07 | 319 | 0.971 | 6.98 | 10.06 | -0.257 | 3.08 |
| Developed_ex_US~Global Ex USA | V2 | 2010-01–2026-07 | 199 | 0.954 | 8.46 | 11.43 | -0.248 | 2.76 |
| Developed_ex_US~Global Ex USA | V3 | 2016-01–2025-12 | 120 | 0.949 | 5.75 | 8.66 | -0.243 | 2.30 |
| Asia_Pacific_ex_Japan~Pacific | V1 | 2000-01–2026-07 | 319 | 0.657 | 10.47 | 5.81 | 0.388 | 10.88 |
| Asia_Pacific_ex_Japan~Pacific | V2 | 2010-01–2026-07 | 199 | 0.677 | 12.17 | 7.40 | 0.397 | 8.35 |
| Asia_Pacific_ex_Japan~Pacific | V3 | 2016-01–2025-12 | 120 | 0.581 | 9.02 | 5.44 | 0.298 | 8.35 |

(La tabla equivalente B vs C esta en `resultados.json` -> `diagnostico_vs_C`; difiere de A vs C en
a lo sumo 0.013 pp de media x12.)

### 5.3 Sensibilidad de emergentes al mes final de la ventana

| fuente | ventana | n | media x12 % | compuesto % | t NW | veredicto |
|---|---|---|---|---|---|---|
| A | 2000-01..2025-12 | 312 | 8.97 | 8.84 | 4.10 | apoyo |
| A | 2000-01..2026-07 | 319 | 9.31 | 9.09 | 4.06 | apoyo |
| A | 2000-01..2026-08 | 320 | 9.59 | 9.37 | 4.21 | apoyo |
| A | 2010-01..2025-12 | 192 | 11.40 | 11.62 | 5.74 | apoyo |
| A | 2010-01..2026-07 | 199 | 11.87 | 11.94 | 5.17 | apoyo |
| A | 2010-01..2026-08 | 200 | 12.30 | 12.40 | 5.47 | apoyo |
| B | 2000-01..2025-12 | 312 | 8.96 | 8.83 | 4.10 | apoyo |
| B | 2000-01..2026-07 | 319 | 9.31 | 9.08 | 4.06 | apoyo |
| B | 2000-01..2026-08 | 320 | 9.58 | 9.37 | 4.21 | apoyo |
| B | 2010-01..2025-12 | 192 | 11.39 | 11.62 | 5.75 | apoyo |
| B | 2010-01..2026-07 | 199 | 11.87 | 11.93 | 5.17 | apoyo |
| B | 2010-01..2026-08 | 200 | 12.29 | 12.39 | 5.48 | apoyo |

Meses de 2026 de WML Emerging (fuente A, % mensual, leidos del CSV): 2026-01 8.02, 2026-02 5.53,
2026-03 -5.03, 2026-04 12.84, 2026-05 9.58, 2026-06 0.36, 2026-07 -16.84, 2026-08 8.02.
2026-04 y 2026-07 son, respectivamente, el mejor y el peor mes de toda la ventana V1 (2000-01 a 2026-08).

### 5.4 Composicion de agregados AQR (adenda 2, descriptiva, desde 2000-01, n=319)

| par | correlacion |
|---|---|
| C:Pacific ~ C:JPN | 0.884 |
| C:Pacific ~ C:AUS | 0.552 |
| C:Pacific ~ C:HKG | 0.680 |
| C:Pacific ~ C:SGP | 0.500 |
| C:Pacific ~ C:NZL | 0.299 |
| C:North America ~ C:USA | 0.999 |
| C:North America ~ C:CAN | 0.774 |
| A:Asia_Pacific_ex_Japan ~ C:JPN | 0.393 |
| A:North_America ~ C:USA | 0.935 |

## 6. Discrepancias entre fuentes y causas probables

1. **A vs B: sin discrepancia material.** Correlacion 1.00000 y diferencia maxima de 0.020 pp en
   un mes (redondeo a 2 decimales de los portafolios). Esto confirma que WML de French es
   1/2(Small High + Big High) - 1/2(Small Low + Big Low) de los portafolios VW, pero **B no es una
   fuente independiente**: usa la misma base (Bloomberg, version 202608) y los mismos portafolios.
2. **Europa y Desarrollados ex-EUA: AQR ~3 pp/ano mas alto que French** (media x12 V1: Europe 12.08
   vs 9.04; Global ex USA 10.06 vs Developed_ex_US 6.98, en meses comunes) con correlaciones
   mensuales 0.95-0.97. Causas probables (no demostradas aqui): (a) AQR forma UMD dentro de cada pais
   y agrega ponderando por capitalizacion rezagada del pais (factor neutral por pais), mientras
   French ordena acciones a nivel region (breakpoints regionales; incluye apuestas entre paises);
   (b) AQR usa orden dependiente (primero tamano, luego momentum) y French independiente — lo
   declara la propia hoja "Sources and Definitions" de AQR; (c) datos distintos: AQR = CRSP +
   Compustat/XpressFeed Global; French internacional = Bloomberg; (d) universos, filtros y
   refrescos historicos distintos. Ambas fuentes coinciden en el signo y en el veredicto ("apoyo").
3. **Japon: alta correlacion (0.98-0.99), medias distintas pero ambas cerca de cero** (V1 media x12
   -0.24 French vs 1.04 AQR). Veredicto "inconcluso" en A, B y C en las tres ventanas.
4. **Norteamerica: correlacion 0.90-0.94 y diferencias mensuales puntuales de hasta 12.67 pp.**
   AQR "North America" tiene media x12 mas alta (V1 4.12 vs 3.18; V2 5.52 vs 4.51) y en V2 cruza el
   umbral: IC95 NW [0.010, 0.909] %/mes, t NW 2.01 -> "apoyo" marginal; French queda en
   "inconcluso" (IC95 NW V2 [-0.044, 0.740]). Causa probable: misma lista de causas del punto 2;
   el agregado AQR es casi igual a USA (correlacion 0.999) pero incorpora CAN, cuyo UMD de pais es
   fuerte en AQR (media x12 15.84 en V1, t NW 3.44), mientras que en French Canada entra mezclada en
   un solo ordenamiento regional dominado por EUA. USA sola (AQR) es "inconcluso" en las 3 ventanas.
5. **Asia Pacifico ex Japon (French) vs Pacific (AQR): NO son comparables.** AQR Pacific incluye
   Japon (la hoja no lista su composicion; la correlacion Pacific~JPN 0.884 frente a
   Asia_Pacific_ex_Japan~JPN 0.393 es consistente con ello); por eso Pacific tiene
   media menor (V1 5.81 vs 10.47) y correlacion baja con French (0.66). No es una contradiccion.
6. **Fin de muestra distinto**: French llega a 2026-08 y AQR a 2026-07; los diagnosticos 5.2 usan
   solo meses comunes.

## 7. Evaluacion de las afirmaciones

### 7.1 "Emergentes 9.6% anual desde 2000 y 12.3% desde 2010"

| fuente | ventana | media x12 % (no es CAGR) | compuesto % | IC95 NW %/mes | t NW | veredicto | coincide con cifra (±0.15 pp) |
|---|---|---|---|---|---|---|---|
| A French WML | 2000-01–2026-08 | 9.59 | 9.37 | [0.427, 1.171] | 4.21 | apoyo | media x12 si; compuesto no |
| A French WML | 2010-01–2026-08 | 12.30 | 12.40 | [0.658, 1.391] | 5.47 | apoyo | media x12 si; compuesto si |
| B reconstruccion | 2000-01–2026-08 | 9.58 | 9.37 | [0.427, 1.170] | 4.21 | apoyo | media x12 si; compuesto no |
| B reconstruccion | 2010-01–2026-08 | 12.29 | 12.39 | [0.658, 1.390] | 5.48 | apoyo | media x12 si; compuesto si |
| C AQR | — | — | — | — | — | — | no evaluable: AQR no publica emergentes |

- **En B se sostiene numericamente**: 9.6 y 12.3 son la media aritmetica x12 de WML Emerging con
  datos French version 202608 y ventana que termina en 2026-08. "9.6% anual" NO es la tasa
  compuesta (9.37%).
- **En C no puede evaluarse** (no hay serie de emergentes). No existe confirmacion independiente
  de la cifra de emergentes entre las fuentes accesibles; B solo verifica la aritmetica sobre los
  mismos datos.
- **Fragilidad**: las cifras dependen del mes final. Con fin en 2025-12: 8.97 (desde 2000) y 11.40
  (desde 2010); con fin en 2026-07: 9.31 y 11.87. 2026 contiene el mejor (+12.84, abril) y el peor
  (-16.84, julio) mes de toda la ventana desde 2000. La ventana fija 2016-01 a 2025-12 da 10.32
  (media x12) y 10.41 (compuesto). La conclusion cualitativa (momentum emergente > 0, IC95 NW
  excluye cero) es robusta en A y B en las tres ventanas y en todas las variantes de fin de ventana.

### 7.2 "Japon y Norteamerica inconclusos"

| serie | V1 | V2 | V3 | ¿inconcluso en V1 y V2? |
|---|---|---|---|---|
| A Japan | inconcluso (t NW -0.09) | inconcluso (0.40) | inconcluso (-0.37) | si |
| B Japan | inconcluso (-0.09) | inconcluso (0.39) | inconcluso (-0.37) | si |
| C JPN | inconcluso (0.37) | inconcluso (0.57) | inconcluso (-0.22) | si |
| A North_America | inconcluso (1.00) | inconcluso (1.74) | inconcluso (0.58) | si |
| B North_America | inconcluso (1.00) | inconcluso (1.74) | inconcluso (0.58) | si |
| C North America | inconcluso (1.22) | **apoyo (2.01; IC inf. 0.010)** | inconcluso (0.35) | **no** |
| C USA (complemento) | inconcluso (0.98) | inconcluso (1.69) | inconcluso (0.17) | si |
| C CAN (complemento) | apoyo (3.44) | apoyo (3.89) | apoyo (2.26) | no |

- **Japon inconcluso: se sostiene en B y en C** (y en A), en las tres ventanas.
- **Norteamerica inconcluso: se sostiene en B; en C se sostiene solo parcialmente**: V1 y V3
  inconcluso, pero V2 (2010-01 a 2026-07) da "apoyo" marginal (limite inferior IC95 NW 0.010
  %/mes). Con USA sola en AQR si es inconcluso en todas las ventanas. Canada, por separado, muestra
  momentum positivo significativo en AQR.

## 8. Conclusiones

### Permitidas

- Con datos French (version 202608, hasta 2026-08), WML de emergentes tiene media x12 de 9.59%
  (desde 2000-01) y 12.30% (desde 2010-01); la reconstruccion desde portafolios 2x3 da 9.58% y
  12.29%. Son medias aritmeticas anualizadas de una serie largo-corto de papel.
- El momentum de emergentes en French es positivo y su IC95 NW excluye cero en V1, V2 y V3.
- Japon: ninguna de las tres fuentes permite distinguir el premio de momentum de cero en ninguna
  ventana.
- Norteamerica (French, A y B): inconcluso en las tres ventanas. AQR North America: inconcluso en V1
  y V3, "apoyo" marginal en V2; AQR USA: inconcluso en las tres.
- Europa, Desarrollados ex-EUA y Asia Pacifico ex Japon: "apoyo" en A y B en las tres ventanas;
  los comparables AQR (Europe, Global ex USA) tambien "apoyo" en las tres ventanas.
- AQR reporta, para Europa y Global ex USA, medias ~3 pp/ano mayores que French con series muy
  correlacionadas; la magnitud del premio depende de la metodologia de construccion.

### NO permitidas

- Decir que "el momentum emergente rinde 9.6% anual" como rendimiento de inversion, CAGR o
  rendimiento de una cuenta: es media aritmetica x12 de un factor largo-corto sin costos de
  transaccion, sin costo de pedir prestado/vender en corto, sin impuestos; el compuesto de la
  propia serie desde 2000 es 9.37%.
- Presentar 9.6%/12.3% como cifras estables: dependen del mes final (8.97%/11.40% con fin en
  2025-12) y de la version del archivo (French reconstruye su historia cada mes).
- Afirmar que la cifra de emergentes fue confirmada por una fuente independiente: B usa los mismos
  datos que A y C no tiene emergentes.
- Decir que el momentum "no funciona" o "es cero" en Japon o Norteamerica: "inconcluso" significa
  que el IC95 NW incluye cero, no que el premio sea cero (p. ej. Japon V1 IC95 NW [-0.481, 0.440]
  %/mes).
- Decir que "Norteamerica inconcluso" se sostiene en todas las fuentes y ventanas: AQR North
  America en V2 da "apoyo" (marginal).
- Comparar directamente Asia_Pacific_ex_Japan de French con Pacific de AQR (este incluye Japon).
- Extrapolar estos resultados historicos a rendimientos futuros o implementables.

## 9. Reproduccion

```
cd laboratorio/auditorias/AC-03-momentum-internacional
(cd datos && sha256sum -c SHA256SUMS.txt)
python3 auditoria.py   # sin red; lee datos/, escribe resultados.json
```

Dos ejecuciones consecutivas producen el mismo `resultados.json` (SHA256 identico).
