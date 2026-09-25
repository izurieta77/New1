---
name: comite-de-inversion
description: Somete una tesis u operación (de papel o real) al comité de agentes especializados y produce un memorándum de decisión con votos, disenso y dimensionamiento. Úsalo antes de cualquier cambio en un portafolio.
---
# Comité de inversión

Entrada: una tesis (activo o empresa, dirección, horizonte, catalizador y fecha) o una orden propuesta.

## Procedimiento

1. **Preparación.** Lee `config/parametros.json` y confirma la fase vigente (`prioridad_actual`). En fase 0 solo se decide en papel. Si hay ficha en `empresas/<TICKER>/ficha.md`, léela.
2. **Dictámenes en paralelo.** Lanza con la herramienta Agent, en un solo mensaje, a estos subagentes, pasando a cada uno la tesis completa:
   - `analista-macro`
   - `analista-fundamental` (si la tesis es de empresa)
   - `analista-cuantitativo`
   - `analista-geopolitico`
   - `abogado-del-diablo`
3. **Riesgo.** Con los dictámenes anteriores, lanza `gestor-de-riesgo` para dimensionar y validar.
4. **Verificación.** Lanza `verificador` sobre las cifras clave que sostienen la decisión.
5. **Decisión.**
   - Si `gestor-de-riesgo` veta, la tesis se rechaza.
   - Si el abogado del diablo dice "no sobrevive" y no hay al menos 4 votos a favor con confianza de 60 o más, la tesis se rechaza.
   - En cualquier otro caso: se aprueba si hay mayoría a favor y la confianza media es de 55 o más; si no, pasa a vigilancia.
6. **Registro.** Escribe `bitacora/decisiones/AAAA-MM-DD-<TICKER>-<slug>.md` con:
   - la tesis y cómo se refutaría;
   - un resumen de 3 líneas de cada dictamen;
   - votos y confianzas;
   - el disenso, que se conserva siempre;
   - el tamaño, el stop y el criterio de salida;
   - los pronósticos registrados en `bitacora/pronosticos.csv`, con su probabilidad y fecha de resolución.
7. **Ejecución.**
   - En papel: `python3 herramientas/portafolio.py registrar ...`.
   - En real, solo si la fase lo permite y el dueño lo aprueba: prepara la orden para capturarla en GBM con ticker tal como aparece en la app, tipo de orden, cantidad, precio límite y stop.

## Reglas

- Ninguna decisión sin tesis refutable, tamaño calculado y pronóstico registrado.
- El disenso nunca se borra. En el post-mortem se evalúa quién tenía razón y ese historial calibra el peso de cada agente.
