# Monitor geopolitico 2026-09-25

> Generado por herramientas/geopolitica.py. Hechos con fecha y fuente; la lectura es del analista. Un precio de mercado de prediccion es una probabilidad implicita neutral al riesgo, no una verdad: revisar liquidez, diferencial compra/venta y criterio de resolucion antes de usarlo.

Palabras clave: Fed, recession, tariff, Taiwan, China, Iran, Russia, Ukraine, Mexico, oil, election

## 1. Indice de riesgo geopolitico (Caldara e Iacoviello)

Fuente: https://www.matteoiacoviello.com/gpr.htm (conteo de articulos de prensa sobre tensiones, amenazas y actos geopoliticos; base 1985-2019 = 100). Mensual y diario.

Ultimo mes: 2026-08 (percentil respecto a 500 meses desde 1985).

| Serie | Ultimo | Prom. 3m | Prom. 12m | Hace 12m | Percentil historico |
|---|---|---|---|---|---|
| GPR total | 117.9 | 155.1 | 171.1 | 139.0 | 78 |
| Amenazas (GPRT) | 130.7 | 178.9 | 192.2 | 160.4 | 82 |
| Actos (GPRA) | 120.3 | 162.0 | 176.4 | 121.7 | 80 |

Por pais (porcentaje de articulos que mencionan riesgo geopolitico y al pais; percentil contra su propia historia desde 1985):

| Pais | Mes | Ultimo | Prom. 12m | Percentil |
|---|---|---|---|---|
| VEN | 2026-08 | 0.18 | 0.57 | 95 |
| SAU | 2026-08 | 0.58 | 0.62 | 94 |
| ISR | 2026-08 | 1.11 | 2.02 | 92 |
| CHN | 2026-08 | 0.93 | 1.16 | 89 |
| UKR | 2026-08 | 0.91 | 1.21 | 88 |
| MEX | 2026-08 | 0.15 | 0.20 | 86 |
| TWN | 2026-08 | 0.14 | 0.22 | 85 |
| IND | 2026-08 | 0.31 | 0.43 | 84 |
| USA | 2026-08 | 3.10 | 4.41 | 83 |
| TUR | 2026-08 | 0.33 | 0.41 | 81 |
| KOR | 2026-08 | 0.36 | 0.36 | 81 |
| RUS | 2026-08 | 1.16 | 1.58 | 77 |
| JPN | 2026-08 | 0.24 | 0.36 | 64 |
| DEU | 2026-08 | 0.35 | 0.70 | 51 |

Diario al 2026-09-21: GPRD 165.2, media 7 dias 155.1, media 30 dias 153.4 (percentil 5 anios de la media 30d: 75).

Picos de los ultimos 90 dias:

| Fecha | GPRD | Evento anotado por los autores |
|---|---|---|
| 2026-07-14 | 333.2 |  |
| 2026-07-24 | 309.0 |  |
| 2026-07-23 | 270.2 |  |
| 2026-06-25 | 227.0 |  |
| 2026-07-30 | 226.7 |  |

Lectura (Caldara e Iacoviello, AER 2022, 112(4): 1194-1225): un GPR alto anticipa menor inversion y empleo y se asocia con mayor probabilidad de desastre y mayor riesgo a la baja; los efectos adversos vienen tanto de las amenazas como de los actos. Usarlo como variable de regimen, no como senal aislada.

### 1b. AI-GPR (Iacoviello, clasificacion con LLM; CSV)

Fuente: https://www.matteoiacoviello.com/ai_gpr.html (articulos puntuados por un LLM; media 100 en 1985-2019). Percentil contra la historia desde 1985.

Ultimo mes: 2026-08.

| Serie | Ultimo | Prom. 12m | Percentil |
|---|---|---|---|
| AI-GPR total | 152.0 | 182.3 | 91 |
| Amenazas | 151.2 | 177.6 | 92 |
| Actos | 157.2 | 203.1 | 89 |
| Petroleo (Oil GPR) | 569.7 | 645.1 | 98 |
| Sin petroleo | 124.7 | 152.0 | 81 |

Por tipo de evento (contribucion al indice):

| Tipo | Ultimo | Prom. 12m | Percentil |
|---|---|---|---|
| Conflicto militar | 70.1 | 91.6 | 93 |
| Tension diplomatica | 37.2 | 45.4 | 73 |
| Otros | 18.8 | 16.2 | 95 |
| Sanciones | 15.7 | 8.4 | 99 |
| Terrorismo | 7.0 | 11.1 | 21 |
| Guerra civil | 1.6 | 4.3 | 1 |
| Amenaza nuclear | 1.3 | 2.9 | 9 |
| Golpe de Estado | 0.4 | 2.4 | 18 |

Por pais (rol: iniciador + respondiente + contagio):

| Pais | Ultimo | Prom. 12m | Percentil |
|---|---|---|---|
| Iran | 61.65 | 68.61 | 99 |
| Saudi Arabia | 16.28 | 15.98 | 96 |
| USA | 116.72 | 150.23 | 93 |
| Israel | 28.53 | 47.35 | 92 |
| South Korea | 4.81 | 2.49 | 91 |
| Ukraine | 25.20 | 22.62 | 90 |
| Russia | 35.11 | 33.56 | 86 |
| Turkey | 5.10 | 3.00 | 83 |
| Venezuela | 1.70 | 14.98 | 80 |
| China | 16.00 | 21.94 | 80 |
| Taiwan | 1.27 | 2.03 | 80 |
| Mexico | 1.91 | 5.35 | 61 |
| Germany | 3.96 | 5.09 | 57 |
| Japan | 2.19 | 3.62 | 43 |
| India | 1.63 | 4.06 | 26 |

Diario al 2026-08-31: AI-GPR promedio 30 dias 149.2; Oil GPR promedio 30 dias 557.8; maximo 30 dias 248.6 el 2026-08-25.

## 2. Polymarket

### Fed

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| Will no Fed rate cuts happen in 2026? | Yes | 97.0% | 0.97/0.97 | 8.5 M | 2027-01-01 | [ver](https://polymarket.com/event/how-many-fed-rate-cuts-in-2026) |
| Will there be no change in Fed interest rates after the October 2026 meeting? | Yes | 32.5% | 0.32/0.33 | 3.5 M | 2026-10-29 | [ver](https://polymarket.com/event/fed-decision-in-october-20260617190323537) |
| Will the Fed increase interest rates by 25 bps after the October 2026 meeting? | Yes | 66.5% | 0.66/0.67 | 3.4 M | 2026-10-29 | [ver](https://polymarket.com/event/fed-decision-in-october-20260617190323537) |
| Will 1 Fed rate cut happen in 2026? | Yes | 1.9% | 0.02/0.02 | 3.4 M | 2027-01-01 | [ver](https://polymarket.com/event/how-many-fed-rate-cuts-in-2026) |
| Will the upper bound of the target federal funds rate be ≥ 4.5% at the end of 2026? | Yes | 41.4% | 0.40/0.43 | 2.4 M | 2027-01-01 | [ver](https://polymarket.com/event/what-will-the-fed-rate-be-at-the-end-of-2026) |
| Will the Fed increase interest rates by 50+ bps after the October 2026 meeting? | Yes | 1.1% | 0.01/0.01 | 2.1 M | 2026-10-29 | [ver](https://polymarket.com/event/fed-decision-in-october-20260617190323537) |

### recession

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| US recession by end of 2026? | Yes | 9.5% | 0.09/0.10 | 2.1 M | 2027-01-31 | [ver](https://polymarket.com/event/us-recession-by-end-of-2026) |
| UK Recession in 2026? | Yes | 13.5% | 0.13/0.14 | 15 mil | 2027-05-01 | [ver](https://polymarket.com/event/uk-recession-in-2026) |

### tariff

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| US x China tariff agreement by December 31? | Yes | 94.1% | 0.93/0.95 | 284 mil | 2027-01-01 | [ver](https://polymarket.com/event/us-x-china-tariff-agreement-by-december-31) |
| US-Canada diplomatic agreement to lower tariffs by September 30? | Yes | 3.0% | 0.03/0.03 | 66 mil | 2026-10-01 | [ver](https://polymarket.com/event/us-canada-diplomatic-agreement-to-lower-tariffs-by-august-31) |
| US-Canada diplomatic agreement to lower tariffs by October 31? | Yes | 17.5% | 0.17/0.18 | 50 mil | 2026-11-01 | [ver](https://polymarket.com/event/us-canada-diplomatic-agreement-to-lower-tariffs-by-august-31) |
| US-Canada diplomatic agreement to lower tariffs by December 31? | Yes | 40.5% | 0.37/0.44 | 35 mil | 2027-01-01 | [ver](https://polymarket.com/event/us-canada-diplomatic-agreement-to-lower-tariffs-by-august-31) |
| US x China tariff agreement by September 30? | Yes | 84.5% | 0.84/0.85 | 17 mil | 2026-10-01 | [ver](https://polymarket.com/event/us-x-china-tariff-agreement-by-december-31) |
| Tariff increase on Canada in effect by December 31, 2026? | Yes | 11.5% | 0.11/0.12 | 12 mil | 2027-01-25 | [ver](https://polymarket.com/event/tariff-increase-on-canada-in-effect-by-june-30) |

### Taiwan

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| China x Taiwan military clash before 2027? | Yes | 5.7% | 0.06/0.06 | 3.4 M | 2027-01-01 | [ver](https://polymarket.com/event/china-x-taiwan-military-clash-before-2027) |
| Will China invade Taiwan by June 30, 2027? | Yes | 8.5% | 0.08/0.09 | 455 mil | 2027-07-01 | [ver](https://polymarket.com/event/will-china-invade-taiwan-by-june-30-2027) |
| Will China blockade Taiwan in 2026? | Yes | 3.7% | 0.03/0.04 | 371 mil | 2027-01-01 | [ver](https://polymarket.com/event/will-china-blockade-taiwan-by-in-2026) |
| Lai Ching-te out as President of Taiwan by December 31, 2026? | Yes | 3.6% | 0.04/0.04 | 106 mil | 2027-01-01 | [ver](https://polymarket.com/event/lai-ching-te-out-as-president-of-taiwan-in-2026) |
| Will Kuomintang (KMT) win the most head of local government elections in the 2026 Taiwan local elections? | Yes | 88.5% | 0.88/0.89 | 74 mil | 2027-07-01 | [ver](https://polymarket.com/event/2026-taiwanese-local-elections-party-winner) |
| Will the Democratic Progressive Party (DPP) win the most head of local government elections in the 2026 Taiwan | Yes | 10.3% | 0.09/0.12 | 46 mil | 2027-07-01 | [ver](https://polymarket.com/event/2026-taiwanese-local-elections-party-winner) |

### China

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| Will China invade Taiwan by end of 2026? | Yes | 3.7% | 0.04/0.04 | 42.8 M | 2027-01-01 | [ver](https://polymarket.com/event/will-china-invade-taiwan-before-2027) |
| China x Taiwan military clash before 2027? | Yes | 5.7% | 0.06/0.06 | 3.4 M | 2027-01-01 | [ver](https://polymarket.com/event/china-x-taiwan-military-clash-before-2027) |
| Will China invade Taiwan by December 31, 2027? | Yes | 11.5% | 0.11/0.12 | 3.2 M | 2028-01-01 | [ver](https://polymarket.com/event/will-china-invade-taiwan-by-december-31-2027) |
| Will China invade Taiwan by September 30, 2026? | Yes | 0.1% | 0.00/0.00 | 2.3 M | 2026-10-01 | [ver](https://polymarket.com/event/will-china-invade-taiwan-by-september-30-2026) |
| China x Japan military clash before 2027? | Yes | 5.5% | 0.05/0.06 | 1.4 M | 2027-01-01 | [ver](https://polymarket.com/event/china-x-japan-military-clash-before-2027) |
| Will China unban Bitcoin by 2027? | Yes | 3.4% | 0.03/0.04 | 1.1 M | 2027-01-01 | [ver](https://polymarket.com/event/will-china-unban-bitcoin-by-2027) |

### Iran

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| Will the U.S. invade Iran before 2027? | Yes | 13.5% | 0.13/0.14 | 68.8 M | 2027-01-01 | [ver](https://polymarket.com/event/will-the-us-invade-iran-before-2027) |
| Will Mojtaba Khamenei be head of state in Iran end of 2026? | Yes | 84.7% | 0.84/0.85 | 6.6 M | 2026-12-31 | [ver](https://polymarket.com/event/iran-leader-end-of-2026) |
| Iran leadership change by December 31? | Yes | 14.5% | 0.14/0.15 | 4.7 M | 2027-01-01 | [ver](https://polymarket.com/event/iran-leadership-change-by) |
| US-Iran Final Nuclear Deal by December 31, 2026? | Yes | 12.5% | 0.12/0.13 | 3.0 M | 2026-06-15 | [ver](https://polymarket.com/event/us-iran-final-nuclear-deal-by-20260621201254412) |
| Israel x Iran ceasefire continues through September 30? | Yes | 95.7% | 0.96/0.96 | 2.8 M | 2026-09-30 | [ver](https://polymarket.com/event/israel-x-iran-ceasefire-continues-throughptptpt-20260716224448963) |
| Will Reza Pahlavi enter Iran by December 31? | Yes | 3.9% | 0.04/0.04 | 2.5 M | 2027-01-01 | [ver](https://polymarket.com/event/will-reza-pahlavi-enter-iran-by-june-30) |

### Russia

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| Putin out as President of Russia by December 31, 2026? | Yes | 4.3% | 0.04/0.04 | 22.1 M | 2027-01-01 | [ver](https://polymarket.com/event/putin-out-before-2027) |
| Russia x Ukraine ceasefire agreement by December 31, 2026? | Yes | 22.5% | 0.22/0.23 | 2.7 M | 2027-01-01 | [ver](https://polymarket.com/event/russia-x-ukraine-ceasefire-agreement-by) |
| NATO x Russia military clash by December 31, 2026? | Yes | 30.5% | 0.30/0.31 | 2.2 M | 2027-01-01 | [ver](https://polymarket.com/event/nato-x-russia-military-clash-in-2025) |
| Russia x Ukraine ceasefire agreement by October 31, 2026? | Yes | 7.0% | 0.06/0.08 | 1.7 M | 2026-11-01 | [ver](https://polymarket.com/event/russia-x-ukraine-ceasefire-agreement-by) |
| Will Russia capture all of Stepnohirsk by September 30, 2026? | Yes | 2.3% | 0.01/0.04 | 1.3 M | 2026-10-01 | [ver](https://polymarket.com/event/will-russia-capture-all-of-stepnohirsk-by) |
| NATO x Russia military clash by October 31, 2026? | Yes | 16.5% | 0.16/0.17 | 1.1 M | 2026-11-01 | [ver](https://polymarket.com/event/nato-x-russia-military-clash-in-2025) |

### Ukraine

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| Zelenskyy out as Ukraine president by end of 2026? | Yes | 5.5% | 0.05/0.06 | 3.3 M | 2027-01-01 | [ver](https://polymarket.com/event/zelenskyy-out-as-ukraine-president-before-2027) |
| Ukraine signs peace deal with Russia before 2027? | Yes | 9.0% | 0.08/0.10 | 2.8 M | 2027-01-01 | [ver](https://polymarket.com/event/ukraine-signs-peace-deal-with-russia-before-2027) |
| Russia x Ukraine ceasefire agreement by December 31, 2026? | Yes | 22.5% | 0.22/0.23 | 2.7 M | 2027-01-01 | [ver](https://polymarket.com/event/russia-x-ukraine-ceasefire-agreement-by) |
| Russia x Ukraine ceasefire agreement by October 31, 2026? | Yes | 7.0% | 0.06/0.08 | 1.7 M | 2026-11-01 | [ver](https://polymarket.com/event/russia-x-ukraine-ceasefire-agreement-by) |
| Ukraine joins NATO before 2027? | Yes | 3.1% | 0.03/0.04 | 1.3 M | 2027-01-01 | [ver](https://polymarket.com/event/ukraine-joins-nato-before-2027) |
| Russia x Ukraine ceasefire by December 31, 2026? | Yes | 13.5% | 0.13/0.14 | 961 mil | 2024-11-28 | [ver](https://polymarket.com/event/russia-x-ukraine-ceasefire-by) |

### Mexico

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| Will the National Regeneration Movement (Morena) win the most seats in the 2027 Mexico legislative election? | Yes | 91.1% | 0.91/0.91 | 57 mil | 2027-06-07 | [ver](https://polymarket.com/event/mexico-legislative-election-winner) |
| Will the National Action Party (PAN) win the second most seats in the 2027 Mexico legislative election? | Yes | 77.0% | 0.76/0.78 | 38 mil | 2027-06-07 | [ver](https://polymarket.com/event/mexico-legislative-election-2nd-place) |
| Claudia Sheinbaum out as President of Mexico by December 31? | Yes | 3.8% | 0.03/0.04 | 34 mil | 2026-07-01 | [ver](https://polymarket.com/event/claudia-sheinbaum-out-as-president-of-mexico-by-june-30) |
| Will Mexico’s 2026 Annual Inflation be between 3.00% and 3.49%? | Yes | 14.4% | 0.14/0.15 | 29 mil | 2027-01-09 | [ver](https://polymarket.com/event/mexico-annual-inflation-2026) |
| No change in Bank of Mexico’s interest rates after November 2026 meeting? | Yes | 70.5% | 0.69/0.72 | 19 mil | 2026-11-05 | [ver](https://polymarket.com/event/bank-of-mexico-decision-in-november) |
| Will the National Action Party (PAN) win the most seats in the 2027 Mexico legislative election? | Yes | 6.4% | 0.06/0.07 | 18 mil | 2027-06-07 | [ver](https://polymarket.com/event/mexico-legislative-election-winner) |

### oil

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| Will Crude Oil reach a new all-time high by December 31? | Yes | 10.5% | 0.10/0.11 | 1.4 M | 2027-01-01 | [ver](https://polymarket.com/event/crude-oil-all-time-high-by) |
| Will WTI Crude Oil (WTI) hit (HIGH) $110 in September? | Yes | 1.7% | 0.01/0.02 | 869 mil | 2026-10-01 | [ver](https://polymarket.com/event/what-price-will-wti-hit-in-september-2026) |
| Saudi Oil Pipeline (East-West) restarts by September 30? | Yes | 27.5% | 0.27/0.28 | 699 mil | 2026-10-01 | [ver](https://polymarket.com/event/saudi-oil-pipeline-east-west-restarts-byptptpt) |
| Will WTI Crude Oil (WTI) hit (HIGH) $115 in September? | Yes | 1.1% | 0.01/0.01 | 558 mil | 2026-10-01 | [ver](https://polymarket.com/event/what-price-will-wti-hit-in-september-2026) |
| Will WTI Crude Oil (WTI) hit (LOW) $80 in September? | Yes | 5.4% | 0.04/0.07 | 334 mil | 2026-10-01 | [ver](https://polymarket.com/event/what-price-will-wti-hit-in-september-2026) |
| Saudi Oil Pipeline (East-West) restarts by October 31? | Yes | 73.2% | 0.71/0.76 | 325 mil | 2026-11-01 | [ver](https://polymarket.com/event/saudi-oil-pipeline-east-west-restarts-byptptpt) |

### election

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| Will Andy Beshear win the 2028 US Presidential Election? | Yes | 1.0% | 0.01/0.01 | 19.2 M | 2029-01-21 | [ver](https://polymarket.com/event/presidential-election-winner-2028) |
| Will Gavin Newsom win the 2028 US Presidential Election? | Yes | 8.2% | 0.08/0.08 | 18.5 M | 2028-11-07 | [ver](https://polymarket.com/event/presidential-election-winner-2028) |
| Will JD Vance win the 2028 US Presidential Election? | Yes | 20.9% | 0.21/0.21 | 16.5 M | 2028-11-07 | [ver](https://polymarket.com/event/presidential-election-winner-2028) |
| Will Luiz Inácio Lula da Silva win the 2026 Brazilian presidential election? | Yes | 43.5% | 0.43/0.44 | 12.2 M | 2026-10-04 | [ver](https://polymarket.com/event/brazil-presidential-election) |
| Will Flávio Bolsonaro win the 2026 Brazilian presidential election? | Yes | 55.4% | 0.55/0.56 | 11.8 M | 2026-10-04 | [ver](https://polymarket.com/event/brazil-presidential-election) |
| Will Steve Hilton win the California Governor Election in 2026? | Yes | 4.5% | 0.04/0.05 | 2.9 M | 2026-11-04 | [ver](https://polymarket.com/event/california-governor-election-2026) |

## 3. Kalshi (API oficial v2)

### Fed

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| Fed decision in Oct 2026? - Fed maintains rate | Fed maintains rate | 32.5% | 0.32/0.33 | 1.1 M | 2026-10-28 | serie KXFEDDECISION / mercado KXFEDDECISION-26OCT-H0 |
| Fed decision in Oct 2026? - Hike 25bps | Hike 25bps | 67.5% | 0.67/0.68 | 913 mil | 2026-10-28 | serie KXFEDDECISION / mercado KXFEDDECISION-26OCT-H25 |
| Fed decision in Oct 2026? - Hike >25bps | Hike >25bps | 1.5% | 0.01/0.02 | 350 mil | 2026-10-28 | serie KXFEDDECISION / mercado KXFEDDECISION-26OCT-H26 |
| Fed decision in Dec 2026? - Fed maintains rate | Fed maintains rate | 23.5% | 0.23/0.24 | 133 mil | 2026-12-09 | serie KXFEDDECISION / mercado KXFEDDECISION-26DEC-H0 |
| Fed decision in Dec 2026? - Hike 25bps | Hike 25bps | 70.5% | 0.70/0.71 | 132 mil | 2026-12-09 | serie KXFEDDECISION / mercado KXFEDDECISION-26DEC-H25 |
| Fed decision in Dec 2026? - Hike >25bps | Hike >25bps | 1.5% | 0.01/0.02 | 118 mil | 2026-12-09 | serie KXFEDDECISION / mercado KXFEDDECISION-26DEC-H26 |

### recession

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| Recession this year? - Starts | Starts | 5.5% | 0.05/0.06 | 3.6 M | 2027-01-31 | serie KXRECSSNBER / mercado KXRECSSNBER-26 |
| Recession in 2027? - Yes | Yes | 25.0% | 0.24/0.26 | 486 mil | 2028-01-31 | serie KXRECSSNBER / mercado KXRECSSNBER-27 |
| When will the next US recession start? - Q4 2025 | Q4 2025 | 4.5% | 0.00/0.12 | 97 mil | 2026-12-31 | serie KXNBERRECESSQ / mercado KXNBERRECESSQ-Q4-2025 |
| When will the next US recession start? - Q1 2026 | Q1 2026 | 9.1% | 0.00/0.39 | 85 mil | 2026-12-31 | serie KXNBERRECESSQ / mercado KXNBERRECESSQ-Q1-2026 |
| When will the next US recession start? - Q3 2025 | Q3 2025 | 1.5% | 0.00/0.03 | 83 mil | 2026-12-31 | serie KXNBERRECESSQ / mercado KXNBERRECESSQ-Q3-2025 |
| Which countries will have a recession before 2027? - United Kingdom | United Kingdom | 15.2% | 0.17/0.69 | 82 mil | 2027-12-31 | serie KXWRECSS / mercado WRECSS-26-UK |

### tariff

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| Will Americans receive tariff stimulus checks? - Before 2027 | Before 2027 | 4.7% | 0.04/0.05 | 1.3 M | 2027-01-01 | serie KXTARIFFCHECKS / mercado KXTARIFFCHECKS-26-27 |

### Taiwan

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| Will the US issue a Level 4 travel advisory for Taiwan? - Before Jan 1, 2027 | Before Jan 1, 2027 | 4.0% | 0.03/0.05 | 205 mil | 2027-01-01 | serie KXTAIWANLVL4 / mercado KXTAIWANLVL4-27JAN01 |
| Will the US issue a Level 4 travel advisory for Taiwan? - Before Jan 1, 2028 | Before Jan 1, 2028 | 16.0% | 0.15/0.17 | 42 mil | 2028-01-01 | serie KXTAIWANLVL4 / mercado KXTAIWANLVL4-28JAN01 |
| Will the US issue a Level 4 travel advisory for Taiwan? - Before Jan 1, 2029 | Before Jan 1, 2029 | 29.5% | 0.27/0.32 | 23 mil | 2029-01-01 | serie KXTAIWANLVL4 / mercado KXTAIWANLVL4-29JAN01 |
| When will Xi Jinping visit Taiwan? - Before 2027 | Before 2027 | 3.0% | 0.02/0.04 | 21 mil | 2027-01-01 | serie KXXITAIWAN / mercado KXXITAIWAN-27JAN01 |
| When will Xi Jinping visit Taiwan? - Before 2029 | Before 2029 | 11.0% | 0.12/0.38 | 16 mil | 2029-01-01 | serie KXXITAIWAN / mercado KXXITAIWAN-29JAN01 |
| When will Xi Jinping visit Taiwan? - Before 2028 | Before 2028 | 8.5% | 0.06/0.11 | 11 mil | 2028-01-01 | serie KXXITAIWAN / mercado KXXITAIWAN-28JAN01 |

### China

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| China overtakes USA’s economy by 2030? - By 2030 | By 2030 | 15.0% | 0.14/0.16 | 130 mil | 2030-01-01 | serie KXCHINAUSGDP / mercado CHINAUSGDP-30 |

### Iran

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| US-Iran nuclear deal? - Before Jan 1, 2027 | Before Jan 1, 2027 | 10.5% | 0.10/0.11 | 1.7 M | 2027-01-01 | serie KXUSAIRANAGREEMENT / mercado KXUSAIRANAGREEMENT-27 |
| US-Iran nuclear deal? - Before Nov 1, 2026 | Before Nov 1, 2026 | 3.5% | 0.03/0.04 | 568 mil | 2026-11-01 | serie KXUSAIRANAGREEMENT / mercado KXUSAIRANAGREEMENT-27-26NOV |
| US-Iran nuclear deal? - Before Dec 1, 2026 | Before Dec 1, 2026 | 8.0% | 0.07/0.09 | 253 mil | 2026-12-01 | serie KXUSAIRANAGREEMENT / mercado KXUSAIRANAGREEMENT-27-26DEC |
| Traffic through the Strait of Hormuz? (9/21 - 9/27) - Above 10 | Above 10 | 97.5% | 0.97/0.98 | 34 mil | 2026-09-29 | serie KXHORMUZWEEKLY / mercado KXHORMUZWEEKLY-26SEP27-T10 |
| Traffic through the Strait of Hormuz? (9/21 - 9/27) - Above 15 | Above 15 | 96.5% | 0.96/0.97 | 30 mil | 2026-09-29 | serie KXHORMUZWEEKLY / mercado KXHORMUZWEEKLY-26SEP27-T15 |
| Traffic through the Strait of Hormuz? (9/21 - 9/27) - Above 75 | Above 75 | 1.5% | 0.01/0.02 | 26 mil | 2026-09-29 | serie KXHORMUZWEEKLY / mercado KXHORMUZWEEKLY-26SEP27-T75 |

### Russia

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| Will U.S. direct flights to Russia resume? - Before 2027 | Before 2027 | 5.2% | 0.03/0.07 | 18 mil | 2027-01-01 | serie KXFLIGHTSRUSSIA / mercado KXFLIGHTSRUSSIA-25-27 |

### Ukraine

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| Volodymyr Zelenskyy departure announced? - Before Oct 1, 2026 | Before Oct 1, 2026 | 0.7% | 0.00/0.01 | 48 mil | 2026-10-01 | serie KXZELENSKYYOUT / mercado KXZELENSKYYOUT-26OCT01 |
| When will Ukraine hold a presidential election? - Before 2027 | Before 2027 | 10.0% | 0.03/0.25 | 17 mil | 2027-01-01 | serie KXELECTUKRAINE / mercado KXELECTUKRAINE-30JAN01-27JAN01 |

### Mexico

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| Will Mexico resume oil exports to Cuba? - Before October 1, 2026 | Before October 1, 2026 | 1.5% | 0.00/0.03 | 6 mil (bajo) | 2026-10-01 | serie KXMEXCUBOIL / mercado KXMEXCUBOIL-26-OCT |
| Bank of Mexico rate decision in November - Maintain current rate | Maintain current rate | 66.5% | 0.64/0.69 | 6 mil (bajo) | 2026-11-05 | serie KXCBDECISIONMEXICO / mercado KXCBDECISIONMEXICO-26NOV05-HOLD |
| Bank of Mexico rate decision in November - Hike 50bps | Hike 50bps | 3.0% | 0.00/0.06 | 5 mil (bajo) | 2026-11-05 | serie KXCBDECISIONMEXICO / mercado KXCBDECISIONMEXICO-26NOV05-H50 |

### oil

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| Oil Price (WTI) on Election Day (November 3, 2026)? - $117 or above | $117 or above | 5.0% | 0.04/0.06 | 92 mil | 2026-11-03 | serie KXWTI / mercado KXWTI-26NOV03-T116.99 |
| Oil Price (WTI) on Election Day (November 3, 2026)? - $73 or above | $73 or above | 87.5% | 0.87/0.88 | 43 mil | 2026-11-03 | serie KXWTI / mercado KXWTI-26NOV03-T72.99 |
| Oil Price (WTI) on Election Day (November 3, 2026)? - $100 or above | $100 or above | 21.0% | 0.20/0.22 | 34 mil | 2026-11-03 | serie KXWTI / mercado KXWTI-26NOV03-T99.99 |
| WTI Oil 15 min · $92.53 target - Target Price: $92.53 | Target Price: $92.53 | 74.5% | 0.74/0.75 | 23 mil | 2026-09-25 | serie KXWTI15M / mercado KXWTI15M-26SEP250900-00 |
| Oil Price (WTI) on Sep 25, 2026? - Above $94.99 | Above $94.99 | 6.5% | 0.06/0.07 | 12 mil | 2026-09-25 | serie KXWTI / mercado KXWTI-26SEP2514-T94.99 |
| Oil Price (WTI) on Sep 25, 2026? - Above $93.49 | Above $93.49 | 31.5% | 0.31/0.32 | 12 mil | 2026-09-25 | serie KXWTI / mercado KXWTI-26SEP2514-T93.49 |

### election

| Pregunta | Resultado | Prob. implicita | Compra/Venta | Volumen | Cierre | Fuente |
|---|---|---|---|---|---|---|
| Los Angeles Mayor winner? - Nithya Raman | Nithya Raman | 57.5% | 0.57/0.58 | 17.9 M | 2027-06-02 | serie KXMAYORLA / mercado KXMAYORLA-26-NRAM |
| Los Angeles Mayor winner? - Karen Bass | Karen Bass | 42.5% | 0.42/0.43 | 16.7 M | 2027-06-02 | serie KXMAYORLA / mercado KXMAYORLA-26-KBAS |
| 2028 Democratic presidential nominee - Gavin Newsom | Gavin Newsom | 13.5% | 0.13/0.14 | 10.3 M | 2028-11-07 | serie KXPRESNOMD / mercado KXPRESNOMD-28-GN |
| 2028 Democratic presidential nominee - Alexandria Ocasio-Cortez | Alexandria Ocasio-Cortez | 15.5% | 0.15/0.16 | 9.4 M | 2028-11-07 | serie KXPRESNOMD / mercado KXPRESNOMD-28-AOC |
| 2028 Democratic presidential nominee - Jon Ossoff | Jon Ossoff | 16.5% | 0.16/0.17 | 8.1 M | 2028-11-07 | serie KXPRESNOMD / mercado KXPRESNOMD-28-JOSS |
| 2028 U.S. Presidential Election winner? - Marco Rubio | Marco Rubio | 9.7% | 0.10/0.10 | 5.3 M | 2029-11-07 | serie KXPRESPERSON / mercado KXPRESPERSON-28-MRUB |

## 4. Como leer estos precios

- Precio de 0.30 en un contrato Si/No = el mercado asigna ~30% (menos comisiones y prima de riesgo). Probabilidad mostrada = punto medio compra/venta si el diferencial es <= 0.10; si no, ultimo precio (regla documentada por Polymarket; aqui se aplica igual a Kalshi).
- Sesgo favorito-longshot: en Polymarket las compras por debajo de 10 centavos pierden ~19 centavos por dolar y las de 90 centavos o mas ganan ~0.8 (arXiv 2609.12878, 2026, 588 millones de operaciones); en Kalshi los contratos baratos ganan menos de lo que su precio implica tras comisiones. Leer los extremos con descuento.
- Diferencial compra/venta amplio o volumen bajo = probabilidad poco informativa.
- Leer el criterio de resolucion exacto (fecha, fuente, definicion) antes de compararlo con un pronostico propio.
- Diferencias grandes entre Polymarket y Kalshi para el mismo evento suelen deberse a criterios distintos, no a arbitraje gratuito.
- Registrar en bitacora/pronosticos.csv la probabilidad propia y la del mercado para medir si se agrega valor.

## 5. Fuentes primarias para revisar

| Region | Fuente | URL |
|---|---|---|
| Mexico | Banxico: anuncios de politica monetaria y calendario | https://www.banxico.org.mx/publicaciones-y-prensa/anuncios-de-las-decisiones-de-politica-monetaria/anuncios-politica-monetaria-t.html |
| Mexico | Diario Oficial de la Federacion (decretos, aranceles, regulacion) | https://www.dof.gob.mx/ |
| Mexico | SHCP (finanzas publicas, deuda, Paquete Economico) | https://www.gob.mx/shcp |
| Mexico | Secretaria de Economia (comercio, T-MEC, aranceles) | https://www.gob.mx/se |
| Mexico | INEGI (inflacion, PIB, empleo) | https://www.inegi.org.mx/ |
| EUA | Federal Reserve: comunicados FOMC y calendario | https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm |
| EUA | Casa Blanca: acciones presidenciales (ordenes ejecutivas, proclamaciones arancelarias) | https://www.whitehouse.gov/presidential-actions/ |
| EUA | Federal Register (aranceles, controles, sanciones publicadas) | https://www.federalregister.gov/ |
| EUA | USTR (Seccion 301, T-MEC, negociaciones) | https://ustr.gov/about-us/policy-offices/press-office/press-releases |
| EUA | Commerce BIS (controles de exportacion, Entity List) | https://www.bis.gov/news-updates |
| EUA | Tesoro OFAC (sanciones: acciones recientes) | https://ofac.treasury.gov/recent-actions |
| EUA | EIA (inventarios y precios de petroleo) | https://www.eia.gov/petroleum/supply/weekly/ |
| China | MOFCOM (comercio, controles de exportacion de China) | https://english.mofcom.gov.cn/ |
| China/Taiwan | Ministerio de Defensa de Taiwan (actividad militar del EPL) | https://www.mnd.gov.tw/ |
| Europa | Comision Europea: comercio y sanciones | https://policy.trade.ec.europa.eu/news_en |
| Energia | OPEP: comunicados de reuniones | https://www.opec.org/opec_web/en/press_room/28.htm |
| Conflictos | ISW (Rusia-Ucrania, Medio Oriente) | https://understandingwar.org/ |
| Conflictos | IAEA (programa nuclear de Iran) | https://www.iaea.org/newscenter/pressreleases |
| Conflictos | ACLED (eventos de conflicto con datos) | https://acleddata.com/ |
| Global | FMI (WEO, consultas por pais) | https://www.imf.org/en/News |

## 6. Estado de las fuentes

- GPR mensual: sin CSV (data_gpr_export.csv: HTTP 404 en https://www.matteoiacoviello.com/gpr_files/data_gpr_export.csv); .xls omitido (BIFF8 no legible con stdlib); se usa .dta
- GPR diario: sin CSV (data_gpr_daily_recent.csv: HTTP 404 en https://www.matteoiacoviello.com/gpr_files/data_gpr_daily_recent.csv); .xls omitido (BIFF8 no legible con stdlib); se usa .dta
