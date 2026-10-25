# Réplica R18: con UPRO al 26.9%, ¿qué tan probable es tocar el cortacircuitos de −8% en un trimestre?

> Laboratorio del 21-oct-2026. Fase 0: no recomienda inversiones. **Pre-registro y script en el mismo commit, antes de correr.** sha256 de `R18.py`: `006e6f0c5c78b0ef0c6d0d40103d674ee2673196dc7219c1b4e194b9ea1e88b9`.

**Origen.** La pregunta abierta del aprendizaje del 20-oct: R16 y R17 mostraron que el riesgo del UPRO se controla con el tamaño, no con capas rápidas. El tamaño actual (26.9% del papel, decisión W40) nunca se contrastó con los cortacircuitos de `config/parametros.json`: −8% reduce el satélite a la mitad y −12% lo deja en cero.

**Conocimiento previo declarado:**
- R16 y R17: V0 en el 3x tiene una MDD de −73.7% en 1990-2026.
- El papel lleva 22 días con una MDD de −3.35%.
- No he medido la probabilidad de toque de la mezcla.
- **Expectativa propia:** entre 15% y 30% por trimestre con la mezcla vigente, por la beta efectiva de ~1.5x (nocional de 1.48x según W40).

## PRE-REGISTRO

### 1. Hipótesis
- **H1:** con la mezcla vigente, la probabilidad de caer 8% o más bajo el máximo dentro de 63 días hábiles es **≤ 15%** en 1990-2026. La mezcla es SPYM 41.0%, QQQM 26.8%, UPRO 26.9% con filtro V0 y efectivo 5.3%, rebalanceada al inicio de cada mes.
- **H2 (informativa):** bajar UPRO a 13.5% (el resto a SPYM) reduce esa probabilidad en **≥ 5 pp**.

### 2. Criterio y estado
- **H1 refutada** si la probabilidad es mayor a 15%.
- **Estado:** H1 sostenida, "Replicado"; refutada, "No replicado".
- **Consecuencia:** ninguna regla cambia en el laboratorio. Es insumo del comité sobre el tamaño del UPRO.

### 3. Datos
- **A:** la caché de R16 (Yahoo `^GSPC`, `^SP500TR`, `^VIX` y FRED DTB3, hasta el 16-oct-2026) y `^NDX` de la caché de R12. QQQM se aproxima con `^NDX` (precio, sin dividendos) menos 0.15% de gasto anual. SPYM, con `^SP500TR` menos 0.02%.
- **B:** la elige el auditor, distinta si es posible.

### 4. Instrumentos
- UPRO = 3x sintético (3·r_TR − 2·rf − 0.91%/252) cuando el filtro V0 está encendido, y T-bill cuando está apagado (igual que R16).
- Moneda: **USD**. No incluye el tipo de cambio, aunque el papel se mide en MXN. Sesgo declarado: el peso suele depreciarse en las caídas, lo que amortigua en MXN.

### 5. Disponibilidad
Filtro como en R16: señal del cierre de t−2 aplicada al rendimiento del día t.

### 6. Periodo y métrica
- **Periodo:** desde que existen todas las series hasta el 16-oct-2026. Subperiodos informativos: 1990-2008 y 2009-hoy.
- **Métrica:** para cada día de inicio t, ¿la curva cae ≥ 8% bajo su máximo desde t, dentro de t+1..t+63? Se reporta la fracción de días de inicio. Igual para 12%.

### 7. Limpieza
Los días sin dato de alguna serie se omiten.

### 8. Variantes (N = 4)
UPRO al 0%, 13.5%, **26.9% (vigente)** y 40%. QQQM (26.8%) y el efectivo (5.3%) quedan fijos; SPYM absorbe la diferencia.

### 9. Costos
Sin costos de rebalanceo: el rebalanceo es mensual y su costo es pequeño frente a la métrica. Sin impuestos.

---

## RESULTADOS (se llenan después de correr)

### Ejecución A (orquestador): `R18.py` (sin cambios desde el pre-registro, `1e12150`), `R18-salida.txt`, `R18-resultados.json`
9,065 días con todas las series (1990-10-17 a 2026-10-16); 9,003 ventanas de 63 días.

| UPRO | P(caer ≥ 8% en 63 días) | 1990-2008 | 2009-hoy | P(≥ 12%) |
|---|---|---|---|---|
| 0% | 29.5% | 32.2% | 26.7% | 14.8% |
| 13.5% | 36.4% | 37.9% | 34.9% | 16.4% |
| **26.9% (vigente)** | **47.8%** | 49.6% | 45.9% | 21.0% |
| 40% | 55.6% | 58.0% | 53.2% | 26.5% |

### Ejecución B (auditor-de-replicas, código desde cero): `laboratorio/auditorias/AC-24-R18/`
- **Datos:** CBOE SPX + multpl, CBOE VIX, DTB3, FRED NASDAQ100 y DEXMXUS. Son copias ya guardadas, porque FRED estaba en mantenimiento.
- **Muestra:** 9,184 días, hasta el 15-oct.
- **Control:** UPRO-V0 solo da MDD −72.6%, contra −73.5% / −73.7% de R16.

| UPRO | P ≥ 8% | 1990-2008 | 2009-hoy | P ≥ 12% | P ≥ 8% en MXN, 1994-hoy (USD, mismo periodo) |
|---|---|---|---|---|---|
| 0% | 29.7% | 32.5% | 26.9% | 15.3% | 30.8% (32.6%) |
| 13.5% | 36.7% | 38.2% | 35.2% | 16.6% | 33.9% (40.0%) |
| **26.9%** | **48.0%** | 49.7% | 46.2% | 21.4% | 42.8% (50.2%) |
| 40% | 56.1% | 58.4% | 53.7% | 26.9% | 52.3% (57.6%) |

Con ventanas sin traslape, B da 49.3% para la vigente.

### Juicio
- **H1 refutada en A y en B:** con la mezcla vigente, la probabilidad de tocar el cortacircuitos de −8% en un trimestre es **~48%**, más del triple del umbral de 15%.
- **H2 sostenida:** bajar UPRO a 13.5% la reduce 11.3 pp (8.9 pp en MXN).
- **Estado (A y B concuerdan): "No replicado".**
- **Lectura:** el −8% de `config/parametros.json` está dentro del ruido trimestral de una cartera de acciones. Incluso **sin UPRO**, la mezcla lo toca en ~30% de los trimestres. Con UPRO al 26.9%, cerca de uno de cada dos.
  - Los cortacircuitos se diseñaron como freno ante algo anormal. Con esta mezcla se dispararían por volatilidad normal, y cada disparo obliga a reducir el satélite a la mitad: vender abajo, la misma mecánica que R16 midió en el stop.
- **No es una recomendación de cambio.** Es insumo para el comité: ajustar el tamaño (UPRO a ~13.5% baja 11 pp) o recalibrar los niveles a la volatilidad de la mezcla. Las dos son decisiones del comité y del dueño (los cortacircuitos los fijó el dueño el 25-sep).
- **Etiqueta:** no aplica (calibración de riesgo, no prueba de ventaja).

## Adenda 2026-10-22 01:15 UTC (trabajo continuo) · perfil de riesgo correcto: `arena_agresivo`
> El pre-registro y los resultados de arriba no se editan. Esta adenda responde a la revisión del 21-oct §1.1 (`bitacora/decisiones-pendientes.md`, entrada de la revisión del 21-oct).

- **Hecho (error de etiqueta):** H1 y el juicio usan el −8% de `config/parametros.json` → `cortacircuitos_drawdown`, que es el perfil **estándar**. El papel GBM (`arena-claude`) corre con el perfil **`arena_agresivo`** (`config/parametros.json` → `perfiles_riesgo.arena_agresivo`; `herramientas/parametros.py`, `parametros_efectivos`). Sus niveles son: −12% reduce el táctico 50%, −20% sin ETF apalancados, −28% pausa 2 semanas y −35% límite duro. **En esta cuenta, −8% no dispara nada.**
- **El estado sigue "No replicado"**, porque H1 está escrita literalmente sobre el −8%. Lo que cambia es la lectura para el comité.
- **Recálculo con las funciones de `R18.py`** (`cargar`, `rendimientos`, `curva`, `prob_toque`; H = 63, ventanas traslapadas), sin modificar el script. Lado A (Yahoo), con B donde ya existía la cifra:

| UPRO | P(≥ 12%) A / B | P(≥ 20%) A | P(≥ 28%) A |
|---|---|---|---|
| 0% | 14.8% / 15.3% | 3.8% | 1.2% |
| 13.5% | 16.4% / 16.6% | 4.2% | 1.0% |
| **26.9% (vigente)** | **21.0% / 21.4%** | **3.1%** | **0.2%** |
| 40% | 26.5% / 26.9% | 4.1% | 0.0% |

- **Lectura corregida:**
  - El primer nivel aplicable (−12%) se tocaría en **~21% de los trimestres**, no en 48%. Sigue arriba del umbral de 15% del pre-registro, pero es de otro orden de magnitud.
  - Bajar UPRO a 13.5% quita **~4.6 pp** (no 11 pp). Sin UPRO, la mezcla aún lo toca en ~15%.
  - El nivel de −20% (el que quita los apalancados) queda en 3-4% en todas las variantes. No es monótono en UPRO porque el filtro V0 saca al 3x en las caídas largas; con n chico de episodios, esa diferencia es ruido.
  - P(≥ 20%) y P(≥ 28%) solo tienen lado A. Antes de usarlos para una decisión, falta que B los recalcule.
- **Para el comité del 23-oct:** leer esta adenda, no el 48%. El argumento "el primer nivel se dispara con la volatilidad normal" pierde fuerza. Queda una pregunta menor: ¿21% por trimestre es aceptable para un freno que recorta el táctico a la mitad?

> **[Conciliación 22-oct-2026 03:0x UTC, `bitacora/arbitraje/2026-10-21.md` §1] Adenda verificada; fallo vinculante para el comité del 23-oct.** Recalculé con código propio, escrito desde cero (no importa `R18.py` ni `R16.py`), y con datos de Yahoo bajados en esta corrida (^GSPC, ^SP500TR, ^VIX, ^NDX; DTB3 de la copia de AC-17, con el último dato arrastrado). Hay 9,001 ventanas al 14-oct. Con UPRO al 26.9%, P(≥ 8%) = 47.8%, **P(≥ 12%) = 21.0%**, P(≥ 20%) = 3.1%, P(≥ 28%) = 0.2% y P(≥ 35%) = 0.0%. Con 0%: 14.8 / 3.8 / 1.2%; con 13.5%: 16.4 / 4.2 / 1.0%; con 40%: 26.5 / 4.1 / 0.0%. **Las cuatro filas de la tabla de la adenda cuadran a la décima.** El recálculo es independiente en el código, no en la fuente de datos (es la misma fuente A). P(≥ 20%) y P(≥ 28%) siguen sin lado B. El pre-registro está intacto (`git diff 1e12150..79543d5` solo agrega líneas al final) y el estado sigue "No replicado" respecto de H1 literal (−8%). **Para el comité, la cifra aplicable es 21%, no 48%.** Además verifiqué que el código de reportes usa el perfil correcto: `riesgo.estado_cortacircuitos` con `parametros_efectivos("arena_agresivo")` da los niveles −12/−20/−28/−35%, y `portafolio.py reporte` imprime "Siguiente nivel: -12%".

### Nota 2026-10-22 18:2x UTC (laboratorio) · lado B de los niveles −20% y −28%
- El auditor recalculó P(≥ 20%) y P(≥ 28%) con su código de AC-24 (`auditorias/AC-24-R18/ac24_niveles_arena.py`, sin leer `R18.py`). P(≥ 12%) reproduce exactamente su cifra previa.
- **B (A):**

  | UPRO | P(≥ 20%) | P(≥ 28%) |
  |---|---|---|
  | 0% | 4.1% (3.8%) | 1.2% (1.2%) |
  | 13.5% | 4.4% (4.2%) | 1.0% (1.0%) |
  | **26.9%** | **3.5% (3.1%)** | **0.6% (0.2%)** |
  | 40% | 4.5% (4.1%) | 0.4% (0.0%) |

- **Concuerdan**, con una diferencia máxima de 0.4 pp. **Rige B** por ser la más conservadora: con la mezcla vigente, **P(−20%) = 3.5%** y **P(−28%) = 0.6%** por trimestre.
- **Por qué difieren en −28%:** abril de 2025 queda al filo de la regla del 0.97. B calcula la SMA200 solo con los días comunes a todas sus series, y a DTB3 le faltan dos días de 2024. Con la SMA sobre todos los días de SPX, B da 0.3% / 0.0%, como A.
- **La muestra es chica:** son 9 episodios que tocan −20% y 2 que tocan −28% (2008 y 2025). La falta de monotonicidad en UPRO también aparece en B: el filtro V0 recorta el episodio de 2008. Es ruido de n chico.
- Para el comité, la cifra aplicable sigue siendo **P(−12%) ≈ 21%**.

### Nota 2026-10-23 23:1x UTC (auditoría semanal W43, abogado del diablo) · la métrica no es la del cortacircuitos
- **El problema:** R18 mide la caída **bajo el máximo desde el inicio de cada ventana**. El cortacircuitos de `herramientas/riesgo.py` (L82-L89) mide contra el **máximo histórico de la cuenta**, y el papel ya está a −3.3% de su pico.
- **Recálculo del abogado** (solo lado A, grado C), con UPRO al 26.9%:

  | Medida | Con 26.9% | Con 13.5% |
  |---|---|---|
  | P(−12% en 63 días), sin condicionar | ~33% | — |
  | P(−12% en 63 días), con el drawdown de hoy | ~25% | ~17% |
  | P(−12% en 126 días) | ~45% | ~30% |

  Bajar el UPRO quita **~8-15 pp**, no 4.6. El tamaño del UPRO **no** controla la cola profunda: MDD de la mezcla −54/−58%, P(−20% en 12 meses) 25-27% con cualquier peso, y un día tipo 1987 (fuera de la muestra) ≈ −29%.
- **Estado:** sin cambio (H1 es literal). Hace falta que B recalcule con el máximo histórico antes del 30-oct. La decisión W43 (B1) sale **reforzada** en su dirección.

### Nota 2026-10-25 01:2x UTC (trabajo continuo) · lado B contra el máximo histórico (AC-24, adenda del 24-oct) [Conciliación 25-oct-2026 03:0x UTC, `bitacora/arbitraje/2026-10-24.md` §1] Hora por `git log`: la nota entró en `5dba311` a las **01:13:51 UTC** (código e informe en `f273735`, 01:13:12); "01:2x" es posterior al commit.]
- **B confirma al lado A del abogado** con su misma definición (11 celdas dentro de ±1.3 pp). Con la definición condicional al estado de hoy (pico de la cuenta = máximo de los 20 días hábiles previos y DD entre −2.8% y −3.8%), **rige B con L20, por ser la más alta**:

  | UPRO | P(−12%) 63 días | P(−12%) 126 días | P(−20%) 63 días | P(−20%) 126 días |
  |---|---|---|---|---|
  | **26.9% (antes de O0006)** | **28%** | **46%** | 5% | 17% |
  | 13.5% (después de O0006) | 22% | 34% | 6% | 18% |

- **El recorte quita 6.1 pp a 63 días y 12.1 pp a 126 días.** Es más que los 4.6 pp de la adenda del 22-oct y menos que los ~8-15 pp del abogado.
- **En −20%, el tamaño del UPRO casi no mueve nada** (14-18% a 126 días con 13.5%, 26.9% o 40%). La cola profunda la ponen SPYM y QQQM.
- **Muestra chica:** ~13 episodios de −12% y ~9 de −20% a 126 días. El ±3 pp no se cumple en la variante de 13.5% a 63 días; la diferencia viene de la definición del pico, no del código.
- **Corrige la nota del 23-oct:** "≈45% a 126 días" es la cifra condicional; la incondicional es 51.3% (B).
- **Estado sin cambio:** "No replicado" frente a H1 literal (−8%).
