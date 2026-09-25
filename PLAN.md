# Plan maestro: torneo de IAs inversionistas (cuenta `arena-claude`)

Actualizado: 25-sep-2026, por la sesión principal (orquestador). Parámetros en `config/parametros.json`; reglas del motor en `rutinas/REGLAS-MOTOR.md`.

## 1. Objetivo

Terminar la temporada con el **mayor TWR en MXN** entre las cuentas de IA. Cada IA arranca con **30,000 MXN: 20,000 en GBM y 10,000 en Binance (cripto)**. La métrica es la cuenta combinada, y además se reportan GBM y Binance por separado. **Temporada actual: 4 meses, del 28-sep-2026 al 28-ene-2027** (dueño, 25-sep).

Hay que lograrlo sin salir del juego. La pérdida máxima que tolera el dueño es de **10,000 MXN en GBM** y **5,000 MXN en cripto**. Los cortacircuitos del perfil `arena_agresivo` (−12%, −20%, −28% y −35%) se disparan antes; rige siempre el límite más restrictivo.

Lo que está en juego:
- las aportaciones progresivas, hasta 100-200k MXN o más;
- la continuidad de la suscripción de cada IA (`escalamiento_capital` en parámetros).

## 2. Rivales

Confirmados por el dueño el 25-sep-2026: **ChatGPT** y **Grok**, cada uno con 20,000 MXN en GBM y 10,000 MXN en Binance. Solo se registra lo que el dueño reporte.

**Barebone AI** no tiene cuenta en el torneo. Es la referencia que hay que superar en calidad y verificabilidad del análisis (ver `arena/investigacion/06-barebone-ai-competidor.md`).

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

**Decisión del dueño (25-sep-2026): la cuenta arena entra en real el lunes 28-sep-2026** con la cartera que apruebe el comité. El patrimonio principal sigue en fase 0 con la regla completa.

| Hito | Criterio | Estado al 25-sep | Fecha |
|---|---|---|---|
| Examen de titulación | ≥90% global y ≥85% por sección | Cumplido: 96.1% | 25-sep-2026 |
| Cartera inicial de la arena | Aprobada por el comité y registrada en git antes de ejecutarse | **Cumplido:** cartera A (7 SPYM + 1 QQQM + liquidez); gestor de riesgo aprueba con cambios | 25-sep-2026 |
| Arena en real (GBM) | El dueño captura las boletas en GBM si se cumple la condición de validez de las 08:45. Stop por línea solo en lo táctico o apalancado (enmienda del 25-sep) | Boletas listas en `bitacora/boletas/2026-09-28.md` | 28-sep-2026 |
| Cartera cripto (Binance) | Comité cripto: solo spot, tope de 5,000 MXN | **Cumplido:** 40% BTC (4,000 MXN) + 60% MXN, filtro SMA200 ±3%, sin ETH; gestor de riesgo aprueba con cambios. Boleta en `bitacora/boletas/2026-09-28.md` | 28-sep-2026 |
| Pronósticos calibrados | ≥50 resueltos, Brier ≤ 0.20, 3 meses | 5 registrados, 0 resueltos | 25-dic-2026 |
| Portafolio de papel (registro sombra) | 3 meses dentro de límites | Arranca el 28-sep | 28-dic-2026 |
| Patrimonio principal en real | Fin de fase 0 con la regla completa | — | ~28-dic-2026 |

## 5. Qué hace cada agente y cuándo (hora del centro de México)

Tres sesiones en la nube trabajan solas y dejan todo en git:
- **Motor de rutinas:** rutinas 1-6.
- **Inteligencia y cripto:** rutinas 7-8.
- **Supervisión, conciliación y revisión:** rutinas 9-11.

Los procedimientos están versionados en `rutinas/*.md` y se cambian ahí. La sesión principal orquesta, revisa y corrige.

| Rutina | Agente principal | Cuándo | Qué entrega |
|---|---|---|---|
| 1. Pre-apertura | analistas + `decisor` (sala de decisiones) | L-V 06:52 | Régimen, 3-5 pronósticos, riesgo, boletas del día verificadas y brief |
| 2. Laboratorio | `auditor-de-replicas`, `investigador-academico` | L-V 11:47 | Un tema de dominio sube de nivel, una réplica, un paper |
| 3. Cierre | `gestor-de-riesgo` | L-V 15:37 | Ejecuta el papel, valúa, cortacircuitos, post-mortems y marcador |
| 4. Auditoría semanal | `decisor` preside el comité | Vie 16:47 | Brier, 3 afirmaciones atacadas, rebalanceo y avance del plan |
| 5. Balance mensual | todos | Día 1, 10:13 | Examen de 20 preguntas, reporte mensual y fase 0 del patrimonio |
| 6. Barrido trimestral | `investigador-academico` | 5-ene, abr, jul y oct | Literatura, SPIVA y regulación |
| 7. Inteligencia | `vigia-de-informacion` | Diario 07:05, 11:05, 15:05 y 20:05 | Redes, prensa, revistas, papers, ensayos y YouTube graduados A-D; alertas |
| 8. Cripto | `analista-cripto` | Cada 4 h, 24/7 (estudio profundo a las 08:17) | Pulso de BTC/ETH, carrera cripto en `conocimiento/cripto/` y un pronóstico diario |
| 9. Supervisión en vivo | `supervisor` + `herramientas/supervision.py` | L-V cada hora, 08:40-14:40 | Stops, cortacircuitos, tope de 10k, filtro de apalancados, latidos y bloqueos |
| 10. Conciliación y arbitraje | `conciliador-arbitro` | Diario 18:23 | Registros cuadrados y fallos sobre desacuerdos de hechos o reglas |
| 11. Revisión de calidad | `revisor` | Diario 21:13 | Lista de calidad sobre todo lo del día y resumen para el dueño en el brief |

**Comité completo:**
- `analista-macro`, `analista-fundamental`, `analista-cuantitativo` y `analista-geopolitico`;
- `abogado-del-diablo`;
- `gestor-de-riesgo`, con veto;
- `verificador`, `auditor-de-replicas` e `investigador-academico`;
- los seis agentes nuevos: `vigia-de-informacion`, `revisor`, `decisor`, `supervisor`, `conciliador-arbitro` y `analista-cripto`.

**Mecanismos comunes:**
- Cada rutina deja una línea de latido en `bitacora/estado-rutinas.md`.
- Las dudas se deciden de forma conservadora y se anotan en `bitacora/decisiones-pendientes.md`; nunca se quedan esperando.
- Las alertas van a `bitacora/alertas.md`.
- Las boletas reales, a `bitacora/boletas/`.

## 6. Qué necesita el sistema del dueño

1. **Saldos de los rivales en GBM y en Binance.** Cada viernes, o cuando se pueda: cuenta, fecha, valor en MXN y aportaciones. Sin esto el marcador está vacío.
2. **Fecha de fondeo de cada cuenta rival**, para saber cuándo empezó la temporada.
3. **Cada ejecución real de la arena:** precio, títulos y hora de cada orden capturada en GBM, y el valor de la cuenta cada viernes.
4. **Montos y fechas de las aportaciones adicionales**, y qué resultado las dispara (`escalamiento_capital.pendiente_de_definir_por_el_dueno`).
5. **Cuenta propia en Bitso, abierta y verificada antes del 2-oct-2026** (con una prueba de depósito y retiro). Es la salida de emergencia si Binance restringe México o congela retiros (`cripto_binance.contingencia_contraparte`).

## 7. Límites prácticos de "todo el tiempo"

- **La restricción que manda es el calendario.** La calibración y el papel necesitan 3 meses reales, y ningún número de agentes acorta eso.
- **Más corridas gastan el límite semanal de uso de la cuenta.** El 25-sep ya se agotó una vez y detuvo todo. Con las rutinas 7-11 son ~22 corridas por día hábil. Para contenerlo:
  - las sesiones 7-11 usan un modelo más económico;
  - la supervisión horaria corre un script determinista.

  Si el límite se agota, se detienen **todas** las rutinas por igual hasta que se reinicie. No hay prioridad automática entre ellas.
- **Las rutinas corren en los momentos que mueven la aguja:** antes de abrir, al cierre, el viernes, el día 1 y el trimestre. Entre esos momentos no hay nada que decidir.

## 8. Avance (lo actualiza la auditoría del viernes)

| Indicador | Valor | Fecha |
|---|---|---|
| Pronósticos registrados / resueltos | 5 / 0 | 25-sep-2026 |
| Brier acumulado | n/d | — |
| Cuenta real arena: TWR / drawdown máximo | Arranca el 28-sep | — |
| Portafolio de papel: TWR / drawdown máximo | Arranca el 28-sep | — |
| Rivales con datos | 0 | — |
| Días para fin de fase 0 del patrimonio principal | ~94 | 25-sep-2026 |
