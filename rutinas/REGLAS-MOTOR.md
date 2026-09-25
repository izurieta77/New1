# Reglas del motor de rutinas

Toda rutina lee este archivo después del `git pull` y lo cumple. Si algo aquí choca con el texto de la rutina, manda este archivo. Lo mantiene la sesión principal (orquestador).

Los procedimientos de cada rutina viven en `rutinas/*.md`:
- `diaria-preapertura.md`
- `diaria-laboratorio.md`
- `diaria-cierre.md`
- `semanal.md`
- `mensual.md`
- `trimestral-investigacion.md`

Los disparadores solo despiertan la sesión y le indican seguir esos archivos. Para cambiar una rutina se edita su archivo en git; no hace falta tocar el disparador.

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

## 5. Competencia

- Rivales vigentes, pendientes de confirmar con el dueño:
  - ChatGPT ("Maquiavelo");
  - Grok;
  - Barebone AI, terminal de investigación que no ejecuta operaciones (ver `arena/investigacion/06-barebone-ai-competidor.md`).
- Solo se registra lo que el dueño reporte, en `competencia/rivales.csv`. **Nunca inventes ni estimes el saldo de un rival.**
- `competencia/marcador.md` compara TWR, drawdown máximo y días invertidos. Mientras no haya datos del dueño, el marcador lo dice así: "sin datos".

## 6. Plan

`PLAN.md` es el plan maestro. La auditoría del viernes actualiza su sección **Avance** con números:
- pronósticos registrados y resueltos, y Brier;
- TWR y drawdown del papel;
- datos de rivales;
- días que faltan para cada hito.

## 7. Pendientes para la próxima rutina (se borran al cumplirse)

- [ ] **R04, decisión del orquestador (25-sep-2026): sí.**
  - Cambia el estado de `laboratorio/replicas/R04-efecto-halloween.md` a **"Replicado con diferencias"**, porque rige la más conservadora de las ejecuciones A y B.
  - Agrega una sección fechada "Segunda ejecución (AC-04)" que enlace `laboratorio/auditorias/AC-04-halloween/README.md` y explique:
    - el criterio (ii) solo se cumple con datos CRSP/French;
    - con Shiller no se cumple;
    - fuera de muestra, A y B coinciden: mismo signo, no significativo.
  - No toques la regla pre-registrada ni las cifras de A. La etiqueta sigue "descartada".
  - La tabla maestra ya lo refleja; solo falta el documento de R04.
