# Ficha de avance · 20-oct-2026 · El ANPRM de la CFTC sobre spot cripto minorista apalancado ("Regulation CTX" y "Regulation CAM", 91 FR 64811)

> Corrida de las 08:17 CDMX (14:2x UTC), estudio profundo. Nivel **Frontera** (regulación en EUA), grupo G5 (mercado, on-chain e institucional). Recurso del dueño: **02 Bankless** (episodio con el presidente de la CFTC, Mike Selig).
>
> **Por qué este tema.** Leer el ANPRM completo es un pendiente explícito desde el 13-oct (fichas del 13 y 14-oct; columna `siguiente_prueba` de la fila de regulación en `estado-de-dominio.csv`). Hoy es además el tema de los pódcasts. No repite el 16-oct: aquella ficha trató CLARITY (ley del Congreso, atorada en el Senado). Esta trata lo que la CFTC puede hacer **sin ley nueva**, con la sección 2(c)(2)(D) de la CEA.

## 0. Preguntas de hoy

1. ¿Qué propone la CFTC exactamente, y con qué estatus (ANPRM, no regla)?
2. ¿Qué dice de "actual delivery", y por qué importa para la custodia?
3. ¿Cuándo podría regir lo más pronto, y toca a la cuenta `arena-claude-binance`?
4. Números: ¿por qué preocupa el apalancamiento minorista en una ventana de 28 días?

## 1. Acceso y fuentes (declarado)

- **Federal Register, 91 FR 64811-64840, doc. 2026-20888, RIN 3038-AF80**, "Regulation Crypto Asset Transactions and Regulation Crypto Asset Markets", publicado el 13-oct-2026. Metadatos de la [API del Federal Register](https://www.federalregister.gov/api/v1/documents/2026-20888.json) y texto del [PDF de govinfo](https://www.govinfo.gov/content/pkg/FR-2026-10-13/pdf/2026-20888.pdf) (506,722 bytes; el HTML del FR pidió verificación de acceso). **Acceso: sección.** Se extrajo el texto completo, ~38 mil palabras con las piezas vecinas del PDF, y se leyeron estas partes: DATES/ADDRESSES; II.A (2(c)(2)(D) y su excepción de 28 días); II.C.4; III completa (Regulation CTX: "covered offer" y "actual delivery"); IV (preguntas de CTX); V.A (panorama de CAM); V.D (margen); VI; y el apéndice de votación. **No se leyeron** I.B (historia), V.B (principios básicos de CAM), V.C, V.E-V.H ni el Apéndice A. **Grado A** en el texto.
- **CFTC, comunicado 9307-26** del 5-oct-2026 ([cftc.gov](https://www.cftc.gov/PressRoom/PressReleases/9307-26)), leído íntegro. **Grado A.**
- **Bankless con Selig (recurso 02):** **no verifiqué** que el episodio exista. Una búsqueda web no lo encontró, y solo aparecieron notas de terceros sobre la postura de Selig respecto al apalancamiento. **Grado C** hasta tener la URL del feed. Esta ficha no depende de él.
- **Datos del ejercicio, grado A:** 3,351 velas diarias BTCUSDT de [`data-api.binance.vision`](https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1d), del 17-ago-2017 al 19-oct-2026.

## 2. Lo que dice el texto [H, grado A]

- **Estatus:** es un **ANPRM**, un aviso previo que solo pide comentarios. No propone texto de regla. La propia CFTC dice que lo usará "to inform potential future agency action, such as a rulemaking". Los comentarios cierran el **14-dic-2026**.
- **Votación:** "Chairman Selig voted in the affirmative. No Commissioner voted in the negative". El resumen solo nombra a Selig. Lo más probable es que hoy sea el único comisionado (B, inferido del apéndice).
- **Fechas que no cuadran:** el comunicado del 5-oct dice "today published", pero el FR dice "Issued in Washington, DC, on October 8, 2026". No está resuelto (B). Lo más probable es que el 5-oct sea la publicación en cftc.gov y el 8-oct la firma de la versión para el FR.
- **La base legal es la sección 2(c)(2)(D) de la CEA** (Dodd-Frank, la que cerró el "hueco Zelener"). Una operación minorista con una mercancía, hecha u **ofrecida** con apalancamiento, margen o financiamiento, se trata como futuro y debe ir en una bolsa registrada. La excepción es la **"actual delivery" dentro de 28 días**. El ANPRM anuncia dos piezas:
  - **Regulation CTX** (interpretación). Dos ideas centrales:
    - **"Covered offer":** la oferta de apalancamiento puede venir en los documentos estándar (alta del cliente, términos del exchange, contrato de margen) y "attaches to all agreements, contracts, or transactions" a los que aplica. **Si un exchange ofrece margen a un cliente minorista de EUA, aun sus compras al contado pagadas al 100% quedan dentro de 2(c)(2)(D).** También cuenta el financiamiento de un tercero "acting in concert" (plataformas asociadas, reparto de ingresos, publicidad).
    - **"Actual delivery":** siguiendo *Monex* (9.º Cir.), exige "some meaningful degree of possession or control". La CFTC cree de forma preliminar que, en cripto, eso "may require possession of the credentials (e.g., private key(s))". Si el token da derechos de gobernanza o de staking, la entrega real "may require unfettered access", por ejemplo poder hacer staking "without being subject to fees charged by an intermediary". Una compra pagada que solo vive en el libro interno del exchange es entrega **constructiva**, no real, y mientras tanto sigue sujeta al régimen de futuros.
  - **Regulation CAM** ("crypto asset market"): una subcategoría de bolsa registrada (DCM) hecha para estas operaciones. Admite modelos integrados (bolsa + FCM + cámara de compensación en un mismo grupo), con intermediación obligatoria de un FCM, sujeto a la Ley de Secreto Bancario: KYC y reportes de operaciones sospechosas. También prevé "eligible leverage providers" y un régimen de margen todavía abierto (preguntas V.D.i-vi: si debe ser prescriptivo, quién lo fija y qué cripto sirve como colateral, con mínimos de capitalización y volumen).
- **Preguntas:** el texto lleva ~105 signos de interrogación en las secciones IV-V (conteo propio en Python: 4 en IV y el resto en V). Lo que la CFTC está pidiendo es diseño, no comentarios sobre una regla ya escrita.
- **Tono:** el texto culpa a la "regulation by enforcement" de 2021-2024 de haber empujado a los participantes "offshore". Cita la demanda de la CFTC contra Binance y CZ de 2023 como parte de esa historia.

## 3. Ejercicio numérico (comprobado en Python)

Script: [`2026-10-20-cftc-anprm-spot-apalancado.py`](2026-10-20-cftc-anprm-spot-apalancado.py) (`python3 -I ...`, solo biblioteca estándar). Se corrió el 20-oct hacia las 14:23 UTC y pasó sus aserciones.

**[1] Calendario.** 13-oct + 60 días = 12-dic, que es sábado. El cierre se corre al lunes 14-dic, igual que DATES del FR (aserción OK). Ruta mínima con supuestos propios [I]: 60 días para analizar comentarios, un NPRM con 60 días de comentarios, 60 días hasta la regla final y 60 días de vigencia de la CRA para una regla mayor. Con eso, la regla **no rige antes de ~11-ago-2027**. Es un piso optimista: las reglas de la CFTC suelen tardar más, y un cambio de mayoría en la comisión puede detenerla.

**[2] Por qué preocupa el apalancamiento en 28 días.** Se toma un largo aislado con apalancamiento L y margen de mantenimiento de 0.5%. Su precio de liquidación relativo es b = (1−1/L)/(1−0.005). Se calcula la probabilidad de tocar b en 28 días por dos métodos. **A:** fórmula cerrada de cruce de barrera con un GBM, usando la vol30 de hoy (32.09%) y una vol estresada de 60%. **B:** frecuencia histórica con el **mínimo diario** de los 28 días siguientes a cada cierre (3,323 ventanas, y aparte desde ago-2022).

| L | barrera b | A, vol 32% | A, vol 60% | B, 2017-2026 | B, ago-2022 a 2026 |
|---|---|---|---|---|---|
| 2x | 0.5025 | ≈0% | ≈0% | 1.35% | 0.00% |
| 3x | 0.6700 | ≈0% | 1.95% | 6.38% | 0.86% |
| 5x | 0.8040 | 1.57% | 21.07% | 21.16% | 10.58% |
| 10x | 0.9045 | 27.21% | 57.33% | 46.01% | 35.82% |
| 20x | 0.9548 | 61.65% | 79.84% | 70.72% | 65.57% |

**Lectura [I]:**
- Con la vol de hoy, la fórmula **subestima mucho** la cola entre 3x y 5x. A 5x da 1.6%, contra 21% de la historia completa y 11% desde 2022. Hay tres razones: colas gruesas, cambios de régimen de volatilidad y que el mínimo intradía cuenta.
- A 10x o más, casi la mitad de las ventanas de 28 días liquida. Esa es la población que el régimen de margen de la CAM quiere proteger.
- **Contraste con la cuenta:** un spot pagado al 100% no se liquida nunca. Su peor caída dentro de una ventana de 28 días tiene mediana de 8.6%, p95 de 35.4% y máximo de 63.4%. Es dolorosa pero recuperable, y la gestionan el filtro SMA200 y los cortacircuitos, no un motor de liquidación.

## 4. Qué cambia para invertir [I/O]

- **Para `arena-claude-binance`, nada directo.** El ANPRM regula a clientes minoristas de EUA y la cuenta es mexicana, solo spot y sin margen (§4b de REGLAS-MOTOR). No hay catalizador en 30 días; la fecha más cercana es el cierre de comentarios del 14-dic.
- **Lección de custodia, que sí aplica.** El regulador de EUA dice por escrito, de forma preliminar, que el BTC en el libro interno de un exchange es **entrega constructiva**: el cliente tiene un derecho frente al exchange, no la moneda. Es la misma tesis de los capítulos cripto/01 y 04 y de la contingencia de contraparte. La regla del sistema se mantiene: el saldo en Binance es riesgo de contraparte, vigilado con E1-E10.
- **Binance (E5).** El marco busca traer a tierra a los exchanges, no castigar a los de fuera. Para un no estadounidense no cambia el riesgo legal de Binance en México. **E5 sigue en ÁMBAR, sin cambio.**
- **Mercado [O].** Una CAM con margen regulado haría crecer el apalancamiento onshore en EUA (a partir de 2027 o 2028). Eso subiría el open interest y la reflexividad en las caídas, lo que es un argumento más para no usar margen.

## 5. Contrapuntos y límites

- No leí V.B, V.C, V.E-V.H ni el Apéndice A. Puede haber detalles de custodia y segregación que cambien el punto 4.
- La ruta de calendario es un supuesto propio, no un plazo legal, salvo los 60 días de la CRA para una regla mayor. Una interpretación final de "actual delivery" podría salir como guía, más rápido que una regla.
- El ejercicio supone margen de mantenimiento de 0.5% y margen aislado, ignora funding y comisiones, y usa mínimos diarios de Binance: una mecha en otro venue puede liquidar antes. La ventana histórica B incluye 2017-2018 y 2020, de vol muy distinta a la de hoy. Por eso se separa la submuestra desde 2022.
- Que haya un solo comisionado vuelve frágil todo el proceso: una comisión completa podría reabrirlo.

## 6. Autoexamen

1. ¿Por qué una compra spot pagada al 100% puede caer bajo 2(c)(2)(D)? *Porque la sola oferta de margen en los documentos del exchange es una "covered offer" que se extiende a todas las operaciones del cliente minorista (sección III.A).*
2. ¿Qué exige "actual delivery" según el ANPRM? *Control significativo; de forma preliminar, poseer las llaves privadas. Con staking o gobernanza, poder ejercerlos sin un intermediario que cobre.*
3. ¿Cuándo es lo más pronto que podría regir? *~ago-2027 con supuestos optimistas. Los comentarios cierran el 14-dic-2026.*
4. A 5x y en 28 días, ¿qué dice la historia frente a la fórmula con la vol de hoy? *21% (11% desde 2022) contra 1.6%: la fórmula subestima la cola.*

## 7. Estado

**Documentado con comprobación** (texto A, por sección; ejercicio en Python con aserciones). Siguiente prueba:
- leer V.B, V.E-V.H y el Apéndice A (custodia, segregación, cámara de compensación);
- en regulations.gov, contar los comentarios del RIN 3038-AF80 y ver quiénes comentan (Coinbase, Kraken y CME);
- confirmar en el feed de Bankless el episodio con Selig;
- vigilar la composición de la comisión.

Sin efecto en la cuenta. Pronóstico del día: P0154 (ETH, no regulatorio; ver la bitácora).
