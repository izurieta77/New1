# Empresas chicas con utilidades: método pre-registrado, evidencia y primera pantalla

> 5-oct-2026. Pedido del dueño: "empresas chicas que nadie ve, con utilidades grandes y que podrían crecer fuerte, y saber cuándo entrar y salir". Fase 0: **papel**, esto NO es una recomendación de compra real. Solo información pública (REGLAS-MOTOR §0).
> Código: `conocimiento/fichas/codigo/2026-10-05-pantalla-chicas.py`. Salidas: `arena/investigacion/pantalla-chicas-2026-10-05.csv` (+ `-operabilidad.csv`, `-backtest.csv`, `.md`).

## 0. Registro previo (escrito ANTES de correr la pantalla y el backtest)

Esta sección se escribió y se congeló antes de ver cualquier resultado de la pantalla o del backtest (solo se conocían los conteos de las listas de la BMV). Los parámetros viven en el bloque `PARAMS` del script; si cambian después de ver resultados, el cambio se anota en §9 como desviación.

**Criterios de pantalla (todos obligatorios):**
| # | Criterio | Umbral |
|---|---|---|
| F1 | Tamaño (capitalización de mercado) | USD 300 M a USD 5,000 M |
| F2 | Utilidad neta | positiva en los 3 últimos ejercicios; NI(0) ≥ 1.2 × NI(−2); UDM positiva y ≥ 0.9 × NI(0) |
| F3 | Rentabilidad | ROIC ≥ 12% (EBIT × (1−t) / capital invertido) |
| F4 | Apalancamiento | deuda neta / EBITDA ≤ 2.0 (caja neta pasa); excluye financieras (sin EBIT/EBITDA comparable) |
| F5 | Caja | FCF (flujo operativo − capex) > 0 en el último ejercicio y en UDM; FCF/NI ≥ 0.6 |
| F6 | Precio | EV/EBIT ≤ 15 y EBIT > 0 |
| F7 | Dilución | acciones(0)/acciones(−2) ≤ 1.10 |
| F8 | Liquidez operable | mediana del importe diario (60 sesiones, serie .MX) ≥ 500,000 MXN; operó ≥ 90% de las sesiones; spread estimado (Corwin-Schultz) ≤ 1.5% |
| F9 | Título | precio de 1 título ≤ 2,500 MXN (25% de 10,000; el SIC no tiene fracciones) |
| F10 | Cobertura de analistas baja | **No hay dato gratuito verificable** (Yahoo quoteSummary exige credencial: HTTP 401). No se aplica; el tamaño máximo y la poca liquidez son el sustituto, y se declara. |

**Ranking de los que pasan:** promedio de rangos de ROIC (mayor mejor), crecimiento anual compuesto de NI a 2 años (mayor mejor) y EV/EBIT (menor mejor). Se reportan ≤ 15.

**Tamaño de posición (10,000 MXN por IA):** máximo 2,500 MXN (25%) por posición; objetivo 4-6 posiciones de 1,500-2,000 MXN; títulos completos; nunca más del 2% del importe diario mediano del título.

**Entrada:** solo después de que sale un reporte (10-K/10-Q) cuyo UDM pasa los filtros; orden limitada ≤ último cierre + 0.5%; dos tramos (50% ahora, 50% a 20 sesiones salvo que el precio haya caído > 10%, caso en que se revisa la tesis en vez de promediar); no se entra en las 5 sesiones previas al siguiente reporte esperado.

**Salida y alertas (se escriben antes de entrar):**
1. Stop duro: cierre −25% contra el costo.
2. Deterioro: tras cada reporte, si UDM NI < 0.75 × UDM del año previo, o FCF UDM < 0, o deuda neta/EBITDA > 3 → vender en ≤ 5 sesiones.
3. Evento legal inmediato (8-K ítems 1.03 quiebra, 3.01 aviso de deslistado, 4.01 cambio de auditor, 4.02 no confiar en estados, 2.04/2.06 aceleración de deuda o deterioro): salir el siguiente día hábil.
4. Dilución: acciones +10% en 12 meses u oferta secundaria > 10% → revisar y, si la tesis no cambia con el nuevo número de acciones, salir.
5. Valuación: EV/EBIT > 22 → vender la mitad.
6. Liquidez: mediana del importe diario < 250,000 MXN → salir.
7. Tiempo: 24 meses máximo; revisión obligatoria a los 12.

**Criterio de refutación (sobre el backtest, costos incluidos):** el método se descarta para papel si, en las fechas de formación probadas, (a) el exceso medio anual NETO (costo de ida y vuelta supuesto 2.0%: 0.58% comisión + 1.4% spread/impacto) contra el grupo de control (empresas del mismo rango de tamaño con utilidad neta positiva, muestra aleatoria con semilla) es ≤ +2 pp, o (b) en menos de 55% de los años gana al control, o (c) el límite inferior del intervalo bootstrap de 80% (por año) del exceso neto es < 0. Forward en papel: con ≥ 12 posiciones cerradas, si el exceso neto medio es ≤ 0 contra IWM convertido a MXN, se archiva.

**Diseño del backtest:** formación el 30-jun de 2015 a 2025 (11 fechas), con el último ejercicio anual completo conocido (período terminado ≥ 90 días antes y accesión del año de formación o anterior), retención de 12 meses, equiponderado. Datos: SEC EDGAR XBRL `frames` (fundamentales) y Yahoo chart v8 (precios; rendimiento con cierre ajustado; capitalización con precio sin ajustar por splits posteriores × acciones diluidas promedio). **Sesgos declarados de antemano:** (1) supervivencia: solo hay precios de Yahoo para tickers vigentes, así que las quiebras y deslistados no aparecen; se cuantifica y se hace un análisis de sensibilidad; (2) `frames` entrega el valor más reciente presentado (reexpresiones: ligera anticipación); (3) liquidez histórica: se usa importe diario en USD ≥ 1 M (60 sesiones previas) como sustituto; (4) solo ejercicios anuales (sin UDM); (5) la muestra de control es aleatoria; (6) poder estadístico bajo (pocas fechas, rendimientos solapados).
