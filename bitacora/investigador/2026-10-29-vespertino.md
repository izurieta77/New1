# Investigador, corrida vespertina · 2026-10-29 (20:12 CDMX; escrita a las 2026-10-30 02:13 UTC)

**Barrido corto, turno de reglas de riesgo**, dirigido al evento del día: el hackeo de Binance y la pausa de retiros (alerta del 30-oct, 00:50 UTC). Rotación: 26-oct riesgo, 27-oct cripto, 28-oct fiscal, 29-oct riesgo.

## Búsquedas
1. **arXiv** (búsqueda completa, ordenada por fecha) con "exchange hack withdrawal", "crypto exchange failure customer recovery" y "centralized exchange counterparty risk": nada reciente sobre tasas base de recuperación tras un hackeo de exchange centralizado.
2. Por eso el presupuesto se usó en el **trabajo empírico clásico** sobre riesgo de exchange, que no estaba en la base.

## Paper verificado (texto completo)
- **Moore y Christin, "Beware the Middleman: Empirical Analysis of Bitcoin-Exchange Risk"**, *Financial Cryptography* 2013 (LNCS 7859). PDF de CMU, lectura íntegra de §1-§4. **Grado B:** arbitrado, pero con una muestra chica (40 exchanges, 2010-2013) y antigua.
  - De 40 exchanges, **18 cerraron**, a menudo con los saldos de los clientes perdidos.
  - **9 sufrieron una brecha de seguridad; 5 de ellos cerraron después** (Mt. Gox, que entonces sobrevivía, quebró en 2014).
  - **Reembolso:** de los 18 cerrados con evidencia, **6 dicen haber reembolsado y 5 no**; del resto no se sabe.
  - **Riesgos proporcionales:** más volumen reduce el riesgo de cierre. La brecha lo multiplica por **2.36 (p = 0.134, no significativo)**.
  - **Regresión logística:** los exchanges **más populares sufren más brechas**.

## Qué cambia
- **Nada en los parámetros.** Es un insumo para unificar la regla de contingencia (decisiones pendientes del 30-oct, comité W44).
  - **Tasa base histórica:** una brecha **no** implica cierre seguro (4 de 9 sobrevivieron en la muestra), pero sí más riesgo. Y cuando hay cierre, el reembolso es una moneda al aire.
  - **El tamaño protege contra el cierre, no contra la brecha.** Binance es el caso del exchange grande con brecha: el paper sugiere que la probabilidad de sobrevivir es alta, pero no la cuantifica para un tamaño así.
- **Lo que no dice el paper:** cuánto tardan en reabrir los retiros. Esa variable es la que define el disparador de 24 h de los parámetros. Queda como hueco para el barrido trimestral, junto con los precedentes Bitget (24-sep-2026) y Bybit (2025) de la lista de señales.
- Adenda fechada en `conocimiento/cripto/04`.
