# Arbitraje · 2026-10-10 · El comité del 9-oct no sesionó: ¿cuándo sesiona y quién lo convoca?

Materia: una regla que choca con otra, más una duda anotada en `bitacora/decisiones-pendientes.md` (revisor, 9-oct, punto 1). **No se decide ningún punto de la agenda.**

## Posiciones
- **Auditoría semanal W41** (`bitacora/semanal/2026-W41.md` L36-L40): el comité "corresponde hoy" (W40 del 2-oct, con 5 días hábiles), pero no corrió la skill porque "un comité con órdenes reales requiere al dueño". Propone mantener la cartera y no fija fecha.
- **Revisor** (`bitacora/revisiones/2026-10-09.md` 1.1): el motivo contradice REGLAS §5b y §1 y `rutinas/semanal.md` paso 6. Es el segundo aplazamiento de varios puntos.

## Fuente primaria (reglas del repo)
- **REGLAS §4 (Rebalanceo):** "Solo con la skill `comite-de-inversion`, **en la auditoría del viernes**, y solo si la última decisión de cartera tiene al menos 5 días hábiles."
- **`rutinas/semanal.md` paso 6:** el comité corre dentro de la auditoría semanal (viernes 16:47 CDMX); "lo preside el agente `decisor`"; el decisor escribe las boletas reales y las órdenes van a `ordenes-pendientes.csv` para el siguiente día hábil.
- **REGLAS §5b:** "toda orden real sale de una decisión del comité registrada en git **antes** de ejecutarse" y el dueño la captura a mano. `config/parametros.json` → `excepcion_cuenta_arena.decision_del_dueno`: "la cartera que apruebe el comité de inversión se replica en dinero real". Esa es la aprobación vigente del dueño.
- **Skill `comite-de-inversion` paso 7:** "En real, solo si la fase lo permite y el dueño lo aprueba: prepara la orden para capturarla en GBM". Es la única frase que podría sostener el motivo de la W41.
- **REGLAS §1:** no esperar al dueño; ante la duda, la opción conservadora y seguir. **`.claude/agents/decisor.md`:** antes del viernes solo hay decisiones extraordinarias por alerta alta confirmada, cortacircuitos o filtro de apalancados roto.

## Fallo
1. **El motivo de la W41 no se sostiene.** El paso 7 de la skill trata de la *ejecución* en real. La aprobación del dueño ya existe en `excepcion_cuenta_arena`, y la ejerce al capturar (o no) cada boleta. Nada condiciona la *sesión* a su presencia, y el papel ni siquiera requiere aprobación. Si choca con REGLAS, manda REGLAS (encabezado del archivo). El comité debió sesionar el 9-oct.
2. **Quién convoca:** la auditoría semanal (orquestador), en su paso 6. **Quién preside:** el `decisor`.
3. **Cuándo sesiona:** por REGLAS §4, la siguiente sesión válida es la **auditoría semanal del viernes 16-oct (W42)**. Sus condiciones se cumplen: la última decisión de cartera sigue siendo la W40 del 2-oct, con ≥ 5 días hábiles. La agenda completa es la que quedó en REGLAS §7 y en la conciliación del 9-oct: destino del ~27% que iba a UPRO/SPXL, stop mental vía GBM USA, efectivo ocioso en GBM y Binance, banda FX y los puntos cambiarios (más la ALERTA FX-1 del 9-oct), BTC 40→65%, `filtro_apalancados` y VIX < 25, IBIT con la advertencia fiscal D7, exchange y plan B, camino por catalizador y regla Kawa.
4. **Una sesión antes del 16-oct** (por ejemplo, el lunes 12) no cabe en REGLAS §4 ni en las causales extraordinarias del decisor: ninguna se cumple hoy, porque la ALERTA FX-1 solo informa y no hay cortacircuitos ni filtro roto. Hacer una excepción al calendario es decisión del dueño. **Escalado:** al dueño, la pregunta de si quiere una sesión extraordinaria; al decisor y al orquestador, que la W42 corra la skill completa sin el motivo "requiere al dueño".
5. **Mientras tanto** rige la cartera vigente (W40 en papel; 3 SPYM + efectivo en real). Ningún punto se da por decidido. La "propuesta mientras tanto" de la W41 no es una decisión de comité.

## Correcciones
- `bitacora/semanal/2026-W41.md`: nota fechada en la sección g).
- `bitacora/decisiones-pendientes.md`: punto (1) del revisor, cerrado como arbitraje y escalado.
- `conocimiento/registro-de-errores.md`: una fila.
