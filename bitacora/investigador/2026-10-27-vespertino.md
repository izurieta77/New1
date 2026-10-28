# Investigador, corrida vespertina · 2026-10-27 (20:12 CDMX; escrita a las 2026-10-28 02:15 UTC del 28-oct)

**Barrido corto, turno de prima cripto.** Rotación: 24-oct cripto, 25-oct fiscal, 26-oct riesgo, 27-oct cripto.

## Búsquedas
1. **arXiv, listados `new`** de q-fin, cs.CR, cs.CE y econ.GN, filtrados por bitcoin, cripto, stablecoin, DeFi, token y activos digitales. Pertinente: **2610.35702**. Revisados por título y sin relación con nuestras reglas: 2610.33538 (sukuk tokenizado), 2610.34930 (derivados de rendimiento DeFi), 2610.33862, 2610.34121 y 2610.27111 (seguridad).
2. **No consultado:** NBER y SSRN (403 desde este entorno).

## Paper verificado (uno, texto completo)
- **Ebadollahyvahed y Umeorah, "Weekend Crypto Volatility and Monday Market Risk"**, arXiv:2610.35702 v1 (q-fin, 26-oct-2026, 35 pp.).
  - **Qué hace:** suma la varianza Garman-Klass de sábado y domingo de BTC, ETH y XRP y la usa como factor común para predecir la varianza del lunes del S&P 500, del oro y de IEF, con modelos HAR. Datos de Yahoo, nov-2017 a jun-2026.
  - **Resultado:**
    - Débil antes de 2024 y significativo después. La ruptura endógena cae a fines de 2023, ante la aprobación de los ETF spot.
    - Post-2024 (~115 lunes): +1σ del factor ≈ **+28% de varianza ajustada del lunes del S&P** (γ = 0.256, p = 0.005; ΔR² de 3.9 pp).
    - Fuera de muestra, QLIKE −22% en el S&P, pero con un Diebold-Mariano **marginal (p = 0.066)**.
    - La volatilidad cripto del viernes no reproduce el efecto. Los flujos de los ETF no lo amplifican: el mecanismo sigue sin resolverse.
  - **Grado: C.** Es un preprint. Tiene una sola muestra corta después de la ruptura y la ruptura se identifica dentro de esa misma muestra. La varianza del lunes es **dentro de la sesión** (Garman-Klass): **no incluye el hueco viernes→lunes**, que es lo que más importa para un stop.
- **Comprobación propia** (`conocimiento/cripto/fichas/2026-10-27-fin-de-semana-cripto-lunes.py`). Solo BTC, con el viernes como único control y sin HAR:
  - **post-2024:** 112 lunes, **corr = 0.413** (paper 0.41), **γ = 0.254** (t 2.81; paper 0.256) y **+30%** de varianza por 1σ;
  - **pre-2024:** 279 lunes, corr −0.01, γ 0.066 (t 1.57).
  - **Reproduce el patrón y la magnitud.**

## Qué cambia
- **Ninguna regla ni parámetro.**
- **Insumo para la supervisión del lunes** [inferencia]: después de un fin de semana de BTC muy volátil, la varianza intradía del S&P del lunes tiende a ser mayor. Eso aumenta la probabilidad de acercarse al stop del UPRO dentro de la sesión, no por el hueco de apertura. El paper no permite cuantificar el hueco.
- **Archivos:** adenda fechada en `conocimiento/cripto/05` y script de comprobación. No hay fila en el registro de errores.
