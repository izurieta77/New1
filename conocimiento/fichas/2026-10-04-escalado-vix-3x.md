# Ficha de estudio: ¿interruptor VIX < 25, escalado continuo por VIX o la banda SMA200 sola para el sleeve 3x?

> Bloque de trabajo continuo, 4-oct-2026 (19:10 CDMX). Fase 0. Responde la pregunta abierta de `bitacora/aprendizaje/2026-10-04.md` y es un insumo para que el comité del 9-oct ratifique `filtro_apalancados`. Tema "Apalancados y filtro de tendencia" (07/14, ya en Contrastado; el nivel no cambia).
> Código: `conocimiento/fichas/codigo/2026-10-04-escalado-vix-3x.py` (stdlib + `herramientas`, ~3 s). Diagnóstico de robustez en §5, ejecutado aparte con las mismas funciones.

## 1. Pregunta
Con un sleeve 3x diario sobre el mercado de EUA y la banda SMA200 de ±3% (entra si ^GSPC > SMA200 × 1.03 y sale si < × 0.97), ¿qué rinde más y con menos caída: (a) la banda sola, (b) la banda más el interruptor VIX < 25 (la regla vigente) o (c) la banda con escalado continuo w = min(1, (K/VIX)²)?

## 2. Fuentes y supuestos
| Fuente | Acceso |
|---|---|
| French `F-F_Research_Data_Factors_daily` (sha256 2f29e2254606…): Mkt-RF y RF, **con dividendos** | Íntegro hasta 2026-08-31 |
| Yahoo ^GSPC (cierre, para la SMA200) y ^VIX (señal) | Íntegros, 1990-2026 |

- 3x sintético: r₃ = 3·(Mkt−RF) + RF − (0.91% de gasto + 2 × 0.50% de diferencial de swap)/252. Fuera del 3x, el sleeve gana RF.
- La señal se toma al cierre de t y se aplica en t+1. Cada cambio de peso cuesta 0.10% por unidad movida.
- **No se modela el stop por precio de la regla real (−10.92%),** porque la regla vigente no define cuándo se reentra después de un stop. Es el límite principal (§6).

## 3. Resultados (CAGR | σ | MDD | exposición media | giro por año)
| Regla | 1990-2026 | 1990-2007 | 2008-2026 |
|---|---|---|---|
| 3x siempre | 15.1% \| 54.7% \| −98.0% | 13.4% \| −93.4% | 17.1% \| −93.8% |
| **Banda SMA200 sola** | **20.9%** \| 35.3% \| −57.0% \| 0.75 \| 1.0 | **17.7%** \| −44.2% | **24.1%** \| −57.0% |
| Banda + VIX < 25 (vigente) | 16.7% \| 31.6% \| **−63.8%** \| 0.70 \| 5.5 | 16.4% \| −42.7% | 17.0% \| −63.8% |
| Banda + escala K=18 | 16.2% \| 28.6% \| −52.1% \| 0.67 \| 5.7 | 15.1% \| −35.4% | 17.3% \| −52.1% |
| Banda + escala K=22 | 19.0% \| 32.4% \| −58.2% \| 0.73 \| 3.3 | 16.8% \| −39.1% | 21.1% \| −58.2% |
| Escala K=18 sin banda | 13.1% \| 33.1% \| −81.8% | 11.5% \| −81.8% | 14.8% \| −58.3% |
| *Referencia: mercado 1x* | *11.0%* | | |

## 4. Lectura
1. **El interruptor VIX < 25 empeora el resultado:** −4.2 pp de CAGR en toda la muestra (−7.0 pp en 2008-2026) y una MDD **mayor**, −63.8% contra −57.0%. Gira 5.5 veces al año contra 1.0: sale en los picos de miedo, que suelen ser mínimos locales, y vuelve a entrar más arriba. Solo en 1990-2007 recorta la MDD, y apenas (−42.7% contra −44.2%), a cambio de 1.3 pp de CAGR.
2. **El escalado continuo es mejor que el interruptor, pero no mejor que la banda sola.** K=18 baja la σ (28.6%) y la MDD (−52.1%) a cambio de 4.7 pp de CAGR. K=22 queda en medio (−1.9 pp de CAGR y MDD casi igual). Es la misma mecánica de Moreira-Muir y Božović: la media sube con el VIX, pero menos que la varianza, así que escalar mejora el riesgo, no el crecimiento.
3. **El escalado sin la banda no sirve:** −81.8% de MDD. La banda de tendencia hace casi todo el trabajo contra la cola; el VIX solo afina.
4. **El orden se sostiene en las dos mitades:** la banda sola gana en CAGR en 1990-2007 y en 2008-2026. El diagnóstico de §5 también lo sostiene.

## 5. Robustez (segunda comprobación)
| Regla | French, ejecución t+1 | ^GSPC sin dividendos, t+1 | French, ejecución t+2 |
|---|---|---|---|
| Banda sola | 20.9% / −57.0% | 15.4% / −53.8% | 20.5% / −59.1% |
| Banda + VIX < 25 | 16.7% / −63.8% | 11.0% / −60.3% | 15.2% / −61.5% |
| Banda + escala K=22 | 19.0% / −58.2% | 13.3% / −53.3% | 18.8% / −60.2% |

- La brecha de ~5.5 pp entre French y ^GSPC es el triple del rendimiento por dividendo (~1.8% × 3), como se espera.
- En los tres casos la MDD es del mismo episodio, **nov-2021 a mar-2023**: la banda entra y sale varias veces en 2022, y el VIX en 25-35 agrega todavía más giros.

## 6. Límites
- **Sin el stop por precio** de la regla real. Con un stop de −10.92% por posición, las MDD de todas las variantes serían menores y el costo por giros mayor. Falta definir la regla de reentrada después del stop para poder modelarla.
- Costos de swap supuestos (0.50% sobre lo prestado), constantes en el tiempo.
- La muestra empieza en 1990 por el VIX, así que no incluye 1929-1932 ni 1973-1974.
- K = 18 y K = 22 no se optimizaron; se eligieron antes de correr el script, como VIX "normal" y "algo alto". Se probaron solo dos valores para no ajustar a la muestra.

## 7. Lo que cambia para el sistema (inferencia, no regla)
**Para el comité del 9-oct:** en 36 años y en las dos mitades, quitar la condición VIX < 25 y quedarse con la banda SMA200 ±3% habría dado más crecimiento (+4.2 pp por año) sin peor MDD. Si el comité quiere un freno de volatilidad, el escalado continuo con K ≈ 22 cuesta menos (−1.9 pp) que el interruptor. La decisión es del comité, con el stop vigente en cualquier caso. Grado: B en la dirección (robusta a fuente, rezago y submuestra) y C en las magnitudes (sin stop, swap supuesto).

## 8. Contraste con la literatura (investigador vespertino, nota 2026-10-04)
- **Bongaerts, Kang y van Dijk (2020), "Conditional Volatility Targeting", *FAJ* 76(4), 54-71, doi:10.1080/0015198X.2020.1790853.** Leído íntegro (acceso abierto, repub.eur.nl/pub/130215). Grado **C**. Detalle en cap. 07 §2.4.
  - **Regla:** w = σ_obj/σ̂_{t−1} (1/σ, con volatilidad realizada mensual) **solo** si σ̂ cae en el quintil superior de su historia; apalanca hasta 2x en el quintil inferior y queda en 1x en el resto.
  - **Resultados en EUA (1982-2019, netos):** +0.16 de Sharpe (significativo al 5%) y −8.3 pp de MDD sobre 52.8%. En el promedio de 10 mercados: +0.07 de Sharpe y −6.6 pp de MDD.
- **Qué confirma:** el umbral VIX ≥ 25 está en la misma zona que su "quintil alto": 17.3% de los días de 1990-2026, con p80 = 24.2 (comprobación rápida, grado D). En esa zona es donde la volatilidad predice mejor y la relación con el rendimiento futuro es más negativa.
- **Qué no confirma:** ellos **reducen en proporción**, no salen a cero. No prueban un interruptor 1/0 ni reportan CAGR, así que su evidencia no contradice nuestro §4.1, pero tampoco lo prueba. Apoya la variante de escalado (§4.2) por encima del interruptor.
- **Por qué nuestra ganancia de MDD es menor que la suya:** ellos escalan sin filtro de tendencia. Aquí la banda SMA200 ya hace casi todo el trabajo contra la cola (§4.3), y el targeting y la tendencia son en buena parte la misma apuesta (Hood-Raughtigan 2025). Por eso K=22 sobre la banda no baja la MDD.
- No cambia la conclusión de §7 ni su grado.
