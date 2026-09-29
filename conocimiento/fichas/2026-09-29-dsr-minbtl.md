# Ficha de estudio: PSR, DSR y MinBTL, las reglas que separan habilidad de suerte

> Laboratorio, 29-sep-2026. Fase 0. El tema sostiene las reglas de validación del sistema (`validacion_estrategias`, DSR ≥ 0.95 en la tabla maestra) y la lectura del marcador de la competencia. Estaba en "Documentado".
> Código: `conocimiento/fichas/codigo/2026-09-29-dsr-minbtl.py` (stdlib + `herramientas.metricas`, ~6 s, semilla 20260929).

## 1. Pregunta
¿Las fórmulas de `herramientas/metricas.py` (PSR, E[max SR], DSR) y las cifras del cap. 07 (MinBTL: "45 pruebas con 5 años; 7 con 2 años"; DSR del paper = 0.90) resisten una comprobación independiente por simulación? ¿Qué implican para juzgar una temporada de 4 meses?

## 2. Fuentes y acceso
| Fuente | Acceso |
|---|---|
| Bailey y López de Prado (2012), *J. of Risk* 15(2): PSR | **No leída** en esta sesión; se usa la fórmula citada en el cap. 07 y se prueba por simulación |
| Bailey y López de Prado (2014), *JPM* 40(5): DSR | **No leída**; el ejemplo numérico del paper se reproduce |
| Bailey, Borwein, López de Prado y Zhu (2014), *Notices AMS*: MinBTL | **No leída**; se re-deriva MinBTL = (E[max Z_N] / SR objetivo)² |
| `herramientas/metricas.py` (líneas 202-262) | Lectura íntegra de las funciones |

## 3. Supuestos y derivación
- **PSR:** Φ[(SR − SR*)·√(n − 1) / √(1 − γ₃SR + (γ₄ − 1)/4·SR²)], con el SR por periodo. Se deriva del error estándar asintótico del SR con momentos no normales (Mertens, 2002).
- **E[max SR] entre N pruebas sin habilidad:** √V·[(1 − γ)Φ⁻¹(1 − 1/N) + γΦ⁻¹(1 − 1/(Ne))], con γ la constante de Euler. Es la aproximación de valores extremos (Gumbel) del máximo de N normales.
- **MinBTL:** con SR anual objetivo S y V = 1 por año, el backtest necesita T > (E[max Z_N]/S)² años. Si es más corto, el mejor de N intentos sin habilidad alcanza S por pura suerte.

## 4. Resultados (salida del script)
| Comprobación | Resultado |
|---|---|
| E[max] con N = 10 / 45 / 100 / 1000: fórmula contra Monte Carlo | 1.575/1.536 · 2.236/2.202 · 2.531/2.507 · 3.255/3.233. La fórmula sobrestima 1-3%: **es conservadora** (exige más). `metricas` coincide con la fórmula al tercer decimal |
| MinBTL (SR 1) | N = 7 → **1.92 años**; N = 45 → **5.00 años**; N = 100 → 6.4; N = 1000 → 10.6. **Confirma el cap. 07** |
| Falsos positivos de PSR(0) ≥ 0.95 con SR real = 0 (T = 252; 4,000 réplicas) | Normal **0.040**; t de Student con 3 gl **0.058** (nominal 0.05). La corrección por momentos funciona bien, con un ligero exceso en colas muy gruesas |
| DSR del ejemplo del paper (SR 2.5, T 1,250, N 100, V 0.5, asimetría −3, curtosis 10) | **0.8997**. Reproduce el 0.90 del cap. 07 |
| Temporada de 85 días: SR anual mínimo para PSR(0) ≥ 0.95 | **2.85** |

## 5. Lectura operable
1. **Las reglas de validación están bien calibradas** y del lado prudente. Nada en `metricas.py` requiere corrección.
2. **Una temporada de 4 meses no distingue habilidad de suerte.** Haría falta un Sharpe anualizado de ~2.85 solo para rechazar "SR = 0" al 95%, y con 3 rivales el umbral sube aún más. El marcador del torneo **no debe usarse para calificar la habilidad** de ninguna IA, la nuestra incluida. Esto coincide con la regla de `competencia/marcador.md` de "no atribuir habilidad por el saldo final". Además, pesa en contra de "subir riesgo por ir atrás" basado en 1-2 meses de datos.
3. **Límite de exploración del laboratorio:** con los ~20 años típicos de los ETF, cualquier familia de más de ~1,000 variantes produce "SR 1" por azar. Con 5 años, no más de 45.

## 6. Límites y contraejemplo
- La aproximación supone pruebas **independientes**. Con variantes correlacionadas (p. ej. SMA de 8, 10 y 12 meses), el N efectivo es menor y la fórmula penaliza de más.
- Colas extremas o autocorrelación del SR (Lo 2002) mueven el umbral. López de Prado-Lipton-Zoonekynd (2026, cap. 07 §4) dan la distribución cerrada con autocorrelación, que aquí no se usó.
- **Contraejemplo:** con t de 3 gl, la tasa de falsos positivos sube a 5.8%. Con cripto (colas más gruesas) el PSR puede exagerar la confianza.

## 7. Segunda comprobación
Hay tres rutas independientes para la pieza central, E[max]: la fórmula, `metricas.sharpe_maximo_esperado` y Monte Carlo. Además se reprodujo el ejemplo publicado (0.8997 contra 0.90). Límite: lo comprobé yo; no hubo un agente independiente.

## 8. Estado nuevo
**Documentado → Comprendido con comprobación.** Siguiente prueba (Contrastado): aplicar el DSR con N efectivo (componentes principales de las variantes) a las familias de R01-R09 y comparar contra el DSR que reportan con N nominal.
