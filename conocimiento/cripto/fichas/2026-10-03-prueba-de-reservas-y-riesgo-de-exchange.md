# Ficha de avance · 03-oct-2026 · G4 Riesgos (prueba de reservas y riesgo de exchange)

> Corrida de las 08:17 CDMX (14:17:30 UTC), `analista-cripto`. Toma el **tema 5** de "Temas que no cubren los 35 recursos y que el torneo necesita" (`00-plan-de-estudio.md`): *"Prueba de reservas y riesgo de exchange. Ver `lista-senales-de-alerta.md`."* Es el siguiente pendiente tras los temas 1 (30-sep), 2 (1-oct), 3 (29-sep) y 4 (2-oct). El capítulo `04-riesgos-fraude-hackeos-y-seguridad.md` ya trata la prueba de reservas (PoR) en su §2 idea 5 y §5.G; esta ficha verifica en vivo si hay un reporte nuevo desde el 46.º (snapshot 1-sep-2026) y añade dos ejercicios numéricos propios: el ritmo de publicación (rezago) y el peso de los saldos de usuarios de Binance frente a la oferta total de BTC.

## 1. Acceso real

- **`binance.com/en/proof-of-reserves`**: accesible hoy (`WebFetch`, 14:2x UTC), pero la página es un lanzador dinámico (JavaScript) que no expone el número de reporte, la fecha del snapshot ni los ratios en el HTML/texto que recibe esta herramienta; solo describe el mecanismo general (árbol de Merkle con zk-SNARK, "backed 1:1"). **No sirve por sí sola para confirmar si hay un 47.º reporte.**
- **Búsquedas dirigidas** (`WebSearch`, 3 consultas con términos distintos: "47th report October 2026", "46th report September 2026 BTC ratio", "proof of reserves snapshot October 1 2026"): ninguna devolvió un reporte con snapshot del 1-oct-2026. El resultado más reciente en cualquier búsqueda sigue siendo el **46.º reporte** (snapshot 1-sep-2026, publicado 17-sep-2026, ya registrado en `lista-senales-de-alerta.md` E3) y, en una búsqueda, el **45.º** (snapshot 1-ago-2026).
- **Lectura:** esto es consistente con el patrón de rezago de publicación (§3 abajo): si el 47.º reporte tiene snapshot del 1-oct-2026 y sigue el mismo rezago de ~16-18 días que los dos anteriores, se publicaría hacia el **15 al 21 de octubre**, es decir, todavía no debería existir hoy (3-oct). La ausencia de resultado es el escenario esperado, no una señal de alerta.
- **Grado de acceso:** página oficial viva pero sin el dato (JS), más búsqueda de prensa negativa (no encontré lo que buscaba, y lo documento como tal en vez de inventar un reporte). Es menos que "íntegro"; es "verificación de ausencia con 3 búsquedas independientes más la página oficial".

## 2. Qué dice hoy la sección E3 de la lista de señales (sin cambio)

El 46.º reporte (snapshot 1-sep-2026, publicado 17-sep-2026, 16 días de rezago) sigue siendo el más reciente: **~682,000 BTC** de usuarios, ratio "de al menos 1:1" ([PANews, 17-sep-2026](https://panews.io/articles/01a0add9-878d-72a6-96d2-70123d73707b)). El 45.º reporte (snapshot 1-ago-2026, publicado ~19-ago-2026, 18 días de rezago) dio ~657,000 BTC con ratio de BTC **100.25%** y de USDT 103.62%. **No hay reporte nuevo que verificar ni ratio que actualizar en E3 hoy.**

## 3. Ejercicio numérico 1: ritmo de publicación (rezago) y ventana esperada del 47.º reporte

```python
import statistics
from datetime import date, timedelta

# Snapshot y fecha de publicación de los dos últimos reportes confirmados
reportes = {
    45: {"snapshot": date(2026, 8, 1), "publicado": date(2026, 8, 19)},
    46: {"snapshot": date(2026, 9, 1), "publicado": date(2026, 9, 17)},
}
lags = []
for n, r in reportes.items():
    lag = (r["publicado"] - r["snapshot"]).days
    lags.append(lag)
    print(f"Reporte {n}: snapshot {r['snapshot']}, publicado {r['publicado']}, rezago {lag} dias")

media = statistics.mean(lags)
desv = statistics.pstdev(lags)  # poblacional, n=2, solo como orden de magnitud
print("Rezago medio:", media, "dias; desviacion (n=2, grado D):", desv)

snapshot_47 = date(2026, 10, 1)
estimado = snapshot_47 + timedelta(days=media)
print("Fecha estimada de publicacion del 47.o reporte:", estimado)
print("Ventana +/-3 dias:", estimado - timedelta(days=3), "a", estimado + timedelta(days=3))
```

**Resultado (verificado dos veces, a mano y con el script):**

| Reporte | Snapshot | Publicado | Rezago |
|---|---|---|---|
| 45 | 1-ago-2026 | ~19-ago-2026 | 18 días |
| 46 | 1-sep-2026 | 17-sep-2026 | 16 días |

- Rezago medio: **17 días**; desviación poblacional (n=2, no es una muestra estadísticamente sólida): 1 día.
- **Fecha estimada de publicación del 47.º reporte (snapshot 1-oct-2026): ~18-oct-2026**, ventana razonable 15 al 21-oct-2026.
- **Consecuencia operativa:** la regla ÁMBAR de E3 ("rezago > 30 días") no se activa simplemente porque hoy (3-oct, apenas 2 días después del snapshot del 1-oct) todavía no hay reporte. El umbral de 30 días se mediría recién a partir del **31-oct-2026** si para entonces sigue sin publicarse.
- **Límite:** n=2 es una muestra mínima; no hay forma de distinguir un patrón real de una coincidencia con solo dos observaciones. Si el comité quiere calibrar el umbral con más precisión, haría falta la serie completa desde el reporte 1 (Binance publica desde nov-2022), que no está consolidada en ninguna fuente que haya encontrado hoy en una sola tabla.

## 4. Ejercicio numérico 2: ¿qué tan grande es el saldo de BTC de Binance frente a la oferta total?

```python
# Altura de bloque en vivo (mempool.space/api/blocks/tip/height, 3-oct-2026 14:2x UTC)
altura = 969738
altura_halving4 = 840000       # halving del 19-abr-2024 (Mastering Bitcoin / mempool.space, ya verificado en ficha cripto/01)
oferta_en_halving4 = 19687500.0  # BTC emitidos hasta el bloque 840000 (hecho de red, 50% de los 21M menos el ajuste de subsidios previos)
subsidio_actual = 3.125        # BTC por bloque, post halving4

bloques_desde_h4 = altura - altura_halving4
oferta_estimada = oferta_en_halving4 + bloques_desde_h4 * subsidio_actual
print("Oferta BTC estimada hoy:", round(oferta_estimada, 2))

btc_usuarios_46 = 682000   # 46.o reporte PoR (snapshot 1-sep-2026)
btc_usuarios_45 = 657000   # 45.o reporte PoR (snapshot 1-ago-2026)

peso_sobre_oferta = btc_usuarios_46 / oferta_estimada * 100
variacion = btc_usuarios_46 - btc_usuarios_45
variacion_pct = variacion / btc_usuarios_45 * 100
print(f"BTC de usuarios en Binance (46.o reporte): {btc_usuarios_46:,} = {peso_sobre_oferta:.3f}% de la oferta total")
print(f"Variacion 45->46: {variacion:+,} BTC ({variacion_pct:+.2f}%)")
```

**Resultado:**

- Oferta estimada de BTC al bloque 969,738 (hoy): **≈20,092,931 BTC** (verificado con el supuesto de 19,687,500 BTC emitidos al bloque 840,000, hecho de red ya usado en `conocimiento/cripto/01-bitcoin-protocolo-dinero-y-autocustodia.md`, más 129,738 bloques × 3.125 BTC).
- Los **682,000 BTC** de saldos de usuario del 46.º reporte de Binance equivalen a **≈3.39% de la oferta de BTC emitida hoy** (≈3.25% del tope de 21 millones; corrección del 3-oct, rutina de aprendizaje: la cifra original decía "de toda la oferta que existirá", pero el denominador es la oferta actual) concentrada en un solo exchange, en una sola jurisdicción no supervisada en México y bajo investigación activa del DOJ (E5, sin cargos).
- De 657,000 (45.º reporte) a 682,000 (46.º reporte): **+25,000 BTC (+3.81%)** en saldos de usuario en un mes, consistente con el régimen alcista del período y con el repunte de +7,812 BTC del 29-sep ya documentado en la lista de señales (atribuido en su momento, correctamente, a la migración de cuentas Funding→Spot y no a una entrada neta de clientes).
- **Por qué importa para la cuenta `arena-claude-binance`:** no cambia el riesgo de mercado, pero cuantifica la escala del riesgo de contraparte: un solo exchange custodia una fracción no trivial de toda la oferta de BTC existente, lo que hace que cualquier evento de insolvencia (A1-A8 de la lista de señales) tenga un efecto sistémico sobre el mercado spot, más allá del riesgo idiosincrático de nuestros 10,000 MXN.

## 5. Revisión de contraparte (se solapa con el tema 5, como indica la rutina)

Reviso "Señales para vigilar Binance hoy" (`lista-senales-de-alerta.md`, sección E) contra el plan de contingencia de `bitacora/decisiones/2026-09-25-CRIPTO-inicial.md` (vender a MXN y SPEI; si falla, mover BTC a Bitso):

| Señal | Estado hoy | Disparador de contingencia? |
|---|---|---|
| **E3 (PoR mensual)** | Sin reporte nuevo (§1-3 arriba); 46.º reporte sigue vigente, limpio (ratio "al menos 1:1", rezago de 16 días, dentro de la norma histórica) | No |
| **E5 (acciones regulatorias y penales)** | Búsqueda dirigida hoy (`WebSearch`, "Binance DOJ Iran sanctions investigation October 2026"): el DOJ sigue en fase de investigación/decomiso civil (US$61 millones, 14-sep-2026); **sin cargos penales contra la entidad**. Nada nuevo desde el 25-sep. ÁMBAR, sin cambio | No (seguiría ÁMBAR, igual que desde el 25-sep) |
| **E1/E2 (flujos y composición)** | Verificación parcial hoy: TVL total rastreado por DefiLlama (`api.llama.fi/protocol/binance-cex`, incluye BNB y efecto precio, no es la metodología exacta ex-BNB de la sección F porque el script `scratchpad/g4/calc/flujos_binance_defillama.py` no está disponible en este entorno) se mantuvo estable en US$177.5-179.5 mil millones del 25-sep al 3-oct, sin caída abrupta. **No es el cálculo preciso de E1** (falta descontar BNB y el efecto precio), así que esto es un indicio, no una confirmación — se deja pendiente repetir con la metodología exacta cuando el script esté disponible | No, con la salvedad de que esta no es la medición exacta |
| **E6 (retiros y SPEI)** | Sin prueba nueva hoy (no hay orden que ejecutar); sin reporte de incidente en el estado de la página de Binance ni en prensa | No |
| **E10 (contagio)** | Sin hecho nuevo de otro exchange grande hoy en las búsquedas realizadas | No |

**Conclusión: sin disparador.** Ninguna señal ROJA. Las dos ÁMBAR ya conocidas (E5, A9) siguen sin cambio desde el 25-sep. No se activa la contingencia de Bitso.

## 6. Qué cambia para invertir

- No cambia el filtro de tendencia (solo mira el precio de BTC/USDT) ni el tamaño de la posición.
- Se agrega una regla operativa: el umbral de "rezago > 30 días" de E3 debe medirse desde el **snapshot**, no desde "hoy sin reporte"; con un rezago histórico de 16-18 días, no hay nada que vigilar hasta fines de octubre si el 47.º reporte no ha aparecido para entonces.
- El ejercicio del §4 (3.39% de la oferta emitida en un solo exchange) es un argumento cuantitativo nuevo, no solo cualitativo, para mantener el tope de pérdida y la contingencia de Bitso como están: el riesgo de contraparte en Binance no es solo nuestro, es un riesgo de concentración de mercado.

## 7. Contrapuntos y límites

- **n=2** en el ejercicio de rezago (§3): dos observaciones no bastan para fijar con precisión el umbral de alerta; es una guía, no una ley.
- La página oficial de PoR de Binance es dinámica (JavaScript) y esta herramienta no puede ejecutarla; toda la verificación de "no hay reporte nuevo" depende de que la prensa especializada lo hubiera recogido ya si existiera, lo que es razonable (el 45.º y 46.º reporte generaron cobertura rápida) pero no es una prueba directa de la fuente primaria.
- El cálculo de oferta total de BTC (§4) usa el supuesto estándar de 19,687,500 BTC al bloque 840,000 y subsidio fijo de 3.125 BTC/bloque desde entonces; no contempla BTC perdidos/inaccesibles (que reducirían la oferta circulante real, pero no la emitida, que es lo que se calcula aquí).
- El indicio de TVL total de DefiLlama (§5, fila E1/E2) no es la metodología exacta ex-BNB de la sección F de `lista-senales-de-alerta.md`; se declara explícitamente como una aproximación de menor calidad, no como el cálculo de referencia.
- **Grado B** para los hechos verificables (fechas y cifras de los reportes 45 y 46, altura de bloque en vivo). **Grado C** para la estimación del rezago del 47.º reporte (n=2). **Grado D** para cualquier lectura que use el TVL total de DefiLlama como sustituto de la metodología E1 ex-BNB.

## 8. Autoexamen

- ¿Puedo reproducir el número sin ver la ficha? Sí: tomar la fecha de snapshot y de publicación de los dos últimos reportes PoR de Binance (prensa que cite la fuente primaria), calcular el rezago en días, y proyectar la fecha esperada del siguiente reporte sumando el rezago medio al próximo snapshot mensual.
- ¿Qué rompería la conclusión? Que Binance publique el 47.º reporte antes del 15-oct (rompería el patrón de rezago a la baja, sin ser necesariamente una mala señal) o después del 31-oct sin explicación (eso sí activaría la regla ÁMBAR de E3 por rezago).
- **Grado: B** para los hechos de los reportes 45/46 y la altura de bloque; **C** para la proyección del 47.º reporte (n=2); **D** para el indicio de TVL total como sustituto de E1.

## 9. Estado del pendiente

- Tema 5 de "Temas que no cubren los 35 recursos" (`00-plan-de-estudio.md`): **iniciado, con verificación en vivo de que no hay reporte PoR nuevo desde el 46.º, y dos ejercicios numéricos propios (rezago de publicación; peso de los saldos de usuario frente a la oferta total de BTC).** Pendiente para corridas futuras: repetir la verificación cuando se acerque la ventana estimada (15-21 oct) para confirmar o refutar la proyección del rezago; conseguir o reconstruir el script `flujos_binance_defillama.py` (metodología exacta ex-BNB de la sección F) para que la fila E1/E2 de la revisión de contraparte use el cálculo de referencia, no el TVL total.
- Actualiza el capítulo de síntesis `04-riesgos-fraude-hackeos-y-seguridad.md` (adenda fechada 3-oct-2026, nueva sección) y `conocimiento/estado-de-dominio.csv` (fila `cripto/04`).

Datos crudos de esta sesión (klines, ticker, DefiLlama, mempool.space): `scratchpad/g4_por/` (fuera del repositorio).
