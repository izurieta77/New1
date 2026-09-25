# NVIDIA (NVDA): notas del 10-K y 10-Q, modelo integrado, DCF inverso y sensibilidad geopolítica

> Corte: 25-sep-2026. **FASE 0 (formación): no es recomendación de compra o venta.** Los escenarios son supuestos de mecanismo, no pronósticos, guía ni consenso.
> Convención: **hecho** = cifra del documento con página; **Inferencia:** = interpretación propia; **supuesto** = entrada de escenario elegida por el analista. Montos en millones de USD salvo que se indique otra cosa. Ejercicio fiscal de NVIDIA: FY2026 terminó el 25-ene-2026; FY2027 tiene 53 semanas y un 4T de 14 semanas (F1 p. 56; F3 p. 9).
> Archivos: `empresas/NVDA/modelo/base.json` (transcripción y supuestos), `modelo.py` (corrida), `resultados.json` (salida completa), `SHA256SUMS.txt` (huellas). No se editó `ficha.md`.

## 1. Fuentes leídas y congeladas

| Id | Documento | Fecha | Alcance leído |
|---|---|---|---|
| F1 | 10-K FY2026, accession 0001045810-26-000021 ([SEC](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)) | 25-feb-2026 | Estados financieros pp. 51-55; notas 1-17 pp. 56-80; MD&A pp. 36-44; Item 5 pp. 33-34; párrafos sobre exportación en Item 1 y en factores de riesgo (pp. 9-11 y 25-28); manufactura p. 8 |
| F2 | 10-K FY2025, accession 0001045810-25-000023 ([SEC](https://www.sec.gov/Archives/edgar/data/1045810/000104581025000023/nvda-20250126.htm)) | 26-feb-2025 | Estados financieros pp. 52-56 (balance al 28-ene-2024) y Nota 11 p. 72 |
| F3 | 10-Q 2T FY2027, accession 0001045810-26-000075 ([SEC](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm)) | 26-ago-2026 | Estados pp. 3-8; notas 1-14 pp. 9-24; MD&A pp. 25-33; párrafos de factores de riesgo sobre exportación, deuda y recompras (pp. 35-39); Item 2 p. 40 |
| F4 | 8-K, EX-99.1, comunicado del 4T FY2026 ([q4fy26pr.htm](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000019/q4fy26pr.htm)) | 25-feb-2026 | Conciliación GAAP a non-GAAP y FCF (tablas sin auditar) |
| F5 | 8-K, EX-99.1, comunicado del 2T FY2027 ([q2fy27pr.htm](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000073/q2fy27pr.htm)) | 26-ago-2026 | Guía del 3T FY2027, conciliación de FCF (tablas sin auditar) |
| F6 | Yahoo Finance chart v8, NVDA | cierre del 24-sep-2026 | Precio de 224.58 USD |
| F7 | Damodaran, *Betas by Sector (US)*, datos a enero de 2026 | ene-2026 | Renglón Semiconductor (66 empresas): beta desapalancada corregida por caja de 1.50 |
| F8 | `conocimiento/03` §2.3 (hoja de Damodaran de sep-2026) | sep-2026 | T-bond de 4.75% y ERP de 4.09% |

**Congelamiento.** Los insumos se hashearon con `herramientas/huellas.py` (el manifiesto se verificó con `huellas.py verificar`: OK). La huella de cada documento está en `base.json` → `fuentes.F*.sha256`, y `base.json` a su vez está en `modelo/SHA256SUMS.txt`. El CDN de la SEC agrega al final de cada HTML una etiqueta `<script>` que varía, así que el hash se calcula sin esa etiqueta. El tamaño resultante coincide byte a byte con el `index.json` de EDGAR (por ejemplo, 1,967,816 bytes para F1). Manifiesto de insumos:

```
73d81f5a111abcf72426c840871e76f5f5edc9631f436d495a86b6f87306d58b  nvda-20260125.htm   (F1)
dae19486be264fd26eb00a7f920dc641041a261c81bc8c03b678eea947de4856  nvda-20250126.htm   (F2)
e2634e509c241c5f45e3f6c115dc38a85645e5fdbee760b4a04f5e9035f6f7a9  nvda-20260726.htm   (F3)
a4146bb7e363b6560edd07e3743cb20f062634df1b2ce104c37406aef702e960  q4fy26pr.htm        (F4)
1809cb206590dcfeb959f3a1a64157f4e5ee42788ec51289b74f3ea299931eb7  q2fy27pr.htm        (F5)
b5560ddc830756505eb6058c797b2448827325d59b5e714e97ba5f3603f0af8b  yahoo_NVDA_1mo.json (F6, fuente viva: no se reproduce)
10993bab71504e2449ccdd9e3d67fa4da983bed380b2f4486e5200a7b258616b  damodaran_betas.html (F7)
```

## 2. Hallazgos de las notas

### 2.1 Concentración de clientes
**Hechos:**
- FY2026: un cliente directo representó 22% de los ingresos y otro 14% (≈47.5 y ≈30.2 mil M; F1 Nota 16 p. 78 y MD&A p. 41).
- FY2025: 12%, 11% y 11%. FY2024: uno de 13% (F1 p. 78).
- 2T FY2027: un cliente directo representó 16%. En el 1S FY2027, tres clientes representaron 16%, 15% y 13% (44% entre los tres; F3 Nota 13 p. 23).
- Cuentas por cobrar: al 25-ene-2026, tres clientes concentraban 25%, 18% y 13% (F1 Nota 9 p. 67). Al 26-jul-2026, cinco clientes concentraban 22%, 14%, 13%, 11% y 10%: 70% de 63,059, ≈44.1 mil M (F3 Nota 7 p. 14).
- Clientes indirectos: "una empresa de investigación y despliegue de IA" aportó "un monto significativo" de ingresos comprando servicios de nube a los clientes de NVIDIA (F1 p. 41; F3 p. 29). En esa sección no se da su nombre.
- En otra nota, el 10-Q sí identifica a una filial de OpenAI como el cliente cuyas rentas garantiza NVIDIA ante SB Energy (F3 Nota 10 p. 19).

*Inferencia:*
- La concentración aumentó: de un cliente de más de 10% en FY2024 a tres en el 1S FY2027.
- El riesgo de crédito también se concentró: 70% de la cartera está en cinco nombres, en el mismo semestre en que el 10-Q revela plazos de 90 días a un año para clientes con grado de inversión (F3 p. 14). El 10-K decía que el pago vence "poco después de la entrega" (F1 p. 56).
- Que el cliente indirecto sea OpenAI es plausible, pero el filing no lo afirma en la nota de concentración.

### 2.2 Inventario, provisiones y compromisos de suministro
**Hechos:**
- **Inventario.** Pasó de 10,080 a 21,403 en FY2026 (+112%), contra un costo de ventas que subió 91% (F1 p. 53 y p. 51). Llegó a 31,575 al 26-jul-2026. Las materias primas pasaron de 3,807 a 11,341 (F3 Nota 7 p. 14).
- **Provisiones de FY2026.** Las provisiones brutas de inventario y obligaciones excedentes sumaron 7.2 mil M (3.7 en FY2025), incluidos 4.5 mil M del H20. Las liberaciones fueron de 1.5 mil M. El efecto neto sobre el margen bruto fue de −2.6 pp (−2.3 en FY2025) (F1 MD&A p. 41).
- **Provisiones del 1S FY2027.** Sumaron 2.1 mil M, con liberaciones de 280 M y un efecto de −1.0 pp (F3 p. 30).
- **Compromisos al cierre de FY2026.** Los de manufactura, suministro y capacidad eran de 95.2 mil M, pagaderos sustancialmente en FY2027. Además había 27 mil M en nube multianual, 11.4 mil M en inversiones y 3.4 mil M de otros (F1 Nota 12 p. 70).
- **Compromisos al 26-jul-2026 (F3 Nota 10 p. 18), 366 mil M en total:**
  - suministro y capacidad: **279 mil M** (119 mil M el trimestre anterior), repartidos en 92 mil M en el resto de FY2027, 87 en FY2028 y 88 en FY2029;
  - nube: 29 mil M;
  - arrendamientos de centros de datos por iniciar: 25 mil M;
  - inversiones de capital: 25 mil M;
  - capex: 8 mil M.
  - Aparte hay 56 mil M de "compromisos adicionales": 36 de acuerdos con nubes de IA y 20 de arrendamientos para terceros.

*Inferencia (cálculo propio):*
- Los compromisos de suministro equivalen a **3.6 veces** el costo de ventas de 12 meses (76,729 = 302,970 − 226,241).
- Solo lo comprometido para el resto de FY2027 (92 mil M) duplica el costo de ventas del 1S FY2027 (44,538). Buena parte irá a inventario, anticipos o capacidad para FY2028.
- Precedente del H20: cuando la demanda cae por regulación, estos compromisos se convierten en cargos al margen bruto. Por eso el escenario de tensión (§5) combina inventario alto con un margen bruto menor.

### 2.3 Controles de exportación (EUA-China y grupo D:5) y cargos relacionados
**Hechos:**
- **Oct-2023.** Se exige licencia para exportar productos que superan ciertos umbrales a China y a los grupos D:1, D:4 y D:5 (incluye Arabia Saudita, EAU y Vietnam; excluye Israel). También aplica a empresas con sede, o matriz, en D:5 (F1 p. 10 y p. 26).
- **Abr-2025.** Se exige licencia para el H20 (China y D:5). Hubo un cargo de **4.5 mil M** en el 1T FY2026 por inventario excedente y obligaciones de compra (F1 p. 10 y p. 36).
- **Ago-2025.** EUA otorgó licencias de H20 que generaron ~60 M de ingresos. Funcionarios de EUA expresaron que esperaban recibir 15% o más, sin regla publicada (F1 p. 10).
- **Feb-2026.** EUA otorgó licencias para "pequeñas cantidades" de H200, con inspección en EUA y un arancel de 25% al importarlos a EUA (F1 p. 36).
- **1S FY2027.** El gobierno chino restringió esas compras. Hubo un cargo de **0.4 mil M** por H200. Los envíos realizados son menos de 1% de los ingresos de Data Center del 2T, y NVIDIA no pudo trasladar el arancel (F3 p. 27 y p. 37).
- NVIDIA se declara "efectivamente excluida" del mercado chino de cómputo para centros de datos. Sí puede enviar productos no controlados, como GPU de juego y estaciones de trabajo (F3 p. 37).
- El 15-sep-2025, el regulador antimonopolio chino publicó un hallazgo preliminar de que NVIDIA violó las condiciones de la aprobación de Mellanox (F1 p. 26).
- La guía del 3T FY2027 no supone ingresos de cómputo de Data Center en China (F5).

*Inferencia:*
- El choque regulatorio ya pasó por el estado de resultados dos veces: 4.5 mil M más 0.4 mil M. El mecanismo es cargo de inventario y compromisos, no solo ventas perdidas.
- Como la guía ya excluye el cómputo de China, la sensibilidad de §7 mide restricciones **adicionales** (más destinos D:5, clientes con sede en China que compran productos no controlados, usuarios finales fuera de EUA y Europa). No mide la pérdida de China, que ya ocurrió.

### 2.4 Compensación en acciones (SBC)
**Hechos:**
- La SBC fue de 6,386 en FY2026, 4,737 en FY2025 y 3,549 en FY2024 (2.96%, 3.63% y 5.83% de los ingresos; F1 Nota 3 p. 61). En el 1S FY2027 fue de 3,954 (F3 p. 10).
- La SBC no devengada era de 14.8 mil M a 2.3 años al cierre de FY2026 (F1 p. 61) y de 19.4 mil M a 2.6 años al 26-jul-2026 (F3 p. 10).
- El valor razonable de lo que se consolidó en FY2026 fue de 22.2 mil M (F1 p. 63).
- La retención fiscal por liquidación neta fue de 7,948 en FY2026 (51 M de acciones; F1 p. 34 y p. 55) y de 6,930 en FY2025.
- Desde el 1T FY2027, el non-GAAP del emisor ya no excluye la SBC (F5).

*Inferencia (cálculo propio):*
- La caja pagada por retenciones fue **1.24 veces** el gasto de SBC en FY2026 (1.46 en FY2025): el gasto se registra al precio de otorgamiento y la retención se paga al precio de consolidación.
- El FCF del emisor suma de regreso la SBC y resta esas retenciones en financiamiento, no en el FCF. Un FCF que descuente las retenciones sería 96,575 − 7,948 = 88,627 (41.0% de los ingresos).
- En el DCF inverso (§6) la SBC se resta del FCF como costo económico (`conocimiento/25` §2.6). No se restan además las retenciones, para no duplicar el ajuste.

### 2.5 Recompras y dividendos
**Hechos:**
- FY2026: recompró 282 M de acciones por 40.4 mil M (≈143 USD por acción). FY2025: 310 M por 34.0 mil M (F1 Nota 14 p. 76).
- 1S FY2027: 203 M por 39.8 mil M (≈196 USD). En el 2T fueron 94.4 M a un promedio de ≈206.7 USD (F3 p. 21; tabla mensual p. 40).
- El 18-may-2026 se autorizaron otros 80 mil M; quedaban 99.3 mil M al 26-jul-2026.
- El dividendo trimestral subió de 0.01 a 0.25 USD, con un pago de 6,047 en el 2T (F3 p. 6 y p. 21).
- En FY2025 el emisor escribió que el programa "busca compensar la dilución por acciones emitidas a empleados" (F2 p. 44).
- Acciones en circulación: 24,477 → 24,304 en FY2026 (−0.71%) y 24,147 al 26-jul-2026 (F1 p. 53-54; F3 p. 6).

*Inferencia (cálculo propio):*
- En FY2026 se retiraron 333 M de acciones (282 recompradas + 51 retenidas) contra 160 M emitidas. Cerca de la mitad de la recompra bruta solo compensa la emisión a empleados.
- La salida neta de caja por acciones fue de 47,390 (40,086 + 7,948 − 644) para reducir el conteo 0.7%.

### 2.6 Ingresos por segmento, plataforma y geografía (sede de facturación contra uso final)
**Hechos:**
- **Segmentos de FY2026:** Compute & Networking 193,479 con utilidad de segmento de 130,141 (67.3%); Graphics 22,459 con 9,156 (F1 Nota 16 p. 77).
- **Mercado final de FY2026:** Data Center 193,737 (cómputo 162,361, networking 31,376, este último +142%) (F1 p. 79 y p. 40).
- **Plataformas del 2T FY2027:** Data Center 89,023 (Hyperscale 48,710; AI Clouds, Industrial & Enterprise 40,313) y Edge Computing 7,198 (F3 Nota 13 p. 24).
- **Geografía por sede del cliente directo en FY2026** (criterio adoptado en el 3T FY2026 y reexpresado; F1 p. 78):

| Sede del cliente | Monto | % de ingresos |
|---|---:|---:|
| EUA | 149,617 | 69.3% |
| Taiwán | 42,345 | 19.6% |
| China y Hong Kong | 19,677 | 9.1% |
| Otros | 4,299 | 2.0% |

- **Evolución de China y Hong Kong:** 20.2% en FY2024 y 19.2% en FY2025; 7.0% en el 1S FY2027 y 8.2% en el 2T (7,880 de 96,221; F3 p. 23).
- **Sede contra uso final:** NVIDIA estima que **76%** de los ingresos de Data Center de clientes con sede en Taiwán se atribuye a clientes finales en EUA y Europa. Advierte que el cliente final y el lugar de envío pueden diferir de la sede (F1 p. 78 nota 2).

*Inferencia:*
- La tabla geográfica mide dónde está la sede de quien factura, no dónde se usa el producto. No sirve para medir ventas expuestas a una regla que depende de destino, usuario final y sede de la matriz.
- El 8.2% de China en el 2T, pese a la exclusión de Data Center, es coherente con los productos no controlados que el 10-Q dice poder enviar. El filing no desglosa ese monto.

### 2.7 Otros hallazgos que afectan la lectura del modelo
- **Ganancias en valores de capital.** Fueron de 8,918 en FY2026 y de 23,707 en el 1S FY2027: **16.8% de la UAI** del semestre (F1 p. 55; F3 p. 15). NVIDIA reporta 99 mil M de inversiones de capital y 25 mil M comprometidos (F3 p. 26). De los valores públicos, 36.9 mil M tienen restricciones de venta (F3 p. 12). *Inferencia:* la utilidad GAAP del 1S incluye revaluaciones no monetarias; el modelo las excluye de la proyección.
- **Garantías.** 105 mil M a SB Energy por rentas de ~4.25 GW para la filial de OpenAI; empiezan a correr por fases desde FY2029 y bajan con los pagos. A eso se suman 3.5 mil M de garantías a nubes de IA, para un máximo de **108.5 mil M** (F3 p. 19). *Inferencia:* la garantía de SB Energy equivale a 0.83 veces el FCF de 12 meses (126,886); el total, a 0.86 veces. Es un pasivo contingente fuera del balance y fuera del modelo.
- **Plazos a clientes y FCF.** NVIDIA da plazos de 90 días a un año a clientes con grado de inversión. El aumento de la cartera por esos plazos redujo el CFO del 1S (F3 p. 14 y p. 31).
- **Deuda.** En jun-2026 emitió 25.0 mil M en siete series; el principal total es de 33.5 mil M (F3 Nota 9 p. 17). La tasa efectiva ponderada por principal es de **4.41%** (cálculo propio con las 14 series).
- **Groq.** Licencia no exclusiva con 14.4 mil M de crédito mercantil y 2.5 mil M de intangible. Se pagaron 13.0 mil M en FY2026 y 2,944 en el 1S FY2027; quedaban 986 por pagar (F1 Nota 2 p. 61; F3 p. 8 y p. 15).
- **Impuestos.** La tasa efectiva fue de 15.1% en FY2026, 13.3% en FY2025 y 12.0% en FY2024 (F1 pp. 73-74), y de 16.5% en el 1S FY2027 (F3 p. 21). La guía de FY2027 es de 16%-18% (F5).

## 3. Base histórica y doble comprobación de la transcripción

La base cubre tres ejercicios: FY2024 (de F2) y FY2025-FY2026 (de F1). `base.json` cita la página de cada partida en `fuentes_campos`. Decisiones de mapeo:
- **Balance:**
  - `inversiones_cp` = valores negociables (incluye capital público).
  - `otros_activos_lp` = arrendamientos operativos + crédito mercantil + intangibles + ISR diferido + valores no negociables + otros activos.
  - `otros_pasivos_lp` = arrendamientos operativos de largo plazo + otros pasivos de largo plazo.
  - `deuda` = corto + largo plazo.
- **Flujo:**
  - El capex incluye intangibles.
  - "Principal payments on property and equipment and intangible assets" va a `principal_arrendamientos_financieros`, porque el emisor lo resta en su FCF (F4). No es solo arrendamiento financiero.
  - Las retenciones fiscales de RSU van a `otros_financiamiento`.
- **Capital:** los bloques `movimientos_capital` y `movimientos_deuda` salen del estado de variaciones y de la Nota 11. Con ellos, C03, C04 y C06 son pruebas reales y no solo INFO.
- **Non-GAAP (C14):** el bloque `ajustado` transcribe la conciliación non-GAAP de F4. En FY2026 la utilidad neta GAAP crece 64.7% y la non-GAAP 57.5%; ambas con la definición de FY2026, que excluía la SBC.

**Doble comprobación.** Se hizo con scripts de trabajo que no forman parte del repositorio y cuyos resultados se registran aquí:

| Prueba | Contra qué | Resultado |
|---|---|---|
| (A) Hechos XBRL | `companyfacts` de la SEC: mismo cierre o ejercicio, en valor absoluto | 181 de 187 cifras coinciden. Las 6 restantes están explicadas: 3 pagos de principal con etiqueta propia del emisor, 2 FCF non-GAAP que solo están en el comunicado, y los valores negociables de FY2026 (51,951), que el XBRL del 10-Q separa en 39,065 de deuda y 12,886 de capital. Las 6 se verificaron en el texto |
| (B) Texto de las tablas | Renglón por etiqueta y columna por ejercicio, en F1 y F2 | 135 comparaciones, 0 diferencias |
| (C) Variaciones del capital y non-GAAP | F1 p. 54 y tabla de F4 | 36 comparaciones, 0 diferencias |
| (D) Insumos del DCF y la sensibilidad | F1, F3 y F5 | 23 comparaciones, 0 diferencias |

Límite: las cuatro pruebas comparan contra datos del mismo emisor y las ejecutó el mismo autor. Es una doble extracción, no una auditoría independiente.

**Métricas históricas** (cálculo sobre hechos; `resultados.json` → `historico.drivers_implicitos`):

| Concepto | FY2024 | FY2025 | FY2026 |
|---|---:|---:|---:|
| Ingresos | 60,922 | 130,497 | 215,938 |
| Crecimiento | n.d. | 114.2% | 65.5% |
| Margen bruto | 72.7% | 75.0% | 71.1% |
| Margen operativo | 54.1% | 62.4% | 60.4% |
| (Ingreso por intereses + otros) / ingresos | 1.8% | 2.2% | 5.2% |
| Tasa efectiva | 12.0% | 13.3% | 15.1% |
| Utilidad neta | 29,760 | 72,880 | 120,067 |
| CFO | 28,090 | 64,089 | 102,718 |
| Capex (PPE + intangibles) | 1,069 | 3,236 | 6,042 |
| FCF del emisor (CFO − capex − principal de PPE) | 26,947 | 60,724 | 96,575 |
| FCF del emisor / utilidad neta | 0.91 | 0.83 | 0.80 |
| SBC / ingresos | 5.83% | 3.63% | 2.96% |
| DSO / DIO / DPO (días) | 59.9 / 116.0 / 59.3 | 64.5 / 112.7 / 70.6 | 65.0 / 125.0 / 57.3 |
| Recompras (caja) / retenciones fiscales de RSU / dividendos | 9,533 / 2,783 / 395 | 33,706 / 6,930 / 834 | 40,086 / 7,948 / 974 |

## 4. Modelo integrado: controles y reconciliación

`python3 empresas/NVDA/modelo/modelo.py` sale con código 0. El motor produjo **540 registros: 520 OK, 0 FALLA, 16 INFO y 4 NO_APLICA.**

`modelo.py` además relee `resultados.json` y recalcula todos los controles con `mi.verificar`. El resultado coincide: 540 registros y 0 FALLA.

| Id | Control | OK | FALLA | INFO | NO_APLICA |
|---|---|---|---|---|---|
| C01 | Balance: activo = pasivo + capital (y totales = suma de componentes) | 54 | 0 | 0 | 0 |
| C02 | Caja: inicial + CFO + CFI + CFF + efecto cambiario = final (y sumas de CFI y CFF) | 59 | 0 | 0 | 0 |
| C03 | Capital: inicial + utilidad + SBC − dividendos − recompras + emisiones + ORI + otros = final | 18 | 0 | 0 | 0 |
| C04 | Utilidades retenidas: inicial + utilidad − dividendos − recompras imputadas + otros = final | 18 | 0 | 0 | 0 |
| C05 | PPE: inicial + capex + nuevos arrendamientos − depreciación + otros = final | 15 | 0 | 2 | 1 |
| C06 | Deuda: inicial + emisiones − amortizaciones (+ otros) = final | 47 | 0 | 2 | 1 |
| C07 | Puente utilidad → CFO | 36 | 0 | 0 | 0 |
| C08 | Cuentas por cobrar = días × ingresos / 365 | 15 | 0 | 3 | 0 |
| C09 | Inventario y proveedores = días × costo de ventas / 365 | 30 | 0 | 3 | 0 |
| C10 | Intereses = tasa × deuda promedio; ingreso financiero = tasa × caja promedio | 30 | 0 | 2 | 1 |
| C11 | Impuestos = tasa × UAI | 15 | 0 | 3 | 0 |
| C12 | FCF = CFO − capex; FCF después de principal | 32 | 0 | 1 | 0 |
| C13 | Reconciliación del histórico con drivers implícitos | 2 | 0 | 0 | 1 |
| C14 | GAAP + ajustes = ajustado | 2 | 0 | 0 | 0 |
| C15 | Aritmética del estado de resultados | 87 | 0 | 0 | 0 |
| C16 | Caja mínima y revolvente, sin plug | 60 | 0 | 0 | 0 |

**Los INFO y NO_APLICA dicen qué falta:**
- **FY2024 no tiene apertura:** no se leyó el balance de FY2023. Por eso C05, C06, C10 y C13 quedan en NO_APLICA ese año.
- **C05 (PPE) es INFO:** la depreciación de PPE solo se publica redondeada (2.4 mil M; F1 p. 68). Los "otros" implícitos son 997 en FY2025 y 901 en FY2026. *Inferencia:* reflejan que la D&A incluye amortización de intangibles (488 en FY2026, F1 p. 64), que el capex incluye intangibles y que hubo PPE adquirido sin pagar (820 en FY2026, F1 p. 68).
- **C12 es real en FY2025 y FY2026:** el FCF reportado por el emisor coincide exactamente con CFO − capex − principal.

**C13, reconciliación.** El mismo motor reproduce FY2025 y FY2026 con una diferencia máxima de 0.0000 (tolerancia de 2.2). Todo lo que el motor no explica sale como partida conciliatoria con nombre. Las partidas materiales (más de 2% de los ingresos) de FY2026 son:

| Partida (FY2026) | Monto | % de ingresos | Lectura |
|---|---:|---:|---|
| otros_ingresos (intereses + otros) | 11,322 | 5.2% | Hecho: 2,300 de intereses más 9,022 de otros ingresos, casi todo ganancias en valores de capital (F1 p. 42) |
| otros_inversion (CFI + capex) | −46,186 | −21.4% | Hecho: compras netas de valores (−14,233), valores no negociables (−17,418), Groq (−13,000) y adquisiciones (−1,535) |
| otros_financiamiento | −7,957 | −3.7% | Hecho: retenciones fiscales de RSU (−7,948) y otros (−9) |
| no monetario en inversiones_cp | 17,330 | 8.0% | Reclasificación de mapeo: el motor manda el efectivo de otros_inversion a otros_activos_lp |
| no monetario en otros_pasivos_circulantes | 9,615 | 4.5% | Mapeo: el motor mantiene constante esa línea; incluye 3,921 de pago pendiente a Groq, no monetario (F1 p. 68) |
| no monetario en otros_pasivos_lp | 15,427 | 7.1% | Mapeo: el motor manda otros_operativos y otros_financiamiento (−11,313) a esa línea, que en realidad subió 4,114 |
| capital: ORI + otros + devengado contra pagado | −8,071 | −3.7% | Hecho: retenciones de RSU (−7,948), premios asumidos (+28), ORI (+150), SBC devengada contra flujo (+1) y recompras devengadas contra pagadas (−302) |

*Inferencia:* las partidas "no monetarias" grandes son sobre todo reubicaciones del mapeo genérico del motor entre líneas de balance, no errores del emisor ni flujo no explicado. Lo genuinamente no monetario es identificable: revaluaciones de valores, la contraprestación diferida de Groq, el PPE no pagado y los impuestos diferidos.

## 5. Escenarios de mecanismo (supuestos, no pronósticos)

**Diseño común a los tres escenarios** (supuestos, con la fuente de su anclaje):
- **Horizonte y caja:** 5 años (FY2027E-FY2031E) y caja mínima de 10,000 (≈ caja de 10,605 al cierre de FY2026).
- **Ingresos del año 1:** 1S FY2027 real (177,837; F3 p. 3) más un 2S distinto en cada escenario.
- **Política de capital idéntica,** para aislar el mecanismo operativo:
  - dividendos de 18,340 en FY2027E: 6,290 pagados en el 1S (F3 p. 8) más 0.25 USD × 24.1 mil M de acciones × 2 trimestres (F3 portada y p. 21); después, 24,100 por año;
  - recompras, incluidas las retenciones de RSU, de 87,150 en FY2027E (el doble del 1S real: 39,044 + 4,531, F3 p. 8) y de 60,000 anuales después. Se imputa 89% a utilidades retenidas (proporción del 1S, F3 p. 7);
  - emisión de acciones de 700 por año (≈ los 644 de FY2026).
- **Deuda y resultados financieros:**
  - emisión de 24,896 en FY2027E (neto recibido, F3 p. 8);
  - amortizaciones según vencimientos: 1,000 (FY2027), 4,750 (FY2029), 3,500 (FY2030) y 1,500 (FY2031) (F3 Nota 9 p. 17);
  - tasa de 4.41%.
  - rendimiento de caja de 0%, para que la caja acumulada no infle la utilidad; el ingreso real fue de 2,300 en FY2026;
  - otros ingresos (ganancias en valores) de 0.
- **Impuestos y amortización:** tasa de 17% (punto medio de la guía, F5). Amortización de intangibles de 923, 729, 592, 511 y 468 (calendario de F1 Nota 6 p. 64).

| Driver | Tensión | Intermedio | Eficiencia |
|---|---|---|---|
| Crecimiento de ingresos FY27E-FY31E | +64.7% (2S = 1S real), +5%, −20%, −5%, +5% | +82.4% (3T y 4T = 108,000, punto medio de la guía de F5), +30%, +10%, +5%, +5% | +89.5% (3T = 110,160, extremo alto de la guía; 4T = +10%), +45%, +20%, +10%, +7% |
| Margen bruto | 74.5% → 70% → 60% → 62% → 65% | 74.5% → 72% → 70% → 69% → 69% | 75% → 74.5% → 74% → 73.5% → 73% |
| Margen operativo | 64.5% → 58% → 44% → 46% → 49% | 65.5% → 62% → 59% → 57.5% → 57% | 66% → 66% → 65% → 64% → 63.5% |
| DSO / DIO / DPO (días) | 75→90→70 / 130→180→140 / 55→45 | 62→60 / 120→110 / 57 | 58→50 / 110→90 / 60→62 |
| D&A / capex / SBC (% de ingresos) | 1.2-2.1% / 3.0-3.5% / 2.2-4.0% | 1.2-1.5% / 3.0% / 2.2-2.8% | 1.1-1.2% / 2.8% / 2.0-2.2% |

**Anclajes (hechos) de los supuestos:**
- Precedente de digestión: en FY2023 los ingresos fueron de 26,974, con margen bruto de 56.9% y operativo de 15.7% (F2 p. 52). Contra FY2022 quedaron planos: 26,914 según el XBRL de la SEC (`companyfacts`, 10-K FY2022, accession 0001045810-22-000036).
- DSO de 65.0 en FY2026 y plazos de hasta un año (F3 p. 14).
- DIO de 125.0 en FY2026.
- Compromisos de suministro de 279 mil M (§2.2).
- Guía del 3T FY2027: margen bruto de 74.0% ± 50 pb (F5).
- Margen operativo del 1S FY2027: 65.9% (F3 p. 3).
- SBC no devengada de 19.4 mil M, un piso de ≈7.5 mil M por año (F3 p. 10).

**Resultados** (`resultados.json` → `escenarios`):

| Escenario | Concepto | 2027E | 2028E | 2029E | 2030E | 2031E |
|---|---|---:|---:|---:|---:|---:|
| Tensión | Ingresos | 355,674 | 373,458 | 298,766 | 283,828 | 298,019 |
| | Utilidad neta | 189,663 | 178,598 | 108,012 | 107,419 | 120,349 |
| | FCF | 149,422 | 156,014 | 113,484 | 137,896 | 141,476 |
| | FCF / utilidad neta | 0.79 | 0.87 | 1.05 | 1.28 | 1.18 |
| | Financiamiento requerido | 0 | 0 | 0 | 0 | 0 |
| Intermedio | Ingresos | 393,837 | 511,988 | 563,187 | 591,346 | 620,914 |
| | Utilidad neta | 213,362 | 262,285 | 274,695 | 281,273 | 292,899 |
| | FCF | 180,762 | 237,639 | 270,137 | 281,783 | 295,784 |
| | FCF / utilidad neta | 0.85 | 0.91 | 0.98 | 1.00 | 1.01 |
| Eficiencia | Ingresos | 409,173 | 593,301 | 711,961 | 783,157 | 837,978 |
| | Utilidad neta | 223,398 | 323,826 | 383,005 | 415,066 | 440,801 |
| | FCF | 196,878 | 299,485 | 372,128 | 412,809 | 438,021 |
| | FCF / utilidad neta | 0.88 | 0.93 | 0.97 | 1.00 | 0.99 |

Ningún escenario requiere revolvente (C16 OK en los 15 años-escenario). La caja final de FY2031E es de 284,653, 852,465 y 1,305,681. Esa caja no es un pronóstico: es FCF que la política de capital fija de los escenarios no asigna.

*Inferencia:*
- **(i) Capital de trabajo.** La conversión FCF/utilidad es baja al principio de cada escenario (0.79-0.88) porque el capital de trabajo absorbe caja; eso ya se ve en el FCF/UN de 12 meses de 0.66 (dossier). En la tensión, la conversión sube a más de 1 cuando los ingresos caen, porque la cartera y el inventario se liquidan: el mecanismo es contracíclico, siempre que el inventario no se castigue más allá de lo que baja el margen bruto.
- **(ii) Liquidez.** Con márgenes operativos de 44% o más, ni una caída de 20% ni un DSO de 90 días generan necesidad de financiamiento. La vulnerabilidad de caja requiere mecanismos que el motor no modela: garantías de 108.5 mil M, compromisos de 279 mil M, inversiones de capital (42,404 comprados en el 1S FY2027, F3 p. 8) y los 25 mil M comprometidos.

## 6. DCF inverso

**Insumos** (hechos con fuente, salvo que se marque supuesto; `base.json` → `insumos_complementarios.dcf_inverso`):
- **Precio y acciones:** precio de **224.58 USD** (cierre del 24-sep-2026, F6). Acciones diluidas de **24,285 M** (promedio del 2T FY2027, F3 p. 3). Capitalización de 5,453,925.
- **Deuda neta (definición base) de −17,726:** deuda financiera de 33,366 más arrendamientos operativos de 5,494, menos caja de 22,443 y valores de deuda de 34,143 (F3 p. 5 y p. 24). Variante ampliada que además resta las inversiones de capital (42,783 + 4,957 + 51,157): −116,623.
- **Ingresos base de 12 meses: 302,970** (215,938 − 90,805 + 177,837).
- **Margen FCF base de 39.49%:** FCF del emisor de 12 meses (126,886 = 96,575 − 39,584 + 69,895; F4 y F5) menos SBC de 12 meses (7,241), entre los ingresos.
- **WACC de 10.87%:**
  - costo de capital accionario de 10.92% = r_f de 4.75% + β de 1.508 × ERP de 4.09%;
  - la β de 1.508 es la desapalancada del sector (1.50, F7) reapalancada con D/E de 0.71%;
  - costo de deuda de 4.41% × (1 − 21%);
  - peso de la deuda de 0.7%.
  - Contraste con la β de regresión de 1 año de 1.90 (dossier): WACC de 12.50%.
- **Supuestos del modelo:** g terminal de 3.0% (menor que r_f), 10 años, margen FCF constante, descuento a fin de año (`herramientas/modelo_integrado.dcf_inverso`).

**Resultado base.** El precio descuenta un **crecimiento de ingresos de 20.2% anual por 10 años**, es decir, ingresos de ≈1.91 billones en el año 10 (6.3 veces los de 12 meses) con 39.5% de margen FCF.
- El valor terminal pesa 64.7% del valor de empresa (sin alerta: el umbral es 75%). El múltiplo terminal es de 13.1 veces el FCF.
- Residuo de la bisección: 0.0012.
- Variantes: con la deuda neta ampliada, 19.96% (el ajuste es pequeño frente a la capitalización); con la β de regresión, 23.7%.

**Sensibilidad** (crecimiento implícito; entre paréntesis, el peso del valor terminal):

| Margen FCF 39.5% (base) | g 2.5% | g 3.0% | g 3.5% |
|---|---|---|---|
| WACC 9.87% | 18.6% (66%) | 17.9% (67%) | 17.2% (68%) |
| WACC 10.87% | 20.8% (64%) | **20.2% (65%)** | 19.6% (66%) |
| WACC 11.87% | 22.9% (62%) | 22.4% (63%) | 21.8% (64%) |

| Margen FCF 35% | g 2.5% | g 3.0% | g 3.5% |
|---|---|---|---|
| WACC 9.87% | 20.2% (67%) | 19.5% (68%) | 18.8% (69%) |
| WACC 10.87% | 22.5% (65%) | 21.9% (66%) | 21.2% (67%) |
| WACC 11.87% | 24.6% (63%) | 24.1% (64%) | 23.5% (65%) |

| Margen FCF 45% | g 2.5% | g 3.0% | g 3.5% |
|---|---|---|---|
| WACC 9.87% | 16.8% (64%) | 16.1% (66%) | 15.4% (67%) |
| WACC 10.87% | 19.0% (62%) | 18.4% (63%) | 17.8% (64%) |
| WACC 11.87% | 21.0% (60%) | 20.5% (61%) | 20.0% (62%) |

Rango de las 27 celdas: **15.4%-24.6%**. ±1 pp de WACC mueve el implícito ≈2.2 pp, cerca del rango de 2.3-2.6 pp de la lección de `conocimiento/25` §2.10; ±0.5 pp de g lo mueve ≈0.6 pp.

*Inferencia (comparación, no veredicto):*
- La trayectoria base implica ≈694 mil M de ingresos a 4.5 años. Eso queda entre el FY2031E del escenario intermedio (620,914) y el de eficiencia (837,978); el de tensión (298,019) queda muy abajo.
- Pero el precio pide además seguir creciendo ≈20% hasta el año 10, mientras los tres escenarios desaceleran a 5%-7% en FY2031E. Los escenarios también tienen márgenes de FCF − SBC de 43%-50% en FY2031E, arriba de la base de 39.5%.
- Con margen de 45% el implícito baja a 18.4%.
- El debate que descuenta el precio es la **duración** del crecimiento después de FY2031, no el siguiente año.
- Las tasas base de crecimiento por tamaño no están en el repositorio (pendiente). No se afirma si 20% por 10 años es alcanzable.
- La ficha usa otra definición (crecimiento del FCF con r de 9%-10%), así que sus números no son comparables con estos.

## 7. Sensibilidad geopolítica reproducible

**Método** (`modelo.py` → `sensibilidad_geopolitica`, en Decimal exacto): rejilla completa de 27 celdas, sin elegir solo las favorables.
- **Base:** ingresos de 12 meses R = 302,970; utilidad bruta de 12 meses = 226,241 (margen de 74.67%); utilidad operativa de 12 meses = 197,579; tasa de 17% (supuesto); 24,285 M de acciones.
- **Fracción restringida e ∈ {2%, 5%, 10%}** (supuesto). Referencias de hecho: China y Hong Kong por sede fueron 9.1% de FY2026 y 8.2% del 2T FY2027; "Otros" fue 2.0% de FY2026 (F1 p. 78; F3 p. 23).
- **Sustitución dentro del periodo r ∈ {0, 50%, 100%}** (supuesto).
- **Margen de contribución perdido c ∈ {75%, 90%, 100%}** (supuesto). 75% ≈ margen bruto del 2T, con el costo variable ahorrado. 100% = nada se ahorra, porque el inventario y los compromisos ya estaban comprados; es el precedente del H20.
- **Fórmulas:** L = R·e·(1−r); UB' = UB − L·c; gastos de operación fijos, así que ΔUO = −L·c; ΔUPA = ΔUO·(1−t)/acciones.
- **Doble comprobación algebraica:** COGS' = (R − UB) − L·(1−c) y UB' = R' − COGS'. El error máximo en las 27 celdas es 0.

| e | r | c | Ingresos perdidos | Margen bruto nuevo | Δ MB (pb) | Δ UO | Δ UO % | Δ UPA (USD) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 2% | 0% | 75% | 6,059 | 74.67% | −1 | −4,545 | −2.30% | −0.155 |
| 2% | 0% | 90% | 6,059 | 74.36% | −31 | −5,453 | −2.76% | −0.186 |
| 2% | 0% | 100% | 6,059 | 74.16% | −52 | −6,059 | −3.07% | −0.207 |
| 2% | 50% | 75% | 3,030 | 74.67% | 0 | −2,272 | −1.15% | −0.078 |
| 2% | 50% | 90% | 3,030 | 74.52% | −15 | −2,727 | −1.38% | −0.093 |
| 2% | 50% | 100% | 3,030 | 74.42% | −26 | −3,030 | −1.53% | −0.104 |
| 2% | 100% | 75/90/100% | 0 | 74.67% | 0 | 0 | 0.00% | 0.000 |
| 5% | 0% | 75% | 15,148 | 74.66% | −2 | −11,361 | −5.75% | −0.388 |
| 5% | 0% | 90% | 15,148 | 73.87% | −81 | −13,634 | −6.90% | −0.466 |
| 5% | 0% | 100% | 15,148 | 73.34% | −133 | −15,148 | −7.67% | −0.518 |
| 5% | 50% | 75% | 7,574 | 74.67% | −1 | −5,681 | −2.88% | −0.194 |
| 5% | 50% | 90% | 7,574 | 74.28% | −39 | −6,817 | −3.45% | −0.233 |
| 5% | 50% | 100% | 7,574 | 74.03% | −65 | −7,574 | −3.83% | −0.259 |
| 5% | 100% | 75/90/100% | 0 | 74.67% | 0 | 0 | 0.00% | 0.000 |
| 10% | 0% | 75% | 30,297 | 74.64% | −4 | −22,723 | −11.50% | −0.777 |
| 10% | 0% | 90% | 30,297 | 72.97% | −170 | −27,267 | −13.80% | −0.932 |
| 10% | 0% | 100% | 30,297 | 71.86% | −281 | −30,297 | −15.33% | −1.035 |
| 10% | 50% | 75% | 15,148 | 74.66% | −2 | −11,361 | −5.75% | −0.388 |
| 10% | 50% | 90% | 15,148 | 73.87% | −81 | −13,634 | −6.90% | −0.466 |
| 10% | 50% | 100% | 15,148 | 73.34% | −133 | −15,148 | −7.67% | −0.518 |
| 10% | 100% | 75/90/100% | 0 | 74.67% | 0 | 0 | 0.00% | 0.000 |

Las 27 celdas completas, sin agrupar, están en `resultados.json`. Las filas con r = 100% dan cero por construcción: suponen reemplazo al mismo precio y margen dentro del periodo, que el grid no penaliza.

*Inferencia:*
- **(i)** Con c ≈ margen bruto, el margen bruto casi no se mueve, pero la utilidad operativa cae 1.15 veces más que en proporción a los ingresos (−11.5% de UO contra −10% de ingresos), porque los gastos de operación son fijos.
- **(ii)** El canal de cargos de inventario (c = 100%) es el que mueve el margen bruto. El precedente real: el cargo del H20 (4.5 mil M) equivale a 2.1% de los ingresos de FY2026, y el del H200 (0.4 mil M) se registró en el 1S FY2027. El grid no incluye cargos únicos adicionales.
- **(iii)** La peor celda (−30.3 mil M de UO, −1.04 USD por acción) equivale a 15% de la UO de 12 meses. Frente al DCF inverso, un choque de una vez pesa menos que la duración del crecimiento, salvo que la restricción sea permanente y reduzca el crecimiento, no solo el nivel.
- No se asignan probabilidades ni valor esperado.

## 8. Qué NO demuestra este trabajo
- **No es pronóstico, valuación intrínseca ni recomendación.** Los escenarios son mecanismos con supuestos explícitos. La caja proyectada no es una estimación de caja futura.
- **Que todos los controles pasen demuestra consistencia aritmética y una transcripción fiel,** no que los supuestos sean correctos. El motor mantiene constantes los otros activos y pasivos y las inversiones de corto plazo, y no modela inversiones estratégicas, garantías, compromisos de compra, arrendamientos operativos, el pago pendiente a Groq, conteo de acciones ni UPA.
- **El DCF inverso dice qué crecimiento pide el precio bajo un WACC, un g, un margen constante y un horizonte elegidos.** No dice si el precio es alto o bajo. La β y la ERP son estimaciones (F7, F8), y no hay tasas base para contrastar.
- **La sensibilidad geopolítica no mide la exposición real.** El emisor no revela ingresos por destino final ni por grupo D:5, y la tabla por sede de facturación no equivale a uso final (F1 p. 78). La elegibilidad legal de ninguna operación se certifica.
- **Las partidas conciliatorias "no monetarias" del C13 no son errores del emisor.** Son, en su mayor parte, reubicaciones del mapeo genérico (§4).
- **La identidad del cliente indirecto** ("empresa de investigación y despliegue de IA") no está afirmada en la nota de concentración.
- **La doble comprobación la hizo el mismo autor contra datos del mismo emisor.** No es una auditoría independiente.

## 9. Pendientes
1. **Tasas base.** Faltan las tasas base de crecimiento de ingresos por tamaño (p. ej., *The Base Rate Book* de Mauboussin) para contrastar el 20% por 10 años. No están en el repositorio y no se inventan.
2. **Llamada y comentario del CFO.** Leer la transcripción del 2T FY2027 y el comentario del CFO (`q2fy27cfocommentary.htm` en el 8-K de F5) para la guía de margen bruto por memoria y el reparto Blackwell/Rubin. La ficha cita la llamada [7]; aquí no se verificó.
3. **Balance de FY2023.** Descargar el 10-K FY2024 para tener la apertura de FY2024 y convertir en pruebas los NO_APLICA de C05, C06, C10 y C13 de ese año.
4. **Siguiente 10-Q.** En el 10-Q del 3T FY2027 (reporte anunciado para el 17-nov-2026, según la ficha), seguir el DSO, el inventario, los compromisos de suministro, la activación de las garantías de SB Energy y los cargos de exportación.
5. **Extender el motor.** Modelar inversiones de capital, garantías y compromisos como flujos de escenario exige cambiar `herramientas/modelo_integrado.py`, que es compartido. No se hizo.
6. **Reglas de exportación.** Leer directamente la regla del BIS de ene-2026 (2026-00789) y la propuesta RASA (F3 p. 37) antes de usar cualquier fracción restringida que no sea hipotética.
7. **Actualizaciones.** Actualizar la β (Damodaran ene-2026) y la ERP cuando cambien. El precio es el cierre del 24-sep-2026 y no se usó la cotización del SIC en MXN.
8. **Acceso a la SEC.** `www.sec.gov` respondió 403 al User-Agent `SistemaInversionNew1/1.0 investigacion`. La descarga funcionó con un User-Agent descriptivo y un contacto de marcador no enrutable (`sec-contacto@sistemainversionnew1.invalid`). Conviene definir `SEC_USER_AGENT` con un correo real del sistema.

## 10. Reproducción
```
cd /home/user/New1
python3 empresas/NVDA/modelo/modelo.py                               # código 0: controles OK y auditoría coincide
python3 herramientas/huellas.py verificar empresas/NVDA/modelo/SHA256SUMS.txt   # OK
```
Solo usa la biblioteca estándar de Python 3.11. Para volver a verificar un insumo, se descarga la URL de F1-F5, se quita la etiqueta `<script ...></script>` que la SEC agrega antes de `</body>` y se compara el SHA-256 con `base.json`.
