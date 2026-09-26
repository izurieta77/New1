# Decisiones pendientes y dudas del motor de rutinas

Cada rutina anota aquí lo que decidió sin poder consultar al dueño (ver `rutinas/REGLAS-MOTOR.md` §1). El orquestador revisa y cierra cada punto.

| Fecha | Rutina | Pregunta | Decisión tomada | Por qué | Estado |
|---|---|---|---|---|---|
| 2026-09-25 | arranque inteligencia-y-cripto | La rama local `claude/investment-strategy-routines-19ep76` de este contenedor tenía 17 commits (V01 adenda, comité de agentes, réplicas) sin ancestro común con `origin/claude/investment-strategy-routines-19ep76` (50 commits, incluye rutinas/, config/, agentes vigía y cripto). No había forma de fusionar; ¿conservar cuál? | Conservé la historia local divergente en la rama `backup/local-diverged-<timestamp>` (sin borrar nada) y recreé `claude/investment-strategy-routines-19ep76` apuntando a `origin/...`, que es la línea activa donde ya trabajan las demás rutinas. | El HEAD detached inicial del contenedor ya coincidía con `origin` (b88da18); la rama local vieja no aparece en ningún punto de esa historia, así que es un remanente de otra sesión/tarea, no trabajo en curso de esta rama. | Cerrado |
| 2026-09-25 | orquestador (comité cripto) | ¿La fila de BTC de §6 en `arena/investigacion/03-teoria-de-torneos-y-estrategia-competitiva.md` usa 252 filas (días hábiles) en vez de 365 (cripto opera 24/7)? El abogado del diablo reporta: −11.8% vs máximo, momentum −14.9% y volatilidad 35%, cuando lo correcto sería −32.6%, −27.5% y 42% | Resuelto por el verificador del comité cripto (25-sep, datos de Yahoo BTC-USD con 365 días): la fila de §6 decía −11.8%, −14.9% y 35.2% (252 filas y √252 sobre una serie 24/7). Se corrigió en sitio a −32.5% frente al máximo de 52 semanas, −30.7% de momentum 12-1 y 42.3% de volatilidad a 63 días (√365), con nota fechada; registrado en `conocimiento/registro-de-errores.md` | Es un error de hechos, no de criterio; la corrección no cambia la decisión del comité cripto | Cerrado |

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
