# Rutina 3 · Cierre de mercado (L-V, 15:37 hora del centro de México)

Este procedimiento escrito manda sobre el texto del disparador, que ya indica seguirlo si existe.

0. Tras el `git pull --rebase --autostash`, lee `rutinas/REGLAS-MOTOR.md` y cúmplelo: autonomía, bloqueos, latido y pendientes (§7). Si §7 tiene pendientes, hazlos aquí.
1. **Ejecuta las órdenes pendientes.** En `bitacora/ordenes-pendientes.csv`, toma las órdenes con `estado=pendiente` cuya `fecha_ejecucion` ya llegó y ejecútalas en papel según REGLAS §4:
   - **Precio:** la apertura de ese día en Yahoo (chart v8, campo `open`).
   - **Comisión:** 0.29% del monto.
   - **Depósito inicial:** 20,000 MXN el día de la primera ejecución.
   - **Cantidad:** los títulos se calculan como monto ÷ (precio × FX si cotiza en USD), redondeando hacia abajo a unidades enteras. El sobrante queda en efectivo.
   - **Registro:** marca cada orden como `ejecutada`, con precio, cantidad y commit.
2. **Valúa el portafolio de papel al cierre:** corre `python3 herramientas/portafolio.py valuar` y `reporte` y actualiza `bitacora/equity.csv`.
3. **Revisa límites y cortacircuitos** del perfil `arena_agresivo` (`herramientas/riesgo.py`). Si se dispara uno, genera en `ordenes-pendientes.csv` las órdenes de reducción que manda el perfil, para la apertura siguiente, y anótalo en el brief.
4. **Empresas de `empresas/universo.csv` que reportaron hoy:**
   - obtén los resultados oficiales;
   - resuelve sus pronósticos numéricos y binarios (`herramientas/pronosticos.py`);
   - escribe `empresas/<TICKER>/post-mortem-AAAA-MM-DD.md` con la skill `post-mortem`;
   - actualiza la ficha con una adenda fechada, sin sobrescribir pronósticos.
5. **Actualiza `competencia/marcador.md`** con el TWR, el drawdown máximo y los días invertidos del papel. Si el dueño agregó filas en `competencia/rivales.csv`, suma los rendimientos de los rivales: TWR cuando haya flujos, y sin atribuir habilidad solo por el saldo final. Sin datos de rivales, escribe "sin datos".
6. Agrega una sección "Cierre" de 10 líneas o menos en `bitacora/briefs/AAAA-MM-DD.md`.
7. **Cierre de la rutina:**
   - deja el latido (REGLAS §3);
   - commit `cierre: AAAA-MM-DD`, pull --rebase y push;
   - respuesta final de 6 líneas o menos.
