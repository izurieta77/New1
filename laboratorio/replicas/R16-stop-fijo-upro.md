# Réplica R16: ¿el stop fijo del UPRO de papel agrega algo encima del filtro de tendencia? (marco de Kaminski y Lo, 2014)

> Laboratorio del 19-oct-2026. Fase 0: no recomienda inversiones. Pre-registro en git **antes** de cualquier corrida (secciones 1 a 9; no se editan después de la primera corrida).

**Origen.** La decisión W40 (`bitacora/decisiones/2026-10-02-CARTERA-W40-modo-C-moderado.md`) metió 2 UPRO de papel con un **stop obligatorio en el precio de ejecución × 0.8908 (−10.92%)**, dimensionado para arriesgar 3% del capital. Hoy está en 135.76 USD. El filtro de tendencia está probado (R06, R11, R12). **El stop nunca se ha probado.** Kaminski y Lo (2014, *J. Financial Markets* 18, 234-254; capítulo 07, L143) dan el marco: un stop suma cuando los rendimientos tienen momentum y resta cuando son independientes o revierten.

**Conocimiento previo declarado:**
- **Resultados que conozco:**
  - R06: el filtro SMA200 da "solo protección" en apalancados.
  - R11 (S&P 3x, 1990-2026): la regla vigente tiene Sharpe 0.54, MDD −73.7% y 108 salidas.
  - R12 (Nasdaq 3x): la condición VIX se queda. El fallo de la conciliación del 18-oct sobre R12 pide declarar todo lo previo.
  - El marco de Kaminski y Lo (cap. 07).
  - La nota de `config/parametros.json` sobre stops intradía en BTC (se disparan en 21-74% de las trayectorias).
- **Lo que no he hecho:** **no he corrido ninguna regla de stop-loss** sobre un 3x ni sobre el S&P. `grep` de "stop" en R06 y R11: sin resultados.
- **Expectativa propia (antes de correr):** con el filtro ya puesto, el stop de −10.92% se dispara pocas veces en caídas largas (el filtro sale antes) y con más frecuencia en caídas rápidas con VIX bajo. Espero un efecto pequeño en la MDD y algo de costo en Sharpe. No tengo cifra.

## PRE-REGISTRO

### 1. Hipótesis y mecanismo
- **H1 (la justificación de la regla):** agregar el stop vigente (−10.92% desde el precio de entrada) a la regla V0 **mejora la MDD en al menos 3 pp** y **no baja el Sharpe más de 0.03**. 3x sintético del S&P 500 TR, 1990-10 a 2026-10-16.
- **H2 (redundancia):** en al menos 50% de las salidas por stop, el filtro V0 por sí solo habría salido en los 21 días hábiles siguientes.
- **Mecanismo:** un 3x pierde 10.92% con una caída de ~3.7% del índice, algo frecuente en correcciones normales.
  - Si las caídas tienden a seguir (momentum de corto plazo), el stop sale antes que la SMA200 y ahorra pérdidas.
  - Si revierten, vende abajo y vuelve a entrar arriba.

### 2. Criterio de refutación y estado
- **H1 refutada** si la mejora de MDD es menor a 3 pp **o** el Sharpe baja más de 0.03.
- **H2 refutada** si la proporción es menor a 50%.
- **Estado** (escala de `laboratorio/README.md` L23):
  - H1 sostenida: **"Replicado"** (el stop se justifica en esta prueba).
  - H1 refutada: **"No replicado"**.
  - H2 es informativa y no cambia el estado.
- **Consecuencia:** ninguna regla cambia en el laboratorio. El stop también es una regla de presupuesto de riesgo (3% por operación) y lo decide el comité.

### 3. Datos
- **A:** Yahoo `^GSPC` (señal), `^SP500TR` (rendimiento), `^VIX` y FRED `DTB3`. Se reutiliza la caché de R11 (`R11-datos/series.json`, hasta el 12-oct-2026) y se extiende al 16-oct con una descarga nueva. Se reportan los sha256.
- **B:** la elige el auditor, distinta de A si es posible (por ejemplo, CBOE SPX, multpl o FRED). Código desde cero.
- **Sensibilidad intradía (solo A):** máximo y mínimo diarios de `^GSPC`.

### 4. Universo e instrumento
3x diario sintético del S&P 500 TR: r3 = 3·r_TR − 2·rf − 0.91%/252, el gasto de UPRO. Mismo que R11.

### 5. Disponibilidad
- **Señal del filtro:** cierre de t, ejecución al cierre de t+1 (igual que R11).
- **Stop:** se evalúa con el cierre del 3x del día t (variante principal) y se ejecuta al cierre de t. Es el caso conservador de una orden stop que se revisa una vez al día.

### 6. Periodo
Desde 200 cierres comunes de `^GSPC` y `^VIX` (VIX desde 1990-01-02) hasta el 16-oct-2026. Subperiodos informativos: 1990-2008 y 2009-hoy.

### 7. Limpieza
Los días sin dato de alguna serie se descartan y se reportan.

### 8. Reglas y variantes (N = 4 niveles de stop, más V0)
- **V0 (filtro vigente, como en R11):**
  - salida si `^GSPC` < SMA200 × 0.97 o VIX ≥ 25;
  - entrada si `^GSPC` > SMA200 y VIX < 25.
- **S8, S10.92 (principal), S15 y S20:** V0 más un stop fijo de 8%, 10.92%, 15% o 20% bajo el valor del 3x en la entrada.
  - El stop **no** es móvil: se fija en cada entrada.
  - **Reentrada tras un stop:** solo cuando el filtro V0 da una **señal de entrada nueva después de haber estado apagado** (reinicio completo). Es el equivalente mecánico de "lo retoma el comité" y evita recomprar al día siguiente.
- **Sensibilidades (solo para S10.92, no deciden):**
  - (a) disparo intradía: el mínimo del día del 3x ≈ 3 × (mínimo de `^GSPC` / cierre previo − 1). Si toca el stop, la salida es al nivel del stop, o a la apertura aproximada si abre por debajo;
  - (b) reentrada a los 21 días hábiles si el filtro sigue encendido.
- **Comparación simple:** comprar y mantener el 3x.

### 9. Costos
0.10% por lado. Fuera del mercado, el efectivo rinde la T-bill. USD, sin impuestos.

---

## RESULTADOS (se llenan después de correr)
