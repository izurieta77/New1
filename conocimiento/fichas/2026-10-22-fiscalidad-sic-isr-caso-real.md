# Ficha · Fiscalidad 2026 y SIC · ISR de una venta en el SIC con el portafolio real del dueño (LISR art. 129)

**Pregunta.** Si el dueño vende hoy lo que tiene en el SIC de GBM, ¿cuánto ISR causa? ¿Se compensan las ganancias de unas emisoras con las pérdidas de otras? ¿Qué parte de la "ganancia" es solo tipo de cambio?

Motivo: el 22-oct el dueño preguntó "¿qué vendemos y a dónde movemos todo para no seguir perdiendo?" (`datos/entrada-dueno/2026-10-22.md`). Esta ficha no responde qué hacer; mide el costo fiscal y de comisiones de vender.

## Fuente y nivel de acceso
| Fuente | Acceso | Grado |
|---|---|---|
| LISR art. 129, primer párrafo (fr. I-IV), segundo párrafo (suma entre emisoras), inciso a) (costo promedio actualizado), párrafos sobre intermediarios, pérdidas a diez años, pérdida del derecho y declaración con la anual (art. 150). Texto de Diputados, última reforma DOF 01-04-2024, SHA-256 `803c2875…f786`, el mismo PDF que bajé hoy de diputados.gob.mx y que está en `laboratorio/replicas/V05-spiva-y-fiscalidad-sic/datos/legal/LISR.txt` (L10146-L10356) | **Lectura íntegra** del artículo | A |
| CFF art. 17-A (factor de actualización; si es menor a 1, el factor es 1) | Sección, citada y leída en el cap. 29 §"Actualización [A]" | A (por referencia interna) |
| INPC ene, mar y ago 2026 (143.588; 145.544; 145.462) | Del cap. 29 (INEGI); no re-descargado hoy | B |
| Correo de GBM del 7-oct (SPYM: 3 a 1,648.50; comisión 12.36 + IVA 1.98) | `bitacora/real/operaciones.csv` | A (documento del intermediario) |
| Capturas del dueño del 22-oct (SIC a las 10:45 CDMX) | `datos/entrada-dueno/2026-10-22.md` | A (pantalla del intermediario) |
| Paquete Económico 2027 (art. 129 sin cambio; SIC sigue en 10%) | Ficha del barrido 2026-Q4 en el cap. 27 | B (iniciativa, no publicada en el DOF) |

## Supuestos
- Persona física residente en México, contrato con GBM (intermediario autorizado por la LMV, así que GBM calcula y emite la constancia).
- Comisión de venta igual a la de compra, 0.25% + IVA (la del correo de GBM). Para las cinco emisoras que no son de Claude, el costo sin comisión se infiere de la ganancia que muestra GBM (valor − ganancia), y la comisión de compra se supone igual.
- Precios de la captura de las 10:45 CDMX, no los de un cierre.

## Derivación (texto del art. 129)
1. **Tasa:** 10% definitivo sobre las ganancias del ejercicio por enajenar acciones de emisoras extranjeras cotizadas en una bolsa concesionada en México (fr. I; el SIC) y títulos que representan índices (fr. II; los ETF).
2. **Por emisora y luego se suman (segundo párrafo, literal):** "La ganancia o pérdida obtenida en el ejercicio se determinará, **sumando o disminuyendo**, según corresponda, las ganancias o pérdidas que deriven por la enajenación de acciones **de cada sociedad emisora** … que efectúe a través de **cada uno de los intermediarios**". Primero se calcula cada emisora con el inciso a); después **se netean entre emisoras** dentro del ejercicio.
3. **Costo (inciso a):** precio de venta menos comisiones de venta, menos el costo promedio con comisiones de compra, **actualizado** desde la adquisición hasta el mes inmediato anterior a la venta. Con el art. 17-A CFF, si el factor sale menor a 1, es 1.
4. **Pérdida neta del ejercicio:** solo se resta de ganancias de este mismo régimen, en el ejercicio o en los **diez siguientes**, actualizada. **Si no se resta pudiendo hacerlo, se pierde ese derecho.**
5. **Declaración:** con la anual del art. 150 (abril del año siguiente). GBM entrega la constancia, que incluye la de pérdida.
6. **Inferencia, no está en el texto:** el costo es "el monto efectivamente pagado" y en el SIC se paga en pesos. Por eso la depreciación del peso entra en la ganancia gravable aunque el ETF no haya subido en dólares.

## Ejercicio comprobado (`fichas/codigo/2026-10-22-sic-isr-caso-real.py`)
**Caso 1. SPYM del sublibro de Claude (3 títulos):**
- Venta neta: 5,043.00 − 14.62 = 5,028.38.
- Costo: 4,945.50 + 14.34 = 4,959.84.
- **Ganancia fiscal 68.54 MXN; ISR 6.85 MXN.**
- **Descomposición:**
  - SPYM **−2.17% en dólares** (91.66 → 89.66 USD);
  - el dólar **+4.24%** (17.985 → 18.7468);
  - en pesos, +1.97%, que cuadra con la captura.
- **Toda la ganancia gravable es cambiaria:** en dólares la posición pierde.

**Caso 2. Todo el SIC de la captura (seis emisoras de las tres IA, mismo contrato):**

| Venta | Resultado fiscal (con comisiones) | ISR |
|---|---|---|
| Todo | **−262.10** | **0**; constancia de pérdida por 262.10, compensable 10 años |
| Solo las ganadoras (SPYM, NFLX, LULU) | +218.26 | 21.83 |
| Solo las perdedoras (NVDA, UBER, FSLR) | −480.36 | 0; pérdida compensable |

- **Comisiones de ida y vuelta de todo el SIC: 133.30 MXN** (~0.58% de ~23,000). Pesan más que el ISR en cualquiera de los tres casos.
- **El resultado fiscal es del dueño, no de cada IA.** Los sublibros de Claude, Grok y ChatGPT están en el mismo contrato de GBM, así que la ley netea todas sus emisoras.

**Caso 3. Actualización del costo:**
- Compra en feb-2026 y venta en sep-2026: factor 145.462 / 143.588 = **1.013051**. Un costo de 10,000 pasa a 10,130.51.
- Compra en abr y venta en sep: el cociente da 0.9994 y se toma **1**.
- En el caso real (compra y venta en octubre) no hay periodo: el factor es 1.

## Evidencia empírica y límites
- **El ISR es pequeño ante el riesgo de mercado.** Una venta total hoy no causa ISR (resultado neto negativo) y cuesta ~133 MXN en comisiones.
- Lo que sí cambia al vender es la **exposición al dólar**. Pasar todo a pesos fija el tipo de cambio de hoy (18.75, +4.2% desde el 7-oct). Eso es una decisión de cartera (comité y dueño), no fiscal.
- **Límites:**
  - Las comisiones de las posiciones de Grok y ChatGPT son supuestas.
  - No se leyeron las reglas de la RMF 2026 sobre constancias. No sé si GBM aplica la actualización o la deja al contribuyente: nv.
  - Las fracciones de la sección USA (RLY, AOA, VOO) no son SIC: un ETF comprado en EUA a través de GBM USA no está en las fr. I-III, y su tratamiento no se cubre aquí.
  - Los dividendos de los ETF (retención en EUA y acreditamiento) no se tocan.

## Contraejemplo
Si las pérdidas de NVDA y UBER se realizan en 2026 y en 2027 no hay ganancias del régimen, la pérdida se arrastra y se actualiza. Pero si en algún ejercicio hay ganancia y el contribuyente no la resta, **pierde ese monto de pérdida para siempre**. El costo de un error administrativo puede superar el ISR del caso.

## Segunda comprobación
- La ganancia de SPYM se recalculó por otra vía: costo en USD × FX inicial × ((1 + r_USD)(1 + r_FX) − 1), menos las comisiones. Da 68.54, igual (`assert` en el código).
- La suma "ganadoras + perdedoras = todo" se comprueba con un `assert`, que es la aditividad que exige el segundo párrafo.

## Corrección de una ficha anterior
La ficha D8 del 10-oct decía que "la compensación entre emisoras del mismo ejercicio no está explícita en el texto". **Es incorrecto:** el segundo párrafo del art. 129 lo dice expresamente ("sumando o disminuyendo … las ganancias o pérdidas … de cada sociedad emisora"). Lo que se determina por emisora es el **cálculo** del inciso a), no el resultado del ejercicio. Queda en `registro-de-errores.md`.

## Estado nuevo
- **"Fiscalidad 2026 y SIC": de Documentado a Comprendido con comprobación.** Su siguiente prueba ("cálculo de ISR sobre ganancia SIC con caso numérico verificado") queda cumplida con un caso real y dos comprobaciones.
- **No sube a Contrastado.** Falta contrastarlo con una constancia real de GBM y con la RMF 2026. La aprobación del Paquete 2027 (Senado ~31-oct, DOF en noviembre) sigue en vigilancia.
- **D8:** se cierra la duda de la compensación entre emisoras. Sigue **Parcial** en `ESTADO.md`, porque faltan apalancados, derivados y cripto.
