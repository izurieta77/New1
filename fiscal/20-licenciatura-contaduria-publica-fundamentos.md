# 20 — Licenciatura en Contaduría Pública: fundamentos y ciclo contable

> Nivel: licenciatura · Actualizado: 2026-09-25 · Naturaleza de este módulo: normativa (no empírica). Las reglas citadas son pronunciamientos vigentes del CINIF (Consejo Mexicano de Normas de Información Financiera y de Sostenibilidad, A.C.) y disposiciones legales federales (Código de Comercio, Código Fiscal de la Federación, Ley del Impuesto sobre la Renta, Ley Federal del Trabajo). Acceso a las fuentes: el texto completo de **NIF A-1** se verificó línea por línea contra el PDF oficial publicado por el CINIF (`cinif.org.mx/files/NIF_A1.PDF`, versión de auscultación 2021 con entrada en vigor 1-ene-2023, confirmada por fuentes secundarias). El texto de las NIF particulares (Series B, C y D) está protegido tras el muro de pago de la obra "NIF 2026" que vende el CINIF y el IMCP; para esas normas este módulo se basa en **resúmenes técnicos de boletines de colegios de contadores (CCPUDG), firmas y plataformas de referencia jurídica (vLex, impuestos.info, elconta.mx)**, contrastados entre al menos dos fuentes independientes cuando fue posible. Esto se marca explícitamente en cada cita. Este módulo es la contraparte contable del despacho; no cubre derecho fiscal sustantivo (eso corresponde a `fiscal/10-12`, aún no creados en este repositorio al momento de escribir).

---

## 1. Objetivos de dominio

Quien complete este módulo debe poder, sin ayuda:

1. Explicar el Marco Conceptual de las NIF (NIF A-1, vigente desde ejercicios que inician el 1-ene-2023): los 8 postulados básicos, las 2 características cualitativas primarias y las 4 secundarias, y las definiciones exactas de activo, pasivo, capital, ingreso y costo/gasto.
2. Ejecutar el ciclo contable completo de una entidad lucrativa: registro por partida doble, pólizas, mayorización, balanza de comprobación, asientos de ajuste, cierre y los cuatro estados financieros básicos.
3. Aplicar las normas de reconocimiento y valuación de las NIF de uso más frecuente en una PyME constructora/manufacturera: cuentas por cobrar (C-3), propiedades, planta y equipo (C-6), deterioro (C-15), provisiones y contingencias (C-9), instrumentos financieros por pagar (C-19), ingresos y costos por contratos con clientes (D-1 y D-2, que sustituyeron al derogado Boletín D-7), inventarios (C-4) e impuestos a la utilidad (D-4).
4. Distinguir cuándo aplica consolidación (NIF B-8) frente a estados financieros individuales.
5. Costear un producto o proyecto por órdenes de producción y por procesos, y calcular el punto de equilibrio de un taller de herrería, carpintería o PVC.
6. Explicar con cifras por qué la utilidad contable y la utilidad fiscal divergen, y construir una conciliación contable-fiscal básica.
7. Ejecutar un cierre contable mensual completo de una constructora/PyME sin omitir pasos críticos (depreciación, provisiones, conciliación bancaria, IVA, nómina, CFDI).
8. Reconocer los errores más comunes de un pasante o contador junior y las trampas normativas que generan observaciones de auditoría o del SAT.

---

## 2. Marco Conceptual de las NIF (NIF A-1)

**Hecho verificado (fuente primaria CINIF):** desde el 1 de enero de 2023, el Marco Conceptual dejó de ser un paquete de ocho normas independientes (NIF A-1 a A-8, emitidas en 2005) y se consolidó en **una sola norma, NIF A-1, "Marco Conceptual de las Normas de Información Financiera"**, dividida en 9 capítulos (numerados 10 a 100) que tienen el mismo carácter normativo. El proyecto se puso en auscultación el 31-may-2021 con vigencia propuesta a partir de ejercicios que inicien el 1-ene-2023; fuentes secundarias (Crowe México) señalan aprobación final del Consejo Emisor el 24-nov-2022, aunque otra fuente secundaria ubica la aprobación en noviembre de 2021 — **este dato puntual de fecha de aprobación final queda sin verificar con precisión de día exacto contra fuente primaria**, no así la vigencia (1-ene-2023), que es consistente en todas las fuentes consultadas [1][2][3].

**Tabla de correspondencia (verificada contra el texto oficial del capítulo Introducción de NIF A-1):**

| Capítulo del nuevo MC | Nombre | NIF individual sustituida (marco 2005) |
|---|---|---|
| 10 | Estructura de las NIF | NIF A-1 |
| 20 | Postulados básicos | NIF A-2 |
| 30 | Objetivo de los estados financieros | NIF A-3 (antes "Necesidades de los usuarios y objetivos de los EF") |
| 40 | Características cualitativas de los EF | NIF A-4 |
| 50 | Elementos básicos de los EF | NIF A-5 |
| 60 | Reconocimiento | NIF A-6 (antes "Reconocimiento y valuación") |
| 70 | Valuación | NIF A-6 |
| 80 | Presentación y revelación | NIF A-7 |
| 90 | Supletoriedad | NIF A-8 |

En la práctica profesional y en la docencia mexicana persiste el uso coloquial de "NIF A-2", "NIF A-4", etc., para referirse a estos capítulos, aunque formalmente ya no son normas separadas [1][4].

### 2.1 Postulados básicos (Capítulo 20 de NIF A-1)

Son ocho, agrupados en tres funciones (texto oficial, párrafo 21.2):

1. **Sustancia económica**: el reconocimiento contable debe basarse en la realidad económica de la transacción, la cual debe prevalecer sobre su forma jurídica cuando ambas no coincidan (párr. 22.1–22.8). Ejemplo del propio texto: una venta con documentación que transfiere la propiedad legal, pero con acuerdos simultáneos que mantienen los beneficios y riesgos en el vendedor, no debe reconocerse como venta consumada.
2. **Entidad económica**: unidad identificable con un conjunto de recursos y actividades conducido por un único centro de control, cuya personalidad es independiente de sus propietarios; no necesariamente coincide con la entidad jurídica (párr. 23.1–23.5). Esto sustenta, por ejemplo, la consolidación de varias personas morales bajo un único centro de decisión.
3. **Negocio en marcha**: se presume existencia permanente en un horizonte ilimitado salvo prueba en contrario; la administración debe evaluar al menos los 12 meses siguientes a la fecha de los estados financieros (párr. 24.1–24.2).
4. **Devengación contable**: los efectos de las transacciones se reconocen cuando ocurren económicamente, independientemente de cuándo se cobren o paguen en efectivo (párr. 25.1). Es la base que separa utilidad contable de flujo de caja.
5. **Asociación de costos y gastos con ingresos**: los costos y gastos deben identificarse con el ingreso que generan, reconociéndose simultáneamente en el mismo periodo (párr. 26).
6. **Valuación**: los efectos financieros deben cuantificarse en términos monetarios atendiendo a los atributos del elemento valuado (párr. 27.1–27.2).
7. **Dualidad económica**: toda transacción se reconoce en forma dual —afecta la estructura financiera (activo/pasivo/capital), los resultados, o ambos simultáneamente— lo que sustenta la partida doble (párr. 28.1–28.4).
8. **Consistencia**: una entidad debe aplicar el mismo tratamiento contable a transacciones similares a través del tiempo, mientras no cambie la sustancia económica de la operación; esto es lo que hace comparable la información (párr. 29.1–29.4).

*Nota de cambio de criterio respecto al marco 2005:* el "periodo contable", antes asociado al postulado de devengación, se reubicó al capítulo 30 (Objetivo de los EF) por considerarse un tema de presentación y no de reconocimiento (párr. IN9) [1].

### 2.2 Características cualitativas (Capítulo 40)

**Cambio de jerarquía verificado (párr. IN11–IN12):** el marco 2005 (antigua NIF A-4) tenía cuatro características primarias (confiabilidad, relevancia, comprensibilidad, comparabilidad). El marco 2023 solo reconoce **dos primarias (fundamentales), indispensables**:

- **Relevancia** (párr. 42.1): los EF influyen en decisiones económicas cuando tienen valor de predicción y confirmación, y muestran los aspectos significativos (importancia relativa / materialidad). La importancia relativa no se define con umbrales numéricos fijos en la NIF; depende del juicio profesional sobre cuantía y circunstancias (párr. 42.1.4–42.1.10).
- **Representación fiel** (antes llamada "confiabilidad") (párr. 42.2): exige reflejar correctamente lo sucedido, estar libre de sesgo (neutralidad) y ser completa.

Las antiguas primarias **comprensibilidad** y **comparabilidad** bajaron de categoría y ahora son, junto con **verificabilidad** y **oportunidad**, las cuatro **características secundarias (de mejora)** (Capítulo 43): altamente deseables pero no indispensables — unos EF sin ellas pueden seguir siendo útiles, cosa que no ocurre si faltan las dos primarias [1].

### 2.3 Elementos básicos de los estados financieros (Capítulo 50)

Definiciones textuales verificadas contra el PDF oficial de NIF A-1:

- **Activo** (párr. 51.2.1): *"un recurso económico, es decir, un derecho que tiene el potencial para producir beneficios económicos futuros, controlado por una entidad, derivado de eventos pasados."* Cambio de fondo respecto al marco 2005: se eliminaron los requisitos de que el activo estuviera "identificado" y "cuantificado en términos monetarios" (ahora se consideran temas de reconocimiento/valuación, no de definición) (párr. IN13).
- **Pasivo** (párr. 51.3.1): *"una obligación presente de una entidad de transferir recursos económicos como resultado de eventos pasados."* Cambio relevante: ya no exige que la salida de recursos sea "probable"; basta que exista la obligación, **aunque la probabilidad de transferencia sea baja** (párr. IN13, tabla comparativa).
- **Capital contable / patrimonio contable** (párr. 51.5.1): *"el valor residual de los activos de la entidad, una vez deducidos todos sus pasivos"* — también llamado "activos netos".
- **Ingreso** (párr. 52.2.1): incremento de activos o decremento de pasivos durante un periodo, con impacto favorable en la utilidad o pérdida neta, distinto de las aportaciones de los propietarios.
- **Costo y gasto** (párr. 52.3.1): decremento de activos o incremento de pasivos durante un periodo, con la intención de generar ingresos y con impacto desfavorable en la utilidad o pérdida neta, distinto de las distribuciones a los propietarios.

**Inferencia práctica:** estas definiciones son la base para resolver, en la práctica de un despacho, casos límite que las NIF particulares no cubren explícitamente (el marco conceptual es normativo en México — a diferencia del IASB, donde el marco no es vinculante y cede ante una NIIF particular en conflicto, párr. IN20) [1].

### 2.4 Supletoriedad (Capítulo 90)

Cuando una NIF particular no cubre un caso, se aplica de forma supletoria otra norma que cumpla ciertos requisitos de calidad (párr. 91–95); en la práctica esto habilita, ante vacíos de las NIF, el uso razonado de las NIIF (IFRS) del IASB, dada la alta convergencia entre ambos marcos desde 2012.

---

## 3. Ciclo contable completo

**Práctica profesional estándar (no varía por NIF, es aplicación operativa de los postulados de devengación y dualidad económica):**

1. **Documento fuente**: CFDI (Comprobante Fiscal Digital por Internet) de ingreso, egreso, nómina o pago; contrato; estado de cuenta bancario.
2. **Póliza** (de ingreso, egreso o diario): registro por partida doble — todo cargo tiene su abono de igual monto, reflejando la dualidad económica.
3. **Catálogo de cuentas**: estructura jerárquica (rubro-cuenta-subcuenta) alineada al código agrupador del SAT para efectos de la Contabilidad Electrónica (obligación fiscal, no contable per se, pero que en la práctica define el catálogo de la mayoría de las PyMEs mexicanas).
4. **Mayorización**: acumulación de los movimientos de cada cuenta.
5. **Balanza de comprobación**: sumas y saldos de todas las cuentas; el total de cargos debe igualar al total de abonos (consecuencia aritmética de la partida doble).
6. **Asientos de ajuste** de fin de periodo, entre otros: depreciación del periodo (NIF C-6), estimación de pérdidas crediticias esperadas (NIF C-3), devengación de intereses, provisiones (NIF C-9), efecto de impuestos diferidos (NIF D-4), ajuste anual por inflación fiscal (para conciliación, no para libros NIF, ya que México dejó de tener economía "de alta inflación" bajo NIF B-10 en 2008).
7. **Balanza ajustada** y **hoja de trabajo**.
8. **Estados financieros básicos**, cuya lista obligatoria (para entidades lucrativas) está establecida en el capítulo 30 de NIF A-1 (antes NIF A-3, párr. 38): estado de situación financiera (NIF B-6), estado de resultado integral (NIF B-3), estado de cambios en el capital contable (NIF B-4) y estado de flujos de efectivo (NIF B-2), acompañados de notas [5][6].
9. **Asientos de cierre**: cancelación de cuentas de resultados contra la cuenta de utilidad o pérdida neta del ejercicio, que pasa a capital contable.

**NIF B-2, Estado de Flujos de Efectivo** (hecho, fuente secundaria consistente con al menos dos fuentes independientes): aprobada por unanimidad por el Consejo Emisor del CINIF en noviembre de 2007, sustituyó al estado de cambios en la situación financiera y entró en vigor el 1-ene-2008; tuvo mejoras vigentes desde ejercicios que inician el 1-ene-2018 (aplicación anticipada permitida desde 2017). Clasifica los flujos en actividades de **operación**, **inversión** y **financiamiento**; permite el método directo o el indirecto para operación (el indirecto, partiendo de la utilidad neta, es el de uso casi universal en México) [5][7].

**Obligaciones mercantiles del Código de Comercio (hecho, ley federal, no NIF):** el Art. 33 obliga a todo comerciante a llevar un sistema de contabilidad adecuado que permita identificar cada operación y conectarla con su comprobante original; el Art. 34 exige, como mínimo, un libro mayor (y libro de actas para personas morales); el Art. 38 obliga a conservar los comprobantes originales por **10 años** [8][9][10]. Esto es un plazo distinto —y más largo— que el de conservación fiscal.

---

## 4. NIF de reconocimiento y valuación para una PyME/constructora

### 4.1 NIF C-3, Cuentas por cobrar

Aprobada por el Consejo Emisor del CINIF en noviembre de 2013; entrada en vigor obligatoria para ejercicios que inicien el 1-ene-2018, con aplicación anticipada permitida desde 2016 si se adoptaba junto con NIF C-20 (Instrumentos financieros para cobrar principal e interés). Su aportación central frente al boletín anterior: exige estimar la incobrabilidad **desde el reconocimiento inicial del ingreso**, con base en **pérdidas crediticias esperadas (PCE)** —modelo prospectivo, no el antiguo modelo de "pérdida incurrida"— considerando experiencia histórica, condiciones actuales y pronósticos razonables y sustentables. Si el plazo de la cuenta por cobrar es significativo, debe reconocerse su valor presente [11][12].

### 4.2 NIF C-6, Propiedades, planta y equipo

Aprobada en diciembre de 2010, vigente desde el 1-ene-2011 (la componentización obligatoria, cuando las partes tienen vidas útiles distintas, se hizo exigible un año después para quien no la hubiera aplicado antes). Converge con la NIC 16 del IASB. Puntos clave verificados en resúmenes técnicos:

- Costo inicial = precio de adquisición + costos directamente atribuibles para poner el activo en condiciones de uso (instalación, pruebas, honorarios) + estimación de costos de desmantelamiento cuando aplique.
- **Componentización obligatoria** (párr. 44.3 de la norma, según boletín técnico): cada componente cuyo costo sea significativo respecto del total, y cuya vida útil o patrón de consumo difiera del componente principal, debe depreciarse por separado. Esto es crítico en una constructora: instalaciones, maquinaria pesada y estructura de un mismo activo pueden tener vidas útiles muy distintas.
- Presentación: costo menos depreciación acumulada menos pérdidas por deterioro acumuladas [13].

### 4.3 NIF C-15, Deterioro en el valor de los activos de larga duración y su disposición

Aprobada en diciembre de 2020, vigente desde ejercicios que inician el 1-ene-2022 (converge con NIC 36). Aplica tanto a activos tangibles (propiedades, planta y equipo) como intangibles. El deterioro es el exceso del valor neto en libros sobre el **monto recuperable**, definido como el mayor entre el **valor de uso** (valor presente de flujos futuros esperados) y el **precio neto de venta**. Si el valor de recuperación de la unidad generadora de efectivo es menor a su valor en libros, la diferencia se reconoce como pérdida en resultados [14].

### 4.4 NIF C-9, Provisiones, contingencias y compromisos

Aprobada en noviembre de 2014, vigente desde el 1-ene-2018 (anticipada desde 2016 junto con NIF C-19). Se apoya en el postulado de devengación contable (Capítulo 20 de NIF A-1) para definir el momento de reconocimiento. Distinción central:

- **Provisión**: pasivo de monto o vencimiento inciertos que **sí** se reconoce en los estados financieros porque es una obligación presente y es **probable** la salida de recursos.
- **Pasivo contingente**: obligación **posible**, sujeta a la ocurrencia o no de eventos futuros inciertos fuera del control total de la entidad; **no** se reconoce como pasivo, solo se revela en notas [15].

### 4.5 NIF C-19, Instrumentos financieros por pagar

Aprobada en noviembre de 2014, vigente desde el 1-ene-2018 (anticipada desde 2016 junto con C-3, C-9 y C-20). Los instrumentos financieros por pagar se valúan inicialmente a valor razonable de la contraprestación y, posteriormente, a **costo amortizado** mediante el **método de interés efectivo** (salvo los que se valúan a valor razonable con efecto en resultados). Esto implica que el gasto por intereses reconocido en resultados de un préstamo o crédito bancario puede diferir del interés nominal pagado, sobre todo cuando hay comisiones o costos de apertura que se amortizan a lo largo de la vida del crédito [16].

### 4.6 NIF B-8, Estados financieros consolidados o combinados

Aprobada en diciembre de 2012, vigente desde el 1-ene-2013. Converge con la NIIF 10. Establece el **principio de control** —no solo la tenencia accionaria mayoritaria— como base para exigir la consolidación de una controladora con sus subsidiarias. Para una PyME familiar con varias sociedades operativas bajo un mismo dueño (frecuente en el sector construcción mexicano), esta NIF determina si deben presentarse estados financieros consolidados cuando existe un centro de control único, aun sin tenencia accionaria formal [17].

### 4.7 NIF D-1 e D-2 (sustituyen al derogado Boletín D-7 y a la INIF 14) — reconocimiento de ingresos y costos en contratos de construcción

**Corrección de criterio frente a materiales de estudio desactualizados:** buena parte del material docente en circulación sigue enseñando el **Boletín D-7, "Contratos de construcción y de fabricación de ciertos bienes de capital"**, con su método de "por ciento de avance". Verificado: **el Boletín D-7 y la INIF 14 fueron derogados** por la entrada en vigor conjunta de **NIF D-1, Ingresos por contratos con clientes**, y **NIF D-2, Costos por contratos con clientes**, ambas aprobadas por el Consejo Emisor del CINIF en 2015 (D-1 en octubre, D-2 en noviembre) y vigentes desde ejercicios que inician el **1-ene-2018**. Convergen con la NIIF 15 / ASC 606 [18][19][20].

**NIF D-1 — modelo de 5 pasos** (verificado):
1. Identificar el contrato con el cliente.
2. Identificar las obligaciones de desempeño (bienes o servicios distintos) del contrato.
3. Determinar el precio de la transacción.
4. Asignar el precio de la transacción a cada obligación de desempeño.
5. Reconocer el ingreso cuando (o a medida que) se satisface cada obligación de desempeño.

**Criterio para reconocer el ingreso a lo largo del tiempo ("over time") en vez de en un punto del tiempo** — relevante para una constructora que factura por avance de obra: se reconoce a lo largo del tiempo cuando se cumple al menos una de estas condiciones: (a) el cliente recibe y consume simultáneamente los beneficios conforme la entidad ejecuta; (b) el desempeño de la entidad crea o mejora un activo que el cliente controla conforme se crea o mejora; o (c) el activo creado no tiene un uso alternativo para la entidad y esta tiene derecho exigible al cobro por el desempeño completado a la fecha. Los contratos de obra por encargo específico de un cliente suelen calificar en (b) o (c), lo que en la práctica preserva, bajo una base conceptual distinta (control, no "grado de avance" per se), un resultado similar al método de avance de obra que ya usaban los contadores de la construcción [18][19].

**NIF D-2** separa y amplía el tratamiento de costos: costos para obtener el contrato (p. ej., comisiones de venta, capitalizables si son incrementales y recuperables) y costos para cumplir el contrato, reconocidos en resultados en el momento en que se transfiere el control de los bienes o servicios al cliente [19].

### 4.8 NIF C-4, Inventarios

Vigente desde el 1-ene-2011, converge con la NIC 2. **Métodos de costeo permitidos: costo promedio y costo identificado**; a diferencia de la NIC 2 internacional, NIF C-4 **no incluye PEPS como método NIF** de forma expresa en el mismo listado que otorga la norma internacional (aunque en la práctica mexicana PEPS se sigue usando y es aceptado fiscalmente). **El método UEPS (LIFO) y el costeo directo fueron eliminados de NIF C-4 desde el 1-ene-2011**; fiscalmente, UEPS ya no es deducible desde 2014 (LISR vigente) [21].

### 4.9 NIF D-4, Impuestos a la utilidad

Aprobada por el Consejo Emisor en julio de 2007, publicada en agosto de 2007, vigente desde el 1-ene-2008. Establece el **método de activos y pasivos** para el impuesto diferido: se compara el valor contable (en libros) y el valor fiscal de cada activo y pasivo; toda diferencia temporal genera un impuesto diferido (activo o pasivo), a diferencia del método anterior a 2000 que solo reconocía diferido por partidas que afectaban la utilidad o pérdida neta. El **Proyecto de Mejoras a las NIF 2026** (auscultación publicada el 15-sep-2025 por el CINIF, con vigencia propuesta a ejercicios que inicien el 1-ene-2026) precisa el alcance de NIF D-4 (párr. 20.1): aplica solo a entidades lucrativas obligadas al pago de impuestos sobre una utilidad fiscal determinada **sobre base neta y no bruta** — aclaración pensada, entre otros casos, para no confundir el ISR corporativo con impuestos calculados sobre ingresos brutos [22][23][24].

**Cambio institucional relevante de 2026, verificado:** el emisor de las NIF cambió su razón social en mayo de 2023 (fuente secundaria) a **"Consejo Mexicano de Normas de Información Financiera y de Sostenibilidad, A.C."** (mismo acrónimo CINIF), reflejando la emisión adicional de Normas de Información de Sostenibilidad (NIS); esto no altera la sigla ni el número de las NIF contables ya emitidas [25][26].

---

## 5. Contabilidad de costos básica: manufactura y construcción (herrería, carpintería, PVC)

**Práctica profesional estándar (contabilidad de costos es disciplina de gestión; su marco de reconocimiento de ingresos y costos de contrato con el cliente está en NIF D-1/D-2 §4.7, y su valuación de inventarios en NIF C-4 §4.8; el "costeo" interno no tiene una NIF única propia):**

**Costos directos** (materia prima directa + mano de obra directa) vs. **costos indirectos de fabricación (CIF)**: energía del taller, depreciación de maquinaria (NIF C-6), renta de nave, supervisión. Los CIF se aplican a la producción mediante una tasa predeterminada (CIF presupuestados / base de aplicación presupuestada, p. ej. horas-máquina u horas-hombre).

- **Costeo por órdenes de producción**: apropiado para un taller de herrería o carpintería que fabrica piezas o proyectos únicos por pedido (un portón, una escalera, una cocina integral). El costo se acumula por orden específica en una hoja de costos; el costo unitario = costo total de la orden / unidades producidas en esa orden.
- **Costeo por procesos**: apropiado para producción homogénea y continua (p. ej., perfiles de PVC estandarizados en serie). El costo se acumula por departamento/proceso y periodo, y se divide entre las unidades equivalentes producidas.

**Punto de equilibrio** (identidad matemática, no norma contable):
- Unidades de equilibrio = Costos fijos totales / (Precio de venta unitario − Costo variable unitario)
- Margen de contribución unitario = Precio − Costo variable unitario.
- **Ejemplo ilustrativo (Inferencia con cifras hipotéticas para fines didácticos, no un dato de mercado verificado):** un taller de herrería con costos fijos mensuales de $80,000 MXN (renta, nómina base, depreciación de maquinaria), que vende portones a $6,000 MXN con costo variable de $3,500 MXN por unidad, tiene margen de contribución de $2,500 MXN; el punto de equilibrio es 80,000/2,500 = **32 portones al mes**.

**Inferencia práctica para una constructora:** cuando el "producto" es un proyecto de obra con contrato específico (no producción en serie), lo relevante no es tanto el punto de equilibrio unitario clásico, sino el **presupuesto de obra por partidas** (números generadores) conciliado contra el avance físico y financiero real, y su vínculo directo con el reconocimiento de ingresos "over time" de NIF D-1 (§4.7): el porcentaje de avance que se usa para facturar y para reconocer contablemente el ingreso debe estar sustentado en el mismo presupuesto de costos que usa el área técnica, o se generan diferencias no explicables ante una auditoría o revisión del SAT.

---

## 6. Relación contabilidad-fiscal: por qué la utilidad contable difiere de la utilidad fiscal

**Hecho:** la utilidad contable se determina con las NIF (devengación, NIF A-1 §2.1; reconocimiento de ingresos NIF D-1; costo amortizado NIF C-19; deterioro NIF C-15; provisiones NIF C-9). La utilidad fiscal se determina con la Ley del Impuesto sobre la Renta (LISR), que tiene sus propias reglas de acumulación de ingresos y deducción de gastos, no siempre alineadas con las NIF. Las causas típicas de divergencia:

**(a) Partidas contablemente reconocidas como gasto/costo pero no deducibles fiscalmente (Art. 28 LISR)**, entre las más frecuentes en una PyME:
- El propio ISR pagado por la entidad (fracción I).
- Gastos e inversiones en la proporción que representen los ingresos exentos respecto del total de ingresos (fracción II).
- Obsequios y atenciones a clientes, salvo los directamente relacionados con la venta y ofrecidos a clientes en general (fracción III).
- Gastos de representación (fracción IV).
- Viáticos que no cumplan los requisitos de comprobación y destino específicos (fracción V).
- Consumos en restaurantes: solo **91.5%** es deducible, y siempre que el pago se haga con medios electrónicos (fracción XX) [27][28].

**(b) Momentos de reconocimiento distintos entre NIF y LISR:**
- **Anticipos de clientes**: bajo NIF D-1, un anticipo se reconoce como **pasivo** (no como ingreso) hasta que se satisface la obligación de desempeño. Bajo el Art. 17, fracción I, inciso c) de la LISR, el ingreso es acumulable cuando se cobra, se factura o es exigible la contraprestación —**lo que ocurra primero**—, lo cual incluye expresamente los anticipos. Esto genera una diferencia temporal clásica: hay ISR a pagar sobre un anticipo que contablemente todavía no es ingreso [29][30].
- **Depreciación**: la LISR (Art. 34–35) fija tasas máximas de deducción por tipo de activo (p. ej., 5% anual para construcciones, 25% para equipo de cómputo, entre otras), que casi nunca coinciden con la vida útil económica que exige NIF C-6 para la depreciación contable. Esto genera diferencias temporales que NIF D-4 obliga a reconocer como impuesto diferido.
- **Provisiones (NIF C-9)**: una provisión (p. ej., de garantías o de una contingencia laboral) se reconoce contablemente cuando es probable la salida de recursos, aunque el pago real ocurra después; fiscalmente, la mayoría de las provisiones **no son deducibles hasta que efectivamente se eroga el gasto** (requisito general de deducibilidad de "efectivamente pagado" o de cumplir los requisitos específicos del Art. 27 LISR), generando otra diferencia temporal.
- **Estimación de cuentas incobrables (NIF C-3, PCE)**: contablemente se reconoce desde el origen del ingreso con base en pérdida esperada; fiscalmente, la deducción de una cuenta incobrable solo procede cuando se cumplen los supuestos específicos del Art. 25/27 LISR (notoria imposibilidad práctica de cobro, plazos y montos específicos), casi siempre en un momento posterior.

**(c) PTU (Participación de los Trabajadores en las Utilidades):** derecho constitucional (Art. 123, apartado A, fracción IX de la Constitución; Arts. 117–131 de la Ley Federal del Trabajo) equivalente al **10% de la renta gravable** determinada conforme a las reglas de la LISR (ingresos acumulables menos deducciones autorizadas, sin restar la propia PTU pagada ni pérdidas fiscales de ejercicios anteriores). Contablemente, la PTU causada del ejercicio se reconoce como un gasto de operación (no como impuesto a la utilidad), pero su base de cálculo nace de la utilidad fiscal, no de la contable, por lo que también participa de las diferencias descritas arriba [31][32].

**(d) Régimen fiscal y su efecto en la brecha contable-fiscal:** desde 2022, el **RESICO para personas morales** (aplicable si los ingresos totales del ejercicio anterior no exceden $35,000,000 MXN y se cumplen otros requisitos societarios) determina el ISR sobre **flujo de efectivo real** —ingresos acumulables cuando se cobran y deducciones cuando se pagan—, lo que **reduce mecánicamente** varias de las diferencias temporales descritas arriba (en particular, la de anticipos y cuentas por cobrar/pagar), aunque la contabilidad NIF de la entidad sigue debiendo llevarse sobre base de devengado. La tasa del ISR corporativo (Art. 9 LISR) es **30%** tanto en el régimen general como en RESICO PM; lo que cambia entre regímenes es la base gravable, no la tasa [33][34].

**Herramienta operativa — conciliación contable-fiscal (práctica profesional estándar, no una NIF):**

```
Utilidad contable antes de impuestos (NIF)
(+) Gastos contables no deducibles (Art. 28 LISR)
(+) Ingresos fiscales no reconocidos aún contablemente (p. ej., anticipos acumulados)
(−) Deducciones fiscales autorizadas no reflejadas como gasto contable del periodo
(−) Ingresos contables ya reconocidos que no son acumulables aún fiscalmente
= Utilidad fiscal (base del ISR del ejercicio, antes de PTU y pérdidas fiscales)
```

El efecto de impuesto diferido (NIF D-4) es, precisamente, el mecanismo contable que reconoce hoy el impuesto que se pagará o se ahorrará en el futuro por estas diferencias **temporales** (las que se revierten con el tiempo); las diferencias **permanentes** (como los gastos no deducibles del Art. 28 que nunca se recuperan) no generan impuesto diferido, solo afectan la tasa efectiva del ejercicio.

---

## 7. Traducción operable: checklist mensual de cierre contable de una PyME constructora

**Práctica profesional (síntesis operativa, no cita textual de una norma):**

1. Conciliar todos los CFDI emitidos y recibidos del mes contra la balanza (ingresos, egresos, nómina, pago).
2. Conciliar bancos: saldo contable vs. estado de cuenta; identificar partidas en tránsito.
3. Registrar la depreciación del mes de propiedades, planta y equipo por componente (NIF C-6), incluida maquinaria de obra.
4. Actualizar la estimación de pérdidas crediticias esperadas de clientes (NIF C-3) con la información más reciente de cartera vencida.
5. Revisar y, si aplica, registrar provisiones de garantías, contingencias laborales o legales conocidas al cierre (NIF C-9), distinguiéndolas de los pasivos contingentes que solo van en notas.
6. Calcular el interés efectivo devengado del mes sobre créditos y pasivos financieros a costo amortizado (NIF C-19).
7. Actualizar el porcentaje de avance de obra de cada contrato activo y conciliarlo entre el área técnica (números generadores) y el reconocimiento de ingresos NIF D-1/costos NIF D-2; verificar que la facturación (CFDI) del periodo sea consistente con el ingreso contable reconocido.
8. Valuar inventarios de materiales de obra en tránsito o en almacén con el método de costeo consistente (costo promedio o costo identificado, NIF C-4).
9. Calcular el IVA del periodo (trasladado menos acreditable) y conciliarlo contra la declaración provisional.
10. Timbrar y contabilizar la nómina del periodo, incluidas las provisiones de aguinaldo, prima vacacional, vacaciones y PTU del ejercicio en curso (aunque el pago sea posterior).
11. Revisar si existe deterioro (NIF C-15) en algún activo de larga duración con indicios de pérdida de valor (obra detenida, maquinaria obsoleta, cliente en incumplimiento grave).
12. Elaborar la balanza de comprobación ajustada y los cuatro estados financieros básicos (NIF B-6, B-3, B-4, B-2).
13. Actualizar la hoja de trabajo de la conciliación contable-fiscal (§6) para efectos de los pagos provisionales de ISR.
14. Respaldar y archivar la documentación soporte conforme a los plazos legales: 10 años (Código de Comercio, Art. 38) y 5 años (Código Fiscal de la Federación, Art. 30) [10][35].

---

## 8. Trampas y errores comunes

- **Confundir "provisión" con "reserva" o con un simple ajuste discrecional de utilidad.** Bajo NIF C-9, una provisión exige una obligación presente y probable salida de recursos con estimación razonable; provisionar "por prudencia" sin esos tres elementos no es correcto y puede maquillar resultados.
- **Depreciar con la tasa fiscal de la LISR en la contabilidad NIF.** Es un error extendido en despachos pequeños por simplicidad administrativa; genera estados financieros NIF que en realidad son híbridos fiscales, y esconde el impuesto diferido que exige NIF D-4.
- **Reconocer el ingreso de un contrato de obra al 100% con la primera factura o al recibir el anticipo**, ignorando el modelo de 5 pasos de NIF D-1 y el criterio de satisfacción de la obligación de desempeño a lo largo del tiempo.
- **Enseñar o aplicar el Boletín D-7** como si siguiera vigente: fue derogado desde 2018 por NIF D-1/D-2 (§4.7). Es uno de los errores de criterio desactualizado más comunes en material docente mexicano en circulación.
- **No componentizar activos con vidas útiles distintas** (NIF C-6), depreciando un edificio industrial completo a una sola tasa cuando instalaciones y maquinaria integradas tienen vidas útiles muy distintas.
- **Tratar los anticipos de clientes como ingreso contable inmediato** (correcto solo si ya se satisfizo la obligación de desempeño) — y, en sentido opuesto, olvidar que fiscalmente el anticipo **sí** suele ser ingreso acumulable de inmediato (Art. 17 LISR), generando una diferencia temporal que hay que reconocer en la conciliación y, si es material, como impuesto diferido.
- **Confundir el plazo de conservación fiscal (5 años, CFF Art. 30) con el mercantil (10 años, Código de Comercio Art. 38)** y destruir documentación societaria o de actas antes de tiempo.
- **Aplicar UEPS o costeo directo de inventarios** creyendo que siguen siendo opciones NIF vigentes: ambos fueron eliminados de NIF C-4 desde 2011.
- **No distinguir entidad económica de entidad jurídica** (NIF A-1, postulado de entidad económica) en grupos familiares con varias razones sociales bajo un mismo control, omitiendo evaluar si corresponde consolidar (NIF B-8).

---

## 9. Autoevaluación (15 preguntas)

1. **¿Cuántos postulados básicos reconoce el capítulo 20 de NIF A-1, y cuáles son los tres que sirven de base directa al reconocimiento contable de transacciones?**
   Ocho postulados; los que dan base directa al reconocimiento son devengación contable, asociación de costos y gastos con ingresos, valuación, dualidad económica y consistencia (los otros tres — sustancia económica, entidad económica, negocio en marcha — delimitan el sistema y la entidad, no el momento del reconocimiento).

2. **¿Cuáles son las dos características cualitativas primarias de los estados financieros bajo el marco vigente desde 2023, y en qué cambiaron respecto al marco 2005?**
   Relevancia y representación fiel (antes "confiabilidad"). Comprensibilidad y comparabilidad bajaron de primarias a secundarias.

3. **Define activo según NIF A-1 (párr. 51.2.1) y señala qué elemento eliminó el marco 2023 respecto a la definición de 2005.**
   Un recurso económico —un derecho con potencial de producir beneficios económicos futuros, controlado por la entidad, derivado de eventos pasados. Se eliminaron los requisitos de estar "identificado" y "cuantificado en términos monetarios".

4. **Una empresa recibe un anticipo de un cliente por una obra que aún no inicia. Contablemente (NIF D-1) y fiscalmente (Art. 17 LISR), ¿cómo se trata ese anticipo?**
   Contablemente es un pasivo hasta que se satisface la obligación de desempeño. Fiscalmente es ingreso acumulable de inmediato (lo que ocurra primero entre cobro, exigibilidad o facturación). Genera una diferencia temporal.

5. **¿Qué NIF derogó al Boletín D-7 y a la INIF 14, y desde cuándo?**
   NIF D-1 (Ingresos por contratos con clientes) y NIF D-2 (Costos por contratos con clientes), vigentes desde ejercicios que inician el 1-ene-2018.

6. **Bajo NIF D-1, ¿cuáles son los tres criterios alternativos para reconocer el ingreso "a lo largo del tiempo" en vez de "en un punto en el tiempo"?**
   (a) El cliente recibe y consume simultáneamente los beneficios; (b) el desempeño crea o mejora un activo que el cliente controla conforme se ejecuta; (c) el activo no tiene uso alternativo y hay derecho exigible al cobro por lo ejecutado a la fecha.

7. **¿Qué diferencia hay entre una provisión y un pasivo contingente bajo NIF C-9?**
   La provisión es una obligación presente con probable salida de recursos: se reconoce como pasivo. El pasivo contingente es una obligación posible sujeta a eventos futuros inciertos: solo se revela en notas, no se reconoce.

8. **¿A costo de qué se valúan posteriormente los instrumentos financieros por pagar bajo NIF C-19?**
   A costo amortizado mediante el método de interés efectivo (salvo los designados a valor razonable con efecto en resultados).

9. **¿Qué método de costeo de inventarios eliminó NIF C-4 desde 2011, y sigue siendo fiscalmente deducible en México?**
   UEPS (y el costeo directo) fueron eliminados de NIF C-4 desde 2011; fiscalmente UEPS dejó de ser deducible desde 2014.

10. **¿Qué principio usa NIF B-8 para exigir la consolidación de estados financieros, y por qué es relevante en un grupo familiar de constructoras?**
    El principio de control (centro único de decisión sobre las actividades relevantes), no solo la tenencia accionaria mayoritaria; puede obligar a consolidar aunque no haya una tenencia formal común.

11. **Explica con un ejemplo por qué la depreciación contable (NIF C-6) casi nunca coincide con la depreciación fiscal (LISR).**
    NIF C-6 usa la vida útil económica real del activo estimada por la entidad; la LISR fija tasas máximas por tipo de activo (p. ej. 5% anual para construcciones). Si la vida útil económica real es de 15 años, la depreciación contable anual será mayor a la fiscal (que se deprecia en 20 años a 5%), generando una diferencia temporal que exige reconocer impuesto diferido bajo NIF D-4.

12. **¿Cuál es la base gravable de la PTU y qué porcentaje se reparte?**
    10% de la renta gravable, equivalente a la utilidad fiscal (ingresos acumulables menos deducciones autorizadas de la LISR), sin restar la PTU pagada del ejercicio ni pérdidas fiscales de ejercicios anteriores.

13. **Un taller de herrería tiene costos fijos mensuales de $80,000 MXN, vende portones a $6,000 MXN con costo variable de $3,500 MXN. ¿Cuál es su punto de equilibrio mensual en unidades?**
    Margen de contribución = $2,500 MXN; punto de equilibrio = 80,000/2,500 = 32 portones.

14. **¿Qué plazo de conservación exige el Código de Comercio (Art. 38) para los comprobantes originales de operaciones, y cuál exige el Código Fiscal de la Federación (Art. 30) para la contabilidad con fines fiscales?**
    10 años (mercantil) y 5 años (fiscal), respectivamente.

15. **¿Qué régimen fiscal para personas morales, disponible desde 2022 con tope de $35,000,000 MXN de ingresos del ejercicio anterior, determina el ISR sobre flujo de efectivo real en vez de devengado, y qué efecto tiene esto sobre la brecha contable-fiscal descrita en la sección 6?**
    RESICO para personas morales. Reduce varias de las diferencias temporales típicas (en especial las de anticipos y cuentas por cobrar/pagar), porque acumula ingresos al cobro y deduce gastos al pago, aunque la contabilidad NIF de la entidad se sigue llevando sobre base de devengado.

---

## 10. Fuentes

1. CINIF — NIF A-1, Marco Conceptual de las Normas de Información Financiera (texto completo, versión de auscultación 31-may-2021, propuesta de vigencia 1-ene-2023; verificado línea por línea): https://cinif.org.mx/files/NIF_A1.PDF
2. Crowe México — Marco Conceptual de las NIF (fechas de emisión 24-nov-2022 y vigencia 1-ene-2023): https://www.crowe.com/mx/noticias/marco_conceptual_de_las_nif
3. CCPUDG — Boletín "Serie NIF A-1, su nuevo Marco Conceptual": https://ccpudg.org.mx/wp-content/uploads/053-Boletin-Comision-NIA-y-NIF-CCPUDG-NIF-A-1-SU-NUEVO-MARCO-CONCEPTUAL.pdf
4. vLex México — NIF A-1, Marco Conceptual de las Normas de Información Financiera: https://vlex.com.mx/vid/nif-1-marco-conceptual-923733972
5. Cofide — NIF B-2, Estado de flujos de efectivo (resumen técnico, fechas de emisión y vigencia): https://www.cofide.mx/hubfs/Recursos%20Extras/13_NIF%20B-2%20Estado%20de%20flujos%20de%20efectivo%20-%20Normas%20de%20Informaci%C3%B3n%20Financiera.pdf?hsLang=es-mx
6. Contadigital — Normas de información financiera, lista de NIF B-3, B-4, B-6: https://www.contadigital.mx/posts/normas-de-informacion-financiera
7. RUA UNAM — Estado de flujos de efectivo NIF-B2: https://www.rua.unam.mx/portal/recursos/ficha/7634/estado-de-flujos-de-efectivo-nif-b2
8. Diputados — Código de Comercio (texto vigente): https://www.diputados.gob.mx/LeyesBiblio/pdf/CCom.pdf
9. leyes-mx.com — Artículo 33 del Código de Comercio: https://leyes-mx.com/codigo_de_comercio/33.htm
10. leyes-mx.com — Artículo 38 del Código de Comercio (conservación de comprobantes): https://leyes-mx.com/codigo_de_comercio/38.htm
11. Pérez Góngora y Asociados — Estimación de Pérdidas Crediticias, NIF C-3: https://www.perezgongora.com/blog/estimacion-de-perdidas-crediticias-de-acuerdo-a-la-norma-de-informacion-financiera-nif-c-3
12. Texto de referencia CINIF, NIF C-3, Cuentas por cobrar (documento hospedado por tercero, contrastar contra edición oficial 2026): https://img1.wsimg.com/blobby/go/9fe88fcd-228a-4f95-a2c6-0870bfa90f31/downloads/C-3%20Cuentas%20por%20Cobrar.pdf
13. CCPUDG — Boletín #014, "Propiedades, Planta y Equipo, NIF C-6": https://ccpudg.org.mx/wp-content/uploads/014-Boletin-Comision-NIF-CCPUDG-NIF-C-6-Propiedades-Planta-y-Equipo.pdf
14. Grupo CPCON — NIF C-15, Deterioro en el valor de los activos de larga duración: https://grupocpcon.com/es-mx/nic-36-deterioro-del-valor-de-los-activos-nif-c-15/
15. AMCP — Tratamiento contable de la NIF C-9, Provisiones, contingencias y compromisos: https://amcpdf.org.mx/tratamiento-contable-de-la-nif-c-9-provisiones-contingencias-y-compromisos/
16. impuestos.info — NIF C-19, Instrumentos financieros por pagar: https://impuestos.info/norma-de-informacion-financiera-c-19-instrumentos-financieros-por-pagar/
17. CCPUDG — Boletín NIF B-8, Estados financieros consolidados o combinados: https://ccpudg.org.mx/wp-content/uploads/067-Boletin-Comision-NIA-y-NIF-CCPUDG-NIF-B-8-Estados-financieros-consolidados-o-combinados.pdf
18. CCPUDG — Boletín NIF D-1, Ingresos por contratos con clientes (modelo de 5 pasos, criterios "over time", vigencia y normas sustituidas): https://ccpudg.org.mx/wp-content/uploads/061-Boletin-Comision-NIA-y-NIF-CCPUDG-NIF-D-1.pdf
19. elconta.mx — Nueva NIF D-2, Costos por contratos con clientes: https://elconta.mx/nif-d-2-costos-por-contratos-con-clientes/
20. IMCP — Norma de Información Financiera D-1, Ingresos por contratos con clientes: https://imcp.org.mx/norma-de-informacion-financiera-d-1-ingresos-por-contratos-con-clientes/
21. Análisis Vinculatégica UANL — Eliminación del método UEPS para efectos fiscales y contables (NIF C-4): http://www.web.facpya.uanl.mx/vinculategica/Revistas/R2/1540-1557%20-%20Analisis%20De%20Los%20Impactos%20Fiscales%20Y%20Financieros%20Por%20La%20Eliminacion%20Del%20Metodo%20Ueps%20Para%20Efectos%20Fiscales.pdf
22. Morgan Online — CPC Ernesto Álvarez Díaz, "NIF D-4, Impuestos a la utilidad": https://morganonline.com.mx/wp-content/uploads/2021/08/D-4-Impuestos-a-la-utilidad.pdf
23. CINIF — Mejoras a las Normas de Información Financiera 2026, Proyecto para auscultación (15-sep-2025; precisión de alcance de NIF D-4, párr. 20.1; vigencia propuesta 1-ene-2026): https://www.cinif.org.mx/uploads/Mejoras_NIF_2026_PROYECTO_AUSCULTACION.pdf
24. CINIF — Normatividad NIF 2026: https://www.cinif.org.mx/normatividad_NIF2026.php
25. CINIF — Sitio oficial (razón social actual, Consejo Mexicano de Normas de Información Financiera y de Sostenibilidad, A.C.): https://www.cinif.org.mx/
26. GLENIF — Ficha de México (contexto institucional del CINIF): https://glenif.org/en/mexico-eng/
27. SDV Asesores — Compendio, Art. 28 LISR 2026, gastos no deducibles: https://sdv.com.mx/compendio/ley-isr/articulo-28/
28. Diputados — Ley del Impuesto sobre la Renta (texto vigente): https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf
29. SDV Asesores — Compendio, Art. 17 LISR 2026, momento de acumulación de ingresos: https://sdv.com.mx/compendio/ley-isr/articulo-17/
30. Consultorio Fiscal UNAM — Tratamiento de los anticipos de clientes: https://consultoriofiscal.unam.mx/articulo.php?id_articulo=3170
31. Fortia — Guía de la PTU o reparto de utilidades (base gravable, 10%, distribución): https://fortia.com.mx/la-guia-definitiva-de-la-ptu-o-reparto-de-utilidades/
32. Siempre al Día — Determinación de la utilidad fiscal, base para reparto de PTU 2026: https://siemprealdia.co/mexico/fiscal/determinacion-de-la-utilidad-fiscal-base-para-reparto-de-ptu/
33. SDV Asesores — Compendio, Art. 9 LISR 2026, tasa del 30% para personas morales: https://sdv.com.mx/compendio/ley-isr/articulo-9/
34. Carbajal Contadores — RESICO Personas Morales 2026: tasas, obligaciones y auditoría del SAT: https://carbajalcontadores.com/2026/09/03/resico-personas-morales-2026-tasas-obligaciones-sat-auditando
35. mley.mx — Artículo 30 del Código Fiscal de la Federación (plazo de conservación de 5 años): https://mley.mx/CFF/articulo/30/
36. IMCP — Normas de Auditoría (adopción de las NIA/ISA en México, sustitución de las NAGAS): https://imcp.org.mx/normas-de-auditoria/
37. IMCP — Principales cambios entre las NAGAS y las NIA: https://imcp.org.mx/principales-cambios-entre-las-normas-de-auditoria-generalmente-aceptadas-en-mexico-antes-del-proceso-de-convergencia-y-las-normas-internacionales-de-auditoria-nias/

**Sin verificar o con verificación parcial en este módulo:**
- La fecha exacta (día) de aprobación final de NIF A-1 por el Consejo Emisor del CINIF: una fuente secundaria indica 24-nov-2022, otra noviembre de 2021; la vigencia (1-ene-2023) sí es consistente entre fuentes.
- El texto íntegro y párrafo exacto de NIF B-2, NIF B-3, NIF B-4, NIF B-6, NIF B-8, NIF C-3, NIF C-6, NIF C-9, NIF C-15, NIF C-19, NIF C-4, NIF D-1, NIF D-2 y NIF D-4: protegido tras el muro de pago del CINIF/IMCP; este módulo se basa en resúmenes técnicos de terceros (boletines de colegios de contadores, firmas y plataformas jurídicas), no en el texto oficial completo párrafo por párrafo como sí se hizo con NIF A-1.
- La fecha exacta (día) del cambio de razón social del CINIF a "y de Sostenibilidad": ubicada en mayo de 2023 por fuente secundaria, sin confirmación contra un comunicado oficial fechado del propio CINIF.
- Si el Proyecto de Mejoras a las NIF 2026 (auscultación del 15-sep-2025, comentarios hasta el 15-oct-2025) fue aprobado en su versión final exactamente como se describe en la auscultación, o si sufrió cambios antes de su entrada en vigor propuesta el 1-ene-2026; se cita como proyecto de auscultación, no como texto definitivo confirmado.
- El método específico ("costo identificado" vs. matices de "costo promedio ponderado vs. móvil") que NIF C-4 detalla para inventarios de proyectos de construcción en curso, más allá de lo confirmado en fuentes secundarias.
- Cifras exactas de tasas de depreciación fiscal por tipo de activo bajo los Arts. 34–35 de la LISR aplicadas al ejemplo de la sección 6 (se citan como referencia general, no verificadas partida por partida contra el texto vigente 2026).
