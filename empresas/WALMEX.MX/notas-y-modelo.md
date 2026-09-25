# WALMEX.MX — Notas y modelo integrado (FASE 0, formación)

Fecha de corte: **2026-09-25**. Moneda: MXN millones salvo que se indique otra cosa. Wal-Mart de México,
S.A.B. de C.V. **no reporta ante la SEC**; toda la información primaria proviene de BMV/Emisnet y de
walmex.mx (Relación con Inversionistas). Este documento y el modelo que describe están en **FASE 0
(formación)**: no contienen ni implican recomendación de compra o venta. Los escenarios de la sección 4 son
supuestos explícitos de **mecanismo**, no pronósticos, guía del emisor ni consenso.

Archivos de este trabajo:
- `empresas/WALMEX.MX/modelo/datos/` — 21 documentos primarios congelados, con huellas SHA-256 en
  `datos/SHA256SUMS.txt` (verificado OK el 2026-09-25).
- `empresas/WALMEX.MX/modelo/modelo.py` — script que transcribe, reconcilia, proyecta 3 escenarios y corre
  el DCF inverso. Reproducible con `python3 empresas/WALMEX.MX/modelo/modelo.py`.
- `empresas/WALMEX.MX/modelo/base.json` — histórico FY2024, FY2025 y 1S2026, con `fuentes_campos` citando
  documento y nota/página por partida.
- `empresas/WALMEX.MX/modelo/resultados.json` — salida completa (controles, reconciliación, escenarios, DCF).
- `empresas/WALMEX.MX/modelo/SHA256SUMS.txt` — huellas de `base.json`, `modelo.py` y `resultados.json`.

No se editó `empresas/WALMEX.MX/ficha.md` ni `pronosticos.csv` (los maneja otro proceso).

---

## 1. Fuentes primarias

| Id | Documento | Fecha | Uso principal |
|---|---|---|---|
| F1 | Informe Anual 2025 (Reporte Anual BMV/Emisnet; estados financieros auditados NIIF 2025/2024) | 2026 | Notas 8, 9, 12, 14/23, 15, 18, 22; balance y flujo detallados |
| F2 | Estados Financieros 4T25 estructurados (hoja de cálculo, BMV) | 2026-02-18 | Balance dic-25/dic-24, flujo anual, P&L trimestral 2024-2025 |
| F3 | Reporte trimestral 2T26 (BMV, formato NIIF con notas) | 2026-07 | Nota de arrendamientos, segmentos, capital social, COFECE (actualización) |
| F4 | Estados Financieros 2T26 estructurados (hoja de cálculo, BMV) | 2026-07 | Balance jun-26/jun-25, flujo de 6 meses, P&L T1-T2 2026 |
| F5 | Earnings Release 4T25 (inglés) | 2026-02-18 | Segunda lectura independiente de totales anuales |
| F6 | Informe Anual 2025 — Resumen Financiero 2015-2025 (pág. 61-62) | 2026 | Segunda lectura independiente de totales anuales, 10 años de historia |
| F7 | Programa de Inversión 2026 y Propuesta de Dividendos (comunicado Walmex Day) | 2026-03-25 | Capex guiado 2026, dividendo propuesto, tope de recompra |
| F8 | Yahoo Finance WALMEX.MX | 2026-09-25 | Precio de cierre para el DCF inverso |
| F9/F10 | A. Damodaran — Betas por industria (emergentes / global) | 2026-01-07 | Beta desapalancada, "Retail (Grocery and Food)" |
| F11 | A. Damodaran — Country default spreads and ERP | 2026-07-01 | CRP México, ERP madura EUA |

Huellas SHA-256 de los 21 archivos: `empresas/WALMEX.MX/modelo/datos/SHA256SUMS.txt` (`huellas.verificar()` → **OK**, sin fallas).

---

## 2. Hallazgos de nota — hecho (con página) vs. inferencia

**Hechos (documento y página/nota citados; cero inferencia):**

- Activo total dic-2025 **$495,273,263 miles**; pasivo total **$259,693,202 miles**; capital contable
  **$235,580,061 miles** — F1, Estado de Situación Financiera Consolidado (INFORME 2025, sección Estados
  Financieros Consolidados); mismas cifras en F2 hoja "Balance sheet".
- Pasivo por arrendamiento neto dic-2025 **$80,848,147 miles** (dic-2024 $79,729,903 miles) — F1 Nota 9,
  "Los pasivos por arrendamiento se integran como sigue" (INFORME 2025 p. 192).
- Pasivo por arrendamiento LP dentro de "Leases and other long-term liabilities" dic-2025: **$75,661,205
  miles**; el resto de ese rubro ($8,327,097 miles) son ISR LP ($6,072,263), ingreso diferido por rentas
  ($2,202,768), partes relacionadas LP ($38,889) y otros ($13,177) — F1 Nota 15 (INFORME 2025 p. 196-197).
- Multa de COFECE a una subsidiaria de WALMEX: **$93.4 millones de pesos** (≈USD 5 millones), resuelta el
  12-dic-2024 por una práctica monopólica relativa sobre contribuciones de proveedores; WALMEX impugnó por
  amparo indirecto el 6-ene-2025 — F1 Nota 23 (p. 205) y F3 (Reporte 2T26, Nota B, actualiza que sigue en
  litigio a jun-2026, sin cambio de estatus).
- Operaciones con partes relacionadas FY2025: compras/comisiones de importación con C.M.A.-U.S.A., LLC y
  WMGS Commercial Services Limited **$7,519,858 miles**; asistencia técnica, servicios y regalías con
  Walmart Inc. **$11,523,698 miles** (accionista mayoritario vía Intersalt, S. de R.L. de C.V., **71.20%**
  de participación) — F1 Nota 1 y Nota 14b (p. 205-206).
- Capex por país FY2025: México **$33,291,269 miles**, Centroamérica **$5,690,686 miles** (consolidado
  $38,981,955 miles, cash flow "Long-lived assets") — F1 Nota 22 (p. 208).
- Programa de Inversión 2026: capex guiado **~$43,000 millones** (+10% vs. 2025); dividendo ordinario
  propuesto **$1.16/acción** (dos pagos de $0.58, 18-nov y 9-dic-2026); tope de recompra **$10,000
  millones**; dividendo extraordinario "por determinar" sobre el remanente del presupuesto de recompra no
  ejercido al 30-nov-2026 — F7 (comunicado 25-mar-2026).
- Acciones en circulación: 17,292,211,803 a dic-2025 (F6 p. 61-62, "Número de acciones en circulación
  (millones) 17,292"); **17,220,231,803** a jun-2026, sin efecto dilutivo (F3 p. 34 y p. 81, "no existen
  efectos dilutivos inherentes a las acciones ordinarias potenciales").
- Segmentos jun-2026 (1S): utilidad de operación México $30,571,773 miles, Centroamérica $4,919,487 miles
  — F3 p. 61.
- Evento subsecuente: en febrero de 2026 el BAPA (Bilateral Advance Pricing Agreement) entre México y
  Estados Unidos fue ratificado para 2023-2029, confirmando metodología de precios de transferencia con
  Walmart Inc. — F1 Nota 24 (p. 209).

**Inferencia (cálculo propio, señalado explícitamente):**

- *Inferencia:* la descomposición de "Leases and other long-term liabilities" y "Other accounts payable" en
  `arrendamientos_financieros` / `otros_pasivos_lp` / `otros_pasivos_circulantes` (ver `modelo.py
  mapear_balance`) se construyó a partir de las notas citadas arriba; **se verificó por cuadre exacto**
  contra el pasivo total publicado en los tres periodos (dif. = 0 en los tres casos; `_check_balance` en
  `modelo.py`), no es un residuo sin comprobar.
- *Inferencia:* `gastos_operativos` del motor = Gastos Generales − Otros Ingresos + Otros Gastos (neto), no
  una línea publicada tal cual; se define así para que Utilidad Bruta − `gastos_operativos` = Utilidad de
  Operación (control C15), y coincide exactamente con las cifras publicadas en F5/F6.
- *Inferencia:* para 1S2026 el desglose de "Leases and other long-term liabilities" en arrendamiento LP +
  otros se obtuvo por diferencia contra el pasivo total por arrendamiento de la nota de arrendamientos del
  trimestre ($83,098,100 miles), porque el reporte trimestral condensado no trae el detalle por partida que
  sí trae la Nota 15 anual. Se verificó por el mismo cuadre exacto contra el pasivo total.
- *Inferencia:* el ISR devengado implícito (para separar "otros_operativos" del flujo) se calculó como
  Income before income taxes − Consolidated net income del mismo estado de flujos (no es una línea
  publicada directamente, pero reproduce el CFO reportado exactamente en los tres periodos).
- *Inferencia:* WACC, beta relevered, CRP y r_f en MXN (sección 5) son estimaciones de mercado con insumos
  citados (Damodaran, FRED), no hechos del emisor.
- *Inferencia:* los tres escenarios de la sección 4 son supuestos de mecanismo elegidos por el analista, no
  guía del emisor ni consenso (el único input directo del emisor es el capex 2026 guiado de F7, usado solo
  como ancla de orden de magnitud para `capex_ventas`).

---

## 3. Histórico transcrito (drivers implícitos, calculados sobre hechos)

| | FY2024 | FY2025 | 1S2026 (6 meses) |
|---|---:|---:|---:|
| Ingresos totales | 958,507.5 | 1,011,597.9 | 495,966.3 |
| Utilidad bruta / ingresos | 24.15% | 24.24% | 24.14% |
| Utilidad operativa / ingresos | 8.07% | 7.76% | 7.16%¹ |
| Tasa efectiva de impuestos | 21.91% | 27.57% | 23.53% |
| Días de cuentas por cobrar | 9.47 | 9.61 | — |
| Días de inventario | 55.57 | 51.17 | — |
| Días de proveedores | 61.23 | 59.01 | — |
| Capex / ingresos | 3.63% | 3.85% | 2.36%¹ |
| D&A / ingresos | 2.36% | 2.47% | 2.65%¹ |
| FCF (CFO − capex) | 37,871.7 | 43,455.8 | 11,580.4 |
| FCF después de arrendamientos (− pago total de renta) | 25,516.6 | 30,170.3 | 4,639.8 |
| Margen FCF después de arrendamientos | 2.66% | 2.98% | 0.94%¹ |

¹ 1S2026 es un periodo de **6 meses, no anualizado**; los "días" de capital de trabajo no se calcularon
para este periodo porque dividir un saldo final entre un flujo semestral y multiplicar por 365 los
infla ~2x (104-111 días "implícitos" vs. ~51-61 anuales) — es un artefacto de la ventana, no un cambio real
de política. Ver sección 6.

**Arrendamientos IFRS 16** (peso relevante en el balance de WALMEX, sin deuda financiera): el pasivo por
arrendamiento pasó de $79,730M (dic-24) a $80,848M (dic-25) a $83,098M (jun-26); interés implícito ≈
11.35% (interés FY2025 $9,115M / saldo promedio $80,289M — moneda mixta MXN/CA). El activo por derecho de
uso (dentro de `ppe_neto` en el motor) representa **~24-25% del PPE+ROU consolidado** en los tres periodos.
Nuevos contratos + modificaciones: $7,070M (2024) y $7,500M (2025), Nota 9.

**Capital de trabajo**: WALMEX opera con **proveedores > inventarios** (59-61 días de proveedores contra
51-56 días de inventario y ~9.5 días de cuentas por cobrar), es decir financia parte de su capital de
trabajo con el crédito de proveedores — rasgo estructural de un retailer de autoservicio de alta rotación.

---

## 4. Escenarios de mecanismo (supuestos explícitos, NO pronósticos)

Los tres escenarios parten de los drivers implícitos FY2025 (sección 3) y aplican un **mecanismo** distinto
durante 5 años (2027E-2031E). No representan probabilidad, consenso ni guía del emisor.

### 4.1 Tensión — consumo débil sostenido
Motivado por el propio lenguaje del emisor en 2T26 ("el entorno de consumo continúa siendo débil", F3):
crecimiento de ingresos 2.0%, compresión de margen bruto a 23.7% (más promocionalidad), margen operativo
7.0%, tasa de impuestos 30% (estatutaria plena), capex/ventas 3.5% (recorte defensivo), días de proveedores
comprimidos a 55 (menor poder de negociación tras el litigio de COFECE), costo de arrendamientos al 11.5%,
payout de dividendos 45%, recompras en pausa.

### 4.2 Intermedio — continuidad de la tendencia 2024-2025
Crecimiento 4.5% (entre el 5.6% de FY2025 y el 8.1% de FY2024, con desaceleración), márgenes ~estables
(bruto 24.2%, operativo 7.8%), capex/ventas 4.0% (cerca de la guía 2026 de F7), días de capital de trabajo
similares al histórico reciente, payout 58%, recompras $8,000M/año.

### 4.3 Eficiencia — aceleración de e-commerce y automatización
Ligado al Programa de Inversión 2026 (F7): nuevos Centros de Distribución automatizados en Guanajuato y
Tlaxcala (2027), 24% del capex a cadena de suministro. Crecimiento 7.0%, margen bruto 24.6%, margen
operativo 8.5% (apalancamiento operativo), capex/ventas 4.3%, mejor negociación con proveedores (63 días),
menor inventario (48 días, "visibilidad de inventario en tiempo real"), payout 60%, recompras $10,000M/año
(tope guiado 2026).

### Tabla resumen (2031E, quinto año de cada escenario)

| Concepto (2031E) | Tensión | Intermedio | Eficiencia |
|---|---:|---:|---:|
| Ingresos | 547,586.9 | 618,064.3 | 695,618.4 |
| Utilidad operativa | 38,331.1 | 48,209.0 | 59,127.6 |
| Utilidad neta | 17,968.9 | 25,376.1 | 32,820.7 |
| CFO | 32,076.2 | 40,707.3 | 50,012.2 |
| Capex | 19,165.5 | 24,722.6 | 29,911.6 |
| FCF después de arrendamientos | 12,910.7 | 15,984.7 | 20,100.6 |
| Dividendos + recompras | 8,086.0 | 22,718.1 | 29,692.4 |
| Financiamiento requerido (revolvente) | 0.0 | 5,775.1 | 9,591.8 |
| Caja final | 64,017.9 | 20,000.0 | 20,000.0 |
| Deuda neta (arrendamientos − caja) | — | 108,873.2 | 124,132.8 |

Nota mecánica: en **intermedio** y **eficiencia**, el revolvente se activa en 2030E-2031E porque
`caja_minima` ($20,000M) se agota — la caja se consume por el ritmo de dividendos+recompras+capex+nuevos
arrendamientos superando al FCF generado; en **tensión** no se activa porque el payout y capex caen más que
el FCF. Esto es "financiamiento requerido" explícito del motor (sin plug de balance), no una predicción de
endeudamiento real. El crecimiento del pasivo por arrendamiento (`nuevos_arrendamientos_financieros`:
$6,000/8,000/10,000M por año, calibrado contra el ritmo histórico de ~$7,000-7,500M/año de Nota 9) es el
principal motor del crecimiento de "deuda neta" en los tres escenarios — refleja el crecimiento físico de
tiendas, no apalancamiento financiero (WALMEX sigue sin deuda financiera en los tres escenarios).

---

## 5. DCF inverso

**Insumos explícitos** (todos declarados en `resultados.json.dcf_inverso.insumos`):

| Insumo | Valor | Fuente |
|---|---:|---|
| Precio de cierre | $45.81 MXN | Yahoo WALMEX.MX, cierre 2026-09-23 (último cierre disponible al 2026-09-25; F8) |
| Acciones en circulación | 17,220.231803 millones | F3 p. 34, a jun-2026; sin dilución (F3 p. 81) |
| Capitalización de mercado | $788,858.8M | precio × acciones |
| Ingresos base (TTM a jun-2026) | $1,020,335.8M | FY2025 − 1S2025 + 1S2026 |
| Caja (jun-2026) | $30,118.3M | F4 |
| Arrendamientos IFRS16 (jun-2026) | $83,098.1M | F3, nota de arrendamientos |
| Deuda neta (arrendamientos como deuda) | $52,979.8M | arrendamientos − caja |
| Deuda neta (sin arrendamientos) | −$30,118.3M | −caja (WALMEX no tiene deuda financiera) |
| WACC (caso base, arrendamientos como deuda) | **12.87%** | ver abajo |
| g terminal | **4.5%** | supuesto explícito (rango de sensibilidad 3.0%-5.5%) |
| Margen FCF (FY2025, después de arrendamientos) | **2.98%** | = control C12 del histórico |
| Horizonte | 10 años | supuesto |

**Costo de capital**: beta desapalancada "Retail (Grocery and Food)" en mercados emergentes = 0.8562
(Damodaran, corregida por caja, F9); relevered con arrendamientos como única deuda (D/E ≈ 10.5%) → beta =
0.9194. r_f USD = DGS10 5.11% (FRED, 2026-09-23); ERP madura EUA = 4.42% (Damodaran, F11); CRP México =
2.72% (ajustada por volatilidad relativa, F11). Ke_USD = 11.89%; convertida a MXN por diferencial de
inflación esperada (México 3.7% —inflación realizada 2025, F6, usada como proxy explícito de la esperada—
vs. EUA 2.33%, breakeven 5 años T5YIE): **Ke_MXN = 13.39%**. Kd de arrendamientos = interés implícito FY2025
= 11.35% (interés Nota 9 / saldo promedio). **WACC = 12.87%** (peso de capital 90.5%).

**Resultado del DCF inverso (caso base)**: al precio de $45.81, con WACC 12.87%, g terminal 4.5% y margen
FCF 2.98%, el **crecimiento anual constante de ingresos que el mercado está descontando durante 10 años es
≈ 15.8%** (estado OK, peso del valor terminal 58.3%, múltiplo terminal FCF ≈ 12.5x, residuo de la bisección
≈ $0.0002M — solución numéricamente exacta).

**Hallazgo relevante**: 15.8% es **2 a 8 veces el crecimiento histórico reciente** (5.6% en FY2025, 8.1% en
FY2024) y también supera el crecimiento del escenario más optimista construido aquí (7.0%, "eficiencia").
Las variantes de sensibilidad no cambian esta conclusión cualitativa:

| Variante | Crecimiento implícito |
|---|---:|
| Caso base (arrendamientos como deuda) | 15.80% |
| Sin arrendamientos como deuda (deuda neta = −caja) | 14.80% |
| Beta global en vez de emergentes | 14.32% |
| Margen FCF promedio 2024-2025 (2.82%) | 16.58% |
| g terminal 3.0% | 17.25% |
| g terminal 5.5% | 14.66% |
| WACC −100pb (11.87%) | 13.73% |
| WACC +100pb (13.87%) | 17.75% |

En **ningún** escenario de sensibilidad razonable el crecimiento implícito baja de ~13-14%. Esto sugiere
que, con un margen FCF constante igual al histórico reciente (~3%), el precio actual exige que WALMEX
sostenga un crecimiento de ingresos muy superior a su historia de los últimos 3 años — o bien que el mercado
esté descontando una **expansión de margen FCF** (vía apalancamiento operativo, menor capex/ventas en el
largo plazo, o crecimiento del negocio inmobiliario/publicitario de mayor margen) que este DCF, con margen
constante, no captura. Esto es una observación descriptiva de lo que implica el precio bajo estos supuestos,
**no una señal de compra o venta**.

---

## 6. Qué NO demuestra este modelo

- **No hay cruce independiente tipo XBRL/visor** (como en modelos de emisores que reportan ante la SEC):
  WALMEX no está sujeto a EDGAR, así que la "doble comprobación" aquí es (a) cuadre aritmético exacto de
  cada partida derivada contra los totales publicados, y (b) una segunda lectura manual de 32 cifras clave
  contra dos documentos distintos del propio emisor (F5 earnings release en inglés y F6 tabla resumen del
  Informe Anual). Ambos documentos son del mismo emisor: no es una auditoría externa independiente.
- **Los "días" de capital de trabajo de 1S2026 no son comparables directamente** a los anuales (ver nota¹ en
  la sección 3): son un artefacto de dividir un flujo semestral entre 365 días.
- **movimientos_ppe y movimientos_arrendamientos no están disponibles para 1S2026** (el reporte trimestral
  condensado no trae el roll-forward detallado de la Nota 8/9 anual): los controles C05/C06 quedan en INFO
  para ese periodo, no FALLA, pero no hay verificación línea-por-línea de esas partidas en el semestre.
- **No hay `movimientos_capital`** en ningún periodo (no se transcribió el Estado de Variaciones en el
  Capital Contable completo): C03/C04 corren en INFO cuando hay periodo previo y NO_APLICA en el primero.
  La reconciliación del histórico (C13) muestra residuos de "capital: movimientos no identificados" de hasta
  −3.3% de ingresos en 1S2026 (marcado ALERTA de materialidad por el motor) — es una partida conciliatoria
  explícita, no una cifra oculta, pero significa que el modelo no reconstruye el detalle de ORI, SBC y otros
  movimientos de capital mes a mes.
- **El DCF inverso usa un margen FCF constante** durante 10 años; no modela la trayectoria de margen que
  cada escenario de mecanismo (sección 4) sí produce año por año. El "puente" entre escenarios y DCF (qué
  crecimiento implicaría cada escenario con su propio margen) no se construyó en esta entrega.
- **Beta, ERP, CRP e inflación esperada de México son estimaciones de mercado** (Damodaran, breakeven de
  EUA, inflación realizada de México como proxy de la esperada), no hechos del emisor ni consenso de
  analistas: son insumos explícitos y sensibles (ver tabla de variantes, sección 5).
- **La tasa libre de riesgo en pesos (rf_mxn ≈ 6.5%) es derivada** (paridad de tasas de interés aproximada),
  no un M-bono a 10 años leído directamente (Banxico SIE requiere token, ver `herramientas/README.md`); el
  proxy de CETES 28d de FRED (`INTGSTMXM193N`, 6.23% en jul-2026) es consistente en magnitud pero no es el
  mismo insumo.
- **El resultado del litigio de COFECE no está modelado como escenario financiero**: la multa ($93.4M) es
  inmaterial (~0.01% de ingresos FY2025), pero las "medidas" que la resolución impone sobre negociación con
  proveedores podrían afectar días de proveedores o costo de ventas de forma no cuantificada aquí; el modelo
  no incorpora esa vía de transmisión.
- **Nada de este documento es una recomendación de compra o venta**, guía de precio objetivo, ni pronóstico
  puntual. Los escenarios son mecanismos; el DCF inverso es una lectura de lo que el precio implica bajo
  supuestos declarados, no una tesis de inversión.

---

## Verificación (2026-09-25)

**FASE B — auditoría independiente sobre el propio trabajo (mismo agente, segundo rol):**

1. **Huellas SHA-256 de `datos/`** (`herramientas/huellas.py verificar`): **OK**, 21/21 archivos, sin
   fallas.
2. **Recotejo directo contra el documento fuente** (no solo contra la segunda lectura F5/F6 programada en
   `modelo.py`): se verificaron con `grep` **25 cifras** de `base.json`/`modelo.py` contra el texto extraído
   de los PDF originales (activo total, pasivo total, capital contable de FY2024 y FY2025; pasivo por
   arrendamiento neto y LP de FY2024/FY2025; "leases and other LT liabilities"; multa COFECE en dos
   documentos distintos —Informe Anual y reporte 2T26—; ventas netas, utilidad bruta, utilidad operativa,
   EBITDA, utilidad neta, dividendo pagado y capex FY2025 de la tabla resumen; acciones en circulación
   dic-2025 y jun-2026; dividendo propuesto, capex guiado y tope de recompra 2026). **23/25 encontradas por
   coincidencia textual exacta**; las 2 restantes (capex del archivo `.xlsx`, que no es texto plano; y
   "17,292" con espaciado OCR "17 ,292") se confirmaron por lectura directa del archivo y por búsqueda
   ajustada al artefacto de OCR, respectivamente. **Ninguna discrepancia real encontrada.**
3. **Doble comprobación programática** (`modelo.py doble_comprobacion`, corrida dentro de
   `modelo.py main()`): 32 cifras anuales (FY2024 y FY2025) comparadas contra una segunda transcripción
   manual independiente de F5 (Earnings Release, inglés) y F6 (tabla resumen del Informe Anual) —
   **32/32 OK** (tolerancia de tres cifras significativas de redondeo a millones).
4. **`herramientas.modelo_integrado.verificar()` sobre `resultados.json` releído del disco**: recalcula los
   **541 controles** (16 tipos, histórico + 3 escenarios) desde cero, sin usar variables internas del motor.
   Resultado: **OK 513, FALLA 0, INFO 23, NO_APLICA 5 — coincide exactamente** con el resumen guardado en el
   momento de construir el modelo (`auditoria == resumen_controles` para total/OK/FALLA/INFO/NO_APLICA).
5. **`resumen_controles.todos_ok` = True** (ningún control en estado FALLA, en histórico ni en los tres
   escenarios).
6. **DCF inverso**: solución numérica exacta (`estado: OK`, residuo ≈ $0.0002M sobre un valor de empresa de
   ~$842,000M — error relativo ≈ 2.4×10⁻¹⁰), con WACC, g terminal y margen FCF explícitos y una rejilla de
   sensibilidad de 63 combinaciones (todas con solución OK dentro de los límites de búsqueda).
7. `python3 empresas/WALMEX.MX/modelo/modelo.py` termina con **código de salida 0** (todos los controles OK,
   huellas OK, doble comprobación OK, auditoría de `resultados.json` releído coincide).

**Conclusión de la verificación**: los controles pasan en su totalidad (0 FALLA de 541), la doble
comprobación de cifras (32 vs. segunda lectura programática + 25 vs. grep directo al documento fuente) no
encontró discrepancias, y las huellas de los documentos congelados son íntegras. Las limitaciones declaradas
en la sección 6 son de **alcance** (qué no se construyó: movimientos de capital completos, cruce tipo
XBRL, vía de transmisión de COFECE), no de **cifras incorrectas encontradas y sin resolver**.
