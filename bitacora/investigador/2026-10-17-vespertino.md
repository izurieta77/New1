# Investigador, corrida vespertina · 2026-10-17 (20:12 CDMX; 2026-10-18 02:14 UTC del 18-oct)

**Barrido corto, turno de reglas de riesgo.** Rotación: 14-oct riesgo, 15-oct cripto, 16-oct fiscal. El tema se dirigió al resultado de R12 de hoy: la condición VIX en el filtro de tendencia de apalancados.

## Búsquedas
- La API de arXiv respondió **"Rate exceeded"** a las tres consultas, con 4 s entre una y otra. Igual que el 15-oct; no reintenté en bucle.
- Hice una búsqueda web: VIX, filtro de tendencia y ETF apalancados en 2026. No apareció ningún paper de arXiv que combine las tres cosas.

## Fuente revisada (una)
- **Quantpedia, "Leveraged ETFs in Low-Volatility Environments"** (2025), basado en Zarattini, Mele y Aziz (2025), *The Volatility Edge: A Dual Approach for VIX ETNs Trading*, SSRN 5316487. Ese paper trata de ETNs de VIX, no de apalancados.
  - **Regla:** invierte en SPXL (3x) un día solo si la media de 60 días del VIX (con 1 día de rezago) supera la volatilidad realizada de 10 días del SPY.
  - **Resultado:** según el texto, rinde "el doble" que SPY, pero con más volatilidad y caídas, y un Sharpe algo menor. La mejor de varias combinaciones (10/10) llega a un Sharpe "cercano a 1" y un Calmar "casi 0.9". Las tablas son imágenes; no copié cifras que no pude leer.
  - **Grado D para nuestra regla:**
    - la muestra es solo 2013-2025, sin 1987, 2000-2002 ni 2008, que es justo donde R12 encontró el valor de la condición VIX;
    - eligió parámetros entre varias variantes, sin pre-registro;
    - su Sharpe va sin tasa libre de riesgo;
    - compara contra SPY, no contra el 3x filtrado.
  - **Mecanismo distinto al nuestro:** usa la prima de volatilidad (VIX implícito contra realizado), no un umbral absoluto de VIX.
- **No verificado:** arXiv 2606.09025 (overlays de efectivo para control de caídas, 2017-2026). Solo vi un fragmento del resumen, así que no cuenta.

## Qué cambia
**Nada.** No hay adenda ni corrección: la evidencia es más débil (D) que R11, R12 y R06, todas replicadas con doble ejecución. Una posible prueba futura para la cola del laboratorio, de baja prioridad: el filtro de prima de volatilidad sobre el 3x del S&P y del Nasdaq en 1990-2026, con el mismo diseño que R12 y pre-registro antes de correrlo. No se propone ningún cambio de regla.
