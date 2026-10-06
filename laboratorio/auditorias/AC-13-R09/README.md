# AC-13: doble ejecución independiente de R09 (efecto cambio de mes, Lakonishok-Smidt / McConnell-Xu)

> Fase 0, formación. Nada de esto es una recomendación de inversión. Cifras históricas en USD, de índices (no invertibles tal cual en GBM).

| Campo | Valor |
|---|---|
| Réplica auditada (A) | `laboratorio/replicas/R09-efecto-cambio-de-mes.md` (corrida 2026-09-25 07:01 UTC, French CRSP 202607, `^GSPC` de Yahoo) |
| Ejecución independiente (B) | `AC13.py` (Python 3, solo stdlib, ~2 min, sin red). Lectores de datos, calendario (pos_ini/pos_fin), regresión con EE MCO/HC1/Newey-West, bootstrap, D_m, E, costos y métricas están escritos desde cero. No usa `herramientas/` ni importa `R09.py`/`R09_verificacion.py` |
| Fecha | 2026-10-06 (descarga 17:50 UTC; `datos/descarga_utc.txt`, `datos/SHA256SUMS.txt`) |
| Comando | `python3 -I laboratorio/auditorias/AC-13-R09/AC13.py > salida.txt` (reproduce `salida.txt` byte a byte; escribe `resultados.json`) |
| sha256 | `AC13.py` `80738071…8411`; `salida.txt` `e32b2eaf…bff4ae`; `resultados.json` `df790c51…6b96` |

## Protocolo y límite de la ceguera

1. De la ficha R09 leí el encabezado y las secciones 1 a 9 (pre-registro) y su sección de desviaciones. No abrí `R09.py` ni `R09_verificacion.py`.
2. **No fue ciega en las cifras:** antes de escribir `AC13.py` leí partes de `R09-salida.txt` (tablas de δ, D_m y estrategias). Por eso la concordancia de B con A no prueba que B habría llegado solo a esas cifras; prueba que un código distinto, con descarga y parser nuevos, las reproduce. Se declara igual que AC-12 declaró su protocolo.
3. Después de la primera corrida comparé contra `R09-salida.txt` y corregí **un** error mío (ver "Errores propios"). Las definiciones de señal, alineación y costos no se cambiaron para acercarme a A.

## Datos: qué es segunda fuente y qué no

| Serie | Origen (descarga 2026-10-06) | Rango usado | ¿Distinta de R09? |
|---|---|---|---|
| French diario **202608** | `mba.tuck.dartmouth.edu/.../F-F_Research_Data_Factors_daily_CSV.zip`, sha256 `2f29e225…a7db` | 1926-07-01 a 2026-07-31 (recorte al fin de R09) | **Misma fuente, otra vintage.** Con 202607 (copia del repo, sha `1916d331…49a8`, la de R09) 26,296 fechas comunes; 6 con diferencia (máx. 0.0001 = 0.01 pp) |
| Yahoo `^GSPC` (cierre) | chart v8 crudo, parser propio | 1927-12-30 a 2026-08-31 | **Misma fuente que R09**, descarga y parser nuevos. Mi descarga termina el 2026-09-21 (la de R09, el 09-24); no afecta, porque ambos recortan a 2026-08-31 |
| Yahoo `^SP500TR` | idem | 1988-01-04 a 2026-08-31 | Serie distinta (rendimiento total del S&P 500) |
| Yahoo `SPY` `adjclose` | idem | 1993-01-29 a 2026-08-31 | Instrumento distinto (ETF invertible, con dividendos) |
| **FRED `SP500`** | `fredgraph.csv?id=SP500` | 2016-10-06 a 2026-08-31 | **Proveedor distinto** (S&P Dow Jones vía FRED). Solo cubre 10 años; 2,501 fechas comunes con `^GSPC`, 4 con diferencia > 0.01% (máx. 0.12%) |
| FRED `DJIA` | idem | 2016-10-06 a 2026-08-31 | Proveedor distinto; índice que usaron L&S (precio) |

**Límite.** Stooq (`^spx`) responde "connection reset" desde el proxy. No hay un tercer proveedor diario para 1926-2005. El "t 8.0" de 1926-2005 solo se contrasta con **French** (rendimiento total, CRSP VW) y con **`^GSPC`** (precio, S&P 90/500), que ya eran las dos fuentes de R09. Las fuentes realmente distintas (`^SP500TR`, SPY, FRED) cubren 1988+ (1993+, 2016+).

## Comparación A contra B

| Cifra | A (R09) | B French 202608 | B French 202607 | B `^GSPC` | Dif. A−B |
|---|---|---|---|---|---|
| **MX panel C 1926-2005: dif TOM−otros (pp/día), t MCO** | 0.1487, 8.03 | 0.1487, 8.03 | igual | 0.1517, 7.01 (A: 0.1517, 7.01) | 0 |
| Panel A / B: dif, t MCO | 0.1493, 7.07 / 0.1465, 3.82 | igual | igual | 0.1602, 6.26 / 0.1256, 3.14 | 0 |
| Exceso sobre RF, panel C: TOM (t) / otros (t) | 0.1476 (9.21) / −0.0010 | 0.1476 (9.21) / −0.0010 (−0.12) | — | — | 0 |
| δ dentro (≤2008-02-29), t NW10 | 0.1405, 7.75 | 0.1405, 7.75 | igual | 0.1393, 6.80 | 0 |
| **δ fuera (>2008-02-29), t NW10** | **0.0150, 0.35** | **0.0150, 0.35** | igual | 0.0198, 0.47 (A igual) | 0 |
| δ fuera, mitades 2008-16 / 2017- | 0.0189 / 0.0114 (t 0.30 / 0.19) | igual | igual | 0.0179 / 0.0214 | 0 |
| D_m fuera: media, t, IC95 | 0.0139, 0.35, [−0.0623, 0.0920] | 0.0139, 0.35, [−0.0622, 0.0906] | — | 0.0204, 0.53 | IC: 0.0001 / 0.0014 (ver 1) |
| D_m dentro: IC95 | [0.1058, 0.1746] | [0.1052, 0.1744] | — | — | ≤ 0.0006 (ver 1) |
| E fuera (exceso 4 días, %): media, t, IC95 | 0.2307, 1.58, [−0.0527, 0.5178] | 0.2306, 1.58, [−0.0532, 0.5135] | 0.2307 | 0.2187, 1.56 | IC: 0.004 (ver 1) |
| Sign test D>0 fuera | 108/220, p 0.632 | 108/220, p 0.632 | — | 110/221 | 0 |
| L&S, TOM 4d / mes, hasta 1986-12 (French; `^GSPC`) | 0.659 / 0.930; 0.615 / 0.543 | igual | — | igual | 0 |
| **Estrategia `tom_m1_p3`, neta, fuera**: CAGR, Sharpe, t NW10, MDD | −4.18%, −0.616, −2.96, −59.3% | −4.18%, −0.616, −2.96, −59.3% | idem | `^GSPC` a 07-31: −4.48%, −0.665, −3.26, −61.5% (A: −4.48%, −0.665, −3.26) | 0 |
| Comprar y mantener, fuera | 12.04%, 0.598, −50.7% | 12.05%, 0.598, −50.7% | 12.05% | `^GSPC` a 07-31: 9.84%, 0.503, −52.6% (A igual) | ≤ 0.01 pp |
| SMA200, fuera | 7.65%, 0.5585, −24.9% | 7.65%, 0.558, −24.9% | 7.66% | `^GSPC` a 07-31: 5.42%, 0.396, −23.8% (A 5.42%, 0.3956) | ≤ 0.01 pp |
| Estrategia neta, dentro / completo: Sharpe | −0.192 / −0.281 | −0.192 / −0.281 | — | — | 0 |
| Estrategia neta, dentro / completo: CAGR | 1.93% / 0.77% | 1.93% / 0.77% | — | — | 0 |
| `tom_m1_p3` bruto, fuera: Sharpe, t NW10 | 0.3418, 1.62 | 0.342, 1.62 | — | — | 0 |
| Operaciones por año (fuera / dentro) | 23.9989 / 23.9895 | 24.01 / 24.00 | — | — | 0.01 (ver 3) |
| Exceso bruto anual, dentro / completo | 6.78% / 6.06% | 6.45% / 5.81% | — | — | 0.3-0.4 pp (ver 2) |
| Costo de equilibrio por lado, dentro / completo | 0.28% / 0.25% | 0.27% / 0.24% | — | — | 0.01 pp (ver 2) |
| Neto de costos GBM negativo en todo tramo (Sharpe < 0, t NW10 < 0) | Sí | Sí (dentro −0.19; fuera −0.62; spread medio −0.89) | Sí | Sí (−0.65) | — |
| Condiciones (i)-(iv) | las cuatro se cumplen | (i) 0.1487 ≥ 0; (ii) 0.1405, t 7.75; (iii) 0.0150 > 0; (iv) 0.0198 > 0 | — | — | — |
| **Estado según la regla** | **Replicado** | **Replicado** | **Replicado** | **Replicado** | — |

### Segunda fuente, fuera de muestra y otras series (cifras nuevas, sin equivalente en A)

| Fuente | Tramo | δ pp/día | t NW10 | D_m fuera (t) | E fuera % (t) | `tom_m1_p3` neto fuera: CAGR / Sharpe / MDD | Comprar y mantener fuera: CAGR / Sharpe |
|---|---|---|---|---|---|---|---|
| French 202608 | fuera | 0.0150 | 0.35 | 0.0139 (0.35) | 0.231 (1.58) | −4.18% / −0.616 / −59.3% | 12.05% / 0.598 |
| Yahoo `^GSPC` (precio) | fuera a 08-31 | 0.0198 | 0.47 | 0.0204 (0.53) | 0.219 (1.56) | −4.34% / −0.649 / −61.5% | 9.95% / 0.508 |
| Yahoo `^SP500TR` | fuera | 0.0189 | 0.45 | 0.0194 (0.51) | 0.246 (1.76) | −4.03% / −0.611 / −59.2% | 12.06% / 0.604 |
| Yahoo `SPY` adjclose | fuera | 0.0182 | 0.44 | 0.0190 (0.50) | 0.244 (1.74) | −4.06% / −0.628 / −59.4% | 11.94% / 0.600 |
| FRED `SP500` | 2017-01 a 08-31 | 0.0214 | 0.37 | 0.0189 (0.35) | 0.248 (1.35) | no aplica (10 años) | — |
| FRED `DJIA` | 2016-11 a 08-31 | 0.0130 | 0.24 | — | — | — | — |
| Yahoo `^SP500TR` | 1988-2008-02 | 0.0818 | 2.23 | 0.0826 (2.34) | 0.382 (2.95) | — | — |
| Yahoo `SPY` | 1993-2008-02 | 0.0638 | 1.40 | 0.0633 (1.48) | 0.303 (1.89) | — | — |

Ninguna fuente da δ fuera de muestra significativo (t NW10 de 0.24 a 0.47; IC95 de D_m incluye 0 en todas). Con costos GBM, `tom_m1_p3` pierde entre 4.0% y 4.5% anual en todas las fuentes, con Sharpe de −0.61 a −0.65 contra +0.51 a +0.60 de comprar y mantener. El costo de equilibrio por lado (0.11% a 0.13%) es un tercio del costo GBM de 0.34%.

## Diferencias explicadas

1. **Límites de los IC bootstrap (0.0001 a 0.004 pp).** Los estimadores puntuales coinciden a 4 decimales; solo cambian los percentiles de bootstrap iid (10,000 repeticiones, ambos con semilla 9 pero generadores y orden de remuestreo distintos). No es un error y ningún IC cambia de lado respecto de cero. La media y t de E difieren en 0.0001 por la vintage (202607 da 0.2307, igual que A; 202608 da 0.2306).
2. **Exceso bruto anual y costo de equilibrio (0.3-0.4 pp y 0.01 pp), solo en tramos largos.** A anualiza el exceso diario con el número observado de datos por año (265 por año en 1927-2008, porque French trae sábados hasta 1952); B multiplica por 252. En el tramo fuera de muestra (251.7 datos por año) coinciden (2.88% = 2.88%). Verificado: 6.45% × 265.0/252 = 6.78% y 5.81% × 262.5/252 = 6.05%. **No es un error**, es una convención. Mismo origen: el Sharpe de A y de B usa 252 con datos que incluyen sábados antes de 1952, lo que lo subestima ≈2.5% en dentro y completo; no cambia ninguna conclusión. El costo de equilibrio (0.28% o 0.27% por lado) queda debajo de 0.34% con cualquier convención.
3. **Operaciones por año (24.01 contra 23.99-24.00).** B cuenta cada cambio de w (2 por mes) dentro del segmento (desde, hasta] y lo divide entre los años calendario. Causa probable de la diferencia: otra convención en los bordes del segmento o en los años (no verificado: no abrí `R09.py`). 0.01 operaciones por año, sin efecto en costos.
4. **Vintage 202608 contra 202607 (≤ 0.01 pp de CAGR).** French revisa 6 fechas entre vintages (máx. 0.01 pp). Cambia `tom_m1_p4` fuera de muestra de −4.79% a −4.80% y SMA200 de 7.66% a 7.65%. Nada cambia en el estado.
5. **`^GSPC` frente a French.** (a) La diferencia de δ (0.0198 contra 0.0150 fuera; 0.1517 contra 0.1487 en panel C) viene del índice (precio contra rendimiento total) y del calendario (Yahoo no trae los 1,085 sábados de 1928-1952, así que el "lunes" absorbe el sábado). A ya lo declara y esos números coinciden con los de A. (b) La estrategia con `^GSPC` a 2026-08-31 (−4.34%, −0.649) no es comparable con la de A (a 07-31: −4.48%, −0.665): B reproduce A solo al recortar a 2026-07-31. Los 21 días de agosto no tienen RF de French (RF = 0 en B y en A).
6. **Fuentes con total return de 1988 en adelante (`^SP500TR`, SPY).** En 1988-2005, δ_MX es 0.117 en `^SP500TR` y 0.136 en French (mismo tramo); la diferencia de 0.019 pp cae dentro de la tolerancia de 0.03 pp. Es compatible con el universo (S&P 500 grandes contra todo CRSP) y con el error de seguimiento (2.2% anual entre las dos series diarias). Ninguna conclusión depende de este contraste.
7. **Los paneles de MX tienen las mismas diferencias vs. el artículo que reporta A** (la mayor, 0.0118 pp en celdas; 0.0013 pp en la diferencia del panel C; t 8.03 contra 8.06). B las reproduce (0.1493 / 0.1465 / 0.1487).

## Errores propios (de B), corregidos antes de fijar la salida

- **L&S, "resto del mes".** Mi primera versión compuso todos los días del mes anterior al día −1 (incluidos +1..+3). Eso dio 0.761% para French contra 0.2646% de A, y no cumplía con la definición pre-registrada (+4..−2). Se corrigió y B da 0.2646% y −0.0736% (`^GSPC`), igual que A. No afectó δ, D_m ni las estrategias.
- Las series que no abarcan 1926-1986 (`^SP500TR`, SPY, FRED) imprimen "sin datos" en los paneles A (división entre cero), lo cual es correcto: no tienen esos años.

## Conclusión

- **¿Coincide el estado "Replicado"? Sí, con las mismas dos salvedades de R09.** Las cuatro condiciones se cumplen en B (French 202608, French 202607 y `^GSPC`). Es el caso que A ya señalaba como "criterio flojo": (iii) y (iv) solo exigen signo.
- **Cifras confirmadas.** δ_MX en 1926-2005 = 0.1487 pp/día (t 8.03; artículo 0.15, t 8.06; con `^GSPC` 0.1517, t 7.01). Fuera de muestra, δ = 0.0150 (t NW10 0.35; 11% del dentro de muestra), con cuatro series desde 2008-03 entre 0.0150 y 0.0198 y dos de 2016-17 en adelante (FRED SP500 y DJIA) entre 0.0130 y 0.0214 (t NW10 de 0.24 a 0.47). Neto de costos GBM, la estrategia es negativa en todos los tramos y fuentes.
- **Qué no se verificó.** (1) Para 1926-2005 no hubo un tercer proveedor independiente de French y Yahoo; (2) la versión publicada en el FAJ y L&S siguen sin leerse; (3) las cifras en MXN (DEXMXUS y CETES), las 58 corridas del motor y el DSR no se auditaron; (4) B no replica el placebo de ventanas, las décadas ni la winsorización.
- **Etiqueta de la tabla maestra: descartada** (sin cambio): fuera de muestra no hay significancia en ninguna de las series y la regla del artículo pierde 4.0%-4.5% anual neta de costos GBM.
