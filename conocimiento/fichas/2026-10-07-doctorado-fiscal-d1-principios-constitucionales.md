# Ficha · Doctorado derecho fiscal D1 · Principios constitucionales del art. 31, fr. IV (legalidad, proporcionalidad, equidad y destino al gasto público) y su efecto en el inversionista persona física

**Pregunta.** ¿Qué exige el art. 31, fr. IV, de la Constitución a una contribución y qué cambia para el inversionista persona física? En concreto: la ganancia en bolsa paga una tasa cedular plana de 10% (art. 129 LISR), mientras el resto del ingreso paga la tarifa progresiva (arts. 96 y 152). ¿Cuánto difieren las dos cargas y es compatible un impuesto cedular plano con la proporcionalidad y la equidad según la Suprema Corte?

## 1. Fuente y nivel de acceso real
| Fuente | Versión | Acceso | Grado |
|---|---|---|---|
| Constitución Política de los Estados Unidos Mexicanos, PDF de diputados.gob.mx (`LeyesBiblio/pdf/CPEUM.pdf`, sha256 `ca63a23a4b7444eb…`) | "Últimas reformas publicadas DOF 02-06-2026"; la fr. IV del art. 31 dice "Fracción reformada DOF 25-10-1993, 29-01-2016" | **Art. 31 leído íntegro** (descarga y extracción de texto hoy) | A |
| Ley del ISR, PDF de diputados.gob.mx (`LISR.pdf`, sha256 `803c2875c09c751c…`) | "Última reforma publicada DOF 01-04-2024" | **Arts. 96 (primer párrafo), 129 y 152 leídos íntegros**. Las tarifas de los arts. 96 y 152 vienen como imagen en el PDF y no se extraen como texto: se tomaron del Anexo 8 | A |
| Anexo 8 de la RMF 2026, PDF de sat.gob.mx (`documentos2026/rmf/anexos/Anexo-8-RMF-2026_DOF-28122025.pdf`, sha256 `69ebaf8a78a3bde5…`, el mismo hash del cap. 32) | DOF domingo 28-dic-2025; apartado C, fr. II: "Tarifa para el cálculo del impuesto correspondiente al ejercicio de 2026 a que se refieren los artículos 97 y 152 de la Ley del ISR" | **Tabla de 11 tramos leída y copiada cifra por cifra** | A |
| Semanario Judicial (sjf2.scjn.gob.mx), bj.scjn.gob.mx y sjf.scjn.gob.mx | — | **No accesibles**: el portal responde con una página de bloqueo (Incapsula) y bucles de redirección. **nv** en fuente oficial | — |
| Tesis 2a. XVI/2017 (10a.), registro 2013887; 2a. XX/2017 (10a.), registro 2013888; 2a. XL/2017 (10a.), registro 2013889; 2a. XLI/2017 (10a.), registro 2013898 | Según la fuente secundaria: Segunda Sala, tesis **aisladas**, Gaceta SJF, libro 40, marzo de 2017, tomo II | **Texto leído solo en un compendio privado** (sdv.com.mx), no en el SJF. Rubros y texto sin cotejo oficial | C (pendiente de cotejo) |

No se cita de memoria ninguna jurisprudencia sobre la definición general de proporcionalidad o equidad. Las tesis "clásicas" que la definen quedan **nv** hasta tener acceso al SJF.

## 2. Supuestos y derivación
**Texto (A).** Art. 31: "Son obligaciones de los mexicanos: … IV. Contribuir para los gastos públicos, así de la Federación, como de los Estados, de la Ciudad de México y del Municipio en que residan, de la manera proporcional y equitativa que dispongan las leyes."

De esa sola oración salen los cuatro principios:
1. **Destino al gasto público:** "Contribuir para los gastos públicos".
2. **Proporcionalidad:** "de la manera proporcional". La palabra no dice "progresiva". Que la Corte la lea como contribuir según la capacidad contributiva, con tarifas progresivas como medio habitual, es doctrina de jurisprudencia que aquí queda **nv** (no se cita de memoria).
3. **Equidad:** "y equitativa". Trato igual a los iguales y desigual a los desiguales: es la lectura que aplican las tesis 2013887 y 2013888 (C), que justifican el trato distinto porque las categorías "no se ubican en un plano de equivalencia".
4. **Legalidad (reserva de ley):** "que dispongan las leyes". Los elementos del tributo (sujeto, objeto, base, tasa) deben estar en ley. La tesis 2013898 (C) aplica esta vertiente a una regla de la RMF 2014 sobre el art. 129 y concluye que la regla no la viola.

**Ley (A).**
- Art. 152 LISR: la persona física suma los ingresos de los Capítulos I, III, IV, V, VI, VIII y IX y aplica la tarifa; "No será aplicable lo dispuesto en este artículo a los ingresos por los que no se esté obligado al pago del impuesto y por los que ya se pagó impuesto definitivo".
- Art. 129 LISR: "aplicando la tasa del 10% a las ganancias obtenidas en el ejercicio", con pago "definitivo", por la enajenación en bolsa concesionada o mercado reconocido de acciones mexicanas, de acciones extranjeras listadas en esas bolsas, de títulos que representen índices accionarios y de los derivados de capital de las frs. I a IV. La declaración se presenta "de manera conjunta a la declaración anual" (art. 150). Las pérdidas solo se restan de ganancias del mismo régimen "en el ejercicio o en los diez siguientes". No aplica a quien, con 10% o más de las acciones, enajene 10% o más en 24 meses (numeral 2), entre otros casos.
- Art. 96 LISR: retención mensual sobre salarios como pago provisional a cuenta del anual. La tarifa mensual está en el Anexo 8 y no se usa en el ejercicio.

**Consecuencia lógica.** La ganancia del art. 129 queda **fuera** de la base del art. 152. Su tasa es la misma para quien gana 50 mil y para quien gana 50 millones, y no se mezcla con el resto de los ingresos de la persona.

**Supuestos del ejercicio.** La base gravable ya es neta de deducciones. No hay deducciones personales (art. 151) ni subsidio. La ganancia cumple todos los requisitos del art. 129. Ejercicio 2026.

## 3. Ejercicio numérico (código: `fichas/codigo/2026-10-07-principios-tributarios.py`)
**Tarifa 2026 (Anexo 8, C, fr. II), copiada cifra por cifra.** Límites inferiores: 0.01 · 10,135.12 · 86,022.12 · 151,176.20 · 175,735.67 · 210,403.70 · 424,353.98 · 668,840.15 · 1,276,925.99 · 1,702,567.98 · 5,107,703.93. Cuotas fijas: 0 · 194.59 · 5,051.37 · 12,140.13 · 16,069.64 · 22,282.14 · 67,981.92 · 125,485.07 · 307,910.81 · 444,116.23 · 1,601,862.46. Tasas: 1.92 · 6.40 · 10.88 · 16.00 · 17.92 · 21.36 · 23.52 · 30.00 · 32.00 · 34.00 · 35.00%.

**(1) Progresividad del art. 152.**
| Base gravable | ISR | Tasa efectiva | Tasa marginal |
|---|---|---|---|
| 50,000 | 2,745.94 | 5.49% | 6.40% |
| 100,000 | 6,572.16 | 6.57% | 10.88% |
| 250,000 | 30,739.91 | 12.30% | 21.36% |
| 500,000 | 85,773.86 | 17.15% | 23.52% |
| 1,000,000 | 224,833.03 | 22.48% | 30.00% |
| 2,000,000 | 545,243.12 | 27.26% | 34.00% |
| 5,000,000 | 1,565,243.12 | 31.30% | 34.00% |
| 10,000,000 | 3,314,166.08 | 33.14% | 35.00% |
| 50,000,000 | 17,314,166.08 | 34.63% | 35.00% |

La tasa efectiva crece en todo el rango (el script lo verifica con un assert) y tiende a 35% sin alcanzarlo. Verificación a mano para 1,000,000: 125,485.07 + (1,000,000 − 668,840.15) × 30% = 224,833.03.

**(2) Cedular plana del art. 129.** El ISR es 10% de la ganancia para cualquier monto: 5,000 sobre 50 mil y 5,000,000 sobre 50 millones. Es proporcional en sentido aritmético, pero no progresiva.

**(3) Una ganancia de 500,000 acumulada frente a la cedular** (ISR incremental = ISR(otros + G) − ISR(otros)):
| Otros ingresos | ISR incremental si se acumulara | Tasa incremental | Cedular 10% | Ahorro de la cedular |
|---|---|---|---|---|
| 0 | 85,773.86 | 17.15% | 50,000 | 35,773.86 |
| 150,000 | 109,041.70 | 21.81% | 50,000 | 59,041.70 |
| 400,000 | 132,053.12 | 26.41% | 50,000 | 82,053.12 |
| 1,000,000 | 154,461.47 | 30.89% | 50,000 | 104,461.47 |
| 3,000,000 | 170,000.00 | 34.00% | 50,000 | 120,000.00 |

El beneficio de la cedular **crece con el ingreso** de la persona. Para el que más tiene, la cedular resulta regresiva frente a la tarifa.

**(4) Equidad horizontal con el mismo ingreso total de 1,000,000.** Quien lo gana en salario paga 224,833.03 (22.48%). Quien lo gana en bolsa paga 100,000 (10%), es decir 2.25 veces menos. Es el supuesto de la tesis 2013887 (C): la Sala sostiene que no viola la equidad porque el salario es regular y constante y la ganancia bursátil es especulativa y está "sujeta a la volatilidad", así que las dos categorías no son equivalentes.

## 4. Evidencia y límites
- **Lo que la Corte habría dicho (C, sin cotejo oficial).** Las tesis aisladas de 2017 que se localizaron tratan el art. 129 bajo **equidad**: frente a los salarios (2013887), frente a las personas morales (2013888) y por el requisito de "gran público inversionista" (2013889, que además invoca la razonabilidad legislativa). También bajo **legalidad** (2013898, regla I.3.2.12 de la RMF 2014). **No se encontró una tesis que examine el art. 129 bajo proporcionalidad**, y no se afirma que exista ni que no exista: queda **nv**.
- **Respuesta a la pregunta, con su grado.** El texto constitucional (A) exige una contribución "proporcional", no "progresiva". Una tasa plana sobre una base que mide la ganancia neta (precio menos costo promedio actualizado y comisiones, con pérdidas compensables durante diez años) grava en proporción a esa manifestación de riqueza. Es un argumento razonable de compatibilidad, pero es inferencia propia (grado C), no jurisprudencia verificada. El punto débil está en la equidad y la progresividad global, no en la letra del art. 31: la persona de mayores ingresos paga menos en proporción a su ingreso total (cuadros 3 y 4). Las tesis localizadas resuelven ese punto a favor de la ley por la falta de equivalencia entre categorías, pero son aisladas, no jurisprudencia obligatoria.
- **Efecto práctico para el inversionista.** (a) Las ganancias del art. 129 no suben la tasa marginal del resto del ingreso. (b) El impuesto es definitivo: no se puede "optar" por la tarifa aunque convenga (ver contraejemplo). (c) Las pérdidas del art. 129 solo se compensan contra ganancias del mismo régimen. (d) Los ETFs extranjeros del SIC entran en las frs. I y II en la medida en que coticen en bolsa concesionada y cumplan los requisitos del art. 129; ese detalle está en el cap. 27 y no se revisó aquí.
- **Límites.** No se verificaron en el SJF ni el rango, ni el texto, ni la vigencia de ninguna tesis. No se modelan dividendos (art. 140, 10% adicional), intereses reales, deducciones personales ni el ajuste por inflación del costo. La LISR usada es la de Diputados, con última reforma del 01-04-2024. No se revisó si la iniciativa 2027 (cap. 32) modifica los arts. 129 o 152 (nv).

## 5. Contraejemplo y segunda comprobación
**Contraejemplo: la cedular no siempre favorece al contribuyente.** Para quien no tiene otros ingresos, la tarifa del art. 152 aplicada a la sola ganancia sale **más barata** que el 10% mientras la ganancia esté por debajo de **194,724.65**, el punto de equilibrio calculado por bisección. Ahí la tarifa da 19,472.46, igual que la cedular (16,069.64 + (194,724.65 − 175,735.67) × 17.92% = 19,472.47 a mano). Con una ganancia de 30,000, la tarifa daría 1,465.94 (4.89%) y la cedular cobra 3,000. Con 100,000, 6,572.16 (6.57%) contra 10,000. Como el pago es definitivo y el art. 152 excluye lo "ya pagado como impuesto definitivo", el pequeño inversionista paga más que con la tarifa general. Por lo tanto, "la cedular es un privilegio" solo vale por encima de cierto nivel. Si alguien quisiera impugnar el régimen por proporcionalidad, este sería el argumento: una tasa plana que no atiende a la capacidad global de quien gana poco. Es inferencia propia, sin tesis que la respalde.

**Segunda comprobación.**
1. Consistencia de la tabla publicada: cada cuota fija coincide, dentro de ±0.05, con la anterior más el tramo por su tasa, y los tramos no tienen huecos (asserts).
2. ISR por dos métodos independientes: cuota fija + excedente (método A) y suma tramo por tramo sin usar las cuotas (método B). Coinciden a menos de 0.05 en los nueve niveles. La diferencia viene del redondeo de las cuotas publicadas.
3. Dos cifras recalculadas a mano (1,000,000 y el equilibrio).

## 6. Estado nuevo
**Documentado con comprobación.** Texto constitucional, LISR y Anexo 8 leídos en fuente primaria (A) y ejercicio comprobado en Python con dos métodos. La jurisprudencia queda en grado C (compendio secundario) y es **nv** en el SJF oficial, que está bloqueado desde este entorno. Siguiente prueba: cotejar en el SJF (con acceso desde un navegador) las tesis 2013887, 2013888, 2013889 y 2013898 y las jurisprudencias que definen proporcionalidad, equidad y legalidad tributaria; buscar si existe tesis sobre el art. 129 bajo proporcionalidad; escribir el capítulo D1 y un examen.
