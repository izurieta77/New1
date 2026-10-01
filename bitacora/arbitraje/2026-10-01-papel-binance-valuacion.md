# Arbitraje · 2026-10-01 (conciliación de la noche del 30-sep)

## Caso: ¿quién valúa a mercado el libro de papel de Binance quien no tuvo operación nueva?

**Los hechos:**
- `rutinas/diaria-cierre.md` (rutina 3, cierre de GBM) dice en su paso 2: "Valúa el portafolio de papel al cierre: corre `portafolio.py valuar` y `reporte` y actualiza `bitacora/equity.csv`" — solo menciona el libro de GBM.
- `rutinas/cripto.md` (rutina 8) solo manda a la rutina cripto ejecutar en papel las filas `clase=cripto` de `bitacora/ordenes-pendientes.csv` cuando hay una orden pendiente; no tiene un paso de "revalúa el libro aunque no haya orden nueva".
- En la práctica, las corridas de cierre del 28-sep (`fbf5f22`) y del 29-sep (`558ddda`) sí revaluaron también `bitacora/papel-binance/equity.csv` el mismo día, dejando un patrón de 2 días de una fila diaria en ese archivo.
- La corrida de cierre del 30-sep (`d5b15af`, 21:40 UTC) solo tocó `bitacora/equity.csv` (GBM) y no agregó una fila para el 30-sep en `bitacora/papel-binance/equity.csv`. Ninguna otra rutina del día (cripto 00:17-18:42 CDMX) lo hizo tampoco, porque no le correspondía por escrito.
- Resultado: al cierre del 30-sep, `competencia/marcador.md` reporta el papel de GBM al 30-sep (20,166.33 MXN) pero el papel de Binance se quedó al 29-sep (10,055.01 MXN), un día desfasado. El propio `marcador.md` lo dice explícitamente ("índice 100.12 al 29-sep"), igual que el decisor vespertino y el brief del día, así que no hay ninguna cifra contradictoria entre archivos — es un hueco de cobertura, no un dato falso.

**Por qué es arbitraje:** es una regla que choca con otra (el procedimiento escrito de la rutina 3 no cubre lo que la práctica de 2 días sí hizo, y ninguna rutina reclama por escrito la valuación diaria sin operación del libro de Binance), no una decisión de inversión ni un cambio de parámetro de riesgo.

**Intenté reconstruir la fila faltante del 30-sep yo mismo** con `herramientas/portafolio.py --perfil cripto_binance ... valuar --reconstruir`, en una copia de prueba (no se tocó el archivo real). El resultado reconstruido difiere de las filas ya grabadas del 28 y 29-sep por hasta ~1.2% (más que la tolerancia de 0.1%), y la vela diaria de BTC-USD de Yahoo para el propio 2026-09-30 vino con `open`/`close` nulos al momento de consultar (03:03 UTC del 1-oct, justo después de medianoche UTC) — un problema de datos de Yahoo para pares 24/7 ya documentado en otro contexto (FX) el 29/30-sep. No es seguro reemplazar lo ya grabado con una reconstrucción que usa una fuente con un hueco de datos ese mismo día.

**Fallo:**
1. No se sobrescriben las filas del 28 y 29-sep de `bitacora/papel-binance/equity.csv` (quedan como están; la discrepancia con `--reconstruir` es una pista para investigar la metodología de valuación de cripto 24/7, no una corrección lista para aplicar bajo esta evidencia incompleta).
2. No se inventa una fila para el 30-sep con datos de Yahoo incompletos. Se deja pendiente para la próxima corrida de cierre (1-oct), cuando la vela del 30-sep ya esté asentada.
3. Se corrige la regla hacia adelante: añadí a `rutinas/diaria-cierre.md` paso 2 la instrucción explícita de revaluar también `bitacora/papel-binance/equity.csv` cada día (igual que ya se hacía el 28 y 29-sep), con instrucción de no guardar una fecha con un precio de otro día si la vela viene incompleta.
4. Pendiente técnico para el laboratorio o trabajo continuo (no para el dueño): revisar por qué `valuar --reconstruir` da para BTC-USD valores de posición distintos (hasta 1.2%) de los que graba `valuar` en vivo en el momento del cierre — candidato: un activo 24/7 no tiene un "cierre" único y el método en vivo captura el precio a la hora en que corre la rutina (21:39-21:55 UTC), no la vela de medianoche UTC que usa `--reconstruir`. Si se confirma, documentar la convención igual que se hizo con el tipo de cambio de costo (arbitraje del 30-sep).

**Efecto:** ninguna cifra ya publicada cambia hoy. `competencia/marcador.md` sigue correcto porque ya revela la fecha real de cada dato. El hueco de cobertura queda cerrado hacia adelante con la instrucción añadida a `rutinas/diaria-cierre.md`.
