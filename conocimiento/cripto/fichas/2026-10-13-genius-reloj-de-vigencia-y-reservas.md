# Ficha de avance · 13-oct-2026 · Frontera regulatoria: el texto de la GENIUS Act y el estado de su reglamentación en el Federal Register

> Corrida de las 08:17 CDMX (14:19 UTC), estudio profundo.
>
> **Por qué este tema.** Los 35 recursos (`recursos/indice.csv`) y los 6 temas extra del plan ya están en "estudiado". El nivel más bajo que sigue sin terminar es la **Frontera**. Ahí, la fila "Regulación: GENIUS, CLARITY, MiCA, Circular 4/2019 de Banxico" nunca tuvo una ficha propia: solo la mencionaban de paso los capítulos 04 y 05, siempre por medio del FMI (recurso 30) o de la prensa. La frontera DAT/Strategy de los últimos 5 días queda en pausa; sus pendientes siguen en `estado-de-dominio.csv`.

## 0. Pregunta de hoy, acotada

¿Qué dice **literalmente** la GENIUS Act (Public Law 119-27) sobre reservas, intereses, vigencia y plazos? Y al 13-oct-2026, ¿algún regulador primario ya publicó una regla final que mueva la fecha de vigencia?

## 1. Acceso y fuentes (declarado)

- **Ley, íntegra y de fuente primaria:**
  - Texto oficial de la Public Law 119-27 (139 Stat. 419), de GPO/govinfo: `govinfo.gov/content/pkg/PLAW-119publ27/html/PLAW-119publ27.htm`. Son 185,846 bytes.
  - Se descargó también la copia de congress.gov (`congress.gov/119/plaws/publ27/PLAW-119publ27.htm`) y `cmp` confirmó que es **idéntica byte por byte**: es la primera verificación.
  - Se extrajeron 184,387 caracteres de texto y se buscó en ellos con `grep`. Se leyeron completas las Secs. 2(25), 3(a)-(c), 4(a)(1)-(4), 4(a)(11), 13(a), 18(b)(6) y 20.
- **Estado de la reglamentación, de fuente primaria:**
  - API del Federal Register (`federalregister.gov/api/v1/documents.json`), consultada a las 14:30 UTC con dos búsquedas independientes:
    - (a) el término "payment stablecoin", todos los tipos, 39 documentos;
    - (b) el término "GENIUS" con `type=RULE` desde el 18-jul-2025, 3 documentos.
  - Es la segunda verificación.
- **Secundario, grado C:** la declaración del Contralor Gould ("the OCC will have a GENIUS Act final rule out **by November**"), según ICBA (20-ago-2026).
- **No se revisaron hoy:** CLARITY (más allá de lo que ya está en la base), MiCA y la Circular 4/2019 de Banxico. Quedan pendientes (§8).

## 2. Lo esencial del texto [H, grado A: texto de la ley]

| Tema | Sección | Qué dice |
|---|---|---|
| Quién puede emitir | 3(a) | Es ilegal emitir una *payment stablecoin* en EUA si no se es *permitted payment stablecoin issuer*. |
| Prohibición a intermediarios | 3(b)(1) | **A partir de los 3 años de la promulgación**, un *digital asset service provider* no puede ofrecer ni vender a personas en EUA una stablecoin de un emisor no permitido. Hay excepciones en 3(c) y en la Sec. 18 (régimen extranjero comparable). |
| Emisor extranjero | 3(b)(2) | El emisor extranjero tiene que poder cumplir, y cumplir, órdenes legales (congelar o bloquear). Es la puerta para Tether. |
| Reservas 1:1 | 4(a)(1)(A) | La lista es cerrada: (i) efectivo o saldo en la Fed; (ii) depósitos a la vista en un banco asegurado; (iii) **T-bills, notes o bonds con vencimiento remanente u original ≤ 93 días**; (iv) repos *overnight* como vendedor, respaldados por T-bills ≤ 93 días; (v) reverse repos *overnight* sobrecolateralizados, tri-party, compensados o bilaterales; (vi) fondos de mercado de dinero de gobierno que solo inviertan en (i)-(v); (vii) otro activo federal "similarmente líquido" que apruebe el regulador; (viii) versiones tokenizadas de (i)-(iii) y (vi)-(vii). **No caben** BTC, oro, préstamos garantizados ni papel comercial. |
| Transparencia | 4(a)(1)(C) | Publicación **mensual** de las reservas: monto, composición, **plazo promedio y ubicación geográfica de la custodia** por categoría. |
| Re-hipotecación | 4(a)(2) | Prohibida, con tres excepciones: margen de repos, custodia y liquidez para redenciones, siempre que el repo sea ≤ 93 días y esté compensado o aprobado por el regulador. |
| Certificación | 4(a)(3) | Una firma registrada en el PCAOB examina cada mes el reporte, y el CEO y el CFO lo certifican. Certificar en falso, a sabiendas, tiene las penas de 18 USC 1350(c). |
| Intereses | 4(a)(11) | El **emisor** (permitido o extranjero) no puede pagar "ninguna forma de interés o rendimiento" **solo por tener, usar o retener** la stablecoin. El texto se dirige al emisor; no menciona a los exchanges ni a terceros que paguen *rewards*. Eso es lo que sigue en disputa en CLARITY. |
| Reglamentación | 13(a) | Los reguladores primarios, el Tesoro y los reguladores estatales debían emitir reglamentos **a más tardar 1 año** después de la promulgación. |
| Vigencia | 20 | Rige en la **primera** de dos fechas: (1) 18 meses después de la promulgación, o (2) **120 días después** de que los reguladores primarios emitan reglas finales. |
| Regulador primario | 2(25) | Según el caso: la agencia bancaria federal que corresponda, la NCUA, la FDIC, la OCC o la Fed. **El Tesoro no es regulador primario.** |

**Hallazgo menor del texto [H]:** la Sec. 4(a)(3)(A) manda examinar "the previous month-end report required under paragraph **(1)(D)**". Pero el párrafo (1) de la ley promulgada solo tiene los incisos (A), (B) y (C); el reporte mensual está en **(1)(C)**. Es una referencia cruzada mal numerada en el texto oficial, y se confirmó en las dos copias idénticas. No cambia la obligación, que es clara por contexto, pero sirve de recordatorio: hay que citar la ley por su texto y no por resúmenes.

## 3. Hallazgo central: la vigencia ya quedó fija el 18-ene-2027 [H/I, grado B]

- **[H, A]** La ley se promulgó el 18-jul-2025. Con 18 meses, la vigencia cae el **18-ene-2027**.
- **[I, cálculo propio, §4]** Para que la vía (2) de la Sec. 20 adelantara esa fecha, la regla final tenía que salir **a más tardar el 20-sep-2026** (18-ene-2027 menos 120 días).
- **[H, B]** Al 13-oct-2026, el Federal Register **no tiene ninguna regla final** de un regulador primario. Las dos búsquedas independientes coinciden:
  - OCC: propuesta 2026-04089 (2-mar-2026; comentarios al 1-may).
  - FDIC: propuestas 2025-23510 y 2026-06974.
  - NCUA: propuestas 2026-02868 y 2026-09915.
  - Fed: propuestas 2026-19860 y 2026-19899 (29-sep-2026, comentarios al 30-nov).
  - Todas son *Proposed Rule*. Las únicas *Rule* con "GENIUS" desde jul-2025 son la del Tesoro sobre formularios del Comité de Certificación de Stablecoins (2026-19966, 30-sep-2026), que no es regulador primario, y dos documentos ajenos al tema (propinas del IRS y la interpretación SEC/CFTC del 23-mar-2026).
- **[I]** **Consecuencia:** cualquier regla final que salga desde hoy cae en la vía (2) con una fecha posterior al 18-ene-2027. Por ejemplo, una regla de hoy daría el 10-feb-2027, y una del 30-nov daría el 30-mar-2027. Así que **la vigencia de GENIUS ya no puede adelantarse; queda fija el 18-ene-2027**, salvo una reforma legal. Es decir, faltan **97 días**.
- **[H]** El plazo de reglamentación de la Sec. 13 (18-jul-2026) lleva **87 días incumplido**.
- **[H]** La prohibición a intermediarios de la Sec. 3(b) empieza el **18-jul-2028**.
- **Límite:** la Sec. 20 dice "**issue** any final regulations", no "publish". Una regla aprobada internamente antes del 20-sep y todavía no publicada podría, en teoría, contar. No hay rastro de eso en el Federal Register, y la OCC misma habló de "by November" en agosto. Por eso el grado es B y no A.

## 4. Ejercicio numérico (Python, verificado dos veces)

Script fuera del repositorio: `scratchpad/calc/genius_fechas.py`. Suma meses con `calendar` y verifica el corte de forma independiente con ordinales. Salida real:

```
18 meses (Sec.20(1)): 2027-01-18
ultima fecha de regla final que adelantaria la vigencia (m18-120d): 2026-09-20
Sec.13 plazo de reglamentacion (1 ano): 2026-07-18 | dias de atraso al 2026-10-13 : 87
Sec.3(b) prohibicion a DASP (3 anos): 2028-07-18
si la regla final saliera hoy -> hoy+120: 2027-02-10 ; vigencia= 2027-01-18
si saliera 30-nov-2026 -> +120: 2027-03-30
dias de hoy a la vigencia: 97
check corte: 2026-09-20
```

Los dos métodos dan el 20-sep-2026 como corte.

## 5. Qué cambia para invertir (`arena-claude-binance`, spot, desde México)

- **[I]** **No hay catalizador regulatorio de stablecoins en EUA en los próximos 30 días que cambie el riesgo de la cuenta.**
  - La vigencia (18-ene-2027) y la prohibición a intermediarios (18-jul-2028) están fijadas por ley.
  - Lo único que puede pasar antes es la regla final de la OCC, que pronostico en P0117 con p=0.30. Esa regla define capital, liquidez y licencias, no la fecha.
- **[I]** **Para el USDT en Binance:** la ley se aplica a lo que se ofrece a personas en EUA, y la restricción a intermediarios llega hasta 2028. No veo una vía por la que GENIUS, en el horizonte del torneo, obligue a Binance a deslistar USDT para una cuenta mexicana. El riesgo de USDT sigue siendo el de su paridad (E8 de `lista-senales-de-alerta.md`), no el de GENIUS.
- **[I]** La lista cerrada de reservas (T-bills ≤ 93 días, sin BTC ni oro) aleja a un emisor que quiera el estatus "permitido" de tener BTC en reservas. Para el precio de BTC es irrelevante a corto plazo (grado C).
- **[H]** La CFTC publicó hoy (13-oct) un **ANPRM**, aviso previo a una propuesta, para reglamentar transacciones y mercados de criptoactivos al amparo de la CEA §2(c)(2)(D): documento 2026-20888, comentarios hasta el 14-dic-2026. Es el inicio de un proceso largo, no una regla. Va en el pulso como noticia, no como alerta.

## 6. Contrapuntos y límites

- La Sec. 20 usa "the primary Federal payment stablecoin regulators issue any final regulations". El texto es ambiguo: no está claro si basta la regla de **un** regulador o se necesitan todas. No cambia la conclusión, porque hoy no hay ninguna.
- Que algo no aparezca en el Federal Register es evidencia por ausencia. La búsqueda por término depende de los títulos y resúmenes indexados. Para reducir el riesgo se hicieron dos búsquedas distintas, y los documentos de las propuestas sí aparecen con esos términos.
- El texto analizado es el promulgado. Una ley posterior (por ejemplo, CLARITY, si se aprobara) podría reformar la GENIUS; hoy no hay evidencia de eso.
- No se cubrieron MiCA ni la Circular 4/2019 de Banxico. La lectura sobre México sigue siendo la del 25-sep (Ley Fintech art. 30; Medá como IFPE).

## 7. Autoexamen (5 preguntas, respuestas en la ficha)

1. ¿Puede un emisor permitido bajo GENIUS tener un T-note a 2 años emitido hace 23 meses? (Sí: el vencimiento remanente es ≤ 93 días, según 4(a)(1)(A)(iii)(I).)
2. ¿Qué fecha rige si la OCC publica la regla final el 15-nov-2026? (El 18-ene-2027, porque 15-nov + 120 días cae el 15-mar-2027, que es posterior.)
3. ¿La Sec. 4(a)(11) prohíbe que un exchange pague *rewards* sobre USDC? (El texto se dirige al emisor; a terceros no los menciona. Esa es la disputa de CLARITY.)
4. ¿Desde cuándo un intermediario no puede ofrecer en EUA una stablecoin de un emisor no permitido? (Desde el 18-jul-2028, Sec. 3(b)(1).)
5. ¿Qué referencia cruzada está mal en el texto oficial? (4(a)(3)(A) cita "(1)(D)"; el reporte mensual está en (1)(C).)

## 8. Estado y pendientes

- **Estado:** "Documentado con comprobación" para GENIUS: texto íntegro, estado de reglamentación y ejercicio. La fila de regulación de la Frontera queda **parcial**.
- **Pendientes:**
  - (a) Circular 4/2019 y su reforma en el DOF: texto primario de Banxico.
  - (b) MiCA, artículos de stablecoins (EMT/ART) en EUR-Lex.
  - (c) Estado de CLARITY después de la cloture fallida del 15-sep.
  - (d) Revisar el Federal Register hacia el 12-nov para P0117.
  - (e) Leer el ANPRM de la CFTC del 13-oct (2026-20888) completo.

**Grado global:** A en el texto de la ley, B en el estado de la reglamentación y en la conclusión sobre la vigencia, y C en el momento de la regla de la OCC.
