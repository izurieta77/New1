# AC-14: doble ejecución independiente de V04 con segunda fuente (benchmarks en pesos y SMA10 con señal en MXN)

> Fase 0, formación. Nada de esto es una recomendación de inversión. Son cifras históricas, antes de impuestos, de índices y ETFs convertidos a MXN. El dueño tiene SPYM (S&P 500) en GBM, así que esta auditoría importa por dos razones: (1) fija la **meta en MXN** contra la que se mide esa posición y (2) dice si la SMA10 con señal en MXN sirve como **regla de salida**.

| Campo | Valor |
|---|---|
| Réplica auditada (A) | `laboratorio/replicas/V04-benchmarks-en-pesos-y-sma10-senal-mxn/` (`reproducir.py`, corrida del 2026-09-25; datos congelados en su `datos/`) |
| Ejecución independiente (B) | `AC14.py` (Python 3, solo stdlib, <2 s, sin red). Escribí desde cero los lectores (Yahoo, FRED/ALFRED, Banxico, French), los cierres de mes E/F, el índice de CETES (por subasta y mensual), la señal, la ejecución T0/T1, los costos, las métricas y el Newey-West. No usa `herramientas/` ni importa `reproducir.py` ni `independiente.py`, y no los abrí |
| Fecha | 2026-10-07 (descarga entre 17:51 y 17:56 UTC; `datos/descarga_utc.txt`, `datos/SHA256SUMS.txt`) |
| Comando | `python3 -I laboratorio/auditorias/AC-14-V04/AC14.py > laboratorio/auditorias/AC-14-V04/salida.txt` (reproduce `salida.txt` byte a byte y escribe `resultados.json`) |
| sha256 | `AC14.py` `3332c41f…572c2e`; `salida.txt` `af7a16bf…fbb467`; `resultados.json` `00aea19a…4cbd` |

## Protocolo y límite de la ceguera

1. De V04 leí el pre-registro (§1-§9) y la tabla de desviaciones. **No abrí `reproducir.py` ni `independiente.py`.**
2. **No fue ciega en las cifras.** El encargo ya traía las cifras objetivo (13.97%, 6.37%, 6.11%, t 0.55), y el README de V04 las repite en el Resumen, que leí junto con el pre-registro. Después de la primera corrida consulté `resultados.json` de A, que solo contiene resultados, para explicar una diferencia de t (0.346 contra 0.345, ver diferencia 1).
3. Después de la primera corrida **no cambié ninguna definición** de señal, alineación, costos ni métricas. Solo agregué diagnósticos (meses con señal distinta, parejas MXN/USD, recorte al 08-31) y más decimales en la salida.
4. Diseño: el **mismo código B** corre sobre cinco configuraciones. "A-datos" aísla el código. B1 y B2 son la segunda fuente. B3 y B4 aíslan, por separado, el tipo de cambio y el activo.

## Datos: qué es segunda fuente y qué no

| Serie | Origen (descarga 2026-10-07) | Uso en B | ¿Distinta de V04? |
|---|---|---|---|
| **French diario, Mkt-RF + RF (CRSP VW)**, vintage 202608 | `mba.tuck.dartmouth.edu/.../F-F_Research_Data_Factors_daily_CSV.zip`, sha `2f29e225…a7db`, la misma que bajó AC-13 | Activo en USD con rendimiento total (B1, B2, B4) | **Proveedor y universo distintos** (CRSP, todo el mercado de EUA, sin gasto de ETF) frente a SPY `adjclose` de Yahoo (S&P 500 con gasto de 0.0945%). Termina el 2026-08-31 |
| **Banxico FIX SF43718** | SIE, exportación CSV pública (CF102) | Tipo de cambio (B1, B3) | **Proveedor distinto** de FRED DEXMXUS, que es el principal de V04. V04 usó el FIX solo como sensibilidad, con otra descarga |
| ALFRED DEXMXUS, vintage 2026-10-07 | `alfred.stlouisfed.org/graph/alfredgraph.csv?id=DEXMXUS` | Tipo de cambio (B2) | **Misma fuente, otra vintage.** Hasta 2026-09-18 coincide en todas las fechas y valores con la de A |
| **Banxico SF282**, CETES 28 promedio mensual | SIE, CF107 | Efectivo y benchmark (B1) | **Serie distinta** del mismo proveedor (A usa la subasta semanal SF43936) |
| **FMI INTGSTMXM193N** vía ALFRED | T-bills de México, mensual | Efectivo y benchmark (B2) | **Proveedor distinto** (FMI/IFS). Falta 2026-08 y se arrastra la tasa de julio |
| Banxico SF43936 (descarga nueva) | SIE, CF107 | Efectivo (B3) | Misma serie que A, otra descarga |
| Yahoo NAFTRAC.MX (descarga nueva) | chart v8 | A2 (IPC) | **Misma fuente** que A |
| ALFRED SPASTT01MXM661N (OECD, precios de acciones de México) | mensual, promedio del mes, sin dividendos | Contraste de precio del IPC | **Proveedor distinto**, pero solo de precio |
| FRED SP500 | copia de `AC-13-R09/datos/fred_SP500.csv` (misma sha) | Control del nivel del S&P 500 (precio, 2016+) | Proveedor distinto, solo 10 años y solo precio |

**Límites.** (1) FRED `fredgraph.csv` falló hoy (HTTP/2 INTERNAL_ERROR); se usó ALFRED. ALFRED `SP500` devolvió 0 bytes. (2) No hay segundo proveedor del **S&P 500 con dividendos** para 1993-2026: Stooq y shillerdata.com cortan la conexión, y `^SP500TR` es de Yahoo, igual que SPY. Por eso la segunda fuente del activo es **otro índice** (CRSP VW), no otra medición del S&P 500. (3) Para el **IPC con dividendos** no hay segunda fuente: S&P DJI respondió 403 en V04, y la OECD solo da precio.

## Comparación A contra B

"B código, datos A" es AC14.py sobre los archivos congelados de V04. B1 es la configuración de segunda fuente principal.

| Cifra (2008-2026 = 2008-01 a 2026-08) | A (V04) | B código, datos A | **B1** French × FIX; CETES SF282 | B2 French × DEXMXUS (ALFRED); CETES FMI | B3 SPY × FIX; SF43936 | A − B1 |
|---|---|---|---|---|---|---|
| **S&P TR en MXN, W1** (2007-12-31 a 2026-08-31) | **13.97%** | 13.97% | **14.16%** | 14.16% | 13.97% | −0.19 pp |
| S&P TR en MXN, W2 / W4 | 14.47% / 14.10% | 14.47% / 14.10% | 14.67% / 14.33% | 14.68% / 14.33% | 14.47% / 14.10% | −0.20 / −0.23 pp |
| S&P TR en USD, W1 | 11.29% | 11.29% | 11.48% | 11.48% | 11.29% | −0.19 pp |
| Rango según el inicio (2007-01 a 2009-12) | 13.4% a 17.2% | 13.41% a 17.18% | 13.62% a 17.31% | 13.62% a 17.30% | 13.41% a 17.19% | ≈ −0.2 pp |
| **CETES 28, W1** | **6.37%** | 6.37% | **6.36%** | 6.36% | 6.37% | +0.01 pp |
| **IPC vía NAFTRAC `adjclose`** (2008-01-02 a 2026-08-31) | **≥ 6.11%** | 6.11% | 6.11% (descarga nueva; los mismos 6 años sin dividendos) | — | — | 0 |
| Año 2008, USD / MXN (fechas fijas) | −36.8% / −19.9% | −36.8% / −19.9% | −36.5% / −19.5% | −36.5% / −19.5% | −36.8% / −19.9% | ≤ 0.4 pp |
| S&P MXN − CETES, ×12 y t NW6 | +7.8 pp, t 2.39 (apoyo) | +7.84, 2.39 | +8.09, 2.40 (apoyo) | +8.08, 2.39 | +7.85, 2.40 | 0.01 de t |
| **SMA10-MXN-T1: CAGR / MDD** | **15.50% / −12.7%** | 15.50% / −12.7% | **15.27% / −13.0%** | 15.17% / −13.0% | 15.37% / −12.8% | +0.23 pp / +0.3 pp |
| Comprar y mantener T1: CAGR / MDD | 13.97% / −29.5% | 13.97% / −29.5% | 14.27% / −28.5% | 14.26% / −28.4% | 13.98% / −29.7% | −0.30 pp / −1.0 pp |
| SMA10-MXN-T0 / comprar y mantener T0 | 15.23% / −12.2% contra 13.97% / −28.4% | igual | 15.05% / −12.7% contra 14.16% / −27.6% | 15.02% / −12.9% contra 14.16% / −27.5% | 15.33% / −12.1% contra 13.97% / −28.5% | — |
| SMA10-MXN-T1: volatilidad / Sharpe (contra CETES) | 11.55% / 0.772 | 11.55% / 0.772 | 11.55% / 0.756 | 11.80% / 0.735 | 11.16% / 0.785 | 0.016 de Sharpe |
| SMA10-MXN-T1: cambios de señal | 18 | 17 (otra convención, ver 2) | 19 | 19 | 19 | — |
| **Dif. SMA10-MXN-T1 − comprar y mantener, ×12, t NW6** | **+0.99 pp, t 0.55** (inconcluso) | +0.987, t 0.548 | **+0.48 pp, t 0.26** (inconcluso) | +0.40, t 0.21 | +0.85, t 0.47 | 0.29 de t |
| Igual, 1995-2007 / 1995-2026 | t 0.34 / 0.64 | t 0.346 / 0.642 | t 0.68 / 0.64 | t 0.71 / 0.62 | t 0.38 / 0.60 | — |
| Igual con T0, 2008-2026 | +0.84, t 0.46 | +0.84, t 0.46 | +0.49, t 0.26 | +0.47, t 0.25 | +0.91, t 0.50 | — |
| SMA10-USD-T1, 2008-2026 | 12.16% (pierde contra 13.97%) | 12.16% | 12.79% (pierde contra 14.27%) | 12.75% | 12.13% | −0.63 pp |
| **1995-2007, SMA10 T1, señal USD contra MXN** | 20.8% / −10.8% contra 18.3% / −19.0% | igual | **19.9% / −10.4% contra 19.4% / −10.4%** | 19.6% / −11.0% contra 19.5% / −11.0% | 20.6% / −10.1% contra 18.3% / −18.1% | ver 4 |
| 16 variantes: MDD 2008-2026 (comprar y mantener T0 / T1) | −10.4% a −21.7% (−28.4 / −29.5) | igual | −10.8% a −17.3% (−27.6 / −28.5) | −10.6% a −17.1% | −11.0% a −21.8% | todas reducen MDD |
| 16 variantes: MDD 1995-2007 | −8.7% a −20.4% (−39.9 / −36.3) | igual | −9.4% a −15.3% (−39.2 / −36.9) | −9.1% a −15.5% | −9.0% a −20.3% | todas reducen MDD |
| Parejas 2008-2026: señal MXN con más CAGR que USD | 8 de 8 | 8 | 8 | 8 | 8 | 0 |
| Parejas 1995-2007: USD con más CAGR / con menor MDD | 6 de 8 / 8 de 8 | 6 / 8 | **4 / 2** | 4 / 2 | 6 / 8 | ver 4 |
| **Estado / conclusión operable** | Replicado con diferencias; control de riesgo, no fuente de rendimiento | igual | igual | igual | igual | — |

**El código B con los datos A reproduce a A.** En las 18 combinaciones de corrida y segmento de `resultados.json` de A (SMA10 MXN/USD, T0/T1, comprar y mantener; 2008-2026, 1995-2007, completo), CAGR, volatilidad, MDD, Sharpe y tiempo invertido coinciden con diferencia máxima de **4.8e-13**. Benchmarks, sensibilidad de inicio, 2008, NW y rangos de las 16 variantes coinciden al redondeo impreso.

**Controles de fuente.** El FIX contra DEXMXUS (A) difiere en 7,981 fechas comunes: mediana de la diferencia absoluta 0.055%, p90 0.19% y máximo 2.97% (días de mucha volatilidad, por la hora de fijación). FRED SP500 contra Yahoo `^GSPC`: 2,504 fechas, 2 con diferencia mayor a 0.01% (máximo 0.12%). S&P precio en MXN, 2016-10 a 2026-08: 12.76% (FRED × FIX) contra 12.81% (Yahoo × DEXMXUS). La OECD (precio, promedio mensual) da 4.28% para México de dic-2007 a ago-2026; `^MXX` precio (A) da 4.35%. Las dos son de precio, y NAFTRAC con 6.11% queda arriba de ambas, como debe.

## Diferencias explicadas

1. **t NW de 0.346 contra 0.345 (1995-2007) y de 0.548 contra 0.547 (2008-2026), con los datos A.** La media es igual a 4 decimales. El cociente de las t es exactamente √(156/155) y √(224/223): A divide las autocovarianzas entre T−1 y B entre T. **Convención, no error.**
2. **Número de cambios de señal (+1 en A en todas las corridas).** A cuenta también el cambio de la posición en el primer mes del segmento respecto del mes anterior, o la entrada inicial. B solo cuenta los cambios dentro del segmento. Convención, sin efecto en costos ni en ninguna métrica.
3. **S&P TR en MXN 14.16% (B1) contra 13.97% (A): −0.19 pp, dentro de la tolerancia de ±0.30 pp.** La causa es **el activo**, no el tipo de cambio ni el código. B3 (SPY × FIX) da 13.97% y B4 (French × DEXMXUS de A) da 14.16%. En USD la brecha es la misma (11.48% contra 11.29%). Descomposición: el gasto de SPY (0.0945%) explica ≈0.08 pp, porque `^SP500TR` da 14.05% en V04. El resto (≈0.11 pp) es el universo: CRSP VW incluye medianas y Nasdaq, y el S&P 500 solo grandes. **Para SPYM, que replica el S&P 500, la meta pertinente sigue siendo la de A:** entre 13.97% (SPY, con su gasto) y 14.05% (índice sin gasto). La cifra de French es del mercado total, no del S&P 500.
4. **SMA10-MXN: la ventaja de CAGR sobre comprar y mantener baja de +1.53 pp (A) a +1.00 pp (B1) en 2008-2026, y la t, de 0.55 a 0.26.** La causa son **meses de señal al filo de la media**. Con el mismo código, B1 cambia la señal en 10 meses respecto de A: 2000-03, 2000-10, 2000-11, 2002-04, 2002-05, 2004-09, 2005-11, 2010-08, 2011-10 y 2025-07. En nueve de ellos el margen P/SMA10 − 1 de A es menor que 1% en valor absoluto (de −0.05% a +0.94%, salvo 2002-05 con −1.67%). Solo cambiar FX (B3) mueve 2 meses (2010-06 y 2018-04); solo cambiar el activo (B4) mueve 9. El mes grande es **2000-03**: A −0.05% (fuera) contra B1 +7.38% (dentro), porque en feb-2000 Nasdaq, incluido en CRSP, subió con fuerza mientras el S&P 500 bajaba. Eso explica también el cambio de **1995-2007**. La MDD de SMA10-MXN-T1 pasa de −19.0% en A (1999-07 a 2000-12) a −10.4% en B1 (1995-04 a 1995-05), y la comparación USD contra MXN de 1995-2007 se empata (4/8 en CAGR; la señal USD solo tiene menos caída en 2 de 8 parejas, contra 8 de 8 en A). **La conclusión de V04 "en 1995-2007 la señal en USD fue mejor" depende del índice.** Con el S&P 500 (A, B3) se sostiene; con CRSP VW (B1, B2, B4) no. La que no depende de la fuente es la de 2008-2026: la señal MXN supera a la USD en 8 de 8 parejas con todas las configuraciones.
5. **Comprar y mantener T1: 14.27% / −28.5% (B1) contra 13.97% / −29.5% (A).** Pesan el activo (punto 3) y un recorte de un día. French termina el 2026-08-31, así que el último periodo T1 de B1, B2 y B4 cierra el 08-31 y no el 09-01. Con los datos A recortados igual: SMA10-MXN-T1 da 15.57% (+0.07) y comprar y mantener 14.03% (+0.06), con diferencia y t idénticas (+0.987 pp, t 0.548), porque las dos estaban invertidas en agosto de 2026. La caída de comprar y mantener T1 es −28.5% con FIX y −29.7% con SPY × FIX: el activo pesa más que el tipo de cambio.
6. **CETES 6.36% (SF282 y FMI) contra 6.37% (SF43936).** El promedio mensual aplicado con interés simple dentro del mes y capitalización mensual da 0.01 pp menos que la acumulación por subasta semanal. El FMI coincide con SF282, porque su serie de México es el promedio mensual de CETES 28. El arrastre de jul-2026 a ago-2026 en la serie del FMI no se nota al redondeo. Sin efecto.
7. **2008 en MXN, −19.5% (B1) contra −19.9% (A).** Por el universo (CRSP VW cayó 36.5% contra 36.8% del SPY) y el tipo de cambio. La conclusión de V04 (el contraste correcto es −36.8% contra −19.9%, no −47% contra −21.6%) no cambia.
8. **Vintage de DEXMXUS.** ALFRED 2026-10-07 y la descarga de A coinciden en todas las fechas hasta el 2026-09-18. B2 y B4 dan lo mismo a 2 decimales, salvo por el CETES del FMI.

## Errores propios (de B)

- Ninguno que cambiara cifras. La primera corrida ya daba las cifras de A con los datos A. Los cambios posteriores fueron diagnósticos y formato. Se borró un archivo vacío (`alfred_SP500.csv`, 0 bytes) que la primera versión listaba en las huellas.

## Hallazgos sobre la documentación de A (anotados en `conocimiento/registro-de-errores.md`)

- La tabla maestra decía "872 cifras cotejadas". Son **871**: `independiente-comparacion.csv` tiene 872 líneas contando el encabezado, y el README de V04 dice 871.
- La tabla maestra (fila de requisitos) decía "No (mismos datos; código independiente)" para la segunda fuente. Desde AC-14 es "Sí, con límite" (otro índice, no otro proveedor del S&P 500; IPC sin segunda fuente).
- Discrepancia entre fuentes, no error de cálculo: "en 1995-2007 la señal en USD fue mejor (20.8% / −10.8% contra 18.3% / −19.0%) y tuvo menos caída en 8 de 8 parejas" solo vale con el S&P 500. Con CRSP VW las dos señales empatan (19.9% / −10.4% contra 19.4% / −10.4%; 2 de 8 parejas).

## Conclusión

- **Metas en MXN (W1, 2007-12-31 a 2026-08-31, antes de impuestos): se confirman con segunda fuente.** S&P TR 13.97% (A, S&P 500 vía SPY) contra 14.16% (CRSP VW × FIX); la diferencia es de índice y queda dentro de ±0.30 pp. CETES 6.37% contra 6.36% (otra serie y otro proveedor). IPC ≥ 6.11%: misma cifra con una descarga nueva, pero **sin segunda fuente con dividendos**. Para medir SPYM, usar 13.97%-14.05%, no la cifra de French.
- **SMA10-MXN: se confirma la reducción de MDD y que no hay ventaja de rendimiento significativa.** En B1 la MDD baja de −28.5% a −13.0% (T1), y las 16 variantes reducen la caída en los dos subperiodos con las cuatro configuraciones. La ventaja de rendimiento es aún más débil que en A (+0.48 pp ×12, t 0.26 contra t 0.55), y la señal depende de meses al filo de la media, que cambian con el proveedor del índice o del tipo de cambio. Para el dueño: como regla de salida de SPYM sería **control de riesgo**, no fuente de rendimiento. Una señal calculada con otro tipo de cambio (FIX en vez de DEXMXUS) habría operado distinto en 2 de 224 meses.
- **Qué no se verificó.** DSR (N = 16), A4 por caída diaria y de crisis, ventanas post-hoc de 2007, SPY.MX/IVV.MX, NAFTRAC con dividendos imputados (EWW), retención de 30% y costos alternativos. Tampoco el listado de SPYM en el SIC ni su gasto.
- **Estado:** se confirma **"Replicado con diferencias"**. A y B coinciden en el veredicto de cada pregunta pre-registrada. La única conclusión secundaria que no se sostiene con la segunda fuente es "la señal USD fue mejor en 1995-2007". **Etiqueta: oportunidad investigable** (sin cambio). Es la más conservadora de A y B: ninguna muestra ventaja de rendimiento, y las dos muestran la propiedad de reducir caídas.
