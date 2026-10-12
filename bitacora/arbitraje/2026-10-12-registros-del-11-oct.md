# Arbitraje · 2026-10-12 · Registros del 11-oct: latido de 55987a6, horas de latido posteriores al commit (escalado) y menores

Materia: hallazgos 1.8, 2.1, 2.2, 3.1, 3.2 y 3.3 de `bitacora/revisiones/2026-10-11.md`.

## 1. Latido de `55987a6` (hallazgo 1.8)
- **Posiciones:** el revisor dice que falta. La línea del orquestador de las 00:19 UTC (`27c93fb`) dice "latido faltante de 55987a6".
- **Fuente primaria:** `git show 55987a6 --stat` no toca `bitacora/estado-rutinas.md`. En el archivo no hay ninguna línea propia del commit fiscal de las 18:23:33 UTC. Lo único que existe es la mención dentro de la línea de las 00:19.
- **Fallo:** esa línea cuenta como **latido retroactivo** de `55987a6`. No se inserta una línea fechada a las 18:23 en medio del archivo, porque se antepone y nunca se reescribe. Le agregué una nota a esa línea. Se cierra.

## 2. Horas de latido y de filas posteriores al commit (hallazgo 2.1): tercera jornada seguida, ya no es solo de la inteligencia
- **Fuente primaria:** `git log --format="%h %ci"` contra la hora que escribió cada latido del 11-oct (hora CDMX del día):

| Rutina | Latido (UTC) | Commit (UTC) | ¿Posterior? |
|---|---|---|---|
| inteligencia 07:05 | 13:45 (filas 13:32-13:40) | `f8ac8c7` 13:12:47 | sí, +32 min |
| inteligencia 11:05 | 17:12 | `05e805d` 17:13:05 | no |
| inteligencia 15:05 | 21:12 (filas 21:10-21:12) | `ddf5b0f` 21:08:57 | sí, +3 min |
| revisión | 00:06 | `e87c4bf` 00:03:58 | sí, +2 min |
| revisión (orquestador) | 00:20 | `e87c4bf` 00:03:58 | sí, +16 min |
| orquestador / aprendizaje | 00:19 / 00:20 | `27c93fb` 00:13:20 | sí, +6/+7 min |
| cripto 18:42 | 00:44 | `339af84` 00:45:59 | no |
| trabajo continuo | 01:16 | `9fcb210` 01:12:21 | sí, +4 min |
| decisor | 01:30 | `f9d4ec5` 01:28:19 | sí, +2 min |
| inteligencia 20:05 | 02:15 | `6d1eb23` 02:12:18 | sí, +3 min |
| investigador | 02:16 | `390860f` 02:14:28 | sí, +2 min |

- **Fallo:** 9 de 11 latidos tienen una hora imposible: el latido se escribe antes del commit, así que no puede ser posterior. Es la tercera jornada seguida (9, 10 y 11-oct CDMX). La nota de regla del fallo del 11-oct ("la hora sale de `date -u`") no cambió nada, y ahora afecta a casi todas las rutinas, no solo a la vigía. Los **hechos** de las filas no cambian: es la hora la que está estimada o redondeada hacia arriba. No reescribo las líneas, siguiendo el precedente del 11-oct.
- **Escalación, por mecanismo y no por texto.** Hay precedente en `decisiones-pendientes.md` (papel Binance, 3-oct, y marcador, 10-oct): a la tercera vez ya no se refuerza el texto de la regla. **El diseño de la cascada lo decide el dueño.** Opciones, sin implementar:
  - (a) Un script `herramientas/latido.py` que antepone la línea con `date -u` en el momento de escribir. Las rutinas lo llaman en vez de redactar la hora.
  - (b) Un control en `herramientas/supervision.py`, a las 21:42, que compare la hora de cada latido del día con la de su commit y la marque si es posterior. Detecta, pero no corrige.
  - (c) Cambiar REGLAS §3: la hora del latido es "hora de inicio de la corrida". La hora real es la del commit, y el campo `<commit>` se llena con el hash en la rutina siguiente.
  - (d) Aceptarlo: tomar la hora del commit como la oficial y dejar la del latido como indicativa, sin seguir auditándola.
  - Recomendación técnica, sin decidir: (a) más (b), con bajo costo y sin depender del criterio del agente.

## 3. Menores
- **2.2, inteligencia 11:05, "sin cambio" 18.3600:** la corrida de las 07:05 dio 18.3880, de la vela del 9-oct 22:59 UTC. Yahoo revisó la última vela del viernes. "Sin cambio" es falso, pero ninguna cifra es inventada. Corregido con nota en L28 y L47 de `bitacora/inteligencia/2026-10-11.md`. Hoy, a las 03:02 UTC del 12-oct, `fx_alerta.py` da OK con 18.4047, contra un umbral de 18.4829.
- **3.1, cripto, "~25 min":** de 12:17 a 18:42 hay 6h25m. La propia corrida de las 13:41 ya lo había reconocido. Agregué una nota en L67 y L71.
- **3.2, cripto, "§8c/§8d":** no existen en `rutinas/cripto.md`. Los pulsos extra son el "paso 1" de REGLAS §0c, y §8b es la cascada de las 18:42. Hay nota en los tres encabezados (05:41, 09:41 y 13:41). Los latidos que dicen §8b/§8c/§8d no se reescriben.
- **3.3, P0103, "venta neta" contra "BTC vendidos > 0":** **manda el criterio literal.** La propia pregunta define entre paréntesis "BTC vendidos > 0 en la tabla de actividad". Una semana con ventas mayores que 0 resuelve SÍ, aunque esa semana también haya compras mayores. Dejé una nota en el campo `notas`. La pregunta y la probabilidad registradas no cambian.
