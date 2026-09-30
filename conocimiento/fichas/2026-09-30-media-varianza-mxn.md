# Ficha de estudio: media-varianza en MXN con ETFs (S&P, Nasdaq, oro y CETES)

> Laboratorio, 30-sep-2026. Fase 0. Tema "Portafolio media-varianza y CAPM" (cap. 02), que estaba en Documentado. El siguiente paso anotado era "frontera eficiente con ETFs SIC en MXN". Sostiene la regla 8 del cap. 02 (nunca media-varianza con medias históricas) y la cartera real (a) del 30-sep.
> Código: `conocimiento/fichas/codigo/2026-09-30-media-varianza-mxn.py` (stdlib + `herramientas`, ~3 s, semilla 20260930).

## 1. Pregunta
En pesos y con los ETFs que el sistema usa o puede usar (S&P 500, Nasdaq-100 y oro), ¿qué dice la frontera eficiente? ¿Los pesos son estables? ¿Una tangente estimada le gana fuera de muestra a 1/N o a una mezcla fija? ¿Dónde queda la cartera (a) del 30-sep (32% S&P, 55% Nasdaq y 13% efectivo)?

## 2. Fuentes y acceso
| Fuente | Acceso |
|---|---|
| Yahoo Finance chart v8, mensual con cierre ajustado: SPY, QQQ, GLD y MXN=X | Íntegro, 2004-12 a 2026-09. El mes de septiembre-2026 es parcial, al 30-sep |
| FRED `INTGSTMXM193N` (T-bills de México, proxy de CETES) | Íntegro hasta 2026-07; ago-sep usan el último dato |
| FRED `EXMXUS` (USD/MXN promedio mensual) | Íntegro; solo para la segunda comprobación |
| DeMiguel, Garlappi y Uppal (2009), RFS 22(5) | Resumen y cifras citadas en el cap. 02; no se releyó hoy |

SPY y QQQ se usan como proxies de SPYM y QQQM, que replican los mismos índices con más historia. No hay costos, impuestos ni spread cambiario del SIC.

## 3. Supuestos y derivación
- Rendimiento en MXN: (P_t·FX_t)/(P_{t−1}·FX_{t−1}) − 1, con los dos precios al cierre de mes.
- La tangente maximiza (μ_p − r_f)/σ_p sin cortos. Se resuelve por malla de 1% (5% en el bootstrap y en la ventana móvil). Con tres activos la malla es exhaustiva y no depende de un optimizador.
- La GMV es la cartera riesgosa de mínima varianza.

## 4. Resultados (salida del script; n = 261 meses, 2005-01 a 2026-09; CETES medio 6.34%)
**4.1 Momentos en MXN (media × 12)**
| | Media | σ | Sharpe |
|---|---|---|---|
| S&P (SPY) | 13.27% | 12.61% | 0.55 |
| Nasdaq (QQQ) | 17.77% | 16.71% | 0.68 |
| Oro (GLD) | 13.92% | 18.61% | 0.41 |

- Correlaciones: S&P-Nasdaq **0.89**, S&P-oro **0.05**, Nasdaq-oro **0.02**.
- En pesos, la σ del S&P es de 12.6% contra ~15% en USD. Coincide con R08 y AC-05: el peso amortigua.

**4.2 Carteras en muestra**
| Cartera | Pesos S&P/Nasdaq/oro | Media | σ | Sharpe |
|---|---|---|---|---|
| Tangente sin cortos | 0 / 66 / 34 | 16.46% | 12.81% | **0.79** |
| 1/N | 33 / 33 / 33 | 14.99% | 11.51% | 0.75 |
| GMV riesgosa | 69 / 0 / 31 | 13.47% | 10.67% | 0.67 |
| **Cartera (a)**, 32/55/0 + 13% CETES | 32 / 55 / 0 | 14.84% | 12.91% | **0.66** |
| 60/40 S&P/Nasdaq | 60 / 40 / 0 | 15.07% | 13.85% | 0.63 |

**4.3 Inestabilidad**
- Por mitades (2005-2015 y 2015-2026), la tangente sale casi igual: 0/65/35 y 0/70/30.
- El bootstrap (1,000 remuestreos) muestra la incertidumbre real:
  - Nasdaq entre **30% y 85%** (p10-p90);
  - oro entre 10% y 50%;
  - S&P con peso 0 en 77% de los remuestreos.
- Las mitades coinciden porque en los dos tramos ganó el Nasdaq. No es prueba de estabilidad.

**4.4 Fuera de muestra** (ventana móvil de 60 meses, 2010-01 a 2026-09, 201 meses, sin costos)
| Estrategia | CAGR | σ | Sharpe | MDD |
|---|---|---|---|---|
| Tangente estimada 60m | 17.28% | 15.44% | 0.73 | **−39.2%** |
| 1/N | 16.35% | 11.87% | **0.83** | −25.5% |
| 60/40 S&P/Nasdaq fijo | 18.26% | 14.01% | **0.84** | −30.5% |
| S&P solo | 16.22% | 12.87% | 0.77 | −26.1% |

La tangente estimada tiene el peor Sharpe y el peor MDD, aunque en muestra era la mejor. Es DeMiguel-Garlappi-Uppal en pequeño: el optimizador concentra el error de estimación.

## 5. Segunda comprobación y contraejemplo
- **Otra fuente de FX (FRED `EXMXUS`, promedio mensual):** las medias casi no cambian (S&P 13.38%, Nasdaq 17.74% y oro 14.05%), pero las σ suben a 14.5/18.1/18.9%. Un tipo de cambio promedio desalinea el precio de cierre de mes y destruye parte de la cobertura natural del peso. **La medición correcta es cierre contra cierre.**
- **Contraejemplo:** desde 1999-04, con Nasdaq y S&P en MXN, el Nasdaq tiene σ de **23%**, media de 15.0% y **MDD de −79.5%** en pesos (2000-2002). La muestra de 2005 en adelante excluye ese episodio. Con ella dentro, el 55% en Nasdaq de la cartera (a) se ve mucho peor. La "tangente con 66% en Nasdaq" es producto del periodo.

## 6. Lo que cambia para el sistema (inferencias, no reglas)
1. **La regla 8 del cap. 02 queda comprobada con nuestros propios activos:** fuera de muestra, la tangente estimada perdió contra 1/N y contra una mezcla fija, con 14 pp más de drawdown que 1/N.
2. **El oro es el único diversificador real de estos tres en MXN** (correlación ~0 con los dos índices). En muestra, 1/N con oro tiene mejor Sharpe (0.75) que la cartera (a) (0.66).
   - No se verificó si GLD (u otro ETF de oro) cotiza en el SIC ni su costo en GBM.
   - Es un insumo para el comité del 2-oct, no una recomendación.
3. **La cartera (a) es, en la práctica, una apuesta de concentración al Nasdaq**, forzada por los títulos enteros. Su Sharpe en muestra está debajo de 1/N, y con 1999-2002 su cola es mucho peor que la de las fichas de cortacircuitos, que parten de 1996 con el S&P.

## 7. Límites
Sin costos ni impuestos, ni el spread cambiario del SIC. SPY y QQQ son proxies de SPYM y QQQM. La media × 12 no es CAGR. La muestra de 21 años está dominada por un ciclo de tecnología.

## 8. Estado nuevo
Portafolio media-varianza y CAPM pasa de **Documentado** a **Comprendido con comprobación**.
