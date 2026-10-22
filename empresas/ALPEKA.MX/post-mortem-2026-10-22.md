# Post-mortem · Alpek (ALPEKA.MX) · 3T26 (entregado a la BMV el 21-oct-2026)

> Rutina de cierre, 22-oct-2026 (~21:45 UTC). Los pronósticos se registraron el 25-sep en `empresas/ALPEKA.MX/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado, y no se modifican. Las resoluciones están en `empresas/ALPEKA.MX/resoluciones.csv`. Sin posición: no hay decisión de cartera ni votos del comité que evaluar, solo pronósticos. No se ejecutó `herramientas/pronosticos.py resolver` ni se tocaron `bitacora/pronosticos.csv` ni `competencia/calibracion-agentes.csv`.

## 1. Resultado real (fuente primaria)
**Fuente:** reporte trimestral 3T26 (IFRS, XBRL) entregado por Alpek a la BMV: [ifrsxbrl_1596828_2026-03_1.zip](https://www.bmv.com.mx/docs-pub/ifrsxbrl/ifrsxbrl_1596828_2026-03_1.zip) (sha256 `c2d79034…`; archivo interno fechado 21-oct-2026 14:06), listado en [información financiera de ALPEK-5057](https://www.bmv.com.mx/es/emisoras/informacionfinanciera/ALPEK-5057-CGEN_CAPIT) junto con la constancia trimestral [constrim_1596829_2026-03_1.pdf](https://www.bmv.com.mx/docs-pub/constrim/constrim_1596829_2026-03_1.pdf). El bloque de comentarios de la administración del XBRL reproduce el comunicado (Tablas 1 a 6, "Principales indicadores" y guía). No hubo evento relevante de resultados en Emisnet (el último evento de ALPEK-5057 es del 18-sep) y no se localizó el PDF del comunicado en alpek.com (la ruta `/inversionistas/` da 404); por eso se usa el XBRL, que es la presentación oficial de la emisora a la BMV.

- **Ingresos 3T26 (Tabla 2, columna trimestral): Ps 37,589 M** (US$2,179 M); 2T26: 37,483; 3T25: 31,073 (+21% a/a). XBRL `Revenue` 2026-07-01 a 2026-09-30 = 37,589,084 miles. Tipo de cambio implícito: 17.25 (cálculo propio).
- Volumen: 1,172 kt (+4% a/a; 2T26: 1,175). Precio promedio en dólares: +1% t/t y +25% a/a (Tabla 1).
- **EBITDA comparable (Tabla 4): US$276 M** (Ps 4,759 M); 2T26: 336; 3T25: 137. EBITDA reportado: US$303 M (ajustes de −27 M: ganancia de inventario y partidas no recurrentes).
- Margen de referencia de PET en China: US$213/t; flete a Sudamérica: US$321/t.
- Resultado financiero neto: −890 M MXN (incluye pérdida cambiaria de 236). Impuestos: 466 M sobre 3,067 M antes de impuestos (tasa de **15.2%**, cálculo propio). Minoritario: 179 M (6.9% de la utilidad consolidada de 2,600).
- **Utilidad atribuible a la controladora: Ps 2,421.2 M.** **UPA básica y diluida (XBRL): Ps 1.16**. Acciones en circulación al 30-sep: 2,084.5 M (2,421.2 / 2,084.5 = 1.162, cálculo propio; el XBRL no da el promedio ponderado por separado).
- Deuda neta: Ps 30,625 M; deuda neta/EBITDA UDM de 1.9x (1.8x en dólares). Flujo libre operativo: Ps 97 M (capital de trabajo: ~Ps 3,900 M).
- **Guía 2026 de EBITDA comparable elevada a US$990 M** (antes US$750-800 M); volumen sin cambio (4.6 Mt).

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ingresos 3T26 (Ps M) | 34,000 (30,800-37,200) | 33,770 | 37,589 | −9.55% | −10.16% | **Fuera** del 80% (arriba del p90) |
| UPA 3T26 (Ps) | 0.60 (0.10-1.20) | 0.442 | 1.16 | −48.3% | −61.9% | Dentro, cerca del p90 |
| P(ingresos > 33,770) | 0.53 | — | Sí | — | — | Brier 0.2209 |
| P(EBITDA comparable > US$200 M) | 0.62 | — | Sí (276) | — | — | Brier 0.1444 |

Brier promedio de los binarios: **0.1827**.

## 3. Matriz y lectura
- **Ingresos: mala decisión, mal resultado.** El supuesto clave era un precio por tonelada **−6.5% t/t**; el real fue **+1%**. Con Brent de ~72 a fin de junio y ~103 a fin de septiembre (cadena C de la propia ficha), suponer precios a la baja contradecía nuestra cadena causal: los precios de PET y PTA se fijan con fórmula de insumos (paraxileno, MEG) más margen. Volumen (1,172 contra ~1,150) y tipo de cambio (17.25 contra ~17.2) se acertaron. El consenso erró igual (−10%), así que no fue un error solitario, pero el intervalo de ±9.4% no alcanzó.
- **UPA: resultado dentro del intervalo, punto muy bajo.** Descomposición (cálculo propio, aproximada):
  - EBITDA comparable de 276 contra 225 supuesto (+51) y EBITDA reportado de 303 (la ganancia de inventario que anticipó la cadena C).
  - Tasa efectiva de 15.2% contra 28% supuesta.
  - Minoritario de 6.9% contra 11% supuesto.
  - El resultado financiero fue peor que el supuesto (−890 M MXN, ~US$52 M, contra 35), pero no compensó.
  - El verificador ya había señalado que con los supuestos de la ficha la UPA salía en ~0.65 y que la D&A probablemente era menor que 68. El punto de 0.60 fue conservador a propósito; el intervalo ancho (0.10-1.20) salvó la calibración.
- **Binario de EBITDA (0.62): buena dirección, poca convicción.** Con 336 en el 2T26, un margen PET de julio de US$215/t y flete alto, el umbral de 200 exigía una caída de 40% t/t. Una probabilidad de ~0.80 era defendible con la información del 25-sep.
- **Binario de ingresos (0.53): coherente con el punto, pero el punto estaba mal.** Ver arriba.
- **Qué se sabía el 25-sep:** Brent al alza desde julio, la mecánica de inventarios (cadena C), el margen PET y el flete de julio arriba de los supuestos de la guía.
- **Qué no se podía saber:** la tasa efectiva del trimestre (15%) y la segunda alza de la guía a US$990 M.
- **Escenario (§7):** la guía 2026 (US$990 M) supera el rango del **base** (US$780-850 M) y apalancamiento de 1.9x ya está abajo del 2.0x del base. La disrupción (cadena A) sigue: margen PET de 213 y flete de 321. **Lectura (inferencia):** el año 2026 se mueve hacia el alcista; el escenario de 12 meses depende de 2027 (Ormuz), que el reporte no aclara. Se anota en la adenda sin cambiar probabilidades.

## 4. Lecciones (cada una cambia algo concreto)
1. **Coherencia entre cadena causal y supuesto de precio.** Si la ficha afirma que los insumos subieron al cierre del trimestre, el supuesto de precio de venta no puede ir a la baja sin un argumento explícito. Checklist de la §8 para petroquímicas (Alpek, Orbia): anotar la variación t/t del insumo de referencia (Brent, paraxileno) junto al supuesto de precio por tonelada.
2. **Binarios de umbral lejano:** cuando el umbral exige una caída de 40% t/t de una variable que la propia ficha ve estable o al alza, la probabilidad debe partir de ~0.80, no de 0.62 (parámetro propuesto, no aplicado).
3. **Tasa efectiva y minoritario en la UPA:** anotar la tasa de los últimos 4 trimestres (tercer caso en dos días, después de AMX y BOLSA) y el porcentaje de minoritario del trimestre previo.
4. **Fuente primaria de Alpek:** la emisora no publica el comunicado como evento relevante en Emisnet; el XBRL trimestral (`ifrsxbrl_..._2026-03`) en "información financiera" llega el mismo día y trae las tablas del comunicado. Usarlo como fuente primaria por defecto para Alpek.

No hay errores de hecho que registrar en `conocimiento/registro-de-errores.md`: los ingresos del 2T26 de la ficha (Ps 37,483 M; US$2,154 M) y el EBITDA comparable de 336 coinciden con la columna 2T26 de este reporte.
