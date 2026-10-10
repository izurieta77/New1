# Ficha de avance · 10-oct-2026 · Frontera DAT (cont.): el texto de los indentures de Strategy — ¿hay vencimiento acelerado ligado al precio de la acción o al mNAV?

> Corrida de las 08:17 CDMX (14:18 UTC), `analista-cripto`, estudio profundo. **Decisión del día:** se avanza uno de los pendientes explícitos de la ficha de ayer (`fichas/2026-10-09-dat-companies-mnav-riesgo.md`, §9) en lugar de abrir una frontera nueva, porque el propio orquestador lo señaló como disponible hoy (fuente primaria, consultable un sábado) y porque cierra directamente una pregunta que el §4 y el autoexamen (§8) de la ficha de ayer dejaron sin responder: *"¿qué rompería la lectura del umbral de 68.5% de caída? Un evento de vencimiento acelerado por incumplimiento de convenio no contemplado en esa ficha."* Hoy se lee el convenio mismo, no un resumen de prensa.

## 0. Pregunta de hoy, acotada

¿Alguno de los convenios (indentures) de las notas convertibles de Strategy Inc. contiene un evento de incumplimiento (default) que acelere el vencimiento del principal si el precio de la acción cae, si el mNAV cae por debajo de un umbral, o si el precio de BTC cae? Si no, ¿cuál es el mecanismo real que sí podría acelerar el vencimiento (cross-default), y qué tan sensible es a los US$6,713,659,000 de deuda convertible que Strategy reporta hoy?

## 1. Acceso y fuentes (declarado)

- **Acceso íntegro, fuente primaria, leída en vivo hoy, con doble verificación cruzada (dos series distintas, no una sola):**
  - **Serie A — "0.625% Convertible Senior Notes due 2030"**, emitida el 11-mar-2024. 8-K: `sec.gov/Archives/edgar/data/1050446/000119312524064321/d749312d8k.htm` (monto US$800M, incluye el ejercicio íntegro de la opción de US$100M). Indenture completo (Exhibit 4.1, ~347,140 caracteres): `.../000119312524064321/d749312dex41.htm`, leído en 4 tramos (offsets 0, 100000, 200000, 300000) para cubrir Artículo 1 (definiciones), Artículo 6 (Events of Default/Acceleration) y Artículo 14 (conversión).
  - **Serie B — "0% Convertible Senior Notes due 2030"**, emitida el 21-feb-2025. 8-K: `.../000119312525032800/d851880d8k.htm` (monto US$2,000M + opción de US$300M). Indenture completo (Exhibit 4.1, ~317,623 caracteres): `.../000119312525032800/d851880dex41.htm`, leído en 4 tramos (offsets 0, 100000, 200000, 300000), cubre Artículo 3 (covenants de reporte), Artículo 4 (Fundamental Change/redención), Artículo 5 (conversión) y Artículo 7 (Events of Default/Acceleration).
  - Ambos indentures están firmados con U.S. Bank Trust Company, National Association, como fiduciario (trustee), y ambos registrados bajo el expediente de registro automático de la compañía en SEC EDGAR (CIK 0001050446).
- **No se usó ningún resumen de prensa para esta parte de la ficha** — toda cita es del texto del indenture mismo, con el número de sección y cita literal entre comillas.
- **No se tocó** ninguna fuente de pago ni información no pública. Fin de semana: SEC EDGAR es un archivo público, consultable cualquier día.

## 2. Hallazgo central: no existe un disparador de default ligado al precio de la acción, al mNAV o al precio de BTC

Se leyeron de forma completa las secciones de **Events of Default** y **Acceleration** de las dos series (Secc. 6.01/6.02 en la Serie A de 2024; Secc. 7.01/7.02 en la Serie B de 2025 — la numeración cambió entre indentures, pero el contenido es equivalente). En ninguna de las dos aparece el precio de la acción, el mNAV o el precio de BTC como condición de un *Event of Default*:

| Evento de incumplimiento (ambas series, equivalente) | ¿Ligado a precio/mNAV/BTC? |
|---|---|
| Impago de principal al vencimiento, redención, recompra o aceleración | No |
| Impago de intereses (30 días consecutivos) | No (y en la Serie B, los intereses "especiales" de hasta 0.50%/año son solo por incumplir reportes SEC o no ser "Freely Tradable", no por precio) |
| Incumplimiento de la obligación de convertir | No |
| Omisión de avisos (cambio fundamental, make-whole) | No (es un defecto de procedimiento, no de precio) |
| Incumplimiento del artículo de fusiones/consolidación | No |
| Incumplimiento de "otros convenios" (60 días tras aviso del fiduciario o de ≥25% de tenedores) | No — es un cajón residual, pero no hay ningún covenant financiero de mNAV o de razón deuda/activos en el cuerpo del indenture que pueda caer aquí |
| **Cross-default**: deuda financiera ("indebtedness for money borrowed") de la Compañía o de una filial significativa que se acelere o no se pague, por encima de un umbral en dólares | No — el umbral es un monto fijo en dólares, no un precio ni un múltiplo (ver §3) |
| Quiebra voluntaria o involuntaria | No |

**El precio de la acción sí aparece en el texto, pero nunca como evento de incumplimiento:**
- Determina si el **tenedor puede convertir** anticipadamente (Serie B, Secc. 5.01(C): se activa si el precio del bono cae bajo 98% del valor de conversión; Serie A, Secc. 14.01(b)(iv): conversión libre si el precio de cierre ≥130% del precio de conversión durante 20 de 30 días).
- Determina si la **Compañía puede redimir anticipadamente** las notas a su elección (Serie B, Secc. 4.04(B): solo si el precio de cierre supera 130% del precio de conversión — es una opción a favor de la empresa, no un riesgo para ella).
- Alimenta la tabla de "Make-Whole Fundamental Change" que ajusta cuántas acciones adicionales recibe el tenedor si hay un cambio de control antes del vencimiento (protección al tenedor, no aceleración automática).

**La "Fundamental Change" tampoco es un disparador de precio.** Su definición (Serie B, Secc. en Artículo 1-4) cubre cuatro supuestos: cambio de control de voto (>50%), venta de "todos o sustancialmente todos" los activos, liquidación aprobada por accionistas, o deslistado de NYSE. Ninguno usa el precio de la acción, el mNAV ni el precio de BTC. Y lo más importante: **un Fundamental Change no acelera el vencimiento por sí mismo** — da al tenedor un **derecho de recompra** ("Fundamental Change Repurchase Right", a elección del tenedor, al valor de principal más intereses), que es un mecanismo completamente distinto de una aceleración forzosa.

## 3. El mecanismo real que sí podría acelerar: cross-default, y es sensible al tamaño de la deuda de un tercero, no al precio de BTC

El único camino hacia una aceleración "por fuera" de un impago directo es el **cross-default** (Serie A Secc. 6.01(g); Serie B Secc. 7.01(A)(vii)): si la Compañía **o cualquier filial significativa** incumple el pago de "indebtedness for money borrowed" (deuda por dinero prestado) por encima de un umbral, y esa aceleración no se anula en 30 días, se activa un *Event of Default* en **esta** serie también — es el mecanismo por el que un problema de pago en una serie de notas (o en cualquier otra deuda de ese tamaño) puede "contagiar" a las demás series.

**El umbral cambió de forma importante entre las dos emisiones, con 11 meses de diferencia:**

```
Serie A (indenture 11-mar-2024): umbral de cross-default = US$30,000,000
Serie B (indenture 21-feb-2025): umbral de cross-default = US$200,000,000
Crecimiento del umbral = 200/30 = 6.67x en 11 meses

Deuda convertible total de Strategy (10-Q, 30-jun-2026) = US$6,713,659,000
Umbral A / deuda total de hoy = 30,000,000 / 6,713,659,000 = 0.447%
Umbral B / deuda total de hoy = 200,000,000 / 6,713,659,000 = 2.979%
```

Script verificado dos veces (ejecución directa + cálculo a mano a 4 decimales, coincide): `scratchpad/g4calc/cross_default.py`, fuera del repositorio.

**Lectura:** la protección contra un cross-default "accidental" (una deuda menor de un proveedor o de una filial pequeña arrastrando a toda la estructura de notas) se hizo **6.7 veces más laxa** en dólares absolutos conforme la compañía emitió más deuda — un patrón consistente con que el umbral de cross-default suele fijarse como una fracción razonable del tamaño total de la estructura de capital, no como un número arbitrario. Con el tamaño de deuda de hoy (US$6.71 mil millones), un cross-default requeriría que **una sola obligación de deuda** (no de acciones preferentes, ver §4) de al menos US$200 millones entrara en impago y no se resolviera en 30 días — un evento de una magnitud muy distinta a "el mNAV bajó de 1" o "BTC cayó X%".

## 4. Matiz importante: las acciones preferentes (STRK, STRF, STRC, STRD) probablemente no activan el cross-default de las notas

El texto de ambos indentures usa literalmente **"indebtedness for money borrowed"** ("deuda por dinero prestado") para definir qué cuenta en el cross-default (Serie A, Secc. 6.01(g), cita exacta: *"indebtedness for money borrowed in excess of $30,000,000"*). **No encontré, en las secciones leídas, una definición explícita de "Indebtedness" que diga en blanco y negro "excluye acciones preferentes"** — es una laguna declarada de esta ficha, no una conclusión verificada al 100%. Pero por convención estándar del lenguaje de mercado de deuda, "dinero prestado" se refiere a obligaciones de deuda (bonos, préstamos, líneas de crédito), **no** a dividendos de acciones preferentes, que son una obligación de capital (equity), no de deuda. Si esa lectura convencional es correcta —y es la interpretación más razonable del texto tal como está escrito, aunque no la verifiqué contra una definición explícita—, entonces **el no pago de un dividendo preferente (STRC, STRK, STRF, STRD), por grande que sea, no dispararía por sí mismo el cross-default de las notas convertibles.** Esto es relevante porque el riesgo de corto plazo que señaló la ficha de ayer (§4) era precisamente el flujo de caja de los dividendos preferentes, no un impago de deuda — y si esta lectura se sostiene, ese riesgo de dividendos preferentes queda más aislado de la deuda convertible de lo que una lectura superficial podría sugerir (sí presiona a diluir o a emitir más acciones, pero no arrastra directamente a un *Event of Default* en las notas).

**Esto se queda declarado como pendiente de verificación exacta** (ver §7): haría falta leer la definición completa de "Indebtedness" si existe en el Artículo 1 de cualquiera de los dos indentures (no apareció en los tramos leídos hoy) o, en su defecto, los términos de las propias series de acciones preferentes (certificados de designación, también en SEC EDGAR) para confirmar si tienen su *propio* mecanismo de default cruzado hacia las notas.

## 5. Autoexamen

- ¿Puedo reproducir cada cita sin ver la ficha? Sí: cada cita trae el número de sección y el accession number/URL exactos de SEC EDGAR; el script de cálculo es reproducible y está fuera del repositorio.
- ¿Qué rompería la lectura del §2-3? Que una de las **otras** series (2028, 2031, 2032, mencionadas en la ficha de ayer pero no leídas hoy) tuviera un covenant distinto — no se puede generalizar de n=2 a las 5+ series completas sin leerlas todas. Es un límite explícito, no una laguna oculta.
- ¿Qué rompería la lectura del §4? Encontrar la definición de "Indebtedness" y que incluya expresamente obligaciones de dividendos preferentes acumulados — no lo descarté, solo no lo encontré en las secciones leídas hoy.
- **Grado A** para las citas literales de los dos indentures (Events of Default, Acceleration, Fundamental Change) y para los montos verificados contra el 8-K primario de cada serie. **B** para el cálculo del §3 (reproducible, verificado dos veces). **C** para la lectura convencional de "indebtedness for money borrowed" del §4 (interpretación razonable, no verificada contra una definición explícita del documento). **D**: ninguna cifra de esta ficha depende de fuente secundaria — a diferencia de la ficha de ayer, hoy no se usó ningún dato de prensa.

## 6. Qué cambia para invertir

- **No cambia el filtro de tendencia de `arena-claude-binance`** (solo mira el precio de cierre de BTC/USDT; no tiene exposición a MSTR).
- **Sí refina la lectura de riesgo de cola de la ficha de ayer:** el escenario de "venta forzada de BTC por un covenant ligado al precio" que el §8 de ayer dejó como pregunta abierta **no existe** en el texto de estas dos series — la vía real de estrés es (a) el cross-default por impago de deuda de ≥US$200M (hoy, un umbral alto frente al tamaño de la compañía) o (b) la presión de caja de los dividendos preferentes, que **probablemente** (no verificado al 100%, §4) es una vía separada que dialuye o fuerza recompras con descuento, no un *Event of Default* directo en las notas. Esto hace la lectura del §4 de ayer ("la venta forzada de BTC es un escenario de cola lejano, no el riesgo de la semana que entra") **más sólida**, con evidencia primaria directa en vez de inferencia.

## 7. Pendientes

- Leer el texto de las series restantes (2028, 2031, 2032; nombres exactos por confirmar en EDGAR) para generalizar el hallazgo del §2-3 de n=2 a la familia completa de notas.
- Buscar la definición explícita de "Indebtedness" en el Artículo 1 de cualquiera de los indentures (no apareció en los tramos leídos hoy) para cerrar la laguna del §4.
- Verificar el 10-Q de Q3-2026 (esperado ~24-26-oct-2026) — sigue sin estar disponible, no se buscó hoy por ser prematuro.
- Verificar en EDINET/TDnet las cifras de Metaplanet y buscar el reporte original de Galaxy Digital (mar-2026) — pendientes de la ficha de ayer, no retomados hoy porque el tiempo de esta corrida se usó en los indentures.

Script de esta sesión: `scratchpad/g4calc/cross_default.py` (fuera del repositorio).
