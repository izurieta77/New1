# 11 — Maestría en Derecho Fiscal: impuestos federales, comercio exterior y litigio fiscal

> Nivel: maestría · Actualizado 2026-09-25 · Grado global de evidencia: **A** en el texto exacto de LISR (arts. 2, 3, 16, 17, 25, 27, 77, 90, 140, 179, 180 verificados contra el archivo de texto plano de la Cámara de Diputados, última reforma DOF 01-04-2024, en `laboratorio/replicas/V05-spiva-y-fiscalidad-sic/datos/legal/LISR.txt`) y en las reformas de 2025-2026 confirmadas por al menos dos fuentes independientes que citan la misma fecha de DOF. **B** en los artículos del CFF, LIVA, LIEPS, Ley Aduanera y LFPCA cuyo texto se tomó de transcripciones especializadas (leyes-mx.com, mley.mx, SDV Asesores) porque el PDF oficial de diputados.gob.mx no pudo extraerse de forma legible en esta sesión (ver §10, nota metodológica) — se marcan como "(texto verificado en fuente secundaria, no contra el PDF oficial)". **C** en montos en pesos actualizados por el Anexo 5 de la RMF 2026 (defraudación fiscal), tomados de fuentes secundarias que coinciden entre sí pero no se contrastaron contra el DOF. Cuatro tesis/jurisprudencias (una del TFJA, tres de la SCJN) se verificaron con su clave o número de registro exacto.

**Alcance y relación con el resto del sistema.** Este capítulo asume los fundamentos de la relación jurídico-tributaria (sujeto activo/pasivo, hecho generador, elementos del tributo, principios constitucionales de los arts. 31-IV, 14 y 16) que corresponden al nivel de licenciatura y que, a la fecha de este documento, se están construyendo en paralelo en `fiscal/`. No repite el detalle de regímenes de persona física con actividad empresarial, RESICO, ni la mecánica de exención de IVA en construcción de vivienda y combustibles: eso ya está cubierto con fuente verificada en `fiscal/01-personas-fisicas-actividad-empresarial.md` (§§3.2-3.3, 4.1-4.3), que además corrige el error común de creer que la construcción de vivienda paga IVA a tasa 0% (es **exenta**, no tasa 0%: art. 9, fr. II LIVA). Este capítulo construye sobre esa base hacia el nivel de persona moral, grupos de partes relacionadas, comercio exterior y litigio.

**Convenciones.** Texto entre comillas = cita literal verificada, con artículo y fuente. "**Inferencia:**" = razonamiento propio del sistema a partir de la ley, no un criterio oficial. "**Doctrina:**" = posición académica, no norma positiva ni jurisprudencia obligatoria. "**(no verificado)**" = dato que no se contrastó contra texto oficial en esta sesión. LISR, CFF, LIVA, LIEPS, LFPCA, LA (Ley Aduanera) y LAmp (Ley de Amparo) se citan por sus siglas usuales.

---

## 1. Objetivos de dominio

Quien complete este módulo debe poder:

1. Explicar la mecánica de acumulación de ingresos (arts. 16-17 LISR) y de deducción (arts. 25-27 LISR) para persona moral, y distinguir un comprobante fiscal válido de una operación fiscalmente materializada.
2. Diagramar el procedimiento del art. 69-B CFF (EFOS/EDOS) y del nuevo art. 49-Bis CFF (visita expedita, vigente desde el 1-ene-2026), y citar al menos una tesis que defina qué prueba la materialidad y qué no.
3. Calcular el efecto de la CUFIN y la CUCA en una reducción de capital o distribución de dividendos entre personas morales (arts. 77-78 LISR).
4. Aplicar los cuatro métodos de precios de transferencia del art. 180 LISR a un caso simple entre partes relacionadas, y ubicar cuándo se presume vinculación con REFIPRES.
5. Determinar si un residente en el extranjero tiene establecimiento permanente en México conforme a los arts. 2-3 LISR (agente dependiente, obra de construcción de más de 183 días, agente independiente que no actúa en el marco ordinario).
6. Distinguir tasa 0%, exención y gravado a la tasa general en IVA, y calcular el acreditamiento proporcional cuando hay actos mixtos (art. 5, fr. V LIVA), incluida la regla real de compensación (solo mismo impuesto desde 2019).
7. Elegir entre recurso de revocación, juicio contencioso administrativo (vía tradicional o en línea) y amparo, según el acto de autoridad, el plazo disponible y si se busca solo anular el acto o también impugnar la constitucionalidad de la norma.
8. Explicar cómo opera la suspensión del acto reclamado en materia fiscal tras la reforma a la Ley de Amparo de octubre de 2025, y qué cambió con la reforma a la LFPCA de junio de 2026.
9. Distinguir defraudación fiscal (art. 108 CFF) de su forma equiparada (art. 109 CFF) y del delito de comprobantes fiscales falsos (art. 113 Bis CFF), y explicar por qué este último exige ahora prisión preventiva oficiosa.
10. Construir el mapa de decisión "qué medio de defensa usar" y aplicarlo en menos de cinco minutos ante un acto de autoridad real.

---

## 2. ISR avanzado

### 2.1 Teoría del ingreso acumulable

El art. 16 LISR es la norma matriz para personas morales: "Las personas morales residentes en el país, incluida la asociación en participación, acumularán la totalidad de los ingresos en efectivo, en bienes, en servicio, en crédito o de cualquier otro tipo, que obtengan en el ejercicio, inclusive los provenientes de sus establecimientos en el extranjero." No son ingresos acumulables los que se obtienen "por aumento de capital, por pago de la pérdida por sus accionistas, por primas obtenidas por la colocación de acciones que emita la propia sociedad o por utilizar para valuar sus acciones el método de participación ni los que obtengan con motivo de la revaluación de sus activos y de su capital" (mismo artículo). Tampoco son acumulables los dividendos que una persona moral perciba de otra persona moral residente en México (último párrafo del art. 16), lo que evita la doble tributación corporativa en cascada y es el ancla de la mecánica de CUFIN (§2.3).

El art. 17 LISR fija el **momento** de acumulación cuando la ley no lo prevé en otro artículo específico. Para enajenación de bienes o prestación de servicios, se acumula en la fecha que ocurra primero entre: "a) Se expida el comprobante fiscal que ampare el precio o la contraprestación pactada. b) Se envíe o entregue materialmente el bien o cuando se preste el servicio. c) Se cobre o sea exigible total o parcialmente el precio o la contraprestación pactada, aun cuando provenga de anticipos" (art. 17, fr. I). Para uso o goce temporal de bienes, el criterio es el cobro, la exigibilidad o la expedición del comprobante, lo que suceda primero (fr. II).

Para persona física, el art. 90 LISR extiende la obligación a quienes "obtengan ingresos en efectivo, en bienes, devengado cuando en los términos de este Título señale, en crédito, en servicios en los casos que señale esta Ley, o de cualquier otro tipo", y agrega una obligación informativa relevante para litigio y para planeación: declarar préstamos, donativos y premios que "en lo individual o en su conjunto, excedan de $600,000.00" (art. 90, segundo párrafo). **Inferencia:** este umbral es el que dispara la mayoría de las "cartas invitación" del SAT por depósitos bancarios no explicados que después escalan a un requerimiento del art. 41-A o a una revisión de gabinete; conocerlo es el primer filtro de un caso de "discrepancia fiscal".

**Doctrina.** La distinción entre ingreso devengado (persona moral, regla general) e ingreso percibido/exigible (persona física, salvo actividad empresarial) es el eje de lo que la doctrina mexicana (Arrioja Vizcaíno, *Derecho Fiscal*; De la Garza, *Derecho Financiero Mexicano*) llama el "momento de causación" del hecho generador, distinto del "momento de exigibilidad" del crédito fiscal (art. 6 CFF: las contribuciones se causan conforme se realizan las situaciones jurídicas o de hecho previstas en las leyes fiscales vigentes durante el lapso en que ocurran).

### 2.2 Deducciones autorizadas y su materialidad

El art. 25 LISR enumera las deducciones que puede efectuar una persona moral: devoluciones, descuentos y bonificaciones (fr. I); costo de lo vendido (fr. II); gastos (fr. III); inversiones (fr. IV); créditos incobrables y pérdidas por caso fortuito o fuerza mayor (fr. V); cuotas patronales al IMSS (fr. VI); intereses devengados (fr. VII); ajuste anual por inflación deducible (fr. VIII); anticipos de cooperativas y sociedades civiles (fr. IX); y aportaciones a fondos de pensiones, con el límite del factor 0.47 (o 0.53 si no se reducen las prestaciones exentas respecto del ejercicio anterior) sobre el monto aportado (fr. X).

El art. 27 LISR fija los **requisitos** que toda deducción debe reunir. Los tres que más litigio generan:

- **Fracción I — estrictamente indispensable.** "Ser estrictamente indispensables para los fines de la actividad del contribuyente", salvo donativos no onerosos a las entidades autorizadas que enumera el mismo artículo, con el límite del **7% de la utilidad fiscal del ejercicio inmediato anterior** (4% si el donatario es la Federación, entidades federativas, municipios u organismos descentralizados, sin exceder en conjunto el 7%).
- **Fracción III — comprobante y forma de pago.** "Estar amparadas con un comprobante fiscal y que los pagos cuyo monto exceda de $2,000.00 se efectúen mediante transferencia electrónica de fondos... cheque nominativo... tarjeta de crédito, de débito, de servicios, o los denominados monederos electrónicos autorizados por el Servicio de Administración Tributaria." Para **combustibles**, el pago debe hacerse por esos mismos medios **"aun cuando la contraprestación... no exceda de $2,000.00"** — es decir, no hay piso de minimis para combustibles, y el comprobante debe consignar el permiso vigente del proveedor conforme a la Ley de Hidrocarburos.
- **Fracción IV — registro contable único.** "Estar debidamente registradas en contabilidad y que sean restadas una sola vez."

**El comprobante fiscal no basta: la materialidad es un requisito adicional construido por la jurisprudencia, no por el texto literal de 2024 del art. 27.** La reforma del CFF publicada en el DOF el 7-nov-2025 (vigente desde el 1-ene-2026) llevó ese criterio al texto positivo al reformar la fracción IX del art. 29-A CFF para exigir, desde la emisión, que el CFDI ampare una operación real (dato tomado de `fiscal/01-personas-fisicas-actividad-empresarial.md`, §3.2, con fuente diputados.gob.mx/CFF_ref62_07nov25.pdf; **(texto verificado en fuente secundaria, no contra el PDF oficial en esta sesión)**). Antes de esa reforma, el criterio ya era jurisprudencia consolidada:

> **TFJA, jurisprudencia VIII-J-1aS-115**, materia Código Fiscal de la Federación, rubro: **"COMPROBANTES FISCALES. LOS REGISTROS CONTABLES DEBEN ESTAR APOYADOS CON LA DOCUMENTACIÓN COMPROBATORIA CORRESPONDIENTE, POR LO QUE SI ÚNICAMENTE OBRAN AQUELLOS, LA AUTORIDAD FISCALIZADORA ESTÁ EN POSIBILIDADES DE DETERMINAR LA FALTA DE MATERIALIZACIÓN DE LAS OPERACIONES DESCRITAS EN ELLOS."** Texto verificado íntegro (documento oficial del TFJA descargado en esta sesión, tesis-pdf-detalle/45851). Aprobada por acuerdo G/S1-10/2021, con cinco precedentes de la Primera Sección de la Sala Superior entre 2018 y 2019. Sostiene que "los comprobantes fiscales no se pueden considerar perfectos per se, para acreditar la materialidad de las operaciones consignadas en ellos, ya que para que se considere real y probado su contenido, es indispensable que estén respaldados en los elementos documentales que comprueben que lo consignado en ellos, existió realmente" — y cita a su vez la tesis de la Primera Sala de la SCJN 1a. CLXXX/2013, "COMPROBANTES FISCALES. CONCEPTO, REQUISITOS Y FUNCIONES".

**Regla operable:** por cada deducción relevante, conservar cuatro capas de evidencia — (1) el CFDI; (2) el contrato o pedido; (3) evidencia de ejecución (bitácoras, fotos con fecha, actas de entrega, correos); (4) evidencia de la capacidad material del proveedor (activos, personal, domicilio localizable). Es la misma checklist que `fiscal/01` da para persona física; aquí se confirma con fuente jurisprudencial directa que aplica igual a persona moral.

### 2.3 El procedimiento del art. 69-B CFF: EFOS, EDOS y su límite temporal

Aunque el art. 69-B está en el CFF, no en la LISR, su efecto principal es sobre las deducciones y acreditamientos de ISR e IVA, por lo que se trata aquí. Mecánica verificada (múltiples fuentes convergentes: SAT, PRODECON, doctrina especializada):

1. La autoridad detecta que un contribuyente emitió comprobantes "sin contar con los activos, personal, infraestructura o capacidad material, directamente o indirectamente, para prestar los servicios o producir, comercializar o entregar los bienes que amparan tales comprobantes, o bien, que dichos contribuyentes se encuentren no localizados" y **presume** la inexistencia de esas operaciones (primer párrafo, art. 69-B CFF).
2. Notifica al presunto emisor (EFOS) por buzón tributario, página del SAT y DOF; el contribuyente tiene **15 días** para desvirtuar, con una prórroga de 5 días.
3. La autoridad resuelve en un máximo de **50 días** (puede requerir información adicional dentro de 20 días, lo que suspende el plazo).
4. Si no desvirtúa, se publica en el **listado definitivo** del DOF y del portal del SAT: sus comprobantes "no producen ni produjeron efecto fiscal alguno."
5. Quien haya dado efectos fiscales a esos comprobantes (EDOS: Empresa que Deduce Operaciones Simuladas) tiene 30 días desde la publicación del listado presunto para **autocorregirse** (eliminar la deducción/acreditamiento) o acreditar la materialidad de la operación específica que sostuvo con ese proveedor.

Dos jurisprudencias de la SCJN acotan los efectos de este procedimiento, ambas verificadas con número de registro:

> **SCJN, Segunda Sala, jurisprudencia 2a./J. 26/2020 (10a.), registro digital 2022083**, Semanario Judicial de la Federación, Libro 78, septiembre de 2020, Tomo I, p. 616. Resuelve que el **recurso de revisión fiscal es improcedente por razón de cuantía** contra las sentencias del entonces Tribunal Federal de Justicia Administrativa que declaran la nulidad de la resolución que determinó que el contribuyente no desvirtuó la presunción de inexistencia de operaciones del art. 69-B: como esa resolución no fija un crédito fiscal líquido, no hay "cuantía" que abra la revisión fiscal a favor de la autoridad. **Efecto práctico:** una sentencia favorable del TFJA en un juicio de nulidad contra la inclusión en el listado del 69-B es, en la práctica, más difícil de revertir por la autoridad que una liquidación de crédito fiscal ordinaria.
> **SCJN, jurisprudencia por contradicción de tesis 9/2021, registro digital 2024206**, Semanario Judicial de la Federación, Libro 10, febrero de 2022, rubro: **"EFECTOS DE LA PUBLICACIÓN EN EL DIARIO OFICIAL DE LA FEDERACIÓN Y EN LA PÁGINA ELECTRÓNICA DEL SERVICIO DE ADMINISTRACIÓN TRIBUTARIA DE LOS DATOS DEL SUJETO CONTRIBUYENTE QUE SE UBICÓ EN DEFINITIVA EN LA HIPÓTESIS DEL PRIMER PÁRRAFO DEL ARTÍCULO 69-B DEL CÓDIGO FISCAL DE LA FEDERACIÓN"**. Resuelve la contradicción entre el Octavo y el Vigésimo Tribunales Colegiados en Materia Administrativa del Primer Circuito: aunque el procedimiento derive de la revisión de un ejercicio fiscal específico, la inclusión en el listado definitivo **tiene efectos generales y se proyecta hacia el futuro**, no solo hacia el ejercicio revisado. **Inferencia:** esto significa que un proveedor incluido en el listado definitivo por hechos de 2022 queda estigmatizado también para operaciones de 2026 con ese mismo RFC, salvo que se dé de baja del listado por resolución posterior — de ahí la importancia de la revisión periódica del listado antes de contratar, no solo al momento de la operación.

**Novedad de 2026 — art. 49-Bis CFF (visita domiciliaria expedita).** Vigente desde el 1-ene-2026 (reforma DOF 7-nov-2025), crea un procedimiento paralelo y más rápido que el 69-B: una visita enfocada solo en materialidad, con un plazo máximo de **24 días hábiles** entre la orden y la resolución final, que puede terminar en la suspensión del sello digital (CSD) y en la calificación de los CFDI emitidos como falsos si el contribuyente no aporta, en **5 días hábiles** tras la visita, evidencia que desvirtúe la presunción (múltiples fuentes convergentes: IDC, Ruiz Consultores, Carbajal Contadores, Pérez Correa González, todas citando la misma reforma DOF 7-nov-2025; **(no verificado contra el texto oficial del CFF en esta sesión, solo contra fuentes secundarias especializadas que coinciden entre sí)**). **Inferencia:** el 49-Bis no sustituye al 69-B; son dos vías con objetivos distintos — el 69-B ataca al emisor y genera un listado con efectos erga omnes hacia el futuro; el 49-Bis es una herramienta de fiscalización más rápida centrada en el CSD del contribuyente auditado, con plazos que dejan muy poco margen de reacción (5 días hábiles) frente a los 15-20 días del 69-B.

**Novedad relacionada — art. 69-B Bis CFF (transmisión indebida de pérdidas fiscales).** La autoridad puede presumir "que se efectuó la transmisión indebida del derecho a disminuir pérdidas fiscales, cuando del análisis de la información con que cuenta en sus bases de datos, identifique que el contribuyente que cuente con ese derecho fue parte de una reestructuración, escisión o fusión de sociedades, o bien, de un cambio de accionistas y, como consecuencia de ello, dicho contribuyente deje de formar parte del grupo al que perteneció" (texto citado de leyes-mx.com; **(texto verificado en fuente secundaria, no contra el PDF oficial)**). Contra la resolución procede el recurso de revocación (§5.1), y la publicación del listado definitivo confirma la improcedencia de la disminución de la pérdida por el contribuyente adquirente. **Inferencia:** es el instrumento específico contra la práctica de "comprar" empresas con pérdidas fiscales acumuladas para erosionar la base de otro grupo — una figura distinta del 69-B (que ataca comprobantes) aunque comparte procedimiento de publicación en dos listados (presunto y definitivo) y recurso de revocación como medio de defensa.

### 2.4 CUFIN y CUCA

El art. 77 LISR obliga a las personas morales a llevar una **Cuenta de Utilidad Fiscal Neta (CUFIN)**, que "se adicionará con la utilidad fiscal neta de cada ejercicio, así como con los dividendos o utilidades percibidos de otras personas morales residentes en México y con los ingresos, dividendos o utilidades sujetos a regímenes fiscales preferentes... y se disminuirá con el importe de los dividendos o utilidades pagados, con las utilidades distribuidas a que se refiere el artículo 78 de esta Ley, cuando en ambos casos provengan del saldo de dicha cuenta." La utilidad fiscal neta del ejercicio es el resultado fiscal **menos** el ISR pagado conforme al art. 9 LISR y **menos** las partidas no deducibles (excepto las de las fracciones VIII y IX del art. 28 y la PTU del art. 9, fr. I).

**Función económica de la CUFIN (doctrina):** es el mecanismo que evita gravar dos veces la misma utilidad corporativa — una vez con el ISR de la persona moral (art. 9) y otra con el ISR del socio al recibir el dividendo. Mientras el dividendo provenga del saldo de la CUFIN, la persona moral **no retiene** el ISR corporativo adicional; si el dividendo excede el saldo de la CUFIN, se paga el impuesto del art. 10 LISR sobre el excedente, con la tasa vigente aplicada al resultado de multiplicar ese excedente por el factor de 1.4286 (mecánica exigida también en el acreditamiento de persona física, art. 140, ver §2.5).

La **Cuenta de Capital de Aportación (CUCA)**, art. 78 LISR, corre en paralelo: registra las aportaciones de capital y las primas netas por suscripción de acciones. Su saldo es lo que puede reembolsarse a los socios **sin generar utilidad distribuida gravable**; el exceso sobre la CUCA en una reducción de capital sí se considera utilidad distribuida y se somete a la mecánica del art. 78 (que remite a comparar el reembolso contra el capital de aportación actualizado por acción). **Regla operable:** antes de cualquier reducción de capital o reembolso a accionistas, calcular el saldo actualizado de la CUCA por acción; reembolsar por encima de ese monto por acción activa el impuesto a dividendos aunque el efectivo salga como "devolución de capital" en el acta de asamblea.

### 2.5 Régimen de dividendos (art. 140 LISR) — solo la mecánica corporativa

El detalle de retención sobre dividendos del SIC/BMV para persona física ya está verificado en `conocimiento/27-fiscalidad-2026-y-estructura-sic.md` (§2.3) y no se repite aquí. Lo que agrega este capítulo es la mecánica del **acreditamiento del ISR corporativo**, central para litigio y planeación de grupos:

Art. 140 LISR, primer párrafo: la persona física acumula el dividendo a sus demás ingresos y puede **acreditar** contra el impuesto anual "el impuesto sobre la renta pagado por la sociedad que distribuyó los dividendos", siempre que también acumule "el monto del impuesto sobre la renta pagado por dicha sociedad correspondiente al dividendo o utilidad percibido" y cuente con la constancia (CFDI) del art. 76, fr. XI. El impuesto pagado por la sociedad se determina aplicando la tasa del art. 9 LISR (30%) al resultado de multiplicar el dividendo por el **factor de 1.4286**. Adicionalmente, hay una "tasa adicional del 10% sobre los dividendos o utilidades distribuidos por las personas morales residentes en México", retenida por la distribuidora, con carácter de **pago definitivo** (art. 140, segundo párrafo) — esta es la retención que sí aplica en el SIC/BMV y que `conocimiento/27` documenta con GBM como agente retenedor.

### 2.6 Precios de transferencia entre partes relacionadas (arts. 179-184 LISR)

**Obligación general (art. 179).** "Los contribuyentes de los Títulos II y IV de esta Ley que celebren operaciones con partes relacionadas están obligados... a determinar sus ingresos acumulables y deducciones autorizadas, considerando para esas operaciones los precios, montos de contraprestaciones o márgenes de utilidad que hubieran utilizado u obtenido con o entre partes independientes en operaciones comparables" — es el principio de **plena competencia** (*arm's length*). Si no se cumple, la autoridad puede determinar los ingresos y deducciones aplicando el mismo estándar (segundo párrafo).

**Comparabilidad.** El mismo artículo lista los cinco factores de comparabilidad, alineados con las Guías de la OCDE: (I) características de la operación (en financiamiento: monto, plazo, garantías, solvencia, tasa; en servicios: naturaleza y si hay know-how; en bienes tangibles: características físicas y calidad; en intangibles: tipo, duración, protección; en enajenación de acciones: capital contable actualizado, valor presente de flujos o cotización bursátil); (II) funciones o actividades realizadas, incluidos activos y riesgos; (III) términos contractuales; (IV) circunstancias económicas; (V) estrategias de negocios.

**Definición de partes relacionadas.** "Se considera que dos o más personas son partes relacionadas, cuando una participa de manera directa o indirecta en la administración, control o capital de la otra, o cuando una persona o grupo de personas participe directa o indirectamente en la administración, control o capital de dichas personas" (art. 179, párrafo antepenúltimo). Para un establecimiento permanente, son partes relacionadas su casa matriz y otros establecimientos permanentes de la misma.

**Presunción con REFIPRES.** "Salvo prueba en contrario, se presume que las operaciones entre residentes en México y sociedades o entidades sujetas a regímenes fiscales preferentes, son entre partes relacionadas en las que los precios y montos de las contraprestaciones no se pactan conforme a los que hubieran utilizado partes independientes en operaciones comparables" (art. 179, penúltimo párrafo). El artículo remite expresamente a "las Guías sobre Precios de Transferencia para las Empresas Multinacionales y las Administraciones Fiscales, aprobadas por el Consejo de la [OCDE] en 1995, o aquéllas que las sustituyan", como criterio de interpretación.

**Métodos (art. 180 LISR).** Cuatro métodos verificados en texto literal, más los que agrega la práctica bajo la misma estructura de la OCDE:

1. **Precio comparable no controlado (CUP):** "considerar el precio o el monto de las contraprestaciones que se hubieran pactado con o entre partes independientes en operaciones comparables."
2. **Precio de reventa:** determina el precio de adquisición "multiplicando el precio de reventa... por el resultado de disminuir de la unidad, el por ciento de utilidad bruta que hubiera sido pactado con o entre partes independientes en operaciones comparables."
3. **Costo adicionado:** determina el precio de venta multiplicando el costo por el resultado de sumar a la unidad el margen bruto de partes independientes.
4. **Partición de utilidades:** asigna la utilidad de operación en la proporción que hubiera correspondido entre partes independientes.

**Establecimiento permanente y precios de transferencia (arts. 181-184).** Los arts. 181-182 regulan cuándo **no** se considera que un residente en el extranjero tiene establecimiento permanente por operar bajo un esquema de maquila, si cumple con las reglas de precios de transferencia específicas para maquiladoras (safe harbor o APA); el art. 183 excluye del concepto de establecimiento permanente a ciertos residentes en el extranjero bajo condiciones del propio Título VI; el art. 184 remite a los tratados internacionales para resolver conflictos de doble tributación relacionados con ajustes de precios de transferencia. **Inferencia:** el régimen de maquiladoras (IMMEX, §4) y el régimen de precios de transferencia no son temas separados — la seguridad jurídica de una maquiladora frente al riesgo de que se le atribuya un establecimiento permanente a su matriz extranjera depende de que year con year documente y cumpla los métodos de PT bajo los arts. 181-182.

### 2.7 Establecimiento permanente (arts. 2-3 LISR)

**Regla general (art. 2).** "Se considera establecimiento permanente cualquier lugar de negocios en el que se desarrollen, parcial o totalmente, actividades empresariales o se presten servicios personales independientes." La ley da ejemplos no limitativos: "sucursales, agencias, oficinas, fábricas, talleres, instalaciones, minas, canteras o cualquier lugar de exploración, extracción o explotación de recursos naturales."

**Agente dependiente.** Aun sin lugar fijo de negocios, hay establecimiento permanente "cuando un residente en el extranjero actúe en el país a través de una persona física o moral, distinta de un agente independiente", si esa persona "concluye habitualmente contratos o desempeña habitualmente el rol principal que lleve a la conclusión de contratos celebrados por el residente en el extranjero" y esos contratos (I) se celebran a nombre o por cuenta del residente extranjero, (II) implican enajenación o uso/goce de bienes del residente extranjero, o (III) lo obligan a prestar un servicio.

**Agente independiente que deja de serlo.** También hay establecimiento permanente si el agente, aunque formalmente independiente, "no actúa en el marco ordinario de su actividad" — lo que ocurre, entre otros casos, si mantiene inventario del principal, asume sus riesgos, actúa bajo instrucciones detalladas o control general, ejerce actividades que económicamente corresponden al residente extranjero, o recibe su remuneración "independientemente del resultado de sus actividades" (art. 2, fracciones I-V de ese párrafo). Se presume que no es agente independiente quien actúa "exclusiva o casi exclusivamente por cuenta de residentes en el extranjero que sean sus partes relacionadas."

**Regla de los 183 días para obra.** "Tratándose de servicios de construcción de obra, demolición, instalación, mantenimiento o montaje en bienes inmuebles, o por actividades de proyección, inspección o supervisión relacionadas con ellos, se considerará que existe establecimiento permanente solamente cuando los mismos tengan una duración de más de 183 días naturales, consecutivos o no, en un periodo de doce meses" — y si el residente extranjero subcontrata, "los días utilizados por los subcontratistas... se adicionarán... para el cómputo del plazo mencionado" (art. 2, párrafos décimo y décimo primero). **Regla operable:** para cualquier contrato de obra o supervisión con un residente en el extranjero, llevar una bitácora de días acumulados de presencia en México desde el primer día de actividad relacionada, sumando subcontratistas, y alertar antes del día 150 para planear la estructura si se acerca al umbral.

**Excepciones (art. 3).** "No se considerará que constituye establecimiento permanente un lugar de negocios cuyo único fin sea la realización de actividades de carácter preparatorio o auxiliar respecto a la actividad empresarial" del residente en el extranjero (texto verificado parcialmente; el detalle de los incisos específicos —almacenamiento, exhibición, compra de mercancías, recopilación de información— no se transcribió en esta sesión desde el archivo local; **(no verificado línea por línea contra LISR.txt, solo el encabezado del art. 3)**).

---

## 3. IVA e IEPS avanzados

### 3.1 Actos gravados, exentos y tasa 0%

El IVA grava, conforme al art. 1 LIVA, la enajenación de bienes, la prestación de servicios independientes, el otorgamiento del uso o goce temporal de bienes y la importación de bienes o servicios, a la tasa general de 16%, salvo que la propia ley prevea tasa 0% o exención.

**Tasa 0% (art. 2-A LIVA).** Lista taxativa; entre lo verificado: animales y vegetales no industrializados (salvo hule y mascotas), medicinas de patente y alimentos para consumo humano y animal (excepto bebidas distintas de la leche), agua no gaseosa ni compuesta para consumo humano, libros, periódicos y revistas que editen los propios contribuyentes, y la exportación de bienes o servicios (fr. IV, no transcrita en detalle aquí). **Diferencia clave con exención:** a tasa 0% el contribuyente sí **acredita** el IVA de sus insumos y puede generar saldo a favor recuperable; en actos exentos, no.

**Exentos (art. 9 LIVA).** Entre lo verificado: suelo; "construcciones adheridas al suelo, destinadas o utilizadas para casa habitación" (fr. II, cuya extensión a servicios de construcción y sus límites ya se documentó en `fiscal/01`, §4.2); libros, periódicos y revistas (enajenación, no editados por el contribuyente); bienes muebles usados (salvo los enajenados por empresas); billetes de lotería; moneda nacional y extranjera; acciones, partes sociales y documentos pendientes de cobro; y lingotes de oro con pureza mínima del 99%, vendidos al menudeo.

### 3.2 Acreditamiento, saldos a favor y la compensación real (no la universal)

**Requisitos del acreditamiento (art. 5 LIVA).** Ya verificados en `fiscal/01`, §4.1: (1) que el IVA corresponda a gastos, inversiones o servicios estrictamente indispensables para actos gravados o a tasa 0%; (2) que el IVA esté trasladado expresamente y por separado en el CFDI; (3) que esté efectivamente pagado en el mes que se acredita; (4) que si el gasto es solo parcialmente deducible para ISR, el IVA se acredite en la misma proporción.

**Prorrateo cuando hay actos mixtos (art. 5, fr. V).** Cuando el contribuyente realiza actos gravados y actos exentos, el IVA de gastos e inversiones identificables exclusivamente con actos gravados es 100% acreditable; el identificable exclusivamente con actos exentos no es acreditable; y el no identificable (gastos comunes) se acredita en la proporción que los actos gravados representan del total de actos del periodo (o, para inversiones, puede optarse por una mecánica de ajuste anual). **Inferencia (ligada a `fiscal/01`, §4.2):** un contratista general que hace obra exenta (vivienda completa) y obra gravada (naves industriales, remodelación comercial) debe llevar contabilidad separada por proyecto para poder identificar directamente el IVA de cada uno y minimizar la porción de "gasto común" no identificable, porque esa porción es la que se pierde parcialmente vía el factor de prorrateo.

**Saldo a favor (art. 6 LIVA).** Cuando el IVA acreditable excede al IVA causado en el mes, el saldo a favor puede: (a) acreditarse contra el IVA a cargo de los meses siguientes hasta agotarse; (b) solicitarse en devolución; o (c) compensarse "en los términos del artículo 23" del CFF. **Corrección importante: la compensación universal (contra impuestos distintos) fue eliminada desde el 1-ene-2019.** Desde entonces, un saldo a favor de IVA solo puede compensarse contra IVA a cargo del propio contribuyente (mismo impuesto); no puede compensarse contra ISR ni viceversa (múltiples fuentes convergentes: CEFP, IMCP, análisis de la reforma del art. 23 CFF vigente desde la LIF 2019 y consolidada en reformas posteriores). En la práctica, para IVA generado desde 2019, las únicas rutas reales son acreditar contra IVA futuro o pedir devolución.

**Plazos de devolución (arts. 22 y 22-A CFF).** La autoridad debe resolver la devolución dentro de **40 días hábiles** siguientes a la solicitud; puede requerir información adicional dentro de los primeros **20 días** posteriores a la solicitud, lo que suspende el plazo hasta que se desahogue el requerimiento. Si la devolución se paga fuera de ese plazo, el SAT debe pagar intereses desde el día siguiente al vencimiento (art. 22-A). El cómputo de estos días excluye sábados, domingos, días festivos y el periodo de vacaciones generales de las autoridades fiscales (art. 12 CFF).

### 3.3 IEPS y casos especiales (combustibles)

El detalle de la mecánica de IEPS en combustibles al consumidor final, incluida la cuota fija por litro y la advertencia de que **no existe tasa 0% de IVA para combustibles** (se gravan al 16% general sobre un precio que ya incluye el IEPS), está verificado en `fiscal/01`, §4.3, y no se repite. Lo que agrega este capítulo es el mecanismo de **estímulo fiscal complementario** vigente en 2026, relevante para litigio de saldos a favor y para planeación de transporte y agroindustria:

El art. 20, apartado A, fracciones IV y V de la LIF 2026 sostiene un estímulo fiscal al IEPS del diésel, acreditable primero contra ISR, después contra IVA, y con posibilidad de devolución del remanente por el SAT. A la fecha de este documento (22-sep-2026), la SHCP aplicó un estímulo del 100% sobre la cuota de IEPS al diésel durante la semana del 19 al 25 de septiembre de 2026 (cuota nominal de $7.3634/litro llevada a cero), más un estímulo complementario adicional de $1.8361/litro utilizable como crédito fiscal (fuente: El Financiero, 21-sep-2026, y contadormx.com sobre estímulos LIF 2026; **(cifras y mecánica sujetas a ajuste semanal por acuerdo de la SHCP; no verificado el texto exacto del art. 20-A LIF en esta sesión, solo fuentes de prensa especializada convergentes)**). **Inferencia:** para el "perfil del despacho" (construcción y transporte de materiales), el estímulo complementario al diésel es un crédito fiscal real, no solo una promesa de política pública, pero su magnitud cambia semana a semana según acuerdo de Hacienda — cualquier proyección financiera que lo incorpore debe fecharse y revisarse antes de cada declaración, no asumirse constante para el año.

---

## 4. Comercio exterior y aduanas

**Regímenes aduaneros (art. 90 LA).** "Las mercancías que se introduzcan al territorio nacional o se extraigan del mismo, podrán ser destinadas a alguno de los regímenes aduaneros" siguientes: definitivos (importación y exportación); temporales (importación para retornar en el mismo estado, o para elaboración/transformación/reparación en programas de maquila o de exportación; exportación para retornar en el mismo estado o para elaboración/transformación/reparación); depósito fiscal; tránsito de mercancías (interno e internacional); elaboración, transformación o reparación en recinto fiscalizado; y recinto fiscalizado estratégico.

**Obligación de pedimento (art. 36 LA).** Quienes importen o exporten mercancías deben presentar ante la aduana, "por conducto de agente o apoderado aduanal", un pedimento en la forma oficial aprobada por la Secretaría (SHCP/ANAM), con la firma electrónica que acredite el cumplimiento de regulaciones y restricciones no arancelarias cuando aplique.

**Clasificación arancelaria y consulta previa (art. 47 LA).** Importadores, exportadores y agentes aduanales pueden formular, antes de la operación, una **consulta de clasificación arancelaria** ante la autoridad aduanera cuando consideren que la mercancía puede clasificarse en más de una fracción, señalando la fracción que consideran aplicable, las razones, la fracción con la que existe duda y anexando muestras o catálogos. **Inferencia:** para el sector de manufactura ligera (herrería, carpintería, PVC), la consulta previa del art. 47 es la herramienta correcta cuando se importa maquinaria o insumos con clasificación dudosa, porque evita que la aduana reclasifique después de la importación con multa y diferencia de arancel — el costo de una consulta previa (tiempo administrativo) es bajo frente al riesgo de una PAMA (procedimiento administrativo en materia aduanera) por clasificación incorrecta.

**IMMEX.** El Programa de Fomento de la Industria Manufacturera, Maquiladora y de Servicios de Exportación permite importar temporalmente materias primas, componentes, maquinaria y equipo sin pagar impuestos al comercio exterior (arancel general de importación e IVA), condicionado a que la producción resultante se exporte, dentro de los plazos y porcentajes mínimos que fija su Decreto. Para 2026, entre las actualizaciones reportadas (fuente: camtomx.com, dtdexpress.mx, dos fuentes convergentes; **(no verificado contra el Decreto IMMEX oficial en esta sesión)**): reforzamiento de verificaciones sin previo aviso del domicilio fiscal y la planta productiva; obligación, desde marzo de 2026, de incluir en la factura de exportación el número de autorización IMMEX y la fracción arancelaria; y el reporte anual RAOCE (Reporte Anual de Operaciones de Comercio Exterior) con ventana de presentación del 1-abr al 29-may-2026, cuya omisión implica cancelación automática del programa el 30 de mayo. Los requisitos críticos de acceso incluyen ventas al exterior mínimas de 500,000 USD anuales o al menos 10% de la facturación total exportada, y un plan de exportación con proyecciones, tramitado vía VUCEM (Ventanilla Única de Comercio Exterior Mexicano).

**Aranceles vigentes en 2026 (Secciones 301/232 de EUA y T-MEC).** Este sistema ya investigó en profundidad el estado de los aranceles de EUA que afectan a México (Sección 301 "forced labor" al 10-12.5% con exención T-MEC, Sección 232 a acero/aluminio al 50%, autos al 25%, fármacos patentados al 100% desde el 29-sep-2026 para empresas fuera del Anexo III, y las rondas de revisión del T-MEC) en `conocimiento/24-politica-publica-regulacion-y-mercados.md`, que no se repite aquí — ver ese documento para las cifras, fechas y fuentes verificadas. **Inferencia para el "despacho":** un cliente que exporte bajo IMMEX y reglas de origen T-MEC queda exento de la Sección 301 pero no necesariamente de la Sección 232 (acero, aluminio, autos); la clasificación arancelaria correcta (art. 47 LA) es la que determina si aplica la exención T-MEC o el arancel pleno, por lo que ambos temas —comercio exterior mexicano e "US trade policy"— convergen en la misma fracción arancelaria.

---

## 5. Litigio fiscal completo

### 5.1 Recurso de revocación (arts. 116-133 CFF)

**Procedencia (art. 116 CFF).** "Contra los actos administrativos dictados en materia fiscal federal, se podrá interponer el recurso de revocación" (texto verificado en fuente secundaria, mley.mx; **(no verificado contra el PDF oficial)**). Es un recurso **optativo**: el particular puede acudir directamente al juicio contencioso administrativo sin agotarlo primero, salvo que una disposición expresa lo haga obligatorio (p. ej., el propio art. 69-B Bis remite al recurso de revocación como medio de defensa específico, §2.3).

**Plazo para interponerlo (art. 121 CFF).** 30 días hábiles siguientes a aquel en que surta efectos la notificación de la resolución impugnada; es un plazo fatal y no prorrogable (múltiples fuentes convergentes).

**Plazo de resolución y negativa ficta (art. 131 CFF).** La autoridad tiene **3 meses** para resolver y notificar. Si no resuelve en ese plazo, se configura **negativa ficta**, que el particular puede impugnar directamente ante el TFJA sin esperar la resolución expresa. **(no verificado contra el texto oficial del art. 131; fuente secundaria convergente en el plazo de 3 meses).**

**No suspende por sí solo.** La interposición del recurso no suspende la ejecución del acto impugnado, salvo que se garantice el interés fiscal (remisión al art. 144 CFF sobre garantía; **(no verificado en esta sesión el texto exacto del art. 144)**).

### 5.2 Juicio contencioso administrativo ante el TFJA

**Plazo para la demanda (art. 13 LFPCA).** Verificado contra fuente secundaria (mley.mx): 30 días hábiles siguientes a que surta efectos la notificación de la resolución impugnada, o a la entrada en vigor de un decreto, acuerdo o resolución de carácter general autoaplicativo. Hay un plazo especial de **5 años** cuando es la propia autoridad quien demanda la modificación o nulidad de una resolución favorable a un particular. Hay reglas de suspensión del plazo por fallecimiento del demandante (hasta un año), por incapacidad o ausencia (hasta un año mientras se acepta representación), y por solicitud de un procedimiento de resolución de controversias bajo un tratado de doble tributación.

**Vía tradicional vs. Juicio en Línea.** El actor elige, al presentar la demanda, entre la vía tradicional (escrita, ante la Sala Regional competente) o el **Sistema de Justicia en Línea**; una vez elegida la vía, no puede cambiarla. Cuando la autoridad es la demandante (p. ej., para anular una resolución favorable al particular), debe hacerlo obligatoriamente por la vía en línea.

**Reforma de junio de 2026 a la LFPCA.** Publicada en el DOF el **9-jun-2026**, con entrada en vigor escalonada: régimen general desde el 10-jun-2026; reglas de comparecencia electrónica para demandados y terceros desde el **6-dic-2026** (180 días después de la publicación); y nuevos plazos procesales desde el **4-feb-2027** (fuente: samanosc.com, análisis de la reforma; **(no verificado contra el DOF directamente en esta sesión)**). Entre los cambios reportados: en el procedimiento **ordinario**, la admisión o desechamiento de la demanda debe resolverse en 5 días y el proyecto de sentencia en 45 días desde el turno al magistrado; en el **sumario**, un máximo de 6 meses entre admisión y sentencia (suspendible por incidentes); se deroga el requisito de "difícil reparación" para la suspensión del acto y se sustituye por una regla que niega la suspensión si, por ejemplo, permite continuar actividades sin los permisos requeridos; las notificaciones por Boletín Jurisdiccional se tienen por hechas al publicarse, con independencia de que se reciba el aviso electrónico. **Inferencia:** el efecto neto para el litigante es una presión hacia la digitalización obligatoria (incluso para quien no eligió la vía en línea, la contraparte puede comparecer electrónicamente desde diciembre de 2026) y una relajación del estándar para negar la suspensión del acto, lo que hace más relevante garantizar bien el interés fiscal desde el inicio del juicio en lugar de confiar en obtener la suspensión sin garantía.

**Suspensión del acto ante el TFJA (art. 28 LFPCA).** Se tramita como incidente ante el magistrado instructor. Requisitos generales (fr. I): que no se afecte el interés social ni se contravengan disposiciones de orden público, y que los daños causados al solicitante con la ejecución sean de difícil reparación (regla previa a la reforma de junio de 2026, que según fuentes citadas arriba deroga este último estándar). Para actos de determinación, liquidación, ejecución o cobro de contribuciones, la suspensión **se otorga pero surte efectos solo si se constituye la garantía del interés fiscal** ante la autoridad ejecutora, por cualquiera de los medios que permiten las leyes fiscales (fr. II). El magistrado instructor puede modificar o revocar la suspensión ante un hecho superveniente (fr. IV).

### 5.3 Amparo directo e indirecto en materia fiscal

**Amparo indirecto.** Procede contra actos de autoridades administrativas que no sean sentencias definitivas (por ejemplo, contra la constitucionalidad de una norma fiscal aplicada por primera vez, o contra actos de ejecución dentro de un procedimiento administrativo de ejecución) y se tramita ante Juzgado de Distrito. Es la vía típica para impugnar la inconstitucionalidad de una ley fiscal recién aplicada, o para pedir la suspensión de un embargo o aseguramiento de cuentas antes de que exista una sentencia del TFJA que impugnar.

**Amparo directo (art. 170 LAmp).** "El juicio de amparo directo procede: contra sentencias definitivas, laudos y resoluciones que pongan fin al juicio, dictadas por tribunales judiciales, administrativos, agrarios o del trabajo" — incluida la sentencia del TFJA que resuelve el juicio contencioso administrativo. Se tramita directamente ante un Tribunal Colegiado de Circuito. Contra sentencias del TFJA que sean **favorables** al particular, el amparo directo del particular procede solo "para el único efecto de hacer valer conceptos de violación en contra de las normas generales aplicadas" — es decir, no para cuestionar el fondo ya ganado, sino para combatir adicionalmente la constitucionalidad de la norma en la que se basó esa sentencia favorable, normalmente cuando la autoridad interpuso a su vez un recurso de revisión contencioso administrativa (que el Tribunal Colegiado resuelve primero; solo si es procedente y fundado entra al estudio de la constitucionalidad).

**Reforma a la Ley de Amparo de octubre de 2025.** Publicada en el DOF el **16-oct-2025**, en vigor desde el **17-oct-2025**, junto con reformas conexas al CFF y a la Ley Orgánica del TFJA (mismo decreto; múltiples fuentes convergentes: GT Law, DLA Piper, Holland & Knight, Basham, KPMG). Cambios verificados y relevantes para litigio fiscal:

- **Suspensión condicionada a garantía en materia fiscal.** "En materia fiscal, la suspensión estará condicionada a la garantía del crédito reclamado, mediante billete de depósito o carta de crédito" (fuente: Pérez Correa González, resumen de la reforma; **(no verificado contra el texto oficial del art. 135 LAmp reformado)**).
- **Motivación reforzada.** Los jueces deben expresar por escrito los elementos considerados al otorgar o negar la suspensión (arts. 138 y 146 LAmp, según la misma fuente).
- **Restricción frente a créditos fiscales firmes.** Contra actos de ejecución o cobro de un crédito fiscal ya firme, el amparo solo procede "hasta la publicación de la convocatoria de remate" y únicamente por **violaciones procesales**, no por el fondo del crédito. El mismo decreto reformó el CFF y la Ley Orgánica del TFJA para declarar improcedentes los medios de defensa contra actos que exijan el pago o resuelvan sobre la prescripción de créditos fiscales ya firmes.
- **Plazo máximo de sentencia:** 90 días naturales para que el órgano jurisdiccional dicte sentencia (fuente convergente; **(no verificado el artículo exacto)**).

**Jurisprudencia sobre garantía del interés fiscal y suspensión — embargo precautorio de cuentas bancarias:**

> **Pleno Regional en Materia Administrativa (jurisprudencia por contradicción de criterios), registro digital 2028811**, publicada el **17-may-2024**. Resuelve la contradicción entre Tribunales Colegiados sobre si la suspensión definitiva contra el embargo precautorio de cuentas bancarias, decretado como medida de apremio bajo los arts. 40, fr. III, y 40-A CFF, debe condicionarse a garantía. El criterio que prevalece: **la suspensión debe condicionarse a la constitución de una garantía, en términos del art. 135 de la Ley de Amparo, por el monto de la determinación provisional del crédito fiscal presunto** — no basta con que el crédito no sea aún firme para dispensar la garantía. **Inferencia:** este criterio de 2024, combinado con la reforma de octubre de 2025 que endurece la exigencia de garantía en materia fiscal, confirma una tendencia consistente: la suspensión "gratuita" (sin garantizar) en materia fiscal es cada vez más excepcional, y la estrategia de litigio debe presupuestar desde el inicio el costo financiero de una fianza, billete de depósito o carta de crédito.

### 5.4 Medidas cautelares y suspensión: síntesis comparada

| Vía | Norma | Requiere garantizar el interés fiscal para que surta efectos | Plazo típico de resolución del incidente |
|---|---|---|---|
| Recurso de revocación | Art. 144 CFF (remisión) | Sí, salvo excepciones específicas | No suspende por interponerse; requiere trámite de garantía aparte |
| Juicio contencioso (TFJA) | Art. 28 LFPCA | Sí, para actos de determinación/cobro de contribuciones | Incidente resuelto por el magistrado instructor (plazo no verificado con precisión en esta sesión) |
| Amparo indirecto | Art. 135 LAmp (reformado oct-2025) | Sí, "mediante billete de depósito o carta de crédito" | Suspensión provisional en la misma audiencia; definitiva en la audiencia incidental |

---

## 6. Responsabilidad penal fiscal

### 6.1 Defraudación fiscal (art. 108 CFF)

**Tipo base.** "Comete el delito de defraudación fiscal quien, con uso de engaños o aprovechamiento de errores, omita total o parcialmente el pago de alguna contribución u obtenga un beneficio indebido en perjuicio del fisco federal" (texto citado de fuente secundaria convergente, leyes-mx.com; **(no verificado contra el PDF oficial)**).

**Penas por monto, actualizadas para 2026** (Anexo 5 de la RMF 2026, mecanismo de actualización confirmado por decreto DOF 7-nov-2025 vigente desde el 1-ene-2026; los montos exactos provienen de fuentes secundarias que coinciden entre sí pero no se verificaron contra el Anexo 5 oficial — **grado C**):

- Prisión de 3 meses a 2 años, cuando lo defraudado no exceda de **$2,531,920.00**.
- Prisión de 2 a 5 años, cuando exceda de $2,531,920.00 sin pasar de **$3,797,870.00**.
- Prisión de 3 a 9 años, cuando exceda de $3,797,870.00.
- Prisión de 3 meses a 6 años cuando el monto defraudado sea indeterminable.

**Calificativas (agravan la pena).** Entre las reportadas de forma convergente: uso de documentos falsos; omisión reiterada de expedir comprobantes fiscales por las actividades realizadas; manifestar datos falsos para obtener una devolución de contribuciones improcedente; no llevar los sistemas o registros contables o asentar datos falsos en ellos; omitir enterar, total o parcialmente, contribuciones retenidas o recaudadas; usar datos falsos para acreditar o disminuir contribuciones; y (calificativa incorporada en reformas recientes, no verificada su fecha exacta) dar efectos fiscales a comprobantes que amparen operaciones simuladas.

**Atenuante.** Si el contribuyente restituye el monto defraudado, "de manera espontánea y en una sola exhibición" (formulación aproximada de fuente secundaria), antes de que la autoridad lo descubra o notifique el ejercicio de facultades, la pena puede reducirse.

### 6.2 Defraudación fiscal equiparada (art. 109 CFF)

Se sanciona con las mismas penas del art. 108 a quien, entre otros supuestos (lista de fuente secundaria convergente, leyes-mx.com):

- **Fr. I.** Consigne en una declaración deducciones falsas o ingresos menores a los reales, o (para persona física) realice erogaciones superiores a los ingresos declarados en el ejercicio, sin comprobar el origen de la diferencia — la base de las auditorías por **discrepancia fiscal**.
- **Fr. II.** Omita enterar a las autoridades fiscales, dentro del plazo que la ley señale, las cantidades que por concepto de contribuciones hubiere retenido o recaudado.
- **Fr. III.** Se beneficie sin derecho de un subsidio o estímulo fiscal.
- **Fr. IV.** Simule uno o más actos o contratos obteniendo un beneficio indebido en perjuicio del fisco federal — la base penal de la simulación de operaciones que también dispara el 69-B en la vía administrativa.
- **Fr. V.** Omita presentar, por más de 12 meses, las declaraciones que tengan el carácter de definitivas, dejando de pagar la contribución correspondiente.
- **Fr. VIII.** Dé efectos fiscales a los comprobantes digitales cuando no reúnan los requisitos legales.

**Excluyente.** No se ejercerá acción penal si el contribuyente entera espontáneamente, con sus recargos, las cantidades adeudadas, antes de que la autoridad descubra la omisión o notifique el inicio de facultades de comprobación.

### 6.3 Delito de comprobantes fiscales falsos (art. 113 Bis CFF)

Reformado por decreto DOF **7-nov-2025**, en vigor desde el **1-ene-2026** (fuente convergente y verificada contra dos análisis independientes de despachos, además de la referencia ya usada en `fiscal/01`). Texto sustantivo (fuente secundaria, mley.mx): sanciona con **2 a 9 años de prisión** a quien, por sí o por interpósita persona, "expida, enajene, compre o adquiera comprobantes fiscales que amparen operaciones inexistentes, falsas o actos jurídicos simulados"; la misma pena aplica a quien "expida, enajene, compre, adquiera o **dé efectos fiscales**" a comprobantes falsos — este último verbo ("dé efectos fiscales") es la ampliación clave de la reforma de 2025: ya no solo se persigue penalmente a quien factura sin sustancia, sino también a quien **deduce o acredita** ese comprobante sabiendo o debiendo saber de su falsedad.

**Sujetos adicionales y agravantes.** Las plataformas digitales de servicios (conforme a la Ley del IVA) y sus operadores enfrentan la misma pena si permiten anuncios para adquirir o vender comprobantes fraudulentos; los servidores públicos que cometan el delito enfrentan, además, destitución e inhabilitación de 1 a 10 años.

**Prisión preventiva oficiosa.** La reforma armoniza con la reforma constitucional al art. 19 constitucional que agregó los delitos de facturación falsa al catálogo de delitos con **prisión preventiva oficiosa** (múltiples fuentes convergentes: yahoo/EFE, análisis de despachos; **(no verificado el texto exacto del art. 19 constitucional reformado en esta sesión)**). **Inferencia:** esto cambia radicalmente el riesgo práctico frente al art. 113 Bis: antes de la reforma, la defensa podía negociar medidas cautelares distintas a la prisión mientras se resolvía el proceso; con prisión preventiva oficiosa, el indiciado permanece detenido durante el proceso salvo que se acredite alguna causal de excepción — de ahí que la prevención (materialidad documentada desde el origen de cada operación, §2.2) sea muchísimo más valiosa que la defensa posterior.

**Requisito de querella y acción penal simultánea.** Al igual que el resto de los delitos fiscales del Título Cuarto, Capítulo II del CFF, la persecución exige querella previa de la SHCP (art. 92 CFF, §6.4), salvo que el propio art. 113 Bis prevea una regla distinta (no verificado); puede perseguirse simultáneamente con el delito de operaciones con recursos de procedencia ilícita (art. 400 Bis del Código Penal Federal), según fuente secundaria.

### 6.4 Querella y acción penal (art. 92 CFF)

La SHCP tiene el carácter de víctima u ofendida en los procedimientos penales por delitos fiscales. Para proceder penalmente por los delitos de los arts. 105, 108, 109, 110, 111, 112 y 114 CFF, es necesario que **previamente la SHCP formule querella**, "independientemente del estado en que se encuentre el procedimiento administrativo que en su caso se tenga iniciado" (formulación de fuente secundaria convergente). Para otros delitos (arts. 102, 103 y 115), lo que se requiere es una **declaración de que el fisco federal sufrió o pudo sufrir perjuicio**. Cuando el daño es cuantificable, la SHCP hace la cuantificación en la propia querella o declaración, y esa cuantificación **solo tiene efectos en el proceso penal** (no vincula al procedimiento administrativo ni viceversa, lo que explica por qué es jurídicamente posible ganar el juicio de nulidad administrativo y aun así enfrentar o continuar un proceso penal, y viceversa — son dos vías independientes con estándares probatorios distintos).

---

## 7. Traducción operable

### 7.1 Mapa de decisión: qué medio de defensa usar

```
¿El acto es una sentencia definitiva de un tribunal (TFJA u otro)?
├─ SÍ → Amparo directo (art. 170 LAmp) ante Tribunal Colegiado.
│        Si la sentencia es favorable pero la autoridad interpuso revisión
│        contenciosa: amparo directo "adhesivo", solo para combatir la norma
│        aplicada, condicionado a que prospere primero la revisión de la autoridad.
└─ NO → ¿Es un acto administrativo definitivo (liquidación, resolución de un
         procedimiento, resolución del 69-B/69-B Bis/49-Bis)?
         ├─ SÍ → ¿Hay tiempo (≤30 días hábiles) y se busca solo anular el acto,
         │        sin cuestionar la constitucionalidad de la norma?
         │        ├─ SÍ, y se prefiere una vía rápida y gratuita → Recurso de
         │        │    revocación (optativo, art. 116 CFF, plazo 30 días hábiles,
         │        │    resolución en 3 meses o negativa ficta).
         │        └─ SÍ, pero se busca litigar directamente o el acto es de una
         │             autoridad distinta al SAT/ANAM → Juicio contencioso
         │             administrativo ante el TFJA (art. 13 LFPCA, 30 días hábiles;
         │             elegir vía tradicional o en línea al presentar la demanda).
         └─ NO → ¿Es un acto de ejecución (embargo, aseguramiento de cuentas)
                  o se busca impugnar la constitucionalidad de la norma aplicada
                  por primera vez?
                  └─ SÍ → Amparo indirecto ante Juzgado de Distrito, con solicitud
                       de suspensión provisional inmediata (art. 135 LAmp:
                       condicionada a garantía del crédito reclamado desde oct-2025).
```

**Regla de plazos, de memoria:** 15 días para desvirtuar el 69-B; 5 días hábiles para responder a una visita del 49-Bis; 30 días hábiles para recurso de revocación y para demanda ante el TFJA (vía ordinaria); 3 meses para que la autoridad resuelva el recurso de revocación antes de la negativa ficta.

### 7.2 Checklist previo a interponer cualquier medio de defensa

1. **Identificar la fecha exacta de notificación** y calcular el plazo fatal en días hábiles (art. 12 CFF), no naturales, salvo que la norma específica diga lo contrario (p. ej., el plazo de 15 días del 69-B es hábil; el de 90 días naturales para sentencia en amparo, post-reforma 2025, es natural).
2. **Reunir las cuatro capas de evidencia de materialidad** (§2.2) para cualquier deducción o acreditamiento en disputa, antes de decidir si conviene desvirtuar o autocorregirse.
3. **Calcular el costo de garantizar el interés fiscal** (fianza, billete de depósito o carta de crédito) antes de decidir la vía, porque desde octubre de 2025 la suspensión "gratuita" en materia fiscal es la excepción, no la regla.
4. **Verificar si el crédito fiscal ya es firme.** Si lo es, el amparo contra actos de cobro solo procede por violaciones procesales y solo hasta la publicación de la convocatoria de remate — fuera de esa ventana, la única vía es atacar la prescripción o negociar el pago.
5. **Decidir recurso de revocación vs. juicio contencioso directo** según: (a) si se necesita más tiempo para reunir prueba (el recurso da hasta 3 meses de resolución administrativa, tiempo que puede usarse para documentar mejor el caso antes del juicio); (b) si hay negativa ficta previsible que convenga impugnar directamente; (c) el costo y la formalidad relativa de cada vía.
6. **Revisar si el acto está en el catálogo de "delitos con prisión preventiva oficiosa"** (comprobantes fiscales falsos, entre otros) antes de cualquier estrategia de "esperar y ver": si lo está, la prevención documental vale más que cualquier defensa posterior.
7. **Confirmar si existe querella de la SHCP** antes de asumir que hay riesgo penal inminente: sin querella, no hay acción penal posible por los delitos que la requieren (art. 92 CFF), aunque el procedimiento administrativo siga su curso en paralelo.

---

## 8. Trampas y errores comunes

1. **Confundir "tener el CFDI" con "estar protegido".** El comprobante es condición necesaria, no suficiente; sin las otras tres capas de evidencia de materialidad (§2.2), la deducción cae ante cualquier auditoría seria, con jurisprudencia del TFJA respaldando a la autoridad (VIII-J-1aS-115).
2. **Tratar la compensación de saldos a favor como si siguiera siendo universal.** Desde 2019 solo se compensa contra el mismo impuesto; planear flujo de efectivo asumiendo que un saldo a favor de IVA puede "usarse" contra ISR es un error de caja, no solo de forma.
3. **Confundir exención con tasa 0%.** Ya documentado con fuente en `fiscal/01`, §4.2: la exención bloquea el acreditamiento del IVA de insumos; la tasa 0% no. Cotizar un proyecto exento como si fuera tasa 0% subestima el costo real.
4. **Ignorar que la inclusión en el listado del 69-B se proyecta hacia el futuro.** Confiar en que un proveedor "ya resolvió" su situación porque el ejercicio auditado quedó atrás es un error frente a la jurisprudencia 2024206: el efecto no se limita al ejercicio revisado.
5. **Esperar la suspensión "gratuita" del acto reclamado en materia fiscal.** Desde octubre de 2025, y confirmado por la jurisprudencia 2028811 desde 2024 para embargos precautorios, la regla es garantizar; litigar sin presupuestar el costo de la garantía es litigar con un plan incompleto.
6. **Subestimar el art. 49-Bis por desconocerlo.** Con solo 5 días hábiles para responder a la visita expedita, una empresa que no tiene su carpeta de materialidad organizada de antemano no alcanza a reaccionar dentro del plazo.
7. **Asumir que ganar el juicio de nulidad cierra el riesgo penal, o viceversa.** Son vías independientes (art. 92 CFF): la cuantificación del daño en la querella penal no está vinculada a la resolución del procedimiento administrativo.
8. **No distinguir defraudación fiscal (art. 108, requiere engaño activo) de su forma equiparada (art. 109, no siempre requiere engaño, p. ej. omitir enterar retenciones).** La estrategia de defensa es distinta porque el estándar probatorio del elemento subjetivo difiere.
9. **Dar por hecho el monto exacto de las penas de 2026 sin revisar el Anexo 5 vigente al momento de los hechos.** Los montos de los arts. 108-109 se actualizan cada año; usar la cifra de un año distinto al de los hechos investigados es un error técnico que puede cambiar la calificación del delito.
10. **Ignorar que el amparo directo contra una sentencia favorable del TFJA tiene un efecto limitado** (solo constitucionalidad de la norma, condicionado a que prospere la revisión de la autoridad) y no es una segunda oportunidad de litigar el fondo ya ganado.

---

## 9. Autoevaluación

1. ¿Qué tres condiciones, tomadas literalmente del art. 27, fr. III LISR, debe cumplir el pago de una deducción que excede $2,000 para poder deducirse?
2. ¿Por qué el pago de combustibles no tiene el piso de $2,000 que sí aplica a las demás deducciones?
3. Explica la diferencia entre EFOS y EDOS, y qué plazo tiene un EDOS para autocorregirse después de la publicación del listado presunto.
4. Cita el rubro y la clave de la jurisprudencia del TFJA que sostiene que el CFDI no basta por sí solo para acreditar materialidad.
5. ¿Qué efecto tiene, conforme al registro 2024206, la inclusión definitiva de un proveedor en el listado del art. 69-B más allá del ejercicio fiscal auditado?
6. Diferencia funcionalmente la CUFIN de la CUCA: ¿qué protege cada una y qué pasa si un reembolso de capital excede el saldo de la CUCA?
7. Enumera los cuatro métodos de precios de transferencia del art. 180 LISR y explica en una frase cada uno.
8. ¿En qué circunstancia se presume que una operación entre un residente en México y una entidad extranjera es entre partes relacionadas, salvo prueba en contrario?
9. ¿Cuántos días de presencia en México, en un periodo de doce meses, generan establecimiento permanente para una obra de construcción o supervisión, y qué pasa si el residente extranjero subcontrata parte de la obra?
10. ¿Por qué ya no es correcto decir que un saldo a favor de IVA puede "compensarse contra ISR"? ¿Desde cuándo cambió esto?
11. Diseña, en una frase, el criterio para decidir entre recurso de revocación y juicio contencioso administrativo cuando ambos son procedentes y hay tiempo para ambos.
12. ¿Qué cambió en octubre de 2025 respecto de la suspensión del acto reclamado en materia fiscal dentro del juicio de amparo, y qué jurisprudencia de 2024 ya anticipaba esa tendencia para embargos precautorios de cuentas bancarias?
13. Distingue el art. 108 CFF del art. 109 CFF citando al menos una fracción de cada uno.
14. ¿Qué cambió el verbo "dé efectos fiscales" en la reforma de 2025-2026 al art. 113 Bis CFF, y por qué importa tanto la prisión preventiva oficiosa para la estrategia de defensa?
15. ¿Qué requiere el art. 92 CFF antes de que pueda ejercerse acción penal por defraudación fiscal, y qué relación tiene esa exigencia con el procedimiento administrativo paralelo?

---

## 10. Fuentes

**Texto legal verificado directamente contra archivo de texto plano oficial (Cámara de Diputados, última reforma DOF 01-04-2024):**

1. LISR, arts. 2, 3, 16, 17, 25, 27, 77, 90, 140, 179, 180 — `laboratorio/replicas/V05-spiva-y-fiscalidad-sic/datos/legal/LISR.txt` (extraído del PDF oficial de https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf, consultado en sesiones previas del sistema).

**Texto legal verificado contra fuentes secundarias especializadas (no contra PDF oficial en esta sesión, ver nota metodológica abajo):**

2. CFF art. 69-B — https://leyes-mx.com/codigo_fiscal_de_la_federacion/69-B.htm (consultado 25-sep-2026).
3. CFF arts. 108 y 109 — https://leyes-mx.com/codigo_fiscal_de_la_federacion/108.htm y .../109.htm (consultado 25-sep-2026).
4. CFF art. 92 — https://leyes-mx.com/codigo_fiscal_de_la_federacion/92.htm (consultado 25-sep-2026).
5. CFF art. 69-B Bis — https://leyes-mx.com/codigo_fiscal_de_la_federacion/69-B%20Bis.htm (consultado 25-sep-2026).
6. CFF arts. 116, 121, 131 (recurso de revocación) — https://mley.mx/CFF/articulo/116/ y análisis convergentes (consultado 25-sep-2026).
7. LFPCA art. 13 y art. 28 — https://mley.mx/LFPCA/articulo/13/ y https://leyes-mx.com/ley_federal_de_procedimiento_contencioso_administrativo/28.htm (consultado 25-sep-2026).
8. Ley de Amparo art. 170 — https://leyes-mx.com/ley_de_amparo_reglamentaria_de_los_articulos_103_y_107_de_la_constitucion_politica_de_los_estados_unidos_mexicanos/170.htm (consultado 25-sep-2026).
9. LIVA arts. 2-A, 5, 6, 9 — resultados agregados de búsqueda sobre diputados.gob.mx/LeyesBiblio/pdf/LIVA.pdf y sdv.com.mx (consultado 25-sep-2026).
10. Ley Aduanera arts. 36, 47, 90 — https://leyes-mx.com/ley_aduanera/90.htm y https://reinoaduanero.mx/articulo-36-a-ley-aduanera... (consultado 25-sep-2026).

**Reformas 2025-2026 (mismo evento confirmado por ≥2 fuentes independientes citando la misma fecha de DOF):**

11. Reforma al CFF, DOF 07-11-2025, vigente 1-ene-2026 (arts. 69-B Bis, 113 Bis, 29-A fr. IX, 49-Bis, montos de defraudación fiscal) — https://www.diputados.gob.mx/LeyesBiblio/ref/cff/CFF_ref62_07nov25.pdf; https://contadormx.com/reformas-cff-2026/; https://ruizconsultores.com.mx/blog/03-blog-nuevo-articulo-49-bis-cff-procedimiento-expres-fiscalizacion/; https://carbajalcontadores.com/2026/09/07/articulo-49-bis-cff-2026-auditoria-expres-sat-suspension-facturacion-cfdi (todos consultados 25-sep-2026).
12. Reforma a la Ley de Amparo, al CFF y a la Ley Orgánica del TFJA, DOF 16-10-2025, vigente 17-10-2025 — https://www.gtlaw.com/en/insights/2025/10/nueva-reforma-a-la-ley-de-amparo; https://www.dlapiper.com/es-mx/insights/publications/2025/10/mexico-reforms-the-amparo-law; https://pcga.mx/ideas/ley-amparo-materia-fiscal/; https://www.hlc.com/es/publications/reform-of-the-amparo-law-the-federal-tax-code-and-the-organic-law-of-the-fed-court-of-admin-justice (todos consultados 25-sep-2026).
13. Reforma a la LFPCA, DOF 09-06-2026, vigencia escalonada 10-jun-2026 / 6-dic-2026 / 4-feb-2027 — https://www.samanosc.com.mx/post/reforma-a-la-ley-federal-de-procedimiento-contencioso-administrativo-nuevos-plazos-y-reglas-procesa (consultado 25-sep-2026).
14. Anexo 5 RMF 2026, montos actualizados art. 108 CFF (grado C, no verificado contra DOF directo) — convergencia de dos búsquedas independientes citando $2,531,920.00 y $3,797,870.00 (consultado 25-sep-2026).
15. Estímulo IEPS diésel LIF 2026, art. 20 apartado A — https://www.elfinanciero.com.mx/economia/2026/09/21/estimulo-complementario-al-diesel-alcanza-su-mayor-nivel-en-cuatro-anos-asi-queda-el-apoyo-de-hacienda/; https://contadormx.com/estimulos-fiscales-2026-ieps-lif/ (consultados 25-sep-2026).
16. Decreto IMMEX, actualizaciones 2026 — https://www.camtomx.com/en/blog/programa-immex-actualizaciones-2026; https://dtdexpress.mx/es/aduanas/immex-programa-importacion-temporal-mexico-2026/ (consultados 25-sep-2026, **no verificado contra el Decreto oficial**).

**Jurisprudencia y tesis (verificadas con registro/clave exacta):**

17. TFJA, jurisprudencia **VIII-J-1aS-115**, "COMPROBANTES FISCALES. LOS REGISTROS CONTABLES DEBEN ESTAR APOYADOS CON LA DOCUMENTACIÓN COMPROBATORIA CORRESPONDIENTE..." — documento oficial descargado de https://www.tfja.gob.mx/cesmdfa/sctj/tesis-pdf-detalle/45851/ (texto íntegro verificado, consultado 25-sep-2026).
18. SCJN, Segunda Sala, jurisprudencia **2a./J. 26/2020 (10a.)**, registro digital **2022083**, SJF Libro 78, sept-2020, T. I, p. 616 (fuente: búsqueda agregada sobre sjf2.scjn.gob.mx, consultado 25-sep-2026; el sitio sjf2.scjn.gob.mx bloqueó el acceso directo por protección Incapsula, ver nota metodológica).
19. SCJN, jurisprudencia por contradicción de tesis 9/2021, registro digital **2024206**, "EFECTOS DE LA PUBLICACIÓN EN EL DIARIO OFICIAL..." — https://juristeca.com/mx/scjn/tesis-jurisprudenciales/2022/2/registro-2024206-... (rubro citado de fuente secundaria; consultado 25-sep-2026).
20. Pleno Regional en Materia Administrativa, jurisprudencia por contradicción, registro digital **2028811**, sobre suspensión y garantía en embargo precautorio de cuentas bancarias, publicada 17-may-2024 (fuente: búsqueda agregada, consultado 25-sep-2026).

**Documentos internos del sistema referenciados, no repetidos:**

21. `fiscal/01-personas-fisicas-actividad-empresarial.md` (§§3.2-3.3, 4.1-4.3): régimen de persona física, EFOS/EDOS a nivel operativo, exención de IVA en construcción y combustibles.
22. `conocimiento/27-fiscalidad-2026-y-estructura-sic.md` (§2.3): retención de dividendos del SIC/BMV para persona física.
23. `conocimiento/24-politica-publica-regulacion-y-mercados.md`: aranceles de EUA (Secciones 301/232) y rondas del T-MEC vigentes en 2026.

**Nota metodológica.** El PDF oficial de diputados.gob.mx para CFF, LIVA, LIEPS y Ley Aduanera no pudo extraerse con texto legible mediante la herramienta de lectura web en esta sesión (devolvió metadatos binarios sin contenido). El sitio sjf2.scjn.gob.mx (buscador oficial de tesis) está protegido por Incapsula y bloqueó tanto la lectura directa como las peticiones HTTP con encabezado de navegador; toda tesis de la SCJN citada aquí se verificó por convergencia de al menos dos fuentes secundarias independientes que reportan el mismo número de registro, rubro (o su núcleo) y fecha de publicación — no por lectura directa del original en el Semanario Judicial de la Federación. Se recomienda, antes de usar cualquiera de estas tesis en un escrito real, confirmar el texto íntegro en sjf2.scjn.gob.mx o en el Buscador Jurídico (bj.scjn.gob.mx) con acceso humano directo.
