# Ficha de avance · 04-oct-2026 · Tema 6 del plan (fiscalidad cripto de una persona física en México)

> Corrida de las 08:17 CDMX (14:17:23 UTC), `analista-cripto`. Toma el **tema 6**, el último de "Temas que no cubren los 35 recursos y que el torneo necesita" (`00-plan-de-estudio.md`): *"Fiscalidad cripto de una persona física en México. ISR y actividad vulnerable según el art. 17, fr. XVI, de la LFPIORPI."* Es el siguiente pendiente tras los temas 1 (30-sep), 2 (1-oct), 3 (29-sep), 4 (2-oct) y 5 (3-oct, ya documentado en `04-riesgos-fraude-hackeos-y-seguridad.md` §6). Con este tema se cierra la lista completa de 6 temas de frontera regulatoria/operativa del plan.

## 1. Ficha y conflictos de interés

- **Objeto:** (a) qué régimen de ISR aplica a la ganancia por venta de cripto de una persona física en México, dado que no existe una ley fiscal específica para activos virtuales; (b) qué activa la "actividad vulnerable" de la fracción XVI del art. 17 de la LFPIORPI y si aplica a la cuenta `arena-claude-binance`.
- **Conflicto de interés:** el dueño de esta cuenta es la persona física cuya situación fiscal se analiza. No soy asesor fiscal ni abogado; esto es investigación para decidir mejor, no asesoría fiscal formal. Cualquier presentación de declaraciones ante el SAT la hace el dueño con su propio contador.
- **Por qué importa para el torneo:** no cambia el filtro de tendencia ni el tamaño de la posición, pero sí el riesgo de cumplimiento del dueño como persona física y la caracterización de Binance frente a la regulación mexicana (ya tocada en `bitacora/decisiones/2026-09-25-CRIPTO-inicial.md`, sección de riesgos no de mercado).

## 2. Acceso real

- **Fuente primaria, leída directamente en esta corrida (texto oficial de la ley, descargado de `diputados.gob.mx` y extraído con `pdfminer.six`, no citas de prensa):**
  - [`LISR.pdf`](https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf) (Ley del Impuesto sobre la Renta), Última Reforma DOF 01-04-2024: arts. 93 fr. XIX inciso b), 119, 125-128, 141, 142, 152.
  - [`LFPIORPI.pdf`](https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPIORPI.pdf) (Ley Federal para la Prevención e Identificación de Operaciones con Recursos de Procedencia Ilícita), Última Reforma DOF 16-07-2025: arts. 17 (encabezado y fr. XVI) y 18.
  - **Nota técnica de acceso:** `WebFetch` no pudo extraer el texto de estos PDF (los devolvía como binario/imagen); se descargaron con `curl` y se extrajeron con la librería `pdfminer.six` (tras instalar `cffi`, porque el entorno tenía rota la dependencia `cryptography`→`_cffi_backend`). Esto es una lectura íntegra del articulado relevante, no un resumen de un tercero.
- **Fuentes secundarias (prensa especializada y agregadores fiscales, declaradas [I], no DOF/INEGI/CONASAMI leído de forma directa):**
  - Valor diario de la UMA 2026 = **$117.31 MXN** (INEGI, DOF 9-ene-2026, vigente desde 1-feb-2026): convergen idconline.mx, mediotiempo.com, record.com.mx, adn40.mx, facturama.mx. No se accedió directamente a `inegi.org.mx` (la página es dinámica y no expuso el valor a `WebFetch`).
  - Salario mínimo general (SMG) diario 2026, zona general = **$315.04 MXN** (CONASAMI, vigente desde 1-ene-2026): convergen unotv.com, siemprealdia.co, cronica.com.mx.
  - Postura de PRODECON sobre el régimen de ISR de cripto (estudio preliminar, no vinculante): resumida por xataka.com.mx, que cita a PRODECON directamente pero no reproduce el documento original; no pude acceder al documento de PRODECON en sí en esta corrida.
  - El PDF de BDO México sobre fiscalidad de criptomonedas no pudo extraerse (binario corrupto para la herramienta); se descarta como fuente de esta ficha.
- **Lo que NO encontré:** ningún criterio normativo del SAT (de los que publica como "Criterios Normativos" o "Criterios no vinculativos") que mencione explícitamente activos virtuales/criptomonedas en el contexto del ISR. Tampoco encontré jurisprudencia de tribunales fiscales mexicanos sobre el tema. **No existe, hasta donde pude verificar hoy, una resolución oficial y vinculante del SAT sobre qué capítulo de la LISR aplica a la venta de cripto por una persona física.**

## 3. Lo esencial

### 3.1 LFPIORPI, art. 17, fr. XVI: quién es el sujeto obligado (no nuestra cuenta)

- **[H]** Texto exacto de la fracción XVI (DOF 16-07-2025), leído directamente del PDF oficial: la actividad vulnerable es *"el ofrecimiento habitual y profesional de intercambio de activos virtuales por parte de sujetos distintos a las Entidades Financieras, que se lleven a cabo a través de plataformas electrónicas, digitales o similares, que administren u operen, facilitando o realizando operaciones de compra o venta de dichos activos propiedad de sus clientes o bien, provean medios para custodiar, almacenar, o transferir activos virtuales distintos a los reconocidos por el Banco de México [...], incluidas las operaciones que se realicen con ciudadanos mexicanos desde otra jurisdicción."*
- **[H]** Son objeto de **Aviso** ante la Secretaría (Hacienda, vía UIF): (a) cuando el monto de la operación de cada Cliente/Usuario es **≥ 210 UMA** (= **$24,635.10 MXN** con la UMA 2026), o (b) cuando la comisión/contraprestación cobrada por el servicio es **≥ 4 UMA** (= **$469.24 MXN**).
- **[H]** El encabezado del art. 17 dice que estas actividades son "objeto de **identificación** en términos del artículo siguiente" — es decir, la identificación del cliente (KYC) es obligatoria **sin importar el monto**; solo el *Aviso* a la autoridad tiene umbral.
- **[H]** El art. 18 confirma que las obligaciones (identificar, conocer, verificar identidad, dar aviso) corresponden a **"quienes realicen las Actividades Vulnerables"**, es decir, el sujeto que **ofrece** el servicio de intercambio/custodia a sus Clientes o Usuarios (la plataforma), no al cliente que la usa.
- **[I] Conclusión para `arena-claude-binance`:** nuestra cuenta **no es sujeto obligado** de la fracción XVI. Operamos spot en Binance con fondos propios del dueño, como **Cliente** de una plataforma —no ofrecemos intercambio de activos virtuales a terceros, no administramos una plataforma, no custodiamos activos de clientes de nadie—. El sujeto obligado por esta fracción es **Binance** (la plataforma), que debe identificarnos a nosotros como clientes y dar aviso de operaciones que superen los umbrales. Esto es exactamente lo que ya concluyó el comité el 25-sep-2026 (`bitacora/decisiones/2026-09-25-CRIPTO-inicial.md`: *"Solo le aplica el régimen de actividad vulnerable de la LFPIORPI (art. 17, fr. XVI)"*, refiriéndose a Binance, no a nuestra cuenta) y lo que confirma ahora la lectura directa del texto de la ley, no solo una inferencia de la decisión previa.
- **[I] Lo que sí nos toca indirectamente:** como clientes de un sujeto obligado, es normal (y esperable) que Binance nos pida KYC — ya ocurrió al abrir la cuenta — y que reporte operaciones nuestras que superen los umbrales. Esto es higiene regulatoria del exchange, no una obligación nuestra. El riesgo relevante para nosotros no es de cumplimiento propio, sino de **contraparte**: si Binance incumple sus obligaciones de PLD (como el DOJ investiga por temas de sanciones, sección E5 de `lista-senales-de-alerta.md`), el riesgo es que Binance enfrente una acción regulatoria que afecte el acceso a nuestros fondos — ya cubierto por la contingencia de Bitso.

### 3.2 ISR: no hay ley específica; dos lecturas posibles de la LISR general, con consecuencias materialmente distintas

- **[H]** No existe en México una ley de impuestos específica para cripto. El propio SAT y la literatura fiscal (PRODECON, BDO, despachos) coinciden en que se aplican las reglas **generales** de la LISR, por "ausencia de categoría específica" — esto es coincidencia de fuentes secundarias y de la propia estructura de la ley (no hay ningún artículo de la LISR que mencione "activos virtuales" o "criptomonedas"; lo verifiqué buscando esos términos en el texto completo del PDF oficial y no aparecen).
- **[H]** El art. 119 LISR (Capítulo IV, "De los ingresos por enajenación de bienes") define el ingreso por enajenación de bienes por referencia a los casos de "enajenación" del Código Fiscal de la Federación, un concepto amplio que no distingue entre bienes corpóreos e incorpóreos.
- **[I] Lectura dominante (PRODECON, estudio preliminar no vinculante; mayoría de despachos fiscales consultados en las búsquedas de hoy):** la venta de cripto se trata como **enajenación de bienes** (Capítulo IV, arts. 119-128), por eliminación: no es salario, no es interés, no es dividendo, no es renta de inmueble, y "bien" en el sentido del CFF es lo bastante amplio como para cubrir un activo intangible transferible. Bajo esta lectura, la base gravable es la **ganancia** (precio de venta menos costo comprobado de adquisición, con ajuste por inflación según los arts. 121-124), que se acumula a los demás ingresos del año vía el art. 152.
- **[I] Lectura alternativa, no descartable con el texto que tengo (Capítulo IX, "De los demás ingresos que obtengan las personas físicas", arts. 141-142):** el art. 141 es un **catch-all explícito** para "ingresos distintos de los señalados en los capítulos anteriores", que se acumulan "en el monto en que... incrementen su patrimonio" — una redacción que, leída literalmente y sin el mecanismo de costo comprobado de adquisición del Capítulo IV, podría interpretarse como gravar el **ingreso bruto percibido**, no solo la ganancia. El art. 142 da una lista de ejemplos (deudas perdonadas, ganancia cambiaria, intereses fuera del Capítulo VI, inversiones en sociedades extranjeras, dividendos extranjeros) que **no incluye cripto**, así que esta lectura dependería de que el SAT considerara que cripto *no* cabe en ninguno de los capítulos anteriores (lo que contradice la lectura dominante de Capítulo IV).
- **[H] Dato clave que reduce la importancia práctica de esta ambigüedad para la tasa (no para la base):** el art. 152 LISR, que fija la tarifa progresiva anual, **suma en la misma cuenta los ingresos de los Capítulos I, III, IV, V, VI, VIII y IX** antes de aplicar la tarifa. Es decir: **la tasa marginal es la misma tarifa progresiva (≈1.92% a 35%) sin importar cuál de los dos capítulos se use.** La diferencia real entre las dos lecturas no está en la tasa, sino en **qué tan grande es la base** a la que se le aplica esa tasa (ver ejercicio numérico, §4): el Capítulo IV permite descontar el costo de adquisición; una lectura literal estricta del Capítulo IX, no.
- **[H] Retención del 20% del art. 126 (solo si aplica el Capítulo IV):** "tratándose de la enajenación de **otros bienes** [distintos de inmuebles], el pago provisional será por el monto que resulte de aplicar la tasa del 20% **sobre el monto total de la operación**" (no sobre la ganancia), retenido por el adquirente residente en México — **excepto** cuando se trata de un bien mueble distinto de título-valor/parte social y el monto de la operación es **menor a $227,400.00 MXN** (cifra fija en el texto de la ley, no indexada a UMA). Si el adquirente no es residente en México (como ocurre al vender en un exchange extranjero como Binance, que no tiene residencia fiscal ni establecimiento permanente en México), el texto traslada la obligación al **enajenante**, quien "enterará el impuesto correspondiente mediante declaración... dentro de los quince días siguientes a la obtención del ingreso" — leído de forma literal, esto generaría una carga de **autodeclaración por cada venta** en un exchange extranjero cuando el monto supera $227,400 MXN, sin que exista un criterio oficial del SAT que confirme o descarte esta lectura para exchanges spot extranjeros como Binance.
- **[I] Exención de bienes muebles de uso personal, art. 93 fr. XIX inciso b) — y una corrección a una cifra que circula en blogs fiscales de cripto:** esta fracción exime la ganancia por venta de "bienes muebles, distintos de las acciones, de las partes sociales, de los títulos valor **y de las inversiones del contribuyente**", cuando la ganancia anual no exceda **"tres veces el salario mínimo general del área geográfica del contribuyente elevado al año"**. Varias páginas de impuestos cripto citan una cifra de "**$128,383 MXN**" como el límite de esta exención, atribuyéndola a "3 UMA anuales" — pero el texto de la ley dice **salario mínimo general (SMG)**, no UMA (ambos se desacoplaron en la reforma constitucional de 2016; desde entonces el SMG ha subido más rápido). Con el SMG 2026 (zona general, $315.04/día), **la cifra correcta de esta exención es 3 × $114,989.60 = $344,968.80 MXN anuales, no $128,383.** Esto es una corrección con fuente primaria a una cifra ampliamente repetida en fuentes secundarias (ver §7, registro de errores). **Pero esta exención, leída de forma literal, excluye explícitamente "las inversiones del contribuyente" — y nuestra posición de BTC se trata, en todos los documentos del comité, exactamente como una inversión (filtro de tendencia, Kelly, stop). Si el SAT caracterizara el BTC como inversión (lectura razonable dado cómo lo trata la propia cuenta), esta exención probablemente no aplicaría en absoluto, sin importar el monto.** No hay criterio del SAT que resuelva esta ambigüedad.
- **[O] Mi lectura, con baja-media certeza:** la lectura dominante (Capítulo IV, enajenación de bienes, con descuento de costo) es la más defendible técnicamente y la que seguiría un contador conservador, pero **no es una regla escrita explícitamente para cripto** — es una analogía razonada ante el silencio de la ley, respaldada solo por un estudio preliminar no vinculante de PRODECON. El dueño debería tratar esto como una zona gris real, no como una regla clara, y consultar a su contador antes de declarar.

## 4. Ejercicio numérico (verificado dos veces: ejecución directa + revisión manual de cada cifra)

```python
UMA_DIARIA_2026 = 117.31   # INEGI/DOF 9-ene-2026 (secundario, convergente en 5 fuentes)
SMG_DIARIO_2026 = 315.04   # CONASAMI, vigente desde 1-ene-2026 (secundario, convergente en 3 fuentes)

# 1) Umbrales de Aviso de LFPIORPI art.17 fr.XVI (texto primario, DOF 16-07-2025)
umbral_aviso_operacion = 210 * UMA_DIARIA_2026   # = 24,635.10 MXN
umbral_aviso_comision = 4 * UMA_DIARIA_2026      # = 469.24 MXN

# 2) Posicion real (boleta bitacora/boletas/2026-09-29-binance-5000.md)
btc_comprado = 0.001325
costo_mxn = 1996.67
# Monto de esa compra (1,996.67 MXN) esta MUY por debajo del umbral de Aviso (24,635.10 MXN)

# 3) Valuacion hoy (4-oct-2026, venta hipotetica), con datos vivos de esta corrida
btc_usdt_hoy = 85192.01    # Binance ticker 24hr, ~14:25 UTC 4-oct-2026
usdmxn_hoy = 18.145        # Yahoo MXN=X, ultimo dato disponible (fin de semana)
precio_mxn_btc_hoy = btc_usdt_hoy * usdmxn_hoy          # = 1,545,809.02 MXN/BTC
valor_hoy_mxn = btc_comprado * precio_mxn_btc_hoy       # = 2,048.20 MXN
ganancia_nominal = valor_hoy_mxn - costo_mxn            # = 51.53 MXN (2.58% en 5 dias)

# 4) Pago provisional art.126: 20% del TOTAL si >= $227,400 MXN y no es titulo-valor/parte social
umbral_retencion_mxn = 227400.00   # cifra fija en el texto de la ley
# 2,048.20 MXN << 227,400.00 MXN -> EXENTA de retencion/pago provisional

# 5) Comparacion de base gravable segun el capitulo de la LISR que se use
base_cap_IV = ganancia_nominal        # Cap.IV: base = ganancia (venta - costo), arts.119-124
base_cap_IX = valor_hoy_mxn           # Cap.IX, lectura literal estricta del art.141: todo lo percibido
# base_cap_IX / base_cap_IV = 39.8x mas base bajo la lectura estricta de Cap.IX

# 6) Tarifa anual art.152 (aprox. 2025 como proxy de 2026; la cifra exacta 2026 no esta en el
#    texto de la ley misma, se indexa cada enero por INPC via Anexo 8 RMF -- declarado como
#    aproximacion, no como cifra primaria verificada)
# Bracket 1 (hasta 8,952.49): cuota fija 0, tasa 1.92%
isr_cap_IV = base_cap_IV * 0.0192     # = 0.99 MXN
isr_cap_IX = base_cap_IX * 0.0192     # = 39.33 MXN (39.8x mas, mismo bracket, misma tasa)

# 7) Escala realista: venta hipotetica de 0.05 BTC (costo 50,000 MXN a 1,000,000 MXN/BTC)
btc_2 = 0.05
costo_2 = 50000.00
valor_2 = btc_2 * precio_mxn_btc_hoy            # = 77,290.45 MXN
ganancia_2 = valor_2 - costo_2                  # = 27,290.45 MXN
# Cap.IV (bracket 2, cuota fija 171.88 + 6.40% del excedente sobre 8,952.50): ISR ~= 1,345.51 MXN
# Cap.IX (bracket 3, cuota fija 4,461.94 + 10.88% del excedente sobre 75,984.56): ISR ~= 4,604.02 MXN
# Diferencia: 3,258.51 MXN (242% mas ISR bajo la lectura estricta de Cap.IX) -- la ambiguedad
# SI importa a escala realista, aunque a escala de nuestra posicion actual (51 MXN de ganancia)
# sea trivial en pesos absolutos.
# Monto de esta venta (77,290.45 MXN) SI supera el umbral de Aviso de LFPIORPI (24,635.10 MXN)
# -- pero ese umbral aplica a la plataforma obligada (Binance), no a esta cuenta.

# 8) Exencion del art.93 fr.XIX inciso b): correccion de la cifra "3 UMA" que circula en blogs
uma_anual_2026 = UMA_DIARIA_2026 * 365          # = 42,818.15
cifra_blog_3_uma = 3 * uma_anual_2026           # = 128,454.45 MXN (cifra que citan varios blogs)
smg_anual_2026 = SMG_DIARIO_2026 * 365          # = 114,989.60
cifra_correcta_3_smg = 3 * smg_anual_2026       # = 344,968.80 MXN (texto real de la ley: SMG, no UMA)
# La cifra correcta es 2.69x mayor que la que circula en blogs de impuestos cripto.
# Ademas, el texto EXCLUYE "las inversiones del contribuyente" de esta exencion.
```

**Resultados clave (verificados):**

| Concepto | Valor |
|---|---|
| Umbral de Aviso LFPIORPI, por operación (210 UMA) | **$24,635.10 MXN** |
| Umbral de Aviso LFPIORPI, por comisión (4 UMA) | **$469.24 MXN** |
| Nuestra compra real del 29-sep (1,996.67 MXN) vs. umbral de Aviso | **muy por debajo** (8.1% del umbral) |
| Ganancia nominal hoy de la posición real (si se vendiera) | **51.53 MXN** (2.58% en 5 días) |
| Umbral de retención/pago provisional (art. 126) | **$227,400.00 MXN** (cifra fija, no indexada) |
| Base gravable: Cap. IV (ganancia) vs. Cap. IX (ingreso bruto), posición actual | **51.53 vs. 2,048.20 MXN** (39.8× de diferencia) |
| Misma comparación, venta hipotética de 0.05 BTC | ISR ~1,345.51 (Cap. IV) vs. ~4,604.02 MXN (Cap. IX); 242% más con la lectura estricta |
| Exención art. 93 fr. XIX-b): cifra que circula en blogs (3×UMA) | $128,454.45 MXN — **incorrecta** |
| Exención art. 93 fr. XIX-b): cifra correcta con el texto de la ley (3×SMG) | **$344,968.80 MXN** |

## 5. Qué cambia para la cuenta

- **No cambia nada operativo hoy:** nuestra posición real (0.001325 BTC, ganancia nominal de ~52 MXN) está muy por debajo de cualquier umbral relevante (retención del art. 126, Aviso de LFPIORPI, incluso la exención mal citada de los blogs). No hay acción fiscal inmediata que tomar.
- **Se confirma con lectura directa de la ley** (no solo con la inferencia de la decisión del 25-sep) que `arena-claude-binance` **no es sujeto obligado** de la LFPIORPI fr. XVI: somos cliente de una plataforma, no la plataforma. El riesgo regulatorio relevante sigue siendo el de contraparte (Binance), ya cubierto por la contingencia de Bitso y por la revisión semanal de `lista-senales-de-alerta.md`.
- **Para el dueño, de cara a su declaración anual (fuera del alcance de esta cuenta, pero relevante para él como persona física):** debe declarar cualquier ganancia por venta de cripto (no hay umbral de exención claro y aplicable; la exención de bienes muebles del art. 93 probablemente no aplica a una posición tratada como inversión), preferentemente bajo el régimen de enajenación de bienes (Capítulo IV, con descuento de costo), y debe consultar a su contador sobre si existe alguna obligación de autodeclaración dentro de 15 días por operación bajo el art. 126 cuando el monto supere $227,400 MXN en un exchange extranjero — esto no está resuelto por ningún criterio oficial que haya encontrado.
- **Para la base de conocimiento:** se corrige la cifra "$128,383 MXN de exención (3 UMA)" que circula en varias páginas de impuestos cripto; el texto real de la ley usa el salario mínimo general, no la UMA, y el límite correcto es de $344,968.80 MXN — además de que la exención probablemente no cubre una posición caracterizada como inversión. Se registra en `conocimiento/registro-de-errores.md` como una corrección a una fuente externa (no a un error propio previo de esta base), con fuente primaria (ley) para la corrección.

## 6. Contrapuntos y límites

- **No hay criterio oficial del SAT ni jurisprudencia** que resuelva cuál capítulo de la LISR aplica a cripto. La lectura de Capítulo IV (enajenación de bienes) es la dominante entre PRODECON (estudio preliminar, no vinculante) y despachos fiscales, pero sigue siendo una analogía razonada, no una regla escrita. Un cambio de postura del SAT (o una miscelánea fiscal futura que mencione expresamente activos virtuales) podría cambiar esta conclusión sin aviso previo.
- **La cifra de UMA y de SMG 2026 son secundarias** (prensa especializada convergente), no verificadas contra el DOF/INEGI/CONASAMI de forma directa en esta corrida (ambas páginas oficiales son dinámicas y no expusieron el dato a `WebFetch`). El riesgo de error es bajo porque convergen 3-5 fuentes independientes para cada cifra, pero no es lectura de fuente primaria.
- **La tarifa del art. 152 usada en el ejercicio (§4) es la de 2025**, como aproximación; la tarifa exacta 2026 (indexada por INPC vía Anexo 8 de la RMF) no está en el texto de la ley misma y no la verifiqué en esta corrida. El efecto sobre las conclusiones cualitativas (qué capítulo aplica, qué umbrales existen) es nulo; sí cambiaría las cifras exactas de ISR en pesos del ejercicio a escala realista (§4.7).
- **La pregunta de si el art. 126 genera una obligación de autodeclaración en 15 días por cada venta en un exchange extranjero** es una lectura literal mía del texto, no confirmada por ningún criterio oficial — podría ser una lectura excesivamente estricta (es plausible que la práctica fiscal real sea declarar la ganancia anual sin pagos provisionales individuales cuando no hay fedatario ni retenedor), pero no encontré fuente que lo zanjara.
- **No investigué el IVA** (si la venta de cripto por un particular sin actividad empresarial habitual causa IVA); el enfoque de esta ficha fue estrictamente ISR y LFPIORPI, como pidió la rutina.

## 7. Autoexamen

- ¿Puedo reproducir las conclusiones sin ver la ficha? Sí: (1) LFPIORPI art. 17 fr. XVI obliga a quien *ofrece* el intercambio a clientes (la plataforma), no al cliente — texto del art. 18 lo confirma; (2) no hay ley específica de ISR cripto, así que se aplican las reglas generales de la LISR, con dos lecturas posibles (Capítulo IV vs. IX) que comparten tarifa (art. 152) pero difieren en la base gravable; (3) el umbral de retención del art. 126 es $227,400 MXN fijo, no indexado a UMA.
- ¿Qué rompería la conclusión? Un criterio normativo oficial del SAT que diga explícitamente "la venta de activos virtuales se grava conforme al Capítulo IX" (o IV) zanjaría la ambigüedad central de esta ficha. Una reforma a la LFPIORPI que incluyera a los clientes finales (no solo a las plataformas) como sujetos obligados cambiaría la conclusión sobre nuestra cuenta — no hay indicio de que esto esté en curso.
- **Grado: B** para los hechos de texto de ley leídos directamente (LISR y LFPIORPI, con número de artículo y cita exacta) y para la conclusión de que `arena-claude-binance` no es sujeto obligado de la fr. XVI. **C** para la caracterización del régimen de ISR aplicable (Capítulo IV vs. IX), por ser una analogía doctrinal sin criterio oficial que la resuelva. **D** para cualquier cifra de ISR en pesos que dependa de la tarifa 2026 exacta del art. 152 (usé la de 2025 como proxy) o de si existe de verdad una obligación de autodeclaración en 15 días por venta en exchange extranjero.

## 8. Estado del pendiente

- Tema 6 de "Temas que no cubren los 35 recursos" (`00-plan-de-estudio.md`): **completado** con lectura directa de las dos leyes primarias relevantes (LISR, LFPIORPI) y un ejercicio numérico propio verificado dos veces. Con esto se cubren los 6 temas de la lista.
- Pendiente para una sesión futura: buscar si existe algún criterio normativo o no vinculativo del SAT específico sobre cripto (no lo encontré hoy, pero la búsqueda no fue exhaustiva en el portal del SAT mismo, que no exploré directamente por falta de tiempo en esta corrida); revisar si una futura Miscelánea Fiscal (2027) menciona expresamente activos virtuales; verificar la tarifa 2026 exacta del art. 152 contra el Anexo 8 de la RMF 2026.
- Actualiza el capítulo de síntesis `04-riesgos-fraude-hackeos-y-seguridad.md` (adenda fechada 4-oct-2026, nueva sección §7) y `conocimiento/estado-de-dominio.csv` (fila `cripto/04`).

Datos crudos de esta sesión (PDF de LISR y LFPIORPI, texto extraído, script del ejercicio): `scratchpad` de esta corrida (fuera del repositorio).
