# Investigador, corrida vespertina · 2026-10-21 (20:12 CDMX; 2026-10-22 02:14 UTC del 22-oct)

**Barrido corto, turno de prima cripto.** Rotación: 18-oct cripto, 19-oct fiscal, 20-oct riesgo.

## Búsquedas
- **No usé la API de arXiv** porque da 429 desde el 15-oct. Usé los listados HTML, que respondieron (HTTP 200).
- **`arxiv.org/list/q-fin/new`** (17 entradas): ninguna es de cripto.
- **`cs.CE/new` y `econ.GN/new`:** tampoco hay nada de cripto.
- **`q-fin/recent?show=500`** (76 entradas), filtrado por bitcoin, crypto, stablecoin, ETF, on-chain, funding, basis, trend, BTC, DeFi y token. Salieron 5:
  - 2610.23283, 2610.21540 y 2610.21491 ya estaban revisados.
  - 2610.21081 (StochLOB) predice la tendencia del libro de órdenes y no toca ninguna regla.
  - **2610.22839** es nuevo.
- **NBER:** revisé los últimos 50 working papers (API de listado, w35876-w35926). Ninguno trata de cripto, BTC, stablecoins ni ETF.
- **SSRN:** no lo intenté en esta corrida.

## Paper verificado (uno)
- **Seo, Cha, Son, Lee, Sung y Lee, "Basis-Only Funding Is Not Dividend Fair: Settlement Design in Crypto Equity Perpetuals"**, arXiv:2610.22839v1 [q-fin.TR], 16-oct-2026.
  - **Tipo:** preprint, sin revisión por pares.
  - **Leído:** el HTML completo (~47 mil caracteres), §1-§8 y referencias.
  - **Pregunta:** los perpetuos sobre acciones listados en exchanges cripto pagan un funding que sale de la base contemporánea (prima del perpetuo sobre el índice). ¿Puede ese funding replicar el flujo del accionista cuando hay dividendo?
  - **Teoría (§4):** el funding cumple dos funciones. Una es controlar la base y la otra es liquidar los flujos del accionista; en las acciones las dos se separan.
    - Prop. 2 y 3: un dividendo predecible es un "átomo", y ningún funding continuo lo replica. Hace falta un crédito puntual en la fecha ex.
    - Prop. 6: con una base que revierte a la media, la regla justa puede moverse en sentido contrario a la del índice de prima.
  - **Simulación (§5):** Monte Carlo calibrado a Hyperliquid (σ de la base 6 pb/h, AR(1) 0.72, vida media 2.1 h, D = 1%). Sin crédito puntual, el largo termina D abajo de forma permanente.
  - **Evidencia (§6, Tabla 1):** solo datos nativos de los exchanges, en 5 fechas ex con pata en Binance (AAPL, MSFT, NVDA, GOOGL y META, may-jun 2026).
    - Binance registra un átomo de funding igual a −D/(Mark−D), con error menor a 5×10⁻⁶. Hyperliquid y OKX no registran ninguno.
    - En Hyperliquid, un largo que cruza la fecha ex pierde el dividendo. Con MSFT, el bloque de residuo es +17 pb sobre D/Mark de 21.7 pb. Por nombre: ORCL 36, MSFT 22 y NVDA 12 pb.
  - **Limitaciones (las reconocen los autores):**
    - Son 5 fechas ex y las afirmaciones son "cualitativas".
    - A resolución horaria, la caída de precio no se separa del ruido.
    - La inversión de signo de la Prop. 6 depende del modelo, porque la pendiente justa no se estima.
    - El "hallazgo" de Binance es casi una identidad, porque coincide con su propia regla publicada.
  - **Inconsistencia menor:** el resumen y la introducción dan un rango de 6-22 pb, pero §6 reporta 36 pb para ORCL, que no aparece en la Tabla 1.
  - **Réplicas:** ninguna. El paquete de reproducción es anónimo.
  - **Grado C:** teoría correcta en su planteamiento, simulación y una muestra mínima.
  - **Nota de cautela:** es el tercer preprint del mismo grupo en una semana, después de 2610.21540 y 2610.21491. El volumen no suma grado.

## Qué cambia
**Nada.** No escribí adenda ni hice corrección.
- **Por qué no aplica:** el sistema opera solo spot (`config/parametros.json` L257: "Solo spot: sin futuros, sin margen…"), y `fapi.binance.com` está geo-restringido (cripto/05 §10). No toca el filtro SMA200 sobre BTC, ni la prima BTCMXN, ni E1-E10, ni la volatilidad objetivo.
- **Lo que deja:** es un argumento más a favor de la regla de solo spot. En un exchange sin crédito por dividendo, el largo en un perpetuo de acciones pierde D/P en cada fecha ex. Es un costo oculto que no aparece en el funding medio.
- **Si algún día el dueño pregunta** por perpetuos de acciones o por acciones tokenizadas, este paper es la referencia.
