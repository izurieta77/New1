# Arbitraje · 2026-10-11 · Pronósticos: formato de la probabilidad y umbral de P0100

Materia: un registro contra la regla de la herramienta y un verificador contra su autor. Son los hallazgos 3.2 y 3.3 de `bitacora/revisiones/2026-10-10.md`.

## 1. Formato de `probabilidad`
- **Hecho:** 11 de las 102 filas llevan 2 decimales: P0047, P0052, P0057, P0059, P0082, P0087, P0092, P0098, P0100, P0101 y P0102. P0101, además, pone entre comillas la probabilidad y la fecha. Las otras 91 filas llevan 4 decimales.
- **Regla:** `herramientas/pronosticos.py` L113 escribe `f"{p:.4f}"`. Las filas con 2 decimales se escribieron a mano, sin pasar por `agregar`.
- **Fallo:** el formato correcto es de 4 decimales y sin comillas. Normalicé las 11 filas. Comprobé con `csv` que solo cambió la columna 4 y que el valor numérico es el mismo. El Brier sigue en 0.2116 con n = 21. Reincide el hallazgo 3.6 del 9-oct.

## 2. Umbral de P0100 (MSTR, mNAV 1.0)
- **Autor (cripto):** 182.76, calculado con 848,000 BTC (8-K del 5-oct), 384,225,751 acciones ("10-Q del 30-jun-2026") y BTC a 82,822.01 (Binance, 14:25 UTC).
- **Revisor:** el recálculo da 182.79.
- **Fuente primaria consultada:**
  - SEC EDGAR, 8-K 0001193125-26-413164 (5-oct): "As of October 4, 2026 … Aggregate BTC Holdings 848,000". Verificado.
  - SEC EDGAR, 10-Q 0001050446-26-000044 (periodo al 30-jun): según la portada, "As of July 24, 2026, … 364,585,501 and 19,640,250 shares of class A … and class B". La suma da 384,225,751, así que la cifra es correcta pero su corte es el **24-jul-2026**, no el 30-jun. El balance al 30-jun da 351,963 + 19,640 miles = 371.6 M.
  - `data-api.binance.vision`: la vela 1m BTCUSDT de las 14:24 UTC cerró en 82,822.01. Verificado.
  - Yahoo: MSTR cerró en 154.34 el 9-oct, y el mNAV de 0.8444 es correcto.
- **Cálculo:** 848,000 × 82,822.01 / 384,225,751 = **182.791**. El 182.76 tiene un error aritmético del 0.017%.
- **Fallo:** el criterio literal de P0100 fija el número ("cierre ≥ 182.76 … el umbral queda fijo en dólares tal como se calculó hoy"), y un pronóstico se resuelve con su criterio literal. **El umbral se queda en 182.76.** En la fila dejé una nota fechada con el valor correcto de la definición (182.79) y con la fecha de corte correcta de las acciones. Si algún cierre cae en [182.76, 182.79), resuelve SÍ por el texto literal, y la nota deja constancia de esa diferencia. El punto del revisor sobre la emisión ATM posterior es un límite de método que ya está declarado; no lo fallo aquí.

## Correcciones
- `bitacora/pronosticos.csv`: 11 probabilidades normalizadas y una nota en P0100.
- `conocimiento/registro-de-errores.md`: dos filas.
