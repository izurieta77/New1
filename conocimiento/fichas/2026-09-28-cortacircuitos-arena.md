# Ficha de estudio: cortacircuitos de la cuenta arena en una temporada de 4 meses

> Laboratorio, 28-sep-2026, el día en que la arena entra en real. Fase 0: formación, no recomendación. El tema sostiene las reglas de riesgo **vigentes** (`perfiles_riesgo.arena_agresivo.cortacircuitos_drawdown`: −12 / −20 / −28 / −35% y tope de 10,000 MXN = −50% de 20,000). Estaba en "Documentado".
> Código: `conocimiento/fichas/codigo/2026-09-28-cortacircuitos-arena.py` (stdlib + `herramientas.datos`; ~3 s). Salida completa en esta ficha.

## 1. Pregunta
Con la cartera real (beta 1 de EUA medida en MXN, sin apalancamiento y sin stops por línea), ¿qué probabilidad hay de que cada cortacircuitos se active en una temporada de ~85 días hábiles? ¿Qué tan bien la aproxima la fórmula cerrada del cap. 07?

## 2. Fuentes y acceso
| Fuente | Acceso |
|---|---|
| Yahoo `^SP500TR` diario (rango 30y: 1996-09-30 a 2026-09-28; 7,546 días) | Descarga completa (chart v8). `range=max` degrada a barras trimestrales, así que no se usa |
| FRED `DEXMXUS` (mediodía NY), desde 1993-11 | Descarga completa |
| Cap. 07 §2.7 (drawdown, E[MDD] ≈ 1.25σ√T, Grossman-Zhou) | Lectura de la sección |
| Fórmula de primer paso del browniano con deriva (Harrison, *Brownian Motion and Stochastic Flow Systems*) | **No leída**; se re-deriva abajo |

## 3. Supuestos
1. La cartera es 100% S&P 500 TR convertido a MXN. La real tiene ~83% invertido, así que estas probabilidades son una **cota superior** para la cuenta.
2. Sin costos, sin impuestos y sin cambios de exposición durante la temporada.
3. Temporadas móviles que empiezan cada 5 días hábiles: 1,493 ventanas **traslapadas**, que equivalen a unas 88 temporadas independientes.

## 4. Derivación (fórmula cerrada)
Con X_t = ln W_t, browniano con deriva μ y volatilidad σ, la probabilidad de que el mínimo en [0, T] toque −b (b = −ln(1 − a)) es:
P = Φ((−b − μT)/(σ√T)) + exp(−2μb/σ²) · Φ((−b + μT)/(σ√T)).
Esto mide la caída **desde el inicio**. Los cortacircuitos miden la caída **desde el pico**, que es ≥, así que la fórmula subestima.

## 5. Resultados (salida del script)
| Nivel | MXN: fórmula (desde el inicio) | MXN: histórico desde el inicio | **MXN: histórico desde el pico** | USD: histórico desde el pico |
|---|---|---|---|---|
| −12% (reducir táctico 50%) | 0.152 | 0.119 | **0.165** | 0.216 |
| −20% (sin apalancados) | 0.019 | 0.019 | **0.026** | 0.058 |
| −28% (pausa) | 0.001 | 0.000 | **0.000** | 0.026 |
| −35% (todo a liquidez) | 0.000 | 0.000 | **0.000** | 0.007 |
| −50% (tope 10,000 MXN) | 0.000 | 0.000 | **0.000** | 0.000 |

Caída máxima de temporada en MXN: mediana 6.2%, p90 15.3%, **peor 26.7%**. En USD: 7.0%, 17.6% y 41.9%. Volatilidad anual casi igual (MXN 19.0%, USD 19.2%) con μ = 12.6% contra 9.9%.

## 6. Lectura
- **El peso recorta la cola, no la volatilidad.** Con la misma σ, en pesos ninguna temporada desde 1996 tocó −28% (en USD, 2.6%), y el peor caso bajó de −41.9% a −26.7%. Es la correlación negativa acciones-peso de R08/AC-05 vista en la ventana relevante para la arena.
- **Para la cartera A (~83% invertido)**, P(tocar −12% desde el pico) ≈ 12-16%, dentro del rango de 6-15% que corrigió la verificación del 25-sep. Los niveles −28% y −35% son prácticamente inalcanzables con beta 1 en MXN. **Solo muerden con apalancamiento**, que es donde el comité del 2-oct (modo C) debe recalcular: un 3x sobre la misma serie multiplica la cola.
- **La fórmula normal sirve para −12% pero no para las colas en USD:** 0.1% contra 2.6% histórico en −28%, por colas gruesas y saltos (2008, 2020).

## 7. Límites
- Ventanas traslapadas: los errores estándar son mayores de lo que sugiere n = 1,493. Solo cuatro o cinco episodios (2002, 2008, 2020, 2022) generan casi todas las caídas grandes.
- DEXMXUS al mediodía de NY no es un precio ejecutable. Hay spread cambiario de GBM y comisiones.
- La muestra empieza en 1996, así que excluye la devaluación de 1994-95 (que favoreció al tenedor de activos en USD). El amortiguador falla cuando el mercado de EUA cae **sin** aversión global al riesgo: el peso no se deprecia (R08 §14 punto 4: en 2000-2002 el USD/MXN solo subió 3.7%). Ver el contraejemplo.

## 8. Contraejemplo
2000-06 a 2002-09: mercado bajista de EUA con peso estable. La caída sin cubrir en MXN fue de −39.9%, contra −42.0% en USD (R08). En un episodio así, una temporada de 4 meses sí puede acercarse a −20% en pesos, y el amortiguador desaparece.

## 9. Segunda comprobación
- E[MDD] sin deriva / (σ√T) por simulación: 1.214, contra √(π/2) = 1.253. La simulación discreta sesga hacia abajo, igual que la cifra de 1.21 del cap. 07.
- La probabilidad histórica desde el inicio (0.119) cae debajo de la fórmula (0.152), como debe pasar si la deriva histórica fue alta y las colas en MXN delgadas.
- La cifra de −12% concuerda con la re-ejecución independiente del verificador (16.4% sin stops, 2000-2026). Límite: no hubo un agente independiente en esta corrida.

## 10. Estado nuevo
**Documentado → Comprendido con comprobación.** Siguiente prueba (Contrastado): repetir con 1.5x y 3x sintéticos (con la convención de R06) y con el filtro SMA200, para el comité del 2-oct, y medir el costo de cada cortacircuitos (rendimiento perdido por activarse en falso).
