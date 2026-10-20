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

### Ejecución A (orquestador): `R16.py`, `R16-salida.txt`, `R16-resultados.json`
- **Datos:** Yahoo `^GSPC`/`^SP500TR`/`^VIX` y FRED DTB3: 9,266 días comunes, de 1990-01-02 al 2026-10-16. Descarga nueva; coincide con la caché de R11 sin diferencias (diferencia relativa máxima 0.00).
- **Desviación declarada:** el pre-registro decía "se reutiliza la caché de R11 y se extiende". Se bajó la serie completa porque la sensibilidad (a) necesita apertura y mínimo. Con el cotejo se demuestra que es la misma serie.

| Variante (1990-10-17 a 2026-10-16) | CAGR | Sharpe | MDD | Salidas (por stop) | Invertido |
|---|---|---|---|---|---|
| V0 filtro vigente | +15.2% | 0.537 | −73.7% | 108 (0) | 75% |
| S8 | +10.0% | 0.398 | −75.9% | 108 (32) | 64% |
| **S10.92 (vigente)** | **+9.8%** | **0.394** | **−76.1%** | 108 (18) | 65% |
| S15 | +14.6% | 0.520 | −75.5% | 108 (8) | 75% |
| S20 | +14.8% | 0.526 | −73.7% | 108 (1) | 75% |
| S10.92, disparo intradía (sens. a) | +10.0% | 0.397 | −71.5% | 108 (27) | 65% |
| S10.92, reentrada a 21 días (sens. b) | +15.4% | 0.543 | −72.0% | 110 (18) | 74% |
| 3x comprar y mantener | +18.5% | 0.538 | −97.9% | — | 100% |

- **Subperiodos:**
  - 1990-2008: V0 Sharpe 0.457 contra S10.92 0.116 (CAGR +13.6% contra +2.6%).
  - 2009-hoy: 0.616 contra 0.647 (MDD −49.3% contra −48.4%).
- **H2:** en 16 de los 18 stops (89%) el filtro V0 sale dentro de 21 días hábiles.
- **Por qué las salidas son 108 en todas las variantes:** con la reentrada por reinicio del filtro, cada ciclo del filtro tiene exactamente una salida, por stop o por filtro. No es un error.

### Ejecución B (auditor-de-replicas, código desde cero): `laboratorio/auditorias/AC-22-R16/`
- **Datos:** CBOE SPX más dividendos de multpl (rendimiento total aproximado), CBOE VIX y DTB3 de AC-17, completado con la tasa del Tesoro a 13 semanas (FRED no respondió). El SPX de CBOE coincide con FRED SP500 en 2,511 de 2,512 días.

| Variante | CAGR | Sharpe | MDD | Salidas (por stop) |
|---|---|---|---|---|
| V0 | 15.11% | 0.516 | −73.5% | 108 (0) |
| S8 | 9.88% | 0.378 | −75.9% | 108 (24) |
| **S10.92** | **9.71%** | **0.372** | **−76.0%** | 108 (17) |
| S15 | 14.44% | 0.499 | −75.4% | 108 (5) |
| S20 | 14.65% | 0.504 | −73.5% | 108 (1) |
| S10.92 reentrada 21 d | 15.23% | 0.522 | −71.9% | 110 (17) |
| 3x comprar y mantener | 18.15% | 0.533 | −97.9% | 0 |

- **H2:** 15 de 17 (88.2%).
- **De dónde sale el costo, según B:** dos stops tempranos, el 1994-12-08 y el 2018-03-23. Como la reentrada exige que el filtro se apague y se vuelva a encender, la cuenta queda fuera hasta 1997 y hasta fines de 2018.

### Juicio
- **H1 refutada en A y en B por los dos criterios.** Con el stop vigente la MDD empeora (−2.4 pp en A, −2.5 pp en B; se pedía mejorar ≥ 3 pp) y el Sharpe baja 0.14 (el tope era −0.03).
- **H2 sostenida:** ~89% de los stops son redundantes con el filtro.
- **Estado (A y B concuerdan): "No replicado".** En esta prueba, el stop fijo de −10.92% no agrega protección encima del filtro y cuesta rendimiento.
- **El costo depende de la reentrada:** con reentrada a los 21 días el Sharpe queda igual (0.543 / 0.522 contra 0.537 / 0.516) y la MDD mejora 1.6-1.7 pp. Tampoco llega a los 3 pp.
- **Disparo intradía (a), solo A:** mejora la MDD 2.2 pp, pero el costo en Sharpe es el mismo.
- **Consecuencia:** la regla no cambia en el laboratorio. El stop también es una regla de presupuesto de riesgo (3% del capital por operación, decisión W40) y su cambio lo decide el comité.
  - **Insumo para el comité del 23-oct:** con la evidencia de R16, el stop vigente funciona como un seguro caro y casi siempre redundante.
  - Si se conserva, la reentrada debería ser explícita y no esperar a que el filtro se reinicie. Hoy no está escrita y quedaría a discreción del comité.
- **Etiqueta:** descartada (el stop como mejora del filtro).

> **Nota fechada (20-oct-2026, trabajo continuo; revisión del 19-oct §2.7).** El pre-registro (`c067ef6`, 17:51:24 UTC) entró sin `R16.py`. El script se escribió y corrió después y entró en `3e16e02` (17:52:57 UTC), pero git no puede probarlo. Respaldo del resultado: la ejecución B (AC-22) se escribió desde cero a partir del pre-registro, sin ver `R16.py`, y concuerda. Desde hoy, la plantilla exige que el pre-registro y el script entren en el mismo commit.
