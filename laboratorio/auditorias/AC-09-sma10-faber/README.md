# AC-09: segunda ejecución independiente de R01 (timing SMA de 10 meses de Faber)

> Fase 0, formación. Nada de esto es una recomendación de inversión. Todas las cifras son históricas, en USD salvo donde se indica, antes de impuestos.

| Campo | Valor |
|---|---|
| Réplica auditada (A) | `laboratorio/replicas/R01-timing-sma10-faber.md` (corrida final 2026-09-25T05:30:38Z, French CRSP 202607, fin 2026-07-31) |
| Ejecución independiente (B) | `AC09.py` en esta carpeta. Biblioteca estándar de Python 3.11; de `herramientas/datos.py` solo usa `parsear_yahoo_json` y `parsear_fred_csv`. Lector OLE2/BIFF8 propio para el xls de Shiller. No importa ni copia `R01.py`, `R01_verificacion.py` ni el motor `herramientas/backtest.py` |
| Fecha | 2026-09-30 (descargas a las 17:49 UTC) |
| Comando | `python3 laboratorio/auditorias/AC-09-sma10-faber/AC09.py` (sin red, ~17 s; lee `datos/`, reescribe `datos/SHA256SUMS.txt`, `salida.txt` y `resultados.json`) |
| sha256 de `AC09.py` | `f5ad1cc6ded08afc18584d7f4112d8900aff4b5a92f34f9fe28b8fcff0637476` |

## Protocolo ciego

1. De la ficha R01 leí solo el encabezado y las secciones 1 a 9 (pre-registro).
2. Descargué los datos, escribí `AC09.py` y generé `salida.txt` (bloques B1, B2, B3, significancia y MXN).
3. Después leí las secciones 10 a 16 de R01 para la comparación. No leí `R01.py`, `R01-salida.txt`, `R01-resultados.json` ni `R01-variantes.csv`; las cifras de A salen de las secciones 10 a 12 de la ficha.

Después de leer A agregué a `AC09.py` solo la función `conciliacion` (al final de la salida): fechas de los MDD, un **control C** (el código de B sobre el zip French 202607 de A, copiado a `datos/` con el mismo sha256 `b840dba5…`), la lista de meses con señal distinta y una descomposición señal × rendimientos. Se verificó con `diff` que todas las líneas anteriores de `salida.txt` quedaron idénticas.

## Fuentes (B usa una fuente distinta de A)

| Serie | Uso en B | Fuente exacta | Rango usado | sha256 |
|---|---|---|---|---|
| Shiller `ie_data.xls` | Dividendos D (anualizados, /12 por mes) antes de 1988; precio promedio P en la sensibilidad B3 | shillerdata.com (`img1.wsimg.com/.../70fec4f5-.../ie_data.xls?ver=1788371540009`), guardado 2026-09-02 | P 1871-01 a 2026-09; D hasta 2026-06 | `044196da…89c1` |
| `^GSPC` | Cierre de fin de mes (precio) 1927-12 a 1988-01; señal de precio (bloque F) | Yahoo chart v8, `period1=-2208988800&period2=4102444800&interval=1d` | 1927-12 a 2026-08 | `89528b5e…b255` |
| `^SP500TR` | Rendimiento total desde 1988-02 | Yahoo, misma URL (diario desde 1988-01-04) | 1988-01 a 2026-08 | `18d373c8…7193` |
| `^SP500TR` range=30y | Control: descarga pedida con `range=30y&interval=1d` y `interval=1mo` | Yahoo | 1996-09 a 2026-09 | `b8e9af31…fee0` / `110e1bf3…a3f` |
| TB3MS | rf desde 1934 (tasa del mes / 1200) | FRED | 1934-01 a 2026-08 | `ebf04b1a…6ae6ab` |
| M1329AUSM193NNBR | rf 1920-1933 (NBER, T-bills y certificados 3-6 meses) | FRED | 1920-01 a 1933-12 | `9025de20…7320` |
| DEXMXUS | MXN: último dato ≤ fin de mes, máximo 10 días | FRED | 1993-12 a 2026-07 | `0b71c05f…e4b` |
| INTGSTMXM193N | Cetes aproximados (tasa/1200 del mismo mes) | FRED | 1994-01 a 2026-07 | `6ffbf4e5…9e22` |
| French 202607 | **Solo control C**, después de leer A | copia de `replicas/R01-datos/202607/` | — | `b840dba5…f5eb` |

Hashes completos en `datos/SHA256SUMS.txt`. La barra de Yahoo del 2026-09-30 es intradía: se usa hasta 2026-08. El cierre de fin de mes de `^SP500TR` es idéntico en la descarga `range=30y` y en la de `period1` (diferencia máxima 0 en 360 meses). En el traslape 1988-02 a 2026-06, `^GSPC` + dividendos de Shiller rinde 11.41% anual contra 11.49% de `^SP500TR`. Condiciones de uso de Yahoo y Shiller: no verificadas.

## Definiciones de B (escritas desde el pre-registro)

- **B1 (principal):** r_t = cierre `^GSPC`_t / cierre_{t−1} − 1 + (D_t/12)/cierre_{t−1} hasta 1988-01; r_t de `^SP500TR` desde 1988-02. Índice TR I construido desde 1927-12. B2 usa `^GSPC` + D en todo el periodo; B3 usa Shiller puro, (P_t + D_t/12)/P_{t−1} con P promedio mensual (sesgado a favor del timing, ver abajo).
- Señal: w_t = 1 si I_{t−1} > media(I_{t−10}, …, I_{t−1}); empate = 0. Rezago: con I_{t−2}. mom12: I_{t−1} > I_{t−13}.
- r_estrategia = w·r + (1−w)·rf − |Δw|·costo; costo por defecto 0.34% por lado; exposición inicial 0. Una corrida continua, recortada por segmento.
- Primera decisión: 1929-01 (12 rendimientos previos, como `min_historia = 12`). **A empieza en 1927-07**; B no tiene cierres de fin de mes antes de 1927-12.
- Segmentos: dentro 1929-01 a 2006-12; fuera 2007-01 a 2026-07 (ventana de A) y a 2026-08; artículo 1929-01 a 2005-12 sin costos.
- CAGR = ∏(1+r)^(12/n) − 1; vol = sd mensual × √12; Sharpe = media/sd del exceso mensual sobre rf × √12; MDD sobre la curva mensual (incluye el valor inicial).
- Significancia: t Newey-West(6) de la diferencia mensual sma10 − B&H; IC95 bootstrap de bloques de 12 meses (5000, semilla 9) de ΔSharpe; DSR (Bailey-López de Prado) con V[SR] de los 5 ensayos, N = 5 y 20.
- MXN: señal en USD (B1); r_MXN = (1 + r_USD)·FX_t/FX_{t−1} − 1. Sharpe en MXN sobre Cetes (A lo mide sobre el efectivo de cada corrida; no son comparables).

## Resultados de B (B1, neto de 0.34% por lado)

| Segmento | Variante | CAGR | Vol | Sharpe | MDD | Invertido | Cambios |
|---|---|---|---|---|---|---|---|
| Dentro 1929-01 a 2006-12 | Comprar y mantener | 9.68% | 19.19% | 0.381 | −83.14% | 100% | — |
| | sma10 | 8.91% | 13.04% | 0.432 | −54.33% | 70.8% | 108 |
| | sma10 con rezago de 1 mes | 8.27% | 13.24% | 0.383 | −57.67% | 70.8% | |
| Fuera 2007-01 a 2026-07 | Comprar y mantener | 10.96% | 15.46% | 0.654 | −50.95% | 100% | — |
| | **sma10** | **7.91%** | 10.80% | **0.617** | −22.93% | 79.1% | 32 |
| | sma10 con rezago | 9.39% | 11.45% | 0.710 | −19.86% | | |
| | sma10, señal `^GSPC` precio | 8.55% | 10.64% | 0.680 | −22.93% | | |
| | sma6 / sma8 / sma12 / mom12 | 9.78 / 9.27 / 8.63 / 9.88% | | 0.809 / 0.741 / 0.666 / 0.711 | −15.5 / −22.9 / −17.6 / −19.9% | | |
| | sma10 con 0.68% por lado | 7.31% | | 0.563 | −24.54% | | |
| Fuera a 2026-08 | sma10 contra B&H | 8.03% contra 11.07% | | 0.627 contra 0.660 | −22.93% contra −50.95% | | |

- **Criterios (tramo artículo 1929-01 a 2005-12, sin costos):** C1 reducción del MDD 0.355 (cumple); C2 −0.27 pp (no cumple); C3 0.705 (cumple); C4 0.70 salidas/año (cumple). Refutación: no (reducción neta 0.347; Sharpe 0.432 contra 0.381). **Estado B: Replicado con diferencias.**
- **Veredicto fuera de muestra B: "Solo protección"** (reducción del MDD 0.550 ≥ 0.20, pero Sharpe 0.617 < 0.654). Igual hasta 2026-08 (0.627 < 0.660).
- **Significancia:** sma10 − B&H: −0.140%/mes (t NW6 −1.07) dentro; −0.285%/mes (t −1.24) fuera. ΔSharpe +0.051 [−0.134, +0.258] dentro; −0.037 [−0.449, +0.440] fuera. DSR dentro 0.999 (N = 5) y 0.998 (N = 20), contra 0, no contra el índice.
- **B3, Shiller puro (precio promedio):** da "Replicado" y "Se sostiene" (C2 +1.69 pp; fuera Sharpe 0.966 contra 0.749), pero con un mes de rezago el CAGR dentro cae de 11.46% a 9.09%. El promedio mensual autocorrelaciona los rendimientos y regala al timing parte del mes de la señal: **no sirve para evaluar la regla**. *Inferencia no verificada:* si el artículo usó alguna serie promediada antes de 1971, eso explicaría parte de su +0.91 pp.
- **MXN (1994-01 a 2026-07):** fuera de muestra, B&H 13.67% (MDD −31.22%); sma10 con salida a T-bill USD 10.55% (MDD −31.16%, reducción ≈ 0); con salida a Cetes 12.00% (MDD −19.74%, reducción 0.368). En 1994-2006, sma10 con Cetes 25.41% contra B&H 22.07%.

## Comparación con A

Tolerancia: 1 pp de CAGR, 0.05 de Sharpe. Las cifras de A son de la ficha R01 §10-§12.

| Métrica | A (French CRSP 202607) | B (S&P: `^GSPC`+Shiller / `^SP500TR`) | Dif. | ¿En tolerancia? |
|---|---|---|---|---|
| Fuera, B&H: CAGR / vol / Sharpe / MDD | 11.02% / 15.91% / 0.645 / −50.31% | 10.96% / 15.46% / 0.654 / −50.95% | −0.06 pp; +0.009 | Sí |
| Fuera, sma10: CAGR / Sharpe | 8.85% / 0.699 | 7.91% / 0.617 | −0.94 pp; **−0.082** | CAGR sí (límite); **Sharpe no** |
| Fuera, sma10: MDD / cambios | −19.31% (2018-09 a 2019-08) / 30 | −22.93% (2021-12 a 2023-02) / 32 | −3.6 pp | No |
| Fuera, veredicto pre-registrado | **Se sostiene** | **Solo protección** | — | **No concordante** |
| Fuera, sma10 con rezago | 9.45% / 0.692 / −21.53% | 9.39% / 0.710 / −19.86% | −0.06 pp; +0.018 | Sí |
| Fuera, sma10 señal `^GSPC` | 8.48% / 0.659 / −24.17% | 8.55% / 0.680 / −22.93% | +0.07 pp; +0.021 | Sí |
| Fuera, sma8 / sma12 / mom12 Sharpe | 0.790 / 0.636 / 0.615 | 0.741 / 0.666 / 0.711 | −0.05 / +0.03 / **+0.10** | mom12 no (definición distinta, ver 4) |
| Dentro, B&H (A 1927-07; B 1929-01) | 10.07% / 0.408 / −83.65% | 9.68% / 0.381 / −83.14% | ventana distinta | Ver control C |
| Dentro, sma10 (A 1927-07; B 1929-01) | 9.31% / 0.472 / −43.50% | 8.91% / 0.432 / −54.33% | ventana distinta | Ver control C |
| Dentro 1929-01 a 2006-12, sma10: A-datos (control C) contra B | 8.78% / 0.436 / −43.50% | 8.91% / 0.432 / −54.33% | +0.13 pp; −0.004; **MDD −10.8 pp** | CAGR y Sharpe sí; **MDD no** |
| C1 reducción MDD (artículo, sin costos) | 0.487 | 0.355 | −0.13 | Ambos dentro de [0.30, 0.60] |
| C2 dif. CAGR (artículo, sin costos) | −0.216 pp | −0.27 pp | −0.05 pp | Sí (ambos fallan C2) |
| C3 / C4 | 0.713 / 0.74 | 0.705 / 0.70 | | Sí |
| Refutación dentro | No | No | | Concordante |
| Estado pre-registrado | Replicado con diferencias | Replicado con diferencias | | Concordante |
| t NW6 sma10 − B&H dentro / fuera | −1.03 / −0.94 | −1.07 / −1.24 | | Sí (ninguno significativo) |
| ΔSharpe IC95 bootstrap dentro / fuera | [−0.134, +0.275] / [−0.348, +0.523] | [−0.134, +0.258] / [−0.449, +0.440] | | Sí (todos incluyen 0) |
| DSR sma10 dentro, N = 5 / 20 | 0.9996 / 0.9987 | 0.999 / 0.998 | | Sí |
| MXN fuera, salida a Cetes: CAGR / MDD / reducción | 12.64% / −14.31% / 0.523 | 12.00% / −19.74% / 0.368 | −0.64 pp; −5.4 pp | CAGR sí; MDD no |
| MXN fuera, salida a T-bill USD: reducción MDD | 0.199 | ≈ 0.00 | | Mismo signo cualitativo (< 0.20) |
| MXN 1994-2006, sma10 con Cetes | 20.56% | 25.41% | **+4.85 pp** | No |

### Explicación de las diferencias

1. **El código no es la causa.** El control C (código de B sobre el zip French 202607 de A, decisiones desde 1927-07) reproduce a A: dentro 9.31% / 0.472 / −43.50% y fuera 8.85% / 0.699 / −19.33% (A −19.31%); C1 0.4867 y C2 −0.216 pp, idénticos. Toda diferencia de abajo viene de la fuente (S&P 500 contra mercado CRSP) o de la ventana.
2. **Fuera de muestra, 4 meses de señal deciden el veredicto.** La señal sma10 del S&P y la de CRSP difieren en 2009-06, 2016-01, 2022-02 y 2022-04. En los cuatro, el índice estaba a menos de 2.3% de su media: el S&P (dominado por las grandes, sobre todo en 2022) seguía arriba mientras el mercado amplio ya estaba abajo. B se quedó dentro en febrero y abril de 2022 (−3.0% y −8.7%) y en enero de 2016 (−5.0%). Descomposición: señal French sobre rendimientos del S&P da 8.92% / Sharpe 0.722 / MDD −17.6%; señal S&P sobre rendimientos French da 7.79% / 0.592 / −24.2%. **La diferencia es de señal, no de rendimientos.** Con la misma regla, el margen de Sharpe fuera de muestra (A +0.054) cambia de signo (B −0.037) por cuatro cruces al filo.
3. **MDD dentro de muestra (−54.33% contra −43.50%).** En mayo y junio de 1930 el S&P estaba 0.3% arriba de su media y CRSP 2.3–2.8% abajo; B se quedó dentro en junio de 1930 (−16.1%). El resto de los 25 meses distintos (de 936) casi no mueve CAGR ni Sharpe (+0.13 pp y −0.004). La reducción del MDD sigue en el rango C1 (0.355), pero más cerca del borde.
4. **Ventana.** B empieza en 1929-01 (sin cierres de fin de mes antes de 1927-12); A en 1927-07 e incluye el alza de 1927-1928. Por eso los niveles dentro de muestra se comparan con el control C recortado a 1929-01. mom12: B usa I_{t−1} > I_{t−13}; A no define la fórmula en el pre-registro (en el control C, B da 9.34%/0.655 fuera contra 8.75%/0.615 de A con los mismos datos), así que es diferencia de definición, no de fuente. No afecta a sma10.
5. **MXN 1994-2006 (+4.85 pp).** La señal difiere en 1994-08 y 1994-12: B (S&P) estaba dentro en diciembre de 1994, el mes de la devaluación, cuando el peso pasó de ~3.4 a ~5 por dólar. Estar en acciones en USD ese mes, en lugar de Cetes, suma ≈ 45% en MXN, ≈ 3 pp al año en 13 años. Es un solo evento; no es un error de ninguna de las dos.
6. **Rf.** B usa T-bill a 3 meses (TB3MS) y NBER antes de 1934; A usa T-bill a 1 mes de French. Efectivo fuera de muestra 1.55% contra 1.51%: efecto < 0.05 pp.

## Veredicto de la auditoría

- **Estado pre-registrado: concordante, "Replicado con diferencias"** (C1, C3 y C4 se cumplen; C2 falla; sin refutación) en A y en B.
- **Veredicto fuera de muestra: no concordante.** A "Se sostiene"; B "Solo protección". Rige el más conservador: **"Solo protección"**. El pre-registro (§2) lleva entonces la regla R1 de "se confirma" a **"se modifica": se mantiene solo como control de drawdown**, con su costo de CAGR declarado (−2.2 pp en A, −3.0 pp en B fuera de muestra, neto). En la práctica, la conclusión operable de R01 ya decía eso (§ Conclusión operable, punto 1); lo que cambia es que el Sharpe fuera de muestra deja de contarse como a favor.
- **Lo robusto en las dos fuentes:** la reducción del MDD (A 0.616, B 0.550 fuera de muestra; ≥ 0.35 dentro), el costo en CAGR, la no significancia del rendimiento medio y que en MXN la protección exige salir a pesos.
- **Lo frágil:** el signo de ΔSharpe fuera de muestra depende de la serie (S&P contra CRSP) y de cuatro cruces dentro de ±2.3% de la media. En B, las seis variantes vecinas (sma6, sma8, sma12, mom12, rezago de 1 mes y señal de precio `^GSPC`) sí superan el Sharpe del índice fuera de muestra (0.666 a 0.809 contra 0.654); la pre-registrada no (0.617). En A pasa lo contrario con sma12 y mom12.
- **Estado de la doble ejecución: Replicado con diferencias.** La etiqueta de R01 no cambia (oportunidad investigable, por la propiedad (b): reducir caídas fuera de muestra, ahora con segunda fuente).
