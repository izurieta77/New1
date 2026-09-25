# B4. Fiscalidad comparada (casa de bolsa mexicana vs. bróker extranjero) y otros brókers extranjeros

**Fecha de corte:** 2026-09-25. Todas las fuentes se consultaron ese día, salvo que se indique otra fecha.
**Frente:** B4 de `arena/investigacion/brokers/`.
**Qué no se repite aquí (solo se cita):**
- La línea base de GBM: `B1-gbm-linea-base-.md` y `../01-gbm-operativa-y-costos.md`.
- Las casas de bolsa y apps mexicanas (Actinver Trade, Kuspit, Finamex, Webull México, Hapi, Revolut): `B2-casas-de-bolsa-y-apps-mexicanas.md`.
- El texto del art. 129 LISR, el 10% de los dividendos, la tarifa sucesoria, los tratados y la liquidez de los UCITS en el SIC: `laboratorio/replicas/V05-spiva-y-fiscalidad-sic/` (`resultados.json`, `datos/legal/`).
- Interactive Brokers: le corresponde a otro frente (B3). Aquí solo aparece como referencia.

`conocimiento/11-mexico` no existe en el repo.

**Pregunta:** para una persona física residente en México con una cuenta de ~20,000 MXN que compite en rendimiento % contra IAs que se quedan en GBM, ¿cómo cambia el régimen fiscal si opera con un bróker extranjero en lugar de una casa de bolsa mexicana? ¿Y qué otros brókers extranjeros (además de IBKR) aceptan residentes mexicanos en 2026, y con qué costos?

**Etiquetas:**
- **[H]** Hecho con fuente y fecha.
- **[C]** Cálculo propio sobre hechos citados. El método está a la vista.
- **[I]** Inferencia (interpretación mía de la ley o de los datos).
- **[R]** Recomendación para la cuenta arena.
- **(no verificado)**: no lo confirmé en fuente oficial, o solo aparece en fuentes secundarias o en resúmenes del buscador.

**Esto no es asesoría fiscal.** El documento describe normas vigentes con su fuente. Antes de operar con un bróker extranjero, conviene que un contador confirme los puntos marcados como [I].

---

## Resumen ejecutivo

1. **[H] Hallazgo principal: B1 y B2 estaban mal en un punto.** B1 (§5) y B2 (§1) infirieron que vender en NYSE o Nasdaq con un bróker extranjero "no parece caber en el art. 129". **El SAT dice lo contrario para las acciones extranjeras listadas en el SIC.** El **criterio normativo 37/ISR/N** (Anexo 7 de la RMF 2026, DOF 09-01-2026) dice textualmente que las ganancias por vender acciones de sociedades extranjeras listadas en el SIC de la BMV o de BIVA "están sujetas a una tasa del 10% en los términos del artículo 129, fracción I de la Ley del ISR, **con independencia de que su enajenación no se realice a través de un intermediario del mercado de valores mexicano**" [4]. El mismo art. 129 prevé ese caso: quien opera con "entidades financieras extranjeras" no autorizadas por la LMV calcula su propia ganancia o pérdida y guarda los estados de cuenta [1].
2. **[H] ¿Hubo cambios en 2026?** La LISR **no se ha reformado desde el DOF 01-04-2024** (historial de reformas de la Cámara de Diputados) [2]. El Paquete Económico 2026 no tocó la LISR [2]. La RMF 2026 salió en el DOF el 28-12-2025 [3] y su Anexo 7 el 09-01-2026 [4]. **[I]** El art. 129 que leyeron B1 y B2 sigue vigente sin cambios.
3. **Mapa fiscal por instrumento (persona física, ganancia por venta):**

   | Instrumento vendido | Con casa de bolsa mexicana (BMV/SIC) | Con bróker extranjero (NYSE/Nasdaq) |
   |---|---|---|
   | Acción extranjera **listada en el SIC** (NVDA, MSFT, MA, LLY, AVGO, XOM, AMD…) | **10% definitivo**, art. 129 fr. I [H] | **10% definitivo**, art. 129 fr. I y criterio 37/ISR/N [H] |
   | ADS/ADR de emisora **mexicana** en NYSE/Nasdaq (p. ej. Vesta VTMX, OMA OMAB) | 10% fr. I (vendiendo la serie local en la BMV) [H] | **10%**, fr. III: bolsas de "mercados reconocidos" (art. 16-C fr. II CFF) de países con tratado [H texto; I aplicación] |
   | **ETF** extranjero listado en el SIC (SPY, QQQ, TQQQ, SOXL…) | **10%**, fr. II ("títulos que representen índices accionarios enajenados en las bolsas") [H] | **Sin confirmar.** La fr. II exige que la venta sea en bolsa concesionada, y el criterio 37 solo habla de "acciones". El IMCP sostiene que un ETF constituido como sociedad y listado en el SIC cabe en la fr. I [7]. **(no verificado con el SAT)** |
   | Acción o ETF **no listado** en el SIC | No se puede comprar (LMV art. 9: vía SIC) [4] | **Fuera del art. 129** [I]: "enajenación de bienes" (arts. 119-122 LISR), **acumulable a tarifa progresiva** (hasta 35%, art. 152) y posible **pago provisional de 20% sobre el monto total** en 15 días (art. 126) [H texto; I aplicación] |
   | ETF "transparente" (*grantor trust*: oro, bitcoin) | — | Según el IMCP, se acumula el ingreso **cada año aunque no se venda** (arts. 4-A/4-B LISR) [7] (secundaria profesional) |

4. **[H] Dividendos de EUA.**
   - La retención en EUA es la misma en ambas rutas: **30% sin W-8BEN y 10% con W-8BEN** (tratado EUA-México, art. 10) [12].
   - **Con casa de bolsa mexicana,** el intermediario retiene el **10% adicional mexicano** y da constancia (RMF 2026, reglas 3.11.7 y 3.1.7) [3].
   - **Con bróker extranjero, nadie retiene ese 10%.** Tú lo **pagas por tu cuenta a más tardar el día 17 del mes siguiente** (art. 142 fr. V). Además acumulas el dividendo en la declaración anual y acreditas el impuesto de EUA (art. 5) [1].
   - **La retención de EUA por encima de la tasa del tratado no se puede acreditar en México** (el 20% extra que se pierde sin W-8BEN). Solo se recupera si un procedimiento amistoso termina en acuerdo (art. 5 LISR y criterio 5/ISR/N) [1][4]. **[I] El W-8BEN no es opcional en ningún bróker.**
5. **[H] En EUA no pagas impuesto por tus ganancias.** La fuente de la venta de bienes muebles la determina el *tax home* del vendedor [9]. Un residente mexicano sin *tax home* en EUA no paga impuesto allá por vender acciones. En ambas rutas.
6. **[H] Pérdidas.**
   - **Bajo el art. 129:** solo se compensan contra ganancias del art. 129, en el ejercicio o en los **10 siguientes**, actualizadas. Si pudiste aplicarlas y no lo hiciste, se pierden [1].
   - **Fuera del art. 129** (enajenación de bienes): se aplican en el año o en los **3 siguientes**, contra otros ingresos salvo salarios y actividad empresarial, y con los requisitos del reglamento (arts. 121-122) [1].
7. **[H] Impuesto sucesorio de EUA (confirma y actualiza V05).**
   - La acción de una sociedad constituida en EUA está sujeta al impuesto "aun si el no residente tenía los certificados en el extranjero". El umbral para declarar es **60,000 USD** (página del IRS revisada el 27-jun-2026) [8].
   - No hay tratado sucesorio entre EUA y México [14] (V05).
   - **[I]** La custodia vía SIC/Indeval **no cambia el *situs* legal** [14][15]. Si cambia en la práctica, no está verificado.
   - **UCITS irlandeses:** el fondo paga **15%** sobre los dividendos de EUA (tratado EUA-Irlanda). Irlanda no retiene nada al inversionista no residente [16]. Una acción de una sociedad extranjera (una *plc* irlandesa) no tiene *situs* en EUA [14].
   - **[C]** Con 20k MXN (~1,130 USD) esto es irrelevante. Solo importa si la cuenta pasa de ~1.06 M MXN en activos de EUA, a 17.70 MXN/USD [36].
8. **[H] Otros brókers extranjeros (sin IBKR):**
   - **Firstrade:** acepta México (lista oficial actualizada el 07-may-2026). Sin mínimo, US$0 en acciones, ETFs y opciones, wire de entrada sin comisión y **US$25 por wire de salida** [22][23][24].
   - **Schwab International:** tiene un flujo de apertura propio para residentes de México. US$0 en acciones y ETFs de EUA y US$0.65 por contrato de opciones [18][19]. **El mínimo actual no está verificado** (fuentes secundarias dicen que se eliminó el de 25,000 USD) [21].
   - **tastytrade:** US$0 en acciones y ETFs más un *clearing* de US$0.0008 por acción. Opciones a US$1 por contrato al abrir (máx. US$10 por pierna) y US$0 al cerrar. **US$45 por wire de salida al extranjero** [26][27]. Que México esté en la lista de países lo dice solo el resumen del buscador; la página oficial no se pudo leer [29] **(no verificado directo)**.
   - **Saxo:** **no atiende a México** (lista oficial, 28-jul-2026) [30].
   - **eToro:** US$1 o US$2 por abrir y cerrar posiciones en acciones según el país. Cobra conversión por depósitos en MXN (no publica la tasa) y US$5 por retiro [31]. Que acepte México sale solo de fuentes secundarias [32][33].
   - **Webull México:** "cero comisiones" y tipo de cambio "competitivo" sin cifra. Los valores de EUA quedan en Webull Financial LLC [34] (ver B2).
9. **[C] Costo de fricción de un bróker extranjero con 20k (sección 5).**
   - **Entrada:** convertir 20,000 MXN a USD con Wise costó **193.84 MXN (0.97%)** en la cotización en vivo del 25-sep-2026, a una tasa media de 17.70 MXN/USD [36].
   - **Salida** (si la temporada termina en pesos): wire de US$25 (Firstrade) o US$45 (tastytrade), más ~1.1% de conversión de regreso [37]. Sube el total a **~4.3% (Firstrade) o ~6.0% (tastytrade)**.
   - **Contra GBM** (0.58% por ida y vuelta, B2): el bróker extranjero gana si la cuenta rota **más de ~1.7 veces** (contando solo la entrada) o **más de ~7.4 veces** (Firstrade, contando la salida).
10. **[R] Veredicto de B4** (lo fiscal no decide el torneo, pero sí el neto del dueño):
    - **Para el marcador (TWR), el régimen fiscal casi no pesa.** El ISR sobre ganancias se paga en la declaración anual, fuera de la cuenta (B1). En dividendos, el bróker extranjero **resta menos dentro de la cuenta**: 10% contra 19% con W-8BEN en el SIC, porque el 10% mexicano lo pagas por fuera.
    - **Para el neto del dueño, un bróker extranjero es fiscalmente equivalente al SIC solo si te limitas a acciones listadas en el SIC y a ADS de emisoras mexicanas.** Comprar ETFs, sobre todo los apalancados, o acciones fuera del SIC con un bróker extranjero abre el riesgo de tributar a tarifa progresiva de hasta 35%, además del pago provisional de 20% sobre el monto bruto.
    - **Entre los brókers extranjeros de B4, el candidato verificado más barato es Firstrade.** Pero **ninguno de los de B4 da acceso a la BMV** (Peñoles y Grupo México están en tu radar). El único bróker extranjero que podría cubrir EUA y la BMV a la vez es IBKR (B3).

---

## 1. Ganancias por venta: casa de bolsa mexicana contra bróker extranjero

### 1.1 Texto de la ley (LISR vigente, última reforma DOF 01-04-2024) [1][2]

- **[H] Art. 129, primer párrafo:** 10% definitivo sobre las ganancias del ejercicio por:
  - **Fr. I:** acciones de sociedades mexicanas "cuando su enajenación se realice en las bolsas de valores concesionadas [...] **o de acciones emitidas por sociedades extranjeras cotizadas en dichas bolsas de valores**".
  - **Fr. II:** "títulos que representen índices accionarios **enajenados en las bolsas de valores** o mercados de derivados a que se refiere la fracción anterior".
  - **Fr. III:** acciones de sociedades mexicanas (o títulos que representen exclusivamente esas acciones) vendidas "en bolsas de valores o mercados de derivados ubicados en **mercados reconocidos** a que se refiere la fracción II del artículo 16-C del CFF **de países con los que México tenga en vigor un tratado** para evitar la doble tributación".
- **[H] Art. 129, párrafo de las entidades extranjeras:** "Los contribuyentes que realicen las enajenaciones [...] a través de contratos de intermediación que tengan con **entidades financieras extranjeras** que no estén autorizados conforme a la Ley del Mercado de Valores, **deberán calcular la ganancia o pérdida fiscales del ejercicio** y, en su caso, el impuesto que corresponda, así como **tener a disposición de la autoridad fiscal los estados de cuenta**". El párrafo de agregación también suma lo operado con "entidades financieras extranjeras con los que tenga un contrato de intermediación" [1].
- **[H] Art. 129, declaración:** "Los contribuyentes deberán presentar declaración por las ganancias obtenidas conforme a esta Sección [...] de manera conjunta a la declaración anual a que se refiere el artículo 150" [1].
- **[H] Art. 16-C, fr. II del CFF** (última reforma DOF 09-04-2026). Son mercados reconocidos "las bolsas de valores y los sistemas equivalentes de cotización [...] que cuenten al menos con cinco años de operación y de haber sido autorizados para funcionar con tal carácter de conformidad con las leyes del país en que se encuentren, donde los precios [...] sean del conocimiento público y no puedan ser manipulados" [5].
  - **[I]** NYSE y Nasdaq cumplen esa definición.
  - **[I]** Un mercado OTC (*over the counter*) no es una "bolsa". Por eso vender en OTC los títulos de Grupo México o Peñoles en EUA (si existen) probablemente no entra en la fr. III **(no verificado)**.

### 1.2 Qué dice la autoridad (RMF 2026 y Anexo 7) [3][4]

- **[H] Criterio 37/ISR/N**, "Acciones emitidas por sociedades extranjeras cotizadas en bolsas de valores concesionadas. Su enajenación está sujeta a la tasa del 10%" (Anexo 7 RMF 2026, DOF 09-01-2026; su primer antecedente es el criterio 46/2014/ISR). Se apoya en el art. 9, tercer párrafo de la LMV: la intermediación con valores extranjeros susceptibles de listarse en el SIC "únicamente podrá[n] proporcionarse a través de dicho sistema". Concluye: las ganancias por vender acciones de sociedades extranjeras "listadas en el apartado de valores autorizados para cotizar en el Sistema Internacional de Cotizaciones [...] están sujetas a una tasa del 10% [...] **con independencia de que su enajenación no se realice a través de un intermediario del mercado de valores mexicano**" [4].
- **[H] Regla 3.2.12 (RMF 2026):** los valores listados en el SIC de la BMV o de BIVA se consideran "colocados entre el gran público inversionista" [3]. Esto importa para la excepción del numeral 1 del último párrafo del art. 129.
- **[H] Regla 3.15.10:** cuando el intermediario que vende no custodia los títulos, el titular declara bajo protesta el costo promedio actualizado y conserva la documentación [3]. **[I]** Es la regla de un traspaso entre intermediarios mexicanos. No aplica a un bróker extranjero, donde el cálculo completo es tuyo.
- **[H] Regla 3.11.9:** permite calcular una sola base sumando las ganancias y pérdidas de los arts. 88 (fondos de inversión) y 129 [3].

### 1.3 El hueco de los ETFs con bróker extranjero

- **[H]** El criterio 37 habla solo de "**acciones** emitidas por sociedades extranjeras" [4]. La fr. II, la que cubre los ETFs, exige que la venta sea "en las bolsas de valores" concesionadas [1].
- **[H, fuente secundaria profesional]** El IMCP (Comisión Fiscal, *Fisco Actualidades* 122, abr-2024, C.P.C. Allen Saracho Carrillo) sostiene lo siguiente [7]:
  - "el artículo 129 de la LISR no requiere que la enajenación de acciones emitidas por sociedades extranjeras se realice en bolsa de valores concesionada". Por eso un ETF constituido como sociedad y listado en el SIC tributaría al 10% por la fr. I, aunque se venda en el extranjero.
  - En cambio, si el ETF es un vehículo fiscalmente transparente (un *grantor trust* como los ETFs de bitcoin), los residentes en México acumulan el ingreso "aun cuando no sean distribuidos" (arts. 4-A y 4-B LISR).
- **[H, secundaria]** Un portal de divulgación afirma que el criterio 37 "también alcanza a acciones y ETFs de EE. UU. listados en el SIC" [39]. Eso **no está en el texto del criterio**.
- **[I]** Muchos ETFs de EUA no son "sociedades" en sentido estricto. SPY es un *unit investment trust*, y los iShares o ProShares son series de *trusts* de Delaware (estructura legal de cada ETF: **no verificada**). Para el SAT, que un *trust* que tributa como RIC (*regulated investment company*) cuente como "sociedad extranjera" que emite "acciones" es una **pregunta abierta**.
- **[R]** Con un bróker extranjero, **el tratamiento fiscal de TQQQ, SOXL, SPXL, QQQ y compañía es incierto.** Con una casa mexicana, el 10% de la fr. II es claro (los tres apalancados están listados en la BMV, según B1). **Si la estrategia depende de ETFs, el SIC es la ruta fiscalmente segura.**

### 1.4 Qué pasa fuera del art. 129 (acciones o ETFs no listados en el SIC, con bróker extranjero)

- **[H] Art. 120:** la ganancia se divide entre los años de tenencia (máximo 20). Esa parte se suma a los demás ingresos y se grava con la tarifa progresiva del art. 152 (**hasta 35%**). El resto se grava a la tasa efectiva que resulte [1].
- **[H] Art. 126, cuarto párrafo:** "Tratándose de la enajenación de otros bienes, el pago provisional será por el monto que resulte de aplicar la tasa del **20% sobre el monto total de la operación** [...]. En el caso de que el adquirente no sea residente en el país [...], el enajenante enterará el impuesto correspondiente mediante declaración [...] **dentro de los quince días siguientes** a la obtención del ingreso" [1].
  - **[I]** Leído al pie de la letra, cada venta de un título no listado en el SIC hecha con un bróker extranjero obligaría a un pago provisional de 20% del valor **bruto** vendido en 15 días, que se recupera en la declaración anual. **No encontré regla de la RMF 2026 ni criterio que lo exima o lo confirme** para operaciones bursátiles en el extranjero **(no verificado)**. Para una cuenta que rota, sería un problema de liquidez del dueño, fuera de la cuenta.
- **[H] Pérdidas (arts. 121-122):** se aplican en el año o en los 3 siguientes, contra ingresos distintos de salarios y actividad empresarial, y con requisitos del reglamento para las acciones [1].
- **[I]** Un ETF transparente (oro físico, bitcoin *spot*) comprado con cualquier bróker tributaría como si tuvieras el subyacente, año por año [7].

### 1.5 Tabla comparada completa (persona física residente)

| Tema | Casa de bolsa mexicana (GBM, Actinver, Kuspit…) | Bróker extranjero (Firstrade, Schwab, tastytrade, IBKR…) | Fuente |
|---|---|---|---|
| Venta de acción extranjera listada en el SIC | 10% definitivo, fr. I | 10% definitivo, fr. I y criterio 37/ISR/N | [1][4] |
| Venta de ETF listado en el SIC | 10% definitivo, fr. II | **Incierto** (fr. II exige bolsa concesionada; el criterio 37 dice "acciones"); IMCP: 10% si el ETF es sociedad | [1][4][7] |
| Venta de ADS de emisora mexicana en NYSE/Nasdaq | (se vende la serie local en la BMV) 10% | 10%, fr. III (EUA tiene tratado; NYSE/Nasdaq cumplen el art. 16-C fr. II) | [1][5] + [I] |
| Venta de título no listado en el SIC | No disponible | Enajenación de bienes: acumulable, tarifa hasta 35%, pago provisional de 20% del bruto en 15 días | [1] + [I] |
| Quién calcula la ganancia | El intermediario, con constancia anual | **Tú.** Guardas los estados de cuenta | [1] |
| Retención en la venta | Ninguna | Ninguna | [1], B1 |
| Declaración | Anual, junto con la del art. 150 | Anual, igual; más los pagos del 17 del mes siguiente por dividendos | [1] |
| Compensación de pérdidas | Solo contra art. 129, 10 años | Igual si es art. 129; 3 años si es enajenación de bienes | [1] |
| Impuesto de EUA sobre la ganancia | 0 (fuente = *tax home* del vendedor) | 0 | [9] |
| Retención de EUA sobre dividendos | 30% / 10% con W-8BEN | 30% / 10% con W-8BEN | [12], B1 |
| 10% mexicano sobre dividendos del extranjero | Lo retiene el intermediario (RMF 3.11.7) | **Lo pagas tú a más tardar el día 17 del mes siguiente** (art. 142 fr. V) | [1][3] |
| Acumular el dividendo y acreditar el impuesto de EUA | Con la constancia (RMF 3.1.7, vía Indeval) | Con el 1042-S u otro comprobante del bróker (art. 5: "contar con la documentación comprobatoria") | [1][3] |
| Retención de EUA por encima del tratado (sin W-8BEN) | No acreditable salvo procedimiento amistoso | Igual | [1][4] |
| Visibilidad ante el SAT | Constancias e información de intermediarios (declaración informativa IEF, RMF 3.5.22) | FATCA México-EUA (IGA Modelo 1, abr-2014). Que la reciprocidad cubra estas cuentas: **secundaria/inferencia** | [3][38] |
| REFIPRE (art. 176) | No aplica | No aplica a una participación de menudeo: exige "control efectivo" (>50%) | [1] + [I] |

---

## 2. Dividendos y acreditamiento: detalle

- **[H] Art. 142 fr. V LISR:** las personas físicas que reciben dividendos de sociedades residentes en el extranjero, "además de acumularlos [...], deberán enterar de forma adicional, el impuesto sobre la renta que se cause por multiplicar la tasa del 10%, al monto al cual tengan derecho del dividendo o utilidad efectivamente distribuido [...], sin incluir el monto del impuesto retenido". Ese pago "tendrá el carácter de definitivo y deberá ser enterado a más tardar el día 17 del mes siguiente" [1].
- **[H] RMF 2026, regla 3.11.7:** cuando el dividendo llega a través de bolsas concesionadas o mercados reconocidos del art. 16-C fr. I (es decir, de México) donde coticen las acciones, **los intermediarios financieros retienen y enteran** ese 10% por cuenta del contribuyente [3]. **[I]** Un bróker extranjero no está sujeto a esa regla, así que el pago mensual es tuyo.
- **[H] Art. 5 LISR (personas físicas):** el ISR extranjero acreditable "no excederá de la cantidad que resulte de aplicar lo previsto en el Capítulo XI del Título IV [...] a los ingresos [...] de fuente de riqueza ubicada en el extranjero". El límite se calcula por país. Si no se puede acreditar dentro de ese límite, se acredita en los 10 ejercicios siguientes [1].
- **[H] Art. 5, párrafo del exceso sobre el tratado, y criterio 5/ISR/N:** "Los contribuyentes que hayan pagado en el extranjero el impuesto sobre la renta en un monto que exceda al previsto en el tratado [...] sólo podrán acreditar el excedente [...] una vez agotado el procedimiento de resolución de controversias contenido en ese mismo tratado" [1]. El criterio 5/ISR/N agrega que solo se puede acreditar si el procedimiento amistoso "concluya con un acuerdo y lo acepten" [4].
- **[C] Carga total sobre un dividendo de EUA de 100 USD.** El bróker extranjero **resta menos dentro de la cuenta**, aunque la carga total del dueño sea la misma (con W-8BEN):

  | Ruta | Retención EUA | 10% México | Carga total | Lo que sale **de la cuenta** |
  |---|---|---|---|---|
  | SIC sin W-8BEN (GBM, B1) | 30 | 7.0 (10% de 70) | 37.0 | 37.0 |
  | SIC con W-8BEN | 10 | 9.0 | 19.0 | 19.0 |
  | Bróker extranjero con W-8BEN | 10 | 9.0 (tú, por fuera) | 19.0 | **10.0** |
  | Bróker extranjero sin W-8BEN | 30 | 7.0 | 37.0 (los 20 de exceso no se acreditan) | 30.0 |

  Además, el dividendo se acumula en la anual y el 10% de EUA se acredita dentro del límite del art. 5, así que la carga final depende de la tasa marginal del dueño (no calculado). **[C]** Con un rendimiento por dividendo de ~1% (SPY, V05 [17]), la diferencia de TWR entre "SIC con W-8BEN" y "extranjero con W-8BEN" es de ~0.09% al año. Es irrelevante para el torneo.
- **[H] W-8BEN:** en general tiene vigencia desde la firma hasta el último día del **tercer año calendario siguiente** (instrucciones del IRS, rev. oct-2021) [11]. En Firstrade forma parte de la solicitud de apertura internacional [22]. En GBM-SIC cuesta 75 USD + IVA (B1); en Actinver Trade es gratis (B2).

---

## 3. Impuesto sucesorio de EUA y ETFs UCITS

- **[H] IRS (página revisada el 27-jun-2026):** el patrimonio de un no residente no ciudadano debe declarar (Form 706-NA) si el valor de sus activos con *situs* en EUA supera **60,000 USD**. Estos incluyen "Stock of corporations organized in or under U.S. law, even if the nonresident held the certificates abroad" [8].
- **[H] Lo que ya verificó V05** [14][15][17]:
  - El crédito unificado es de 13,000 USD (26 USC 2102).
  - La tasa marginal llega a 40%.
  - La excepción para acciones de RIC (fondos) venció en 2011, así que las acciones de ETFs domiciliados en EUA también tienen *situs* en EUA.
  - **México no aparece en la lista de tratados sucesorios del 706-NA.**
  - La ilustración de V05: sobre 100,000 USD se pagan 10,800 USD (10.8%), y sobre 1 M USD, 33.28%.
- **[I] Custodia vía SIC/Indeval.** El *situs* lo define la ley de constitución de la emisora, "irrespective of the location of the certificates" (26 CFR 20.2104-1(a)(5)) [15]. Comprar Apple en el SIC no cambia el *situs* legal. Si en la práctica la cadena de custodia Indeval → custodio extranjero hace más o menos probable que se cobre el impuesto: **no verificado, sin fuente**.
- **[H] UCITS irlandeses** (State Street Global Advisors, 02-jun-2026) [16]:
  - Los UCITS irlandeses "incur a 15% WHT on US dividends at the fund level" por el tratado EUA-Irlanda (art. 10: 15%, [13]).
  - "Distributions from Irish-domiciled UCITS ETFs are generally not subject to withholding tax for non-resident investors."
  - **[I]** Una *plc* irlandesa es una acción de sociedad extranjera y no tiene *situs* en EUA (706-NA, V05).
- **[H] UCITS disponibles en el SIC** (V05, datos de mercado al 24-sep-2026) [17]: CSPX/N con mediana de ~47 M MXN al día, VUAA/N con ~5.3 M, CNDX/N con ~4.8 M, más VWRA/N, ISAC/N, EIMI/N e IWDA/N.
  - **[I]** En la **ruta SIC**, un UCITS de acumulación se vende con el 10% de la fr. II y no genera dividendo ni pago mensual. Es la estructura fiscalmente más limpia para ETFs de índice.
  - Con **Schwab International,** "Non-U.S. ETFs: Online Trades Not available" (por teléfono cuestan US$50) [18]. Firstrade y tastytrade solo operan mercados de EUA [23][27] **[I]**.
- **[C] Para la cuenta arena:** 20,000 MXN ≈ 1,130 USD a 17.70 [36]. El umbral de 60,000 USD equivale a **~1.06 M MXN**. **El impuesto sucesorio no es relevante para esta temporada.** Solo cuenta si la cuenta crece mucho. En ese caso la protección es usar UCITS (vía SIC o un bróker con acceso a Londres/Xetra, ver B3) o tener menos activos con *situs* en EUA.

---

## 4. Otros brókers extranjeros (además de IBKR) para residentes mexicanos

| Bróker | ¿Acepta residentes de México? | Acciones/ETFs EUA | Opciones | Mínimo | Fondeo | Salida | BMV / UCITS | Estado |
|---|---|---|---|---|---|---|---|---|
| **Firstrade** (EUA, SIPC) | **Sí.** México está en la lista oficial (actualizada 07-may-2026). Solo cuentas individuales, sin SSN/ITIN de EUA [22] | **US$0** en acciones, ETFs, opciones y fondos [23] | US$0 [23] | **Sin mínimo** [22][23] | Wire; "Firstrade does not charge any fees" por wire de entrada (pueden cobrar el banco emisor y el intermediario). ACH solo con banco de EUA [23][24] | **US$25** por wire de salida internacional [24] | Solo EUA [I] | **Verificado** (fuente oficial) |
| **Charles Schwab International** (EUA, SIPC) | **Sí.** Hay un flujo de apertura propio para México ("Residents of Mexico may submit [...] Voter ID Card [or] Consular ID Card"), captura Wayback del 17-abr-2026 [19] | **US$0** en acciones y ETFs listados, en línea [18] | US$0 + US$0.65 por contrato [18] | **(no verificado)**. Fuentes secundarias: se eliminó el mínimo de 25,000 USD en 2025 [21] | Wire USD (costo no verificado) | (no verificado) | "Non-U.S. ETFs: Not available" en línea [18] | Precios verificados (Wayback 03-jun-2026); mínimo sin verificar |
| **tastytrade** (EUA; custodia Apex) | **Probable.** México aparece en el resumen del buscador de su página de países; la página no se pudo leer (carga con JS) [29] | **US$0** + *clearing* de US$0.0008 por acción + cuotas regulatorias [27] | US$1 por contrato al abrir (máx. US$10 por pierna), US$0 al cerrar [26] | (no verificado) | Wire, cheque o *stablecoins* (USDC, USDT, PYUSD, RLUSD) [28] | **US$45** por wire de salida al extranjero; ACH gratis [27] | Solo EUA [I] | Costos verificados (hoja del 30-jul-2026); aceptación de México sin verificar directo |
| **Saxo** | **No.** México no está en la lista de países atendidos (28-jul-2026) [30] | — | — | — | — | — | — | **Descartado** |
| **eToro** (entidades en Chipre, Reino Unido, Australia, Seychelles y EAU) | Secundaria: sí, con una entidad internacional [33]. Su documento de clasificación de países pondría a México en "Tier 1" (resumen de buscador) [32] | Acciones: "A commission fee of **$1 or $2** may apply when opening and closing [...] depending on your country of residence". ETFs: sin comisión [31] | No | (no verificado) | Conversión por depósitos en moneda distinta del USD; **no publica la tasa para MXN** [31] | **US$5** por retiro desde una cuenta en USD; inactividad "Free" [31] | No BMV (secundaria) | Parcial. **[I]** No es un bróker de EUA con SIPC; entidad aplicable a México: no verificada |
| **Webull México** (Vifaru CB + Webull Financial LLC) | Sí [34] | "Cero comisiones" [34] | Sí [34] | "Sin depósito mínimo" [34] | MXN → USD a tasa "competitiva" sin cifra publicada [34] | (no verificado) | BMV no mencionada [34]; ver B2 | Parcial. Tratamiento fiscal (¿constancia mexicana para lo que opera en EUA?): **no verificado** |
| **XTB** | Secundaria: disponible en México [35] | Secundaria: 0% hasta 100,000 EUR al mes [35] | No | — | — | — | — | **(no verificado)**. Revisar si ofrece acciones reales o solo CFDs |
| **Hapi / Revolut** | Ver B2 | Ver B2 | — | — | — | — | — | B2 |
| **Interactive Brokers** | Ver B3 | Ver B3 | Ver B3 | — | — | — | Posible acceso a la BMV y a LSE (ver B3) | B3 |

**Lecturas de la tabla:**
- **[I] Ninguno de los brókers de B4 da acceso a la BMV.** Tu radar incluye Peñoles y Grupo México (solo cotizan en la BMV) y también Vesta y OMA, que sí tienen ADS en NYSE/Nasdaq. Con Firstrade, Schwab o tastytrade **pierdes Peñoles y Grupo México**.
- **[I] Firstrade es el más barato verificado de B4** para una cuenta chica: sin mínimo, sin comisión y con la salida más barata (US$25). Schwab tiene la marca más grande y opciones a US$0.65, pero su mínimo actual no está confirmado. tastytrade es el mejor en opciones (US$0 al cerrar), pero cobra US$45 por la salida y la aceptación de México no se leyó en su página oficial.
- **[I] eToro** cobra por operación en acciones (US$1 a US$2 por lado ≈ 0.09% a 0.18% sobre ~1,100 USD) y una conversión MXN no publicada, y además no es un bróker de EUA. Queda por debajo de los tres anteriores.

---

## 5. [C] Fricción de un bróker extranjero con 20,000 MXN contra GBM

**Datos:**
- **Wise MXN→USD** (cotización pública de su API, 25-sep-2026 06:15 UTC): 20,000 MXN pagados por transferencia bancaria → **1,119.05 USD**. Comisión de **193.84 MXN (0.97%)**, a una tasa media de 0.0564999 USD/MXN (**17.70 MXN/USD**) [36]. Con salida por SWIFT: 301.77 MXN (1.51%) → 1,112.95 USD [36].
- **Wise USD→MXN** (06:17 UTC): 1,100 USD → 19,249.69 MXN, con comisión de **12.57 USD (1.14%)**, a una tasa media de 17.702 [37].
- **Wire de salida:** US$25 en Firstrade [24] y US$45 en tastytrade [27].
- **GBM:** 0.29% por lado con IVA, o sea **0.58% por ida y vuelta** (B1, B2).

**Supuestos:**
- **(a)** El bróker acepta el depósito que llega desde Wise a tu nombre (**no verificado**; algunos brókers rechazan fondos de terceros).
- **(b)** Los bancos intermediarios no cobran nada (optimista).
- **(c)** La salida a pesos solo cuenta si el torneo se liquida en MXN.

| Costo sobre 20,000 MXN | Firstrade | tastytrade | GBM (referencia) |
|---|---|---|---|
| Entrada (MXN→USD, Wise) | 193.84 (0.97%) | 193.84 (0.97%) | 0 |
| Comisiones por 6 idas y vueltas | ~0 | ~0 (*clearing* ≈ US$0.02 por orden de ~20 acciones) | 696 (3.48%) (B2) |
| Salida: wire | 442.5 (2.21%) = US$25 × 17.70 | 796.5 (3.98%) = US$45 × 17.70 | 0 |
| Salida: USD→MXN (Wise, 1.14% sobre lo que queda) | ~221 (1.10%) | ~217 (1.08%) | 0 |
| **Total si se cuenta la salida** | **~857 (4.29%)** | **~1,207 (6.04%)** | 696 (3.48%) con R = 6 |
| **Total solo con la entrada** | **194 (0.97%)** | **194 (0.97%)** | 696 (3.48%) con R = 6 |

**Punto de equilibrio contra GBM** (idas y vueltas por temporada a partir de las cuales el bróker extranjero sale más barato):
- **Contando solo la entrada:** 0.97 / 0.58 ≈ **1.7**.
- **Contando la salida,** Firstrade: 4.29 / 0.58 ≈ **7.4**.
- **Contando la salida,** tastytrade: 6.04 / 0.58 ≈ **10.4**.

B1 estima además un costo cambiario implícito de ~0.1% a 0.3% por lado en el SIC. Si se suma, la ida y vuelta en GBM cuesta ~0.8% a 1.2%, y los equilibrios bajan a **~0.8 a 1.2** (solo entrada) y **~3.6 a 5.5** (Firstrade con salida).

- **[I]** Con el ritmo que presupuestó B2 (R = 6 a 9), **Firstrade empata o le gana a GBM aunque se cuente la salida**, y le gana con holgura si solo se cuenta la entrada. Pero solo cubre EUA, sin BMV.
- **[I] La exposición al peso es la misma en ambas rutas.** Una acción de EUA en el SIC cotiza en MXN igual a su precio en USD por el tipo de cambio, así que el TWR en MXN de una cuenta en USD es económicamente equivalente. Lo que cambia es el costo de convertir, no el riesgo cambiario.

---

## 6. Implicaciones para la competencia y para el neto del dueño

1. **[I] Marcador (TWR en MXN).**
   - En **ninguna** de las dos rutas el ISR sobre las ganancias sale de la cuenta durante la temporada; se paga en abril del año siguiente.
   - En la ruta extranjera, los dividendos restan menos dentro de la cuenta (10% contra 19%, §2).
   - La fricción de la ruta extranjera se concentra en el cambio de divisas y en el wire (§5).
   - **Para la comparación justa con las IAs en GBM hay que anotar dos cosas.** (a) Si la cuenta arena se mide desde el depósito en MXN, el 0.97% de la entrada cuenta como costo del bróker. (b) Si la temporada se liquida en MXN, la salida también cuenta.
2. **[I] Neto del dueño (después de impuestos).**
   - Con un bróker extranjero, **solo las acciones listadas en el SIC y los ADS de emisoras mexicanas tienen el 10% confirmado.**
   - Los **ETFs** (incluidos TQQQ, SOXL y SPXL) quedan en una zona gris.
   - Los títulos **no listados en el SIC** pasan a la tarifa progresiva de hasta 35%, con un posible pago provisional de 20% del bruto en 15 días.
   - **[R] Si la cuenta se muda a un bróker extranjero:** (a) verificar que cada ticker esté listado en el SIC antes de comprarlo (catálogo del SIC de la BMV); (b) preferir acciones individuales a ETFs, o tener los ETFs en la ruta SIC; (c) llevar una bitácora del costo promedio en MXN por emisora (el art. 129 obliga a actualizarlo por inflación).
3. **[I] Carga operativa del dueño con un bróker extranjero.**
   - Pagar el 10% de los dividendos el día 17 de cada mes en que haya dividendos.
   - Calcular la ganancia o pérdida anual de cada emisora, en MXN y actualizada, con los estados de cuenta.
   - Llenar y renovar el W-8BEN cada 3 años.
   - Declarar en la anual.
   - Con 20k y dividendos de pocos pesos, **el costo de cumplimiento (tiempo o contador) puede ser mayor que el dividendo**. Por eso conviene favorecer emisoras sin dividendo o con dividendo bajo.
4. **[R] Contribución de B4 a la decisión "escoge otra, lo importante es ganar más dinero":**
   - **Si la decisión final es un bróker extranjero,** B4 no descalifica a ninguno por motivos fiscales, siempre que se operen **acciones listadas en el SIC**.
   - Entre los extranjeros de B4, **Firstrade** es la opción verificada más barata.
   - **Si la estrategia necesita ETFs apalancados o emisoras de la BMV,** B4 empuja hacia una casa de bolsa mexicana (B2: Kuspit o Actinver Trade) o hacia IBKR (B3), si IBKR da acceso a la BMV y los ETFs se tienen vía SIC.
   - En cualquier caso, **antes de operar** hay que recalcular las réplicas con los costos del bróker elegido, como pediste.

---

## 7. Correcciones y actualizaciones a documentos previos

| Documento | Afirmación previa | Corrección con fuente |
|---|---|---|
| B1 §5 [I] y resumen, punto 8 | "Una venta en NYSE o Nasdaq [...] no entra en las fracciones I ni II" / "no parece caber en el art. 129" | **Incorrecto para acciones listadas en el SIC:** el criterio 37/ISR/N (Anexo 7 RMF 2026) aplica el 10% "con independencia de que su enajenación no se realice a través de un intermediario del mercado de valores mexicano" [4]. Sigue abierto para ETFs (§1.3) y para títulos no listados (§1.4) |
| B1 tabla de impuestos y `01-gbm` §"Ganancia en Trading USA" | "Tasa no verificada" | **[I]** Para acciones de Trading USA (DriveWealth) que estén listadas en el SIC aplica el 10% por el criterio 37 [4]. El criterio no menciona a GBM ni a DriveWealth: la aplicación es mía |
| B2 §1 | "la venta directa en NYSE/Nasdaq probablemente no entra ahí (inferencia)" | Mismo ajuste que B1 |
| B2, lista de no verificados | "Reformas al art. 129 posteriores al 01-04-2024" | **Resuelto:** no hay reformas a la LISR después del DOF 01-04-2024 [2] |
| V05, puntos 5 y 6 del pre-registro | Umbral de 60,000 USD, *situs* y 15% de los UCITS (fuentes legales congeladas) | **Confirmado con fuentes de 2026:** página del IRS revisada el 27-jun-2026 [8] y SSGA del 02-jun-2026 [16] |
| B1 §5 (W-8BEN no se paga solo) | Con 20k el W-8BEN del SIC no se recupera | **Nuevo matiz:** sin W-8BEN, el 20% de exceso sobre el tratado **tampoco se acredita en México** (art. 5 y criterio 5/ISR/N [1][4]). La pérdida es definitiva, no diferida. La conclusión de B1 se mantiene para 20k porque el monto es muy chico |

---

## 8. Lo que no se pudo verificar

1. **ETFs vendidos con un bróker extranjero:** si el SAT los trata con el 10% del art. 129 (fr. I como "acciones de sociedades extranjeras" o fr. II) o fuera de él. Solo hay opinión profesional (IMCP [7]) y divulgación [39]. No hay criterio ni regla del SAT.
2. **Estructura legal de TQQQ, SOXL, SPXL, QQQ y SPY** (*trust* contra *corporation*) y si para el SAT son "títulos que representan índices accionarios" siendo apalancados con *swaps*.
3. **Pago provisional de 20% del art. 126** en ventas de títulos no listados en el SIC hechas con un bróker extranjero: si aplica en la práctica y si hay alguna facilidad.
4. **Si el 10% de EUA se puede acreditar contra el 10% adicional mexicano** del art. 142 fr. V (que es "definitivo"), o solo contra el ISR del dividendo acumulado.
5. **Tipo de cambio para calcular el costo en MXN** de compras y ventas en USD con un bróker extranjero (probablemente el del DOF del día anterior, art. 20 CFF; no verificado) y el trato de la ganancia cambiaria sobre el efectivo en USD que queda en el bróker (art. 142 fr. II).
6. **Schwab International:** mínimo de apertura actual, costo del wire y si da W-8BEN y fracciones. El sitio devuelve 403 y las capturas de Wayback se cortaron.
7. **tastytrade:** que México esté en la lista oficial de países (la página carga con JS; solo lo vi en el resumen del buscador) y el mínimo de apertura.
8. **eToro:** la entidad que atiende a México, la tasa de conversión para depósitos en MXN y si custodia acciones reales o CFDs para México.
9. **XTB:** si acepta a México, en qué entidad y si ofrece acciones reales.
10. **Webull México:** su margen cambiario MXN→USD y si emite algún documento fiscal mexicano por lo operado en EUA con Webull Financial LLC.
11. **Fondeo con Wise:** si Firstrade, Schwab o tastytrade aceptan el depósito que llega desde Wise, y si un residente mexicano puede recibir en Wise los USD del wire de salida. La cotización mostró "multi currency account is currently not available in your country" para la opción de pagar desde saldo; el país lo infiere Wise y puede reflejar la IP del *proxy*.
12. **Reciprocidad FATCA:** si los brókers de EUA reportan al SAT las cuentas de residentes mexicanos, y con qué alcance (solo fuente secundaria [38]).
13. **Custodia SIC/Indeval y el impuesto sucesorio:** efecto práctico (no el legal) sobre el cobro.
14. **Página del IRS sobre el *tax home* y la regla de los 183 días:** lo leí en el resumen del buscador de irs.gov y en la tabla de fuente del ingreso [9][10]. No leí completa la Pub. 519.

---

## 9. Fuentes (consultadas el 2026-09-25 salvo otra indicación)

1. Cámara de Diputados, *Ley del Impuesto sobre la Renta*, texto vigente, última reforma DOF 01-04-2024: arts. 5, 119-126, 129, 142 fr. V y 176. https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf. Copia congelada y extraída en `laboratorio/replicas/V05-spiva-y-fiscalidad-sic/datos/legal/LISR.txt` (descargada el 25-sep-2026 por V05).
2. Cámara de Diputados, historial de reformas de la LISR (la última es el DOF 01-04-2024). https://www.diputados.gob.mx/LeyesBiblio/ref/lisr.htm. Complemento: Holland & Knight, "Aspectos fiscales del Paquete Económico 2026 en México" (sep-2025), https://www.hklaw.com/en/insights/publications/2025/09/aspectos-fiscales-del-paquete-economico-2026-en-mexico (resumen de buscador: "no hay cambios específicos a las leyes del ISR y del IVA").
3. SAT/DOF, *Resolución Miscelánea Fiscal para 2026*, DOF 28-12-2025: reglas 3.1.7, 3.2.12, 3.5.20, 3.5.22, 3.11.7, 3.11.9 y 3.15.10. https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rmf/rmf/RMF_2026-DOF-28122025.pdf. Nota del DOF: https://dof.gob.mx/nota_detalle.php?codigo=5777217&fecha=28%2F12%2F2025
4. SAT/DOF, *Anexo 7 de la RMF 2026, Compilación de criterios normativos*, DOF 09-01-2026: criterios **37/ISR/N** (págs. 45-46) y **5/ISR/N**. https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rmf/anexos/Anexo_7_RMF2026-09012026.pdf
5. Cámara de Diputados, *Código Fiscal de la Federación*, última reforma DOF 09-04-2026, art. 16-C. https://www.diputados.gob.mx/LeyesBiblio/pdf/CFF.pdf
6. (Referencia interna) GBM, FAQ de impuestos en el SIC y dividendos, citadas en B1 [14][15][16].
7. IMCP, Comisión Fiscal, *Fisco Actualidades* 122, "Aspectos fiscales de la inversión en Exchange Traded Funds" (abr-2024), C.P.C. Allen Saracho Carrillo. https://imcp.org.mx/wp-content/uploads/2024/04/Fisco_122_24.pdf. El original dio 403; se leyó la captura de Wayback: https://web.archive.org/web/2025id_/https://imcp.org.mx/wp-content/uploads/2024/04/Fisco_122_24.pdf. **Fuente secundaria profesional, no del SAT.**
8. IRS, "Some nonresidents with U.S. assets must file estate tax returns" (revisada el 27-jun-2026). https://www.irs.gov/individuals/international-taxpayers/some-nonresidents-with-us-assets-must-file-estate-tax-returns
9. IRS, "Nonresident aliens – source of income" (revisada el 18-ago-2026): la venta de bienes muebles tiene su fuente en el "seller's tax home". https://www.irs.gov/individuals/international-taxpayers/nonresident-aliens-source-of-income
10. IRS, "The taxation of capital gains of nonresident students, scholars and employees of foreign governments" y Pub. 519. https://www.irs.gov/individuals/international-taxpayers/the-taxation-of-capital-gains-of-nonresident-students-scholars-and-employees-of-foreign-governments ; https://www.irs.gov/publications/p519. **Solo resumen del buscador.**
11. IRS, *Instructions for Form W-8BEN* (Rev. oct-2021), vigencia del formulario. https://www.irs.gov/instructions/iw8ben. **Resumen del buscador de la página oficial.**
12. IRS, Convenio EUA-México para evitar la doble tributación, art. 10 (10% "in other cases"). https://www.irs.gov/pub/irs-trty/mexico.pdf (congelado en V05, `datos/legal/irs-tratado-eua-mexico.txt`).
13. IRS, Convenio EUA-Irlanda, art. 10 (15%). https://www.irs.gov/pub/irs-trty/ireland.pdf (congelado en V05).
14. IRS, *Instructions for Form 706-NA* (rev. 09/2025): umbral de 60,000 USD, crédito de 13,000 USD, *situs* de acciones, excepción RIC 2005-2011 y lista de tratados. https://www.irs.gov/instructions/i706na (congelado en V05).
15. eCFR, 26 CFR 20.2104-1(a)(5). https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-26?part=20&section=20.2104-1 (congelado en V05).
16. State Street Global Advisors, "Considerations for non-US investors: US-domiciled ETFs vs. Irish-domiciled UCITS ETFs" (02-jun-2026). https://www.ssga.com/us/en/institutional/insights/considerations-for-non-us-investors-us-etfs-vs-irish-ucits
17. `laboratorio/replicas/V05-spiva-y-fiscalidad-sic/resultados.json`: `sic_ucits`, `sic_eua`, `fuga_por_dividendos`, `citas_legales` e `impuesto_sucesorio_ilustracion` (25-sep-2026).
18. Charles Schwab International, "Fees & Commissions" (captura de Wayback del 03-jun-2026). https://international.schwab.com/pricing → https://web.archive.org/web/20260603144902id_/https://international.schwab.com/pricing (el sitio en vivo da 403).
19. Charles Schwab International, "Open an account – Step 2 (MEX)" (captura de Wayback del 17-abr-2026). https://web.archive.org/web/20260417022334id_/https://international.schwab.com/open-account-step-2MEX
20. Charles Schwab International, página de países restringidos (captura del 21-ene-2026; texto genérico de rechazo, sin lista). https://web.archive.org/web/20260121154410id_/https://international.schwab.com/open-account-intro/restrict
21. The Poor Swiss, "Charles Schwab International Review 2026", y EarlyRetireAbroad (mínimo de 25,000 USD eliminado en 2025). https://thepoorswiss.com/charles-schwab-international-review/ ; https://earlyretireabroad.com/charles-schwab-international-account/. **Secundarias.**
22. Firstrade Help Center, "Can I open an international account?" (actualizada el 07-may-2026). https://help.firstrade.info/en/articles/9268315-can-i-open-an-international-account
23. Firstrade, "International Stock Investing Accounts". https://www.firstrade.com/accounts/international
24. Firstrade Help Center, "What are the fees for wire transfers?" (actualizada el 15-jul-2024). https://help.firstrade.info/en/articles/9260062-what-are-the-fees-for-wire-transfers
25. Firstrade, "Get a Wire Transfer Fee Rebate" (reembolso por wires de ≥10,000 USD desde 01/05/2026; solo resumen del buscador). https://www.firstrade.com/accounts/wire-fee-rebate
26. tastytrade, "Pricing". https://tastytrade.com/pricing/
27. tastytrade, "Commissions & Fees" (PDF, "Last updated July 30, 2026"). https://tastytrade.com/commissions-and-fees/ → https://assets.contentstack.io/v3/assets/blt7dc2e3d4a7071563/blt2b752fef372188fe/commissions-and-fees
28. tastytrade, "International Accounts" (actualizada el 19-mar-2026). https://tastytrade.com/learn/accounts/account-types/international-account/
29. tastytrade Support, "Supported Countries for International Accounts". https://support.tastytrade.com/support/s/solutions/articles/43000435355 (no legible; la lista con México sale del resumen del buscador) y Brokerage-Review (secundaria): https://www.brokerage-review.com/investing-firm/foreigner/tastyworks-for-non-us-citizens.aspx
30. Saxo Help Center, "Which countries are serviced by Saxo?" (actualizada el 28-jul-2026). https://www.help.saxo/hc/en-us/articles/10611416570269-Which-countries-are-serviced-by-Saxo
31. eToro, "Fees". https://www.etoro.com/trading/fees/
32. eToro, "Countries classification" (PDF, abr-2024; solo resumen del buscador). https://www.etoro.com/wp-content/uploads/2024/04/countries-classification.pdf
33. Finantres, "eToro opiniones en México 2026" y Rankia, "Review eToro". https://finantres.mx/etoro-opiniones/ ; https://www.rankia.mx/blog/forex-mexico/6383498-review-etoro. **Secundarias.**
34. Webull México, página principal. https://www.webull.com.mx/
35. BrokerChooser, "¿Está disponible XTB para inversores en México?". https://brokerchooser.com/es/broker-reviews/xtb-review/xtb-mexico. **Secundaria (resumen del buscador).**
36. Wise, cotización pública MXN→USD por 20,000 MXN (API `POST https://api.wise.com/v3/quotes/`, rateTimestamp 2026-09-25T06:15:31Z; y `https://wise.com/gateway/v1/price?sourceAmount=20000&sourceCurrency=MXN&targetCurrency=USD`). Cotización anónima: el precio real para un residente mexicano puede variar.
37. Wise, cotización pública USD→MXN por 1,100 USD (API `POST https://api.wise.com/v3/quotes/`, rateTimestamp 2026-09-25T06:16:32Z).
38. Clearstream, "U.S.A.: FATCA: U.S.A. and Mexico sign new Model I Intergovernmental Agreement" (IGA del 09-abr-2014). https://www.luxcsd.com/luxcsd-en/products-and-services/assetservices/U.S.A.-FATCA-U.S.A.-and-Mexico-sign-new-Model-I-Intergovernmental-Agreement-1305594. **Secundaria. La reciprocidad es inferencia.**
39. El Fondo, "Impuestos por acciones y ETFs de EE. UU. desde México: SAT, W-8BEN y el 30% (2026)". https://www.el-fondo.com/es/articles/impuestos-acciones-etfs-eeuu-desde-mexico-sat-w8ben. **Secundaria (resumen del buscador).** Extiende el criterio 37 a los ETFs; el texto del criterio no lo dice.
40. Documentos internos: `B1-gbm-linea-base-.md`, `B2-casas-de-bolsa-y-apps-mexicanas.md` y `../01-gbm-operativa-y-costos.md` (25-sep-2026).

**Búsquedas web realizadas:** 20 (art. 129 con bróker extranjero, RMF 2026, criterio 37/ISR/N, ETFs con bróker extranjero, reformas a la LISR 2026, Pub. 519 del IRS, retenciones de UCITS irlandeses, Schwab International, Firstrade (2), tastytrade (3), Saxo, eToro (2), Webull México, W-8BEN, XTB/Trading 212/moomoo, FATCA México). Además se consultaron páginas oficiales directamente: SAT (RMF y Anexo 7), Cámara de Diputados (LISR, CFF e historial), IRS (3), SSGA, Schwab (Wayback), Firstrade (3), tastytrade (3), Saxo, eToro, Webull México y la API pública de Wise (2).
