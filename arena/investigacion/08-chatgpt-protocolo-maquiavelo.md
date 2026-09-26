# Rival ChatGPT: "Maquiavelo · Programa y Protocolo de Inversión" (registro de inteligencia)

**Registrado:** 25-sep-2026 (noche), sesión principal. **Identificación del rival [H]:** el propio documento, en sus versiones 1.1 y 1.3 (recibidas del dueño el 25-sep a las 04:53 y 05:10), dice: "Eduardo utiliza GBM, asigna aproximadamente $20,000 MXN exclusivamente a **ChatGPT** y prevé abrir una cuenta por participante". Es el protocolo de ChatGPT bajo el mismo nombre de persona ("Maquiavelo") que el dueño usa para todos sus asistentes.

## Lo que tenemos y lo que no

| Versión | Fuente | Estado |
|---|---|---|
| 1.1 y 1.3 | Archivos `.txt` subidos por el dueño el 25-sep (madrugada) | En disco; no se auditaron formalmente |
| **1.7 + Adenda 9** | Solo el resumen que ChatGPT le dio al dueño y que el dueño pegó en el chat (25-sep, ~20:00) | **No tenemos el archivo.** Lo que sigue es verificación de sus afirmaciones contra nuestra base, no una auditoría del documento |

## Las 5 afirmaciones de la Adenda 9, contra nuestra base

| # | Afirma ChatGPT | Qué dice nuestra base | Veredicto |
|---|---|---|---|
| 1 | LAB-VOL-001 era "una adaptación híbrida (riesgo diario, retornos mensuales), no una réplica completa de Daniel–Moskowitz ni una ejecución diaria" | [I] Escalar rendimientos mensuales por la varianza realizada de los datos diarios del mes anterior **es la construcción estándar de Moreira-Muir (2017)**, no un híbrido defectuoso; lo que no es, es Daniel-Moskowitz (2016), que es otra cosa (momentum dinámico con pronóstico de varianza del *factor* momentum). Nuestra R05 replica Moreira-Muir en el periodo del artículo y prueba la crítica de Cederburg et al. (2020): α post-2017 −0.75% (t −0.15), **descartada** para dinero. D-M está documentado con grado A en `conocimiento/02` §151 y `06` §162, con nuestra regla de control de crash (`02` §256), no replicado | Su corrección de alcance es honesta; su etiqueta "híbrido" mezcla dos artículos distintos. **Nosotros ya corrimos la prueba y la descartamos; ellos la dejaron "pendiente de ejecutar"** |
| 2 | Derivó el Sharpe con agregación temporal y un contraejemplo: √12 se sesga con autocorrelación | [H] Lo (2002, FAJ 58(4)) exactamente eso; en `conocimiento/07` §146, §224 y §353 tenemos además López de Prado-Lipton-Zoonekynd (2026, JPM), Jobson-Korkie con Memmel, Ledoit-Wolf (2008, bootstrap de bloques circulares) y el desuavizado de Getmansky-Lo-Makarov (2004) | Correcto y ya cubierto, con más profundidad en nuestra base |
| 3 | Diseñó "la réplica correcta, con bootstrap por bloques, costos y series temporalmente coherentes; pendiente ejecutarla al localizar insumos congelados/código de origen" | [H] Nuestro laboratorio ya exige doble ejecución independiente (auditor de réplicas), costos de GBM y segunda fuente de datos; R05 tiene `R05_verificacion.py`. 18 pruebas en la tabla maestra, 0 con ventaja demostrada | Diseño razonable; **no ejecutado**. Sin insumos ni código, no es evidencia |
| 4 | Confirmó la construcción oficial del factor Momentum de Kenneth French y separó teoría documentada de evidencia replicada | [H] V01 (MOM y RMW de EUA con datos de French, dos auditorías ciegas AC-01 y AC-02): replicado con diferencias, descartada; R02 (TSMOM): descartada; `02` §82 y `06` con las fuentes A | Correcto; nosotros ya lo replicamos y calificamos |
| 5 | Banxico mantiene la tasa objetivo en 6.50%; contexto, no recomendación | [H] Brief del 25-sep, línea 13: 6.50% por unanimidad, 24-sep, tercera pausa; fuente El Universal. Coincide | Correcto, ya en nuestro brief |

**Su siguiente investigación** ("reconciliar utilidad contable, flujo operativo, impuestos corriente/diferido y reinversión con reportes públicos de una empresa real"): [H] nosotros ya lo hicimos como modelo integrado de 3 estados con notas de 10-K/20-F para MSFT, NVDA, TSM, AMX y WALMEX (tarea #12, `conocimiento/03` §31-§88 y `25`). Van una etapa atrás en esto.

## Lectura de conjunto [I]

- El protocolo de ChatGPT sigue en fase de estudio y diseño ("queda pendiente ejecutarla"); no reporta ninguna prueba ejecutada con doble corrida ni una cartera decidida. Nosotros entramos en real el 28-sep con una decisión sellada y auditada.
- Lo que sí hace bien: separar teoría de evidencia replicada y corregir su propio alcance. Es el mismo estándar que el nuestro; no hay nada que copiar, pero sí que vigilar: si ejecuta esa réplica con bootstrap de bloques, hay que pedirle al dueño el paquete y auditarlo como el de Pepe v3.
- La cascada de horarios del rival (`07-horarios-de-la-competencia.md`) **podría** ser también de ChatGPT, porque su protocolo dice "rutinas activas"; no está confirmado.

## Pendiente

- Que el dueño suba `Maquiavelo_Inversion_Programa_y_Protocolo.md` v1.7 y, si existe, el paquete de LAB-VOL-001 (datos congelados y código). Con eso se hace una auditoría ciega como la de Pepe, no antes.
