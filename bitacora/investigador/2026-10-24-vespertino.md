# Investigador, corrida vespertina · 2026-10-24 (20:12 CDMX del sábado; 2026-10-25 02:13-02:16 UTC)

**Barrido corto, turno de prima cripto.** Rotación: 21-oct cripto, 22-oct fiscal, 23-oct riesgo.

## Búsquedas
- **No usé la API de arXiv** porque sigue dando 429. Usé los listados HTML y la búsqueda HTML, que respondieron (HTTP 200).
- **`q-fin/new`** (22 entradas, sin actualizar por ser sábado) y **`cs.CE/new`** (11): nada de cripto. La única coincidencia, 2609.31570 (rough volatility con redes), no es de BTC.
- **`cs.CR/new`** (72): solo 2610.30595 (extensión de EIP-1559) se acerca, y es diseño de comisiones de Ethereum. No toca ninguna regla.
- **`q-fin/recent?show=500`** (77): 2610.28863 (LP en DEX con liquidez concentrada, WETH/USDC) y 2610.25468 (embeddings de WSB para volatilidad de acciones). Ninguno toca el spot BTC/ETH. 2610.23283 y 2610.22839 ya estaban revisados.
- **Búsqueda HTML de arXiv por fecha** ("bitcoin", "stablecoin", "spot ETF crypto", "cryptocurrency exchange", "bitcoin volatility"). Lo nuevo es:
  - 2610.30350 (parches de Lightning), 2610.26713 (PoW de inferencia), 2610.22451 (minería), 2610.21526 (gossip) y 2610.24274 (AML): ninguno es de inversión.
  - 2610.26324 (agentes de trading en Hyperliquid): es un reporte de disciplina de reglas sin control de suerte y con muestra de 6 meses. Lo descarté.
  - 2610.22899: no es de stablecoins, aunque salga en la búsqueda.
  - **2610.24270 (tendencia de ley de potencia y volatilidad de BTC): es el único que toca un tema de la regla.**
- **NBER:** revisé los 60 working papers más recientes (API de listado, w35839-w35918). Nada sobre cripto, BTC, stablecoins, ETF ni volatilidad.
- **SSRN:** respondió 403, como el 23-oct.
- **Excluido por instrucción:** 2610.22839, 2610.21540, 2610.21491, 2610.23283 y lo de la ficha poscuántica del 24-oct.

## Paper verificado (uno)
- **Bomfim, Calvache y Quintino, "Stochastic models with power-law trends: An analysis of Bitcoin price dynamics"**, arXiv:2610.24270v1 [stat.ME], 16-oct-2026, CC BY 4.0.
  - **Tipo:** preprint, sin revisión por pares. Los autores son de estadística (UnB, Sergipe y el tribunal electoral de Ceará), no de finanzas.
  - **Leído:** el HTML completo (~45 mil caracteres con fórmulas), §1-§5. Las referencias las revisé por encima.
  - **Muestra:** cierres diarios de BTC/USD del 13-jul-2010 al 4-oct-2026 (n = 5,928), con el tiempo medido en años desde el bloque génesis (t0 = 1.52). Entrenan con 5,863 días y **validan con solo 65** (31-jul a 4-oct-2026).
  - **Método:**
    - ln P(t) = ln P0 + β ln t + σ(t) N(t), con ruido Wiener, Lévy (W+CPP, VG, α-estable) o fBm, y volatilidad de ley de potencia σ(t) = σ0 (t/t0)^(−γ).
    - Estiman con LSE, LSE filtrado y QMLE en dos pasos, y comparan contra un GBM con la misma volatilidad.
  - **Hallazgos con magnitud:**
    1. **La volatilidad decae con el tiempo:** γ̂ = 0.55 (EE 0.063, IC 95% [0.43, 0.67]), y se rechaza γ = 0. Este es el resultado sólido del paper.
    2. **La tendencia:** β̂ = 5.60 (WLSE) o 6.87 (filtrado, con 7.1% de los incrementos quitados). **El paper no reporta el IC de β.** Lo calculé con su Teorema 2.5 y sus propias cifras (σ0 = 1.963, γ = 0.55, T ≈ 17.6): EE ≈ 1.45, **IC 95% ≈ [2.75, 8.45]**. A un año, eso equivale a una deriva logarítmica de +31% con IC [+15%, +46%]. Con γ ≈ 1/2 el estimador apenas es consistente (Teorema 2.5c: lo es solo si γ ≥ 1/2), así que más historia casi no lo afina.
    3. **Fuera de muestra (Tabla 3, multipaso a 65 días):** **el GBM gana al PLT.** El MAE es 0.1666 en GBM, 0.1781 en PLT-Wiener, 0.1723 en PLT-VG y 0.1939 en PLT-fBm. A un paso todos empatan (≈0.026). La ventaja del PLT es solo a un año dentro de muestra (MAE 1.088 contra 1.280) y en el ajuste visual log-log.
    4. **Inconsistencia:** dicen que "PLT-fBm was selected for multi-step predictions", pero en su propia Tabla 3 es el peor de los no estables en MAE y RMSE. La elección parece venir de la cobertura de la Tabla 4 (6.2% fuera de la banda), pero el texto no lo dice.
    5. **Memoria larga:** Ĥ = 0.528, casi browniano. No hay evidencia de memoria larga material en el nivel diario.
    6. **Pronóstico:** desde 86,480 USD (4-oct), la mediana al 31-dic-2026 es 93,146 USD, con banda de 95% de [53,255, 161,687].
  - **Lo que verifiqué con datos propios** (espejo público `data-api.binance.vision`, BTCUSDT diario, hasta el 25-oct-2026):
    - El cierre del 4-oct es 86,530.00, contra los 86,480 que da el paper. Cuadra, con diferencia de fuente.
    - El σ(t) del modelo para hoy (t ≈ 17.75 años) es de **≈51% anual**.
    - La volatilidad realizada es de **44.0%** a 365 días, 44.0% a 730, 36.5% a 180 y 37.6% a 90.
    - El modelo sobreestima en ~7 pp la volatilidad del último año. Es lo esperable, porque es una curva suave ajustada a toda la historia, con 2011-2013 dentro.
  - **Limitaciones:**
    - Hay una sola ventana de validación, de 65 días, y sin costos ni regla de trading.
    - El "tiempo desde génesis" es un origen arbitrario, y el β depende de él.
    - El sesgo de selección de la ley de potencia es grande: el modelo se construye mirando el gráfico log-log (nota 1 del paper, que cita un blog de Medium).
    - No hay prueba contra alternativas de tendencia con quiebre.
    - Reconocen que β no es consistente con σ constante.
  - **Réplicas:** ninguna. No hay código publicado que yo haya encontrado.
  - **Grado:**
    - **C** para el decaimiento de la volatilidad: la estimación es formal y el IC es estrecho, pero es un solo trabajo y un preprint.
    - **D** para la tendencia de ley de potencia como guía de precio: no le gana al GBM fuera de muestra en su propia tabla, y el IC de β es de un factor de 3.

## Qué cambia
**Nada.** No escribí adenda, ni corrección, ni fila en `estado-de-dominio.csv`.
- **Filtro SMA200 ×0.97/×1.03:** el paper no prueba ninguna regla de trading. Que Ĥ ≈ 0.53 no dice nada sobre la tendencia de ~7 meses en la que se basa el filtro (cap. 05, adenda del 19-oct).
- **La nota de `config/parametros.json` L279** ("volatilidad de 43% anual") se sostiene: la realizada a 365 días es de 44.0%. El 51% del modelo es una extrapolación suave de toda la historia y no un pronóstico a 12 meses. No conviene usarlo para recalibrar los límites de pérdida.
- **Para la conversación con el dueño:** si llega la narrativa del "corredor de ley de potencia" (redes o pódcasts), este paper es la referencia académica más formal hasta hoy, y aun así muestra que la tendencia no supera a un GBM fuera de muestra y que su pendiente es muy incierta (β entre ~2.8 y ~8.4). La narrativa es grado D.
- **Duda:** ninguna nueva. No agregué nada a `decisiones-pendientes.md`.
