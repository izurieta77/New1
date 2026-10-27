# Ficha de avance · 27-oct-2026 · Variance swap propio sobre la cadena de Deribit y prima de evento de la elección intermedia de EUA (3-nov)

> **Por qué este tema.** Es el siguiente punto de la cola académica del plan (`00-plan-de-estudio.md`, fila "Literatura académica…": "prima de evento de la elección de EUA (3-nov) y VRP con variance swap propio") y los puntos 1 y 2 de la §7 de la ficha del 26-oct. Ayer la prima de evento se midió con IV ATM; el DVOL es una varianza de swap. Hoy se construye el swap propio, se coteja contra el DVOL publicado y se aplica a la elección, que cae en 7 días.

## 0. Preguntas de hoy

1. ¿Puedo reproducir el DVOL con la fórmula de variance swap sobre la cadena pública de Deribit? ¿Cuánto separa el swap de la IV ATM?
2. ¿Cuánta varianza extra cotiza la cadena para la elección del martes 3-nov, y cuánto movió BTC el día de resultados en las elecciones de 2014 a 2024?
3. ¿Cambia la lectura del FOMC del 28-oct al pasar de ATM a swap?

## 1. Acceso y fuentes (declarado)

| Fuente | Grado | Acceso real |
|---|---|---|
| **CBOE, *VIX White Paper*** (fórmula σ² = (2/T) Σ ΔK/K² e^{rT} Q(K) − (1/T)(F/K0 − 1)², interpolación a 30 días) | **A** (emisor del índice) | **Secundario aquí:** la fórmula se aplicó como la resume la metodología DVOL de Deribit leída el 26-oct (sección íntegra; ficha del 26-oct §1). El PDF de CBOE no se volvió a leer hoy |
| **Deribit API pública**: `public/get_book_summary_by_currency?currency=BTC&kind=option` (876 opciones, `mark_price`, posturas, `mark_iv`, `underlying_price`), `public/get_index_price`, `public/get_volatility_index_data` (DVOL 1 min) | **A** (dato del mercado) | Íntegro; foto del 27-oct 14:36 UTC guardada en [`2026-10-27-variance-swap-eleccion-datos.json`](2026-10-27-variance-swap-eleccion-datos.json) |
| **Binance** `data-api.binance.vision` klines BTCUSDT 8h (2018, 2020, 2022, 2024) y **Yahoo** `BTC-USD` 1d (2014-2024) | **A** / **B** | Íntegro (en el `.json`) |
| **2 U.S.C. § 7** ([LII Cornell](https://www.law.cornell.edu/uscode/text/2/7)): la elección es "the Tuesday next after the 1st Monday in November, in every even numbered year" | **A** (ley) | Íntegro. En 2026, primer lunes = 2-nov → **martes 3-nov** |

**No leído (no se cita como evidencia):** literatura de elecciones y volatilidad implícita en acciones (p. ej., Kelly-Pástor-Veronesi, JF 2016, sobre opciones que abarcan elecciones). Solo lo nombro como marco; queda en la cola.

## 2. Método [H]

- **Precio en USD a plazo:** Deribit liquida opciones inversas (pago en BTC = pago en USD / S_T). Una opción que cuesta `mark_price` BTC vale `mark_price × S0` USD hoy y `mark_price × F` USD a plazo, con F = `underlying_price` del vencimiento. Con eso la fórmula del VIX se aplica sin factor de descuento.
- **Franja:** puts OTM debajo de K0 (mayor strike ≤ F), calls OTM arriba, promedio put-call en K0; corte tras dos precios cero consecutivos (regla CBOE). Tres variantes: precio `mark` (modelo de Deribit), punto medio de posturas (solo con bid > 0) y **filtro |Δ| ≥ 5%** (regla del DVOL; delta de Black-76 con `mark_iv`).
- **30 días:** varianza total lineal en el tiempo entre los vencimientos que rodean 30 días (13-nov y 27-nov).
- **Evento:** varianza total w = σ²T; vol a plazo del tramo = Δw/ΔT; varianza extra del evento = w del tramo − (tasa base × duración). Base: tramo limpio siguiente (6→13-nov).
- **Comprobación sintética** (en el `.py`): cadena Black-76 con vol plana 40% a 9 días, strikes de 1,000 en 1,000: el swap da **40.13** (sesgo de discretización +0.13) y la ATM 40.00.

## 3. Ejercicio numérico (comprobado en Python)

Código: [`2026-10-27-variance-swap-eleccion.py`](2026-10-27-variance-swap-eleccion.py). Se reproduce con `python3 -I conocimiento/cripto/fichas/2026-10-27-variance-swap-eleccion.py` (y `… descargar` para una foto nueva).

### A. Swap por vencimiento y réplica del DVOL (foto 27-oct 14:36 UTC; índice 80,229; DVOL 37.47)

| Vencimiento (08:00 UTC) | Días | Strikes | Swap (mark) | IV ATM | Swap − ATM | Swap, |Δ| ≥ 5% |
|---|---|---|---|---|---|---|
| mié 28-oct | 0.72 | 27 | 31.56 | 27.76 | +3.80 | 29.44 |
| jue 29-oct | 1.72 | 27 | 37.32 | 34.17 | +3.15 | 35.18 |
| vie 30-oct | 2.72 | 56 | 37.98 | 33.93 | +4.06 | 35.12 |
| sáb 31-oct | 3.72 | 26 | 36.12 | 33.56 | +2.56 | 34.86 |
| vie 6-nov | 9.72 | 22 | 40.01 | 37.79 | +2.22 | 38.65 |
| vie 13-nov | 16.72 | 17 | 38.11 | 36.37 | +1.74 | 37.60 |
| vie 27-nov | 30.72 | 48 | 39.15 | 35.98 | +3.17 | 37.48 |
| vie 25-dic | 58.72 | 60 | 42.27 | 36.83 | +5.44 | 38.53 |

- **Swap a 30 días propio: 39.12** con la franja completa (39.13 con punto medio). **Con el filtro |Δ| ≥ 5% del DVOL: 37.49, contra 37.47 publicado (+0.02 pts).** La réplica es exacta a la segunda decimal.
- Las alas con |Δ| < 5% suman **+1.63 pts**: 8.2% de la varianza a 30 días (39.12² − 37.49² = 124.9 de 1,530.4). El DVOL **deja fuera la cola profunda** por construcción.
- **Swap − ATM = +1.4 a +5.4 pts** según el plazo (+2.6 a +4.1 en los diarios). La sonrisa pesa: medir eventos con ATM (como el 26-oct) subestima la varianza en ~7-24%.

### B. Varianza a plazo por tramo

| Tramo | Días | Vol a plazo swap | σ del tramo | Vol a plazo ATM | Qué trae |
|---|---|---|---|---|---|
| 28→29-oct | 1 | 40.99 | 2.15% | 38.16 | **FOMC (decisión 28-oct 18:00 UTC)** |
| 29→30-oct | 1 | 39.10 | 2.05% | 33.50 | PIB EUA, BCE |
| 30→31-oct | 1 | 30.46 | 1.59% | 32.55 | viernes→sábado |
| **31-oct→6-nov** | 6 | **42.25** | **5.42%** | 40.20 | **elección 3-nov** |
| 6→13-nov | 7 | 35.30 | 4.89% | 34.30 | base (IPC de octubre: fecha sin verificar, BLS da 403) |
| 13→27-nov | 14 | 40.36 | 7.90% | 35.51 | — |

- **Elección (swap):** varianza extra **8.86 %²** → **salto de 1σ de 2.98%**; el día de resultados vale **3.59×** un día base (ATM: 2.69% y 3.24×). σ del día 3→4-nov implícita **≈ 3.50%** contra 1.85% de un día base.
- **FOMC (swap):** σ del tramo 2.15% (ATM 2.00%); razón contra la base 6→13-nov **1.35** (ATM 1.24; contra 30→31-oct, un tramo de fin de semana, 1.81). Sigue **arriba del intervalo histórico 0.47-1.11** de la ficha del 26-oct: la conclusión "prima del FOMC cara" no cambia al pasar a swap. P0184 sigue igual (umbral 2.07% entre el ATM 2.00% y el swap 2.15%).

### C. Histórico: día de resultados contra los 20 días previos

Ventana Binance: martes 08:00 → miércoles 08:00 UTC (velas 8h). Yahoo: vela UTC del miércoles (cierre miércoles / cierre martes). r²/σ² = razón de varianzas del evento.

| Elección | Tipo | Binance r | r²/σ² | Yahoo r | r²/σ² |
|---|---|---|---|---|---|
| 4-nov-2014 | intermedia | — | — | +2.69% | 0.98 |
| 8-nov-2016 | presidencial | — | — | +1.87% | 0.57 |
| 6-nov-2018 | intermedia | +1.76% | 4.21 | +1.06% | 2.42 |
| 3-nov-2020 | presidencial | +1.16% | 0.30 | +1.31% | 0.31 |
| **8-nov-2022** | intermedia | −8.19% | 13.73 | −15.49% | 26.51 |
| 5-nov-2024 | presidencial | +6.30% | 15.56 | +8.67% | 22.61 |

- **2022 está contaminado:** fue la semana de la quiebra de FTX (cap. 04: balance de Alameda del 2-nov-2022, quiebra el 11-nov-2022; el 8-nov Binance anunció y luego abandonó la compra, [H] secundario). No es un efecto electoral; se excluye.
- **Sin 2022 (5 elecciones en Yahoo):** mediana **0.98**, media 5.38, dominada por 2024 (presidencial con candidato pro-cripto). **Solo intermedias limpias (2014, 2018): 0.98-4.21.**
- **Lectura:** la razón implícita (3.6) queda **arriba de la mediana histórica (~1) pero dentro del rango de las intermedias** (hasta 4.2). Con 5 eventos no se puede decir que esté cara; a diferencia del FOMC (46 eventos, 1.35 contra un techo de 1.11), aquí no hay muestra para un veredicto.

### D. Probabilidades para el pronóstico (día 3→4-nov, 08:00→08:00 UTC)

| Umbral \|r\| | Normal con σ implícita de elección (3.50%) | Normal con σ base (1.85%) | Empírica sin evento (80 días base escalados) |
|---|---|---|---|
| 2.0% | 0.57 | 0.28 | 0.24 |
| 2.5% | 0.48 | 0.18 | 0.17 |
| **3.0%** | **0.39** | **0.10** | **0.14** |

Con la mediana histórica de las intermedias limpias (razón ~2.4 entre 0.98 y 4.21), σ ≈ 1.85% × √2.4 ≈ 2.9% y P(|r| > 3%) ≈ 0.30 (normal). Elecciones limpias con |r| > 3%: 1 de 5 (2024).

## 4. Qué cambia para invertir [I/O]

- **El DVOL es reproducible con datos públicos.** El pulso puede verificarlo y, sobre todo, **calcular el swap de cualquier tramo** (el DVOL solo da 30 días). La VRP de la ficha del 26-oct, medida con DVOL, ya es una VRP de swap truncado; con la franja completa la implícita sube ~1.6 pts y la VRP sube lo mismo. La conclusión "en calma, la realizada futura superó al DVOL" **se debilita**: con la franja completa, la fila "RV < 35" pasaría de −3.2 a ≈ −1.6 pts (estimación con la diferencia de hoy, no medida en la serie).
- **La elección es el evento más caro del calendario cercano:** salto implícito de ~3% (1σ). Para el filtro (salida 70,839, colchón +13.3% al precio de la foto): un salto de 3σ de la elección (~9%) no lo alcanza solo. **Ninguna acción**; la cuenta es spot y no vende opciones (`cripto_binance` prohíbe opciones).
- **Para el pulso:** a partir de hoy, la σ de un tramo se mide con el swap (no ATM) y se compara con la base del tramo limpio siguiente.

## 5. Contrapuntos y límites

- **`mark_price` es modelo de Deribit**, no precio operado; el punto medio de posturas da lo mismo (39.13), pero las alas profundas tienen poca liquidez. El DVOL usa VWAP con profundidad de 2 BTC; aquí no.
- **No hay diarios del 3 ni del 4-nov todavía**: el evento se aísla con un tramo de 6 días (31-oct→6-nov) contra una base de 7. Ambos tienen fin de semana (2 de 6 días contra 2 de 7) y la base puede traer el IPC de octubre (fecha sin verificar): si la base está inflada, el salto electoral está **subestimado**. Repetir cuando Deribit liste el 4-nov.
- **Historia mínima:** 5 elecciones limpias, 2 intermedias. 2024 sola mueve la media de ~1 a 5.4. Una razón implícita de 3.6 no es refutable con esa muestra.
- **Sesgo de discretización:** +0.13 pts en la prueba sintética con strikes cada 1,000; en vencimientos de un día con 26-27 strikes, mayor. Afecta poco a los cocientes entre tramos.
- **Una sola foto** (14:36 UTC). La estructura de plazo se mueve día a día; las cifras de B son de hoy.

## 6. Autoexamen

1. ¿Por qué el precio de una opción de Deribit en USD a plazo es `mark_price × F` y no `mark_price × S0`? (S0 da el valor hoy; para la fórmula del VIX, Q va en valor a plazo, e^{rT}·Q = mark × S0 × e^{rT} = mark × F.)
2. ¿Qué parte de la diferencia entre mi swap (39.12) y el DVOL (37.47) explica la regla |Δ| ≥ 5%? (Toda: con el filtro da 37.49.)
3. ¿Cómo se obtiene el salto de 1σ de un evento sin un vencimiento diario que lo aísle? (w del tramo − tasa base × días del tramo; raíz de la diferencia.)
4. ¿Por qué se excluye 2022 de la muestra electoral? (FTX quebró esa misma semana: el movimiento no es electoral.)

## 7. Estado

- **Documentado con comprobación** (Doctorado: microestructura de opciones). Swap propio validado contra el DVOL (+0.02 pts) y contra una cadena sintética; elección medida con datos A; historia con 5 eventos limpios (A/B).
- **Siguiente prueba:**
  1. resolver P0190 (4-nov) y P0184 (29-oct); repetir B con los diarios del 3-4-nov cuando se listen;
  2. leer Kelly-Pástor-Veronesi (JF 2016) si hay copia legal, y el PDF de CBOE para la regla de corte exacta;
  3. VRP de swap con franja completa en la serie histórica (requiere cadenas históricas: sin vía pública gratuita conocida).
