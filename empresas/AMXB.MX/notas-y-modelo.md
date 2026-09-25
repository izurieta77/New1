# América Móvil (AMXB.MX): notas del 20-F 2025 y del 2T26, modelo integrado, DCF inverso y sensibilidad geopolítica

> Corte: 25-sep-2026. **FASE 0 (formación): no es recomendación de compra o venta.** Los escenarios son supuestos de mecanismo, no pronósticos, guía ni consenso.
> Convención: **hecho** = cifra del documento con página; **Inferencia:** = interpretación propia; **supuesto** = entrada elegida por el analista. Montos en millones de MXN salvo que se indique otra cosa (el 20-F reporta en miles; aquí se dividen entre 1,000 sin redondear). IFRS; ejercicio = año calendario.
> Archivos: `empresas/AMXB.MX/modelo/base.json` (mapeo y supuestos), `modelo.py` (corrida), `resultados.json` (salida completa), `SHA256SUMS.txt` (huellas), `datos/` (transcripción en miles, segunda extracción e insumos congelados). No se editó `ficha.md`.

## 0. Resumen

- **Base histórica FY2023-FY2025** transcrita del 20-F 2025 (y del 20-F 2024 para el balance de 2023): 463 cifras con página. Doble comprobación: 140/140 identidades, 463/463 cifras encontradas en el texto de su página, 422/463 confirmadas además contra una fuente independiente (XBRL de la SEC o visor XBRL del 20-F) y 0 diferencias (§3).
- **Motor:** 539 registros de control: 523 OK, **0 FALLA**, 14 INFO y 2 NO_APLICA. El motor reproduce FY2024 y FY2025 (C13) con diferencia máxima de 0.0000, y cada partida no explicada aparece con nombre y monto (§4).
- **Hallazgos de notas (hechos):**
  - 73.9% de la deuda no está en pesos.
  - 59.9% del pasivo por arrendamientos es con partes relacionadas.
  - Hay **debilidades materiales** de control interno en 2023, 2024 y 2025, con opinión **adversa** del auditor sobre el control interno de 2025.
  - La utilidad de 2024 bajó 5,406 entre el comunicado del 4T24 y el 20-F.
  - El plan de pensiones de México tiene un déficit de 183,298 y está cubierto 46.7% por activos.
  - Brasil tiene contingencias fiscales de 130,739, de las cuales está provisionado 19.4% (§2).
- **DCF inverso** (§6; FCFF = flujo libre para la empresa, antes de pagos a acreedores y accionistas). Con precio de 19.60 MXN (24-sep-2026), WACC de 11.02%, g terminal de 3.5% y el margen FCFF de 2025 (7.87%), el precio exige que los ingresos crezcan **9.9% anual durante 10 años**. En la rejilla (WACC ±1 pp, g ±0.5 pp y tres márgenes históricos), el crecimiento exigido va de 4.4% a 16.2%.
  - *Inferencia:* el precio no descuenta estancamiento. Exige crecimiento nominal alto o una mejora duradera de la conversión a caja: con el margen FCFF promedio del escenario intermedio (12.6%) bastaría un crecimiento de 3.3%.
- **Sensibilidad geopolítica y regulatoria** (§7):
  - Una depreciación de 10% del peso contra el USD resta entre 4,905 y 11,007 a la utilidad neta (5.5%-12.3% de la de 12 meses), según la cobertura.
  - La suspensión de líneas por el registro obligatorio resta entre 0.2% y 5.7% del EBITDA de 12 meses en la rejilla de parámetros.

## 1. Fuentes leídas y congeladas

| Id | Documento | Fecha | Alcance leído |
|---|---|---|---|
| F1 | 20-F 2025, PDF "as filed" del emisor ([q4cdn](https://s22.q4cdn.com/604986553/files/doc_financials/2025/ar/AS-FILED-AMERICA-MOVIL-SAB-DE-CV-20F-2025.pdf)). Es el mismo documento que `ef20060642_20f.htm`, accession 0001140361-26-017486 ([SEC](https://www.sec.gov/Archives/edgar/data/1129137/000114036126017486/ef20060642_20f.htm)) | 28-abr-2026 | Datos seleccionados p. 4. MD&A pp. 16-19. Factores de riesgo pp. 31, 37 y 42. Controles pp. 61-62. Regulación en México pp. 65-72. Auditor y estados F-1 a F-8. Notas 1, 2 (riesgo de mercado F-30/31), 6, 7, 10, 13 (conciliación de tasa), 14, 15, 16, 17, 18, 19, 20, 22, 23 y 25 |
| F2 | 20-F 2024, PDF del emisor ([sitio del emisor](https://sustainability-americamovil-com.amxdigital.net/portal/su/pdf/Annual-Report-20F-2024.pdf)), accession 0001140361-25-018954 | 14-may-2025 | Balance al 31-dic-2023 (p. F-6) y cambios en pasivos de financiamiento 2022-2023 (p. F-82) |
| F3 | Reporte 2T26 ([2Q26.pdf](https://s22.q4cdn.com/604986553/files/doc_financials/2026/q2/2Q26.pdf)), sin auditar | 21-jul-2026 | pp. 2-12 y 29-32 |
| F4 | Reporte 4T25 ([4Q25.pdf](https://s22.q4cdn.com/604986553/files/doc_financials/2025/q4/4Q25.pdf)), sin auditar | 10-feb-2026 | pp. 3, 8-10, 12 y 31-33 |
| F5 | Reporte 4T24 original ([4Q24.pdf](https://s22.q4cdn.com/604986553/files/doc_financials/2024/q4/4Q24.pdf)), sin auditar | feb-2025 | pp. 8 y 31 |
| F6 | Visor XBRL de la SEC del 20-F 2025: R2, R3, R4, R5, R83, R109 y R136 (leídos con WebFetch) | 28-abr-2026 | Segunda extracción |
| F7 | SEC `companyfacts` y `submissions`, CIK 1129137 (data.sec.gov) | 25-sep-2026 | Hechos XBRL del 20-F 2024; historial de presentaciones |
| F8 | Yahoo Finance chart v8: AMXB.MX y MXN=X | 24/25-sep-2026 | Precio y tipo de cambio |
| F9 | FRED: DGS10, T5YIE, IRLTLT01MXM156N | sep-2026 | Tasas |
| F10 | Damodaran, *Country Risk Premiums*, 1-jul-2026 (corregido el 9-jul) | jul-2026 | Prima madura, diferenciales y CRP |
| F11 | Damodaran, *Betas by Sector*, emergentes y global (5-ene-2026) | ene-2026 | Renglón Telecom. Services |
| F12 | `conocimiento/03` §2.3 y §6.1; `conocimiento/23` y `24` §4.9-4.11; `conocimiento/25` | 25-sep-2026 | Método y contexto |

**Acceso a la SEC.** `www.sec.gov/Archives` respondió 403 al User-Agent declarado ("SistemaInversionNew1/1.0 investigacion"). No se inventó un correo. En su lugar:
- se usó el PDF "as filed" que publica el emisor, que es el mismo documento;
- se leyeron las tablas del visor XBRL de la SEC con WebFetch;
- se consultó `data.sec.gov`, que sí acepta el User-Agent (en esa API todavía no aparece el 20-F 2025).

**Congelamiento.** En `base.json`, bajo `fuentes.F1-F5`, está el sha256 de cada PDF:

```
d340b7db3eeada61ad651b4d328cafd138aa58fe650f3d995ec4c429446a835a  20-F 2025 (F1, 1,724,696 bytes)
7b50911068a8e33faeef7d01b30f2339e8e61cd7bab97828e2826f612a1c7289  20-F 2024 (F2, 4,882,413 bytes)
8f13d33da7778c26e8240b3eeaa7d7341971305064f57ba3f7c585ca5482dd92  2Q26.pdf   (F3, 6,243,701 bytes)
4c68d83c8262530dd939c98cf7f0275b059b882c1064cc585e87bf2b8fd0d00c  4Q25.pdf   (F4, 967,242 bytes)
a14487a6094bd468e9ca0698398ae41d7bea334b307ff3a0f065486572096fc5  4Q24.pdf   (F5, 1,057,814 bytes)
```

Los insumos derivados se congelaron con `herramientas/huellas.py` en `modelo/datos/SHA256SUMS.txt` (11 archivos: transcripción, extractos de texto de las páginas citadas, segunda extracción, XBRL, submissions, Yahoo, FRED y Damodaran). `huellas.py verificar` da OK, y `modelo.py` se niega a pasar si alguna huella cambia. Yahoo y FRED son fuentes vivas: una nueva descarga no reproduce el hash.

## 2. Hallazgos de las notas

### 2.1 Deuda por moneda y vencimiento (F1 Nota 14, pp. F-58 a F-61; F3 p. 32)

**Hechos:**
- **Deuda al 31-dic-2025: 524,907.** Se compone de bonos por 465,049 y líneas de crédito y otros por 59,858 (F-59). Por moneda, sumando bonos y líneas de crédito (F-59):

  | Moneda | Monto | % |
  |---|---:|---:|
  | USD | 168,694 | 32.1% |
  | MXN | 136,982 | 26.1% |
  | EUR | 81,951 | 15.6% |
  | GBP | 53,183 | 10.1% |
  | BRL | 27,755 | 5.3% |
  | PEN | 24,590 | 4.7% |
  | CLP | 15,676 | 3.0% |
  | COP | 14,585 | 2.8% |
  | JPY | 1,490 | 0.3% |

  El total no denominado en pesos es **73.9%** (cálculo propio, sin derivados).
- **Costo.** El costo promedio ponderado fue de 6.29% en 2025 y 6.14% en 2024, sin comisiones ni la retención de ~4.9% que se reembolsa a acreedores extranjeros (F-60). Incluyendo derivados, la tasa ponderada fue de 5.7% (F-38).
- **Corto plazo:** 91,973, el 17.5% del total, con tasa ponderada de 5.09% (F-60).
- **Vencimientos de largo plazo:** 2027: 42,013; 2028: 42,837; 2029: 54,254; 2030: 47,390; 2031: 22,000; 2032 en adelante: 224,439, el 51.8% de la deuda de largo plazo (F-60).
- **Covenants:** deuda/EBITDA ≤ 4.0x y EBITDA/intereses pagados ≥ 2.5x; se cumplían al cierre (F-61). Hay cláusulas de cambio de control y tres revolventes sin disponer: el equivalente en euros de US$1,500 M (2030), US$2,500 M (2029) y €1,000 M de Telekom Austria (2030) (F-61).
- **Reapertura en pesos.** El 25-nov-2025 se reabrieron bonos globales en pesos por 10 mil M: 6.5 mil M del AMX34 al 9.3% y el resto del AMX29 al 8.5% (F4 p. 3; F-60).
- **Jun-26 (F3 p. 32):**
  - deuda de 476,927, que se reparte en MXN 128,181, US$9,001 M, €3,432 M, £2,200 M, R$10,000 M y otras monedas por Ps 38,290;
  - efectivo y valores de 75,943 y deuda neta de 400,984;
  - 1.31x deuda neta/EBITDAaL (F3 p. 7).

*Inferencia (cálculo propio):*
- El gasto por intereses de 2025 sin los de arrendamientos fue de 44,162 (60,319 − 16,157). Eso da **8.08%** sobre la deuda promedio (546,246), contra el 6.29% declarado. La brecha es compatible con la retención, las comisiones y la deuda en BRL a CDI, pero el filing no la desglosa (pendiente §9).
- **Refinanciamiento.** En 2026 vence 17.5% de la deuda, y entre 2027 y 2030 alrededor de 10% por año. Con acceso al mercado, el perfil es manejable. El escenario de tensión (§5) mide qué pasa si solo se refinancia la mitad.

### 2.2 Cobertura cambiaria y sensibilidad del emisor (F1 Nota 7 pp. F-38/39; Nota 2 pp. F-30/31)

**Hechos:**
- **Derivados activos:** 2,417. Incluyen XCS (swaps de moneda) USD-MXN por US$1,700 M (valor razonable de 1,891), XCS MXN-USD por MXN 2,018 M (250), forwards BRL-USD por R$5,843 M (160) y EUR-USD por €681 M (116).
- **Derivados pasivos:** −16,132. Incluyen:
  - XCS USD-MXN por US$3,190 M (−4,315);
  - XCS GBP-USD por £1,560 M (−7,544);
  - XCS GBP-EUR por £640 M (−1,685);
  - XCS USD-EUR por US$950 M (−1,038);
  - XCS EUR-USD por €802 M (−859);
  - XCS JPY-USD por ¥13,000 M (−617);
  - forward USD-MXN por US$100 M (−13).
- **Valuación de derivados:** pérdida de −697 en 2025, −2,142 en 2024 y −10,269 en 2023 (F-39).
- **Operaciones en el extranjero:** "The Company does not use derivatives to hedge the exchange risk arising from having operations in different countries" (F-30).
- **Sensibilidad publicada por el emisor:**
  - si todos los tipos de cambio suben 5%, la deuda pasa de 524,907 a 551,152 (+26,245) (F-31);
  - si las tasas suben 100 pb, junto con una fluctuación del USD/MXN de 8.4%, los intereses netos suben 5,002 (F-31).
- **Resultado cambiario:** −70,698 en 2024, cuando el USD/MXN pasó de 16.8935 a 20.2683 (+20.0%), y +19,787 en 2025, cuando bajó a 17.9667 (−11.4%) (F1 p. F-6; F5 p. 31; F4 p. 31).

*Inferencia:*
- **Cobertura del USD.** Los instrumentos USD→MXN (US$1,700 + US$3,190 + forward de US$100 = **US$4,990 M**) cubren ~53% de la deuda en USD de dic-25 (US$9,389 M, F4 p. 33). Sobre la de jun-26 (US$9,001 M) cubrirían ~55%, si siguen vigentes (supuesto, §7).
- **Libra.** Los £2,200 M se convierten con swaps a USD (£1,560 M) y a EUR (£640 M), no a pesos. La exposición cambia de moneda, pero no desaparece.
- **Sensibilidad del emisor.** Aplica el 5% también a los 136,982 de deuda en pesos y no neta los derivados. El equivalente sobre la deuda en USD sin coberturas es 7,862 (§7).
- **Elasticidad observada.** Por cada +1% del USD/MXN, el resultado cambiario fue −3,539 en 2024 y −1,742 en 2025. La diferencia indica que otras monedas y la posición cubierta pesan tanto como el USD/MXN. No es una beta estable.

### 2.3 Arrendamientos IFRS 16 y torres de partes relacionadas (F1 Nota 15 p. F-62, con tablas en PDF 157)

**Hechos:**
- **Saldos.** Los activos por derecho de uso suman 197,544: torres y sitios 177,296, inmuebles 12,849 y otro equipo 7,399. El pasivo es de 214,109: 35,867 de corto plazo y 178,242 de largo plazo.
- **Movimiento de 2025 en el pasivo:** altas y bajas 14,848, modificaciones 28,874, combinación de negocios 37, intereses 16,157, pagos −51,586 y conversión −7,324. La depreciación del derecho de uso fue de 39,226.
- **Partes relacionadas:** 119,147 del activo (60.3%) y **128,238 del pasivo (59.9%)**. En 2025, la depreciación con partes relacionadas fue de 20,110 y los intereses de 9,681: **29,792 en total, 3.2% de los ingresos** (cálculo propio).
- **Vencimientos del pasivo de largo plazo:** 2027: 31,184; 2028: 31,121; 2029: 27,018; 2030: 23,772; 2031: 23,752; 2032 en adelante: 41,395.
- **2024.** Hubo altas por 74,430, modificaciones por 31,997 y combinación de negocios por 5,286, y el pasivo pasó de 125,169 a 213,103 (+70%).
- **Clasificación en el flujo.** Todo el pago del pasivo (51,586) va en financiamiento, igual que los intereses de deuda pagados (32,325) (F-8).
- **Nota 6.** La tabla de transacciones con partes relacionadas solo muestra 605 de "Rent of towers" en 2025 (F-37).

*Inferencia:*
- **El CFO IFRS (272,399) no descuenta ni intereses ni arrendamientos.** El modelo los reclasifica a operación (CFO del motor: 223,917) para que el FCF histórico sea comparable con el proyectado (§3).
- **El pasivo equivale a ~4.2 años de pagos** (214,109 / 51,586). Como los contratos de torres se renuevan, la mayor parte del costo futuro no está en el balance.
- **En el DCF, esta es la trampa más grande del caso.** Tratar los arrendamientos como deuda sin restar los arrendamientos nuevos (43,721 en 2025) sube el margen FCFF de 8.2% a 12.8% y baja el crecimiento implícito de 9.6% a 3.6% (§6).
- **Contraparte.** Que las torres arrendadas a partes relacionadas pertenezcan a Sitios Latinoamérica o Telesites es plausible, porque ambas aparecen en la Nota 6. Pero la Nota 15 no nombra a la contraparte.
- **Salto de 2024.** Es consistente con la consolidación de Claro Chile y con renovaciones grandes, pero el filing no da el detalle.

### 2.4 Capex (F1 p. F-8; Nota 10 p. F-43; Nota 17 p. F-63; F3 p. 10; F4 p. 10)

**Hechos:**
- **Capex en caja de 2025:** 130,817 (compras de PPE 114,431 más intangibles 16,386), el 13.9% de los ingresos. El emisor reporta la misma cifra (F4 p. 10). En 2024 fue de 130,835 (15.1%) y en 2023 de 156,339 (19.2%).
- **Diferencias entre devengado y caja:**
  - las adiciones de PPE devengadas fueron de 128,740;
  - las compras de PPE en cuentas por pagar (no monetarias) fueron 15,226 en 2025, contra 11,701 en 2024 y 6,929 en 2023 (F-43);
  - los intereses capitalizados fueron de 1,570, a una tasa de 6.2% (F-43).
- **Compromisos de capex no reconocidos:** 68,814 (F-63).
- **Primer semestre:** capex de 48,112 en 1S26 (10.1% de los ingresos), contra 54,919 en 1S25 (11.8%) (F3 p. 10 y p. 8).

*Inferencia:*
- La baja del capex de 19.2% a 13.9% de los ingresos explica casi toda la mejora del FCF entre 2023 y 2025 (FCF del motor: de 52,073 a 93,100).
- Las compras de PPE por pagar subieron 3.5 mil M: parte del menor capex en caja es de calendario.
- La licitación de espectro 5G (CRT, 2S26, según la `ficha.md`; no verificada aquí) iría a intangibles, es decir, a capex. El escenario de tensión la modela como un salto a 16.5% en 2027.

### 2.5 Recompras y dividendos (F1 pp. F-7, F-9, F-74/75 y F-82; F3 pp. 3 y 10)

**Hechos:**
- **Recompras de 2025:** 736.5 M de acciones por 11,944, a ≈ Ps 16.22 por acción (cálculo propio).
  - Al cierre había 981.5 M en tesorería.
  - Las acciones en circulación bajaron de 61,000 M a 60,263.5 M (−1.2%) (F-74/75).
- **Dividendo de 2025:** Ps 0.52 en dos pagos de 0.26, el 14-jul y el 10-nov-2025 (F-75). Los dividendos pagados sumaron 33,160, incluidos los de minoritarios (F-8).
- **Asamblea del 23-abr-2026 (F-82):**
  - dividendo de Ps 0.54, en dos pagos de 0.27;
  - fondo de recompra de Ps 10 mil M;
  - cancelación de las acciones en tesorería.
- **1S26:** recompras de 4,568 (F3 p. 10) y 60.1 mil M de acciones al cierre de junio (F3 p. 3).
- **Dilución:** la UPA básica es igual a la diluida (F-75) y no hay planes de pago en acciones: la búsqueda de "share-based" en el 20-F no arroja resultados.

*Inferencia:* las distribuciones de 2025 sumaron 45,104 (dividendos pagados más recompras). Eso es el 78% del FCF después de arrendamientos (57,670) y el 55% del FCF que define el emisor (81,884).

### 2.6 Operaciones en países con riesgo regulatorio o político

**México** (37.4% de los ingresos externos de 2025: Telcel 27.6% y Telmex 9.7%; F-80).
- **Regulación asimétrica.** AMX, sus filiales mexicanas, Grupo Carso y Grupo Financiero Inbursa forman el "agente económico preponderante" desde 2014 y están sujetos a regulación asimétrica (p. 65).
- **Nuevos reguladores.** La reforma constitucional de 2024 disolvió el IFT (oct-2025) y creó la CRT y la CNA, "*expected to be more aligned with the federal government's agenda and to have broader authority to impose additional regulations and greater sanctions*" (p. 65). La CNA puede imponer o modificar la regulación asimétrica (p. 65).
- **Bucle local.** En dic-2025, la CRT levantó la regulación de precios de la desagregación indirecta del bucle local en 107 municipios (p. 67).
- **Registro de líneas:**
  - cada línea debe vincularse a una CURP o un RFC; las no vinculadas al 30-jun-2026 se suspenden (p. 70);
  - una persona física puede tener hasta 10 líneas (p. 71);
  - según el 2T26, la CRT extendió el plazo: va del 15-ago al 31-dic-2026 según el último dígito, y el prepago que no se registre se suspende (F3 p. 11).
- **Multas y litigios:**
  - el IFT multó a Telcel con 1,782.6 M por la distribución de SIM en tiendas de conveniencia (jun-2025); Telcel promovió un amparo y garantizó la multa (F-64);
  - las tarifas de interconexión de 2018-2026 están impugnadas (F-64);
  - hay una acción colectiva sin provisión (F-64);
  - Telmex registró una multa regulatoria en el 2T26. Sin ella, el EBITDA de México habría subido 4.3% (F3 p. 11).

**Argentina** (3.9%). Es economía hiperinflacionaria (IAS 29).
- La ganancia por posición monetaria fue de 5,420 en 2025, 27,387 en 2024 y 9,321 en 2023 (F-8).
- El segmento tuvo utilidad de operación de 1,037 y pérdida atribuible de −3,983 en 2025 (F-80).

**Brasil** (18.8%).
- Contingencias fiscales de 130,739 (R$40,040 M), con provisión de 25,361, es decir, 19.4% (F-64).
- TFI por 23,538 sin provisión (F-65).
- Anatel calcula una corrección monetaria de 16,236; la provisión es de 6,232 (F-65).

**Europa.** El conflicto Rusia-Ucrania puede traer sanciones que afecten "*our operations in Belarus*". El conflicto en Medio Oriente también se cita como fuente de incertidumbre (p. 42). AMX tiene 61% de A1 (F3 p. 3).

**EUA.** El IRS propone ajustes de precios de transferencia de TracFone (2013-2019) por ~US$364 M sin intereses. El procedimiento de acuerdo mutuo concluyó sin resolución en dic-2025 (F-64).

*Inferencia:*
- Con el marco de 2025, la regulación mexicana se vuelve una variable política. Coincide con `conocimiento/24` §4.9: los autónomos se sustituyen y la preponderancia se pronostica como decisión política.
- Las provisiones de Brasil cubren una fracción baja del reclamo. Es una cola fiscal que ni el modelo ni el DCF incluyen (§8).

### 2.7 Partes relacionadas (F1 Nota 6 pp. F-36/37; Nota 15; p. 65)

**Hechos:**
- **Transacciones de 2025 con partes relacionadas: 18,556.** Se reparten así:
  - construcción, materiales y PPE: 11,016, de los cuales 8,164 fueron con subsidiarias de Grupo Carso;
  - seguros, honorarios y otros: 5,178, de los cuales 4,323 fueron primas con Seguros Inbursa y Fianzas Guardiana Inbursa;
  - renta de torres: 605;
  - otros servicios: 1,757.
  
  Los ingresos con partes relacionadas fueron de 2,150 (F-37).
- **Saldos.** Las cuentas por cobrar suman 1,248: Sears 324, Sanborns 267, Patrimonial Inbursa 235, Sitios Latinoamérica 139 y Telesites 106. Las cuentas por pagar suman 3,264: Carso Infraestructura 693, Sitios Latinoamérica 664 y Fianzas Guardiana Inbursa 459 (F-36).
- **Arrendamientos IFRS 16 con partes relacionadas:** pasivo de 128,238 y costo anual de 29,792 (§2.3).

*Inferencia:* la relación económica más grande con el grupo de control son los arrendamientos (IFRS 16). Su costo es **1.6 veces** todo lo que muestra la tabla de la Nota 6 (29,792 contra 18,556), y esa tabla no los incluye.

### 2.8 Pensiones (F1 Nota 18 p. F-66; F-8; Nota 22 p. F-76; F4 pp. 10 y 32)

**Hechos:**
- **Pasivo total por beneficios a empleados:** 203,387 en 2025, contra 167,152 en 2024. De ese total, México son 185,513.
- **México:** obligación por beneficios definidos (DBO) de 343,621 y activos del plan de 160,323, para un neto de **183,298**. La cobertura con activos es de 46.7% (cálculo propio).
- **Costos:**
  - el costo neto del periodo fue de 21,445;
  - el costo financiero de las obligaciones laborales (17,259) está dentro de "otros resultados financieros" (F-76);
  - los beneficios pagados fueron de 21,578 (F-8);
  - la remedición registrada en ORI fue de −26,395.
- **FCF del emisor.** Suma de regreso las "obligaciones laborales" (18,535 en 2025) y las presenta como un uso del FCF (F4 pp. 10 y 32).

*Inferencia:*
- El pasivo neto de 194,454 (todas las geografías) funciona como deuda. Equivale a 16.5% de la capitalización (§6, variante).
- El FCF que publica el emisor luce mejor que el FCF IFRS porque excluye ese servicio: el FCF de 2025 se reconcilia con el del motor en −0.6 (`resultados.json` → `calculos_notas`).

### 2.9 Control interno y confiabilidad de las cifras

**Hechos:**
- **Debilidades materiales** en 2023, 2024 y 2025 (p. 37; pp. 61-62). Son de dos tipos:
  - controles generales de TI débiles (accesos, administración de cambios y segregación en la aprobación de pólizas);
  - controles sobre la información que produce la entidad (IPE).
- **Opinión del auditor.** Galaz, Yamazaki, Ruiz Urquiza (Deloitte) emitió opinión **adversa** sobre el control interno al 31-dic-2025 y opinión sin salvedades sobre los estados financieros (pp. 61-62; F-1).
- **Reexpresión de 2024.** El reporte 4T24 mostraba ISR de 29,832 y utilidad neta de 28,308 para 2024 (F5 p. 8). El 20-F muestra 35,238 y 22,902: **+5,406 de impuestos** (F1 p. F-6).
- **Presentaciones tardías o corregidas** (F7 submissions): la SEC recibió un NT 20-F el 30-abr-2025 y un 20-F/A de 2023 el 10-abr-2025.
- **Deuda de dic-24:** el reporte 4T25 dice 568,482 (F4 p. 33) y el 20-F dice 567,586 (F-58). La diferencia de 896 no está explicada (cálculo propio).
- **EBITDAaL.** Fue de 310,860 en 2025 (F4 p. 10). El EBITDA menos los pagos de arrendamiento da 320,623, así que hay 9,763 de "ajustes no monetarios" que no se concilian con el filing (cálculo propio). En el 1S26, el EBITDA subió 3.8% y el EBITDAaL bajó 0.5% (153,601 contra 154,386; F3 p. 10).

*Inferencia:*
- Las cifras no IFRS del emisor (EBITDAaL, FCF) no se pueden reconstruir exactamente. El modelo usa solo IFRS y verifica el EBITDA (C14).
- Con debilidades materiales de control interno, el riesgo de error ya no está solo en la transcripción: también puede estar en la cifra fuente.

## 3. Base histórica y doble comprobación

La base cubre FY2023, FY2024 y FY2025. La capa de hechos es `datos/transcripcion_filing_miles.json`, con renglones en miles y la página de cada bloque. `modelo.py` la convierte en `base.json` (`mapear_periodo`) y en cada corrida comprueba que `base.json` coincide con ese mapeo (**control de mapeo: OK**).

**Decisiones de mapeo** (declaradas en `base.json` → `fuentes_campos` y `notas`):
- **Balance:**
  - `ppe_neto` = PPE + activos por derecho de uso;
  - `arrendamientos_financieros` = pasivo por derecho de uso;
  - `deuda` = corto + largo plazo;
  - `proveedores` = el renglón completo de cuentas por pagar circulantes (Nota 16a incluye acreedores diversos, intereses y dividendos por pagar);
  - todos los `otros_*` son sumas de renglones reportados; ninguno se deriva como residuo.
- **Flujo:**
  - `capex` = PPE + intangibles (la misma cifra que usa el emisor);
  - **CFO del motor = CFO IFRS − intereses pagados − intereses de arrendamientos (Nota 15)**;
  - el principal de arrendamientos es el pago menos el interés devengado (supone que el interés del año se pagó en el año);
  - `sbc` = 0.
- **Estado de resultados:** `costo_ventas` no incluye D&A, así que el "margen bruto" del motor es antes de D&A. `otros_ingresos` = cambiario + valuación, costo laboral y otros + asociadas.
- **Capital:** `movimientos_capital` sale del estado de variaciones (F-7). En utilidades retenidas se separan la utilidad y los dividendos de la participación no controladora, los traspasos del superávit por revaluación y las adquisiciones de minoritarios. Con eso, C03 y C04 son pruebas reales.
- **EBITDA:** C14 compara la UO más la D&A contra el EBITDA publicado por el emisor (F5 p. 8; F4 p. 8).

**Doble comprobación** (`resultados.json` → `doble_comprobacion`; corre en cada ejecución):

| Prueba | Contra qué | Resultado |
|---|---|---|
| (A) Identidades | Totales, cruces entre estados, roll-forwards de las Notas 10, 15 y 19, y continuidad entre años | 140/140 |
| (B) Texto de la página | Cada cifra (463), con separadores de miles, en el texto extraído de su página citada | 463/463 |
| (C) SEC companyfacts (XBRL del 20-F 2024) | FY2023-FY2024: mismo periodo, valor absoluto | 249/309 aplicables. Las 60 restantes son columnas del estado de variaciones, etiquetas propias del emisor o renglones de notas que companyfacts no publica |
| (D) Visor XBRL de la SEC del 20-F 2025 (R2-R5, R83, R109, R136) | Renglón por renglón | 347/347 |
| Cobertura independiente (C o D) | Cifras confirmadas fuera del PDF | **422/463**. Las 41 restantes solo tienen (A) y (B): movimientos del estado de variaciones, movimientos del derecho de uso 2023-2024, depreciación de PPE 2023-2024, Nota 19 de 2023 y EBITDA del emisor de 2023 |

**Límites:**
- Las cuatro pruebas las ejecutó el mismo autor: es doble lectura, no auditoría.
- WebFetch convierte la página con un modelo auxiliar, y eso produjo un error que las identidades detectaron. En R83 (PPE), la combinación de negocios de 2024 (33,764) apareció en la columna de 2023; con ese renglón, la suma de 2023 no cierra, y sin él sí. Por eso de R83 solo se usa 2025.

**Métricas históricas** (cálculo sobre hechos; `resultados.json` → `historico.drivers_implicitos`):

| Concepto | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|
| Ingresos | 816,013 | 869,221 | 943,638 |
| Crecimiento | n.d. | 6.5% | 8.6% |
| Margen bruto sin D&A | 61.2% | 61.9% | 62.1% |
| EBITDA (UO + D&A) | 319,570 | 344,228 | 372,209 |
| Margen EBITDA | 39.2% | 39.6% | 39.4% |
| Margen operativo | 20.6% | 20.7% | 20.3% |
| Tasa efectiva | 30.0% | 56.1% | 37.9% |
| Utilidad neta consolidada / controladora | 80,790 / 76,111 | 27,591 / 22,902 | 88,117 / 82,819 |
| CFO IFRS reportado | 248,092 | 239,341 | 272,399 |
| CFO del motor (después de intereses de deuda y de arrendamientos) | 208,412 | 191,664 | 223,917 |
| Capex (PPE + intangibles) / % de ingresos | 156,339 / 19.2% | 130,835 / 15.1% | 130,817 / 13.9% |
| D&A / ingresos | 18.6% | 18.9% | 19.2% |
| FCF = CFO del motor − capex | 52,073 | 60,829 | 93,100 |
| Pagos totales de arrendamiento | 39,498 | 45,286 | 51,586 |
| FCF después de arrendamientos | 23,223 | 32,138 | 57,670 |
| Dividendos pagados / recompras | 30,467 / 14,331 | 31,007 / 22,747 | 33,160 / 11,944 |
| DSO / DIO / DPO (días) | 92.5 / 22.2 / 187.0 | 92.9 / 26.2 / 184.0 | 93.4 / 28.9 / 170.6 |
| Deuda financiera − caja − inversiones de CP | 400,324 | 484,250 | 447,522 |
| Pasivo por arrendamientos | 125,169 | 213,103 | 214,109 |
| Pasivo por beneficios a empleados | 143,516 | 167,152 | 203,387 |

La tasa efectiva de 56.1% en 2024 se explica así en la conciliación de F-53 (hecho): tasa legal de 30.0%, más 8.6 pp de otras partidas no deducibles, 8.8 pp de subsidiarias extranjeras, 5.7 pp de beneficios a empleados y 4.9 pp de efectos inflacionarios, entre otros. C11 la marca como ALERTA INFO. *Inferencia:* esas partidas pesaron más porque la pérdida cambiaria de 70,698 redujo la UAI a 62,830.

## 4. Modelo integrado: controles y reconciliación

`python3 empresas/AMXB.MX/modelo/modelo.py` sale con código 0. El motor produjo **539 registros: 523 OK, 0 FALLA, 14 INFO y 2 NO_APLICA**. Además, `modelo.py` relee `resultados.json` y recalcula todos los controles con `mi.verificar`, y el resultado coincide.

| Id | Control | OK | FALLA | INFO | NO_APLICA |
|---|---|---|---|---|---|
| C01 | Balance y totales | 54 | 0 | 0 | 0 |
| C02 | Caja y sumas de CFI y CFF | 59 | 0 | 0 | 0 |
| C03 | Roll-forward del capital (+ ORI) | 18 | 0 | 0 | 0 |
| C04 | Utilidades retenidas | 18 | 0 | 0 | 0 |
| C05 | PPE + derecho de uso | 18 | 0 | 0 | 0 |
| C06 | Deuda, arrendamientos y revolvente | 51 | 0 | 0 | 0 |
| C07 | Puente utilidad → CFO | 36 | 0 | 0 | 0 |
| C08 | Cuentas por cobrar | 15 | 0 | 3 | 0 |
| C09 | Inventario y proveedores | 30 | 0 | 3 | 0 |
| C10 | Intereses | 30 | 0 | 2 | 1 |
| C11 | Impuestos | 15 | 0 | 3 | 0 |
| C12 | FCF | 30 | 0 | 3 | 0 |
| C13 | Reconciliación del histórico | 2 | 0 | 0 | 1 |
| C14 | IFRS + D&A = EBITDA del emisor | 3 | 0 | 0 | 0 |
| C15 | Aritmética del estado de resultados | 84 | 0 | 0 | 0 |
| C16 | Caja mínima y revolvente | 60 | 0 | 0 | 0 |

**INFO y NO_APLICA:**
- C08-C11 son INFO en el histórico porque ahí el driver sale del mismo dato.
- C10 y C13 son NO_APLICA en FY2023 porque es el primer ejercicio y no hay saldo de apertura en la base.
- C12 es INFO porque el emisor no publica un FCF IFRS; el suyo es no IFRS y tiene otra definición (§2.8).
- En C10, la "tasa sobre deuda" del motor (11.0%) divide todos los intereses, incluidos los de arrendamientos, entre la deuda financiera. La tasa limpia es 8.08% (§2.1).

**C14.** El EBITDA del emisor coincide con UO + D&A en los tres años. Las diferencias (0.42, −0.45 y 0.33) son de redondeo a millones.

**C13, reconciliación.** El motor reproduce FY2024 y FY2025 con diferencia máxima de 0.0000 (tolerancias de 8.7 y 9.4). Partidas materiales (más de 2% de los ingresos) y su lectura:

| Partida | FY2024 | FY2025 | Lectura (hecho con página) |
|---|---:|---:|---|
| otros_ingresos (cambiario + otros financieros + asociadas + intereses cobrados) | −61,250 (−7.0%) | 10,902 (1.2%) | Resultado cambiario de −70,698 y +19,787 (F-6) |
| otros_operativos del CFO | 13,917 | −20,391 (−2.2%) | Sobre todo el cambiario no monetario revertido en el CFO: +69,722 en 2024 y −19,787 en 2025 (F-8) |
| nuevos arrendamientos (implícito) | 116,625 (13.4%) | 36,435 (3.9%) | Altas + combinación + modificaciones de 111,712 y 43,758, más la conversión (Nota 15) |
| no monetario en ppe_neto | 87,694 (10.1%) | −14,885 | Combinaciones de negocios (33,764 de PPE y 5,512 de derecho de uso en 2024, Claro Chile), conversión e hiperinflación (+52,164 en 2024; −18,929 en 2025), revaluación y bajas (Notas 10 y 15) |
| no monetario en deuda | 37,599 (4.3%) | −24,290 (−2.6%) | "Cambiario y otros" de la Nota 19 (F-74), idéntico al del filing |
| no monetario en otros_pasivos_lp | 37,118 (4.3%) | 60,411 (6.4%) | Sobre todo beneficios a empleados (+23,636 y +36,234), cuyo aumento es principalmente remedición en ORI; además, el motor carga ahí otros_operativos y otros_financiamiento |
| no monetario en otros_activos_lp | 46,778 (5.4%) | 30,627 (3.2%) | ISR diferido, intangibles de combinaciones, otros activos y el reparto de otros_inversion que hace el motor |
| no monetario en inversiones_cp | −27,072 (−3.1%) | −4,254 | Venta y valuación de inversiones (KPN en 2024, F-74) |
| capital: ORI + otros + devengado contra pagado | 36,644 (4.2%) | −47,525 (−5.0%) | ORI de +39,444 y −46,576, adquisiciones de minoritarios y dividendos decretados contra pagados (F-7) |

*Inferencia:* las partidas materiales son movimientos no monetarios que el filing documenta: tipo de cambio, hiperinflación, combinaciones de negocios, remedición de pensiones y altas de arrendamientos. No hay flujo sin explicar. El motor los reubica entre renglones de balance por su mapeo genérico.

## 5. Escenarios de mecanismo (supuestos, no pronósticos)

**Diseño común** (`base.json` → `supuestos`):
- **Horizonte y caja:** 5 años (2026E-2030E) desde el balance al 31-dic-2025. Caja mínima de 25,000, cercana al mínimo de 2023-2025 (26,598).
- **Tipo de cambio constante:** el resultado cambiario vale 0; el choque cambiario se mide en §7.
- **Deuda:** las amortizaciones siguen los vencimientos (2026: la deuda de corto plazo de 91,973; 2027-2030: F-60). Se refinancia 50%, 80% o 60% según el escenario, y el faltante se cubre con revolvente ("financiamiento requerido").
- **Resultados financieros:**
  - `otros_ingresos` = otros resultados financieros sin intereses de caja ni cambiario; en 2025 fueron −18,306 + 294 (F-6), con el costo financiero laboral de 17,259 dentro (F-76);
  - rendimiento de 6% sobre la caja más las inversiones de CP, cercano al objetivo de Banxico de 6.50% (`conocimiento/03` §2.3).
- **Capital:** SBC = 0. Dividendos a partir de Ps 0.54 × ~60.1 mil M de acciones más minoritarios ≈ 34,650 (F-82; F3 p. 3). Las recompras se imputan 100% a utilidades retenidas; en 2025 fue 99.98% (F-7).

| Driver (supuesto) | Tensión | Intermedio | Eficiencia | Ancla (hecho) |
|---|---|---|---|---|
| Crecimiento de ingresos 2026E-2030E | +1%, 0%, +2%, +3%, +3% | +3%, +4.5%, +4.5%, +4.5%, +4% | +4%, +5.5%, +5.5%, +5%, +5% | 1S26 +2.6% en MXN; servicios del 2T26 +5.1% a tipo de cambio constante (F3 pp. 7-8) |
| Margen bruto sin D&A | 61.5% | 62.5% | 63.2% | 62.1% (2025); 63.0% (1S26, F3 p. 8) |
| Margen operativo | 20% → 18% | 21% | 21.5% → 24% | 20.3% (2025); 21.4% (1S26) |
| D&A / ingresos | 19% | 18.7% | 18% | 19.2% (2025); 18.4% (1S26) |
| Capex / ingresos | 13.5%, **16.5% (espectro 2027)**, 15%, 14.5%, 14.5% | 13.5% | 12.5% → 12% | 13.9% (2025); 10.1% (1S26); 19.2% (2023) |
| Tasa de impuestos | 40% | 37% | 33% | 37.9% (2025); 30.0% (2023); 56.1% (2024) |
| DSO / DIO / DPO | 97 / 30 / 160 | 93 / 29 / 170 | 90 / 28 / 175 | 93.4 / 28.9 / 170.6 (2025) |
| Tasa de la deuda / de arrendamientos | 9.0% / 8.0% | 8.1% / 7.56% | 7.5% / 7.2% | 8.08% / 7.56% implícitas en 2025 (§2.1, §2.3) |
| Otros resultados financieros | −28,000 | −18,000 | −12,000 | −18,012 (2025); −32,186 (2023) |
| Dividendos (monto) | 34,650 fijo | 34,650, +4% anual | 34,650, +8% anual | 33,160 pagados en 2025 |
| Recompras | 5,000 | 10,000 | 15,000 | 11,944 (2025); fondo de 10 mil M (F-82) |
| Arrendamientos nuevos / principal | 48,000 / 37,000 | 44,000 / 36,000 | 40,000 / 35,000 | 43,721 / 35,429 (2025) |
| Refinanciamiento de vencimientos | 50% | 80% | 60% | — |

**Resultados** (`resultados.json` → `escenarios`; tabla completa en el Anexo A):

| Concepto | Tensión | Intermedio | Eficiencia |
|---|---:|---:|---:|
| Ingresos 2030E (TCAC 2025-2030) | 1,031,339 (1.8%) | 1,153,520 (4.1%) | 1,204,266 (5.0%) |
| Utilidad neta acumulada 2026E-2030E | 284,194 | 501,317 | 674,185 |
| FCF después de arrendamientos acumulado | 275,697 | 573,280 | 805,995 |
| Dividendos + recompras acumulados | 198,250 | 237,674 | 278,278 |
| **Financiamiento requerido (revolvente)** | **54,068** (2026E-2029E; máximo 54,068) | 0 | 0 |
| Caja 2030E | 25,000 (en el mínimo) | 314,867 | 451,284 |
| Deuda neta 2030E, con arrendamientos (2025: 661,631) | 639,185 | 366,026 | 158,914 |

*Inferencia (mecanismo):*
- En tensión, el faltante aparece desde 2026 aunque el FCF sea positivo. La razón es el refinanciamiento parcial, no una pérdida operativa. Con una política de dividendos fija, el acceso al mercado es la variable crítica.
- En los otros dos escenarios la caja se acumula porque no se supone ningún uso para el excedente. No es una predicción de política de capital.

**Puente escenarios → DCF** (`resultados.json` → `puente_escenarios_dcf`). Componentes del margen FCFF (opción B, §6) como % de los ingresos:

| Componente | 2025 real | Tensión 2026E | Intermedio 2026E | Eficiencia 2026E |
|---|---:|---:|---:|---:|
| EBITDA | 39.44% | 39.00% | 39.70% | 39.50% |
| Impuestos (pagados en 2025; modelados en los escenarios) | −5.64% | −4.34% | −5.08% | −5.09% |
| Capex | −13.86% | −13.50% | −13.50% | −12.50% |
| Arrendamientos (interés + principal) | −5.47% | −5.73% | −5.40% | −5.16% |
| Capital de trabajo | **−2.39%** | −2.10% | **−0.44%** | +0.61% |
| Ajuste financiero (escudo de la deuda e intereses cobrados) | −1.67% | −1.31% | −1.12% | −0.98% |
| Resto (2025: pensiones pagadas, PTU y no monetarias; escenarios: otros resultados financieros) | −2.55% | −2.94% | −1.85% | −1.22% |
| **Margen FCFF** | **7.87%** | **9.08%** | **12.31%** | **15.17%** |

| Escenario | TCAC de ingresos 2025-2030 | Margen FCFF promedio 2026E-2030E | Crecimiento que exige el precio con ese margen (WACC 11.02%, g 3.5%) |
|---|---:|---:|---:|
| Tensión | 1.8% | 8.42% | 9.0% |
| Intermedio | 4.1% | 12.64% | 3.3% |
| Eficiencia | 5.0% | 15.98% | 0.1% |

*Inferencia:*
- La mayor parte de la brecha entre el 7.87% de 2025 y el 12.3% del intermedio viene del capital de trabajo (1.95 pp) y del resto (0.70 pp). Ninguna de las dos está anclada en un driver con historia.
  - El motor mantiene constantes los "otros activos", cuyo aumento drenó 10,720 en 2025 (F-8).
  - Tampoco modela pagos de pensiones por encima del costo.
- Por eso el margen del intermedio **no es evidencia**: es consecuencia de los supuestos y de la simplificación del motor.
- La variable a vigilar para saber si el precio "cuadra" es la conversión de EBITDA a caja (capital de trabajo, impuestos pagados y pensiones), más que el crecimiento de los ingresos.

## 6. DCF inverso

**Método** (`mi.dcf_inverso`, `conocimiento/03` §2.7):
- VE objetivo = precio × acciones + deuda neta.
- FCFF = ingresos × margen, con ingresos que crecen a una tasa constante g durante 10 años.
- Valor terminal de Gordon a g terminal; descuento a fin de año.
- g se despeja por bisección.

**Insumos (hechos y cálculos):**
- **Precio:** 19.60 MXN, el `regularMarketPrice` de Yahoo del 24-sep-2026 (F8). La barra diaria de ese día aún no traía cierre. Como variante se usa el cierre del 23-sep, 19.34.
- **Acciones:** 60,100 M al cierre de jun-26 (F3 p. 3). La cifra del emisor está redondeada, con error de ±0.08%.
- **Capitalización:** 1,177,960.
- **Deuda neta base: 466,586.** Se compone de:
  - deuda financiera de 476,927 menos efectivo y valores de 75,943 (jun-26, F3 p. 32);
  - participación no controladora en libros de 65,602 (dic-25, F-5), porque el FCFF es consolidado.
- **VE objetivo:** 1,644,546.
- **Ingresos base de 12 meses a jun-26:** 955,730 (= 943,638 − 465,823 + 477,915; F1 y F3 p. 8).

**Tratamiento de los arrendamientos:**
- **Base, opción B:** los arrendamientos se tratan como costo operativo. El FCFF resta todos los pagos de arrendamiento y la deuda neta los excluye.
- **Variante, opción A:** los arrendamientos se tratan como deuda. El FCFF se calcula antes de los pagos, pero **se restan los arrendamientos nuevos** (inversión en especie), y la deuda neta suma el pasivo de 214,400.

**Margen FCFF (opción B)** = (CFO IFRS − intereses cobrados − pagos de arrendamiento − capex − 30% × (gasto por intereses − intereses de arrendamientos)) / ingresos (`resultados.json` → `dcf_inverso.margenes_fcff`):

| | 2023 | 2024 | 2025 | 12m a jun-26 |
|---|---:|---:|---:|---:|
| FCFF (B) | 37,204 | 47,903 | 74,243 | 92,213 |
| Margen FCFF (B) | 4.56% | 5.51% | **7.87%** | 9.65% |

- En la columna de 12 meses, los intereses cobrados y el escudo fiscal son los de 2025, porque no se publican trimestrales.
- El promedio 2023-2025 es 5.98%.

**WACC en MXN** (método del sistema, `conocimiento/03` §2.3 y §6.1):

| Insumo | Valor | Fuente |
|---|---:|---|
| r_f en USD ajustada = T-bond de 5.11% − diferencial de default de EUA de 0.22% | 4.89% | F9 (DGS10, 23-sep-2026); F10 |
| β desapalancada, Telecom Services en emergentes, corregida por caja (142 empresas) | 0.614 | F11 |
| D/E a mercado = (476,927 + 214,400 de arrendamientos) / 1,177,960 | 0.587 | cálculo; Damodaran desapalanca con arrendamientos |
| β reapalancada = 0.614 × (1 + 0.7 × 0.587) | 0.866 | cálculo |
| Prima de mercado maduro | 4.20% | F10 |
| CRP ponderada por ingresos externos de 2025 (tabla abajo) | 3.04% | F1 Nota 23 p. F-80; F10 |
| k_e en USD = 4.89% + 0.866 × 4.20% + 3.04% | 11.57% | cálculo |
| Inflación esperada: México (**supuesto**, meta de Banxico de 3% ± 1 pp) / EUA (T5YIE, 24-sep) | 3.5% / 2.33% | supuesto / F9 |
| k_e en MXN = (1.1157)(1.035)/(1.0233) − 1 | 12.85% | cálculo |
| k_d en MXN, antes y después de impuestos (AMX34 al 9.3%; t = 30%) | 9.30% / 6.51% | F4 p. 3; F1 p. F-53 |
| Peso del capital (sin arrendamientos) | 71.2% | cálculo |
| **WACC base** | **11.02%** | cálculo |
| r_f en MXN implícita (para el tope de g) | 6.09% | cálculo |

| Segmento (F1 Nota 23) | Peso en ingresos externos | Países (Damodaran, jul-2026) | CRP |
|---|---:|---|---:|
| México (Telcel y corporativo) + Telmex | 27.6% + 9.7% | México (Baa3) | 2.72% |
| Brasil | 18.8% | Brasil | 3.10% |
| Europa | 12.8% | Austria (**supuesto**: el filing no desglosa por país; Belarús tiene CRP de 27.2%) | 0.34% |
| Colombia | 8.3% | Colombia | 2.72% |
| Andina | 6.1% | Ecuador y Perú (promedio simple) | 5.63% |
| Centroamérica | 6.0% | 5 países (promedio simple) | 5.59% |
| Caribe | 3.9% | Rep. Dominicana y EUA (Puerto Rico) | 1.97% |
| Argentina | 3.9% | Argentina | 9.28% |
| Uruguay, Paraguay y Chile | 2.9% | promedio simple | 2.04% |
| **Ponderada** | 100% | | **3.04%** |

**Resultado base.** El precio de 19.60 exige un crecimiento de ingresos de **9.88% anual durante 10 años**. El valor terminal pesa 56.8% del VE, con un múltiplo terminal de 13.8x el FCFF. El estado es OK y sin alertas: g < r_f y el valor terminal pesa menos de 75%.

**Sensibilidad (WACC ±1 pp × g ±0.5 pp × margen).** Crecimiento anual implícito y, entre paréntesis, peso del valor terminal:

| Margen FCFF | WACC \ g | 3.0% | 3.5% | 4.0% |
|---|---|---:|---:|---:|
| Bajo: 5.98% (promedio 2023-2025) | 10.02% | 12.1% (61%) | 11.4% (63%) | 10.7% (64%) |
| | 11.02% | 14.2% (59%) | 13.6% (60%) | 13.0% (62%) |
| | 12.02% | 16.2% (57%) | 15.7% (58%) | 15.2% (59%) |
| **Base: 7.87% (2025)** | 10.02% | 8.4% (58%) | 7.8% (59%) | 7.1% (60%) |
| | 11.02% | 10.4% (56%) | **9.9% (57%)** | 9.3% (58%) |
| | 12.02% | 12.3% (54%) | 11.8% (55%) | 11.3% (56%) |
| Alto: 9.65% (12m a jun-26) | 10.02% | 5.6% (55%) | 5.1% (56%) | 4.4% (57%) |
| | 11.02% | 7.6% (53%) | 7.1% (54%) | 6.5% (55%) |
| | 12.02% | 9.4% (51%) | 9.0% (52%) | 8.5% (53%) |

**Variantes** (WACC de 11.02%, g de 3.5% y margen de 7.87%, salvo que se indique otra cosa):

| Variante | WACC | Margen | Deuda neta | Crecimiento implícito |
|---|---:|---:|---:|---:|
| Precio de cierre del 23-sep (19.34) | 11.02% | 7.87% | 466,586 | 9.8% |
| Sin participación no controladora en la deuda neta | 11.02% | 7.87% | 400,984 | 9.3% |
| Arrendamientos como deuda (FCFF antes de arrendamientos menos arrendamientos nuevos) | 10.36% | 8.19% | 680,986 | 9.6% |
| **TRAMPA:** arrendamientos como deuda sin restar los arrendamientos nuevos | 10.36% | 12.82% | 680,986 | **3.6%** |
| Pensiones como deuda (+21,578 de pagos al FCFF; +194,454 a la deuda neta) | 11.02% | 10.15% | 661,040 | 7.9% |
| r_f local: M-bono de 10 años (9.16%, ago-2026) − default de México (1.75%) | 11.90% | 7.87% | 466,586 | 11.6% |
| β global de Telecom Services (0.496) | 10.52% | 7.87% | 466,586 | 8.8% |

*Inferencia:*
- **El precio exige mucho con la historia reciente.** Con cualquier margen FCFF histórico y un WACC de 10% a 12%, el crecimiento que exige va de 4.4% a 16.2% nominal anual en pesos durante 10 años. Solo con el margen de los últimos 12 meses (9.65%) y un WACC de 10% baja a ~5%.
  - Las tasas base de un operador maduro con 414.5 M de accesos (F3 p. 4) y crecimiento de servicios de ~5% a tipo de cambio constante (F3 p. 7) están más cerca de 4%-5% que de 10%. Esta comparación es cualitativa: no se calcularon tasas base del sector (pendiente).
- **La lectura consistente es otra.** El mercado descuenta una **mejora sostenida en la conversión a caja**: capex cerca de 12%-13% de los ingresos, menor drenaje de capital de trabajo y de pensiones. No descuenta crecimiento alto. El puente de §5 cuantifica ese mecanismo.
- **La forma de tratar los arrendamientos es la decisión metodológica que más mueve el resultado.** La versión inconsistente (TRAMPA) haría ver el precio como "barato" (3.6%).
- **El WACC está calculado, no es un dato.** La variante con r_f local (M-bono) lo sube 0.9 pp y el crecimiento exigido a 11.6%.

## 7. Sensibilidad geopolítica y regulatoria reproducible

Son dos mecanismos con insumos citados y parámetros hipotéticos. **No hay probabilidades ni valor esperado.** El cálculo usa `Decimal` y comprueba identidades en las 24 celdas (error máximo: 0). Resultados en `resultados.json` → `sensibilidad_geopolitica`.

**(1) Registro obligatorio de líneas en México** (política pública; `conocimiento/24` §4.9; §2.6).

Insumos (hechos):
- 68,421 mil líneas de prepago de Telcel a jun-26 y ARPU móvil de México de 194 MXN al mes, mezcla de prepago y pospago (F3 p. 12);
- servicio móvil de México anualizado a partir del 2T26: 196,108 (F3 p. 12);
- EBITDA de 12 meses a jun-26: 379,163 (F4 p. 8 y F3 p. 8);
- utilidad de la controladora de 12 meses: 89,567;
- 60,100 M de acciones;
- tasa marginal de 30%.

Parámetros (supuestos):
- s = fracción del prepago suspendida todo un año;
- k = ARPU de las líneas suspendidas relativo al promedio (muchas suspendidas estarían inactivas);
- c = fracción del ingreso perdido que cae al EBITDA.

| s | k | Líneas (M) | Ingreso perdido/año | % servicio móvil MX | Δ EBITDA (c = 0.7 / 0.9) | % EBITDA 12m (c = 0.9) | Δ UPA MXN (c = 0.9) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 5% | 10% | 3.42 | 796 | 0.4% | −557 / −717 | −0.2% | −0.008 |
| 5% | 25% | 3.42 | 1,991 | 1.0% | −1,394 / −1,792 | −0.5% | −0.021 |
| 5% | 50% | 3.42 | 3,982 | 2.0% | −2,787 / −3,584 | −0.9% | −0.042 |
| 15% | 10% | 10.26 | 2,389 | 1.2% | −1,672 / −2,150 | −0.6% | −0.025 |
| 15% | 25% | 10.26 | 5,973 | 3.0% | −4,181 / −5,376 | −1.4% | −0.063 |
| 15% | 50% | 10.26 | 11,946 | 6.1% | −8,362 / −10,752 | −2.8% | −0.125 |
| 30% | 10% | 20.53 | 4,779 | 2.4% | −3,345 / −4,301 | −1.1% | −0.050 |
| 30% | 25% | 20.53 | 11,946 | 6.1% | −8,362 / −10,752 | −2.8% | −0.125 |
| 30% | 50% | 20.53 | 23,893 | 12.2% | −16,725 / −21,503 | −5.7% | −0.250 |

*Inferencia:*
- El conteo de líneas puede caer mucho sin que el ingreso caiga en la misma proporción. El parámetro que más mueve el resultado es k, el ARPU de las líneas suspendidas, y el filing no lo publica (pendiente §9).
- La `ficha.md` cita que al 25-jun estaba registrado 39.1% del universo (Expansión, secundaria; no verificado aquí).

**(2) Choque cambiario sobre la deuda en USD** (macro-geopolítica).

Contexto:
- el T-MEC pasó a revisiones anuales y la 4ª ronda está anunciada, de forma tentativa, para el 28-29 de septiembre;
- el diferencial entre Banxico y el techo de la Fed es de 250 pb;
- Moody's calificó a México Baa3 el 20-may-2026 (`conocimiento/24` §4.8, §4.10 y §4.11);
- hay una guerra en Irán (F3 p. 7).

Insumos:
- deuda en USD de US$9,001 M y USD/MXN de 17.47 a jun-26 (F3 pp. 32 y 30);
- coberturas USD→MXN de US$4,990 M a dic-25 (F1 Nota 7). **Supuesto:** siguen vigentes, lo que da una cobertura de 55.4%.
- el USD/MXN estaba en 17.69 el 25-sep-2026 (F8).

| Depreciación del MXN | Cobertura | Aumento de la deuda en USD | Pérdida cambiaria antes de impuestos | Δ utilidad neta | % utilidad 12m | Δ UPA MXN |
|---:|---:|---:|---:|---:|---:|---:|
| 5% | 0% | 7,862 | 7,862 | −5,504 | −6.1% | −0.092 |
| 5% | 55.4% | 7,862 | 3,504 | −2,453 | −2.7% | −0.041 |
| 10% | 0% | 15,725 | 15,725 | −11,007 | −12.3% | −0.183 |
| 10% | 55.4% | 15,725 | 7,007 | −4,905 | −5.5% | −0.082 |
| 20% | 0% | 31,449 | 31,449 | −22,015 | −24.6% | −0.366 |
| 20% | 55.4% | 31,449 | 14,014 | −9,810 | −11.0% | −0.163 |

La elasticidad observada fue de −3,539 por cada +1% del USD/MXN en 2024 y de −1,742 en 2025 (§2.2). La rejilla con cobertura (−701 por 1%) queda por debajo de ambas.

*Inferencia:*
- La rejilla solo incluye el USD. Deja fuera EUR, GBP (swapeada a USD y EUR) y las posiciones intercompañía.
- En 2024 y 2025 el efecto real fue 2.5 a 5 veces mayor por punto porcentual. La sensibilidad cambiaria "verdadera" del resultado neto es probablemente mayor que la de la tabla, pero no se puede reconstruir con lo publicado.
- **Diferencia entre los dos choques:**
  - El cambiario es sobre todo contable (reexpresión de deuda) y se revierte si el peso se recupera. Mueve la UPA trimestral; es relevante para los pronósticos registrados del 3T26 en la ficha.
  - El del registro de líneas afecta el EBITDA y la caja.

## 8. Qué NO demuestra este trabajo

1. **No es una valuación ni una recomendación.** El DCF inverso solo traduce el precio en el crecimiento que exige bajo supuestos explícitos. El resultado cambia por varios puntos según el WACC, el margen y el tratamiento de arrendamientos y pensiones.
2. **Los escenarios no son pronósticos.** Su margen FCFF es mayor que el histórico en parte por simplificaciones del motor:
   - otros activos y pasivos constantes;
   - sin driver para "otros operativos";
   - pensiones pagadas iguales al costo.
   
   El puente de §5 lo cuantifica, pero no lo corrige.
3. **La doble comprobación la hizo el mismo autor** y no es una auditoría. De 463 cifras, 41 solo se verificaron contra el PDF y por identidades. Las debilidades materiales del emisor (§2.9) implican además un riesgo de error en la cifra fuente.
4. **El WACC depende de estimaciones:**
   - β sectorial de Damodaran (enero de 2026);
   - CRP por segmento con promedios simples, y Europa igual a Austria;
   - inflación esperada de México como supuesto;
   - k_d tomado de una emisión de nov-2025.
5. **La sensibilidad cambiaria** supone que las coberturas de dic-25 siguen vigentes. Ignora el EUR, la GBP y la conversión de las subsidiarias.
6. **La sensibilidad del registro de líneas** no estima cuántas líneas se suspenderán ni su ARPU real. Solo muestra el rango del mecanismo.
7. **Quedaron fuera del modelo:**
   - la cola fiscal de Brasil (130,739 de contingencias frente a 25,361 provisionados);
   - el IRS (US$364 M);
   - la posible licitación 5G (salvo como supuesto de capex en tensión);
   - la adquisición de Desktop (F-82) y la de WOW Perú (F3 p. 4).
8. **No se leyó el 20-F completo.** Items 4 a 7 se leyeron solo en parte; en particular, la sección de transacciones con partes relacionadas del Item 7 y las condiciones de los contratos de torres.

## 9. Pendientes

1. Definir `SEC_USER_AGENT` con un correo real del sistema. Con él se puede descargar `ef20060642_20f.htm` y la instancia XBRL del 20-F 2025, y confirmar por máquina las 41 cifras que hoy solo dependen del PDF.
2. Obtener el ARPU de prepago y la proporción de líneas de prepago que generan ingresos, para calibrar k en §7. Seguir las suspensiones del 3T26-4T26 contra la rejilla.
3. Confirmar las coberturas vigentes a jun-26 y la dirección de cada pata de los XCS (6-K del 2T26 con estados intermedios).
4. Desglosar el gasto por intereses: tasa implícita de 8.08% contra 6.29% declarada (retención, comisiones, CDI).
5. Identificar las contrapartes, plazos y escalamientos de los arrendamientos con partes relacionadas (Item 7 del 20-F).
6. Conseguir ingresos por país dentro de Europa, Andina y Centroamérica para afinar la CRP. Revisar la prima de Belarús.
7. Obtener el motivo documentado de la reexpresión de 2024 (NT 20-F del 30-abr-2025) y el contenido del 20-F/A de 2023.
8. Sustituir el supuesto de inflación de México (3.5%) por la encuesta de expectativas de Banxico (requiere token de SIE).
9. Proponer al motor un driver para "otros operativos" o para la variación de otros activos, que cierre la brecha de conversión a caja de §5.
10. Calcular tasas base de crecimiento de ingresos para operadores de telecomunicaciones de tamaño comparable (`conocimiento/03` §6.1, regla 5) y compararlas con el crecimiento implícito.
11. Con el reporte del 3T26 (~20-oct-2026): contrastar ingresos, EBITDA, capex y capital de trabajo contra los tres escenarios (sin tratarlos como pronósticos) y contra los pronósticos registrados en la ficha.

## 10. Reproducción y huellas

```
python3 empresas/AMXB.MX/modelo/modelo.py          # codigo 0; escribe resultados.json y SHA256SUMS.txt
python3 herramientas/huellas.py verificar empresas/AMXB.MX/modelo/datos/SHA256SUMS.txt   # OK
(cd empresas/AMXB.MX/modelo && sha256sum -c SHA256SUMS.txt)                            # base.json, modelo.py, resultados.json: OK
python3 empresas/AMXB.MX/modelo/modelo.py --base   # regenera base.json.historico desde datos/transcripcion_filing_miles.json
```

- La corrida es determinista: dos ejecuciones seguidas producen el mismo `resultados.json` (mismo sha256).
- Solo usa la biblioteca estándar.
- No se modificó `herramientas/`, y las 237 pruebas de `herramientas/tests` pasan.
- Las extracciones de trabajo (pypdf, openpyxl y xlrd para leer PDF y Excel) se hicieron fuera del repositorio. Sus productos están congelados en `datos/` con hash.

## Anexo A. Salida del motor (`mi.resumen_markdown`, sin edición)

Motor herramientas/modelo_integrado.py v1.0 | America Movil, S.A.B. de C.V. | MXN millones

> FASE 0 (formacion). Escenarios con supuestos explicitos: no son pronosticos, guia del emisor ni consenso, y no constituyen recomendacion de compra o venta.

**Controles:** 539 registros, OK 523, FALLA 0, INFO 14, NO_APLICA 2. Todos OK: si.

| Id | Control | OK | FALLA | INFO | NO_APLICA |
|---|---|---|---|---|---|
| C01 | Balance: activo = pasivo + capital (y totales = suma de componentes) | 54 | 0 | 0 | 0 |
| C02 | Caja: inicial + CFO + CFI + CFF + efecto cambiario = final (y sumas de CFI y CFF) | 59 | 0 | 0 | 0 |
| C03 | Capital: inicial + utilidad + SBC - dividendos - recompras + emisiones + ORI + otros = final | 18 | 0 | 0 | 0 |
| C04 | Utilidades retenidas: inicial + utilidad - dividendos - recompras imputadas + otros = final | 18 | 0 | 0 | 0 |
| C05 | PPE: inicial + capex + nuevos arrendamientos - depreciacion + otros = final | 18 | 0 | 0 | 0 |
| C06 | Deuda: inicial + emisiones - amortizaciones (+ otros) = final (deuda, arrendamientos, revolvente) | 51 | 0 | 0 | 0 |
| C07 | Puente utilidad -> CFO: utilidad + D&A + SBC + capital de trabajo + otros = CFO | 36 | 0 | 0 | 0 |
| C08 | Cuentas por cobrar = dias_cxc x ingresos / 365 | 15 | 0 | 3 | 0 |
| C09 | Inventario y proveedores = dias x costo de ventas / 365 | 30 | 0 | 3 | 0 |
| C10 | Intereses = tasa x deuda promedio; ingreso financiero = tasa x caja promedio | 30 | 0 | 2 | 1 |
| C11 | Impuestos = tasa x utilidad antes de impuestos | 15 | 0 | 3 | 0 |
| C12 | FCF = CFO - capex; FCF despues de principal de arrendamientos financieros = FCF - principal | 30 | 0 | 3 | 0 |
| C13 | Reconciliacion del historico: el motor reproduce los estados cargados con drivers implicitos | 2 | 0 | 0 | 1 |
| C14 | Conciliacion GAAP vs ajustado: cifra GAAP + ajustes = cifra ajustada | 3 | 0 | 0 | 0 |
| C15 | Aritmetica del estado de resultados (ingresos, bruta, operativa, UAI, neta) | 84 | 0 | 0 | 0 |
| C16 | Caja minima y revolvente: caja >= minimo; financiamiento requerido explicito, sin plug | 60 | 0 | 0 | 0 |

**Reconciliacion FY2024** (calculo sobre hechos; max |dif| = 0.0000, tolerancia 8.6922)

| Partida conciliatoria | Monto | % ingresos | Origen | Material |
|---|---|---|---|---|
| otros_ingresos (UAI - UO + intereses; incluye ingreso financiero) | -61,250.4 | -7.0% | implicito | ALERTA |
| otros_operativos del CFO (incluye diferencia capital de trabajo balance vs flujo) | 13,917.4 | 1.6% | implicito |  |
| otros_inversion (CFI + capex) | 1,599.2 | 0.2% | implicito |  |
| otros_financiamiento (CFF - componentes) | -2,310.1 | -0.3% | implicito |  |
| efecto_cambiario | 3,070.8 | 0.4% | reportado |  |
| nuevos arrendamientos financieros (saldo final - inicial + principal) | 116,624.7 | 13.4% | implicito | ALERTA |
| movimiento no monetario / no explicado en inversiones_cp | -27,071.9 | -3.1% | residuo explicito | ALERTA |
| movimiento no monetario / no explicado en otros_activos_circulantes | 11,748.5 | 1.4% | residuo explicito |  |
| movimiento no monetario / no explicado en otros_activos_lp | 46,777.8 | 5.4% | residuo explicito | ALERTA |
| movimiento no monetario / no explicado en ppe_neto | 87,694.2 | 10.1% | residuo explicito | ALERTA |
| movimiento no monetario / no explicado en otros_pasivos_circulantes | 10,858.6 | 1.2% | residuo explicito |  |
| movimiento no monetario / no explicado en otros_pasivos_lp | 37,117.7 | 4.3% | residuo explicito | ALERTA |
| movimiento no monetario / no explicado en deuda | 37,598.8 | 4.3% | residuo explicito | ALERTA |
| capital: ORI + otros + diferencias devengado vs pagado (del estado de variaciones) | 36,644.2 | 4.2% | derivado de movimientos_capital | ALERTA |
| utilidades retenidas: movimientos distintos de utilidad, dividendos pagados y recompras | -2,254.6 | -0.3% | residuo explicito |  |

**Reconciliacion FY2025** (calculo sobre hechos; max |dif| = 0.0000, tolerancia 9.4364)

| Partida conciliatoria | Monto | % ingresos | Origen | Material |
|---|---|---|---|---|
| otros_ingresos (UAI - UO + intereses; incluye ingreso financiero) | 10,902.2 | 1.2% | implicito |  |
| otros_operativos del CFO (incluye diferencia capital de trabajo balance vs flujo) | -20,391.2 | -2.2% | implicito | ALERTA |
| otros_inversion (CFI + capex) | 7,917.2 | 0.8% | implicito |  |
| otros_financiamiento (CFF - componentes) | -737.7 | -0.1% | implicito |  |
| efecto_cambiario | -3,055.4 | -0.3% | reportado |  |
| nuevos arrendamientos financieros (saldo final - inicial + principal) | 36,434.8 | 3.9% | implicito | ALERTA |
| movimiento no monetario / no explicado en inversiones_cp | -4,253.7 | -0.5% | residuo explicito |  |
| movimiento no monetario / no explicado en otros_activos_circulantes | -7,440.3 | -0.8% | residuo explicito |  |
| movimiento no monetario / no explicado en otros_activos_lp | 30,627.1 | 3.2% | residuo explicito | ALERTA |
| movimiento no monetario / no explicado en ppe_neto | -14,885.4 | -1.6% | residuo explicito |  |
| movimiento no monetario / no explicado en otros_pasivos_circulantes | 12,397.4 | 1.3% | residuo explicito |  |
| movimiento no monetario / no explicado en otros_pasivos_lp | 60,410.5 | 6.4% | residuo explicito | ALERTA |
| movimiento no monetario / no explicado en deuda | -24,290.3 | -2.6% | residuo explicito | ALERTA |
| capital: ORI + otros + diferencias devengado vs pagado (del estado de variaciones) | -47,525.3 | -5.0% | derivado de movimientos_capital | ALERTA |
| utilidades retenidas: movimientos distintos de utilidad, dividendos pagados y recompras | -2,782.2 | -0.3% | residuo explicito |  |

**Escenario tension** (supuesto de escenario; no es pronostico): Mecanismo de tension: bajas de prepago en Mexico por el registro obligatorio de lineas y competencia (ingresos planos 2026-2027), regulacion asimetrica mas dura y pago de espectro 5G en 2027 (capex 16.5%), tasas altas, acceso limitado a mercado (se refinancia 50% de los vencimientos) y costo financiero no operativo como 2023.

| Concepto | 2026E | 2027E | 2028E | 2029E | 2030E |
|---|---|---|---|---|---|
| Ingresos | 953,074.8 | 953,074.8 | 972,136.3 | 1,001,300.4 | 1,031,339.4 |
| Utilidad operativa | 190,615.0 | 176,318.8 | 174,984.5 | 180,234.1 | 185,641.1 |
| Utilidad neta | 62,038.2 | 53,520.9 | 52,544.0 | 56,057.9 | 60,033.5 |
| CFO | 223,091.5 | 234,605.1 | 234,798.0 | 242,553.5 | 252,124.0 |
| Capex | 128,665.1 | 157,257.3 | 145,820.4 | 145,188.6 | 149,544.2 |
| FCF | 94,426.4 | 77,347.8 | 88,977.5 | 97,365.0 | 102,579.8 |
| FCF despues de arrendamientos | 57,426.4 | 40,347.8 | 51,977.5 | 60,365.0 | 65,579.8 |
| Dividendos + recompras | 39,650.0 | 39,650.0 | 39,650.0 | 39,650.0 | 39,650.0 |
| Financiamiento requerido | 18,255.8 | 20,309.0 | 9,091.0 | 6,411.8 | 0.0 |
| Caja final | 25,000.0 | 25,000.0 | 25,000.0 | 25,000.0 | 25,000.0 |
| Revolvente | 18,255.8 | 38,564.8 | 47,655.8 | 54,067.6 | 51,833.0 |
| Deuda neta | 654,855.1 | 665,157.3 | 663,829.8 | 654,114.8 | 639,185.0 |
- 2026E: FINANCIAMIENTO REQUERIDO 18255.8 (revolvente) para mantener caja_minima 25000
- 2027E: FINANCIAMIENTO REQUERIDO 20309 (revolvente) para mantener caja_minima 25000
- 2028E: FINANCIAMIENTO REQUERIDO 9091.03 (revolvente) para mantener caja_minima 25000
- 2029E: FINANCIAMIENTO REQUERIDO 6411.85 (revolvente) para mantener caja_minima 25000

**Escenario intermedio** (supuesto de escenario; no es pronostico): Mecanismo intermedio: continuidad de 2025-1S26 (servicios +5% a tipo de cambio constante, margen de operacion ~21% como en 1S26, capex 13.5% como 2025, tasa efectiva 37%) con dividendo creciendo 4% y recompras de Ps 10 mil M; se refinancia 80% de los vencimientos.

| Concepto | 2026E | 2027E | 2028E | 2029E | 2030E |
|---|---|---|---|---|---|
| Ingresos | 971,947.6 | 1,015,685.2 | 1,061,391.0 | 1,109,153.6 | 1,153,519.8 |
| Utilidad operativa | 204,109.0 | 213,293.9 | 222,892.1 | 232,922.3 | 242,239.2 |
| Utilidad neta | 84,060.1 | 91,671.0 | 99,795.1 | 108,554.6 | 117,235.9 |
| CFO | 261,529.8 | 276,796.0 | 293,250.7 | 310,715.7 | 328,066.9 |
| Capex | 131,212.9 | 137,117.5 | 143,287.8 | 149,735.7 | 155,725.2 |
| FCF | 130,316.9 | 139,678.4 | 149,962.9 | 160,980.0 | 172,341.7 |
| FCF despues de arrendamientos | 94,316.9 | 103,678.4 | 113,962.9 | 124,980.0 | 136,341.7 |
| Dividendos + recompras | 44,650.0 | 46,036.0 | 47,477.0 | 48,976.0 | 50,535.0 |
| Financiamiento requerido | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Caja final | 66,226.7 | 115,466.4 | 173,384.9 | 238,538.2 | 314,866.8 |
| Revolvente | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Deuda neta | 619,964.5 | 570,322.1 | 511,836.1 | 443,832.2 | 366,025.5 |

**Escenario eficiencia** (supuesto de escenario; no es pronostico): Mecanismo de eficiencia: ahorro de costos (IA en atencion y red), margen de operacion subiendo a 24%, capex normalizado en 12% de ingresos, menor tasa efectiva (33%, como 2023), menor costo financiero; dividendo +8% anual, recompras de Ps 15 mil M y desendeudamiento (se refinancia 60% de los vencimientos).

| Concepto | 2026E | 2027E | 2028E | 2029E | 2030E |
|---|---|---|---|---|---|
| Ingresos | 981,383.9 | 1,035,360.1 | 1,092,304.9 | 1,146,920.1 | 1,204,266.1 |
| Utilidad operativa | 210,997.5 | 229,849.9 | 249,045.5 | 268,379.3 | 289,023.9 |
| Utilidad neta | 101,339.8 | 117,282.7 | 133,893.8 | 151,314.3 | 170,354.1 |
| CFO | 284,016.2 | 298,338.0 | 324,907.2 | 352,387.6 | 381,481.1 |
| Capex | 122,673.0 | 124,243.2 | 131,076.6 | 137,630.4 | 144,511.9 |
| FCF | 161,343.2 | 174,094.8 | 193,830.6 | 214,757.2 | 236,969.1 |
| FCF despues de arrendamientos | 126,343.2 | 139,094.8 | 158,830.6 | 179,757.2 | 201,969.1 |
| Dividendos + recompras | 49,650.0 | 52,422.0 | 55,416.0 | 58,649.0 | 62,141.0 |
| Financiamiento requerido | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Caja final | 74,858.4 | 144,725.8 | 231,005.6 | 330,412.4 | 451,284.4 |
| Revolvente | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Deuda neta | 589,938.2 | 508,265.4 | 409,850.7 | 293,742.5 | 158,914.4 |

