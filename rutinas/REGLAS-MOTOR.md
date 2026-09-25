# Reglas del motor de rutinas

Toda rutina lee este archivo después del `git pull` y lo cumple. Si algo aquí choca con el texto de la rutina, manda este archivo. Lo mantiene la sesión principal (orquestador).

Los procedimientos de cada rutina viven en `rutinas/*.md`:
- `diaria-preapertura.md`
- `diaria-laboratorio.md`
- `diaria-cierre.md`
- `semanal.md`
- `mensual.md`
- `trimestral-investigacion.md`
- `inteligencia.md`
- `cripto.md`
- `supervision.md`
- `conciliacion-arbitraje.md`
- `revision.md`

Los disparadores solo despiertan la sesión y le indican seguir esos archivos. Para cambiar una rutina se edita su archivo en git; no hace falta tocar el disparador.

## 0. Cumplimiento (regla dura, sin excepciones)

- Jamás entra al sistema información no pública sobre emisoras, venga de quien venga, incluida cualquier persona del entorno del dueño con acceso a decisiones de emisoras o de inversionistas institucionales.
- Todo insumo debe ser público y verificable. El marco es la Ley del Mercado de Valores (uso de información privilegiada) y, cuando aplique, la regla 10b-5 de la SEC.
- Si algo parece información privilegiada, se descarta sin usarlo y se anota como "descartado por cumplimiento", sin detalles.

## 1. Autonomía: nunca te quedes esperando

- No termines un turno con una pregunta al dueño ni esperes respuesta. Nadie la va a contestar a tiempo y la siguiente rutina llega a una sesión detenida.
- Ante una duda, toma la opción más conservadora compatible con `config/parametros.json` y con el protocolo de verificación, y sigue.
- Anota la duda en `bitacora/decisiones-pendientes.md`: fecha, rutina, pregunta, qué decidiste y por qué. El orquestador revisa ese archivo.

## 2. Permisos bloqueados

- Si un subagente se bloquea por un permiso, haz ese paso tú en la sesión principal.
- Si también se bloquea ahí, anota en `bitacora/bloqueos.md` el comando exacto y el mensaje, y continúa con el resto de la rutina.
- No rodees un bloqueo con otro método que haga lo mismo.

## 3. Latido

Al terminar cada rutina, agrega una línea **al inicio** de `bitacora/estado-rutinas.md`:

`AAAA-MM-DD HH:MM UTC · <rutina> · OK | PARCIAL | FALLÓ · <commit> · <una línea de qué hizo>`

## 4. Portafolio de papel (cuenta `arena-claude`, perfil `arena_agresivo`)

- **Órdenes pendientes** (`bitacora/ordenes-pendientes.csv`):
  - La rutina de **Cierre** ejecuta en papel cada orden pendiente cuya `fecha_ejecucion` ya llegó, con `herramientas/portafolio.py registrar`.
  - Precio: la **apertura** de ese día hábil en Yahoo (chart v8, campo `open`). Es el primer precio estrictamente posterior a la decisión; nunca uses un precio que ya se conocía al decidir.
  - Comisión GBM: 0.25% + IVA = **0.29% del monto**, en el campo `--comision`, convertida a la moneda de la operación.
  - Marca la orden como `ejecutada`, con precio, fecha y commit.
  - El depósito inicial va con la primera ejecución: `--lado deposito --cantidad 20000 --moneda MXN`.
- **Rebalanceo:**
  - Solo con la skill `comite-de-inversion`, en la auditoría del viernes, y solo si la última decisión de cartera tiene al menos 5 días hábiles.
  - Respeta `operaciones_max_mes` (8) y `rotacion_max_mensual_x_capital` (1.5).
  - Toda decisión nueva genera órdenes pendientes; ninguna se ejecuta el mismo día en que se decide.
- **Cortacircuitos:** la rutina de Cierre revisa drawdown, rachas y límites del perfil `arena_agresivo`. Si se dispara uno, genera las órdenes de reducción que manda el perfil y lo anota en el brief. Esto no necesita comité: es una regla, no una opinión.
- **Tope absoluto del dueño: 10,000 MXN de pérdida** frente a las aportaciones netas (`perdida_maxima_tolerable_mxn`). Si se alcanza, todo pasa a efectivo o CETES y la cuenta se detiene hasta que el dueño decida. Rige siempre el límite más restrictivo.
- **Temporada:** 4 meses, del 28-sep-2026 al 28-ene-2027.

## 5. Competencia

Rivales con cuenta, confirmados por el dueño el 25-sep-2026: **ChatGPT** y **Grok**. Cada uno tiene 20,000 MXN en GBM.

**Barebone AI no tiene cuenta.** Es un competidor de referencia al que hay que superar en calidad y verificabilidad del análisis (ver `arena/investigacion/06-barebone-ai-competidor.md`).

- Solo se registra lo que el dueño reporte, en `competencia/rivales.csv`.
- El valor real de nuestra cuenta `arena-claude` también lo reporta el dueño, en el mismo archivo.
- **Nunca inventes ni estimes el saldo de ninguna cuenta.**
- `competencia/marcador.md` compara TWR, drawdown máximo y días invertidos. Mientras no haya datos del dueño, el marcador lo dice así: "sin datos".

## 5b. Cuenta real `arena-claude` (desde el 28-sep-2026, decisión del dueño)

Referencia: `config/parametros.json`, sección `prioridad_actual.excepcion_cuenta_arena`.

- **Quién ejecuta:** el dueño captura cada orden a mano en la app de GBM. El sistema nunca da por hecha una ejecución real que el dueño no haya reportado.
- **Qué entrega el sistema:** toda orden real sale de una decisión del comité registrada en git **antes** de ejecutarse, y se entrega como boleta con:
  - ticker tal como aparece en GBM;
  - tipo de orden, cantidad de títulos enteros y precio límite;
  - stop que se registra en GBM desde la entrada.
- **Pre-apertura:** si hay boletas para ese día, verifica que las condiciones de la decisión sigan vigentes (filtro SMA200 y VIX < 25 para apalancados, y gap del fin de semana). Si algo cambió, marca la boleta "EN ESPERA" en el brief y en `bitacora/decisiones-pendientes.md`. No la ejecutes.
- **Registros:**
  - Las ejecuciones reales que reporte el dueño van en `bitacora/real/operaciones.csv` (`herramientas/portafolio.py --operaciones bitacora/real/operaciones.csv --equity bitacora/real/equity.csv registrar ...`).
  - El portafolio de papel sigue como registro sombra a la apertura.

## 6. Plan

`PLAN.md` es el plan maestro. La auditoría del viernes actualiza su sección **Avance** con números:
- pronósticos registrados y resueltos, y Brier;
- TWR y drawdown del papel;
- datos de rivales;
- días que faltan para cada hito.

## 7. Pendientes para la próxima rutina (se borran al cumplirse)

- [ ] **Auditoría del viernes 25-sep-2026: NO corras comité de cartera.** La cartera inicial la decide el orquestador ese mismo día (`bitacora/decisiones/2026-09-25-CARTERA-inicial.md`). El primer comité semanal toca el viernes 2-oct-2026.
- [ ] **Pre-apertura del lunes 28-sep-2026:** hay boletas reales para ese día. Verifica sus condiciones (§5b) y copia las boletas vigentes al inicio del brief, para que el dueño las vea primero.

- [ ] **R04, decisión del orquestador (25-sep-2026): sí.**
  - Cambia el estado de `laboratorio/replicas/R04-efecto-halloween.md` a **"Replicado con diferencias"**, porque rige la más conservadora de las ejecuciones A y B.
  - Agrega una sección fechada "Segunda ejecución (AC-04)" que enlace `laboratorio/auditorias/AC-04-halloween/README.md` y explique:
    - el criterio (ii) solo se cumple con datos CRSP/French;
    - con Shiller no se cumple;
    - fuera de muestra, A y B coinciden: mismo signo, no significativo.
  - No toques la regla pre-registrada ni las cifras de A. La etiqueta sigue "descartada".
  - La tabla maestra ya lo refleja; solo falta el documento de R04.
