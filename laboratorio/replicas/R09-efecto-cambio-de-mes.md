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
| Estado | (se llena al final) |

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

