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
| Estado | **Replicado** según la regla pre-registrada (sección 16). Fuera de muestra: mismo signo, **no significativo**. No es candidata para dinero (sección 17) |

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

---

## RESULTADOS (se llenan después de correr)

> Corrida del 2026-09-25 (UTC 05:49). Las cifras y tablas vienen de `python3 laboratorio/replicas/R04.py`, cuya salida completa está en `R04-salida.txt` y las cifras clave en `R04-resultados.json`. Las tablas se insertaron sin redondear a mano. En las pruebas del efecto, y = 100·ln(1+R): α₁ está en **puntos porcentuales log por mes** y D_Y en puntos log de 6 meses. En las estrategias, el Sharpe es el del exceso mensual sobre el efectivo, anualizado, y `nw_t` es la t de Newey-West (12 rezagos) del exceso neto mensual. MDD = drawdown máximo.

### Desviaciones del pre-registro

| Fecha | Qué cambió | Por qué | ¿Invalida el tramo de prueba? |
|---|---|---|---|
| 2026-09-25 | **Antes de cualquier corrida** se agregaron a la sección 6 dos "ventanas de contraste": EUA 1973-01 a 1996-12 (versión de 1997) y EUA y México 1998-09 a 2011-07 (Jacobsen-Zhang). Solo sirven para comparar α₁ con cifras publicadas y no son criterio | Faltaban para la sección 13 | No: se escribieron sin ningún rendimiento calculado |
| 2026-09-25 | **La primera ejecución falló antes de registrar nada**: el CSV no existía. `^MXX` llega a 2026-08 y CETES a 2026-07, y la prueba de exceso exigió tasas en toda la ventana. Solo se habían impreso los rangos de datos, ningún resultado. Se aplicó lo que ya decía la sección 6 ("hasta el último mes común con CETES"): las series de México y NAFTRAC de las pruebas del efecto se recortan a los meses con CETES. Se volvió a ejecutar todo | Error de código | **No.** Ninguna cifra del efecto ni de las estrategias se había visto. El CSV tiene una sola ejecución: 178 filas, 62 corridas y una sola marca de tiempo |
| 2026-09-25 | Se agregó un **chequeo de datos** de NAFTRAC contra `^MXX`: correlación de rendimientos mensuales, diferencia de medias y meses con rendimiento 0. Motivo: Yahoo reporta para NAFTRAC.MX una fecha de referencia de 2019-06-28, aunque sus barras llegan a 2026-08-31 | Validación de datos (flujo, paso 2) | No. Resultado: correlación 0.9971 (n = 223), diferencia de medias NAFTRAC − `^MXX` = 0.00130 por mes y 0 meses con rendimiento exactamente 0. Los datos se consideran utilizables |
| 2026-09-25 | **Aclaración de lectura, sin cambio.** En la ventana "traslape articulo" de México, D_Y usa solo años Halloween completos (1993–1997, N = 5) y la regresión usa todos los meses (1991-12 a 1998-08). Por eso la media de D es negativa (−5.777) y 6·α₁ es positivo (11.135) | Diferencia de composición de la muestra | No |

### 10. Variantes probadas

- **Archivo.** `laboratorio/replicas/R04-variantes.csv`: 178 filas de **una** ejecución (62 corridas).
  - 18 variantes en cada familia (EUA y México), con 3 escenarios de costo y 3 segmentos: 162 filas.
  - 4 corridas USMXN × 3 segmentos: 12 filas.
  - 4 corridas NAFTRAC, sin corte: 4 filas.
- **Variantes con `es_prueba=1`: 10** (5 de EUA y 5 de México), en 30 filas.
  - Las referencias y las sensibilidades van con `es_prueba=0` y una nota: "referencia", "sensibilidad: spread medio…", "sensibilidad: bruto…", "sensibilidad: MXN…" y "sensibilidad: NAFTRAC…".
- **Pruebas fuera del registro:**
  - Las comprobaciones con datos **sintéticos**, sin registrar (`id_replica=None`). La diferencia máxima entre la regresión y `estadistica.newey_west`, y entre la exposición y los costos de la señal de calendario y sus valores esperados, fue 8.327e-16.
  - La ejecución fallida calculó en memoria las regresiones de EUA, sin imprimirlas, y ninguna estrategia.
  - Se usa `n_pruebas` = 10.

**Salida de `sharpe_deflactado_de_registro`** (umbral 0.95; SR anualizado; el DSR mide el Sharpe del exceso **sobre el efectivo** después de la selección, **no** si la regla le gana a comprar y mantener):

| Lectura | Segmento | Variante | DSR | ¿Cumple? | N | V por periodo | SR anual | SR0 anual | n_obs | PSR sin deflactar |
|---|---|---|---|---|---|---|---|---|---|---|
| Por defecto: mejor de las 10, V de todas | dentro_muestra | US_nov_abr | 0.9082 | No | 10 | 0.002014 | 0.3962 | 0.2448 | 908 | 0.9997 |
| Mejor de EUA, V de EUA (5 Sharpes) | dentro_muestra | US_nov_abr | 0.9990 | Sí | 10 | 0.000066 | 0.3962 | 0.0442 | 908 | 0.9997 |
| Regla del artículo EUA, V de todas | dentro_muestra | US_nov_abr | 0.9082 | No | 10 | 0.002014 | 0.3962 | 0.2448 | 908 | 0.9997 |
| Mejor de México, V de México | dentro_muestra | MX_oct_abr | 0.5480 | No | 10 | 0.000684 | 0.1810 | 0.1426 | 123 | 0.7153 |
| Regla del artículo México, V de México | dentro_muestra | MX_nov_abr | 0.4700 | No | 10 | 0.000684 | 0.1187 | 0.1426 | 123 | 0.6457 |
| Regla del artículo México, V de todas | dentro_muestra | MX_nov_abr | 0.3457 | No | 10 | 0.002014 | 0.1187 | 0.2448 | 123 | 0.6457 |
| Mejor de EUA, V de EUA (selección *ex post*) | fuera_muestra | US_nov_may | 0.9735 | Sí | 10 | 0.001087 | 0.5894 | 0.1799 | 283 | 0.9973 |
| Regla del artículo EUA, V de EUA | fuera_muestra | US_nov_abr | 0.9462 | No | 10 | 0.001087 | 0.5161 | 0.1799 | 283 | 0.9932 |
| Regla del artículo EUA, V de todas | fuera_muestra | US_nov_abr | 0.9405 | No | 10 | 0.001217 | 0.5161 | 0.1903 | 283 | 0.9932 |
| Mejor de México, V de México | fuera_muestra | MX_nov_abr | 0.9158 | No | 10 | 0.000074 | 0.3356 | 0.0470 | 283 | 0.9454 |
| Regla del artículo México, V de todas | fuera_muestra | MX_nov_abr | 0.7560 | No | 10 | 0.001217 | 0.3356 | 0.1903 | 283 | 0.9454 |

**Lectura pre-registrada: se aplica el DSR menor.** La regla del artículo **no** alcanza DSR ≥ 0.95 en ninguna lectura conservadora:

- EUA: 0.9082 dentro de muestra y 0.9405 fuera de muestra.
- México: 0.3457 y 0.7560.

`US_nov_abr` pasa solo con V de su familia dentro de muestra (0.9990). `US_nov_may` pasa fuera de muestra con V de su familia (0.9735), pero esa selección se hizo mirando el tramo de prueba y no cuenta.

### 11. Resultados

#### 11.1 Periodo del artículo contra la cifra publicada (EUA, 1970-01 a 1998-08, 344 meses)

| modelo | coef | articulo/MP | replica | diferencia | t MP | t MCO replica | t NW12 replica |
|---|---|---|---|---|---|---|---|
| A | mu | 0.4235 | 0.4454 | 0.0219 | 1.21 | 1.27 | 1.39 |
| A | a1 | 1.0349 | 1.0377 | 0.0028 | 2.1 | 2.09 | 2.32 |
| B (dummy oct-87 y ago-98) | mu | 0.68 | 0.7011 | 0.0211 | 2.08 | 2.13 | 2.49 |
| B | a1 | 0.7784 | 0.7819 | 0.0035 | 1.69 | 1.68 | 1.90 |
| B | a2 (dummy) | -22.056 | -21.9958 | 0.0602 | -7.27 | -7.20 | -7.06 |
| C (+ enero) | a1 | 0.6205 | 0.6248 | 0.0043 | 1.28 | 1.28 | 1.48 |
| C | a3 (enero) | 0.9363 | 0.9320 | -0.0043 | 1.08 | 1.07 | 0.91 |

- α₁ de la réplica = **1.0377** contra 1.0349 de Maberly-Pierce (que reproducen a Bouman-Jacobsen). La diferencia es de **0.0028 pp**, dentro de la tolerancia de ±0.20 pp. La t MCO es 2.09 contra 2.10.
- También se reproducen los paneles B y C de Maberly-Pierce (diferencias ≤ 0.0043 pp en α₁).
- **Con dummies para octubre de 1987 y agosto de 1998, α₁ baja a 0.7819 y deja de ser significativo al 5%:** t MCO 1.68 y t NW12 1.90. La crítica de Maberly-Pierce se confirma con estos datos.
- Contraste con la versión de 1997 (1973-01 a 1996-12, Datastream): el artículo reporta α₁ = 0.696 (no significativo) y la réplica con French da 0.8166, con t HC1 de 1.52 y t NW12 de 1.79. Mismo signo, tampoco significativo al 5%.

#### 11.2 Efecto en EUA (French Mkt, USD, con dividendos)

Regresión principal por ventana:

| ventana | desde | hasta | n | mu (verano) | a1 | t MCO | t HC1 | t NW12 | p NW | media inv. | media ver. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| completo | 1926-07-31 | 2026-07-31 | 1201 | 0.5266 | 0.5895 | 1.93 | 1.93 | 2.18 | 0.0293 | 1.1161 | 0.5266 |
| dentro_muestra 1926-07 a 2002-12 | 1926-07-31 | 2002-12-31 | 918 | 0.4467 | 0.6819 | 1.86 | 1.86 | 2.07 | 0.0387 | 1.1286 | 0.4467 |
| fuera_muestra 2003-01 al final | 2003-01-31 | 2026-07-31 | 283 | 0.7872 | 0.2886 | 0.56 | 0.56 | 0.70 | 0.4866 | 1.0758 | 0.7872 |
| pre-articulo 1926-07 a 1969-12 | 1926-07-31 | 1969-12-31 | 522 | 0.5679 | 0.3603 | 0.68 | 0.68 | 0.75 | 0.4536 | 0.9282 | 0.5679 |
| ARTICULO 1970-01 a 1998-08 | 1970-01-31 | 1998-08-31 | 344 | 0.4454 | 1.0377 | 2.09 | 2.09 | 2.32 | 0.0204 | 1.4831 | 0.4454 |
| hueco 1998-09 a 2002-12 | 1998-09-30 | 2002-12-31 | 52 | -0.7659 | 1.5532 | 1.00 | 1.00 | 1.37 | 0.1707 | 0.7872 | -0.7659 |
| contraste WP1997 1973-01 a 1996-12 | 1973-01-31 | 1996-12-31 | 288 | 0.5572 | 0.8166 | 1.52 | 1.52 | 1.79 | 0.0735 | 1.3738 | 0.5572 |
| contraste JZ-OOS 1998-09 a 2011-07 | 1998-09-30 | 2011-07-31 | 155 | -0.0548 | 0.9300 | 1.20 | 1.20 | 1.63 | 0.1033 | 0.8753 | -0.0548 |

Pruebas robustas: α₁ con dummy de enero; α₁ winsorizado al 1% y 99%; dummies de Maberly-Pierce solo en ventanas que contienen 1987-10 y 1998-08.

| ventana | a1 con enero | t NW | a1 enero (coef) | t NW enero | a1 winsor 1/99 | t NW winsor | a1 MP-B | t MCO MP-B | a1 MP-C | t MCO MP-C |
|---|---|---|---|---|---|---|---|---|---|---|
| completo | 0.5397 | 1.95 | 0.2986 | 0.60 | 0.5734 | 2.32 | 0.5166 | 1.72 | 0.4669 | 1.48 |
| dentro_muestra 1926-07 a 2002-12 | 0.5638 | 1.69 | 0.7115 | 1.26 | 0.6806 | 2.26 | 0.5869 | 1.63 | 0.4689 | 1.24 |
| fuera_muestra 2003-01 al final | 0.4598 | 1.01 | -1.0132 | -1.01 | 0.2336 | 0.58 | NA | NA | NA | NA |
| pre-articulo 1926-07 a 1969-12 | 0.2509 | 0.52 | 0.6615 | 0.97 | 0.3803 | 0.88 | NA | NA | NA | NA |
| ARTICULO 1970-01 a 1998-08 | 0.8805 | 1.96 | 0.9320 | 0.91 | 0.9460 | 2.23 | 0.7819 | 1.68 | 0.6248 | 1.28 |
| hueco 1998-09 a 2002-12 | 1.6171 | 1.19 | -0.4153 | -0.17 | 1.5490 | 1.37 | NA | NA | NA | NA |
| contraste WP1997 1973-01 a 1996-12 | 0.5945 | 1.32 | 1.3328 | 1.15 | 0.7455 | 1.71 | NA | NA | NA | NA |
| contraste JZ-OOS 1998-09 a 2011-07 | 1.2935 | 2.02 | -2.1808 | -1.79 | 0.8185 | 1.46 | NA | NA | NA | NA |

Diferencia anual pareada (D_Y = invierno − verano):

| ventana | anios | media D | mediana D | t iid | IC95 bootstrap | D>0 | p signo (1 cola) | 6*a1 | peor anio | mejor anio |
|---|---|---|---|---|---|---|---|---|---|---|
| completo | 1927-2025 (N=99) | 3.590 | 5.216 | 2.00 | [0.050, 7.067] | 67/99 | 0.0003 | 3.537 | 1932: -70.98 | 1930: 38.50 |
| dentro_muestra 1926-07 a 2002-12 | 1927-2002 (N=76) | 4.143 | 6.101 | 1.89 | [-0.272, 8.283] | 51/76 | 0.0019 | 4.091 | 1932: -70.98 | 1930: 38.50 |
| fuera_muestra 2003-01 al final | 2004-2025 (N=22) | 2.394 | 4.090 | 0.87 | [-3.059, 7.500] | 16/22 | 0.0262 | 1.731 | 2009: -24.75 | 2011: 24.62 |
| pre-articulo 1926-07 a 1969-12 | 1927-1969 (N=43) | 2.358 | 5.917 | 0.69 | [-4.788, 8.732] | 27/43 | 0.0631 | 2.162 | 1932: -70.98 | 1930: 38.50 |
| ARTICULO 1970-01 a 1998-08 | 1971-1997 (N=27) | 5.850 | 3.827 | 2.26 | [0.832, 10.915] | 19/27 | 0.0261 | 6.226 | 1982: -19.65 | 1971: 33.55 |
| hueco 1998-09 a 2002-12 | 1999-2002 (N=4) | 13.445 | 14.339 | 2.67 | [5.276, 21.222] | 4/4 | 0.0625 | 9.319 | 2001: 0.94 | 2002: 24.16 |
| contraste WP1997 1973-01 a 1996-12 | 1974-1996 (N=23) | 5.645 | 3.827 | 2.18 | [0.494, 10.370] | 17/23 | 0.0173 | 4.900 | 1982: -19.65 | 1987: 30.81 |
| contraste JZ-OOS 1998-09 a 2011-07 | 1999-2010 (N=12) | 5.386 | 4.659 | 1.29 | [-2.879, 12.860] | 9/12 | 0.0730 | 5.580 | 2009: -24.75 | 2002: 24.16 |

Exceso sobre la RF por mitad del año (prueba de Jacobsen-Zhang):

| ventana | exceso nov-abr | t NW | exceso may-oct | t NW | semestres inv. (N) | media semestre | mediana | % semestres > 0 | peor semestre |
|---|---|---|---|---|---|---|---|---|---|
| completo | 0.8498 | 3.97 | 0.2538 | 1.17 | 100 | 5.099 | 5.967 | 0.740 | 1932: -52.08 |
| dentro_muestra 1926-07 a 2002-12 | 0.8218 | 3.16 | 0.1337 | 0.51 | 76 | 4.954 | 6.252 | 0.724 | 1932: -52.08 |
| fuera_muestra 2003-01 al final | 0.9401 | 2.78 | 0.6457 | 1.91 | 23 | 5.611 | 5.900 | 0.783 | 2022: -13.93 |
| pre-articulo 1926-07 a 1969-12 | 0.7782 | 2.06 | 0.4155 | 1.05 | 43 | 4.857 | 5.646 | 0.721 | 1932: -52.08 |
| ARTICULO 1970-01 a 1998-08 | 0.9427 | 2.71 | -0.1097 | -0.34 | 28 | 6.364 | 7.016 | 0.750 | 1974: -21.85 |
| hueco 1998-09 a 2002-12 | 0.4571 | 0.44 | -1.0949 | -1.04 | 4 | 3.007 | 5.317 | 0.750 | 2001: -17.33 |
| contraste WP1997 1973-01 a 1996-12 | 0.8063 | 2.13 | -0.0257 | -0.08 | 23 | 5.529 | 6.318 | 0.739 | 1974: -21.85 |
| contraste JZ-OOS 1998-09 a 2011-07 | 0.6641 | 1.27 | -0.2737 | -0.44 | 13 | 3.985 | 5.900 | 0.769 | 2001: -17.33 |

Placebo de calendario. El lugar de noviembre–abril entre las 12 ventanas de 6 meses consecutivos es 1 en la muestra completa, en la muestra dentro, en la ventana del artículo y en la de Jacobsen-Zhang (1998-09 a 2011-07). Es 2 antes de 1970 y en la ventana de 1997, 3 en el hueco 1998–2002 y **4 fuera de muestra**. Las 12 rotaciones son 6 cortes con signo opuesto (la ventana k+6 es el complemento de k). La lista completa está en `R04-salida.txt`.

#### 11.3 Efecto en México (`^MXX`, MXN, índice de precio sin dividendos; efectivo CETES)

| ventana | desde | hasta | n | mu (verano) | a1 | t MCO | t HC1 | t NW12 | p NW | media inv. | media ver. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| completo | 1991-12-31 | 2026-07-31 | 416 | 0.3237 | 1.2115 | 1.93 | 1.93 | 2.13 | 0.0331 | 1.5352 | 0.3237 |
| dentro_muestra 1991-12 a 2002-12 | 1991-12-31 | 2002-12-31 | 133 | -0.0326 | 2.2850 | 1.45 | 1.45 | 1.54 | 0.1244 | 2.2524 | -0.0326 |
| fuera_muestra 2003-01 al final | 2003-01-31 | 2026-07-31 | 283 | 0.4905 | 0.7063 | 1.27 | 1.27 | 1.60 | 0.1092 | 1.1968 | 0.4905 |
| traslape articulo 1991-12 a 1998-08 | 1991-12-31 | 1998-08-31 | 81 | 0.0122 | 1.8558 | 0.86 | 0.86 | 0.81 | 0.4166 | 1.8680 | 0.0122 |
| hueco 1998-09 a 2002-12 | 1998-09-30 | 2002-12-31 | 52 | -0.1016 | 2.9602 | 1.30 | 1.30 | 1.32 | 0.1871 | 2.8586 | -0.1016 |
| contraste JZ-OOS 1998-09 a 2011-07 | 1998-09-30 | 2011-07-31 | 155 | 0.9216 | 1.3578 | 1.30 | 1.30 | 1.36 | 0.1734 | 2.2794 | 0.9216 |

| ventana | a1 con enero | t NW | a1 enero (coef) | t NW enero | a1 winsor 1/99 | t NW winsor | a1 MP-B | t MCO MP-B | a1 MP-C | t MCO MP-C |
|---|---|---|---|---|---|---|---|---|---|---|
| completo | 1.3521 | 2.21 | -0.8398 | -0.64 | 1.1888 | 2.24 | NA | NA | NA | NA |
| dentro_muestra 1991-12 a 2002-12 | 2.4224 | 1.56 | -0.8368 | -0.26 | 2.2219 | 1.56 | NA | NA | NA | NA |
| fuera_muestra 2003-01 al final | 0.8465 | 1.70 | -0.8295 | -0.66 | 0.6999 | 1.70 | NA | NA | NA | NA |
| traslape articulo 1991-12 a 1998-08 | 2.1587 | 0.94 | -1.7739 | -0.49 | 1.7749 | 0.80 | NA | NA | NA | NA |
| hueco 1998-09 a 2002-12 | 2.8297 | 1.05 | 0.8479 | 0.14 | 2.9434 | 1.34 | NA | NA | NA | NA |
| contraste JZ-OOS 1998-09 a 2011-07 | 1.7484 | 1.53 | -2.3438 | -0.94 | 1.3096 | 1.35 | NA | NA | NA | NA |

| ventana | anios | media D | mediana D | t iid | IC95 bootstrap | D>0 | p signo (1 cola) | 6*a1 | peor anio | mejor anio |
|---|---|---|---|---|---|---|---|---|---|---|
| completo | 1993-2025 (N=33) | 6.129 | 4.345 | 1.84 | [-0.256, 12.404] | 22/33 | 0.0401 | 7.269 | 1995: -41.78 | 2002: 52.68 |
| dentro_muestra 1991-12 a 2002-12 | 1993-2002 (N=10) | 10.801 | 12.951 | 1.23 | [-6.280, 26.204] | 7/10 | 0.1719 | 13.710 | 1995: -41.78 | 2002: 52.68 |
| fuera_muestra 2003-01 al final | 2004-2025 (N=22) | 4.863 | 4.410 | 1.62 | [-0.975, 10.608] | 15/22 | 0.0669 | 4.238 | 2009: -19.99 | 2008: 35.46 |
| traslape articulo 1991-12 a 1998-08 | 1993-1997 (N=5) | -5.777 | -5.666 | -0.48 | [-27.333, 14.688] | 2/5 | 0.8125 | 11.135 | 1995: -41.78 | 1996: 31.46 |
| hueco 1998-09 a 2002-12 | 1999-2002 (N=4) | 26.305 | 25.649 | 2.50 | [7.871, 45.396] | 4/4 | 0.0625 | 17.761 | 2001: 1.24 | 2002: 52.68 |
| contraste JZ-OOS 1998-09 a 2011-07 | 1999-2010 (N=12) | 10.936 | 10.374 | 1.72 | [-1.151, 22.885] | 9/12 | 0.0730 | 8.147 | 2009: -19.99 | 2002: 52.68 |

| ventana | exceso nov-abr | t NW | exceso may-oct | t NW | semestres inv. (N) | media semestre | mediana | % semestres > 0 | peor semestre |
|---|---|---|---|---|---|---|---|---|---|
| completo | 0.5997 | 1.44 | -0.5561 | -1.31 | 34 | 3.027 | 3.487 | 0.618 | 1995: -46.84 |
| dentro_muestra 1991-12 a 2002-12 | 0.4753 | 0.44 | -1.6549 | -1.91 | 10 | 0.798 | 5.355 | 0.600 | 1995: -46.84 |
| fuera_muestra 2003-01 al final | 0.6584 | 1.90 | -0.0418 | -0.09 | 23 | 3.925 | 1.890 | 0.609 | 2020: -20.75 |
| traslape articulo 1991-12 a 1998-08 | -0.1859 | -0.13 | -1.8563 | -1.09 | 6 | -5.008 | 1.726 | 0.500 | 1995: -46.84 |
| hueco 1998-09 a 2002-12 | 1.5180 | 1.03 | -1.3450 | -0.95 | 4 | 9.508 | 13.179 | 0.750 | 2001: -14.95 |
| contraste JZ-OOS 1998-09 a 2011-07 | 1.4568 | 2.32 | 0.1393 | 0.16 | 13 | 8.741 | 10.949 | 0.846 | 2001: -14.95 |

Placebo: noviembre–abril queda en el lugar **1 fuera de muestra** y en el lugar 2 en las demás ventanas.

#### 11.4 Estrategia contra las reglas sencillas, costos por defecto

**EUA, dentro de muestra (1927-05 a 2002-12)**

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual |
|---|---|---|---|---|---|---|---|---|---|
| US_nov_abr | 0.0821 | 0.1253 | 0.3962 | 3.1779 | 0.6240 | -0.5760 | 0.4978 | 1.9955 | 0.0068 |
| US_oct_abr | 0.0794 | 0.1397 | 0.3515 | 2.8781 | 0.5271 | -0.6852 | 0.5815 | 1.9955 | 0.0068 |
| US_nov_may | 0.0814 | 0.1386 | 0.3666 | 2.6015 | 0.5547 | -0.7077 | 0.5815 | 2.0219 | 0.0069 |
| US_dic_abr | 0.0702 | 0.1129 | 0.3275 | 2.8027 | 0.5205 | -0.5284 | 0.4141 | 1.9955 | 0.0068 |
| US_nov_mar | 0.0753 | 0.1060 | 0.3893 | 3.1168 | 0.5820 | -0.5501 | 0.4152 | 1.9955 | 0.0068 |
| US_ref_comprar_mantener | 0.0980 | 0.1936 | 0.3874 | 3.1261 | 0.5840 | -0.8365 | 1.0000 | 0.0132 | 0.0000 |
| US_ref_efectivo | 0.0379 | 0.0090 | 0.0000 | NA | 0.0000 | -0.0009 | 0.0000 | 0.0000 | 0.0000 |
| US_ref_sma10 | 0.0910 | 0.1313 | 0.4475 | 3.3445 | 0.6546 | -0.4350 | 0.7093 | 1.5065 | 0.0051 |
| US_ref_verano | 0.0389 | 0.1484 | 0.0801 | 0.7461 | 0.1162 | -0.6968 | 0.5022 | 2.0087 | 0.0068 |

**EUA, fuera de muestra (2003-01 a 2026-07). Es el tramo de prueba, mirado una sola vez.**

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual |
|---|---|---|---|---|---|---|---|---|---|
| US_nov_abr | 0.0687 | 0.1079 | 0.5161 | 2.7626 | 0.8285 | -0.3032 | 0.5018 | 1.9931 | 0.0068 |
| US_oct_abr | 0.0776 | 0.1223 | 0.5370 | 2.6902 | 0.8328 | -0.4210 | 0.5830 | 1.9931 | 0.0068 |
| US_nov_may | 0.0807 | 0.1149 | 0.5894 | 3.4243 | 0.9378 | -0.2902 | 0.5866 | 1.9931 | 0.0068 |
| US_dic_abr | 0.0448 | 0.0985 | 0.3253 | 1.9075 | 0.4958 | -0.2095 | 0.4205 | 1.9931 | 0.0068 |
| US_nov_mar | 0.0481 | 0.0948 | 0.3680 | 1.6554 | 0.5507 | -0.3339 | 0.4170 | 1.9931 | 0.0068 |
| US_ref_comprar_mantener | 0.1183 | 0.1495 | 0.7149 | 3.4165 | 1.0905 | -0.5031 | 1.0000 | 0.0000 | 0.0000 |
| US_ref_efectivo | 0.0168 | 0.0054 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| US_ref_sma10 | 0.0968 | 0.1039 | 0.7823 | 3.6652 | 1.2538 | -0.1931 | 0.7986 | 1.3994 | 0.0048 |
| US_ref_verano | 0.0496 | 0.1053 | 0.3564 | 1.9237 | 0.5185 | -0.3216 | 0.4982 | 1.9931 | 0.0068 |

**México, dentro de muestra (1992-10 a 2002-12)**

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual |
|---|---|---|---|---|---|---|---|---|---|
| MX_nov_abr | 0.2343 | 0.2189 | 0.1187 | 0.4015 | 0.1637 | -0.4683 | 0.5041 | 2.0487 | 0.0070 |
| MX_oct_abr | 0.2499 | 0.2386 | 0.1810 | 0.5440 | 0.2565 | -0.5116 | 0.5935 | 2.0487 | 0.0070 |
| MX_nov_may | 0.2025 | 0.2303 | 0.0072 | 0.0246 | 0.0097 | -0.4341 | 0.5854 | 2.0487 | 0.0070 |
| MX_dic_abr | 0.2068 | 0.2020 | -0.0039 | -0.0131 | -0.0053 | -0.4703 | 0.4146 | 2.0487 | 0.0070 |
| MX_nov_mar | 0.2512 | 0.2104 | 0.1809 | 0.6058 | 0.2533 | -0.4343 | 0.4228 | 2.0487 | 0.0070 |
| MX_ref_comprar_mantener | 0.1606 | 0.3126 | -0.0377 | -0.1552 | -0.0509 | -0.4491 | 1.0000 | 0.0976 | 0.0003 |
| MX_ref_efectivo | 0.2316 | 0.0367 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| MX_ref_sma10 | 0.1551 | 0.2286 | -0.1797 | -0.7085 | -0.2473 | -0.3636 | 0.6829 | 1.9511 | 0.0066 |
| MX_ref_verano | 0.1419 | 0.2255 | -0.2337 | -0.9485 | -0.3057 | -0.4401 | 0.4959 | 2.1462 | 0.0073 |

**México, fuera de muestra (2003-01 a 2026-07)**

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual |
|---|---|---|---|---|---|---|---|---|---|
| MX_nov_abr | 0.1020 | 0.1201 | 0.3356 | 1.9156 | 0.5146 | -0.2166 | 0.5018 | 1.9931 | 0.0068 |
| MX_oct_abr | 0.0987 | 0.1347 | 0.2906 | 1.5278 | 0.4241 | -0.2950 | 0.5830 | 1.9931 | 0.0068 |
| MX_nov_may | 0.0969 | 0.1294 | 0.2841 | 1.5320 | 0.4294 | -0.2762 | 0.5866 | 1.9931 | 0.0068 |
| MX_dic_abr | 0.0894 | 0.1085 | 0.2534 | 1.6944 | 0.3728 | -0.2166 | 0.4205 | 1.9931 | 0.0068 |
| MX_nov_mar | 0.0956 | 0.1104 | 0.3022 | 1.5663 | 0.4555 | -0.2233 | 0.4170 | 1.9931 | 0.0068 |
| MX_ref_comprar_mantener | 0.1067 | 0.1615 | 0.3115 | 1.2797 | 0.4571 | -0.4448 | 1.0000 | 0.0000 | 0.0000 |
| MX_ref_efectivo | 0.0664 | 0.0068 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| MX_ref_sma10 | 0.1006 | 0.1145 | 0.3343 | 1.1657 | 0.5151 | -0.2125 | 0.6572 | 1.9931 | 0.0068 |
| MX_ref_verano | 0.0565 | 0.1083 | -0.0317 | -0.1324 | -0.0434 | -0.3606 | 0.4982 | 1.9931 | 0.0068 |

**Ventanas pre-registradas, EUA**

| variante | ventana | n | cagr | vol_anual | sharpe | nw_t | mdd | exposicion_media |
|---|---|---|---|---|---|---|---|---|
| US_nov_abr | pre-articulo (1927-04-30 a 1969-12-31) | 512 | 0.0578 | 0.1354 | 0.3509 | 2.09 | -0.5760 | 0.4961 |
| US_nov_abr | articulo (1969-12-31 a 1998-08-31) | 344 | 0.1225 | 0.1058 | 0.5242 | 2.67 | -0.2758 | 0.5000 |
| US_nov_abr | hueco (1998-08-31 a 2002-12-31) | 52 | 0.0617 | 0.1381 | 0.2162 | 0.49 | -0.2323 | 0.5000 |
| US_nov_abr | fuera de muestra (2002-12-31 a 2026-07-31) | 283 | 0.0687 | 0.1079 | 0.5161 | 2.76 | -0.3032 | 0.5018 |
| US_ref_comprar_mantener | pre-articulo (1927-04-30 a 1969-12-31) | 512 | 0.0918 | 0.2138 | 0.4340 | 2.59 | -0.8365 | 1.0000 |
| US_ref_comprar_mantener | articulo (1969-12-31 a 1998-08-31) | 344 | 0.1227 | 0.1593 | 0.3945 | 2.14 | -0.4651 | 1.0000 |
| US_ref_comprar_mantener | hueco (1998-08-31 a 2002-12-31) | 52 | 0.0013 | 0.1921 | -0.1048 | -0.19 | -0.4499 | 1.0000 |
| US_ref_comprar_mantener | fuera de muestra (2002-12-31 a 2026-07-31) | 283 | 0.1183 | 0.1495 | 0.7149 | 3.42 | -0.5031 | 1.0000 |
| US_ref_sma10 | pre-articulo (1927-04-30 a 1969-12-31) | 512 | 0.0830 | 0.1355 | 0.5268 | 2.77 | -0.4350 | 0.7051 |
| US_ref_sma10 | articulo (1969-12-31 a 1998-08-31) | 344 | 0.1107 | 0.1282 | 0.3722 | 1.89 | -0.2484 | 0.7529 |
| US_ref_sma10 | hueco (1998-08-31 a 2002-12-31) | 52 | 0.0423 | 0.1081 | 0.0700 | 0.16 | -0.1433 | 0.4615 |
| US_ref_sma10 | fuera de muestra (2002-12-31 a 2026-07-31) | 283 | 0.0968 | 0.1039 | 0.7823 | 3.67 | -0.1931 | 0.7986 |
| US_ref_verano | pre-articulo (1927-04-30 a 1969-12-31) | 512 | 0.0366 | 0.1666 | 0.1905 | 1.31 | -0.6968 | 0.5039 |
| US_ref_verano | articulo (1969-12-31 a 1998-08-31) | 344 | 0.0538 | 0.1191 | -0.0520 | -0.33 | -0.2961 | 0.5000 |
| US_ref_verano | hueco (1998-08-31 a 2002-12-31) | 52 | -0.0327 | 0.1319 | -0.4894 | -1.01 | -0.3793 | 0.5000 |
| US_ref_verano | fuera de muestra (2002-12-31 a 2026-07-31) | 283 | 0.0496 | 0.1053 | 0.3564 | 1.92 | -0.3216 | 0.4982 |

**Ventanas pre-registradas, México**

| variante | ventana | n | cagr | vol_anual | sharpe | nw_t | mdd | exposicion_media |
|---|---|---|---|---|---|---|---|---|
| MX_nov_abr | traslape articulo (1992-09-30 a 1998-08-31) | 71 | 0.2088 | 0.2299 | -0.1461 | -0.41 | -0.4683 | 0.5070 |
| MX_nov_abr | hueco (1998-08-31 a 2002-12-31) | 52 | 0.2700 | 0.2048 | 0.5134 | 1.19 | -0.1583 | 0.5000 |
| MX_nov_abr | fuera de muestra (2002-12-31 a 2026-07-31) | 283 | 0.1020 | 0.1201 | 0.3356 | 1.92 | -0.2166 | 0.5018 |
| MX_ref_comprar_mantener | traslape articulo (1992-09-30 a 1998-08-31) | 71 | 0.1466 | 0.3287 | -0.1771 | -0.43 | -0.4491 | 1.0000 |
| MX_ref_comprar_mantener | hueco (1998-08-31 a 2002-12-31) | 52 | 0.1799 | 0.2922 | 0.1791 | 0.45 | -0.2770 | 1.0000 |
| MX_ref_comprar_mantener | fuera de muestra (2002-12-31 a 2026-07-31) | 283 | 0.1067 | 0.1615 | 0.3115 | 1.28 | -0.4448 | 1.0000 |
| MX_ref_sma10 | traslape articulo (1992-09-30 a 1998-08-31) | 71 | 0.2135 | 0.2366 | -0.1223 | -0.41 | -0.2116 | 0.8028 |
| MX_ref_sma10 | hueco (1998-08-31 a 2002-12-31) | 52 | 0.0799 | 0.2177 | -0.2633 | -0.58 | -0.3636 | 0.5192 |
| MX_ref_sma10 | fuera de muestra (2002-12-31 a 2026-07-31) | 283 | 0.1006 | 0.1145 | 0.3343 | 1.17 | -0.2125 | 0.6572 |
| MX_ref_verano | traslape articulo (1992-09-30 a 1998-08-31) | 71 | 0.1981 | 0.2380 | -0.1657 | -0.37 | -0.4401 | 0.4930 |
| MX_ref_verano | hueco (1998-08-31 a 2002-12-31) | 52 | 0.0696 | 0.2077 | -0.3451 | -0.77 | -0.3460 | 0.5000 |
| MX_ref_verano | fuera de muestra (2002-12-31 a 2026-07-31) | 283 | 0.0565 | 0.1083 | -0.0317 | -0.13 | -0.3606 | 0.4982 |

**Criterios pre-registrados** (salida textual del script):

- (i) EUA 1970-01..1998-08: a1=1.0377 (MP 1.0349; |dif|=0.0028 <= 0.2?), t MCO=2.09 -> True
- (ii) EUA 1926-07..2002-12: a1=0.6819, t NW12=2.07 -> True
- (iii) EUA 2003-01..final: a1=0.2886 -> True
- (iv) Mexico 2003-01..final: a1=0.7063 -> True
- Estado segun la regla pre-registrada: Replicado
- Significativo fuera de muestra US (t NW12 >= 2 y IC95 bootstrap de D excluye 0): False (t NW12=0.70; IC95 D=[-3.059, 7.500]); exceso nov-abr=0.9401 (t NW12=2.78)
- Significativo fuera de muestra MX (t NW12 >= 2 y IC95 bootstrap de D excluye 0): False (t NW12=1.60; IC95 D=[-0.975, 10.608]); exceso nov-abr=0.6584 (t NW12=1.90)
- Regla [R] 6 de arena/investigacion/03 segun el criterio pre-registrado: modificar
- H5 US_nov_abr vs US_ref_comprar_mantener fuera de muestra: Sharpe 0.5161 vs 0.7149; MDD -0.3032 vs -0.5031; CAGR 0.0687 vs 0.1183 -> NO supera en ambos
- H5 US_nov_abr vs US_ref_sma10 fuera de muestra: Sharpe 0.5161 vs 0.7823; MDD -0.3032 vs -0.1931; CAGR 0.0687 vs 0.0968 -> NO supera en ambos
- H5 MX_nov_abr vs MX_ref_comprar_mantener fuera de muestra: Sharpe 0.3356 vs 0.3115; MDD -0.2166 vs -0.4448; CAGR 0.1020 vs 0.1067 -> supera en Sharpe y MDD
- H5 MX_nov_abr vs MX_ref_sma10 fuera de muestra: Sharpe 0.3356 vs 0.3343; MDD -0.2166 vs -0.2125; CAGR 0.1020 vs 0.1006 -> NO supera en ambos

### 12. Sensibilidad

**Costos.** EUA fuera de muestra, spread "medio" y bruto:

Tabla `US - costos medio - segmento fuera_muestra`:

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual |
|---|---|---|---|---|---|---|---|---|---|
| US_nov_abr | 0.0666 | 0.1079 | 0.4978 | 2.6633 | 0.7967 | -0.3053 | 0.5018 | 1.9931 | 0.0088 |
| US_oct_abr | 0.0754 | 0.1223 | 0.5204 | 2.6088 | 0.8048 | -0.4222 | 0.5830 | 1.9931 | 0.0088 |
| US_nov_may | 0.0785 | 0.1149 | 0.5721 | 3.3232 | 0.9080 | -0.2923 | 0.5866 | 1.9931 | 0.0088 |
| US_dic_abr | 0.0427 | 0.0985 | 0.3049 | 1.7885 | 0.4632 | -0.2119 | 0.4205 | 1.9931 | 0.0088 |
| US_nov_mar | 0.0460 | 0.0947 | 0.3472 | 1.5601 | 0.5174 | -0.3359 | 0.4170 | 1.9931 | 0.0088 |
| US_ref_comprar_mantener | 0.1183 | 0.1495 | 0.7149 | 3.4165 | 1.0905 | -0.5031 | 1.0000 | 0.0000 | 0.0000 |
| US_ref_efectivo | 0.0168 | 0.0054 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| US_ref_sma10 | 0.0953 | 0.1039 | 0.7682 | 3.5739 | 1.2285 | -0.1979 | 0.7986 | 1.3994 | 0.0062 |
| US_ref_verano | 0.0476 | 0.1053 | 0.3373 | 1.8208 | 0.4893 | -0.3257 | 0.4982 | 1.9931 | 0.0088 |

Tabla `US - costos bruto - segmento fuera_muestra`:

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual |
|---|---|---|---|---|---|---|---|---|---|
| US_nov_abr | 0.0760 | 0.1083 | 0.5776 | 3.0993 | 0.9361 | -0.2960 | 0.5018 | 1.9931 | 0.0000 |
| US_oct_abr | 0.0849 | 0.1222 | 0.5929 | 2.9666 | 0.9280 | -0.4170 | 0.5830 | 1.9931 | 0.0000 |
| US_nov_may | 0.0880 | 0.1153 | 0.6474 | 3.7675 | 1.0381 | -0.2829 | 0.5866 | 1.9931 | 0.0000 |
| US_dic_abr | 0.0519 | 0.0985 | 0.3943 | 2.3115 | 0.6067 | -0.2022 | 0.4205 | 1.9931 | 0.0000 |
| US_nov_mar | 0.0552 | 0.0954 | 0.4378 | 1.9788 | 0.6635 | -0.3270 | 0.4170 | 1.9931 | 0.0000 |
| US_ref_comprar_mantener | 0.1183 | 0.1495 | 0.7149 | 3.4165 | 1.0905 | -0.5031 | 1.0000 | 0.0000 | 0.0000 |
| US_ref_efectivo | 0.0168 | 0.0054 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| US_ref_sma10 | 0.1021 | 0.1037 | 0.8296 | 3.9832 | 1.3389 | -0.1764 | 0.7986 | 1.3994 | 0.0000 |
| US_ref_verano | 0.0568 | 0.1054 | 0.4209 | 2.2730 | 0.6180 | -0.3076 | 0.4982 | 1.9931 | 0.0000 |

EUA dentro de muestra, spread "medio" y bruto:

Tabla `US - costos medio - segmento dentro_muestra`:

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual |
|---|---|---|---|---|---|---|---|---|---|
| US_nov_abr | 0.0799 | 0.1253 | 0.3801 | 3.0493 | 0.5968 | -0.5777 | 0.4978 | 1.9955 | 0.0088 |
| US_oct_abr | 0.0773 | 0.1398 | 0.3370 | 2.7611 | 0.5042 | -0.6921 | 0.5815 | 1.9955 | 0.0088 |
| US_nov_may | 0.0792 | 0.1386 | 0.3518 | 2.4973 | 0.5311 | -0.7093 | 0.5815 | 2.0219 | 0.0089 |
| US_dic_abr | 0.0680 | 0.1129 | 0.3096 | 2.6501 | 0.4908 | -0.5392 | 0.4141 | 1.9955 | 0.0088 |
| US_nov_mar | 0.0731 | 0.1060 | 0.3703 | 2.9650 | 0.5513 | -0.5608 | 0.4152 | 1.9955 | 0.0088 |
| US_ref_comprar_mantener | 0.0979 | 0.1936 | 0.3873 | 3.1256 | 0.5839 | -0.8365 | 1.0000 | 0.0132 | 0.0001 |
| US_ref_efectivo | 0.0379 | 0.0090 | 0.0000 | NA | 0.0000 | -0.0009 | 0.0000 | 0.0000 | 0.0000 |
| US_ref_sma10 | 0.0894 | 0.1313 | 0.4358 | 3.2408 | 0.6366 | -0.4367 | 0.7093 | 1.5065 | 0.0066 |
| US_ref_verano | 0.0368 | 0.1484 | 0.0665 | 0.6198 | 0.0963 | -0.6986 | 0.5022 | 2.0087 | 0.0088 |

Tabla `US - costos bruto - segmento dentro_muestra`:

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual |
|---|---|---|---|---|---|---|---|---|---|
| US_nov_abr | 0.0895 | 0.1254 | 0.4506 | 3.6146 | 0.7168 | -0.5702 | 0.4978 | 1.9955 | 0.0000 |
| US_oct_abr | 0.0868 | 0.1395 | 0.4009 | 3.2758 | 0.6054 | -0.6776 | 0.5815 | 1.9955 | 0.0000 |
| US_nov_may | 0.0888 | 0.1387 | 0.4165 | 2.9553 | 0.6350 | -0.7037 | 0.5815 | 2.0219 | 0.0000 |
| US_dic_abr | 0.0775 | 0.1131 | 0.3877 | 3.3211 | 0.6214 | -0.4975 | 0.4141 | 1.9955 | 0.0000 |
| US_nov_mar | 0.0826 | 0.1061 | 0.4535 | 3.6322 | 0.6869 | -0.5135 | 0.4152 | 1.9955 | 0.0000 |
| US_ref_comprar_mantener | 0.0980 | 0.1936 | 0.3876 | 3.1276 | 0.5844 | -0.8365 | 1.0000 | 0.0132 | 0.0000 |
| US_ref_efectivo | 0.0379 | 0.0090 | 0.0000 | NA | 0.0000 | -0.0009 | 0.0000 | 0.0000 | 0.0000 |
| US_ref_sma10 | 0.0966 | 0.1312 | 0.4870 | 3.7042 | 0.7155 | -0.4294 | 0.7093 | 1.5065 | 0.0000 |
| US_ref_verano | 0.0461 | 0.1483 | 0.1262 | 1.1750 | 0.1844 | -0.6905 | 0.5022 | 2.0087 | 0.0000 |

México fuera de muestra, spread "medio" y bruto:

Tabla `MX - costos medio - segmento fuera_muestra`:

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual |
|---|---|---|---|---|---|---|---|---|---|
| MX_nov_abr | 0.0998 | 0.1201 | 0.3188 | 1.8202 | 0.4872 | -0.2166 | 0.5018 | 1.9931 | 0.0088 |
| MX_oct_abr | 0.0965 | 0.1348 | 0.2756 | 1.4500 | 0.4012 | -0.2964 | 0.5830 | 1.9931 | 0.0088 |
| MX_nov_may | 0.0947 | 0.1294 | 0.2685 | 1.4482 | 0.4047 | -0.2791 | 0.5866 | 1.9931 | 0.0088 |
| MX_dic_abr | 0.0873 | 0.1084 | 0.2349 | 1.5696 | 0.3445 | -0.2166 | 0.4205 | 1.9931 | 0.0088 |
| MX_nov_mar | 0.0934 | 0.1104 | 0.2839 | 1.4720 | 0.4263 | -0.2264 | 0.4170 | 1.9931 | 0.0088 |
| MX_ref_comprar_mantener | 0.1067 | 0.1615 | 0.3115 | 1.2797 | 0.4571 | -0.4448 | 1.0000 | 0.0000 | 0.0000 |
| MX_ref_efectivo | 0.0664 | 0.0068 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| MX_ref_sma10 | 0.0984 | 0.1147 | 0.3164 | 1.0972 | 0.4864 | -0.2235 | 0.6572 | 1.9931 | 0.0088 |
| MX_ref_verano | 0.0544 | 0.1084 | -0.0500 | -0.2091 | -0.0683 | -0.3606 | 0.4982 | 1.9931 | 0.0088 |

Tabla `MX - costos bruto - segmento fuera_muestra`:

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual |
|---|---|---|---|---|---|---|---|---|---|
| MX_nov_abr | 0.1095 | 0.1203 | 0.3924 | 2.2395 | 0.6078 | -0.2166 | 0.5018 | 1.9931 | 0.0000 |
| MX_oct_abr | 0.1062 | 0.1345 | 0.3417 | 1.7921 | 0.5024 | -0.2902 | 0.5830 | 1.9931 | 0.0000 |
| MX_nov_may | 0.1044 | 0.1295 | 0.3368 | 1.8165 | 0.5135 | -0.2663 | 0.5866 | 1.9931 | 0.0000 |
| MX_dic_abr | 0.0969 | 0.1089 | 0.3157 | 2.1181 | 0.4687 | -0.2166 | 0.4205 | 1.9931 | 0.0000 |
| MX_nov_mar | 0.1031 | 0.1106 | 0.3638 | 1.8863 | 0.5551 | -0.2166 | 0.4170 | 1.9931 | 0.0000 |
| MX_ref_comprar_mantener | 0.1067 | 0.1615 | 0.3115 | 1.2797 | 0.4571 | -0.4448 | 1.0000 | 0.0000 | 0.0000 |
| MX_ref_efectivo | 0.0664 | 0.0068 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| MX_ref_sma10 | 0.1081 | 0.1140 | 0.3951 | 1.4056 | 0.6131 | -0.1741 | 0.6572 | 1.9931 | 0.0000 |
| MX_ref_verano | 0.0637 | 0.1082 | 0.0308 | 0.1285 | 0.0426 | -0.3606 | 0.4982 | 1.9931 | 0.0000 |

Lectura de costos:

- En EUA dentro de muestra, la ventaja de Sharpe de `US_nov_abr` sobre comprar y mantener es:
  - Bruta: 0.4506 contra 0.3876.
  - Casi toda desaparece con los costos por defecto: 0.3962 contra 0.3874.
  - **Se invierte** con spread "medio": 0.3801 contra 0.3873.
- Fuera de muestra, `US_nov_abr` queda debajo de comprar y mantener **incluso bruta**: 0.5776 contra 0.7149.
- En México fuera de muestra, la regla supera a comprar y mantener en Sharpe en los tres escenarios: 0.3356, 0.3188 y 0.3924, contra 0.3115.

**Parámetros vecinos** (las 4 ventanas alternativas; tablas de 11.4):

- EUA fuera de muestra: ninguna ventana supera a comprar y mantener (0.7149) ni a la SMA10 (0.7823) en Sharpe. Van de 0.3253 (`US_dic_abr`) a 0.5894 (`US_nov_may`).
- México fuera de muestra: van de 0.2534 a 0.3356. La del artículo es la mejor.

**Subperiodos.** α₁ de EUA por década (diagnóstico):

| decada | desde | hasta | n | a1 | t NW12 | media inv. | media ver. |
|---|---|---|---|---|---|---|---|
| 1920s | 1926-07-31 | 1929-12-31 | 42 | 1.1574 | 1.58 | 1.8993 | 0.7419 |
| 1930s | 1930-01-31 | 1939-12-31 | 120 | -0.8607 | -0.52 | -0.4522 | 0.4085 |
| 1940s | 1940-01-31 | 1949-12-31 | 120 | -0.3574 | -0.40 | 0.5768 | 0.9342 |
| 1950s | 1950-01-31 | 1959-12-31 | 120 | 1.3031 | 3.22 | 2.0551 | 0.7520 |
| 1960s | 1960-01-31 | 1969-12-31 | 120 | 1.0962 | 1.88 | 1.2094 | 0.1131 |
| 1970s | 1970-01-31 | 1979-12-31 | 120 | 1.3889 | 1.74 | 1.1847 | -0.2042 |
| 1980s | 1980-01-31 | 1989-12-31 | 120 | 0.7843 | 1.13 | 1.6914 | 0.9071 |
| 1990s | 1990-01-31 | 1999-12-31 | 120 | 1.0730 | 1.42 | 1.9153 | 0.8422 |
| 2000s | 2000-01-31 | 2009-12-31 | 120 | 0.4610 | 0.69 | 0.1988 | -0.2622 |
| 2010s | 2010-01-31 | 2019-12-31 | 120 | 1.0732 | 2.16 | 1.5992 | 0.5261 |
| 2020s | 2020-01-31 | 2026-07-31 | 79 | -0.6927 | -0.66 | 0.8239 | 1.5166 |

α₁ es negativo en los años treinta, en los cuarenta y en 2020–2026 (−0.6927, 79 meses). Antes de 1970, α₁ = 0.3603 (t NW12 = 0.75).

**Otra moneda (MXN).** Un inversionista mexicano con el mercado de EUA convertido con DEXMXUS y efectivo en CETES:

Tabla `USMXN (sensibilidad, MXN) - costos defecto - segmento dentro_muestra`:

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual |
|---|---|---|---|---|---|---|---|---|---|
| USMXN_nov_abr | 0.2620 | 0.2072 | 0.1777 | 0.5226 | 0.3576 | -0.2114 | 0.5046 | 2.0915 | 0.0071 |
| USMXN_ref_comprar_mantener | 0.2416 | 0.2375 | 0.1132 | 0.3029 | 0.2002 | -0.3986 | 1.0000 | 0.1101 | 0.0004 |
| USMXN_ref_efectivo | 0.2393 | 0.0386 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| USMXN_ref_sma10 | 0.2258 | 0.1441 | -0.0147 | -0.0507 | -0.0208 | -0.1313 | 0.6881 | 1.7613 | 0.0060 |

Tabla `USMXN (sensibilidad, MXN) - costos defecto - segmento fuera_muestra`:

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual |
|---|---|---|---|---|---|---|---|---|---|
| USMXN_nov_abr | 0.0887 | 0.0922 | 0.2688 | 1.1790 | 0.4192 | -0.1730 | 0.5018 | 1.9931 | 0.0068 |
| USMXN_ref_comprar_mantener | 0.1427 | 0.1296 | 0.5979 | 2.5167 | 0.9776 | -0.2997 | 1.0000 | 0.0000 | 0.0000 |
| USMXN_ref_efectivo | 0.0664 | 0.0068 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| USMXN_ref_sma10 | 0.1326 | 0.1050 | 0.6253 | 2.6510 | 1.0717 | -0.1431 | 0.7986 | 1.3994 | 0.0048 |

**Otro instrumento (NAFTRAC, rendimiento total con dividendos, 2008-12 a 2026-07, sin corte):**

Tabla `NAFTRAC (sensibilidad, MXN) - costos defecto - segmento completo`:

| variante | cagr | vol_anual | sharpe | nw_t | sortino | mdd | exposicion_media | operaciones_por_anio | costo_anual |
|---|---|---|---|---|---|---|---|---|---|
| NAFTRAC_nov_abr | 0.0843 | 0.1221 | 0.2274 | 1.3226 | 0.3378 | -0.2122 | 0.5047 | 2.0380 | 0.0069 |
| NAFTRAC_ref_comprar_mantener | 0.0865 | 0.1546 | 0.2202 | 1.0080 | 0.3276 | -0.2838 | 1.0000 | 0.0566 | 0.0002 |
| NAFTRAC_ref_efectivo | 0.0627 | 0.0073 | 0.0000 | NA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| NAFTRAC_ref_sma10 | 0.0498 | 0.1033 | -0.0668 | -0.2630 | -0.0931 | -0.2002 | 0.6698 | 2.3210 | 0.0079 |

Efecto en NAFTRAC:

| ventana | desde | hasta | n | mu (verano) | a1 | t MCO | t HC1 | t NW12 | p NW | media inv. | media ver. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NAFTRAC completo | 2008-02-29 | 2026-07-31 | 222 | 0.0456 | 0.9250 | 1.48 | 1.48 | 1.81 | 0.0705 | 0.9706 | 0.0456 |

| ventana | anios | media D | mediana D | t iid | IC95 bootstrap | D>0 | p signo (1 cola) | 6*a1 | peor anio | mejor anio |
|---|---|---|---|---|---|---|---|---|---|---|
| NAFTRAC completo | 2009-2025 (N=17) | 2.832 | 3.760 | 0.98 | [-2.550, 8.489] | 11/17 | 0.1662 | 5.550 | 2009: -18.97 | 2024: 24.20 |

| ventana | exceso nov-abr | t NW | exceso may-oct | t NW | semestres inv. (N) | media semestre | mediana | % semestres > 0 | peor semestre |
|---|---|---|---|---|---|---|---|---|---|
| NAFTRAC completo | 0.4575 | 1.38 | -0.4670 | -1.03 | 18 | 2.618 | 1.620 | 0.611 | 2020: -19.74 |

### 13. Diferencia frente al artículo

| Aspecto | Artículo | Réplica | ¿Explica la diferencia? |
|---|---|---|---|
| Datos / versión, EUA | MSCI con dividendos, en moneda local (AER). La cifra usada viene de Maberly-Pierce: CRSP VW con dividendos | French Mkt-RF + RF (CRSP 202607, sha256 b840dba5…) | Diferencia de 0.0028 pp en α₁: no hay nada material que explicar |
| Datos, México | MSCI México con dividendos; cifra del AER **no leída** | `^MXX` de precio, sin dividendos, desde 1991-12 | No hay cifra contra la cual medir. Contra Jacobsen-Zhang (1998-09 a 2011-07): 6·α₁ = 8.147 (t NW12 1.36) en la réplica contra β = 8.15 (t 1.36) |
| Contraste Jacobsen-Zhang, EUA (β semestral, t NW) | 1970 a 1998-08: β = 5.82 (t 2.45); 1998-09 a 2011-07: 4.90 (t 1.57) | 1970-01 a 1998-08: 6·α₁ = 6.226 (t NW12 2.32), media de D = 5.850. 1998-09 a 2011-07: 6·α₁ = 5.580 (t NW12 1.63), media de D = 5.386 | Mismo orden de magnitud y significancia; las fuentes de datos son distintas |
| Periodo | 1970-01 a 1998-08 | El mismo, más 1926–1969, el hueco 1998–2002 y 2003–2026 | El efecto de EUA se concentra en 1950–1999 y en los 2010s. En 1926–1969 no es significativo. La ventana "fuera de muestra" de Jacobsen-Zhang (desde 1998-09) incluye el hueco 1998-09 a 2002-12, en el que ganó el invierno los 4 años (EUA D = 13.445; México D = 26.305). Eso **infla** su evidencia post-muestra frente al tramo post-publicación (2003+) usado aquí |
| Método | Regresión con dummy y EE HC (versión de 1997) | MCO, HC1, NW12, D pareada con bootstrap, prueba de signo, winsorización, enero, dummies MP y placebo | En la ventana del artículo, t MCO = 2.09. Con NW12, 2.32; con dummy de enero (t NW12), 1.96; con dummies MP (t MCO), 1.68 |
| Costos | La versión de 1997 afirma que la estrategia gana "even net of transactions costs", sin modelo explícito | GBM: 0.29% de comisión + 0.05% de spread por lado; 0.68% anual con 2 cambios por año | En EUA dentro de muestra, los costos por defecto eliminan casi toda la ventaja de Sharpe sobre comprar y mantener |
| Regla | Índice de noviembre a abril; T-bills de mayo a octubre | La misma, al cierre de mes, con efectivo RF (EUA) o CETES (México) | — |
| Estrategia contra comprar y mantener, EUA | Versión de 1997 (1973–1996): 11.61% contra 11.37% anual, con desviación de 11.38% contra 16.40% | Ventana del artículo (1970-01 a 1998-08), neta: CAGR 0.1225 contra 0.1227, vol 0.1058 contra 0.1593, Sharpe 0.5242 contra 0.3945 | Mismo patrón: rendimiento casi igual con menos riesgo. **Fuera de muestra ya no:** CAGR 0.0687 contra 0.1183 y Sharpe 0.5161 contra 0.7149 |

### 14. Conclusiones permitidas

- **La cifra de EUA del artículo se reproduce** con datos French/CRSP en su periodo (1970-01 a 1998-08, USD, rendimientos log): α₁ = 1.0377 pp por mes (t MCO 2.09, t NW12 2.32), contra 1.0349 (t 2.10).
- **La crítica de Maberly-Pierce también se reproduce.** Con dummies para octubre de 1987 y agosto de 1998, α₁ = 0.7819 (t MCO 1.68).
- **En la historia larga de EUA dentro de muestra (1926-07 a 2002-12)**, α₁ = 0.6819 (t NW12 = 2.07). La significancia es frágil:
  - Con dummy de enero: t = 1.69.
  - Con dummies MP: t = 1.63 (MCO).
  - El IC95 bootstrap de D incluye el 0: [−0.272, 8.283].
  - Resiste la winsorización: t = 2.26.
  - Prueba de signo: 51 de 76 años, p = 0.0019.
- **En EUA 1926–2026 completo**, α₁ = 0.5895 (t NW12 = 2.18). El invierno le ganó al verano en 67 de 99 años (p de signo = 0.0003).
- **México (`^MXX`, sin dividendos).**
  - Dentro de muestra (1991-12 a 2002-12, 133 meses): α₁ = 2.2850, t NW12 = 1.54. No es significativo.
  - Muestra completa (1991-12 a 2026-07): α₁ = 1.2115, t NW12 = 2.13. Con dummy de enero la t es 2.21 y winsorizado 2.24.
  - Pero el IC95 bootstrap de D incluye el 0: [−0.256, 12.404]. Signo: 22 de 33 años (p = 0.0401).
- **Fuera de muestra (2003-01 a 2026-07), el efecto tiene el mismo signo en EUA y en México, pero no es significativo** según la definición pre-registrada:
  - EUA: α₁ = 0.2886, t NW12 = 0.70, IC95 de D = [−3.059, 7.500].
  - México: α₁ = 0.7063, t NW12 = 1.60, IC95 de D = [−0.975, 10.608].
  - Prueba de signo (secundaria): EUA 16 de 22 años (p = 0.0262) y México 15 de 22 (p = 0.0669).
- **En EUA fuera de muestra**, el exceso de noviembre a abril sobre la RF fue positivo y significativo: 0.9401 pp log por mes, t NW12 = 2.78, con 78.3% de los semestres de invierno positivos (23 semestres). **El de mayo a octubre también fue positivo:** 0.6457, t NW12 = 1.91.
- **Antes de 1970 el efecto de EUA no es significativo** (α₁ = 0.3603, t NW12 = 0.75), y en los años treinta y cuarenta es negativo. Esto coincide con el resumen de Plastun, Sibande, Gupta y Wohar (2020, *International Economics* 161:130–138), consultado en IDEAS/RePEc: en EUA el efecto "only became detectable in the middle of the 20th century". Solo se leyó el resumen.
- **Como estrategia en EUA fuera de muestra, neta de costos GBM**, Halloween reduce la volatilidad (0.1079 contra 0.1495) y el MDD (−0.3032 contra −0.5031). A cambio, rinde menos CAGR (0.0687 contra 0.1183) y **menos Sharpe** (0.5161 contra 0.7149). También queda debajo de la SMA10 en Sharpe (0.7823) y en MDD (−0.1931).
- **En México fuera de muestra**, con `^MXX` sin dividendos y costos por defecto, Halloween supera a comprar y mantener en Sharpe (0.3356 contra 0.3115) y en MDD (−0.2166 contra −0.4448), con CAGR de 0.1020 contra 0.1067. Con NAFTRAC (rendimiento total, 2008-12 a 2026-07), la ventaja de Sharpe se reduce a 0.2274 contra 0.2202 y el MDD es −0.2122 contra −0.2838.

### 15. Conclusiones que NO se sostienen

- "Sell in May funciona en EUA después de publicarse". Post-2002, α₁ = 0.2886 (t 0.70), noviembre–abril queda en el lugar 4 de 12 y en 2020–2026 α₁ es negativo.
- "El efecto se está haciendo más fuerte" (Jacobsen-Zhang, citado en `arena/investigacion/03`). En EUA, α₁ fuera de muestra (0.2886) es menor que dentro de muestra (0.6819). La evidencia post-muestra de Jacobsen-Zhang depende en parte del hueco 1998–2002.
- "La mitad noviembre–abril tiene un rendimiento esperado demostrablemente mayor que la otra mitad", hoy y en EUA. No fuera de muestra.
- "Halloween le gana a comprar y mantener" en EUA. Fuera de muestra pierde en CAGR y en Sharpe, incluso bruto.
- "Halloween le gana a la regla sencilla". No supera a la SMA10 en ambas métricas ni en EUA ni en México.
- "Funciona para un inversionista mexicano que compra EUA en MXN". USMXN fuera de muestra: Sharpe 0.2688 contra 0.5979 de comprar y mantener y 0.6253 de la SMA10.
- "La ventaja en México es real y de ese tamaño". `^MXX` no tiene dividendos, lo que favorece a Halloween. La diferencia NAFTRAC − `^MXX` es de 0.00130 por mes. Además, no se modelan los impuestos por realizar ganancias cada año ni el DSR ≥ 0.95.
- "Es robusto a valores extremos" en la ventana del artículo. Con dummies MP la t cae a 1.68.
- "Tiene ventaja con dinero real" o "es candidata para el satélite". DSR < 0.95 en la lectura conservadora; no hay papel ni impuestos.

### 16. Estado y reproducción

- **Estado: Replicado** (regla pre-registrada: se cumplen (i), (ii), (iii) y (iv)). Alcance del estado:
  - El hallazgo del artículo se reproduce en su periodo y con sus datos equivalentes.
  - Fuera de muestra, en ambos mercados, el efecto tiene **el mismo signo pero no es significativo**.
  - La regla, como estrategia, **no** agrega valor frente a comprar y mantener en EUA.
  - "Replicado" no significa "usable con dinero" (README, sección 1).
- **Comando que reproduce todo:** `python3 laboratorio/replicas/R04.py`, desde la raíz del repo. Tarda unos 2 s con caché y agrega 178 filas nuevas al CSV en cada ejecución.
- **Huella de datos (`huella_datos` del CSV):**
  - EUA: `e85ac74d630dff95`.
  - México (`^MXX`-CETES): `88e4d9f1c178a318`.
  - USMXN: `8266d9090e0a3a0c`.
  - NAFTRAC: `3964e250b9f0175c`.
- **French** `F-F_Research_Data_Factors_CSV.zip`: CRSP 202607, sha256 `b840dba55d319f4818fc7300e65c52eff5f64870c8d495fa58ff5d4cd749f5eb`.
- **Yahoo y FRED:**
  - `^MXX`: barras de 1991-11-30 a 2026-08-31.
  - NAFTRAC.MX: barras de 2008-01-31 a 2026-08-31.
  - INTGSTMXM193N: de 1986-10 a 2026-07, sin meses rellenados.
  - DEXMXUS: de 1993-11-08 a 2026-09-18.
  - Todo descargado el 2026-09-25.
- **Fecha de la corrida final:** 2026-09-25, 05:49 UTC.
- **Comprobación independiente:** se recalcularon fuera del motor, directamente de French, el CAGR bruto fuera de muestra de `US_nov_abr` (0.07599) y de comprar y mantener (0.11835), y α₁ de la ventana del artículo como diferencia de medias (1.03769). Coinciden con el motor.
- **Pendientes:**
  - Leer el PDF del AER (acceso bloqueado) para confirmar la cifra de EUA y obtener la de México.
  - Revisión independiente (`auditor-de-replicas`).
  - Capa de impuestos (ISR de 10% sobre ganancias realizadas cada año).
  - Spread cambiario de GBM en SIC.

### 17. Conclusión operable

1. **Regla [R] 6 de `arena/investigacion/03-teoria-de-torneos-y-estrategia-competitiva.md` ("Estacionalidad a favor, no en contra"): MODIFICAR**, por el criterio pre-registrado. El exceso de invierno es positivo, pero α₁ no es significativo fuera de muestra. Texto propuesto (no se aplicó en ese documento; lo decide su responsable):
   - "El efecto Halloween se replicó en la ventana del artículo (R04), pero post-2002 la diferencia invierno-verano no es significativa: EUA α₁ = 0.29 pp por mes (t 0.70) y México 0.71 (t 1.60).
   - No usar el calendario para **subir** exposición ni para justificar un sesgo de μ adicional.
   - 'No arrancar en efectivo' se sostiene con la prima de mercado, no con la estación. En EUA 2003–2026 el exceso fue positivo en ambas mitades (nov–abr 0.94 y may–oct 0.65 pp log por mes), y 18 de 23 semestres de invierno tuvieron exceso positivo.
   - Grado del efecto como ventaja: **C** (baja de B)."
   - Nota sobre la cifra que cita ese documento: en la versión de trabajo SSRN 2154873 que se leyó, **4.52% es el rendimiento anual promedio de la estrategia Halloween en el Reino Unido, 1693–2009** (tabla 8; comprar y mantener: 1.38%). No es una cifra de EUA ni de México. La versión publicada (2020) no se leyó.
2. **"Sell in May" como regla de timing sobre el índice de EUA: DESCARTAR como candidata.**
   - Fuera de muestra, neta de costos GBM, no supera a comprar y mantener en Sharpe (0.5161 contra 0.7149) ni a la SMA10 (0.7823).
   - Rinde casi 5 pp menos de CAGR al año (0.0687 contra 0.1183).
   - En MXN es peor todavía: 0.2688 contra 0.5979.
   - DSR de 0.9082 dentro de muestra y 0.9405 fuera de muestra: menor a 0.95.
3. **Halloween sobre el IPC o NAFTRAC: INVESTIGAR; no es candidata.**
   - Reduce el MDD: con `^MXX`, a menos de la mitad (−0.2166 contra −0.4448); con NAFTRAC, de −0.2838 a −0.2122.
   - Su Sharpe es apenas mayor (NAFTRAC 0.2274 contra 0.2202).
   - No supera a la SMA10 en ambas métricas.
   - Su DSR es de 0.3457 dentro de muestra y 0.7560 fuera de muestra.
   - No descuenta impuestos anuales.
   - Si se retoma, será como capa de reducción de drawdown, con nuevo pre-registro, papel y capa fiscal. No como fuente de rendimiento.
