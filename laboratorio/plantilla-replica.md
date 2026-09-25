# Réplica <ID>: <nombre corto del hallazgo>

> Copia este archivo a `laboratorio/replicas/<ID>.md`. Llena las secciones 1 a 9 **antes** de la primera corrida y no las edites después: los cambios van a "Desviaciones del pre-registro". El ID usa letras, números, `-`, `_` o `.` (ejemplo: `R001-tendencia-10m`). El registro de variantes se escribe solo en `replicas/<ID>-variantes.csv`.

| Campo | Valor |
|---|---|
| ID | |
| Artículo o hallazgo | Autores, año, título, revista o working paper, versión, URL |
| Fecha de publicación (primera versión pública) | |
| Pre-registro escrito el | AAAA-MM-DD, antes de cualquier corrida |
| Responsable | |
| Estado | Pendiente / Replicado / Replicado con diferencias / No replicado |

---

## PRE-REGISTRO (secciones 1 a 9; no se editan después de la primera corrida)

### 1. Hipótesis previa y mecanismo

- **Hipótesis.** Una frase con signo y magnitud esperados; por ejemplo, "la regla X reduce el drawdown máximo frente a comprar y mantener sin reducir el Sharpe".
- **Mecanismo económico.** Por qué existiría el efecto: riesgo, comportamiento, fricción o restricción institucional. Por qué no se arbitra.
- **Resultado declarado en el artículo.** Tabla y página, métrica, periodo y cifra exacta, sin redondear.

### 2. Criterio de refutación

- Métrica principal: p. ej. Sharpe del exceso fuera de muestra, neto de costos.
- Tolerancia para "Replicado": p. ej. el mismo signo y la magnitud dentro de ±X de la cifra del artículo en su periodo.
- **Resultado que refuta la hipótesis.** Escríbelo concreto; por ejemplo, "Sharpe fuera de muestra ≤ el de comprar y mantener", o "DSR < 0.95 con N variantes".

### 3. Datos y licencia

| Serie | Fuente y archivo | Versión / huella | Frecuencia | Condiciones de uso |
|---|---|---|---|---|
| | p. ej. French `F-F_Research_Data_Factors` | `version_crsp`, `sha256` | mensual | copiar las de la fuente o marcar "pendiente de verificar" |

### 4. Universo

Qué activos entran y cuáles no, y por qué. Revisa el sesgo de supervivencia: ¿el universo se armó con información de hoy? Considera también los cambios de metodología del índice o del proveedor.

### 5. Fecha de disponibilidad

Para cada serie, indica cuándo se conocía cada dato: rezago de publicación, vintage de ALFRED y hora del cierre. Indica también cómo se garantiza que la señal en *t* solo usa lo disponible al cierre de *t-1*.

### 6. Periodo

- Periodo del artículo:
- Periodo propio total:
- Cortes: desarrollo / validación / prueba, o dentro / fuera de muestra (fecha de publicación):

### 7. Limpieza

Reglas de limpieza fijadas **antes** de ver resultados: faltantes (-99.99 en French y `fechas_sin_precio` en Yahoo), periodos incompletos, *splits*, cambios de fuente (T-bill de Ibbotson a ICE BofA desde 202406) y valores extremos. Ninguna observación se elimina después de ver resultados.

### 8. Regla y variantes planeadas

- Regla exacta (pseudocódigo):
- Parámetros del artículo:
- Variantes planeadas (lista cerrada; todo lo demás es desviación):
- Exposición mínima y máxima, efectivo usado y moneda:

### 9. Costos y comparación simple

- Costos: comisión 0.29% por lado (GBM, hecho) + spread 0.05% por lado (supuesto) y escenario "medio" de 0.15%. Agrega los extras que apliquen: FX, préstamo o margen.
- Reglas sencillas con idénticas condiciones: comprar y mantener, 100% efectivo y ______.

---

## RESULTADOS (se llenan después de correr)

### Desviaciones del pre-registro

| Fecha | Qué cambió | Por qué | ¿Invalida el tramo de prueba? |
|---|---|---|---|

### 10. Variantes probadas

- Archivo: `replicas/<ID>-variantes.csv`
- Número de variantes con `es_prueba=1`:
- Pruebas fuera del registro (a mano, en otra sesión o en otro script): ___. Ese total se pasa como `n_pruebas`.
- Salida de `sharpe_deflactado_de_registro`: DSR, N, V, SR0 y la variante elegida.

### 11. Resultados

Pega las tablas generadas por el código (`comparar(...)`, `r.resumen()`), sin redondear a mano:

- Periodo del artículo contra la cifra del artículo.
- Dentro de muestra y fuera de muestra (o desarrollo, validación y prueba).
- Contra las reglas sencillas.

### 12. Sensibilidad

Costos (escenarios de spread), parámetros vecinos, subperiodos y regímenes, otra moneda (MXN) y otros mercados o activos. Registra las corridas de sensibilidad con `es_prueba=False` y una nota.

### 13. Diferencia frente al artículo

| Aspecto | Artículo | Réplica | ¿Explica la diferencia? |
|---|---|---|---|
| Datos / versión | | | |
| Periodo | | | |
| Costos | | | |
| Regla | | | |

### 14. Conclusiones permitidas

Solo lo que los resultados sostienen, con su alcance: periodo, mercado, costos y moneda.

### 15. Conclusiones que NO se sostienen

Lo que sería tentador afirmar y no se puede. Por ejemplo: "funciona en MXN", "funcionará en el futuro", "es mejor que la regla sencilla" (si no lo es fuera de muestra) o "tiene ventaja con dinero real".

### 16. Estado y reproducción

- Estado: Replicado / Replicado con diferencias / No replicado / Pendiente (qué falta).
- Comando que reproduce todo: `python3 laboratorio/replicas/<ID>.py`
- Huella de datos (`huella_datos` del CSV) y `sha256` de los archivos French:
- Fecha de la corrida final:
