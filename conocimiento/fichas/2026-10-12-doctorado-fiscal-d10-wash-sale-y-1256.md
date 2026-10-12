# Ficha · 12-oct-2026 · Doctorado fiscal D10: venta ficticia (IRC §1091) y contratos 1256 (60/40)

> Laboratorio del lunes (REGLAS §0d: lunes, miércoles y viernes, tema doctoral). D10 estaba en "Localizado" (solo PFIC). Esta ficha cubre dos de sus cuatro piezas: *wash sale* y contratos 1256. Queda la venta ficticia en sentido amplio (*constructive sale*, §1259).

## 1. Pregunta

¿Qué dicen exactamente el §1091 y el §1256 del Código de Rentas Internas de EUA, cómo cambian el resultado fiscal de una operación y si le aplican a un residente fiscal en México que invierte por el SIC o por una cuenta en EUA?

## 2. Fuente y acceso

- **26 U.S.C. §1091** y **§1256**, texto en LII (Cornell Law School), leído el 12-oct por fragmentos citados literalmente (la herramienta limita la cita; el resto es resumen fiel). Grado **A** en lo citado; el texto íntegro de la página no se transcribió.
- **No verificado:** tasas vigentes (IRC §1(h) y tabla ordinaria) y los reglamentos del Tesoro (§1.1091-1). Las tasas del ejercicio son **parámetros ilustrativos**.

## 3. Lo que dice la ley

**§1091(a), venta ficticia (*wash sale*).** Si alguien vende acciones o valores con pérdida y, en los **30 días anteriores o posteriores** a la venta, adquiere (o contrata u obtiene opción para adquirir) **"substantially identical stock or securities"**, "no deduction shall be allowed under section 165". Hay excepción para *dealers* en el curso ordinario de su negocio. La definición incluye "contracts or options to acquire or sell stock or securities".

**§1091(d), base.** La base de lo recomprado es "the basis of the stock or securities so sold or disposed of", "increased or decreased … by the difference" entre el precio de recompra y el de venta. **La pérdida no se pierde: se difiere** a la base nueva.

**§1256(a), contratos 1256.**
- (a)(1) Cada contrato 1256 abierto al cierre del año "shall be treated as sold" a valor de mercado del último día hábil: **marcar a mercado** anual.
- (a)(3) La ganancia o pérdida es **40% de corto plazo y 60% de largo plazo**, sin importar cuánto se haya tenido.

**§1256(b), qué es un contrato 1256:** futuros regulados, contratos de divisas, opciones no sobre acciones (*nonequity options*, como las de índices amplios), *dealer equity options* y *dealer securities futures contracts*. **(b)(2)(B)** excluye swaps de tasa, de divisa, de base, *caps*, *floors*, de materias primas, de acciones, de índices de acciones, *credit default swaps* y similares.

## 4. Ejercicio (código: `codigo/2026-10-12-d10-wash-sale-1256.py`, con aserciones)

**Venta ficticia.** Compra 100 acciones en 5,000; vende en 4,000 (pérdida de 1,000); recompra dentro de 30 días en 4,200.
- Pérdida no deducible: **1,000**.
- Base nueva: 5,000 + (4,200 − 4,000) = **5,200**, que es lo mismo que 4,200 + 1,000 diferidos.
- Si después vende en 4,800: pérdida reconocida de **400** (1,000 diferidos menos 600 de alza). Comprobado.

**60/40.** Con tasas ilustrativas de 20% (largo) y 37% (corto), la tasa combinada de un contrato 1256 es 0.6 × 20% + 0.4 × 37% = **26.8%**, contra 37% de una ganancia de corto plazo ordinaria. Es la razón por la que los futuros de índice son más eficientes fiscalmente en EUA que comprar y vender el ETF en pocos días.

## 5. ¿Le aplica al dueño? (inferencia, D)

- Como con el PFIC (ficha del 9-oct), estas reglas gravan a **contribuyentes de EUA**. Un residente fiscal en México sin condición de *US person* no presenta declaración de ganancias de capital en EUA por ventas de acciones en bolsa; en general, solo puede haber retención en la fuente sobre dividendos. La ganancia la grava México (LISR 129 en el SIC; 4-B y 176-178 si aplica el régimen preferente).
- **Lo que sí sirve:** entender por qué los precios y los volúmenes de cierre de año de EUA se mueven (ventas para cosechar pérdidas antes del 31-dic, restringidas por la ventana de 30 días) y por qué los futuros y las opciones de índice tienen ventaja fiscal para el inversionista de EUA.
- **Pendiente:** verificar si la LISR tiene una regla mexicana equivalente para recompras dentro de un plazo (no la encontré en la lectura del art. 129 del 10-oct; falta una búsqueda dirigida).

## 6. Contraejemplo y límites

- *"Substantially identical"* no está definido en el texto leído: dos ETF de distintos emisores que siguen el mismo índice (p. ej., SPY y VOO) son un caso gris que depende de reglamentos y criterios del IRS, no del artículo.
- El ejercicio ignora la regla de tenencia (el periodo de tenencia de la acción vendida se suma al de la recomprada, §1223) y la de compras parciales.

## 7. Estado nuevo

D10: de **Localizado** a **Documentado** (PFIC del 9-oct + §1091 y §1256 con ejercicio comprobado). Falta §1259 (*constructive sale*) y verificar las tasas.
