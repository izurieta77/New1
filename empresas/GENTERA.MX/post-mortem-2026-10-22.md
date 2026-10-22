# Post-mortem · Gentera (GENTERA.MX) · 3T26 (reportado el 21-oct-2026)

> Rutina de cierre, 22-oct-2026 (~21:45 UTC). Los pronósticos se registraron el 25-sep en `empresas/GENTERA.MX/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado, y no se modifican. Las resoluciones están en `empresas/GENTERA.MX/resoluciones.csv`. Sin posición en Gentera: no hay decisión de cartera ni votos del comité que evaluar, solo pronósticos. No se ejecutó `herramientas/pronosticos.py resolver` ni se tocaron `bitacora/pronosticos.csv` ni `competencia/calibracion-agentes.csv` (fuera del alcance de esta tarea).

## 1. Resultado real (fuente primaria)
**Fuente:** BMV, evento relevante del 21-10-2026 a las 14:59, "GENTERA RESULTADOS 3T26": [eventemi_1596864_1.pdf](https://www.bmv.com.mx/docs-pub/eventemi/eventemi_1596864_1.pdf) (18 pp., sha256 `151d7827…`). Versión en inglés en el evento 1596866 (15:00). Listado en [eventos relevantes de GENTERA-7472](https://www.bmv.com.mx/es/emisoras/eventosrelevantes/GENTERA-7472-CGEN_CAPIT).

Estado de resultados consolidado, 3T26 (Ps M; entre paréntesis, 3T25 / 2T26):
- Ingresos por intereses: 13,247 (12,421 / 12,967). Gastos por intereses: 1,663 (2,042 / 1,810; −18.6% a/a).
- **Margen financiero: 11,584** (10,379 / 11,157).
- Estimación preventiva: **3,753** (2,849 / 3,437; +31.7% a/a).
- **Comisiones cobradas 1,797; pagadas 132; intermediación 5; otros ingresos (egresos) de la operación 356.**
- Gastos de administración y promoción: 6,369 (+4.8%). Resultado de la operación: 3,488. Impuestos: 1,146 (tasa efectiva **32.9%**, cálculo propio).
- Utilidad neta: 2,342 (+8.6%). **Controladora: 2,261 M** (+7.7%); no controladora: 81.
- **UPA de la controladora reportada: "~$1.43"**. Acciones en circulación al 30-sep: 1,579,243,876. Comprobación: 2,261 / 1,579.24 = 1.432 (cálculo propio).
- **Ingresos totales de la operación (definición del pronóstico)** = 11,584 + 1,797 − 132 + 5 + 356 = **13,610** (cálculo propio; +11.6% a/a contra 12,191 y +4.4% t/t contra 13,038, con la misma suma).
- Operación: cartera de 95,220 M (+8.5% a/a); **etapa 3 de 4.57%** (3.43% en 3T25; 4.04% en 2T26); cobertura de 206.4%; **costo de riesgo de 15.8%** (13.3%); en Banco Compartamos, etapa 3 de 5.20%. ROE controlador de 23.8%. Segundo pago del dividendo: ~Ps 1,642.9 M el **13-nov-2026** (la ficha decía "a más tardar el 27-nov").
- UPA de 9M26: ~4.42, contra la guía 2026 de 5.88-6.03 (el reporte no repite la guía en el texto extraído; no verificado si cambió).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos totales de la operación | 13,250 (12,900-13,600) | 13,210 | 13,610 | −2.65% | −2.94% | **Fuera** del 80% por 10 M (arriba del p90) |
| UPA controladora | 1.45 (1.32-1.58) | 1.46 | 1.43 | +1.40% | +2.10% | Dentro del 80% |
| P(ingresos > 13,210) | 0.53 | — | Sí | — | — | Brier 0.2209 |
| P(UPA > 1.46) | 0.45 | — | No | — | — | Brier 0.2025 |

Brier promedio de los binarios: **0.2117** (apenas mejor que 0.25). El error = (punto − real) / real, misma convención que `empresas/AMXB.MX/resoluciones.csv`.

## 3. Matriz y lectura
- **Ingresos: proceso razonable, resultado malo por poco.** El supuesto de ingresos por intereses (~13.2 mil M) acertó (13,247). Falló el **gasto por intereses**: el margen financiero salió en 11,584 contra ~11.4 mil M supuesto, porque el costo de fondeo siguió bajando (−8.1% t/t en gasto por intereses). Los otros ingresos de la operación (356 contra 276 del 2T) sumaron otros ~80 M. El intervalo (±2.6%) era estrecho para una serie cuyo cambio t/t fue de −2.5% a +6.5% en los seis trimestres previos (tabla de la §3 de la ficha; cálculo propio); el p90 quedó a 10 M del real.
- **UPA: buen resultado, en parte por compensación de errores (suerte).** El punto quedó a 2 centavos, pero los componentes no:
  - Ingresos ~360 M arriba del supuesto.
  - Provisiones de 3,753 contra 3.3-3.5 mil M supuesto: ~250-450 M arriba (el deterioro del crédito, cadena A, fue más fuerte de lo modelado).
  - Gastos de 6,369 (supuesto ~6.4 mil M) y tasa de 32.9% (supuesto ~31%).
  - Más ingreso y más provisión se cancelaron. **El acierto en UPA no valida el modelo de provisiones.**
- **Binario de ingresos (0.53): decisión tímida, resultado favorable.** Con el punto en 13,250 (arriba de 13,210) y el fondeo bajando, 0.53 era coherente pero bajo; el Brier de 0.22 refleja casi una moneda.
- **Binario de UPA (0.45): decisión defendible, resultado favorable.** El consenso venía bajando (1.53 → 1.46) y el riesgo era de provisiones; se cumplió. Brier de 0.20, mejor que la moneda pero sin convicción.
- **Qué se sabía el 25-sep:** la tendencia de fondeo más barato (cadena B, ya visible en 2T26: costo de 7.2% contra 9.1%), el deterioro del crédito individual (etapa 3 de 6.12%) y el recorte de la guía de cartera.
- **Qué no se podía saber:** la magnitud del salto de la etapa 3 a 4.57% en un trimestre y los otros ingresos no recurrentes.
- **Escenario (§7):** la etapa 3 (4.57%) ya rebasa el umbral del **bajista** ("arriba de 4.5%"); el costo de riesgo (15.8%) queda justo debajo del umbral bajista (16%) y la cartera crece +8.5% (base 6-9%). La UPA 9M (~4.42) deja el año en ruta a la parte baja de la guía. **Lectura (inferencia):** señales mixtas, con sesgo hacia el bajista en calidad de activos; la ficha no se reescribe aquí, solo se anota en la adenda.

## 4. Lecciones (cada una cambia algo concreto)
1. **Ingresos de financieras: modelar el gasto por intereses con la tendencia del costo de fondeo, no plano.** En Gentera, el margen financiero se desvió por el lado del gasto, no del ingreso. Checklist de la §8: anotar el gasto por intereses de los últimos 4 trimestres y su variación t/t junto al supuesto.
2. **Intervalos de ingresos:** si el cambio t/t de la serie oscila entre −2.5% y +6.5%, el intervalo de 80% no debe ser menor a ±3.5% alrededor del punto (parámetro propuesto, no aplicado).
3. **Cuando el punto de UPA acierta por compensación de errores, registrarlo como acierto con suerte.** Para la próxima ficha, separar en la §8 un pronóstico explícito de provisiones (o de etapa 3), que es la variable que mueve el escenario.
4. **Fecha del dividendo:** la ficha decía "a más tardar el 27-nov"; el reporte fija el 13-nov. Dato a corregir en la próxima actualización de la ficha (no es error de hecho de la ficha: el plazo máximo era correcto).

No hay errores de hecho que registrar en `conocimiento/registro-de-errores.md`: las cifras del 2T26 de la ficha (13,038 de ingresos; 2,284 de UN controladora; etapa 3 de 4.04%) coinciden con la columna 2T26 de este reporte.
