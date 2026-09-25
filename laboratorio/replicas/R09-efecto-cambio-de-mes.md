# Réplica R09: efecto de cambio de mes, "turn of the month" (Lakonishok y Smidt, 1988; McConnell y Xu, 2008)

> Fase 0: formación. Esta ficha no recomienda inversiones. Las secciones 1 a 9 son el pre-registro. Se escribieron el 2026-09-25 (≈06:55 UTC), antes de calcular cualquier rendimiento, media, t, Sharpe o caída con los datos de esta réplica. No se editan después. Cualquier cambio posterior va a "Desviaciones del pre-registro", con fecha.

| Campo | Valor |
|---|---|
| ID | `R09` (registro: `laboratorio/replicas/R09-variantes.csv`; script: `laboratorio/replicas/R09.py`; comprobación sin el motor: `laboratorio/replicas/R09_verificacion.py`) |
| Artículo original | Lakonishok, J. y Smidt, S. (1988). "Are Seasonal Anomalies Real? A Ninety-Year Perspective". *The Review of Financial Studies* 1(4): 403-425, octubre de 1988. doi:10.1093/rfs/1.4.403. Cita verificada el 2026-09-25 con Crossref, IDEAS/RePEc y Oxford Academic. **El texto no se pudo leer**: la copia de la Universidad de Toronto responde 404 y la de Oxford es de pago. Las cifras de L&S de abajo vienen de la cita textual en McConnell y Xu (versión de trabajo de 2006, p. 1); son de **segunda mano** |
| Artículo de extensión (fuera de muestra de L&S) | McConnell, J. J. y Xu, W. (2008). "Equity Returns at the Turn of the Month". *Financial Analysts Journal* 64(2): 49-64, marzo/abril de 2008. doi:10.2469/faj.v64.n2.11. Cita verificada con Crossref, CFA Institute e IDEAS. **Versión leída:** Xu y McConnell, "Equity Returns at the Turn of the Month", versión de trabajo del 14-jul-2006 (primer borrador de noviembre de 2004; SSRN 917884), 50 páginas, leída completa con `pypdf` desde https://www.chesler.us/resources/academia/turn_of_the_month_stock_returns.pdf. **La versión publicada en el FAJ no se leyó** (tandfonline y SSRN responden 403; el PDF de Purdue redirige). El resumen publicado sí se leyó (CFA Institute) |
| Fecha de publicación | L&S: octubre de 1988. McConnell-Xu: versión de trabajo en SSRN desde 2006; revista el 1-mar-2008 |
| Pre-registro escrito el | 2026-09-25, antes de cualquier corrida con rendimientos |
| Responsable | Claude (laboratorio del sistema). Revisión independiente pendiente (`auditor-de-replicas`) |
| Estado | **Replicado** según la regla pre-registrada (sección 16): casi exacto en 1926-2005. Fuera de muestra (2008-03 al final), mismo signo, **no significativo y ≈11% de la magnitud** de dentro de muestra. Como estrategia con costos GBM no sobrevive en ningún tramo. No es candidata para dinero (sección 17) |

**Conocimiento previo declarado.** Este pre-registro no es ciego. Antes de escribirlo ya conocía:

1. Las tablas 1 y 2 de la versión de trabajo de McConnell-Xu (transcritas en la sección 1) y la cifra de L&S que ellos citan.
2. El renglón "Turn-of-the-month (TOM)" de `arena/investigacion/03-teoria-de-torneos-y-estrategia-competitiva.md` (0.15% diario en el TOM contra −0.001% el resto, "1926-2005"; Quantpedia: 7.2% anual, vol de 6.9%, Sharpe de 1.04; grado "B como efecto; C como estrategia en GBM"; uso: "solo para el timing de entradas").
3. Un resumen (WebFetch, 2026-09-25) de la nota de QuantSeeker "Turn-of-the-Month Strategies: Do They Still Work?" (https://www.quantseeker.com/p/turn-of-the-month-strategies-do-they). Dice que la ventana clásica [0:3] "has essentially disappeared" en ETFs de EUA ("none of these differences are statistically significant") y que, con 5 pb por lado, las estrategias TOM bajan el CAGR y dan Sharpe "lower or comparable" frente a comprar y mantener. **No verifiqué sus cifras.** Es una fuente secundaria y la tomo solo como información previa.
4. Resultados propios del laboratorio: en R01 y R04, comprar y mantener el mercado de EUA rindió mucho después de 2002-2007 (R04: exceso positivo en ambas mitades del año, 2003-2026). Eso anticipa que comprar y mantener será una referencia difícil fuera de muestra.
5. **Solo estructura de fechas**, sin rendimientos (script de exploración en el scratchpad, no en el repo):
   - French `F-F_Research_Data_Factors_daily`: 1926-07-01 a 2026-07-31, 26,296 días, CRSP 202607, 0 faltantes, columnas Mkt-RF, SMB, HML y RF, sha256 `1916d331c2c51d2aee3d00215897d2b8e5995cb387f1f4569ba46bff5fb049a8`. Trae **1,158 sábados** (el último, 1952-05-24) y ningún domingo. Hay 9 huecos de más de 4 días naturales: 1929-11-27→12-02, 1933-03-03→03-15, 1956-12-21→12-26, 1958-12-24→12-29, 1961-05-26→05-31, 1968-07-03→07-08, 2001-09-10→09-17, 2006-12-29→2007-01-03 y 2012-10-26→10-31.
   - Yahoo `^GSPC` 1d: 1927-12-30 a 2026-09-24, 24,799 días, USD, `adjclose` = `close` (índice de precio), `fechas_sin_precio` = [2026-09-22]. **No trae ningún sábado.** Todas sus fechas están en French, y a French le sobran 1,085 fechas dentro del rango de Yahoo (88 en los veinte, 492 en los treinta, 418 en los cuarenta y 87 en los cincuenta; ninguna después de 1952).

---

## PRE-REGISTRO (secciones 1 a 9)

### 1. Hipótesis previa y mecanismo

**Definición.** El cambio de mes (TOM) son los días de negociación −1, +1, +2 y +3: el último día hábil del mes y los tres primeros del mes siguiente. El "resto" son todos los demás días. McConnell-Xu comparan además contra "otros días" en sentido estrecho: los días −10 a −2 y +4 a +10.

**Resultado declarado en los artículos** (cifras textuales):

- **L&S (1988)**, citado por McConnell-Xu (versión de 2006, p. 1): con el Dow Jones Industrial (índice de precio), 1897-1986, "the average cumulative return over the four-day turn-of-the-month is 0.473% whereas the average cumulative return over the full month is 0.349%, indicating that returns were, on average, negative over the remaining days of the month". Es decir, "the four days at the turn-of-the-month account for all of the positive return to the DJIA over the period of 1897-1986".
- **McConnell-Xu, tabla 1** (versión de 2006; rendimiento diario **bruto** del índice CRSP ponderado por valor, VW, en %). "Otros días" = −10 a −2 y +4 a +10. La t de la última columna prueba la diferencia:

| Panel | Día −1 | +1 | +2 | +3 | TOM [−1,+3] | Otros días | Diferencia |
|---|---|---|---|---|---|---|---|
| A. ene-1926 a dic-1986 | 0.17 | 0.09 | 0.18 | 0.21 | 0.16 (t 8.50) | 0.01 (t 0.98) | **0.15 (t 7.07)** |
| B. ene-1987 a dic-2005 | 0.19 | 0.25 | 0.13 | 0.08 | 0.15 (t 4.35) | −0.00 (t −0.07) | **0.15 (t 3.78)** |
| C. ene-1926 a dic-2005 | 0.18 | 0.12 | 0.17 | 0.18 | 0.16 (t 9.60) | 0.01 (t 0.87) | **0.15 (t 8.06)** |

  - "% positivos" de la diferencia mensual (VW): 62% (A), 61% (B) y 62% (C). Con índice EW la diferencia es 0.17, 0.20 y 0.18.
  - En el texto (p. 10), para 1987-2005: "the average daily return over the four-day turn-of-the-month interval is 0.15%, while it is -0.001 over all other days".
- **McConnell-Xu, tabla 2** (exceso sobre la T-bill de 30 días, VW). Panel C, 1926-2005: TOM 0.15 (t 8.98), otros días **0.00 (t 0.15)**, diferencia 0.15 (t 7.93). De ahí la frase del resumen publicado: "on average, investors received no reward for bearing market risk except at turns of the month". El efecto aparece en 31 de 35 países (resumen publicado; la versión de 2006 dice 30 de 34 países fuera de EUA).
- **Estrategia.** McConnell-Xu no reportan estrategia neta de costos. Citan a Hensel y Ziemba (1996): S&P 500 en el TOM y T-bills el resto, 1928-1993, "outperformed ... buying and holding the S&P 500 by roughly 0.63% per year". No se verificó.
- **Nota de verificación (hecho).** En `arena/investigacion/03`, "0.15% diario en el TOM contra −0.001% el resto" está atribuido a 1926-2005. En la versión de 2006, "−0.001" corresponde a **1987-2005** (panel B). En 1926-2005, la cifra es 0.16 contra 0.01 bruto, o 0.15 contra 0.00 en exceso. La versión publicada podría tener otras cifras; no se leyó.

**Mecanismo económico.** McConnell-Xu descartan que el efecto venga del tamaño o del precio de las acciones, del cambio de año o de trimestre, o de mayor volatilidad. Rechazan también la hipótesis de "día de pago" de Ogden (1990): no encuentran patrón en el volumen de la NYSE ni en los flujos netos a fondos (TrimTabs, 1998-2005). Lo dejan como "a puzzle in search of an answer". Otras explicaciones de la literatura, que no se verificaron aquí: flujos de liquidez institucional alrededor del fin de mes (Etula et al. 2020, citado por QuantSeeker) y maquillaje de cartera. [I] ¿Por qué no se arbitraría? Por tres razones:

1. Operarlo cuesta dos lados por mes: 24 lados al año.
2. El premio por evento es pequeño (≈0.6% en 4 días según las cifras de arriba) frente al ruido diario.
3. Si el efecto es un pago por proveer liquidez a flujos mecánicos, su tamaño está acotado por esos flujos.

**Hipótesis (signo y magnitud esperados):**

- **H1, periodo de McConnell-Xu (CRSP VW, 1926-2005).** Con el mercado de French (Mkt-RF + RF, bruto), la diferencia diaria entre el TOM y los "otros días" (−10..−2, +4..+10) queda en 0.15 ± 0.03 pp con t ≥ 1.96. Se espera casi idéntica: el mercado de French es el VW de CRSP con filtros de acciones comunes.
  - **H1b.** En exceso sobre la RF, 1926-2005, la media de los "otros días" no es distinta de cero (|t| < 1.96).
  - **H1c (L&S).** En 1928-1986 con `^GSPC` (precio, como el Dow de L&S), el rendimiento acumulado medio de los 4 días del TOM es ≥ al rendimiento medio del mes completo. Con French (rendimiento total) se reporta igual, como contraste.
- **H2, dentro de muestra (1926-07-01 a 2008-02-29).** δ = media diaria del TOM − media diaria del resto > 0, con t NW(10) ≥ 2. Se espera muy significativa.
- **H3, fuera de muestra (2008-03-01 al final, post-publicación en el FAJ).** δ > 0 en French y en `^GSPC`. Se espera **menor** que dentro de muestra y, por el conocimiento previo 3, probablemente **no significativa**.
- **H4, estrategia sola (mercado solo en [−1,+3], efectivo el resto), neta de costos GBM.** Son 24 lados al año: con 0.34% por lado, ≈8.2% anual de costo con rotación completa. Se espera que **no sobreviva a los costos** fuera de muestra: exceso neto sobre el efectivo ≤ 0 o no significativo, y Sharpe y CAGR muy por debajo de comprar y mantener.
- **H5, timing de entradas y salidas** (la regla vigente de `arena/investigacion/03`). El exceso acumulado medio de los 4 días del TOM por evento es > 0 fuera de muestra. Magnitud esperada de 0.2% a 0.6% por evento; significancia incierta. Esto es lo que se pierde al comprar después del día +3 en lugar de antes del cierre del día −1.

### 2. Criterio de refutación

- **Métrica principal del efecto.** δ en puntos porcentuales por día (rendimiento simple × 100), con t de Newey-West (Bartlett, 10 rezagos, corrección n/(n−k)).
- **Métricas secundarias del efecto:**
  - t MCO y t HC1 (White).
  - Comparación estrecha de McConnell-Xu: TOM contra −10..−2 y +4..+10, con t MCO (equivale a la t de dos muestras con varianza común), t Welch y t NW(10).
  - Diferencia mensual pareada D_m (definición en la sección 8): media, mediana, t iid, IC bootstrap de 95% y prueba de signo.
  - Estilo L&S: rendimiento acumulado de 4 días del TOM contra el mes completo.
  - Robustez: winsorización diaria al 0.5% y 99.5%; sin el cambio diciembre-enero; sin los meses con cierres no programados cerca del TOM.
  - Placebo: el lugar del TOM entre ventanas de 4 días.
- **Métrica principal de la estrategia.** Sharpe anualizado del exceso diario sobre el efectivo, **neto de costos por defecto, fuera de muestra**. Secundarias: t NW(10) del exceso neto diario, CAGR, MDD y costo por lado de equilibrio.
- **Condiciones del estado:**
  - (i) French, 1926-07 a 2005-12: δ_MX = media(TOM) − media(otros −10..−2, +4..+10) > 0, |δ_MX − 0.15| ≤ 0.03 pp y t MCO ≥ 1.96.
  - (ii) French dentro de muestra (1926-07-01 a 2008-02-29): δ > 0 y t NW(10) ≥ 2.
  - (iii) French fuera de muestra (2008-03-01 a 2026-07-31): δ > 0.
  - (iv) `^GSPC` fuera de muestra (2008-03-01 a 2026-08-31): δ > 0.
- **Estado final** (regla fijada ahora):
  - **Replicado** si se cumplen (i), (ii), (iii) y (iv).
  - **Replicado con diferencias** si δ_MX > 0 en French 1926-2005 y se cumple al menos una de (iii) o (iv), pero no las cuatro condiciones. Esto incluye el caso de que la magnitud o la t de (i) queden fuera de tolerancia.
  - **No replicado** si δ_MX ≤ 0 en French 1926-2005, **o** si δ ≤ 0 fuera de muestra **tanto** en French como en `^GSPC`.
- **"Significativo fuera de muestra"** exige dos cosas: t NW(10) ≥ 2 **y** que el IC bootstrap de 95% de D_m excluya el cero. Si falla una, se describe como "mismo signo, no significativo".
- **La estrategia sobrevive a los costos (S1)** si, fuera de muestra y neta de costos por defecto, la regla del artículo (`US_tom_m1_p3`) tiene Sharpe > 0 **y** t NW(10) del exceso neto diario ≥ 2.
- **Agrega valor frente a comprar y mantener (S2)** si su Sharpe neto fuera de muestra es mayor que el de comprar y mantener **y** su MDD es menos severo.
- **Agrega valor frente a la regla sencilla (S3)**: lo mismo contra la SMA de 200 días.
- Se evalúa en French y se reporta igual en `^GSPC`. Si no se cumplen S2 y S3, la conclusión es "no agrega valor frente a la regla sencilla", aunque el efecto exista.
- **DSR.** N = número de variantes con `es_prueba=1` (10 por diseño). Se reportan tres lecturas: V de las 10, V por familia (French o `^GSPC`) y la regla del artículo. **Para decidir se usa el DSR menor.** Si DSR < 0.95, la regla no es candidata para dinero, cualquiera que sea el estado.
- **Regla del sistema afectada:** `arena/investigacion/03-teoria-de-torneos-y-estrategia-competitiva.md`, en dos lugares. El renglón TOM de la tabla de la sección 5 ("[I] Con 0.58% por vuelta (A1) no conviene operarlo solo. **Úsalo para el timing**: compra antes del cierre de mes y vende después del día +3") y la regla [R] 5 ("TOM: solo para el timing de entradas"). La decisión se fija ahora con E = exceso acumulado de 4 días del TOM sobre la RF, por evento, fuera de muestra, en French:
  - **Confirmar** si la estrategia sola no sobrevive (S1 o S2 falsos) **y** E > 0 con t iid ≥ 2 y un IC bootstrap de 95% que excluya el cero.
  - **Modificar** en dos casos. (a) E > 0 pero no significativo: se mantiene "no operarlo solo", pero el timing baja a "criterio de desempate sin costo" (no se retrasa ni se adelanta una operación por el TOM) y el grado del efecto baja de B a C. (b) S1 y S2 verdaderos: se contradice "no conviene operarlo solo" y pasa a "investigar como satélite", con nuevo pre-registro.
  - **Descartar** la regla de timing si E ≤ 0 fuera de muestra en French **y** en `^GSPC`.

### 3. Datos y licencia

| Serie | Fuente y archivo | Versión / huella | Frecuencia | Condiciones de uso |
|---|---|---|---|---|
| Mercado de EUA (Mkt-RF + RF) y RF diaria | French `F-F_Research_Data_Factors_daily_CSV.zip` (`dh.french(..., "diaria")`) | CRSP 202607; sha256 `1916d331…a8` (se imprime completo) | diaria, con sábados hasta 1952 | Pendiente de verificar |
| S&P 500 (precio, sin dividendos) | Yahoo chart v8 `^GSPC` (`dh.yahoo_historia("^GSPC", "1d")`) | URL, rango, `fechas_sin_precio`; `adjclose` = `close` | diaria, sin sábados | Pendiente de verificar |
| MXN por USD (solo sensibilidad) | FRED `DEXMXUS` (Fed H.10, mediodía en Nueva York) | Fecha de descarga y rango | diaria | Dominio público según FRED; referencia, no es cotización ejecutable en GBM |
| CETES (efectivo en MXN, solo sensibilidad) | FRED `INTGSTMXM193N` (FMI IFS, % anual, promedio mensual) | Fecha de descarga y rango | mensual | Pendiente de verificar |

Los datos crudos no se redistribuyen: el caché está en `.gitignore`.

### 4. Universo

- **French.** Es el mercado total de EUA: CRSP, NYSE/AMEX/NASDAQ, ponderado por valor, con dividendos. No tiene sesgo de supervivencia. Difiere del índice VW de CRSP de McConnell-Xu en los filtros de French (acciones comunes, códigos 10 y 11). **No es invertible directamente**; el proxy sería un ETF del S&P 500 o del mercado total en el SIC.
  - No se replica la versión EW (el archivo de factores no la trae).
- **`^GSPC`.** Índice de **precio** del S&P 500 (S&P 90 antes de 1957), sin dividendos: el análogo más cercano al Dow de precio de L&S. Es la segunda fuente de la réplica.
  - Antes de 1953 no trae sábados. Su calendario de días de negociación (y por tanto las posiciones −1, +1, …) difiere del de French en 1928-1952.
  - Sus dividendos repartidos a lo largo del mes afectan el "resto" más que el TOM (inferencia; no se corrige).
- **No se agregan otros países.** El artículo tiene 35; esta réplica se limita a EUA, el mercado que el sistema compraría en el SIC. El IPC diario **no** se incluye.

### 5. Fecha de disponibilidad

- **La señal es de calendario.** La exposición del día t depende solo de la posición de t dentro de su mes (la cuenta desde el inicio, +1, +2, …, y desde el fin, −1, −2, …).
- **Supuesto declarado: el calendario de sesiones se conoce de antemano.** La bolsa publica sus días feriados con anticipación. Para saber al cierre de t−1 si t será el último día hábil del mes, hace falta conocer ese calendario.
  - Implementación. Para cada fecha d_{t−1}, el motor recibe como `extras` (con fecha de disponibilidad d_{t−1}) la posición del día **siguiente** en la serie: `pos_ini_sig` y `pos_fin_sig`. La señal comprueba que la última entrada visible tenga fecha = `h.fecha_decision` y no lee ningún rendimiento.
  - **Excepción: los cierres no programados.** Con el calendario realizado, la señal "sabe" de un cierre imprevisto. Solo importa si el cierre cae junto al TOM. Esos meses se listan como diagnóstico (huecos de más de 4 días naturales entre los días −2 y +1) y se repiten las pruebas del efecto sin ellos. Candidatos vistos en la estructura de fechas: nov-1929, may-1961 y oct-2012 (huracán Sandy).
- **RF de French.** Es la tasa diaria de la T-bill; se conoce al inicio del mes.
- **CETES.** Es el promedio mensual de la tasa anual. Solo afecta el rendimiento del efectivo en MXN, nunca la señal.
- **DEXMXUS.** Es la tasa de mediodía de Nueva York, cuatro horas antes del cierre de las acciones. El desfase agrega ruido a la versión en MXN; no se corrige.
- **Ejecución.** Se supone al **cierre** del día −2 (compra) y del día +3 (venta), como el TOM de McConnell-Xu (rendimiento cierre a cierre). [I] En GBM, la orden en el SIC se ejecuta durante la sesión, no al cierre exacto. Esa diferencia se trata como parte del spread supuesto; no está verificada.

### 6. Periodo

- **Periodos de los artículos:** L&S 1897-1986 (Dow). McConnell-Xu 1926-2005: paneles A (1926-1986), B (1987-2005) y C (1926-2005).
- **Periodo propio total:**
  - French: 1926-07-01 a 2026-07-31.
  - `^GSPC`: primer rendimiento en 1928-01 (el 1927-12-30 solo sirve de precio base). Las pruebas del efecto llegan hasta **2026-08-31** (último mes completo). Los backtests llegan hasta **2026-07-31**, último día con RF de French.
- **Corte único: 2008-02-29.** El artículo salió en el número de marzo/abril de 2008 del FAJ (CFA Institute: 1-mar-2008).
  - `dentro_muestra`: hasta 2008-02-29.
  - `fuera_muestra`: desde 2008-03-01. Es post-publicación y se mira una sola vez.
  - Nota: la versión de trabajo circulaba desde 2006, así que 2006-01 a 2008-02 es un "hueco" entre el fin de la muestra (2005-12) y la publicación.
- **Ventanas de reporte** (fijadas ahora, calculadas sobre los mismos datos, sin nuevas variantes):
  - Completo, dentro de muestra y fuera de muestra.
  - Paneles A, B y C de McConnell-Xu.
  - El hueco 2006-01 a 2008-02.
  - Mitades del tramo fuera de muestra: 2008-03 a 2016-12 y 2017-01 al final (diagnóstico).
  - Décadas, solo con French (diagnóstico).
  - En `^GSPC`, las mismas ventanas a partir de 1928-01.
- **Backtests:** `min_historia` = 200 días en todas las corridas de una familia, para que la SMA de 200 días y las reglas de calendario arranquen igual.

### 7. Limpieza

Reglas fijadas antes de ver resultados:

- **French.** Los valores −99.99 y −999 son faltantes y se omiten; no se espera ninguno. Los sábados (hasta 1952) son sesiones reales y cuentan como días de negociación. El cambio de la fuente de la RF en 202406 (de Ibbotson a ICE BofA) no se ajusta. Se registran la versión CRSP y el sha256.
- **`^GSPC`.** Se usan los precios de Yahoo tal como vienen. Las fechas en `fechas_sin_precio` se descartan (2026-09-22 queda fuera por el recorte a 2026-08-31). La falta de sábados antes de 1953 **no se corrige**: el rendimiento del lunes abarca de viernes a lunes y las posiciones se cuentan sobre las fechas de Yahoo. Se reporta cuántos días −1 difieren entre French y Yahoo.
- **Posiciones.** Se calculan sobre las fechas de cada serie. `pos_ini` = 1 para el primer día de negociación del mes calendario; `pos_fin` = −1 para el último. El primer mes de cada serie se usa solo si la serie arranca en su primer día hábil. French arranca el 1926-07-01. En `^GSPC`, diciembre de 1927 solo aporta el precio base.
- **Efectivo para `^GSPC`.** Es la RF diaria de French compuesta sobre las fechas de French en (d_{t−1}, d_t].
- **CETES diario (sensibilidad MXN).** r = tasa del mes/100 × días naturales desde la fecha anterior/360. Si falta un mes, se arrastra la tasa anterior y se reporta.
- **Sin cambios después de ver resultados.** No se elimina ningún valor extremo; el 19-oct-1987 y 1929-1933 se quedan. La winsorización y la exclusión de meses con cierres no programados son pruebas **adicionales** pre-registradas, no limpieza.

### 8. Regla y variantes planeadas

**Pruebas estadísticas del efecto** (no son estrategias y no van al CSV). En cada ventana y serie se reportan **todas**:

1. **Regresión diaria** y_t = μ + δ·TOM_t + ε_t, con y_t = 100·r_t (rendimiento simple bruto) y TOM_t = 1 si pos_fin = −1 o pos_ini ∈ {1, 2, 3}. Se calculan la t MCO, la t HC1 y la t NW(10).
2. **Comparación de McConnell-Xu:** media del TOM, media de "otros" (−10..−2 o +4..+10, fuera del TOM) y su diferencia δ_MX, con t MCO, t Welch y t NW(10). También las medias de los días −1, +1, +2 y +3, y el % de días positivos. Solo en French: las mismas medias en exceso sobre la RF, como en su tabla 2.
3. **Diferencia mensual pareada.** La unidad es el mes calendario m. El TOM de m es el día −1 de m más los días +1..+3 de m+1. El resto de m son los días +4..−2 de m. D_m = media diaria del TOM de m − media diaria del resto de m, y se asigna a la ventana por la fecha del día −1. Se reportan la media, la mediana, la t iid, el IC bootstrap de 95% (remuestreo iid de meses, 10,000 repeticiones, semilla 9) y la prueba de signo (D_m > 0; p binomial exacta de una cola).
4. **Estilo L&S.** Por mes m se calculan el rendimiento acumulado (compuesto) de los 4 días del TOM, del mes calendario completo m y del resto de m. Se reportan las medias y la razón TOM/mes.
5. **Exceso por evento E_m** (solo French, con su RF; en `^GSPC` con la RF asignada): Π(1+r) − Π(1+rf) de los 4 días del TOM, en %. Se reportan la media, la t iid, el IC bootstrap de 95% (semilla 9), el % de eventos positivos y la comparación con el costo de 1 lado (0.34%) y de 2 lados (0.68%). Es la prueba de H5.
6. **Winsorización diaria** al 0.5% y 99.5% dentro de la ventana: δ y t NW(10).
7. **Sin el cambio diciembre-enero** (se quitan del TOM y del resto los días −1 de diciembre y +1..+3 de enero): δ y t NW(10).
8. **Sin meses con cierres no programados cerca del TOM.** Se quitan los meses m en que hay un hueco de más de 4 días naturales entre el día −2 de m y el día +1 de m+1. Se reportan δ y t NW(10).
9. **Día relativo τ** (solo completo, dentro y fuera). τ = pos_fin para los días más cerca del fin de mes (−1, −2, …) y τ = pos_ini − 1 para los más cerca del inicio (+1 → 0, +2 → 1, …). Se reportan la media diaria y la t iid para τ = −10..+9.
   - **Placebo:** el lugar del TOM (τ ∈ {−1, 0, 1, 2}) entre las 16 ventanas de 4 días consecutivos de τ, con inicios de −9 a +6.
10. **Décadas** (solo French): δ y t NW(10).

**Estrategias** (motor `backtest_senal`, diario). Exposición 1 si el día t cae en la ventana [a, b] (pos_fin(t) ≥ a o pos_ini(t) ≤ b) y 0 si no:

| # | Variante (`es_prueba=1`) | Ventana | Activo / efectivo / moneda |
|---|---|---|---|
| 1 | `US_tom_m1_p3` (**regla del artículo**) | [−1, +3] | French Mkt / RF French / USD |
| 2 | `US_tom_m2_p3` | [−2, +3] | igual |
| 3 | `US_tom_m3_p3` | [−3, +3] (la ventana de 7 días de Etula et al., citada por QuantSeeker) | igual |
| 4 | `US_tom_m1_p2` | [−1, +2] | igual |
| 5 | `US_tom_m1_p4` | [−1, +4] | igual |
| 6-10 | `SPX_tom_m1_p3` (**regla del artículo**), `SPX_tom_m2_p3`, `SPX_tom_m3_p3`, `SPX_tom_m1_p2`, `SPX_tom_m1_p4` | como 1 a 5 | `^GSPC` precio / RF French asignada / USD |

**Referencias.** Se registran con `es_prueba=0` y nota "referencia":

- `*_ref_comprar_mantener` (w = 1).
- `*_ref_efectivo` (w = 0).
- `*_ref_sma200`: `senal_media_movil(200)` sobre el índice diario, la regla sencilla de timing.
- `*_ref_resto`: el complemento de [−1, +3], en el mercado todos los días salvo el TOM.

**Sensibilidades.** Se registran con `es_prueba=0` y nota. Es una lista cerrada:

1. Las 10 variantes y las 8 referencias con spread "medio" (0.15% por lado).
2. Las 10 variantes y las 8 referencias brutas (comisión y spread en 0).
3. **MXN para un inversionista mexicano.** Activo: French Mkt convertido con `DEXMXUS`. Efectivo: CETES diario aproximado (`efectivo_en_mxn=True`). Costos por defecto, el mismo corte, desde que existe DEXMXUS (1993-11). Variantes `USMXN_tom_m1_p3`, `USMXN_ref_comprar_mantener`, `USMXN_ref_efectivo` y `USMXN_ref_sma200`.

**Diagnósticos** (solo se reportan):

- Métricas de la estrategia por ventana de reporte.
- La t NW(10) del exceso neto diario.
- Las operaciones por año.
- **El costo por lado de equilibrio**, en el que el exceso neto se vuelve cero: exceso bruto anual medio / rotación anual, a partir de las corridas brutas.
- La **traducción a una cuenta de 20,000 MXN**:
  - El costo anual en MXN de la regla del artículo con costos por defecto.
  - La prima media por evento en MXN (20,000 × E) contra el costo de un lado (68 MXN con 0.34%).
  - El valor final de 20,000 MXN invertidos al inicio del tramo fuera de muestra en `USMXN_*`.

**Comprobación independiente** (`R09_verificacion.py`, no registra variantes). Recalcula sin el motor:

- δ, δ_MX y E en French dentro y fuera de muestra.
- La curva neta de `US_tom_m1_p3` y de comprar y mantener con el mismo modelo de costos (|Δw| × (comisión + spread), con deriva).
- Que cada mes tenga exactamente 4 días de TOM salvo en los extremos de la serie.

**Exposición, efectivo y moneda.** Exposición en {0, 1}, sin cortos ni apalancamiento. USD con T-bills de French; MXN solo en la sensibilidad 3.

### 9. Costos y comparación simple

- **Costos:**
  - Por defecto: comisión de 0.29% por lado (GBM, 0.25% + IVA: hecho) más spread de 0.05% por lado (supuesto [I]), sobre |Δw|. La regla del artículo compra y vende una vez al mes: unos 24 lados al año, ≈8.2% anual con costos por defecto.
  - Escenario "medio": spread de 0.15%. Bruto: cero.
  - No se modelan el spread cambiario de GBM, los impuestos ni la liquidación final.
  - [I] Los impuestos (ISR de 10% sobre la ganancia neta anual en el SIC) se causan igual en ambas reglas si todo se realiza en el año. Comprar y mantener difiere la ganancia; la regla TOM la realiza cada mes. No se cuantifica aquí.
  - El mínimo de 20 MXN por operación (no verificado, `01-gbm` §2) no ata con 20,000 MXN: 0.29% × 20,000 = 58 MXN > 20.
- **Reglas sencillas con idénticas condiciones:** comprar y mantener, 100% efectivo y SMA de 200 días (mismas fechas, costos, moneda y efectivo). Además, el complemento `ref_resto` para ver la otra parte del mes.

---

## RESULTADOS (se llenan después de correr)

> Corrida del 2026-09-25 (07:01 UTC). Las cifras y tablas vienen de `python3 laboratorio/replicas/R09.py`; la salida completa está en `R09-salida.txt` y las cifras clave en `R09-resultados.json`. Las tablas se copiaron por programa, sin redondear a mano.
>
> Unidades:
> - δ, medias diarias y D_m: puntos porcentuales por día (rendimiento simple × 100).
> - "TOM 4 días", "mes completo", "resto del mes" y E: % acumulado.
> - Estrategias: el Sharpe es el del exceso diario sobre el efectivo, anualizado con 252; `nw_t` es la t NW(10) del exceso neto diario.
> - `costo_equilibrio_lado` = exceso bruto acumulado / rotación acumulada: el costo por lado que dejaría el exceso neto en cero. Solo tiene sentido en reglas que rotan; en comprar y mantener no se interpreta.
> - MDD = caída máxima.

### Desviaciones del pre-registro

| Fecha | Qué cambió | Por qué | ¿Invalida el tramo de prueba? |
|---|---|---|---|
| 2026-09-25 | **Antes de la primera corrida con datos reales** se hicieron dos cambios de código al revisar. (a) Error real: la RF asignada al primer día de `^GSPC` acumulaba la RF de French desde 1926; se ancló al precio base (1927-12-30). (b) Protección: en el índice del percentil de winsorización se cambió `int` por `round`. Con 0.005 y 0.995 ambos dan los mismos índices (5 y 995, comprobado), así que no cambia ningún resultado | Error de código y protección | **No.** Solo habían corrido las comprobaciones con datos sintéticos; no se había calculado ningún rendimiento real |
| 2026-09-25 | **Aclaración, sin cambio.** La regla mecánica de "meses con hueco de más de 4 días entre el día −2 y el +1" encontró 4 meses: 1929-11, 1961-05, 2006-12 y 2012-10. La sección 5 listaba a ojo solo tres candidatos (1929-11, 1961-05 y 2012-10). El hueco 2006-12-29 → 2007-01-03 cae entre el día −1 y el +1 y también cuenta | La lista escrita a mano estaba incompleta; la regla aplicada es la pre-registrada | No |
| 2026-09-25 | **Aclaración, sin cambio.** 21 fechas de `^GSPC` (agosto de 2026) no tienen RF de French, que termina el 2026-07-31, y llevan RF = 0. Solo entran en las pruebas del efecto de `^GSPC`; en E afectan únicamente los días +1..+3 del evento de julio de 2026 | Límite de datos | No |
| 2026-09-25 | **Aclaración, sin cambio.** En 66 meses, todos antes de 1952, el día −1 de French y el de `^GSPC` no coinciden, porque Yahoo no trae sábados (sección 4) | Diferencia de fuente ya declarada | No |
| 2026-09-25 | **Lección de diseño, sin cambio de estado.** Las condiciones (iii) y (iv) solo exigían signo. Con δ fuera de muestra de 0.0150 pp (t NW10 0.35), la réplica queda "Replicado" por regla, aunque ese δ es 11% del de dentro de muestra y no es significativo. En las próximas réplicas conviene exigir una magnitud mínima fuera de muestra | Debilidad del criterio pre-registrado | No: el estado se asigna con la regla escrita |

### 10. Variantes probadas

- **Archivo** `laboratorio/replicas/R09-variantes.csv`: 174 filas de **una** ejecución (58 corridas × 3 segmentos: completo, dentro y fuera de muestra), con una sola marca de tiempo (2026-09-25T07:01 UTC).
  - French y `^GSPC`: 5 variantes y 4 referencias por familia, en 3 escenarios de costo: 54 corridas.
  - USMXN: 4 corridas.
- **Variantes con `es_prueba=1`: 10** (5 de French y 5 de `^GSPC`), en 30 filas. Las referencias y las sensibilidades van con `es_prueba=0` y una nota ("referencia", "sensibilidad: spread medio…", "sensibilidad: bruto…" o "sensibilidad: MXN…").
- **Pruebas fuera del registro.** Ninguna es una variante adicional de la regla:
  - Las comprobaciones con datos sintéticos (`id_replica=None`; diferencia máxima 5.551e-17).
  - El script de exploración de fechas, previo al pre-registro y sin rendimientos.
  - `R09_verificacion.py`, que recalcula sin registrar.
- Se usa `n_pruebas` = 10.

**Salida de `sharpe_deflactado_de_registro`.** Umbral de 0.95 y SR anualizado con 252. El DSR mide el Sharpe del exceso neto **sobre el efectivo**:

| Lectura | Segmento | Variante | DSR | ¿Cumple? | N | V por periodo | SR anual | SR0 anual | n_obs | PSR sin deflactar |
|---|---|---|---|---|---|---|---|---|---|---|
| Por defecto: mejor de las 10, V de todas | dentro_muestra | US_tom_m3_p3 | 0.0024 | No | 10 | 1.234e-04 | -0.0278 | 0.2777 | 21463 | 0.3989 |
| Mejor de French, V de French | dentro_muestra | US_tom_m3_p3 | 0.0007 | No | 10 | 1.636e-04 | -0.0278 | 0.3197 | 21463 | 0.3989 |
| Regla del artículo French, V de todas | dentro_muestra | US_tom_m1_p3 | 0.0000 | No | 10 | 1.234e-04 | -0.1916 | 0.2777 | 21463 | 0.0388 |
| Mejor de ^GSPC, V de ^GSPC | dentro_muestra | SPX_tom_m2_p3 | 0.0003 | No | 10 | 1.018e-04 | -0.1307 | 0.2522 | 19928 | 0.1231 |
| Regla del artículo ^GSPC, V de todas | dentro_muestra | SPX_tom_m1_p3 | 0.0000 | No | 10 | 1.234e-04 | -0.2555 | 0.2777 | 19928 | 0.0117 |
| Mejor de las 10 (selección *ex post*), V de todas | fuera_muestra | US_tom_m3_p3 | 0.0050 | No | 10 | 1.649e-04 | -0.2741 | 0.3210 | 4633 | 0.1179 |
| Regla del artículo French, V de French | fuera_muestra | US_tom_m1_p3 | 0.0000 | No | 10 | 1.918e-04 | -0.6157 | 0.3462 | 4633 | 0.0036 |
| Regla del artículo French, V de todas | fuera_muestra | US_tom_m1_p3 | 0.0000 | No | 10 | 1.649e-04 | -0.6157 | 0.3210 | 4633 | 0.0036 |
| Regla del artículo ^GSPC, V de todas | fuera_muestra | SPX_tom_m1_p3 | 0.0000 | No | 10 | 1.649e-04 | -0.6654 | 0.3210 | 4633 | 0.0018 |

**Todas las variantes tienen Sharpe neto negativo, incluso dentro de muestra.** La mejor es `US_tom_m3_p3`, con −0.0278. El DSR es ≤ 0.0050 en todas las lecturas. Ninguna regla es candidata para dinero.

### 11. Resultados

#### 11.1 Periodo del artículo contra las cifras publicadas

Tabla 1 (VW, bruto) y tabla 2 (exceso) de McConnell-Xu, contra French:

| panel | concepto | articulo | replica French | diferencia | t articulo | t replica (MCO) |
|---|---|---|---|---|---|---|
| A | d-1 | 0.17 | 0.1672 | -0.0028 | NA | 4.78 |
| A | d+1 | 0.09 | 0.0881 | -0.0019 | NA | 2.46 |
| A | d+2 | 0.18 | 0.1839 | 0.0039 | NA | 4.92 |
| A | d+3 | 0.21 | 0.2121 | 0.0021 | NA | 5.65 |
| A | TOM [-1,+3] | 0.16 | 0.1628 | 0.0028 | 8.5 | 8.93 |
| A | otros dias | 0.01 | 0.0135 | 0.0035 | 0.98 | 1.41 |
| A | diferencia | 0.15 | 0.1493 | -0.0007 | 7.07 | 7.07 |
| B | d-1 | 0.19 | 0.1782 | -0.0118 | NA | 2.75 |
| B | d+1 | 0.25 | 0.2499 | -0.0001 | NA | 3.67 |
| B | d+2 | 0.13 | 0.1237 | -0.0063 | NA | 1.75 |
| B | d+3 | 0.08 | 0.0765 | -0.0035 | NA | 1.19 |
| B | TOM [-1,+3] | 0.15 | 0.1571 | 0.0071 | 4.35 | 4.68 |
| B | otros dias | -0.0 | 0.0106 | 0.0106 | -0.07 | 0.61 |
| B | diferencia | 0.15 | 0.1465 | -0.0035 | 3.78 | 3.82 |
| C | d-1 | 0.18 | 0.1698 | -0.0102 | NA | 5.51 |
| C | d+1 | 0.12 | 0.1267 | 0.0067 | NA | 3.99 |
| C | d+2 | 0.17 | 0.1695 | -0.0005 | NA | 5.13 |
| C | d+3 | 0.18 | 0.1797 | -0.0003 | NA | 5.53 |
| C | TOM [-1,+3] | 0.16 | 0.1614 | 0.0014 | 9.6 | 10.08 |
| C | otros dias | 0.01 | 0.0128 | 0.0028 | 0.87 | 1.53 |
| C | diferencia | 0.15 | 0.1487 | -0.0013 | 8.06 | 8.03 |
| C (tabla 2, exceso) | TOM | 0.15 | 0.1476 | -0.0024 | 8.98 | 9.21 |
| C (tabla 2, exceso) | otros dias | 0.0 | -0.0010 | -0.0010 | 0.15 | -0.12 |

- **La tabla 1 se reproduce casi exacta.** En 1926-2005, la diferencia TOM − otros días es 0.1487 pp por día contra 0.15 del artículo, con t MCO de 8.03 contra 8.06. En las 21 celdas de los paneles A, B y C, la mayor diferencia es 0.0118 pp (día −1, panel B).
- **H1b se cumple.** En exceso sobre la RF (tabla 2, panel C), los "otros días" rinden −0.0010 pp (t −0.12), contra 0.00 (t 0.15) del artículo. En 1926-2005, fuera del cambio de mes no hubo premio por riesgo de mercado.
- **H1c (L&S) se cumple.** Con `^GSPC` 1928-1986 (índice de precio, como el Dow):
  - El TOM de 4 días rinde 0.6149%, contra 0.5434% del mes completo (razón 1.13).
  - El resto del mes rinde −0.0736%.
  - Es el mismo patrón de L&S (0.473% contra 0.349%, 1897-1986): el TOM se lleva todo el rendimiento del mes y el resto es negativo.
  - Con French (rendimiento total), el resto del mes es positivo (0.2646%) y la razón TOM/mes es 0.71. [I] Es consistente con que los dividendos se reparten a lo largo del mes; no se verificó.

#### 11.2 Efecto en EUA (French, USD, con dividendos)

Regresión diaria:

| ventana | desde | hasta | n | n TOM | mu (resto) | delta | t MCO | t HC1 | t NW10 | p NW | media TOM |
|---|---|---|---|---|---|---|---|---|---|---|---|
| completo | 1926-07-01 | 2026-07-31 | 26296 | 4804 | 0.0215 | 0.1177 | 6.85 | 7.07 | 7.00 | 0.0000 | 0.1392 |
| dentro_muestra hasta 2008-02 | 1926-07-01 | 2008-02-29 | 21663 | 3920 | 0.0154 | 0.1405 | 7.72 | 7.98 | 7.75 | 0.0000 | 0.1559 |
| fuera_muestra 2008-03 al final | 2008-03-03 | 2026-07-31 | 4633 | 884 | 0.0504 | 0.0150 | 0.32 | 0.33 | 0.35 | 0.7271 | 0.0654 |
| MX panel A 1926-1986 | 1926-07-01 | 1986-12-31 | 16326 | 2904 | 0.0125 | 0.1503 | 7.11 | 7.39 | 7.25 | 0.0000 | 0.1628 |
| MX panel B 1987-2005 | 1987-01-02 | 2005-12-30 | 4794 | 912 | 0.0224 | 0.1347 | 3.53 | 3.59 | 3.35 | 0.0008 | 0.1571 |
| MX panel C 1926-2005 | 1926-07-01 | 2005-12-30 | 21120 | 3816 | 0.0147 | 0.1467 | 7.94 | 8.21 | 7.95 | 0.0000 | 0.1614 |
| hueco 2006-01 a 2008-02 | 2006-01-03 | 2008-02-29 | 543 | 104 | 0.0417 | -0.0908 | -0.93 | -0.91 | -1.08 | 0.2817 | -0.0490 |
| fuera mitad 1 2008-03 a 2016-12 | 2008-03-03 | 2016-12-30 | 2226 | 424 | 0.0390 | 0.0189 | 0.26 | 0.27 | 0.30 | 0.7623 | 0.0579 |
| fuera mitad 2 2017-01 al final | 2017-01-03 | 2026-07-31 | 2407 | 460 | 0.0610 | 0.0114 | 0.19 | 0.19 | 0.19 | 0.8478 | 0.0724 |

Comparación estrecha de McConnell-Xu (TOM contra −10..−2 y +4..+10):

| ventana | d-1 | d+1 | d+2 | d+3 | TOM (t) | otros (t) | dif | t MCO | t Welch | t NW10 | % pos TOM | % pos otros |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| completo | 0.1304 (t 4.63) | 0.1255 (t 4.08) | 0.1508 (t 5.00) | 0.1502 (t 4.95) | 0.1392 (9.33) | 0.0189 (2.42) | 0.1204 | 6.99 | 7.15 | 7.08 | 0.594 | 0.535 |
| dentro_muestra hasta 2008-02 | 0.1642 (t 5.42) | 0.1284 (t 4.10) | 0.1665 (t 5.15) | 0.1643 (t 5.09) | 0.1559 (9.87) | 0.0133 (1.61) | 0.1426 | 7.83 | 8.01 | 7.79 | 0.607 | 0.532 |
| fuera_muestra 2008-03 al final | -0.0195 (t -0.27) | 0.1125 (t 1.21) | 0.0810 (t 1.03) | 0.0878 (t 1.07) | 0.0654 (1.60) | 0.0436 (2.04) | 0.0218 | 0.46 | 0.47 | 0.50 | 0.538 | 0.546 |
| MX panel A 1926-1986 | 0.1672 (t 4.78) | 0.0881 (t 2.46) | 0.1839 (t 4.92) | 0.2121 (t 5.65) | 0.1628 (8.93) | 0.0135 (1.41) | 0.1493 | 7.07 | 7.26 | 7.11 | 0.617 | 0.533 |
| MX panel B 1987-2005 | 0.1782 (t 2.75) | 0.2499 (t 3.67) | 0.1237 (t 1.75) | 0.0765 (t 1.19) | 0.1571 (4.68) | 0.0106 (0.61) | 0.1465 | 3.82 | 3.88 | 3.64 | 0.583 | 0.528 |
| MX panel C 1926-2005 | 0.1698 (t 5.51) | 0.1267 (t 3.99) | 0.1695 (t 5.13) | 0.1797 (t 5.53) | 0.1614 (10.08) | 0.0128 (1.53) | 0.1487 | 8.03 | 8.23 | 7.97 | 0.609 | 0.532 |
| hueco 2006-01 a 2008-02 | -0.0408 (t -0.24) | 0.1885 (t 1.00) | 0.0562 (t 0.46) | -0.4000 (t -1.84) | -0.0490 (-0.54) | 0.0316 (0.72) | -0.0806 | -0.82 | -0.80 | -0.95 | 0.529 | 0.556 |
| fuera mitad 1 2008-03 a 2016-12 | -0.0467 (t -0.41) | 0.0779 (t 0.49) | 0.0622 (t 0.52) | 0.1381 (t 1.30) | 0.0579 (0.92) | 0.0313 (0.95) | 0.0265 | 0.36 | 0.37 | 0.42 | 0.517 | 0.541 |
| fuera mitad 2 2017-01 al final | 0.0055 (t 0.06) | 0.1443 (t 1.43) | 0.0984 (t 0.94) | 0.0414 (t 0.34) | 0.0724 (1.37) | 0.0550 (2.00) | 0.0174 | 0.29 | 0.29 | 0.29 | 0.559 | 0.550 |

Exceso sobre la RF, como en su tabla 2:

| ventana | exceso TOM | t | exceso otros | t |
|---|---|---|---|---|
| completo | 0.1268 | 8.50 | 0.0065 | 0.84 |
| dentro_muestra hasta 2008-02 | 0.1419 | 8.98 | -0.0006 | -0.08 |
| fuera_muestra 2008-03 al final | 0.0599 | 1.47 | 0.0381 | 1.78 |
| MX panel A 1926-1986 | 0.1500 | 8.22 | 0.0007 | 0.08 |
| MX panel B 1987-2005 | 0.1400 | 4.17 | -0.0065 | -0.38 |
| MX panel C 1926-2005 | 0.1476 | 9.21 | -0.0010 | -0.12 |
| hueco 2006-01 a 2008-02 | -0.0675 | -0.75 | 0.0131 | 0.30 |
| fuera mitad 1 2008-03 a 2016-12 | 0.0572 | 0.91 | 0.0307 | 0.93 |
| fuera mitad 2 2017-01 al final | 0.0624 | 1.18 | 0.0450 | 1.63 |

Pruebas robustas:

| ventana | delta winsor 0.5/99.5 | t NW | delta sin dic-ene | t NW | delta sin cierres | t NW | meses con hueco |
|---|---|---|---|---|---|---|---|
| completo | 0.1188 | 7.34 | 0.1129 | 6.53 | 0.1169 | 6.95 | 1929-11-27, 1961-05-31, 2006-12-29, 2012-10-31 |
| dentro_muestra hasta 2008-02 | 0.1397 | 8.02 | 0.1357 | 7.27 | 0.1395 | 7.70 | 1929-11-27, 1961-05-31, 2006-12-29 |
| fuera_muestra 2008-03 al final | 0.0226 | 0.54 | 0.0102 | 0.23 | 0.0147 | 0.34 | 2012-10-31 |
| MX panel A 1926-1986 | 0.1502 | 7.56 | 0.1428 | 6.66 | 0.1485 | 7.17 | 1929-11-27, 1961-05-31 |
| MX panel B 1987-2005 | 0.1334 | 3.46 | 0.1337 | 3.27 | 0.1347 | 3.35 | - |
| MX panel C 1926-2005 | 0.1459 | 8.24 | 0.1408 | 7.40 | 0.1453 | 7.88 | 1929-11-27, 1961-05-31 |
| hueco 2006-01 a 2008-02 | -0.0874 | -1.04 | -0.0560 | -0.71 | -0.0822 | -0.95 | 2006-12-29 |
| fuera mitad 1 2008-03 a 2016-12 | 0.0313 | 0.51 | 0.0103 | 0.16 | 0.0181 | 0.29 | 2012-10-31 |
| fuera mitad 2 2017-01 al final | 0.0152 | 0.27 | 0.0102 | 0.16 | 0.0114 | 0.19 | - |

Diferencia mensual pareada:

| ventana | N | media D | mediana D | t iid | IC95 bootstrap | D>0 | p signo (1 cola) |
|---|---|---|---|---|---|---|---|
| completo | 1200 | 0.1168 | 0.0910 | 7.26 | [0.0855, 0.1486] | 704/1200 (0.587) | 0.0000 |
| dentro_muestra hasta 2008-02 | 980 | 0.1399 | 0.1131 | 7.98 | [0.1058, 0.1746] | 596/980 (0.608) | 0.0000 |
| fuera_muestra 2008-03 al final | 220 | 0.0139 | -0.0154 | 0.35 | [-0.0623, 0.0920] | 108/220 (0.491) | 0.6319 |
| MX panel A 1926-1986 | 726 | 0.1507 | 0.1245 | 7.53 | [0.1113, 0.1904] | 448/726 (0.617) | 0.0000 |
| MX panel B 1987-2005 | 228 | 0.1336 | 0.1245 | 3.42 | [0.0574, 0.2089] | 138/228 (0.605) | 0.0009 |
| MX panel C 1926-2005 | 954 | 0.1466 | 0.1245 | 8.21 | [0.1113, 0.1816] | 586/954 (0.614) | 0.0000 |
| hueco 2006-01 a 2008-02 | 26 | -0.1092 | -0.0269 | -1.51 | [-0.2546, 0.0208] | 10/26 (0.385) | 0.9157 |
| fuera mitad 1 2008-03 a 2016-12 | 106 | 0.0230 | -0.0150 | 0.41 | [-0.0821, 0.1333] | 52/106 (0.491) | 0.6145 |
| fuera mitad 2 2017-01 al final | 114 | 0.0055 | -0.0154 | 0.10 | [-0.1037, 0.1147] | 56/114 (0.491) | 0.6106 |

Estilo L&S y exceso por evento E. Las dos últimas columnas son la fracción de eventos con E mayor que el costo de 1 lado (0.34%) y de 2 lados (0.68%):

| ventana | meses | TOM 4 dias | mes completo | resto del mes | TOM/mes | E medio | t iid E | IC95 E | E>0 | E > 0.34 | E > 0.68 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| completo | 1200 | 0.5571 | 0.9584 | 0.3969 | 0.58 | 0.5075 | 8.49 | [0.3920, 0.6232] | 0.642 | 0.567 | 0.494 |
| dentro_muestra hasta 2008-02 | 980 | 0.6255 | 0.9341 | 0.3015 | 0.67 | 0.5697 | 8.72 | [0.4418, 0.6975] | 0.657 | 0.583 | 0.508 |
| fuera_muestra 2008-03 al final | 220 | 0.2526 | 1.0670 | 0.8222 | 0.24 | 0.2307 | 1.58 | [-0.0527, 0.5178] | 0.573 | 0.495 | 0.432 |
| MX panel A 1926-1986 | 726 | 0.6593 | 0.9299 | 0.2646 | 0.71 | 0.6081 | 8.08 | [0.4585, 0.7553] | 0.669 | 0.594 | 0.515 |
| MX panel B 1987-2005 | 228 | 0.6203 | 1.0013 | 0.3773 | 0.62 | 0.5518 | 3.90 | [0.2748, 0.8199] | 0.632 | 0.566 | 0.513 |
| MX panel C 1926-2005 | 954 | 0.6500 | 0.9470 | 0.2915 | 0.69 | 0.5946 | 8.95 | [0.4652, 0.7260] | 0.660 | 0.587 | 0.515 |
| hueco 2006-01 a 2008-02 | 26 | -0.2727 | 0.4612 | 0.6666 | -0.59 | -0.3455 | -1.15 | [-0.9512, 0.1903] | 0.538 | 0.423 | 0.269 |
| fuera mitad 1 2008-03 a 2016-12 | 106 | 0.2349 | 0.8147 | 0.5936 | 0.29 | 0.2325 | 1.05 | [-0.1967, 0.6714] | 0.557 | 0.481 | 0.415 |
| fuera mitad 2 2017-01 al final | 114 | 0.2691 | 1.3016 | 1.0347 | 0.21 | 0.2289 | 1.19 | [-0.1385, 0.5994] | 0.588 | 0.509 | 0.447 |

Lectura:

- **Dentro de muestra (1926-07 a 2008-02), el efecto es grande y robusto.**
  - δ = 0.1405 pp por día (t NW10 7.75).
  - Se sostiene con winsorización (t 8.02), sin el cambio diciembre-enero (t 7.27) y sin los meses con cierres no programados (t 7.70).
  - D_m es positivo en 596 de 980 meses, con IC95 de [0.1058, 0.1746].
- **Fuera de muestra (2008-03 a 2026-07), casi desaparece.** δ = 0.0150 pp (t NW10 0.35; p 0.7271): el 11% del valor dentro de muestra.
  - D_m = 0.0139, con IC95 de [−0.0623, 0.0920]. Es positivo en 108 de 220 meses (p de signo 0.6319).
  - En las dos mitades vale 0.0189 (t 0.30) y 0.0114 (t 0.19).
  - En el hueco 2006-01 a 2008-02 fue negativo: −0.0908 (t −1.08).
- **Después de 2008 sí hubo premio fuera del cambio de mes.**
  - El exceso de los "otros días" fue 0.0381 pp (t 1.78).
  - El resto del mes acumuló 0.8222% por mes, contra 0.2526% del TOM (razón TOM/mes 0.24).
  - La frase "no reward for bearing market risk except at turns of the month" vale para 1926-2005, no para 2008-2026.
- **Exceso por evento E fuera de muestra:** 0.2307% (t 1.58; IC95 [−0.0527, 0.5178]), con 57.3% de eventos positivos.
  - Dentro de muestra fue 0.5697% (t 8.72).
  - Fuera de muestra, E supera el costo de un lado (0.34%) en 49.5% de los eventos y el de dos lados en 43.2%.

Día relativo y placebo (detalle en `R09-salida.txt`):

- **Dentro de muestra**, la ventana τ ∈ [−1, +2] (el TOM) queda en el **lugar 1** de 16 ventanas de 4 días (0.1559 pp). Los días τ = −2 a +2 tienen t ≥ 3.3.
- **Fuera de muestra** queda en el **lugar 5** (0.0654 pp). Las primeras son [−5, −2] (0.1084) y [−4, −1] (0.1073).
  - Esto es una descripción, no una prueba: con 20 días relativos se espera algún t ≥ 2 por azar (τ = −4 da 0.233, t 2.5).

Por década (diagnóstico):

| decada | desde | hasta | n | delta | t NW10 | media TOM | media resto |
|---|---|---|---|---|---|---|---|
| 1920s | 1926-07-01 | 1929-12-31 | 1037 | 0.2092 | 2.50 | 0.2342 | 0.0250 |
| 1930s | 1930-01-02 | 1939-12-30 | 2988 | 0.1979 | 2.44 | 0.1797 | -0.0181 |
| 1940s | 1940-01-02 | 1949-12-31 | 2918 | 0.1645 | 4.46 | 0.1705 | 0.0059 |
| 1950s | 1950-01-03 | 1959-12-31 | 2598 | 0.1754 | 5.74 | 0.2093 | 0.0339 |
| 1960s | 1960-01-04 | 1969-12-31 | 2489 | 0.1163 | 3.37 | 0.1278 | 0.0115 |
| 1970s | 1970-01-02 | 1979-12-31 | 2526 | 0.1118 | 2.13 | 0.1174 | 0.0056 |
| 1980s | 1980-01-02 | 1989-12-29 | 2528 | 0.1503 | 2.91 | 0.1879 | 0.0376 |
| 1990s | 1990-01-02 | 1999-12-31 | 2528 | 0.0951 | 2.04 | 0.1457 | 0.0506 |
| 2000s | 2000-01-03 | 2009-12-31 | 2515 | 0.0557 | 0.85 | 0.0534 | -0.0023 |
| 2010s | 2010-01-04 | 2019-12-31 | 2516 | 0.0115 | 0.23 | 0.0646 | 0.0531 |
| 2020s | 2020-01-02 | 2026-07-31 | 1653 | 0.0230 | 0.30 | 0.0836 | 0.0606 |

- δ tiene t NW10 ≥ 2 en todas las décadas de los años veinte a los noventa.
- En los 2000 baja a 0.0557 (t 0.85), en los 2010 a 0.0115 (t 0.23) y en 2020-2026 es 0.0230 (t 0.30).
- [I] El debilitamiento empieza antes de la publicación en el FAJ (2008). Coincide con la circulación de la versión de trabajo (2004-2006) y llega más de diez años después de L&S (1988). La causa no se puede identificar con estos datos.

#### 11.3 Efecto con `^GSPC` (precio, sin dividendos): segunda fuente

| ventana | desde | hasta | n | n TOM | mu (resto) | delta | t MCO | t HC1 | t NW10 | p NW | media TOM |
|---|---|---|---|---|---|---|---|---|---|---|---|
| completo | 1928-01-03 | 2026-08-31 | 24782 | 4736 | 0.0093 | 0.1169 | 6.08 | 6.20 | 6.35 | 0.0000 | 0.1262 |
| dentro_muestra hasta 2008-02 | 1928-01-03 | 2008-02-29 | 20128 | 3848 | 0.0018 | 0.1393 | 6.61 | 6.71 | 6.80 | 0.0000 | 0.1411 |
| fuera_muestra 2008-03 al final | 2008-03-03 | 2026-08-31 | 4654 | 888 | 0.0417 | 0.0198 | 0.42 | 0.44 | 0.47 | 0.6355 | 0.0615 |
| MX panel A 1928-1986 | 1928-01-03 | 1986-12-31 | 14791 | 2832 | -0.0049 | 0.1568 | 6.18 | 6.26 | 6.42 | 0.0000 | 0.1518 |
| MX panel B 1987-2005 | 1987-01-02 | 2005-12-30 | 4794 | 912 | 0.0188 | 0.1126 | 2.82 | 2.91 | 2.80 | 0.0051 | 0.1313 |
| MX panel C 1928-2005 | 1928-01-03 | 2005-12-30 | 19585 | 3744 | 0.0009 | 0.1460 | 6.79 | 6.90 | 6.99 | 0.0000 | 0.1468 |
| hueco 2006-01 a 2008-02 | 2006-01-03 | 2008-02-29 | 543 | 104 | 0.0351 | -0.1010 | -1.03 | -1.02 | -1.21 | 0.2270 | -0.0659 |
| fuera mitad 1 2008-03 a 2016-12 | 2008-03-03 | 2016-12-30 | 2226 | 424 | 0.0290 | 0.0179 | 0.25 | 0.26 | 0.29 | 0.7686 | 0.0470 |
| fuera mitad 2 2017-01 al final | 2017-01-03 | 2026-08-31 | 2428 | 464 | 0.0534 | 0.0214 | 0.36 | 0.37 | 0.37 | 0.7087 | 0.0748 |

| ventana | N | media D | mediana D | t iid | IC95 bootstrap | D>0 | p signo (1 cola) |
|---|---|---|---|---|---|---|---|
| completo | 1183 | 0.1177 | 0.0884 | 6.73 | [0.0835, 0.1513] | 680/1183 (0.575) | 0.0000 |
| dentro_muestra hasta 2008-02 | 962 | 0.1400 | 0.1096 | 7.15 | [0.1009, 0.1784] | 570/962 (0.593) | 0.0000 |
| fuera_muestra 2008-03 al final | 221 | 0.0204 | -0.0048 | 0.53 | [-0.0538, 0.0954] | 110/221 (0.498) | 0.5535 |
| MX panel A 1928-1986 | 708 | 0.1586 | 0.1208 | 6.80 | [0.1133, 0.2041] | 426/708 (0.602) | 0.0000 |
| MX panel B 1987-2005 | 228 | 0.1118 | 0.1063 | 2.91 | [0.0363, 0.1850] | 134/228 (0.588) | 0.0048 |
| MX panel C 1928-2005 | 936 | 0.1472 | 0.1188 | 7.37 | [0.1080, 0.1853] | 560/936 (0.598) | 0.0000 |
| hueco 2006-01 a 2008-02 | 26 | -0.1187 | -0.0927 | -1.70 | [-0.2599, 0.0078] | 10/26 (0.385) | 0.9157 |
| fuera mitad 1 2008-03 a 2016-12 | 106 | 0.0219 | 0.0036 | 0.41 | [-0.0802, 0.1283] | 53/106 (0.500) | 0.5387 |
| fuera mitad 2 2017-01 al final | 115 | 0.0189 | -0.0076 | 0.35 | [-0.0869, 0.1228] | 57/115 (0.496) | 0.5739 |

| ventana | meses | TOM 4 dias | mes completo | resto del mes | TOM/mes | E medio | t iid E | IC95 E | E>0 | E > 0.34 | E > 0.68 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| completo | 1183 | 0.5051 | 0.6552 | 0.1508 | 0.77 | 0.4551 | 6.95 | [0.3244, 0.5834] | 0.614 | 0.543 | 0.476 |
| dentro_muestra hasta 2008-02 | 962 | 0.5658 | 0.6017 | 0.0326 | 0.94 | 0.5093 | 6.91 | [0.3636, 0.6516] | 0.624 | 0.557 | 0.490 |
| fuera_muestra 2008-03 al final | 221 | 0.2408 | 0.8881 | 0.6650 | 0.27 | 0.2188 | 1.56 | [-0.0514, 0.4957] | 0.570 | 0.480 | 0.416 |
| MX panel A 1928-1986 | 708 | 0.6149 | 0.5434 | -0.0736 | 1.13 | 0.5628 | 6.34 | [0.3891, 0.7383] | 0.637 | 0.562 | 0.501 |
| MX panel B 1987-2005 | 228 | 0.5164 | 0.8195 | 0.3030 | 0.63 | 0.4480 | 3.23 | [0.1774, 0.7111] | 0.596 | 0.557 | 0.474 |
| MX panel C 1928-2005 | 936 | 0.5909 | 0.6106 | 0.0182 | 0.97 | 0.5349 | 7.12 | [0.3872, 0.6788] | 0.627 | 0.561 | 0.495 |
| hueco 2006-01 a 2008-02 | 26 | -0.3365 | 0.2807 | 0.5536 | -1.20 | -0.4092 | -1.39 | [-0.9980, 0.1176] | 0.500 | 0.423 | 0.308 |
| fuera mitad 1 2008-03 a 2016-12 | 106 | 0.1890 | 0.5966 | 0.4196 | 0.32 | 0.1866 | 0.87 | [-0.2261, 0.6069] | 0.547 | 0.462 | 0.387 |
| fuera mitad 2 2017-01 al final | 115 | 0.2885 | 1.1567 | 0.8912 | 0.25 | 0.2485 | 1.35 | [-0.1167, 0.6011] | 0.591 | 0.496 | 0.443 |

Mismo patrón que con French:

- Dentro de muestra, δ = 0.1393 (t NW10 6.80).
- Fuera de muestra, δ = 0.0198 (t 0.47), con D_m de 0.0204 (IC95 [−0.0538, 0.0954]).
- E fuera de muestra: 0.2188% (t 1.56; IC95 [−0.0514, 0.4957]).

#### 11.4 Estrategia contra las reglas sencillas, con costos por defecto

**French, dentro de muestra (1927-03 a 2008-02)**

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual | exceso_bruto_anual | costo_equilibrio_lado |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US_tom_m1_p3 | 0.0193 | 0.0687 | -0.1916 | -1.7567 | -0.2749 | -0.3409 | 0.1810 | 23.9895 | 0.0816 | 0.0678 | 0.0028 |
| US_tom_m2_p3 | 0.0298 | 0.0770 | -0.0362 | -0.3304 | -0.0530 | -0.4080 | 0.2263 | 23.9895 | 0.0816 | 0.0787 | 0.0033 |
| US_tom_m3_p3 | 0.0295 | 0.0853 | -0.0278 | -0.2536 | -0.0397 | -0.5394 | 0.2716 | 23.9895 | 0.0816 | 0.0791 | 0.0033 |
| US_tom_m1_p2 | 0.0017 | 0.0593 | -0.5111 | -4.7931 | -0.6957 | -0.6050 | 0.1358 | 23.9895 | 0.0816 | 0.0497 | 0.0021 |
| US_tom_m1_p4 | 0.0268 | 0.0785 | -0.0698 | -0.6281 | -0.1028 | -0.3773 | 0.2263 | 24.0142 | 0.0816 | 0.0760 | 0.0032 |
| US_ref_comprar_mantener | 0.0977 | 0.1644 | 0.4167 | 3.5901 | 0.5884 | -0.8407 | 1.0000 | 0.0123 | 0.0000 | 0.0721 | 5.8375 |
| US_ref_efectivo | 0.0361 | 0.0020 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | NA |
| US_ref_sma200 | 0.0979 | 0.1110 | 0.5525 | 4.6660 | 0.7772 | -0.3819 | 0.7136 | 5.7288 | 0.0195 | 0.0840 | 0.0147 |
| US_ref_resto | -0.0525 | 0.1505 | -0.4890 | -4.2305 | -0.6697 | -0.9915 | 0.8190 | 24.0018 | 0.0816 | 0.0043 | 0.0002 |

**French, fuera de muestra (2008-03 a 2026-07). Es el tramo de prueba, mirado una sola vez.**

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual | exceso_bruto_anual | costo_equilibrio_lado |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US_tom_m1_p3 | -0.0418 | 0.0860 | -0.6157 | -2.9616 | -0.8173 | -0.5931 | 0.1908 | 23.9989 | 0.0816 | 0.0288 | 0.0012 |
| US_tom_m2_p3 | -0.0267 | 0.0956 | -0.3809 | -1.8365 | -0.5101 | -0.4680 | 0.2385 | 23.9989 | 0.0816 | 0.0453 | 0.0019 |
| US_tom_m3_p3 | -0.0196 | 0.1034 | -0.2741 | -1.3481 | -0.3715 | -0.3770 | 0.2862 | 23.9989 | 0.0816 | 0.0533 | 0.0022 |
| US_tom_m1_p2 | -0.0504 | 0.0749 | -0.8390 | -3.9722 | -1.1008 | -0.6469 | 0.1431 | 23.9989 | 0.0816 | 0.0189 | 0.0008 |
| US_tom_m1_p4 | -0.0479 | 0.0990 | -0.5874 | -2.7979 | -0.7739 | -0.6365 | 0.2385 | 23.9989 | 0.0816 | 0.0235 | 0.0010 |
| US_ref_comprar_mantener | 0.1204 | 0.2014 | 0.5979 | 2.9449 | 0.8380 | -0.5073 | 1.0000 | 0.0000 | 0.0000 | 0.1202 | NA |
| US_ref_efectivo | 0.0140 | 0.0012 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | NA |
| US_ref_sma200 | 0.0765 | 0.1204 | 0.5585 | 2.3577 | 0.7572 | -0.2490 | 0.7775 | 5.3753 | 0.0183 | 0.0854 | 0.0159 |
| US_ref_resto | 0.0068 | 0.1838 | 0.0536 | 0.2551 | 0.0743 | -0.4827 | 0.8092 | 23.9989 | 0.0816 | 0.0914 | 0.0038 |

**`^GSPC`, dentro de muestra (1928-10 a 2008-02)**

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual | exceso_bruto_anual | costo_equilibrio_lado |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SPX_tom_m1_p3 | 0.0114 | 0.0819 | -0.2555 | -2.3338 | -0.3637 | -0.4271 | 0.1911 | 24.0023 | 0.0816 | 0.0608 | 0.0025 |
| SPX_tom_m2_p3 | 0.0197 | 0.0913 | -0.1307 | -1.1904 | -0.1883 | -0.5569 | 0.2390 | 24.0023 | 0.0816 | 0.0698 | 0.0029 |
| SPX_tom_m3_p3 | 0.0168 | 0.0999 | -0.1389 | -1.2563 | -0.1974 | -0.6267 | 0.2868 | 24.0023 | 0.0816 | 0.0678 | 0.0028 |
| SPX_tom_m1_p2 | -0.0026 | 0.0702 | -0.5099 | -4.7469 | -0.7068 | -0.5868 | 0.1434 | 24.0023 | 0.0816 | 0.0460 | 0.0019 |
| SPX_tom_m1_p4 | 0.0170 | 0.0932 | -0.1541 | -1.4167 | -0.2283 | -0.4418 | 0.2389 | 24.0023 | 0.0816 | 0.0673 | 0.0028 |
| SPX_ref_comprar_mantener | 0.0531 | 0.1873 | 0.1809 | 1.6099 | 0.2553 | -0.8619 | 1.0000 | 0.0126 | 0.0000 | 0.0338 | 2.6827 |
| SPX_ref_efectivo | 0.0362 | 0.0020 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | NA |
| SPX_ref_sma200 | 0.0582 | 0.1234 | 0.2333 | 2.1053 | 0.3257 | -0.5388 | 0.6577 | 6.0730 | 0.0206 | 0.0493 | 0.0081 |
| SPX_ref_resto | -0.0838 | 0.1695 | -0.6435 | -5.7650 | -0.8831 | -0.9992 | 0.8089 | 24.0149 | 0.0817 | -0.0270 | -0.0011 |

**`^GSPC`, fuera de muestra (2008-03 a 2026-07)**

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual | exceso_bruto_anual | costo_equilibrio_lado |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SPX_tom_m1_p3 | -0.0448 | 0.0844 | -0.6654 | -3.2610 | -0.8829 | -0.6152 | 0.1908 | 23.9989 | 0.0816 | 0.0255 | 0.0011 |
| SPX_tom_m2_p3 | -0.0320 | 0.0942 | -0.4453 | -2.1935 | -0.5938 | -0.5170 | 0.2385 | 23.9989 | 0.0816 | 0.0398 | 0.0017 |
| SPX_tom_m3_p3 | -0.0268 | 0.1016 | -0.3538 | -1.7929 | -0.4768 | -0.4500 | 0.2862 | 23.9989 | 0.0816 | 0.0457 | 0.0019 |
| SPX_tom_m1_p2 | -0.0526 | 0.0737 | -0.8863 | -4.2337 | -1.1624 | -0.6621 | 0.1431 | 23.9989 | 0.0816 | 0.0164 | 0.0007 |
| SPX_tom_m1_p4 | -0.0514 | 0.0972 | -0.6374 | -3.0849 | -0.8384 | -0.6583 | 0.2385 | 23.9989 | 0.0816 | 0.0197 | 0.0008 |
| SPX_ref_comprar_mantener | 0.0984 | 0.1987 | 0.5028 | 2.5279 | 0.7042 | -0.5258 | 1.0000 | 0.0000 | 0.0000 | 0.0997 | NA |
| SPX_ref_efectivo | 0.0140 | 0.0012 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | NA |
| SPX_ref_sma200 | 0.0542 | 0.1155 | 0.3956 | 1.6930 | 0.5325 | -0.2378 | 0.7734 | 5.8097 | 0.0198 | 0.0654 | 0.0112 |
| SPX_ref_resto | -0.0100 | 0.1816 | -0.0407 | -0.1964 | -0.0563 | -0.5291 | 0.8092 | 23.9989 | 0.0816 | 0.0742 | 0.0031 |

**Ventanas pre-registradas, French**

| variante | ventana | n | cagr | vol_anual | sharpe | nw_t | mdd | exposicion_media | costo_equilibrio_lado |
|---|---|---|---|---|---|---|---|---|---|
| US_tom_m1_p3 | MX panel A (1927-03-03 a 1986-12-31) | 16126 | 0.0203 | 0.0678 | -0.1378 | -1.10 | -0.3409 | 0.1779 | 0.0030 |
| US_tom_m1_p3 | MX panel B (1986-12-31 a 2005-12-30) | 4794 | 0.0264 | 0.0718 | -0.2019 | -0.86 | -0.2190 | 0.1902 | 0.0028 |
| US_tom_m1_p3 | hueco (2005-12-30 a 2008-02-29) | 543 | -0.0676 | 0.0661 | -1.7346 | -2.81 | -0.1579 | 0.1915 | -0.0014 |
| US_tom_m1_p3 | fuera de muestra (2008-02-29 a 2026-07-31) | 4633 | -0.0418 | 0.0860 | -0.6157 | -2.96 | -0.5931 | 0.1908 | 0.0012 |
| US_tom_m1_p3 | fuera mitad 1 (2008-02-29 a 2016-12-30) | 2226 | -0.0551 | 0.0916 | -0.5908 | -1.99 | -0.4217 | 0.1905 | 0.0011 |
| US_tom_m1_p3 | fuera mitad 2 (2016-12-30 a 2026-07-31) | 2407 | -0.0294 | 0.0804 | -0.6445 | -2.20 | -0.3096 | 0.1911 | 0.0012 |
| US_ref_comprar_mantener | MX panel A (1927-03-03 a 1986-12-31) | 16126 | 0.0945 | 0.1649 | 0.4094 | 2.96 | -0.8407 | 1.0000 | 4.3255 |
| US_ref_comprar_mantener | MX panel B (1986-12-31 a 2005-12-30) | 4794 | 0.1133 | 0.1648 | 0.4721 | 2.12 | -0.4923 | 1.0000 | NA |
| US_ref_comprar_mantener | hueco (2005-12-30 a 2008-02-29) | 543 | 0.0523 | 0.1424 | 0.1043 | 0.19 | -0.1599 | 1.0000 | NA |
| US_ref_comprar_mantener | fuera de muestra (2008-02-29 a 2026-07-31) | 4633 | 0.1204 | 0.2014 | 0.5979 | 2.94 | -0.5073 | 1.0000 | NA |
| US_ref_comprar_mantener | fuera mitad 1 (2008-02-29 a 2016-12-30) | 2226 | 0.0879 | 0.2145 | 0.4925 | 1.73 | -0.5073 | 1.0000 | NA |
| US_ref_comprar_mantener | fuera mitad 2 (2016-12-30 a 2026-07-31) | 2407 | 0.1513 | 0.1884 | 0.7113 | 2.45 | -0.3422 | 1.0000 | NA |
| US_ref_sma200 | MX panel A (1927-03-03 a 1986-12-31) | 16126 | 0.1061 | 0.1103 | 0.6339 | 4.55 | -0.3819 | 0.6983 | 0.0171 |
| US_ref_sma200 | MX panel B (1986-12-31 a 2005-12-30) | 4794 | 0.0887 | 0.1132 | 0.4252 | 1.79 | -0.3810 | 0.7524 | 0.0120 |
| US_ref_sma200 | hueco (2005-12-30 a 2008-02-29) | 543 | -0.0367 | 0.1117 | -0.6965 | -1.06 | -0.1899 | 0.8250 | -0.0024 |
| US_ref_sma200 | fuera de muestra (2008-02-29 a 2026-07-31) | 4633 | 0.0765 | 0.1204 | 0.5585 | 2.36 | -0.2490 | 0.7775 | 0.0159 |
| US_ref_sma200 | fuera mitad 1 (2008-02-29 a 2016-12-30) | 2226 | 0.0551 | 0.1163 | 0.5051 | 1.51 | -0.2490 | 0.7314 | 0.0140 |
| US_ref_sma200 | fuera mitad 2 (2016-12-30 a 2026-07-31) | 2407 | 0.0967 | 0.1241 | 0.6053 | 1.81 | -0.2200 | 0.8201 | 0.0178 |
| US_ref_resto | MX panel A (1927-03-03 a 1986-12-31) | 16126 | -0.0589 | 0.1514 | -0.4999 | -3.66 | -0.9863 | 0.8221 | 0.0000 |
| US_ref_resto | MX panel B (1986-12-31 a 2005-12-30) | 4794 | -0.0383 | 0.1496 | -0.4735 | -2.08 | -0.6250 | 0.8098 | 0.0004 |
| US_ref_resto | hueco (2005-12-30 a 2008-02-29) | 543 | 0.0036 | 0.1277 | -0.2719 | -0.53 | -0.1371 | 0.8085 | 0.0020 |
| US_ref_resto | fuera de muestra (2008-02-29 a 2026-07-31) | 4633 | 0.0068 | 0.1838 | 0.0536 | 0.26 | -0.4827 | 0.8092 | 0.0038 |
| US_ref_resto | fuera mitad 1 (2008-02-29 a 2016-12-30) | 2226 | -0.0206 | 0.1958 | -0.0170 | -0.06 | -0.4827 | 0.8095 | 0.0033 |
| US_ref_resto | fuera mitad 2 (2016-12-30 a 2026-07-31) | 2407 | 0.0328 | 0.1720 | 0.1282 | 0.41 | -0.3860 | 0.8089 | 0.0043 |

Lectura:

- **Con los costos de GBM, la regla del artículo no sobrevivió ni en su mejor época.** Dentro de muestra:
  - `US_tom_m1_p3` rindió 1.93% anual, contra 3.61% del efectivo, con Sharpe de −0.1916.
  - El costo por lado de equilibrio fue 0.28%, menor que el 0.34% supuesto.
  - Bruta, en cambio, tuvo un Sharpe de 0.9544, contra 0.4170 de comprar y mantener (sección 12). El efecto existía; lo que no alcanzaba era para pagar 24 lados al año a 0.34%.
- **Fuera de muestra pierde contra todo:**
  - `US_tom_m1_p3`: CAGR −4.18%, Sharpe −0.6157 (t NW10 −2.96) y MDD −59.31%. Su costo por lado de equilibrio fue 0.12%.
  - Comprar y mantener: 12.04%, 0.5979 y −50.73%.
  - SMA200: 7.65%, 0.5585 y −24.90%.
  - Efectivo: 1.40%.
- **Ninguna de las 5 ventanas tiene Sharpe neto positivo** en ningún segmento, ni con French ni con `^GSPC`.
- **El MDD de la regla TOM es peor que el de comprar y mantener fuera de muestra** (−59.31% contra −50.73%) pese a estar invertida solo 19% de los días. Viene de la erosión continua de 8.16% anual de costos, no del riesgo de mercado.

**Criterios pre-registrados** (salida textual del script):

- (i) French 1926-07..2005-12: delta_MX=0.1487 (articulo 0.15; |dif|=0.0013 <= 0.03?), t MCO=8.03 -> True
- (ii) French dentro de muestra: delta=0.1405, t NW10=7.75 -> True
- (iii) French fuera de muestra: delta=0.0150 -> True
- (iv) ^GSPC fuera de muestra: delta=0.0198 -> True
- Estado segun la regla pre-registrada: Replicado
- H1b: exceso de 'otros dias' 1926-2005 = -0.0010 (t -0.12) -> no distinto de cero
- H1c (L&S con ^GSPC 1928-1986): TOM 4 dias 0.6149% contra mes 0.5434% -> TOM >= mes
- Significativo fuera de muestra US (t NW10 >= 2 y IC95 bootstrap de D excluye 0): False (t NW10=0.35; IC95 D=[-0.0623, 0.0920])
- Significativo fuera de muestra SPX (t NW10 >= 2 y IC95 bootstrap de D excluye 0): False (t NW10=0.47; IC95 D=[-0.0538, 0.0954])
- US_tom_m1_p3 fuera de muestra, neto defecto: Sharpe -0.6157 (t NW10 -2.96), CAGR -0.0418, MDD -0.5931; comprar y mantener: Sharpe 0.5979, CAGR 0.1204, MDD -0.5073; SMA200: Sharpe 0.5585, CAGR 0.0765, MDD -0.2490 -> S1 (sobrevive a costos)=False; S2 (vs comprar y mantener)=False; S3 (vs SMA200)=False
- SPX_tom_m1_p3 fuera de muestra, neto defecto: Sharpe -0.6654 (t NW10 -3.26), CAGR -0.0448, MDD -0.6152; comprar y mantener: Sharpe 0.5028, CAGR 0.0984, MDD -0.5258; SMA200: Sharpe 0.3956, CAGR 0.0542, MDD -0.2378 -> S1 (sobrevive a costos)=False; S2 (vs comprar y mantener)=False; S3 (vs SMA200)=False
- E fuera de muestra French: media 0.2307% (t iid 1.58; IC95 [-0.0527, 0.5178]); ^GSPC: media 0.2188% (t iid 1.56; IC95 [-0.0514, 0.4957])
- Regla TOM de arena/investigacion/03 (renglon TOM y [R] 5) segun el criterio pre-registrado: modificar (a): E > 0 no significativo; timing solo como desempate sin costo; grado C

### 12. Sensibilidad

**Costos.** French fuera de muestra, bruto:

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual | exceso_bruto_anual | costo_equilibrio_lado |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US_tom_m1_p3 | 0.0398 | 0.0843 | 0.3418 | 1.6179 | 0.4766 | -0.1581 | 0.1908 | 23.9989 | 0.0000 | 0.0288 | 0.0012 |
| US_tom_m2_p3 | 0.0562 | 0.0948 | 0.4788 | 2.2848 | 0.6675 | -0.1562 | 0.2385 | 23.9989 | 0.0000 | 0.0453 | 0.0019 |
| US_tom_m3_p3 | 0.0639 | 0.1023 | 0.5223 | 2.5355 | 0.7329 | -0.1656 | 0.2862 | 23.9989 | 0.0000 | 0.0533 | 0.0022 |
| US_tom_m1_p2 | 0.0305 | 0.0730 | 0.2592 | 1.2089 | 0.3630 | -0.1497 | 0.1431 | 23.9989 | 0.0000 | 0.0189 | 0.0008 |
| US_tom_m1_p4 | 0.0332 | 0.0976 | 0.2417 | 1.1383 | 0.3300 | -0.2476 | 0.2385 | 23.9989 | 0.0000 | 0.0235 | 0.0010 |
| US_ref_comprar_mantener | 0.1204 | 0.2014 | 0.5979 | 2.9449 | 0.8380 | -0.5073 | 1.0000 | 0.0000 | 0.0000 | 0.1202 | NA |
| US_ref_efectivo | 0.0140 | 0.0012 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | NA |
| US_ref_sma200 | 0.0964 | 0.1201 | 0.7127 | 3.1165 | 0.9725 | -0.2203 | 0.7775 | 5.3753 | 0.0000 | 0.0854 | 0.0159 |
| US_ref_resto | 0.0926 | 0.1829 | 0.5007 | 2.3777 | 0.7027 | -0.4455 | 0.8092 | 23.9989 | 0.0000 | 0.0914 | 0.0038 |

French fuera de muestra, spread "medio" (0.15% por lado):

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual | exceso_bruto_anual | costo_equilibrio_lado |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US_tom_m1_p3 | -0.0646 | 0.0870 | -0.8848 | -4.2799 | -1.1551 | -0.7352 | 0.1908 | 23.9989 | 0.1056 | 0.0288 | 0.0012 |
| US_tom_m2_p3 | -0.0499 | 0.0963 | -0.6277 | -3.0404 | -0.8293 | -0.6541 | 0.2385 | 23.9989 | 0.1056 | 0.0453 | 0.0019 |
| US_tom_m3_p3 | -0.0429 | 0.1041 | -0.5030 | -2.4876 | -0.6734 | -0.5931 | 0.2862 | 23.9989 | 0.1056 | 0.0533 | 0.0022 |
| US_tom_m1_p2 | -0.0730 | 0.0760 | -1.1423 | -5.4343 | -1.4676 | -0.7705 | 0.1431 | 23.9989 | 0.1056 | 0.0189 | 0.0008 |
| US_tom_m1_p4 | -0.0706 | 0.0999 | -0.8229 | -3.9381 | -1.0707 | -0.7632 | 0.2385 | 23.9989 | 0.1056 | 0.0235 | 0.0010 |
| US_ref_comprar_mantener | 0.1204 | 0.2014 | 0.5979 | 2.9449 | 0.8380 | -0.5073 | 1.0000 | 0.0000 | 0.0000 | 0.1202 | NA |
| US_ref_efectivo | 0.0140 | 0.0012 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | NA |
| US_ref_sma200 | 0.0707 | 0.1206 | 0.5130 | 2.1420 | 0.6938 | -0.2573 | 0.7775 | 5.3753 | 0.0237 | 0.0854 | 0.0159 |
| US_ref_resto | -0.0171 | 0.1844 | -0.0769 | -0.3662 | -0.1061 | -0.5551 | 0.8092 | 23.9989 | 0.1056 | 0.0914 | 0.0038 |

French dentro de muestra, bruto:

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual | exceso_bruto_anual | costo_equilibrio_lado |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US_tom_m1_p3 | 0.1061 | 0.0676 | 0.9544 | 8.5009 | 1.4725 | -0.2278 | 0.1810 | 23.9895 | 0.0000 | 0.0678 | 0.0028 |
| US_tom_m2_p3 | 0.1175 | 0.0756 | 0.9897 | 8.7606 | 1.5441 | -0.2837 | 0.2263 | 23.9895 | 0.0000 | 0.0787 | 0.0033 |
| US_tom_m3_p3 | 0.1172 | 0.0837 | 0.8984 | 7.9879 | 1.3508 | -0.4233 | 0.2716 | 23.9895 | 0.0000 | 0.0791 | 0.0033 |
| US_tom_m1_p2 | 0.0869 | 0.0581 | 0.8144 | 7.4236 | 1.2114 | -0.3208 | 0.1358 | 23.9895 | 0.0000 | 0.0497 | 0.0021 |
| US_tom_m1_p4 | 0.1143 | 0.0775 | 0.9318 | 8.1909 | 1.4531 | -0.2753 | 0.2263 | 24.0142 | 0.0000 | 0.0760 | 0.0032 |
| US_ref_comprar_mantener | 0.0977 | 0.1644 | 0.4170 | 3.5922 | 0.5888 | -0.8407 | 1.0000 | 0.0123 | 0.0000 | 0.0721 | 5.8375 |
| US_ref_efectivo | 0.0361 | 0.0020 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | NA |
| US_ref_sma200 | 0.1196 | 0.1109 | 0.7205 | 6.2256 | 1.0196 | -0.3356 | 0.7136 | 5.7288 | 0.0000 | 0.0840 | 0.0147 |
| US_ref_resto | 0.0283 | 0.1499 | 0.0271 | 0.2342 | 0.0377 | -0.8282 | 0.8190 | 24.0018 | 0.0000 | 0.0043 | 0.0002 |

- **Bruto (sin costos) y fuera de muestra**, `US_tom_m1_p3` tiene un Sharpe de 0.3418 (t NW10 1.62), contra 0.5979 de comprar y mantener y 0.7127 de la SMA200. **Aun sin costos**, la regla del artículo queda debajo de comprar y mantener después de 2008.
- Las ventanas más anchas tienen t NW10 ≥ 2 en bruto (`US_tom_m2_p3` 2.28 y `US_tom_m3_p3` 2.54), pero su Sharpe (0.4788 y 0.5223) también queda debajo del de comprar y mantener.
- Con spread "medio", `US_tom_m1_p3` fuera de muestra da CAGR −6.46% y Sharpe −0.8848.

**Costo por lado de equilibrio** (corridas por defecto; exceso bruto acumulado / rotación acumulada):

| variante | equilibrio por lado, dentro de muestra | equilibrio por lado, fuera de muestra |
|---|---|---|
| US_tom_m1_p3 | 0.0028 | 0.0012 |
| US_tom_m2_p3 | 0.0033 | 0.0019 |
| US_tom_m3_p3 | 0.0033 | 0.0022 |
| US_tom_m1_p2 | 0.0021 | 0.0008 |
| US_tom_m1_p4 | 0.0032 | 0.0010 |
| SPX_tom_m1_p3 | 0.0025 | 0.0011 |
| SPX_tom_m2_p3 | 0.0029 | 0.0017 |
| SPX_tom_m3_p3 | 0.0028 | 0.0019 |
| SPX_tom_m1_p2 | 0.0019 | 0.0007 |
| SPX_tom_m1_p4 | 0.0028 | 0.0008 |

- Ninguna ventana llega al 0.34% por lado de GBM, ni siquiera dentro de muestra. Las más cercanas son `US_tom_m2_p3` y `US_tom_m3_p3`, con 0.33%.
- Fuera de muestra, el equilibrio va de 0.07% a 0.22% por lado.

**Parámetros vecinos:** las 5 ventanas tienen Sharpe neto negativo (tablas de 11.4).

**Subperiodos:** décadas (11.2) y mitades del tramo fuera de muestra. En las dos mitades, `US_tom_m1_p3` tiene Sharpe neto de −0.5908 y −0.6445.

**Otra moneda (MXN).** French convertido con DEXMXUS y efectivo en CETES:

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual | exceso_bruto_anual | costo_equilibrio_lado |
|---|---|---|---|---|---|---|---|---|---|---|---|
| USMXN_tom_m1_p3 | 0.0847 | 0.0921 | -0.8717 | -3.1952 | -1.1580 | -0.2011 | 0.1901 | 23.9726 | 0.0815 | 0.0018 | 0.0001 |
| USMXN_ref_comprar_mantener | 0.1934 | 0.2207 | 0.1608 | 0.6474 | 0.2524 | -0.4567 | 1.0000 | 0.0699 | 0.0002 | 0.0357 | 0.5105 |
| USMXN_ref_efectivo | 0.1796 | 0.0112 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | NA |
| USMXN_ref_sma200 | 0.1618 | 0.1872 | 0.0094 | 0.0369 | 0.0152 | -0.2321 | 0.7405 | 7.9676 | 0.0271 | 0.0289 | 0.0036 |

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual | exceso_bruto_anual | costo_equilibrio_lado |
|---|---|---|---|---|---|---|---|---|---|---|---|
| USMXN_tom_m1_p3 | -0.0113 | 0.0827 | -0.8448 | -4.3766 | -1.0925 | -0.3779 | 0.1908 | 23.9989 | 0.0816 | 0.0119 | 0.0005 |
| USMXN_ref_comprar_mantener | 0.1500 | 0.1976 | 0.4944 | 2.7620 | 0.7238 | -0.3075 | 1.0000 | 0.0000 | 0.0000 | 0.0976 | NA |
| USMXN_ref_efectivo | 0.0636 | 0.0030 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | NA |
| USMXN_ref_sma200 | 0.1034 | 0.1243 | 0.3583 | 1.5538 | 0.5089 | -0.2422 | 0.7775 | 5.3753 | 0.0183 | 0.0627 | 0.0117 |

Traducción a una cuenta de 20,000 MXN (salida textual; es una simulación, no un rendimiento realizado):

- Costo anual de US_tom_m1_p3 fuera de muestra con costos por defecto: 0.0816 del capital = 1,632 MXN al anio (24.00 operaciones al anio)
- Costo de un lado: 0.0034 x 20,000 = 68 MXN
- Prima media por evento fuera de muestra (French): 0.2307% x 20,000 = 46 MXN (x12 = 554 MXN al anio, antes de costos); IC95 [-11, 104] MXN por evento
- Prima media por evento fuera de muestra (^GSPC): 0.2188% x 20,000 = 44 MXN (x12 = 525 MXN al anio, antes de costos); IC95 [-10, 99] MXN por evento
- USMXN_tom_m1_p3: 20,000 MXN el 2008-02-29 -> 16,209 MXN el 2026-07-31 (CAGR -0.0113, MDD -0.3779)
- USMXN_ref_comprar_mantener: 20,000 MXN el 2008-02-29 -> 262,339 MXN el 2026-07-31 (CAGR 0.1500, MDD -0.3075)
- USMXN_ref_efectivo: 20,000 MXN el 2008-02-29 -> 62,262 MXN el 2026-07-31 (CAGR 0.0636, MDD 0.0000)
- USMXN_ref_sma200: 20,000 MXN el 2008-02-29 -> 122,456 MXN el 2026-07-31 (CAGR 0.1034, MDD -0.2422)

**Magnitud económica contra significancia estadística.** Separar las dos cosas es una de las ideas del protocolo externo que compartió el dueño.

- Dentro de muestra, el efecto era **estadísticamente** muy fuerte (t ≈ 8). **Económicamente** no alcanzaba para GBM: E medio de 0.5697% por evento contra 0.68% de ida y vuelta. Solo el 50.8% de los eventos superó ese costo.
- Fuera de muestra no es significativo (t 1.58) y es pequeño: 0.2307% por evento, un tercio del costo de ida y vuelta.
- En la cuenta de 20,000 MXN son 46 MXN de prima media por evento, contra 136 MXN de ida y vuelta (68 MXN por lado).
- [I] ¿Cuánto de E se debe al calendario? Con las cifras de 11.2, fuera de muestra 4 × δ = 4 × 0.0150 = 0.06 pp por evento (≈12 MXN en 20,000). El resto de E (≈0.17 pp) es lo que habría dado cualquier bloque de 4 días en el mercado (μ del resto = 0.0504 pp por día). **Lo que se gana al "comprar antes del cambio de mes" es casi todo prima de mercado, no calendario.**

### 13. Diferencia frente al artículo

| Aspecto | Artículo | Réplica | ¿Explica la diferencia? |
|---|---|---|---|
| Datos y versión (McConnell-Xu) | Índice CRSP VW, datos hasta 2005, versión de trabajo del 14-jul-2006 (la publicada no se leyó) | French Mkt-RF + RF, CRSP 202607, sha256 `1916d331…a8` | Diferencias ≤ 0.0118 pp por celda; no hay nada material que explicar. La versión publicada podría traer otras cifras |
| Datos (L&S) | DJIA de precio, 1897-1986. Cifra citada por McConnell-Xu; el original no se leyó | `^GSPC` de precio, 1928-1986 (y French con rendimiento total) | El patrón coincide: TOM ≥ mes y resto negativo con el índice de precio. Las magnitudes son mayores (0.6149 contra 0.473 en el TOM), con otro índice y otro periodo; no se atribuye la diferencia |
| Periodo | 1926-2005 (McConnell-Xu); 1897-1986 (L&S) | French 1926-07 a 2026-07; `^GSPC` 1928-01 a 2026-08 | El efecto se sostiene en 1987-2005 (panel B: 0.1465, t 3.82) y se apaga desde los 2000 |
| Método | t de diferencia de medias (dos muestras) | MCO, HC1, NW(10), Welch, D_m pareada con bootstrap, signo, winsorización, sin diciembre-enero, sin cierres y placebo | Dentro de muestra todas las pruebas coinciden; fuera de muestra ninguna es significativa |
| Costos | McConnell-Xu no modelan costos. Citan a Hensel y Ziemba (1996): el TOM le gana a comprar y mantener por ≈0.63% anual en 1928-1993 (no verificado) | GBM: 0.29% + 0.05% por lado; 24 lados al año ≈ 8.16% anual | Con costos de GBM, el TOM no pagaba ni dentro de muestra (equilibrio de 0.28% por lado) |
| Regla | Mercado en [−1, +3] y T-bills el resto (Hensel-Ziemba; Quantpedia) | La misma, ejecutada al cierre, con la RF de French | — |
| Cifra de Quantpedia citada en `arena/03` (secundaria) | 7.2% anual, vol de 6.9%, Sharpe de 1.04, 1926-2005 (no verificado) | Bruto, 1927-03 a 2008-02: CAGR 10.61%, vol 6.76%, Sharpe 0.9544 | Vol y Sharpe del mismo orden. El CAGR no es comparable: no se sabe si el 7.2% es exceso o rendimiento total, ni el periodo exacto |
| Cifra de `arena/03`: "0.15% contra −0.001%, 1926-2005" | En la versión de 2006, −0.001 es de **1987-2005**. En 1926-2005 la cifra es 0.16 contra 0.01 (bruto) o 0.15 contra 0.00 (exceso) | Réplica 1926-2005: 0.1614 contra 0.0128 (bruto); 0.1476 contra −0.0010 (exceso) | Error de atribución de periodo en `arena/03` |

### 14. Conclusiones permitidas

- **El hallazgo de McConnell-Xu se reproduce casi exacto en su periodo y con datos equivalentes** (CRSP VW vía French, 1926-2005, USD).
  - TOM − otros días = 0.1487 pp por día (t 8.03), contra 0.15 (t 8.06).
  - También se reproducen sus paneles de 1926-1986 y 1987-2005.
  - Y su tabla 2: en exceso sobre la RF, los otros días rinden −0.0010 pp (t −0.12).
- **El patrón de L&S aparece con el S&P 500 de precio en 1928-1986.** El TOM rinde más que el mes completo (0.6149% contra 0.5434%) y el resto del mes es negativo (−0.0736%).
- **Dentro de muestra (1926-07 a 2008-02), el efecto es grande y resiste todas las pruebas pre-registradas** (t NW10 de 7.27 a 8.02). Aparece con t ≥ 2 en cada década, de los años veinte a los noventa, y en las dos fuentes (French y `^GSPC`).
- **Fuera de muestra (2008-03 a 2026-07/08) tiene el mismo signo, pero es casi cero en lo económico y en lo estadístico.**
  - δ = 0.0150 pp (t 0.35) en French y 0.0198 (t 0.47) en `^GSPC`.
  - El IC95 de D_m incluye el cero, y solo el 49% de los meses es positivo.
  - En 2008-2026 el mercado también pagó premio fuera del cambio de mes.
- **Como estrategia sola, con costos de GBM (0.34% por lado), la regla del artículo tuvo exceso neto negativo sobre el efectivo en todos los tramos**, incluso dentro de muestra (Sharpe −0.1916).
  - Fuera de muestra perdió 4.18% anual en USD (Sharpe −0.6157, t −2.96) y 1.13% anual en MXN.
  - El costo por lado de equilibrio fue 0.28% dentro de muestra y 0.12% fuera.
- **Aun sin costos, fuera de muestra la regla del artículo no supera a comprar y mantener** (Sharpe 0.3418 contra 0.5979) ni a la SMA200 (0.7127).
- **Cuenta de 20,000 MXN, 2008-03 a 2026-07.** Es una simulación con DEXMXUS y CETES, no un rendimiento realizado:
  - La regla TOM habría llevado 20,000 MXN a 16,209 MXN.
  - Comprar y mantener, a 262,339 MXN; CETES, a 62,262 MXN; la SMA200, a 122,456 MXN.
  - Los costos de la regla TOM suman ≈1,632 MXN al año.

### 15. Conclusiones que NO se sostienen

- **"El cambio de mes sigue funcionando en EUA."** Después de 2008, δ = 0.0150 pp (t 0.35) y el TOM queda en el lugar 5 de 16 en el placebo.
- **"Los inversionistas solo reciben premio en el cambio de mes"**, como hecho actual. Es cierto en 1926-2005. En 2008-2026, el exceso de los otros días fue 0.0381 pp diario (t 1.78) y el TOM explica solo el 24% del rendimiento medio mensual.
- **"El efecto desapareció por la publicación de McConnell-Xu."** El debilitamiento empieza en los 2000 (t 0.85), antes de 2008. Con estos datos no se distingue entre arbitraje, cambio de microestructura o azar.
- **"Operar el TOM en GBM da ventaja"** o "es candidata para el satélite". Nunca pagó con 0.34% por lado y su DSR es ≈0.
- **"Con costos menores se arregla."** Fuera de muestra, el equilibrio fue 0.12% por lado, abajo del 0.25% de Trading USA (que además suma conversión cambiaria). Y aun bruta no supera a comprar y mantener.
- **"Comprar antes del cierre de mes mejora las entradas de forma demostrable."** E fuera de muestra no es significativo (t 1.58; el IC95 incluye el cero). [I] La parte atribuible al calendario sería ≈0.06 pp por evento.
- **"La ventana correcta es otra"** ([−3, +3] o [−5, −2]). Elegir la ventana mirando el tramo fuera de muestra es sobreajuste; la mejor tiene DSR de 0.0050.
- **"Funciona en México (IPC o NAFTRAC)."** No se probó aquí.
- **"Tiene ventaja con dinero real."** No: DSR < 0.95 en todas las lecturas, sin papel y sin capa fiscal.

### 16. Estado y reproducción

- **Estado: Replicado**, por la regla pre-registrada: se cumplen (i), (ii), (iii) y (iv). Alcance del estado:
  - La réplica de McConnell-Xu en 1926-2005 es casi exacta.
  - Fuera de muestra, el efecto tiene **el mismo signo, pero no es significativo y su magnitud es ≈11% de la de dentro de muestra**. Las condiciones (iii) y (iv) solo exigían signo (ver la lección en "Desviaciones").
  - Como estrategia con costos de GBM, no agrega valor en ningún tramo.
  - "Replicado" no significa "usable con dinero" (README, sección 1).
- **Comando que reproduce todo:** `python3 laboratorio/replicas/R09.py`, desde la raíz del repo. Tarda unos 60 s con caché y agrega 174 filas nuevas al CSV en cada ejecución.
- **Comprobación independiente:** `python3 laboratorio/replicas/R09_verificacion.py`, que no registra nada. Recalcula sin el motor, con su propio código:
  - El calendario: 1,201 de 1,201 meses con 4 días de TOM.
  - δ, δ_MX y E.
  - Las curvas netas de `US_tom_m1_p3` y de comprar y mantener. La diferencia máxima contra el CSV es de 3.09e-14.
- **Huella de datos (`huella_datos` del CSV):** US `a167a7fa2e659d4e`; SPX `f1c02485bcdc828c`; USMXN `4f2c746fc3ec044a`.
- **French** `F-F_Research_Data_Factors_daily_CSV.zip`: CRSP 202607, sha256 `1916d331c2c51d2aee3d00215897d2b8e5995cb387f1f4569ba46bff5fb049a8`.
- **Yahoo y FRED** (leídos el 2026-09-25):
  - `^GSPC` 1d: barras de 1927-12-30 a 2026-09-24, usadas hasta 2026-08-31; `fechas_sin_precio` = [2026-09-22].
  - DEXMXUS: de 1993-11-08 a 2026-09-18.
  - INTGSTMXM193N: de 1986-10 a 2026-07, sin meses rellenados.
- **Fecha de la corrida final:** 2026-09-25, 07:01 UTC.
- **Pendientes:**
  - Leer la versión publicada en el FAJ (tandfonline y SSRN respondieron 403) y el texto de L&S (Oxford, de pago).
  - Revisión independiente (`auditor-de-replicas`).
  - El efecto en el IPC o NAFTRAC (fuera del alcance de esta réplica).
  - Agregar la fila de R09 a `laboratorio/tabla-maestra.md` (no se tocó en esta sesión).

### 17. Conclusión operable

1. **Renglón TOM y regla [R] 5 de `arena/investigacion/03-teoria-de-torneos-y-estrategia-competitiva.md`: MODIFICAR.** Es el caso (a) del criterio pre-registrado: E > 0 fuera de muestra pero no significativo, y la estrategia sola no sobrevive. Texto propuesto (no se aplicó en ese documento; lo decide su responsable):
   - "El TOM se replicó casi exacto en 1926-2005 (R09: 0.149 pp diarios sobre los otros días, t 8.0). Desde 2008 la diferencia es 0.015 pp diarios (t 0.35), y desde los 2000 no es significativa.
   - **No operarlo solo.** Con GBM (0.34% por lado) no pagó ni en 1927-2008 (equilibrio de 0.28% por lado), y después de 2008 perdió 4.2% anual en USD.
   - **Timing: solo como desempate sin costo.** No retrasar una compra ni adelantar una venta por el calendario. Si una compra ya decidida puede hacerse antes o después del cambio de mes, hacerla antes cuesta lo mismo. La ganancia esperada que se puede atribuir al calendario es ≈0.06 pp por evento [I] y no es significativa.
   - Grado del efecto: **C** (baja de B). Como estrategia en GBM: **D** (propuesta; baja de C, porque el exceso neto es negativo en todos los tramos y el DSR es ≈0)."
   - Corregir también la cifra: "0.15% diario contra −0.001%" es de 1987-2005 (versión de trabajo de 2006). En 1926-2005 es 0.16% contra 0.01% bruto, o 0.15% contra 0.00% en exceso.
2. **El cambio de mes como estrategia, de núcleo o de satélite: DESCARTAR.** Fuera de muestra y neta de costos, no supera a comprar y mantener, a la SMA200 ni al efectivo. El DSR de la regla del artículo es 0.0000.
3. **Para la cuenta de 20,000 MXN, cuando el sistema opere:** ninguna operación por el calendario de fin de mes.
   - Si ya se va a comprar, no hay que esperar al cambio de mes ni retrasar la entrada: después de 2008 el premio estuvo en todo el mes.
   - Operar el TOM costaría 24 lados al año, ≈1,632 MXN (8.2% de la cuenta).
   - Es consistente con R04: "no arrancar en efectivo" se sostiene con la prima de mercado, no con el calendario.
