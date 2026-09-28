# AC-06: segunda ejecución independiente de R05 (portafolios con volatilidad gestionada)

> Fase 0, formación. Nada de esto es una recomendación de inversión. Todas las cifras son históricas.

| Campo | Valor |
|---|---|
| Réplica auditada (A) | `laboratorio/replicas/R05-portafolio-volatilidad-gestionada.md` (corrida final 2026-09-25, French CRSP 202607) |
| Ejecución independiente (B) | `AC06.py` en esta carpeta. Solo biblioteca estándar de Python 3.11; de `herramientas/datos.py` toma únicamente `parsear_yahoo_json` y `parsear_fred_csv`. No importa ni copia `R05.py` ni `R05_verificacion.py`, y no usa el motor `herramientas/backtest.py` |
| Fecha | 2026-09-28 (descargas a las 17:49 UTC) |
| Comando | `python3 laboratorio/auditorias/AC-06-volatilidad-gestionada/AC06.py` (sin red, unos 2 s; lee `datos/` y reescribe `datos/SHA256SUMS.txt`, `salida.txt` y `resultados.json`) |

## Protocolo ciego

1. De la ficha R05 leí solo las secciones 1 a 9 (pre-registro).
2. Descargué los datos por mi cuenta, escribí `AC06.py` y generé `salida.txt`.
3. Solo después leí las secciones 10 a 17 de R05 para la comparación de abajo. No leí `R05-salida.txt`, `R05-resultados.json` ni `R05-variantes.csv`; las cifras de A se toman de la sección 11 de la ficha.

Después de leer A no cambió ninguna línea de lógica. Solo se borró un archivo descargado que no se usaba (`fred_DTB3.csv`) y se volvió a correr (mismas cifras).

## Fuentes (B usa una fuente principal distinta de A)

| Serie | Uso en B | Fuente exacta | sha256 |
|---|---|---|---|
| S&P 500 Total Return diario | Rendimiento mensual (fin de mes) desde 1988-02 y varianza realizada diaria desde 1988-02 | Yahoo `https://query1.finance.yahoo.com/v8/finance/chart/%5ESP500TR?period1=-2208988800&period2=4102444800&interval=1d&events=div%2Csplit` (1988-01-04 a 2026-09-28) | `ac96fd45a7c0a1010d2c85447cdc3c44f177665adc69acd943664fe3df750938` |
| S&P 500 precio diario | Varianza realizada 1928-01 a 1988-01 y precio de fin de mes antes de 1988-02 | Yahoo `%5EGSPC`, misma URL (1927-12-30 a 2026-09-28). Antes de 1957-03 es el índice de 90 acciones | `07aeb4d429031632217a8e0f074cb0dbf9608f61724f53fa6250d9d61375d2da` |
| Dividendo de Shiller | Dividendo mensual antes de 1988-02: D anualizado/12 sobre el precio de fin del mes previo | Copia CSV de los datos de Shiller en datahub: `https://raw.githubusercontent.com/datasets/s-and-p-500/main/data/data.csv` (dividendos hasta 2023-06). El `ie_data.xls` original no se usó porque es .xls y la biblioteca estándar no lo lee | `ed6a0faf1864d60161806b594b45a2642f6149f59b26b3d7b32c2ce38758dc6f` |
| T-bill a 3 meses | Efectivo desde 1934-02: RF_t = TB3MS_{t−1}/1200 | FRED `https://fred.stlouisfed.org/graph/fredgraph.csv?id=TB3MS` (1934-01 a 2026-08) | `ebf04b1ae5bc5729ba3bb2b35dbb0e0c5e22dace36bea0c02632782d625ae6ab` |
| Rendimiento de valores del Tesoro de 3 a 6 meses (NBER) | Efectivo 1928-01 a 1934-01 (mismo rezago de un mes) | FRED `...?id=M1329AUSM193NNBR` (1920-01 a 1934-03) | `9025de20bf0ee087437b7fd470a1f70b8f86ed01dbaba9dae96bdad642ac7320` |
| French Mkt-RF y RF, diario y mensual (CRSP **202608**) | Solo control C: la misma lógica de B con los datos de A, para separar el efecto de la ventana del de la fuente | `https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip` y `..._CSV.zip` | diario `2f29e22546069914890a712680a6f81f3680ebc3543b52864484d209ca13a7db`; mensual `593f4fbef03181bc0b22ff6292f217689dd1fb79355049ca905d95b262040a66` |

Condiciones de uso: Yahoo y la copia de datahub no tienen licencia verificada para redistribución; los archivos se guardan aquí solo para reproducir la auditoría.

**Control de dividendos.** En el traslape 1988-02 a 2023-06 (425 meses), SP500TR − (GSPC + dividendo de Shiller) tiene media de +0.067 pp/año y desviación de 0.063 pp/mes. La construcción anterior a 1988 es confiable a ese nivel.

## Definiciones de B (escritas desde el pre-registro)

- RV²(t) = Σ_j (d_j − d̄_t)² sobre los J_t días del mes (RV de MM, días reales). Al desmediar, la tasa libre diaria constante no cambia la RV, así que se usan rendimientos diarios del índice, no en exceso. Se exige J_t ≥ 15 y RV² > 0 (ningún mes falló).
- f_t = R_t − RF_t. Primera RV: 1928-01; primer mes gestionado: **1928-02** (A empieza en 1926-08; Yahoo no tiene datos diarios antes del 1927-12-30).
- Parte A (estadística de MM): f^σ_t = (c/RV²(t−1)) f_t con c que iguala sd(f^σ) = sd(f) en la ventana; MCO con t IID, HC0 y Newey-West de 12 rezagos (Bartlett). Post-publicación: c fija de la ventana del artículo.
- `vol_c1`: w_t = min(1, k_t/RV(t−1)), k_t = sd(f_s)/sd(f_s/RV(s−1)) con todos los s ≤ t−1 (al menos 120; primera decisión 1938-02 en B y 1936-08 en C). Costo |w_t − w_pre,t| × 0.34% (0.29% comisión GBM + 0.05% spread por lado), w_pre = peso a la deriva del mes previo, exposición inicial 0 (paga la entrada). Comprar y mantener paga solo la entrada. Una sola corrida continua recortada por segmentos; MDD sobre la curva neta reiniciada en cada segmento.

## Resultados: B contra A

### Estadística de MM (c de toda la ventana; no es estrategia)

| Caso | Fuente | Ventana | N | α %/año | t IID / HC0 / NW12 | β | SR mercado | SR gestionada |
|---|---|---|---|---|---|---|---|---|
| A (R05 §11.1) | French 202607 | 1926-08 a 2015-12 | 1073 | 4.88 | — / 3.13 / 2.78 | 0.601 | 0.415 | 0.511 |
| C (mi código, French 202608) | French | 1926-08 a 2015-12 | 1073 | 4.88 | 3.07 / 3.13 / 2.78 | 0.601 | 0.415 | 0.511 |
| C | French | 1928-02 a 2015-12 | 1055 | 4.71 | 2.92 / 2.98 / 2.65 | 0.600 | 0.402 | 0.492 |
| **B** | S&P 500 TR | 1928-02 a 2015-12 | 1055 | **4.21** | 2.54 / 2.59 / 2.27 | 0.580 | 0.402 | 0.455 |
| B sin 1928-1937 | S&P 500 TR | 1938-01 a 2015-12 | 936 | 1.88 | 1.43 / 1.40 / 1.31 | 0.672 | 0.511 | 0.465 |
| A post (R05 §11.2) | French 202607 | 2017-08 a 2026-07 | 108 | −0.75 | — / −0.15 / −0.14 | 0.587 | 0.758 | 0.407 |
| **B post** | S&P 500 TR | 2017-08 a 2026-07 | 108 | **−0.32** | −0.05 / −0.05 / −0.05 | 0.768 | 0.794 | 0.450 |
| B post | S&P 500 TR | 2017-08 a 2026-08 | 109 | −0.27 | −0.05 / −0.04 / −0.04 | 0.769 | 0.807 | 0.460 |

### `vol_c1` operable, costos GBM (neto)

| Tramo | Versión | CAGR | vol | Sharpe | MDD | α vs mercado (t HC0; NW12) | CyM: CAGR / Sharpe / MDD |
|---|---|---|---|---|---|---|---|
| Dentro de muestra | A 1936-08 a 2015-12 | 9.91% | 14.00% | 0.491 | −42.2% | 0.32 (0.76; 0.73) | 10.38% / 0.482 / −50.3% |
| Dentro de muestra | C 1936-08 a 2015-12 | 9.91% | 14.00% | 0.491 | −42.2% | 0.32 (0.77; 0.73) | 10.38% / 0.482 / −50.3% |
| Dentro de muestra | C 1938-02 a 2015-12 | 10.38% | 13.89% | 0.520 | −41.1% | 0.24 (0.56; 0.52) | 11.02% / 0.517 / −50.3% |
| Dentro de muestra | **B 1938-02 a 2015-12** | **10.57%** | 14.07% | **0.520** | **−37.9%** | 0.31 (0.80; 0.73) | 10.95% / 0.509 / −50.9% |
| Fuera de muestra | A 2017-08 a 2026-07 | 11.24% | 12.66% | 0.713 | −16.2% | 0.05 (0.04; 0.04) | 14.65% / 0.758 / −24.8% |
| Fuera de muestra | **B 2017-08 a 2026-07** | **12.28%** | 13.02% | **0.764** | **−18.1%** | 0.16 (0.14; 0.16) | 14.97% / 0.794 / −23.9% |
| Fuera de muestra | B 2017-08 a 2026-08 | 12.49% | 12.97% | 0.780 | −18.1% | 0.21 (0.19; 0.22) | 15.17% / 0.807 / −23.9% |

Rotación media fuera de muestra: B 0.094/mes (51 meses con operación), C 0.115/mes (70). Exposición media: B 0.890, A 0.852. Costo estimado: B 0.38%/año, C 0.47%/año.

## Explicación de las diferencias

1. **Mi código reproduce A con los datos de A.** El control C da, a dos o tres decimales, las cifras de A en la estadística de MM (α 4.88, t HC0 3.13, NW 2.78, β 0.601, Sharpe 0.415/0.511) y en `vol_c1` (Sharpe 0.491 y 0.713, CAGR 9.91% y 11.25%, MDD −42.2% y −16.2%). Las diferencias de B frente a A vienen de los datos y de la ventana, no del código.
2. **α de MM: 4.21 (B) contra 4.88 (A), −0.67 pp.** Queda dentro de 1 e.e. del artículo (1.56). Se descompone en: ventana (empezar en 1928-02 porque Yahoo no tiene diarios de 1926-1927) −0.17 pp; fuente (S&P 500 de 90 y luego 500 acciones, más la T-bill de FRED/NBER, contra CRSP total y T-bill de Ibbotson) −0.50 pp. El Sharpe de la gestionada baja de 0.511 a 0.455 por las mismas dos causas (−0.019 y −0.037). La t HC0 baja de 3.13 a 2.59, sigue ≥ 2. La RV diaria del S&P 500 fue en promedio 39% mayor que la de CRSP en 1928-1956 y 9% menor en 2016-2026 (media de log(RV_B/RV_French)): el índice de 90 acciones es menos diversificado.
3. **El α de B depende de 1928-1937.** Sin esos años el α de B cae a 1.88 (t 1.40) y el Sharpe de la gestionada queda debajo del mercado (0.465 contra 0.511). Es la lectura de Cederburg et al. (concentración en la Gran Depresión), vista con otra fuente.
4. **Post-publicación: α −0.32 (B) contra −0.75 (A).** Los dos son ≈ 0 con |t| ≤ 0.15. El α depende de la escala c (c_B = 10.95×10⁻⁴ contra c_French = 9.28×10⁻⁴), y el Sharpe no: la gestionada queda 0.34 abajo del mercado en ambas fuentes (0.450 contra 0.794 en B; 0.407 contra 0.758 en A).
5. **`vol_c1` dentro de muestra.** B empieza en 1938-02 (A en 1936-08) y así excluye la caída de 1937-38, que es la MDD de A (−42.2%, 1937-02 a 1938-03). Con French en la misma ventana, C da Sharpe 0.520 (igual a B) y MDD −41.1%. La MDD de B (−37.9%) es 3.2 pp menor que la de C; es diferencia de fuente. La ventaja de Sharpe sobre comprar y mantener es igual de pequeña en las tres (+0.009 A, +0.003 C, +0.011 B).
6. **`vol_c1` fuera de muestra: Sharpe 0.764 (B) contra 0.713 (A), +0.051, apenas sobre la tolerancia de 0.05; CAGR +1.04 pp.** Causas: (a) el mercado mismo rindió más con menos volatilidad en B (CyM 0.794 contra 0.758; +0.32 pp de CAGR; el S&P 500 le ganó al mercado total en 2017-2026); (b) k_t se estima con una historia en la que la RV del S&P 500 era relativamente más alta que ahora, así que B quedó más expuesto (0.890 contra 0.852) y rotó menos (51 contra 70 meses con operación; costo de 0.38% contra 0.47% anual). Con más exposición en un mercado alcista, el CAGR sube. La brecha contra comprar y mantener no cambia de signo: −0.030 de Sharpe y −2.69 pp de CAGR en B, contra −0.045 y −3.41 pp en A.
7. **Periodo.** B llega a 2026-08 (Yahoo y TB3MS); A llega a 2026-07. Con el mismo corte de 2026-07, las conclusiones no cambian.
8. **No verificado en B:** H3 (combinación en tiempo real de Cederburg), las variantes apalancadas y la SMA10. B no las corrió.

## Veredicto

- **Estado de A ("Replicado" en el periodo del artículo; negativo fuera de muestra): concordante.** Con criterios del pre-registro aplicados a B: H1 **Replicado** (α 4.21 dentro de [3.30, 6.42], t HC0 2.59 ≥ 2); H2 **refutada** (α ≤ 0 y Sharpe de la gestionada < mercado); H4 **refutada** (Sharpe neto fuera de muestra de `vol_c1` 0.764 < 0.794 de CyM). Matiz: el Sharpe de la gestionada en B (0.455) queda fuera de la banda secundaria 0.52 ± 0.05, y la evidencia de B es más débil que la de A (t NW12 2.27 contra 2.78).
- **Conclusión operable ("freno con costo, no fuente de alfa"): concordante.** `vol_c1` redujo la MDD en ambos tramos (−37.9% contra −50.9% dentro; −18.1% contra −23.9% fuera), costó CAGR (−0.38 pp y −2.69 pp por año) y su α contra el mercado es ≈ 0 (t HC0 0.80 dentro, 0.14 fuera). La sensibilidad `var_c1` (1/RV², tope 1) quedó debajo de CyM en Sharpe en ambos tramos (0.470 y 0.679), igual que en A.
- **Correcciones fuera de esta carpeta (no hechas):** en la ficha R05, la sección 16 puede citar AC-06 como segunda ejecución concordante. La cifra "−3.41 pp/año" de la regla 10 propuesta (§17) depende de la fuente: con el S&P 500 TR es −2.69 pp; conviene darla como rango (≈ −2.7 a −3.4 pp en 2017-2026).
