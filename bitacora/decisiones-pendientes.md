# Decisiones pendientes y dudas del motor de rutinas

Cada rutina anota aquí lo que decidió sin poder consultar al dueño (ver `rutinas/REGLAS-MOTOR.md` §1). El orquestador revisa y cierra cada punto.

| Fecha | Rutina | Pregunta | Decisión tomada | Por qué | Estado |
|---|---|---|---|---|---|
| 2026-09-25 | arranque inteligencia-y-cripto | La rama local `claude/investment-strategy-routines-19ep76` de este contenedor tenía 17 commits (V01 adenda, comité de agentes, réplicas) sin ancestro común con `origin/claude/investment-strategy-routines-19ep76` (50 commits, incluye rutinas/, config/, agentes vigía y cripto). No había forma de fusionar; ¿conservar cuál? | Conservé la historia local divergente en la rama `backup/local-diverged-<timestamp>` (sin borrar nada) y recreé `claude/investment-strategy-routines-19ep76` apuntando a `origin/...`, que es la línea activa donde ya trabajan las demás rutinas. | El HEAD detached inicial del contenedor ya coincidía con `origin` (b88da18); la rama local vieja no aparece en ningún punto de esa historia, así que es un remanente de otra sesión/tarea, no trabajo en curso de esta rama. | Cerrado |
| 2026-09-25 | orquestador (comité cripto) | ¿La fila de BTC de §6 en `arena/investigacion/03-teoria-de-torneos-y-estrategia-competitiva.md` usa 252 filas (días hábiles) en vez de 365 (cripto opera 24/7)? El abogado del diablo reporta: −11.8% vs máximo, momentum −14.9% y volatilidad 35%, cuando lo correcto sería −32.6%, −27.5% y 42% | Resuelto por el verificador del comité cripto (25-sep, datos de Yahoo BTC-USD con 365 días): la fila de §6 decía −11.8%, −14.9% y 35.2% (252 filas y √252 sobre una serie 24/7). Se corrigió en sitio a −32.5% frente al máximo de 52 semanas, −30.7% de momentum 12-1 y 42.3% de volatilidad a 63 días (√365), con nota fechada; registrado en `conocimiento/registro-de-errores.md` | Es un error de hechos, no de criterio; la corrección no cambia la decisión del comité cripto | Cerrado |
| 2026-09-26 | sesión inteligencia-y-cripto | El dueño reportó (en chat, no como duda de rutina): "no veo agentes trabajando seguido cada mínimo una hora". Medí los huecos reales del día: cripto e inteligencia se turnaban con huecos de ~2h48 tres veces al día (04:17→07:05, 08:17→11:05, 12:17→15:05), más ~2h35 de madrugada y ~1h40 por la tarde. Se le preguntó directamente (no es una duda autónoma) si quería cadencia horaria estricta, dejarlo igual, o cerrar solo los huecos más largos. | El dueño eligió "punto medio". Se crearon 3 disparadores nuevos (`trig_01PZvdFoUyyTzKkbEuEiKjYM`, `trig_01EkNjrpTmRnn37GaNTes9xm`, `trig_01PqeezHY58oXTQtv2Sb5EVo`) a las 05:41, 09:41 y 13:41 CDMX, cada uno solo con el paso 1 (Pulso) de `rutinas/cripto.md`, documentados en `rutinas/REGLAS-MOTOR.md` §0c. | Instrucción directa del dueño, con su elección explícita entre 3 opciones (incluida "dejarlo como está"); no se tocó la cascada vespertina ni los huecos de tarde/madrugada, que el dueño no pidió cerrar. | Cerrado |
| 2026-09-27 | inteligencia (corrida 20:05 del 26-sep) | El subagente vigía escribió la fila P0022 de `bitacora/pronosticos.csv` con comillas internas escapadas como `\"...\"` (estilo Python/JSON) en vez del escape estándar de CSV (`""..."""`). `csv.reader` partía esa fila en 12 campos en vez de 10, lo que habría roto cualquier herramienta que lea el archivo con un parser CSV estricto (p. ej. `herramientas/pronosticos.py`). | Corregí en sitio con un reemplazo de `\"` por `""` en todo el archivo y verifiqué con `csv.reader` que las 23 filas (22 pronósticos + encabezado) quedan con exactamente 10 campos cada una. No cambié ninguna probabilidad, criterio ni texto salvo el carácter de escape. | Es un error de formato, no de contenido; el dato y la cita de Trump quedan intactos y legibles. Dejo la nota aquí para que el orquestador confirme que no hay más filas con este patrón de escape en corridas futuras. | Cerrado |
| 2026-09-28 | inteligencia (corrida 11:05 CDMX) | `bitacora/inteligencia/2026-09-28.md` no existía al iniciar esta corrida y no hay latido de `inteligencia` en `bitacora/estado-rutinas.md` para el barrido de las 07:05 CDMX de hoy (el último latido de `inteligencia` es el cierre del 27-sep, 02:15 UTC) — parece que la corrida de las 07:05 no se ejecutó o no dejó rastro, patrón similar a huecos de disparadores ya vistos el 25/26-sep. | Seguí con el alcance normal de la corrida de las 11:05 (actualización de la sesión) y creé el archivo del día con esa sola sección, dejando explícita la nota de que falta el barrido de las 07:05. No intenté reconstruir retroactivamente el barrido de la noche/Asia/Europa. | Es lo más conservador: no se pierde información (queda anotado el hueco) y no se bloquea la rutina actual; el patrón de huecos de disparadores ya tiene precedente resuelto sin acción especial (ver entradas del 25/26-sep en `bitacora/bloqueos.md`). | Cerrado — el orquestador confirma: sí hubo un disparador de rutina 7 a las 13:19 UTC (07:19 CDMX) que llegó a esta sesión, pero una falla transitoria del clasificador de auto-mode en Bash/Agent (server-side, ~13:19-14:15 UTC) impidió completarlo con el subagente vigía; para no perder la ventana se aprovechó que `rutinas/diaria-preapertura.md` (rutina 1, 06:52 CDMX, L-V, **distinta** de la rutina 7 de inteligencia) ya había cubierto en `bitacora/briefs/2026-09-28.md` y sus anexos el mismo contenido sustantivo (régimen MIXTO+1, geopolítica Irán/Ormuz con el salto de crudo, USD/MXN, 4 pronósticos). No se reconstruye retroactivamente el barrido de las 07:05 porque ya es tarde (pasadas las 11:05) y duplicaría trabajo; el hueco de latido queda documentado aquí para la auditoría. Sin pérdida de información material: el vigía de las 11:05 ya retomó y actualizó todo lo relevante. |

## 2026-09-25 · auditoría semanal 2026-W39 · Para el comité del 2-oct-2026
- **Pregunta:** el abogado del diablo (`bitacora/semanal/2026-W39-abogado.md`) dice que la tesis de la cartera inicial no sobrevive como está escrita: se abstiene. Sus argumentos:
  - la tasa base con el 10a subiendo más de 50 pb en 3 meses da un S&P mediano de +1.5% a 4 meses, por debajo de CETES;
  - el 83% en USD queda expuesto a que el peso se aprecie 5-8%;
  - la refutación no es falsable.
- **Qué decidí:** nada en la cartera. La regla §7 prohíbe el comité hoy y las órdenes O0001-O0002 siguen igual. Lo que propone queda para la agenda del 2-oct:
  - refutar al 28-ene contra "50% SPYM + 50% CETES − 2 pp", sin la cláusula "sin choque";
  - registrar un pronóstico de USD/MXN < 16.90;
  - usar USD/MXN < 16.90 o 10a > 5.50% como disparadores de revisión, no de venta;
  - no usar SPXL mientras el 10a esté en 5% o más.
- **Por qué:** es lo más conservador compatible con REGLAS §4, que pide 5 días hábiles desde la última decisión y ninguna ejecución el mismo día.

## 2026-09-25 · sesión principal · Meta del dueño 40/60/200% y modo de operación
- **Hecho:** el dueño declaró la meta '+40/60/200% en 4 meses, para las tres IAs'. Se le mostró que choca con sus topes (10k/5k) y la probabilidad histórica de 4 modos (`arena/modelos/salida_meta_dueno_40_60_200.txt`).
- **Decisión del dueño:** mantener topes y operar en modo C (máxima agresividad que permiten). Registrada en `config/parametros.json` → `meta_temporada_dueno`.
- **Qué sigue:** nada cambia el lunes 28-sep; el comité del 2-oct rediseña (REGLAS §7). Estado: abierto hasta el 2-oct.

## 2026-09-29 · bloque de trabajo continuo · Insumo para el comité del 2-oct (modo C)
- **Qué hay:** `conocimiento/fichas/2026-09-29-cortacircuitos-apalancados.md`. Con 50% en 3x del S&P **y filtro SMA200**:
  - la mediana de temporada casi no cambia (+5.2% contra +4.8% de la cartera A);
  - el p90 sube de +14% a +21%;
  - P(tocar −12%) sube de 17% a 29%;
  - ninguna temporada desde 1997 pasa de −28%.
- **Sin filtro:** el tope de 10,000 MXN se toca en 0.8% de las temporadas y la pausa de −28% en 14%.
- **La meta del dueño (+40%)** tiene 0-4% de probabilidad histórica en cualquier candidata.
- **Qué decidí:** nada; no es competencia de esta rutina. El comité debe pesar estos números y decirle al dueño con claridad cuánto riesgo implica acercarse a su meta.

## 2026-09-29 · pre-apertura · Para el conciliador: tipo de cambio de ejecución en `portafolio.py`
- **Problema:** `_fx_de` convierte las compras en USD con MXN=X "del cierre del día de la operación". El 28-sep ese dato era intradía (17.9865). Al día siguiente Yahoo lo fijó con otro valor, y el efectivo de la misma cartera pasó de 3,181.94 a 3,404.32 MXN sin ninguna operación nueva.
- **Qué decidí:** borré el snapshot prematuro del 29-sep en `bitacora/equity.csv` y no toqué el código, porque no es tarea de esta rutina.
- **Propuesta:** agregar una columna opcional `tipo_cambio` en `operaciones.csv` (la ejecución fue a 17.825) y usarla en `_fx_de` cuando exista. Después, reconstruir el 28-sep.
- **Cerrado (conciliación, 30-sep):** implementado. Fallo completo en `bitacora/arbitraje/2026-09-30.md`. Resumen: `portafolio.py` ya soporta `--tipo-cambio` en `registrar` y usa ese valor congelado para el costo; `operaciones.csv` migrado con 17.825 en O0001/O0002; `equity.csv` reconstruido (28-sep: efectivo estable en 3,332.93; 29-sep: equity 20,193.12, TWR +1.01%); `competencia/marcador.md` actualizado; 2 pruebas nuevas, batería completa 281/281 OK. Instrucción agregada a `rutinas/REGLAS-MOTOR.md` §4 para que el Cierre pase `--tipo-cambio` de aquí en adelante.

## 2026-09-29 · laboratorio · Insumo adicional para el comité del 2-oct (AC-07, ETF reales, MXN, temporadas de 4 meses)
- **Resultados** (P(DD ≥ 12/20/28/35%); p10 / mediana / p90):
  - 50% UPRO filtrado + 50% SPY: 30.3 / 8.5 / 0.4 / 0.0%; −9.2 / +7.4 / +22.3%
  - 50% TQQQ filtrado + 50% QQQ: 62.7 / 19.9 / 4.0 / 0.4%; −12.0 / +10.0 / +30.0%
  - 100% SPY: 13.1 / 0 / 0 / 0%; −4.6 / +5.6 / +14.2%
- **Lectura:**
  - La mezcla con TQQQ activa el cortacircuitos de −20% en 1 de cada 5 temporadas; la de UPRO, en 1 de cada 12.
  - La regla debe fijar qué serie da la señal: SPY y ^GSPC dan 21.6% y 17.5% de CAGR en UPRO.
  - La ficha del PSR (29-sep) muestra que 4 meses no distinguen habilidad de suerte.
- **Qué decidí:** nada; es competencia del comité.

## 2026-09-29 · bloque de trabajo continuo · Insumo para el comité del 2-oct (volatility drag)
- **Qué hay:** `conocimiento/fichas/2026-09-29-volatility-drag.md`. Con σ = 17.5%, el L* por crecimiento es 2.68 si μ = 8.2% (100 años), pero cae a 1.31 si μ = 4% y a 0.66 si μ = 2%. UPRO real rindió 2.22 pp/año menos que la fórmula sin costos (2009-2026). Sin filtro, cualquier L ≥ 2 perdió 98% o más en 1929-1932.
- **Qué decidí:** nada; es competencia del comité.

## 2026-09-30 · sesión principal · Tipo de cambio: para el comité del 2-oct-2026
- **Hecho:** el dólar subió de 16.87 (FIX 4-sep) a 18.071 (FIX 29-sep). El dueño reclamó que nadie le avisó y mandó un podcast (El Arte de Invertir, presentado por GBM). Expediente: `arena/investigacion/12-dolar-peso-2026-09.md`; prueba del carry: `laboratorio/auditorias/AC-08-carry-peso/` (la regla "diferencial ≤3% ⇒ −14%" no se sostiene: n=2 regímenes opuestos).
- **Qué decidí hoy:** nada en la cartera. La orden de GBM se ejecuta como está (solo se actualizaron los límites con la fórmula). Se instaló la regla FX-1 de alerta cambiaria.
- **Para el comité (propuestas del verificador):**
  1. Pesos ociosos (≈1,139 en Smart Cash de GBM y 3,001.83 en Binance): quedarse en pesos; convertirlos subiría la exposición al dólar de 72% a ~92% sin ventaja histórica (22 episodios: mediana −1.3% a 85 días, p = 0.53). El destino de los 3,001.83 lo define el mandato cripto (cuánto BTC), no una apuesta cambiaria.
  2. Declarar una banda de exposición al dólar de 60-80% del capital combinado (hoy 72%).
  3. Reemplazar el disparador de un solo lado del abogado del diablo (USD/MXN < 16.90) por uno de revisión en dos sentidos: FIX < 17.10 o > 19.10 (rango intercuartil a 85 días tras episodios como este).
  4. Si el dueño quiere expresar la tesis del podcast: cobertura parcial (≤50% de los ociosos) con invalidación explícita (FIX < 17.20).
  5. Calibración: P0027 (USD/MXN > 17.90 el 9-oct, p = 0.40) va del lado "sí"; P0041 y P0042 registran el 18.50 / 19.50 del podcast con plazo al 31-dic.
- **Estado:** abierto hasta el 2-oct.

## 2026-09-30 · laboratorio · AC-09 cambia la lectura de la regla R1 (SMA10) y duda sobre la escala de estados
- **AC-09** (código ciego con Shiller, ^GSPC/^SP500TR y TB3MS) confirma R01 como "Replicado con diferencias", pero fuera de muestra (2007-2026, neto de costos) da **"Solo protección"**: la SMA10 rinde 7.91% contra 10.96% de comprar y mantener, con MDD −22.9% contra −51.0%. A decía "Se sostiene". Rige lo más conservador: **según el §2 del pre-registro, R1 pasa de "se confirma" a "se modifica"** y queda como control de caídas, no como fuente de rendimiento. **Qué decidí:** actualizar ficha, tabla maestra y estado de dominio; no toqué la cartera. Al comité del 2-oct le toca decidir si la regla del filtro fija la serie de la señal (lo mismo que dijo AC-07 para el SMA200).
- **Duda de escala (para la auditoría del viernes):** la escala oficial es Localizado → Documentado → Comprendido → **Contrastado → Replicado** (ideas-adoptadas, laboratorio/README). El 28 y el 29-sep moví "Volatilidad gestionada" y "Apalancados y filtro" de Replicado a Contrastado tras una auditoría concordante, y lo reporté como subida. Con la escala literal eso sería una bajada. **Qué decidí:** no revertir sin fallo; hoy dejé SMA10 en Replicado. La auditoría debe fijar si "Contrastado" significa "segunda fuente concordante" (y va arriba de Replicado) o si se corrige el orden de esos dos temas.
