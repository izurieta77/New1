# TSMC (TSM): notas del 20-F y del 2T26, modelo integrado, DCF inverso y sensibilidad geopolítica

> Corte: 25-sep-2026. **FASE 0 (formación): no es recomendación de compra o venta.** Los escenarios son supuestos de mecanismo, no pronósticos, guía ni consenso.
> Convención: **hecho** = cifra del documento con página; **Inferencia:** = interpretación propia; **supuesto** = entrada de escenario elegida por el analista. Montos en **millones de NT$** (un decimal, como el 20-F) salvo que se indique USD. TSMC reporta en IFRS de IASB en el 20-F y en TIFRS en los 6-K; en 2025 ingresos, utilidad bruta, utilidad de operación y flujo coinciden entre ambas bases, y los impuestos y la utilidad neta no (§3, C14).
> Archivos: `empresas/TSM/modelo/base.json` (transcripción renglón por renglón, composición de campos y supuestos), `modelo.py` (corrida y controles propios), `resultados.json` (salida completa), `SHA256SUMS.txt` y `datos/SHA256SUMS.txt` (huellas). No se editó `ficha.md`.

## 1. Fuentes leídas y congeladas

| Id | Documento | Fecha | Alcance leído |
|---|---|---|---|
| F1 | 20-F 2025, accession 0001628280-26-025362 ([SEC](https://www.sec.gov/Archives/edgar/data/1046179/000162828026025362/tsm-20251231.htm)) | 16-abr-2026 | Estados pp. F-4 a F-12; notas 15, 16, 18, 19, 22, 24, 26, 30, 31, 33, 36, 37 y 38; riesgos pp. 3-12; Item 4 pp. 16-17 y 25-26; Item 5 pp. 26-35; Item 11 pp. 71-72 |
| F2 | 20-F 2024, accession 0001193125-25-083423 ([SEC](https://www.sec.gov/Archives/edgar/data/1046179/000119312525083423/d896993d20f.htm)) | 17-abr-2025 | Balance al 31-dic-2023 pp. F-4/F-5; Nota 11 p. F-32; Nota 16 p. F-38; Nota 31 pp. F-66/F-67 |
| F3 | 6-K, comunicado y presentación del 2T26, accession 0001046179-26-000451 ([SEC](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000451/a2q26e_withguidancexfinal.htm)) | 16-jul-2026 | Comunicado completo; diapositivas 4, 7, 8, 9, 10 y 11 |
| F4 | 6-K, estados consolidados del 1S26 (TIFRS, revisión limitada), accession 0001046179-26-000541 ([SEC](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000541/a2026q2consolidatedreport-.htm)) | 14-ago-2026 | Balance p. 3; resultados pp. 4-5; flujo pp. 7-9; notas 13 (p. 20), 15 (p. 22), 20 (pp. 31-32) y 33 (pp. 53-54) |
| F5 | 6-K, estados consolidados 2025 en TIFRS, accession 0001046179-26-000024 | 26-feb-2026 | Resultados p. 7 y flujo (comparación contra IFRS) |
| F6 | 6-K, comunicado y presentación del 1T26, accession 0001046179-26-000199 | 16-abr-2026 | Diapositivas 4, 7, 8 y 10 |
| F7 | 6-K, comunicado y presentación del 4T25, accession 0001046179-26-000008 | 15-ene-2026 | Comunicado (guía de capex 2026); diapositivas 4 y 8; "Future Outlook" |
| F8 | 6-K, comunicado y presentación del 3T25, accession 0001046179-25-000116 | 16-oct-2025 | Ingresos en USD; diapositivas 4 y 8 |
| F9 | 6-K del 2T25 (comunicado, accession 0001046179-25-000082) y del 1T25 (presentación, 0001046179-25-000035) | jul-2025 / abr-2025 | Ingresos en USD del 2T25 y del 1T24 |
| F10 | Transcripción editada de la llamada del 2T26 (LSEG StreetEvents), alojada por TSMC en investor.tsmc.com | 16-jul-2026 | pp. 3-7 y 12; búsqueda de texto en las 22 páginas |
| F11 | Federal Register 2026-06851, 91 FR 17851-17852 ([govinfo](https://www.govinfo.gov/content/pkg/FR-2026-04-09/pdf/2026-06851.pdf)) | 9-abr-2026 | Documento completo (se excluye la regla de la EPA que comparte la p. 17852) |
| F12 | BIS, guía del 31-may-2026 sobre entidades con sede en el grupo D:5 y Macao ([bis.gov](https://www.bis.gov/media/documents/bis-guidance-may-31-2026.pdf)) | 31-may-2026 | Documento completo (1 página) |
| F13 | Yahoo Finance chart v8: TSM, 2330.TW y TWD=X | cierre del 24-sep-2026 | TSM 451.15 USD; 2330.TW 2,475 NT$; 31.7895 NT$/USD |
| F14 | Damodaran, *Betas by Sector (US)*, ene-2026 | ene-2026 | Semiconductor (66 empresas): beta desapalancada corregida por caja de 1.50 |
| F15 | Damodaran, *Country Default Spreads and Risk Premiums* ("Last updated: January 5, 2026") | 5-ene-2026 | Taiwán: Aa3, diferencial 0.51%, prima de riesgo país 0.78%, tasa corporativa 20% |
| F16 | `conocimiento/03` §2.3 (hoja de Damodaran de sep-2026) | sep-2026 | T-bond de 4.75% y ERP de 4.09% |

**Acceso.** `data.sec.gov` respondió con el User-Agent `SistemaInversionNew1/1.0 investigacion`; `www.sec.gov/Archives` respondió 403 con ese mismo agente y funcionó al agregarle un contacto de marcador no enrutable (igual que en NVDA). El sitio de relación con inversionistas de TSMC bloquea `curl` (desafío de Cloudflare); la transcripción F10 se obtuvo con WebFetch y se leyó localmente. `companyfacts` todavía no incluye el 20-F 2025 (su último 20-F es el de 2024), así que la comprobación XBRL de F1 se hizo con su propio iXBRL.

**Congelamiento.** Los insumos pequeños y de dominio público (JSON de Yahoo, extracto de Damodaran, F11 y F12) están en `modelo/datos/` con manifiesto creado por `herramientas/huellas.py crear` (verificado con `huellas.py verificar`: OK). Los documentos grandes o con derechos de terceros solo se hashean; la huella está en `base.json → fuentes.F*.sha256`. En los HTML de la SEC el hash se calcula sin la etiqueta `<script>` que agrega el CDN; el tamaño resultante coincide byte a byte con el `index.json` de EDGAR (por ejemplo, 10,355,816 bytes para F1).

```
c3ebd05cd8fb383f53fc21a0ac497ee12cf908b709c380f9bec4f39c4916647b  tsm-20251231.htm               (F1)
8239f280b4e9b70fedddd536db181f6ea96fd898ceb2b93cacd730c6aaae2c1e  d896993d20f.htm                (F2)
6e877956870c87d857d8af23144f35ddcbd3b569d464c962e7cf368c46860be3  a2q26e_withguidancexfinal.htm  (F3)
939d51f10b81ee70e87864e3fa0f93b7eb0a9e4868d6a226b6bd284d407583af  a2q26presentatione.htm         (F3, presentación)
f421f6fe7b0c14ba15969f57749effdd54a04342cbfff49ef1fadf128f495251  a2026q2consolidatedreport-.htm (F4)
43a740eb791fb01939cc4e47886d9f2d4171155f285c87f6a55d3c3f9c747393  a2025q4consolidatedreport-.htm (F5)
38894a5f4e753a6b17e451671419f21dd0e05ba0a39e6700e368dc99f1344a3f  a1q26e_withguidancexfinal.htm  (F6)
182ec7f50f514c1c6e1f396febaef2589ee735f3e7c400356c6c56591a9d745b  a4q25e_withguidancexfinal.htm  (F7)
37c3e6006cbbcf2374d178f2cee25ac10fbcae30b40c5976f93f5c23b30ea634  a4q25presentatione.htm         (F7, presentación)
f0748d8cb463ad4fb2c1808b3e001927425cae06601eeb2cd37811413f2309a5  a3q25e_withguidancexfinal.htm  (F8)
17947a4c33c3ef2153641706eef7051422ab8594251dfbb64646b92d9a4cc915  tsmc_2q26_transcript.pdf       (F10; no se versiona)
0666f438edf78fa65402c84cc2a3fe6ca162a042924d82117744959c18605999  fr_2026-06851.pdf              (F11; en datos/)
d7296438740efad835badddb5daa6cfd8d3a43bb62fedbf5a7a817c79828610b  bis_guidance_2026-05-31.pdf    (F12; en datos/)
10993bab71504e2449ccdd9e3d67fa4da983bed380b2f4486e5200a7b258616b  Betas.html                     (F14; igual a NVDA F7)
ea30d57fc0858072c520930e2e5b8a5e5affdce81f7f2e1f9054efab79959dbc  ctryprem.html                  (F15)
```

## 2. Hallazgos de las notas

### 2.1 Capex, compromisos y cómo se financia la expansión
**Hechos:**
- Capex (compra de PPE): 949,817 en 2023, 956,007 en 2024 y 1,272,411 en 2025 (US$40,895 M al promedio de 31.11 NT$/USD). Se financió con flujo de operación y bonos (F1 p. 16).
- **Guía de capex 2026:** US$52-56 mil M en ene-2026 (F7 comunicado; F1 p. 16). El 16-jul-2026 se **elevó a US$60-64 mil M**: 70%-80% a procesos avanzados, ~10% a especialidades y 10%-20% a empaquetado avanzado, pruebas y máscaras (F10 p. 4). Capex del 2T26: US$15.7 mil M (F10 p. 3). En el 1S26 la compra de PPE fue de 846,764.7 (F4 p. 8).
- "El capex de los próximos tres años será **aún más significativamente** mayor que el de los tres anteriores" (F10 p. 7). Anuncio de **US$100 mil M adicionales en Arizona** (total de US$265 mil M; calendario "según el mercado") y de 13 fábricas de vanguardia y empaquetado en Taiwán "en los próximos años" (F10 pp. 5 y 7). Tres fábricas adicionales de 3 nm: Taiwán, Arizona y Japón (F10 p. 6).
- **Compromisos al 31-dic-2025** (F1 p. 34): compras de capital y otras por **1,534,575** (1,220,393 a menos de un año); deuda de largo plazo con intereses por 1,229,859; arrendamientos por 39,470; y **anticipos temporales de clientes** por 189,858 (146,559 a menos de un año).
- **Anticipos de clientes** ("temporary receipts", pagos para reservar capacidad; se reembolsan o se compensan contra cuentas por cobrar de mutuo acuerdo): 189,858.2 al 31-dic-2025 y **234,225.1 al 30-jun-2026**; la porción no circulante pasó de 43,298.9 a 92,372.0 (F1 p. 17; F4 p. 32).
- **Subsidios:** 47,545.9, 75,164.3 y 76,258.8 cobrados en 2023-2025 por TSMC Arizona, ESMC, JASM y TSMC Nanjing, y TSMC Arizona puede solicitar un crédito de inversión de 25% (F1 Nota 30 p. F-67). La Ley CHIPS otorga hasta US$6.6 mil M directos y hasta US$5 mil M en préstamos, con garantía de TSMC; ESMC tiene hasta 5 mil M de euros de ayuda estatal alemana (F1 pp. 7 y 25). En el 1S26 se cobraron **590.4** de subsidios para PPE, contra 67,128.2 en el 1S25 (F4 p. 8).

*Inferencia (cálculo propio):*
- Los compromisos de compra equivalen a 1.21 veces el capex de 2025, y los de menos de un año, a 0.96 veces. El capex de 2026 está en buena parte contratado; por eso el escenario de tensión mantiene el capex alto en 2027 aunque caigan los ingresos (§5).
- La guía de US$60-64 mil M equivale a 1.91-2.04 billones de NT$ al tipo de cambio de 31.79: **43%-46% de los ingresos de 12 meses** (4,440,492.5). En el 2S26 implica US$33-37 mil M, contra ≈US$26.8 mil M del 1S (1T26 convertido al tipo de cambio promedio de 31.59, F6 diap. 4; 2T26 de US$15.7 mil M, F10 p. 3).
- El CFO del 1S26 incluye un aumento de 102,502.2 en "otros pasivos no circulantes" (F4 p. 7), en el que están los anticipos de clientes. Parte del FCF reciente depende de que los clientes sigan prepagando capacidad.
- Los subsidios son irregulares (590 contra 67,128 en semestres comparables). El modelo proyecta el capex bruto sin subsidios; es un supuesto conservador.

### 2.2 Fábricas en el extranjero y dilución de margen: consolidado contra incremental
**Hechos:**
- **Arizona (Fab 21):** la primera fábrica entró en volumen a fines de 2024, la segunda está en construcción y la tercera empezó en 2025; en 2026 se compró más terreno (F1 p. 25). **JASM (Kumamoto):** volumen desde dic-2024 y construcción de la segunda planta desde oct-2025; TSMC tiene 72.6%. **ESMC (Dresde):** construcción desde 2024; TSMC tiene 70.0% (F1 pp. 25-26).
- **Activos no circulantes por país** (F1 Nota 38 p. F-82): Taiwán 3,102,343.0 (**80.0%** del total de 3,876,339.8), EUA 540,057.4 (13.9%), Japón 117,403.2 (3.0%), China 65,019.9 (1.7%) y EMEA 51,515.1 (1.3%). En 2024 Taiwán era 77.2% (2,613,112.2 de 3,383,106.4).
- **Dilución comunicada** (F10 p. 4): la de las fábricas en el extranjero se estima en **2-3 pp en la etapa temprana y se amplía a 3-4 pp en la etapa posterior**, "en los próximos años". Aparte, la rampa de **N2 diluye 3-4 pp en el 2S26**. El margen bruto del 2T26 subió 1.5 pp, a 67.7%, "parcialmente compensado por la dilución de las fábricas en el extranjero" (F10 p. 3); es decir, **esa dilución ya está dentro del margen consolidado**. La guía del 3T26 es de 65%-67% (F3).
- Objetivos de la administración (ene-2026): margen bruto de largo plazo de **56% o más** a lo largo del ciclo, CAGR de ingresos en USD 2024-2029 de "cerca de 25%" y ROE "high-20s" (F7 "Future Outlook").
- El 20-F solo habla de "mayores costos" de construir fábricas nuevas y de la pérdida de sinergias del ecosistema de Taiwán (F1 p. 5); no cuantifica la dilución.

*Inferencia (cómo se evita el doble conteo):*
- El margen consolidado del 1S26 (67.02%; F4 p. 4) ya incluye la etapa temprana (2-3 pp). Lo único que falta por restar es el **paso de 2-3 pp a 3-4 pp: entre 0 y 2 pp (1 pp en los puntos medios)**. Restar al margen consolidado el rango completo de 2-4 pp contaría dos veces la dilución.
- N2 es un mecanismo distinto: es temporal y la empresa lo reporta por separado. Sumarlo automáticamente a la dilución del extranjero también puede duplicar costos (una fábrica N2 en Arizona entra en ambos).
- Por eso el modelo usa un **puente explícito** (`base.json → insumos_complementarios.puente_margen_bruto`): margen bruto = ancla de 67.0% − N2 y nodos nuevos − **incremental del extranjero (limitado a 0-2 pp)** − tipo de cambio + utilización, precio y costo. El control **P01** verifica en los 15 años-escenario que el supuesto coincide con el puente y que el componente del extranjero nunca pasa de 2 pp (§4).
- En 2025 la participación de Taiwán en los activos no circulantes **subió** (77.2% → 80.0%), mientras la de EUA bajó en NT$ (541,836.3 → 540,057.4; el dólar se depreció frente al NT$). Medida en activos, la diversificación no avanzó en 2025. El 20-F no desglosa la capacidad calificada por país.

### 2.3 Controles de exportación y aranceles
**Hechos:**
- **20-F:** las "October Rules" de 2022 y 2023; en ene-2025, reglas que pueden exigir licencia antes de enviar productos de **16 nm o menos** a destinos especificados, salvo que se cumplan ciertas condiciones. La autorización VEU de Nanjing venció en dic-2025 y fue sustituida por una **licencia anual**. Al 16-abr-2026, los resultados "no han sido afectados materialmente" (F1 p. 4). La fábrica en China requiere licencias para adquirir ciertas herramientas (F1 p. 5). En oct-2024 TSMC notificó a EUA y a Taiwán que un chip de un cliente pudo haberse desviado a una entidad restringida; coopera con las autoridades y advierte que su visibilidad sobre el uso final es limitada (F1 p. 12).
- **FR 2026-06851** (F11, leído completo): regla final del BIS publicada el 9-abr-2026 y **vigente desde el 7-abr-2026**. En la Nota 1 al ECCN 3A090.a, párrafos a.(2) y a.(3), sustituye la fecha del 13-abr-2026 por el **31-dic-2026**, tanto para el estatus de diseñador de CI autorizado como para el plazo para solicitar ser diseñador aprobado. El antecedente es la regla interina del 16-ene-2025 (90 FR 5298), que creó **presunciones para "front-end fabricators" y empresas OSAT** que exportan "applicable advanced logic ICs" bajo 3A090.a, superables vía diseñadores aprobados, OSAT aprobadas o diseñadores autorizados. El BIS estima 20 diseñadores aprobados adicionales por la extensión.
- **Guía del BIS del 31-may-2026** (F12, leída completa): aclara que **sigue vigente** la licencia exigida desde el 17-nov-2023 para artículos de cómputo avanzado (3A090.a y .b, 4A090.a y .b, y los .z relacionados) destinados a entidades con sede, o con matriz última, en el grupo D:5 o Macao, **aunque estén ubicadas fuera** de esos destinos (§742.6(a)(6)(iii)(A)). La política de no aplicación de la AI Diffusion Rule (may-2025) no cubre esos casos. Los operadores de centros de datos de buena fe no tienen que dejar de usar lo que ya tienen.
- **Aranceles** (F1 p. 3): la Suprema Corte anuló en feb-2026 los aranceles recíprocos basados en IEEPA, y EUA impuso uno de reemplazo con la Sección 122. En mar-2026 la USTR abrió dos investigaciones de la Sección 301 que incluyen a Taiwán. La Sección 232 terminó en dic-2025 con un **arancel de 25% a ciertos chips de cómputo avanzado**, salvo los importados para uso designado en EUA. El acuerdo EUA-Taiwán de ene-2026 limita el arancel recíproco a 15% y da trato preferente en la 232 a los productores taiwaneses que invierten en EUA.
- **China por sede del cliente:** 12% de los ingresos en 2023, 11% en 2024 y 9% en 2025 (327,503; F1 p. 17). En el 1S26 fue 6.8% (162,572.4) y en el 2T26 6.0% (76,730.5) (F4 p. 31).
- En las 22 páginas de la transcripción del 2T26 no aparecen las palabras "export", "tariff" ni "China" (búsqueda de texto en F10).

*Inferencia:*
- TSMC es un "front-end fabricator". FR 2026-06851 **aplaza, no elimina**, la fecha a partir de la cual la presunción sobre sus envíos de lógica avanzada solo se supera con diseñadores aprobados o autorizados. El punto a vigilar es el 31-dic-2026.
- La guía del 31-may-2026 cierra la ruta de filiales fuera de China de clientes con matriz en D:5. El efecto sobre TSMC pasa por lo que puedan comprar esos clientes, no por su propia licencia. Con 6.0%-6.8% de ingresos de clientes con sede en China (que incluyen nodos maduros no controlados), el filing no permite estimar qué fracción está sujeta. Esa fracción se trata como supuesto en §7.
- Que la llamada no mencione controles ni aranceles no prueba que el riesgo sea bajo (el cap. 23 §6 sugiere contar esas menciones). Registra que la administración no los trató como tema del trimestre.

### 2.4 Concentración de clientes
**Hechos:**
- Los diez mayores clientes fueron 70%, 76% y **78%** de los ingresos en 2023, 2024 y 2025. El mayor, 25%, 22% y 19%; el segundo, 11%, 12% y 17% (F1 p. 8).
- Nota 38: en 2025, el **cliente A** sumó 726,974.3 (19%) y el **cliente B** 645,178.7 (17%). En 2024, B fue 22% y A 12%. En 2023, B fue 25% y C 11% (F1 p. F-82).
- Cuentas por cobrar: los diez mayores clientes concentraban 93% al cierre de 2024 y 84% al cierre de 2025 (F1 Nota 33 p. F-71).
- Por sede, Norteamérica fue 75% de 2025 (2,875,270) y EUA 75.6% del 1S26 (F1 p. 17; F4 p. 31). Por plataforma, HPC fue 58% de 2025, 63.4% del 1S26 y 66% del 2T26 (F1 p. 19; F4 p. 31; F10 p. 3).

*Inferencia:*
- El liderazgo cambió en 2025: A pasó de 12% a 19% y superó a B, que bajó de 25% (2023) a 17%. Es coherente con el peso creciente de HPC. El filing no nombra a los clientes; atribuirles identidad sería especulación.
- La concentración de ingresos subió (70% → 78% en los diez mayores), pero la de cobranza bajó (93% → 84%).

### 2.5 Tipo de cambio
**Hechos:**
- Casi todas las ventas están en USD, y más de la mitad del capex está en otras monedas (USD, euros y yenes) (F1 pp. 11 y 71).
- **Cada 1% de depreciación del USD frente al NT$ reduce ~0.3 pp el margen operativo** (base 2025; F1 p. 11).
- Un choque cambiario adverso de 10% sobre los activos y pasivos monetarios, neto de coberturas, reduciría la utilidad neta en 1,987 (F1 p. 72).
- Tipo de cambio promedio: 31.11 en 2025 (F1 p. 16), 29.91 en el 3T25 (F8 diap. 4) y 31.60 en el 2T26 (F3 diap. 4). La guía del 3T26 supone 32 (F3). El 24-sep-2026 cerró en 31.79 (F13).
- El margen bruto de 2025 subió a 59.9% por utilización y costos, "parcialmente compensado por un tipo de cambio desfavorable" (F1 p. 31).

*Inferencia:*
- Con la regla de 0.3 pp por 1%, pasar de 32 (supuesto de la guía) a 30 NT$/USD cuesta ~1.9 pp de margen operativo. En el escenario de tensión se usa 1.5 pp (desde 31.6).
- El riesgo cambiario está en el margen, no en el balance: la sensibilidad monetaria es pequeña (1,987 contra 1.7 billones de utilidad).

### 2.6 Otros hallazgos que afectan la lectura del modelo
- **IFRS contra TIFRS.** En 2025 el impuesto IFRS fue de 346,529.8 y el TIFRS de 326,266.1. La utilidad neta fue de 1,695,124.9 en IFRS y de 1,715,396.8 en TIFRS; en 2024, de 1,157,523.9 y 1,172,431.8 (F1 p. F-6; F5 p. 7). La Nota 26 IFRS incluye 64,394.7 de "impuesto adicional sobre utilidades no distribuidas" en 2025 y −56,886.1 de ajustes de años previos (F1 pp. F-59/F-60). *Inferencia:* la diferencia es sobre todo de **momento de reconocimiento** de ese impuesto. La utilidad neta de los 6-K (TIFRS) no es comparable con la del 20-F sin este ajuste; el modelo lo prueba con C14.
- **Ganancia de VIS.** En may-2026 TSMC vendió 152 M de acciones de Vanguard, bajó a 19% y perdió influencia significativa. Reconoció una ganancia de **63,202.3**, que incluye la revaluación no monetaria de la participación restante a valor razonable (56,398.8) (F4 p. 20). Aportó 2.24 NT$ a la UPA del 2T26 (F10 p. 3) y equivale a 4.1% de la UAI del 1S26. Los escenarios no la incluyen (`otros_ingresos` = 0).
- **Impuestos.** La tasa corporativa en la R.O.C. es de 20%, con créditos de 25% sobre I+D y 5% sobre equipo avanzado (F1 p. 35). La tasa efectiva IFRS fue de 13.1%, 17.7% y 17.0% en 2023-2025 (F1 p. F-6).
- **Deuda.** Deuda de largo plazo de 1,032,988 (136,926 circulante), con tasas fijas de 0.41%-4.63% y vencimientos de hasta 35 años; sin préstamos de corto plazo (F1 p. 34). Tasa implícita sobre deuda y arrendamientos promedio: 1.17% en 2025 (C10, INFO). Los costos financieros son netos de intereses capitalizados (7,615.9 en 2025; F1 p. F-68).
- **Dividendos.** 467 mil M de NT$ pagados en 2025 (NT$18 por acción); en 2026, NT$24 por acción (+33%), y la administración espera que sigan subiendo en 2027 (F10 p. 4).

### 2.7 Contraste con el material recibido ("Maquiavelo, tanda 2", módulo TSMC)
Se volvió a leer cada fuente primaria citada en ese módulo en lugar de copiar sus cifras.
- **Confirmado contra el documento:**
  - las cifras del 2T26: US$40.20 mil M, margen bruto de 67.7%, guía del 3T de US$44.6-45.8 mil M con margen de 65%-67% y tipo de cambio de 32 (F3);
  - la dilución del extranjero de 2-3 pp → 3-4 pp y la de N2 tratada por separado (F10 p. 4);
  - el capex de US$60-64 mil M y los US$100 mil M adicionales en Arizona (F10 pp. 4-5);
  - el contenido de FR 2026-06851 y de la guía del BIS (F11, F12);
  - los datos trimestrales del 2T26: 1,270.38, 706.56, 783.36, 496.00 y 27.25 (F3).
- **Corrección de método:** esa rejilla usa una "presión adicional" d ∈ {2, 3, 4} pp sobre el margen reportado de 67.7%. El texto aclara que d es incremental e hipotética, pero **esos valores coinciden con el rango total comunicado**, y el margen de 67.7% ya incluye la dilución temprana (F10 p. 3). Si d es incremental, el rango coherente con la guía es 0-2 pp. En §7, d ∈ {0, 1, 2} pp, y `resultados.json` cuantifica cuánto se sobreestimaría cada celda si d se leyera como dilución total: entre 79,929 y 88,810 de utilidad bruta de 12 meses.
- **Diferencia de escala:** allá se usa un trimestre en USD con margen redondeado. Aquí se usan 12 meses en NT$ (IFRS/TIFRS, idénticos en ingresos y utilidad bruta).

## 3. Base histórica y doble comprobación de la transcripción

La base cubre tres ejercicios: FY2023 (balance de F2; resultados, flujo y capital de F1) y FY2024-FY2025 (F1). `base.json → transcripcion` guarda **cada renglón** de los estados tal como está impreso (en inglés), con su página. `base.json → composicion` declara, por campo del motor, qué renglones suma y con qué signo. `modelo.py` rehace esas sumas (T01). Decisiones de mapeo:
- **`deuda`** = bonos + préstamos bancarios (incluida la porción circulante) + préstamos bancarios designados como cobertura de inversión neta. Estos últimos sumaban 27,290.4 al cierre de 2023, están en "Hedging financial liabilities" y se pagaron en 2024 (F2 Nota 11 p. F-32; Nota 31 pp. F-66/F-67).
- **`arrendamientos_financieros`** = pasivo IFRS 16 total. La porción circulante (3,833.0 en 2025) está dentro de "Accrued expenses and other current liabilities" y se reubica (F1 Nota 16 p. F-38).
- **`capex`** = compra de PPE, que es la definición de capex de TSMC. Con ella, el FCF del emisor (CFO − capex) de 2025 coincide con la suma de los cuatro trimestres publicados: **C12 es prueba real** (diferencia de 4.9 por redondeo). Los intangibles (10,146.9) van a `otros_inversion`.
- **Flujo IFRS:** parte de la UAI, clasifica los intereses pagados en financiamiento y los cobrados en inversión. El motor parte de la utilidad neta, así que el impuesto del periodo, los ajustes no monetarios, los demás cambios operativos y los impuestos pagados quedan en `otros_operativos` como detalle renglón por renglón. Con eso **C07 (utilidad → CFO) es prueba real** en los tres años.
- **Capital:** `movimientos_capital` sale del estado de variaciones (columnas Total Equity y utilidades retenidas; F1 pp. F-8/F-9). Los aportes de minoritarios se toman de los renglones de variaciones en no controladoras. **C03 y C04 son pruebas reales** en los tres años. En C04 se agrega la pérdida de la participación no controladora, porque las utilidades retenidas usan la utilidad de la controladora.
- **PPE (C05):** se usa la Nota 15 (adiciones, depreciación, bajas, reclasificaciones, deterioro, tipo de cambio y activos arrendados a terceros). Es prueba real en 2024 y 2025; en 2023 queda NO_APLICA porque falta el saldo inicial de los activos arrendados a terceros.
- **Deuda (C06):** es prueba real en 2023 y 2024 con la conciliación de pasivos de F2. En 2025 queda INFO: F1 solo concilia los bonos (flujo 32,499.7, tipo de cambio −24,602.7 y otros 384.0; p. F-68), y en los préstamos bancarios queda un movimiento no monetario de −1,528.5 que no está documentado (*inferencia:* efecto del yen sobre 39,253.5 de préstamos en JPY, Nota 19 p. F-46).

**Doble comprobación.** Se hizo con scripts de trabajo que no forman parte del repositorio; sus resultados se registran aquí. Las pruebas T01, T02 y T03 sí viven en `modelo.py` y se repiten en cada corrida.

| Prueba | Contra qué | Resultado |
|---|---|---|
| (A) Hechos XBRL | iXBRL de F1 (2024-2025 y flujos, resultados y capital de 2023) e instancia XBRL de F2 (balance de 2023): mismo periodo, valor absoluto | **482 de 482** renglones coinciden. 461 coinciden de forma directa con hechos sin dimensión. Los otros 21 están explicados: 6 saldos de caja inicial y final son hechos de instante; 7 renglones del balance de 2023 usan etiquetas propias de TSMC que no están en `companyfacts` y se verificaron en la instancia de F2; 5 valores de la columna de utilidades retenidas son hechos con dimensión; y 3 sumas de aportes de minoritarios se verificaron por componente |
| (A2) Balance 2024 en F1 contra F2 | Instancia XBRL de F2 | 53 de 53 renglones iguales: no hubo reexpresión |
| (A3) Notas | Nota 15, notas 16 y 19, conciliación de F2 | 48 de 50 valores directos; los 2 restantes (total de préstamos 2024 y 2025) son sumas probadas en T02 |
| (B) T01: composición de los campos del motor | `base.json → transcripcion` | 144 comparaciones, 0 fallas (incluye el detalle renglón por renglón de `otros_operativos`, `otros_inversion`, `otros_financiamiento` y `cambio_capital_trabajo`) |
| (C) T02: aritmética de los estados transcritos | Subtotales, totales, caja, capital y notas de deuda | 97 comparaciones, 0 fallas |
| (D) Insumos de 12 meses y del DCF | Diapositivas de FCF trimestral y JSON de precios congelados | T03: FCF del emisor de 12 meses (1,143,556.3) contra la suma de los trimestres (1,143,550), diferencia de 6.3 por redondeo. D01: los tres precios coinciden con `datos/` |

Límite: las pruebas comparan contra datos del mismo emisor (sus estados y su XBRL) y las ejecutó el mismo autor. Es una doble extracción, no una auditoría independiente.

**Métricas históricas** (cálculo sobre hechos; `resultados.json → historico.drivers_implicitos`):

| Concepto | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|
| Ingresos | 2,161,735.8 | 2,894,307.7 | 3,809,054.3 |
| Crecimiento | n.d. | 33.9% | 31.6% |
| Margen bruto | 54.4% | 56.1% | 59.9% |
| Margen operativo | 42.6% | 45.7% | 50.8% |
| Tasa efectiva (IFRS) | 13.1% | 17.7% | 17.0% |
| Utilidad neta | 851,027.7 | 1,157,523.9 | 1,695,124.9 |
| CFO | 1,241,967.3 | 1,826,177.1 | 2,274,975.6 |
| Capex (PPE) | 949,816.8 | 956,006.5 | 1,272,410.5 |
| Capex / ingresos | 43.9% | 33.0% | 33.4% |
| FCF del emisor (CFO − capex) | 292,150.5 | 870,170.6 | 1,002,565.1 |
| FCF / utilidad neta | 0.34 | 0.75 | 0.59 |
| D&A / ingresos | 24.6% | 22.9% | 18.1% |
| DSO / DIO / DPO (días) | 34.1 / 92.9 / 21.2 | 34.3 / 82.7 / 21.3 | 27.0 / 68.8 / 20.1 |
| Dividendos pagados | 291,721.9 | 363,055.2 | 466,779.2 |
| Caja + valores circulantes | 1,687,644.4 | 2,422,019.7 | 3,068,594.8 |
| Deuda financiera + arrendamientos | 986,358.9 | 1,050,091.1 | 1,068,415.7 |

**12 meses a jun-2026** (2025 − 1S25 + 1S26; `resultados.json → ttm`):
- Ingresos de **4,440,492.5** (US$142.93 mil M: 33.10 + 33.73 + 35.90 + 40.20; F8, F7, F6, F3).
- Margen bruto de 64.23% y margen operativo de 56.10%.
- CFO de 2,634,679.0 (59.3% de los ingresos) y capex de PPE e intangibles de 1,500,529.5 (33.8%).
- FCF de 1,134,149.5 (25.5%).

## 4. Modelo integrado: controles y reconciliación

`python3 empresas/TSM/modelo/modelo.py` sale con código 0.
- El motor produjo **540 registros: 521 OK, 0 FALLA, 16 INFO y 3 NO_APLICA**.
- `modelo.py` relee `resultados.json` y recalcula todos los controles con `mi.verificar`. El resultado coincide: 540 registros y 0 FALLA.
- Los controles propios suman **291 registros y 0 FALLA**: T01 144, T02 97, T03 1, P01 45, D01 3 y G01 1.

| Id | Control | OK | FALLA | INFO | NO_APLICA |
|---|---|---|---|---|---|
| C01 | Balance: activo = pasivo + capital (y totales = suma de componentes) | 54 | 0 | 0 | 0 |
| C02 | Caja: inicial + CFO + CFI + CFF + efecto cambiario = final (y sumas de CFI y CFF) | 59 | 0 | 0 | 0 |
| C03 | Capital: roll-forward con ORI | 18 | 0 | 0 | 0 |
| C04 | Utilidades retenidas: roll-forward | 18 | 0 | 0 | 0 |
| C05 | PPE: inicial + capex + nuevos arrendamientos − depreciación + otros = final | 17 | 0 | 0 | 1 |
| C06 | Deuda, arrendamientos y revolvente | 47 | 0 | 3 | 0 |
| C07 | Puente utilidad → CFO | 36 | 0 | 0 | 0 |
| C08 | Cuentas por cobrar = días × ingresos / 365 | 15 | 0 | 3 | 0 |
| C09 | Inventario y proveedores = días × costo de ventas / 365 | 30 | 0 | 3 | 0 |
| C10 | Intereses = tasa × saldo promedio; ingreso financiero = tasa × caja promedio | 30 | 0 | 2 | 1 |
| C11 | Impuestos = tasa × UAI | 15 | 0 | 3 | 0 |
| C12 | FCF = CFO − capex; FCF después de principal | 31 | 0 | 2 | 0 |
| C13 | Reconciliación del histórico con drivers implícitos | 2 | 0 | 0 | 1 |
| C14 | IFRS + diferencias = TIFRS (utilidad neta) | 2 | 0 | 0 | 0 |
| C15 | Aritmética del estado de resultados | 87 | 0 | 0 | 0 |
| C16 | Caja mínima y revolvente, sin plug | 60 | 0 | 0 | 0 |

**Los INFO y NO_APLICA dicen qué falta:**
- **FY2023 sin apertura completa:** no hay saldo inicial de activos arrendados a terceros (C05), de deuda para la tasa implícita (C10) ni balance de apertura para C13.
- **C06 INFO:** en 2025, el movimiento no monetario de los préstamos bancarios no está documentado (§3). En 2024 y 2025 no se cargó un roll-forward del pasivo por arrendamiento (el de 2025 no está publicado).
- **C12 INFO en 2023 y 2024:** no se reunieron los FCF trimestrales de 2023-2024. En 2025 es prueba real.
- **C08-C11:** por diseño, son INFO en el histórico.

**C13, reconciliación.** El mismo motor reproduce FY2024 y FY2025 con una diferencia máxima de 0.0000 (tolerancias de 28.9 y 38.1). Lo que no explica aparece con nombre. Las partidas materiales (más de 2% de los ingresos) de FY2025 son:

| Partida (FY2025) | Monto | % ingresos | Lectura |
|---|---:|---:|---|
| otros_ingresos | 117,933.4 | 3.1% | Hecho: intereses (105,739.1) + asociadas (5,488.5) + otros (591.7) + tipo de cambio (13,831.3) + otras pérdidas (−7,717.2) |
| otros_operativos | −109,651.4 | −2.9% | Hecho: cambios en otros activos y pasivos de operación e impuestos pagados menos el impuesto del periodo (detalle en `base.json`) |
| otros_inversion | 128,017.1 | 3.4% | Hecho: intereses cobrados (98,954.7), subsidios (76,258.8), compras netas de valores (−36,855.8 = −66,823.2 − 188,288.6 + 80,052.3 + 138,203.7), intangibles (−10,146.9) y otros |
| no monetario en ppe_neto | −134,573.5 | −3.5% | Explicado: adiciones contables de 1,160,977.7 contra 1,272,410.5 pagados (−111,432.8: subsidios por cobrar, pasivos con proveedores de equipo e intereses capitalizados, F1 Nota 31 pp. F-67/F-68), + 12,727.4 de D&A que no reduce PPE (amortización y derecho de uso), − 7,120.2 de arrendamientos que el motor manda a PPE y − 28,747.9 de bajas, reclasificaciones, deterioro y tipo de cambio (Nota 15) |
| no monetario en otros_activos_lp / otros_pasivos | 183,455.4 / 125,802.6 / 98,453.4 | 4.8% / 3.3% / 2.6% | Reubicaciones del mapeo genérico: el motor mantiene constantes esas líneas y manda los flujos "otros" a una sola línea |
| capital: diferencias devengado contra pagado | −120,939.6 | −3.2% | Hecho: dividendos declarados (531,618.4) contra pagados (466,779.2) = −64,839.2, más ORI de −56,326.5 y otros |

*Inferencia:* como en NVDA, las partidas grandes son sobre todo reubicaciones del mapeo genérico (el motor mantiene constantes otros activos y pasivos), no flujo sin explicar. Lo genuinamente no monetario es identificable: el tipo de cambio sobre bonos y PPE, los subsidios por cobrar, los intereses capitalizados, el ORI y los dividendos declarados y no pagados.

## 5. Escenarios de mecanismo (supuestos, no pronósticos)

**Diseño común** (supuestos, con su ancla):
- **Horizonte y caja:** 5 años (2026E-2030E). Caja mínima de 1.5 billones de NT$ (≈ caja de 1,465,427.8 al cierre de 2023).
- **Política de capital idéntica** en los tres escenarios, para aislar el mecanismo operativo:
  - dividendos pagados de NT$24 por acción en 2026 (F10 p. 4) y +NT$4 por año después (supuesto), sobre 25,932 M de acciones (F3 diap. 7): de 622,368 a 1,037,280;
  - sin recompras, con deuda constante y con arrendamientos de saldo constante (4,000 nuevos = 4,000 de principal).
- **Resultados financieros e impuestos:**
  - tasa de interés de 1.2% (implícita de 2025: 1.17%);
  - rendimiento de la caja de 3.0% (implícito de 2025: 3.85% sobre caja y valores circulantes);
  - tasa de impuestos de 17.5% (IFRS: 17.0% en 2025 y 17.7% en 2024);
  - otros ingresos de 0 (se excluye la ganancia de VIS).
- **D&A** = 20.5% del PPE inicial más 0.22% de los ingresos por amortización. Anclas: la depreciación fue 21.3% y 21.0% del PPE inicial en 2024 y 2025, y 19.5% anualizada en el 1S26.
- **Capex** = compra de PPE; no se restan subsidios.

| Driver | Tensión | Intermedio | Eficiencia |
|---|---|---|---|
| Crecimiento de ingresos (NT$) 2026E-2030E | +34.5% (2S en el extremo bajo de la guía del 3T, 4T = 3T, NT$ a 30.5), −8%, −12%, +5%, +6% | +44.2% (3T en el punto medio, año ≈ +40% en USD a 32), +20%, +12%, +8%, +6% | +46.1% (extremo alto), +28%, +18%, +12%, +8% |
| Margen bruto | 63.75% → 55.6% → 51.5% → 53% → 55% | 66% → 64.25% → 63.5% → 63% → 62.5% | 66.5% → 66.75% → 67% |
| Gasto operativo neto / ingresos | 8.6% → 11.0% (2028) → 10.5% | 8.3% → 8.0% | 8.0% → 7.2% |
| Capex / ingresos | 36.4%, 40%, 31%, 27.5%, 28% | 36.1%, 34%, 32%, 30%, 28% | 36.5%, 33%, 30%, 28%, 27% |
| DSO / DIO / DPO (días) | 34→38→33 / 90→100→88 / 22→20→22 | 30→29 / 85→75 / 24→23 | 28→27 / 80→70 / 25→24 |

**Puente del margen bruto** (pp; ancla de 67.0% = margen consolidado del 1S26, que ya incluye la dilución temprana del extranjero; P01 lo verifica):

| Escenario | Año | N2 y nodos nuevos | Extranjero **incremental** (0-2) | Tipo de cambio | Utilización, precio y costo | Margen bruto |
|---|---|---:|---:|---:|---:|---:|
| Tensión | 2026E / 2027E / 2028E / 2029E / 2030E | 1.75 / 2.5 / 1.5 / 1.5 / 0.5 | 0.25 / 1.0 / 1.5 / 2.0 / 2.0 | 0.75 / 1.5 / 1.5 / 1.5 / 1.5 | −0.5 / −6.4 / −11.0 / −9.0 / −8.0 | 63.75 / 55.6 / 51.5 / 53.0 / 55.0 |
| Intermedio | ídem | 1.75 / 2.0 / 1.5 / 1.0 / 0.5 | 0.25 / 0.75 / 1.0 / 1.0 / 1.0 | 0 | +1.0 / 0 / −1.0 / −2.0 / −3.0 | 66.0 / 64.25 / 63.5 / 63.0 / 62.5 |
| Eficiencia | ídem | 1.5 / 1.5 / 1.0 / 0.5 / 0 | 0 / 0.25 / 0.5 / 0.5 / 0.5 | 0 | +1.0 / +1.5 / +1.5 / +1.0 / +0.5 | 66.5 / 66.75 / 67.0 / 67.0 / 67.0 |

Anclas de los supuestos (hechos):
- guía del 3T26 (F3);
- crecimiento de 2026 "ligeramente arriba de 40%" en USD (F3 diap. 10; F10 p. 5), después de "cerca de 30%" en ene-2026 y "arriba de 30%" en abr-2026 (F7, F6);
- capex de US$60-64 mil M (F10 p. 4);
- N2 de 3-4 pp en el 2S26 y extranjero de 2-3 → 3-4 pp (F10 p. 4);
- A14 en volumen desde 2028 (F10 p. 6);
- 0.3 pp de margen por cada 1% de tipo de cambio (F1 p. 11);
- margen bruto de 54.4% en 2023, el último año débil (F1 p. F-6);
- objetivo de largo plazo de 56% o más (F7).

**Resultados** (`resultados.json → escenarios`; millones de NT$):

| Escenario | Concepto | 2026E | 2027E | 2028E | 2029E | 2030E |
|---|---|---:|---:|---:|---:|---:|
| Tensión | Ingresos | 5,123,178 | 4,713,324 | 4,147,725 | 4,355,111 | 4,616,418 |
| | Margen operativo | 55.15% | 46.10% | 40.50% | 42.20% | 44.50% |
| | Utilidad neta | 2,400,577 | 1,867,906 | 1,470,134 | 1,617,130 | 1,813,566 |
| | FCF (CFO − capex) | 967,727 | 850,676 | 1,437,619 | 1,677,023 | 1,745,472 |
| | Caja final | 3,109,216 | 3,229,796 | 3,833,590 | 4,573,061 | 5,277,253 |
| Intermedio | Ingresos | 5,492,656 | 6,591,188 | 7,382,130 | 7,972,700 | 8,451,063 |
| | Margen operativo | 57.70% | 56.25% | 55.50% | 55.00% | 54.50% |
| | Utilidad neta | 2,687,071 | 3,151,292 | 3,504,321 | 3,783,764 | 4,016,959 |
| | FCF | 1,196,797 | 1,787,109 | 2,335,091 | 2,824,047 | 3,275,894 |
| | Caja final | 3,338,286 | 4,395,298 | 5,896,566 | 7,783,061 | 10,017,674 |
| Eficiencia | Ingresos | 5,565,028 | 7,123,236 | 8,405,419 | 9,414,069 | 10,167,195 |
| | Margen operativo | 58.50% | 59.25% | 59.70% | 59.80% | 59.80% |
| | Utilidad neta | 2,759,237 | 3,580,595 | 4,281,737 | 4,846,085 | 5,291,081 |
| | FCF | 1,276,486 | 2,120,581 | 2,933,481 | 3,669,862 | 4,243,615 |
| | Caja final | 3,417,975 | 4,808,460 | 6,908,117 | 9,640,427 | 12,842,761 |

Ningún escenario requiere revolvente (C16 OK en los 15 años-escenario). La caja final no es un pronóstico: es FCF que la política de capital fija de los escenarios no asigna.

**Diagnósticos** (`resultados.json → diagnosticos_escenarios`; la conversión a USD con 32 es un supuesto de presentación):
- **Crecimiento de 2026 en USD:** 30.8% en tensión, **40.2% en intermedio** (coherente con la guía de "ligeramente arriba de 40%") y 42.0% en eficiencia.
- **CAGR en USD 2024-2029:** 8.6%, 22.6% y 26.7%, contra el "cerca de 25%" de la administración (F7). La base de 2024 es de US$90.07 mil M; el 2T24 se calcula con el +44.4% a/a de F9.
- **ROE sobre el capital promedio:** en el intermedio baja de 41.8% (2026E) a 23.8% (2030E), por debajo del "high-20s" objetivo. *Inferencia:* sin recompras ni más dividendos, la caja acumulada diluye el ROE. El objetivo de ROE depende de la asignación de capital que el modelo no supone.
- **FCF / utilidad neta:** 0.45 en 2026E (capex de 36%) y 0.82 en 2030E en el intermedio.

**Punto de quiebre de liquidez** (`resultados.json → punto_de_quiebre_financiamiento`; cálculo de mecanismo). Con el capex y los dividendos de tensión sin cambio, hace falta recortar **17.9 pp** los márgenes bruto y operativo de todos los años para que la caja baje del mínimo de 1.5 billones. Eso lleva el margen bruto de 2028E a 33.6% y el operativo a 22.6%, y el primer año con financiamiento sería 2030E.

*Inferencia:*
- **(i) Liquidez.** No es el riesgo que se activa primero. Con márgenes operativos de 40% o más y caja de 2.8 billones, ni una caída de 12% ni un capex de 40% de los ingresos obligan a endeudarse. El riesgo está en el valor: duración del crecimiento, márgenes y retorno del capex (§6).
- **(ii) Capex.** Es el mecanismo dominante del FCF. En tensión, el FCF / ingresos cae a 18% en 2026E-2027E con un capex rígido y sube a 35%-38% cuando el capex se ajusta. La conversión no depende del ciclo de ingresos tanto como del ritmo de inversión.
- **(iii) Doble conteo.** Si el escenario intermedio restara la dilución total de 3-4 pp en lugar de la incremental de 1 pp, su margen bruto de 2030E sería de 59.5%-60.5%, no de 62.5%. Eso es 2-3 pp menos por contar dos veces lo que el 67% del 1S26 ya incluye (`resultados.json → puente_margen_bruto`).

## 6. DCF inverso (en USD)

**Insumos** (hechos con fuente, salvo que se marque supuesto; `base.json → insumos_complementarios.dcf_inverso`):
- **Moneda.** El DCF se calcula en USD porque casi todas las ventas están en USD (F1 p. 11). El balance en NT$ se convierte a **31.7895** (F13, 24-sep-2026).
- **Precio y acciones:** **451.15 USD por ADS** (TSM, cierre del 24-sep-2026, F13). Cada ADS representa 5 acciones (F1 p. 46), sobre 25,932 M de acciones (F3 diap. 4 y 7). Resultan 5,186.4 M de ADS equivalentes y una capitalización de US$2,339,844 M. El precio local de 2,475 NT$ equivale a 389.28 USD por ADS: **el ADR cotiza con prima de 15.9%**.
- **Deuda neta al 30-jun-2026 de −2,112,021.3 millones de NT$ (−US$66,438 M):** bonos y préstamos de 1,031,673.6, más arrendamientos de 36,882.4, más dividendos por pagar de 337,435.8, menos caja y valores circulantes de 3,518,013.1 (F4 pp. 3 y 22). Los dividendos por pagar se suman porque la caja del 30-jun ya estaba comprometida con los tenedores de fechas ex anteriores. El de NT$7.00 del 1T26 tuvo fecha ex el 16-sep-2026 (F3 diap. 11).
- **Ingresos de 12 meses de US$142,930 M** (§3).
- **Margen FCF base de 25.53%:** (CFO − capex de PPE − intangibles − SBC) de 12 meses entre ingresos de 12 meses, es decir, (2,634,679.0 − 1,491,122.7 − 9,406.8 − 683.5) / 4,440,492.5. El capex de 12 meses (33.8% de los ingresos) está en máximos.
- **WACC de 11.48%:**
  - costo de capital accionario de 11.58% = r_f de 4.75% + β de 1.517 × ERP de 4.09% + λ de 0.800 × CRP de 0.78%;
  - la β de 1.517 es la desapalancada del sector (1.50, F14) reapalancada con D/E de 1.44% y t de 20%;
  - **λ = 80.0%** es la fracción de activos no circulantes en Taiwán (F1 p. F-82; supuesto de exposición por producción, no por ventas);
  - la CRP de Taiwán es de 0.78% (F15, ene-2026);
  - costo de deuda de (4.75% + 0.51%) × (1 − 20%) = 4.21%, con peso de 1.4%.
- **Supuestos del modelo:** g terminal de 3.0% (menor que r_f), 10 años, margen FCF constante y descuento a fin de año (`herramientas/modelo_integrado.dcf_inverso`).

**Resultado base.** El precio descuenta un **crecimiento de ingresos de 26.0% anual por 10 años**: ≈US$455 mil M en el año 5 y ≈US$1.44 billones en el año 10 (10.1 veces los de 12 meses), con 25.5% de margen FCF.
- El valor terminal pesa 66.5% del valor de empresa (sin alerta: el umbral es 75%). El múltiplo terminal es de 12.2 veces el FCF.
- Residuo de la bisección: 0.00002.

**Sensibilidad** (crecimiento implícito; entre paréntesis, el peso del valor terminal):

| Margen FCF 20% | g 2.5% | g 3.0% | g 3.5% |
|---|---|---|---|
| WACC 10.48% | 27.8% (69%) | 27.1% (71%) | 26.4% (72%) |
| WACC 11.48% | 30.1% (68%) | 29.5% (69%) | 28.9% (70%) |
| WACC 12.48% | 32.4% (66%) | 31.8% (67%) | 31.2% (68%) |

| Margen FCF 25.5% (base) | g 2.5% | g 3.0% | g 3.5% |
|---|---|---|---|
| WACC 10.48% | 24.4% (67%) | 23.7% (69%) | 23.0% (70%) |
| WACC 11.48% | 26.6% (65%) | **26.0% (67%)** | 25.4% (68%) |
| WACC 12.48% | 28.7% (64%) | 28.2% (65%) | 27.7% (66%) |

| Margen FCF 34% | g 2.5% | g 3.0% | g 3.5% |
|---|---|---|---|
| WACC 10.48% | 20.4% (65%) | 19.7% (66%) | 19.1% (67%) |
| WACC 11.48% | 22.5% (63%) | 22.0% (64%) | 21.4% (65%) |
| WACC 12.48% | 24.6% (61%) | 24.1% (62%) | 23.5% (63%) |

- El margen de 34% es un supuesto: el margen de CFO de 12 meses (59.3%) con el capex normalizado a 25% de los ingresos.
- Rango de las 27 celdas: **19.1%-32.4%**.
- ±1 pp de WACC mueve el implícito ≈2.1-2.3 pp, cerca de la lección de 2.3-2.6 pp de `conocimiento/25` §2.10. ±0.5 pp de g lo mueve ≈0.6 pp.

**Variantes** (`resultados.json → dcf_inverso.variantes`):

| Variante | Crecimiento implícito |
|---|---:|
| Deuda neta sin dividendos por pagar / ampliada (resta 209,809 de activos financieros no circulantes) / con anticipos de clientes como deuda | 25.96% / 25.98% / 26.07% |
| λ por ingresos (sede Taiwán 1S26: 6.85%; WACC de 10.91%) | 24.7% |
| Precio local 2330.TW (sin la prima del ADR) | 23.9% |
| Margen = FCF − SBC de 2030E de cada escenario: tensión 37.8% / intermedio 38.7% / eficiencia 41.7% | 20.5% / 20.1% / 19.1% |

*Inferencia (comparación, no veredicto):*
- La trayectoria base implica ≈US$405 mil M de ingresos a 4.5 años (fin de 2030). En los escenarios, a 32 NT$/USD, 2030E es de US$144 mil M (tensión), US$264 mil M (intermedio) y US$318 mil M (eficiencia). Los tres quedan por debajo **con el margen actual de 25.5%**, deprimido por el capex.
- La comparación coherente usa el margen que cada escenario alcanza en 2030E (38%-42%). Así, el precio pide **≈19%-20% anual por 10 años**. El escenario de eficiencia da 19.4% anual entre los 12 meses y 2030E (4.5 años) y desacelera a 8% en 2030E; el intermedio da 14.6%.
- El precio pide sostener un crecimiento **del tipo de eficiencia más allá de 2030**, con márgenes de FCF de ~40%. El debate es la **duración** del ciclo de IA y la normalización del capex, no el 3T26.
- La prima del ADR (15.9%) sola equivale a ~2 pp de crecimiento implícito.
- No hay tasas base de crecimiento por tamaño en el repositorio (pendiente). No se afirma si 19%-26% por 10 años es alcanzable.

## 7. Sensibilidad geopolítica reproducible

**Método** (`modelo.py → sensibilidad_geopolitica`, en Decimal exacto): rejilla completa de **81 celdas**, sin elegir solo las favorables.
- **Base de 12 meses:** R = 4,440,492.5; utilidad bruta = 2,852,135.8 (m = 64.23%); utilidad operativa = 2,491,156.1; tasa de 17.5% (supuesto); 25,932 M de acciones; 31.7895 NT$/USD.
- **e = fracción de ingresos restringida ∈ {2%, 5%, 10%}** (supuesto). Referencias de hecho: clientes con sede en China fueron 9% de 2025, 6.8% del 1S26 y 6.0% del 2T26 (F1 p. 17; F4 p. 31). No todo eso está controlado: incluye nodos maduros.
- **r = sustitución dentro del periodo ∈ {0, 50%, 100%}** (supuesto).
- **c = fracción del ingreso perdido que no se ahorra en costo ∈ {80%, 90%, 100%}** (supuesto). Referencia calculada: 1 − (costo de ventas − D&A) / ingresos = 79.7%. Es el tope si todo el costo no ligado a depreciación fuera variable.
- **d = presión incremental del extranjero ∈ {0, 1, 2} pp** (supuesto acotado por la guía: de 2-3 a 3-4 pp; §2.2).
- **Fórmulas:** L = R·e·(1−r); R' = R − L; UB' = R·m − L·c − R'·d; gastos de operación fijos, así que ΔUO = −(L·c + R'·d); ΔUPA = ΔUO·(1−t)/acciones.
- **Doble comprobación algebraica (G01):** COGS' = R(1−m) − L(1−c) + R'·d y UB' = R' − COGS'. El error máximo en las 81 celdas es 0.

| e | r | c | Ingresos perdidos | ΔUO d=0 | ΔUO d=1 pp | ΔUO d=2 pp | ΔUO % (d = 0 / 1 / 2 pp) | Δ margen bruto pb (d = 0 / 2 pp) | ΔUPA US$/ADS (d = 0 / 2 pp) |
|---|---|---|---:|---:|---:|---:|---|---|---|
| 2% | 0% | 80% | 88,810 | −71,048 | −114,565 | −158,082 | −2.9% / −4.6% / −6.3% | −32 / −232 | −0.356 / −0.791 |
| 2% | 0% | 90% | 88,810 | −79,929 | −123,446 | −166,963 | −3.2% / −5.0% / −6.7% | −53 / −253 | −0.400 / −0.835 |
| 2% | 0% | 100% | 88,810 | −88,810 | −132,327 | −175,844 | −3.6% / −5.3% / −7.1% | −73 / −273 | −0.444 / −0.880 |
| 2% | 50% | 80% | 44,405 | −35,524 | −79,485 | −123,446 | −1.4% / −3.2% / −5.0% | −16 / −216 | −0.178 / −0.618 |
| 2% | 50% | 90% | 44,405 | −39,964 | −83,925 | −127,886 | −1.6% / −3.4% / −5.1% | −26 / −226 | −0.200 / −0.640 |
| 2% | 50% | 100% | 44,405 | −44,405 | −88,366 | −132,327 | −1.8% / −3.5% / −5.3% | −36 / −236 | −0.222 / −0.662 |
| 5% | 0% | 80% | 222,025 | −177,620 | −219,804 | −261,989 | −7.1% / −8.8% / −10.5% | −83 / −283 | −0.889 / −1.311 |
| 5% | 0% | 90% | 222,025 | −199,822 | −242,007 | −284,192 | −8.0% / −9.7% / −11.4% | −136 / −336 | −1.000 / −1.422 |
| 5% | 0% | 100% | 222,025 | −222,025 | −264,209 | −306,394 | −8.9% / −10.6% / −12.3% | −188 / −388 | −1.111 / −1.533 |
| 5% | 50% | 80% | 111,012 | −88,810 | −132,105 | −175,399 | −3.6% / −5.3% / −7.0% | −40 / −240 | −0.444 / −0.878 |
| 5% | 50% | 90% | 111,012 | −99,911 | −143,206 | −186,501 | −4.0% / −5.7% / −7.5% | −66 / −266 | −0.500 / −0.933 |
| 5% | 50% | 100% | 111,012 | −111,012 | −154,307 | −197,602 | −4.5% / −6.2% / −7.9% | −92 / −292 | −0.555 / −0.989 |
| 10% | 0% | 80% | 444,049 | −355,239 | −395,204 | −435,168 | −14.3% / −15.9% / −17.5% | −175 / −375 | −1.778 / −2.178 |
| 10% | 0% | 90% | 444,049 | −399,644 | −439,609 | −479,573 | −16.0% / −17.6% / −19.3% | −286 / −486 | −2.000 / −2.400 |
| 10% | 0% | 100% | 444,049 | −444,049 | −484,014 | −523,978 | −17.8% / −19.4% / −21.0% | −397 / −597 | −2.222 / −2.622 |
| 10% | 50% | 80% | 222,025 | −177,620 | −219,804 | −261,989 | −7.1% / −8.8% / −10.5% | −83 / −283 | −0.889 / −1.311 |
| 10% | 50% | 90% | 222,025 | −199,822 | −242,007 | −284,192 | −8.0% / −9.7% / −11.4% | −136 / −336 | −1.000 / −1.422 |
| 10% | 50% | 100% | 222,025 | −222,025 | −264,209 | −306,394 | −8.9% / −10.6% / −12.3% | −188 / −388 | −1.111 / −1.533 |
| cualquier e | 100% | 80/90/100% | 0 | 0 | −44,405 | −88,810 | 0.0% / −1.8% / −3.6% | 0 / −200 | 0.000 / −0.444 |

Las 81 celdas completas, sin agrupar, están en `resultados.json → sensibilidad_geopolitica.filas`, con ΔUPA en NT$ por acción y en USD por ADS. Las filas con r = 100% agrupan 27 celdas cuyo único efecto es d.

*Inferencia:*
- **(i) Canales.** Son dos y no deben sumarse sin pensar: la restricción (e, r, c) quita ingresos, y el extranjero (d) quita margen sobre todo lo que queda. Con e = 5% y r = 50%, cada punto de d cuesta ≈43 mil M, cerca de la mitad de lo que cuesta la restricción misma (89-111 mil M).
- **(ii) Peor celda.** Es e = 10%, r = 0, c = 100% y d = 2 pp: −524 mil M de utilidad operativa (−21.0%), el margen bruto baja a 58.3% y −2.62 USD por ADS en un año. Es un choque de nivel. En el DCF inverso, lo que mueve el precio es la duración del crecimiento, salvo que la restricción sea permanente y reduzca la tasa de crecimiento (§6).
- **(iii) Doble conteo.** Si d se tomara como la dilución total comunicada (2-4 pp), cada celda sobreestimaría la pérdida en 2 pp × R': entre 79,929 y 88,810, o 3.2%-3.6% de la utilidad operativa de 12 meses.
- **(iv) Cola.** La rejilla no incluye el tipo E de `conocimiento/23` (bloqueo o invasión de Taiwán, donde está el 80% de los activos no circulantes). Ese riesgo no se modela con sensibilidades marginales, y no se asignan probabilidades ni valor esperado.

## 8. Qué NO demuestra este trabajo
- **No es pronóstico, valuación intrínseca ni recomendación.** Los escenarios son mecanismos con supuestos explícitos; la caja proyectada no es una estimación de caja futura.
- **Que todos los controles pasen demuestra consistencia aritmética y una transcripción fiel**, no que los supuestos sean correctos. El motor mantiene constantes los otros activos y pasivos. No modela anticipos de clientes, subsidios, aportes de minoritarios (JASM, ESMC), capex de intangibles ni la ganancia de VIS. Supone deuda constante y rendimiento de 3% sobre toda la caja.
- **El puente de margen es una contabilidad de supuestos**, no una medición. TSMC no publica la dilución realizada por fábrica ni por país en el 20-F, y el 2-3/3-4 pp es una estimación de la administración (F10 p. 4).
- **El DCF inverso dice qué crecimiento pide el precio bajo un WACC, un g, un margen constante y un horizonte elegidos.** No dice si el precio es alto o bajo. La β (del sector en EUA), la ERP, la CRP (ene-2026) y λ son estimaciones o supuestos.
- **La sensibilidad geopolítica no mide la exposición real.** TSMC categoriza sus ingresos por sede del cliente, no por destino ni por uso final (F1 p. 17), y no revela qué fracción está sujeta a licencias. No se certifica la elegibilidad legal de ninguna operación ni se afirma que no existan modificaciones regulatorias posteriores a F11 y F12.
- **La identidad de los clientes A y B no está en el filing.**
- **La doble comprobación la hizo el mismo autor contra datos del mismo emisor** (sus estados y su XBRL). No es una auditoría independiente.

## 9. Pendientes
1. **Dilución realizada.** Leer las transcripciones del 4T25 y del 1T26, y el *Management Report* del 2T26 (investor.tsmc.com bloquea `curl`; usar WebFetch), para ver si la administración cuantificó la dilución del extranjero ya realizada en 2025-2026. El 20-F no lo hace.
2. **Tasas base.** Faltan tasas base de crecimiento de ingresos por tamaño (p. ej., Mauboussin, *The Base Rate Book*) para contrastar el 19%-26% por 10 años. No están en el repositorio y no se inventan.
3. **Reglas primarias.** Leer la regla interina del 16-ene-2025 (90 FR 5298, umbrales de la presunción para "front-end fabricators") y la proclamación de la Sección 232 (arancel de 25%, uso designado, programa de compensación) antes de usar cualquier fracción restringida que no sea hipotética. Vigilar el 31-dic-2026 (F11).
4. **Siguiente reporte.** El comunicado del 3T26 se contrasta con la guía (US$44.6-45.8 mil M; margen bruto de 65%-67%; tipo de cambio de 32). En FASE 0 se puede registrar como pronóstico con `herramientas/pronosticos.py` antes de la fecha; no se hizo aquí.
5. **Prima de riesgo país.** Actualizar la CRP de Taiwán con la actualización de jul-2026 de Damodaran (aquí se usó la página de ene-2026) y revisar λ.
6. **Deuda 2025.** Documentar el movimiento no monetario de −1,528.5 en préstamos bancarios (probablemente tipo de cambio del yen) para convertir en prueba el C06 INFO de 2025. Para FY2023, conseguir el saldo de activos arrendados a terceros al 1-ene-2023 (20-F 2023) y cerrar C05.
7. **Extender el motor.** Modelar anticipos de clientes, subsidios y aportes de minoritarios exige cambiar `herramientas/modelo_integrado.py`, que es compartido. No se hizo.
8. **Acceso a la SEC.** Definir `SEC_USER_AGENT` con un correo real del sistema: `www.sec.gov` respondió 403 al agente sin contacto.

## 10. Reproducción
```
cd /home/user/New1
python3 empresas/TSM/modelo/modelo.py                                      # código 0: controles OK y auditoría coincide
python3 herramientas/huellas.py verificar empresas/TSM/modelo/SHA256SUMS.txt        # OK
python3 herramientas/huellas.py verificar empresas/TSM/modelo/datos/SHA256SUMS.txt  # OK
```
Solo usa la biblioteca estándar de Python 3.11. `resultados.json` es determinista: dos corridas dan el mismo SHA-256. Para volver a verificar un documento de la SEC: se descarga la URL de F1-F9, se quita la etiqueta `<script type="text/javascript" src="/...">` que agrega el CDN y se compara el SHA-256 con `base.json`.
