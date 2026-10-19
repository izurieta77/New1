# Ficha · Doctorado en contabilidad C4: consolidación, combinaciones de negocios y participación no controladora (IFRS 10, IFRS 3, IAS 24)

> Trabajo continuo del 18-oct-2026 (19:10 CDMX; 01:10 UTC del 19-oct). Área con cobertura "Sin" en `doctorados/ESTADO.md`. Fase 0: no recomienda inversiones.

## Pregunta
Cuando una emisora consolida subsidiarias que no posee al 100%, ¿qué parte de sus cifras es de sus accionistas y qué parte no? ¿Dónde se esconden utilidades contables sin efectivo?

Sirve para leer los reportes de grupos con minoritarios, como AMX (reporta el 20-oct) y los conglomerados del IPC, y para no equivocar múltiplos.

## Fuente y nivel de acceso
- **Texto íntegro de las normas, grado A:** Reglamento (UE) 2023/1803 de la Comisión, del 13-ago-2023, que adopta las NIIF. HTML oficial de EUR-Lex (CELEX 32023R1803), descargado el 19-oct-2026; 12.3 MB. Es la versión adoptada en la UE a esa fecha.
  - **Acceso: sección.** Se extrajeron con búsqueda literal y se leyeron completos IFRS 10 §7, §23, §25 y B94-B99, IFRS 3 §19, §32 y §42, e IAS 24 §9. No se leyó todo el texto.
- **Resúmenes oficiales de ifrs.org, grado A**, de IFRS 3, IFRS 10 e IAS 24 (consultados el 19-oct-2026): objetivo de cada norma e historia (IAS 22 → IFRS 3 en 2004; IAS 27 → IFRS 10 en 2011).
- **No leído:**
  - **US GAAP, ASC 805 y 810:** incluye el modelo de entidades de interés variable (VIE), que es distinto del control de IFRS 10. La Codificación de FASB exige cuenta.
  - **NIF B-7 y B-8 del CINIF:** son de pago.
  - **IFRS 12** (revelaciones) e **IAS 36** (prueba de deterioro del crédito mercantil).
  - Todo esto queda como pendiente.

## Lo que dicen las normas (cita literal, traducción propia)
| Norma | Regla | Texto |
|---|---|---|
| IFRS 10 §7 | **Control = tres elementos a la vez** | El inversionista controla "if and only if" tiene: (a) poder sobre la participada, (b) exposición o derechos a rendimientos variables y (c) capacidad de usar ese poder para afectar sus rendimientos |
| IFRS 10 (resumen) | Se consolida todo | Los estados consolidados presentan activos, pasivos, capital, ingresos, gastos y flujos de la matriz y sus subsidiarias "as those of a single economic entity" |
| IFRS 10 B94 | Atribución | La utilidad y el ORI se atribuyen a la controladora y a la participación no controladora, "even if this results in the non-controlling interests having a deficit balance" |
| IFRS 10 §23 | Comprar o vender minoritarios sin perder el control | Son "equity transactions": no generan resultado ni cambian el crédito mercantil |
| IFRS 10 §25 | Pérdida de control | Se da de baja la subsidiaria, se mide lo retenido **a valor razonable** y se reconoce la ganancia o pérdida atribuible a la antigua controladora |
| IFRS 3 §19 | Medición del minoritario, adquisición por adquisición | (a) a valor razonable, o (b) por la parte proporcional de los activos netos identificables |
| IFRS 3 §32 | Crédito mercantil | (contraprestación + minoritario + participación previa a valor razonable) − activos netos identificables a la fecha de adquisición |
| IFRS 3 §42 | Adquisición por etapas | La participación previa se remide a valor razonable y la diferencia va "in profit or loss or other comprehensive income, as appropriate" |
| IAS 24 §9 | Parte relacionada | Quien controla, controla en conjunto o influye significativamente, o es personal clave de la entidad o de su matriz (y sus familiares cercanos). Se revela la naturaleza de la relación, las operaciones y los saldos "regardless of whether a price is charged" |

## Ejercicio numérico (comprobado)
Código: `conocimiento/fichas/codigo/2026-10-19-c4-consolidacion-ifrs3-ifrs10.py` (aserciones; cifras ilustrativas, en millones).
1. **Opción del §19:** compra de 60% por 600; activos netos identificables de 700.
   - Minoritario proporcional, 280: crédito mercantil **180**.
   - Minoritario a valor razonable, 380: crédito mercantil **280**.
   - La diferencia (100) es el crédito mercantil que corresponde al minoritario. El mismo negocio puede mostrar crédito mercantil y capital distintos según la opción que eligió la emisora.
2. **Por etapas (§42):** ya tenía 20% (libros 150, valor razonable 200) y compra otro 40% por 440.
   - Reconoce una **ganancia de 50 sin efectivo**: va a resultados si la participación previa era una asociada; si era capital a FVOCI, va al ORI.
   - El crédito mercantil queda en 220.
3. **Compra de minoritarios (§23):** pasar de 60% a 80% pagando 250 da de baja 140 de minoritario y carga **110 al capital de la controladora**. Ni resultados ni crédito mercantil cambian.
4. **Lectura del analista:** se consolida el 100% del EBITDA (1,000), pero la utilidad de la controladora es 360 y no la consolidada de 400.
   - **EV/EBITDA:** 8.60x con el minoritario a mercado (600) contra 8.00x sin él. Omitirlo subestima el múltiplo ~7%.
   - **P/U:** 16.67x sobre la utilidad de la controladora contra 15.00x sobre la consolidada. Usar la consolidada hace ver barata a la emisora.

## Contraejemplo y límites
- **Control sin mayoría:** IFRS 10 §7 no pide más de 50%. Con 45% y el resto disperso, o con derechos contractuales, puede haber control. Con 51% sin poder efectivo (por ejemplo, derechos de veto de otro socio), puede no haberlo. El porcentaje no basta: hay que leer la nota de juicios significativos (IFRS 12, no leída).
- **US GAAP (VIE):** en EUA una entidad puede consolidarse por ser el "beneficiario primario" de una VIE, sin derechos de voto. Las cifras de bancos y tecnológicas de EUA pueden diferir por eso. No se leyó ASC 810.

## Uso en el sistema
- **En toda ficha de empresa del universo:** P/U contra la utilidad atribuible a la controladora, y EV con la participación no controladora (a mercado si cotiza la subsidiaria; si no, en libros, declarándolo).
- **En los post-mortems:** separar del resultado las ganancias por remedición (§42) y por pérdida de control (§25), que no son operativas ni de efectivo.
- **AMX el 20-oct:** leer el renglón de participación no controladora y la nota de partes relacionadas (IAS 24) antes de comparar su utilidad con lo pronosticado. Aquí no se dan cifras de AMX porque hoy no se consultaron.

## Segunda comprobación
Las cuatro cifras centrales se recalcularon a mano: 600 + 280 − 700 = 180; 440 + 280 + 200 − 700 = 220; 250 − 140 = 110; 8,600 / 1,000 = 8.6x. Coinciden con las aserciones.

## Estado nuevo
C4 pasa de **"Sin" a "Parcial"** en `doctorados/ESTADO.md`: control, combinación de negocios, minoritario y partes relacionadas, con texto íntegro de la norma por sección y un ejercicio. Faltan:
- VIE de US GAAP (ASC 810) y NIF B-7/B-8;
- IFRS 11 (acuerdos conjuntos) e IAS 28 (método de participación);
- IFRS 12 e IAS 36 (deterioro del crédito mercantil);
- un caso real de una emisora del universo.
