# 32 — LISR Título II (personas morales), LIVA e IEPS a combustibles automotrices (áreas D5 y D6 del doctorado en derecho fiscal; caso: estación de servicio, régimen general)

> Nivel: doctorado (derecho tributario sustantivo de una persona moral del Título II de la LISR que revende gasolina y diésel) · Actualizado 2026-10-07 · Grado global: **A en la letra de la ley y de los acuerdos y decretos citados**, porque cada artículo, regla, acuerdo e iniciativa se leyó en el texto oficial (Cámara de Diputados, Gaceta Parlamentaria, SAT, SIDOF) y las frases entrecomilladas se verificaron mecánicamente contra ese texto (§10). **B** en las cifras calculadas (se comprobaron en Python, pero mezclan texto de ley con supuestos del caso). **C** en la aplicación al caso de la estación (inferencias sin regla expresa). **D / nv** en lo no leído (§9 y lista final). **Esto no es asesoría fiscal**: la presenta la empresa con su contador y su representante legal.

Capítulos relacionados que aquí no se repiten: [29 Código Fiscal de la Federación y defensa fiscal](29-codigo-fiscal-de-la-federacion-y-defensa-fiscal.md) (plazos de defensa, recargos, multas, caducidad) · [30 Portal del SAT para una persona moral](30-portal-sat-persona-moral.md) (e.firma, buzón, CFDI, controles volumétricos como trámite, calendario) · [27 Fiscalidad 2026 y estructura del SIC](27-fiscalidad-2026-y-estructura-sic.md) (persona física inversionista). Este capítulo trata **cuánto impuesto causa y cómo se determina**: ISR de la persona moral, IVA e IEPS de la cadena de combustibles, y qué cambia si se aprueba la iniciativa fiscal 2027.

**Convenciones.** Hecho = lleva artículo, regla o documento y fuente [n]. "**Inferencia:**" = razonamiento propio. "**Regla:**" = propuesta operable para el sistema, no para terceros. "(nv)" = no verificado en esta sesión. "**SUPUESTO**" = cifra inventada para el ejercicio, no dato de ninguna fuente. **Grados:** **A** = texto oficial leído y frase verificada mecánicamente; **B** = texto leído, pero la conclusión exige un cálculo o combinar fuentes; **C** = inferencia sin regla expresa o apoyada en fuente secundaria; **D** = no verificado o rumor. Siglas: LISR, LIVA, LIEPS, CFF, LFT (Ley Federal del Trabajo), LIF (Ley de Ingresos de la Federación), RMF (Resolución Miscelánea Fiscal para 2026, compilada con la Primera Modificación del 09-07-2026), CUFIN (cuenta de utilidad fiscal neta), UFN (utilidad fiscal neta), PP (pago provisional), AAI (ajuste anual por inflación), PTU (participación de los trabajadores en las utilidades), CNE (Comisión Nacional de Energía).

---

## 1. Objetivos de dominio

1. Determinar el ISR anual de una persona moral con la mecánica del art. 9 LISR (ingresos acumulables, deducciones, PTU pagada, pérdidas) y explicar el momento en que se acumula el ingreso (art. 17).
2. Dominar los requisitos de deducibilidad (arts. 25, 27 y 28) y aplicarlos a las erogaciones de una estación: costo de lo vendido, pago de combustible, IVA, nómina, intereses.
3. Calcular pagos provisionales con coeficiente de utilidad (art. 14), detectar cuándo conviene pedir coeficiente menor y medir el efecto de la iniciativa 2027.
4. Aplicar pérdidas fiscales (art. 57), PTU (art. 9 LISR y arts. 117 a 127 LFT) y AAI (arts. 44 a 46).
5. Distribuir utilidades sin impuesto adicional: CUFIN (art. 77), tasa del art. 10, retención del 10% (art. 140 y art. 164).
6. Operar el IVA: tasa del 16%, traslado, acreditamiento y sus requisitos (arts. 1, 4, 5 LIVA), saldo a favor y devolución (art. 6 LIVA y art. 22 CFF), retenciones (art. 1-A) y DIOT (art. 32 fr. VIII).
7. Entender el IEPS de combustibles automotrices en 2026: cuotas por litro, quién es contribuyente, quién acredita, y qué estímulos existen y para quién.
8. Resolver el caso de la estación de servicio y corregir las premisas que no son ciertas en derecho (§2.7).
9. Relacionar todo con la iniciativa del Ejecutivo del 8-sep-2026 (LISR y LIF 2027) con fuente primaria.

---

## 2. Núcleo

### 2.0 Fecha de los textos y reformas recientes (hechos con fecha)

- **LISR [1]:** texto vigente en Diputados, "Última reforma publicada DOF 01-04-2024". El índice de leyes vigentes de la misma Cámara muestra esa misma fecha como la última reforma de la LISR, así que el PDF **no va atrasado** (verificado en el índice [13]). El Paquete Económico 2026 (DOF 07-11-2025) no reformó la LISR; el cap. 27 ya lo había dicho.
- **LIVA [2]:** "Última reforma publicada DOF 12-11-2021", también confirmada en el índice [13].
- **LIEPS [3]:** "Última reforma publicada DOF 07-11-2025", con las cuotas actualizadas por el **Acuerdo 179/2025 (DOF 22-12-2025) [4]**. Ese acuerdo trae el factor 1.0379 (INPC de noviembre de 2025, 142.645, entre el de noviembre de 2024, 137.424).
- **LIF 2026 [5]:** nueva ley DOF 07-11-2025. El art. 20, apartado A, contiene los estímulos del diésel para quien lo consume (no para quien lo vende).
- **Decreto DOF 31-12-2025 [6]:** prorroga hasta el 31-dic-2026 los estímulos fronterizos de ISR e IVA y los decretos de estímulos del IEPS a combustibles (incluido el estímulo a estaciones en la franja fronteriza).
- **Iniciativa del Ejecutivo, 8-sep-2026 [11][12]:** reforma la LISR (Capítulo X, arts. 78-A a 78-F) y propone en la LIF 2027 (art. 25, fr. XIX) un régimen de pago del IEPS para quienes **no** son fabricantes, productores ni importadores de combustibles. Estado: **iniciativa**, no ley (§2.8).

### 2.1 LISR Título II: resultado fiscal, ingresos y deducciones

**Mecánica del art. 9 [A].** Las personas morales aplican "la tasa del 30%" al resultado fiscal del ejercicio. La utilidad fiscal es la totalidad de los ingresos acumulables menos las deducciones autorizadas "y la participación de los trabajadores en las utilidades de las empresas pagada en el ejercicio"; a esa utilidad se le restan las pérdidas fiscales pendientes. El impuesto se paga con declaración "dentro de los tres meses siguientes a la fecha en la que termine el ejercicio fiscal" (31 de marzo si el ejercicio es el año natural).

**Ingreso acumulable (arts. 16 y 17) [A].** Se acumulan todos los ingresos "en efectivo, en bienes, en servicio, en crédito o de cualquier otro tipo". No son acumulables los dividendos que una persona moral reciba de otra residente en México (art. 16, último párrafo). En venta de bienes el ingreso se obtiene cuando ocurra primero: se expide el comprobante, se entrega el bien o se cobra el precio (art. 17, fr. I, a, b y c). **Inferencia:** en una estación de servicio la entrega y el cobro coinciden en el despachador; la factura global (cap. 30) no difiere el ingreso.

**Deducciones autorizadas (art. 25) [A].** Entre otras: devoluciones, descuentos y bonificaciones; **el costo de lo vendido**; gastos netos; inversiones; créditos incobrables; cuotas IMSS patronales; intereses devengados a cargo; el AAI deducible; y los anticipos de sociedades cooperativas.

**Requisitos del art. 27 que pesan en una estación [A].**

| Fracción | Qué exige | Efecto en la estación |
|---|---|---|
| I | "Ser estrictamente indispensables para los fines de la actividad del contribuyente" | Criterio de fondo de todo gasto |
| III | Comprobante fiscal y pagos de más de $2,000.00 por transferencia, cheque nominativo, tarjeta o monedero autorizado | Proveedores de mostrador y servicios |
| III, 2.º párrafo | Combustible para vehículos marítimos, aéreos y terrestres: pago por esos medios "aun cuando" no exceda $2,000.00 y el comprobante debe traer el permiso vigente del proveedor y que no esté suspendido | **Lo cumple la estación como comprador** (sus camionetas) y **lo exigen sus clientes empresariales** al comprarle |
| IV | "Estar debidamente registradas en contabilidad y que sean restadas una sola vez" | Base de cualquier ajuste por inventario |
| V | Cumplir retenciones y entero a cargo de terceros; en pagos que son ingreso de salarios, comprobantes y alta en IMSS | Nómina del despachador |
| VI | IVA trasladado en forma expresa y por separado en el comprobante, más retención de IVA cuando proceda | Se liga con el acreditamiento (§2.5) |
| XIII | Costo de adquisición e intereses "correspondan a los de mercado" | Compras a partes relacionadas |
| XVIII | Requisitos a más tardar el último día del ejercicio; comprobante antes de la fecha de la declaración | Cierre anual |

**Partidas no deducibles (art. 28) [A].** Interesan la fr. III (el ISR propio y los accesorios, salvo recargos efectivamente pagados), la **fr. XV** (el IVA o IEPS que el contribuyente pagó o le trasladaron, salvo cuando no tenga derecho a acreditarlos y el gasto o inversión sea deducible; y tampoco el IVA ni IEPS trasladado de una erogación que no sea deducible), la fr. XXVI (participaciones en la utilidad), la fr. XXX (pagos que son ingreso exento del trabajador: 0.53 o 0.47 del monto) y la fr. XXXII (intereses netos por arriba del 30% de la utilidad fiscal ajustada, solo si los intereses devengados exceden de $20,000,000.00).

**Controles volumétricos y deducibilidad [A/C].** La LISR no contiene la palabra "volumétricos" (0 coincidencias en LISR, LIVA, LIEPS y LIF 2026). La obligación está en el **CFF art. 28, fr. I, apartado B**: quien "enajene cualquier tipo de hidrocarburo o petrolífero" debe contar con equipos y programas informáticos, certificados y dictámenes de laboratorio, y los controles volumétricos "formarán parte de la contabilidad del contribuyente". Las consecuencias son de infracciones (CFF art. 81 fr. XXV y 82 fr. XXV, cap. 30) y de **presunción**: el CFF art. 56, fr. VII, permite determinar presuntivamente diferencias de más de 0.5% en líquidos. **Inferencia (C):** no hay una causal expresa de no deducibilidad por no llevar controles; el riesgo para la deducción del costo pasa por el art. 27, fr. IV (registro en contabilidad) y por la presunción del art. 56. El requisito de controles **sí** es expreso para pedir en devolución el estímulo fronterizo (RMF 11.7.1, apartado A, fr. III, inciso b, §2.6).

### 2.2 Pagos provisionales (art. 14) y coeficiente de utilidad

**Hechos [A].** Los pagos son mensuales, "a más tardar el día 17 del mes inmediato posterior". Fr. I: coeficiente de utilidad = utilidad fiscal del último ejercicio de doce meses entre los ingresos nominales del mismo ejercicio. Si no resulta coeficiente, se usa el del último ejercicio de doce meses que lo tenga, "sin que ese ejercicio sea anterior en más de cinco años". Fr. II: utilidad fiscal del PP = coeficiente por ingresos nominales acumulados del año hasta el mes, menos (a) la **PTU pagada en el mismo ejercicio, "por partes iguales" en los pagos de mayo a diciembre**, (b) anticipos de cooperativas y (c) la pérdida fiscal de ejercicios anteriores. Fr. III: tasa del art. 9 sobre esa utilidad, acreditando los PP anteriores. **Ingresos nominales** son "los ingresos acumulables, excepto el ajuste anual por inflación acumulable". Inciso b) del último párrafo: quien estime que su coeficiente es superior al del ejercicio puede, "a partir del segundo semestre", solicitar autorización para aplicar uno menor; si resulta que pagó menos, cubre recargos.

**Declaraciones [A].** Se presentan siempre que haya impuesto a pagar, saldo a favor o cuando sea la primera declaración sin impuesto a cargo.

### 2.3 Pérdidas fiscales, PTU y ajuste anual por inflación

**Pérdidas (art. 57) [A].** La pérdida fiscal es la diferencia cuando las deducciones superan los ingresos, **incrementada con la PTU pagada**. Se disminuye "de la utilidad fiscal de los diez ejercicios siguientes hasta agotarla". Si pudiendo no se disminuye en un ejercicio, se pierde el derecho "hasta por la cantidad en la que pudo haberlo efectuado". Se actualiza con el factor desde el primer mes de la segunda mitad del ejercicio en que ocurrió hasta el último mes del mismo, y luego, hasta el último mes de la primera mitad del ejercicio en que se aplica. El derecho es personal y no se transmite ni siquiera por fusión.

**PTU [A].** La LFT art. 117 remite al porcentaje que fije la Comisión Nacional para la Participación de los Trabajadores en las Utilidades de las Empresas; art. 120: la utilidad es "la renta gravable, de conformidad con las normas de la Ley del Impuesto sobre la Renta"; art. 122: el reparto se hace "dentro de los sesenta días siguientes a la fecha en que deba pagarse el impuesto anual"; art. 123: la utilidad repartible se divide en dos mitades (días trabajados y salarios); art. 127: no participan directores, administradores y gerentes generales, y el monto tiene "como límite máximo tres meses del salario del trabajador o el promedio de la participación recibida en los últimos tres años" (el más favorable al trabajador, fr. VIII); art. 126, fr. I: las empresas de nueva creación quedan exceptuadas el primer año. En la LISR, art. 9: la renta gravable para PTU **no disminuye** la PTU pagada ni las pérdidas, y se disminuyen de los ingresos las cantidades no deducibles de la fr. XXX del art. 28. La PTU pagada se deduce en el art. 9 (y en los PP, art. 14, fr. II, a), pero no es deducible "de los ingresos acumulables" por la vía del art. 28 fr. XXVI. **El 10%** que se usa como porcentaje **no se leyó en la resolución de la Comisión Nacional: es SUPUESTO (nv)**.

**AAI (arts. 44 a 46) [A].** Al cierre de cada ejercicio: saldo promedio anual de deudas y de créditos (suma de saldos al último día de cada mes entre los meses del ejercicio, sin intereses devengados del mes). Si deudas > créditos, la diferencia por el factor de ajuste anual es **ingreso acumulable**; si créditos > deudas, es **deducible**. Factor = (INPC del último mes del ejercicio entre el del último mes del ejercicio anterior) menos uno. **No son créditos** "el efectivo en caja" (art. 45, fr. VII), los pagos provisionales de impuestos ni los estímulos fiscales (fr. IV), ni los préstamos al personal (fr. III). Los saldos a favor de contribuciones son créditos solo desde el día siguiente a su declaración. Son deudas (art. 46) las obligaciones en numerario pendientes, las contribuciones causadas desde el último día del periodo y hasta su pago, y los pasivos y reservas deducibles.

### 2.4 Dividendos, CUFIN y retención del 10%

**CUFIN (art. 77) [A].** Se adiciona con la UFN del ejercicio y con dividendos recibidos de otras PM residentes, y se disminuye con dividendos pagados de su saldo. UFN del ejercicio = resultado fiscal menos (I) el ISR pagado conforme al art. 9, (II) las partidas no deducibles (excepto art. 28 frs. VIII y IX y la PTU del art. 9, fr. I) y (III) el monto de la fórmula de impuestos pagados en el extranjero. El saldo se actualiza al cierre y a la fecha de distribución o percepción.

**Dividendo sobre el saldo (art. 10) [A].** Quien distribuye dividendos o utilidades **calcula el impuesto** multiplicando el dividendo por el factor **1.4286** y aplicando la tasa del art. 9 (30%); "no se estará obligado" cuando provengan de la CUFIN; el pago es **definitivo** (a más tardar el día 17 del mes siguiente) y puede acreditarse contra el ISR del ejercicio y de los dos siguientes; el acreditamiento reduce la UFN en "impuesto acreditado entre el factor 0.4286". **No se consideran dividendos la PTU.** Reducción de capital: art. 78.

**Retención del 10% [A].** El art. 140, 2.º párrafo, fija a las personas físicas "una tasa adicional del 10%" sobre dividendos o utilidades distribuidos por personas morales residentes; éstas "estarán obligadas a retener el impuesto" y lo enteran con el pago provisional del periodo; el pago es definitivo. A residentes en el extranjero: art. 164, fr. I, retención con "la tasa del 10%". Son dividendos para el art. 140 también los préstamos a socios que no cumplan el plazo menor a un año y tasa mínima (fr. II) y las erogaciones no deducibles que beneficien a accionistas (fr. III). El pagador debe expedir constancia y comprobante (art. 76, fr. XI).

### 2.5 LIVA: tasa, acreditamiento, saldo a favor, retenciones, DIOT

**Tasa y traslado (art. 1) [A].** "la tasa del 16%"; el IVA "en ningún caso se considerará que forma parte de dichos valores"; el traslado es "en forma expresa y por separado". El contribuyente paga la diferencia entre el impuesto a su cargo y el trasladado o pagado en importación, "siempre que sean acreditables".

**Valor en enajenaciones (art. 12) [A].** Precio pactado más "las cantidades que además se carguen o cobren al adquirente por otros impuestos, derechos, intereses normales o moratorios" Esto metería el IEPS en la base, **salvo** la cuota del art. 2-A LIEPS (ver §2.6).

**Acreditamiento (arts. 4 y 5) [A].** Es restar el impuesto acreditable (el trasladado y el pagado en importación "en el mes de que se trate"). Requisitos del art. 5: (I) gastos "estrictamente indispensables", que son los deducibles para ISR (si son parcialmente deducibles, el IVA acredita en esa proporción); (II) traslado expreso y por separado en comprobante; (III) **efectivamente pagado** en el mes; (IV) retenciones enteradas; (V) proporciones cuando hay actividades gravadas y no gravadas, e inversiones con ajuste a 60 meses.

**Pago mensual (art. 5-D) [A].** "a más tardar el día 17 del mes siguiente"; pago = impuesto del mes menos acreditable y retenciones.

**Saldo a favor (art. 6) [A].** Se acredita en meses siguientes "hasta agotarlo" o se solicita su devolución sobre el total del saldo; lo solicitado no puede acreditarse después. **Devolución (CFF art. 22) [A]:** la autoridad debe devolver "dentro del plazo de cuarenta días" desde la solicitud completa; puede requerir datos dentro de veinte días. **RMF 2.3.4 [A]:** se solicita con el FED y la DIOT del periodo debe estar presentada.

**Retenciones (art. 1-A) [A].** Las personas morales retienen el IVA cuando reciben servicios personales independientes u otorgamiento de uso o goce de personas físicas, adquieren desperdicios, reciben **servicios de autotransporte terrestre de bienes** (inciso c, prestado por personas físicas o morales) o servicios de comisionistas personas físicas. La **tasa de retención no está en la ley** (el art. 1-A remite al reglamento para autorizar una menor): **nv**, no se leyó el Reglamento de la LIVA. Se entera el día 17 del mes siguiente (o con el pago del mes) y no cabe acreditamiento contra el entero.

**DIOT (art. 32, fr. VIII) [A].** Información mensual de "pago, retención, acreditamiento y traslado" con proveedores, desglosada por tasa, "a más tardar el día 17 del mes inmediato posterior". El Anexo 1 de la RMF la lista como "DIOT" con programa electrónico (SAT); el formato del layout no se leyó (nv).

### 2.6 LIEPS aplicado a combustibles automotrices

**Cuotas 2026 [A].** Art. 2.º, fr. I, inciso D, y art. 2.º-A, con el Acuerdo 179/2025 [4] (vigentes desde el 1-ene-2026):

| Combustible | Art. 2.º, fr. I, D (pesos por litro) | Art. 2.º-A (centavos por litro) |
|---|---:|---:|
| Gasolina menor a 91 octanos | 6.7001 | 59.1390 |
| Gasolina mayor o igual a 91 octanos | 5.6579 | 72.1605 |
| Diésel | 7.3634 | 49.0817 |
| Combustibles no fósiles | 5.6579 | no aplica |

**Quién paga: el hecho que corrige el encargo [A].** El **art. 8.º, fr. I, inciso c)**: "No se pagará el impuesto" en las enajenaciones "que realicen personas diferentes de los fabricantes, productores o importadores" de los bienes de los incisos C), D), G) y H) y del art. 2.º-A, y esas personas "no se consideran contribuyentes de este impuesto por dichas enajenaciones". Por tanto la **estación de servicio no causa IEPS ni lo traslada** por la venta de gasolina y diésel; el IEPS lo pagan Pemex u otros fabricantes o importadores y llega a la estación **incluido en el precio**. La iniciativa 2027 lo reconoce en su exposición de motivos (§2.8).

**Acreditamiento (art. 4) [A].** Solo procede el impuesto "trasladado al contribuyente por la adquisición de los bienes a que se refieren los incisos A), D), F), G), I) y J)" y no cabe cuando quien lo pretende "no sea contribuyente del impuesto por la enajenación del bien". Además exige traslado expreso y por separado (fr. III). Pero el **art. 2.º-A** ordena que los contribuyentes trasladen en el precio un monto equivalente "pero en ningún caso lo harán en forma expresa y por separado". **Inferencia (B):** la estación no tiene IEPS acreditable ni a cargo; su IEPS es un costo de adquisición. El art. 28, fr. XV, LISR (no deducibles IVA e IEPS trasladados) no es obstáculo porque el IEPS no se le traslada: se incorpora al precio de la mercancía y se deduce vía costo de lo vendido (art. 25, fr. II LISR; inferencia C).

**IVA y cuotas [A].** Art. 2.º-A: las cuotas "no computarán para el cálculo del impuesto al valor agregado". RMF 5.1.5: los distribuidores y "quienes realicen la venta al público en general" no consideran como valor para el IVA "la cantidad que resulte de aplicar a los litros enajenados las cuotas" correspondientes. La cuota del art. 2.º, fr. I, D, **sí** forma parte de la base de IVA (la regla solo excluye las cuotas del art. 2.º-A; **inferencia B** por el texto de la regla y el art. 12 LIVA).

**Estímulo semanal [A].** Decreto DOF 27-12-2016 modificado por el de 31-12-2025 [6]: art. Primero, estímulo "durante los ejercicios fiscales de 2021, 2022, 2023, 2024, 2025 y 2026" a "los contribuyentes que importen y enajenen" gasolinas y diésel, "consistente en una cantidad equivalente a un porcentaje de las cuotas". El monto lo da a conocer SHCP por acuerdo semanal. **Acuerdo 145/2026 [7], periodo 26-sep al 02-oct-2026:** porcentajes 72.09% (menor a 91), 72.11% (mayor o igual a 91) y 100.00% (diésel); montos $4.8300, $4.0800 y $7.3634 por litro; **cuotas disminuidas** $1.8701, $1.5779 y $0.0000; estímulo complementario al diésel $1.1896 por litro. (Esto es el estado a la fecha de lectura: **cambia cada semana**; nv el de las semanas posteriores.)

**Estímulo a estaciones en la frontera [A].** Art. Segundo del mismo decreto: estímulo a quienes tengan permisos "expedidos por la Comisión Reguladora de Energía o la Comisión Nacional de Energía" para expendio al público en estaciones de la **franja fronteriza de 20 kilómetros** con Estados Unidos, "consistente en una cantidad por litro de gasolina enajenada" por zona geográfica (el decreto de 2016 y el acuerdo por litro **no se leyeron: monto nv**). El del sur (Decreto 28-12-2020) tiene estructura equivalente. Su devolución, RMF 11.7.1: plazo máximo de **trece días hábiles** con e.firma y opinión positiva, para lo generado en 2025 o 2026; exige papel de trabajo por estación, **acuses de los reportes diarios de controles volumétricos** que deben corresponder con la contabilidad, pólizas, escrito de que el suministro fue en tanques de vehículos, estado de cuenta y la disminución del costo de adquisición de las gasolinas por el monto del estímulo. Si hay requerimiento del art. 22 CFF, rige el plazo del CFF.

**LIF 2026, art. 20, apartado A [A].** Los estímulos de diésel son del **consumidor**: (I) actividades empresariales con ingresos menores a 60 millones de pesos, solo en maquinaria excepto vehículos; (IV) transporte público y privado de personas o carga y turístico; el monto acreditable es la cuota del art. 2.º, fr. I, D, numeral 1, subinciso c), "vigente en el momento" de la adquisición por los litros, "con los ajustes que, en su caso, correspondan", y se acredita contra el ISR del ejercicio. **Condición de pago (fr. IV):** el pago a "distribuidores o estaciones de servicio" debe hacerse con monedero autorizado, tarjeta a nombre del contribuyente, cheque nominativo o transferencia desde cuentas a su nombre. Los beneficiarios acumulan el estímulo cuando lo acreditan. Para la estación significa que sus clientes transportistas le exigirán medios de pago rastreables y comprobante con complemento de hidrocarburos (RMF 2.7.1.48).

**Obligaciones LIEPS que no tiene la estación [A].** Art. 5.º (pago mensual el día 17), art. 19 fr. I y II (contabilidad y comprobantes) y art. 21 (declaraciones semestrales de volúmenes los días 20 de septiembre y 20 de marzo) son de los contribuyentes del inciso D). La estación sí queda en el CFF art. 28 y en RMF 2.7.1.48 (CFDI con el "Complemento Concepto para la facturación de Hidrocarburos y Petrolíferos" y claves 15101505, 15101514 y 15101515).

**Anexos 5 y 8 [A].** Se leyeron completos en lo que importa: **no contienen ninguna cuota ni estímulo de combustibles** (0 coincidencias de gasolina, diésel y combustible). El Anexo 8 son tarifas de ISR de personas físicas (art. 96 LISR); el Anexo 5, "Cantidades Actualizadas del Código Fiscal de la Federación" (art. 17-A, sexto párrafo). Los estímulos de combustibles se publican por **acuerdo y decreto**, no por anexo.

### 2.7 El caso: estación de servicio, persona moral, régimen general

**Correcciones al planteamiento [A/B].**
1. Una estación **compra a Pemex o a mayoristas y vende al público**; no "vende a Pemex". Sus ventas son al consumidor y a flotillas.
2. No es contribuyente del IEPS (art. 8, fr. I, c) y **no hay IEPS trasladado ni acreditable** en su declaración; el IEPS está en el precio de compra.
3. Tampoco acredita estímulos del IEPS en su declaración del IEPS: el estímulo del art. Primero es de importadores y enajenantes de primera mano; el art. Segundo solo es suyo si está en la franja de 20 km; los de la LIF 2026 art. 20 son de sus clientes.
4. El control volumétrico es obligación del CFF art. 28 y requisito expreso de la devolución del estímulo fronterizo; **no es requisito expreso de deducibilidad** de la LISR (inferencia C en §2.1).

**Estructura económica por litro (ejercicio 1, SUPUESTO de precios y márgenes).** Con precio de bomba de $24.00 (gasolina menor a 91), la base de IVA es el precio sin IVA menos la cuota del art. 2.º-A. El IVA correcto es **$3.22877**, no los $3.31034 que resultan de dividir entre 1.16 (diferencia de $0.08157 por litro, 0.34% del precio). El IEPS que va dentro del precio es $1.8701 + $0.59139 = $2.46149 por litro (con el estímulo de la semana). Sin estímulo serían $7.29149 por litro. **Estos importes son de la cadena que paga Pemex; la estación solo los ve como parte del costo.**

**Márgenes bajos.** Con los supuestos del §5 la estación gana un margen bruto de 5.92% de sus ingresos y utilidad fiscal de 0.65% (ejercicio 3). Con utilidades así de pequeñas, el coeficiente del año anterior puede quedar por encima del margen real (y generar saldo a favor de ISR anual, como en el ejercicio 3), y la iniciativa 2027 afecta de forma directa a este perfil de empresa (ejercicio 4).

### 2.8 Iniciativa fiscal 2027 (fuente primaria: Gaceta Parlamentaria de la Cámara de Diputados, 8-sep-2026)

**Hechos [A, sobre el texto de la iniciativa; no son ley].**
1. **LISR, Anexo E de la Gaceta 7121 [12]:** se adiciona el **Capítulo X** (arts. 78-A a 78-F) "Del mecanismo de control de las deducciones autorizadas y de las pérdidas fiscales"; aplica a PM residentes con ingresos acumulables "superiores a 50 millones de pesos" que "determinen utilidad fiscal del ejercicio". **Art. 78-B:** si las deducciones autorizadas son menores o iguales a ingresos por **0.9667**, el límite es el total de las deducciones por 0.9900; si son mayores, el límite es ingresos por 0.9667. Lo no disminuido pasa a "los veinte ejercicios siguientes", actualizado. **Art. 78-C:** las pérdidas de ejercicios anteriores solo disminuyen hasta la utilidad fiscal (después del límite de deducciones) por **0.5000**; el excedente de pérdidas se aplica en veinte ejercicios (y las generadas antes de la reforma se aplican en veinte ejercicios, según la exposición de motivos). **Art. 78-D:** el mismo 50% en los PP. **Art. 78-E:** exclusiones (coordinados, agrícolas, maquila, quiebra, otros). Se **deroga** el Capítulo VI del Título II (arts. 59 a 71). El último artículo del proyecto de decreto dice que entra en vigor el 1-ene-2027.
2. **Transitorio Segundo, fr. I, para los PP de 2027:** si las deducciones de la última anual son menores o iguales a ingresos por 0.9667, el coeficiente se multiplica por **1.0658**; si son mayores, por **2.6162**; y la pérdida solo se disminuye hasta 0.5000 de la utilidad del PP.
3. **LIF 2027, Anexo A [11], art. 25, fr. XIX:** las personas diferentes de fabricantes, productores e importadores que enajenen combustibles automotrices y fósiles del tipo gasolinas y diésel "estarán obligadas a aplicar las cuotas" del art. 2.º, fr. I, D y H, y del 2.º-A "sin estímulo, disminución o acreditamiento alguno" a "la diferencia positiva" entre las unidades enajenadas y las adquiridas en el mes. Pago mensual a más tardar el día 17; se calcula "finalizado el mes"; "no trasladarán" el impuesto ni lo incluirán en el precio; la autoridad revisa con controles volumétricos, comprobantes y pedimentos; **entra en vigor el 1-jul-2027**.
4. La exposición de motivos afirma que el IEPS lo paga solo quien fabrica, produce o importa (art. 8, fr. I, c) y que quienes salgan del régimen "resentirán el impuesto en su propio peculio".
5. No se encontró en el Anexo A, D, E ni F de la Gaceta una iniciativa de reforma al CFF ni a la LIVA o LIEPS por separado: el cambio al IEPS va en la LIF 2027 (limitado a esta búsqueda; ver §9).

---

## 3. Fuentes primarias y canónicas

| # | Tema | Fuente | Nivel de acceso | Grado | URL y sha256 (16) |
|---|---|---|---|---|---|
| [1] | LISR vigente (reforma DOF 01-04-2024) | Cámara de Diputados | **Leído** arts. 9, 10, 14, 16, 17, 25, 27, 28, 44 a 46, 57, 75 a 78, 140, 164 (PDF extraído con pdfminer.six; `803c2875c09c751c`) | A | https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf |
| [2] | LIVA vigente (reforma DOF 12-11-2021) | Cámara de Diputados | **Leído** arts. 1, 1-A, 4, 4-A, 5, 5-D, 6, 12, 32 (`f2b5b1770441a6a4`) | A | https://www.diputados.gob.mx/LeyesBiblio/pdf/LIVA.pdf |
| [3] | LIEPS vigente (reforma DOF 07-11-2025) | Cámara de Diputados | **Leído** arts. 2.º (inciso D), 2.º-A, 3.º (definición), 4, 5, 8, 19, 21 (`32639ede8448f91e`) | A | https://www.diputados.gob.mx/LeyesBiblio/pdf/LIEPS.pdf |
| [4] | **Acuerdo 179/2025** (DOF 22-12-2025), cuotas LIEPS 2026 | Cámara de Diputados (copia del DOF) | **Leído completo** (`15f41d5389daf641`) | A | https://www.diputados.gob.mx/LeyesBiblio/ref/lieps/LIEPS_cant14_22dic25.pdf |
| [5] | LIF 2026 (DOF 07-11-2025), art. 20 | Cámara de Diputados | **Leído** art. 19 y art. 20 completo (`a305ca23bba43cdf`) | A | https://www.diputados.gob.mx/LeyesBiblio/pdf/LIF_2026.pdf |
| [6] | **Decreto DOF 31-12-2025** que prorroga estímulos fronterizos y de IEPS a combustibles | SAT, minisitio Estímulos Fiscales Frontera Norte y Sur | **Leído completo** (`b5fa87e8f9ccabd9`) | A | https://www.sat.gob.mx/minisitio/EstimulosFiscalesFronteraNorteSur/documentos/Decreto_modifica_diversos_estimulos_fiscales_region_fronteriza_norte_sur.pdf |
| [7] | **Acuerdo 145/2026**, porcentajes, montos y cuotas disminuidas (26-sep al 02-oct-2026) | SIDOF (Segob) | **Leído completo** (HTML; `9d2991be47abd1c6`) | A | https://sidof.segob.gob.mx/notas/docFuente/5799679 |
| [8] | Acuerdo 144/2026, estímulos sector pesquero y agropecuario, octubre 2026 (todos en 0.00%) | SIDOF | **Leído** (`a9f73c737f19e58b`) | A | https://sidof.segob.gob.mx/notas/docFuente/5799582 |
| [9] | **RMF 2026 compilada** con la Primera Modificación (857 págs.), reglas 2.3.4, 2.7.1.48, 5.1.5, 5.1.6, caps. 11.6 y 11.7 | SAT | **Leído** las reglas citadas (`edd1ae82fe16ba96`, igual que en el cap. 30) | A | https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rmf/compiladas/Compilado_Primera_Modificacion_a_la-Resolucion_Miscelanea_Fiscal_para_2026.pdf |
| [10] | **Anexos 5 y 8** (DOF 28-12-2025) y Anexo 1 | SAT | Anexos 5 y 8 **leídos** (sin combustibles; `ed96a19389de60bb`, `69ebaf8a78a3bde5`); Anexo 1 solo la lista de formas (`acbfb10b4f4dca44`) | A / B | …/documentos2026/rmf/anexos/Anexo-5-RMF-2026_DOF-28122025.pdf, Anexo-8-…, Anexo-1-… |
| [11] | **Iniciativa del Ejecutivo: LIF 2027** (Gaceta 7121-A, 08-09-2026) | Gaceta Parlamentaria, Cámara de Diputados | **Leído**: exposición sobre LIEPS, art. 25 fr. XIX, transitorio primero, art. 20 (`55d8436ec681a681`) | A (es iniciativa) | https://gaceta.diputados.gob.mx/PDF/66/2026/sep/20260908-A.pdf |
| [12] | **Iniciativa del Ejecutivo: reforma a la LISR** (Gaceta 7121-E, 08-09-2026) | Gaceta Parlamentaria | **Leído**: motivos de arts. 78-A a 78-F, texto de 78-A a 78-E, transitorio segundo (`5e8afc6ced347842`) | A (es iniciativa) | https://gaceta.diputados.gob.mx/PDF/66/2026/sep/20260908-E.pdf |
| [13] | Índice de leyes federales vigentes (fechas de última reforma) y páginas de la LIEPS | Cámara de Diputados | **Leído** (HTML) | A | https://www.diputados.gob.mx/LeyesBiblio/index.htm y …/ref/lieps.htm |
| [14] | CFF (reforma DOF 09-04-2026), arts. 17-A, 22, 28, 56 y 81 | Cámara de Diputados | **Leído** en lo citado (`be7427b20d355277`) | A | https://www.diputados.gob.mx/LeyesBiblio/pdf/CFF.pdf |
| [15] | LFT (reforma DOF 14-05-2026), arts. 117 a 127 | Cámara de Diputados | **Leído** arts. 117, 118, 120 a 123, 126, 127 (`12f09393a1951a91`) | A | https://www.diputados.gob.mx/LeyesBiblio/pdf/LFT.pdf |
| [16] | Gaceta 7121-D (LFD), 7121-F (Aduanera), otros anexos del paquete | Gaceta Parlamentaria | **Leído solo encabezados** | D | https://gaceta.diputados.gob.mx/Gaceta/66/2026/sep/pef2027.html |
| [17] | Notas de prensa y despachos sobre el Paquete 2027 (idconline, EY, México Cómo Vamos) | Terceros | **No usadas como fuente de ningún hecho**; una nota (idconline) se leyó solo para orientar la búsqueda y coincide con [12] | C | — |
| [18] | Decreto DOF 27-12-2016 (texto original), acuerdo semanal del estímulo fronterizo por litro, Decreto 28-12-2020, Reglamentos de LISR y LIVA, resolución de la Comisión Nacional de PTU | DOF / SHCP / STPS | **No leídos** | D | `www.dof.gob.mx` y `hacienda.gob.mx` fallan por certificado (curl 60); no se debilitó la verificación TLS |
| [19] | Capítulos 29, 30 y 27 de este repo | Repo | Referencia interna (A en su registro) | A | `conocimiento/` |

---

## 4. Lo más reciente (estado al 7-oct-2026)

1. **Iniciativa 2027 (8-sep-2026):** LISR con límite a deducciones (0.9667 y 0.9900), límite del 50% a la pérdida fiscal, 20 años de arrastre y modificación del coeficiente de los PP de 2027; LIF 2027 con régimen del IEPS para quienes no son fabricantes, productores ni importadores de combustibles, desde el **1-jul-2027**. Ambos son proyectos: **pueden cambiar** en la discusión del Congreso. Fecha de aprobación y contenido final: nv.
2. **Estímulos 2026 a combustibles:** vigentes hasta el 31-dic-2026 (Decreto DOF 31-12-2025). En la semana del 26-sep al 2-oct-2026 el diésel tiene 100% de estímulo (cuota disminuida $0.0000) y las gasolinas más de 72%.
3. **RMF:** la Primera Modificación (DOF 09-07-2026) reformó la regla 11.7.1 (devolución del estímulo fronterizo) y agregó la regla 11.7.3 (precio base del diésel, con reducciones de $0.28 a $1.04 por litro entre el 1-abr y el 2-jul-2026).
4. **Sin cambios en 2026:** LISR (DOF 01-04-2024) y LIVA (DOF 12-11-2021).

---

## 5. Evidencia: ejercicios con cifras

Todas las cifras de este capítulo se obtuvieron con un script (apéndice al final, §10) y se leyeron de su salida. **SUPUESTO** marca los datos inventados: litros, precios de bomba, márgenes, gastos operativos, saldos, el 10% de PTU y los INPC ilustrativos.

**Ejercicio 1: las cuotas 2026 reproducen el Acuerdo 179/2025 (art. 17-A CFF).**
- Factor exacto = 142.645 / 137.424 = **1.037992**. El Acuerdo publica **1.0379**: **truncó a cuatro decimales** (redondeado habría sido 1.0380). Hallazgo: la cuota 2026 sale de multiplicar la de 2025 por 1.0379 y truncar: gasolina menor a 91: 6.4555 × 1.0379 = 6.700163, publicada **6.7001**; diésel: 7.0946 × 1.0379 = 7.363485, publicada **7.3634** (redondear daría 7.3635); art. 2.º-A, magna: 56.9795 × 1.0379 = 59.1390.
- Acuerdo 145/2026: monto = cuota × porcentaje: 6.7001 × 0.7209 = 4.8301 (publicado **4.8300**); 5.6579 × 0.7211 = 4.0799 (publicado **4.0800**); diésel 7.3634 × 1.00 = 7.3634. Cuota disminuida = cuota − monto publicado: 1.8701, 1.5779 y 0.0000 (coincide con lo publicado). **Lección:** los porcentajes están redondeados a dos decimales y el SHCP publica el monto ya redondeado; hay que usar el monto publicado, no recalcularlo.

**Ejercicio 2: estructura de un litro y IVA correcto (SUPUESTO de precios y márgenes).** Precio de bomba P (con IVA); IVA = 0.16 × (S − c2A) y S = (P + 0.16 × c2A) / 1.16, con c2A la cuota del art. 2.º-A en pesos.

| Producto | P | S (precio sin IVA) | IVA correcto | IVA "ingenuo" (P/1.16 × 0.16) | Diferencia | IEPS en el precio con estímulo de la semana | IEPS sin estímulo |
|---|---:|---:|---:|---:|---:|---:|---:|
| Gasolina < 91 | 24.00 | 20.77123 | 3.22877 | 3.31034 | 0.08157 | 2.46149 | 7.29149 |
| Gasolina ≥ 91 | 26.50 | 22.94436 | 3.55564 | 3.65517 | 0.09953 | 2.29950 | 6.37950 |
| Diésel | 26.80 | 23.17115 | 3.62885 | 3.69655 | 0.06770 | 0.49082 | 7.85422 |

Con litros mensuales SUPUESTO de 300,000 (< 91), 80,000 (≥ 91) y 120,000 (diésel), márgenes brutos SUPUESTO sin IVA de $1.30, $1.50 y $1.10 por litro y los precios de la tabla: ingresos del mes **$10,847,454.27**, costo **$10,205,454.27**, margen **$642,000.00** (5.92% de los ingresos). IVA trasladado **$1,688,545.73**; IVA acreditable (el que le trasladó el proveedor sobre la misma mecánica) **$1,585,825.73**; **IVA a cargo $102,720.00** = 0.16 × margen. No hay IEPS en la declaración de la estación.

**Ejercicio 3: PP con coeficiente, PTU y saldo a favor (art. 14).** SUPUESTO: ejercicio 2025 con ingresos $126,000,000, deducciones autorizadas $124,590,000 y PTU pagada en 2025 de $130,000; utilidad fiscal 2025 = 126,000,000 − 124,590,000 − 130,000 = **$1,280,000**; coeficiente = 1,280,000 / 126,000,000 = **0.0101587** (se usa sin redondear; el redondeo reglamentario es nv). PTU de 2025 (renta gravable $1,410,000; porcentaje 10% SUPUESTO) = **$141,000**, pagadera a más tardar el **30-may-2026** (31-mar + 60 días, art. 122 LFT). En 2026, con los ingresos del ejercicio 2 constantes, los PP son: enero a abril **$33,058.91** cada mes (utilidad PP 110,196.36 × 30%), y de mayo a diciembre **$27,771.41** cada mes al restar la PTU en ocho partes iguales de $17,625.00. Acumulado a septiembre: utilidad del PP $903,642.25 e ISR acumulado $271,092.67. Al cierre: ingresos del ejercicio $130,169,451.21, utilidad fiscal real **$843,000** (después de PTU pagada de $141,000), ISR anual **$252,900**, PP acumulados **$354,406.90**: **saldo a favor $101,506.90**. El coeficiente real fue 0.006476 contra 0.0101587 aplicado. **Lección:** con márgenes que caen, el art. 14 (inciso b del último párrafo) permite pedir un coeficiente menor desde el segundo semestre; si no se hace, se adelanta caja al fisco.

**Ejercicio 4: efecto de la iniciativa 2027 sobre el mismo perfil (SUPUESTO: igual al de 2025 con PTU de 2027 de $141,000).** Deducciones / ingresos = 124,590,000 / 126,000,000 = **0.98881 > 0.9667**.
- Ley actual: utilidad fiscal = 126,000,000 − 124,590,000 − 141,000 = **$1,269,000**; ISR **$380,700**.
- Art. 78-B (límite = 0.9667 × 126,000,000 = **$121,804,200**): deducciones no disminuibles del año **$2,785,800** (arrastre de 20 años); utilidad fiscal = 126,000,000 − 121,804,200 − 141,000 = **$4,054,800**; ISR **$1,216,440**; aumento **$835,740** (3.2 veces) con la misma operación económica. (**Inferencia C:** se supone que la PTU pagada se sigue deduciendo por el art. 9, fr. I, que la iniciativa no altera según lo leído.)
- Art. 78-C con pérdida pendiente de $3,000,000: límite = 0.5000 × 4,054,800 = **$2,027,400**; utilidad tras pérdida $2,027,400; ISR **$608,220** (hoy, art. 57: la pérdida absorbería toda la utilidad y el ISR sería **$0**).
- PP 2027 (transitorio Segundo): coeficiente 0.0101587 × 2.6162 = **0.026577**, 2.6 veces más caja en los PP.
- **Lectura:** el umbral de 0.9667 equivale a un margen de utilidad antes de PTU de **3.33%** de los ingresos acumulables; una estación con margen menor tributa como si lo tuviera, siempre que **determine utilidad fiscal** (si el ejercicio da pérdida, el mecanismo no aplica según el art. 78-A).

**Ejercicio 5: CUFIN y dividendos (art. 77, 10 y 140).** SUPUESTO: resultado fiscal $1,000,000, ISR pagado $300,000, partidas no deducibles (sin las excepciones de las frs. VIII y IX) $50,000. **UFN = 1,000,000 − 300,000 − 50,000 = $650,000.**
- Dividendo de $500,000 (de CUFIN): no hay ISR a nivel sociedad. Si el accionista es persona física, **retención 10% = $50,000**, definitiva.
- Dividendo de $800,000: exceso sobre la CUFIN $150,000; 150,000 × 1.4286 × 30% = **$64,287.00** (1/0.7 = 1.428571; la ley usa 1.4286). Retención de 10% a la persona física sobre todo el dividendo: **$80,000**. Cuando se acredite el impuesto de $64,287.00 contra el ISR del ejercicio, la UFN se reduce en 64,287 / 0.4286 = **$149,993.00** (frente a $150,000 por redondeo del factor).

**Ejercicio 6: AAI (art. 44), factor ilustrativo.** El factor legal usa diciembre contra diciembre; **no se tienen aquí esos índices**; se usó el cociente de noviembre de 2025 (142.645) entre noviembre de 2024 (137.424) menos uno = **0.037992** solo como ilustración. SUPUESTO: deudas promedio $2,700,000 (proveedores $2,400,000 y contribuciones por pagar $300,000), créditos promedio $1,800,000 (cuentas por cobrar de tarjetas; la caja **no** cuenta, art. 45, fr. VII). Diferencia $900,000 × 0.037992 = **AAI acumulable $34,192.72**. Si fuera al revés (créditos mayores en $700,000): AAI **deducible $26,594.34**. El AAI acumulable no entra a los ingresos nominales del PP (art. 14).

**Ejercicio 7: IVA con inversión y devolución.** SUPUESTO: se compran tanques y dispensarios por $3,000,000 más IVA de **$480,000** en el mes 1. IVA a cargo del mes (ejercicio 2) $102,720.00; saldo a favor **$377,280.00** (art. 6 LIVA). Si se acredita contra los meses siguientes, el saldo baja a $274,560.00, $171,840.00 y $69,120.00 (meses 2 a 4) y se agota en el mes 5, en el que la estación paga $33,600.00 (102,720.00 − 69,120.00). Si se solicita devolución, lo solicitado ya no se acredita; el plazo del art. 22 CFF es de cuarenta días (sin contar requerimientos) y la RMF 2.3.4 exige tener presentada la DIOT del periodo.

**Ejercicio 8: acreditamiento del cliente transportista (LIF 2026, art. 20, A, IV).** Si un autotransportista compra **10,000 litros de diésel**, el monto acreditable que dice la ley es 10,000 × 7.3634 = **$73,634.00**, contra su ISR, **siempre que pague con tarjeta, monedero, cheque o transferencia**. Pero en la semana del Acuerdo 145/2026 la cuota disminuida del diésel es $0.0000; la LIF dice "con los ajustes que, en su caso, correspondan" y **no se leyó la regla que explique esos ajustes** (nv): no se debe prometer el monto completo a un cliente sin leerla.

**Ejercicio 9: lo que haría la fr. XIX del art. 25 de la LIF 2027 (iniciativa).** Con las cuotas **2026 sin estímulo** de gasolina menor a 91 (6.7001 + 0.591390 = **$7.29149** por litro; las de 2027 no existen aún). (a) Un mes con compras de 500,000 litros y ventas de 503,000: 3,000 × 7.29149 = **$21,874.47** (la tolerancia del 0.5% de CFF art. 56 serían 2,500 litros, pero la fracción XIX no trae tolerancia). (b) **Efecto de calendario:** mes 1 compra 520,000 y vende 500,000 (pago **$0**); mes 2 compra 480,000 y vende 500,000: diferencia positiva de 20,000 litros y pago de **$145,829.80**, aunque en los dos meses juntos compró 1,000,000 y vendió 1,000,000. **Inferencia (B):** el texto compara compras y ventas "en el mes" sin arrastre de inventario; la exposición de motivos dice que no pretende gravar "diferencias legítimas" derivadas de inventarios, pero el artículo no lo dice. No se puede trasladar al cliente ni incluir en el precio.

**Ejercicio 10: estímulo agropecuario de la LIF (A, II, 2).** Quien se dedica exclusivamente a actividades agropecuarias o silvícolas acredita el factor **0.355** sobre el precio con IVA consignado en el comprobante de compra en estaciones; para $100,000 con IVA, $35,500.00 (sin el IEPS del art. 2.º-A, que no se considera dentro del precio señalado).

---

## 6. Traducción operable

### 6.1 Principio rector

Una estación de servicio es un **revendedor con margen de 1 a 6%**: el impuesto que más le cuesta es el ISR sobre una utilidad pequeña, y el que más le puede doler en 2027 es el que se define sobre **litros** y no sobre utilidad. El control de existencias y los controles volumétricos son, a la vez, su defensa y su base de pago.

### 6.2 Reglas (propuestas; no modifican nada del repo)

1. **R1.** No registrar IEPS por separado en la contabilidad de la estación (no es contribuyente por el art. 8, fr. I, c); registrar el costo del combustible completo como costo de lo vendido y conservar facturas con complemento de hidrocarburos.
2. **R2.** Calcular el IVA de venta con la fórmula del ejercicio 2 (restar la cuota del art. 2.º-A) y no dividiendo entre 1.16; validar contra el CFDI de Pemex del proveedor.
3. **R3.** Cada mes de julio, comparar coeficiente aplicado contra margen real y evaluar pedir coeficiente menor (art. 14, inciso b).
4. **R4.** Antes del 1-nov-2026, simular el ISR 2027 con el art. 78-B y el 78-C si los ingresos pasan de 50 millones, con los datos del cierre de septiembre.
5. **R5.** Antes del 1-jul-2027 (si se aprueba), llevar un tablero mensual de litros comprados y vendidos por producto y un manejo de inventario que evite el efecto de calendario del ejercicio 9 (compras hacia el principio del mes, no al final).
6. **R6.** No ofrecer a un cliente transportista un monto de acreditamiento sin haber leído los ajustes del art. 20, A, IV de la LIF y las reglas del SAT.
7. **R7.** Pedir a los clientes empresariales pago rastreable y confirmar que su comprobante lleve el permiso vigente del proveedor (art. 27, fr. III, 2.º párrafo).
8. **R8.** Guardar para cada distribución de dividendos: saldo de CUFIN actualizado, constancia de retención (art. 76, fr. XI) y el entero del 10% con el PP del periodo.

### 6.3 *Checklist* mensual (día 17)

PP de ISR (art. 14) · IVA (art. 5-D) y DIOT (art. 32, fr. VIII) · retenciones de IVA por autotransporte (art. 1-A, II, c) · retención del 10% de dividendos pagados (art. 140) · reporte volumétrico (cap. 30; mes del segundo posterior, primeros tres días naturales) · conciliar litros comprados contra recibidos y vendidos.

---

## 7. Trampas y contraejemplo

1. **Creer que la estación traslada y acredita IEPS.** Art. 8, fr. I, c): no es contribuyente por esa enajenación; art. 2.º-A: el traslado "en ningún caso" es expreso y por separado.
2. **Dividir el precio de bomba entre 1.16.** Ignora la exclusión de la cuota del art. 2.º-A (RMF 5.1.5); da un IVA mayor en $0.07 a $0.10 por litro.
3. **Creer que "estímulo" del IEPS lo recibe la estación.** Es de importadores y enajenantes de primera mano; solo el art. Segundo del decreto es para estaciones en la franja de 20 km; los de la LIF son del consumidor.
4. **Tomar los porcentajes del Acuerdo para recalcular el monto.** Hay redondeos ($4.8301 contra $4.8300): usar el monto publicado.
5. **Dar por vigente el estímulo semanal de hoy.** Cambia cada semana y el decreto termina el 31-dic-2026.
6. **Creer que la falta de controles volumétricos "no deduce" por ley.** No hay causal expresa; el riesgo es la presunción del art. 56 CFF y el art. 27, fr. IV.
7. **Confundir PTU con dividendo.** El art. 10 excluye la PTU de los dividendos; y la PTU pagada se resta en el art. 9 pero la renta gravable de PTU no resta pérdidas.
8. **Olvidar que los créditos del AAI no incluyen la caja ni los PP.**
9. **Dar por ley la iniciativa 2027.** Es un proyecto; hasta que no se publique en el DOF no hay que cambiar nada, solo planear.
10. **Contraejemplo (margen de 3% que desaparece en 2027).** Una estación con ingresos de $126,000,000, margen de utilidad de 1.0% y pérdidas acumuladas de $3,000,000 hoy paga **$0** de ISR (las pérdidas absorben la utilidad). Con la iniciativa paga **$608,220** (ejercicio 4) y arrastra $2,785,800 de deducciones que no podrá usar en el año: "no tener utilidad" ya no es "no pagar". Y si además se aprueba el art. 25, fr. XIX de la LIF 2027, un mes de ventas por encima de compras genera un pago por litro **que no puede trasladar** (ejercicio 9).

---

## 8. Examen (siete preguntas)

1. **Una estación vende 300,000 litros de gasolina menor a 91 a $24.00 el litro con IVA. ¿Cuánto IVA traslada por litro y por qué no es $3.31034?**
   $3.22877. El IVA se calcula sobre el precio sin IVA menos la cuota del art. 2.º-A (59.1390 centavos); LIEPS 2.º-A, 5.º párrafo, y RMF 5.1.5. Si se divide entre 1.16 se obtiene $3.31034, diferencia de $0.08157 por litro; en 300,000 litros, $24,471 al mes que se trasladarían de más (inferencia aritmética del §5).

2. **¿Puede la estación acreditar IEPS? ¿Y trasladarlo?**
   No. Art. 8, fr. I, c): "no se consideran contribuyentes" por la enajenación; art. 4: no procede el acreditamiento cuando quien lo pretende "no sea contribuyente del impuesto por la enajenación del bien"; art. 2.º-A: el monto se traslada en el precio, nunca "expresa y por separado". El IEPS es costo del combustible.

3. **Calcule el pago provisional de mayo con coeficiente 0.0101587 (1,280,000 / 126,000,000), ingresos acumulados de $54,237,271.34 y PTU de $141,000. ¿En cuántas partes se resta la PTU?**
   Se resta en 8 partes iguales ($17,625) en mayo a diciembre; en mayo se resta una parte. Utilidad del PP = 54,237,271.34 × 0.0101587 − 17,625 = 533,356.80; ISR acumulado a 30% = $160,007.04; PP del mes = 160,007.04 − 132,235.63 (PP de enero a abril) = **$27,771.41**. Art. 14, fr. II, a).

4. **Un ejercicio da pérdida fiscal de $2,000,000 y la estación pagó PTU de $100,000. ¿De cuánto es la pérdida fiscal y en cuántos ejercicios se amortiza hoy y con la iniciativa 2027?**
   $2,100,000: el art. 57 la incrementa con la PTU pagada. Hoy se amortiza en los diez ejercicios siguientes (actualizada). La iniciativa propone veinte y límite del 50% de la utilidad fiscal para quien tenga ingresos mayores a 50 millones y determine utilidad (art. 78-C). El punto del 50% se calcula después del límite a deducciones (art. 78-B).

5. **La sociedad tiene UFN de $650,000 y reparte $800,000 a una persona física. ¿Qué impuestos hay y a cargo de quién?**
   La sociedad paga art. 10 sobre el exceso de $150,000: 150,000 × 1.4286 × 30% = $64,287 (definitivo; se acredita en el ISR del ejercicio y dos más). Además retiene 10% de $800,000 = $80,000 (art. 140, definitivo, se entera con el PP). La persona física acumula el dividendo y puede acreditar el ISR pagado por la sociedad solo si acumula también ese impuesto y tiene la constancia (art. 140, 1.er párrafo); el 10% es adicional (2.º párrafo).

6. **Una estación tiene saldo a favor de IVA de $377,280 por inversión. ¿Puede acreditarlo y pedir devolución del mismo monto? ¿Cuánto tarda?**
   No ambas: lo solicitado en devolución no puede acreditarse (art. 6 LIVA). Debe pedir devolución del total del saldo. El CFF art. 22 da cuarenta días desde que la solicitud esté completa; la autoridad puede pedir datos en veinte días y esos requerimientos suspenden el plazo. RMF 2.3.4: DIOT del periodo presentada. La regla de trece días hábiles (RMF 11.7.1) es del estímulo fronterizo, no del IVA.

7. **Con la iniciativa 2027, una estación con ingresos de $126,000,000 y deducciones de $124,590,000 se pregunta cuánto cambia su ISR y por qué el cálculo no depende de su "utilidad".**
   De $380,700 a $1,216,440 (más $835,740) porque el límite del art. 78-B es 0.9667 de los ingresos cuando las deducciones lo superan (ratio 0.98881); queda utilidad mínima de 3.33% antes de PTU, y el excedente de deducciones ($2,785,800) se difiere veinte años. Hay que añadir que si hay pérdidas anteriores, solo reducen 50% de la utilidad así determinada. Aplica solo con ingresos mayores a 50 millones y utilidad fiscal en el ejercicio (art. 78-A), y es **iniciativa**.

---

## 9. Preguntas abiertas

1. **Tasa de retención de IVA por autotransporte** (art. 1-A, II, c): está en el Reglamento de la LIVA, no leído (nv).
2. **Montos por litro del estímulo fronterizo del art. Segundo** y zonas geográficas: texto del decreto de 2016 y acuerdos no leídos (nv).
3. **Ajustes del art. 20, A, IV de la LIF** al acreditamiento de diésel cuando hay cuota disminuida: regla no leída (nv).
4. **Aprobación definitiva** de la iniciativa 2027 y sus cambios en Cámaras; hay que revisar la Gaceta y el DOF (nv).
5. **Si el decreto de vigencia 31-12-2025 se prorroga para 2027** (nv; ninguna fuente).
6. **Porcentaje de PTU** fijado por la Comisión Nacional: resolución no leída (nv); el 10% es supuesto.
7. **Coeficiente de utilidad: redondeo** (reglamento): no leído (nv).
8. **Si la iniciativa de LIF 2027 se aplicaría con las cuotas actualizadas 2027** y cómo se calcula con estímulos de sectores: no leído más allá de la fr. XIX.
9. **Régimen de PM para cooperativas, coordinados y otros**: fuera del alcance.
10. **Jurisprudencia** de la SCJN sobre art. 27, fr. III (pago de combustible) y sobre estricta indispensabilidad: no consultada (nv).
11. **Iniciativas de LIVA y CFF** para 2027: no hay en los anexos de la Gaceta leídos; podría haber en otros paquetes (nv).
12. **Efecto en ISR de los estímulos fronterizos** (disminución del costo de adquisición, RMF 11.7.1) para una estación en la franja: se leyó la regla, no el decreto original.

---

## 10. Registro de verificación (7-oct-2026)

- **Descargas.** Con `curl` y el proxy del entorno: `diputados.gob.mx` (LISR, LIVA, LIEPS, LIF 2026, CFF, LFT, Acuerdo 179/2025, índice de leyes), `sat.gob.mx` (RMF compilada, Anexos 1, 5 y 8, Decreto 31-12-2025), `sidof.segob.gob.mx` (acuerdos 144 y 145/2026) y `gaceta.diputados.gob.mx` (Anexos A, D, E, F y otros de la Gaceta 7121). Extracción con `pdf2txt.py` (pdfminer.six). Los hashes (16 caracteres) están en el §3. `www.dof.gob.mx` y `hacienda.gob.mx` fallan por certificado y no se debilitó la verificación TLS. El hash del CFF coincide con el del cap. 30; el hash de la RMF compilada coincide con el del cap. 30.
- **Verificación de cifras en Python** (script completo al final de este capítulo): factor 1.0379 (truncado, no redondeado), cuotas 2026 a partir de 2025, montos del Acuerdo 145/2026, IVA con exclusión del art. 2.º-A, PP mensuales, PTU y su plazo (31-mar + 60 días = 30-may-2026), límite 78-B y 78-C, CUFIN y dividendos, AAI, saldo a favor de IVA, fr. XIX del art. 25 de la LIF 2027. Resumen del cálculo central:
  - `S = (P + 0.16·c2A)/1.16` y `IVA = 0.16·(S − c2A)`; para P = 24.00 y c2A = 0.591390: S = 20.77123 e IVA = 3.22877; P = S + IVA = 24.00000.
  - `uf25 = 126,000,000 − 124,590,000 − 130,000 = 1,280,000`; `coef = 1,280,000 / 126,000,000 = 0.0101587`.
  - `limite78B = 0.9667 × 126,000,000 = 121,804,200`; `UF = 126,000,000 − 121,804,200 − 141,000 = 4,054,800`.
  - `dividendo: 150,000 × 1.4286 × 0.30 = 64,287`.
- **Verificación mecánica de frases.** Se extrajeron las cadenas entrecomilladas de 20 o más caracteres del capítulo y se buscaron, con espacios normalizados, en los textos extraídos de los documentos del §3. Resultado: 87 cadenas; las que no aparecen literalmente son artefactos del emparejamiento de comillas (texto entre dos citas), la frase del encargo "IEPS trasladado y acreditable" y ninguna cita de ley sin coincidencia tras corregir una (art. 12 LIVA, que se había abreviado con puntos suspensivos).
- **Hallazgos de cuidado.** (1) El encargo suponía "ventas a Pemex" y "IEPS trasladado y acreditable" en la estación: ninguna de las dos premisas es cierta en derecho (art. 8, fr. I, c, LIEPS). (2) El encargo suponía el control volumétrico como requisito de deducibilidad de la LISR: no existe esa causal expresa (0 menciones en LISR, LIVA, LIEPS y LIF). (3) Los Anexos 5 y 8 no traen nada de combustibles. (4) Los estímulos semanales se publican por acuerdo de SHCP, no por anexo. (5) El factor del Acuerdo 179/2025 está truncado, no redondeado. (6) La LISR y la LIVA de Diputados no van atrasadas: el índice de leyes muestra las mismas fechas. (7) La iniciativa 2027 sí tiene fuente primaria en la Gaceta; dos medios secundarios (idconline, EY) solo sirvieron de guía.
- **Seguridad.** No se pidió ni se usó ninguna credencial, e.firma o contraseña.

### No verificado (lista)

1. Texto del Decreto DOF 27-12-2016 (zonas, montos, requisitos) y acuerdos semanales del estímulo fronterizo por litro.
2. Reglamentos de la LISR y de la LIVA (redondeo del coeficiente, tasa de retención de IVA por autotransporte, AAI en detalle).
3. Resolución de la Comisión Nacional de PTU (porcentaje); jurisprudencia de PTU.
4. Regla del SAT sobre los "ajustes" del acreditamiento de diésel (LIF art. 20, A, IV).
5. Layout de la DIOT (Anexo 1) y fichas de devolución de IVA (Anexo 2) más allá de la regla 2.3.4.
6. Aprobación, cambios y publicación en el DOF de la iniciativa 2027; cuotas y estímulos 2027; prórroga de los decretos.
7. Arts. 59 a 71 de la LISR (régimen derogado en la iniciativa) y arts. 78-F de la iniciativa; resto del articulado de la iniciativa de LISR (arts. 22, 25, 27, 77, 78, 113-E, 206 y 209).
8. Efecto de la fr. XIX del art. 25 de la LIF 2027 sobre las cuotas de 2027 y sobre el CFF.
9. Aplicación a una estación concreta: zona fronteriza o no, ingresos reales, partes relacionadas, permisos de la CNE.
10. Jurisprudencia y criterios no vinculativos del SAT (Anexo 7).
11. Las mediciones de la Primera Modificación de la RMF posteriores a 09-07-2026 y la Segunda (01-10-2026) en lo que toca IEPS.
12. Dictámenes de laboratorio y reglas 2.6.1.x de controles volumétricos (en el cap. 30).

### Apéndice: script de verificación (Python 3, sin dependencias)

```python
# Verificacion numerica del cap. 32 (todas las cifras de entrada salen de fuentes leidas o estan marcadas SUPUESTO)
from decimal import Decimal as D, ROUND_HALF_UP, ROUND_DOWN
def r2(x): return float(D(str(x)).quantize(D('0.01'),rounding=ROUND_HALF_UP))
print("== E1 cuotas 2026 (Acuerdo 179/2025)")
f=142.645/137.424; print("factor exacto",f,"truncado 4:",int(f*1e4)/1e4,"redondeado 4:",round(f,4))
old={"magna_2ID":6.4555,"prem_2ID":5.4513,"dsl_2ID":7.0946,"magna_2A":0.569795,"prem_2A":0.695255,"dsl_2A":0.472895}
new={"magna_2ID":6.7001,"prem_2ID":5.6579,"dsl_2ID":7.3634,"magna_2A":0.591390,"prem_2A":0.721605,"dsl_2A":0.490817}
for k in old:
    p=old[k]*1.0379; print(k,old[k],"x1.0379 =",round(p,6),"publicada",new[k], "trunc4",int(p*1e4)/1e4, "round4",round(p,4))
print("== E1b Acuerdo 145/2026 (26-sep a 2-oct-2026)")
cuota={"magna":6.7001,"prem":5.6579,"dsl":7.3634}
pct={"magna":.7209,"prem":.7211,"dsl":1.0}
mon={"magna":4.8300,"prem":4.0800,"dsl":7.3634}
cd={"magna":1.8701,"prem":1.5779,"dsl":0.0}
for k in cuota:
    m=cuota[k]*pct[k]; print(k,"cuota*pct=",round(m,4),"monto publicado",mon[k],"cuota-monto=",round(cuota[k]-mon[k],4),"cuota disminuida publicada",cd[k])
print("== E2 estructura de precio por litro (precios de bomba SUPUESTO)")
c2A={"magna":.591390,"prem":.721605,"dsl":.490817}
P={"magna":24.00,"prem":26.50,"dsl":26.80}
marg={"magna":1.30,"prem":1.50,"dsl":1.10}   # SUPUESTO margen bruto sin IVA por litro
L={"magna":300000,"prem":80000,"dsl":120000}  # SUPUESTO litros/mes
S={};IVA={};Sc={};IVAc={}
for k in P:
    S[k]=(P[k]+0.16*c2A[k])/1.16
    IVA[k]=0.16*(S[k]-c2A[k])
    Sc[k]=S[k]-marg[k]; IVAc[k]=0.16*(Sc[k]-c2A[k])
    naive=P[k]/1.16*0.16
    ieps=cd[k]+c2A[k]
    print(k,"P",P[k],"S",round(S[k],5),"IVA",round(IVA[k],5),"check P",round(S[k]+IVA[k],5),"IVA ingenuo",round(naive,5),"dif",round(naive-IVA[k],5),"IEPS en precio (cuota disminuida+2A)",round(ieps,5),"IEPS bruto sin estimulo",round(cuota[k]+c2A[k],5))
ing=sum(S[k]*L[k] for k in L); cost=sum(Sc[k]*L[k] for k in L)
ivat=sum(IVA[k]*L[k] for k in L); ivac=sum(IVAc[k]*L[k] for k in L)
gm=sum(marg[k]*L[k] for k in L)
print("ingresos mes",r2(ing),"costo",r2(cost),"margen",r2(gm),"margen/ing",gm/ing)
print("IVA trasladado",r2(ivat),"IVA acreditable",r2(ivac),"IVA a cargo",r2(ivat-ivac),"=0.16*margen",r2(0.16*gm))
opex=560000 # SUPUESTO
print("opex",opex,"utilidad antes de PTU mes",r2(gm-opex),"ratio deducciones/ingresos",(cost+opex)/ing)
print("== E3 pagos provisionales 2026 (art. 14 LISR)")
ing25=126_000_000; ded25=124_590_000; ptu_paid25=130_000
uf25=ing25-ded25-ptu_paid25; coef=uf25/ing25
print("utilidad fiscal 2025",uf25,"coef",coef)
renta_ptu25=ing25-ded25; ptu25=0.10*renta_ptu25
print("renta gravable PTU 2025",renta_ptu25,"PTU 10% (supuesto de tasa)",ptu25)
import datetime
print("fecha limite declaracion anual 31-mar-2026 +60 dias:",datetime.date(2026,3,31)+datetime.timedelta(days=60))
ing_m=ing/1  # mensual
prev=0;ptu_month=ptu25/8
for m in range(1,10):
    acum=ing_m*m
    ptu_acum= ptu_month*max(0,m-4)   # mayo=5 -> 1 parte
    base=acum*coef-ptu_acum
    pp=base*0.30-prev
    print(m,"ing acum",r2(acum),"util PP",r2(base),"ISR acum",r2(base*.3),"PP del mes",r2(pp))
    prev+=pp
print("== E4 2027 inic.: limite deducciones 78-B y perdidas 78-C")
ing27=126_000_000; ded27=124_590_000; ptu27=141_000; pf=3_000_000
print("ratio",ded27/ing27,">0.9667?",ded27/ing27>0.9667)
uf_act=ing27-ded27-ptu27; isr_act=0.30*uf_act
lim=0.9667*ing27; nodeduc=ded27-lim
uf_prop=ing27-lim-ptu27; isr_prop=0.30*uf_prop
print("limite",lim,"no deducible del ejercicio",nodeduc,"UF actual",uf_act,"ISR actual",isr_act,"UF propuesta",uf_prop,"ISR propuesto",isr_prop,"diferencia",isr_prop-isr_act)
lim78c=0.5*uf_prop; aplic=min(pf,lim78c)
print("perdida pendiente",pf,"limite 78-C",lim78c,"aplicada",aplic,"UF tras perdida",uf_prop-aplic,"ISR",0.30*(uf_prop-aplic),"vs actual art.57 (aplica toda)",0.30*max(0,uf_act-pf))
print("coef 2027 PP: 0.010159 x 2.6162 =",coef*2.6162,"x1.0658",coef*1.0658)
ded25_ratio=ded25/ing25; print("ratio 2025",ded25_ratio)
print("== E5 dividendos y CUFIN")
rf=1_000_000; isr=300_000; nd=50_000
ufn=rf-isr-nd; print("UFN",ufn)
for div in (500_000,800_000):
    exc=max(0,div-ufn); imp=exc*1.4286*0.30
    print("dividendo",div,"exceso sobre CUFIN",exc,"ISR art.10",r2(imp),"retencion 10% PF",0.10*div,"1.4286 chk",1/0.7)
print("UFN a disminuir por acreditamiento art 10 f.II: impuesto/0.4286 =",r2(imp/0.4286))
print("== E6 ajuste anual por inflacion (art. 44) factor ilustrativo Nov/Nov")
fa=142.645/137.424-1; print("factor ilus",fa)
deu=2_400_000+300_000; cre=1_800_000+0; print("deudas prom",deu,"creditos prom",cre,"dif",deu-cre,"AAI acumulable",r2((deu-cre)*fa))
print("creditos>deudas: dif 700000 ->deducible",r2(700000*fa))
print("== E7 IVA saldo a favor")
capex=3_000_000; iva_c=0.16*capex
a_cargo=0.16*gm
print("IVA capex",iva_c,"a cargo mes",r2(a_cargo),"saldo a favor mes1",r2(iva_c-a_cargo))
s=iva_c-a_cargo;n=1
while s>0:
    s-=a_cargo;n+=1
print("meses para agotar acreditando (incl. mes 1):",n, "resto",r2(s))
print("== E8 LIF 20-A-IV diesel 10,000 L")
print(10000*7.3634, 10000*0.0, "cuota disminuida dsl",cd["dsl"])
print("== E9 2027 LIEPS fr XIX")
c=6.7001+0.591390
print("cuota sin estimulo magna 2026",c)
print("compra 500000 vende 503000 ->",3000*c)
print("mes1 compra 520000 vende 500000 ->",0,"; mes2 compra 480000 vende 500000 ->",20000*c)
print("tolerancia 0.5% sobre 500000 L =",500000*0.005)
print("== E10 estimulo LIF 20-A-I agro 0.355 sobre precio con IVA")
print("ejemplo 100,000 pesos con IVA ->",100000*0.355)
print("== E3b cierre 2026")
ing_a=ing*12; cost_a=cost*12; opex_a=opex*12; ptu26=141000
uf26=ing_a-cost_a-opex_a-ptu26; isr26=uf26*0.3
pp_total=(ing_a*coef-ptu26)*0.30
print("ingresos 2026",r2(ing_a),"UF 2026",r2(uf26),"ISR anual",r2(isr26),"PP acumulados dic",r2(pp_total),"saldo a favor",r2(pp_total-isr26),"coef real",uf26/ing_a)
print("coef real*ing acum dic ->",r2((ing_a*(uf26/ing_a)-ptu26)*.3))
```
