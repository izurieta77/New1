# Ficha de avance · 22-oct-2026 · ¿Tether infla el precio de BTC? Griffin y Shams (JF 2020) puestos a prueba con 2020-2026

> Corrida de las 08:17 CDMX (14:2x UTC), estudio profundo. Nivel **Doctorado** (literatura de manipulación), grupo G5 (mercado, on-chain e institucional).
>
> **Por qué este tema.** Es el siguiente de la cola académica que fijó el plan el 19-oct (Liu-Tsyvinski → Makarov-Schoar → **Griffin-Shams**). Además viene al caso hoy: el USDT en circulación bajó US$1.2 mil millones en una semana (184.02 → 182.80 mm según DefiLlama), mientras BTC cae a 81.7k. Hay que saber si las emisiones y las quemas de USDT sirven de señal de precio o solo hacen ruido.

## 0. Preguntas de hoy

1. ¿Qué afirma el paper y con qué evidencia?
2. ¿Siguen apareciendo sus dos huellas fuera de muestra (jun-2020 a oct-2026), con datos públicos diarios? La primera: la emisión llega después de las caídas. La segunda: la emisión anticipa alzas.
3. ¿Qué cambia para la cuenta cripto y para la señal E8?

## 1. Acceso y fuentes (declarado)

- **Griffin, J. M. y Shams, A. (2020). "Is Bitcoin Really Untethered?"** *Journal of Finance* 75(4):1913-1964, [doi:10.1111/jofi.12903](https://doi.org/10.1111/jofi.12903).
  - **Acceso: solo el resumen.** Leí el resumen oficial en [RePEc/IDEAS](https://ideas.repec.org/a/bla/jfinan/v75y2020i4p1913-1964.html). Wiley ([texto](https://onlinelibrary.wiley.com/doi/full/10.1111/jofi.12903)) y SSRN ([3195066](https://papers.ssrn.com/abstract=3195066)) respondieron **403**. Había una copia en un servidor de terceros (`ucg.cdn.doma.dev`) que **no usé**: no consta que esté autorizada.
  - Las cifras de la sección 2 que no vienen en el resumen salen de un **resumen secundario, grado C**: [Quantpedia](https://quantpedia.com/a-very-influential-paper-about-tether-bitcoin-relationship-manipulation/), que cita 50%, 64%, 87 horas, mar-2017 a mar-2018 y −6% a fin de mes. Hay que cotejarlas con el texto cuando haya acceso legal (una biblioteca o el sitio del autor).
- **Contraste regulatorio, grado A:** [CFTC, comunicado 8450-21 (15-oct-2021)](https://www.cftc.gov/PressRoom/PressReleases/8450-21). Multa de US$41 M a Tether y de US$1.5 M a Bitfinex. Tether tuvo reservas suficientes "for only 27.6% of the days in a 26-month sample time period from 2016 through 2018".
- **Datos de la prueba, grado A en datos:**
  - USDT en circulación diario de [DefiLlama](https://stablecoins.llama.fi/stablecoin/1);
  - velas diarias BTCUSDT de [`data-api.binance.vision`](https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=1000).
- **Conflictos de interés:** Griffin fundó Integra FEC, una consultora de litigios financieros, y el paper se citó en demandas colectivas contra Tether y Bitfinex. Tether lo rechazó públicamente (prensa, C). Nada de esto invalida los datos del paper, pero sí obliga a leer con cuidado la parte que atribuye intenciones.

## 2. Lo que dice el paper [H]

- **Tesis (resumen oficial, A):** las compras con Tether "are timed following market downturns and result in sizable increases in Bitcoin prices". Además, el flujo:
  - "is attributable to one entity";
  - "clusters below round prices";
  - induce autocorrelaciones asimétricas;
  - y sugiere reservas insuficientes antes de los fines de mes.
  - La conclusión es que todo esto encaja mejor con la **hipótesis de oferta** (dinero digital sin respaldo que infla precios) que con la de **demanda** (inversionistas con efectivo).
- **Magnitudes (Quantpedia, C):**
  - muestra de mar-2017 a mar-2018;
  - las 87 horas con los mayores flujos rezagados de Tether y BTC, menos de 1% de la serie, se asocian con **~50% del rendimiento compuesto de BTC** y con ~64% del de otras seis criptomonedas;
  - en los meses de mucha emisión hay un rendimiento anormal de **−6% al cierre de mes**.
- **Corroboración posterior (A):** la CFTC confirmó en 2021 la mitad del argumento, la de las reservas: el respaldo fue insuficiente casi tres cuartas partes de los días de 2016-2018. **No** confirmó la otra mitad (la manipulación de precio): esa orden no la trata.

## 3. Ejercicio numérico: las dos huellas, de jun-2020 a oct-2026 (comprobado en Python)

Script [`2026-10-22-griffin-shams-tether.py`](2026-10-22-griffin-shams-tether.py), corrido el 22-oct a las 14:2x UTC. Son 2,334 días consecutivos, del 1-jun-2020 al 21-oct-2026.

- **Emisión neta del día d:** ln(circ a las 00:00 del d+1 / circ a las 00:00 del d), en puntos base.
- **Rendimiento del día d:** el de la vela diaria BTCUSDT del día d.
- Errores Newey-West con 5 rezagos.
- La muestra arranca en jun-2020 porque, antes de esa fecha, la serie de DefiLlama no cubre todas las cadenas. Marca 0.03 mm el 1-ene-2019, cuando el dato real era de ~2 mm.

| Tramo | H1: emisión_d ~ r_d, r_d−1, r_d−2, r_d−3 (b, pb de emisión por unidad de log-rend.; t NW) | H2: r_d+1 (%) ~ emisión_d (pb), r_d | Decil superior de emisión: r de los 3 días previos / r del día siguiente (incondicional) |
|---|---|---|---|
| Todo (2,334 d) | **+114 (2.0), +270 (4.5), +189 (3.3), +152 (3.1)** | b = 0.0020 (t 1.18) | **+2.04%** (+0.27%) / +0.38% (+0.09%) |
| jun-2020 a 2021 (579 d) | +59 (0.5), **+428 (3.3)**, +145 (1.4), +173 (1.8) | b = 0.0014 (t 0.78) | +2.79% (+0.85%) / +0.71% (+0.27%) |
| 2022-2026 (1,755 d) | **+128 (3.2), +137 (4.1), +195 (3.4), +114 (2.5)** | b = 0.0029 (t 0.80) | +1.28% (+0.09%) / +0.07% (+0.03%) |

Con r_d+2 en lugar de r_d+1, por si la foto de DefiLlama va desfasada, H2 sigue en cero: t 0.87 en todo el periodo y t 1.06 en 2022-2026.

**Lectura [I]:**

1. **H1 se invierte.** Fuera de la muestra del paper, la emisión de USDT llega **después de alzas** de BTC, no de caídas. Todos los coeficientes son positivos, y en 2022-2026 los cuatro son significativos. En los días de emisión más alta, BTC había subido +2.0% en los tres días previos, contra +0.27% en un día cualquiera. Esto es la huella de la **hipótesis de demanda**: entra dinero con efectivo y Tether acuña para atenderlo.
2. **H2 desaparece.** Una vez que se controla por el rendimiento del día, la emisión no predice el rendimiento del día siguiente (t entre 0.8 y 1.2). La diferencia del decil superior (+0.38% contra +0.09%) no es significativa en la regresión. En 2022-2026 casi no existe: +0.07% contra +0.03%.
3. **Hoy:** emisión neta de **−0.73 mm USD en 30 días** y −1.2 mm del 15 al 22-oct, con quemas de −382 M (15-oct), −430 M (19-oct) y −234 M (20-oct). BTC bajó −2.96% (log) en 30 días. Es lo que predice la hipótesis de demanda, con la causalidad al revés: se queman USDT porque hay menos demanda, no al contrario. Las quemas **no** son una señal de precio que se pueda operar.

## 4. Qué cambia para invertir [I/O]

- **No se agrega ninguna regla de "emisión de USDT" al filtro.** Al nivel diario no tiene poder predictivo fuera de muestra, y su signo es el de la demanda. Esto coincide con lo que ya mostraron Liu-Tsyvinski (19-oct): la mayor parte de las "señales" cripto no sobreviven fuera de muestra.
- **Para E8 (stablecoins en Binance), la emisión no es la variable correcta.** La lección del paper que sí sigue vigente es la de las **reservas** (CFTC, 27.6% de los días). El riesgo de Tether se vigila con:
  - la paridad, hoy USDT/USD 0.99891 en Kraken;
  - las atestaciones;
  - la regla que ya existe: la reserva va en MXN y USDT solo se usa para cruzar.
- **Una quema grande y repentina** (más de 2-3 mm en un día) que coincida con un descuento de más de 1% en la paridad sí sería un evento de cola (E8 ÁMBAR/ROJA). Hoy la mayor es de −0.43 mm, con la paridad intacta.

## 5. Contrapuntos y límites

- **No es una réplica.** El paper usa flujos **horarios** de Tether entre Bitfinex y otros exchanges, agrupados por cartera. Aquí se usa la oferta **total diaria**, que mezcla canjes institucionales y cambios entre cadenas: hay pares −2/+2 mm en días seguidos que son contabilidad, no flujo. Un efecto que dura horas se diluye al pasarlo a días. La evidencia solo dice que **la huella diaria no está**, no que el mecanismo horario haya sido falso en 2017.
- **El régimen cambió.** Después de 2021 hubo atestaciones, una orden de la CFTC, un acuerdo con la fiscalía de NY, opinión de KPMG sobre 2025 (cap. 05) y ETFs spot que traen demanda en efectivo. Que en 2022-2026 la huella de demanda sea más fuerte encaja con ese cambio.
- **Calidad de los datos:** DefiLlama reconstruye la oferta por cadena, y la cobertura anterior a jun-2020 está incompleta (ya corregido). Puede haber revisiones del día en curso.
- **Lo que no se verificó:** las cifras de 50%, 64%, 87 horas y −6% vienen de un resumen secundario (C). Falta el texto del JF.

## 6. Autoexamen

1. ¿Qué signo tiene H1 bajo la hipótesis de oferta y cuál bajo la de demanda? *Oferta: negativo (se emite después de caídas para sostener el precio). Demanda: positivo (se emite cuando entra dinero, que tiende a coincidir con alzas).*
2. ¿Por qué no sirve "la emisión del día predice el rendimiento" sin controlar por r_d? *Porque la emisión está correlacionada con el rendimiento propio (H1), y el rendimiento propio tiene autocorrelación. Sin el control, se confunden las dos cosas.*
3. ¿Qué parte de la tesis confirmó la CFTC en 2021? *La de las reservas insuficientes (27.6% de los días con respaldo completo en 2016-2018), no la de la manipulación.*
4. ¿Por qué la quema de −1.2 mm de esta semana no justifica vender? *Porque, fuera de muestra, la emisión no predice el día siguiente (t ≈ 1), y su signo responde a la demanda pasada.*

## 7. Estado

**Documentado con comprobación** de las dos huellas fuera de muestra, con acceso al **resumen** del paper.

Pendiente:
- cotejar el texto íntegro del JF (biblioteca o versión del autor);
- repetir con datos **horarios** de acuñación en la Treasury de Tether en Tron y Ethereum, para acercarse al diseño original;
- estudio de atención como predictor (§4.2 de Liu-Tsyvinski).

Pronóstico ligado: **P0166** (USDT en circulación, DefiLlama, el 20-nov ≥ 182.80 mm; p = 0.42).
