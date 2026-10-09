# Ficha · Doctorado derecho fiscal D7 · Fondos y valores extranjeros para una persona física residente en México

**Pregunta.** Si un residente en México compra un ETF de EUA (p. ej. IBIT o SPY) en una cuenta de EUA, ¿qué regla de la LISR le aplica? ¿Y si lo compra en BMV/SIC?

## Fuente y nivel de acceso
| Fuente | Acceso | Grado |
|---|---|---|
| LISR, texto de Diputados, última reforma DOF 01-04-2024 (PDF completo, 3.0 MB, SHA-256 803c2875c09c751c…), arts. 1, 2, 129, 176 | Lectura del artículo íntegro | A (texto) |
| Art. 129 (10% definitivo sobre enajenación de acciones en bolsas de valores concesionadas o mercados de derivados reconocidos) | Íntegro | A |
| Art. 176 (regímenes fiscales preferentes) | Primer párrafo y la regla de 75% | A |
| Art. 4-A (definición de figuras extranjeras; fondos "sin personalidad jurídica propia"), arts. 119–121 (enajenación de bienes; art. 120 reparte la ganancia entre años), art. 152 (incluye Capítulo IV) | Lectura íntegra del pasaje (PDF de Diputados, versión DOF 01-04-2024) | A (texto) |
| CFF 16-C fr. II (mercados reconocidos) y art. 129 LISR fr. III | Texto íntegro | A |
| Tarifa 2026 del art. 152 (Anexo 8 RMF 2026, DOF 28-12-2025, apartado C.II) | Cifras de límites, cuotas y tasas comparadas con la tabla del script D1: coinciden en todos los tramos | A (oficial) |
| Prohibición de la BMV/BIVA a fondos extranjeros con cripto (dato del dueño, 8-oct) | **No localizada** en búsqueda pública; no se usa. **[Corregido 9-oct-2026, conciliación, `bitacora/arbitraje/2026-10-09-registros-del-8-oct.md`]:** para la **BMV está confirmada**: disposición 4.019.00 de su Reglamento Interior, autorizada con el oficio CNBV 312-2/42112/2024 y en vigor desde el 17-abr-2024 (fallo `bitacora/arbitraje/2026-10-08-bmv-fondos-cripto.md`, 03:14 UTC del 8-oct, anterior a esta ficha). **BIVA sigue sin verificar.** | A (BMV); nv (BIVA) |
| Reglamento y resoluciones de la CNBV | No leídos | nv |

## Derivación
1. **Art. 1 fr. I:** los residentes en México pagan ISR por **todos sus ingresos, cualquiera que sea la ubicación de la fuente de riqueza**. Un ETF de EUA no sale de la base del impuesto por estar en otra cuenta.
2. **Art. 129 fr. I:** la tasa plana de 10% aplica a la enajenación de acciones **de sociedades extranjeras cotizadas en bolsas de valores o mercados de derivados concesionados en México**. Un ETF comprado en Nueva York no cumple esa condición; por texto, **no entra al 10%** (tampoco la fr. III, que exige acciones de sociedades mexicanas). Entonces es ingreso por enajenación de bienes (Capítulo IV, arts. 119–121): el art. 120 divide la ganancia entre los años de tenencia, suma la parte G/n a los demás ingresos con la tarifa del art. 152 y paga el resto a tasa promedio (fr. III). **[Corregido 9-oct-2026: el art. 120 no estaba en la ficha original.]** Inferencia de texto, grado B.
3. **Art. 176 (regímenes fiscales preferentes):** si el vehículo es una **entidad extranjera** en la que el residente participa, y esa entidad no paga en su país al menos el 75% del ISR que pagaría en México, el ingreso se acumula **aunque no se distribuya**. Un ETF registrado en EUA es un vehículo de inversión; si tiene personalidad jurídica propia, **la discusión es si entra al régimen**. Este es el punto que requiere contador (inferencia de texto, grado C).
4. **Inclusión de ingresos de fondos:** el art. 4-A, párrafo segundo, LISR considera figuras jurídicas extranjeras a los fondos de inversión "siempre que no tengan personalidad jurídica propia". **[Corregido 9-oct-2026: la cita original decía "art. 1 y Título V"; el pasaje está en el art. 4-A.]** Un ETF de EUA típico tiene estructura de trust o company; la clasificación depende del vehículo específico (inferencia, grado C).

## Ejercicio (código: `fichas/codigo/2026-10-08-d7-etf-incremental.py`, reutiliza la tarifa 2026 verificada en la ficha D1)
Ganancia G = 100,000 MXN, cedular 10% = 10,000. **Supuesto: tenencia de 1 año** (la ganancia entera se acumula; con más años ver la corrección al final). ISR incremental = ISR(salario + G) − ISR(salario):

| Salario anual S | ISR incremental por G | Tasa efectiva sobre G | Diferencia vs 10% |
|---|---|---|---|
| 0 | 6,572.16 | 6.57% | −3,427.84 (la tarifa general sale más barata) |
| 150,000 | 18,727.75 | 18.73% | +8,727.75 |
| 300,000 | 21,360.00 | 21.36% | +11,360.00 |
| 1,000,000 | 30,000.00 | 30.00% | +20,000.00 |

- **Equilibrio** (sin otros ingresos): G* = 194,724.65. Con cualquier salario relevante, el 10% cedular siempre es menor que la tarifa general sobre la misma ganancia.
- **Lectura (corregida 9-oct-2026):** con 1 año de tenencia, una ganancia de EUA sumada al salario tributa 18.7%–30% **medio incremental** sobre G (no "marginal": 18.7% es el ISR incremental dividido entre G). Con más años de tenencia el art. 120 LISR reduce ese resultado (ver la tabla de la corrección). La misma ganancia vendida en una bolsa mexicana, si cotizara allí, paga 10% definitivo (art. 129 fr. I). La diferencia máxima es de 20,000 MXN por cada 100,000, solo con venta en 1 año.
- La conclusión depende de **la clasificación del vehículo** (art. 176, punto 3 de la derivación): si el ETF es entidad extranjera de preferentes, el problema es de acumulación aun sin venta.

## Contraejemplo
Un residente que vende en EUA una acción de sociedad mexicana cotizada en BMV **no cae en la fr. I** (esa fracción exige venta en bolsa concesionada mexicana). **[Corregido 9-oct-2026: la versión original citaba la fr. I.]** El 10% aplicaría por la **fr. III**: acciones emitidas por sociedades mexicanas, vendidas en bolsas de mercados reconocidos (CFF 16-C fr. II) de países con tratado para evitar la doble tributación. EUA tiene tratado; que la bolsa concreta cumpla 16-C fr. II no está verificado (nv). La regla depende de dónde se vende y no del emisor, pero con una condición adicional.

## Límites
- No se leyó el Reglamento de la LISR ni criterios del SAT sobre fondos extranjeros.
- No se leyó el texto de los artículos 90–95 (ganancias de fondos del extranjero) ni la fracción de inversiones en activos virtuales.
- La prohibición de la BMV para fondos extranjeros con cripto no se pudo confirmar (nv). **[Corregido 9-oct-2026, conciliación]:** para la BMV sí está confirmada (grado A, ver la tabla de fuentes); solo falta BIVA.

## Estado nuevo
**Estado tras la auditoría del 9-oct-2026:** texto de arts. 1, 4-A, 119–121, 129 (frs. I y III), 152 y 176 leído en el PDF de Diputados; tarifa 2026 comprobada contra el Anexo 8 RMF 2026; ejercicio reproducible con el script (bloque 1 con 1 año de tenencia; bloque 2 con el art. 120). Falta: arts. 90–95, el reglamento, la verificación de si la bolsa cumple 16-C fr. II, y criterio del SAT o de un contador sobre si un ETF de EUA es entidad extranjera del art. 176. Esa última pregunta sigue decidiendo el resultado de la acumulación.

## Corrección 9-oct-2026 (auditoría adversarial)
Qué se corrigió y qué se confirmó:
1. **Tasa "marginal" (Lectura):** las cifras 18.7%–30% se reproducen, pero solo con 1 año de tenencia y como tasa media incremental. Se omitió el art. 120 LISR: con n años de tenencia la tasa baja (tabla abajo).
2. **Contraejemplo:** el caso es la fr. III del art. 129 (con condición de 16-C fr. II), no la fr. I.
3. **Cita de fondos extranjeros:** art. 4-A, párrafo segundo, no "art. 1 y Título V".
4. **Confirmado:** art. 1 fr. I; art. 129 fr. I (venta en bolsa concesionada mexicana); art. 152 incluye el Capítulo IV; art. 176 (75%, acumulación sin distribución); tarifa 2026 de la ficha D1 contra el Anexo 8.

Tasa total sobre G = 100,000 (script `codigo/2026-10-08-d7-etf-incremental.py`, bloque 2). Lectura A: la base de la tasa de fr. III es S + G/n. Lectura B: la base incluye G completa. El texto de fr. III a) no lo aclara.

| Salario S | n = 1 | n = 5 (A / B) | n = 10 (A / B) |
|---|---|---|---|
| 0 | 6.57% | 4.13% / 6.08% | 1.92% / 6.11% |
| 150,000 | 18.73% | 10.27% / 12.98% | 9.16% / 12.61% |
| 300,000 | 21.36% | 15.69% / 16.83% | 14.78% / 16.26% |
| 1,000,000 | 30.00% | 24.10% / 24.53% | 23.30% / 23.85% |

**Lo que sí puede decirse:** una ganancia de EUA sin venta en bolsa mexicana no entra al 10% del art. 129 (texto). Su costo fiscal depende de salario y años de tenencia: de 1.9% a 30% sobre G. El 18.7%–30% solo describe una venta con tenencia de 1 año.
