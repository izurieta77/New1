# AC-10: segunda ejecución independiente de R02 (momentum de series de tiempo, TSMOM-12)

> Fase 0, formación. Nada de esto es una recomendación de inversión. Todas las cifras son históricas, en USD salvo donde se indica, antes de impuestos.

| Campo | Valor |
|---|---|
| Réplica auditada (A) | `laboratorio/replicas/R02-momentum-series-de-tiempo.md` (corridas 2026-09-25, French CRSP 202607 mensual y diario; Yahoo `adjclose` descargado el 2026-09-25) |
| Ejecución independiente (B) | `AC10.py` en esta carpeta. Biblioteca estándar de Python 3.11; de `herramientas/datos.py` solo usa `parsear_yahoo_json` y `parsear_fred_csv`; del código de AC-09 solo el lector OLE2/BIFF8 del xls de Shiller. No importa ni copia `R02.py`, `R02_verificacion.py` ni `herramientas/backtest.py`. La señal, la EWMA, la alineación de fechas, el motor de cartera, los costos, las métricas, el t de Newey-West y el DSR están escritos en `AC10.py` |
| Fecha | 2026-10-01 (descargas a las 17:49-17:52 UTC; `datos/descarga_utc.txt`) |
| Comando | `python3 laboratorio/auditorias/AC-10-tsmom/AC10.py` (sin red, ~1 s; lee `datos/`, reescribe `datos/SHA256SUMS.txt`, `salida.txt` y `resultados.json`) |
| sha256 de `AC10.py` | `a7e11be11bde758d8635e0975304bfd041d495f1c30477d66aa8ea357ddad1a4` (versión ciega, antes de la conciliación: `84ce8f7f…553f`) |

## Protocolo ciego

1. De la ficha R02 leí solo el encabezado y las secciones 1 a 9 (pre-registro: hipótesis, refutación, datos, universo, disponibilidad, periodos, limpieza, reglas y costos).
2. Descargué los datos, escribí `AC10.py` y generé `salida.txt` (bloques (a), (b), H4, DSR, MXN y criterios). Guardé esa salida (sha256 `c252afb8…8f79`) a las 17:55 UTC.
3. Después leí las secciones 10 a 17 de R02 para la comparación. No leí `R02.py`, `R02_verificacion.py` ni `R02-variantes.csv`; las cifras de A salen de las secciones 10 a 12 y 16 de la ficha.

Después de leer A agregué a `AC10.py` solo la función `conciliacion` (al final de la salida) y copié a `datos/` los dos zip French 202607 de A (mismos sha256 `b840dba5…` y `1916d331…`, tomados de `replicas/R08-datos/french/`). Se verificó con `diff` que todas las líneas anteriores de `salida.txt` quedaron idénticas a la salida ciega (solo se agregan las dos huellas French en el encabezado).

## Fuentes (B usa una fuente distinta de A)

| Serie | Uso en B | Fuente exacta | Rango usado | sha256 |
|---|---|---|---|---|
| `^GSPC` | (a) precio de fin de mes hasta 1996-10 y volatilidad EWMA diaria (precio) en todo el periodo | Yahoo chart v8, `period1=-2208988800&period2=4102444800&interval=1d` | 1927-12-30 a 2026-09-30 | `e1c5a167…f615f` |
| Shiller `ie_data.xls` | (a) dividendo D (anual) → D/12 por mes, hasta 1996-10 | shillerdata.com (`…/70fec4f5-…/ie_data.xls?ver=1788371540009`), descargado 2026-10-01 (idéntico byte a byte al de AC-09) | 1928-01 a 1996-10 | `044196da…89c1` |
| `^SP500TR` | (a) rendimiento total desde 1996-11 | Yahoo, `range=30y&interval=1d` | 1996-10-01 a 2026-09-30 | `244d8687…8f94` |
| SPY, EFA, EEM, TLT, IEF, GLD, DBC, VNQ | (b) rendimiento total **construido aquí**: (cierre_d + dividendo ex_d)/cierre_{d−1} − 1, con el cierre de Yahoo (ajustado solo por splits) y los eventos de dividendo; fin de mes = último día hábil; volatilidad EWMA con el mismo índice diario. No usa `adjclose` ni barras `1mo` (A sí) | Yahoo, `range=30y&interval=1d&events=div,split` | desde el alta de cada ETF a 2026-09-30 | ver `datos/SHA256SUMS.txt` |
| TB3MS | rf de (a) desde 1934 y de (b): tasa del mes / 1200 (A usa la T-bill a 1 mes de French) | FRED | 1934-01 a 2026-08 | `ebf04b1a…6ae6ab` |
| M1329AUSM193NNBR | rf de (a) 1928-1933 (NBER) | FRED | 1920-01 a 1933-12 | `9025de20…7320` |
| DEXMXUS | MXN: último dato ≤ fin de mes | FRED | 1993-11 a 2026-09 | `0b71c05f…e4b` |
| French 202607 mensual y diario | **Solo control C**, después de leer A | copia de `replicas/R08-datos/french/` | — | `b840dba5…f5eb` / `1916d331…a8` |

Stooq rechazó la conexión (reset), así que para los ETFs la segunda fuente es la misma Yahoo con **otra construcción** (cierre + dividendos propios, diario) y no otro proveedor. Chequeo cruzado impreso: diferencia máxima mensual entre el rendimiento propio y el de `adjclose` ≤ 0.065 pp en los 8 ETFs; CAGR igual a 0.01 pp. En el traslape 1996-11 a 2026-06, `^GSPC` + D/12 de Shiller rinde 10.21% anual contra 10.27% de `^SP500TR`. La barra de Yahoo del 2026-10-01 es intradía y se descarta. Condiciones de uso de Yahoo y Shiller: no verificadas.

## Definiciones de B (escritas desde el pre-registro)

- **(a)** r_t = cierre `^GSPC`_t/cierre_{t−1} − 1 + (D_t/12)/cierre_{t−1} hasta 1996-10; r_t de `^SP500TR` desde 1996-11. Efectivo = rf (TB3MS/1200; NBER antes de 1934).
- **Señal:** s_L = +1 si ∏(1+r) > ∏(1+rf) en los meses t−L … t−1; si no, −1. σ = EWMA diaria, δ = 60/61, E[r²] − E[r]² con cada media normalizada por 1 − δ^n, × 261, mínimo 120 días; se usa la σ del último día hábil ≤ fin del mes t−1. Largo/corto: w = s·min(0.40/σ, 10) (en (b), /8 por activo). Solo-largos: 1{s = +1}; en (b) operable, 1{s = +1}·min(1, 0.10/σ_i)/8. SMA10: índice TR en t−1 > media de t−10 … t−1.
- **Motor:** pesos con deriva W_pre = W·(1+r_i)/(1+r_b); costo = Σ|W − W_pre|·c; r_neto = r_b − costo·(1+r_b); se empieza en efectivo; una corrida continua recortada por segmento. c = 0.34% por lado (0.29% GBM + 0.05% spread); medio 0.44%; bruto 0.
- **Ventanas:** (a) primer mes evaluado **1929-01** (12 meses de historia después del primer cierre de `^GSPC` en 1927-12; **A empieza en 1927-07**); dentro 1929-01 a 2011-12; artículo 1985-01 a 2009-12; fuera 2012-01 a 2026-07 (y a 2026-08). (b) muestra común desde 2006-03, primer mes evaluado 2007-03 (igual que A).
- **Métricas:** CAGR, vol, Sharpe = media/sd del exceso mensual × √12, Sortino, MDD mensual (incluye el valor inicial), t NW(6) de la media del exceso. DSR de Bailey-López de Prado con V[SR] de los 15 ensayos (`es_prueba=1`) en el mismo tramo y N = 15.

## Resultados de B (neto de 0.34% por lado salvo que se diga)

| Hipótesis / segmento | Variante | CAGR | Vol | Sharpe | t NW6 | MDD |
|---|---|---|---|---|---|---|
| H1, (a) 1929-01 a 2011-12 | `A_ls_vt40_L12` | 4.80% | 44.01% | **0.257** | **2.19** | −98.68% |
| | `A_lo_L12` / comprar y mantener / SMA10 / largo vt40 | 8.82 / 9.05 / 8.60 / 11.69% | | 0.448 / 0.359 / 0.426 / 0.402 | | −53.40 / −83.14 / −54.32 / −94.56% |
| H1b, (a) 1985-2009 **bruto** | `A_ls_vt40_L12` | 23.74% | 38.55% | **0.646** | 3.40 | −69.16% |
| | L3 / L6; largo vt40 bruto | | | 0.030 / 0.291; 0.580 | | |
| H2, (a) 2012-01 a 2026-07 | `A_ls_vt40_L12` | 13.72% | 37.73% | **0.491** | **1.67** | −73.57% |
| | `A_lo_L12` / comprar y mantener / SMA10 / largo vt40 | 10.84 / 15.09 / 9.13 / 30.79% | | 0.784 / 0.961 / 0.697 / 0.880 | 3.05 / 5.05 / 2.57 / 3.94 | −19.86 / −23.87 / −22.88 / −52.15% |
| H3, (b) 2012-01 a 2026-07 | `B_ls_vt40_L12` | 3.30% | 19.31% | **0.178** | **0.76** | −45.35% |
| H4, (b) 2012-01 a 2026-07 | `B_lo_vt10_L12` | 3.36% | 3.75% | **0.463** | 1.97 | **−6.61%** |
| | 1/N | 6.33% | 9.28% | 0.533 | 2.33 | −19.21% |
| | 1/N-SMA10 | 4.26% | 5.52% | 0.486 | 1.98 | −6.93% |
| | 1/N-vt10 (control) | 3.96% | 5.63% | 0.429 | 1.85 | −10.90% |
| H4 bruto | `B_lo_vt10_L12` / 1/N / 1/N-SMA10 | 3.82 / 6.44 / 5.01% | | 0.584 / 0.543 / 0.616 | | −6.09 / −19.14 / −6.27% |

- **Criterios §2 (B):** (i) cumple (0.646 > 0); (ii) cumple (0.257, t 2.19 ≥ 2); (iii) no cumple (0.178, t 0.76). **Estado B: Replicado con diferencias.**
- **H4 (B): refutada.** `B_lo_vt10_L12` tiene menor MDD que 1/N pero menor Sharpe (0.463 < 0.533): "no agrega valor frente a 1/N". Contra 1/N-SMA10, menor Sharpe (0.463 < 0.486) aunque MDD apenas menor (−6.61% contra −6.93%): "no agrega valor frente a la regla sencilla". Diferencia mensual contra 1/N −0.268%/mes (t NW6 −1.98); contra 1/N-SMA10 −0.080%/mes (t −1.08). En bruto supera a 1/N (0.584 contra 0.543) y sigue debajo de 1/N-SMA10 (0.616).
- **DSR (fuera de muestra, N = 15, V de los 15):** `B_lo_vt10_L12` 0.508; `B_ls_vt40_L12` 0.142; `A_ls_vt40_L12` 0.549. Dentro de (a), `A_ls_vt40_L12` 0.428. Ninguno ≥ 0.95.
- **Mitades de (b) fuera de muestra (Sharpe):** `B_ls_vt40_L12` 0.142 / 0.227; `B_lo_vt10_L12` 0.473 / 0.449; 1/N 0.604 / 0.495; 1/N-SMA10 0.362 / 0.606.
- **MXN fuera de muestra (CAGR / MDD):** `B_lo_vt10_L12` 4.90% / −24.33%; 1/N 7.92% / −27.19%; 1/N-SMA10 5.82% / −22.20%.
- **Timing (a), solo-largos L12:** covarianza +0.114%/mes dentro y −0.180%/mes fuera (mismo signo que A).

## Comparación con A

Tolerancia: 1 pp de CAGR, 0.05 de Sharpe. Cifras de A de la ficha R02 §10-§12 y §16.

| Métrica | A (French CRSP 202607; Yahoo `adjclose`) | B (S&P 500 TR; ETFs TR propio; TB3MS) | Dif. | ¿En tolerancia? |
|---|---|---|---|---|
| H1 `A_ls_vt40_L12` neto dentro, Sharpe (t) | 0.3348 (2.97), 1927-07 a 2011-12 | 0.257 (2.19), 1929-01 a 2011-12 | **−0.078** | **No** (ventana + fuente; ver 1 y 2) |
| H1b `A_ls_vt40_L12` bruto 1985-2009, Sharpe (t) | 0.4836 (2.45) | 0.646 (3.40) | **+0.162** | **No** (fuente; ver 2) |
| H2 `A_ls_vt40_L12` neto fuera, Sharpe (t) | 0.3790 (1.23) | 0.491 (1.67) | **+0.112** | **No** (fuente; ambos no significativos) |
| `A_lo_L12` fuera, Sharpe / MDD | 0.7052 / −24.52% | 0.784 / −19.86% | **+0.079**; +4.7 pp | **No** (fuente) |
| Comprar y mantener fuera, CAGR / Sharpe / MDD | 14.94% / 0.9282 / −24.84% | 15.09% / 0.961 / −23.87% | +0.15 pp; +0.033 | Sí |
| SMA10 (a) fuera, Sharpe | 0.8032 | 0.697 | **−0.106** | **No** (misma causa que AC-09) |
| H3 `B_ls_vt40_L12` fuera, Sharpe (t) / MDD | 0.2071 (0.88) / −45.32% | 0.178 (0.76) / −45.35% | −0.029 | Sí |
| H4 `B_lo_vt10_L12` fuera, CAGR / Sharpe / MDD | 3.37% / 0.4874 / −6.69% | 3.36% / 0.463 / −6.61% | −0.01 pp; −0.024 | Sí |
| 1/N fuera, CAGR / Sharpe / MDD | 6.33% / 0.5406 / −19.22% | 6.33% / 0.533 / −19.21% | −0.008 | Sí |
| 1/N-SMA10 fuera, Sharpe / MDD | 0.4906 / −6.96% | 0.486 / −6.93% | −0.005 | Sí |
| 1/N-vt10 fuera, Sharpe / MDD | 0.4373 / −11.08% | 0.429 / −10.90% | −0.008 | Sí |
| `B_lo_L12` fuera, Sharpe | 0.5591 | 0.531 | −0.028 | Sí |
| (b) dentro 2007-03 a 2011-12: `B_ls_vt40_L12` / `B_lo_vt10_L12` | 0.7887 / 0.8863 | 0.796 / 0.896 | +0.01 | Sí |
| H4 bruto: `B_lo_vt10_L12` / 1/N / 1/N-SMA10 | 0.6036 / 0.5515 / 0.6211 | 0.584 / 0.543 / 0.616 | ≤ 0.02 | Sí (mismo orden) |
| MXN `B_lo_vt10_L12` / 1/N: CAGR; MDD | 4.92% / 7.93%; −24.64% / −27.20% | 4.90% / 7.92%; −24.33% / −27.19% | ≤ 0.3 pp | Sí |
| DSR pre-especificadas fuera (V de 15) | 0.43 / 0.20 / 0.59 (`A_ls`, `B_ls`, `B_lo_vt10`) | 0.55 / 0.14 / 0.51 | | Sí: ninguno ≥ 0.95 |
| Criterios (i) / (ii) / (iii) | cumple / cumple / no cumple | cumple / cumple / no cumple | | **Concordante** |
| Estado pre-registrado | Replicado con diferencias | Replicado con diferencias | | **Concordante** |
| H4 | Refutada (1/N y 1/N-SMA10) | Refutada (1/N y 1/N-SMA10) | | **Concordante** |

### Explicación de las diferencias

1. **El código no es la causa.** El control C (código de B sobre los zip French 202607 de A, desde 1927-07, σ de Mkt-RF diario, RF de French) reproduce a A a tres decimales: H1 0.335 (t 2.97), H1b bruto 0.484 (t 2.46), H2 0.379 (t 1.24), `A_lo_L12` dentro 0.507 / −45.17% y fuera 0.705 / −24.52%, comprar y mantener 0.386 / −83.65% y 0.928 / −24.84%, SMA10 fuera 0.803 / −19.31%. En (b), cambiar solo TB3MS por la RF de French da 0.207 (t 0.88), 0.487 / −6.69%, 0.541, 0.491 / −6.96% y 0.437 / −11.08%: **A exacto**. Toda diferencia viene de la fuente o de la ventana.
2. **(a): la serie decide 6 meses de señal en 1985-2009 y 6 en 2012-2026.** El signo de 12 meses del S&P 500 y el del mercado CRSP difieren en 1987-11, 1990-05, 1991-02, 1998-09, 1998-10, 2003-07, 2016-04/05/06, 2019-09/10 y 2022-05. En 1990-05, 1991-02 y 1998-09/10 el S&P (grandes) tenía exceso de 12 meses positivo y el mercado amplio (con pequeñas rezagadas) negativo; B estuvo largo con w ≈ 1.5-3 y A corto en meses de +6% a +9%: solo esos cuatro meses suman ≈ +64 pp de exceso a B y −68 pp a A. Descomposición (Sharpe bruto 1985-2009 / neto fuera): B puro 0.646 / 0.491; B con rf French 0.630 / 0.491; B con σ French 0.626 / 0.480; **B con la señal de French 0.530 / 0.424**; rendimientos S&P con señal, σ y rf French 0.513 / 0.412; A 0.484 / 0.379. **La diferencia es sobre todo de señal**; σ (^GSPC/Mkt-RF ≈ 1.05) y rf pesan ≤ 0.02. Es el mismo mecanismo que AC-09 encontró para la SMA10 (cruces al filo con S&P contra CRSP), aquí multiplicado por el apalancamiento de 40%/σ (|w| medio ≈ 3).
3. **H1 dentro de muestra (0.257 contra 0.3348): ventana y fuente, mitad y mitad.** A empieza en 1927-07; B no tiene cierres diarios de `^GSPC` antes de 1927-12-30 y empieza en 1929-01. Los 18 meses 1927-07 a 1928-12 de A dieron a la regla un Sharpe de 2.12 (CAGR 210%, con el alza de 1928). Con French recortado a 1929-01, A daría 0.296 (t 2.62): la ventana explica −0.039. El resto (0.296 → 0.257) es la señal S&P (B con señal French: 0.291). **El criterio (ii) se sigue cumpliendo (t 2.19), pero con menos margen**: con rendimientos French y señal S&P el t es 2.07.
4. **Orden de horizontes (conclusión 2 de A).** En B se sostiene en la ventana del artículo (bruto: L3 0.030 < L6 0.291 < L12 0.646), pero **no** en 1929-2011: L6 0.276 > L12 0.257 neto (0.388 > 0.338 bruto). Con French desde 1929 el orden sí se cumple (0.162 < 0.296 neto). Es dependiente de la serie.
5. **"El largo/corto no supera al largo escalado por volatilidad en ninguna ventana de EUA" (conclusión 4 de A).** En B **falla en la ventana del artículo**: bruto 0.646 contra 0.580 del largo vt40. Se sostiene dentro de muestra (0.257 contra 0.402) y fuera (0.491 contra 0.880). La conclusión debe leerse como dependiente de la serie en 1985-2009.
6. **SMA10 fuera (0.697 contra 0.8032) y `A_lo_L12` fuera (+0.079).** Son las mismas diferencias de señal S&P contra CRSP. Con S&P, TSMOM-12 solo-largos **supera** a SMA10 fuera de muestra en Sharpe (0.784 contra 0.697) y en MDD (−19.86% contra −22.88%); con CRSP es al revés (0.705 contra 0.803; −24.52% contra −19.31%). La frase de A "SMA10 fue igual o mejor fuera de muestra en EUA" no es robusta a la serie. Ambas siguen debajo de comprar y mantener (0.961 en B).
7. **(b) diferencias menores (≤ 0.03 de Sharpe).** Vienen de la rf: TB3MS (3 meses) rinde 1.67% anual en 2012-2026 contra 1.59% de la T-bill a 1 mes de French, lo que baja el exceso. Con la RF de French, B reproduce a A exactamente (punto 1). Construir el rendimiento total con cierre + dividendos diarios en lugar de `adjclose` `1mo` cambia < 0.07 pp por mes.

## Veredicto de la auditoría

- **Estado pre-registrado: concordante, "Replicado con diferencias"** en A y en B: (i) se cumple, (ii) se cumple (B con menos margen: t 2.19), (iii) no cumple la significancia (t 0.88 en A, 0.76 en B).
- **H2 (EUA post-publicación): concordante.** Sharpe positivo y no significativo en las dos (t 1.23 y 1.67), debajo de comprar y mantener y del largo con volatilidad objetivo.
- **H3 y H4 (8 ETFs): concordantes y casi idénticas.** La regla del artículo no es significativa después de 2012; la versión operable `B_lo_vt10_L12` no supera a 1/N ni a 1/N-SMA10 en el criterio doble, neta de costos GBM; su ventaja es solo de MDD. En MXN la reducción de MDD casi desaparece en las dos.
- **DSR:** ninguna variante alcanza 0.95 en ninguna de las dos ejecuciones.
- **Lo frágil (depende de la serie S&P contra CRSP, por cruces de signo al filo):** las magnitudes de (a) (H1b +0.16, H2 +0.11, H1 −0.08 de Sharpe), el orden L12 > L6 en 1929-2011, la comparación TSMOM contra el largo vt40 en 1985-2009 y la comparación TSMOM-12 solo-largos contra SMA10 fuera de muestra en EUA.
- **Estado de la doble ejecución: Replicado con diferencias** (estado, H2, H3 y H4 concordantes; diferencias de (a) fuera de tolerancia, explicadas por la fuente y la ventana, sin error de código).
- **La etiqueta de R02 se sostiene: descartada.** La versión operable no supera a 1/N ni a la regla sencilla en las dos ejecuciones, y la regla del artículo no es significativa después de publicarse en ninguna.
