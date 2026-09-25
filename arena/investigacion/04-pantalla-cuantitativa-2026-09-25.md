# Pantalla cuantitativa de momentum en MXN

**Fecha:** 2026-09-25 · **Tarea:** A4 · **Cuenta:** `arena-claude` (20,000 MXN, perfil `arena_agresivo` PROVISIONAL)
**Datos:** cierres al **24-sep-2026** (última sesión completa de EUA). Fuente de precios: Yahoo Finance chart v8 [1].
**Archivos:** script `arena/investigacion/pantalla.py` · resultados `arena/investigacion/pantalla-2026-09-25.csv` (68 filas, 34 columnas).
**Disponibilidad en el SIC:** se confirma en A2 (`02-universo-sic-bmv-agresivo.md`). Esta pantalla mide el comportamiento del precio. No dice qué se puede comprar.

**Convenciones**
- **[H]** Hecho con fuente y fecha.
- **[C]** Cálculo propio con datos que tienen fuente. El método está en la sección 1.
- **[I]** Inferencia.
- **[R]** Recomendación para la cuenta arena.

---

## Resumen ejecutivo

1. **[C] El régimen es alcista en renta variable de EUA.** 46 de 68 instrumentos (68%) están arriba de su SMA200 en MXN. Lo están los 5 ETFs de índices de EUA y 10 de los 12 sectoriales.
2. **[C] Top 5 por momentum compuesto con filtro de tendencia:** AMD, TECL, MU, SPXL y GMEXICOB. 14 de los 20 primeros son semiconductores, tecnología o apalancados sobre índices de EUA.
3. **[C] El liderazgo es una sola apuesta.** La correlación diaria a 60 días (en MXN) entre AMD, MU, TECL, TQQQ y SOXL va de 0.67 a 0.95.
4. **[C] Hay dos bloques en tendencia con poca correlación con los semis:**
   - Metales (GMEXICOB, COPX, GDX): 12-1 de +33% a +70%, pero con 1m negativo.
   - Defensivos y energía (LLY, XLV, XLE): correlación de −0.14 a −0.57 con los semis.
5. **[C] Abajo de la tabla quedan los activos sensibles a tasas y los perdedores del ciclo:** TLT, XLU, KWEB, COST, WALMEX, ORCL (−57% en 12-1), NFLX, UBER y URA.
   - [H] Contexto: el bono del Tesoro a 10 años está en 5.11%, su máximo de 12 meses [2]. La Fed subió 25 pb el 16-sep [3].
6. **[C] Efecto del peso.** El USD/MXN cerró en 17.72 al cierre de EUA del 24-sep, con +4.5% en un mes. Eso agrega ~4.5 pp al retorno de 1m en MXN de todo activo en USD. A 6 meses el efecto cambiario es casi cero (−0.4%).
7. **[C] El filtro de apalancados de `parametros.json` se cumple hoy para los 7 apalancados del universo:** su subyacente está arriba de la SMA200 y el VIX cerró en 15.67 (el límite es 25) [1].
8. **[C] Varios líderes no caben en el SIC.** Sin fracciones, un solo título de AMD es el 56% de la cuenta, uno de MU el 96% y uno de LLY el 105%. Los tres rompen el tope de 30% por acción. Los vehículos de tecnología o de índice de EUA del top con un título ≤30% de la cuenta son TECL, TQQQ, QLD, SOXL, XLK, NVDA y AAPL (esta última justo en el límite), más SPXL (S&P 500, no tecnología; 25%). SOXX (49%) y SMH (53%) quedan bajo `etf_indice_max` = 0.6, pero un título es media cuenta.
9. **[C] Hallazgo técnico.** En Yahoo, la vela diaria de `MXN=X` fechada *d* es el tipo de cambio de ~23:00 UTC de *d−1*. Usarla con cierres de EUA atrasa el tipo de cambio un día. Por eso la pantalla usa velas horarias al cierre de Nueva York. `herramientas/portafolio.py` y `tablero.py` usan la vela diaria y hay que revisarlos.
10. **[R] Insumo para la estrategia (no es una orden):**
    - Una pierna de momentum tecnológico en un solo vehículo apalancado: TECL o TQQQ, o SPXL si se quiere menos volatilidad.
    - 1 o 2 piernas en tendencia y con baja correlación: XLE, XLV, GDX o COPX.
    - Histéresis de ranking, para no pasar de 8 operaciones al mes.

---

## 1. Metodología

### 1.1 Datos
- **[H] Precios.** Endpoint `https://query1.finance.yahoo.com/v8/finance/chart/<TICKER>?range=2y&interval=1d`, con User-Agent `Mozilla/5.0`, una pausa de 1 s entre solicitudes y reintentos si hay un 429 [1]. Se usa el cierre ajustado (`adjclose`, que incluye splits y dividendos) cuando existe. La descarga pasa por `herramientas/datos.py` (`yahoo_grafica`), con caché de 6 h.
- **Universo:** 68 instrumentos.
  - 42 ETFs: 5 de índices de EUA, 12 sectoriales, 1 temático, 7 internacionales, 6 de materias primas, 3 de bonos, 1 de cripto y 7 apalancados.
  - 19 acciones de EUA o ADRs.
  - 7 emisoras de la BMV (`.MX`).
  - Los 68 tuvieron datos completos. Hubo 0 errores de descarga.
- **Corte:** 2026-09-24, la última sesión de SPY. No se usa ningún dato posterior al corte.

### 1.2 Conversión a MXN y el problema del tipo de cambio diario
- **[C] Hallazgo.** Comparé las velas diarias de `MXN=X` con sus velas horarias (rango de 1 mes, intervalo de 1 h). En las 23 velas diarias del 25-ago al 24-sep-2026, la apertura y el cierre difieren menos de 0.1%. En las de martes a viernes, ese valor coincide (±0.1%) con la vela horaria de las 23:00 UTC del día previo. O sea, la vela diaria fechada *d* es una foto de ~23:00 UTC de *d−1*, el inicio del día de Londres [1].
  - Ejemplo: la vela diaria del 24-sep marca 17.5413. La vela horaria de las 23:00 UTC del 23-sep cerró en 17.5419. Al cierre de EUA del 24-sep (vela de 19:00 UTC) el tipo de cambio ya estaba en 17.7188.
- **[C] Consecuencia.** Si se multiplica el cierre de EUA del día *d* por la vela diaria *d*, se usa el tipo de cambio del día anterior. Los niveles cambian hasta ~1% en días como el 24-sep. La volatilidad en MXN también sale sesgada, porque se pierde la correlación del mismo día entre el peso y el riesgo. Ejemplo con SPY: vol 60d en MXN de 12.9% con la vela diaria contra 9.4% con la horaria.
- **Solución en `pantalla.py`:** USD/MXN a las 16:00 de Nueva York, tomado del cierre de la vela horaria de las 15:00 a las 16:00 NY. Se descargan 2 años de velas de 1 h. Si falta esa vela, se usa la última vela horaria de las 6 horas previas; si tampoco hay, la vela diaria de *d+1* (la foto de ~23:00 UTC de *d*, unas 3 h después del cierre de EUA). Las series `.MX` ya están en MXN y no se convierten.
  - [C] Auditoría del 25-sep (verificación): hasta el corte, 519 días usan la vela exacta, 3 usan la vela previa (anterior al cierre) y **0** usan el respaldo diario de *d+1*. No hay dato cambiario posterior al cierre de EUA en esta corrida.
- **[C] Validación cruzada del tipo de cambio.** Dividí el precio BMV del 24-sep entre el precio de EUA:
  - AMD: 11,139 / 629.26 = 17.70
  - MU: 19,126 / 1,080.53 = 17.70
  - LLY: 20,970 / 1,181.89 = 17.74
  - XLV: 3,023 / 169.87 = 17.80

  Precios BMV de [16]. El tipo de cambio horario que usa la pantalla es 17.72 [1]. A2 reporta un tipo de cambio implícito SPY BMV/EUA de 17.75 [A2].
- **[C] Validación cruzada de precios.** Los retornos a 6m en USD de la pantalla coinciden con los de A2, que usa StockAnalysis y S&P Global como fuente:

  | Instrumento | Pantalla | A2 |
  |---|---|---|
  | TQQQ | +81.2% | +81.2% |
  | QLD | +53.6% | +53.6% |
  | SPXL | +52.7% | +52.7% |
  | SSO | +34.4% | +34.4% |
  | SOXL | +166.4% | +166.4% |
  | SOXX | +66.2% | +66.2% |
  | QQQ | +27.2% | +27.2% |
  | SPY | +18.0% | +18.0% |
  | XLK | +43.3% | +43.3% |
  | TECL | +144.3% | +144.1% |

### 1.3 Métricas (todas sobre la serie en MXN)
| Métrica | Definición |
|---|---|
| 1m, 3m, 6m | P(t) / P(t − n meses calendario) − 1, con el último cierre ≤ la fecha objetivo |
| 12-1 | P(t − 1m) / P(t − 12m) − 1. Omite el último mes, convención estándar del momentum 12-1 (no verifiqué aquí la fuente primaria de la reversión de 1 mes) |
| Vol 60d | Desviación estándar de 60 rendimientos log diarios × √252 |
| vs SMA200 | P / promedio de los últimos 200 cierres − 1. También se reporta en moneda local (columna `dist_sma200_local`) |
| DD máx 1a | Caída máxima de pico a valle dentro de los últimos 12 meses |
| vs máx 52s | P / máximo de 12 meses − 1 |
| 6m/vol | Retorno 6m / vol 60d (ratio simple, sin tasa libre de riesgo) |

### 1.4 Ranking
- **Momentum compuesto (Score)** = promedio de los rangos de 3m, 6m y 12-1 sobre los 68 instrumentos. El rango 1 es el mejor y los empates reciben rango promedio. Un Score menor es mejor.
- **Filtro de tendencia:** P > SMA200 en MXN. El "Top 20" usa solo los que pasan el filtro. El "Bottom 10" usa el universo completo.
- Base académica:
  - Momentum de sección cruzada a 3-12 meses [10] y por industria [11].
  - Momentum de serie de tiempo [12].
  - Filtro de media móvil de 10 meses (≈ SMA200) como regla de tendencia [14].
  - Riesgo de *momentum crash* [13].

### 1.5 Limitaciones
- **[I] Sesgo de selección.** El universo se eligió hoy con nombres conocidos. La pantalla describe el presente y no es un backtest.
- **[I] Los apalancados y su subyacente cuentan por separado.** Hay tres vehículos sobre el S&P 500 (SPXL, UPRO y SSO), dos sobre el Nasdaq-100 (TQQQ y QLD) y tres sobre semis (SOXL, SOXX y SMH). Eso infla la presencia de estas exposiciones en el top. El apalancamiento sube los retornos en tendencia y, por construcción, sube su rango.
- **[C] El filtro en MXN puede cambiar solo por el peso.** XLI (+0.4% en MXN y −1.2% en USD), XLP (+0.6% y −1.0%) y HYG (+1.1% y −0.4%) pasan el filtro en MXN y no en USD. El `filtro_apalancados` de `parametros.json` se evalúa sobre el subyacente en moneda local.
- **Datos:** NAFTRAC.MX tiene último dato del 23-sep en Yahoo, un día de rezago. `adjclose` incluye dividendos brutos. En el SIC, el dividendo neto es menor por las retenciones (ver `01`).
- **Reproducir:** `python3 arena/investigacion/pantalla.py --salida arena/investigacion/pantalla-AAAA-MM-DD.csv --markdown`. Tarda ~2 min por la pausa de 1 s entre 70 descargas (68 series + 2 de tipo de cambio). Opciones: `--corte AAAA-MM-DD` y `--cache-horas 0`.

---

## 2. Contexto de mercado al corte

| Variable | Valor | Referencia | Fuente |
|---|---|---|---|
| USD/MXN al cierre de EUA | **17.72** (24-sep) | 1m +4.5% · 3m +0.5% · 6m −0.4% · 12m −3.9% (hace 12m: 18.43) | [C][1] |
| USD/MXN interbancario, cierre de agosto | 16.9971 | Contra 17.6380 del 24-sep a media sesión: "una depreciación cercana a 3.8%". FIX: 17.2203 (21-sep) y 17.5030 (23-sep) | [H][5] |
| Bono del Tesoro de EUA a 10 años | **5.11%** (23-sep) | 4.47% el 1-jun-2026; 4.15% el 22-sep-2025; máximo de 12 meses | [H][2] |
| Bono del Tesoro de EUA a 2 años | 4.85% (23-sep) | 4.05% el 1-jun-2026 | [H][2] |
| Fed funds efectiva | 3.88% (desde el 17-sep) | 3.63% antes (sin cambio del 25-jul al 16-sep) | [H][2] |
| Fed (FOMC 16-sep-2026) | +25 pb a **3.75%–4.00%**, votación 12-0 | "Inflation remains elevated." | [H][3] |
| Banxico (24-sep-2026) | Mantuvo **6.50%**, por unanimidad | La política "no tendría que reaccionar de manera mecánica ante los ajustes previstos a la tasa de fondos federales" | [H][4] |
| Bono del Tesoro de EUA a 30 años / petróleo | 5.46% ("su nivel más alto desde 2004"); WTI 93.69 USD y Brent 105.15 USD | Nota de prensa del 24-sep, 11:25 (dato intradía). FRED DGS30 del 23-sep: 5.40% [2] | [H][5] |
| VIX | **15.67** (24-sep) | Máximo de 12 meses: 31.05 al cierre (27-mar-2026); 35.30 intradía | [H][1] |
| S&P 500 | 7,704.13 | −1.2% contra su máximo de 12 meses (7,798.99) | [C][1] |
| Índice de semiconductores (^SOX) | 12,492.54 | −14.6% contra su máximo de 12 meses (14,634.72) | [C][1] |
| S&P/BMV IPC | 64,264.16 | −10.2% contra su máximo de 12 meses (71,601.35) | [C][1] |
| Bitcoin (BTC-USD) | 84,383 (23-sep; la vela del 24-sep viene vacía en Yahoo) | −32.4% contra su máximo de 12 meses al cierre (124,752.5, 6-oct-2025) | [C][1] |
| DXY | 101.29 (24-sep) | −0.3% contra su máximo de 12 meses al cierre (101.61, 24-jun-2026) | [C][1] |

---

## 3. Top 20 con filtro de tendencia (P > SMA200 en MXN)

Retornos en MXN. "1 título ≈ % de 20k" usa el precio BMV cuando está verificado (A2 o [16]). Con `*` es una estimación: precio en EUA × 17.72.

| # | Ticker | Qué es | 1m | 3m | 6m | 12-1 | Vol 60d | vs SMA200 | DD máx 1a | vs máx 52s | 6m/vol | Score | 1 título ≈ % de 20k | SIC (se confirma en A2) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | AMD | Semis | +44.0% | +21.7% | +205.2% | +161.2% | 67% | +76.9% | −31.2% | +0.0% | 3.04 | 3.7 | **56%** | Sí: cotizó en BMV a 11,139 MXN [16] |
| 2 | TECL | 3x tecnología | +30.2% | +11.9% | +143.3% | +50.0% | 81% | +47.9% | −47.6% | −13.9% | 1.77 | 10.0 | 20% | Sí [A2] |
| 3 | MU | Semis (memoria) | +24.0% | +3.6% | +172.3% | +418.8% | 78% | +67.9% | −39.2% | −9.8% | 2.20 | 12.7 | **96%** | Sí: 19,126 MXN [16] |
| 4 | SPXL | 3x S&P 500 | +5.7% | +12.3% | +52.1% | +26.6% | 30% | +18.5% | −27.1% | −0.9% | 1.72 | 12.7 | 25% | Sí [A2] |
| 5 | GMEXICOB | Minería y cobre (BMV) | −6.1% | +13.3% | +23.1% | +70.2% | 31% | +10.7% | −21.1% | −6.3% | 0.74 | 13.7 | 1% (220.98 MXN, BMV en Yahoo) | Sí (emisora local) |
| 6 | UPRO | 3x S&P 500 | +5.5% | +11.9% | +51.3% | +26.0% | 30% | +18.2% | −27.2% | −1.1% | 1.69 | 14.0 | 13%* | **No verificado** [A2] |
| 7 | TQQQ | 3x Nasdaq-100 | +19.2% | +8.0% | +80.5% | +25.9% | 56% | +27.8% | −38.2% | −7.3% | 1.43 | 14.7 | 7% | Sí [A2] |
| 8 | COPX | Mineras de cobre | −4.6% | +14.9% | +18.1% | +59.7% | 39% | +7.0% | −24.7% | −7.0% | 0.46 | 15.3 | 8% | Sí, baja liquidez [A2] |
| 9 | AAPL | Hardware | +13.1% | +15.3% | +33.2% | +13.6% | 29% | +19.0% | −17.6% | +0.0% | 1.15 | 18.0 | 30%* | Sí [A2] |
| 10 | SSO | 2x S&P 500 | +5.5% | +8.7% | +33.8% | +16.8% | 19% | +13.9% | −18.5% | +0.0% | 1.75 | 18.3 | 6%* | **No verificado** [A2] |
| 11 | QLD | 2x Nasdaq-100 | +14.5% | +6.9% | +53.0% | +19.3% | 37% | +21.6% | −26.5% | −1.9% | 1.42 | 18.7 | 8% | Sí, muy poco operado [A2] |
| 12 | XLK | Tecnología | +13.1% | +7.1% | +42.8% | +19.4% | 26% | +21.6% | −17.5% | +0.0% | 1.62 | 18.7 | 17% | Sí [A2] |
| 13 | LLY | Farmacéutica | −0.9% | +6.5% | +30.8% | +55.6% | 32% | +12.7% | −26.7% | −3.4% | 0.95 | 18.7 | **105%** | Sí: 20,970 MXN [16] |
| 14 | GDX | Mineras de oro | −6.8% | +24.5% | +10.2% | +32.7% | 44% | +3.3% | −38.3% | −18.1% | 0.23 | 19.3 | 8% | Sí, baja liquidez [A2] |
| 15 | TSM | Semis (ADR) | +15.3% | +3.2% | +31.6% | +35.5% | 36% | +20.6% | −21.6% | −4.0% | 0.88 | 21.7 | 40%* | **No verificado** [A2] |
| 16 | XLE | Energía | +4.3% | +18.2% | +3.8% | +31.4% | 23% | +15.0% | −17.9% | −1.3% | 0.17 | 21.7 | 6% | Sí [A2] |
| 17 | SOXX | Semiconductores | +16.9% | −5.3% | +65.5% | +73.5% | 48% | +29.0% | −28.6% | −11.8% | 1.36 | 22.0 | 49% | Sí [A2] |
| 18 | SMH | Semiconductores | +14.8% | −2.5% | +51.6% | +57.1% | 40% | +24.2% | −24.2% | −8.4% | 1.29 | 22.3 | 53% | Sí [A2] |
| 19 | XLV | Salud | +2.0% | +11.8% | +17.8% | +19.4% | 20% | +11.5% | −15.0% | +0.0% | 0.90 | 22.7 | 15% | Sí: 3,023 MXN [16] |
| 20 | NVDA | Semis | +12.7% | +13.6% | +28.0% | +8.5% | 37% | +14.8% | −21.8% | −1.8% | 0.75 | 23.7 | 20%* | Sí [A2] |
| *21* | *SOXL* | *3x semiconductores* | *+37.7%* | *−35.9%* | *+165.4%* | *+199.0%* | *147%* | *+30.6%* | *−69.3%* | *−50.3%* | *1.12* | *24.3* | *13%* | *Sí [A2]* |

Lectura rápida [C]:
- **Top 1x (sin apalancados):** AMD, MU, GMEXICOB, COPX, AAPL, XLK, LLY, GDX, TSM, XLE, SOXX, SMH, XLV y NVDA (14 de los 20).
- **Mejor 6m/vol entre los filtrados:** AMD 3.04, MU 2.20, SPY 1.87, VOO 1.84, TECL 1.77, SSO 1.75, SPXL 1.72, UPRO 1.69 y XLK 1.62.
- **Posiciones 22 a 27:** ARKK, MSFT, PLTR, ASML, IGV y META. Salvo ASML (3m −1.6%, 12-1 +70%), todos tienen 3m fuerte y 12-1 negativo: PLTR +71% / −10%, META +40% / −32%, MSFT +37% / −11%, IGV +25% / −18% y ARKK +20% / −7%. Son **rebotes**, no tendencias de 12 meses, y el Score los castiga.
- **SOXL:** 6m de +165% pero 3m de −36%, por el desplome de julio documentado en A2. Tiene vol de 147% y está a −50% de su máximo. Su subyacente SOXX está a −11.8%.

---

## 4. Bottom 10 (universo completo, sin filtro)

| # general | Ticker | Qué es | 1m | 3m | 6m | 12-1 | Vol 60d | vs SMA200 | DD máx 1a | vs máx 52s | 6m/vol | Score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 59 | AMXB | Telecom (BMV) | −3.1% | −13.8% | −10.1% | +9.8% | 18% | −6.2% | −18.5% | −17.1% | −0.57 | 53.7 |
| 60 | COST | Consumo básico | −3.6% | −6.1% | −8.0% | −4.9% | 22% | −4.9% | −19.7% | −16.4% | −0.36 | 55.7 |
| 61 | KWEB | Internet China | −1.7% | +2.1% | −13.0% | −38.4% | 25% | −15.0% | −44.6% | −41.3% | −0.53 | 56.7 |
| 62 | TLT | Bonos del Tesoro de EUA 20+ años | +0.9% | −7.6% | −5.9% | −11.1% | 9% | −4.3% | −15.8% | −13.6% | −0.65 | 58.0 |
| 63 | UBER | Plataformas | −8.8% | −5.8% | −4.7% | −25.4% | 36% | −6.6% | −37.5% | −33.5% | −0.13 | 59.0 |
| 64 | NFLX | Medios | −6.3% | +0.4% | −21.4% | −38.9% | 38% | −14.2% | −48.5% | −44.5% | −0.57 | 59.0 |
| 65 | XLU | Servicios públicos | −4.1% | −12.5% | −11.9% | −5.9% | 15% | −8.9% | −16.6% | −16.4% | −0.80 | 59.3 |
| 66 | URA | Uranio | −6.5% | −8.2% | −15.5% | −9.4% | 41% | −13.9% | −38.3% | −31.9% | −0.38 | 60.3 |
| 67 | ORCL | Software y nube | +2.4% | −10.6% | −4.8% | −57.0% | 53% | −13.7% | −64.8% | −56.7% | −0.09 | 63.0 |
| 68 | WALMEX | Comercio (BMV) | −1.9% | −10.8% | −18.2% | −15.2% | 20% | −14.2% | −27.1% | −25.9% | −0.91 | 63.3 |

También están abajo de su SMA200 (en MXN): GLD, IAU, SLV, EWW, NAFTRAC, FXI, INDA, IEF, AVGO, TSLA, XLY y CEMEX.

---

## 5. Categorías y sectores

**Medianas por categoría (MXN), ordenadas por Score mediano [C]**

| Categoría | N | 3m | 6m | 12-1 | Vol 60d | % sobre SMA200 | Score mediano |
|---|---|---|---|---|---|---|---|
| Apalancados | 7 | +8.7% | +53.0% | +26.0% | 37% | 100% | 14.7 |
| Temático (ARKK) | 1 | +20.2% | +32.4% | −7.5% | 35% | 100% | 24.3 |
| Acciones EUA | 19 | +3.2% | +23.0% | +6.6% | 38% | 68% | 28.3 |
| Cripto (IBIT) | 1 | +41.9% | +21.2% | −36.2% | 37% | 100% | 30.7 |
| Materias primas | 6 | +9.8% | −3.4% | +23.6% | 37% | 33% | 32.0 |
| Sectoriales EUA | 12 | +0.2% | +7.4% | +6.8% | 21% | 83% | 33.8 |
| Índices EUA | 5 | +4.9% | +17.6% | +7.8% | 10% | 100% | 35.0 |
| Internacional | 7 | +2.1% | +1.2% | +8.9% | 17% | 43% | 42.0 |
| BMV | 7 | −2.7% | −0.5% | +14.1% | 22% | 43% | 45.7 |
| Bonos | 3 | −3.8% | −3.9% | −8.1% | 6% | 33% | 53.7 |

**ETFs de índices y sectoriales de EUA, por rango general [C]**

| Rango | ETF | Sector | 3m | 6m | 12-1 | Sobre SMA200 |
|---|---|---|---|---|---|---|
| 12 | XLK | Tecnología | +7.1% | +42.8% | +19.4% | Sí |
| 16 | XLE | Energía | +18.2% | +3.8% | +31.4% | Sí |
| 17 | SOXX | Semiconductores | −5.3% | +65.5% | +73.5% | Sí |
| 18 | SMH | Semiconductores | −2.5% | +51.6% | +57.1% | Sí |
| 19 | XLV | Salud | +11.8% | +17.8% | +19.4% | Sí |
| 26 | IGV | Software | +25.0% | +32.1% | −18.2% | Sí |
| 30 | QQQ | Nasdaq-100 | +4.9% | +26.7% | +9.4% | Sí |
| 36 / 40 | VOO / SPY | S&P 500 | +5.5% / +5.4% | +17.6% | +7.2% / +7.1% | Sí |
| 43 | IWM | Russell 2000 | −4.3% | +13.3% | +14.3% | Sí |
| 44 | DIA | Dow Jones | −0.3% | +11.5% | +7.8% | Sí |
| 45 | XLF | Financiero | +2.4% | +11.0% | +1.1% | Sí |
| 46 | XLC | Comunicaciones | +7.9% | +2.8% | −11.2% | Sí |
| 48 | XLI | Industrial | −5.6% | +3.1% | +9.1% | Sí (solo en MXN) |
| 50 | XLP | Consumo básico | −2.1% | +1.7% | +4.6% | Sí (solo en MXN) |
| 54 | XLY | Consumo discrecional | −3.4% | +0.6% | −8.6% | No |
| 65 | XLU | Servicios públicos | −12.5% | −11.9% | −5.9% | No |

**Correlación diaria de rendimientos log en MXN, 60 sesiones (26-jun a 24-sep-2026) [C]**

|  | AMD | MU | TECL | TQQQ | SPXL | SOXL | GMEX | COPX | GDX | XLE | XLV | LLY |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AMD | 1 | 0.77 | 0.82 | 0.77 | 0.51 | 0.88 | 0.33 | 0.50 | 0.16 | −0.20 | −0.54 | −0.44 |
| MU | | 1 | 0.78 | 0.67 | 0.38 | 0.85 | 0.34 | 0.51 | 0.33 | −0.14 | −0.38 | −0.29 |
| TECL | | | 1 | 0.95 | 0.74 | 0.94 | 0.41 | 0.55 | 0.29 | −0.39 | −0.51 | −0.40 |
| TQQQ | | | | 1 | 0.88 | 0.86 | 0.41 | 0.52 | 0.26 | −0.48 | −0.41 | −0.34 |
| SPXL | | | | | 1 | 0.58 | 0.32 | 0.38 | 0.24 | −0.53 | −0.15 | −0.16 |
| SOXL | | | | | | 1 | 0.40 | 0.55 | 0.27 | −0.32 | −0.57 | −0.43 |
| GMEX | | | | | | | 1 | 0.77 | 0.60 | −0.31 | −0.20 | −0.16 |
| COPX | | | | | | | | 1 | 0.72 | −0.30 | −0.29 | −0.17 |
| GDX | | | | | | | | | 1 | −0.37 | 0.03 | 0.05 |
| XLE | | | | | | | | | | 1 | 0.11 | 0.15 |
| XLV | | | | | | | | | | | 1 | 0.85 |

Otros valores [C]:
- NVDA: 0.39 a 0.64 con los semis y apalancados de tecnología (AMD, MU, TECL, TQQQ, SOXL); 0.51 con SPXL.
- AAPL: −0.22 a −0.32 con los mismos y −0.26 con NVDA; −0.06 con SPXL. AAPL es líder, pero no forma parte del bloque de semis.
- IBIT: −0.38 (con XLE) a 0.44 (con GDX) con el resto; 0.09 a 0.27 con semis, apalancados y NVDA.
- TLT: −0.38 con XLE y +0.42 con XLV.

---

## 6. Observaciones de régimen

**Hechos que explican a los líderes**
- [H] **Hardware de IA.**
  - AMD llegó a 1 billón de USD de valor de mercado el 21-sep-2026, con "shares surging 9.6% to a record $613.50" [6].
  - MU: la nota del 23-sep atribuye el alza a la escasez de memoria: "Micron has sold out its entire 2026 production of high bandwidth memory" [7]. La misma nota (fechada 23-sep, actualizada 25-sep) dice que MU cerró arriba de 1,000 USD "for the first time on September 22, 2026". Ese dato no cuadra: en Yahoo, MU cerró en 1,035.50 el 1-jun-2026 (cierre nominal; 1,035.34 ajustado) y volvió a cerrar arriba de 1,000 el 18-sep (1,015.80), antes del 22-sep [1].
  - **Micron reporta su cuarto trimestre fiscal el miércoles 30-sep-2026**, con llamada a las 2:30 p.m. hora de la Montaña, después del cierre [17].
- [H] **META** subió 11% en un día por su agente Muse, lanzado el 8-sep [8]. En Yahoo, el salto fue el 21-sep: +11.3%, de 665.75 a 741.25 USD [1]. En la pantalla tiene 1m de +45%, 3m de +40% y 12-1 de −32%, así que queda en el lugar 27.
- [H] **Tasas al alza.**
  - La Fed subió a 3.75%–4.00% el 16-sep [3].
  - El bono del Tesoro a 10 años está en 5.11% [2] y el de 30 años en 5.46%, "su nivel más alto desde 2004" [5].
  - Banxico se quedó en 6.50% [4]. [I] Con la Fed subiendo y Banxico quieto, el diferencial de tasas se estrecha. La prensa cita la expectativa de una Fed más restrictiva y el alza de los rendimientos del Tesoro entre las causas de la caída del peso [5].
- [H] **ORCL.** La prensa liga su caída al costo de la deuda con la que financia sus centros de datos de IA: "Higher rates mean Oracle's debt expenses could climb higher than they already are" [9].

**Lectura de la pantalla**
- [C] **Qué lidera:**
  - Semiconductores y tecnología: XLK, SOXX, SMH, AMD, MU, TSM y NVDA.
  - Metales: cobre (GMEXICOB, COPX) y mineras de oro (GDX).
  - Energía (XLE, +18% en 3m) y salud (XLV, LLY).
- [C] **Qué se rezaga:**
  - Duración: TLT, IEF y XLU.
  - Consumo: XLY, COST y WALMEX.
  - China: KWEB y FXI.
  - México doméstico: WALMEX, AMX, CEMEX y NAFTRAC bajo su SMA200.
  - Uranio (URA) y oro físico (GLD e IAU, −4.4% bajo su SMA200 en MXN y −5.9% en USD).
- [I] **El patrón corresponde a una expansión con tasas al alza.** Ganan el capex de IA y los productores de materias primas. Pierden los activos de duración larga y el consumo. Es coherente con el comunicado del FOMC: "Economic activity is expanding at a solid pace… capital investment is robust" [3].
- [I] **Por industria [11].** El momentum de acciones se explica en buena parte por el de su industria. Aquí, AMD, MU, TSM y NVDA van con SOXX/SMH. Por eso un vehículo sectorial (TECL, SOXL o TQQQ) captura casi todo el efecto sin el riesgo idiosincrático, y además cabe en la cuenta.
- [I] **Riesgo de "momentum crash" [13].** Daniel y Moskowitz encuentran que los crashes de momentum ocurren en estados de "pánico": después de caídas del mercado, con volatilidad alta y coincidiendo con rebotes. Hoy el VIX está en 15.67 y el S&P 500 a −1.2% de su máximo, así que el estado actual no es de pánico. Ese riesgo se activaría tras una corrección fuerte seguida de rebote.
- [I] **Concentración de evento.** El resultado de MU del 30-sep cae en la semana previa al inicio de la temporada. Los tres primeros del ranking (AMD, TECL y MU) tienen correlación de 0.77 a 0.82 entre sí. Una sorpresa de MU movería a todo el bloque.
- [C] **Extensión.**
  - AMD está +77% sobre su SMA200 y MU +68%. El siguiente, TECL, está en +48%.
  - Ninguno de los 20 está más de 18.1% abajo de su máximo de 52 semanas (el más lejano es GDX).
  - No calculé la distribución histórica de esta distancia. Qué implica para el retorno siguiente **no está verificado**.
- [C] **El peso en 1 mes.** La depreciación de 4.5% explica casi todo el 1m en MXN de los índices de EUA. SPY rindió +0.7% en USD y +5.3% en MXN en el mismo mes. Si el peso revierte, el 1m en MXN se corrige sin que el activo se mueva.

---

## 7. Implicaciones para la cuenta arena

Contexto [H]: `parametros.json` pone al sistema en fase 0. Lo que sigue es insumo para diseñar la estrategia de la temporada, no órdenes.

1. **[R] Vehículo principal de momentum: TECL o TQQQ, no AMD ni MU.**
   - AMD (56% por título) y MU (96%) rompen el tope `accion_individual_max` = 0.30 en el SIC. LLY ni siquiera cabe.
   - TECL tiene correlación de 0.82 con AMD y 0.78 con MU. Captura el mismo factor con incrementos de 20% de la cuenta.
   - TQQQ: 7% por título, correlación de 0.95 con TECL y menos volatilidad (56% contra 81%).
   - Comprar AMD o MU exigiría Trading USA (fracciones en USD, conversión cambiaria; costos en `01`).
   - [H] Choque con A2: A2 propone (provisional, no está en `parametros.json`) un tope de 0.25 para los 3x con σ del subyacente ≥ 30%, y pone a TECL en ese grupo (XLK: 30.1% a 6 meses en USD). Con ese tope, TECL sería un solo título (~20%). TQQQ y SPXL quedan en el tope de 0.5 [A2].
2. **[R] SPXL como versión de menor varianza.** Tiene la menor volatilidad de los apalancados verificados en el SIC (30%) y el segundo mejor 6m/vol entre ellos (1.72, detrás de TECL con 1.77). Está a −0.9% de su máximo. UPRO y SSO puntúan parecido, pero su disponibilidad en el SIC **no está verificada** (A2). No usarlos hasta confirmarlos en la app.
3. **[R] No sumar varios apalancados de tecnología creyendo que diversifican.** TECL, TQQQ y SOXL tienen correlación de 0.86 a 0.95. Dos de ellos son la misma apuesta con más fricción.
4. **[R] Pierna(s) de diversificación con tendencia positiva y correlación baja o negativa contra los semis:**
   - XLE (6% por título; −0.39 con TECL).
   - XLV (15%; −0.51 con TECL).
   - GDX (8%; 0.29 con TECL; liquidez baja, solo con orden limitada).

   COPX y GMEXICOB se correlacionan más con los semis y apalancados de tecnología (0.32 a 0.55) y ya perdieron momentum de 1m. GMEXICOB tiene la ventaja de estar en MXN.
5. **[R] SOXL: solo como palanca de máxima varianza.** TECL domina a SOXL en la pantalla: mejor Score (10.0 contra 24.3), cerca de la mitad de la volatilidad (81% contra 147%) y correlación de 0.94. SOXL solo se justifica si el modo torneo pide subir la varianza (`modo_torneo`: ir atrás del rival por ≥5 pp).
6. **[C] El filtro de apalancados permite hoy los 7 apalancados.** Todos los subyacentes están sobre su SMA200 en USD y el VIX está en 15.67. Si el VIX pasa de 25 o el subyacente pierde su SMA200, `parametros.json` obliga a vender.
7. **[R] Evitar lo que está abajo de la SMA200:** bonos largos, XLU, KWEB, WALMEX, ORCL, NFLX y URA. Tampoco hay argumento de momentum para IBIT (12-1 de −36%), que además **no está verificado en el SIC** (A2).
8. **[R] Riesgo cambiario.** Todo lo del SIC es una posición larga en USD. El peso ya se depreció 4.5% en un mes, con Fed al alza y Banxico quieto [3][4][5]. Si revierte, resta directo al TWR. GMEXICOB es la única pierna del top en MXN sin exposición cambiaria directa.
9. **[R] Rutina.**
   - Correr `pantalla.py` cada semana y antes de cada rebalanceo.
   - Histéresis contra el tope de 8 operaciones al mes: una posición solo se sustituye si sale del top 15 filtrado o pierde la SMA200. Solo entra una nueva si está en el top 5.
   - Revisar la pantalla después del resultado de MU (30-sep), antes del fondeo.
10. **[R] Corregir el kit.** `herramientas/portafolio.py` valúa en MXN con el cierre diario de `MXN=X` "en o antes de la fecha", que en realidad es la foto de la noche anterior. Como el TWR de la competencia se mide en MXN, conviene reusar `fx_cierre_eua()` de `pantalla.py` o documentar el desfase. Lo mismo aplica a `tablero.py`.

---

## Fuentes

1. Yahoo Finance, API chart v8. Precios diarios: `https://query1.finance.yahoo.com/v8/finance/chart/<TICKER>?range=2y&interval=1d`. USD/MXN horario: https://query1.finance.yahoo.com/v8/finance/chart/MXN=X?range=2y&interval=1h. Índices: ^VIX, ^GSPC, ^SOX, ^MXX, BTC-USD, DX-Y.NYB. Consultado el 25-sep-2026.
2. FRED, Federal Reserve Bank of St. Louis. Series DGS10, DGS2 y DFF. https://fred.stlouisfed.org/series/DGS10 , https://fred.stlouisfed.org/series/DGS2 , https://fred.stlouisfed.org/series/DFF (último dato 23-sep-2026; consultado el 25-sep-2026)
3. Federal Reserve, "Federal Reserve issues FOMC statement", 16-sep-2026. https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm
4. Investing.com México, "Banxico deja tasa de interés en 6.50%; advierte: no seguirá mecánicamente a la Fed", 24-sep-2026. https://mx.investing.com/news/economic-indicators/banxico-mantiene-la-tasa-de-interes-en-650-3775785
5. Expansión (Octavio Torres), "¿Qué le pasó al superpeso? se deprecia en una semana clave para Banxico", 24-sep-2026, 11:25. https://expansion.mx/economia/2026/09/24/tipo-cambio-hoy-24-septiembre-peso-dolar
6. The Tech Portal, "AMD joins $1 Trillion club as stock surges nearly 10%", 21-sep-2026. https://thetechportal.com/2026/09/21/amd-1-trillion-market-capitalisation-stock-price
7. Startup Fortune, "Micron stock tops $1,000 for the first time as the AI memory boom rages on", 23-sep-2026. https://startupfortune.com/micron-stock-tops-1000-for-the-first-time-as-the-ai-memory-boom-rages-on/
8. The Motley Fool, "News About Muse Drove a 1-Day 11% Jump in Meta Stock…", 24-sep-2026. https://www.fool.com/investing/2026/09/24/news-about-muse-drove-1-day-11-jump-in-meta-stock/
9. The Motley Fool, "Why Oracle Stock Fell Quickly Today", 14-sep-2026. https://www.fool.com/investing/2026/09/14/why-oracle-stock-fell-quickly-today/
10. Jegadeesh, N. y Titman, S. (1993), "Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency", *Journal of Finance* 48(1), 65-91. https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1993.tb04702.x
11. Moskowitz, T. y Grinblatt, M. (1999), "Do Industries Explain Momentum?", *Journal of Finance* 54(4), 1249-1290. https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00146
12. Moskowitz, T., Ooi, Y. H. y Pedersen, L. H. (2012), "Time Series Momentum", *Journal of Financial Economics* 104(2), 228-250. https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf
13. Daniel, K. y Moskowitz, T. (2016), "Momentum Crashes", *Journal of Financial Economics* 122(2), 221-247. https://www.sciencedirect.com/science/article/pii/S0304405X16301490 (versión NBER w20439: https://www.nber.org/papers/w20439)
14. Faber, M. (2007), "A Quantitative Approach to Tactical Asset Allocation", *Journal of Wealth Management*; SSRN 962461. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461
15. Documentos internos: `arena/investigacion/01-gbm-operativa-y-costos.md` (costos, fracciones, Trading USA), `arena/investigacion/02-universo-sic-bmv-agresivo.md` ("A2": disponibilidad en el SIC, precios BMV, liquidez) y `config/parametros.json` (perfil `arena_agresivo`, `filtro_apalancados`, límites de concentración).
16. StockAnalysis (datos de S&P Global), cotizaciones BMV del 24-sep-2026: https://stockanalysis.com/quote/bmv/AMD/ (11,139 MXN), https://stockanalysis.com/quote/bmv/MU/ (19,126 MXN), https://stockanalysis.com/quote/bmv/LLY/ (20,970 MXN), https://stockanalysis.com/quote/bmv/XLV/ (3,023 MXN). Consultado el 25-sep-2026.
17. Micron Technology (GlobeNewswire), "Micron Technology to Report Fiscal Fourth Quarter Results on September 30, 2026", 26-ago-2026. https://www.globenewswire.com/news-release/2026/08/26/3351673/14450/en/micron-technology-to-report-fiscal-fourth-quarter-results-on-september-30-2026.html

---

## Registro de verificación (2026-09-25)

Verificador adversarial. Ejecución: ~05:27 UTC del 25-sep-2026, antes de la apertura de EUA.

**1. Reproducción de cálculos [C]**
- **Re-ejecución de `pantalla.py` sin caché** (`--cache-horas 0`, salida en scratchpad; el CSV publicado no se tocó). Las 68 filas coinciden con `pantalla-2026-09-25.csv` en 16 columnas (rangos, precios, retornos, vol, SMA200, DD, máx 52s, 6m/vol y Score), con tolerancia de 1e-4. Hubo 0 diferencias.
- **Recálculo independiente** con código propio: JSON crudo de Yahoo, sin importar `pantalla.py` ni `datos.py`. Cubre 18 tickers: AMD, TECL, MU, SPXL, GMEXICOB, LLY, XLV, SOXL, SPY, NAFTRAC, TQQQ, XLE, ORCL, WALMEX, XLK, SOXX, GDX y COPX. La diferencia máxima contra el CSV es de 3.9e-5 (<0.004 pp).
- **Tablas contra el CSV:**
  - Secciones 3 y 4: 31 filas × 10 métricas = 310 celdas, con 0 diferencias.
  - Medianas por categoría: 0 diferencias.
  - Filtro MXN contra USD: solo cambia en XLI, XLP y HYG, como dice el texto.
- **Correlaciones:** la matriz de 12×12 se reproduce exacta (60 rendimientos log, fechas comunes del 26-jun al 24-sep). NVDA y TLT también se confirmaron. IBIT y AAPL se corrigieron (ver abajo).
  - Nota de método: la intersección con GMEXICOB quita los feriados de la BMV (p. ej., 16-sep). Algunos rendimientos de EUA en la ventana abarcan 2 sesiones. Sin GMEXICOB, las cifras cambian ≤0.02.

**2. Conversión a MXN [C]**
- La vela diaria de `MXN=X` fechada 24-sep tiene *timestamp* de 23:00 UTC del 23-sep (gmtoffset 3600, Londres) y vale 17.5413. La vela horaria de las 23:00 UTC del 23-sep cerró en 17.5419, y la de las 19:00 UTC del 24-sep en 17.7188. Confirmado.
- En las 23 velas diarias del 25-ago al 24-sep, la desviación máxima contra la horaria de las 23:00 UTC del día previo es de 0.072%. Se cumple también en las velas de lunes.
- La vol 60d de SPY en MXN es de 9.4% con el tipo de cambio horario y de 12.9% con la vela diaria. Confirmado.
- USD/MXN: 1m +4.5%, 3m +0.5%, 6m −0.4% y 12m −3.9% (18.43 el 24-sep-2025). Confirmado.
- SPY rindió +0.7% en 1m en USD y +5.3% en MXN. Confirmado.
- Validación BMV/EUA: AMD 17.70, MU 17.70, LLY 17.74 y XLV 17.80. Los precios BMV se confirmaron en StockAnalysis (cierres del 24-sep: 11,139, 19,126, 20,970 y 3,023.00 MXN).

**3. Look-ahead y fecha de los datos [C]**
- **Corte en 24-sep.** Es la última sesión completa de EUA: `regularMarketTime` de SPY = 24-sep a las 16:00 NY, y el script corrió antes de la sesión del 25-sep. Todas las series se recortan a ≤ corte.
- **Tipo de cambio.** Ningún día usó el respaldo de la vela diaria de *d+1*, que es la única vía que metería un dato ~3 h posterior al cierre. Tres días usaron la vela horaria previa, que es anterior al cierre.
- **`adjclose`.** Ajusta hacia atrás de forma multiplicativa, así que no altera los retornos entre fechas anteriores al ajuste. No hay look-ahead material.
- **Hallazgo: dos datos posteriores al corte.** El contexto de mercado usaba BTC y DXY intradía del 25-sep. Se sustituyeron por el último cierre ≤ corte. En BTC, la vela del 24-sep viene vacía en Yahoo, así que se usa la del 23-sep.
- **NAFTRAC.MX.** La vela del 24-sep existe, pero con cierre nulo. El rezago de un día se confirma.

**4. Hechos externos verificados [H]**
- **FRED:**
  - DGS10: 5.11% el 23-sep (máximo de 12 meses), 4.47% el 1-jun-2026 y 4.15% el 22-sep-2025.
  - DGS2: 4.85% y 4.05%.
  - DFF: 3.88% desde el 17-sep.
- **FOMC del 16-sep:** subió la tasa a 3-3/4–4%, con votación 12-0. Las citas son textuales.
- **Banxico (Investing.com):** tasa de 6.50%, decisión unánime. La cita es textual.
- **Expansión (O. Torres, 24-sep, 11:25):** 16.9971 al cierre de agosto; FIX de 17.5030 el 23-sep; bono a 30 años en 5.46%, "su nivel más alto desde 2004"; WTI 93.69 y Brent 105.15.
- **Notas de empresas:**
  - The Tech Portal: cita de AMD textual; Yahoo da un cierre de 615.52 el 21-sep, coherente.
  - GlobeNewswire: MU reporta el 30-sep a las 2:30 p.m., hora de la Montaña.
  - Startup Fortune: la cita de HBM es textual (la oración continúa).
  - Fool: META +11% por Muse, lanzado el 8-sep; la cita de ORCL es textual.
- **Daniel y Moskowitz (NBER w20439):** el resumen dice "'panic' states - following market declines and when market volatility is high… contemporaneous with market rebounds". Coincide con el texto.
- **Índices en Yahoo:** VIX 15.67; S&P 500 7,704.13 contra 7,798.99; ^SOX 12,492.54 contra 14,634.72; IPC 64,264.16 contra 71,601.35. Todos confirmados; los máximos son al cierre.

**5. Correcciones hechas en este archivo**
1. **Resumen 8.** La lista de vehículos que "caben" presentaba SPXL como tecnología y omitía QLD. Se reescribió y se agregó que SOXX y SMH equivalen a media cuenta por título.
2. **Sección 1.2.** Faltaba el respaldo intermedio del tipo de cambio (vela horaria previa dentro de 6 h). Se agregó la auditoría de uso de respaldos.
3. **Sección 2, USD/MXN de agosto.**
   - La cita no era textual. Dice "una depreciación cercana a 3.8%", no "aproximadamente 3.8%".
   - La base es 16.9971 → 17.6380 a media sesión del 24-sep, no "en el mes".
   - Se agregó el FIX del 21-sep.
4. **Sección 2, Fed funds.** El valor previo era 3.63%, no 3.64%.
5. **Sección 2, bono a 30 años.** Se aclaró que 5.46% es un dato intradía de prensa del 24-sep. FRED DGS30 da 5.40% el 23-sep.
6. **Sección 2, VIX.** El máximo de 31.05 es al cierre; el intradía fue 35.30.
7. **Sección 2, BTC y DXY.** Eran datos intradía del 25-sep, posteriores al corte.
   - BTC: 84,179 → 84,383 (23-sep), con −32.4%.
   - DXY: 101.28 → 101.29 (24-sep), con −0.3% contra su máximo.
8. **Sección 3, GMEXICOB.** Se quitó el asterisco de estimación: es el precio BMV en MXN, no USD × 17.72.
9. **Sección 3, "Top 1x".** Faltaban XLV y NVDA; son 14 y no 12.
10. **Sección 3, ARKK.** Su 12-1 es −7.5%, que redondea a −7%, no a −8%.
11. **Sección 5, "Otros valores".**
    - IBIT decía 0.09 a 0.44 "con el resto". Es falso: con XLE da −0.38.
    - En AAPL, el −0.06 es contra SPXL; contra semis y apalancados de tecnología el rango es −0.22 a −0.32.
12. **Sección 6, MU.**
    - El cierre de 1,035.34 era el ajustado; el nominal fue 1,035.50.
    - Se agregó que MU también cerró arriba de 1,000 el 18-sep, antes del "first time on September 22" de la nota.
13. **Sección 6, META.** Se agregó la fecha del salto en Yahoo: 21-sep, +11.3%.
14. **Sección 6, GLD e IAU.** Estaban a −4.4% de su SMA200 en MXN y −5.9% en USD, no a −5.4%.
15. **Sección 7.2, SPXL.** El texto decía que tenía "el mejor 6m/vol entre los apalancados verificados", y es falso: TECL tiene 1.77 y SPXL 1.72. Se reescribió: SPXL tiene la menor vol y el segundo mejor 6m/vol.
16. **Sección 7.1.** Se agregó el choque con la propuesta de A2 de un tope de 0.25 para TECL.

**6. Sin verificar o fuera de alcance**
- **Disponibilidad en el SIC y precios BMV de A2.** Se tomaron de A2 sin re-verificar; les corresponde la verificación de A2. Los "1 título" con `*` siguen siendo estimaciones con 17.72.
- **Reversión de 1 mes como justificación del 12-1.** Sigue **(no verificado)** en la fuente primaria.
- **Referencias académicas [10]–[12] y [14].** No se volvieron a descargar. Se revisó solo [13].
- **Tiempo de corrida "~2 min".** Es aproximado.
- **Inconsistencia en `parametros.json`, no en este archivo.**
  - `rivales.capital_inicial_mxn` = 20000 y `metrica_competencia` dice "igual capital para todos".
  - El dueño declaró 15,000 MXN para `arena-grok`.
  - El TWR % no depende del capital. La granularidad sin fracciones del SIC sí depende del capital: 1 título de TECL es ~26% de 15k.
