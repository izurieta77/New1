# Arbitraje · 2026-10-10 (conciliación de la noche del 9-oct) · Cruce transitorio de FX-1 (17:18-17:20 UTC): ¿re-escala, se registra y reinicia la ventana?

Materia: una regla que choca con otra (división de trabajo inteligencia/supervisión/decisor contra el deber de avisar el mismo día) y una duda anotada en `bitacora/decisiones-pendientes.md` (vigía 11:05 del 9-oct; revisor punto 4; decisor vespertino del 10-oct).

## Posiciones
- **Vigía (11:05 y 15:05 del 9-oct):** el script dio ALERTA real en tres lecturas (18.4737, 18.4801, 18.4820; umbral 18.4733; episodio +7.31% a +7.35% en 14 días hábiles). No corrió `--registrar` porque su rutina usa el script "solo lectura" y el registro es de la supervisión. A las 15:05 lo cerró "sin escalamiento adicional".
- **Supervisión (12:40 a 14:40 CDMX):** ninguna lectura programada vio el cruce; escribió "nunca se cruzó el umbral" (ya corregido por el orquestador).
- **Orquestador (10-oct 00:25 UTC):** registró la alerta tarde en `bitacora/alertas.md` como **Media**, dirigida a "Dueño (informativo) y comité".
- **Decisor vespertino (10-oct 01:29 UTC):** FX-1 OK a 18.36; la severidad Media contradice la regla; pide el fallo sobre la ventana.

## Fuente primaria (código y reglas del repo)
- `herramientas/fx_alerta.py::_bloqueo`: un registro suprime a un candidato solo si la dirección es la misma, el nivel es igual o mayor **y** `log(spot / usdmxn_registrado) < σd·√10`. Con el registro del 30-sep (18.08737) y σd 0.67%, el límite era 18.4733; a 18.4737-18.4820 el candidato "ALERTA sube (episodio)" **no estaba suprimido**: `decidir()` lo devuelve como `disparo`. Es decir, por la regla escrita **sí re-escaló**.
- `decidir()` arma el registro nuevo con `fecha = hoy` y `usdmxn = spot` **de la corrida en curso**; `main()` solo lo guarda si esa misma corrida trae `--registrar` y hay disparo. El docstring: el estado "solo lo escribe la supervisión (rutina 9) o `--registrar`". `rutinas/supervision.md` 3b: `estado-fx.json` "lo escribe el script, no se edita a mano".
- `rutinas/supervision.md` 3b: con `FX-1 ALERTA`, **el mismo día**, fila de severidad **Alta** a "Dueño; comité del viernes" con la frase del script, la frase en la primera línea de la respuesta y punto automático del comité. `rutinas/inteligencia.md` §3: un AVISO o ALERTA de FX-1 cuenta como urgencia alta. `rutinas/decisor-vespertino.md` 2b: si el dueño no recibió la frase, el decisor corre `--registrar` y la escribe.
- Lectura de esta corrida (`python3 herramientas/fx_alerta.py`, sin `--registrar`, 02:59 UTC del 10-oct = 20:59 CDMX del 9-oct): "FX-1 OK · sin disparo nuevo · USD/MXN 18.3600 · Δ10 +3.44% · σd 0.77%". No hay candidato: `--registrar` ahora **no escribiría nada**.

## Fallo
1. **El cruce sí era una ALERTA no suprimida que debía avisarse y registrarse el mismo día.** La regla no distingue entre un cruce largo y uno de dos minutos: la vigía lo vio con el script y la regla de urgencia alta le aplicaba. La división de trabajo (`--registrar` es de la supervisión) no la eximía de abrir la fila Alta a nombre del dueño ni de pedirle a la supervisión siguiente una lectura inmediata. Tampoco se debió cerrar "sin escalamiento" a las 15:05.
2. **Severidad: Alta, no Media.** Corregí la fila en `bitacora/alertas.md` (Alta; "Dueño; comité del viernes"), con nota fechada.
3. **Ventana de supresión: no se reinicia.** Si se hubiera registrado a las 17:18, el registro nuevo habría sido ALERTA sube del 9-oct a ~18.474: supresión hasta el 22-oct inclusive y re-escalada arriba de ~18.87-18.93 (según σd). No se registró, la herramienta ya no puede hacerlo (sin disparo desde las 17:41 UTC) y editar `estado-fx.json` a mano está prohibido y sería fabricar un registro retroactivo. **No corrí `--registrar` y no toqué `estado-fx.json`.** Queda vigente el registro del 30-sep: suprime hasta el 13-oct inclusive (el 14-oct ya cuenta 10 días hábiles) y, con σd 0.77%, re-escala arriba de ~18.53.
4. **Efecto práctico:** la opción vigente es la más sensible (la supresión vence antes y el umbral es más bajo), así que el error no oculta alertas futuras: si del 14-oct en adelante el episodio sigue ≥ 6%, sale una ALERTA nueva sin supresión.
5. **Lo que la regla no resuelve:** qué hacer con un disparo que se detecta después de que el precio volvió. El código no tiene un modo "registro retroactivo" y las rutinas no lo prevén. No invento regla: si el dueño o el comité quieren reiniciar la ventana a mano (o que el script acepte `--registrar` con fecha y nivel de un disparo ya observado), es un cambio de parámetro o de herramienta que les toca a ellos. Queda escalado en `bitacora/decisiones-pendientes.md`.
6. **Aviso al dueño:** la frase literal que imprimió el script a las 17:18 no se guardó y no la reconstruyo. Lo verificable: el dólar llegó a 18.48 (episodio +7.3% en 14 días hábiles) y cerró el día en 18.36; cada 1% del dólar mueve unos ±311 MXN en los cuatro libros (±71 MXN en los dos reales del dueño). Es favorable para las posiciones en USD y no pide ninguna acción. Va en el latido y en la respuesta de esta corrida, y como punto del comité (banda FX, ya en agenda).

## Correcciones
- `bitacora/alertas.md`, fila del 10-oct 00:25: severidad y destinatario, con nota fechada.
- `bitacora/decisiones-pendientes.md`: punto (4) del revisor, la entrada del vigía y la del decisor vespertino, cerrados como arbitraje; la pregunta del registro retroactivo queda escalada.
- `conocimiento/registro-de-errores.md`: dos filas (cierre sin escalar a las 15:05; severidad Media en el registro tardío).
