# Ideas incorporadas al sistema (25-sep-2026)

> Origen: documento de programa y protocolo compartido por el dueño. Se toman las ideas útiles; cada una se integra en el archivo indicado.

## Ideas incorporadas

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

## Pendientes de integración

- Rutina diaria de laboratorio: una ficha, un avance de réplica, actualización de `estado-de-dominio.csv` y del registro de errores.
- Nivel de acceso por fuente en la bibliografía consolidada (consulta directa o indexada; lectura íntegra o solo del hallazgo principal).
