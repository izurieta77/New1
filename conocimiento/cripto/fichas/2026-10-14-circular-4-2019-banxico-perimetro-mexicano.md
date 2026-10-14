# Ficha de avance · 14-oct-2026 · Frontera regulatoria (México): la Circular 4/2019 de Banxico y el perímetro en el que opera la cuenta en Binance

> Corrida de las 08:17 CDMX (14:19 UTC), estudio profundo.
>
> **Por qué este tema.** Es el pendiente (a) de la ficha de ayer (`2026-10-13-genius-reloj-de-vigencia-y-reservas.md` §8), dentro de la fila de Frontera "Regulación: GENIUS, CLARITY, MiCA, Circular 4/2019 de Banxico" (`00-plan-de-estudio.md`). Va primero que MiCA y CLARITY porque toca directo la cuenta del dueño (`arena-claude-binance`, desde México, con SPEI por Medá). La decisión del 25-sep (`bitacora/decisiones/2026-09-25-CRIPTO-inicial.md` §"Riesgos no de mercado") ya citaba la disposición 3.a, pero no se había leído el texto primario.

## 0. Pregunta de hoy, acotada

¿Qué dice **literalmente** la Circular 4/2019, y en qué estado está al 14-oct-2026? ¿Tiene reformas posteriores a 2020? Y lo práctico: ¿regula a Binance, o define un perímetro que deja a Binance fuera?

## 1. Acceso y fuentes (declarado)

- **Texto compilado oficial, íntegro, de Banxico:** "TEXTO COMPILADO de la Circular 4/2019 publicada en el DOF el 8 de marzo de 2019, incluyendo sus modificaciones dadas a conocer mediante la Circular 37/2020 publicada en el referido Diario el 30 de septiembre de 2020". 16 páginas. URL: `banxico.org.mx/marco-normativo/normativa-emitida-por-el-banco-de-mexico/circular-4-2019/{ACDFD34F-1226-1893-52EE-D87A28645384}.pdf`.
- **Facsímil del DOF del 8-mar-2019, íntegro:** Primera Sección, páginas 90 a 92, alojado por Banxico (`.../circular-4-2019/{8D7769AF-03F6-701A-68AA-EF25A73AD035}.pdf`, 10 páginas). Es la **segunda verificación**. **Límite de acceso:** `dof.gob.mx` falló la verificación TLS desde este entorno (el certificado no corresponde al host), así que no se consultó el portal del DOF directamente; se usó el facsímil de la página del DOF.
- **Circular 37/2020, íntegra:** DOF del 30-sep-2020, 1 página (`.../circular-4-2019/{7AB92A88-9308-9EE4-9B02-2AA7C81CD971}.pdf`).
- **Lista oficial de normativa de Banxico por año:** `banxico.org.mx/marco-normativo/normativa-agrupada-por-ano-cr.html`, consultada hoy. Llega hasta la **12/2026**.
- **Ley para Regular las Instituciones de Tecnología Financiera (LRITF), íntegra:** `diputados.gob.mx/LeyesBiblio/pdf/LRITF.pdf`, 76 páginas, "Última reforma publicada DOF 14-11-2025". Se leyeron completos los arts. 30 a 34 y 88.
- **Comunicado conjunto de Banxico, SHCP y CNBV del 28-jun-2021**, íntegro (Banxico, `publicaciones-y-prensa/miscelaneos/{56A7FE3D-...}.pdf`).
- **Secundario (grado C/D, solo contexto):** la crítica de inconstitucionalidad de un despacho (Simposio Fiscal, vía CriptoNoticias) y los perfiles de CryptoSlate. No se usan para ninguna afirmación.

## 2. Lo esencial del texto [H, grado A: texto primario en dos copias]

| Disposición | Qué dice |
|---|---|
| **1.a Objeto** | Determinar qué activos virtuales y en qué condiciones pueden operar las "Instituciones"; plazos ante bifurcaciones (*forks*) o cambios de características; requisitos y características de la autorización. |
| **2.a Definiciones** | **"Institución"** = instituciones de crédito (bancos) e ITF autorizadas. **"Operaciones Internas"** = las actividades que la Institución hace internamente para sus operaciones pasivas, activas y de servicios con clientes o por cuenta propia, incluido el soporte de transferencias internacionales de fondos. **"Operación con Activos Virtuales"** = solo las Operaciones Internas. |
| **3.a Características de las operaciones** | (i) Solo Operaciones Internas, **con autorización previa de Banxico**. (ii) La Institución debe "impedir en todo momento que se transmita, directa o indirectamente, el riesgo" a sus clientes. (iii) **"No serán elegibles para la obtención de la autorización [...] aquellas Operaciones [...] mediante las cuales pretendan prestar de manera directa a sus Clientes servicios de intercambio, transmisión o custodia de activos virtuales."** |
| **4.a Características del activo** | Unidades de información identificables, incluso fraccionables, que no representen la titularidad de un subyacente (o la representen por un valor inferior); controles de emisión por protocolos a los que pueden suscribirse terceros; protocolos que impidan el doble gasto. BTC y ETH caben en la definición; una stablecoin respaldada 1:1 en principio no (I, no lo dice el texto por nombre). |
| **5.a a 9.a** | La autorización es por Institución y con plazo; se puede renovar. La solicitud lleva modelo, manuales, un "marco integral de riesgos" (negocio, cambiario, financiero, operativo, ciberseguridad, PLD y reputacional) y un plan de **liquidación ordenada de compromisos en moneda de curso legal**. Si Banxico no responde a los cambios al manual en 30 o 60 días hábiles bancarios, se entienden **negados**: es **negativa ficta**, no afirmativa. Hay 6 causales de revocación. |
| **10.a a 15.a** | Contratación de terceros (incluidos los extranjeros), con autorización previa. Banxico puede visitarlos, el auditor externo tiene acceso, el tercero no puede subcontratar y el tercero extranjero debe residir en una jurisdicción con protección de datos e intercambio de información. La Institución responde siempre por el tercero. |
| **16.a a 18.a** | Evaluación por un Tercero Independiente **cada 2 años**, con un máximo de **3 periodos consecutivos** y una pausa mínima de **5 años** para recontratarlo. |
| **Transitorias** | Entró en vigor al día siguiente de su publicación. Tuvo consulta pública de 60 días hábiles bancarios. |

**Circular 37/2020 [H, A]:** su único cambio es la fracción II de la 11.a. La aprobación del contrato con un tercero la da el **"Órgano de Administración de la Institución"**, y ya no el "consejo de administración u órgano equivalente [...] del tercero" del texto original. La motivación expresa es un comentario recibido en la consulta pública.

**LRITF, el marco legal [H, A]:**
- **Art. 30:** define el activo virtual ("representación de valor registrada electrónicamente y utilizada entre el público como medio de pago [...]"; nunca la moneda de curso legal ni las divisas). Las ITF "solo podrán operar con los activos virtuales que sean determinados por el Banco de México", con autorización previa.
- **Arts. 31 a 33:** prevén que una ITF **entregue al cliente sus activos virtuales**, que liquide en el mismo acto la compraventa con clientes, y que **custodie** sin poder prestar ni dar en garantía los activos de clientes (art. 33).
- **Art. 34:** exige divulgar 4 riesgos.
- **Art. 88:** permite a los bancos operar con activos virtuales con autorización.
- Los **arts. 30 a 34 no tienen ninguna reforma** desde 2018: no aparece ninguna nota "reformado/adicionado DOF" entre el art. 30 y el Título III; se verificó con una búsqueda en Python.

## 3. Hallazgo central [H/I, grado A en el texto, B en la lectura]

1. **[H, A] La Circular 4/2019 está intacta en lo sustantivo desde hace 7.6 años.** En la lista oficial de Banxico hay **una sola** circular que "Modifica la Circular 4/2019": la 37/2020. Ninguna de las circulares de 2021 a la 12/2026 trata de activos virtuales. La única modificación, de forma, lleva **2,204 días** (6.03 años) sin cambios (§4).
2. **[H, A] El perímetro está cerrado por diseño.** La ley (arts. 31 a 33) **contempla** que una ITF custodie y compravenda activos virtuales con clientes. La circular que la reglamenta declara **no elegible** justo esa operación (3.a, tercer párrafo). Resultado: **en México no existe una vía de autorización** para que una entidad supervisada ofrezca al público intercambio o custodia de cripto. El comunicado conjunto del 28-jun-2021 lo confirma: "las instituciones financieras del país no están autorizadas a realizar y ofrecer al público operaciones con activos virtuales, tales como Bitcoin, Ether, XRP [...] incluidos los depósitos o cualquier otra forma de custodia". Sobre stablecoins, agrega que no se ha autorizado el manejo de saldos en pesos o divisas mediante "monedas estables".
3. **[I, B] Para la cuenta del dueño, la Circular 4/2019 no regula a Binance ni puede protegernos.** Binance no es banco ni ITF, así que no es "Institución" en el sentido de la 2.a. La circular no le aplica, y Banxico **no tiene un régimen** bajo el cual autorizarla. El único régimen mexicano que sí le aplica es el de **actividad vulnerable** (LFPIORPI, art. 17, fr. XVI), que es de prevención de lavado y **no protege al cliente** (ficha del 4-oct). La lectura del comité del 25-sep era correcta, pero la redacción "no puede estar supervisado" es más fuerte de lo que dice el texto. Lo preciso es esto: **ninguna figura autorizable en México le permitiría ofrecer ese servicio**. No es que la ley lo prohíba a un extranjero; es que el perímetro supervisado lo deja fuera.
4. **[I, C] El punto frágil mexicano está en el riel de pesos, no en Binance.** Medá es una IFPE, es decir, una ITF y por tanto una "Institución". Mientras solo mueva pesos (fondos de pago electrónico), no hace "Operaciones con Activos Virtuales". Pero la 3.a y el comunicado de 2021 (con su "sana distancia" entre cripto y el sistema financiero) dan a Banxico y a la CNBV base para presionar a una ITF que sirva de rampa de entrada a un exchange no supervisado. **No encontré ninguna acción de este tipo** (grado C: es ausencia de evidencia en la lista de normativa, no una búsqueda exhaustiva de oficios). El disparador "SPEI caído más de 48 h" del plan de contingencia es el que mide exactamente este riesgo.
5. **[I] No hay catalizador regulatorio mexicano a 30 días.** Lleva 6 años sin cambios, no hay consulta pública abierta en la lista de 2026 y la LRITF no se ha tocado en ese capítulo. La probabilidad de un cambio de régimen en el horizonte del torneo es baja. El riesgo mexicano sigue siendo **operativo** (SPEI y Medá), no normativo.

## 4. Ejercicio numérico (Python, verificado dos veces)

Script fuera del repositorio: `scratchpad/calc/circ4_verif.py`.
- **Verificación 1:** normaliza los dos textos, el compilado de Banxico y el facsímil del DOF. Quita encabezados, números de página y espacios, que `pypdf` mete de forma espuria. Después los parte por disposición y los compara con `difflib.SequenceMatcher`.
- **Verificación 2:** busca la frase literal de exclusión de la 3.a en ambos textos.

Salida real (resumida):

```
disposiciones compilado: 1..19 (19)   disposiciones DOF: 1..19 (19)
18 de 19 disposiciones con ratio=1.0000 (idénticas carácter por carácter)
11.a  ratio=0.9880  -> DOF: "consejo de administración u órgano equivalente que tenga bajo su
                        responsabilidad las funciones ... del tercero"  vs compilado: "Órgano de
                        Administración de la Institución"   (= exactamente el cambio de la Circular 37/2020)
frase 3.a en compilado: True | en DOF: True
vigor 4/2019: 2019-03-09 (sábado) | días en vigor a hoy: 2776 = 7.6 años
vigor 37/2020 (día hábil bancario siguiente): 2020-10-01 (jueves) | días sin cambios: 2204 = 6.03 años
Tercero Independiente: máx. 6 años continuos; ciclo mínimo hasta recontratarlo: 11 años
```

**Lectura:** el texto compilado reproduce fielmente el DOF, con la única diferencia que explica la 37/2020. Así que puede citarse el compilado como texto vigente. Los dos métodos coinciden.

**Hallazgo menor del texto [H]:** la 12.a, fracción II, del compilado sigue diciendo "consejo de administración u órgano equivalente [...] a que se refiere la fracción II de la Disposición anterior". Pero la 37/2020 cambió esa fracción II a "Órgano de Administración de la Institución". Es un remanente de redacción que la reforma no armonizó, y no cambia el sentido. Es el mismo tipo de hallazgo que la referencia cruzada mal numerada de GENIUS de ayer.

## 5. Qué cambia para invertir (`arena-claude-binance`, spot, desde México)

- **[I]** **No hay una acción nueva.** El riesgo regulatorio mexicano es estructural y estable; no hay un evento que vigilar en 30 días.
- **[I]** **Hay que precisar el registro de riesgos.** El riesgo de "Binance restringe México" (3% según el geopolítico) **no** proviene de Banxico ni de la Circular 4/2019, que no le aplican. Si llegara, vendría de una decisión comercial de Binance, de la UIF y la SHCP (vía LFPIORPI) o del riel de pesos (Medá). La señal E5 de la lista de alerta ("aviso de restricción para México") sigue siendo la correcta; conviene añadir como fuente la **CNBV/Banxico sobre IFPE** que den servicio a exchanges.
- **[I]** **La protección del cliente es cero por diseño.** Ninguna autoridad mexicana responde por los saldos en Binance. Eso confirma que el tope de 10,000 MXN de la cuenta real es la única defensa de contraparte (decisión del 25-sep, tabla de contingencia: "el tope no cubre el riesgo de contraparte").

## 6. Contrapuntos y límites

- **El texto no es la práctica.** Banxico pudo haber dado autorizaciones de "Operaciones Internas" a algún banco (por ejemplo, para pagos transfronterizos) sin que eso salga en la lista de normativa. No se buscaron oficios individuales de autorización.
- **La ausencia en la lista es evidencia por ausencia.** La lista de normativa por año se leyó hoy hasta la 12/2026, pero una regla conjunta o un criterio de la CNBV o la UIF que no sea circular de Banxico no aparecería ahí.
- **No se revisaron** las Disposiciones de la CNBV para ITF, el régimen de la UIF ni el criterio del SAT, más allá de la ficha del 4-oct. Tampoco iniciativas legislativas de 2026 sobre activos virtuales en México. Quedan como pendiente.
- La crítica de inconstitucionalidad (la circular restringe lo que la ley permite) es la opinión de un despacho, **grado D** como argumento. Pero el hecho que señala, la tensión entre los arts. 31-33 y la 3.a, sí se verifica en los textos primarios (§3.2).
- **La extracción de PDF con `pypdf`** mete espacios dentro de palabras ("Cli entes"). Por eso la comparación se hizo sin espacios; las citas textuales de esta ficha se cotejaron contra el texto con espacios.

## 7. Autoexamen (5 preguntas, respuestas en la ficha)

1. ¿Puede un banco mexicano obtener autorización de Banxico para custodiar BTC de sus clientes? (No: la 3.a declara no elegibles los servicios directos de intercambio, transmisión o custodia.)
2. ¿Qué cambió la Circular 37/2020? (Solo la 11.a, fr. II: la aprobación del contrato con un tercero la da el Órgano de Administración de la Institución, no el del tercero.)
3. ¿La Circular 4/2019 le aplica a Binance? (No: solo a las "Instituciones", es decir, bancos e ITF autorizadas. A Binance le aplica la LFPIORPI, art. 17, fr. XVI.)
4. Si Banxico no responde en 30 días hábiles bancarios a un cambio del manual operativo, ¿qué pasa? (Se entiende negado: es negativa ficta, 8.a.)
5. ¿Qué artículo de la LRITF prohíbe a una ITF prestar los activos virtuales que custodia? (El art. 33.)

## 8. Estado y pendientes

- **Estado:** "Documentado con comprobación" para la Circular 4/2019: texto compilado igual al DOF en 18 de 19 disposiciones, con la 19.ª explicada; lista de normativa al día; LRITF leída. La fila de regulación de la Frontera sigue **parcial**: faltan MiCA y CLARITY.
- **Pendientes:**
  - (a) MiCA, títulos III y IV (EMT y ART), en EUR-Lex;
  - (b) estado de CLARITY después del 15-sep;
  - (c) ANPRM de la CFTC 2026-20888;
  - (d) Federal Register hacia el 12-nov (P0117);
  - (e) México: Disposiciones de la CNBV para IFPE y cualquier iniciativa de 2026 sobre activos virtuales; reintentar `dof.gob.mx` si el TLS se corrige.

**Grado global:** A en el texto (dos copias primarias concordantes) y en el estado normativo según la lista oficial; B en la lectura del perímetro para Binance; C en el riesgo del riel de pesos (Medá).
