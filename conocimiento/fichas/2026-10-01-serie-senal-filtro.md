# Ficha de estudio: ¿qué serie debe dar la señal del filtro de 200 días?

> Bloque de trabajo continuo, 1-oct-2026 (19:10 CDMX). Cierra la pregunta que dejaron abierta tres auditorías ciegas seguidas: AC-07 (apalancados), AC-09 (SMA10) y AC-10 (TSMOM). Las tres dicen que la regla debe **fijar la serie de la señal**. Es insumo directo para el comité del 2-oct (modo C, `filtro_apalancados`).
> Código: `conocimiento/fichas/codigo/2026-10-01-serie-senal-filtro.py` (stdlib + `herramientas`, ~3 s).

## 1. Pregunta y diseño
- **Sujeto:** un 3x diario sintético filtrado del S&P 500 (1993-2026) y del Nasdaq-100 (1999-2026).
- **Señales comparadas:** sobre (a) el índice de precio (^GSPC o ^NDX), (b) el ETF con dividendos (SPY o QQQ, cierre ajustado) y (c) el precio del ETF sin ajustar. Cada una sin banda y con banda de ±3% (sale bajo SMA × 0.97 y entra sobre SMA × 1.03).
- **Supuestos:** rezago de 1 día. Fuera del 3x se gana la T-bill (FRED DTB3). Costos: gasto de 0.91%/año, financiamiento de 2 × r_f y 0.29% por cambio de posición (GBM). Fuente: Yahoo, historia completa (`yahoo_historia`).

## 2. Resultados
| Subyacente | Banda | Serie de la señal | CAGR | MDD | Cambios/año | Días con señal distinta a la del índice |
|---|---|---|---|---|---|---|
| S&P 500 | 0% | Índice de precio | 13.79% | −70.6% | 6.7 | — |
| | 0% | ETF ajustado (TR) | 15.04% | −73.6% | 6.4 | 185 |
| | 0% | ETF sin ajustar | 13.54% | −72.0% | 6.6 | 46 |
| | **±3%** | **Índice de precio** | **21.41%** | **−53.0%** | **1.0** | — |
| | ±3% | ETF ajustado (TR) | 19.78% | −55.1% | 1.0 | 132 |
| | ±3% | ETF sin ajustar | 19.60% | −55.9% | 1.0 | 15 |
| Nasdaq-100 | 0% | Índice de precio | 10.13% | −96.4% | 6.9 | — |
| | 0% | ETF ajustado (TR) | 10.32% | −95.4% | 6.7 | 49 |
| | 0% | ETF sin ajustar | 11.53% | −95.4% | 6.2 | 28 |
| | ±3% | Índice de precio | 12.50% | −93.6% | 1.7 | — |
| | ±3% | ETF ajustado (TR) | 14.10% | −90.9% | 1.7 | 38 |
| | ±3% | ETF sin ajustar | 14.33% | −90.9% | 1.7 | 23 |

Referencia de comprar y mantener 1x: SPY 10.81% y QQQ 10.88% de CAGR.

## 3. Lectura
1. **La serie importa poco y sin dirección estable.** Cambiarla mueve el CAGR entre 0.2 y 1.8 pp, pero el orden se invierte según el subyacente y la banda: con el S&P y banda gana el índice de precio; con el Nasdaq ganan los ETF. Ninguna serie es "la buena". Es ruido de umbral: la señal del ETF ajustado difiere en 132-185 días porque los dividendos suben su SMA. Por eso **hay que fijarla por regla antes de operar**, no elegirla después de ver resultados.
2. **La banda importa mucho más que la serie.** Con el S&P, ±3% sube el CAGR de 13.8% a 21.4%, baja los cambios de 6.7 a 1.0 por año (menos costo y menos serrucho) y recorta el MDD de −71% a −53%. Coincide con la banda de ±3% que el gestor de riesgo ya propuso para cripto (`config/parametros.json`).
3. **El filtro no protege a un 3x del Nasdaq de una burbuja que revienta en escalones.** De mar-2000 a mar-2003, el 3x filtrado perdió **93.6%** aun con banda. Cada rebote cruzaba la SMA y la volvía a perder. Con el S&P, el peor tramo fue 2022-2023, con −53% de serrucho. **"Solo protección" (AC-07) vale para el S&P desde 1993, no para el Nasdaq en 2000-2002.** La muestra de AC-07 con ETF reales (TQQQ desde 2010) no tenía ese episodio.

## 4. Propuesta para el comité del 2-oct (no aplicada)
- **Fijar `filtro_apalancados`:** **señal sobre el índice de precio del subyacente** (^GSPC para SPXL/UPRO, ^NDX para TQQQ), al cierre, con **banda de ±3%** y ejecución al día siguiente. El índice de precio no depende de dividendos ni de errores de ajuste del proveedor, y es el mismo para cualquier ETF del mismo índice.
- **Si el comité usa un 3x del Nasdaq en modo C:** dimensionarlo sabiendo que el filtro, históricamente, **no** evitó un −94% en 2000-2003. Con 50% de la cuenta, eso equivale a ~−47% de la cuenta antes de los cortacircuitos, que tendrían que actuar antes (−12/−20/−28/−35%).

## 5. Límites
- 3x sintético (diario, con costos aproximados), no ETF reales antes de 2010. Un solo camino histórico para cada índice.
- Las diferencias de CAGR entre series están dentro del ruido; no se hizo prueba formal de significancia.
- QQQ empieza en 1999-03, así que el filtro del Nasdaq arranca hacia dic-1999, ya cerca del pico.

## 6. Estado
"Apalancados y filtro de tendencia" no cambia de nivel. Se amplía su evidencia: serie de la señal, banda y el episodio de 2000-2003 del Nasdaq.
