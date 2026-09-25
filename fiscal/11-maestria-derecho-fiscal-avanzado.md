# 11 — Maestría en Derecho Fiscal: impuestos federales, comercio exterior y litigio fiscal

> Nivel: maestría · Actualizado 2026-09-25 · Grado global: **A** en los artículos de la LISR citados textualmente (2, 3, 16, 17, 25, 27, 77, 90, 140, 179, 180), verificados contra el archivo de texto plano oficial de la Cámara de Diputados (última reforma DOF 01-04-2024) en `laboratorio/replicas/V05-spiva-y-fiscalidad-sic/datos/legal/LISR.txt`. **B** en los artículos de CFF, LIVA, Ley Aduanera, LFPCA y Ley de Amparo, tomados de transcripciones especializadas (leyes-mx.com, mley.mx) porque el PDF oficial de diputados.gob.mx no se pudo extraer legible en esta sesión (nota metodológica en §10). **C** en los montos en pesos del art. 108 CFF (Anexo 5, RMF 2026), confirmados por dos fuentes secundarias coincidentes pero no contra el DOF. Cuatro tesis/jurisprudencias (TFJA y SCJN) se citan con clave o registro exacto, verificadas por convergencia de fuentes ante el bloqueo del buscador oficial sjf2.scjn.gob.mx (protección Incapsula).

**Alcance.** Este capítulo asume los fundamentos de licenciatura (sujetos, hecho generador, elementos del tributo) que se construyen en paralelo en `fiscal/`. No repite lo ya verificado en `fiscal/01-personas-fisicas-actividad-empresarial.md` (régimen de persona física, EFOS/EDOS operativo, y la corrección de que la construcción de vivienda es **exenta** de IVA, no tasa 0%: art. 9, fr. II LIVA) ni en `conocimiento/27-fiscalidad-2026-y-estructura-sic.md` (retención de dividendos del SIC/BMV). Construye sobre esa base hacia persona moral, grupos, comercio exterior y litigio.

**Convenciones.** Comillas = cita literal verificada. "**Inferencia:**" = razonamiento propio, no criterio oficial. "**Doctrina:**" = posición académica. "**(nv)**" = no verificado contra texto oficial en esta sesión.

---

## 1. Objetivos de dominio

1. Explicar la acumulación de ingresos (arts. 16-17 LISR) y la deducción (arts. 25-27 LISR) de persona moral, y distinguir un CFDI válido de una operación materializada.
2. Diagramar el art. 69-B CFF (EFOS/EDOS) y el nuevo art. 49-Bis CFF (visita expedita, vigente 1-ene-2026), citando la tesis que define qué prueba la materialidad.
3. Calcular el efecto de CUFIN y CUCA en una distribución de dividendos o reducción de capital (arts. 77-78 LISR).
4. Aplicar los cuatro métodos de precios de transferencia del art. 180 LISR y ubicar la presunción de vinculación con REFIPRES.
5. Determinar si un residente extranjero tiene establecimiento permanente (arts. 2-3 LISR): agente dependiente, obra >183 días, agente independiente que deja de serlo.
6. Distinguir tasa 0%, exención y tasa general en IVA; calcular el acreditamiento proporcional con actos mixtos y la regla real de compensación (solo mismo impuesto desde 2019).
7. Elegir entre recurso de revocación, juicio contencioso (tradicional o en línea) y amparo, según el acto, el plazo y si se busca anular el acto o combatir la norma.
8. Explicar la suspensión del acto reclamado tras la reforma a la Ley de Amparo (oct-2025) y la reforma a la LFPCA (jun-2026).
9. Distinguir defraudación fiscal (art. 108), su forma equiparada (art. 109) y el delito de comprobantes falsos (art. 113 Bis), y por qué este último exige prisión preventiva oficiosa.
10. Construir el mapa de decisión "qué medio de defensa usar" y aplicarlo en minutos ante un acto real.

---

## 2. ISR avanzado

### 2.1 Ingreso acumulable

Art. 16 LISR (personas morales): "acumularán la totalidad de los ingresos en efectivo, en bienes, en servicio, en crédito o de cualquier otro tipo, que obtengan en el ejercicio, inclusive los provenientes de sus establecimientos en el extranjero." No son acumulables los ingresos "por aumento de capital, por pago de la pérdida por sus accionistas, por primas obtenidas por la colocación de acciones... ni los que obtengan con motivo de la revaluación de sus activos y de su capital", ni los dividendos que una persona moral perciba de otra residente en México (último párrafo) — ancla de la mecánica de CUFIN (§2.4).

Art. 17 LISR fija el **momento** de acumulación cuando la ley no lo prevé en otro artículo: para enajenación de bienes o servicios, la fecha que ocurra primero entre "a) Se expida el comprobante fiscal... b) Se envíe o entregue materialmente el bien o se preste el servicio. c) Se cobre o sea exigible... aun cuando provenga de anticipos" (fr. I).

Para persona física, el art. 90 LISR obliga a informar en la declaración anual préstamos, donativos y premios que "en lo individual o en su conjunto, excedan de $600,000.00" (segundo párrafo). **Inferencia:** ese umbral dispara la mayoría de las cartas invitación por depósitos no explicados que escalan a discrepancia fiscal.

**Doctrina.** La distinción entre ingreso devengado (persona moral) e ingreso percibido/exigible (persona física) es, para Arrioja Vizcaíno y De la Garza, el eje del "momento de causación" del hecho generador (art. 6 CFF), distinto del momento de exigibilidad del crédito fiscal.

### 2.2 Deducciones autorizadas y su materialidad

Art. 25 LISR lista las deducciones de persona moral: devoluciones/descuentos (I), costo de lo vendido (II), gastos (III), inversiones (IV), incobrables y pérdidas por caso fortuito (V), cuotas IMSS patronales (VI), intereses devengados (VII), ajuste anual por inflación deducible (VIII), anticipos de cooperativas/civiles (IX), aportaciones a fondos de pensiones con tope del factor 0.47 o 0.53 (X).

Art. 27 LISR — requisitos con más litigio:

- **Fr. I:** "Ser estrictamente indispensables para los fines de la actividad del contribuyente", salvo donativos no onerosos con tope del **7%** de la utilidad fiscal del ejercicio anterior (4% si el donatario es gobierno).
- **Fr. III:** "Estar amparadas con un comprobante fiscal y que los pagos cuyo monto exceda de $2,000.00 se efectúen mediante transferencia... cheque nominativo... tarjeta... o monederos electrónicos autorizados." Para **combustibles**, el pago debe hacerse por esos medios "aun cuando la contraprestación... no exceda de $2,000.00" — sin piso de minimis.
- **Fr. IV:** "Estar debidamente registradas en contabilidad y que sean restadas una sola vez."

**El CFDI no basta: la materialidad es un requisito construido por jurisprudencia**, hoy también positivizado: la reforma al CFF (DOF 7-nov-2025, vigente 1-ene-2026) modificó el art. 29-A, fr. IX CFF para exigir desde la emisión que el CFDI ampare una operación real (fuente: `fiscal/01`, §3.2; nv contra el PDF oficial). Jurisprudencia verificada íntegra:

> **TFJA, jurisprudencia VIII-J-1aS-115**, materia CFF, rubro: **"COMPROBANTES FISCALES. LOS REGISTROS CONTABLES DEBEN ESTAR APOYADOS CON LA DOCUMENTACIÓN COMPROBATORIA CORRESPONDIENTE, POR LO QUE SI ÚNICAMENTE OBRAN AQUELLOS, LA AUTORIDAD FISCALIZADORA ESTÁ EN POSIBILIDADES DE DETERMINAR LA FALTA DE MATERIALIZACIÓN DE LAS OPERACIONES DESCRITAS EN ELLOS."** Aprobada por acuerdo G/S1-10/2021, cinco precedentes de la Primera Sección de la Sala Superior (2018-2019). Sostiene que "los comprobantes fiscales no se pueden considerar perfectos per se... es indispensable que estén respaldados en los elementos documentales que comprueben que lo consignado en ellos, existió realmente", citando la tesis 1a. CLXXX/2013 de la Primera Sala SCJN, "COMPROBANTES FISCALES. CONCEPTO, REQUISITOS Y FUNCIONES."

**Regla operable:** cuatro capas de evidencia por operación relevante — CFDI, contrato/pedido, evidencia de ejecución (bitácoras, fotos con fecha, actas), y evidencia de capacidad material del proveedor. Aplica igual a persona moral.

### 2.3 El procedimiento del art. 69-B CFF y sus novedades de 2026

Mecánica (fuentes convergentes SAT/PRODECON): (1) la autoridad presume inexistencia de operaciones cuando el emisor carece de "activos, personal, infraestructura o capacidad material... para prestar los servicios o producir, comercializar o entregar los bienes", o no es localizable; (2) notifica por buzón, portal y DOF, con **15 días** para desvirtuar (prórroga de 5); (3) resuelve en máximo **50 días** (puede requerir información en 20 días, suspendiendo el plazo); (4) si no desvirtúa, publica el **listado definitivo**: sus comprobantes "no producen ni produjeron efecto fiscal alguno"; (5) el EDOS tiene 30 días desde el listado presunto para autocorregirse o acreditar materialidad.

Dos jurisprudencias SCJN acotan sus efectos:

> **2a./J. 26/2020 (10a.), registro 2022083**, SJF Libro 78, sept-2020, T. I, p. 616: el **recurso de revisión fiscal es improcedente por cuantía** contra sentencias del TFJA que anulan la inclusión en el 69-B, porque esa resolución no fija un crédito líquido.
> **Contradicción de tesis 9/2021, registro 2024206**, SJF Libro 10, feb-2022, rubro sobre los **"EFECTOS DE LA PUBLICACIÓN..."**: aunque el procedimiento derive de un ejercicio específico, la inclusión definitiva **tiene efectos generales y se proyecta hacia el futuro**. **Inferencia:** un proveedor listado por hechos de 2022 sigue estigmatizado en 2026 con el mismo RFC — revisar el listado antes de cada contratación, no solo al operar.

**Novedad — art. 49-Bis CFF (visita expedita, vigente 1-ene-2026):** procedimiento paralelo y más rápido, máximo **24 días hábiles** entre orden y resolución, con solo **5 días hábiles** de respuesta tras la visita; puede terminar en suspensión del sello digital (fuentes convergentes: IDC, Ruiz Consultores, Carbajal Contadores; nv contra texto oficial). No sustituye al 69-B: ataca al contribuyente auditado (CSD), no genera listado erga omnes.

**Novedad relacionada — art. 69-B Bis CFF (transmisión indebida de pérdidas fiscales):** presunción cuando el contribuyente con derecho a disminuir pérdidas "fue parte de una reestructuración, escisión o fusión... o de un cambio de accionistas" y deja de pertenecer al grupo original; procede recurso de revocación contra la resolución (texto de fuente secundaria, nv oficial).

### 2.4 CUFIN y CUCA

Art. 77 LISR: la **CUFIN** "se adicionará con la utilidad fiscal neta de cada ejercicio... y con los ingresos, dividendos o utilidades sujetos a regímenes fiscales preferentes... y se disminuirá con el importe de los dividendos o utilidades pagados... cuando... provengan del saldo de dicha cuenta." La utilidad fiscal neta es el resultado fiscal menos el ISR del art. 9 y menos las partidas no deducibles (salvo art. 28, fr. VIII-IX y PTU).

**Función (doctrina):** evita gravar dos veces la misma utilidad — ISR corporativo (art. 9) y ISR del socio al recibir dividendo. Mientras el dividendo provenga de la CUFIN, no hay retención corporativa adicional; el excedente paga el impuesto del art. 10 sobre el resultado de multiplicarlo por el factor **1.4286**.

**CUCA (art. 78):** registra aportaciones de capital y primas de suscripción; su saldo se reembolsa sin generar utilidad gravable. El exceso sobre la CUCA en una reducción de capital sí es utilidad distribuida. **Regla:** calcular el saldo actualizado de CUCA por acción antes de cualquier reembolso.

### 2.5 Dividendos (art. 140 LISR): solo la mecánica corporativa

El detalle de retención sobre dividendos del SIC/BMV ya está en `conocimiento/27` §2.3. Aquí solo el acreditamiento: la persona física acumula el dividendo y puede acreditar "el impuesto sobre la renta pagado por la sociedad", determinado aplicando la tasa del art. 9 (30%) al resultado de multiplicar el dividendo por el factor **1.4286**, siempre que acumule también ese impuesto y tenga la constancia (art. 76, fr. XI). Además hay una "tasa adicional del 10%... con carácter de pago definitivo" (segundo párrafo) — la que retiene GBM en el SIC/BMV.

### 2.6 Precios de transferencia (arts. 179-184 LISR)

**Obligación (art. 179):** quienes celebren operaciones con partes relacionadas deben usar "los precios, montos de contraprestaciones o márgenes de utilidad que hubieran utilizado u obtenido con o entre partes independientes en operaciones comparables" (principio *arm's length*); si no, la autoridad puede determinarlos con el mismo estándar.

**Comparabilidad:** cinco factores — características de la operación, funciones/activos/riesgos, términos contractuales, circunstancias económicas y estrategias de negocio. Remite expresamente a "las Guías sobre Precios de Transferencia... de la OCDE... de 1995, o aquéllas que las sustituyan."

**Partes relacionadas:** cuando una participa "de manera directa o indirecta en la administración, control o capital de la otra." **Presunción con REFIPRES:** salvo prueba en contrario, las operaciones con entidades en regímenes fiscales preferentes se presumen entre partes relacionadas sin condiciones de mercado.

**Métodos (art. 180), texto literal verificado:** (1) **Precio comparable no controlado:** precio pactado entre independientes en operaciones comparables. (2) **Precio de reventa:** precio de reventa por (1 − % utilidad bruta de independientes). (3) **Costo adicionado:** costo por (1 + % utilidad bruta de independientes). (4) **Partición de utilidades:** utilidad de operación en la proporción de independientes.

**Establecimiento permanente y maquila (arts. 181-184):** los arts. 181-182 fijan cuándo no hay EP por operar como maquiladora si se cumplen reglas de PT específicas (safe harbor/APA); el 184 remite a tratados para conflictos de doble tributación por ajustes de PT. **Inferencia:** el régimen IMMEX (§4) y el de precios de transferencia están entrelazados — la seguridad frente al riesgo de EP de la matriz extranjera depende de documentar los métodos de los arts. 181-182 cada año.

### 2.7 Establecimiento permanente (arts. 2-3 LISR)

**Regla general:** "cualquier lugar de negocios en el que se desarrollen, parcial o totalmente, actividades empresariales o se presten servicios personales independientes" — sucursales, agencias, oficinas, fábricas, talleres, minas, canteras, etc.

**Agente dependiente:** hay EP si una persona "concluye habitualmente contratos o desempeña habitualmente el rol principal" para el residente extranjero, a nombre de él, sobre bienes suyos u obligándolo a prestar un servicio.

**Agente independiente que deja de serlo:** si mantiene inventario del principal, asume sus riesgos, actúa bajo instrucciones detalladas, o su remuneración es independiente del resultado.

**Regla de 183 días para obra:** construcción, demolición, instalación, mantenimiento, montaje o supervisión generan EP solo si duran "más de 183 días naturales, consecutivos o no, en un periodo de doce meses"; los días de subcontratistas se suman. **Regla operable:** llevar bitácora de días acumulados desde el primer día de actividad, sumando subcontratistas, con alerta antes del día 150.

**Excepciones (art. 3):** no hay EP en "un lugar de negocios cuyo único fin sea la realización de actividades de carácter preparatorio o auxiliar" (nv el detalle de incisos específicos en esta sesión).

---

## 3. IVA e IEPS avanzados

### 3.1 Gravado, exento y tasa 0%

El art. 1 LIVA grava enajenación, servicios independientes, uso o goce temporal e importación, a **16%**, salvo tasa 0% o exención.

**Tasa 0% (art. 2-A):** lista taxativa — animales/vegetales no industrializados (salvo hule y mascotas), medicinas de patente y alimentos (excepto bebidas distintas de leche), agua no gaseosa, libros/periódicos/revistas editados por el contribuyente, y exportación de bienes/servicios. A tasa 0% **sí se acredita** el IVA de insumos.

**Exentos (art. 9):** suelo; "construcciones adheridas al suelo, destinadas o utilizadas para casa habitación" (fr. II, detalle ya en `fiscal/01` §4.2); libros/periódicos usados; bienes muebles usados; billetes de lotería; moneda; acciones y documentos por cobrar; lingotes de oro ≥99% al menudeo. En exento **no se acredita** el IVA de insumos.

### 3.2 Acreditamiento, saldos a favor y compensación real

Requisitos del acreditamiento (art. 5, ya en `fiscal/01` §4.1): gasto estrictamente indispensable para actos gravados/tasa 0%; IVA trasladado expresamente en el CFDI; efectivamente pagado en el mes; y proporcional si el gasto es solo parcialmente deducible para ISR.

**Prorrateo con actos mixtos (art. 5, fr. V):** IVA identificable con actos gravados es 100% acreditable; el de actos exentos, no acreditable; el común se acredita en la proporción de actos gravados sobre el total. **Inferencia:** un contratista con obra exenta y gravada debe separar contabilidad por proyecto para minimizar el IVA "común" perdido en el prorrateo.

**Saldo a favor (art. 6):** se acredita contra IVA futuro, se pide en devolución, o se compensa "en términos del art. 23" CFF. **Corrección: la compensación universal se eliminó desde el 1-ene-2019** — desde entonces solo se compensa contra el **mismo impuesto** (IVA contra IVA), nunca contra ISR.

**Plazos de devolución (arts. 22, 22-A CFF):** 40 días hábiles para resolver; requerimiento de información posible dentro de los primeros 20 días (suspende el plazo); intereses a cargo del SAT si se paga tarde. Días hábiles conforme al art. 12 CFF.

### 3.3 IEPS: estímulo complementario al diésel (2026)

El detalle de cuotas de IEPS a combustibles y la ausencia de tasa 0% de IVA para ellos ya está en `fiscal/01` §4.3. Lo nuevo: el art. 20, apartado A, fr. IV-V de la LIF 2026 sostiene un estímulo al IEPS del diésel acreditable primero contra ISR, luego IVA, con devolución posible del remanente. A la fecha de este documento, la SHCP aplicó estímulo del 100% (cuota de $7.3634/litro a cero) más un complementario de $1.8361/litro, ambos por acuerdo semanal (fuente: El Financiero, 21-sep-2026; contadormx.com; nv el texto exacto del art. 20-A). **Inferencia:** para transporte y construcción, el crédito es real pero variable semana a semana — no proyectarlo como constante.

---

## 4. Comercio exterior y aduanas

**Regímenes aduaneros (art. 90 LA):** definitivos (importación/exportación); temporales (retorno en el mismo estado, o elaboración/transformación/reparación bajo maquila o exportación); depósito fiscal; tránsito (interno e internacional); elaboración/transformación/reparación en recinto fiscalizado; recinto fiscalizado estratégico.

**Pedimento (art. 36 LA):** obligación de presentarlo ante la aduana "por conducto de agente o apoderado aduanal", con firma electrónica que acredite regulaciones no arancelarias cuando aplique.

**Clasificación arancelaria (art. 47 LA):** consulta previa ante la autoridad aduanera cuando la mercancía admite más de una fracción, señalando la fracción propuesta, razones y anexando muestras o catálogos. **Inferencia:** para manufactura ligera que importa maquinaria o insumos, la consulta previa evita una reclasificación posterior con multa (PAMA); su costo administrativo es bajo frente al riesgo.

**IMMEX.** Permite importar temporalmente insumos, componentes y maquinaria sin arancel general ni IVA, condicionado a exportar la producción. Actualizaciones 2026 (fuentes convergentes, nv contra el Decreto oficial): verificaciones sin previo aviso; desde marzo de 2026, la factura de exportación debe incluir el número de autorización IMMEX y la fracción arancelaria; reporte anual RAOCE (1-abr al 29-may-2026), cuya omisión cancela el programa automáticamente el 30 de mayo. Requisitos de acceso: ventas al exterior ≥500,000 USD/año o ≥10% de facturación exportada, plan de exportación, alta vía VUCEM.

**Aranceles 2026 (Secciones 301/232 de EUA y T-MEC).** Ya investigado con detalle y fuentes verificadas en `conocimiento/24-politica-publica-regulacion-y-mercados.md` (301 "forced labor" 10-12.5% con exención T-MEC; 232 acero/aluminio 50%, autos 25%, fármacos 100% desde 29-sep-2026 fuera del Anexo III) — no se repite aquí. **Inferencia:** un exportador IMMEX con reglas de origen T-MEC queda exento de la 301 pero no necesariamente de la 232; la clasificación arancelaria correcta (art. 47 LA) es la que decide cuál arancel aplica.

---

## 5. Litigio fiscal completo

### 5.1 Recurso de revocación (arts. 116-133 CFF)

**Procedencia (art. 116):** "Contra los actos administrativos dictados en materia fiscal federal, se podrá interponer el recurso de revocación" (fuente secundaria, nv oficial). Es **optativo**: puede acudirse directo al juicio contencioso, salvo remisión expresa (p. ej. el propio 69-B Bis).

**Plazo (art. 121):** 30 días hábiles desde la notificación, fatal e improrrogable.

**Resolución y negativa ficta (art. 131):** la autoridad tiene **3 meses** para resolver; si no lo hace, hay negativa ficta impugnable directamente ante el TFJA (nv el texto exacto).

**No suspende por sí solo:** requiere garantizar el interés fiscal (remisión al art. 144 CFF, nv en esta sesión).

### 5.2 Juicio contencioso administrativo ante el TFJA

**Plazo (art. 13 LFPCA):** 30 días hábiles desde la notificación, o desde la entrada en vigor de una norma general autoaplicativa; 5 años cuando la autoridad demanda anular una resolución favorable a un particular; suspensiones por fallecimiento o incapacidad del demandante (hasta un año), o por solicitud de un procedimiento de resolución de controversias bajo tratado.

**Tradicional vs. en línea:** el actor elige al presentar la demanda y no puede cambiar de vía; si la autoridad demanda, debe hacerlo en línea obligatoriamente.

**Reforma LFPCA, DOF 9-jun-2026** (vigencia escalonada: general desde 10-jun-2026; comparecencia electrónica de demandados desde 6-dic-2026; nuevos plazos desde 4-feb-2027; nv contra el DOF directo): en vía ordinaria, admisión/desechamiento en 5 días y proyecto de sentencia en 45 días desde el turno; en sumaria, máximo 6 meses entre admisión y sentencia; se deroga el estándar de "difícil reparación" para la suspensión, sustituido por causales de afectación al interés público; notificaciones por Boletín surten efectos al publicarse, sin importar el aviso electrónico. **Inferencia:** presión hacia digitalización obligatoria y relajación del estándar para negar la suspensión — conviene presupuestar la garantía desde el inicio, no confiar en la suspensión sin garantía.

**Suspensión ante el TFJA (art. 28 LFPCA):** incidente ante el magistrado instructor; para actos de determinación/cobro de contribuciones, la suspensión se otorga pero **surte efectos solo si se garantiza el interés fiscal**; el magistrado puede modificarla o revocarla ante hecho superveniente.

### 5.3 Amparo directo e indirecto en materia fiscal

**Indirecto:** contra actos que no sean sentencia definitiva (constitucionalidad de una norma recién aplicada, actos de ejecución, embargos), ante Juzgado de Distrito.

**Directo (art. 170 LAmp):** "procede contra sentencias definitivas, laudos y resoluciones que pongan fin al juicio, dictadas por tribunales judiciales, administrativos, agrarios o del trabajo" — incluida la sentencia del TFJA, ante Tribunal Colegiado. Si la sentencia del TFJA es **favorable** al particular, su amparo directo procede solo "para el único efecto de hacer valer conceptos de violación en contra de las normas generales aplicadas", condicionado a que antes prospere la revisión contenciosa que interponga la autoridad.

**Reforma a la Ley de Amparo, DOF 16-oct-2025, vigente 17-oct-2025** (junto con reformas conexas al CFF y a la Ley Orgánica del TFJA; fuentes convergentes: GT Law, DLA Piper, Holland & Knight, KPMG, Pérez Correa González):

- Suspensión en materia fiscal **condicionada a garantía** del crédito reclamado, "mediante billete de depósito o carta de crédito" (nv el texto exacto del art. 135 reformado).
- Motivación reforzada: el juez debe expresar por escrito los elementos de su decisión (arts. 138, 146).
- Contra créditos fiscales **firmes**, el amparo solo procede hasta la publicación de la convocatoria de remate y solo por **violaciones procesales**, no de fondo; CFF y Ley Orgánica del TFJA declaran improcedentes los medios de defensa contra el cobro o la prescripción de créditos firmes.
- Plazo máximo de sentencia: 90 días naturales (nv el artículo exacto).

Jurisprudencia sobre garantía y suspensión:

> **Pleno Regional en Materia Administrativa, jurisprudencia por contradicción, registro 2028811**, publicada 17-may-2024: la suspensión definitiva contra el **embargo precautorio de cuentas bancarias** (arts. 40, fr. III y 40-A CFF) debe condicionarse a garantía conforme al **art. 135 de la Ley de Amparo**, por el monto de la determinación provisional — no basta que el crédito no sea firme para dispensarla. **Inferencia:** este criterio de 2024, sumado a la reforma de 2025, confirma que la suspensión "gratuita" en materia fiscal es cada vez más excepcional.

### 5.4 Síntesis comparada

| Vía | Norma | ¿Garantía para que surta efectos? | Plazo/nota |
|---|---|---|---|
| Recurso de revocación | Art. 144 CFF | Sí, salvo excepciones | No suspende al interponerse |
| Juicio contencioso (TFJA) | Art. 28 LFPCA | Sí, para determinación/cobro | Incidente ante magistrado instructor |
| Amparo indirecto | Art. 135 LAmp (reformado 2025) | Sí, billete de depósito o carta de crédito | Provisional en la misma audiencia |

---

## 6. Responsabilidad penal fiscal

### 6.1 Defraudación fiscal (art. 108 CFF)

"Comete el delito de defraudación fiscal quien, con uso de engaños o aprovechamiento de errores, omita total o parcialmente el pago de alguna contribución u obtenga un beneficio indebido en perjuicio del fisco federal" (fuente secundaria, nv oficial).

**Penas por monto (Anexo 5, RMF 2026 — grado C, no contra DOF):** 3 meses a 2 años si no excede **$2,531,920.00**; 2 a 5 años si excede eso sin pasar de **$3,797,870.00**; 3 a 9 años por encima; 3 meses a 6 años si el monto es indeterminable.

**Calificativas:** documentos falsos; omisión reiterada de expedir CFDI; datos falsos para devolución improcedente; no llevar registros contables o asentar datos falsos; omitir enterar retenciones; datos falsos para acreditar/disminuir contribuciones; dar efectos fiscales a comprobantes simulados.

**Atenuante:** restitución espontánea, en una sola exhibición, antes de que la autoridad descubra la omisión.

### 6.2 Defraudación equiparada (art. 109 CFF)

Mismas penas del 108 para quien: (I) consigne deducciones falsas o ingresos menores a los reales, o (persona física) tenga erogaciones superiores a sus ingresos declarados sin comprobar el origen — base de la **discrepancia fiscal**; (II) omita enterar contribuciones retenidas o recaudadas; (III) se beneficie sin derecho de un estímulo fiscal; (IV) simule actos o contratos con perjuicio al fisco — base penal de la simulación que también dispara el 69-B administrativo; (V) omita más de 12 meses declaraciones definitivas; (VIII) dé efectos fiscales a comprobantes que no reúnan requisitos.

**Excluyente:** no hay acción penal si el contribuyente entera espontáneamente lo adeudado antes de que la autoridad descubra la omisión.

### 6.3 Comprobantes fiscales falsos (art. 113 Bis CFF)

Reformado DOF **7-nov-2025**, vigente **1-ene-2026**: **2 a 9 años de prisión** a quien "expida, enajene, compre o adquiera comprobantes fiscales que amparen operaciones inexistentes, falsas o actos jurídicos simulados", y a quien "expida, enajene, compre, adquiera o **dé efectos fiscales**" a comprobantes falsos — este verbo amplía el tipo también a quien deduce o acredita sabiendo de la falsedad. Las plataformas digitales que permitan anuncios de compraventa de comprobantes enfrentan la misma pena; servidores públicos, además, destitución e inhabilitación de 1 a 10 años.

**Prisión preventiva oficiosa** por reforma constitucional al art. 19 (nv el texto exacto). **Inferencia:** con prisión oficiosa, el indiciado permanece detenido durante el proceso salvo excepción — la prevención documental (§2.2) vale más que la defensa posterior.

Requiere querella previa de la SHCP (art. 92, §6.4); puede perseguirse junto con el art. 400 Bis del Código Penal Federal (operaciones con recursos de procedencia ilícita).

### 6.4 Querella (art. 92 CFF)

La SHCP es víctima u ofendida en los procesos por delitos fiscales. Para los delitos de los arts. 105, 108, 109, 110, 111, 112 y 114, se requiere **querella previa de la SHCP**, "independientemente del estado" del procedimiento administrativo; para los arts. 102, 103 y 115, basta una declaración de perjuicio. La cuantificación del daño que haga la SHCP en la querella **solo surte efectos en lo penal** — de ahí que ganar el juicio de nulidad administrativo no cierre automáticamente el riesgo penal, ni viceversa: son vías independientes.

---

## 7. Traducción operable

### 7.1 Mapa de decisión

```
¿Es sentencia definitiva de un tribunal (TFJA u otro)?
├─ SÍ → Amparo directo (art. 170 LAmp), Tribunal Colegiado.
│        Si es favorable pero la autoridad interpuso revisión: amparo
│        directo solo contra la norma aplicada, condicionado a esa revisión.
└─ NO → ¿Acto administrativo definitivo (liquidación, 69-B/69-B Bis/49-Bis)?
         ├─ SÍ → ¿Hay ≤30 días hábiles y solo se busca anular el acto?
         │        ├─ Vía rápida y gratuita → Recurso de revocación
         │        │    (art. 116 CFF, 30 días, resuelve en 3 meses o ficta).
         │        └─ Litigio directo o autoridad no fiscal → Juicio
         │             contencioso ante el TFJA (art. 13 LFPCA, 30 días;
         │             elegir vía tradicional o en línea).
         └─ NO → ¿Acto de ejecución (embargo) o norma inconstitucional
                  aplicada por primera vez?
                  └─ SÍ → Amparo indirecto, Juzgado de Distrito, con
                       suspensión condicionada a garantía (art. 135 LAmp).
```

**Plazos de memoria:** 15 días para desvirtuar el 69-B; 5 días hábiles tras una visita del 49-Bis; 30 días hábiles para revocación y demanda ordinaria; 3 meses para negativa ficta.

### 7.2 Checklist previo a interponer cualquier medio de defensa

1. Fijar la fecha exacta de notificación y calcular el plazo fatal en días hábiles (art. 12 CFF), salvo que la norma diga naturales.
2. Reunir las cuatro capas de evidencia de materialidad antes de decidir entre desvirtuar o autocorregirse.
3. Calcular el costo de garantizar el interés fiscal antes de elegir vía: desde octubre de 2025 la suspensión gratuita es la excepción.
4. Verificar si el crédito ya es firme: si lo es, el amparo por cobro solo procede por violaciones procesales y solo hasta la convocatoria de remate.
5. Decidir revocación vs. juicio directo según el tiempo para reunir prueba, la previsibilidad de una negativa ficta, y el costo relativo.
6. Revisar si el acto está en el catálogo de prisión preventiva oficiosa antes de cualquier estrategia de "esperar y ver".
7. Confirmar si existe querella de la SHCP: sin ella no hay acción penal posible, aunque el procedimiento administrativo siga en paralelo.

---

## 8. Trampas y errores comunes

1. **CFDI ≠ protección.** Sin las otras tres capas de evidencia, la deducción cae ante cualquier auditoría (jurisprudencia VIII-J-1aS-115).
2. **Compensación universal ya no existe.** Un saldo a favor de IVA no puede usarse contra ISR desde 2019; planear caja con ese supuesto es un error real, no solo formal.
3. **Exento ≠ tasa 0%.** La exención bloquea el acreditamiento de insumos; cotizar un proyecto exento como si fuera tasa 0% subestima el costo.
4. **El 69-B se proyecta al futuro.** Confiar en que un proveedor "ya resolvió" porque el ejercicio auditado pasó ignora la jurisprudencia 2024206.
5. **No presupuestar la garantía.** Desde 2025 (y ya desde la jurisprudencia 2028811 de 2024 para embargos) litigar sin costear la fianza es litigar con un plan incompleto.
6. **Subestimar el 49-Bis.** Con solo 5 días hábiles de respuesta, sin carpeta de materialidad previa no da tiempo de reaccionar.
7. **Confundir el juicio de nulidad ganado con el riesgo penal cerrado.** Son vías independientes (art. 92 CFF).
8. **Confundir el art. 108 (engaño activo) con el 109 (a veces solo omisión, p. ej. no enterar retenciones).** La defensa cambia según el elemento subjetivo exigido.
9. **Usar el monto de defraudación de un año distinto al de los hechos.** Los montos del art. 108 se actualizan anualmente (Anexo 5).
10. **Creer que el amparo directo reabre el fondo de una sentencia ya ganada.** Solo ataca la constitucionalidad de la norma, condicionado a la revisión de la autoridad.

---

## 9. Autoevaluación

1. ¿Qué tres condiciones exige el art. 27, fr. III LISR para deducir un pago mayor a $2,000, y por qué combustibles no tiene ese piso?
2. Diferencia EFOS de EDOS y el plazo del EDOS para autocorregirse.
3. Cita el rubro y clave de la jurisprudencia del TFJA sobre insuficiencia del CFDI para acreditar materialidad.
4. ¿Qué efecto tiene, conforme al registro 2024206, la inclusión definitiva en el 69-B más allá del ejercicio auditado?
5. Diferencia funcionalmente CUFIN de CUCA; ¿qué pasa si un reembolso de capital excede la CUCA?
6. Enumera los cuatro métodos del art. 180 LISR en una frase cada uno.
7. ¿Cuándo se presume vinculación entre un residente en México y una entidad en REFIPRES?
8. ¿Cuántos días de presencia generan establecimiento permanente por obra, y qué pasa si hay subcontratistas?
9. ¿Por qué ya no es correcto decir que un saldo a favor de IVA se "compensa contra ISR"? ¿Desde cuándo?
10. Criterio para elegir entre recurso de revocación y juicio contencioso cuando ambos proceden y hay tiempo para ambos.
11. ¿Qué cambió en octubre de 2025 sobre la suspensión fiscal en amparo, y qué jurisprudencia de 2024 ya anticipaba esa tendencia?
12. Distingue el art. 108 del art. 109 CFF citando al menos una fracción de cada uno.
13. ¿Qué cambió el verbo "dé efectos fiscales" en el art. 113 Bis, y por qué importa la prisión preventiva oficiosa?
14. ¿Qué exige el art. 92 CFF antes de la acción penal, y qué relación tiene con el procedimiento administrativo paralelo?
15. ¿Qué procedimiento del CFF (69-B, 69-B Bis o 49-Bis) usarías si el objetivo de la autoridad es atacar la pérdida fiscal transmitida en una fusión, y por qué?

---

## 10. Fuentes

**Verificadas contra archivo de texto plano oficial (Cámara de Diputados, DOF 01-04-2024):**

1. LISR arts. 2, 3, 16, 17, 25, 27, 77, 90, 140, 179, 180 — `laboratorio/replicas/V05-spiva-y-fiscalidad-sic/datos/legal/LISR.txt` (fuente: https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf).

**Verificadas contra fuentes secundarias especializadas (no contra PDF oficial en esta sesión):**

2. CFF arts. 69-B, 69-B Bis, 92, 108, 109, 116, 121, 131 — https://leyes-mx.com/codigo_fiscal_de_la_federacion/ (69-B.htm, 69-B%20Bis.htm, 92.htm, 108.htm, 109.htm); https://mley.mx/CFF/articulo/116/ (consultadas 25-sep-2026).
3. LFPCA arts. 13, 28 — https://mley.mx/LFPCA/articulo/13/; https://leyes-mx.com/ley_federal_de_procedimiento_contencioso_administrativo/28.htm (25-sep-2026).
4. Ley de Amparo art. 170 — https://leyes-mx.com/ley_de_amparo_reglamentaria_de_los_articulos_103_y_107_de_la_constitucion_politica_de_los_estados_unidos_mexicanos/170.htm (25-sep-2026).
5. LIVA arts. 2-A, 5, 6, 9 — agregado sobre https://www.diputados.gob.mx/LeyesBiblio/pdf/LIVA.pdf y sdv.com.mx (25-sep-2026).
6. Ley Aduanera arts. 36, 47, 90 — https://leyes-mx.com/ley_aduanera/90.htm; https://reinoaduanero.mx/articulo-36-a-ley-aduanera... (25-sep-2026).

**Reformas 2025-2026 (confirmadas por ≥2 fuentes independientes con la misma fecha de DOF):**

7. Reforma CFF, DOF 07-11-2025, vigente 1-ene-2026 (69-B Bis, 113 Bis, 29-A fr. IX, 49-Bis, montos art. 108) — https://www.diputados.gob.mx/LeyesBiblio/ref/cff/CFF_ref62_07nov25.pdf; https://ruizconsultores.com.mx/blog/03-blog-nuevo-articulo-49-bis-cff-procedimiento-expres-fiscalizacion/; https://carbajalcontadores.com/2026/09/07/articulo-49-bis-cff-2026-auditoria-expres-sat-suspension-facturacion-cfdi.
8. Reforma Ley de Amparo + CFF + Ley Orgánica TFJA, DOF 16-10-2025, vigente 17-10-2025 — https://www.gtlaw.com/en/insights/2025/10/nueva-reforma-a-la-ley-de-amparo; https://pcga.mx/ideas/ley-amparo-materia-fiscal/.
9. Reforma LFPCA, DOF 09-06-2026, vigencia escalonada 10-jun-2026/6-dic-2026/4-feb-2027 — https://www.samanosc.com.mx/post/reforma-a-la-ley-federal-de-procedimiento-contencioso-administrativo-nuevos-plazos-y-reglas-procesa.
10. Anexo 5 RMF 2026, montos art. 108 (grado C) — convergencia de dos búsquedas citando $2,531,920.00 y $3,797,870.00.
11. Estímulo IEPS diésel, LIF 2026 art. 20-A — https://www.elfinanciero.com.mx/economia/2026/09/21/estimulo-complementario-al-diesel-alcanza-su-mayor-nivel-en-cuatro-anos-asi-queda-el-apoyo-de-hacienda/.
12. Decreto IMMEX, actualizaciones 2026 — https://www.camtomx.com/en/blog/programa-immex-actualizaciones-2026 (nv contra el Decreto oficial).

**Jurisprudencia (registro/clave verificados):**

13. TFJA, jurisprudencia **VIII-J-1aS-115** — texto oficial íntegro descargado de https://www.tfja.gob.mx/cesmdfa/sctj/tesis-pdf-detalle/45851/.
14. SCJN, 2a. Sala, **2a./J. 26/2020 (10a.), registro 2022083** — SJF Libro 78, sept-2020, T. I, p. 616.
15. SCJN, contradicción de tesis 9/2021, **registro 2024206** — SJF Libro 10, feb-2022.
16. Pleno Regional en Materia Administrativa, **registro 2028811**, publicada 17-may-2024.

**Documentos internos referenciados, no repetidos:**

17. `fiscal/01-personas-fisicas-actividad-empresarial.md` §§3.2-3.3, 4.1-4.3.
18. `conocimiento/27-fiscalidad-2026-y-estructura-sic.md` §2.3.
19. `conocimiento/24-politica-publica-regulacion-y-mercados.md` (aranceles EUA y T-MEC).

**Nota metodológica.** El PDF oficial de diputados.gob.mx para CFF, LIVA y Ley Aduanera no se pudo extraer legible con la herramienta de lectura web en esta sesión (devolvió metadatos binarios). El buscador oficial de tesis sjf2.scjn.gob.mx está protegido por Incapsula y bloqueó tanto la lectura directa como peticiones HTTP con encabezado de navegador; toda tesis SCJN aquí citada se verificó por convergencia de al menos dos fuentes secundarias que reportan el mismo registro, núcleo del rubro y fecha — no por lectura directa del Semanario Judicial. Confirmar el texto íntegro en sjf2.scjn.gob.mx o en bj.scjn.gob.mx con acceso humano antes de usar estas tesis en un escrito real.
