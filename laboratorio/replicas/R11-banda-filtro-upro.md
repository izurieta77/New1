# Réplica R11: banda de −3% en la salida del filtro de apalancados (regla vigente del UPRO de papel)

| Campo | Valor |
|---|---|
| ID | R11 |
| Artículo o hallazgo | Regla operativa del comité (boleta `bitacora/boletas/2026-10-05.md` y `config/parametros.json` → `perfiles_riesgo.arena_agresivo.filtro_apalancados`): **salir** del 3x si ^GSPC cierra < SMA200 × 0.97 **o** VIX ≥ 25; **entrar** solo con ^GSPC > SMA200 y VIX < 25. R06 (Gayed-Bilello) probó el filtro sin la banda de −3%; esta réplica mide el efecto de la banda. |
| Fecha de publicación (primera versión pública) | Regla aprobada el 5-oct-2026 |
| Pre-registro escrito el | 2026-10-13, antes de cualquier corrida |
| Responsable | A: orquestador (laboratorio). B: `auditor-de-replicas`, código desde cero y segunda fuente |
| Estado | Pendiente |

---

## PRE-REGISTRO (secciones 1 a 9; no se editan después de la primera corrida)

### 1. Hipótesis previa y mecanismo

- **Hipótesis.** Sobre un 3x diario del S&P 500, la regla con banda (salida a SMA200 × 0.97 o VIX ≥ 25; entrada con ^GSPC > SMA200 y VIX < 25) produce **menos salidas** que la regla sin banda (salida a SMA200 × 1.00 o VIX ≥ 25) **y no empeora la caída máxima en más de 5 pp ni el Sharpe en más de 0.05**.
- **Mecanismo.** Cerca de la media, el índice cruza muchas veces; cada salida y reentrada en un 3x paga costos y se pierde rebotes. La banda reduce cruces en falso a cambio de reaccionar un poco tarde.
- **Resultado declarado.** No hay artículo. R06 reportó que el filtro de 200 días es "solo protección" sobre el 3x.

### 2. Criterio de refutación

- **Métricas:** número de salidas, MDD, CAGR y Sharpe (rf = T-bill 3 meses), netos de costos, de la regla con banda contra la regla sin banda (misma condición de VIX); y de las dos contra comprar y mantener el 3x.
- **Refuta la hipótesis:** la banda **no** reduce el número de salidas, **o** empeora la MDD en más de 5 pp, **o** baja el Sharpe en más de 0.05, en el periodo completo.
- **Subperiodos:** 1990-2008 (3x sintético) y 2009-07 a hoy (UPRO real si la fuente lo permite; si no, sintético). Si el signo del efecto en Sharpe se invierte en un subperiodo: "Replicado con diferencias".

### 3. Datos y licencia

| Serie | Fuente A | Fuente B |
|---|---|---|
| S&P 500 (señal) | Yahoo `^GSPC` chart v8, diario | la elige el auditor (p. ej., Stooq `^spx` o FRED SP500 para el tramo disponible) |
| Rendimiento del subyacente para el 3x | Yahoo `^SP500TR` (total return) | la elige el auditor |
| VIX | Yahoo `^VIX` | CBOE (historia oficial de VIX) o FRED `VIXCLS` |
| Tasa libre de riesgo y financiamiento | FRED `DTB3` | la elige el auditor |

### 4. Universo

Un solo activo: 3x diario sobre el S&P 500 total return. Sintético: r3x = 3 × r_TR − 2 × rf_diaria − 0.91%/252 (gasto anual de UPRO). Sesgo: el S&P 500 es un índice sobreviviente; se declara.

### 5. Fecha de disponibilidad

Señal con el cierre del día t; ejecución al cierre del día t+1. Sin información futura.

### 6. Periodo

Desde que hay 200 cierres del S&P y datos de VIX (VIX desde 1990-01-02) hasta el último cierre disponible.

### 7. Limpieza

Días sin dato de alguna serie se descartan y se reportan.

### 8. Regla y variantes planeadas

- **Principal:** con banda (salida < SMA200 × 0.97 o VIX ≥ 25; entrada > SMA200 y VIX < 25), t+1.
- **Comparación directa:** sin banda (salida < SMA200 o VIX ≥ 25; misma entrada).
- **Variantes declaradas (2):** solo SMA200 con banda, sin VIX; banda de −5%. N = 4 configuraciones más comprar y mantener.

### 9. Costos y comparación simple

0.10% por lado (comisión + deslizamiento en un ETF muy líquido). Efectivo rinde la T-bill a 3 meses cuando se está fuera. Comparación simple: comprar y mantener el 3x. USD; sin impuestos.

---

## RESULTADOS (se llenan después de correr)

### Desviaciones del pre-registro

- Yahoo devuelve barras mensuales con `range=max`; A descarga con `period1`/`period2` desde 1989 (diario). El periodo efectivo empieza el 1990-10-17 (200 cierres comunes con VIX + 2 días de rezago de ejecución).

### 10. Variantes probadas

### 11. Resultados

**Ejecución A** (`R11.py`; Yahoo `^GSPC`, `^SP500TR`, `^VIX` y FRED `DTB3`; 9,262 días comunes del 1990-01-02 al 2026-10-12; sha256 `b55f0e60…`; salida en `R11-salida.txt`). 3x sintético: 3 × TR − 2 × rf − 0.91%/252; costo 0.10% por lado; rf fuera del mercado.

| Periodo | Configuración | CAGR | Sharpe | MDD | Salidas | Invertido |
|---|---|---:|---:|---:|---:|---:|
| 1990-10-17 → 2026-10-12 | **Vigente: banda −3% + VIX** | +15.4% | 0.54 | −73.7% | 108 | 75% |
| | Sin banda + VIX | +13.8% | 0.52 | −75.3% | 169 | 71% |
| | Banda −3% sin VIX | **+21.4%** | **0.65** | **−58.4%** | 32 | 81% |
| | Banda −5% + VIX | +14.3% | 0.51 | −79.5% | 104 | 76% |
| | 3x comprar y mantener | +18.7% | 0.54 | −97.9% | — | 100% |
| 1990-2008 | Vigente / sin banda | +13.6% / +10.7% | 0.46 / 0.39 | −73.7% / −75.3% | 47 / 87 | — |
| 2009-07 → hoy | Vigente / sin banda | +17.8% / +17.6% | 0.64 / 0.65 | −49.3% / −54.0% | 61 / 82 | — |
| 2009-07 → hoy | Banda −3% sin VIX / 3x B&H | +26.2% / +34.8% | 0.77 / 0.81 | −55.0% / −76.6% | 19 / — | — |

**Contra la hipótesis (vigente contra sin banda):** salidas 108 contra 169 (−36%); MDD 1.6 pp mejor; Sharpe +0.02. **No se refuta** en el periodo completo. Por subperiodo, el efecto en Sharpe es +0.07 (1990-2008) y −0.01 (2009-hoy): **cambia de signo**, así que el estado sería "Replicado con diferencias" (§2).

**Hallazgo no pre-registrado como hipótesis (variante):** la condición de **VIX ≥ 25 sin banda propia** genera la mayoría de las salidas (108 con VIX contra 32 sin VIX) y empeora todo: sin VIX, Sharpe 0.65 contra 0.54 y MDD −58% contra −74% en el periodo completo. Es una de N = 4 configuraciones; se reporta como candidato a investigar, no como cambio de regla.

**Ejecución B** (auditor, segunda fuente): en curso.

### 12. Sensibilidad

### 13. Diferencia frente al artículo

### 14. Conclusiones permitidas

### 15. Conclusiones que NO se sostienen

### 16. Estado y reproducción
