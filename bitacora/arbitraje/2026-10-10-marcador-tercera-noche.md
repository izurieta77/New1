# Arbitraje · 2026-10-10 · Tercera noche seguida sin el paso 5 del cierre (marcador y `rivales.csv`): se corrige el registro y se escala al dueño como problema de mecanismo

Materia: una regla escrita que no se cumple, por tercera vez (7, 8 y 9-oct). Precedentes: `2026-10-08-marcador-cierre.md` (primera vez, nota fechada a-e en `rutinas/diaria-cierre.md` paso 5), `2026-10-09-marcador-cierre-reincidencia.md` (segunda) y, para la escalación, `2026-10-03-papel-binance-tercera-vez.md`.

## Hechos verificados
- `git show --stat a8c5582` ("cierre: 2026-10-09", 21:39 UTC): el commit tocó `competencia/marcador.md` pero **no** `competencia/rivales.csv`, y no creó `competencia/valuacion-real-2026-10-09.md`.
- **Nota a:** el renglón "Actualizado" y las dos filas de papel seguían en el 8-oct (+2.53% y +0.01%). Los CSV ya tenían la fila del 9-oct: 104.414749 y 100.814091.
- **Nota b:** las cuatro filas reales volvieron a decir "sobre 10,000 / 5,000", sin el índice ni su `equity.csv` como fuente. Es una **regresión**: el cierre sobrescribió lo que la conciliación del 9-oct había corregido.
- **Nota c:** los rivales decían "Yahoo 2d", sin hora, precios ni tipo de cambio (el brief L33 solo trae "USD/MXN 18.36").
- **Nota d:** `rivales.csv` no tenía filas del 9-oct de `arena-claude` ni de `arena-claude-binance`.
- **Nota e:** las seis filas reales decían 9 días invertidos y no daban drawdown.
- **Las cifras de valor sí estaban bien.** Las recalculé con Yahoo chart v8 1d del 9-oct y USD/MXN 18.36:
  - las de Claude, exactas: papel 1,079.03 USD × 18.36 = 19,810.99; real 3 × 91.64 × 18.36 = 5,047.53; BTC implícito 82,466 contra la vela de 15m de las 21:45 UTC, 82,465.54;
  - las de los rivales, a ±0.013% (`competencia/valuacion-real-2026-10-09.md`).

## Fallo
1. **Se corrige el registro al 9-oct, contra los cuatro `equity.csv`.**
   - Papel GBM **+4.41%** (104.41), DD −0.46%, 10 días hábiles.
   - Papel Binance **+0.81%** (100.81), DD −1.77%, 12 días naturales.
   - Real GBM **+0.88%** (100.88), DD −0.32%, 3 días.
   - Real Binance **+0.16%** (100.16), DD −0.63%, 11 días.
   - Rivales: ChatGPT GBM −0.62% (DD −0.82%) y Grok GBM +0.26% (DD **−0.86%**); ChatGPT Binance −1.53% (DD −3.11%) y Grok Binance +0.26% (DD −1.76%).
   - Se agregan las dos filas de Claude a `rivales.csv` y se crea el respaldo de valuación del día.
2. **Error propio de la conciliación del 9-oct:** el DD de Grok GBM (−0.38%) medía el mínimo contra la aportación y no contra el pico. Con el pico del 8-oct (10,112.43) y el valor del 9-oct (10,025.54) es −0.86%.
3. **No se edita el texto de `rutinas/diaria-cierre.md` paso 5 por cuarta vez.** Las notas a-e están escritas desde el 8-oct y dos fallos ya las reforzaron. Tres incumplimientos seguidos, uno de ellos una regresión, prueban que el problema es de **mecanismo** y no de redacción, igual que con el papel de Binance el 3-oct.
4. **Se escala al dueño** (entrada en `bitacora/decisiones-pendientes.md` y fila Alta en `bitacora/alertas.md`), con opciones concretas de mecanismo, ninguna implementada:
   - **(A) Script que regenere el marcador.** Un subcomando, por ejemplo `portafolio.py marcador` o `herramientas/marcador.py`, que lea los cuatro `equity.csv`, los `competencia/*-real-*.md` de posiciones y una consulta de precios, y escriba la tabla de `marcador.md` (índice, DD pico-valle, días invertidos con la convención escrita), las filas del día de Claude en `rivales.csv` y el `valuacion-real-AAAA-MM-DD.md` con hora, precios y tipo de cambio. El cierre solo lo llama. Las notas a-e dejan de depender del criterio del agente de turno.
   - **(B) Chequeo en `herramientas/supervision.py`.** Una función tipo `revisar_marcador()` que compare la fecha del renglón "Actualizado" y la fila más reciente de cada `equity.csv` con las filas de `rivales.csv` y con la existencia del `valuacion-real` del día. Daría AVISO en la supervisión vespertina de las 21:42 y en la de la mañana siguiente. Detecta, pero no corrige: se combina bien con (A).
   - **(C) Prueba de consistencia en `herramientas/tests/`.** Fallaría si el índice que cita el marcador difiere del último `equity.csv`. Solo sirve si alguien corre las pruebas después del cierre.
   - **(D) Pasar el paso 5 a la conciliación**, que de hecho lo está haciendo cada noche, y quitarlo del cierre.
   - **(E) Aceptar otra cadencia**, por ejemplo marcador semanal en la auditoría del viernes y solo el brief a diario.

   La recomendación técnica es (A) más (B). La decisión es del dueño, porque cambia el diseño de la cascada.
5. Mientras el dueño no decida, la conciliación seguirá corrigiendo el registro cada noche. No se fabrica ningún dato.

## Correcciones
`competencia/marcador.md` (renglón Actualizado y 8 filas, con nota fechada), `competencia/rivales.csv` (2 filas), `competencia/valuacion-real-2026-10-09.md` (nuevo), `bitacora/decisiones-pendientes.md`, `bitacora/alertas.md` y `conocimiento/registro-de-errores.md`.
