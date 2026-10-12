# Ficha de avance · 12-oct-2026 · Frontera DAT (cont.): no existe un término definido "Indebtedness" en los dos indentures de Strategy, verificado con búsqueda de texto completo

> Corrida de las 08:17 CDMX (14:26 UTC), estudio profundo. **Decisión del día:** de los cinco pendientes declarados en `fichas/2026-10-11-galaxy-prediccion-23-ventas-forzadas-dat.md` §9, el orquestador señaló intentar Metaplanet de nuevo por una vía distinta a EDINET/TDnet. Se intentó primero (§3, resultado: sigue bloqueado, con un dato nuevo) y, con el tiempo restante, se avanzó un segundo pendiente de la misma lista que sí se pudo cerrar con evidencia primaria directa: la búsqueda de la definición exacta de "Indebtedness" en el Artículo 1 de los dos indentures de Strategy, que las fichas del 10 y 11-oct dejaban como lectura "convencional, no verificada al 100%".

## 0. Pregunta de hoy, acotada

¿Los indentures de las Series A (2024) y B (2025) de notas convertibles de Strategy Inc. contienen, en su Artículo 1 (Definiciones), un término capitalizado "Indebtedness" que fije qué cuenta para el cross-default de la Sección de Events of Default? Si no existe esa definición, ¿qué implica para la lectura de que los dividendos de acciones preferentes no activarían el cross-default?

## 1. Acceso y fuentes (declarado)

- **Acceso íntegro, fuente primaria, descargada en vivo hoy, con búsqueda de texto completo (no solo lectura por tramos como el 10-oct):**
  - Serie A — Exhibit 4.1 del indenture del 11-mar-2024: `sec.gov/Archives/edgar/data/1050446/000119312524064321/d749312dex41.htm` (621,746 bytes de HTML; 344,737 caracteres de texto extraído).
  - Serie B — Exhibit 4.1 del indenture del 21-feb-2025: `sec.gov/Archives/edgar/data/1050446/000119312525032800/d851880dex41.htm` (644,154 bytes de HTML; 310,798 caracteres de texto extraído).
  - Ambos descargados completos (no por tramos) con `curl`, limpiados de etiquetas HTML con un script propio y buscados con expresiones regulares en los dos métodos descritos en §2.
- **Metaplanet (§3):** IR oficial en inglés, `metaplanet.jp/en/ir` (accesible, HTTP 200); EDINET y TDnet probados de nuevo, mismo resultado que el 9 y 11-oct.
- **No se tocó** ninguna fuente de pago ni información no pública.

## 2. Hallazgo central: ningún indenture define "Indebtedness"; el cross-default usa lenguaje llano, no un término capitalizado

Las fichas del 9 y 10-oct ya habían citado la cláusula de cross-default ("indebtedness for money borrowed" / "indebtedness for borrowed money" por encima de un umbral), pero dejaron pendiente verificar si el Artículo 1 define ese término con mayúscula inicial de forma expresa (lo que podría, en teoría, incluir o excluir explícitamente obligaciones de dividendos preferentes). Hoy se descargó el texto **completo** de ambos indentures (no por tramos de 100,000 caracteres como el 10-oct) y se buscó con dos métodos independientes:

**Método 1** — listar todo término definido que empieza con "I" (patrón `"X" means`, con las comillas tipográficas que usa el documento de SEC):

| Documento | Términos definidos que empiezan con "I" |
|---|---|
| Serie A (2024) | `Indenture`, `Interest Payment Date` |
| Serie B (2025) | `Indenture`, `Initial Purchasers`, `Interest Payment Date`, `Issue Date` |

**Método 2** — contar todas las ocurrencias de la palabra "indebtedness" (cualquier capitalización) y verificar si alguna va precedida de las comillas tipográficas que marcarían una definición formal (`"Indebtedness" means`):

| Documento | Ocurrencias de "indebtedness" | ¿Alguna es `"Indebtedness" means`? |
|---|---|---|
| Serie A (2024) | 8 | No |
| Serie B (2025) | 9 | No |

**Conclusión, con los dos métodos coincidiendo:** **ninguno de los dos indentures define formalmente un término capitalizado "Indebtedness".** La palabra aparece siempre en minúscula y en lenguaje corrido, casi siempre dentro de la cláusula de cross-default (Serie A, Secc. 6.01(g): *"indebtedness for money borrowed in excess of $30,000,000"*; Serie B, Secc. 7.01(vii): *"indebtedness for borrowed money of at least two hundred million dollars ($200,000,000)"*), y un puñado de veces en contextos no relacionados con deuda financiera (p. ej., "evidences of indebtedness" dentro de la definición de distribuciones de capital, que es terminología estándar de "valores de deuda" en cláusulas de ajuste de conversión, no el cross-default).

## 3. Lo que no se logró hoy (de nuevo): Metaplanet

Se repitió el intento con las dos vías ya identificadas como mejores candidatas (ficha del 11-oct): EDINET (`edinet-fsa.go.jp`) sigue sin resolver DNS desde este entorno; TDnet (`release.tdnet.info`) sigue devolviendo HTTP 403. La IR oficial en inglés (`metaplanet.jp/en/ir`) sí es accesible y hoy aportó un dato nuevo pequeño: el listado de octubre trae, además del aviso del 5-oct ya visto el 11-oct ("Notice of Additional Purchase of Bitcoin"), tres avisos más en la misma fecha ("Notice Regarding Introduction of the Net Interest Income Strategy", "Notice Regarding the Q3 FY2026 Results of the Bitcoin Income Generation Business", "Notice Regarding Further Revision of Capital Allocation Policy") y uno del 1-oct ("Notice Regarding the Status of Share Repurchases"). **Sigue sin haber enlaces a PDF ni cifras extraíbles** desde esa página listado-only; búsquedas dirigidas en inglés y japonés (`site:xj-storage.jp`, `site:kabutan.jp`, consultas directas por fecha) no devolvieron el documento primario ni una cifra de tenencias de BTC confiable y fechada en octubre-2026 — las cifras que aparecen en prensa (coinpost.jp) son inconsistentes entre sí (17,132; 20,136; 25,555 BTC, según el artículo) y no se usan aquí. **No se afirma ninguna cifra de Metaplanet hoy, por cuarto día consecutivo de intento.** Se documenta en `bitacora/decisiones-pendientes.md` como pendiente técnico (necesita un mecanismo de acceso que no está disponible en este entorno, o la intervención del dueño).

## 4. Ejercicio numérico (verificado dos veces: lectura manual tramo por tramo el 10-oct + script Python con dos métodos independientes hoy)

Script de esta sesión (fuera del repositorio): `scratchpad/g4calc/indebtedness_check.py`. Salida real, reproducida arriba en la tabla del §2. El script hace dos cosas de forma independiente sobre el mismo texto (extraído de HTML a texto plano con una sola función `load_text`, reutilizada para ambos métodos, así que no hay doble conteo por limpieza distinta):

```
Metodo 1 (regex "X" means, X empieza con I):
  Serie A: ['Indenture', 'Interest Payment Date']
  Serie B: ['Indenture', 'Initial Purchasers', 'Interest Payment Date', 'Issue Date']

Metodo 2 (conteo de ocurrencias + verificación de patrón de definición):
  Serie A: 8 ocurrencias, 0 definidas como término capitalizado
  Serie B: 9 ocurrencias, 0 definidas como término capitalizado

Conclusión (n=2 series, 100% de cobertura de las dos ya leídas): NO hay definición formal en ninguna.
```

**Lectura:** esto no es evidencia de que las series restantes (2028, 2031, 2032, todavía no leídas; sigue pendiente generalizar de n=2 a la familia completa) se comporten igual, pero sí cierra, con certeza para las dos series ya revisadas, la pregunta exacta que la ficha del 10-oct dejó abierta ("buscar la definición explícita de 'Indebtedness'... no apareció en los tramos leídos hoy"). **La ausencia de una definición formal es, en sí misma, información:** cuando un indenture quiere ampliar o acotar un concepto financiero más allá de su sentido ordinario, lo hace con una definición explícita (así se define, por ejemplo, "Capital Stock", "Indenture" o "Significant Subsidiary" en estos mismos documentos). Que "indebtedness for borrowed money" **no** tenga una definición propia, y que el resto de las definiciones del Artículo 1 no lo mencionen ni lo amplíen, es consistente con que el redactor pretendía su sentido llano y restringido (deuda financiera por dinero prestado), no uno expandido que capturara obligaciones de dividendos preferentes acumulados. Esto **refuerza, con evidencia directa en vez de inferencia de "convención de mercado"**, la lectura declarada como pendiente en la ficha del 10-oct §4: el no pago de un dividendo preferente (STRK, STRF, STRC, STRD) no encajaría, por su propio texto, en la cláusula de cross-default de estas dos series.

## 5. Qué cambia para invertir

- **No cambia el filtro de tendencia de `arena-claude-binance`** (solo mira el precio de cierre de BTC/USDT; no tiene exposición a MSTR).
- **Cierra, con mayor certeza que antes, uno de los pendientes explícitos de las fichas del 10 y 11-oct:** el riesgo de caja de los dividendos preferentes de Strategy (el riesgo de corto plazo real que esta serie de fichas viene documentando desde el 9-oct) queda más claramente aislado del mecanismo de cross-default de la deuda convertible — no es una lectura basada en "cómo se suele escribir en el mercado", sino en la ausencia verificada de una definición que lo amplíe en el texto mismo.
- **No cambia ningún pronóstico ni boleta de la cuenta hoy.** Se registra un pronóstico nuevo verificable ligado a esta misma frontera (financiamiento de las DAT bajo mNAV deprimido), ver `bitacora/pronosticos.csv`, P0111.

## 6. Contrapuntos

- Esta es una lectura de "argumento por ausencia" (expressio unius / lo que no está definido se interpreta en su sentido ordinario), que es una herramienta estándar de interpretación contractual, pero no una certeza jurídica absoluta: un tribunal podría, en teoría, interpretar "indebtedness for borrowed money" de forma más amplia si hubiera evidencia extrínseca de intención distinta. No se consultó jurisprudencia de Delaware ni de Nueva York (ley aplicable de los indentures) sobre esta frase exacta — límite declarado, no verificado hoy.
- Dos series (n=2) no son toda la familia de notas de Strategy. Si una serie posterior (2031, 2032) sí definiera "Indebtedness" de forma expresa y distinta, el hallazgo de hoy no se extendería automáticamente a ella.

## 7. Autoexamen

- ¿Puedo reproducir cada cifra sin ver la ficha? Sí: el script está completo en `scratchpad/g4calc/indebtedness_check.py` (fuera del repositorio), usa solo los dos archivos HTML descargados hoy de las URLs citadas, y los dos métodos son independientes entre sí pero comparten la misma función de limpieza de texto (declarado, no es una limitación oculta).
- ¿Qué rompería la lectura del §2 y §4? Que el patrón de regex usado (comillas tipográficas `&#147;...&#148;` seguidas de "means") no capture alguna forma alternativa de definir el término (p. ej., "Indebtedness" definido por referencia a otro documento, o con una tipografía de comillas distinta). Se verificó manualmente que el patrón sí capturó correctamente los ~90-100 términos de cada documento con esa estructura (conteo visual de una muestra, no exhaustivo al 100%), y que el documento usa consistentemente esas comillas tipográficas en toda su extensión (confirmado al ver "Indenture", "Capital Stock", etc. con el mismo patrón).
- **Grado A** para la ausencia verificada de la definición en los dos documentos leídos íntegros hoy (reproducible, dos métodos, mismo resultado). **B** para la lectura de que esa ausencia refuerza la interpretación restringida del cross-default (es una inferencia razonable de técnica de redacción contractual, no una certeza absoluta — ver §6). **D** para cualquier generalización a las series 2028/2031/2032, no leídas.

## 8. Pendientes (actualizado)

- Leer el texto de las series restantes (2028, 2031, 2032) para generalizar el hallazgo de n=2 a la familia completa de notas convertibles de Strategy.
- **Metaplanet: sigue pendiente, cuarto intento fallido.** EDINET sin DNS, TDnet con 403, IR en inglés solo con títulos sin PDF. Ver `bitacora/decisiones-pendientes.md` (12-oct-2026): se decide, de forma conservadora, declarar este acceso como bloqueado por el entorno (no por falta de esfuerzo) y no reintentarlo todos los días; se reintentará cuando haya una vía nueva identificada (p. ej., un agregador distinto) o el dueño pueda aportar el documento.
- Verificar el 10-Q de Q3-2026 de Strategy (esperado ~24-26-oct-2026).
- Re-verificar los 5 casos no-Strategy de la predicción #23 de Galaxy contra el artículo original de CoinDesk.
- Confirmar si hubo alguna venta de BTC de Strategy antes de 2026 (un resumen de hoy, vía búsqueda web, grado D, dice que Strategy "began selling Bitcoin for the first time in several years" en **mayo-2026**, no agosto — contradice la cronología de "primera vez en agosto" de CoinDesk citada el 11-oct; no verificado hoy contra ningún 8-K de mayo, queda como pendiente explícito con la fecha en disputa).
- Dar seguimiento al pronóstico P0111 (nueva emisión de deuda convertible de Strategy en los próximos 30 días).

Script de esta sesión: `scratchpad/g4calc/indebtedness_check.py` (fuera del repositorio, usa `indentureA.html` e `indentureB.html` descargados en vivo el 12-oct-2026 de las URLs citadas en §1).
