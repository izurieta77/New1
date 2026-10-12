# Ficha · 11-oct-2026 · Doctorado contabilidad C5: impuesto diferido (NIC 12 / IAS 12) con reglas fiscales mexicanas

> Bloque de trabajo continuo (19:09 CDMX del 11-oct; 01:10 UTC del 12-oct). Tarea elegida por la regla de cobertura (REGLAS §0d): C5 estaba en "Sin". Se cubre solo la parte de impuestos diferidos; pensiones y pagos basados en acciones quedan pendientes.

## 1. Fuentes

- **IFRS Foundation, página oficial de la NIC 12** (`ifrs.org/issued-standards/list-of-standards/ias-12-income-taxes/`), leída hoy: objetivo, impuesto corriente, diferencias temporarias, reconocimiento de pasivos y activos diferidos, e historial (1996; adoptada por el IASB en 2001; enmiendas de 2010, 2016, mayo-2021 sobre transacción única y mayo-2023 sobre el Pilar Dos). Grado **A** para lo que dice el resumen; **el texto íntegro de la norma no se leyó** (requiere registro).
- **LISR** (copia local con última reforma DOF 01-04-2024): art. 9 (tasa 30%), art. 34 fr. VI (25% automóviles) y fr. VII (30% computadoras), art. 36 fr. II (automóviles deducibles hasta 175,000). Grado A en la letra; confirmar en la versión 2026.
- **No leídos:** NIF D-4 (CINIF, de pago) y ASC 740 (FASB, requiere registro). Las diferencias NIIF / NIF / US GAAP quedan pendientes.

## 2. Lo esencial (según el resumen oficial)

- **Diferencia temporaria** = importe en libros de un activo o pasivo menos su **base fiscal** (lo que se le atribuye para efectos fiscales).
- **Pasivo por impuesto diferido:** cuando recuperar el valor en libros hará pagar impuesto (libros > base fiscal en un activo).
- **Activo por impuesto diferido:** cuando hará pagar menos impuesto (libros < base fiscal en un activo, o un pasivo contable que se deducirá al pagarse), o por pérdidas y créditos no usados, **sujeto a condiciones** de recuperabilidad.
- **Regla general:** reconocer diferidos por todas las diferencias temporarias, con excepciones.
- **Tasas:** las promulgadas o prácticamente promulgadas al cierre (lo dice el resumen para el impuesto corriente; para el diferido falta leer el párrafo de la norma).

## 3. Ejercicio (código: `codigo/2026-10-11-c5-impuesto-diferido.py`, con aserciones)

**Caso A · equipo de cómputo de 90,000.** Contable: línea recta a 5 años. Fiscal: 30% anual (LISR 34 fr. VII).

| Año | Libros | Base fiscal | Diferencia imponible | Pasivo diferido (30%) | Movimiento en resultados |
|---|---:|---:|---:|---:|---:|
| 1 | 72,000 | 63,000 | 9,000 | 2,700 | +2,700 |
| 2 | 54,000 | 36,000 | 18,000 | 5,400 | +2,700 |
| 3 | 36,000 | 9,000 | 27,000 | 8,100 | +2,700 |
| 4 | 18,000 | 0 | 18,000 | 5,400 | −2,700 |
| 5 | 0 | 0 | 0 | 0 | −5,400 |

El diferido acumulado regresa a cero: la deducción acelerada solo **adelanta** el beneficio fiscal. Los movimientos suman cero (comprobado en el código).

**Caso B · provisión de vacaciones de 50,000** reconocida en el año 1 y pagada en el 2. El pasivo contable tiene base fiscal cero porque se deduce al pagarse: **activo diferido de 15,000** en el año 1, que se revierte en el 2.

**Caso C · automóvil de 300,000.** El LISR 36 fr. II solo deja deducir 175,000; los 125,000 restantes **nunca** se deducirán. No es una diferencia que se revierta. **Inferencia (D):** por la excepción de reconocimiento inicial de la NIC 12 (adquisición de un activo fuera de una combinación de negocios que no afecta ni la utilidad contable ni la fiscal), no se registra diferido por esa parte, y el efecto aparece año con año como partida de conciliación de la tasa efectiva. La excepción se cita de memoria, porque el resumen oficial no la detalla; falta leer el párrafo exacto.

**Simplificaciones declaradas:** años completos (el LISR 31 deduce por meses desde que se usa el bien), sin actualización por inflación de la deducción, sin valor residual y tasa constante.

## 4. Por qué importa para el sistema

- **Análisis de emisoras (C6/C10):** un pasivo diferido que crece año tras año en una empresa intensiva en capital indica deducción acelerada y no necesariamente deuda económica. Un activo diferido grande por pérdidas depende de utilidades futuras: es el renglón que se castiga primero en una crisis.
- **Conciliación de tasa efectiva:** las partidas permanentes (como el tope de automóviles o los gastos no deducibles) explican por qué la tasa efectiva de una emisora mexicana se aleja del 30%.

## 5. Pendientes

1. Texto íntegro de la NIC 12: excepción de reconocimiento inicial, no descuento, compensación y presentación.
2. NIF D-4 y ASC 740, con sus diferencias frente a la NIC 12.
3. Pensiones (NIC 19 / NIF D-3) y pagos basados en acciones (NIIF 2): el resto de C5.
4. Un caso real: la nota de impuestos diferidos de una emisora del universo, por ejemplo en un 20-F con NIIF.

**Grado:** resumen de la norma **A**; LISR **A** (versión 2024); ejercicio **comprobado en código**; tratamiento del caso C **D**.
