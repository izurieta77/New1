# Decisor vespertino · 2026-10-14 (corrida 19:27 CDMX del 14-oct; ejecución 01:27 UTC del 15-oct)

**Pregunta:** ¿alguna alerta de hoy amerita actuar antes del viernes 16-oct?
**Respuesta:** No. Ninguna regla de riesgo se disparó y no hay orden nueva.

## Revisado
- **`bitacora/alertas.md`, Alta del vigía (17:10 UTC; actualizada al cierre):**
  - El UPRO de papel cruzó −2% en pesos (regla §3 de inteligencia). Cerró en 150.36 USD: −3.24% en USD y −2.59% en pesos, ≈ −148 MXN en 2 títulos.
  - Causa: el CPI de septiembre caliente (+0.6% m/m general, 3.7% a/a) con caída de megacaps y semiconductores.
  - Es una alerta **informativa**: no toca stop, cortacircuitos ni filtro. El stop de 135.76 queda a **10.8%**; el filtro se cumple (^GSPC 7,718.94 contra SMA200 × 0.97 ≈ 7,046; VIX 16.87 < 25).
- **Papel GBM:** drawdown −1.66% desde el pico del 9-oct; el primer cortacircuitos está en −12%. Sin rachas.
- **Supervisión del 14-oct (última):** sin stops, cortacircuitos ni órdenes vencidas.
- **Cripto (cascada vespertina):** filtro BTC ENCENDIDO, SMA200 72,243; salida en 70,076, lejos del precio.
- **`herramientas/fx_alerta.py`:** `OK · FX-1 OK · sin disparo nuevo`, USD/MXN 18.4817, Δ10 +2.24%. Para la fecha de cálculo del script, la ALERTA pediría ≥ 18.5938 por episodio o ≥ 19.3607 por Δ10. Según la revisión, para el 15-oct el nivel de episodio sube a ≈ 18.803.

## Decisión
- **Sin acción antes del viernes.** Sin boleta ni cambio de cartera (REGLAS-MOTOR §4).
- La baja del UPRO es la volatilidad esperada de un 3x en un día de −1.1% del S&P 500 (3 × −1.11% ≈ −3.3%), sin señal de régimen. Va al comité del 16-oct como contexto, junto con la propuesta R12 sobre la condición de VIX y el destino del efectivo.
