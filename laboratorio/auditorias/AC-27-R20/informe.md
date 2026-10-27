# AC-27-R20: ejecución B independiente de la réplica R20 (brecha UPRO real contra 3x sintético)

> Auditor de réplicas, 27-oct-2026. Fase 0: no recomienda inversiones. Escribí el código desde cero, solo con la biblioteca estándar, y **no leí `R20.py` ni `R20-resultados.json` hasta terminar mi cálculo**. Del archivo de la réplica solo leí el pre-registro (§1-§5).
> Reproducción: `python3 -I laboratorio/auditorias/AC-27-R20/ac27_r20.py` (usa la caché de `datos/`; con `--descargar` la regenera). La salida completa está en `salida.txt` y los números en `resultados.json`.

## 1. Método

- **Brecha diaria:** g_t = r_UPRO,t − [3·r_idx,t − 2·f_t − 0.0091/252], con rendimientos del 2009-06-26 al 2026-10-23. El primer rendimiento es del cierre del 25-jun al cierre del 26-jun.
- **Fechas:** la intersección de UPRO, ^SP500TR y SPY en Yahoo. Los rendimientos se calculan entre fechas consecutivas de esa intersección. Uso la fecha local de Nueva York (gmtoffset).
- **Independencia respecto de A** (tres ejes; se pedían al menos dos):
  1. **Tasa:** FRED **DFF** (fed funds efectiva) en la versión principal. También reporto **DTB3**.
  2. **UPRO:** **reconstruido** con el cierre de Yahoo (ajustado por splits, no por dividendos) más las distribuciones de `events=div`: (P_t + D_t)/P_{t−1} − 1, con D en la fecha ex. Control contra el adjclose de Yahoo: diferencia media de 0.00003 pp por año y máxima diaria de 5 pb.
  3. **Total return del índice:** ^SP500TR de Yahoo, porque Yahoo no ofrece otro índice TR diario y FRED SP500 solo cubre 10 años sin dividendos. Como construcción alternativa uso **SPY reconstruido** (cierre más dividendos) más su gasto de 0.0945% anual. Control: SPY-TR − ^SP500TR = −0.03 pp por año en media, con una desviación diaria de 6.6 pb.
- **Alineación de la tasa:** en la versión principal, f_t usa la tasa vigente al cierre anterior (t−1), con el último dato hacia adelante. Como variante uso la tasa del mismo día t, que es lo que hace A.
- **Devengo:** /252 por día hábil en la versión principal. Variante: días naturales/360 (ACT/360), f_t = y·(t − t₋₁)/360.
- **Tramos:** se clasifican con la tasa usada en cada variante. Además, la variante "DFF con tramos DTB3" usa la definición literal del pre-registro.
- **Regresiones:** OLS con covarianza HAC Newey-West (Bartlett, 6 rezagos), escrita a mano. M3 regresa g sobre f_t; M4 regresa g sobre r_idx.
- **CAGR (M1b):** años = días naturales/365.25. A anualiza con 252/n; afecta el nivel de cada CAGR en ~0.06 pp, pero no la diferencia.

## 2. Fuentes y sha256 (`datos/`, en .gitignore)

| Archivo | Fuente | sha256 |
|---|---|---|
| yahoo_UPRO.json | Yahoo chart v8, UPRO, events=div\|split | `1bfe7151e640c7334f9dd118ac5bbcc7a25cab9f20f6e00d35f201b7397474b2` |
| yahoo_SP500TR.json | Yahoo chart v8, ^SP500TR | `87774cb75451eaf1fc0808e731f6f5a818a3fae91143c301ff39071253154c85` |
| yahoo_SPY.json | Yahoo chart v8, SPY, events=div\|split | `03b29e1b02e1cb2f1a04b5bb0eafcf7549ecb23ca0651d6f6ac4d81892ca24d0` |
| yahoo_GSPC.json | Yahoo chart v8, ^GSPC (descargado, no usado) | `0fbf7af24a2600a8523e0fbd296f45eb0375493103121cbf256930da76d4bce4` |
| fred_DTB3.csv | FRED fredgraph.csv?id=DTB3 | `bbf5cf79827f89fdc123f14e8d567fcfa327a3e33fc00836b952e0da6e8038b3` |
| fred_DFF.csv | FRED fredgraph.csv?id=DFF | `f0dd235ce3f4ed3afad1089216ea58b3508667197b5e655dd088cbf821fdaa84` |

Las descargas se hicieron el 27-oct-2026. Yahoo se pidió con el User-Agent "Mozilla/5.0". FRED corta la conexión con ese UA, así que lo descargué con el UA por defecto de urllib. No hay correos en ningún encabezado.

## 3. Resultados (n = 4,359 días, 2009-06-26 → 2026-10-23)

| Variante | M1 (pp/año) | M1b CAGR real − sint. (pp) | Tramo <0.5% | 0.5-3% | ≥3% | Alto − bajo | M3 const. (pp) | M3 pendiente (t) | M4 pendiente (t NW6) |
|---|---|---|---|---|---|---|---|---|---|
| **B principal: DFF, /252, t−1, UPRO rec., ^SP500TR** | **−1.551** | −1.749 | −1.26 | −1.57 | −2.22 | **−0.96** | −1.25 | −0.21 (−1.46) | **−0.0322 (−6.47)** |
| DTB3, /252, t−1, rec., ^SP500TR | −1.601 | −1.816 | −1.27 | −1.68 | −2.31 | −1.04 | −1.30 | −0.21 (−1.46) | −0.0322 (−6.46) |
| DTB3, /252, mismo día, rec. | −1.600 | −1.814 | −1.32 | −1.55 | −2.29 | −0.97 | −1.32 | −0.20 (−1.36) | −0.0322 (−6.45) |
| DTB3, /252, mismo día, adjclose (receta del pre-registro) | −1.600 | −1.815 | −1.32 | −1.54 | −2.30 | −0.98 | −1.31 | −0.20 (−1.37) | −0.0321 (−6.44) |
| DFF, /252, tramos por DTB3 | −1.551 | −1.749 | −1.18 | −1.73 | −2.25 | −1.07 | −1.25 | −0.21 (−1.46) | −0.0322 (−6.47) |
| DFF, ACT/360 | −1.497 | −1.675 | −1.26 | −1.51 | −2.05 | −0.79 | −4.07* | +1.71 (+8.74)* | −0.0323 (−6.49) |
| DTB3, ACT/360 | −1.552 | −1.750 | −1.26 | −1.62 | −2.15 | −0.89 | −4.06* | +1.70 (+8.75)* | −0.0323 (−6.46) |
| **DFF, /252, índice = SPY-TR + 0.0945%** | −1.468 | −1.917 | −1.02 | −1.72 | −2.30 | −1.28 | −1.07 | −0.27 (−1.86) | **−0.0105 (−0.66)** |
| DTB3, /252, SPY-TR | −1.519 | −1.985 | −1.10 | −1.65 | −2.36 | −1.26 | −1.16 | −0.25 (−1.73) | −0.0105 (−0.66) |
| DFF, ACT/360, SPY-TR | −1.414 | −1.844 | −1.02 | −1.66 | −2.13 | −1.11 | −2.76* | +0.90 (+6.37)* | −0.0105 (−0.66) |

Días por tramo: con DFF, 2,423 / 911 / 1,025; con DTB3, 2,391 / 935 / 1,033.
\* En ACT/360 el regresor de M3 varía sobre todo con el número de días naturales del intervalo (lunes contra otros días) y no con la tasa. Por eso la constante y la pendiente no se comparan con las de /252 (ver §5).

**M2 por año** (B principal con DFF; DTB3 entre paréntesis): 2009 −1.55 (−1.60), 2010 −0.54 (−0.62), 2011 −1.90 (−2.00), 2012 −0.08 (−0.19), 2013 −1.16 (−1.26), 2014 −1.41 (−1.53), 2015 −1.21 (−1.37), 2016 −0.26 (−0.42), 2017 −1.19 (−1.33), 2018 −2.28 (−2.07), 2019 −1.72 (−1.92), 2020 −2.62 (−2.65), 2021 −1.04 (−1.11), 2022 −2.36 (−1.67), 2023 −1.96 (−1.87), 2024 −1.86 (−2.22), 2025 −2.58 (−2.87), 2026 −2.34 (−2.26).

## 4. Veredicto B con el umbral literal

| Hipótesis | Umbral | B principal (DFF) | B con DTB3 | Variante SPY-TR |
|---|---|---|---|---|
| H1 | M1 ≤ −0.5 pp | **Sostenida** (−1.55) | Sostenida (−1.60) | Sostenida (−1.47) |
| H2 | brecha(≥3%) − brecha(<0.5%) ≤ −0.5 pp | **Sostenida** (−0.96) | Sostenida (−1.04) | Sostenida (−1.28) |
| H3 | pendiente < 0 y t NW(6) ≤ −2 | **Sostenida** (−0.032; t = −6.47) | Sostenida (t = −6.46) | **Refutada** (−0.0105; t = −0.66) |

## 5. Comparación con A (hecha después de terminar mi cálculo)

| Medida | A | B principal (DFF) | B, receta A (DTB3, adjclose, mismo día) | B en la ventana de A (desde 06-29) | Diferencia B principal − A |
|---|---|---|---|---|---|
| n | 4,358 | 4,359 | 4,359 | 4,358 | +1 día |
| M1 (pp) | −1.592 | −1.551 | −1.600 | **−1.592** | +0.041 (tolerancia ±0.3) |
| M1b (pp) | −1.81 | −1.749 | −1.815 | −1.806 | +0.06 |
| Tramo <0.5% | −1.305 | −1.26 | −1.32 | −1.305 | +0.05 |
| Tramo 0.5-3% | −1.542 | −1.57 | −1.54 | −1.542 | −0.03 |
| Tramo ≥3% | −2.302 | −2.22 | −2.30 | −2.302 | +0.08 |
| M3 const. / pendiente / t | −1.302 / −0.200 / −1.39 | −1.25 / −0.206 / −1.46 | −1.31 / −0.197 / −1.37 | −1.30 / −0.200 / −1.39 | pequeñas |
| M4 pendiente / t | −0.03214 / −6.44 | −0.03222 / −6.47 | −0.03214 / −6.44 | −0.03214 / −6.44 | ≈0 |

Cada diferencia tiene su explicación:
1. **Un día de menos en A.** A filtra las fechas a ≥ 2009-06-26 antes de calcular rendimientos, así que su primer rendimiento es el del 29-jun y pierde el del 26-jun. Mi variante con la ventana de A **reproduce A exactamente** en M1, M2, M3 y M4 (al tercer decimal). Ese día explica que 2009 dé −1.35 en A y −1.60 en B con DTB3, y 0.008 pp de M1.
2. **DFF en lugar de DTB3** (+0.05 pp en M1). DFF promedió unos 2.5 pb **más** que DTB3 en el periodo. Como el sintético carga 2× la tasa, el sintético queda un poco más abajo y la brecha resulta 0.05 pp menos negativa. Con DFF la diferencia por año más grande es la de 2022 (−2.36 frente a −1.67): en 2022 DTB3 se adelantó a las alzas y DFF las siguió con rezago. Los tramos cambian ligeramente porque se clasifican con otra tasa.
3. **M1b** (0.004-0.06 pp). Se debe a la anualización (A usa 252/n y B días naturales) y a la tasa. No afecta el criterio.
4. **Tasa de t−1 o de t, adjclose o reconstrucción:** ≤ 0.01 pp en M1. Es irrelevante.
5. **ACT/360** (+0.05 pp en M1 frente a /252). Carga 365/360 del rendimiento anual en lugar de ≈1×. El diagnóstico por día de la semana muestra cuándo se devenga el financiamiento. Con SPY-TR y tasa ≥3%, la brecha media diaria es de −3.44 pb el viernes y +1.03 pb el lunes; en los demás días está entre −1.1 y 0 pb. Es decir, UPRO **devenga el fin de semana en el rendimiento del viernes** (cierre del jueves al viernes), no en el del lunes. ACT/360 asignado al intervalo que cubre el fin de semana queda desalineado un día. Por eso M3 en ACT/360 da pendientes positivas y espurias (+1.7): el regresor mide el día de la semana. **Para M3, /252 es la especificación adecuada** [inferencia].
6. **H3 depende de la construcción del índice (hallazgo nuevo de B).** Con ^SP500TR, la pendiente de M4 es −0.032 (t ≈ −6.5), igual que en A. Con SPY-TR (un ETF que cotiza al mismo cierre de mercado que UPRO), la pendiente baja a −0.0105 y deja de ser significativa (t = −0.66). Además, UPRO − 3·SPY-TR regresado sobre r(^SP500TR) da −0.005 (t = −0.34). Mi lectura [inferencia] es que la mayor parte del "apalancamiento efectivo ≈2.97" que A atribuye al timing de Bianchi-Goldberg es un **error de medición entre el índice (precios oficiales de cierre) y el precio de mercado de los ETF**. El ruido diario entre SPY-TR y ^SP500TR es de 6.6 pb y se correlaciona negativamente con r_idx: la pendiente de SPY-TR − ^SP500TR sobre r_idx es −0.009, con t = −1.9. No es una propiedad económica del UPRO. Los niveles de M1 y H1-H2 no cambian (la diferencia de medias entre SPY-TR y ^SP500TR es de −0.03 pp por año), pero H3 no sobrevive al cambio de construcción.

## 6. Estado propuesto

- **Criterio del pre-registro:** B, con código propio y otra fuente (DFF; UPRO reconstruido con dividendos), concuerda en el **signo de H1-H3** (las tres se sostienen en B principal y en B con DTB3) y tiene **M1 dentro de ±0.3 pp**: −1.551 frente a −1.592, una diferencia de 0.04 pp.
- **Estado propuesto: Replicado.**
- **Salvedad obligatoria para la fila maestra:** H3 se replica solo con ^SP500TR como índice. Con SPY-TR como benchmark, la pendiente sigue negativa pero no es significativa (t = −0.66). Recomiendo:
  - presentar H3 como "**sostenida con ^SP500TR, frágil a la construcción del índice**";
  - **retirar la lectura** "apalancamiento efectivo ≈2.97" como mecanismo hasta medirla contra el NAV o contra un benchmark sincronizado.
- **Consecuencia práctica** (no cambia): los backtests R16-R18 sobrestiman al UPRO en ~1.5-1.6 pp por año en promedio (de −1.41 a −1.60 según tasa e índice). En el régimen ≥3% la sobrestimación es de ~2.1-2.4 pp por año. Con ACT/360, la brecha de ese tramo baja a −2.05/−2.15 (DFF/DTB3), porque el sintético carga más financiamiento.
