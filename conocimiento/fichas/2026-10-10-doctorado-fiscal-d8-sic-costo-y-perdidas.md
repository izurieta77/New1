# Ficha · Doctorado derecho fiscal D8 · Ganancias en el SIC: costo promedio y pérdidas (LISR art. 129)

**Pregunta.** ¿Cómo se calcula la ganancia fiscal de una venta de acciones o ETF en el SIC para una persona física, y qué pasa con las pérdidas?

## Fuente y nivel de acceso
| Fuente | Acceso | Grado |
|---|---|---|
| LISR art. 129 (texto de Diputados, DOF 01-04-2024, SHA-256 803c2875c09c751c…), fracciones I a III, reglas a) y b) de cálculo, pérdidas | Lectura íntegra de los párrafos citados | A (texto) |
| Art. 16-C CFF (mercados reconocidos, que la fr. III exige) | Citado por el art. 129; no leído en esta ficha | nv |
| Reglas de la RMF 2026 sobre intermediarios y constancias | No leídas | nv |
| Criterio del SAT sobre activos virtuales (cripto) | No localizado; el texto de LISR y CFF no contiene las palabras "cripto" ni "activo virtual" (búsqueda exhaustiva en el texto de LISR, 0 coincidencias) | A (ausencia en el texto) |

## Derivación
1. **Alcance (fr. I a III):** la tasa de 10% definitivo aplica a acciones de sociedades mexicanas cotizadas en bolsa, a títulos que representan índices accionarios, y a acciones de sociedades extranjeras cotizadas en bolsas o mercados de derivados concesionados en México (fr. I y II); la fr. III extiende a bolsas de países con tratado para evitar la doble tributación, siempre que el mercado sea reconocido en los términos del art. 16-C fr. II CFF.
2. **Cálculo (regla a):** ganancia = precio de venta menos comisiones de venta, menos costo promedio de adquisición por título vendido. El costo promedio = (monto pagado por las compras + comisiones de compra) / número de títulos comprados, **actualizado** desde cada compra hasta el mes anterior a la venta.
3. **Determinación por emisora:** las ganancias y pérdidas se determinan **por cada sociedad emisora** o título de índice.
4. **Pérdidas:** la pérdida del ejercicio solo se disminuye contra la ganancia del mismo contribuyente en el ejercicio o en los **diez siguientes**, y únicamente por las operaciones de este mismo régimen. No se puede aplicar contra salarios ni contra otros ingresos.
5. **Intermediario:** la ganancia la calcula el intermediario que opera la cuenta, si el contribuyente le instruye hacerlo (texto del art. 129).

## Ejercicio (código: `fichas/codigo/2026-10-10-d8-sic-costo-promedio.py`)
- Compras: 10 títulos a 100 con comisión 2.50, y 10 a 120 con comisión 2.50. Costo promedio = 110.25 por título (sin actualización por INPC, que se omite aquí).
- Venta de 10 a 130 con comisión 3.25: **ganancia fiscal = 194.25** (1,300 − 3.25 − 1,102.50).
- Pérdida de 8,000 en 2026 y ganancia de 15,000 en 2027: se aplican 8,000 y la base gravable es 7,000 (la pérdida se agota dentro de los diez años).

## Contraejemplo
Una pérdida en una emisora no compensa la ganancia de otra si el texto determina la ganancia por emisora; la compensación entre emisoras del mismo ejercicio no está explícita en el texto de la regla (el texto dice "se determinará... por cada sociedad emisora"). Esta ficha no resuelve esa interpretación: queda como pregunta para el intermediario o un contador (nv).

## Límites
- No se incluye la actualización por INPC del costo promedio (regla a): el efecto depende de los índices del periodo de tenencia.
- No se leyó el art. 16-C CFF; para saber si una bolsa extranjera cumple la fr. III, hace falta esa lectura.
- Las constancias de intermediario y la RMF 2026 no se leyeron.
- La cripto no está en la LISR ni en el CFF de este texto: su tratamiento no se deduce de la ley y queda sin ficha.

## Estado nuevo
D8 pasa de **Parcial** a **Documentado con comprobación**: texto de art. 129 leído, reglas de costo y pérdidas probadas con código. Falta el art. 16-C CFF, la RMF 2026 y el criterio de compensación entre emisoras.
