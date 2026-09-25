# Banco de examen G5 · Mercado, on-chain, stablecoins e institucional

> Creado el 25-sep-2026 por `analista-cripto` · 8 preguntas difíciles, a libro cerrado salvo que se indique otra cosa · Cada respuesta de referencia trae su fuente.
>
> **Material:** capítulo [05](../05-mercado-on-chain-stablecoins-e-institucional.md) y fichas [05](../recursos/05-the-week-on-chain.md), [26](../recursos/26-state-of-crypto-2025.md), [30](../recursos/30-understanding-stablecoins.md), [34](../recursos/34-charting-crypto-q3-2026.md) y [35](../recursos/35-26-predictions-for-crypto-in-2026.md).
>
> **Calificación:**
> - 10 puntos por pregunta;
> - la respuesta vale solo si trae **número, mecanismo y fuente**;
> - un número correcto sin fuente vale la mitad.

---

**1. (Cálculo, se permite calculadora.)** Datos de Coin Metrics al 24-sep-2026:
- `CapMrktCurUSD` = 1,695,229,926,223.29;
- `CapMVRVCur` = 1.577304652515512;
- `SplyCur` = 20,088,857.378;
- `PriceUSD` = 84,386.58.

`CapRealUSD` responde 403 en la API comunitaria. Calcula la capitalización realizada, el precio realizado y la NUPL. Demuestra por qué el precio realizado es igual a `PriceUSD / MVRV` y di qué **no** mide esta NUPL.

*Respuesta de referencia:*
- Capitalización realizada = 1,695,229,926,223.29 / 1.577304652515512 = **US$1,074,763,789,937** (≈ 1.07 billones).
- Precio realizado = eso / 20,088,857.378 = **US$53,500.49**.
- NUPL = 1 − 1/MVRV = **0.366**.
- Demostración: `CapMrktCurUSD = PriceUSD × SplyCur`, porque 1.6952 billones / 20,088,857 = 84,386.58. Entonces CapReal / Oferta = (Precio × Oferta / MVRV) / Oferta = Precio / MVRV.
- Esta NUPL **no** está ajustada por entidad, a diferencia de la que usa Coinbase en el recurso 34, pp. 17-18. Tampoco separa cohortes STH y LTH.
- *Fuente:* API de Coin Metrics, consultada el 25-sep-2026; guía NUPL de Glassnode ("(Market Cap − Realized Cap) / Market Cap"); cap. 05 §3.

---

**2. (Inferencia con datos traslapados.)** Con la historia completa, cuando el MVRV estuvo a ±0.10 del de hoy **y** venía subiendo contra 90 días antes, BTC subió a 120 días en el 69% de los casos:
- 227 días;
- 14 observaciones sin traslape;
- 9 episodios.

El dato incondicional es 63%. ¿Es evidencia de ventaja para la temporada? Da al menos tres razones cuantitativas.

*Respuesta de referencia:* **no.**
1. **Tamaño de muestra efectivo.** Con 14 observaciones independientes, el error estándar de una proporción cercana a 0.5 es √(0.25/14) ≈ **13.4 pp**. La diferencia de 6 pp es ruido.
2. **Traslape.** Los 227 días comparten casi toda su ventana de 120 días. Hay 9 episodios, no 227 datos.
3. **Fragilidad:**
   - con la banda sola desde 2017, la mediana a 120 días es **−3.6%** (P>0 43%);
   - con la banda ±0.05 y la historia completa, −3.4%;
   - con ±0.05 y "subiendo", +30.9%, pero con solo 11 observaciones.
   - El signo cambia con supuestos razonables.
4. **Dispersión.** p10 −35.9% y p90 +65.1%: la incertidumbre es mucho mayor que cualquier ventaja.
- **Conclusión:** grado C. No hay ventaja direccional; la cuenta se juega por supervivencia.
- *Fuente:* cap. 05 §4, con dos implementaciones independientes.

---

**3. (Umbrales que se degradan.)** La guía de Glassnode dice que un MVRV > 3.5 "generally served as a strong signal for late stage bull cycles". ¿Habría funcionado esa regla en el ciclo 2024-2025? ¿Qué muestra la historia de picos por ciclo? ¿Por qué incluir 2010-2013 contamina la regla?

*Respuesta de referencia:*
- **No habría funcionado.** Con Coin Metrics, el MVRV máximo del ciclo fue **2.78** (11-mar-2024) y el techo de precio del **6-oct-2025** (cierre de US$124,824) llegó con MVRV de **2.29**. La regla nunca se activó.
- **Picos por ciclo:** 7.74 (2011), 5.88 (2013), 4.72 (2017), 3.96 (2021) y 2.78 (2024). Cada techo llega con menos ganancia no realizada.
- **Contaminación:** en 2010-2013 el MVRV pasó de 3 muchas veces y **después siguió subiendo mucho**; la mediana a 365 días con MVRV > 3 es de +219.8%.
- Un umbral fijo calibrado en toda la historia mezcla regímenes. Lo sensato es un percentil móvil o un z-score, pero **sin probar todavía**.
- **El otro extremo:** MVRV < 1 tuvo 7 episodios, con mediana a 365 días de +122.7%. Es grado C por el tamaño de muestra.
- *Fuente:* guía MVRV de Glassnode; cálculo propio con Coin Metrics; cap. 05 §2 y §4.4.

---

**4. (Niveles de costo base y replicación.)**
- (a) Hoy la SMA200 de BTC es US$70,848 (Coin Metrics) y el costo base STH es ≈ US$71.3-71.6 mil. Si el precio cae a 70 mil, ¿tienes dos señales independientes de deterioro?
- (b) Glassnode ubica el "mean MVRV price" en US$96.7 mil. Reprodúcelo con datos gratuitos y explica por qué no es un número exacto.
- (c) ¿Dónde está el punto de equilibrio del complejo de ETF y qué implica para la oferta?

*Respuesta de referencia:*
- **(a) No.** Son casi la misma línea. El costo base de quienes compraron en los últimos ≈ 5 meses (155 días) y la media de 200 días del precio miden algo muy parecido. Cuenta como **una** señal: nuestro filtro SMA200 ya incluye el costo base STH.
- **(b)** Mean MVRV price = precio realizado × MVRV promedio de largo plazo.
  - Con Coin Metrics, MVRV promedio desde 2011 = 1.812 y precio realizado del 21-sep ≈ 53,367: **96,726**.
  - Desde 2014 da 91.9 mil y desde 2010, 104.7 mil. El nivel depende de la ventana.
- **(c)** ≈ **US$86 mil.**
  - El complejo de ETF cerró debajo de ese nivel 228 sesiones seguidas; su pérdida latente llegó a ≈ US$18 mil M el 5-feb-2026 y era ≈ 3.9 mil M el 7-sep (Glassnode semana 36).
  - Junto con el bloque de LTH en 83-86 mil, es una zona donde puede aparecer oferta de quienes vendan en su punto de equilibrio.
- *Fuente:* Glassnode semanas 36-38; BGeometrics; Coin Metrics; ficha 05.

---

**5. (Stablecoins: paridad y decisión de cartera.)** Explica por qué un minorista con USDT puede tener que vender debajo de US$1 aunque Tether sea solvente. Da **tres mecanismos distintos** de pérdida de paridad o de liquidez, cada uno con un ejemplo y su dato. Justifica la decisión del comité de tener la reserva en MXN.

*Respuesta de referencia:*
- **Por qué:** el canje directo pide registro, comisión y un **mínimo de US$100,000** en USDT (FMI, p. 9, nota 12). El minorista depende del mercado secundario, donde la paridad la sostienen arbitrajistas con acceso al canje (Ma-Zeng-Zhang, NBER 33882). En una crisis, **gana el que sale primero** (p. 23).
- **Mecanismos:**
  1. **Banco custodio:** USDC cotizó **−12%** (≈ US$0.88) en mar-2023 porque Circle tenía ≈ US$3.3 mil M en SVB. Pasó ≈ 2 días debajo de 1 (pp. 16 y 25).
  2. **Contagio del ecosistema:** USDT perdió la paridad en may-2022 con el colapso de TerraUSD (p. 16).
  3. **Congelamiento de liquidez en DeFi:** el exploit de rsETH de KelpDAO (18-abr-2026) dejó los mercados de USDC y USDT de Aave al 100% de utilización ≈ **135 horas**. La moneda no perdió la paridad, pero el depósito no se podía retirar (CoinDesk, 20 y 21-abr-2026).
- **Base rate:** ≈ 99% de las desviaciones intradía quedaron dentro de 1% (p. 16).
- **Decisión del comité:** la reserva en MXN evita la cola de paridad y de contraparte. Además:
  - el FMI dice que Tether no tiene "full, independent audit" (p. 44);
  - en abr-2026 una stablecoin "a la par" quedó atrapada.
  - USDT se usa solo **de paso** en la ruta MXN→USDT→BTC.
- *Fuente:* FMI DP 25/09; CoinDesk; decisión del comité del 25-sep-2026.

---

**6. (Regulación comparada.)** Compara GENIUS y MiCA en cuatro puntos: (a) quién puede emitir; (b) emisores extranjeros; (c) intereses; (d) reservas y liquidez. Di qué dice el FMI de Tether. Explica por qué la cloture fallida de CLARITY el 15-sep-2026 no contradice que GENIUS esté vigente.

*Respuesta de referencia:*
- **(a)** GENIUS no deja emitir directamente a los bancos comerciales; deben usar una subsidiaria dedicada. MiCA sí deja a las instituciones de crédito (FMI, nota 70, p. 40).
- **(b)** MiCA exige una entidad y una licencia en la UE. GENIUS acepta emisores extranjeros si están sujetos a un régimen comparable y guardan en un custodio de EUA reservas suficientes para los tenedores de EUA (nota 71, pp. 43-44).
- **(c)** Ambas prohíben que el emisor pague intereses. MiCA lo prohíbe también a los CASP (p. 43). El FMI advierte que se puede remunerar de forma indirecta por medio de intermediarios (p. 9).
- **(d)** GENIUS: efectivo, depósitos, cuenta en la Fed, T-bills, fondos de mercado de dinero gubernamentales y ciertos reportos, sin rehipotecar; certificación mensual (p. 44). MiCA:
  - capital: el mayor de €350 mil, ¼ de los gastos fijos o 2% de las reservas (3% si es significativo);
  - ≥ 30% en efectivo o equivalentes (60%);
  - ≥ 20% a un día (40%);
  - 30% a una semana (60%);
  - auditoría cada 6 meses (notas 78-79).
- **Tether:** "domiciled in El Salvador and not subject to a full, independent audit or 1:1 backing… at this time" (p. 44).
- **CLARITY:** es la ley de **estructura de mercado** (jurisdicción SEC/CFTC sobre activos digitales), distinta de GENIUS (stablecoins de pago, firmada el 18-jul-2025). Que CLARITY no avance en el Senado deja vigente a GENIUS, cuyos reglamentos se siguen publicando (FinCEN/OFAC, Federal Register, 10-abr-2026).
- *Fuente:* FMI pp. 40-47; a16z lám. 47; decisión del comité (votación 234 del Senado).

---

**7. (Datos que dependen del proveedor.)** Explica con datos por qué **no** debemos usar como señal de trading: (a) los flujos netos a exchanges; (b) una cifra de "volumen ajustado" de stablecoins tomada de un reporte y comparada con la de otro; (c) el nivel de la oferta de stablecoins mezclando proveedores. ¿Qué sí es robusto entre proveedores?

*Respuesta de referencia:*
- **(a) Flujos a exchanges.** Con Coin Metrics:
  - el 13-ago-2026 el saldo en exchanges subió **46,954 BTC** con un flujo neto de solo **+3,192**, por reetiquetado de direcciones;
  - del 1-jul al 24-sep los flujos netos suman **−141,806 BTC** y aun así el saldo **subió 38,778**;
  - Glassnode (semana 32) veía entradas netas la mayoría de los días de 2026;
  - Glassnode reconoce que sus saldos son "lower bounds" y "may undergo retrospective revisions".
- **(b) Volumen ajustado.** a16z/Allium da **US$9 billones en 12 meses** a sep-2025 (lám. 18). Artemis da **US$7.2 billones en un solo mes** (feb-2026). Son definiciones incompatibles, ≈ 10× de diferencia. El FMI estima que ≈ 80% de las transacciones son de bots (p. 14).
- **(c) Nivel de la oferta al 25-sep-2026:** DefiLlama 313.9 mil M, CoinGecko 292.7 y Glassnode ≈ 301. Las diferencias llegan a ≈ 7%.
- **Robusto:** precio realizado y MVRV. Coin Metrics, Glassnode y BGeometrics difieren en ≤ 1% (por ejemplo, 53,247.55 contra 52,850.93 el 18-sep: 0.75%).
- *Fuente:* cap. 05 §3.4 y §6; ficha 05; aviso de datos de exchanges de Glassnode.

---

**8. (Historial de un tercero.)** Califica, con criterio y dato, las predicciones #4 (inflación de Solana) y #16 (tasas de préstamo en DeFi) de Galaxy para 2026. Da la tasa de aciertos que Galaxy se atribuye en 2025. Describe con precisión el caso LUNA. ¿Por qué todo esto pone sus pronósticos de precio en grado D?

*Respuesta de referencia:*
- **#4, FALLIDA.** Galaxy dijo que ninguna reducción de inflación pasaría en 2026 **y** que SIMD-0411 se retiraría sin votarse.
  - La 0411 sí se cerró sin votarse.
  - Pero la **SIMD-0550**, el mismo cambio ("previously proposed as SIMD-0411"), se aprobó en la votación **SGP-0002** el **28-ago-2026** con **67.001%**, contra un umbral de dos tercios: 176.29 M SOL a favor y 66.19 M en contra.
- **#16, FALLIDA.** Tras el exploit de KelpDAO (18-abr-2026), los mercados de USDC y USDT de Aave quedaron al 100% de utilización. El rendimiento del depositante de USDC en Aave v3 Ethereum llegó a **12.60%** el 19 y 20-abr (DefiLlama), así que la tasa de **préstamo** pasó de 12.6%, por encima del 10% prometido.
- **2025:** **7 aciertos de 23** (30%), según Galaxy.
- **LUNA:**
  - *Assurance of Discontinuance* No. 25-011 de la Fiscalía de Nueva York (firmada por la Fiscalía el 27-mar-2025);
  - Galaxy **acordó pagar US$200 M** como devolución de ganancias, en 4 partes (40 a 15 días, 40 al año, 60 a los 2 años y 60 a los 3 años), por promover LUNA mientras la vendía entre oct-2020 y may-2022;
  - leyes aplicadas: Martin Act y art. 63(12);
  - "neither admit nor deny".
  - Decir que "pagó US$200 M en 2025" es impreciso: en 2025 solo vencían US$40 M.
- **Grado D:**
  - no asigna probabilidades, así que no se puede medir su calibración;
  - su tasa de aciertos es baja y autoevaluada;
  - declara posiciones en BTC, ETH, HYPE, SOL y Tether;
  - en 2026 sus predicciones de flujos y precio van muy lejos de la meta (ETF, préstamos, privacidad, US$250 mil).
- *Fuente:* archivo `arena/investigacion/fuentes-terceros/2026-09-25-galaxy-predicciones-2026.md`; ag.ny.gov (¶118 y ¶122); P2P.org; CoinDesk; DefiLlama.
