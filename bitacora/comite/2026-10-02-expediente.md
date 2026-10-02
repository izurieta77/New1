# Expediente del comité semanal · viernes 2-oct-2026 (W40)

## Pregunta al comité
Para la cuenta **arena-claude** (temporada 28-sep-2026 a 28-ene-2027; papel GBM 20,000 + papel Binance 10,000 como registro sombra; real GBM 10,000 SIN FONDEAR y real Binance 5,000 con 2,000 en BTC), decidir:
1. **GBM:** (A) mantener la cartera A 1x (SPYM ~56% + QQQM ~27% + efectivo en papel; en real, boleta (a) 2 SPYM + 1 QQQM) o (C) rediseño **modo C** por mandato del dueño: hasta 50% en un ETF 3x (TQQQ o SPXL/UPRO) con `filtro_apalancados` + resto en índice 1x. Si C, ¿qué 3x, qué peso y qué regla de filtro?
2. **Binance:** exposición a BTC (hoy papel ~40% BTC / 60% MXN; real 2,000 de 5,000 = 40%): mantener 40%, escalar a 65%, o hasta 100% con filtro.
3. **Tipo de cambio:** ¿se toma una decisión explícita sobre exposición USD/MXN?
4. **GBM real sin fondear 4 días:** qué hacer con la boleta del 30-sep.

## Hechos clave (verificados en el repo)
- **Mandato del dueño (25-sep):** meta +40/60/200% en 4 meses; mantener topes de pérdida; operar con la máxima agresividad que permiten (modo C). `config/parametros.json` → `meta_temporada_dueno`. Probabilidad histórica del modo C: mediana 4 meses +18.4%, p10 −19.2%, p90 +58% (`arena/modelos/salida_meta_dueno_40_60_200.txt`). La meta +40% tiene 0-4% de probabilidad histórica en cualquier candidata.
- **Topes vigentes (provisionales, gestor de riesgo 29-sep, ratificar hoy):** pérdida absoluta 5,000 GBM / 2,500 cripto; orden mínima 2,500; etf_indice_max 60%, etf_apalancado_max 50%, cripto_max 30% (perfil arena_agresivo). Cortacircuitos sobre TWR: −12/−20/−28/−35%.
- **Desempeño:** papel GBM +2.68% (índice 102.68 al 2-oct; en USD +0.8%, el resto es el peso 17.825→18.145); papel Binance +0.12% (29-sep); drawdown 0%.
- **Régimen (tablero 2-oct):** MIXTO +0 (tendencia alcista, VIX 15.3, crédito HY en vigilancia, peso en depreciación rápida). 10a 5.28%, Fed subió 25 pb el 16-sep. NFP sep +29k, desempleo 4.2%. S&P ~7,723 (percentil 98 de 5 años).
- **Irán/Ormuz en ALTA desde el 1-oct:** tercer portaaviones; estrecho efectivamente cerrado; Brent ~100. Evidencia propia: el choque GPR no predice rendimiento siguiente (`conocimiento/fichas/2026-10-02-gpr-rendimientos.md`); Hirshleifer et al. RFS 2025: prima por guerra (a favor de mantener). Känzig-Stock-Zanotti 2026: con EUA exportador, daño vía tasas.
- **Laboratorio sobre apalancados y filtro:**
  - R06/AC-07: apalancado filtrado = "solo protección" fuera de muestra con ETF reales 2010+. En MXN, 50% TQQQ filtrado + 50% QQQ tocó −20% en 19.9% de temporadas de 4 meses y −28% en 4.0%; 50% UPRO filtrado + 50% SPY: 8.5% y 0.4%.
  - `conocimiento/fichas/2026-10-01-serie-senal-filtro.md`: la serie de señal mueve 0.2-1.8 pp sin dirección estable; la banda ±3% domina (S&P 3x: CAGR 13.8→21.4%, cambios 6.7→1.0/año, MDD −71→−53%); **Nasdaq 3x filtrado perdió −93.6% en 2000-03 aun con banda.**
  - `conocimiento/fichas/2026-09-29-volatility-drag.md`: L* = μ/σ² muy sensible a μ (μ 4% → L* 1.31); UPRO real 2.22 pp/año debajo de la fórmula.
  - `conocimiento/fichas/2026-09-29-cortacircuitos-apalancados.md` y decisiones-pendientes: con 50% 3x S&P filtrado, P(tocar −12%) ~29%.
- **Media-varianza en MXN** (`conocimiento/fichas/2026-09-30-media-varianza-mxn.md`): la cartera (a) es apuesta de concentración al Nasdaq; 1/N con oro tiene mejor Sharpe en muestra; QQQ −79.5% en MXN 1999-2002.
- **Tipo de cambio:** después de alzas de +6% del USD/MXN no hay dirección predecible (22 episodios); el peso amortigua las caídas en MXN (R08/AC-05).
- **Cripto:** BTC ~84,500; filtro SMA200 ENCENDIDO (salida ~69,200); funding plano; 895+ días desde H4 (zona histórica de mínimos de ciclo, grado C/D).
- **Abogado del diablo W39** (`bitacora/semanal/2026-W39-abogado.md`): no SPXL con el 10a ≥ 5%; condición de 6 reportes de rivales antes de apalancar.
- **Pendiente operativo:** el dueño no ha confirmado que TQQQ/SPXL aparezcan en la app de GBM.
