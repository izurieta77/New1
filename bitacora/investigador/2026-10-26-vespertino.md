# Investigador, corrida vespertina · 2026-10-26 (20:12 CDMX; escrita a las 2026-10-27 02:15 UTC)

**Barrido corto, turno de reglas de riesgo.** Rotación: 23-oct riesgo, 24-oct cripto, 25-oct fiscal, 26-oct riesgo.

## Búsquedas
1. **arXiv, listados `new`** de q-fin RM, PM, TR, ST, MF y CP: **nada nuevo** sobre drawdown, cortacircuitos, tamaño de apalancados, filtro de tendencia ni stops. Revisados por título y sin pertinencia: 2610.32614, 2610.32959, 2610.29652, 2610.32237, 2610.31903, 2610.31825, 2610.32350, 2610.32970.
2. **Se usó el presupuesto en un pendiente del 23-oct:** arXiv:2604.27287, que toca el UPRO de la cartera y el debate de tamaño de R18.
3. **No consultado:** NBER (revisado el 23-oct) y SSRN (403 desde este entorno).

## Paper verificado (uno, texto completo)
- **Bianchi y Goldberg, "A Levered ETF Anomaly Explained"**, arXiv:2604.27287 v1 (q-fin.PM, 30-abr-2026, 10 pp.), UC Berkeley y BlackRock.
  - **Tesis:** de ene-2022 a dic-2023, el S&P 500 subió 0.08% mientras SSO cayó −11.1% y UPRO −28.2%. Dos tercios de la brecha los explican la composición y la volatilidad (G ≈ (1+E)e^(−V²/2) − 1). El resto lo atribuyen a la covarianza entre la "razón de rendimiento" diaria λ = R_ETF/R y el índice, que leen como un efecto de sincronización.
  - **Grado: C.** Es un working paper sin arbitraje. Usa rendimientos de precio (CRSP `retx` y `sprtrn`), "neglecting dividends and market frictions": **no modela el financiamiento ni la comisión**. Su término de covarianza es una identidad contable, Cov(λ, R) = E(R_ETF) − E(λ)E(R), y absorbe todo lo omitido.
- **Verificación propia** (`conocimiento/fichas/codigo/2026-10-26-bianchi-goldberg-upro-acarreo.py`). Datos: Yahoo (cierres sin ajustar y ajustados de UPRO, SSO, ^GSPC y ^SP500TR) y FRED DFF (fed funds promedio de 3.36% en el periodo).
  - **Reproduce su brecha:** −5.42 pp/año en UPRO (paper −5.44) y −2.16 en SSO (paper −2.18). Los niveles difieren ~0.3 pp en el índice porque tomo 500 días y ellos 501.
  - **Modelo de acarreo:** 3 × rendimiento total − 2 × fed funds por día natural − comisión de 0.91%. Explica **~2.8 de los 5.4 pp de UPRO (≈51%)**: se pagan 2 × 3.36% de financiamiento, se cobran 3 × 1.66% de dividendos (que su índice de precio omite) y se resta la comisión.
  - **Residuo contra el precio ajustado:** −2.0 pp/año en UPRO (−2.2 en 2022, −1.8 en 2023) y −0.85 en SSO. [Inferencia] Es del orden del diferencial de los swaps sobre fed funds más el error de seguimiento. Coincide con lo que ya medimos: en R11-B el UPRO sintético rinde ~1.6 pp/año más que el real (2009-hoy).

## Qué cambia
- **Nada en las reglas ni en los parámetros.** El paper no corrige nada nuestro. Nuestras simulaciones (R16, R18) ya descuentan 2 × DTB3 y la comisión, que es lo que el paper omite.
- **Lo útil:** la parte "inexplicada" del arrastre del UPRO es sobre todo acarreo. Con tasas altas cuesta ~2 × r más que el 3x ideal. El residuo de ~2 pp/año contra el sintético es un sesgo optimista conocido de nuestros backtests (R11-B), no una anomalía nueva.
- **Archivos:** adenda fechada en el cap. 07 y script de verificación. No hay fila en el registro de errores ni cambios en el estado de dominio.
