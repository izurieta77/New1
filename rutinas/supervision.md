# Rutina 9 · Supervisión en vivo (L-V cada hora, de 08:40 a 14:40, hora del centro de México)

Sesión: "Sistema de inversión · Supervisión, conciliación y revisión". Agente: `supervisor` (`.claude/agents/supervisor.md`).

0. Corre `git pull --rebase --autostash`. Lee `rutinas/REGLAS-MOTOR.md` y cúmplelo.
1. Corre `python3 herramientas/supervision.py`. El código de salida indica el estado: 0 = OK, 1 = AVISO, 2 = ALERTA.
   - El script usa el perfil `arena_agresivo` y revisa los libros de papel y real, stops, tope, cortacircuitos, filtro de apalancados, órdenes vencidas, latidos, bloqueos y dudas, y la regla cambiaria **FX-1** (paso 3b).
   - Si falla, anótalo en `bitacora/bloqueos.md` y haz la revisión a mano con `python3 herramientas/portafolio.py valuar --sin-guardar` (el perfil por defecto es la arena) y `python3 herramientas/fx_alerta.py`.
2. **Boletas del día con condición de validez** (`bitacora/boletas/AAAA-MM-DD.md`). En la corrida de las 08:40:
   - evalúa la condición con Yahoo chart v8, intervalo 1m;
   - calcula los precios límite que pida la boleta;
   - escribe VIGENTE o EN ESPERA, con límites y hora, al inicio de la boleta y de `bitacora/alertas.md`.
   Si la condición no se cumple, marca las órdenes sombra correspondientes de `bitacora/ordenes-pendientes.csv` como `en_espera`.
3. Aplica el método del agente `supervisor`: stops, cortacircuitos, tope de 10,000 MXN, filtro de apalancados, órdenes vencidas, latidos, bloqueos y dudas abiertas.
3b. **Regla FX-1, alerta cambiaria (30-sep-2026).** La evalúa el mismo `supervision.py` (código en `herramientas/fx_alerta.py`); su línea empieza con `FX-1`. Informa y pide revisión; **nunca** genera boleta URGENTE ni órdenes: el paso 4 no aplica a FX-1.
   - Qué mide: spot USD/MXN (Yahoo `MXN=X`, 1m) contra la referencia diaria: el FIX de Banxico (SF43718) si `BANXICO_TOKEN` está en el entorno; si no, cierres diarios de Yahoo; si Yahoo falla, Binance USDT/MXN (base 0.1-0.25%). La línea dice qué fuente usó.
   - Niveles: **AVISO** si |Δ1| ≥ máx(1%, 2σd) o |Δ10| ≥ máx(3%, 2σd√10); **ALERTA** si |Δ10| ≥ máx(4.5%, 3σd√10) o el USD/MXN está 6% o más arriba del mínimo (o abajo del máximo) de los últimos 15 días hábiles. En las dos direcciones: un peso que se aprecia también avisa.
   - La línea trae Δ1, Δ10, σd, fuente, hora y el efecto en MXN por cuenta por cada 1% del dólar (parte en USD de papel, real, papel-binance y real-binance). La de ALERTA trae además la frase para el dueño. Si la referencia más reciente no es la del día hábil anterior (feriado o un cierre que faltó), las notas lo dicen: Δ1 y Δ10 miden días de más. La fecha de la regla es la de la Ciudad de México.
   - **El efecto en la frase es el que de verdad tuvo el dinero del dueño** (libros real y real-binance): cada lote cuenta el movimiento desde el inicio de la ventana medida o desde su compra, lo que sea más tarde (tipo de cambio de la operación o referencia de su fecha). Lo comprado con el dólar ya arriba casi no suma. No lo recalcules a mano con "parte en USD de hoy × movimiento de la ventana": sobreestima.
   - **Supresión:** la misma alerta (mismo nivel o menor, misma dirección) no se repite en 10 días hábiles, salvo que el dólar se aleje otro σd√10; entonces sale como `FX-1 OK · ... suprimida` y no hay que volver a avisar. El estado vive en `bitacora/supervision/estado-fx.json`: lo escribe el script, no se edita a mano y se sube en el commit de la rutina. Si está ilegible o mal formado, el script lo ignora (la supresión arranca de cero), lo dice en las notas de la línea `FX-1` y sigue con el resto de la supervisión: anótalo en `bitacora/bloqueos.md`.
   - **Si sale `FX-1 AVISO`:** fila de severidad Alta en `bitacora/alertas.md` (cuenta como urgencia alta, igual que para el vigía; origen "supervisor · FX-1", a quién va: "decisor vespertino y brief de mañana") con la línea completa. No se le escribe al dueño.
   - **Si sale `FX-1 ALERTA`:** el mismo día, (a) fila de severidad Alta en `bitacora/alertas.md`, a quién va: "Dueño; comité del viernes", con la frase para el dueño copiada tal cual (ej.: "el dólar subió 5.1% en 10 días; a tu dinero le suma unos X MXN; hoy tienes unos Y MXN en dólares: cada 1% del dólar les mueve unos Z MXN; no hay que hacer nada hoy, lo revisa el comité del viernes"); (b) esa frase va en la primera línea de la respuesta final de la rutina; (c) punto automático del siguiente comité: entrada en `bitacora/decisiones-pendientes.md` ("Comité del viernes AAAA-MM-DD: revisar FX-1 ALERTA del AAAA-MM-DD — exposición en USD por cuenta y si se cubre o se deja correr"); si ya hay una entrada cambiaria abierta para ese comité, agrega una línea a esa entrada en vez de duplicarla.
   - Si sale `FX-1 sin datos` o `FX-1 error`, corre `python3 herramientas/fx_alerta.py` a mano una vez; si también falla, anótalo en `bitacora/bloqueos.md`. Una falla de FX-1 nunca detiene el resto de la supervisión (stops, tope, cortacircuitos).
4. **Si se dispara una regla** (excepto FX-1, que solo informa): boleta URGENTE al inicio de `bitacora/boletas/AAAA-MM-DD.md`, alerta alta en `bitacora/alertas.md` y órdenes de reducción según el perfil.
5. Una línea en `bitacora/supervision/AAAA-MM-DD.md`; incluye siempre la línea `FX-1` tal cual (también si es OK, y "FX-1 no evaluada" si corriste con `--sin-red`), porque de ahí la leen el decisor vespertino y la pre-apertura.
6. **Cierre de la rutina:**
   - latido solo si hubo AVISO o ALERTA, para no llenar el archivo de "OK";
   - commit `supervision: AAAA-MM-DD HH:MM` solo si hubo cambios (incluye `bitacora/supervision/estado-fx.json` si FX-1 disparó);
   - pull --rebase y push;
   - respuesta final de 3 líneas o menos.

## 9b · Supervisor, cierre de la cascada vespertina (21:42, todos los días)

Último paso de la cascada del dueño (25-sep-2026). No es supervisión de mercado (eso ya lo hizo la sección de arriba en horario bursátil): es una auditoría de que **todas** las rutinas de hoy dejaron su latido.

1. Lee `bitacora/estado-rutinas.md` completo (no solo la última línea) y arma la lista de rutinas que debieron correr hoy según sus horarios en `rutinas/REGLAS-MOTOR.md` §6.
2. Para cada una, confirma que hay un latido de hoy. Si falta uno:
   - si la rutina es de mercado y hoy es fin de semana o feriado (NYSE/BMV cerradas), no es una falla: anótalo así;
   - si no hay motivo para que faltara, es un bloqueo: escríbelo en `bitacora/bloqueos.md` con la rutina, la hora esperada y que nadie dejó latido.
3. Revisa también `bitacora/decisiones-pendientes.md`: si algo lleva más de 48 horas sin cerrarse, escala con una alerta.
4. **Cierre:** una línea en `bitacora/estado-rutinas.md` ("supervisor-vespertino · OK | N sin latido"); commit `supervision-vespertina: AAAA-MM-DD` solo si hubo bloqueos nuevos; pull --rebase y push; respuesta final de 4 líneas o menos.
