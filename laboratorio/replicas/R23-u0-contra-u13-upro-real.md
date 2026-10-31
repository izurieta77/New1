# Réplica R23: ¿aporta el último UPRO (U13.5) frente a no tenerlo (U0)? UPRO real fuera de muestra y deriva del S&P como variable

> Trabajo continuo del 30-oct-2026 (CDMX; 01:1x UTC del 31-oct). Fase 0: no recomienda inversiones. **Pre-registro y script en el mismo commit, antes de correr.** sha256 de `R23.py`: `6c2150a602da3653f4581cb19b66a728862d0f8b589038916546cb484c67f812`.

| Campo | Valor |
|---|---|
| ID | R23 |
| Origen | Comité W44 (`bitacora/decisiones/2026-10-30-CARTERA-W44-U0-y-contingencia-binance.md`): "no hay reentrada al UPRO sin un R23 pre-registrado (U0 contra U13.5, μ de 5/7/9/11%, r 3.8%, fuera de muestra 2009-2026 con UPRO real)". Abogado del diablo W44 §2: "si en R23, con μ = 7%, U13.5 supera a U0 en ≥ 0.3 pp de CAGR sin sumar más de 3 pp a P(−12%), retiro la objeción". R21 declaró que no compara contra U0 (su nota contra U0 fue exploratoria y movía el peso a SPYM, no a efectivo) |
| Pre-registro escrito el | 2026-10-31 01:12 UTC, antes de cualquier corrida (el script solo se compiló con `py_compile`) |
| Commit | el commit que trae este archivo junto con `R23.py` |
| Responsable | orquestador (A); auditor-de-replicas (B, `auditorias/AC-30-R23/`) |
| Estado | pendiente de ejecución |

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
