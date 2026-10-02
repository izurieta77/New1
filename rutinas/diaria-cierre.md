# Rutina 3 · Cierre de mercado (L-V, 15:37 hora del centro de México)

Este procedimiento escrito manda sobre el texto del disparador, que ya indica seguirlo si existe.

0. Tras el `git pull --rebase --autostash`, lee `rutinas/REGLAS-MOTOR.md` y cúmplelo: autonomía, bloqueos, latido y pendientes (§7). Si §7 tiene pendientes, hazlos aquí.
1. **Ejecuta las órdenes pendientes.** En `bitacora/ordenes-pendientes.csv`, toma las órdenes con `estado=pendiente` cuya `fecha_ejecucion` ya llegó y ejecútalas en papel según REGLAS §4:
   - **Precio:** la apertura de ese día en Yahoo (chart v8, campo `open`). **Si la fila trae su propia `regla_precio`** (condición de validez, hora o títulos fijos), **manda la fila**; si su condición no se cumplió, márcala `en_espera` y no la ejecutes.
   - **Comisión:** 0.29% del monto.
   - **Depósito inicial:** 20,000 MXN el día de la primera ejecución.
   - **Cantidad:** los títulos se calculan como monto ÷ (precio × FX si cotiza en USD), redondeando hacia abajo a unidades enteras. El sobrante queda en efectivo.
   - **Registro:** marca cada orden como `ejecutada`, con precio, cantidad y commit.
   - **Las filas con `clase=cripto` no son tuyas:** las ejecuta la rutina cripto en `bitacora/papel-binance/`.
2. **Valúa el portafolio de papel al cierre:** corre `python3 herramientas/portafolio.py valuar` y `reporte` y actualiza `bitacora/equity.csv`. **Haz lo mismo con el libro de papel de Binance** (`python3 herramientas/portafolio.py --perfil cripto_binance --operaciones bitacora/papel-binance/operaciones.csv --equity bitacora/papel-binance/equity.csv valuar`), aunque no haya orden nueva ese día: es la práctica ya seguida el 28 y 29-sep-2026 y evita que `competencia/marcador.md` quede con el índice de Binance desactualizado respecto al de GBM (hallazgo de la conciliación del 2026-10-01, que encontró un día sin esa fila). Si el precio de BTC-USD de Yahoo para el día viene incompleto o nulo (le pasa a veces a los pares 24/7 justo después de medianoche UTC), reintenta antes de guardar; si sigue incompleto, dilo en el brief y deja la fila pendiente para el día siguiente en vez de guardar un precio de un día distinto con la fecha de hoy. **Nota fechada 2026-10-02 (conciliación):** el 1-oct esta instrucción no se cumplió — la corrida de cierre de ese día no tocó `bitacora/papel-binance/equity.csv` (ni para registrar el día ni para avisar que el dato venía incompleto) y el brief atribuyó la valuación a la rutina cripto, que no la hace salvo que haya una orden nueva. Resultado: dos filas faltantes seguidas (30-sep y 1-oct). Fallo completo en `bitacora/arbitraje/2026-10-02-papel-binance-incumplimiento.md`. **Para que esto se note de inmediato la próxima vez:** la sección "Cierre" del brief del día (paso 6) debe citar explícitamente la fecha de la fila de `bitacora/papel-binance/equity.csv` que acabas de guardar hoy (no solo el valor), aun si el valor no cambió; si no pudiste guardar una fila nueva, dilo con esas palabras ("papel Binance: sin fila nueva hoy, [razón]") en vez de reportar en silencio el último valor conocido como si fuera del día.
3. **Revisa límites y cortacircuitos** del perfil `arena_agresivo` (`herramientas/riesgo.py`). Si se dispara uno, genera en `ordenes-pendientes.csv` las órdenes de reducción que manda el perfil, para la apertura siguiente, y anótalo en el brief.
4. **Empresas de `empresas/universo.csv` que reportaron hoy:**
   - obtén los resultados oficiales;
   - resuelve sus pronósticos numéricos y binarios (`herramientas/pronosticos.py`);
   - escribe `empresas/<TICKER>/post-mortem-AAAA-MM-DD.md` con la skill `post-mortem`;
   - actualiza la ficha con una adenda fechada, sin sobrescribir pronósticos.
5. **Actualiza `competencia/marcador.md`** con el TWR, el drawdown máximo y los días invertidos del papel. Para el benchmark CETES 28 usa `python3 herramientas/banxico.py` (serie SF43936) si `BANXICO_TOKEN` está en el entorno; si no, el proxy documentado, marcado como proxy. El token nunca se escribe en el repo. Si el dueño agregó filas en `competencia/rivales.csv`, suma los rendimientos de los rivales: TWR cuando haya flujos, y sin atribuir habilidad solo por el saldo final. Sin datos de rivales, escribe "sin datos".
6. Agrega una sección "Cierre" de 10 líneas o menos en `bitacora/briefs/AAAA-MM-DD.md`.
7. **Cierre de la rutina:**
   - deja el latido (REGLAS §3);
   - commit `cierre: AAAA-MM-DD`, pull --rebase y push;
   - respuesta final de 6 líneas o menos.
