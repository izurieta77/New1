# Ficha de estudio: Kelly fraccional y el tope `kelly.fraccion_max` = 0.25

> Laboratorio de estudio, 2026-09-25. Fase 0: formación, no recomendación. Tema elegido porque **sostiene una regla de riesgo** (`config/parametros.json` → `kelly.fraccion_max` = 0.25; 0.5 en la arena) y estaba en "Documentado".
> Código: `conocimiento/fichas/codigo/2026-09-25-kelly-fraccional.py` (stdlib, semilla 20260925, ~2 s).

## 1. Pregunta
¿Es correcta la tabla del cap. 07 §2.2 (crecimiento 2c − c² y P(tocar x) = x^(2/c − 1))? ¿Bajo qué supuestos se sostiene, y justifica el tope de 0.25?

## 2. Fuentes y nivel de acceso real
| Fuente | Versión | Acceso |
|---|---|---|
| Kelly (1956), Bell System Tech. J. 35:917-926 | original | **No leída** en esta sesión; se usa la fórmula estándar |
| Thorp (2008), Handbook of Asset & Liability Mgmt. | capítulo | **No leída**; la fórmula continua f* = (μ − r)/σ² se re-deriva abajo |
| MacLean, Thorp y Ziemba (2010), QF 10(7) | publicada | **No leída** en esta sesión (citada en el cap. 07) |
| Bermin (2026), *Kelly trading and expected utility*, Annals of Finance 22(2), doi:10.1007/s10436-026-00487-y | publicada, CC BY 4.0 | **Solo el resumen** (Crossref, consultado 2026-09-25). Springer redirige a login |
| Cap. 07 §2.2 del repositorio | 2026-09-25 | lectura íntegra de la sección |

Todo el contenido matemático de esta ficha se **deriva y comprueba aquí**. No depende de haber leído los originales.

## 3. Supuestos
1. Precio lognormal (movimiento browniano geométrico) con μ y σ constantes y **conocidos**.
2. Rebalanceo continuo a peso constante w = c·f*, sin costos ni impuestos.
3. **Riqueza medida en exceso sobre el efectivo (r = 0)** o en términos reales con tasa real nula.
4. Horizonte infinito para la probabilidad de tocar un nivel.

## 4. Derivación
- Con un peso w en el activo riesgoso: d ln W = [r + w(μ − r) − w²σ²/2] dt + wσ dB.
- Si se maximiza g(w) = r + w(μ − r) − w²σ²/2, entonces w* = f* = (μ − r)/σ² y g* − r = SR²/2.
- Con w = c·f*: g(c) − r = SR²(c − c²/2). Dividido entre SR²/2 da **2c − c²**. La volatilidad de ln W es wσ = c·(μ − r)/σ = c·SR: proporcional a c.
- Para ln W, con deriva ν > 0 y volatilidad s, la probabilidad de tocar alguna vez ln x < 0 es x^(2ν/s²) (ruina del browniano con deriva). Con r = 0: ν = SR²(c − c²/2) y s = c·SR, así que el exponente es 2(c − c²/2)/c² = **2/c − 1**.
- Si c ≥ 2, entonces ν ≤ 0 y el nivel se toca con probabilidad 1.

## 5. Ejercicio numérico (salida del script)
Supuestos del cap. 07: prima de 5% y σ = 16% → f* = 1.953, SR = 0.3125, g* = 4.88% anual en exceso.

| c | Crecimiento (fórmula) | P(−20/−35/−50%), fórmula r = 0, ∞ | Monte Carlo, 30 años mensual, 6,000 trayectorias | P(−35%) con r = 4% nominal |
|---|---|---|---|---|
| 1.00 | 100% | 0.800 / 0.650 / 0.500 | 0.746 / 0.586 / 0.429 (g = 4.73% vs 4.88%) | 0.457 |
| 0.50 | 75.0% | 0.512 / 0.275 / 0.125 | 0.456 / 0.228 / 0.091 (g = 3.67% vs 3.66%) | 0.067 |
| 0.25 | 43.8% | 0.210 / 0.049 / 0.008 | 0.171 / 0.034 / 0.004 (g = 2.15% vs 2.14%) | 0.0002 |

- **Binario** (p = 0.55, b = 1): f* = 0.10; g/g* = 74.9% con c = 0.5, 43.7% con c = 0.25 y −2.8% con c = 2. Coincide con el cap. 07.
- **Error de estimación:** si crees operar a c = 0.5 y la prima real es la mitad, la c efectiva es 1.00 y P(−35%) pasa de 0.275 a 0.650. Con el tope de 0.25, el mismo error te deja en c = 0.50.

## 6. Evidencia empírica
No hay prueba empírica propia en esta ficha: es matemática bajo supuestos (grado A condicional). Lo empírico relevante está en el cap. 07: Baker-McHale (2013), sobre encoger la apuesta con incertidumbre (B), y Busseti-Ryu-Boyd (2016), sobre Kelly con restricción de drawdown (B). Bermin (2026) da un fundamento teórico al Kelly **escalado**: la estrategia de utilidad potencia es, bajo condiciones, un escalamiento componente a componente del Kelly. No tiene datos.

## 7. Límites
- La fórmula x^(2/c − 1) **sobrestima** el riesgo frente a (a) un horizonte finito y (b) r > 0 nominal. Es conservadora solo si los parámetros son conocidos.
- Lo **subestima** con colas gruesas, saltos, volatilidad estocástica y, sobre todo, error en μ, que casi siempre sesga hacia sobreapostar.
- El cap. 07 no decía que las probabilidades suponen r = 0. Se agregó el 2026-09-25 (ver `registro-de-errores.md`).

## 8. Contraejemplo
Un salto de −30% en un mes, fuera del modelo lognormal: con Kelly completo (peso 1.95×) la riqueza queda en 0.41; con c = 0.5, en 0.71; con c = 0.25, en 0.85. Octubre de 1987 (−21.5% en un día en el S&P 500) muestra que estos saltos existen. Kelly continuo **no** protege contra ellos; el tope fraccional sí amortigua el golpe.

## 9. Segunda comprobación
Tres rutas independientes coinciden: (i) fórmula cerrada; (ii) Monte Carlo, donde g empírico ≈ g teórico en ±0.15 pp; las probabilidades de horizonte finito quedan por debajo de las de horizonte infinito, como debe ser; (iii) caso binario por esperanza exacta, que reproduce las cifras del cap. 07 (43.7%, 74.9%, −2.8%). Límite de la comprobación: la hice yo mismo, no un agente independiente.

## 10. Conclusión y estado nuevo
- La tabla del cap. 07 es **correcta bajo sus supuestos**. Faltaba explicitar que r = 0.
- El tope de 0.25 se justifica sobre todo por el **error de estimación**: si la prima real es la mitad, 0.25 se convierte en 0.5. Además, cuesta 56% del crecimiento teórico a cambio de reducir 4× la volatilidad.
- **Estado:** Documentado → **Comprendido con comprobación**. Siguiente prueba: **Contrastado**, simulando con rendimientos históricos (French 1927-2026, saltos reales) y con μ estimado en ventanas móviles, para medir la c efectiva real frente a la nominal.
