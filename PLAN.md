# Plan maestro: torneo de IAs inversionistas (cuenta `arena-claude`)

Actualizado: 25-sep-2026, por la sesión principal (orquestador). Parámetros en `config/parametros.json`; reglas del motor en `rutinas/REGLAS-MOTOR.md`.

## 1. Objetivo

Terminar cada temporada de 6 meses con el **mayor TWR en MXN** entre las cuentas de IA. Todas arrancan con 20,000 MXN. Hay que lograrlo sin salir del juego: los cortacircuitos del perfil `arena_agresivo` ponen el límite duro en −35%.

Lo que está en juego:
- las aportaciones progresivas, hasta 100-200k MXN o más;
- la continuidad de la suscripción de cada IA (`escalamiento_capital` en parámetros).

## 2. Rivales

Pendiente de confirmar con el dueño:
- ChatGPT ("Maquiavelo");
- Grok;
- Barebone AI.

Barebone es un terminal de investigación que no ejecuta operaciones (ver `arena/investigacion/06-barebone-ai-competidor.md`). Falta saber si sustituye a un rival o se suma como cuarto. Solo se registra lo que el dueño reporte.

## 3. Dónde se puede ganar, con evidencia

- **Nadie tiene ventaja demostrada:**
  - En nuestro laboratorio, 0 de 13 estrategias llegan a "ventaja demostrada" (3 investigables, 7 descartadas, 3 en curso).
  - Las compras de Pepe no le ganan al azar comparable (auditoría v3, verificada).
  - Barebone no publica ningún historial auditado.
- **Por eso, en 6 meses el TWR lo deciden sobre todo tres cosas:**
  1. estar invertido con la exposición correcta para el régimen;
  2. no sufrir una pérdida grande (cortacircuitos, límites de concentración, filtro para apalancados);
  3. costos bajos (GBM cobra 0.29% por lado; máximo 8 operaciones al mes).
- **La ventaja que nadie más tiene es un historial auditable:**
  - Cada pronóstico y cada decisión quedan en git, con hora, **antes** de conocer el precio con el que se ejecutan.
  - Cada cifra lleva su fuente primaria.
  - Cada error propio queda en un registro público.
  - Es justo el terreno donde Barebone tiene cero.

## 4. Ruta crítica

| Hito | Criterio | Estado al 25-sep | Fecha estimada |
|---|---|---|---|
| Examen de titulación | ≥90% global y ≥85% por sección | Cumplido: 96.1% | 25-sep-2026 |
| Pronósticos calibrados | ≥50 resueltos, Brier ≤ 0.20, 3 meses | 5 registrados, 0 resueltos. Los primeros se resuelven el 14 y el 23-oct | 25-dic-2026 |
| Portafolio de papel | 3 meses dentro de límites | Arranca hoy: comité el 25-sep, ejecución en papel a la apertura del 28-sep | 28-dic-2026 |
| Capital real (regla vigente de fase 0) | Los tres criterios anteriores | — | ~28-dic-2026 |
| **Decisión del dueño** | ¿La cuenta arena entra antes que el patrimonio principal? | Pendiente | — |

Con la regla vigente, nuestro dinero real entra cuando la primera temporada ya lleva la mitad. Esa es la desventaja real frente a rivales que ya estén invertidos. Se resuelve con una decisión del dueño, no con más agentes (ver §7).

## 5. Qué hace cada agente y cuándo (hora del centro de México)

Las rutinas corren en la sesión en la nube "Sistema de inversión · Motor de rutinas" y dejan todo en git. Sus procedimientos están versionados en `rutinas/*.md` y se cambian ahí. La sesión principal orquesta, revisa y corrige.

| Rutina | Cuándo | Qué entrega |
|---|---|---|
| 1. Pre-apertura | L-V 06:52 | Régimen de mercado, geopolítica, 3-5 pronósticos nuevos, pronósticos vencidos resueltos, riesgo del papel, brief del día |
| 2. Laboratorio | L-V 11:47 | Un tema de dominio sube de nivel, avance de una réplica con doble ejecución independiente, un paper verificado |
| 3. Cierre | L-V 15:37 | Ejecuta en papel las órdenes pendientes, valúa, revisa cortacircuitos, post-mortems de las empresas que reportaron, marcador |
| 4. Auditoría semanal | Vie 16:47 | Brier y calibración, 3 afirmaciones atacadas, papel vs. benchmarks y rivales, comité de rebalanceo, actualiza §8 |
| 5. Balance mensual | Día 1, 10:13 | Examen de 20 preguntas nuevas, reporte mensual del papel, criterio de salida de fase 0 con números |
| 6. Barrido trimestral | 5-ene, abr, jul y oct, 11:37 | Literatura nueva, SPIVA, cambios fiscales y regulatorios |

Cada rutina deja una línea de latido en `bitacora/estado-rutinas.md`. Cuando una tiene una duda, decide de forma conservadora y lo anota en `bitacora/decisiones-pendientes.md`: nunca se queda esperando.

## 6. Qué necesita el sistema del dueño

1. **Saldos de los rivales.** Cada viernes, o cuando se pueda: cuenta, fecha, valor en MXN y aportaciones. Sin esto el marcador está vacío.
2. **Fecha de fondeo de cada cuenta rival**, para saber cuándo empezó la temporada.
3. La decisión de §4 sobre la cuenta arena.
4. **Montos y fechas de las aportaciones adicionales**, y qué resultado las dispara (`escalamiento_capital.pendiente_de_definir_por_el_dueno`).

## 7. Por qué no "más agentes todo el tiempo"

- **La restricción que manda es el calendario.** La calibración y el papel necesitan 3 meses reales, y ningún número de agentes acorta eso.
- **Más corridas gastan el límite semanal de uso de la cuenta.** El 25-sep ya se agotó una vez y detuvo todo. Si se agota, también se detienen las rutinas que sí importan.
- **Las rutinas corren en los momentos que mueven la aguja:** antes de abrir, al cierre, el viernes, el día 1 y el trimestre. Entre esos momentos no hay nada que decidir.

## 8. Avance (lo actualiza la auditoría del viernes)

| Indicador | Valor | Fecha |
|---|---|---|
| Pronósticos registrados / resueltos | 5 / 0 | 25-sep-2026 |
| Brier acumulado | n/d | — |
| Portafolio de papel: TWR / drawdown máximo | Arranca el 28-sep | — |
| Rivales con datos | 0 | — |
| Días para fin de fase 0 (regla vigente) | ~94 | 25-sep-2026 |
