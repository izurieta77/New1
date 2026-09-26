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
- `resumen-diario-aprendizaje.md`
- `bloque-trabajo-continuo.md`
- `decisor-vespertino.md`
- `investigador-vespertino.md`

Los disparadores solo despiertan la sesión y le indican seguir esos archivos. Para cambiar una rutina se edita su archivo en git; no hace falta tocar el disparador.

## 0. Cumplimiento (regla dura, sin excepciones)

- Jamás entra al sistema información no pública sobre emisoras, venga de quien venga, incluida cualquier persona del entorno del dueño con acceso a decisiones de emisoras o de inversionistas institucionales.
- Todo insumo debe ser público y verificable. El marco es la Ley del Mercado de Valores (uso de información privilegiada) y, cuando aplique, la regla 10b-5 de la SEC.
- Si algo parece información privilegiada, se descarta sin usarlo y se anota como "descartado por cumplimiento", sin detalles.

## 0b. Cascada vespertina (todos los días, hora del centro de México)

Decisión del dueño (25-sep-2026, "con otros horarios o agentes mejorados pero van más o menos así"): describió el patrón de un rival y pidió adoptarlo, adaptado. Es una segunda pasada diaria, además de las rutinas de mercado (1-6), que no depende de que la BMV o el NYSE estén abiertos.

| Hora | Rutina | Agente | Qué hace |
|---|---|---|---|
| 17:57 | `revision.md` | `revisor` | Revisa lo acumulado del día antes de que seas de la noche |
| 18:08 | `resumen-diario-aprendizaje.md` | orquestador (Motor) | Resumen de lo que el sistema aprendió hoy, para el dueño |
| 18:42 | `cripto.md` §8b | `analista-cripto` | Pulso de cripto, cascada vespertina (reemplaza el pulso de las 20:17) |
| 19:09 | `bloque-trabajo-continuo.md` | orquestador (Motor) | Avanza una tarea de la cola del plan |
| 19:27 | `decisor-vespertino.md` | `decisor` | ¿Alguna alerta de hoy amerita actuar antes del viernes? Casi siempre no |
| 20:12 | `investigador-vespertino.md` | `investigador-academico` | Barrido corto de literatura nueva (no el trimestral completo) |
| 20:57 | `conciliacion-arbitraje.md` | `conciliador-arbitro` | Resuelve lo que haya quedado abierto |
| 21:42 | `supervision.md` §9b | `supervisor` | Cierra el día: revisa que todas las rutinas de hoy dejaron latido |

**Por qué en este orden:** el revisor va primero porque revisa lo pendiente del investigador y del cripto de ayer, no lo de hoy; el decisor y el investigador van después de que cripto y el bloque de trabajo continuo produjeron algo nuevo; conciliación y supervisor van al final porque resuelven y auditan lo que dejó el resto de la noche.

**Costo:** son 6 corridas nuevas por día (2 retiman rutinas que ya existían). El límite semanal de uso sigue siendo el mismo (§7 de `PLAN.md`); si se agota, se detienen todas por igual.

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
  - **Si la fila trae su propia `regla_precio`** (condición de validez, hora, títulos fijos), **manda la fila**. Si la condición no se cumple, marca `estado=en_espera`, no ejecutes y anótalo en el brief.
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

## 4b. Cuenta cripto en Binance (`arena-claude-binance`, perfil `cripto_binance`)

Decisión del dueño (25-sep-2026): **10,000 MXN por IA**, que cuentan para la competencia. **Tope de pérdida en cripto: 5,000 MXN.**

- **Operaciones permitidas:** solo spot. Sin futuros, margen, opciones, préstamos ni productos con bloqueo de liquidez. Universo inicial: BTC y ETH; otra moneda requiere comité y pesa 20% como máximo.
- **Registros:**
  - papel sombra en `bitacora/papel-binance/`;
  - real, según lo que reporte el dueño, en `bitacora/real-binance/`;
  - se usa `herramientas/portafolio.py --perfil cripto_binance --operaciones <ruta> --equity <ruta>`.
- **Precios:** Yahoo `BTC-USD` y `ETH-USD` en USD, convertidos con `MXN=X`.
- **Ejecución en papel:** el precio de ejecución es el cierre de la primera vela horaria completa posterior al commit de la decisión (Yahoo, intervalo 1h). Comisión: 0.1% por lado (tarifa spot estándar; verificar la tarifa real en la app).
- **Boletas reales** en `bitacora/boletas/`, con: par tal como aparece en la app (BTC/MXN si existe; si no, BTC/USDT), tipo de orden (límite; stop-limit u OCO si la app lo permite), cantidad y precio.
- **Cortacircuitos** (sobre el TWR de la cuenta cripto):
  - −20%: exposición a 50%;
  - −30%: exposición a 25%;
  - −40%: pausa;
  - −50% equivale al tope de 5,000 MXN: todo a MXN y la cuenta se detiene hasta que el dueño decida.
- **Exposición, filtro de tendencia y stops** (gestor de riesgo, 25-sep-2026): `config/parametros.json` → `cripto_binance.exposicion`, `.filtro_tendencia` y `.stops`.
  - 40% en BTC al inicio; tramos 2 y 3 solo por comité y con sus cuatro condiciones.
  - Salida total con un cierre de BTC/USDT < SMA200 × 0.97; reentrada con un cierre > SMA200 × 1.03.
  - Sin stop registrado en la app.
- **Órdenes de papel cripto:** las filas de `bitacora/ordenes-pendientes.csv` con `clase=cripto` las ejecuta la **rutina cripto**, no la de Cierre, según su `regla_precio`, en `bitacora/papel-binance/`.
- **Contingencia de contraparte:** `cripto_binance.contingencia_contraparte`. Si se cumple un disparador, alerta alta y boleta URGENTE.

## 5. Competencia

Rivales con cuenta, confirmados por el dueño el 25-sep-2026: **ChatGPT** y **Grok**. Cada IA, nosotros incluidos, tiene **20,000 MXN en GBM y 10,000 MXN en Binance**. La métrica es el TWR en MXN de la cuenta combinada, y además se reportan GBM y Binance por separado.

**Barebone AI no tiene cuenta.** Es un competidor de referencia al que hay que superar en calidad y verificabilidad del análisis (ver `arena/investigacion/06-barebone-ai-competidor.md`).

- Solo se registra lo que el dueño reporte, en `competencia/rivales.csv`, con la columna `cuenta` como `<ia>-gbm` o `<ia>-binance` (por ejemplo, `chatgpt-binance`).
- El valor real de nuestra cuenta `arena-claude` también lo reporta el dueño, en el mismo archivo.
- **Nunca inventes ni estimes el saldo de ninguna cuenta.**
- `competencia/marcador.md` compara TWR, drawdown máximo y días invertidos. Mientras no haya datos del dueño, el marcador lo dice así: "sin datos".

## 5b. Cuenta real `arena-claude` (desde el 28-sep-2026, decisión del dueño)

Referencia: `config/parametros.json`, sección `prioridad_actual.excepcion_cuenta_arena`.

- **Quién ejecuta:** el dueño captura cada orden a mano en la app de GBM. El sistema nunca da por hecha una ejecución real que el dueño no haya reportado.
- **Qué entrega el sistema:** toda orden real sale de una decisión del comité registrada en git **antes** de ejecutarse, y se entrega como boleta con:
  - ticker tal como aparece en GBM;
  - tipo de orden, cantidad de títulos enteros y precio límite;
  - stop registrado en GBM desde la entrada para lo táctico, sectorial, de acción individual o apalancado. Los ETF de índice amplio sin apalancar (hoy SPYM y QQQM) van sin stop por línea; los protegen los cortacircuitos y el tope de 10,000 MXN (enmienda del 25-sep-2026 en `config/parametros.json` → `excepcion_cuenta_arena.enmiendas`).
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

- [ ] **Comité del viernes 2-oct-2026 (rutina 4 + skill `comite-de-inversion`): rediseño al modo C por mandato del dueño.** Lee `config/parametros.json` → `meta_temporada_dueno`. Candidatas: GBM con hasta 50% en un ETF 3x del Nasdaq o del S&P (TQQQ/SPXL, solo si el dueño confirmó que aparece en la app de GBM y con `filtro_apalancados` encendido) + índice 1x; Binance hasta 100% BTC con filtro. Resuelve de frente la objeción del abogado del diablo de W39 (no SPXL con el 10a ≥ 5%) y la condición del 25-sep (6 reportes de rivales antes de apalancar): el apetito de riesgo lo fijó el dueño; la seguridad operativa no se negocia. El gestor de riesgo conserva el veto. Registra P(tocar −12/−20/−28/−35%) del diseño elegido con el mismo método que `arena/modelos/meta_dueno_40_60_200.py`.
- [ ] **Pre-apertura del lunes 28-sep:** pide al dueño en el brief que confirme si TQQQ y SPXL aparecen en el buscador de la app de GBM (mercado SIC). Es requisito del comité del 2-oct.

- [ ] **Pre-apertura del lunes 28-sep-2026:** hay boletas reales para ese día en `bitacora/boletas/2026-09-28.md`. Copia las boletas al inicio del brief, para que el dueño las vea primero, con el estado de futuros del S&P y del VIX a esa hora. La condición de validez formal se evalúa a las 08:45.
- [ ] **Supervisión de las 08:40 del lunes 28-sep (y del martes 29-sep si quedó EN ESPERA):**
  - Evalúa la condición de validez de la boleta GBM con Yahoo (intervalo 1m): SPYM > 88.98 USD y ^VIX < 25.
  - Calcula los límites exactos, precio NYSE × MXN=X × 1.003, de SPYM (7 títulos; 6 si 7 × límite > 12,000 MXN) y de QQQM (1 título).
  - Escribe al inicio de `bitacora/alertas.md` y de la boleta: VIGENTE o EN ESPERA, con los dos límites y la hora.
- [ ] **Cierre del lunes 28-sep:** ejecuta en papel O0001 y O0002 según su `regla_precio` (vela de 1 minuto de las 14:45 UTC, no la apertura). Registra primero el depósito de 20,000 MXN. La O0003 (cripto) no es tuya.
- [ ] **Boleta de Binance del lunes 28-sep:**
  - **Supervisión de las 08:40:** evalúa la condición de validez de C1 (BTC/USDT ≥ 77,000 y ningún cierre diario desde el 25-sep < SMA200 × 0.97, con klines de Binance). Calcula el tope sintético BTC/USDT × USDT/MXN × 1.003 y escribe VIGENTE o EN ESPERA en `bitacora/alertas.md` y al inicio de la sección de Binance de la boleta.
  - **Rutina cripto de las 12:17:** ejecuta la O0003 en papel.
  - **Rutina cripto de las 20:17 de cada día:** calcula el nivel de salida del filtro y lo publica en `bitacora/cripto/AAAA-MM-DD.md`.
