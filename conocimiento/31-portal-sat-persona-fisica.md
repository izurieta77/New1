# 31 — Portal del SAT para una persona física inversionista y empresaria (de la A a la Z)

> Nivel: operativo-doctoral (cumplimiento y defensa dentro del portal, aplicado a una persona física con actividad empresarial o profesional, RESICO, sueldos, intereses, dividendos, arrendamiento, GBM/SIC y cripto) · Actualizado 2026-10-06 · Grado global: **A** en lo que dicen la RMF 2026, su Anexo 2 (fichas de trámite), el CFF, la LISR y las guías PDF del SAT, porque se leyó el texto oficial extraído y cada frase entrecomillada se verificó mecánicamente (ver §10). **B** en las cifras calculadas. **C** en cripto y en cualquier lectura que combine artículos sin regla expresa. **D / nv** en toda pantalla que exige iniciar sesión: **no se inició sesión nunca, no se pidió ni se usó ninguna credencial**, y no se describe ninguna pantalla que no esté en un documento oficial leído. **Esto no es asesoría fiscal**: describe normas y trámites con fuente; los trámites reales los presenta el dueño con su contador (REGLAS-MOTOR §0 y §0d).

Capítulos relacionados que aquí no se repiten: [29 CFF y defensa fiscal](29-codigo-fiscal-de-la-federacion-y-defensa-fiscal.md) (plazos de notificación, caducidad, infracciones, recurso, TFJA, amparo, PRODECON) · [27 Fiscalidad 2026 y estructura SIC](27-fiscalidad-2026-y-estructura-sic.md) (qué impuesto causa cada operación) · [11 México: mercado, instrumentos y fiscalidad](11-mexico-mercado-instrumentos-fiscalidad.md) · `cripto/fichas/2026-10-04-fiscalidad-cripto-mexico.md`. Este capítulo trata **cómo se opera cada trámite en el portal y en la app**: qué se necesita, dónde se hace, en cuánto tiempo responde el SAT y qué documento queda.

**Convenciones.** Hecho = lleva ficha, regla o artículo y fuente [n]. "**Inferencia:**" = razonamiento propio. "**Regla:**" = propuesta operable para el sistema del dueño, no para terceros. "(nv)" = no verificado en esta sesión (en particular todo lo que está detrás de login). **Grados:** **A** = texto oficial leído y frase verificada; **B** = texto leído pero la conclusión exige un cálculo o combinar dos textos; **C** = inferencia sin regla expresa o apoyada en fuente secundaria; **D** = no verificado o rumor. CSF = Constancia de Situación Fiscal. CIF = Cédula de Identificación Fiscal (las fichas hablan de "Constancia de Situación Fiscal con CIF"). RMF = Resolución Miscelánea Fiscal. "Ficha NN/CFF" = trámite del Anexo 2 de la RMF 2026. Los plazos "en días" de los trámites son días hábiles (CFF art. 12, cap. 29 §2.1).

---

## 1. Objetivos de dominio

1. Ubicar cada obligación y cada trámite de una persona física con inversiones en su **ficha de trámite** (número, quién lo presenta, cuándo, dónde, requisitos, plazo de respuesta, documento final).
2. Operar el acceso al portal (RFC, Contraseña, e.firma, SAT ID, SAT Móvil, buzón) sin pedir ni compartir credenciales, y saber cuál medio sirve para qué.
3. Declarar el mes y el año: precarga, deducciones personales, pago con línea de captura, saldo a favor, devolución automática y compensación.
4. Cumplir lo que depende del intermediario (GBM u otro): constancias, cálculo de ganancia o pérdida, costo promedio, regla de pérdidas del art. 129 LISR, y lo que el intermediario informa al SAT.
5. Distinguir qué sí existe oficialmente para activos virtuales (ninguna regla ni ficha: 0 coincidencias) y qué es inferencia.
6. Usar los canales de aclaración y defensa que están **dentro** del portal: aclaraciones, reducción de multas, recurso de revocación en línea.
7. Saber qué trámites se hacen desde el celular y cuáles no.

---

## 2. Núcleo

### 2.0 Mapa de fuentes y tres hallazgos de numeración (hechos)

- **Hallazgo 1 [A]:** en 2026 **las fichas de trámite ya no están en el Anexo 1-A sino en el Anexo 2** de la RMF. La regla 1.4 dice: "Anexo 2, que contiene los trámites fiscales" y el Anexo 1 queda para "formas oficiales fiscales". La regla 1.3 dice: "se dan a conocer en el Anexo 2, las fichas de trámites fiscales". La RMF sigue mencionando el "Anexo 1-A" solo en un transitorio (Vigésimo Tercero) que remite a fichas del IEPS "del Anexo 2". Cualquier guía, blog o prompt que cite "Anexo 1-A" usa la numeración de 2025 o anterior. El Anexo 2 vigente se publicó en el DOF **29-dic-2025 (edición vespertina)** y es el PDF que se leyó [3].
- **Hallazgo 2 [A]:** la numeración de las fichas cambió respecto de años anteriores (por ejemplo, la opinión de cumplimiento es 26/CFF y la aclaración a la opinión es 27/CFF). Toda ficha de este capítulo se leyó en el PDF del Anexo 2 de 2026; **no se cita ninguna por memoria**.
- **Hallazgo 3 [A]:** `https://www.sat.gob.mx` responde 200 por el proxy, pero las páginas `/portal/public/tramites/...` son una aplicación de una sola página (1,477 bytes de HTML sin contenido) y varias rutas devuelven 301 hacia una IP privada o 403; el host `wwwmat.sat.gob.mx` falla el protocolo TLS ("dh key too small") desde este entorno. Por eso las fuentes son los PDF oficiales (RMF, Anexo 2, guías de llenado) y las notas de `gob.mx/sat`. Las páginas dinámicas del portal quedan **nv**.

### 2.1 Inscripción en el RFC, Contraseña y e.firma

| Trámite | Ficha | Quién y cuándo | Dónde | Requisitos y condiciones clave | Respuesta / vigencia |
|---|---|---|---|---|---|
| Inscripción PF | **1/CFF** | "Dentro del mes siguiente al día en que inicies operaciones o requieras tu clave en el RFC" | Oficina del SAT, "previa cita registrada" en `citas.sat.gob.mx` | Comprobante de domicilio (original), identificación oficial vigente (original); condición: "Tener CURP"; si hay representante, instrumento de representación (poder para actos de administración, dominio o especiales, o carta poder con dos testigos y firmas ratificadas) | Inmediato; se recibe acuse único de inscripción y CSF; vigencia indefinida |
| Inscripción PF por oficina virtual | **3/CFF** | Solo mexicanos en el extranjero sin obligaciones, PF que solo perciban salarios y PF sin obligaciones. **Una persona con actividad empresarial no entra** | Videollamada con cita en `citas.sat.gob.mx` | Archivos PDF de máximo 4 MB: formato FOV-I, comprobante de domicilio (antigüedad máxima 4 meses), identificación | Inmediato |
| Validar clave por CURP | 10/CFF | (título; contenido no leído) | nv | nv | nv |
| Contraseña | **12/CFF** | PF, "cuando lo requieras"; en el Portal solo si ya hay e.firma vigente; por **SAT ID** con credencial INE vigente (mexicano mayor de edad); en oficina solo extranjeros, adultos mayores, gestantes o con discapacidad | Portal, SAT ID (`satid.sat.gob.mx`), SAT Móvil para generarla (según nota de gob.mx), oficina | Contraseña de 8 caracteres, solo letras y números, "no se acepta el RFC como Contraseña" | Inmediato. RMF 2.2.1: vigencia de cuatro años desde la generación o última actualización |
| e.firma, primera vez | **14/CFF** | Cuando se necesita por primera vez o cambió un dato de identidad en el RFC | Oficina del SAT con cita | USB (preferentemente nueva), identificación, comprobante de domicilio, correo con acceso, CURP validada; se puede generar antes el archivo .req con el programa Certifica | Inmediato; el certificado "estará vigente por 4 años" (ficha 20/CFF) |
| Renovación e.firma | **15/CFF** | PF con certificado vencido o por vencer | Portal (si está vigente: Certifica y CertiSAT Web), SAT ID (si perdió vigencia hasta **un año** antes) u oficina con cita | .key, .cer y contraseña de la llave privada | Inmediato (portal); SAT ID depende de validación |
| Aclaración en trámites de Contraseña o e.firma | **20/CFF** | Cuando el sistema devolvió "requerimiento de información adicional" | Portal / oficina | Responder en 6 días hábiles (plazo para cumplir) | El SAT resuelve en 10 días |
| Revocación de certificados | 18/CFF | (contenido no leído) | nv | nv | nv |
| e.firma portable | **19/CFF** | PF con e.firma activa y Contraseña | Portal: alta con correo registrado en el buzón; luego app **SAT Móvil** con código QR | App SAT Móvil, correo registrado en el buzón | Genera "clave dinámica" para entrar a trámites del Portal |

- **Regla [A, de la regla 2.2.1 y ficha 12/CFF]:** la Contraseña "sustituye la firma autógrafa y produce los mismos efectos que las leyes otorgan a los documentos correspondientes". La e.firma es la firma de lo importante (declaraciones con saldo a favor alto, recurso, devolución). **Inferencia [B]:** perder la llave privada o su contraseña obliga a una cita presencial para generar de nuevo la e.firma (la ficha 14/CFF no tiene ruta digital para quien no tiene certificado vigente ni vencido hace menos de un año).
- **Regla del dueño:** nunca entregar la .key, la contraseña de la llave ni la Contraseña del SAT a un tercero, a una herramienta de IA ni a este repositorio. Quien presenta por el dueño lo hace con su propia e.firma de contador o con la del dueño bajo su control directo.
- **Cambios de datos:** avisos al RFC en la ficha **28/CFF** ("Dentro del mes siguiente a aquel en que cambies tu actividad económica o modifiques tus obligaciones fiscales"), **35/CFF** (domicilio fiscal) y **36/CFF** (corrección de nombre y datos de identidad). Quien tiene intereses y además otros ingresos queda "relevado" del aviso por los intereses si ya está inscrito por esos otros ingresos (RMF 3.17.2).

### 2.2 Buzón tributario

- **Qué es [A, CFF 17-K]:** "un sistema de comunicación electrónico ubicado en la página de Internet del Servicio de Administración Tributaria". Por él la autoridad notifica y el contribuyente presenta promociones, avisos y respuestas a requerimientos.
- **Habilitarlo [A, ficha 21/CFF y RMF 2.2.7]:** en el Portal, minisitio Buzón Tributario; con RFC y Contraseña (o e.firma); se registra "al menos una dirección de correo electrónico y [...] número de teléfono celular" (máximo cinco correos y un celular) y se **confirman en las 72 horas siguientes** (RMF 2.2.7). Quien opta por RESICO debe hacerlo "dentro de los dos meses siguientes" a su aviso (ficha 21/CFF).
- **Obligación [A, CFF 17-K, cap. 29 §2.2]:** consultarlo "dentro de los tres días siguientes" a que llegue el aviso; si no se habilita o los medios están mal, "se entenderá que se opone a la notificación" y se notifica por estrados (art. 134, fr. III).
- **Amparo [A, RMF 2.2.9]:** quien obtuvo suspensión que deshabilita el buzón presenta una aclaración con la etiqueta "AMPARO_BLOQUEO BT".
- **App [A, gob.mx/sat]:** SAT Móvil permite "consultar los mensajes de interés de Buzón Tributario" y "habilitar las notificaciones" para saber si llegó uno. **Inferencia [C]:** una notificación push no sustituye la obligación legal de abrir el buzón en 3 días; el aviso legal es el que llega al correo y al celular registrados.
- **Qué se hace en el buzón [A, fichas]:** recurso de revocación (121/CFF), devoluciones (69 y 70/CFF), respuestas a requerimientos (art. 17-K fr. II). Lo que muestra cada pantalla: nv.

### 2.3 Constancia de Situación Fiscal, opinión de cumplimiento y estatus

- **CSF con CIF [A, ficha 22/CFF]:** gratuita, inmediata, sin documentos si se entra con e.firma o Contraseña. Canales: Portal (Trámites y servicios, Más trámites y servicios, Constancias, devoluciones y notificaciones), **SAT Móvil** (apartado "Mi RFC", opción Constancia), **SAT ID** (sin Contraseña ni e.firma, con credencial INE; se entrega por correo en PDF), oficina virtual con cita y cualquier oficina del SAT sin cita. Fundamento: CFF 27 apartado C fr. VIII y RMF 2.4.9. **Uso:** es el documento que piden bancos, intermediarios y clientes para emitir CFDI (régimen, código postal). Ficha 23/CFF: Cédula de Datos Fiscales (contenido no leído).
- **Opinión de cumplimiento [A, ficha 26/CFF, RMF 2.1.36, CFF 32-D]:** PF y PM, "Trámite inmediato", gratuita; se entra con RFC y Contraseña o e.firma por el aplicativo del artículo 32-D; permite "autorizar [...] para que un tercero [...] pueda consultar su opinión". La opinión es **positiva** cuando "esté inscrito y al corriente" en las obligaciones que lista la regla 2.1.36 (numerales 1 a 12). La lista detallada y los sentidos "negativa" y "inscrito sin obligaciones" no se transcriben aquí (nv). Hay opinión también en SAT Móvil (nota de gob.mx).
- **Si la opinión sale negativa [A, ficha 27/CFF]:** "Aclara las inconsistencias [...] con las que no estés de acuerdo", por **Mi portal** con RFC y Contraseña; el SAT responde en **6 días**; fundamento CFF 32-D y 33-A, RMF 2.1.36.
- **Regla [B]:** una opinión negativa bloquea contratar con el sector público (CFF 32-D, leído en cap. 29), pero también es señal de que falta una declaración. Para un inversionista, la causa típica es una declaración mensual omitida cuando se registró una obligación en el RFC (sección 2.5).

### 2.4 CFDI: emitir, recibir, descargar

- **Emitir [A, RMF 2.7.1.6]:** sin proveedor de certificación si se usa "Genera tu factura" en el Portal o la app **Factura SAT Móvil** (con lector y generador de QR). Se necesita el Certificado de Sello Digital (CSD): ficha **41/CFF**, que se genera con el software "Certifica" (RMF 2.7.1.5).
- **Validar y descargar [A, RMF 2.7.1.4]:** el Portal ofrece validación de CFDI uno a uno, validación masiva y "un servicio para la descarga masiva de los CFDI que se hayan emitido y/o recibido"; Factura SAT Móvil permite consultar los emitidos y recibidos.
- **RESICO PF [A, LISR 113-G]:** debe "contar con firma electrónica avanzada y buzón tributario activo", expedir CFDI por todos sus ingresos efectivamente cobrados y obtener CFDI de gastos e inversiones. **Cancelar CFDI tiene efecto grave**: el art. 113-F dice que se actualiza el supuesto del art. 109 fr. I CFF "cuando los contribuyentes cancelen los comprobantes fiscales digitales por Internet, aún y cuando los receptores hayan dado efectos fiscales a los mismos" (cap. 29, delito equiparable).
- **Para el inversionista [B]:** el CFDI que importa no lo emite él sino el intermediario o el banco: comisiones (para deducir o para el costo, art. 129 LISR) y, en su caso, constancias de retención. GBM no emite CFDI por la cuenta de Trading USA (cap. 27, fuente de GBM, nv aquí). Una plataforma extranjera no emite CFDI (**inferencia [C]**, cap. 29 §2.2).

### 2.5 Por régimen: qué obligación aparece y qué trámite la cubre

| Ingreso | Régimen y artículo | Obligación en el portal | Fuente |
|---|---|---|---|
| Honorarios o negocio, régimen general | Actividad empresarial y servicios profesionales (LISR Título IV Cap. II Sec. I) | Pagos provisionales mensuales y anual (abril) con "Declaraciones y Pagos"; anual precargada con CFDI y pagos provisionales | RMF 2.8.3.1; guía [7] |
| Honorarios, negocio o arrendamiento hasta 3.5 millones | **RESICO PF** (LISR 113-E a 113-J) | Pago mensual el **día 17** del mes siguiente, tasa 1.00 % a 2.50 % sobre ingresos **efectivamente cobrados** sin IVA y **sin deducciones**; declaración "prellenada con la información de los CFDI de tipo ingreso, de egreso y de pago"; el pago mensual es definitivo y releva de la anual por esos ingresos (RMF 3.13.7) | LISR 113-E; RMF 3.13.7 |
| Sueldos | Título IV Cap. I | Retiene y entera el patrón; si hay otros ingresos, anual (art. 98 y 150) | LISR 150; guía [8] |
| Intereses | Título IV Cap. VI | Retención del intermediario; el intermediario informa al SAT (ficha 46/ISR). Anual obligatoria si los ingresos acumulables por sueldos e intereses suman más de 400,000, si los intereses reales pasan de 100,000 o si hay retención no aplicada (art. 150); quien solo tiene intereses reales de más de 100,000 usa el programa de declaraciones anuales (RMF 3.17.2) | LISR 150; RMF 3.17.2 |
| Dividendos nacionales y extranjeros | Título IV Cap. IX | Tratamiento en cap. 27 (arts. 140 y 142); retención sobre dividendos extranjeros por el intermediario cuando cotizan en bolsa (RMF 3.11.7, "deberán emitir a la persona física un comprobante que acredite dicha retención") | RMF 3.11.7 |
| Arrendamiento | Título IV Cap. III o RESICO | Mensual o trimestral; la guía del SAT para arrendamiento por "Mis cuentas" existe (nv su contenido); en RESICO pasa a 113-E | LISR 113-E; guía [10] (nv) |
| Venta de acciones en bolsa y SIC | LISR 129 | 10 % definitivo; no hay pago mensual: "deberá entregarse de manera conjunta a la declaración anual" | LISR 129 |
| Cripto | ninguno | **0 coincidencias** (ver §2.8) | §2.8 |

- **Regla [A]:** el menú del aplicativo de pagos "mostrará las obligaciones registradas en el RFC del contribuyente correspondientes al periodo seleccionado" (RMF 2.8.3.1, fr. III). Si el régimen o la obligación están mal en el RFC, la declaración que el portal ofrece es la equivocada. Se corrige con la ficha 28/CFF **antes** de presentar.
- **Inferencia [B]:** quien es RESICO y además tiene sueldos o intereses calcula esos ingresos aparte: la RMF 3.13.8 dice que debe "determinar de forma independiente el impuesto anual correspondiente a los citados Capítulos".

### 2.6 Declaraciones: mensual, anual, pago, saldo a favor y devolución

**Mensual (ISR e IVA) [A, RMF 2.8.3.1].** Servicio "Declaraciones y Pagos": (I) se entra con RFC y Contraseña o e.firma; (II) se elige periodo y tipo; (III) el programa muestra las obligaciones del RFC; (IV) "en el caso de las declaraciones prellenadas, solo se validará la información" y el sistema hace los cálculos; (V) se envía y llega un acuse con "número de operación, fecha de presentación y el sello digital", y si hay cantidad a pagar, el acuse trae el **importe y la línea de captura con su fecha de vigencia**; (VI) se paga "por transferencia electrónica de fondos mediante pago con línea de captura vía Internet" en un banco autorizado por la TESOFE, y el banco entrega el recibo. Quienes hayan tenido ingresos menores a **2,421,720** (con actividad empresarial) o **415,150** (sin ella) en el ejercicio anterior pueden pagar también en ventanilla, en efectivo, con tarjeta o cheque. Si se presenta tarde, el aplicativo habilita "Parte actualizada" y "Recargos" (guía [7], p. 86).

**Anual [A, LISR 150, guías, gob.mx].**
1. **Cuándo:** "en el mes de abril del año siguiente". Disponible "los 7 días de la semana, las 24 horas del día" (gob.mx, 6-abr-2026).
2. **Quién la presenta aunque no deba pagar:** art. 150: quien tuvo ingresos totales superiores a **500,000** "deberán declarar la totalidad de sus ingresos", incluidos exentos e impuesto definitivo. Por eso un inversionista que vendió acciones con ganancia y tiene ingresos por encima de ese monto declara todo.
3. **Acceso:** RFC y Contraseña, o "e.firma, si tu saldo a favor es igual o mayor a 10,001 pesos" (gob.mx). Ruta: Trámites y servicios, Declaraciones para personas, Anual (guía [7], p. 4).
4. **Menú del aplicativo [A, guía p. 5-7]:** Presentar declaración, Consultar declaración, Impresión de acuse, Declaraciones pagadas.
5. **Precarga [A, guía p. 9-12, gob.mx]:** se eligen ejercicio, tipo (normal o complementaria) y "Ingresos a declarar"; "se impide que se desmarque el tipo de ingreso" cuando hay información de terceros o de pagos provisionales; el aplicativo pregunta por impuestos pagados en el extranjero y por la información de situación fiscal del art. 32-H CFF, y muestra "las fuentes de información junto con la fecha de corte". En 2025 hay que completar cada apartado antes de avanzar, y existe el **Visor de retenciones** (precarga sugerida de retenedores para actividad empresarial, arrendamiento, RESICO y plataformas), el **Visor de deducciones personales** y el **Visor de nómina** (gob.mx).
6. **Estructura [A, guía p. 12]:** Ingresos, Deducciones personales, Determinación, Pago, Vista previa y envío, Acuse.
7. **Deducciones personales [A, LISR 151 y guía p. 54-64]:** los CFDI aparecen precargados por tipo (honorarios médicos, dentales y gastos hospitalarios, funerales, colegiaturas, etc.); cada uno puede validarse, verse o eliminarse (el eliminado no se recupera sin rehacer el formulario); para 2025 hay la opción "Sin clasificación" para CFDI con alguna inconsistencia, que se pueden reclasificar "siempre que se cuente con la documentación soporte". **Tope [A]:** "no podrá exceder de la cantidad que resulte menor entre cinco veces el valor anual de la Unidad de Medida y Actualización, o del 15% del total de los ingresos" (no aplica a la fracción V, aportaciones complementarias de retiro). Los pagos de gastos médicos y similares deben hacerse por medios electrónicos o tarjeta, no en efectivo (art. 151 fr. I).
8. **Pago [A, guía p. 85-97]:** si hay impuesto a cargo se pueden pedir **compensación** de saldos a favor o pagos de lo indebido y **hasta seis parcialidades** (RMF 3.17.3: se presenta en abril y se paga la primera parcialidad en ese plazo; factores 0.9859, 1.9581, 2.9167, 3.8619 y 4.7938 para 2 a 6 pagos; "El monto de la parcialidad obtenida incluye el financiamiento"). El sistema genera la línea de captura.
9. **Saldo a favor [A, guía de sueldos y guía [7]; RMF 2.3.2]:** la pregunta "¿Qué deseas hacer con tu saldo a favor?" ofrece **Devolución** o **Compensación**; con devolución se elige "una CLABE interbancaria" a nombre del titular. **Sistema Automático de Devoluciones (RMF 2.3.2):** opción en el recuadro de la declaración, "hasta el día 31 de julio" del ejercicio de la RMF; con e.firma para saldos de **10,001 a 150,000**, y con Contraseña si es "igual o menor a $10,000"; la CLABE debe estar activa y a nombre del contribuyente. Quien no usa esa facilidad solicita con el Formato Electrónico de Devoluciones (FED) y las fichas 69/CFF o 70/CFF (RMF 2.3.8). Plazo para pedir: "cinco años siguientes a la fecha en que se haya determinado el saldo a favor" (ficha 69/CFF); la ficha 69 se presenta por el buzón con e.firma y deja acuse; el estado se consulta en "Consulta tu devolución". **Inferencia [B]:** la ficha 69/CFF lleva en el título "Grandes Contribuyentes o Hidrocarburos", pero en "quién puede solicitar" dice "Las personas físicas y morales"; la RMF 2.3.8 dirige a esa ficha solo a quienes son competencia de la AGGC y la AGH, y a la 70/CFF (Auditoría Fiscal Federal) a PF con remanente de sueldos. La ficha que corresponde a un PF ordinario con saldo de IVA o de pago de lo indebido es nv (no se identificó su número en el Anexo 2 leído).

### 2.7 GBM e intermediarios: constancias, ganancia o pérdida, costo y reporte

- **Quién calcula [A, LISR 129]:** las entidades financieras autorizadas por la LMV "deberán hacer el cálculo de la ganancia o pérdida del ejercicio"; la información "deberá entregarse al contribuyente"; "En caso de que se genere una pérdida fiscal en el ejercicio, los intermediarios del mercado de valores deberán emitir a las personas físicas enajenantes una constancia de dicha pérdida"; las constancias se expiden "por contrato de intermediación". Si el contrato termina antes del cierre, el intermediario calcula el periodo; si se cambia de intermediario, el cliente le remite toda la información y el intermediario que cede entrega "la información del costo promedio".
- **Cálculo [A, LISR 129 y RMF 3.15.12]:** por cada emisora, precio de venta menos comisiones de venta, menos costo promedio de adquisición más comisiones de compra; el costo promedio se recalcula con cada compra y se actualiza con el INPC "del mes inmediato anterior" (RMF 3.15.12). Por serie si la emisora tiene varias (RMF 3.15.9). Se puede "calcular una sola base" sumando ganancias y restando pérdidas (RMF 3.11.9).
- **Regla de acreditación de pérdidas [A, LISR 129]:** la pérdida del ejercicio se disminuye "únicamente contra el monto de la ganancia que en su caso obtenga el mismo contribuyente en el ejercicio o en los diez siguientes por las enajenaciones u operaciones a que se refiere el primer párrafo"; se actualiza por INPC; y "Cuando el contribuyente no disminuya la pérdida fiscal durante un ejercicio pudiendo haberlo hecho conforme a este artículo, perderá el derecho a hacerlo en los ejercicios posteriores y hasta por la cantidad en la que pudo haberlo efectuado". La declaración por estas ganancias "deberá entregarse de manera conjunta a la declaración anual". **Efecto [B]:** olvidar la pérdida en el año en que había ganancia la extingue.
- **Qué informa el intermediario al SAT [A, RMF 3.5.8 y ficha 46/ISR]:** a más tardar el **15 de febrero** de cada año, una base de datos (ficha **46/ISR**, "Informe de intereses y enajenación de acciones del sector financiero") con intereses nominales y reales, retenciones, saldo promedio de inversiones por mes, y, para cumplir el art. 56 LISR, "el saldo promedio mensual de la cartera accionaria de cada contribuyente" y "el total de las comisiones cobradas por la enajenación de acciones". La RMF 3.5.22 manda reportar la ganancia o pérdida neta del art. 129 del ejercicio 2025 en la declaración informativa IEF, campo 04, "Importe de la enajenación". Cotitulares: "las ganancias o pérdidas fueron percibidas por el titular y, en su caso, por todos los cotitulares en la misma proporción salvo prueba en contrario" (RMF 3.5.20). **Inferencia [B]:** el SAT ya tiene del intermediario el monto de enajenación y la cartera; una declaración anual que omita la ganancia no es un secreto para él.
- **Costo cuando la custodia está en otro intermediario [A, RMF 3.15.10]:** el titular entrega un documento "bajo protesta de decir verdad" con el costo promedio ponderado actualizado de cada venta, y conserva la comprobación por el plazo del art. 30 CFF.
- **"Reporte de pagos de ISR por enajenación de acciones" [nv]:** no se encontró en el Anexo 2, la RMF ni las guías leídas una ficha con ese nombre. El art. 129 no prevé pago provisional mensual: el ISR se declara con la anual. Si GBM o el portal muestran un reporte con ese nombre, es contenido de sesión (nv). **No se inventa la pantalla.**
- **Fuera de México [A, LISR 129]:** quien opera por "entidades financieras extranjeras que no estén autorizados conforme a la Ley del Mercado de Valores" debe calcular él mismo ganancia o pérdida y "tener a disposición de la autoridad fiscal los estados de cuenta" (aplica a Trading USA o a un bróker extranjero).

### 2.8 Activos virtuales (cripto)

- **Hecho [A]:** buscando `activo virtual`, `cripto`, `bitcoin` y `blockchain` en el texto extraído de la **RMF 2026, el Anexo 1, el Anexo 2, el CFF y la LISR** hay **0 coincidencias** en los cinco documentos. No existe en el portal una ficha de trámite ni una obligación de declaración específica de activos virtuales en las fuentes oficiales leídas.
- **Hecho [A]:** la ficha **168/CFF** ("Acceso en línea a la información fiscal de plataformas digitales") es para quienes prestan servicios digitales conforme a los arts. 1o.-A Bis y 18-B de la Ley del IVA; no trata de exchanges de cripto.
- **Inferencia [C]:** una venta de cripto se ubicaría en la enajenación de bienes (cap. 29 §2.8) y se declara en la anual como ingreso del capítulo que corresponda; sin norma expresa, el art. 5 CFF (aplicación estricta) es la defensa. Qué informa Binance, a quién y qué hace el SAT con eso: nv.
- **Regla del dueño:** conservar el historial del exchange y de la wallet (CFF art. 30, cap. 29) y fechar cada decisión de tratamiento en `bitacora/`.

### 2.9 Aclaraciones, atención y la "solicitud de aclaración"

- **Aclaraciones generales [A, fichas 53/CFF y 113/CFF]:** ruta del Portal: "Trámites y servicios / Más trámites y servicios / Herramientas de cumplimiento / Presenta tu aclaración, orientación, servicio o solicitud"; en **Mi portal** con RFC y Contraseña ("Servicios por Internet / Aclaraciones / Solicitud"). Ficha **53/CFF** (constancias de declaraciones y pagos): costo variable; el SAT responde en 20 días. Ficha **113/CFF**: aclara requerimientos, multas o comunicados por omisión de declaraciones cuando se considera improcedente; plazos para presentar: requerimiento 15 días posteriores a la recepción, multa 30 días hábiles desde que surte efectos la notificación, comunicados en cualquier momento; el SAT responde en 6 días. Otras aclaraciones útiles: **27/CFF** (opinión), **20/CFF** (Contraseña y e.firma), **85/CFF** (datos publicados en el listado del art. 69 CFF), **112/CFF** (liberación de depósitos bancarios inmovilizados: cuando el monto inmovilizado excede el crédito, la cuenta recibe ingresos de las fracciones X, XI y XIII del art. 157 o hay sentencia firme).
- **"SAC" [nv]:** no se encontró en las fuentes oficiales leídas una definición del acrónimo. Si se refiere al servicio de aclaraciones del portal, es el flujo anterior ("servicio de aclaraciones del SAT" aparece literal en la RMF 2.2.9). Si se refiere al Servicio de Atención al Contribuyente (oficinas), su canal está en las fichas (abajo). No se asume.
- **Canales [A, fichas]:** **MarcaSAT 55 627 22 728** (lunes a viernes 09:00 a 18:00, hora del centro; exterior +52 55 627 22 728; opción 5 para inscripción), chat `chat.sat.gob.mx`, oficinas (lunes a jueves 09:00 a 16:00, viernes 08:30 a 15:00), oficina virtual con cita. **Quejas y denuncias:** 55 885 22 222 y SAT Móvil, apartado Quejas y Denuncias. La nota de gob.mx para la anual da MarcaSAT "opción 0, subopción 2", OrientaSAT y chat uno a uno.
- **Citas [A, fichas 1/CFF, 14/CFF y 22/CFF]:** `https://citas.sat.gob.mx/`. Servicios con cita citados: inscripción PF, e.firma, renovación y revocación de e.firma PF, "Entrega de Constancias (oficina virtual)". La CSF no requiere cita en oficina.

### 2.10 Representación

- **Hecho [A, ficha 1/CFF, 14/CFF]:** el representante exige instrumento (poder para actos de administración, dominio o especiales, en copia certificada, o carta poder con dos testigos y firmas ratificadas ante autoridad fiscal o fedatario) e identificación; para la e.firma de menores, incapaces, sucesiones, ausentes, privados de libertad o enfermos en etapa terminal, la ficha 14/CFF lista el documento de cada caso. "El representante legal deberá estar previamente inscrito en el RFC y contar con Certificado de e.firma".
- **Hecho [A, RMF 3.17.3, guía]:** la e.firma de la declaración es del contribuyente; los contadores presentan con la e.firma o Contraseña que el contribuyente les confía, lo cual es una decisión del dueño, no una exigencia del portal. **Regla:** el portal permite a un tercero consultar la opinión de cumplimiento con autorización (ficha 26/CFF); para otros trámites no se encontró autorización electrónica de terceros (nv). Los poderes y la figura de "autorización de terceros" del buzón, nv.

### 2.11 App móvil: qué sí y qué no (según el SAT)

Fuente: nota oficial de gob.mx/sat del 11-jun-2025 [9] y fichas 12, 19, 22/CFF.

| Sí se puede en **SAT Móvil** (entrando con RFC y Contraseña) | Sí se puede en otra app del SAT | Fuera de la lista oficial (no se sabe si existe en la app: nv) |
|---|---|---|
| Consultar, descargar y guardar la CSF y la Cédula; obtener la opinión de cumplimiento; presentar declaraciones provisionales, definitivas y la anual de PF; consultar y guardar acuses de las anuales; leer mensajes del buzón y activar notificaciones; generar o actualizar la Contraseña; ver datos de identificación, domicilio, medios de contacto, régimen, obligaciones y actividades; ver el certificado de e.firma y los CSD; citas; clave dinámica de la **e.firma portable**; quejas y denuncias; alertas | **Factura SAT Móvil** (emitir, consultar y compartir CFDI de ingreso), **Verificador SAT** (autenticidad de documentos) | Recurso de revocación (la ficha 121/CFF dirige a "Mi portal" y buzón, con firma e.firma: **en la web**); devolución con FED y fichas 69/70/CFF; reducción de multas (fichas 57 y 58 piden Portal); generar e.firma por primera vez (ficha 14/CFF exige oficina con cita); solicitudes de aclaración largas |

- **SAT ID [A, fichas 12, 15, 22/CFF]:** servicio web `satid.sat.gob.mx` con foto de la credencial INE vigente y video; sirve para Contraseña, renovación de e.firma vencida hasta un año y CSF. Requiere ser "persona física mayor de edad y de nacionalidad mexicana". Quien tenga discapacidad que impida el video puede pedir ayuda a un tercero que lo explique en el mismo video.
- **Regla [C]:** el celular es cómodo para consultar y declarar lo precargado; para firmar un recurso o un escrito con anexos de hasta 50 MB (ficha 121/CFF) se usa la computadora, porque la ficha pide PDF y firma con e.firma (.key y .cer), que normalmente no residen en el teléfono. Cómo se comporta cada pantalla de la app: nv.

### 2.12 Defensa dentro del portal: multas, recargos, recurso en línea

- **Recurso de revocación en línea [A, ficha 121/CFF, CFF 121]:** presentado en el Portal por **buzón tributario**, con "Escrito de promoción", anexos en PDF de máximo **50 Megabytes**, firma con e.firma; se obtiene "número de registro de tu promoción" y constancias. **Plazos:** "dentro de los treinta días siguientes a aquel en que haya surtido efectos la notificación", 10 días contra violaciones del procedimiento de ejecución desde la publicación de la convocatoria de remate, y "en cualquier tiempo" para el tercero que afirme ser propietario. **Recurso exclusivo de fondo:** contra resoluciones de facultades de comprobación cuando la cuantía supere "doscientas veces la UMA, elevada al año" (cálculo: 200 x 42,794.64 = **8,558,928.00**, UMA 2026 del cap. 29 [9]); se debe indicar el origen del agravio conforme al art. 133-D CFF. Contenido restante de la ficha: ver Anexo 2 [3]. Plazos y efectos procesales (garantía, suspensión): cap. 29 §2.7.
- **Reducción de multas por pago pronto [A, CFF 75 fr. VII]:** "En el caso de que la multa se pague dentro de los 30 días siguientes a la fecha en que surta efectos la notificación [...] la multa se reducirá en un 20% de su monto, sin necesidad de que la autoridad que la impuso dicte nueva resolución". No aplica a materia aduanera ni cuando proceda la reducción del séptimo párrafo del art. 76 ni el art. 78. Se paga con línea de captura (ficha 47/CFF: solicitud del formato por Portal, MarcaSAT, salas de internet "Mi @spacio" u oficialía de partes; el SAT responde en 6 días).
- **Reducción de multas por solicitud [A, CFF 74 y fichas 57/CFF y 58/CFF]:** la SHCP "podrá reducir hasta el 100% las multas"; "no constituirá instancia" y la resolución no se impugna con los medios del CFF; solo procede sobre multas **firmes** y puede dar "suspensión del procedimiento administrativo de ejecución, si así se pide y se garantiza el interés fiscal". Ficha **57/CFF**: PF y PM, desde que se notifica la resolución con multas o desde que inician las facultades de comprobación "y hasta antes de que se notifique la resolución que determine el monto de las contribuciones omitidas"; respuesta en **45 días**, el SAT puede pedir información en 10 días y el contribuyente responde en 10. Ficha **58/CFF**: reducción de multas y tasa de recargos por prórroga cuando hay contribuciones determinadas por facultades de comprobación; respuesta en 45 días, 20 para pedir información y 15 para contestarla.
- **Recargos [A, RMF 2.1.20]:** "la tasa mensual de recargos por mora aplicable en el ejercicio fiscal de 2026 es de 2.07%" (LIF art. 11 fr. I). **Esto cierra la duda del cap. 29 (pregunta abierta 4): la tasa de 2.07 % deja de ser derivación [B] y pasa a grado A.**
- **Aclaraciones y quejas dentro del portal:** 113/CFF (vigilancia de declaraciones), 112/CFF (depósitos inmovilizados), 62/CFF (adeudos reportados a buró de crédito), 105/CFF (liquidación del art. 41 fr. II): títulos leídos; el contenido de 62 y 105 no se transcribe (nv). La queja ante PRODECON y el acuerdo conclusivo son trámites de PRODECON (cap. 29), no del portal del SAT.
- **Consulta en línea [A, ficha 120/CFF]:** consultas y autorizaciones en línea por Mi portal; el SAT resuelve en 3 meses; sirve para pedir criterio sobre una situación real y concreta (por ejemplo, cripto). La respuesta no se conoce de antemano (nv).

---

## 3. Fuentes primarias y canónicas

| # | Tema | Fuente | Nivel de acceso | URL |
|---|---|---|---|---|
| [1] | Resolución Miscelánea Fiscal para 2026 (DOF 28-dic-2025): reglas 1.3, 1.4, 2.1.20, 2.1.36, 2.2.1, 2.2.7, 2.2.9, 2.3.2, 2.3.8, 2.7.1.4 a 2.7.1.6, 2.8.3.1, 3.5.8, 3.5.20, 3.5.22, 3.11.7 a 3.11.9, 3.13.7, 3.13.8, 3.15.9 a 3.15.12, 3.17.2, 3.17.3 | SAT, minisitio de normatividad | **Leído** (PDF de 666 págs.; sha256 `6f71ccce...`, ver §10). Grado A | https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rmf/rmf/RMF_2026-DOF-28122025.pdf |
| [2] | Anexo 1 de la RMF 2026 (formas oficiales) | SAT | **Leído** el índice (las formas son imágenes; no se extrae texto de cada forma). Grado A para el índice | https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rmf/anexos/Anexo-1-RMF-2026_DOF-28122025.pdf |
| [3] | **Anexo 2 de la RMF 2026 (trámites fiscales; equivale al antiguo Anexo 1-A)** (DOF 29-dic-2025): fichas 1, 3, 12, 14, 15, 19, 20, 21, 22, 26, 27, 28, 47, 53, 57, 58, 69, 85, 112, 113, 120, 121, 168/CFF; 2, 46, 52/ISR | SAT | **Leído** (PDF de 181 págs., sha256 `ea38b1fa...`; se leyeron completas las fichas citadas y el índice de todas). Grado A | https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rmf/anexos/Anexo-2-RMF-2026_DOF-28122025.pdf |
| [4] | Primera modificación al Anexo 1 de la RMF 2026 (DOF 17-jul-2026) | SAT | **Leído** el índice (tiene los mismos números de ficha 3/CFF, 35/CFF, 36/CFF; no cambia los trámites de este capítulo, que son del Anexo 2). Su efecto sobre las fichas citadas: **nv** (no se revisó una modificación al Anexo 2) | https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rmf/anexos/Primera-Modificacion-Anexo-1-DOF-17072026.pdf |
| [5] | CFF (última reforma DOF 09-04-2026): arts. 17-K, 32-D, 74, 75 fr. VII, 121, 134 | Cámara de Diputados | **Leído** (PDF; sha256 `be7427b2...`) | https://www.diputados.gob.mx/LeyesBiblio/pdf/CFF.pdf |
| [6] | LISR (DOF 01-04-2024 en Diputados): arts. 113-E, 113-F, 113-G, 129, 150, 151 | Cámara de Diputados | **Leído** (sha256 `803c2875...`) | https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf |
| [7] | Guía de llenado de la declaración anual 2025, actividades empresariales y servicios profesionales (97 págs.) | SAT, minisitio de Declaración Anual | **Leído** (texto extraído; las capturas de pantalla son imágenes, no se leen). Grado A en estructura, B en detalle de pantalla | https://www.sat.gob.mx/minisitio/DeclaracionAnual/Personas/documentos/GuiaLlenado_ActividadesEmpresarialesProfesionales2025.pdf |
| [8] | Guía de llenado de la declaración anual, sueldos y salarios (65 págs.) | SAT | **Leído** (misma limitación) | https://www.sat.gob.mx/minisitio/DeclaracionAnual/Personas/documentos/GuiaLlenado_SueldosSalarios.pdf |
| [9] | SAT Móvil: trámites y servicios (11-jun-2025) y Declaración Anual 2025 de personas (6-abr-2026) | gob.mx/sat | **Leído** (HTML) | https://www.gob.mx/sat/articulos/sat-movil-tramites-y-servicios-a-tu-alcance · https://www.gob.mx/sat/articulos/declaracion-anual-2025-de-personas |
| [10] | Guías del SAT de pago mensual RESICO PF, arrendamiento por Mis cuentas y plataformas (existen según el buscador) | SAT (`wwwmat.sat.gob.mx`) | **No leídas**: el host falla TLS desde este entorno (nv). Grado D | resultados de búsqueda; sin descarga |
| [11] | Portal del SAT, pantallas con sesión: Mi portal, buzón, Declaraciones y Pagos, SAT Móvil, SAT ID, FED | SAT | **nv, requiere login. No se accedió** | https://www.sat.gob.mx |
| [12] | Capítulos 27 y 29 del repo | Repo | Primaria ya verificada (V05 y cap. 29 §10) | `conocimiento/27-...md`, `29-...md` |
| [13] | Cápsulas y cursos en video (Capacítate, Aprende SAT en YouTube) | SAT | **No consultados**: los transcritos están bloqueados desde este entorno. Solo se usó texto oficial. nv | — |
| [14] | Capacítate o Aprende SAT en texto (cursos escritos) y OrientaSAT | SAT | **No localizados** como texto descargable en esta sesión. nv | — |

---

## 4. Lo más reciente (estado al 6-oct-2026)

1. **Numeración 2026:** fichas en el **Anexo 2** (no 1-A) [A, §2.0].
2. **Tasa de recargos 2026:** 2.07 % mensual, RMF 2.1.20 [A].
3. **Declaración anual 2025 (abril de 2026):** se exige completar cada apartado antes de avanzar; nuevos visores de retenciones, deducciones personales y nómina; opción "Sin clasificación" en deducciones personales; precarga de retenedores para actividad empresarial, arrendamiento, RESICO y plataformas [A, gob.mx 6-abr-2026].
4. **Primera modificación al Anexo 1 (DOF 17-jul-2026):** existe; no se leyó una modificación al Anexo 2 ni a la RMF por ese decreto. Si cambió una ficha de este capítulo, es nv.
5. **Sin iniciativa de reforma al CFF para 2027** (cap. 11 y cap. 29 §2.0). La LISR tiene iniciativa 2027 centrada en personas morales y RESICO (cap. 11): revisar cuando se publique el decreto la regla 3.13.7 y el art. 113-E.
6. **Cripto:** sin cambio en el texto oficial leído (0 coincidencias).

---

## 5. Evidencia: ejercicios con cifras

**Ejercicio 1 — Tope de deducciones personales [B].** UMA anual 2026 = 42,794.64 (cap. 29 [9]); cinco veces = **213,973.20**. (a) Ingresos totales 800,000: 15 % = 120,000; el tope es el menor: **120,000**. (b) Ingresos 2,000,000: 15 % = 300,000; el menor es **213,973.20**. Un contribuyente con gastos médicos de 250,000 puede aprovechar solo ese tope. Las aportaciones complementarias de retiro (fr. V) no cuentan en el tope. *Nota: en la declaración anual de abril de 2026 (ejercicio 2025) el valor de la UMA anual de 2025 es la que aplica; la de 2026 sirve para el ejercicio 2026.*

**Ejercicio 2 — RESICO mensual y anual [B].** Ingresos cobrados del mes, sin IVA: 80,000. Está en el tramo "Hasta 83,333.33", tasa 1.50 %: ISR mensual = 80,000 x 1.5 % = **1,200** (se paga a más tardar el día 17 del mes siguiente). Si en el año cobra 900,000 en total, la tabla anual da 1.50 % (tramo hasta 1,000,000): 13,500; el ISR mensual pagado se resta (art. 113-F). Con ingresos repartidos en 12 meses de 75,000, los pagos mensuales suman 13,500: sin saldo.

**Ejercicio 3 — Pérdida bursátil y regla de 10 años [B].** 2025: pérdida neta de 40,000 reportada por el intermediario (constancia). 2026: ganancia de 100,000 en la misma cuenta. Con factor de actualización ilustrativo de 1.04 (no es INPC real; el factor real se calcula con INPC publicados): pérdida actualizada 41,600; base = 100,000 - 41,600 = **58,400**; ISR = 10 % = **5,840** (ahorro 4,160). Si en 2026 la ganancia existe y no se resta la pérdida, "perderá el derecho a hacerlo" hasta por la cantidad que pudo restar (art. 129). La pérdida de 2025 se pudo restar en 2026 contra ganancias hasta 2035 (ejercicio en que ocurrió y diez siguientes: **inferencia [B]**, el texto dice "en el ejercicio o en los diez siguientes").

**Ejercicio 4 — Multa con 20 % por pago pronto [B].** Multa impuesta de 55,000, notificada y con efectos el martes 13-oct-2026. Pagando dentro de los 30 días del art. 75 fr. VII (días hábiles por art. 12, inferencia B; sin el 16-nov, tercer lunes de noviembre) paga 55,000 x 0.80 = **44,000** con línea de captura; sin pedir nada a la autoridad. Si se impugna, no hay reducción (el cap. 29 explica el pago o la garantía).

**Ejercicio 5 — Parcialidades de la anual [B].** Impuesto a cargo de 60,000 en seis parcialidades (RMF 3.17.3): primera = 60,000 / 6 = 10,000; las otras cinco = (60,000 - 10,000) / 4.7938 = 10,430.14 cada una; total = 10,000 + 5 x 10,430.14 = **62,150.69** (financiamiento de 2,150.69 incluido, no hay recargos si se cumple). Si no se paga la primera dentro de abril, la opción se pierde.

**Ejercicio 6 — Umbral del recurso exclusivo de fondo [B].** 200 x 42,794.64 = **8,558,928.00** (UMA anual 2026). Una resolución determinante de 12,000,000 permite el recurso exclusivo de fondo; una de 5,000,000, no (solo el recurso ordinario o la vía contenciosa; ver cap. 29).

**Ejercicio 7 — Saldo a favor y devolución [B].** Saldo a favor de 12,000: pedir devolución en el recuadro de la declaración con e.firma y CLABE a nombre del titular; presentada la anual en abril, entra al Sistema Automático de Devoluciones si se opta "hasta el día 31 de julio" (regla 2.3.2). Saldo de 9,500: Contraseña basta. Saldo de 180,000: sale de la facilidad (rango 10,001 a 150,000) y se solicita por FED con ficha 69 o 70/CFF según competencia (RMF 2.3.8) (competencia: nv).

---

## 6. Traducción operable

### 6.1 Principio rector

Casi todo lo que cuesta dinero en el portal sale de **tres descuidos**: un buzón sin habilitar o sin abrir, un régimen u obligación mal registrada en el RFC (el portal ofrece la declaración equivocada), y una pérdida o una constancia de GBM que se pierde. Los tres se controlan con hábitos y con una revisión del RFC cada año.

### 6.2 Reglas (propuestas; no modifican `config/parametros.json`)

1. **Regla:** el dueño nunca entrega credenciales (Contraseña, .key, contraseña de la llave) al sistema ni a una IA. El sistema trabaja con documentos exportados (PDF de acuses, constancias, estados de cuenta), no con acceso al portal.
2. **Regla:** cada enero, el dueño baja la CSF (ficha 22/CFF) y verifica régimen, obligaciones y domicilio; si algo no coincide con su realidad, presenta el aviso 28/CFF dentro del mes siguiente al cambio.
3. **Regla:** antes del 15 de abril, revisar los visores (retenciones, deducciones personales, nómina) y la constancia de GBM; presentar la anual en abril (art. 150), no en el último día.
4. **Regla:** si hay pérdida en el art. 129 y hay ganancia en el mismo ejercicio, restar la pérdida (art. 129, pérdida del derecho si no se resta).
5. **Regla:** guardar el PDF del acuse de cada declaración, de cada línea de captura pagada y de cada constancia, en carpeta fuera del portal (CFF art. 30).
6. **Regla:** una multa recibida se paga con 20 % de reducción dentro de los 30 días, salvo que se vaya a impugnar (CFF 75 fr. VII); la reducción del art. 74 (fichas 57 y 58) se pide por separado y no es medio de defensa.
7. **Regla:** el recurso de revocación en línea se prepara en computadora, con PDF de menos de 50 MB, y el dueño o su abogado lo firma con e.firma (ficha 121/CFF).
8. **Regla:** antes de afirmar que "en el portal se hace X", citar ficha o regla; si no hay, escribir "nv".

### 6.3 *Checklist* trimestral del portal

| # | Pregunta | Fuente |
|---|---|---|
| 1 | ¿La e.firma vence en 90 días o menos? ¿La Contraseña tiene menos de 4 años? | Fichas 15/CFF y 12/CFF; RMF 2.2.1 |
| 2 | ¿El buzón está habilitado con correo y celular actuales? | Ficha 21/CFF; CFF 17-K |
| 3 | ¿Se revisó el buzón cada semana? | CFF 17-K |
| 4 | ¿La CSF coincide con el régimen y las obligaciones reales? | Ficha 22/CFF y 28/CFF |
| 5 | ¿La opinión de cumplimiento sale positiva? | Ficha 26/CFF |
| 6 | ¿Se presentaron las mensuales con acuse y pago? | RMF 2.8.3.1 |
| 7 | ¿Hay constancia de GBM del ejercicio y está guardada? | LISR 129 |
| 8 | ¿Hay pérdida pendiente de amortizar documentada? | LISR 129 |

---

## 7. Trampas y contraejemplo

1. **Citar "Anexo 1-A" en 2026.** Las fichas están en el Anexo 2. **Contraejemplo:** un escrito que cite "ficha 12/ISR del Anexo 1-A" remite a otra cosa o a nada.
2. **Creer que la declaración precargada es la correcta.** La RMF 2.8.3.1 dice que "solo se validará la información"; el contribuyente responde por ella.
3. **Eliminar un CFDI de deducciones personales y no poder recuperarlo** sin rehacer el formulario (guía p. 64).
4. **Creer que el buzón se abre en cualquier momento.** CFF 17-K: tres días desde el aviso; si no, se notifica por estrados.
5. **Creer que SAT Móvil sirve para todo.** No aparece en la lista oficial: recurso, devolución con FED, primera e.firma.
6. **Creer que RESICO deduce.** El art. 113-E aplica la tasa sobre ingresos cobrados "sin aplicar deducción alguna".
7. **Cancelar CFDI en RESICO.** Art. 113-F: se actualiza el supuesto del art. 109 fr. I CFF.
8. **No restar una pérdida bursátil cuando se pudo.** Se pierde el derecho (art. 129).
9. **Creer que hay una ficha o un reporte para cripto.** 0 coincidencias en RMF, Anexos, CFF y LISR.
10. **Usar la reducción del art. 74 como defensa.** "No constituirá instancia" y no se impugna; solo para multas firmes.
11. **Pagar en ventanilla sin estar en los montos de 2,421,720 o 415,150.** Fuera de ellos, es por Internet con línea de captura.
12. **Confiar en un blog para el número de ficha.** La numeración cambió; solo el Anexo 2 vale.

---

## 8. Examen (cinco preguntas)

1. **Una persona física con honorarios (RESICO) cobró 80,000 en octubre de 2026. ¿Cuánto paga, cuándo, y qué tiene que haber hecho en el RFC y con qué documento comprueba el pago?**
   ISR = 80,000 x 1.50 % = 1,200 (tramo hasta 83,333.33); a más tardar el 17-nov-2026 (LISR 113-E; RMF 3.13.7). Debe estar inscrita en RESICO, tener e.firma y buzón activo (113-G); la declaración "ISR simplificado de confianza. Personas físicas" viene prellenada con CFDI de ingreso, egreso y pago; paga con línea de captura en banco autorizado; conserva acuse y recibo bancario (RMF 2.8.3.1).

2. **Un inversionista tuvo pérdida en 2025 por 40,000 y ganancia de 100,000 en 2026 en GBM y no la restó. ¿Qué pierde y qué dice la ley sobre la constancia?**
   Pierde el derecho a restar esa pérdida "hasta por la cantidad en la que pudo haberlo efectuado" (LISR 129). La constancia de pérdida debe emitirla el intermediario en 2025 ("deberán emitir a las personas físicas enajenantes una constancia de dicha pérdida"). La declaración se presenta con la anual. Ejercicio 3 del §5 da el efecto en pesos.

3. **¿Qué trámites de la lista del SAT se pueden hacer en SAT Móvil, y por qué no el recurso de revocación?**
   CSF, opinión, declaraciones y anual de PF, acuses, buzón (mensajes y notificaciones), Contraseña, datos del RFC, e.firma (consulta y clave dinámica). El recurso (ficha 121/CFF) pide Portal, buzón, PDF hasta 50 MB y firma con e.firma; no aparece en la lista de la app.

4. **Recibes una multa de 55,000 el martes 13-oct-2026. ¿Qué puedes hacer en el portal y qué no?**
   Pagar con 20 % de reducción dentro de 30 días (75 fr. VII; 44,000); pedir reducción adicional con la ficha 57/CFF si es firme (el SAT resuelve en 45 días; no es medio de defensa); impugnar con recurso en línea (ficha 121/CFF) en 30 días. No se combinan el 20 % con la impugnación del mismo acto. Garantizar o pagar para suspender cobro: cap. 29.

5. **¿Qué encuentra el portal sobre cripto y qué debe hacer el contribuyente?**
   Nada: 0 coincidencias en cinco textos oficiales. Debe conservar historial (art. 30 CFF), decidir el tratamiento (inferencia: enajenación de bienes) y, si quiere seguridad, usar la consulta en línea (ficha 120/CFF, respuesta en 3 meses). Qué informa el exchange al SAT: nv.

---

## 9. Preguntas abiertas

1. **Pantallas con login (nv):** cómo se ven hoy Mi portal, Declaraciones y Pagos, el Visor de retenciones, el Visor de deducciones personales y la aplicación SAT Móvil. Solo se leyeron guías y fichas.
2. **Ficha de devolución ordinaria de PF (nv):** número exacto de la ficha para un PF con saldo de IVA o pago de lo indebido; el Anexo 2 lista 69 y 70/CFF, y las reglas 2.3.4 y 2.3.8 remiten al FED.
3. **"SAC" (nv):** qué acrónimo oficial designa la solicitud de aclaración. Hay "Servicio de aclaraciones" en la RMF 2.2.9; no se encontró "SAC".
4. **Reporte de pagos de ISR por enajenación de acciones (nv):** si GBM o el SAT ofrece un reporte con ese nombre; el art. 129 no prevé pago mensual.
5. **Opinión de cumplimiento (nv):** los 12 numerales de la regla 2.1.36 y los sentidos negativa y "inscrito sin obligaciones".
6. **Modificaciones posteriores a la RMF 2026 y al Anexo 2 (nv):** solo se leyó la primera modificación al Anexo 1 (17-jul-2026).
7. **Cripto:** CARF/OCDE y qué informa cada exchange; criterio del SAT (nv).
8. **Cursos escritos "Capacítate/Aprende SAT" y cápsulas (nv):** los transcritos de YouTube están bloqueados.
9. **Fichas no leídas completas:** 2, 4 a 11, 16 a 18, 23 a 25, 29 a 46, 48 a 52, 54 a 56, 59 a 68, 71 a 168/CFF y la mayoría de las ISR/IVA: solo su título.
10. **Hash del CFF en cap. 29:** el cap. 29 anota `be427b20...` y el PDF descargado hoy da `be7427b2...`; parece errata del cap. 29 (nv hasta confirmar que el PDF no cambió).

---

## 10. Registro de verificación (6-oct-2026)

- Todos los PDF se bajaron con `curl` por el proxy; el texto se extrajo con `pypdf` (de las guías PDF solo sale texto, no las capturas de pantalla). Hashes sha256: RMF 2026 `6f71ce0cccf430171fe858c5d244b1c321fa68306f962d44ec4977858a52919a`; Anexo 2 `ea38b1fa101a8fb07a4b913589aad3f0cda85e67345581cbe199fa016a4c7e1d`; CFF `be7427b20d3552775ab42018f8f87578078770095bf8cf46322c25e36ee3aa7d`; LISR `803c2875c09c751c1966b8eb4dca99f460b237da4ef67ee04b4fa325d8c2f786` (igual al del cap. 29).
- **Verificación mecánica de frases:** 127 cadenas entrecomilladas del capítulo se buscaron, sin espacios y sin mayúsculas, en el texto extraído de RMF, Anexos 1 y 2, CFF, LISR, guías [7] y [8] y notas [9]. Las que no coinciden son 19 y se revisaron a mano: 14 son artefactos del emparejado de comillas (rótulos "Inferencia:", "Regla:", "nv", y trozos entre dos citas); 1 es el mensaje de error TLS ("dh key too small", de `curl`); 1 es la cita de gob.mx, que en la página aparece partida en renglones (se corrigió para citar solo "e.firma, si tu saldo a favor es igual o mayor a 10,001 pesos"); las otras son rótulos propios (nombres de reportes o de cursos que se dicen **no encontrados**, o ejemplos de lo que no hay que citar). Ninguna frase atribuida a una norma o ficha quedó sin coincidir.
- **Cálculos de §5:** hechos con Python (213,973.20; 8,558,928.00; 1,200; 13,500; 44,000; 10,430.14; 62,150.69; 58,400; 5,840).
- **Acceso:** `https://www.sat.gob.mx` responde 200; las rutas `/portal/public/...` son SPA vacía por curl; `wwwmat.sat.gob.mx` falla TLS ("dh key too small"); `dof.gob.mx/2025/SHCP/SHCP_281225_01.pdf` es la RMF y `_02.pdf` es el Anexo 1; el Anexo 2 está en la ruta del SAT citada en [3].
- **No verificado (nv):** todo lo que está detrás de login (pantallas de Mi portal, buzón, Declaraciones y Pagos, SAT Móvil, SAT ID, FED); guías del SAT por RESICO, arrendamiento y plataformas [10]; ficha de devolución ordinaria de PF; "SAC"; reporte de pagos por enajenación de acciones; contenido completo de las fichas 18, 23, 62, 105; los 12 numerales de la regla 2.1.36; cripto (exchange, CARF y criterio del SAT); modificaciones posteriores al Anexo 2; cursos, cápsulas y transcritos del SAT (bloqueados); reglas 2.8.1.x sobre "Mis cuentas"; guía y ficha de arrendamiento; texto completo de la guía de RESICO.
