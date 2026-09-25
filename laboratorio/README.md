# Laboratorio de réplicas

> Fase 0: formación. El laboratorio no recomienda inversiones. Su propósito es llevar un hallazgo del estado **Documentado** al estado **Replicado**, con datos reales, código reproducible y todas las variantes registradas, antes de que cualquier regla se use con dinero.
> Actualizado: 2026-09-25.

## 1. Qué cuenta como réplica

Una réplica reproduce la regla de un artículo, o de un hallazgo del sistema, con datos que cualquiera puede descargar otra vez. Debe cumplir cuatro condiciones:

- Tiene un pre-registro fechado **antes** de la primera corrida.
- Tiene un script que la reproduce de principio a fin.
- Tiene un registro completo de variantes (`replicas/<ID>-variantes.csv`).
- Tiene una ficha llenada con `plantilla-replica.md`.

Una réplica **no** se mide por el número de artículos leídos ni por el tiempo invertido.

### Estados de una réplica

| Estado | Criterio |
|---|---|
| **Replicado** | En el periodo del artículo, el efecto tiene el mismo signo y una magnitud dentro de la tolerancia pre-registrada. Datos, reglas y diferencias están explicados. |
| **Replicado con diferencias** | El efecto tiene el mismo signo, pero la magnitud cae fuera de la tolerancia. O el efecto aparece solo en algunos segmentos. O requiere datos o reglas distintos a los del artículo. Toda diferencia queda explicada o marcada como no explicada. |
| **No replicado** | Se cumple el criterio de refutación pre-registrado. |
| **Pendiente** | Falta un dato, un acceso, una corrida o una decisión de método. La ficha dice exactamente qué falta. |

"Replicado" **no** significa "usable con dinero". Para que una regla sea candidata se necesitan, además:

- Resultado fuera de muestra (de preferencia después de la publicación), neto de costos.
- DSR ≥ `validacion_estrategias.deflated_sharpe_min_probabilidad`, que hoy es 0.95 en `config/parametros.json`.
- Superar a la regla sencilla en las mismas condiciones.
- Un backtest de al menos `backtest_min_anios` (10) años.
- Papel durante `paper_trading_min_meses` (3) y `paper_trading_min_operaciones` (30).

Los estados del conocimiento (Localizado, Documentado, Comprendido con comprobación, Contrastado, Replicado, Pendiente) siguen el protocolo del programa. Una réplica en estado Replicado es la evidencia que permite marcar el concepto como Replicado.

## 2. Flujo obligatorio

1. **Pre-registro.** Se copia `plantilla-replica.md` a `replicas/<ID>.md` y se llenan las secciones 1 a 9 **antes** de correr nada:
   - Hipótesis y mecanismo.
   - Criterio de refutación.
   - Datos, universo y periodo.
   - Regla y variantes planeadas.
   - Costos y regla sencilla de comparación.
   - Métrica principal y tolerancia.

   Se anota la fecha. Después **no se edita**. Cualquier cambio posterior va a "Desviaciones del pre-registro", con fecha y motivo.
2. **Datos.** Se descargan con `herramientas/datos_historicos.py`. Por cada fuente se anotan:
   - URL y versión (`version_crsp` y `sha256` en French).
   - Rango de fechas.
   - Huecos (`fechas_sin_precio` en Yahoo).
   - Fecha de disponibilidad de cada dato.
3. **Desarrollo.** Se corre con `herramientas/backtest.py` y `id_replica=<ID>`. **Cada** corrida se agrega sola al CSV de variantes. Esto incluye las fallidas, las que "no cuentan" y las que se corrieron por curiosidad.
4. **Validación y prueba.** El tramo de prueba se mira **una sola vez**, al final. Si después de verlo se ajusta algo, ese tramo pasa a ser de desarrollo. Esto se declara en la ficha y se busca un tramo nuevo (otro periodo, otro mercado u otra frecuencia).
5. **Deflactar.** `sharpe_deflactado_de_registro("<ID>")` usa el número de variantes probadas y la varianza de sus Sharpes. Si hubo pruebas fuera del registro (en otro script, a mano o en otra sesión), se pasa un `n_pruebas` mayor. El código no permite contar menos variantes de las registradas.
6. **Sensibilidad.** Se prueban fechas, parámetros vecinos, costos (escenarios de spread), subperiodos y moneda. Las corridas de sensibilidad de costos o de datos se registran con `es_prueba=False` y una `nota`. Quedan en el CSV, pero no inflan N.
7. **Conclusión.** Se llenan "Conclusiones permitidas" y "Conclusiones que NO se sostienen", y se asigna el estado.
8. **Resultados negativos.** Se conservan y se reportan igual que los positivos. Nunca se borran filas del CSV de variantes ni fichas No replicadas.

## 3. Separación de muestras

- **Un corte** (`cortes=[fecha]`) produce `dentro_muestra` y `fuera_muestra`. El corte natural es la fecha de publicación del artículo, o el fin de su muestra si se quiere replicar exactamente. La literatura documenta que muchos efectos se debilitan después de publicarse (McLean y Pontiff, 2016, *Journal of Finance*; ficha pendiente). Por eso el tramo posterior a la publicación es la prueba más exigente.
- **Dos cortes** producen `desarrollo`, `validacion` y `prueba`.
- Un periodo con fecha ≤ corte pertenece al segmento anterior. La curva de cada segmento arranca en el cierre del periodo previo.
- Si las ventanas de una señal se traslapan (por ejemplo, momentum de 12 meses), las primeras observaciones de un segmento usan datos del segmento anterior. Esto es legítimo porque son datos pasados, pero se declara.
- La selección de la variante ganadora ocurre **solo** en desarrollo o dentro de muestra. El DSR se calcula en ese segmento.

## 4. Anti look-ahead

El motor da tres garantías (detalle en el encabezado de `herramientas/backtest.py`):

1. **Estructural.** La señal recibe una `Historia` con vistas de solo lectura. Cuando decide el periodo *t*, las listas que ve contienen exactamente *t* observaciones (0..t-1): el dato *t* se agrega después de la decisión. `h.activo[t]` lanza `IndexError`. Las series externas (`extras`, `fx`) solo muestran entradas con fecha de disponibilidad ≤ fecha de *t-1*.
2. **Capturas.** Si la señal lleva, por *closure*, argumentos por defecto, atributos de `self`, `partial` o globales, un contenedor del tamaño de la muestra, se lanza `ErrorLookAhead`. La revisión es heurística. La regla del laboratorio es que la señal sea una función pura de su argumento.
3. **Señales precalculadas.** Solo se aceptan con `auditar_constructor`, que prueba la invariancia de prefijo. Una media centrada o un z-score con la media de toda la muestra no pasan.

Los datos macro revisables (PIB, empleo, inflación) se toman de **ALFRED** (`alfred(serie, fecha_vintage)`) o se desplazan a su fecha de publicación (`con_rezago`). Nunca se usa la serie revisada de FRED como si se hubiera conocido en su momento.

## 5. Costos (supuestos declarados)

| Concepto | Valor por defecto | Tipo | Fuente |
|---|---|---|---|
| Comisión por lado | 0.29% (0.25% + IVA 16%) | Hecho | Guía de Servicios GBM V1025, en `arena/investigacion/01-gbm-operativa-y-costos.md` §2.1 y §3 |
| Spread por lado | 0.05% (líquido); escenarios 0.15% (medio) y 0.30% (ilíquido) | **Supuesto [I], no verificado** | Mitad de la estimación de ida y vuelta 0.10/0.30/0.60% del mismo documento, §3 |
| Conversión cambiaria | No incluida por defecto | Pendiente | El spread cambiario de GBM no está publicado (§2.3). Se agrega como sensibilidad |
| Impuestos | Capa separada, no modelada | Pendiente | Protocolo §3.4 |

El modelo del motor cobra `|Δw| × (comisión + spread)` sobre el valor de la cartera, con deriva de pesos entre rebalanceos. No cobra costo de margen, préstamo de títulos ni la venta final. Toda réplica corre al menos el escenario por defecto y el de spread "medio".

**Moneda.** Con `fx` (MXN por USD, p. ej. FRED `DEXMXUS`, desde 1993-11-08) se usa 1 + R_MXN = (1 + R_USD) × FX_t / FX_{t-1}. Si el efectivo es CETES (ya en MXN), se pasa `efectivo_en_mxn=True`. DEXMXUS es una referencia de mediodía en Nueva York, no una cotización ejecutable en GBM.

## 6. Comparación contra una regla sencilla

Cada réplica corre, con las mismas fechas, costos, moneda y efectivo:

- Comprar y mantener (`senal_comprar_y_mantener`).
- 100% efectivo (`senal_efectivo`).
- Una regla sencilla del mismo tipo que la hipótesis (p. ej. `senal_media_movil(10)` o `senal_momentum_absoluto(12)`).

Si la regla del artículo no supera a la sencilla en Sharpe **y** en drawdown fuera de muestra, la conclusión permitida es "no agrega valor frente a la regla sencilla", aunque el efecto exista.

## 7. Datos: lo verificado en vivo el 2026-09-25

| Fuente | Rango | Notas |
|---|---|---|
| French `F-F_Research_Data_Factors` mensual | 1926-07-31 a 2026-07-31 (1201 meses) | CRSP 202607. Sección anual 1927–2025 (99 años). RF: Ibbotson hasta 202405 e ICE BofA desde 202406 (según el preámbulo del archivo) |
| French `F-F_Research_Data_Factors_daily` | 1926-07-01 a 2026-07-31 (26296 días) | CRSP 202607 |
| French `F-F_Momentum_Factor` mensual | 1927-01-31 a 2026-07-31 (1195 meses) | Faltantes marcados con -99.99 / -999 (0 en esta versión) |
| French `F-F_Research_Data_5_Factors_2x3` mensual | 1963-07-31 a 2026-07-31 (757 meses) | |
| Yahoo `^GSPC` mensual | 1985-01-31 a 2026-08-31 (500 meses) | Índice de **precio**: adjclose = close, sin dividendos. Se descartó septiembre de 2026 por estar incompleto |
| Yahoo `^GSPC` diario | 1927-12-30 a 2026-09-24 (24799 días) | Yahoo trae cierre nulo el 2026-09-22 (queda en `fechas_sin_precio`) |
| FRED `DEXMXUS` | 1993-11-08 a 2026-09-18 | |
| ALFRED `GDPC1` vintage 2008-10-31 | Última observación 2008-07-01 = 11720.0 | Un vintage anterior a la primera publicación responde 404 |

Comprobación de alineación. Se compararon los rendimientos mensuales de `^GSPC` (precio) con los del mercado French (Mkt-RF + RF, rendimiento total) en 498 meses comunes (1985-02 a 2026-07):

- Correlación de 0.9894 con las fechas alineadas, contra 0.0153 si se desfasan un mes.
- La diferencia media es de 0.181 pp al mes. Es consistente con que French incluye dividendos y `^GSPC` no; la atribución exacta no se ha verificado.

Advertencias de datos:

- **French.** Se registran `version_crsp` y `sha256` en cada réplica. El protocolo (fuente S07) menciona un cambio de formato desde enero de 2025 que afecta rendimientos y dividendos. Aquí solo se verificó el formato actual del archivo (preámbulo con la versión CRSP y la nota de la T-bill), no el efecto del cambio en las cifras. Al comparar con un artículo, hay que usar su versión de los datos o explicar la diferencia.
- **Yahoo.** Con `range=max` la API degrada la granularidad en silencio: devuelve `3mo` y 169 puntos desde 1984. `yahoo_historia` pide `period1`/`period2` y falla si la granularidad no coincide. Las barras mensuales traen fecha del día 1 con el cierre del último día del mes, y se re-etiquetan a fin de mes. Para rendimiento total del S&P 500 se usa `^SP500TR` o French.
- **Supervivencia.** Un universo armado con los componentes actuales de un índice tiene sesgo de supervivencia. Los factores French no lo tienen (vienen de CRSP), pero no son invertibles directamente.
- **Licencias.** Las condiciones de uso de cada fuente se copian a la ficha tal como las publica la fuente. Para French y Yahoo están **pendientes de verificar**. No se redistribuyen los datos crudos: el caché `datos/cache/` está en `.gitignore`.

## 8. Herramientas

```python
from herramientas import datos_historicos as dh, backtest as bt

f = dh.french("F-F_Research_Data_Factors", "mensual")    # fechas fin de mes; columnas en decimales
mercado = dh.rendimiento_mercado_french(f)                # [(fecha, Mkt-RF + RF)]
rf = dh.columna(f, "RF")
g = dh.yahoo_historia("^GSPC", "1mo")                     # dict: fechas, precios, fechas_sin_precio...
fx = dh.fred("DEXMXUS")
pib_2008 = dh.alfred("GDPC1", "2008-10-31")

r = bt.backtest_senal(mercado, rf, bt.senal_media_movil(10), id_replica="R001-ejemplo",
                      variante="sma10", min_historia=10, cortes=["2007-01-01"],
                      parametros={"ventana": 10}, fuente_datos=f"French CRSP {f['version_crsp']}")
print(r.resumen())
print(bt.sharpe_deflactado_de_registro("R001-ejemplo"))
```

- `backtest_senal(...)` pide `id_replica` de forma obligatoria. `id_replica=None` corre sin registrar y está reservado para pruebas unitarias.
- `comparar([r1, r2, ...], segmento)` arma una tabla de texto para la ficha.
- `leer_registro("<ID>")` devuelve las filas del CSV de variantes.

Pruebas, sin red:

```
python3 -m unittest herramientas.tests.test_backtest herramientas.tests.test_datos_historicos
```

Prueba en vivo de las fuentes (descarga y reporta rangos):

```
python3 -m herramientas.datos_historicos
```

## 9. Estructura

```
laboratorio/
  README.md                 este documento
  plantilla-replica.md      ficha y pre-registro
  replicas/
    <ID>.md                 ficha (pre-registro + resultados)
    <ID>.py                 script reproducible
    <ID>-variantes.csv      registro automático, una fila por corrida y segmento; nunca se edita a mano
```

Pendientes del laboratorio:

- PBO (probabilidad de sobreajuste del backtest, `validacion_estrategias.pbo_max` = 0.25) no está implementado.
- Costo cambiario verificado en GBM.
- Condiciones de uso de French y Yahoo.
- Ficha de McLean y Pontiff (2016).
