# Réplica R04: efecto Halloween, "Sell in May and go away" (Bouman y Jacobsen, 2002)

> Fase 0: formación. Esta ficha no recomienda inversiones. Las secciones 1 a 9 son el pre-registro. Se escribieron el 2026-09-25, antes de calcular cualquier rendimiento estacional o de estrategia, y no se editan después. Cualquier cambio posterior va a "Desviaciones del pre-registro", con fecha.

| Campo | Valor |
|---|---|
| ID | `R04` (registro: `laboratorio/replicas/R04-variantes.csv`; script: `laboratorio/replicas/R04.py`) |
| Artículo | Bouman, S. y Jacobsen, B. (2002). "The Halloween Indicator, 'Sell in May and Go Away': Another Puzzle". *American Economic Review* 92(5), 1618–1635, diciembre de 2002. doi:10.1257/000282802762024683. Ficha verificada con WebSearch/WebFetch el 2026-09-25 en aeaweb.org, IDEAS/RePEc y EconPapers (volumen, número, mes, páginas y DOI coinciden) |
| Acceso al texto | **El PDF publicado no se pudo leer**: aeaweb.org respondió 403 (Cloudflare) y SSRN 403. Se leyeron: (a) la versión de trabajo de noviembre de 1997 (Bouman y Jacobsen, "The Halloween Indicator: Sell in May and go away", 17 países, Datastream 1973–1996) con `pypdf`; (b) Maberly y Pierce (2004), *Econ Journal Watch* 1(1):29–46, que cita textualmente el artículo y reproduce su cifra de EUA; (c) Jacobsen y Zhang, SSRN 2154873 (versión de trabajo "an even bigger puzzle"), que resume el artículo y lo extiende |
| Fecha de publicación | Número de diciembre de 2002 del AER. Versión de trabajo circulando desde noviembre de 1997 (SSRN 76248) |
| Pre-registro escrito el | 2026-09-25, antes de calcular rendimientos estacionales o de estrategia |
| Responsable | Claude (laboratorio del sistema). Revisión independiente pendiente (`auditor-de-replicas`) |
| Estado | Pendiente (se asigna en la sección 16) |

**Conocimiento previo declarado.** Este pre-registro no es ciego. Antes de escribirlo ya conocía:

1. La cifra de EUA de Maberly y Pierce (2004) en la ventana del artículo (abajo). También sé que ellos atribuyen el efecto de EUA a dos meses extremos (octubre de 1987 y agosto de 1998).
2. La tabla 3 de Jacobsen y Zhang (SSRN 2154873): EUA dentro de muestra β = 5.82 (t = 2.45) y fuera de muestra (sep-1998 a jul-2011) β = 4.90 (t = 1.57). México: 5.06 (t = 0.82) y 8.15 (t = 1.36).
3. Que la versión de trabajo de 1997 **no** encontró un efecto significativo en EUA.
4. Que el documento `arena/investigacion/03-teoria-de-torneos-y-estrategia-competitiva.md` ya usa el efecto como regla [R] 6 ("estacionalidad a favor").

Para elegir fuentes y fijar el calendario de cortes solo se revisó **la existencia y el rango de fechas** de las series, sin calcular ningún rendimiento:

- `^MXX` mensual: de 1991-11-30 a 2026-08-31 (418 barras; índice de precio, `adjclose` = `close`).
- `NAFTRAC.MX` mensual: de 2008-01-31 a 2026-08-31 (`adjclose` ≠ `close`).
- FRED `INTGSTMXM193N`: de 1986-10 a 2026-07.
- FRED `DEXMXUS`: de 1993-11-08 a 2026-09-18.
- El zip mensual de French ya estaba en caché (CRSP 202607, usado en R01 y R02).

---

## PRE-REGISTRO (secciones 1 a 9)

### 1. Hipótesis previa y mecanismo

**Resultado declarado en el artículo** (cifras textuales):

- **Hallazgo principal** (texto del artículo, p. 1618, citado por Maberly y Pierce 2004, p. 30): "Surprisingly, we find the Sell in May effect is present in 36 of the 37 countries in our sample. The effect tends to be particularly strong and highly significant in European countries, and also proves to be robust over time. [...] in the U.K. stock market, for instance, we have found evidence of a Sell in May effect as far back as 1694. We find no evidence that the effect can be explained by factors like risk, cross correlation between markets, or the January effect."
- **Estrategia** (p. 1619, misma fuente): "A simple strategy based on the saying would outperform a buy and hold portfolio in many countries . . . and would also be a lot less risky".
- **Muestra.** Rendimientos mensuales de enero de 1970 a agosto de 1998, índices de 37 países desarrollados y emergentes (MSCI), en moneda local y con dividendos. México forma parte de los 37.
- **Modelo** (versión de 1997, ec. 1.1, y Maberly-Pierce, ec. 1). La regresión es r_t = μ + α₁·S_t + ε_t, con r_t el rendimiento mensual continuamente compuesto y S_t = 1 de noviembre a abril (0 de mayo a octubre). El efecto es α₁ > 0. La prueba se repite con una dummy de enero (modelo II).
- **Cifra de EUA (objetivo de magnitud).** El texto del AER no se pudo leer. Maberly y Pierce (2004, tabla 1, panel A) reestiman con el índice ponderado por valor de CRSP con dividendos, en logaritmos, de 1970-01 a 1998-08 (344 meses), y dicen que sus resultados son "virtually identical to those reported by Bouman and Jacobsen":
  - μ = 0.4235% (t = 1.21, p = 0.226).
  - **α₁ = 1.0349% mensual (t = 2.10, p = 0.037).**
  - Panel B, con dummy para oct-1987 y ago-1998: α₁ = 0.7784% (t = 1.69, p = 0.092).
  - Panel C, además con dummy de enero: α₁ = 0.6205% (t = 1.28, p = 0.200).
- **Contraste: versión de trabajo de 1997** (Datastream, 1973–1996, tabla 2). EUA α₁ = 0.696% con error estándar HC de 0.518: **no significativo**. En la tabla 4, la estrategia Halloween de EUA rinde 11.61% anual con desviación de 11.38%, contra 11.37% y 16.40% de comprar y mantener.
- **Costos.** La versión de 1997 afirma que la estrategia supera al índice "even net of transactions costs". No hay cifra de costos de GBM.

**Mecanismo económico.** Los autores no encuentran una explicación de riesgo. La que consideran más compatible son las vacaciones de verano: menor participación y aversión al riesgo estacional. Jacobsen y Zhang dicen que es "consistent with all empirical evidence to date". La evidencia contraria es Maberly y Pierce (2004): el efecto de EUA depende de dos meses extremos y no se puede explotar con futuros del S&P 500 entre 1982 y 2003.

¿Por qué no se arbitraría? Por tres razones:

1. El premio es una **diferencia de medias**, no un rendimiento negativo seguro. Salir en verano sacrifica la prima de verano, que suele ser pequeña pero positiva.
2. El ruido es enorme frente a la señal: una observación por año.
3. Hay riesgo de carrera profesional por quedar fuera en veranos alcistas.

Todo esto es inferencia, no hecho.

**Hipótesis (signo y magnitud esperados):**

- **H1, ventana del artículo en EUA.** Con el mercado de French (CRSP VW con dividendos) en logaritmos, de 1970-01 a 1998-08, α₁ > 0, con magnitud dentro de ±0.20 pp de 1.0349% y t MCO ≥ 1.96. Se espera casi idéntica. La diferencia de versión de CRSP y la construcción de French frente al índice VW de CRSP debería ser pequeña.
- **H2, historia larga de EUA dentro de muestra (1926-07 a 2002-12).** α₁ > 0 con t de Newey-West (12 rezagos) ≥ 2. Magnitud esperada entre 0.3 y 1.0 pp mensual.
- **H3, EUA fuera de muestra (2003-01 a 2026-07, post-publicación).** α₁ > 0. Se espera más débil que en H1, por el decaimiento post-publicación (McLean-Pontiff). Con unos 283 meses, **no** se espera t ≥ 2.
- **H4, IPC de México (`^MXX`, MXN, sin dividendos).** α₁ > 0 dentro de muestra (1991-12 a 2002-12) y fuera de muestra (2003-01 a 2026-07). Con muestras cortas y un índice volátil se espera t < 2 en ambos tramos.
- **H5, estrategia operable.** Mercado de noviembre a abril y efectivo de mayo a octubre, neta de costos GBM. Fuera de muestra se espera un **Sharpe mayor que comprar y mantener** (volatilidad menor) y un **CAGR menor** que comprar y mantener, porque la prima de verano de EUA probablemente es positiva. Se espera también un drawdown máximo menos severo.

### 2. Criterio de refutación

- **Métrica principal del efecto.** α₁ en % mensual, rendimientos logarítmicos, con t de Newey-West (Bartlett, 12 rezagos, corrección n/(n−k)).
- **Métricas secundarias del efecto:**
  - t MCO y t HC1 (White).
  - La diferencia anual pareada D_y (invierno menos verano, sumas de 6 meses): media, t, intervalo bootstrap de 95% y prueba de signo exacta.
  - Robustez a valores extremos: winsorizar al 1% y 99% dentro de cada ventana y usar las dummies de Maberly-Pierce en la ventana del artículo.
  - Control de enero (modelo II).
  - Exceso sobre el efectivo en cada mitad del año (la prueba de Jacobsen-Zhang).
  - Placebo de calendario: el α de las 12 rotaciones de una ventana de 6 meses consecutivos.
- **Métrica principal de la estrategia.** Sharpe anualizado del exceso mensual sobre el efectivo, neto de costos por defecto, fuera de muestra. Secundarias: MDD, CAGR y t de NW (12 rezagos) del exceso neto.
- **Condiciones:**
  - (i) EUA, 1970-01 a 1998-08: α₁ > 0, |α₁ − 1.0349| ≤ 0.20 pp y t MCO ≥ 1.96.
  - (ii) EUA, 1926-07 a 2002-12: α₁ > 0 y t NW ≥ 2.
  - (iii) EUA, 2003-01 a 2026-07: α₁ > 0.
  - (iv) México (`^MXX`), 2003-01 a 2026-07: α₁ > 0.
- **Estado final** (regla fijada ahora):
  - **Replicado** si se cumplen (i), (ii), (iii) y (iv).
  - **Replicado con diferencias** si α₁ > 0 en la ventana del artículo de EUA y se cumple al menos una de (iii) o (iv), pero no las cuatro condiciones. Esto incluye el caso de que la magnitud o la t de (i) queden fuera de tolerancia.
  - **No replicado** si α₁ ≤ 0 en EUA de 1970-01 a 1998-08, **o** si α₁ ≤ 0 fuera de muestra **tanto** en EUA como en México.
- **"Significativo fuera de muestra"** exige dos cosas: t NW ≥ 2 **y** que el intervalo bootstrap de 95% de D_y excluya el cero. Si no se cumplen ambas, el resultado fuera de muestra se describe como "mismo signo, no significativo".
- **Refutación de H5 (conclusión operable):**
  - Si la estrategia de noviembre a abril no supera a comprar y mantener en Sharpe **y** en MDD fuera de muestra, la conclusión es "no agrega valor frente a comprar y mantener".
  - Si no supera a la SMA10, la conclusión es "no agrega valor frente a la regla sencilla".
- **DSR.** Se usa N = número de variantes con `es_prueba=1` (10 por diseño). Se reportan dos lecturas: V de las 10 variantes y V por familia (EUA o México). **Para decidir se usa el DSR menor.** Si DSR < 0.95, la regla no es candidata para dinero, cualquiera que sea el estado de la réplica.
- **Regla del sistema afectada.** Es la regla [R] 6 de `arena/investigacion/03-teoria-de-torneos-y-estrategia-competitiva.md` ("Estacionalidad a favor, no en contra"), que asigna grado B al efecto y lo usa como sesgo de μ para la temporada de oct-2026 a abr-2027. La decisión se fija ahora:
  - **Confirmar** si, fuera de muestra, α₁ es significativo (definición de arriba) en EUA o en México **y** el exceso de noviembre a abril sobre el efectivo es > 0 con t NW ≥ 2.
  - **Modificar** si el exceso de invierno es > 0 pero α₁ no es significativo fuera de muestra. En ese caso, "no arrancar en efectivo" se justifica con la prima de mercado y no con el calendario, y el grado del efecto baja.
  - **Descartar** el uso del efecto si α₁ ≤ 0 fuera de muestra en ambos mercados.

### 3. Datos y licencia

| Serie | Fuente y archivo | Versión / huella | Frecuencia | Condiciones de uso |
|---|---|---|---|---|
| Mercado de EUA (Mkt-RF + RF) y RF | French `F-F_Research_Data_Factors_CSV.zip` | `version_crsp` y `sha256` que imprime el script | mensual | Pendiente de verificar |
| IPC de México | Yahoo chart v8 `^MXX` (`yahoo_historia`, `1mo`). Índice de **precio**: no incluye dividendos | URL, primer y último dato, `fechas_sin_precio` | mensual | Pendiente de verificar |
| NAFTRAC (ETF del IPC, solo sensibilidad) | Yahoo `NAFTRAC.MX` (`adjclose`: incluye dividendos) | URL, rango | mensual | Pendiente de verificar |
| CETES (efectivo en MXN) | FRED `INTGSTMXM193N` ("Interest Rates, Government Securities, Treasury Bills for Mexico", FMI IFS, % anual, promedio mensual) | Fecha de descarga y rango | mensual | Pendiente de verificar (datos del FMI redistribuidos por FRED) |
| MXN por USD (solo sensibilidad) | FRED `DEXMXUS` (Fed H.10, mediodía en Nueva York) | Fecha de descarga | diaria | Dominio público según FRED; solo referencia, no es una cotización ejecutable en GBM |

Los datos crudos no se redistribuyen: el caché está en `.gitignore`.

### 4. Universo

- **EUA.** Un solo activo: el mercado total de French (CRSP, NYSE/AMEX/NASDAQ ponderado por valor, con dividendos). No tiene sesgo de supervivencia, pero **no es invertible directamente**; el proxy invertible sería un ETF del mercado total o del S&P 500. Difiere del índice VW de CRSP que usan Maberly-Pierce en los filtros de French (acciones comunes, códigos 10 y 11) y del MSCI USA que usa el artículo.
- **México.** El IPC (`^MXX`), en MXN y **sin dividendos**. El artículo usa MSCI México con dividendos.
  - El sesgo que introduce la falta de dividendos se declara ahora. Comprar y mantener pierde 12 meses de dividendos al año y la estrategia Halloween solo 6. Por eso la comparación estrategia contra comprar y mantener **favorece** a Halloween en aproximadamente la mitad del rendimiento por dividendo anual.
  - Si los dividendos del IPC son estacionales, α₁ también se sesga. No se sabe en qué sentido; no se verificó.
  - Como sensibilidad se usa `NAFTRAC.MX` con rendimiento total, desde 2008.
- **No se agregan otros países.** El artículo tiene 37. Esta réplica se limita a los dos mercados del mandato (EUA y México).

### 5. Fecha de disponibilidad

- **La señal es de calendario.** La exposición del mes t depende solo del número del mes t, que se conoce con certeza al cierre de t−1. En el motor, la señal usa `h.fecha_decision` (fin de t−1) y calcula el mes siguiente. No lee ningún rendimiento. Pasa `buscar_capturas`: solo captura un `frozenset` de meses con ≤ 12 elementos.
- **RF de French.** Es la T-bill del mes t, conocida al inicio del mes.
- **CETES.** `INTGSTMXM193N` es el **promedio** del mes t de la tasa anual. Se usa como rendimiento del efectivo durante t: r = tasa/100 × días del mes/360. Es una aproximación. No es el rendimiento realizado de rolar CETES a 28 días y usa un promedio que no se conoce completo al inicio de t. Solo afecta el rendimiento del efectivo, nunca la señal. La SMA10 no usa efectivo.
- **Ejecución.** Se supone al cierre del último día hábil del mes, igual que en el artículo (comprar al cierre de octubre y vender al cierre de abril).

### 6. Periodo

- **Periodo del artículo:** 1970-01 a 1998-08.
- **Periodo propio total:**
  - EUA: 1926-07 a 2026-07 (French CRSP 202607).
  - México: 1991-12 (primer rendimiento mensual completo de `^MXX`) al último mes común con CETES; se espera 2026-07.
  - Pruebas estadísticas: todos los meses de cada ventana.
  - Backtests: `min_historia` = 10 en todas las corridas de una familia, para que la SMA10 y las reglas de calendario arranquen igual. Primer mes evaluado: 1927-05 en EUA y 1992-10 en México.
- **Corte único: 2002-12-31** (el artículo se publicó en el número de diciembre de 2002).
  - `dentro_muestra`: hasta 2002-12.
  - `fuera_muestra`: 2003-01 al final. Es post-publicación y se mira una sola vez.
- **Ventanas de reporte**, fijadas ahora y calculadas sobre las mismas corridas, sin nuevas variantes:
  - EUA: 1926-07 a 1969-12 (pre-artículo); 1970-01 a 1998-08 (artículo); 1998-09 a 2002-12 (hueco entre el fin de la muestra y la publicación); 2003-01 a 2026-07 (fuera de muestra). Además, α₁ por décadas (solo diagnóstico).
  - México: 1991-12 a 1998-08 (traslape con el artículo); 1998-09 a 2002-12; 2003-01 a 2026-07.
- **Ventanas de contraste** (solo para comparar α₁ con cifras publicadas; no son criterio):
  - EUA 1973-01 a 1996-12, la de la versión de trabajo de 1997 (α₁ = 0.696%, Datastream).
  - EUA y México 1998-09 a 2011-07, el "fuera de muestra" de Jacobsen-Zhang (tabla 3: β semestral de 4.90 en EUA y 8.15 en México). Se compara contra 6·α₁ y contra la media de D_y.

### 7. Limpieza

Reglas fijadas antes de ver resultados:

- **French.** Los valores −99.99 y −999 son faltantes y se omiten; no se espera ninguno. El cambio de la fuente de RF en 202406 (de Ibbotson a ICE BofA) no se ajusta. Se registran la versión CRSP y el sha256.
- **Yahoo mensual.** Se usan barras `1mo` re-etiquetadas a fin de mes y se descarta el mes en curso. Los meses en `fechas_sin_precio` se reportan; su rendimiento siguiente abarca dos meses y se acepta así. No se espera ninguno.
- **La primera barra de `^MXX`** (1991-11-30) solo sirve de precio base: el primer rendimiento es el de 1991-12.
- **CETES.** Si falta un mes dentro del rango de `^MXX`, se arrastra la tasa del mes anterior y se reporta cuántos meses. Las fechas de FRED (día 1) se llevan a fin de mes.
- **Sin cambios después de ver resultados.** No se eliminan valores extremos. La winsorización y las dummies de Maberly-Pierce son pruebas **adicionales** pre-registradas, no limpieza.

### 8. Regla y variantes planeadas

**Pruebas estadísticas del efecto** (no son estrategias y no van al CSV). Se reportan **todas**:

1. Regresión mensual y_t = μ + α₁·S_t + ε_t, con y_t = 100·ln(1 + R_t):
   - En EUA, R_t es Mkt-RF + RF.
   - En México, R_t es el rendimiento de precio de `^MXX`.
   - Se calculan la t MCO, la t HC1 y la t NW(12).
2. Modelo II: con dummy de enero, t NW(12).
3. Solo en la ventana del artículo de EUA: modelo con dummy D_t = 1 en 1987-10 y 1998-08 (Maberly-Pierce, panel B), y modelo con D_t más enero (panel C).
4. Winsorización al 1% y 99% dentro de la ventana, t NW(12).
5. Diferencia anual pareada. Para cada año Halloween *y* completo en la ventana:
   - D_y = Σ y(nov_{y−1} … abr_y) − Σ y(may_y … oct_y).
   - Se reportan la media, la t iid, el IC bootstrap de 95% (remuestreo iid de años, 10,000 repeticiones, semilla 4) y la prueba de signo (número de D_y > 0 y p binomial exacta de una cola).
6. Exceso sobre el efectivo por mitad del año: media mensual de y_t − 100·ln(1 + rf_t) en noviembre–abril y en mayo–octubre, cada una con t NW(12). En EUA el efectivo es la RF de French y en México CETES. También el porcentaje de semestres de invierno con exceso positivo.
7. Placebo de calendario: α de las 12 ventanas de 6 meses consecutivos (inicio en cada mes) y el lugar que ocupa noviembre–abril.
8. Solo en EUA, α₁ por década (diagnóstico).
9. NAFTRAC (rendimiento total, 2008-02 al final): la regresión 1 como contraste de México con dividendos.

**Estrategias (motor `backtest_senal`, mensual).** Exposición 1 si el mes de t está en la ventana y 0 si no.

| # | Variante (`es_prueba=1`) | Meses en el mercado | Activo / efectivo / moneda |
|---|---|---|---|
| 1 | `US_nov_abr` (**regla del artículo**) | 11, 12, 1, 2, 3, 4 | French Mkt / RF / USD |
| 2 | `US_oct_abr` | 10 a 4 | igual |
| 3 | `US_nov_may` | 11 a 5 | igual |
| 4 | `US_dic_abr` | 12 a 4 | igual |
| 5 | `US_nov_mar` | 11 a 3 | igual |
| 6 | `MX_nov_abr` (**regla del artículo**) | 11 a 4 | `^MXX` / CETES / MXN |
| 7-10 | `MX_oct_abr`, `MX_nov_may`, `MX_dic_abr`, `MX_nov_mar` | como 2 a 5 | igual |

**Referencias.** Se registran con `es_prueba=0` y nota "referencia":

- `US_ref_comprar_mantener` y `MX_ref_comprar_mantener`: w = 1.
- `US_ref_efectivo` y `MX_ref_efectivo`: w = 0.
- `US_ref_sma10` y `MX_ref_sma10`: `senal_media_movil(10)`, la regla sencilla de timing.
- `US_ref_verano` y `MX_ref_verano`: mercado de mayo a octubre, el complemento, para ver la otra mitad.

**Sensibilidades.** Se registran con `es_prueba=0` y nota. Es una lista cerrada:

1. Las 10 variantes y las 8 referencias con spread "medio" (0.15% por lado).
2. Las 10 variantes y las 8 referencias brutas (comisión y spread en 0).
3. EUA en MXN para un inversionista mexicano: activo French Mkt convertido con `DEXMXUS` y efectivo CETES (`efectivo_en_mxn=True`), costos por defecto. Variantes `USMXN_nov_abr`, `USMXN_ref_comprar_mantener`, `USMXN_ref_efectivo` y `USMXN_ref_sma10`, con el mismo corte.
4. NAFTRAC con rendimiento total y efectivo CETES, costos por defecto, sin corte: todo es posterior a 2002. Variantes `NAFTRAC_nov_abr`, `NAFTRAC_ref_comprar_mantener`, `NAFTRAC_ref_efectivo` y `NAFTRAC_ref_sma10`.

**Diagnósticos** (solo se reportan):

- Métricas de la estrategia por ventana de reporte.
- La t NW(12) del exceso neto mensual.
- Las operaciones por año.
- La distribución del exceso de los semestres de invierno (media, mediana, % positivos y peor semestre), útil para la regla [R] 6.

**Exposición, efectivo y moneda.** Exposición en {0, 1}, sin cortos ni apalancamiento. EUA en USD con T-bills y México en MXN con CETES.

### 9. Costos y comparación simple

- **Costos:**
  - Por defecto: comisión de 0.29% por lado (GBM, 0.25% + IVA: hecho) más spread de 0.05% por lado (supuesto [I]), sobre |Δw|. La regla del artículo cambia dos veces al año: unos 0.68% anuales por defecto.
  - Escenario "medio": spread de 0.15%. Bruto: cero.
  - No se modelan el spread cambiario de GBM (en SIC), los impuestos ni la liquidación final. Los impuestos (ISR de 10% sobre ganancias en BMV y SIC) **perjudican** a Halloween frente a comprar y mantener, porque realiza ganancias cada año. No se cuantifica aquí.
- **Reglas sencillas con idénticas condiciones.** Comprar y mantener, 100% efectivo y SMA10 (mismas fechas, costos, moneda y efectivo).
