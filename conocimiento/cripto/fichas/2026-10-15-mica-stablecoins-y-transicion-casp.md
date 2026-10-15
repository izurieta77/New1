# Ficha de avance · 15-oct-2026 · Frontera regulatoria (UE): MiCA, títulos III-IV (stablecoins) y la transición del art. 143 que dejó a Binance fuera de la UE

> Corrida de las 08:17 CDMX (14:19 UTC), estudio profundo.
>
> **Por qué este tema.** Es el pendiente (a) de la ficha de ayer (`2026-10-14-circular-4-2019-banxico-perimetro-mexicano.md` §8), dentro de la fila de Frontera "Regulación: GENIUS, CLARITY, MiCA, Circular 4/2019 de Banxico" (`00-plan-de-estudio.md`). Va antes que CLARITY porque explica un hecho que ya está en la lista de alerta (E5: "UE: solo retiros desde el 1-jul-2026") y porque se compara directo con GENIUS (ficha del 13-oct).

## 0. Pregunta de hoy, acotada

¿Qué dicen **literalmente** los títulos III (fichas referenciadas a activos, ART) y IV (fichas de dinero electrónico, EMT) del Reglamento (UE) 2023/1114 sobre reservas, reembolso e intereses? ¿Qué fecha fija el art. 143 para los proveedores (CASP) que ya operaban? ¿Y qué dice el registro oficial de ESMA sobre Binance al 15-oct-2026?

## 1. Acceso y fuentes (declarado)

- **Texto del DOUE, íntegro, en inglés:** Reglamento (UE) 2023/1114, DO L 150 del 9-jun-2023, pp. 40 y ss. Se obtuvo de la Oficina de Publicaciones de la UE (`publications.europa.eu/resource/celex/32023R1114`, XHTML, 1.68 MB), que es el repositorio (Cellar) del que sirve EUR-Lex. **Límite de acceso:** `eur-lex.europa.eu` (HTML y PDF) devolvió HTTP 202 vacío (desafío anti-bot) desde este entorno.
- **Segunda copia, íntegra, en español:** la misma fuente con `Accept-Language: spa` (1.78 MB). Las cifras y fechas citadas se cotejaron en las dos lenguas (§4).
- **Versión consolidada más reciente:** `02023R1114-20240109` (misma fuente). Su única modificación (M1) es el Reglamento (UE) 2023/2869 (punto de acceso único europeo, ESAP), que no toca los artículos de esta ficha. La consulta SPARQL de la Oficina de Publicaciones (`publications.europa.eu/webapi/rdf/sparql`) devuelve solo dos consolidaciones (9-jun-2023 y 9-ene-2024) y un solo acto modificador (32023R2869). Grado B: SPARQL refleja lo indexado, no garantiza que no haya un acto en trámite.
- **Registro provisional de MiCA de ESMA (CSV oficiales):** `esma.europa.eu/sites/default/files/2024-12/CASPS.csv` (370 filas) y `EMTWP.csv` (50 filas), descargados hoy a las 14:2x UTC. Última actualización dentro del archivo: **6-oct-2026**.
- **No se usó prensa** para ninguna afirmación de esta ficha.

## 2. Lo esencial del texto [H, grado A: texto primario en dos lenguas]

| Artículo | Qué dice |
|---|---|
| **48** (EMT) | Solo puede ofrecer al público una EMT en la UE su emisor, y solo si es **entidad de crédito o entidad de dinero electrónico** y notificó y publicó su libro blanco. Las EMT "se considerarán dinero electrónico". Hay que notificar a la autoridad 40 días hábiles antes de la oferta. |
| **49** (EMT) | El tenedor tiene un **crédito frente al emisor**. Emisión **a la par** contra fondos recibidos. Reembolso **en cualquier momento y a la par**, en fondos que no sean dinero electrónico, **sin comisión**. |
| **50** (EMT) y **40** (ART) | **Prohibición de intereses** en dos niveles: (1) el emisor no puede pagar intereses y (2) **los proveedores de servicios de criptoactivos tampoco** "cuando presten servicios [...] relacionados con" la ficha. El ap. 3 define como interés **cualquier remuneración o beneficio ligado al tiempo de tenencia**, incluidos descuentos o compensaciones de terceros o vía el precio de otros productos. |
| **54** (EMT) | De los fondos recibidos: **al menos 30% en cuentas separadas en entidades de crédito**; el resto en activos seguros, de bajo riesgo y muy líquidos (criterios del art. 38(1)), **en la misma moneda** que la ficha. |
| **36** (ART; y EMT significativas vía art. 58) | Reserva de activos **segregada jurídica y operativamente**, valuada a mercado y **al menos igual** a los créditos de los tenedores. Las normas técnicas de la EBA fijan el mínimo de depósitos en cada moneda, que "no puede ser inferior al 30%". |
| **23** (ART; y EMT en moneda no-UE vía art. 58(3)) | Si el uso **como medio de cambio** dentro de una zona monetaria supera, en promedio trimestral diario, **1 millón de operaciones y 200 millones de EUR**, el emisor debe **dejar de emitir** y presentar en 40 días hábiles un plan para bajar de ahí. |
| **43** (umbral de "significativa") | Entre otros criterios: valor emitido o reserva > **5,000 millones de EUR**; > **2.5 millones de operaciones y 500 millones de EUR** diarios. Basta cumplir 3 criterios (art. 56 para EMT); la supervisión pasa a la EBA. |
| **143(3)** (transición CASP) | Los CASP que operaban conforme a la ley nacional antes del 30-dic-2024 **"podrán seguir haciéndolo hasta el 1 de julio de 2026 o hasta"** que se les conceda o deniegue la autorización del art. 63, **lo que ocurra antes**. Cada Estado podía acortar o eliminar ese plazo. |
| **149** | Aplicación general desde el **30-dic-2024**; títulos III y IV desde el **30-jun-2024**. |

## 3. Hallazgo central [H/I]

1. **[H, A] El 1-jul-2026 fue un precipicio legal, no una fecha administrativa.** El art. 143(3) no da prórroga: después de esa fecha, un CASP sin autorización MiCA no puede seguir prestando servicios en la UE. El estado "solo retiros desde el 1-jul-2026" que la lista de alerta registra para Binance (E5) es exactamente lo que el texto exige a quien no obtuvo la autorización.
2. **[H, A en el dato; B en la lectura] Binance no aparece en el registro de CASP de ESMA.** De 365 entidades únicas (LEI), **ninguna** tiene "Binance" en el nombre, el nombre comercial o el sitio web (dos métodos de lectura, §4). Sus rivales directos sí están: Coinbase (LU, 20-jun-2025), Kraken/Payward (IE, 25-jun-2025), OKX (MT, 27-ene-2025), Crypto.com/Foris DAX (MT, 27-ene-2025), Bybit (AT, 28-may-2025), Bitstamp (LU), Gemini (MT), KuCoin (AT, 27-nov-2025) y Revolut (CY). Bitget tampoco aparece. Lectura: de los 11 exchanges grandes buscados, **solo Binance y Bitget no tienen autorización MiCA notificada**. El registro es "provisional" y tiene rezago (§6), pero la última actualización es del 6-oct-2026, más de tres meses después del precipicio.
3. **[H, A] MiCA prohíbe el rendimiento sobre stablecoins también a los exchanges; GENIUS no.** El art. 50(2) se lo prohíbe a los CASP y el 50(3) cierra la puerta a los beneficios indirectos ligados al tiempo de tenencia. GENIUS, en cambio, solo dirige la prohibición al emisor (sec. 4(a)(11), ficha del 13-oct). Esa diferencia es justo la disputa que frenó CLARITY en EUA (rendimiento pagado por exchanges sobre stablecoins). Es el puente hacia el pendiente (b).
4. **[H, A] Las reservas europeas están más bancarizadas que las de EUA.** MiCA exige **≥ 30% en depósitos bancarios** (art. 54), mientras GENIUS permite una lista cerrada dominada por T-bills ≤ 93 días sin un mínimo de depósitos. [I] Esto cambia el tipo de riesgo de cola: más exposición a la quiebra de un banco (el canal del desanclaje de USDC con SVB, mar-2023), menos al riesgo de liquidar bonos. No es mejor ni peor en abstracto: es otro riesgo.
5. **[H, A] Tether (USDT) no aparece en el registro de EMT de ESMA** (0 de 50 filas; 25 emisores únicos). Circle (Francia) y Paxos (Finlandia) sí. Con el art. 48, una EMT sin emisor autorizado no puede ofrecerse al público en la UE.
6. **[I, C] El art. 23 pone un tope a las stablecoins en dólares dentro de la zona euro.** Por el art. 58(3), una EMT en moneda no-UE que supere 1 millón de operaciones y 200 millones de EUR diarios **como medio de cambio** debe dejar de emitirse. Anualizado son ~73,000 millones de EUR en pagos. Es una barrera explícita a la "dolarización" vía stablecoin en la UE.

## 4. Ejercicio numérico (Python, verificado dos veces)

Scripts fuera del repositorio: `scratchpad/calc/mica_ej.py` y `scratchpad/calc/mica_reg.py`.
- **Método A:** `csv.DictReader` por nombre de columna. **Método B:** `csv.reader` por índice de columna sobre el mismo texto crudo y búsqueda de "binance" en la fila completa unida. Los dos coinciden en todo.
- Las cifras del texto (1 millón / 200,000,000 EUR, 30%, 1-jul-2026, 30-jun-2024, la prohibición del 50(2)) se cotejaron en el XHTML inglés, en el español y en la consolidación 2024-01-09.

Salida real:

```
dias 30-dic-2024 -> 1-jul-2026: 548
dias desde fin transitorio a hoy: 106
dias titulos III/IV aplicables (30-jun-2024) a hoy: 837
EMT 1000000000 EUR -> deposito minimo bancario 300000000 EUR
EMT 10000000000 EUR -> deposito minimo bancario 3000000000 EUR
art.23 tope anualizado EUR: 73.0 mil millones
CASP LEI unicos A=365 B=365
Binance en CASP A=0 B=0
filas autorizadas al 1-jul-2026 A=296 B=296
fechas futuras (errores del registro): [('Raiffeisenbank Rehling eG', '30/10/2026'), ('REGULAR FINANCE SAS', '11/09/2028')]
EMT filas 50 emisores unicos 25
tether 0   circle 3   paxos 4
```

**Ritmo de autorizaciones (primera fecha por LEI):** dic-2025 44, jun-2026 **75** (el mes previo al precipicio), jul 31, ago 17, sep 16 y oct 7 (al 12-oct). Después del 1-jul el ritmo se estabilizó en ~16-17 por mes. Ese ritmo calibra el pronóstico P0129.

## 5. Qué cambia para invertir (`arena-claude-binance`, spot, desde México)

- **[I]** **No hay acción nueva.** La cuenta opera desde México, fuera del perímetro de MiCA. Pero el hallazgo 2 confirma con fuente primaria lo que E5 tenía como dato secundario: Binance quedó **fuera del mercado regulado más grande** que tiene un régimen cripto completo. Es un factor de riesgo reputacional y de flujos (E1), no un evento de 30 días.
- **[I]** **Lo que se vigila de aquí en adelante:** una fila con "Binance" en `CASPS.csv` sería una **señal positiva** de contraparte; un anuncio de cierre de otro mercado grande seguiría siendo ÁMBAR de E5. Se propone añadir `CASPS.csv` como fuente de E5.
- **[I]** **Para la tesis de stablecoins:** en la UE la liquidez en USDT pasa a pares no ofrecidos por CASP autorizados. Para la cuenta en Binance desde México, el USDT sigue siendo el par principal; nada de MiCA lo cambia en 30 días.

## 6. Contrapuntos y límites

- **El registro de ESMA es "provisional"** (lo dice su propio nombre de archivo de dic-2024) y depende de lo que notifica cada autoridad nacional. Tiene **dos fechas imposibles** (30-oct-2026 y 11-sep-2028): son errores de captura, no autorizaciones futuras. Una autorización reciente puede tardar semanas en aparecer.
- **Ausencia en el registro no prueba que Binance no tenga ninguna licencia en la UE**; prueba que no tiene la autorización MiCA de CASP notificada a ESMA al 6-oct-2026. Puede tener registros nacionales de PLD antiguos que ya no habilitan servicios después del 1-jul-2026 (art. 143(3)).
- **No se leyeron** las normas técnicas de la EBA sobre liquidez de reservas (art. 36(4)), que fijan los porcentajes para las ART y EMT significativas, ni las directrices de ESMA sobre la "solicitud inversa" (art. 61). Quedan como pendiente.
- **EUR-Lex no fue accesible**; se usó Cellar, que sirve el mismo documento con el mismo identificador CELEX. Si se exige la vista de EUR-Lex, hay que reintentar desde otra red.
- La comparación con GENIUS usa la ficha del 13-oct; no se releyó hoy la Public Law 119-27.

## 7. Autoexamen (5 preguntas, respuestas en la ficha)

1. ¿Quién puede ofrecer al público una EMT en la UE? (Solo su emisor, si es entidad de crédito o de dinero electrónico y notificó su libro blanco; art. 48. Otros, con consentimiento escrito del emisor.)
2. ¿Puede un exchange autorizado en la UE pagar rendimiento sobre USDC a sus clientes? (No: art. 50(2) y (3), incluido cualquier beneficio ligado al tiempo de tenencia.)
3. ¿Qué porcentaje mínimo de los fondos de una EMT va a depósitos bancarios? (30%, art. 54(a).)
4. ¿Hasta cuándo podía operar un CASP con licencia nacional anterior a MiCA? (Hasta el 1-jul-2026 o hasta que se le concediera o denegara la autorización, lo que ocurriera antes; art. 143(3).)
5. ¿Qué pasa si una stablecoin en dólares supera 1 millón de operaciones y 200 millones de EUR diarios como medio de cambio en la zona euro? (Debe dejar de emitirse y presentar un plan en 40 días hábiles; arts. 23 y 58(3).)

## 8. Estado y pendientes

- **Estado:** "Documentado con comprobación" para MiCA títulos III-IV y art. 143: texto del DOUE en dos lenguas más la consolidación vigente; registro de ESMA leído con dos métodos. La fila de regulación de la Frontera sigue **parcial**: falta CLARITY.
- **Pendientes:**
  - (a) estado de CLARITY después de la votación de cloture fallida del 15-sep (congress.gov), con foco en el rendimiento sobre stablecoins (hallazgo 3);
  - (b) normas técnicas de la EBA sobre liquidez de reservas (art. 36(4)) y directrices de ESMA sobre solicitud inversa (art. 61);
  - (c) ANPRM de la CFTC 2026-20888;
  - (d) Federal Register hacia el 12-nov (P0117);
  - (e) México: Disposiciones de la CNBV para IFPE;
  - (f) reintentar EUR-Lex directo.

**Grado global:** A en el texto (DOUE en dos lenguas más la consolidación) y en el dato del registro de ESMA; B en la ausencia de reformas (SPARQL) y en la lectura de Binance como uno de los dos grandes sin autorización MiCA; C en la lectura del art. 23 como tope a la dolarización.
