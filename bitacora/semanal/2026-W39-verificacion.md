# Acta de verificación semanal 2026-W39

- **Fecha:** 25-sep-2026. **Rol:** fact-checker (supuesto de partida: hay errores hasta probar lo contrario).
- **Alcance:** tres afirmaciones agregadas esta semana en `bitacora/decisiones/2026-09-25-CARTERA-inicial.md` y `bitacora/briefs/2026-09-25.md` §2.
- **Resultado:** 9 elementos revisados; 6 confirmados, 3 corregidos, 0 eliminados. Filas nuevas en `conocimiento/registro-de-errores.md`.

## 1. Bono de 10 años y sensibilidad del S&P

### 1a. "Bono de 10 años en ~5.18% (máximo desde 2007)": **confirmada**
- FRED DGS10 (base estadística, dato del 24-sep-2026; el del 25-sep aún no se publica): **5.18%**, máximo de 2026.
- Último dato ≥ 5.18% antes de 2026: **6-jul-2007 (5.19%)**. El máximo de 2023 fue 4.98% (19-oct-2023).
- Acceso: serie completa, https://fred.stlouisfed.org/series/DGS10.

### 1b. "Cada +100 pb del bono restó 7.9% al S&P en 2026": **corregida**
Cálculo propio. Datos: FRED DGS10 y SP500, del 2-ene al 24-sep-2026 (n = 183 días con ambos datos). Pendiente de log(S&P) contra el rendimiento en pp:

| Especificación | Pendiente por +100 pb | t | R² | n |
|---|---|---|---|---|
| Niveles diarios (NW 20) | **+18.2%** (signo invertido) | +7.3 | 0.61 | 183 |
| Cambios diarios (NW 5) | −8.1% | −4.8 | 0.19 | 182 |
| Cambios semanales, viernes (NW 4) | −6.2% | −1.6 | 0.12 | 38 |
| Cambios semanales, miércoles (NW 4) | −8.7% | −3.1 | 0.12 | 38 |
| Cambios mensuales (White) | −3.6% | −0.7 | 0.03 | 8 |
| Punta a punta 2026 | bono +99 pb, S&P **+12.3%** | – | – | – |

- **Conclusión:** el −7.9% se aproxima a la beta de cambios diarios (−8.1%), pero no es un efecto realizado ("restó"). En 2026 los dos subieron juntos. En frecuencia semanal la cifra depende del día de corte y en mensual no es significativa. En niveles, la relación es espuria por tendencia.
- **Texto corregido en sitio:** "sensibilidad de alta frecuencia de −6% a −9% por +100 pb; no es efecto acumulado". Grado C.
- Script: `scratchpad/r1b.py` de la sesión (OLS con Newey-West en numpy). Descarga: `fredgraph.csv?id=DGS10` e `id=SP500`.

## 2. P(−12%) de la cartera A: **corregida (comparación entre métodos)**

- **Re-ejecución** de `arena/modelos/cartera_inicial_simulacion.py` (20,000 trayectorias, semilla 20260925, 54 s): reproduce `salida_cartera_inicial.txt` con diferencias de 0.1 pp o menos. La única entrada que cambió fue DTB3: 4.04% → 4.08%, por la publicación del 24-sep.
- **P(tocar −12%) de la cartera A, 85 días:**

| Método | Sin stops | Con stops (st3) |
|---|---|---|
| M1 bootstrap 2011-2026, régimen de hoy | 5.6% | **3.4%** |
| M2 deriva conservadora | 8.9% | 4.5% |
| M3 ventanas 1999-2026 | **15.2%** | 4.7% |
| M3 antes de 2016-03 | **16.7%** | – |
| M3c régimen de hoy | 6.5% | 2.9% |

- **Error:** el documento compara el 3% (M1 con stops) contra el 15-17% (M3 sin stops). Así mezcla el efecto del método con el de los stops. Con el mismo método, los stops reducen la probabilidad de 1.6 a 3.2 veces, no 5. Sin stops, el rango honesto es **6-15%**.
- **Recálculo independiente** (código propio, comprar y mantener 56.3% SPY y 27.1% QQQ en MXN vía DEXMXUS, más 16.6% a 6.15%, sin cortacircuitos): 16.4% (6,700 ventanas, 2000-2026) y 9.1% (2011-2026). GBM paramétrico con μ = 6%: σ 12% da 6.5%, σ 14.8% da 16.8% y σ 18% da 31%. Las cifras de M3 se reproducen, pero la probabilidad es muy sensible a la vol supuesta.
- **Supuestos:**
  - *Vol:* M1 y M3c condicionan al régimen de vol baja actual (vol 60 d de SPY en MXN 9.7%, frente a 19% de largo plazo), lo que es razonable pero optimista. M3 incluye 2000-02 y 2008. Hay que reportar el rango, no el punto.
  - *Correlación:* el bootstrap conjunto conserva SPY-QQQ (0.85) y S&P-USD/MXN (−0.30). Es adecuado.
  - *Horizonte:* 85 días hábiles de NYSE (28-sep a 28-ene) es correcto. Pero el criterio de refutación dice "al 28-dic-2026" (64 días): no coincide con el modelo.
  - *FX:* se toma la historia conjunta; M2 usa deriva cero. No se modela la reversión después del +4% del mes. Es razonable.
  - *Stops:* se ejecutan al cierre, sin hueco intradía ni iliquidez en el SIC, así que el número con stops es optimista. El propio documento lo reconoce.
- **Corrección en sitio:** nota fechada bajo el criterio de refutación.

## 3. Brief §2: macro

| Afirmación | Veredicto | Evidencia (tipo, acceso) |
|---|---|---|
| Fed 16-sep: +25 pb a 3.75-4.00%, voto 12-0 | **Confirmada** | Comunicado del FOMC, lectura íntegra: "approved ... by a 12–0 vote ... raise the target range ... by 1/4 percentage point to 3-3/4 to 4 percent". https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm (reporte narrativo) |
| 16 de 18 esperan otra alza en 2026 | **Confirmada** | SEP, Figura 2: en 2026 hay 4 participantes en 4.375, 12 en 4.125 y 2 en 3.875 (el punto medio actual), es decir, 16 de 18 por arriba. https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm (base estadística, tabla completa) |
| CPI agosto 3.4% a/a general, 2.4% subyacente (julio 2.5%), +0.4 y +0.3 m/m, energía +16.3% | **Confirmada** | BLS, resumen del comunicado del 11-sep (https://www.bls.gov/news.release/cpi.nr0.htm; curl directo dio 403, se leyó el resumen por otra vía). Cotejo con FRED (BLS, base estadística): CPIAUCSL m/m +0.40%, a/a SA 3.35%; CPILFESL m/m +0.29%, a/a SA 2.45% (la cifra oficial NSA es 2.4); CPIENGNS a/a +16.28% |
| Banxico 24-sep: 6.50%, por unanimidad, 3.ª pausa | **Confirmada** | Comunicado de Banxico (PDF, lectura íntegra): "decidió por unanimidad mantener ... en 6.50%". Índice de anuncios: se mantuvo el 25-jun, el 6-ago y el 24-sep. INPC de la 1.ª quincena de septiembre 3.42% (subyacente 3.79%); meta en el 4T-2027. https://www.banxico.org.mx/publicaciones-y-prensa/anuncios-de-las-decisiones-de-politica-monetaria/anuncios-politica-monetaria-t.html |
| Peso −4.3% en septiembre | **Corregida** | FRED DEXMXUS: 31-ago 17.0081; USD/MXN 16:00 NY del 25-sep 17.7093. En el mes, peso −3.96% (USD +4.12%). −4.38% es el cambio a 1 mes (desde el 25-ago, 16.9331). No se consultó el FIX de Banxico (el SIE pide token) |

Aparte: "primera alza desde 2023" no está en el comunicado. Es coherente con la historia conocida (última alza el 26-jul-2023), pero no se verificó hoy contra fuente primaria.

## Veredicto de confiabilidad
- **Brief §2: alta.** Los hechos de Fed, BLS y Banxico coinciden con la fuente primaria. Un error menor de etiqueta en el peso.
- **Decisión de cartera: media.** Las cifras se reproducen, pero dos se presentaron fuera de contexto: una beta diaria descrita como efecto acumulado, y probabilidades comparadas entre métodos distintos. La elección de A no cambia: A sigue siendo la de menor riesgo entre las candidatas con cualquier método.
