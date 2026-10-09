# Ficha · Doctorado derecho fiscal D7 · Fondos y valores extranjeros para una persona física residente en México

**Pregunta.** Si un residente en México compra un ETF de EUA (p. ej. IBIT o SPY) en una cuenta de EUA, ¿qué regla de la LISR le aplica? ¿Y si lo compra en BMV/SIC?

## Fuente y nivel de acceso
| Fuente | Acceso | Grado |
|---|---|---|
| LISR, texto de Diputados, última reforma DOF 01-04-2024 (PDF completo, 3.0 MB, SHA-256 803c2875c09c751c…), arts. 1, 2, 129, 176 | Lectura del artículo íntegro | A (texto) |
| Art. 129 (10% definitivo sobre enajenación de acciones en bolsas de valores concesionadas o mercados de derivados reconocidos) | Íntegro | A |
| Art. 176 (regímenes fiscales preferentes) | Primer párrafo y la regla de 75% | A |
| Prohibición de la BMV/BIVA a fondos extranjeros con cripto (dato del dueño, 8-oct) | **No localizada** en búsqueda pública; no se usa. **[Corregido 9-oct-2026, conciliación, `bitacora/arbitraje/2026-10-09-registros-del-8-oct.md`]:** para la **BMV está confirmada**: disposición 4.019.00 de su Reglamento Interior, autorizada con el oficio CNBV 312-2/42112/2024 y en vigor desde el 17-abr-2024 (fallo `bitacora/arbitraje/2026-10-08-bmv-fondos-cripto.md`, 03:14 UTC del 8-oct, anterior a esta ficha). **BIVA sigue sin verificar.** | A (BMV); nv (BIVA) |
| Reglamento y resoluciones de la CNBV | No leídos | nv |

## Derivación
1. **Art. 1 fr. I:** los residentes en México pagan ISR por **todos sus ingresos, cualquiera que sea la ubicación de la fuente de riqueza**. Un ETF de EUA no sale de la base del impuesto por estar en otra cuenta.
2. **Art. 129 fr. I:** la tasa plana de 10% aplica a la enajenación de acciones **de sociedades extranjeras cotizadas en bolsas de valores o mercados de derivados concesionados en México**. Un ETF comprado en Nueva York no cumple esa condición; por texto, **no entra al 10%** y tributa por la tarifa progresiva del art. 96/152 como ingreso ordinario (inferencia de texto, grado B).
3. **Art. 176 (regímenes fiscales preferentes):** si el vehículo es una **entidad extranjera** en la que el residente participa, y esa entidad no paga en su país al menos el 75% del ISR que pagaría en México, el ingreso se acumula **aunque no se distribuya**. Un ETF registrado en EUA es un vehículo de inversión; si tiene personalidad jurídica propia, **la discusión es si entra al régimen**. Este es el punto que requiere contador (inferencia de texto, grado C).
4. **Inclusión de ingresos de fondos:** el propio texto del art. 1 y del Título V considera figuras extranjeras a los fondos de inversión "siempre que no tengan personalidad jurídica propia". Un ETF de EUA típico tiene estructura de trust o company; la clasificación depende del vehículo específico (inferencia, grado C).

## Ejercicio (código: `fichas/codigo/2026-10-08-d7-etf-incremental.py`, reutiliza la tarifa 2026 verificada en la ficha D1)
Ganancia G = 100,000 MXN, cedular 10% = 10,000. ISR incremental = ISR(salario + G) − ISR(salario):

| Salario anual S | ISR incremental por G | Tasa efectiva sobre G | Diferencia vs 10% |
|---|---|---|---|
| 0 | 6,572.16 | 6.57% | −3,427.84 (la tarifa general sale más barata) |
| 150,000 | 18,727.75 | 18.73% | +8,727.75 |
| 300,000 | 21,360.00 | 21.36% | +11,360.00 |
| 1,000,000 | 30,000.00 | 30.00% | +20,000.00 |

- **Equilibrio** (sin otros ingresos): G* = 194,724.65. Con cualquier salario relevante, el 10% cedular siempre es menor que la tarifa general sobre la misma ganancia.
- **Lectura:** para un asalariado, una ganancia de EUA sumada a su ingreso tributa a 19–30% marginal. La misma ganancia comprada en la BMV (art. 129 fr. I, si cotizara allí) paga 10% definitivo. La diferencia es de hasta 20,000 MXN por cada 100,000 de ganancia.
- La conclusión depende de **la clasificación del vehículo** (art. 176, punto 3 de la derivación): si el ETF es entidad extranjera de preferentes, el problema es de acumulación aun sin venta.

## Contraejemplo
Un residente que vende en EUA una acción de sociedad mexicana cotizada en BMV sigue cayendo en el 10% del art. 129 fr. I, porque la condición es la bolsa de la venta y no el emisor. El orden de la regla (dónde se negocia) importa más que la nacionalidad del emisor, según el texto de la fracción.

## Límites
- No se leyó el Reglamento de la LISR ni criterios del SAT sobre fondos extranjeros.
- No se leyó el texto de los artículos 90–95 (ganancias de fondos del extranjero) ni la fracción de inversiones en activos virtuales.
- La prohibición de la BMV para fondos extranjeros con cripto no se pudo confirmar (nv). **[Corregido 9-oct-2026, conciliación]:** para la BMV sí está confirmada (grado A, ver la tabla de fuentes); solo falta BIVA.

## Estado nuevo
**Documentado con comprobación** (8-oct): texto de arts. 1, 129 y 176 leído íntegro y ejercicio numérico reproducible con la tarifa 2026. Falta: lectura de los arts. 90–95 y del reglamento, y criterio del SAT o de un contador sobre si un ETF de EUA es entidad extranjera del art. 176. Esa es la única pregunta que decide el resultado.
