# AC-07: segunda ejecución independiente de R06 (ETF 2x/3x con filtro de 200 días)

> Fase 0, formación. Nada de esto es una recomendación de inversión. Todas las cifras son históricas, en USD salvo donde se indica, antes de impuestos.

| Campo | Valor |
|---|---|
| Réplica auditada (A) | `laboratorio/replicas/R06-apalancados-y-filtro-de-tendencia.md` (corrida final 2026-09-25T06:25:57Z, French CRSP 202607, fin 2026-07-31) |
| Ejecución independiente (B) | `AC07.py` en esta carpeta. Biblioteca estándar de Python 3.11; de `herramientas/datos.py` solo usa `parsear_yahoo_json` y `parsear_fred_csv`. No importa ni copia `R06.py`, `R06_verificacion.py`, el script de la ficha `2026-09-29-cortacircuitos-apalancados.py` ni el motor `herramientas/backtest.py` |
| Fecha | 2026-09-29 (descargas a las 17:49 UTC) |
| Comando | `python3 laboratorio/auditorias/AC-07-apalancados-filtro/AC07.py` (sin red, < 2 s; lee `datos/`, reescribe `datos/SHA256SUMS.txt`, `salida.txt` y `resultados.json`) |
| sha256 de `AC07.py` | `d999e615ea444029bc7b925f67520b54ec4a222d1d6dfdca7f045e8b5a6a8126` |

## Protocolo ciego

1. De la ficha R06 leí solo las secciones 1 a 9 (pre-registro).
2. Descargué los datos, escribí `AC07.py` y generé `salida.txt`.
3. Después leí las secciones 10 a 17 de R06 para la comparación. No leí `R06-salida.txt`, `R06-resultados.json` ni `R06-variantes.csv`; las cifras de A salen de las secciones 11 y 12 de la ficha.

Después de leer A agregué a `AC07.py` solo **controles de conciliación**, sin cambiar la lógica ya corrida: (a) ventanas 1990-01 a 2015-10, 2000-01 a 2015-10, 2015-11 a 2019-12 y 2020-01 a 2026-07 (las de A); (b) la corrida `efectivo`; (c) la señal sobre SPY/QQQ `adjclose` en los ETFs reales (la señal principal de A); (d) Sharpe = 0 cuando la volatilidad del exceso es nula (antes daba un número sin sentido en `efectivo`). Las cifras ya escritas no cambiaron.

## Fuentes (B usa una fuente distinta de A)

| Serie | Uso en B | Fuente exacta | Rango | sha256 |
|---|---|---|---|---|
| ^SP500TR | Subyacente de 2x/3x simulados y señal principal (rendimiento total, como el artículo) | Yahoo chart v8 `https://query1.finance.yahoo.com/v8/finance/chart/%5ESP500TR?period1=-2208988800&period2=4102444800&interval=1d&events=div%2Csplit` | 1988-01-04 a 2026-09-28 | `2d9408285b95813d24e2dfaca2a66eada79771efb05330b197f6795e278123b3` |
| ^GSPC | Señal de SSO y UPRO; variante de señal del simulado | Yahoo, misma URL con `%5EGSPC` | 1927-12-30 a 2026-09-28 | `342f032ab813fcbf91b078739f51ff4bbad389653bcd1bd527795d5293aaa9af` |
| ^NDX | Señal de QLD y TQQQ | Yahoo, `%5ENDX` | 1985-10-01 a 2026-09-28 | `02e4089c60ba25a0d1f705db0b8b6fe7c88973a7a3cbf96948a662bc3067d641` |
| SPY, QQQ (adjclose) | Índice 1x real y manga 1x de las carteras | Yahoo | 1993-01-29 / 1999-03-10 a 2026-09-28 | `962a26fe…5f66` / `10c98393…12e6` |
| SSO, UPRO, QLD, TQQQ (adjclose) | ETFs apalancados reales | Yahoo | 2006-06-21 / 2009-06-25 / 2006-06-21 / 2010-02-11 a 2026-09-28 | ver `datos/SHA256SUMS.txt` |
| DTB3 | Efectivo y financiamiento: rf_t = DTB3_{t−1}/100 × días naturales/360 | FRED `https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTB3` | hasta 2026-09-25 | `03ec32ba6230e1349f4062a0999a45722059afa2dbb78e7a5170b77e450a67b9` |
| DEXMXUS | Conversión a MXN (último dato ≤ fecha, máximo 10 días) | FRED `...?id=DEXMXUS` | hasta 2026-09-25 | `0b71c05f77c3663baa78d1f3b2db2a4e1a4fbf538b7002d4f0d783a30ae53e4b` |

El punto de Yahoo del 2026-09-29 (intradía) se descarta. Ninguna serie tiene cierres nulos en el tramo usado (A reportó un nulo el 2026-09-22 que en esta descarga ya no aparece). Sin saltos sospechosos (|r| > 25% en 1x, > 40% en 2x, > 60% en 3x). Condiciones de uso de Yahoo: no verificadas; los archivos se guardan solo para reproducir.

## Definiciones de B (escritas desde el pre-registro)

- Simulado: r_L,t = L·r_t − (L−1)·rf_t − 0.9%·Δd/365.25 (L ≥ 2), r = ^SP500TR.
- Filtro: on(d) = nivel(d) > media simple de los 200 cierres que terminan en d (empate fuera). "Al cierre": el peso del día t usa on del día hábil anterior (t−1) del calendario del subyacente; "rezago": on(t−2).
- Peso 1 en el activo o 0 en T-bill. Costo |Δw| × 0.34% (0.29% GBM + 0.05% spread), exposición inicial 0 (la primera compra paga). Una corrida continua por variante, recortada por segmento; MDD sobre la curva reiniciada.
- CAGR con días naturales/365.25 desde el cierre anterior al primer día del segmento; vol = sd diaria × √252; Sharpe = media/sd del exceso diario sobre rf × √252.
- Fuera de muestra = 2015-11-02 a **2026-08-31** (último mes completo); también 2015-11-02 a 2026-07-31 (ventana de A). Dentro de muestra: B solo tiene 1988-11 a 2015-10 (A: 1928-10 a 2015-10).
- Veredicto (pre-registro §2): "Se sostiene" si LRS 2x y 3x tienen Sharpe ≥ 1x y CAGR > 1x; "Solo protección" si no, pero MDD(LRS L) menos profundo que MDD(L× comprar y mantener) en L = 2 y 3.
- Temporadas (extra, comité 2-oct): 85 días hábiles, inicio cada 5 días, sobre la curva continua. Cartera: 50% en el 3x cuando el filtro (^GSPC o ^NDX) está arriba, esa mitad en T-bill USD cuando está abajo; 50% en SPY o QQQ. Rebalanceo a 50/50 solo si la mitad apalancada sale de 45%–55%; costo 0.34% sobre cada pierna de ETF operada. MXN = valor USD × DEXMXUS. DD de temporada = peor caída desde el máximo dentro de la temporada (incluye el valor inicial). Percentiles con interpolación lineal. Temporadas traslapadas (≈ 17 por ventana), no independientes.

## Resultados de B

### Simulado desde ^SP500TR (señal sobre ^SP500TR, al cierre)

| Variante | Fuera 2015-11 a 2026-08: CAGR / Sharpe / MDD | Toda 1988-11 a 2026-08: CAGR / Sharpe / MDD |
|---|---|---|
| 1x comprar y mantener | 14.77% / 0.74 / −33.8% | 11.42% / 0.53 / −55.3% |
| 2x comprar y mantener | 23.56% / 0.71 / −59.1% | 15.71% / 0.51 / −87.6% |
| 3x comprar y mantener | 29.87% / 0.72 / −76.6% | 17.35% / 0.51 / −97.9% |
| LRS 2x | 16.36% / 0.66 / −40.1% | 13.19% / 0.52 / −50.8% |
| LRS 3x | 23.05% / 0.70 / −53.3% | 17.79% / 0.56 / −67.9% |
| LRS 2x con rezago | 14.87% / 0.61 / −45.3% | 12.56% / 0.50 / −45.6% |
| LRS 3x con rezago | 20.67% / 0.64 / −59.4% | 16.80% / 0.54 / −61.2% |

- **Veredicto fuera de muestra: "Solo protección"** (al cierre, con rezago y en la ventana de A). LRS 2x y 3x ganan en CAGR al 1x pero pierden en Sharpe; reducen el MDD del mismo apalancado en 19 y 23 pp.
- Dentro de muestra 1988-11 a 2015-10: no hay refutación (LRS 2x 11.94%, Sharpe 0.46 contra 1x 10.10%, 0.45), pero el margen de Sharpe es mínimo (0.01); en 1990-2015, LRS 2x 10.67% (Sharpe 0.42) contra 1x 9.41% (0.42). El LRS 1x queda debajo del índice en CAGR y Sharpe en las dos ventanas.
- Señal sobre ^GSPC de precio en lugar de ^SP500TR: coincide en 97.3% de los días, pero baja el CAGR de LRS 3x fuera de muestra de 23.05% a 18.82% (5.4 cruces/año contra 6.6).

### ETFs reales (señal ^GSPC / ^NDX de precio)

| ETF | Tramo | B&H del ETF | Filtro al cierre | Filtro con rezago | 1x (SPY o QQQ) |
|---|---|---|---|---|---|
| UPRO | fuera 2015-11 a 2026-08 | 27.90% / 0.69 / −76.8% | 17.48% / 0.58 / −53.1% | 18.90% / 0.61 / −57.8% | 14.66% / 0.73 / −33.7% |
| UPRO | toda 2009-06 a 2026-08 | 32.90% / 0.79 / −76.8% | 19.48% / 0.64 / −53.1% | 21.30% / 0.68 / −57.8% | 15.12% / 0.83 / −33.7% |
| TQQQ | fuera | 37.01% / 0.78 / −81.7% | 35.25% / 0.82 / −55.3% | 34.74% / 0.81 / −56.9% | 19.41% / 0.81 / −35.1% |
| TQQQ | toda 2010-02 a 2026-08 | 42.43% / 0.86 / −81.7% | 30.76% / 0.78 / −55.3% | 28.09% / 0.73 / −56.9% | 19.42% / 0.89 / −35.1% |
| SSO | fuera | 22.62% / 0.69 / −59.3% | 12.80% / 0.54 / −39.3% | 13.78% / 0.58 / −43.9% | (SPY) |
| QLD | fuera | 30.72% / 0.78 / −63.7% | 25.71% / 0.80 / −41.0% | 25.67% / 0.79 / −41.5% | (QQQ) |

Veredicto con ETFs reales, fuera de muestra: "Solo protección" en S&P (SSO/UPRO) y en Nasdaq (QLD/TQQQ), al cierre y con rezago. En el Nasdaq, TQQQ filtrado tiene Sharpe ≥ QQQ (0.82 contra 0.81), pero QLD filtrado queda 0.01 debajo (0.80; 0.79 con rezago) y la regla exige los dos. El filtro reduce el MDD del mismo ETF en UPRO y TQQQ con las dos ejecuciones. Validación del simulador (desde SPY/QQQ, toda la historia): ρ diaria 0.9956 a 0.9989; CAGR sim − real +0.72 (SSO), +1.53 (UPRO), +0.79 (QLD), +1.47 (TQQQ) pp/año.

### Temporadas de 85 días hábiles en MXN (ETFs reales; principal: rezago de 1 día)

| Cartera (MXN) | Desde | n | P(DD ≥ 12%) | P(≥ 20%) | P(≥ 28%) | P(≥ 35%) | p10 | Mediana | p90 | Peor DD |
|---|---|---|---|---|---|---|---|---|---|---|
| 50% UPRO filtrado + 50% SPY | 2009-06-26 | 848 | 30.3% | 8.5% | 0.4% | 0.0% | −9.2% | 7.4% | 22.3% | −28.7% |
| ídem, al cierre | | 848 | 30.7% | 8.7% | 0.0% | 0.0% | −8.6% | 7.0% | 22.2% | −27.7% |
| ídem, en USD | | 848 | 44.3% | 9.4% | 2.0% | 0.0% | −13.3% | 7.4% | 24.1% | −30.9% |
| 50% UPRO sin filtro + 50% SPY | | 848 | 39.4% | 16.2% | 9.9% | 2.7% | −10.3% | 10.4% | 25.6% | −45.7% |
| 100% SPY | | 848 | 13.1% | 0.0% | 0.0% | 0.0% | −4.6% | 5.6% | 14.2% | −19.1% |
| 50% TQQQ filtrado + 50% QQQ | 2010-02-12 | 816 | 62.7% | 19.9% | 4.0% | 0.4% | −12.0% | 10.0% | 30.0% | −35.3% |
| ídem, al cierre | | 816 | 61.9% | 18.1% | 4.9% | 0.4% | −11.9% | 10.7% | 30.1% | −36.0% |
| ídem, en USD | | 816 | 61.9% | 28.8% | 6.0% | 1.7% | −15.1% | 9.4% | 31.2% | −44.3% |
| 50% TQQQ sin filtro + 50% QQQ | | 816 | 69.5% | 29.5% | 11.2% | 8.7% | −11.0% | 14.3% | 32.1% | −47.1% |
| 100% QQQ | | 816 | 16.3% | 5.6% | 0.0% | 0.0% | −4.7% | 8.2% | 18.1% | −25.0% |

El peso amortigua los DD (se deprecia en las caídas de EUA): en MXN, P(DD ≥ 20%) baja de 28.8% a 19.9% en la cartera TQQQ. Es una cobertura observada 2009-2026, no garantizada. Solo 16-17 años de historia real, sin 2000-2002.

## Comparación con A

| Métrica (misma ventana) | A (French/CRSP; SPY/QQQ señal) | B (^SP500TR/DTB3; ^GSPC/^NDX señal) | Diferencia | ¿Dentro de tolerancia (1 pp CAGR, 0.05 Sharpe)? |
|---|---|---|---|---|
| Fuera 2015-11 a 2026-07, 1x B&H | 14.54% / 0.712 / −34.22% | 14.60% / 0.73 / −33.8% | +0.06 pp | Sí |
| ídem, 2x B&H | 22.87% / 0.687 / −59.71% | 23.21% / 0.70 / −59.1% | +0.34 pp | Sí |
| ídem, 3x B&H | 28.40% / 0.695 / −77.18% | 29.28% / 0.71 / −76.6% | +0.88 pp | Sí (límite) |
| ídem, LRS 2x | 15.11% / 0.612 / −37.86% | 15.97% / 0.65 / −40.1% | +0.86 pp; Sharpe +0.04; MDD −2.2 pp | Sí |
| ídem, LRS 3x | 21.02% / 0.649 / −50.96% | 22.44% / 0.69 / −53.3% | **+1.42 pp**; Sharpe +0.04; MDD −2.3 pp | No en CAGR |
| ídem, LRS 2x / 3x con rezago | 15.62% / 21.83% | 14.47% / 20.06% | **−1.15 / −1.77 pp** | No |
| 1990-01 a 2015-10, LRS 2x | 9.49% / 0.385 / −61.79% | 10.67% / 0.42 / −50.8% | **+1.18 pp; MDD +11 pp** | No |
| ídem, LRS 3x | 12.32% / 0.428 / −76.92% | 13.96% / 0.46 / −67.9% | **+1.64 pp; MDD +9 pp** | No |
| ídem, 1x B&H | 9.46% / 0.433 / −54.57% | 9.41% / 0.42 / −55.3% | −0.05 pp | Sí |
| 2000-01 a 2015-10, LRS 2x / 3x | 1.69% / 1.35% | 3.90% / 4.61% | **+2.2 / +3.3 pp** | No |
| UPRO real, filtro ^GSPC (post-hoc de A) | 16.82% / 0.561 / −53.06% | 16.88% / 0.56 / −53.1% | +0.06 pp | Sí |
| TQQQ real, filtro ^NDX (post-hoc de A) | 34.15% / 0.807 / −55.44% | 34.23% / 0.81 / −55.3% | +0.08 pp | Sí |
| UPRO / TQQQ real con señal SPY/QQQ (principal de A), al cierre | 21.52% / 32.13% | 21.58% / 32.21% | +0.06 / +0.08 pp | Sí |
| ídem con rezago | 18.65% (−59.69%) / 31.17% (−61.24%) | 18.71% (−59.4%) / 31.24% (−61.0%) | +0.06 / +0.07 pp | Sí |
| SSO / QLD real, señal SPY/QQQ | 15.58% / 23.78% | 15.64% / 23.85% | +0.06 / +0.07 pp | Sí |
| UPRO, TQQQ, SPY, QQQ B&H fuera | 27.33 / 35.99 / 14.50 / 19.12% | 27.33 / 35.99 / 14.50 / 19.12% | 0 | Sí |
| Simulador: CAGR sim − real (SSO, UPRO, QLD, TQQQ) | +0.72, +1.63, +0.79, +1.56 pp | +0.72, +1.53, +0.79, +1.47 pp | ≤ 0.1 pp (B termina un mes después) | Sí |
| Veredicto fuera de muestra (sim y reales) | Solo protección | Solo protección | — | Concordante |

### Explicación de las diferencias

1. **ETFs reales: concordancia completa.** Con la misma señal que A (SPY/QQQ adjclose), B reproduce los 8 resultados de A dentro de 0.06–0.08 pp de CAGR y 0.3 pp de MDD. El residuo sistemático de +0.06 pp es el efectivo: DTB3 (tasa de descuento a 3 meses) contra la T-bill a 1 mes de French, sobre el ~17% del tiempo fuera del mercado. Lo mismo con la señal de índice de precio (post-hoc de A): +0.06/+0.08 pp. Los B&H coinciden al centésimo: misma fuente (Yahoo adjclose).
2. **Simulado fuera de muestra, LRS 3x +1.42 pp.** Es la diferencia de índice, no de código: French (todo el mercado CRSP) contra S&P 500 TR. (a) La señal cruza en fechas distintas: sobre series casi idénticas, un cruce de 200 días un día antes o después cambia el resultado de un 3x (el mismo efecto que A documenta al pasar de SPY a ^GSPC: 21.5% contra 16.8% en UPRO). (b) French tiene más volatilidad diaria fuera de muestra (18.4% contra 17.9%), lo que añade ≈ 0.5 pp de decaimiento a un 3x. El B&H 3x difiere solo 0.88 pp, y los B&H 1x y 2x menos; el grueso de la brecha en LRS viene de (a).
3. **Rezago fuera de muestra, cambia el signo.** A: el rezago **mejora** el CAGR simulado (21.02% → 21.83% en 3x). B: lo **empeora** (22.44% → 20.06%). En ETFs reales, con señal SPY el rezago cuesta 2.9 pp en UPRO (A y B coinciden), pero con señal ^GSPC lo mejora 1.4 pp (B). *Inferencia:* el efecto del rezago de un día después de 2015 es ruido de fechas de cruce; lo robusto es que el MDD empeora con rezago en todas las versiones (A y B: 3x de ≈ −51/−53% a ≈ −58/−59%).
4. **1990-2015: B da LRS mejor que A en 1.2–1.6 pp y 9–11 pp menos de MDD.** Se concentra en 2000-2015 (A: LRS 3x 1.35%, MDD −76.9%; B: 4.61%, −62.7%). En 2000-2002 el mercado CRSP (con más peso de tecnología y small caps del Nasdaq) tuvo más falsos cruces que el S&P 500. Los B&H 1x coinciden (9.46% contra 9.41%). No es un error de ninguna de las dos.
5. **Dentro de muestra 1928-1988 no es comparable:** ^SP500TR empieza en 1988. B no puede evaluar C1–C6 ni la refutación en la ventana del artículo; solo confirma que en 1988-2015 no hay refutación (LRS 2x 11.94% y Sharpe 0.46 contra 10.10% y 0.45 del 1x; margen de Sharpe 0.01).

## Veredicto de la auditoría

- **Concordante en estado:** "Replicado con diferencias" se sostiene. B no puede probar C1–C6 (no tiene 1928-1988), pero no encuentra refutación en 1988-2015 y reproduce los resultados fuera de muestra y de ETFs reales.
- **Concordante en el veredicto fuera de muestra: "Solo protección"**, simulado (al cierre, con rezago, hasta 2026-07 y hasta 2026-08) y con ETFs reales (S&P y Nasdaq, las dos ejecuciones).
- Diferencias fuera de tolerancia: explicadas por índice (CRSP contra S&P TR) y por la serie que define el cruce. Ninguna apunta a un error de código de A.

## Conclusión operable

1. **Filtro de 200 días en apalancados: se confirma como protección, no como rendimiento.** En UPRO y TQQQ reales fuera de muestra reduce el MDD de −77/−82% a −53/−57% (−58/−57% con rezago), a cambio de 9.0–10.4 pp de CAGR en UPRO y 1.8–2.3 pp en TQQQ frente al ETF comprado y mantenido.
2. **Hay que fijar qué serie define el cruce.** Con la misma regla, UPRO fuera de muestra da 21.6% (señal SPY con dividendos) o 17.5% (señal ^GSPC de precio), y SSO 16.0% o 12.8%. Es un parámetro sin evidencia a favor de ninguno; la regla operativa debe nombrarlo y mantenerlo.
3. **No contar con que el rezago "no cuesta":** su efecto sobre el CAGR tiene signo inestable; su efecto sobre el MDD es consistentemente negativo (≈ 5–7 pp más profundo en 3x).
4. **Para el comité del 2-oct (en MXN, 85 días):** "50% UPRO filtrado + 50% SPY" tocó −20% en 8.5% de las temporadas y −28% en 0.4% (peor −28.7%); "50% TQQQ filtrado + 50% QQQ" tocó −20% en 19.9%, −28% en 4.0% y −35% en 0.4% (peor −35.3%). Con el cortacircuitos de −20%, la versión TQQQ lo activaría en 1 de cada 5 temporadas; la versión UPRO, en 1 de cada 12. Ambas ganan en mediana a su 1x (7.4% contra 5.6%; 10.0% contra 8.2%) con p10 dos veces más negativo. La muestra no incluye 2000-2002 (en el Nasdaq simulado de A, el MDD fue −66% a −74% con 50%).

## Pendientes fuera de esta carpeta (no editados)

- `laboratorio/replicas/R06-apalancados-y-filtro-de-tendencia.md`: agregar la sección "Doble ejecución independiente (2026-09-29)" con la tabla de arriba y el estado sin cambio ("Replicado con diferencias"; fuera de muestra "Solo protección").
- R06 §17.1 dice que el rezago "costó de 1.84 a 3.56 pp por año" en apalancados sobre el S&P. B muestra que con señal ^GSPC el rezago mejoró a SSO y UPRO fuera de muestra (+1.0 y +1.4 pp), y A mismo muestra que el simulado fuera de muestra mejora con rezago. Conviene matizar: el costo del rezago en CAGR no es robusto; el daño en MDD sí.
- R06 §3 registra el cierre nulo de Yahoo del 2026-09-22 en ^GSPC, ^NDX y UPRO; en la descarga del 2026-09-29 ya no aparece (Yahoo lo corrigió). No afecta a ninguna cifra.
