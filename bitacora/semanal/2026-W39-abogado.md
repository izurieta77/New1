# Auditoría semanal 2026-W39: abogado del diablo

- **Fecha:** 25-sep-2026, después del cierre. Solo lectura; no se ejecuta nada.
- **Tesis atacada** (`bitacora/decisiones/2026-09-25-CARTERA-inicial.md`): "en 4 meses el TWR lo decide la exposición y el control de pérdidas; beta de EUA sin apalancar (7 SPYM + 1 QQQM, títulos enteros, ~16% en liquidez MXN) es la mejor opción; ningún análisis mostró ventaja sobre beta 1".
- **Conflicto declarado:** el abogado del diablo del 25-sep votó A con confianza 70. Este dictamen parte de que ese voto también puede estar mal.

## 1. Pre-mortem (es 28-ene-2027: la cartera perdió o quedó última)

1. **Choque de tasas sin colchón de prima de riesgo.** El CPI del 14-oct sale caliente y la Fed sube en octubre y diciembre. El 10a pasa a 5.5-6%. Con P/U adelantado de 19.2, el rendimiento de utilidades es ~5.2%, igual que el 10a (5.1-5.2%), así que la prima de riesgo es ~0. El múltiplo se comprime, sobre todo en el NDX (QQQM pesa 27%, una sola línea sin divisibilidad). El S&P cae 12-15% en USD. Sin stops (P(−12%) = 15-17% según el gestor de riesgo), la cuenta toca el cortacircuitos, y la reducción del −12% no tiene nada táctico que recortar.
2. **El escenario "bueno" nos deja últimos: Ormuz → carry → peso.** Hay acuerdo EUA-Irán y el WTI baja de 96 a 75. La energía del CPI cede, la Fed pausa y el diferencial Banxico-Fed deja de estrecharse. El carry regresa y el USD/MXN vuelve de 17.71 a 16.3-16.8 (peso +5-8%). El S&P sube +6% en USD, pero con 83.4% de exposición en USD la cuenta hace ~0 a −1% en MXN. Los rivales con activos en MXN, CETES a 6%+ o beta >1 nos rebasan. Compramos el dólar justo después de un −4.3% del peso en un mes, es decir, en el peor momento de entrada para el componente cambiario.
3. **Fricción y rigidez de la estructura.** Hay títulos enteros (1 QQQM = 27%, imposible de ajustar fino) y un SIC sin operaciones el 24-sep, con huecos y días con el SIC cerrado y NYSE abierta. Hay una condición de validez que puede dejar la cuenta fuera del mercado justo antes de un rebote. Y el 16% en Smart Cash rinde 4.00%, por debajo de CETES (~6.3%). La cartera no es ni beta 1 ni CETES: sus retornos quedan en el medio en los dos escenarios.

## 2. Tasas base (cálculo propio, grado C; Yahoo ^GSPC y ^TNX diarios 1970-sep-2026 y MXN=X 2004-2026; ventanas de 85 días hábiles ≈ 4 meses, traslapadas; n independiente ≈ n/21)

| Condición al inicio | n (≈indep.) | Media 4m | Mediana 4m | P(<0) | P(<−10%) | P(DD ≥10% dentro de la ventana) |
|---|---|---|---|---|---|---|
| Incondicional | 14,114 (~673) | +3.1% | +3.5% | 33% | 7% | 16% |
| 10a sube >50 pb en 3 meses | 2,166 (~104) | +2.1% | +2.4% | 38% | 7% | 14% |
| **10a +50 pb en 3m y 10a >4%** | 1,724 (~83) | **+1.3%** | **+1.5%** | **42%** | 8% | 15% |
| 10a +50 pb en 3m y S&P a <3% de su máximo de 5 años | 562 (~27) | +1.6% | +2.0% | 39% | 5% | 13% |

- **Lectura:** en el régimen actual, la mediana del S&P a 4 meses (+1.5% en USD) queda **por debajo de CETES a 4 meses (~+2.1%)**. La prima esperada de la renta variable a este horizonte es ~0. La cola (DD ≥10% en ~15%) no empeora mucho. Lo que desaparece es la **ventaja**, no la seguridad.
- **CAPE >35:** solo hay ~3 episodios independientes (1999-2000, 2021 y 2024-26). A 4 meses no hay muestra útil: a 10 años la mediana es ~3% anual ([Fidelity Institutional](https://institutional.fidelity.com/app/proxy/content?literatureURL=%2F9921888.PDF)), y a 4 meses la valuación no predice (coincide el fundamental). Se trata como **sin tasa base**. Según el cap. 08 §2, las probabilidades propias se encogen hacia 50%.
- **Peso tras depreciarse >4% en un mes** (USD/MXN, 2004-2026, n = 575 días, pocos episodios independientes y dominados por 2008 y 2020): mediana del USD/MXN a 85 días −1.2%. **P(peso se aprecia >5%) = 29%** frente a 15% incondicional; P(>8%) = 12%. La reversión del peso tras un golpe es **el doble de probable** de lo normal.
- **Contraste con los pronósticos del comité:** P0012 (S&P > 7,743 al 28-ene) = 0.63 frente a una tasa base condicional de ~0.58 de retorno positivo. Es un sesgo leve, pero en la dirección de la tesis.

## 3. Quién está del otro lado

- **Acción (SPYM/QQQM):** el vendedor es un formador de mercado o arbitrajista de ETF en el SIC. No sabe más sobre el índice, pero cobra el diferencial y los huecos en un libro sin operaciones.
- **El lado relevante es el cambiario.** Al comprar 83% en USD a 17.71 vendemos pesos a quien entra en carry después de un −4.3%. Ese comprador cobra ~275 pb de diferencial (225 pb descontados a fin de año) y apuesta a que la Fed no sube tanto y a que Ormuz se resuelve. Además, el consenso de fin de año (17.75-17.88, [Yahoo Finanzas](https://es-us.finanzas.yahoo.com/noticias/usdmxn-bajar-tipo-cambio-d%C3%B3lar-192511907.html)) ya no espera más depreciación: el colchón cambiario que invoca el macro ("el USD amortigua") ya está en el precio.
- **Renta fija:** a 5.1-5.2%, el tenedor del Tesoro recibe lo mismo que el rendimiento de utilidades del S&P, sin riesgo de acción. El vendedor de bolsa que rota a bonos no tiene que saber más: solo tiene que cobrar lo mismo con menos riesgo.

## 4. Evidencia contraria (fuentes externas)

1. **La prima de riesgo es casi nula, la más baja desde la burbuja punto com.** Con el 10a arriba de 5% sostenido, el riesgo de corrección sube ([ECM Source, 2026](https://ecmsource.com/equity-risk-premium-near-zero-stocks-bonds-2026/); [BigGo Finance](https://finance.biggo.com/news/7R0SY54BmHHDnbgyH5qD); [InvestorPlace, may-2026](https://investorplace.com/hypergrowthinvesting/2026/05/the-treasury-yield-line-that-could-break-this-bull-market/)). Hoy el 10a está en 5.1-5.2%, arriba del umbral que esas notas marcaban como peligro.
2. **CAPE ≥40 solo tiene un precedente (1999-2000)** ([Yahoo Finance/Motley Fool](https://finance.yahoo.com/markets/stocks/articles/p-500-flashing-ominous-warning-062000835.html)). Los mayores retornos negativos posteriores a CAPE alto coinciden con crisis ([Fidelity](https://institutional.fidelity.com/app/proxy/content?literatureURL=%2F9921888.PDF)). Aplica a 10 años, no a 4 meses. Sirve para decir que la cola no es simétrica, no para medir el tiempo.
3. **El peso se apreció 5.6% entre enero y agosto de 2026 por carry** ([Yahoo Noticias/EFE](https://es-us.noticias.yahoo.com/carry-trade-empuja-peso-mexicano-232002398.html)). Kapital ve el diferencial "todavía suficiente" para sostener flujos. Es el mismo mecanismo que en 2022, el único de 10 episodios de crisis en que el USD **amplificó** la pérdida en MXN (`conocimiento/17-crisis-burbujas-libro-de-patrones.md`, líneas 196 y 212).
4. **Interna:** la cartera A tiene 83% de renta variable en USD. El benchmark del propio repositorio es 50% S&P en MXN + 50% CETES (cap. 17, línea 212). Nadie probó esa beta de ~0.5 contra A.

**Aritmética del riesgo cambiario:** 83.4% en USD × apreciación del peso de 5% / 8% = **−4.2% / −6.7%** en MXN solo por tipo de cambio. Con la mediana condicional del S&P (+1.5%), la cartera queda en ≈ **−2.9% / −5.4%**, frente a +2.1% de CETES. En el escenario de Ormuz con S&P +6%, queda en ≈ +0.8% / −1.7%. Matiz a favor de la tesis: en la cola mala (escalada), el peso tiende a depreciarse y amortigua. El riesgo cambiario es sobre todo de **arrepentimiento en el torneo**, no de ruina.

## 5. Sesgos del comité

- **Confirmación (el principal):** "ninguna alternativa tiene ventaja significativa sobre beta 1" se lee como "beta 1 es óptima". Las mismas t (−1.17 a −0.31) tampoco prueban que beta 1 le gane a CETES ni a 50/50. La ausencia de evidencia contra A no es evidencia a favor de A.
- **Anclaje:** en las 78 temporadas incondicionales (1999-2026), que no se condicionan al régimen actual (10a en máximo desde 2007, prima de riesgo ~0), y en el 3% de P(−12%) con stops, ya corregido a 15-17%, pero con P0014 registrado a 0.90.
- **Recencia:** en "el USD amortigua" (el peso cayó 4.3% en septiembre) y en "XLE funcionó en 2026" (geopolítico y cuantitativo).
- **Narrativa:** la cadena Ormuz → WTI → Fed → tasa real → NDX es elegante. Nadie la siguió hasta el peso: si el acuerdo abarata el crudo, el carry regresa y el mismo evento que sube el NDX nos quita 5-8% por tipo de cambio.
- **Exceso de confianza:** P0011 (0.72) y P0012 (0.63) por encima de la tasa base condicional (~0.58). Macro y fundamental piden SPXL con una prima esperada a 4 meses de ~0.
- **Del propio abogado del diablo (25-sep):** confianza 70 en A sin tasa base condicional y sin atacar la pata cambiaria.

## 6. Falsabilidad

- **Refutación actual:** "−12% al 28-dic" o "3 pp atrás de un rival con beta ≤ 1.2 **sin que haya un choque de mercado que lo explique**".
- **La cláusula en negritas es una salida de emergencia:** todo retraso se podrá atribuir a un "choque". Además, la fecha de refutación (28-dic) no coincide con el fin de temporada (28-ene), y no hay criterio para la pata cambiaria.
- **Tal como está escrita, la segunda condición no es refutable con un dato fechado.**

## Veredicto: **no sobrevive** tal como está redactada

- **Sobrevive:** la mitad defensiva. No apalancar tiene soporte: a mediana igual, P(−12%) sube de ~16% a ~39% con 3x.
- **No sobrevive:** "beta 1 en USD es la **mejor** opción". En el régimen actual:
  - la tasa base da una mediana a 4 meses por debajo de CETES;
  - la cartera carga una apuesta cambiaria no declarada (83% USD tras un −4.3% del peso, con P(reversión >5%) de 29%).
- **La tesis mezcla dos apuestas y solo defendió una.**

## Condiciones mínimas para sobrevivir (propuesta al comité del 2-oct; no se ejecuta nada)

1. **Reescribir la refutación con datos fechados y sin cláusula de escape.**
   - Al 28-ene-2027 (fin de temporada, no 28-dic), la tesis falla si se cumple cualquiera de estas:
     - TWR < TWR de "50% SPYM en MXN + 50% CETES" menos 2 pp;
     - la cuenta toca −12%;
     - quedamos 3 pp o más atrás de la mediana de los rivales con beta ≤ 1.2.
   - Se elimina "sin choque que lo explique".
2. **Declarar la pata cambiaria y registrar un pronóstico** (p. ej., "USD/MXN < 16.90 el 28-ene-2027", p ≈ 0.25). **Disparador de revisión (no de venta automática):** cierre del USD/MXN < 16.90 o del 10a > 5.50%. En ese caso, el comité evalúa pasar la línea de QQQM (27%, la más sensible a tasas) a CETES o liquidez en MXN.
3. **Congelar el "modo torneo" (SPXL) mientras el 10a esté ≥ 5.0%**, además de la condición previa de 6 reportes. Con una prima de riesgo de ~0, el apalancamiento multiplica una prima que no existe.
4. **Recalificar P0011 y P0012 contra la tasa base condicional (~0.58)** y anotar en el post-mortem que se emitieron sin ella.

## Voto: **abstención**

- A es la menos mala de las candidatas votadas, así que no voto en contra de la cartera.
- No voto a favor de la tesis mientras no cumpla las condiciones 1 y 2. Paso a **a favor** si el comité del 2-oct las adopta.

**Datos y guion:** scratchpad de la sesión (`br.py`), Yahoo v8 con corte al 21-sep-2026. El ^TNX de Yahoo marcaba 4.96 el 21-sep, frente a los 5.11-5.18 del brief del 25-sep. No cambia las tasas base.
