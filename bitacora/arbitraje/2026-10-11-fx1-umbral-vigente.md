# Arbitraje · 2026-10-11 (conciliación de la noche del 10-oct) · FX-1: ¿qué umbral de re-escalada vale, ~18.53 o 18.4818?

Materia: cifras repetidas que no coinciden y verificador contra autor. El hallazgo es el 1.2 de `bitacora/revisiones/2026-10-10.md`, y el autor es esta misma conciliación.

## Posiciones
- **Fallo propio del 10-oct** (`2026-10-10-fx1-cruce-transitorio.md`, punto 3) y su escalación en `decisiones-pendientes.md`: "re-escala arriba de ~18.53, con σd 0.77%".
- **Inteligencia del 10-oct** (L11 y L45) y **revisor**: el script dice "salvo que el USD/MXN pase de 18.4818", con σd 0.68%.

## Fuente primaria (código)
- `herramientas/fx_alerta.py`:
  - L175-176: σd = desviación estándar de los rendimientos de la ventana de cierres que baja **cada corrida**, y s10 = σd·√10.
  - L437-441: umbral = `usdmxn` del registro × exp(s10). Se imprime en cada corrida.
  - El umbral no se guarda en `estado-fx.json`; solo se guarda el nivel del registro, que es 18.08737 (30-sep).
- Corrida de esta conciliación (`python3 herramientas/supervision.py`, línea FX-1, ~02:57 UTC del 11-oct): σd 0.68%, "no se repite hasta el 14-oct salvo que el USD/MXN pase de **18.4818**".
- La corrida del 10-oct a las 02:59 UTC daba σd 0.77%, y de ahí salía el ~18.53. El σd cambió aunque el mercado estuvo cerrado el sábado. La explicación probable, que no verifiqué vela por vela, es que Yahoo revisó el último dato del 9-oct (18.36 → 18.388, lo anota la revisión del 10-oct) y que la ventana de 3 meses se recorrió.

## Fallo
1. **El umbral vigente es el que imprime el script en cada corrida.** No es una cifra fija de ningún fallo. Hoy es 18.4818, y el lunes será el que dé la herramienta ese día. El ~18.53 fue correcto para su hora y no debe usarse como umbral fijo. Gana la inteligencia.
2. **La fecha coincide en los dos textos.** "No se repite hasta el 14-oct" quiere decir que la supresión vale hasta el 13-oct inclusive.
3. **No se tocó** `estado-fx.json` y no se corrió `--registrar`, porque no hubo disparo.

## Correcciones
- `bitacora/arbitraje/2026-10-10-fx1-cruce-transitorio.md`: nota fechada al final; la historia no se reescribe.
- `bitacora/decisiones-pendientes.md`: nota bajo la escalación (2). La pregunta sigue abierta para el dueño o el comité.
- `conocimiento/registro-de-errores.md`: una fila (error propio).
