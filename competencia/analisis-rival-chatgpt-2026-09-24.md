# Análisis del rival: programa de ChatGPT (versión 1.1, corte 24-sep-2026)

> Fuente: documento del rival que compartió el dueño el 25-sep-2026. Este archivo resume lo que el rival **declara** tener. No es una auditoría de su trabajo.

## 1. Lo que declara tener (hechos del documento)

| Rubro | Rival (ChatGPT) | Este sistema (25-sep-2026) |
|---|---|---|
| Capital futuro | ~20,000 MXN en GBM | 20,000 MXN en GBM (mismo capital) |
| Fuentes | 28 referencias: 23 consultadas directamente y 5 solo indexadas | 26 capítulos en curso, cada uno con verificación adversarial de 30 o más elementos |
| Ejercicios comprobados | 4 ejercicios elementales (expectativa, perpetuidad, pruebas múltiples, Kelly binario) | Matemática de rachas por programación dinámica y exámenes de titulación por capítulo |
| Réplicas con datos | **0**. Todas "pendientes" | 9 réplicas pre-registradas en curso, cada una re-ejecutada por un verificador independiente |
| Herramientas | Ninguna declarada | Kit en Python (métricas, riesgo, tablero FRED/Yahoo, ledger de pronósticos, portafolio, EDGAR, dossier, monitor geopolítico, motor de backtest) |
| Datos en vivo | No declara | FRED, ALFRED, Kenneth French, Yahoo, SEC EDGAR, GPR, Polymarket y Kalshi |
| Rutinas | Estudio L-V, auditoría los sábados y balance mensual | Pre-apertura diaria, semanal, mensual y trimestral (se agrega laboratorio diario; ver §3) |
| Trayectoria de inversión | Ninguna todavía | Ninguna todavía: la competencia real no ha empezado |

## 2. Ideas del rival que adoptamos (y por qué)

1. **Estados de conocimiento**: Localizado → Documentado → Comprendido con comprobación → Contrastado → Replicado, más el estado Pendiente. Separa haber leído algo de haberlo demostrado. Se adopta en `conocimiento/estado-de-dominio.csv`.
2. **Fichas atómicas** con pregunta, fuente y versión, acceso real, supuestos, derivación, ejercicio, evidencia, límites, contraejemplo, segunda comprobación y estado. Son la unidad de estudio diaria.
3. **Registro de errores**: afirmación anterior, qué la contradice, corrección, efecto en otros conceptos y fecha. Consolida las correcciones de los registros de verificación de cada capítulo.
4. **Registro de todas las variantes** en cada backtest. Ya está integrado en `herramientas/backtest.py` y alimenta el Sharpe deflactado.
5. **Jerarquía de evidencia con la columna "qué no demuestra"**. Un backtest no demuestra dinero real. Un pantallazo de X no demuestra habilidad.
6. **Filtro estricto para X y foros**: publicación original fechada, historial con pérdidas, reglas previas al resultado, capital, flujos y costos.
7. **Medición en pesos**: 1 + R_MXN = (1 + R_USD) × (FX_final / FX_inicial). Se registran fuente, hora y tipo de cambio. El FIX de Banxico es una referencia, no un precio ejecutable en GBM.
8. **Pronósticos numéricos con intervalos y escenarios**. Las probabilidades de escenarios exhaustivos suman 100%. La versión original nunca se sobrescribe y se evalúa la cobertura de los intervalos. Se agrega al ledger de pronósticos.
9. **Cadena causal obligatoria**: acontecimiento → exposición de la empresa → efecto económico → estado financiero → valoración → diferencia contra lo que descuenta el precio.
10. **Expediente de 10 puntos por empresa**. Añade al dossier el historial de promesas de la dirección contra resultados, las partes relacionadas y los vencimientos, monedas y restricciones de la deuda.
11. **Fuentes nuevas de 2026 citadas por el rival**, que se verificarán antes de usarse: SPIVA U.S. Year-End 2025, arXiv 2601.00593, 2601.13770, 2603.29086 y 2608.27734, NBER w33351 y w34861, la Guía de Servicios de GBM V1025, y el cambio de formato de Kenneth French de enero de 2025.

## 3. Dónde vamos adelante y cómo mantener la ventaja

- **Réplicas reales.** El rival no tiene ninguna. Aquí cada réplica pre-registra su hipótesis y su criterio de refutación, registra todas sus variantes y pasa por un verificador independiente.
- **Infraestructura propia de datos y herramientas.** Permite medir en lugar de opinar.
- **Profundidad y verificación adversarial** de 26 capítulos, desde licenciatura hasta la frontera de 2026.
- **Comité de agentes y examen de titulación** (en construcción).
- **Riesgo operable.** Los límites viven en un solo archivo (`config/parametros.json`) que leen las herramientas.

## 4. Dónde el rival es más fuerte (a corregir)

- **Declara con precisión el nivel de acceso a cada fuente** (consulta directa o indexada). Nuestros capítulos confirman existencia y hallazgo principal por búsqueda, pero no siempre hubo lectura íntegra. **Acción:** la bibliografía consolidada marcará el nivel de acceso de cada fuente.
- **Tiene una rutina diaria de estudio profundo.** **Acción:** agregar la rutina diaria de *laboratorio* (una ficha, un avance de réplica, actualizar el estado de dominio y el registro de errores).
