# V05. Pre-registro: SPIVA y fiscalidad del SIC

> Escrito el 2026-09-25 a las 05:37 UTC, **antes** de abrir cualquier PDF de SPIVA, antes de descargar precios y antes de calcular nada. Este archivo no se edita después: su huella SHA-256 queda en `SHA256SUMS.txt` antes de la primera descarga. Cualquier cambio posterior va a "Desviaciones del pre-registro" en `README.md`.
>
> Lo único que se sabe al escribirlo: el texto de las afirmaciones recibidas y que S&P Dow Jones Indices (S&P DJI) publica los *SPIVA Scorecards* en PDF dos veces al año (cierre de año y mitad de año).

## 1. Afirmaciones recibidas (literales, 25-sep-2026)

- **A1.** "el 85.6% de los fondos grandes de EUA queda debajo del S&P 500 a 10 años" (confirmado, según el emisor, "con los PDF oficiales de SPIVA").
- **A2.** "en México el 82.9% queda debajo de su índice" (a 10 años, contra el S&P/BMV IPC).
- **A3.** "Los fondos mexicanos que sí ganaron tenían en común una cartera muy distinta a la de su índice y parte de su dinero en fondos o ETFs extranjeros."

## 2. Fuentes admitidas

- **Primarias para A1 y A2:** solo los PDF de los *SPIVA U.S. Scorecard* y *SPIVA Latin America Scorecard* publicados por S&P DJI en `spglobal.com`. Notas de prensa, blogs o resúmenes de terceros solo sirven como pista, nunca como confirmación.
- **Primarias para A3:** un documento de S&P DJI (scorecard, comentario o investigación) o datos de los propios fondos (prospectos, carteras publicadas, CNBV/AMIB) que documenten *active share* o exposición extranjera **de los fondos que superaron al índice**. Un texto que diga que "algunos fondos tienen exposición extranjera" sin ligarlo a los ganadores no confirma A3.

## 3. Ediciones que se revisan (lista cerrada)

Todas las ediciones de *SPIVA U.S.* y *SPIVA Latin America* publicadas entre el cierre de 2023 y el 25-sep-2026 que se puedan descargar del sitio oficial: Year-End 2023, Mid-Year 2024, Year-End 2024, Mid-Year 2025, Year-End 2025 y Mid-Year 2026 (si ya existe). Para cada una se registra:

- A1: % de fondos de la categoría *All Large-Cap Funds* por debajo del S&P 500 a 10 años (reporte 1, rendimiento absoluto), y la fecha de corte y de publicación.
- A2: % de fondos de la categoría *Mexico Equity* por debajo del S&P/BMV IPC a 10 años, y la fecha de corte y de publicación.
- Las ediciones que no se puedan descargar se listan como "no obtenidas", sin inferir su contenido.

## 4. Criterio de veredicto para A1 y A2

- **Confirmada:** la cifra exacta (con tolerancia de ±0.05 pp por redondeo) aparece en la edición **más reciente** publicada al 25-sep-2026, en la categoría y el horizonte afirmados.
- **Confirmada con matices:** la cifra aparece en una edición oficial pero (a) no es la más reciente, o (b) la categoría, el horizonte o la métrica difieren (por ejemplo, ajustada por riesgo o ponderada por activos), o (c) la etiqueta de la afirmación no corresponde a la del reporte (por ejemplo, "fondos grandes" frente a *All Large-Cap Funds*). El matiz se describe siempre.
- **No confirmada:** la cifra no aparece en ninguna de las ediciones revisadas.
- Se reporta además la cifra de la edición más reciente, aunque la afirmación no se confirme.

## 5. Criterio para A3

- **Confirmada:** una fuente primaria del punto 2 liga a los fondos ganadores con *active share* alto **y** con exposición extranjera.
- **Confirmada con matices:** una fuente primaria documenta solo una de las dos características, o las documenta para la categoría sin distinguir ganadores de perdedores.
- **No confirmada:** no hay fuente primaria que lo documente. Esto no prueba que sea falso.

## 6. Análisis B (mecánico, con datos propios; descriptivo más una prueba)

Pregunta: ¿cuánto ganaría contra el IPC un fondo mexicano que solo cambia una parte de su cartera por el S&P 500, sin talento alguno para elegir acciones?

- **Ventana:** los 10 años que cubre la edición donde aparece A2. Si A2 no aparece, la ventana de la edición más reciente de SPIVA Latin America.
- **Series (en MXN, mensuales, de fin de mes):**
  - IPC con dividendos: `NAFTRAC.MX` de Yahoo, columna `adjclose` (incluye la comisión del ETF, así que queda ligeramente por debajo del índice de rendimiento total).
  - S&P 500 con dividendos en MXN: `SPY` de Yahoo, `adjclose` (dividendos brutos, sin retención) por el tipo de cambio de fin de mes `DEXMXUS` de FRED (último dato hábil del mes).
  - Carteras fijas IPC/S&P con rebalanceo mensual: 100/0, 90/10, 80/20, 70/30 y 50/50.
- **Qué se reporta:** CAGR de cada cartera, diferencia de CAGR contra 100/0 (en pp por año), y la fracción en S&P 500 que haría falta para compensar 1, 2 y 3 pp de gastos anuales (interpolación lineal sobre la diferencia de CAGR).
- **Prueba:** diferencia mensual S&P(MXN) − IPC en la ventana, media, t Newey-West con 6 rezagos e IC 95%. Veredicto: apoyo si el límite inferior > 0, contraria si el superior < 0, inconcluso en otro caso. Es una sola prueba.
- **Conclusión que se permitirá:** solo la mecánica ("con X% en el S&P se superaba al IPC por Y pp en esa ventana"). **No** se concluirá que los fondos ganadores ganaron por eso, a menos que A3 quede confirmada por fuente primaria.

## 7. Parte documental de fiscalidad (sin veredicto estadístico)

Se verifican con fuente primaria (ley, DOF, SAT, IRS, Tesoro de EUA, BMV, emisor del ETF, GBM) y se etiqueta cada punto como **verificado**, **parcialmente verificado** o **no verificado**:

1. ISR de 10% sobre la ganancia en BMV y SIC (persona física residente), sin retención en la venta, y cómo se aplican las pérdidas.
2. Dividendos de emisoras mexicanas y extranjeras del SIC: retención en EUA y 10% en México.
3. Tasa de retención anual de ISR sobre intereses para 2026 según la Ley de Ingresos de la Federación 2026.
4. Constancia fiscal anual de GBM.
5. Impuesto sucesorio de EUA para no residentes: exención de 60,000 USD, existencia o no de tratado México-EUA en sucesiones, y si la custodia vía Indeval/SIC cambia el *situs* de acciones y ETFs de EUA. Si no hay certeza, se dice.
6. ETFs UCITS domiciliados en Irlanda listados en el SIC (existencia verificada en BMV o en datos de mercado) y tratamiento de dividendos (15% en el fondo irlandés frente a 10% del tratado México-EUA con W-8BEN, o 30% sin él).

## 8. Lo que no se hará

- No se adopta ninguna cifra de SPIVA sin haberla leído en el PDF oficial congelado en `datos/`.
- No se da asesoría fiscal: el capítulo describe normas vigentes con fuente y marca lo no verificado. Fase 0: sin recomendaciones reales.
