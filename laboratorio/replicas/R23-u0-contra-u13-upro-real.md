# Réplica R23: ¿aporta el último UPRO (U13.5) frente a no tenerlo (U0)? UPRO real fuera de muestra y deriva del S&P como variable

> Trabajo continuo del 30-oct-2026 (CDMX; 01:1x UTC del 31-oct). Fase 0: no recomienda inversiones. **Pre-registro y script en el mismo commit, antes de correr.** sha256 de `R23.py`: `6c2150a602da3653f4581cb19b66a728862d0f8b589038916546cb484c67f812`.

| Campo | Valor |
|---|---|
| ID | R23 |
| Origen | Comité W44 (`bitacora/decisiones/2026-10-30-CARTERA-W44-U0-y-contingencia-binance.md`): "no hay reentrada al UPRO sin un R23 pre-registrado (U0 contra U13.5, μ de 5/7/9/11%, r 3.8%, fuera de muestra 2009-2026 con UPRO real)". Abogado del diablo W44 §2: "si en R23, con μ = 7%, U13.5 supera a U0 en ≥ 0.3 pp de CAGR sin sumar más de 3 pp a P(−12%), retiro la objeción". R21 declaró que no compara contra U0 (su nota contra U0 fue exploratoria y movía el peso a SPYM, no a efectivo) |
| Pre-registro escrito el | 2026-10-31 01:12 UTC, antes de cualquier corrida (el script solo se compiló con `py_compile`) |
| Commit | el commit que trae este archivo junto con `R23.py` |
| Responsable | orquestador (A); auditor-de-replicas (B, `auditorias/AC-30-R23/`) |
| Estado | **Replicado** (B AC-30, 31-oct-2026; ver sección al final) |

**Conocimiento previo declarado:** R18 (3x sintético; U0 convención SPYM), R20 (brecha UPRO real −1.59 pp/año; −2.30 con DTB3 ≥ 3%), R21 (con la brecha, U13.5: P(−12%, 126 d) 30.43%, CAGR 13.083%; nota exploratoria vs U0-SPYM: +0.73 pp CAGR por +5.0 pp P(−12%)). Ficha del 27-oct: el 3x empata al 1x con μ ≈ 11.2% (r 3.8%, σ 17%) **antes del filtro** y sin mezcla. Expectativa honesta: en 1990-2026 (S&P TR ≈ 10-11%) U13.5 gana algo de CAGR a U0; con μ = 7% casi no gana o pierde; fuera de muestra 2009-2026 (μ ≈ 14%) gana claramente pero con más cola. **Sesgo declarado:** el resultado se usará en una decisión ya tomada (U0); los umbrales se fijan aquí para que no se muevan después.

## PRE-REGISTRO
### 1. Hipótesis (U13.5 frente a **U0-efectivo**: el 13.5% del UPRO pasa a efectivo a `rf`, como decidió W44; QQQM 26.8% y el efectivo de R18 (5.3%) fijos)
- **H1 (criterio del abogado del diablo):** en el contrafactual con deriva del S&P TR de **7%** nominal, la objeción a U13.5 **se sostiene**: ΔCAGR(U13.5 − U0-efectivo) **< 0.30 pp/año** **o** ΔP(−12%, 126 d) **> 3.0 pp**.
- **H2:** el μ de empate (ΔCAGR = 0, con la mezcla y el filtro) está entre **6% y 12%** nominal.
- **H3 (fuera de muestra, 2009-06-29 a 2026-10-23, UPRO real de R20):** U13.5 gana a U0-efectivo en CAGR por **> 1.0 pp/año** y le suma **≥ 3.0 pp** a P(−12%, 126 d). (Si gana sin sumar cola, la objeción pierde fuerza; si no gana ni en el mejor periodo del UPRO, la objeción se refuerza.)
- **H4 (validación del sintético):** en esa misma ventana, el CAGR de U13.5 con UPRO real difiere del de U13.5 con sintético + brecha por tramos en **≤ 0.50 pp/año** en valor absoluto.

### 2. Medidas
- CAGR, MDD, P(−12%) y P(−20%) a 126 días hábiles (toque contra el máximo de cada ventana, como R18/R21), para tres carteras: **U0-efectivo**, **U0-SPYM** (convención de R18, solo informativa) y **U13.5**.
- **Contrafactual de deriva:** se suma una constante diaria δ a los rendimientos brutos del S&P TR y del NDX (el mismo δ) tal que el CAGR del S&P TR en la muestra 1990-2026 sea μ ∈ {5, 7, 9, 11, 13}%. El 3x sintético usa el rendimiento desplazado: 3·(r₁+δ) − 2·rf − gasto − brecha por tramos de DTB3 (R20-A). `rf` no cambia (se reporta su media muestral). μ de empate por bisección entre 3% y 15%.
- **Fuera de muestra:** rendimientos diarios del UPRO real (adjclose de Yahoo en `R20-datos/series.json`, ya netos de gasto) en lugar del sintético; el UPRO solo se tiene cuando el filtro V0 de R16 está encendido; si no, esa fracción gana `rf` (igual que R21).

### 3. Criterio y estado
- Cada hipótesis se sostiene o se refuta con su umbral literal.
- **"Replicado"** si B, con código propio (sin importar R16/R18/R21/R23), concuerda en el veredicto de H1-H4 y su ΔCAGR con μ = 7% queda a ≤ 0.15 pp del de A y su ΔP(−12%) a ≤ 1.0 pp.
- **Etiqueta:** no aplica (calibración de riesgo); R23 no busca una ventaja sino el precio de una pata de la cartera.

### 4. Datos, reglas y sesgos declarados
- Datos: caché de R16 (S&P TR, VIX, DTB3; 1990-2026, sha256 `42339a50…466b`) y de R12 (^NDX); `R20-datos/series.json` (UPRO adjclose desde 2009-06-26). Nada se descarga.
- Rebalanceo mensual a pesos objetivo; costos anuales de R18 (UPRO 0.91%, SPYM 0.02%, QQQM 0.15%); sin impuestos ni comisiones de operación (R19b: ~1.3-1.5 pp/año de ISR para el libro en MXN, no se modela aquí).
- **Sesgos:** (1) la señal del filtro se calcula sobre el precio real; el δ solo desplaza rendimientos, no la señal (simplificación); (2) la brecha de R20 se midió en 2009-2026 y se aplica a 1990-2008; (3) el UPRO real empieza en 2009 (sin 2000-02 ni 2008); (4) μ = 7% es un supuesto, no un pronóstico; la ficha del 27-oct y el macro W44 lo usan como μ plausible; (5) los pesos (QQQM 26.8%, efectivo 5.3%) son los de R18, no los del libro de hoy (efectivo 18.9%, 32% tras O0008).

## RESULTADOS · Ejecución A (31-oct-2026 01:1x UTC, después del commit del pre-registro `feddc59` 01:13:12 UTC)
Datos: caché de R16 (sha256 `42339a50…466b`), 1990-10-17 a 2026-10-16, 9,065 días; `R20-datos/series.json` (UPRO real) sha256 en `R23-resultados.json`. S&P TR en la muestra: CAGR **11.615%**; `rf` media **2.627%**. Salida íntegra en `R23-salida.txt`.

### Histórico 1990-2026 (sintético con brecha por tramos, sin desplazar)
| Cartera | CAGR | MDD | P(−12%, 126 d) | P(−20%, 126 d) |
|---|---|---|---|---|
| U0-efectivo | 11.253% | −53.6% | 21.87% | 8.04% |
| U0-SPYM (informativa) | 12.357% | −58.3% | 25.46% | 9.37% |
| U13.5 | 13.083% | −57.0% | 30.43% | 12.60% |

U13.5 − U0-efectivo: **+1.83 pp/año de CAGR por +8.56 pp de P(−12%)** (y +4.6 pp de P(−20%)).

### Contrafactual de deriva (δ constante; `rf` fijo en su media muestral de 2.63%)
| μ del S&P TR | CAGR U0-efectivo | CAGR U13.5 | ΔCAGR (pp) | P(−12%) U0-ef / U13.5 | ΔP(−12%) (pp) |
|---|---|---|---|---|---|
| 5% | 5.864 | 5.632 | **−0.232** | 23.70 / 34.84 | +11.14 |
| **7%** | 7.499 | 7.878 | **+0.379** | 23.34 / 33.48 | **+10.14** |
| 9% | 9.129 | 10.130 | +1.001 | 22.60 / 33.02 | +10.42 |
| 11% | 10.754 | 12.388 | +1.634 | 21.88 / 31.39 | +9.51 |
| 13% | 12.374 | 14.652 | +2.278 | 21.77 / 29.09 | +7.32 |

**μ de empate (ΔCAGR = 0): 5.76%.**

### Fuera de muestra 2009-06-29 a 2026-10-16 (4,353 días; UPRO real)
| Cartera | CAGR | MDD | P(−12%, 126 d) | P(−20%, 126 d) |
|---|---|---|---|---|
| U0-efectivo | 13.611% | −26.4% | 18.95% | 3.41% |
| U0-SPYM | 15.429% | −30.6% | 22.92% | 5.18% |
| U13.5 (UPRO real) | 16.044% | −28.8% | 30.51% | 9.32% |
| U13.5 (sintético + brecha, mismas fechas) | 16.025% | −28.8% | 30.51% | 9.32% |

### Veredictos
- **H1 sostenida, pero por la segunda cláusula.** Con μ = 7%, ΔCAGR = **+0.379 pp** (≥ 0.30: la parte de rendimiento del criterio del abogado **no** se cumple) y ΔP(−12%) = **+10.14 pp** (> 3.0: la de cola sí). La objeción a U13.5 se sostiene porque el UPRO compra 0.38 pp/año con 10 pp más de probabilidad de un −12% semestral.
- **H2 refutada (por poco):** μ* = **5.76%**, debajo del rango [6%, 12%] pre-registrado. Lectura: con `rf` en 2.63% (media 1990-2026) y la mezcla con filtro, el 3x al 13.5% empieza a sumar CAGR desde un S&P de ~5.8%, mucho menos que el 11.2% de la ficha del 27-oct (que era 3x contra 1x sin filtro ni mezcla, con r = 3.8%). El filtro recorta la pérdida del 3x en los mercados bajistas y baja el umbral.
- **H3 sostenida:** fuera de muestra, U13.5 ganó **+2.43 pp/año** a U0-efectivo y le sumó **+11.56 pp** a P(−12%) (MDD −28.8% contra −26.4%). En el mejor periodo del UPRO (S&P ≈ 14%), el 3x sí pagó, y con la cola que se esperaba.
- **H4 sostenida:** |ΔCAGR real − sintético| = **0.019 pp**. **Salvedad:** no es validación independiente: la brecha de R20 se calibró en esta misma ventana, así que la coincidencia es casi por construcción (comprobación: 3,504 días con filtro encendido, correlación diaria real-sintético 0.9969, diferencia media +0.013 pp/año). Lo que sí confirma es que el motor de R23 usa el UPRO real y que la brecha de R20 está bien aplicada.

### Exploratorio (no pre-registrado; después de ver A)
Con `rf` desplazado a **3.8%** de media (el nivel de hoy) en el contrafactual: μ* = **7.06%**; con μ = 7%, ΔCAGR = **−0.018 pp** y ΔP(−12%) = +10.45 pp; con μ = 9%, +0.60 pp; con μ = 11%, +1.22 pp. Es decir, **a la tasa de hoy el último UPRO empata en rendimiento con un S&P del 7% y cuesta ~10 pp de probabilidad de −12% semestral en todos los μ**.

### Lectura para el comité (I)
- La decisión U0 de W44 **no dependía** de R23 y R23 no la contradice: para que el 13.5% de UPRO valga sus ~10 pp de cola hace falta creer en un S&P ≥ 9% nominal sostenido (ΔCAGR ≥ +0.6 a +1.0 pp con `rf` 3.8%). Con el μ de Vanguard/Morningstar (4-7%) o el 7% del macro W44, no suma.
- **Regla de reentrada propuesta (para el comité, no automática):** reentrar al UPRO solo si (a) el filtro V0 está encendido **y** (b) la tasa corta (DTB3) está ≤ 2.5% **o** el comité adopta por escrito un μ ≥ 9% con evidencia; nunca por "ya rebotó".
- Límite claro: R23 mide la cola con la métrica de R18 (máximo de cada ventana) y sin impuestos; R19b añade ~1.3-1.5 pp/año de ISR al libro en MXN, que castiga más a la pata que más rota.

## Doble ejecución independiente (31-oct-2026) · B, `auditorias/AC-30-R23/` (`ac30.py`, `salida.txt`, `informe.md`)
Código desde cero (biblioteca estándar; sin leer ni importar `R16.py`/`R18.py`/`R21.py`/`R23.py`); las mismas cachés que declara el pre-registro (sha256 de R16 `42339a50…466b`, R12 `44d25f4e…d466`, R20 `94226cbe…ee65`). 9,065 días (1990-10-17 a 2026-10-16); OOS 4,353 días (2009-06-29 a 2026-10-16; la caché de la señal termina el 16-oct, no el 23). Control: brecha UPRO real − sintético en OOS −1.593 pp/año (R20-A −1.592).

| | B | A | Diferencia |
|---|---|---|---|
| ΔCAGR U13.5 − U0-efectivo, μ = 7% | +0.380 pp | +0.379 pp | 0.001 (≤ 0.15) |
| ΔP(−12%, 126 d), μ = 7% | +10.05 pp | +10.14 pp | 0.09 (≤ 1.0) |
| μ* de empate | 5.76% | 5.76% | 0 |
| OOS real: ΔCAGR / ΔP(−12%) | +2.43 / +11.49 pp | +2.43 / +11.56 pp | 0.00 / 0.07 |
| H4: CAGR real − sintético+brecha | +0.019 pp | +0.019 pp | 0 |
| 1990-2026 U13.5: CAGR / MDD / P(−12%) / P(−20%) | 13.073 / −57.00 / 30.23 / 12.48 | 13.083 / −57.00 / 30.43 / 12.60 | 0.01 / 0 / 0.20 / 0.12 |
| 1990-2026 U0-efectivo | 11.244 / −53.60 / 21.73 / 7.97 | 11.253 / −53.60 / 21.87 / 8.04 | 0.01 / 0 / 0.14 / 0.07 |

- **Veredictos de B: H1 sostenida, H2 refutada, H3 sostenida, H4 sostenida.** Iguales a A.
- **Diferencias de nivel, explicadas y verificadas:** (1) B calcula el CAGR con años calendario y A con 252 días/año: con 252 d B reproduce el CAGR de A al milésimo en todas las celdas (−0.01 pp histórico, −0.03 pp OOS). (2) B mide el toque en ventanas de 126 puntos (t..t+125) y A en 127 (t..t+126, la lectura literal de R18): con 127 puntos B reproduce P(−12%) y P(−20%) de A al centésimo en las 12 celdas. MDD, δ y μ* coinciden sin ajuste. Ninguna diferencia toca un umbral.
- **Estado: Replicado** (H1-H4 concordantes; ΔCAGR a ≤ 0.15 pp y ΔP(−12%) a ≤ 1.0 pp). Independencia de código, no de datos.
