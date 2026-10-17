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
