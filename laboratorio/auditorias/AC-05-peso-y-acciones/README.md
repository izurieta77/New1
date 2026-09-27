# AC-05: segunda ejecución independiente de R08 (el peso y las acciones de EUA para quien mide en pesos)

> Fase 0, formación. Nada de esto es una recomendación de inversión. Todas las cifras son históricas.

| Campo | Valor |
|---|---|
| Réplica auditada (A) | `laboratorio/replicas/R08-peso-y-acciones-para-un-mexicano.md` (corrida final 2026-09-25 06:56 UTC) |
| Ejecución independiente (B) | `AC05.py` en esta carpeta. Solo usa la biblioteca estándar de Python 3.11; de `herramientas/datos.py` toma únicamente `parsear_yahoo_json` y `parsear_fred_csv`. No importa ni copia `R08.py` |
| Fecha | 2026-09-27 (descargas entre 01:10 y 01:11 UTC) |
| Comando | `python3 laboratorio/auditorias/AC-05-peso-y-acciones/AC05.py` (sin red, tarda unos 3 s; lee `datos/` y reescribe `datos/SHA256SUMS.txt`, `salida.txt` y `resultados.json`) |

## Protocolo ciego

1. De la ficha R08 leí solo las secciones 1 a 9 (pre-registro).
2. Descargué los datos por mi cuenta. Del archivo `R08-datos/bitacora_descarga.json` solo miré las URL de descarga, no resultados.
3. Escribí `AC05.py` y generé `salida.txt`.
4. Solo después leí las secciones 10 a 16 de R08 para la comparación de abajo.

Hubo un solo cambio de código después de la primera corrida y antes de leer A: la regla de la conclusión operable. La primera versión aplicaba "se descarta" primero; la segunda reporta el choque entre las dos reglas del pre-registro. No cambió ninguna cifra.

## Fuentes (B usa fuentes principales distintas de A)

| Serie | Uso en B | Fuente exacta | sha256 |
|---|---|---|---|
| S&P 500 Total Return | **R principal** (fin de mes: último cierre ≤ fin de mes con antigüedad ≤ 10 días; diario para H3) | Yahoo `https://query1.finance.yahoo.com/v8/finance/chart/%5ESP500TR?period1=-2208988800&period2=4102444800&interval=1d&events=div%2Csplit` (1988-01-04 a 2026-09-25) | `5cd21a1d57ed9001330dbdcc36fcba48094713ebf74ca32c367165615b6a2b2c` |
| USD/MXN FIX | **S principal** (fin de mes; diario para H3) | Banxico SIE, POST sin token a `https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarSeries` con `idCuadro=CF102, series=SF43718, formatoCSV` (1991-11-12 a 2026-09-25) | `3a1e47e7830ae2ed46f36613c940ca992349f81c665a0b98482ec116d18a6cc1` |
| CETES (FMI) | **Efectivo y tasa MX de la cobertura**: valor del mes t−1 / 1200 | FRED `https://fred.stlouisfed.org/graph/fredgraph.csv?id=INTGSTMXM193N` (1986-10 a 2026-07) | `6ffbf4e5f6682a53c1a859f0f1b0156c54090559664f31d89d0a21745bf89e22` |
| T-bill a 3 meses | **Tasa de EUA de la cobertura** y referencia USD: mes t−1 / 1200 | FRED `...?id=TB3MS` | `ebf04b1ae5bc5729ba3bb2b35dbb0e0c5e22dace36bea0c02632782d625ae6ab` |
| USD/MXN Yahoo | Contraste 2004-01+ (la serie empieza el 2003-12-01) | Yahoo `MXN%3DX`, misma URL que arriba | `28983d956dcbb6ab28b220467627278e1cfc802e0a4c88b39010d5724afebd0c` |
| USD/MXN H.10 | Contraste (fuente principal de A) y cifras del capítulo (S3b) | FRED `...?id=DEXMXUS` | `676efa2ae952594c0b1ec94a6e6c76bdafd679a9d4a6b7dd3266ff118a0d696e` |
| CETES 28 subasta | Contraste (fuente principal de A): última subasta ≤ fin de t−1, tasa × días/360 | Banxico SIE `CF107, SF43936` | `ef8c8d98b4494b0dc42dde9e66cf9cc7cf1476771c75dc616898beb41544a35b` |
| S&P 500 precio | Solo S3b (cifras del capítulo) | Yahoo `%5EGSPC` | `08bdf58f050e30df9b53b6df355951f579bc876082454dced814c40e35fef396` |

Control de calidad: en fin de mes, MXN=X se separa del FIX como máximo 1.79% (2009-02) y DEXMXUS como máximo 1.36% (1995-01). No encontré saltos erróneos en MXN=X.

Construcción, igual a la de la sección 8 del pre-registro: x = S_t/S_{t−1} − 1; U = (1+R)(1+x) − 1; f = (1+cetes)/(1+i_US) − 1; R^h = U − h·(x − f). Costo de entrada de 0.34% (0.29% + 0.05%). El 50/50 se rebalancea cada mes con deriva y paga 0.34% sobre lo negociado. P6 usa ventana expansiva, un mínimo de 36 meses y recorte a [0, 1]. El *bootstrap* usa bloques móviles de 12, 5000 repeticiones y semilla 20260925. Los t son de Newey-West(6).

## Comparación B contra A (neto; A = French CRSP × DEXMXUS × CETES Banxico × RF French)

| Métrica | A (R08) | B (AC-05) | Dif. |
|---|---|---|---|
| corr(R,x) completo / dentro / fuera | −0.370 / −0.174 / −0.557 | −0.364 / −0.159 / −0.559 | ≤ 0.015 |
| IC95 corr completo | [−0.571, −0.211] | [−0.567, −0.204] | — |
| H2: x y A en meses con R < −5% (n) | +3.68%, 0.411 (38) | +3.57%, 0.414 (38) | 0.11 pp |
| H3: ventaja MXN crisis / 2020 / 2022 (pp) | 16.2 / 18.0 / −2.0 | 17.0 / 16.4 / −2.0 | 1.6 pp en 2020 |
| Vol h0 / h1 completo | 16.71 / 16.15 | 16.53 / 15.69 | — |
| **vol(h1) − vol(h0) completo** | **−0.56 pp** | **−0.84 pp** | 0.28 pp |
| vol(h1) − vol(h0) dentro / fuera | −4.40 / +2.60 | −4.81 / +2.49 | ≤ 0.41 pp |
| IC95 dvol fuera | [0.00, 5.21] | [−0.01, 4.97] | — |
| MDD h0 / h1 completo | −39.86 / −48.70 | −39.83 / −49.37 | 0.67 pp |
| MDD h0 / h1 fuera | −29.97 / −48.70 | −31.30 / −49.37 | 1.33 pp |
| CAGR h0 / h1 completo | 16.92 / 19.29 | 16.94 / 19.18 | 0.11 pp |
| CAGR h0 / h1 fuera | 13.56 / 14.89 | 13.52 / 14.74 | 0.15 pp |
| Sharpe h0 / h1 completo | 0.383 / 0.535 | 0.394 / 0.549 | ≤ 0.014 |
| Sharpe h0 / h1 fuera | 0.543 / 0.555 | 0.558 / 0.564 | ≤ 0.015 |
| h de mínima varianza: completo / dentro / fuera | 0.547 / 0.785 / 0.227 | 0.567 / 0.799 / 0.245 | ≤ 0.02 |
| H5: media (f−x) ×12, t NW | 2.05%, 0.79 | 1.89%, 0.72 | 0.16 pp |
| H6 50/50 completo: vol h0/h1, MDD h0/h1 | 8.67/8.54, −11.87/−23.67 | 8.54/8.32, −12.37/−24.24 | ≤ 0.57 pp |
| H6 50/50 fuera: vol h0/h1, MDD h0/h1 | 6.86/8.17, −11.87/−23.67 | 6.67/7.93, −12.22/−24.24 | ≤ 0.57 pp |
| H7: rango de h (P6); Δvol y ΔMDD fuera | 0.54–0.93; +0.69 pp, −14.04 pp | 0.56–0.93; +0.66 pp, −13.77 pp | ≤ 0.3 pp |
| S3b (A1, A2, A3, A4, A6) | 1996-2026: corr −0.502, vol 15.3/13.6, CAGR 8.51/11.41 | idénticos | 0 |

Número de operaciones: ninguna implementación tiene operaciones discrecionales. Comprar y mantener paga solo la entrada; el 50/50 hace 391 rebalanceos mensuales en ambas. La división dentro/fuera de muestra es la misma en las dos: 161 y 230 meses, con corte el 2007-05-31.

## Explicación de las diferencias (todas bajo tolerancia: < 0.05 de Sharpe y < 1 pp de CAGR)

1. **Activo: CRSP total contra S&P 500 TR.** Es la causa de las diferencias en volatilidad y MDD. El S&P TR es menos volátil en 1994-2007 (usd_referencia: 14.11% en B contra 14.55% en A) y cae un poco más en 2008-09. Prueba: la sensibilidad S3a de A (`^SP500TR` × DEXMXUS) da fuera de muestra 13.41 / 15.87 de vol y −31.22 / −49.31 de MDD. B da 13.38 / 15.87 y −31.30 / −49.37. Con el mismo activo, las dos coinciden a 0.1 pp.
2. **FX: FIX de Banxico (mediodía en CDMX, "fecha de determinación") contra DEXMXUS (mediodía en NY).** En mensual casi no importa: en el contraste de B con DEXMXUS, la dvol completa cambia de −0.84 a −0.80 y la corr de −0.364 a −0.366. En **diario sí importa en días de pánico**. La caída en MXN de 2020 es −17.3% con FIX, −14.9% con DEXMXUS y −17.2% con MXN=X (cierre de Londres). De ahí sale la diferencia de H3 en 2020 (16.4 contra 18.0 pp). También pesa el activo: A usa French diario. Con el mismo ^SP500TR, la conclusión no cambia con ninguna de las tres fuentes: la ventaja es de al menos 16 pp en 2020 y de al menos 17 pp en la crisis financiera.
3. **CETES: FMI mensual / 1200 contra subasta de Banxico × días/360; y TB3MS contra RF de French.** Explica el −0.14 pp de CAGR del cubierto y los 0.16 pp de *carry*. Prueba: el contraste de B con CETES de Banxico lleva el dCAGR completo a 2.38 pp, el mismo valor que A. cetes_100 da 11.03% en B contra 11.17% en A.
4. **Sharpe (+0.01).** Viene de la vol más baja del S&P TR y de un CETES del FMI ligeramente menor. No cambia el orden de las variantes.
5. **Dividendos y fechas.** Las dos versiones usan rendimiento total. Las fechas de corte y de las ventanas son las del pre-registro en ambas. La única diferencia de calendario es que B toma el último dato ≤ fin de mes de cada fuente.
6. **IC de la dvol fuera de muestra.** En A, el límite inferior es +0.0015 pp; en B, −0.01 pp. Ninguno es criterio de refutación, pero las dos versiones coinciden en que el aumento de volatilidad por cubrir fuera de muestra está **en el límite de la significancia**.

## Veredicto

- **Estado: concordante, "No replicado".** H4 queda refutada en la muestra completa, y en B con más margen que en A: vol(h1) − vol(h0) = −0.84 pp contra −0.56 pp. La razón es la misma en las dos: la devaluación de 1994-95 (en B, la vol sin cubrir dentro de muestra es 20.16% contra 15.35% cubierta). H1, H2, H3, H5 (signo y rango, sin significancia), H6 fuera de muestra y H7 dan el mismo resultado en A y en B. H6 completo tampoco se cumple en B, igual que en A: la vol cubierta es menor por 0.22 pp.
- **Conclusión operable: concordante.** B reproduce el mismo **choque de reglas del pre-registro**. Las cuatro condiciones de "se confirma" se cumplen fuera de muestra (H1 −0.559 con IC que excluye el 0; H3 +17.0 y +16.4 pp; H4 fuera +2.49 pp; H6 fuera), y al mismo tiempo se activa "se descarta" por la refutación de H4 en la muestra completa. Ninguna cobertura parcial domina a h = 0 fuera de muestra: h = 0.25 tiene menos vol, 13.05 contra 13.38, pero peor MDD, −35.8 contra −31.3. El costo de no cubrir no es significativo (t NW 0.72). P6 se descarta. Por lo tanto, "no cubrir acciones de EUA fuera de muestra, como regla de control de caídas en choques globales y no de menor volatilidad en todo régimen" se sostiene igual con la segunda fuente.

## Para corregir fuera de esta carpeta (no lo edité)

- R08 §16 dice: "No hay segunda implementación con código independiente". Esa frase quedó desactualizada: AC-05 es esa implementación, y concuerda.
- El choque entre "se confirma" y "se descarta" de la sección 8 de R08 ya está declarado por A como defecto del pre-registro. B lo confirma. Conviene que la tabla maestra muestre la conclusión operable como "post-hoc" y no como replicada.
