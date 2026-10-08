# Ficha · Doctorado derecho fiscal D7 · Fondos y valores extranjeros para una persona física residente en México

**Pregunta.** Si un residente en México compra un ETF de EUA (p. ej. IBIT o SPY) en una cuenta de EUA, ¿qué regla de la LISR le aplica? ¿Y si lo compra en BMV/SIC?

## Fuente y nivel de acceso
| Fuente | Acceso | Grado |
|---|---|---|
| LISR, texto de Diputados, última reforma DOF 01-04-2024 (PDF completo, 3.0 MB, SHA-256 803c2875c09c751c…), arts. 1, 2, 129, 176 | Lectura del artículo íntegro | A (texto) |
| Art. 129 (10% definitivo sobre enajenación de acciones en bolsas de valores concesionadas o mercados de derivados reconocidos) | Íntegro | A |
| Art. 176 (regímenes fiscales preferentes) | Primer párrafo y la regla de 75% | A |
| Prohibición de la BMV/BIVA a fondos extranjeros con cripto (dato del dueño, 8-oct) | **No localizada** en búsqueda pública; no se usa | nv |
| Reglamento y resoluciones de la CNBV | No leídos | nv |

## Derivación
1. **Art. 1 fr. I:** los residentes en México pagan ISR por **todos sus ingresos, cualquiera que sea la ubicación de la fuente de riqueza**. Un ETF de EUA no sale de la base del impuesto por estar en otra cuenta.
2. **Art. 129 fr. I:** la tasa plana de 10% aplica a la enajenación de acciones **de sociedades extranjeras cotizadas en bolsas de valores o mercados de derivados concesionados en México**. Un ETF comprado en Nueva York no cumple esa condición; por texto, **no entra al 10%** y tributa por la tarifa progresiva del art. 96/152 como ingreso ordinario (inferencia de texto, grado B).
3. **Art. 176 (regímenes fiscales preferentes):** si el vehículo es una **entidad extranjera** en la que el residente participa, y esa entidad no paga en su país al menos el 75% del ISR que pagaría en México, el ingreso se acumula **aunque no se distribuya**. Un ETF registrado en EUA es un vehículo de inversión; si tiene personalidad jurídica propia, **la discusión es si entra al régimen**. Este es el punto que requiere contador (inferencia de texto, grado C).
4. **Inclusión de ingresos de fondos:** el propio texto del art. 1 y del Título V considera figuras extranjeras a los fondos de inversión "siempre que no tengan personalidad jurídica propia". Un ETF de EUA típico tiene estructura de trust o company; la clasificación depende del vehículo específico (inferencia, grado C).

## Ejercicio (cálculo ilustrativo, sin Python en esta ficha)
Ganancia de 100,000 MXN en una acción de EUA vendida en Nueva York:
- Art. 129 (solo si cotizara en México): 10,000 de ISR, definitivo.
- Tarifa general, si entra a la progresividad: el ISR depende de los demás ingresos del año; con un ingreso total de solo 100,000, la tarifa del art. 152 da una tasa efectiva de ~5.5%; con ingresos de salario de 1 millón, la marginal supera el 30%.
- La diferencia entre tributar por el 10% y por la tarifa general puede ser de **cero a varias veces más** según el resto de ingresos. Por eso el tratamiento del ETF de EUA **no debe asumirse** como el del SIC.

## Contraejemplo
Un residente que vende en EUA una acción de sociedad mexicana cotizada en BMV sigue cayendo en el 10% del art. 129 fr. I, porque la condición es la bolsa de la venta y no el emisor. El orden de la regla (dónde se negocia) importa más que la nacionalidad del emisor, según el texto de la fracción.

## Límites
- No se leyó el Reglamento de la LISR ni criterios del SAT sobre fondos extranjeros.
- No se leyó el texto de los artículos 90–95 (ganancias de fondos del extranjero) ni la fracción de inversiones en activos virtuales.
- La prohibición de la BMV para fondos extranjeros con cripto no se pudo confirmar (nv).

## Estado nuevo
**Localizado** (sin cambio de nivel). Se leyó el texto de los artículos clave; falta la prueba de ejercicio numérico con la tarifa del art. 152 y la lectura de los arts. 90–95 y del reglamento. Siguiente prueba: contrastar con criterio del SAT o un contador sobre si un ETF de EUA es entidad extranjera del art. 176.
