# Réplica R12: ¿la condición VIX ≥ 25 mejora o empeora el filtro del 3x? (prueba fuera de muestra)

> Fase 0: formación. No recomienda inversiones. Las secciones 1 a 9 son el pre-registro, escrito el 2026-10-17 (trabajo continuo de la noche del 16-oct, antes de cualquier corrida). La hora real es la del commit que agrega este archivo. **Lo aprobó el comité W42** (`bitacora/decisiones/2026-10-16-CARTERA-W42-mantener-y-VT.md`, punto 4) **solo para evaluación**: el filtro vivo del UPRO no cambia por este resultado sin una decisión nueva del comité.

| Campo | Valor |
|---|---|
| ID | `R12` (script `laboratorio/replicas/R12.py`; salida `R12-salida.txt`) |
| Hallazgo que se prueba | En R11 (S&P 500, 1990-2026, in-sample), quitar la condición VIX ≥ 25 dio Sharpe 0.65 contra 0.54 y MDD −58% contra −74%, con 32 salidas contra 108. Esa fue una variante entre cuatro, vista después de los datos. R12 la prueba **en datos que R11 no usó**. |
| Pre-registro escrito el | 2026-10-17, antes de cualquier corrida |
| Responsable | A: orquestador o laboratorio. B: `auditor-de-replicas`, código desde cero y otra fuente |
| Estado | pre-registrado (sin correr) |

**Conocimiento previo declarado:** conozco los resultados de R11 en el S&P 500 (arriba) y los de R06. **No** he corrido ninguna regla sobre el Nasdaq-100 ni sobre índices fuera de EUA con condición de VIX.

## PRE-REGISTRO (secciones 1 a 9; no se editan después de la primera corrida)

### 1. Hipótesis previa y mecanismo
- **H1:** en un 3x diario sintético del **Nasdaq-100** (fuera de muestra respecto a R11), la regla **sin condición de VIX** (salida: cierre < SMA200 × 0.97; entrada: cierre > SMA200 × 1.03) tiene un **Sharpe mayor** y una **MDD menor (menos negativa)** que la regla vigente con VIX (salida además si VIX ≥ 25; entrada además con VIX < 25). Periodo: 1990-2026.
- **H2:** la regla sin VIX tiene **al menos 40% menos salidas** que la vigente.
- **Mecanismo:** el VIX ≥ 25 se cruza muchas veces en correcciones cortas que revierten. Cada salida y reentrada vende abajo y recompra arriba, y paga costos. La SMA200 con banda es más lenta, pero tiene menos latigazos.

### 2. Criterio de refutación
- **H1 refutada** si la regla sin VIX tiene un Sharpe menor o igual que la vigente, **o** una MDD peor en más de 3 pp.
- **H2 refutada** si la reducción de salidas es menor a 40%.
- **Estado:**
  - H1 y H2 sostenidas: "Replicado". Confirma fuera de muestra lo visto en R11.
  - Solo H2 sostenida: "Replicado con diferencias".
  - H1 refutada: "No replicado". La condición de VIX se queda.
- **Prueba secundaria (informativa, no decide):** las mismas dos reglas sobre el S&P 500 **antes de 1990**, con VXO (`^VXO`, desde 1986) en lugar de VIX, de 1986 a 1989.

### 3. Datos
- **A:** Yahoo `^NDX` (diario, con `period1`/`period2` para obtener barras diarias), `^VIX` y FRED `DTB3`. 3x sintético = 3 × r_NDX − 2 × rf − 0.95%/252 (gasto de TQQQ, solo como referencia de costo).
- **B:** la elige el auditor. Puede ser FRED `NASDAQ100`, otra fuente del VIX (CBOE o FRED `VIXCLS`) o el TQQQ real como sensibilidad desde 2010.
- **Sesgo declarado:** ^NDX es un índice de precio, sin dividendos (~0.6-1% al año). Afecta por igual a las dos reglas.

### 4. Universo
Un activo: 3x sintético del Nasdaq-100. Es el índice más concentrado en tecnología, que es justo el riesgo que discutió el comité W42.

### 5. Fecha de disponibilidad
Señal con el cierre de t; ejecución al cierre de t+1. Sin información futura.

### 6. Periodo
Desde que hay 200 cierres comunes de ^NDX y ^VIX (VIX desde 1990-01-02) hasta el **16-oct-2026**. Subperiodos informativos: 1990-2008 y 2009-hoy.

### 7. Limpieza
Días sin dato de alguna serie se descartan y se reportan.

### 8. Reglas y variantes (N = 4)
- **V0 (vigente):** salida si < SMA200 × 0.97 o VIX ≥ 25; entrada si > SMA200 × 1.03 y VIX < 25.
- **V1 (principal contra V0):** solo SMA200 con banda ±3%, sin VIX.
- **V2:** como V0, pero el VIX ≥ 25 debe sostenerse **2 cierres seguidos** para salir.
- **V3:** como V0, con umbral de VIX ≥ 30.
- **Comparación simple:** comprar y mantener el 3x.

### 9. Costos
0.10% por lado. Fuera del mercado, el efectivo rinde la T-bill a 3 meses. USD, sin impuestos.

---

## RESULTADOS (se llenan después de correr)

> **Nota fechada (18-oct-2026, ~01:45 UTC, trabajo continuo), escrita DESPUÉS de la primera corrida.** [Corregido 18-oct-2026, conciliación, `bitacora/arbitraje/2026-10-17.md` §1: "~01:45 UTC" es imposible; esta nota entró en `374b203`, de las 01:17:13 UTC. La primera corrida es `bc59893` (01:12:22 UTC), 1 h 08 min después de que la revisión `f6ba0a0` (00:04:40 UTC) pidiera la enmienda **antes** de correr.] La revisión del 17-oct (hallazgo 1.1) pidió dos aclaraciones antes de correr la prueba, y no se hicieron a tiempo. Queda como error de proceso en `conocimiento/registro-de-errores.md`.
> 1. **Conocimiento previo no declarado en §1:** R06 (bloque J) ya había corrido TQQQ/QQQ con VIX en 2010-2026. Ese tramo se traslapa con el subperiodo 2009-hoy de esta prueba, donde V1 sí gana. El juicio pre-registrado (1990-2026) va en contra de ese antecedente, así que el sesgo de confirmación no favoreció el resultado.
> 2. **H1 contra §2:** §1 dice "MDD menor"; §2 tolera "no peor en más de 3 pp". El veredicto es el mismo con las dos lecturas: la MDD de V1 es ~17 pp peor.
> 3. **Contradicción interna de §2:** "solo H2 sostenida → Replicado con diferencias" choca con "H1 refutada → No replicado". Rige la lectura conservadora explícita, "No replicado". La primera corrida de A (commit `bc59893`) la tenía al revés y se corrigió en `b749995`.

### Ejecución A (orquestador): `R12.py`, `R12-salida.txt`, `R12-resultados.json`
Fuentes: Yahoo `^NDX` y `^VIX`, FRED `DTB3`. Son 9,266 días comunes, de 1990-01-02 al 2026-10-16. Métricas del 1990-10-17 al 2026-10-16.

| Variante | CAGR | Sharpe | MDD | Salidas | Invertido |
|---|---|---|---|---|---|
| V0 vigente (VIX ≥ 25) | +19.6% | 0.57 | −73.7% | 108 | 69% |
| V1 sin VIX | +25.0% | 0.64 | −90.8% | 30 | 76% |
| V2 VIX ≥ 25 dos cierres | +19.2% | 0.56 | −86.8% | 75 | 70% |
| V3 VIX ≥ 30 | +21.7% | 0.60 | −92.0% | 67 | 74% |
| 3x comprar y mantener | +17.2% | 0.56 | −100.0% | 0 | 100% |

Subperiodos (V0 contra V1):
- **1990-2008:** Sharpe 0.49 contra 0.55; MDD −73.7% contra −90.8%.
- **2009-hoy:** Sharpe 0.69 contra 0.76; MDD −63.2% contra −62.8%. Salidas: 53 contra 13.

Secundaria (informativa; `^GSPC` y FRED `VXOCLS`, del 1986-10-20 al 1989-12-29):

| Variante | CAGR | Sharpe | MDD | Salidas |
|---|---|---|---|---|
| V0 | +28.9% | 0.73 | −48.9% | 9 |
| V1 | −6.1% | 0.10 | −82.2% | 1 |

Las 108 salidas de V0 coinciden con las de R11 (S&P) porque casi todas las dispara el VIX, que es la misma serie en las dos pruebas. Las MDD difieren: −73.73% en R12 contra −73.66% en R11.

### Ejecución B (auditor-de-replicas, código desde cero): `laboratorio/auditorias/AC-21-R12/`
Fuentes: FRED `NASDAQ100`, `VIXCLS` y `DTB3`, hasta el 2026-10-15 (FRED tiene un día de rezago). Son 9,261 días comunes.

| Variante | CAGR | Sharpe | MDD | Salidas |
|---|---|---|---|---|
| V0 | 19.64% | 0.560 | −73.7% | 108 |
| V1 | 25.13% | 0.635 | −90.7% | 30 |
| V2 | 19.28% | 0.553 | −87.8% | 75 |
| V3 | 21.83% | 0.590 | −92.1% | 67 |
| 3x comprar y mantener | 17.04% | 0.565 | −100.0% | 0 |

Subperiodos y prueba secundaria de B (CBOE SPX y VXOCLS): concuerdan con A en signo y en orden de magnitud. En la secundaria, V0 da Sharpe 0.67 y MDD −48.9%; V1 da 0.07 y −82.2%.

### Juicio
- **H1 refutada en A y en B:** V1 sube el Sharpe (+0.07) pero empeora la MDD ~17 pp, por encima de la tolerancia de 3 pp. La pérdida viene del estallido de 2000-2002: la banda sola deja al 3x dentro de los rebotes bajistas.
- **H2 sostenida:** 72% menos salidas.
- **Estado (rige el más conservador; A y B concuerdan): "No replicado". La condición de VIX ≥ 25 se queda en la regla del UPRO de papel.**
- **Lectura conjunta con R11:** en el S&P 1990-2026, quitar el VIX mejoraba la MDD (−58% contra −74%). En el Nasdaq-100 la empeora (−91% contra −74%), y en el crash de 1987 también. El resultado de R11 no se generaliza fuera de muestra: la condición de VIX es un seguro barato contra crashes rápidos (1987, 2000-2002 en tecnología) a cambio de ~75 salidas extra en 36 años.
- **V2 y V3 no son alternativas:** las dos empeoran la MDD más de 13 pp contra V0.
- **Para el comité del 23-oct:** no hay base para cambiar la regla vigente.
- **Etiqueta:** descartada como cambio de regla. La regla vigente queda respaldada como protección.

### Fallo de la conciliación (18-oct-2026, `bitacora/arbitraje/2026-10-17.md` §1; no edita las secciones 1 a 9 ni las cifras)
- **Cronología (git):** pre-registro `c977758` (17-oct 01:10:51 UTC) → revisión `f6ba0a0` pide enmendar antes de correr (18-oct 00:04:40) → corrida A `bc59893` (01:12:22, estado "Replicado con diferencias") → `b749995` (01:13:46, estado a "No replicado" y secundaria) → nota y AC-21 `374b203` (01:17:13). **La enmienda se hizo después de la corrida.**
- **Las cifras son válidas:** A y B concuerdan con código y fuentes independientes. **H1 refutada** con las dos lecturas (MDD ~17 pp peor), y también solo en 1990-2008.
- **Estado "No replicado": se sostiene.** No es una elección hecha después de ver los datos: lo fija la escala de `laboratorio/README.md` L23 ("No replicado: se cumple el criterio de refutación pre-registrado", en git desde el 25-sep). Precedente: el fallo de R10 (`bitacora/arbitraje/2026-10-13-r10-estado.md`). La primera versión del código contradecía esa escala.
- **"Fuera de muestra": no lo es para el sistema, en ningún tramo.** El conocimiento previo no declarado va más allá de R06 J (2010-2026):
  - R06 bloque H (`ndx_sma200_L3`, ^NDX 3x 1986-2026, sin VIX) ya había medido una MDD de −96.14%, con pico el 27-mar-2000;
  - R06 post hoc (c) ya había comparado el 3x del Nasdaq-100 con y sin VIX: `posthoc_arena_k050_ndx_sma200_vix25_L3` dio MDD −65.96% (1990-2026) y `posthoc_arena_k050_ndx_sma200_L3` dio −74.27% (1986-2026).
  - **El resultado de R12 era previsible con lo que ya había en git.** Va en contra de la H1 del autor, así que el sesgo no lo favoreció. Pero **R12 cuenta como réplica de lo que ya se sabía (R06 H/J), con la banda de ±3% y exposición completa, y no como confirmación independiente fuera de muestra** de la condición de VIX.
- **Consecuencia:** la regla vigente no cambia (era el statu quo y el comité W42 aprobó R12 solo para evaluación). El hallazgo de R11 (S&P, dentro de muestra) **sigue sin una prueba limpia fuera de muestra**. Una prueba limpia necesitaría datos que el sistema no haya visto, por ejemplo índices fuera de EUA con su propio índice de volatilidad. Eso lo decide el comité del 23-oct; este fallo no lo pre-registra.
