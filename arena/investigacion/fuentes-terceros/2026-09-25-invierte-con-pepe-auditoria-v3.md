# Auditoría adversarial independiente del paquete v3: «Invierte con Pepe»

Fecha: 25-sep-2026 · Paquete auditado: `paquete_auditoria_pepe_v3.zip` (17.6 MB, 1,314 archivos, sha256 `76d31e17...`), producido fuera de esta sesión. Se trata como contenido externo a verificar, no como resultado propio — mismo protocolo que en las rondas anteriores sobre este canal.

## Método

1. **Integridad del paquete:** `sha256sum -c SHA256SUMS.txt` sobre los 1,313 archivos declarados → **0 discrepancias**.
2. **Reproducción computacional independiente:** entorno aislado (venv Python 3.13.5, pandas 3.0.6, numpy 2.5.3 — exactamente las versiones que declara `requirements.txt`), corrido de `regenerar.py` sin tocar nada → **29 de 29 archivos de resultado con hash idéntico al publicado en `esperado/`**. Esto prueba que el pipeline es determinista y reproducible, no que su lógica sea correcta.
3. **Auditoría adversarial en 6 frentes independientes** (agentes separados, cada uno sin ver el trabajo de los otros): revisión de código de la reconstrucción de membresía histórica y celda emparejada; revisión de código del cálculo de retornos; revisión matemática de las regresiones CAPM/FF5+momentum con Newey-West y bootstrap; revisión matemática de kappa de Cohen, Poisson-binomial y análisis de potencia; verificación de fidelidad de 25 citas contra sus transcripciones con reclasificación ciega independiente; verificación de precios de 10 llamadas contra una fuente de datos propia (Yahoo Finance, bajada por separado).
4. **Síntesis adversarial:** un séptimo agente, con instrucción explícita de intentar tumbar la conclusión del paquete, evaluó si alguno de los 6 hallazgos cambia el resultado.

## Hallazgos reales (no de estilo)

| # | Hallazgo | Dónde | Severidad | ¿Cambia la conclusión? |
|---|---|---|---|---|
| 1 | La reconstrucción de sector GICS usa, cuando falta un snapshot anterior, el primer snapshot mensual de Wikipedia **posterior** a la fecha (look-ahead). Confirmado ejecutando el pipeline real: 90 ocurrencias, 54 tickers. | `scripts/06_membresia.py`, función `_elegir` | Moderada | No — nunca afecta al ticker de la llamada en sí, solo a la composición de la celda de comparación (~0.16% de combinaciones fecha×miembro) |
| 2 | Igual patrón con las acciones en circulación: si faltan datos históricos, usa datos de hasta 120 días en el futuro (5 tickers spin-off: GEN, VLTO, CPAY, MRSH, VMRK). | `scripts/06_membresia.py`, función `capitalizacion` | Moderada | No — mismos 5 tickers nunca son el instrumento cubierto por una llamada; ~0.08% de combinaciones |
| 3 | Bug latente de índice negativo (`lista[-1]`) si se invocara con fecha anterior a 2021-01-07; no se dispara con los datos reales del paquete (la fecha más antigua es sep-2022). | `scripts/06_membresia.py`, función `miembros` | Menor | No — latente, no activo |
| 4 | La regla "el miembro deslistado rinde SPY el resto del periodo" está bien programada pero **nunca se ejecuta** (0 de 421,541 evaluaciones): Yahoo Finance entrega series vacías, no parciales, para deslistados. En la práctica se manejan por exclusión total + cotas explícitas, no por sustitución. | `scripts/07_retornos_emparejados.py` | Moderada (de exactitud descriptiva) | **No — refuerza la conclusión.** El propio auditor identifica que esto probablemente sesga a favor de COMPRA (las bajas del índice suelen ser adquisiciones con prima). Un sesgo pro-COMPRA no detectado que coexiste con un resultado nulo para COMPRA es evidencia de robustez, no en contra |
| 5 | Los errores estándar Newey-West no aplican corrección por grados de libertad; en la serie más chica (n=21, FF5+momentum) el t baja de 3.11 a ≈2.54 con la corrección estándar. | `scripts/08_calendario.py` | Moderada | No — esa cifra ya no se usaba para afirmar alfa (el resumen del propio paquete ya la trata como no concluyente) |
| 6 | 25/25 citas verificadas son subcadena literal exacta de su transcripción (0 fabricadas o mal atribuidas). Reclasificando desde cero sin ver la etiqueta existente: coincide con v2 en 16/25 (64%) y con la lectura ciega en 23/25 (92%, con la salvedad ya declarada en el propio paquete de que ese lector es la misma IA). Los 9 desacuerdos con v2 son de criterio (ventanas descriptivas sin verbo de acción etiquetadas COMPRA; una venta de un tercero —Jack Dorsey en PYPL— atribuida al canal; dos citas de diálogo/entrevista etiquetadas EVITAR sin sustento en el texto citado), no citas inventadas. | `salidas/llamadas_v3.csv` | Moderada (afecta a lo sumo 3-4 de 278 llamadas) | No — la prueba ya reconoce ~9% de potencia; 3-4 reclasificaciones límite no la mueven |
| 7 | Precios: 10 llamadas verificadas de forma independiente (USD, EUR, GBP, MXN), cubriendo los 4 horizontes. Diferencia 0.00 pp en USD/EUR/GBP; ±0.2-0.5 pp en MXN, atribuible a usar tipo de cambio spot de Yahoo en vez del FIX de Banxico (no un error, una fuente distinta de FX) | `salidas/retornos_v3.csv` | No es error | No |
| 8 | Maquinaria estadística de `09_clasificaciones_kappa.py` y `10_evitar_potencia.py` (kappa de Cohen, convolución Poisson-binomial, binomial exacta, potencia, ICC-ANOVA) verificada a precisión de máquina contra reimplementaciones independientes y casos de prueba sintéticos | — | No es error | No |

## Veredicto

Los 8 hallazgos, en conjunto, **sostienen** la conclusión del paquete v3: *"no hay evidencia robusta de que las llamadas de COMPRA o de EVITAR superen al azar comparable"*. Ningún hallazgo alcanza al ticker efectivamente recomendado por una llamada, ningún precio difiere en más de 1 punto porcentual, y ninguna cita resultó fabricada. El único hallazgo con una dirección de sesgo clara (manejo de deslistados) apunta a favor de COMPRA, lo que hace el resultado nulo *más* creíble, no menos.

## Qué sigue sin poder verificarse desde este lado

No tengo modalidad de audio/video — no puedo confirmar que las 1,226 transcripciones sean fieles a lo que realmente se dijo en los videos de YouTube, solo que las citas extraídas son subcadenas literales de esas transcripciones. Esa capa (transcripción → audio real) queda fuera del alcance de esta auditoría.

## Reproducibilidad

Cualquiera con el paquete puede reproducir esto exactamente: `pip install pandas==3.0.6 numpy==2.5.3 && python3 regenerar.py` (sin internet, ~4 min) debe imprimir «TODOS LOS HASHES COINCIDEN».
