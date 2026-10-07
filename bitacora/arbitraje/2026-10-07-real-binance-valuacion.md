# Arbitraje · 2026-10-07 (conciliación de la noche del 6-oct)

## Caso: el libro real de Binance nunca se revalúa a mercado, a diferencia del libro de papel

**Los hechos:**
- `bitacora/real-binance/equity.csv` tiene una sola fila, la del **30-sep-2026** (fecha de apertura de la posición: 0.001325 BTC, efectivo 3,001.83 MXN, equity 4,995.30 MXN, índice 100). No se agregó ninguna fila más desde entonces: hoy, 7-oct, el archivo sigue exactamente igual.
- `competencia/rivales.csv` repite el mismo patrón: la última fila de `arena-claude-binance` (real) es la del 30-sep (4,995.30 MXN). `competencia/marcador.md` cita ese mismo valor como el estado de la cuenta real de Binance, con "días invertidos: 1", sin que ese contador avance.
- `rutinas/REGLAS-MOTOR.md` §4b dice que el libro real "según lo que reporte el dueño" — eso rige para **registrar ejecuciones** nuevas (correcto: sin una operación nueva que el dueño reporte, no hay nada que registrar). Pero **valuar a mercado una posición ya abierta no depende de que haya una operación nueva**: es exactamente la misma situación que ya se corrigió para el libro de **papel** de Binance el 1-oct-2026 (`bitacora/arbitraje/2026-10-01-papel-binance-valuacion.md`), que desde entonces se revalúa cada cierre aunque no haya orden nueva.
- Ninguna rutina escrita (`rutinas/diaria-cierre.md` §2, `rutinas/cripto.md`) manda revaluar `bitacora/real-binance/equity.csv`. El resultado práctico: la cuenta real (dinero real del dueño, con tope de pérdida de 5,000 MXN) lleva **7 días sin una valuación nueva**, más que el papel-binance en su peor racha (3 días, escalada el 3-oct).
- **Esto no compromete el control de riesgo en vivo:** `herramientas/supervision.py::revisar_libro` reconstruye el libro real desde `operaciones.csv` con el precio de BTC y el tipo de cambio **en vivo** en cada corrida (no depende de `equity.csv` para el cortacircuito ni para el tope absoluto), confirmado leyendo el código. El problema es de **reporte** (TWR, drawdown y "días invertidos" en `marcador.md`/`rivales.csv` quedan congelados), no de seguridad.
- Verificación de la alerta de BTC de hoy (02:11 UTC, `bitacora/alertas.md`): la aritmética de ambos libros cuadra. Papel-binance 0.002698 BTC: 85,786.59×18.0616×0.002698 ≈ 4,183.9 MXN (5-oct) → 83,968.13×18.0084×0.002698 ≈ 4,079.7 MXN (hoy), igual que la alerta (≈4,183→≈4,079). Real-binance 0.001325 BTC: 85,786.59×18.0616×0.001325 ≈ 2,053.0 MXN → 83,968.13×18.0084×0.001325 ≈ 2,003.6 MXN, igual que la alerta (≈2,053→≈2,004). La fila de `papel-binance/equity.csv` del 6-oct (posiciones 4,145.61 MXN) usa el precio de BTC de la hora del cierre de mercado (21:38 UTC, BTC≈85,565.75), **anterior** a la caída documentada entre 00:00 y 02:09 UTC del 7-oct; no es una cifra contradictoria, es un corte más temprano del mismo día.

**Por qué es arbitraje:** es una regla incompleta (cubre el libro de papel de Binance pero no el real, que tiene el mismo tipo de posición y la misma necesidad de mark-to-market), no una decisión de inversión ni un cambio de parámetro de riesgo.

**Fallo:**
1. No se fabrica ninguna fila retroactiva para el 1 al 6-oct: el precio exacto de cada uno de esos días ya no se puede fijar con la misma vela que se habría usado en vivo ese día (mismo criterio ya aplicado al papel-binance el 30-sep/1-oct).
2. Se corrige la regla hacia adelante: agregué a `rutinas/diaria-cierre.md` §2 la instrucción explícita de valuar también `bitacora/real-binance/equity.csv` cada cierre, con el mismo cuidado de no guardar un precio de vela incompleta.
3. Se deja una nota fechada en `competencia/marcador.md` junto a la fila de `arena-claude-binance (real)` para que no se lea como un valor del día de hoy.
4. Se registra en `conocimiento/registro-de-errores.md` como una omisión de cobertura (no una cifra equivocada: las cifras citadas hasta hoy —4,995.30 MXN al 30-sep— son correctas para su fecha, solo faltó actualizarlas).

**Efecto:** ninguna cifra ya publicada cambia. El hueco de cobertura queda documentado y cerrado hacia adelante; la primera fila nueva de `bitacora/real-binance/equity.csv` la debe dejar la próxima corrida de Cierre (día hábil) que corra con la regla ya corregida.
