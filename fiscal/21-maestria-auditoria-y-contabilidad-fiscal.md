# 21 — Maestría en Contaduría: auditoría, dictamen fiscal y control interno

> Nivel: maestría (auditoría y contabilidad fiscal para el "despacho" del sistema) · Actualizado 2026-09-25 · Grado global: **A** en las claves y títulos exactos de las NIA vigentes y en el texto de los artículos del CFF citados (verificados contra transcripciones directas de despachos y colegios profesionales). **B** en los montos 2026 del art. 32-A/32-H CFF (verificados en dos fuentes independientes que citan el Anexo 5 de la RMF 2026, DOF 28-dic-2025, sin acceso al PDF oficial). **C** en el estado de adopción formal de la NIA-LCE por el IMCP: el folio existe y su título indica adopción, pero su contenido completo no pudo leerse (403). Esto no es asesoría profesional: es material de estudio con cita y fecha, que marca lo no verificado.

Capítulos y documentos relacionados, que aquí no se repiten: [27 Fiscalidad 2026 y estructura del SIC](../conocimiento/27-fiscalidad-2026-y-estructura-sic.md) (ISR de persona física en bolsa, no de persona moral) · `fiscal/20` (no existe en este repositorio: no hay nada que evitar repetir). Este capítulo abre la carpeta `fiscal/` con el primer documento de nivel maestría.

**Convenciones.** Hecho = lleva fuente y fecha. "**Inferencia:**" = razonamiento propio a partir de hechos verificados, sin fuente directa. "**Práctica profesional:**" = uso común en el ejercicio de la contaduría en México, no una norma con clave. "(nv)" = no verificado en esta sesión. NIA = Norma Internacional de Auditoría (traducción autorizada del IMCP de la ISA del IAASB/IFAC). NIF = Norma de Información Financiera (CINIF). CFF = Código Fiscal de la Federación. RMF = Resolución Miscelánea Fiscal. CPR o CPI = Contador Público Registrado o Inscrito ante el SAT. SIPRED = Sistema de Presentación del Dictamen de estados financieros para efectos fiscales.

---

## 1. Objetivos de dominio

1. Ubicar cada NIA citada en este capítulo con su número, título exacto y estatus de adopción en México por el IMCP, para poder planear una auditoría de estados financieros de una PyME o revisar un dictamen fiscal con el marco correcto.
2. Distinguir con precisión quién está **obligado** a dictaminarse para efectos fiscales, quién puede **optar** por hacerlo y quién no tiene ninguna de las dos cargas, con los montos vigentes en 2026 del art. 32-A CFF.
3. Explicar el valor legal del dictamen fiscal (presunción de certeza del art. 52 CFF) y su función como elemento de defensa vía la revisión secuencial del art. 52-A CFF.
4. Aplicar el marco COSO (2013) de control interno a una PyME constructora con equipo pequeño, incluyendo controles compensatorios cuando la segregación de funciones ideal no es posible.
5. Construir y leer razones financieras y un análisis de rentabilidad por proyecto de obra con costeo ABC, suficientes para presentar a un banco o para decidir internamente.
6. Calcular impuestos diferidos bajo NIF D-4 y conciliar la tasa efectiva de impuesto contra la tasa legal.
7. Saber qué es un dictamen pericial contable, cuándo se usa y qué lo distingue de un dictamen fiscal o de una auditoría de estados financieros.
8. Tener un checklist operable de auditoría interna previa al cierre fiscal y una lista de qué documentación conservar para blindarse ante el SAT o ante el propio auditor externo.

---

## 2. Normas Internacionales de Auditoría (NIA) adoptadas en México

### 2.1 Adopción y estructura general

El IMCP adoptó de forma integral las Normas Internacionales de Auditoría (ISA del IAASB/IFAC, traducidas como NIA) para las auditorías de estados financieros correspondientes a ejercicios que inician a partir del 1 de enero de 2012 [1][2]. El IMCP publica anualmente el volumen *Normas de Auditoría, para Atestiguar, Revisión y Otros Servicios Relacionados* (edición vigente: **2025**), que contiene la traducción autorizada de las NIA vigentes más la normatividad de la Comisión de Normas de Auditoría y Aseguramiento (CONAA): Normas para Atestiguar (serie 7000, NAT), Normas de Revisión (serie 9000, NR) y Normas para Otros Servicios Relacionados (serie 11000, NS) [2].

En diciembre de 2023 el IFAC/IAASB aprobó la emisión de una **Norma Internacional de Auditoría para Entidades Menos Complejas (NIA-LCE / ISA for LCE)**, un estándar independiente y proporcional a la complejidad de la entidad, distinto del conjunto completo de NIA. El IMCP tradujo la norma al español y la publicó en el sitio de la IFAC el 18-ene-2024, y emitió el **Folio 47/2023-2024**, titulado "Adopción de las Normas Internacionales de Auditoría para auditorías de estados financieros de Entidades Menos Complejas para los ejercicios contables que iniciarán a partir del 15 de diciembre de 2025" [3][4]. La norma aplica, por diseño del IAASB, a PyME privadas con estructuras simples, organizaciones sin fines de lucro sin operaciones complejas y entidades públicas pequeñas sin obligación pública significativa; **no aplica** a empresas que cotizan en bolsa, instituciones financieras reguladas ni grupos corporativos grandes o con operaciones complejas [4]. **Inferencia, con nota:** el título del folio del IMCP usa la palabra "Adopción", lo que indica que el instituto formalizó su incorporación al catálogo normativo mexicano; no se pudo leer el texto completo del folio (403 al acceder a imcp.org.mx) para confirmar si la aplicación queda como opción del auditor (según su juicio profesional de que la entidad es "menos compleja") o si requiere algún paso adicional de la CNBV para entidades reguladas. Es el hallazgo más relevante de este capítulo para un despacho pequeño: si un auditor decide que una PyME constructora califica como "entidad menos compleja", desde ejercicios que inicien a partir del 15-dic-2025 puede usar la NIA-LCE en vez del conjunto completo de NIA, con procedimientos más proporcionales.

### 2.2 Las cinco NIA centrales del ciclo de auditoría, con clave y título exacto

| Clave | Título exacto (traducción IMCP/NIA-ES) | Qué exige al auditor |
|---|---|---|
| **NIA 300** | Planificación de una Auditoría de Estados Financieros [5] | Desarrollar una estrategia global de auditoría que fije el alcance, el momento y la dirección de la auditoría, y un plan de auditoría detallado, antes de ejecutar procedimientos sustantivos. |
| **NIA 315 (Revisada en 2019)** | Identificación y Valoración de los Riesgos de Incorrección Material [6] | Obtener conocimiento de la entidad, su entorno y su sistema de control interno para identificar y valorar los riesgos de incorrección material, a nivel de los estados financieros y de las afirmaciones. Es la norma que sufrió una revisión sustancial del IAASB en 2019, aplicable a auditorías de periodos que comienzan a partir del 15-dic-2021, con un marco de valoración de riesgo más exigente y una guía de aplicación reorganizada. |
| **NIA 320** | Importancia Relativa o Materialidad en la Planificación y Ejecución de la Auditoría [7] | Fijar la materialidad para los estados financieros en su conjunto y, si aplica, materialidades de ejecución y para clases particulares de transacciones, saldos o revelaciones. |
| **NIA 500** | Evidencia de Auditoría [8] | Diseñar y aplicar procedimientos de auditoría (inspección, observación, confirmación externa, recálculo, reejecución, procedimientos analíticos e indagación) que obtengan evidencia suficiente y adecuada para las conclusiones. |
| **NIA 700 (Revisada)** | Formación de la Opinión y Emisión del Informe de Auditoría sobre los Estados Financieros [9] | Evaluar las conclusiones obtenidas de la evidencia y formarse una opinión sobre si los estados financieros están, en todos los aspectos materiales, de acuerdo con el marco de información financiera aplicable (en México, las NIF o, en su caso, las NIIF). |
| **NIA 705 (Revisada)** | Opinión Modificada en el Informe de Auditoría Emitido por un Auditor Independiente [9] | Regula cuándo y cómo se emite una opinión con salvedades, una opinión negativa (adversa) o una abstención de opinión. |
| **NIA 706 (Revisada)** | Párrafos de Énfasis y Párrafos sobre Otras Cuestiones en el Informe de Auditoría Emitido por un Auditor Independiente [9] | Regula la inclusión de párrafos adicionales al informe, sin modificar la opinión, para llamar la atención sobre un asunto ya presentado o revelado, o sobre un asunto relevante para entender la auditoría, el rol del auditor o el informe. |

**Inferencia sobre la secuencia lógica:** NIA 300 y NIA 315 son iterativas entre sí (la planeación inicial detona la evaluación de riesgos, que a su vez ajusta el plan); NIA 320 fija el filtro cuantitativo que decide qué incorrecciones importan; NIA 500 es el motor de recolección de evidencia a lo largo de todo el trabajo; y las NIA 700/705/706 gobiernan cómo se comunica el resultado. Un auditor que no documente materialidad (NIA 320) antes de diseñar procedimientos de NIA 500 no puede justificar por qué revisó una muestra y no otra.

### 2.3 Trampa de vigencia

Cualquier cita de "NIA 315" sin la coletilla "(Revisada en 2019)" describe, casi con certeza, la versión anterior a la revisión de 2019, que dejó de estar vigente. La NIA 315 (Revisada 2019) tiene una estructura de requerimientos distinta (más centrada en "qué" hacer, con guía de aplicación separada sobre "por qué" y "cómo") [6]. Al construir programas de auditoría o material de capacitación para el sistema, siempre citar el año de revisión de la norma.

---

## 3. Dictamen fiscal en México

### 3.1 Naturaleza jurídica

El dictamen fiscal es el informe que un Contador Público Registrado (CPR o CPI, "Contador Público Inscrito" en el texto del CFF) emite sobre si los estados financieros de un contribuyente están razonablemente presentados y, adicionalmente, sobre el cumplimiento de disposiciones fiscales relevantes, con fundamento en el art. 52 del CFF.

### 3.2 Quién está obligado y quién puede optar (art. 32-A CFF, 2026)

Desde la reforma de 2014, el dictamen dejó de ser obligatorio de forma general: se volvió **opción** del contribuyente [10]. La reforma de 2022 **reintrodujo una obligación** para contribuyentes grandes y para emisoras públicas, vigente en 2026 [11][14]. El artículo distingue tres situaciones:

**a) Opción de dictaminar** (primer párrafo del art. 32-A). Personas físicas con actividades empresariales y personas morales pueden **optar** por dictaminar sus estados financieros por contador público autorizado si, en el ejercicio inmediato anterior:
- obtuvieron ingresos acumulables superiores a **$157,785,270.00** (monto vigente en 2026), o
- el valor de su activo fue superior a **$124,650,380.00** (monto vigente en 2026), o
- tuvieron cuando menos **300 trabajadores** que les prestaron servicios en cada uno de los meses del ejercicio inmediato anterior [10][12].

Las entidades paraestatales federales no pueden ejercer esta opción, y la opción se manifiesta al presentar la declaración del ejercicio [12]. Estos montos se actualizan cada año (art. 17-A CFF) vía anexo de la RMF; para 2026 aparecen en el **Anexo 5 "Cantidades actualizadas del CFF"**, RMF 2026, DOF 28-dic-2025 [13] — **(B):** verificados en dos fuentes secundarias que citan el Anexo 5 literalmente, no en el PDF oficial, no localizado en esta sesión.

**b) Dictamen obligatorio.** Personas morales que tributan en el Título II de la LISR y que en el último ejercicio fiscal declarado consignaron en sus declaraciones normales ingresos acumulables iguales o superiores a **$2,013,710,870.00** (monto vigente en 2026, Anexo 5 RMF 2026) están obligadas a dictaminar [13][14]. También están obligadas las entidades cuyas acciones se coloquen entre el gran público inversionista en bolsa de valores, con independencia de su nivel de ingresos [11][13]. Esta obligación es la que reinstaló la reforma de 2022 (el umbral base en 2022 fue de $1,650,490,600.00, indexado cada año desde entonces) [11].

**c) Sin obligación ni opción ejercida.** El resto de las personas físicas con actividad empresarial y personas morales no tiene esta carga; pueden, en cambio, quedar sujetas a la Información Sobre Situación Fiscal (ISSIF, art. 32-H CFF) si superan un umbral de ingresos distinto y menor: **$1,103,204,520.00** en 2026 [13]. Quien está obligado a dictaminar, o quien ejerce la opción del art. 32-A, se tiene por cumplida automáticamente la obligación de presentar la ISSIF [11].

**Inferencia operable para el "despacho" del sistema:** una PyME constructora mexicana típica, salvo que sea un desarrollador o constructora muy grande (con ingresos de más de ~2,000 millones de pesos) o cotice en bolsa, no está obligada a dictaminarse. La decisión de dictaminarse (opción) es, para ese tamaño de empresa, una decisión de gobierno corporativo y de imagen crediticia, no una obligación legal.

### 3.3 SIPRED, plazos y estructura del formato (2026)

El dictamen se presenta a través del **Sistema de Presentación del Dictamen (SIPRED)**, con la e.firma del CPR, a más tardar el **15 de mayo** del año siguiente al que corresponda (el plazo se redujo de julio a mayo con la reforma de 2022) [11][12]. Para el ejercicio 2025, presentado en 2026, el sistema se identifica como **SIPRED'2025**. La RMF 2026 reorganizó los anexos que contienen los instructivos y formatos: lo que hasta la RMF 2025 era el **Anexo 16** (dictamen general, contribuyentes no financieros, "Tipo I") pasó a ser el **Anexo 18**, y lo que era el **Anexo 16-A** (sector financiero, "Tipo II") pasó a ser el **Anexo 19**, ambos publicados por el SAT el 19-ene-2026 [15][16]. **(B):** la renumeración se confirmó en un despacho fiscal (SDV Asesores) y coincide con la existencia de la URL oficial del SAT para el Anexo 18 de la RMF 2026; no se abrió el PDF completo del Anexo para verificar cada campo del formato.

### 3.4 Responsabilidad del CPR ante el SAT

**Requisitos para registrarse** (art. 52, fracción I, CFF): nacionalidad mexicana, título de contador público registrado ante la SEP, ser miembro de un colegio profesional reconocido por la SEP durante los tres años previos a la solicitud de registro, contar con certificación vigente expedida por un organismo certificador registrado ante la SEP y tener un mínimo de tres años de experiencia participando en la elaboración de dictámenes fiscales; además, estar al corriente en sus obligaciones fiscales conforme al art. 32-D CFF [17][18]. Los contadores extranjeros pueden registrarse conforme a los tratados internacionales aplicables [17].

**Obligación de informar delitos e incumplimientos** (art. 52, fracción III, tercer párrafo, CFF): si el CPR, derivado de la elaboración del dictamen, tiene conocimiento de que el contribuyente incumplió disposiciones fiscales o aduaneras, o realizó una conducta que pueda constituir un delito fiscal, debe informarlo a la autoridad conforme a las reglas de carácter general que emita el SAT [17][19].

**Responsabilidad penal (encubrimiento):** el art. 96, fracción III, del CFF hace responsable del delito de **encubrimiento** al CPR que, derivado de la elaboración del dictamen, tuvo conocimiento de un hecho probablemente constitutivo de delito y omitió informarlo conforme al art. 52, fracción III, tercer párrafo [19][20]. La pena por encubrimiento en el CFF va de **tres meses a seis años de prisión** [20].

**Sanciones administrativas al registro:** cuando el CPR no cumple las disposiciones del Código, su Reglamento o las reglas generales del SAT, o no aplica las normas o procedimientos de auditoría, la autoridad, previa audiencia, puede exhortarlo, amonestarlo o **suspender hasta por tres años los efectos de su registro**; procede la **cancelación definitiva** si hay reincidencia, si participó en la comisión de un delito fiscal, o si no exhibe los papeles de trabajo de la auditoría cuando la autoridad los requiere. En estos casos se avisa por escrito al colegio profesional y, en su caso, a la federación de colegios a la que pertenezca el CPR [17][21].

### 3.5 El dictamen como elemento de defensa: presunción de certeza y revisión secuencial

**Presunción de certeza** (art. 52, primer párrafo, CFF): se presumen ciertos, salvo prueba en contrario, los hechos afirmados en los dictámenes formulados por contadores públicos sobre los estados financieros de los contribuyentes, siempre que se cumplan los requisitos del propio artículo [17][22].

**Revisión secuencial** (art. 52-A CFF): cuando la autoridad fiscal, en ejercicio de sus facultades de comprobación, va a revisar a un contribuyente que dictaminó sus estados financieros, debe seguir un **orden secuencial**: primero requiere al CPR que formuló el dictamen la información y documentación relacionada; solo si esa información resulta insuficiente, la autoridad puede requerir directamente al contribuyente [23]. La autoridad tiene un plazo de **doce meses**, contado a partir de la notificación del requerimiento al CPR, para concluir la revisión del dictamen; si no emite la resolución correspondiente dentro de ese plazo, se entiende que no hay observaciones sobre la auditoría ni sobre las operaciones revisadas, y la autoridad pierde el derecho de actuar directamente con el contribuyente por los mismos hechos ya revisados [23][24].

**Inferencia central de valor de defensa:** para el contribuyente que dictamina, estas dos figuras (presunción de certeza + revisión secuencial) generan una **capa de protección procesal** que no tiene quien no dictamina: la autoridad no puede saltarse al CPR y llegar directo al contribuyente, y tiene un reloj corriendo. Esto no exime de la obligación sustantiva de pagar correctamente los impuestos; es una ventaja de forma y de proceso, no un blindaje de fondo.

### 3.6 Conservación de documentación (art. 30 CFF)

La contabilidad y la documentación relacionada deben conservarse durante **cinco años**, contados a partir de la fecha en que se presentaron o debieron presentarse las declaraciones relacionadas con ella [25]. Reglas especiales: (i) para actos cuyos efectos fiscales se prolongan en el tiempo, el plazo corre desde la declaración del último ejercicio en que se produjeron esos efectos; (ii) para documentación sujeta a un recurso o juicio, el plazo corre desde que quede firme la resolución que le ponga fin [25]. **Práctica profesional:** aunque la ley marca cinco años, muchos despachos recomiendan conservar los papeles de trabajo de actos con efectos fiscales prolongados (activos fijos con depreciación larga, pérdidas fiscales amortizables a 10 años, CUFIN, CUCA) por el plazo completo del efecto, no solo cinco años desde la última declaración relacionada — esto es coherente con la excepción de la propia ley, no una regla adicional inventada.

---

## 4. Control interno: marco COSO (2013)

### 4.1 Los cinco componentes y los 17 principios

El *Internal Control – Integrated Framework* de COSO (2013, vigente; sustituyó al marco de 1992) organiza el control interno en **cinco componentes** integrados entre sí, que en conjunto se desagregan en **17 principios** [26][27][28]:

| Componente | # de principios | Principios (resumen) |
|---|---|---|
| **Entorno de Control** | 5 (1-5) | (1) Compromiso con integridad y valores éticos; (2) el órgano de gobierno ejerce supervisión independiente del control interno; (3) la dirección establece estructuras, líneas de reporte y autoridad/responsabilidad; (4) compromiso de atraer, desarrollar y retener personas competentes; (5) la organización hace responsables a las personas de sus funciones de control interno |
| **Evaluación de Riesgos** | 4 (6-9) | (6) especifica objetivos con suficiente claridad para poder identificar y evaluar riesgos; (7) identifica y analiza riesgos para determinar cómo gestionarlos; (8) considera la probabilidad de fraude al evaluar riesgos; (9) identifica y evalúa cambios que podrían afectar significativamente el sistema de control interno |
| **Actividades de Control** | 3 (10-12) | (10) selecciona y desarrolla actividades de control que mitigan riesgos a niveles aceptables; (11) selecciona y desarrolla controles generales de tecnología; (12) despliega las actividades de control a través de políticas y procedimientos |
| **Información y Comunicación** | 3 (13-15) | (13) genera y usa información de calidad y relevante; (14) comunica internamente objetivos y responsabilidades de control interno; (15) comunica externamente asuntos que afectan el funcionamiento del control interno |
| **Actividades de Supervisión (Monitoreo)** | 2 (16-17) | (16) selecciona, desarrolla y realiza evaluaciones continuas y/o independientes; (17) evalúa y comunica oportunamente las deficiencias a los responsables de tomar acción correctiva |

**Regla del marco:** para que el control interno sea efectivo bajo COSO 2013, deben estar **presentes y funcionando** los cinco componentes, y funcionar **de manera integrada** entre sí; no basta con que cada uno exista por separado [26].

### 4.2 Aplicación práctica en una PyME constructora con equipo pequeño

Una constructora chica no tiene, ni puede tener, la separación de funciones de una empresa grande (la misma persona que compra material también recibe la factura y programa el pago). COSO no exige una plantilla mínima de personal; exige que los **riesgos** que la falta de segregación crea estén cubiertos por **controles compensatorios**:

- **Entorno de control (Principios 1, 3).** Código de conducta y reglas de autorización de gastos por escrito, aunque breves, fijadas por el dueño/director general.
- **Evaluación de riesgos (Principio 8).** Antes de cada obra, identificar riesgos propios del proyecto: sobreprecio de proveedores ligados al personal de compras, doble pago de facturas, y estimaciones de avance que no corresponden al avance físico real — este último es un riesgo de fraude agudo en construcción porque el "avance de obra" es un juicio, no un hecho verificable con un solo documento.
- **Actividades de control compensatorias, con equipo pequeño:** doble firma en pagos por encima de un monto fijado (el dueño o el despacho contable como segundo firmante); conciliación bancaria revisada por alguien distinto de quien registra o autoriza pagos; corte físico de obra validado en campo por una persona distinta de quien elabora el número financiero que sustenta la estimación; rotación o revisión periódica de que existan varias cotizaciones de proveedor en compras relevantes; acceso a la banca electrónica separado en roles de consulta, captura y autorización, aunque sean solo dos o tres personas en total.
- **Información y comunicación (Principios 13-14).** Reporte mensual de avance físico vs. financiero por obra, dirigido al dueño y no solo al residente o al administrativo.
- **Supervisión (Principios 16-17).** El despacho contable externo, en su visita periódica, hace una revisión analítica básica: ¿el gasto de nómina de obra es coherente con el avance reportado?, ¿hay pagos a proveedores nuevos sin cotización?, ¿las estimaciones están firmadas por el cliente o el supervisor de obra?

**Práctica profesional:** en una PyME, el control compensatorio más eficaz suele ser un tercero externo (el despacho contable, un consejo asesor, un familiar sin operación diaria) que revisa periódicamente lo que la falta de personal impide segregar. Esto no sustituye el control interno; reduce el riesgo cuando la segregación ideal es económicamente inviable.

---

## 5. Contabilidad de costos avanzada y finanzas corporativas para PyME

### 5.1 Costeo ABC (Activity-Based Costing) en construcción

El costeo tradicional por absorción, que prorratea costos indirectos con una sola base (horas-hombre o costo directo de material), distorsiona la rentabilidad real de cada obra cuando los proyectos son heterogéneos en tamaño, duración o complejidad: es un problema documentado específicamente en obras civiles y de edificación, donde el costeo tradicional maneja mal los costos indirectos y generales de obra [29][30]. El costeo ABC asigna los costos indirectos a **actividades** (gestión de permisos, supervisión técnica, logística de materiales, control de calidad, administración de subcontratistas) y de ahí a cada obra según su consumo real de esa actividad (el "inductor de costo" o *cost driver*), en vez de un prorrateo único [30][31].

**Aplicación operable:** (1) identificar las actividades indirectas que consumen una proporción significativa del gasto general — típicamente supervisión técnica, logística/fletes, administración de obra y trámites; (2) elegir un inductor defendible por actividad (horas de supervisión por obra, viajes de material, monto de subcontratos administrados); (3) calcular el costo por unidad de inductor y aplicarlo a cada obra según su consumo real; (4) comparar el margen de cada obra bajo ABC contra el prorrateo tradicional. **Inferencia:** las obras pequeñas y dispersas casi siempre resultan menos rentables bajo ABC de lo que parecían bajo el prorrateo tradicional, porque consumen desproporcionadamente supervisión y logística respecto de su tamaño; las obras grandes y concentradas suelen mejorar su margen aparente. Es la razón práctica para migrar a ABC: decide mejor si conviene tomar obras chicas dispersas o concentrarse en menos obras más grandes.

### 5.2 Capital de trabajo en obra

El capital de trabajo (activo circulante menos pasivo circulante) en construcción tiene una particularidad crítica frente a otras industrias: gran parte del activo circulante no es "efectivo ni por cobrar en sentido estricto" sino **estimaciones de obra por cobrar** y, del lado del inventario, **obra en proceso**. Bajo NIF D-7 (Contratos de construcción y de fabricación de ciertos bienes de capital), el método reconocido para el reconocimiento de ingresos y costos en contratos de construcción es el de **por ciento de avance**: los ingresos y sus costos relacionados se reconocen conforme avanza el contrato, comparando el avance físico/técnico contra los costos incurridos; si las estimaciones más recientes indican que el costo total del contrato superará el ingreso total del contrato, la pérdida esperada debe reconocerse de inmediato y en su totalidad en el periodo en que se vuelve evidente [32][33]. **Práctica profesional:** el ciclo de conversión de efectivo de una constructora suele ser largo porque paga mano de obra y materiales de forma casi inmediata, pero cobra estimaciones con retraso (revisión y aprobación del cliente, retenciones contractuales de garantía) — por eso el capital de trabajo de una constructora debe planearse con una reserva de liquidez mayor a la que sugeriría solo el margen del proyecto.

### 5.3 Razones financieras clave para banco o decisión interna

Conjunto mínimo que un banco pide o que una dirección debe monitorear (fórmulas de uso estándar en finanzas corporativas, no claves normativas con número) [34][35]:

| Razón | Fórmula | Qué mide |
|---|---|---|
| Razón circulante | Activo circulante / Pasivo circulante | Capacidad de cubrir obligaciones de corto plazo con activos de corto plazo |
| Prueba del ácido | (Activo circulante − Inventarios) / Pasivo circulante | Liquidez inmediata, sin depender de vender inventario (en construcción, sin depender de que la obra en proceso se convierta en efectivo) |
| Rotación de cuentas por cobrar | Ventas a crédito / Cuentas por cobrar promedio | Eficiencia de cobranza; en construcción, de cobro de estimaciones |
| Días de cuentas por cobrar | 365 / Rotación de cuentas por cobrar | Plazo real de cobro, comparado contra el plazo contractual pactado |
| Razón de deuda a capital (apalancamiento) | Pasivo total / Capital contable | Qué proporción del negocio está financiada con deuda frente a recursos propios |
| Margen EBITDA por obra | EBITDA de la obra / Ingresos de la obra | Rentabilidad operativa de cada proyecto antes de estructura financiera y fiscal — el número que conecta directamente con el costeo ABC de la sección 5.1 |

**Práctica profesional:** para PyME en crecimiento, se recomienda calcular estas razones **mensualmente**; para negocios ya estables, trimestralmente; en periodos de estrés (por ejemplo, una obra grande con estimaciones detenidas), monitoreo semanal de liquidez [35].

---

## 6. Impuestos diferidos avanzado (NIF D-4)

### 6.1 Marco normativo

El CINIF emitió la **NIF D-4, "Impuestos a la utilidad"**, vigente desde ejercicios que inician a partir del 1 de enero de 2008 (sustituyó al Boletín D-4 anterior) [36]. El método reconocido es el de **activos y pasivos**: el impuesto diferido se determina tomando como base las diferencias temporales entre los valores contables y los valores fiscales de activos y pasivos, más las pérdidas fiscales por amortizar y los créditos fiscales, multiplicando esa suma por la tasa de impuesto que se espera esté vigente cuando la diferencia se revierta [36][37].

### 6.2 Diferencias temporales

Una diferencia temporal surge cuando el valor contable (NIF) de un activo o pasivo difiere de su valor fiscal (LISR), y esa diferencia se revertirá en el futuro generando un efecto fiscal. Ejemplos comunes en una PyME constructora:
- **Depreciación fiscal acelerada vs. contable** (activo fijo con tasas de depreciación fiscal distintas a la vida útil contable) — genera pasivo por impuesto diferido si la depreciación fiscal es mayor a la contable en los primeros años.
- **Ingresos por obra reconocidos contablemente por avance de obra (NIF D-7) antes de ser exigibles fiscalmente**, o viceversa, si el momento de acumulación fiscal de ingresos de construcción difiere del momento contable — genera activo o pasivo por impuesto diferido según el sentido de la diferencia.
- **Estimaciones y provisiones contables no deducibles hasta que se cumplan requisitos fiscales** (por ejemplo, provisión contable de garantías de obra, deducible fiscalmente hasta que efectivamente se eroga) — genera activo por impuesto diferido.
- **Pérdidas fiscales por amortizar** — generan un activo por impuesto diferido, sujeto a una estimación de recuperabilidad: solo se reconoce en la medida en que sea probable que existan utilidades fiscales futuras suficientes para aplicarlas.

### 6.3 Tasa efectiva de impuesto y su conciliación

La **tasa efectiva de impuesto** es el resultado de dividir el impuesto a la utilidad total del periodo (impuesto causado + impuesto diferido) entre la utilidad antes de impuestos [36]. NIF D-4 exige revelar la tasa efectiva y su **conciliación con la tasa legal** (en México, la tasa general de ISR de personas morales es 30%), explicando las partidas que provocan que la tasa efectiva se aparte de la tasa legal: partidas no deducibles (por ejemplo, ciertos gastos no estrictamente indispensables, previsión social excedida de límites), ingresos no acumulables, efectos de inflación fiscal (ajuste anual por inflación), diferencias permanentes entre la utilidad contable y la fiscal, y el efecto de estimaciones por irrecuperabilidad de activos por impuesto diferido [36][37].

**Práctica profesional:** una conciliación bien hecha es, en sí misma, una herramienta de auditoría interna: si la tasa efectiva de una PyME constructora se aleja mucho y de forma no explicada del 30% legal, es señal de que hay partidas no deducibles grandes y recurrentes (gastos mal documentados, sin CFDI, o no estrictamente indispensables) que conviene corregir antes de que las detecte el SAT.

---

## 7. Peritajes contables básicos

Un **dictamen pericial contable** (o peritaje contable) es un documento emitido por un experto en contabilidad, nombrado o designado dentro de un proceso judicial, arbitral o administrativo, que analiza, interpreta y valora hechos financieros, económicos o patrimoniales en disputa, y que se ofrece como **medio de prueba** en el proceso [38][39]. A diferencia del dictamen fiscal (dirigido al SAT, con presunción de certeza legal propia del art. 52 CFF) o de una auditoría de estados financieros (dirigida a usuarios generales de la información financiera bajo NIA), el dictamen pericial contable está dirigido a una **autoridad judicial** (civil, mercantil, familiar, penal) y responde a puntos específicos planteados por las partes o por el juez, no a la razonabilidad general de los estados financieros [38].

**Cuándo se usa:** típicamente para comprobar el saldo cierto de una cuenta, el correcto registro de operaciones en litigio, determinar un daño patrimonial cuantificable, valuar una empresa o participación societaria en un litigio societario o de divorcio, o verificar el cumplimiento de un contrato con obligaciones económicas medibles [38][39]. Su elaboración exige el análisis del expediente completo (demanda, contestación, pruebas ofrecidas) y ceñirse estrictamente al alcance específico del encargo fijado por el juez o por las partes [38]. **(nv):** no se verificó en esta sesión el artículo específico del Código Nacional de Procedimientos Civiles y Familiares (de reciente adopción gradual en México) que regula el nombramiento y desahogo de la prueba pericial; el uso de la prueba pericial contable en materia mercantil y penal sigue, según el estado procesal de cada entidad, el Código de Comercio o el Código Nacional de Procedimientos Penales respectivamente, no verificado en detalle aquí.

---

## 8. Traducción operable

### 8.1 Checklist anual de auditoría interna previa al cierre fiscal

1. **Conciliaciones bancarias** de todas las cuentas, al mes de cierre, revisadas por alguien distinto de quien las elabora.
2. **Confirmación de saldos** con los tres o cinco clientes y proveedores más relevantes (o con quien concentre exposición significativa), aunque no sea obligatorio (es práctica de auditoría, no requisito fiscal).
3. **Inventario físico de obra en proceso** cotejado contra el registro contable de avance de obra (NIF D-7): revisar que las estimaciones facturadas correspondan al avance físico real validado por el residente de obra.
4. **Revisión de CFDI recibidos vs. gastos registrados**: que cada gasto deducible tenga CFDI válido, con los requisitos fiscales completos, y que no haya gastos sin comprobante o con comprobantes de proveedores en listas negras del SAT (art. 69-B CFF — verificar directamente en el listado del SAT antes del cierre).
5. **Cálculo preliminar de la tasa efectiva de impuesto** (sección 6.3) para detectar partidas no deducibles grandes antes del cierre, cuando aún hay tiempo de documentarlas o corregirlas.
6. **Revisión de pérdidas fiscales por amortizar** y su plazo de vigencia (diez ejercicios en LISR), para no perder el derecho a aplicarlas.
7. **Revisión de impuestos diferidos** (activos y pasivos, NIF D-4): que las diferencias temporales estén identificadas y que la estimación de recuperabilidad de pérdidas fiscales esté sustentada con proyecciones razonables.
8. **Revisión de nómina y outsourcing**: cumplimiento de la reforma de subcontratación (REPSE) si aplica, y de retenciones de ISR e IMSS.
9. **Revisión de contratos de obra vigentes**: que estén firmados, con anexos técnicos y de precios, y que respalden el reconocimiento contable de ingresos bajo el método de por ciento de avance.
10. **Revisión de las actividades de control compensatorias** listadas en la sección 4.2: ¿se aplicó la doble firma en pagos grandes durante todo el año?, ¿hubo excepciones no documentadas?
11. **Comparación de la utilidad fiscal contra la utilidad contable** y explicación documentada de cada diferencia relevante (la base misma de la conciliación de la sección 6.3).
12. Si la empresa dictamina (opción del art. 32-A), revisar que los papeles de trabajo del CPR estén completos y disponibles: recordar que no exhibirlos ante un requerimiento de la autoridad es causal de cancelación definitiva del registro del CPR (sección 3.4) y deja al contribuyente sin la protección de la revisión secuencial.

### 8.2 Documentación que la empresa debe conservar para blindarse

- Contabilidad completa y CFDI (ingresos y egresos), por **cinco años** desde la declaración relacionada (art. 30 CFF), y más tiempo si el efecto fiscal se prolonga (activo fijo, pérdidas fiscales, CUFIN/CUCA) o si hay litigio en curso sobre el concepto.
- Contratos de obra, convenios modificatorios, bitácoras de obra y estimaciones firmadas por el cliente o supervisor externo — son el respaldo del reconocimiento de ingresos bajo NIF D-7 y de las partidas más frecuentemente cuestionadas por el SAT en construcción (¿la estimación corresponde a avance real?).
- Papeles de trabajo de impuestos diferidos: cédulas de diferencias temporales, cálculo de la tasa efectiva y su conciliación (NIF D-4), porque son la primera pieza que un auditor externo o el propio SAT revisa para detectar inconsistencias.
- Evidencia de las actividades de control compensatorias (bitácoras de doble firma, correos de autorización, reportes de conciliación revisados) — sin esta evidencia, un control "existe" solo de palabra, y COSO exige que el control esté "presente y funcionando", no solo diseñado.
- Si la empresa dictamina: papeles de trabajo del CPR completos y disponibles, porque son el primer punto de contacto de la autoridad en la revisión secuencial (art. 52-A CFF).

---

## 9. Trampas y errores comunes

1. **Citar "NIA 315" sin decir "(Revisada 2019)".** La revisión de 2019 cambió sustancialmente la estructura de la norma; el número solo no basta.
2. **Confundir "dictamen fiscal obligatorio" con "dictamen fiscal en general".** Desde 2014 el dictamen es opcional para la generalidad; la obligación reintroducida en 2022 aplica solo a contribuyentes muy grandes (ingresos de más de dos mil millones de pesos en 2026) o a emisoras públicas. Una PyME casi nunca está en ese supuesto.
3. **Confundir el umbral de la opción (art. 32-A, ~$157.8 millones / ~$124.6 millones) con el umbral de la obligación (~$2,013.7 millones) o con el de la ISSIF (~$1,103.2 millones).** Son tres cifras distintas con tres consecuencias distintas.
4. **Creer que dictaminar exime de pagar correctamente los impuestos.** La presunción de certeza es "salvo prueba en contrario" y la revisión secuencial es una protección de forma y de plazo, no de fondo.
5. **Tratar la segregación de funciones ideal de COSO como un requisito absoluto imposible de cumplir en una PyME, y por eso no implementar nada.** El marco exige gestionar el riesgo, no clonar la estructura de una empresa grande; los controles compensatorios (revisión de un tercero externo, doble firma, conciliaciones cruzadas) son la respuesta correcta, no la excusa para no tener control interno.
6. **Prorratear costos indirectos de obra con una sola base (por ejemplo, solo costo directo) y creer que el margen resultante por proyecto es correcto.** El costeo ABC suele revelar que obras chicas y dispersas son menos rentables de lo que el prorrateo tradicional sugiere.
7. **Reconocer ingresos de obra por el monto facturado en vez de por el avance real (NIF D-7).** Facturar una estimación no es lo mismo que haber generado el ingreso contable; hacerlo mal distorsiona tanto los estados financieros como el cálculo de impuestos diferidos.
8. **Reconocer una pérdida esperada de un contrato de obra "cuando se materialice" en vez de inmediatamente al volverse evidente.** NIF D-7 exige reconocerla de inmediato y en su totalidad, no de forma gradual.
9. **Confundir un dictamen pericial contable con un dictamen fiscal o con una auditoría de estados financieros.** Tienen destinatarios, alcance y efectos legales distintos.
10. **No exhibir los papeles de trabajo cuando el SAT los requiere al CPR.** Es causal expresa de cancelación definitiva del registro del CPR, no solo de suspensión.
11. **Calcular la tasa efectiva de impuesto sin conciliarla contra la tasa legal.** La cifra sola no dice nada; la conciliación es la que revela partidas no deducibles recurrentes que conviene corregir.
12. **Suponer que existe una "NIF para PyMES" obligatoria y distinta en México, como el IFRS for SMEs internacional.** No existe una norma diferenciada y obligatoria; las PyME mexicanas aplican las mismas NIF que las grandes empresas (con el Régimen de Revelaciones Reducido del CINIF como único esfuerzo de simplificación identificado en esta sesión, sin verificar en detalle su alcance) (nv).

---

## 10. Autoevaluación

1. ¿Cuál es la diferencia entre la NIA 300 y la NIA 315 (Revisada 2019) en el ciclo de una auditoría?
   *Respuesta:* NIA 300 exige construir la estrategia global y el plan de auditoría; NIA 315 exige, antes y durante esa planeación, obtener conocimiento de la entidad y su control interno para identificar y valorar los riesgos de incorrección material que la estrategia debe atender. Son iterativas: los riesgos identificados con NIA 315 ajustan el plan de NIA 300.

2. Una empresa mexicana tuvo ingresos acumulables de $140 millones de pesos en 2025. ¿Está obligada a dictaminarse en 2026?
   *Respuesta:* No. Está por debajo del umbral de la **opción** de dictaminar ($157,785,270 en 2026), así que ni siquiera puede optar por ese criterio de ingresos (salvo que cumpla el criterio de activo o de 300 trabajadores). No está ni obligada ni tiene la opción de ingresos disponible.

3. ¿Qué diferencia hay entre el umbral del art. 32-A CFF para la obligación de dictaminar y el umbral del art. 32-H CFF para la ISSIF?
   *Respuesta:* El de la obligación de dictaminar (2026: ~$2,013.7 millones) es más alto que el de la ISSIF (2026: ~$1,103.2 millones). Quien está obligado a dictaminar, o quien opta por dictaminar, se tiene por cumplida automáticamente la obligación de la ISSIF.

4. ¿Qué protege al contribuyente que dictamina, frente a uno que no dictamina, cuando lo audita el SAT?
   *Respuesta:* La presunción de certeza de los hechos afirmados en el dictamen (art. 52 CFF, salvo prueba en contrario) y la revisión secuencial (art. 52-A CFF): la autoridad debe requerir primero al CPR y tiene doce meses para concluir esa revisión antes de poder ir directamente al contribuyente por los mismos hechos.

5. ¿Qué le pasa al CPR que detecta, al dictaminar, que su cliente cometió un delito fiscal y no lo informa a la autoridad?
   *Respuesta:* Puede ser responsable del delito de encubrimiento (art. 96, fracción III, CFF), con pena de tres meses a seis años de prisión, además de exponerse a sanciones administrativas sobre su registro (suspensión hasta por tres años o cancelación definitiva).

6. Enumera los cinco componentes de COSO 2013 y di cuántos principios tiene cada uno.
   *Respuesta:* Entorno de Control (5), Evaluación de Riesgos (4), Actividades de Control (3), Información y Comunicación (3), Actividades de Supervisión (2). Total: 17.

7. En una constructora con solo dos personas en administración, ¿cómo se compensa la falta de segregación de funciones en el manejo de pagos a proveedores?
   *Respuesta:* Con un control compensatorio, por ejemplo doble firma para pagos por encima de un monto fijado (con un tercero externo como segundo firmante si no hay una tercera persona interna) y conciliaciones bancarias revisadas por alguien distinto de quien captura o autoriza los pagos.

8. ¿Por qué el costeo tradicional por absorción puede sobrestimar la rentabilidad de las obras pequeñas y dispersas de una constructora?
   *Respuesta:* Porque prorratea los costos indirectos (supervisión, logística, administración de obra) con una sola base, sin reflejar que las obras chicas y dispersas consumen desproporcionadamente esas actividades respecto de su tamaño. El costeo ABC, al asignar el costo por actividad real consumida, suele revelar un margen menor en esas obras.

9. Bajo NIF D-7, ¿cuándo se reconoce una pérdida esperada de un contrato de construcción?
   *Respuesta:* De inmediato y en su totalidad, en el periodo en que se vuelve evidente que el costo total del contrato superará el ingreso total del contrato — no de forma gradual conforme avanza la obra.

10. ¿Qué es la tasa efectiva de impuesto bajo NIF D-4 y para qué sirve conciliarla contra la tasa legal?
    *Respuesta:* Es el impuesto a la utilidad total del periodo (causado + diferido) entre la utilidad antes de impuestos. Conciliarla contra la tasa legal (30% en personas morales) revela qué partidas (no deducibles, ingresos no acumulables, efectos inflacionarios, estimaciones de irrecuperabilidad) explican la diferencia, lo que sirve como señal de alerta de riesgos fiscales antes del cierre.

11. ¿En qué se diferencia un dictamen pericial contable de un dictamen fiscal?
    *Respuesta:* El dictamen pericial contable está dirigido a una autoridad judicial dentro de un litigio y responde a puntos específicos del proceso, como medio de prueba; el dictamen fiscal está dirigido al SAT, tiene presunción de certeza bajo el art. 52 CFF y opina sobre la razonabilidad de los estados financieros y el cumplimiento fiscal en general, no sobre un litigio.

12. ¿Qué es la NIA-LCE y a qué tipo de entidades aplica?
    *Respuesta:* Es la Norma Internacional de Auditoría para Entidades Menos Complejas, un estándar independiente del conjunto completo de NIA, aprobado por el IAASB/IFAC en diciembre de 2023 y con folio de adopción del IMCP para ejercicios que inicien a partir del 15 de diciembre de 2025. Aplica a PyME privadas con estructuras simples, OSC sin operaciones complejas y entidades públicas pequeñas; no aplica a emisoras públicas, instituciones financieras reguladas ni grupos corporativos grandes.

13. ¿Cuánto tiempo debe conservarse la contabilidad conforme al art. 30 CFF, y qué excepción aplica a un activo fijo que se sigue depreciando?
    *Respuesta:* Cinco años desde la fecha en que se presentaron o debieron presentarse las declaraciones relacionadas. Para actos con efectos fiscales prolongados (como la depreciación de un activo fijo), el plazo corre desde la declaración del último ejercicio en que se produjeron esos efectos, no desde la compra del activo.

14. ¿Qué pasa si la autoridad fiscal no concluye la revisión secuencial de un dictamen dentro de los doce meses del art. 52-A CFF?
    *Respuesta:* Se entiende que no hay observaciones sobre la auditoría practicada ni sobre las operaciones revisadas, y la autoridad pierde el derecho de actuar directamente con el contribuyente por los mismos hechos ya revisados.

15. Nombra tres razones financieras que un banco típicamente pide a una PyME constructora y qué mide cada una.
    *Respuesta:* Razón circulante (capacidad de cubrir pasivo de corto plazo con activo de corto plazo), prueba del ácido (liquidez inmediata sin depender de vender obra en proceso/inventario) y razón de deuda a capital (qué proporción del negocio está financiada con deuda frente a recursos propios). Otras válidas: rotación/días de cuentas por cobrar, margen EBITDA por obra.

---

## 11. Fuentes

1. IMCP, adopción integral de las NIA en México desde ejercicios a partir del 1-ene-2012: https://mexico.unir.net/noticias/economia/normas-internacionales-auditoria/ (25-sep-2026)
2. IMCP, "Normas de Auditoría" (series NAT 7000, NR 9000, NS 11000; edición 2025): https://imcp.org.mx/normas-de-auditoria/ · https://tienda.imcp.org.mx/auditoria (25-sep-2026)
3. AMCP, "Norma Internacional de Auditoría para Entidades Menos Complejas (NIA-LCE)": https://amcpdf.org.mx/norma-internacional-de-auditoria-para-auditorias-de-estados-financieros-de-entidades-menos-complejas-nia-lce/ (25-sep-2026)
4. IMCP, Folio 47/2023-2024, "Adopción de las NIA para Entidades Menos Complejas... a partir del 15 de diciembre de 2025": https://imcp.org.mx/folio-no-47-2023-2024-adopcion-de-las-normas-internacionales-de-auditoria-para-auditorias-de-estados-financieros-de-entidades-menos-complejas-para-los-ejercicios-contables-que-iniciaran-a-partir-del/ (título confirmado por buscador; 403 al abrir, 25-sep-2026)
5. NIA 300, "Planificación de una Auditoría de Estados Financieros" (texto NIA-ES): https://www.icjce.es/adjuntos/niaes-300.pdf (25-sep-2026)
6. IAASB, "NIA 315 (Revisada en 2019)": https://www.iaasb.org/publications/nia-315-revisada-en-2019-identificacion-y-valoracion-de-los-riesgos-de-incorreccion-material · adopción IMCP, Folio 96: https://test2.imcp.org.mx/wp-content/uploads/2021/08/Anexo-1-Folio-96.-NIA-315-Revisada-2019-y-modificaciones-de-concordancia-y-en-consecuencia-a-otras-normas-internacionales-que-surgen-de-la-NIA-315-Revisada-2019.pdf (25-sep-2026)
7. NIA 320, "Importancia relativa o materialidad en la planificación y ejecución de la auditoría" (NIA-ES): https://www.icac.gob.es/node/68 (25-sep-2026)
8. NIA 500, "Evidencia de Auditoría": https://www.icjce.es/adjuntos/niaes-500.pdf · IMCP: https://imcp.org.mx/evidencia-de-auditoria/ (25-sep-2026)
9. NIA 700 (Revisada), 705 (Revisada) y 706 (Revisada): https://vlex.com.mx/vid/nia-700-revisada-formacion-866668780 · https://www.icjce.es/adjuntos/niaes-705r.pdf (25-sep-2026)
10. IDC, "Dictamen fiscal ¿opcional para todos?" (reforma 2014): https://idconline.mx/fiscal/2015/06/19/dictamen-fiscal-opcional-para-todos (25-sep-2026)
11. Carbajal Contadores, "Dictamen Fiscal SAT 2026 (Art. 32-A CFF) e ISSIF (Art. 32-H)": https://carbajalcontadores.com/2026/09/05/dictamen-fiscal-sat-2026-art-32-a-cff-issif-obligados-limites-ingresos-plazos-multas (25-sep-2026)
12. mLey.mx, art. 32-A CFF: https://mley.mx/CFF/articulo/32-a/ (25-sep-2026)
13. AMCPMX, "Anexo 5 «Cantidades actualizadas del CFF» RMF 2026, DOF 28/12/2025": https://www.amcp.mx/anexo-5-cantidades-actualizadas-del-cff-rmf-2026-dof-28-12-2025/ (25-sep-2026)
14. Snippet de buscador sobre la reforma 2022 al art. 32-A CFF (sin URL única verificable) (25-sep-2026)
15. SAT, "Anexo 18 de la RMF 2026" (SIPRED'2025 Tipo I): https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rmf/anexos/Anexo_18_RMF2026-19012026.pdf (URL oficial confirmada, contenido no revisado a detalle, 25-sep-2026)
16. SDV Asesores, "Anexos RMF 2026: Dictamen fiscal": https://sdv.com.mx/compendio/anexos-rmf-2026/anexo-16/ (25-sep-2026)
17. leyes-mx.com, art. 52 CFF: https://leyes-mx.com/codigo_fiscal_de_la_federacion/52.htm (25-sep-2026)
18. Colegio de Contadores Públicos de Guadalajara, "Artículo 52 CFF: requisitos del CPI": https://ccpg.org.mx/2023/05/05/codigo-fiscal-de-la-federacion-articulo-52-requisitos-para-que-el-cpi-emita-dictamen-fiscal/ (25-sep-2026)
19. elConta.mx, "Dictamen Fiscal y la responsabilidad penal del auditor y/o dictaminador" (arts. 52 fr. III y 96 fr. III CFF): https://elconta.mx/dictamen-fiscal-y-la-responsabilidad-penal-del-auditor-y-o-dictaminador/ (25-sep-2026)
20. BADO.mx, art. 96 CFF (encubrimiento): https://bado.mx/articulos/1230/codigo-fiscal-de-la-federacion/articulo-96-responsables-de-encubrimiento-en-los-delitos-fiscales/ (25-sep-2026)
21. Reglamento del CFF, texto oficial: https://www.diputados.gob.mx/LeyesBiblio/regley/Reg_CFF.pdf (25-sep-2026)
22. SAT, ficha temática art. 52 CFF: http://omawww.sat.gob.mx/fichas_tematicas/dictamen_fiscal_info_alternativa/Paginas/ARTICULO_52_CFF.aspx (503 al cargar, 25-sep-2026)
23. COEM, "La revisión secuencial de un dictamen fiscal debe ser en 12 meses" (art. 52-A CFF): https://coem.mx/revision-secuencial-en-12-meses/ (25-sep-2026)
24. leyes-mx.com, art. 52-A CFF: https://leyes-mx.com/codigo_fiscal_de_la_federacion/52-A.htm (25-sep-2026)
25. csnsc.com.mx, "Análisis del Artículo 30 del CFF": https://csnsc.com.mx/analisis-del-articulo-30-del-cff-obligaciones-de-conservacion/ · mLey.mx: https://mley.mx/CFF/articulo/30/ (25-sep-2026)
26. Auditool, "Estructura del marco COSO 2013": https://www.auditool.org/blog/control-interno/entendiendo-la-estructura-del-marco-coso-2013-un-enfoque-sistematico (25-sep-2026)
27. Auditool, "17 principios de Control Interno según COSO 2013": https://www.auditool.org/blog/control-interno/diecisiete-principios-de-control-interno-segun-coso-iii (25-sep-2026)
28. Clubensayos, "Los 17 principios fundamentales de COSO 2013" (lista numerada 1-17 por componente, 5-4-3-3-2): https://www.clubensayos.com/Espa%C3%B1ol/LOS-17-PRINCIPIOS-FUNDAMENTALES-DE-COSO-2013-ASOCIADOS/2244287.html (25-sep-2026)
29. Gestio et Productio, "Eficiencia económica en proyectos de construcción": https://iieakoinonia.org/ojs3/index.php/gestioep/article/view/92 (25-sep-2026)
30. Repositorio Digital Uniandes, "Modelo de costeo ABC para la Constructora A.B. de Ibarra" (caso Ecuador, referencia metodológica): https://dspace.uniandes.edu.ec/handle/123456789/3056 (25-sep-2026)
31. Universidad de Guanajuato, "Costeo Basado en Actividades (ABC)": https://blogs.ugto.mx/contador/clase-digital-7-costeo-basado-en-actividades-costeo-abc/ (25-sep-2026)
32. vLex México, "NIF D-7, Contratos de construcción": https://vlex.com.mx/vid/d-contratos-ciertos-bienes-capital-510655670 (25-sep-2026)
33. Studocu, "Resumen NIF D-7" (material didáctico, no la norma original): https://www.studocu.com/es-mx/document/universidad-bancaria-de-mexico/estatica-en-la-construccion/nif-d7-resumido-documento-de-la-nif-d7/85357271 (25-sep-2026)
34. metricas.mx, "Razones financieras": https://metricas.mx/blog/razones-financieras-que-son-tipos-formulas-y-ejemplos-practicos (25-sep-2026)
35. cofide.mx, "Razones financieras": https://www.cofide.mx/blog/razones-financieras-que-son-y-como-mejoran-tu-contabilidad (25-sep-2026)
36. elConta.mx, "NIF D-4. Efectos de los impuestos diferidos": https://elconta.mx/efectos-impuestos-diferidos-informacion-financiera/ (25-sep-2026)
37. IPN, José Luis Castro Peralta, "Impuestos diferidos (NIF D-4)": https://www.investigacion.escasto.ipn.mx/cp/files/2015/09/IMPUESTOS-DIFERIDOS-NIF-D-4.pdf (25-sep-2026)
38. Colegio de Contadores Públicos de México, "Dictamen pericial contable, clave para la toma de decisiones judiciales": https://www.contadoresmexico.org.mx/Vida-colegiada/Dictamen-pericial-contable-clave-para-la-toma-de-decisiones-judiciales (25-sep-2026)
39. Veritas/IMCP, "Aspectos generales de la pericial contable": https://www.veritas.org.mx/Normatividad/Cumplimiento/aspectos-generales-de-la-pericial-contable (25-sep-2026)

### Registro de verificación (25-sep-2026)

- 21 búsquedas web y 9 lecturas de página/PDF (`WebFetch`), por encima del mínimo de 15 exigido.
- Verificados contra al menos dos fuentes independientes: los siete números y títulos de NIA (300, 315 Rev. 2019, 320, 500, 700 Rev., 705 Rev., 706 Rev.), los montos 2026 de los arts. 32-A y 32-H CFF, los arts. 52, 52-A, 96 y 30 CFF, la distribución 5-4-3-3-2 de los 17 principios de COSO 2013, y la vigencia de NIF D-4 desde 2008.
- **(nv):** el contenido completo del Folio 47/2023-2024 del IMCP (403); el alcance exacto del Régimen de Revelaciones Reducido del CINIF; el artículo específico del Código Nacional de Procedimientos Civiles y Familiares sobre prueba pericial contable; el PDF oficial del Anexo 5 RMF 2026 (se usaron dos citas secundarias); el texto íntegro del art. 52-A CFF (transcripción de tercero, coherente entre dos fuentes).
- Se encontró una cifra discordante en un resumen de buscador para Anexo 18/19 ("$1,855,919,380" y "$1,484,735,520") frente a la usada en el cuerpo ($2,013,710,870 y $124,650,380/$157,785,270, con cita literal del Anexo 5 en dos fuentes). Se descartó la discordante por no tener cita textual de respaldo; se documenta para que quien audite este capítulo la revise si localiza el PDF oficial del Anexo 5.
