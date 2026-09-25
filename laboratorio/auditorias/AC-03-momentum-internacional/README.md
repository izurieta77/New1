# AC-03 — Momentum internacional (auditoria ciega)

Estado: ESPECIFICACION PRE-REGISTRADA (escrita antes de descargar datos y antes de calcular).
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

## 3. Resultados

(pendiente — se completa despues de descargar y calcular)
