# Decisión: cartera cripto inicial real de la cuenta `arena-claude-binance` (10,000 MXN)

- **Fecha de decisión:** 25-sep-2026, después del cierre de NYSE. La hora queda sellada por el commit de este archivo, antes de cualquier precio de ejecución.
- **Ejecución:** lunes 28-sep-2026, en real, por el dueño en la app de Binance. Solo spot. Decisión del dueño del 25-sep-2026: 10,000 MXN por IA, que cuentan para la competencia.
- **Temporada:** 28-sep-2026 a 28-ene-2027.
- **Perfil:** `cripto_binance`. Tope del dueño: pérdida de 5,000 MXN.
- **Estado de este documento:** completo. Comité, verificador y gestor de riesgo (aprueba con cambios, ya aplicados). Boletas en `bitacora/boletas/2026-09-28.md`.

## Tesis y cómo se refutaría

**Tesis:** en 4 meses no hay ventaja demostrada entre las variantes cripto. Con la cartera A en GBM:
- P(quedar primero) es 36.9% para 100% BTC, 37.2% con filtro SMA200 y 36.2% sin cripto (cuantitativo, 9 métodos; el error estándar es de 5-9 pp);
- la cripto aporta 80-88% de la varianza de la cuenta combinada con 33% del capital.

Por eso la cuenta cripto se juega por **supervivencia y desempate por menor caída**: BTC como única moneda, reserva en MXN, un filtro de tendencia, sin ETH y sin compra de caídas.

**Se refuta si, al 28-dic-2026:**
- la cuenta cripto tocó −30%; o
- quedó 5 pp o más debajo de un 100% BTC comprar-y-mantener medido en papel, sin haber tenido una caída máxima al menos 10 pp menor.

## Dictámenes (3 líneas cada uno)

- **Abogado del diablo, confianza 70. Voto: en contra de K1-K4 tal como están.**
  - Tasa base (BTC en MXN, ventanas de 122 días desde 2018): tocó −30% en 26.5% de las ventanas y −50% en 3.7%.
  - K2 le ganó a K1 solo en 25% de las ventanas. K4 (comprar caídas) sube P(−30%) de 12.8% a 19.2%.
  - Prefiere 65% BTC / 35% MXN: tocó −30% en 8.5% de las ventanas; peor caso −38.7%.
  - Condiciones:
    - cortacircuitos que vendan (ya aplicados, commit c31a2c9);
    - ruta MXN→USDT→BTC con límite;
    - sin stops en pares MXN;
    - plan por si Binance restringe México.
- **Macro, confianza 60. Voto: K4 con freno (55% BTC, 20% ETH, 25% USDC).**
  - Régimen mixto: VIX 14.9 y spread HY 2.73% a favor; tasa real de 2.85% y bono a 10 años en 5.18% en contra. En 2026, BTC pierde 1.1% por cada +10 pb semanales de tasa real.
  - Con la tasa real subiendo 40 pb o más, P(−50%) fue 13% en K1 y 0% en K4 con freno (n≈5, grado C).
  - Riesgo: la Fed del 28-oct y una tasa real mayor a 3.1%.
- **Analista cripto, confianza 55. Voto: K4 modificada (60% BTC en dos tramos, 20% ETH, 20% reserva en −10%).**
  - Régimen alcista: +18.5% sobre la SMA200, flujos a ETFs de +2,560 M USD en septiembre.
  - En estados como el de hoy, P(tocar −20%) es K1 51%, K3 65% y K4 37%. Según él, K3 duplica lo que ya hacen los cortacircuitos.
  - Verificó pares con MXN, OCO, comisión de 0.10%, SPEI por Medá y la migración de Funding a Spot desde el 29-sep.
- **Cuantitativo, confianza 45. Voto: K3, 100% BTC con salida total bajo la SMA200.**
  - K2 y K4 quedan debajo de K1 en los 9 métodos. K1 y K3 empatan estadísticamente. La compra de caídas es grado D (t = 1.05).
  - BTC cae 20% o más desde su máximo en 61-82% de las temporadas.
  - Simulación en `arena/modelos/cripto_inicial_simulacion.py`.
- **Geopolítico, confianza 60. Voto: K3 con destino 65% BTC / 35% MXN, sin ETH.**
  - Escalonado: 4,000 MXN el 28-sep, 1,500 tras el FOMC del 28-oct y 1,000 tras el 4-nov. BTC no fue refugio en 10 choques militares (2022-26).
  - Contraparte: el DOJ investiga a Binance por sanciones a Irán, sin cargos. Según el verificador, es solo un reporte de Bloomberg del 22-sep, leído vía CoinDesk; no hay fuente primaria. El exchange no está autorizado en México y no puede estarlo; ver la verificación.
  - Contingencia: abrir y probar Bitso, con disparadores definidos.

## Votos y regla aplicada (por componente, como en la cartera de GBM)

| Componente | A favor | ¿Sobrevive al abogado del diablo? | Resultado |
|---|---|---|---|
| BTC | 5 de 5 (confianza media 58) | Sí | **Entra** |
| ETH | 2 de 5 (macro 60, analista cripto 55) | No: "no sobrevive" y no hay 4 votos con confianza ≥ 60 | Fuera |
| Compra de caídas o reserva que compra | 2 de 5 (macro, analista cripto) | No: "no sobrevive" | Fuera |
| Filtro SMA200 (reducir o pausar bajo la SMA200) | 3 de 5 (cuantitativo, macro, geopolítico) | Sí, con condiciones (whipsaw; el dueño ejecuta a mano) | **Entra**. La forma exacta la fija el gestor de riesgo. |
| Efectivo en MXN o en stablecoin | MXN: abogado, geopolítico y analista cripto; USDC: macro | — | **MXN** |
| Exposición y escalonamiento | Abogado 65% y geopolítico 65% escalonado; cuantitativo 100%; macro y analista cripto 55-60% en BTC | — | La fija el gestor de riesgo |

**Decisión:** BTC como única moneda, con reserva en MXN, filtro SMA200 y sin ETH ni compra de caídas. Tamaño, escalonamiento, stop y boletas quedan a cargo del gestor de riesgo.

## Disenso (se conserva íntegro)

- **Macro y analista cripto** quieren 20% en ETH y una reserva que compre caídas. El macro argumenta que USDC protege en MXN porque el USD/MXN subió en 9 de 10 crisis.
- **El cuantitativo** quiere 100% BTC con salida total bajo la SMA200. Cambia a K1 si GBM sube a beta 1.3 o más y el comité acepta la deriva histórica.
- **El analista cripto** sostiene que el filtro SMA200 duplica los cortacircuitos y empeora la mediana (K3: −6.0% contra −0.2% de K1 en estados como el de hoy).
- **El geopolítico** acepta K4 solo con ETH ≤ 5%, efectivo en MXN y compras únicamente tras choques militares.

## Riesgos no de mercado y contingencia

- **[H] Regulación en México** (verificador; filing regulatorio):
  - Los pesos pasan por **Medá**, IFPE autorizada por la CNBV (oficio P112/2021; DOF del 12-may-2022; PES clave 65-030), solo en moneda nacional.
  - **El exchange no está supervisado en México y no puede estarlo.** Le faltaría la autorización de Banxico como ITF (Ley Fintech, art. 30), y la disposición 3.a de la Circular 4/2019 excluye prestar a clientes servicios de intercambio, transmisión o custodia de activos virtuales.
  - Solo le aplica el régimen de actividad vulnerable de la LFPIORPI (art. 17, fr. XVI).
  - La nota de Excélsior es del 10-abr-2024, anterior a Medá.
- **[H] Precedentes:**
  - UE: "solo retiros" desde el 1-jul-2026, con 6 días de aviso;
  - Brasil, 2022: 18 días sin PIX.
- **[P] Estimaciones del geopolítico:** Binance restringe México, 3%; SPEI caído más de 7 días, 5%; cargos del DOJ, 6%.
- **Contingencia** (el detalle operativo lo fija el gestor de riesgo):
  - abrir y probar una cuenta en Bitso;
  - disparadores: aviso de Binance, SPEI caído más de 48 h, o acción de CNBV, FinCEN, OFAC o DOJ;
  - respuesta: vender a MXN y retirar por SPEI; si falla, mover BTC a Bitso.

## Pronósticos del comité

| ID | Autor | Pregunta | p | Resuelve |
|---|---|---|---|---|
| P0015 | abogado del diablo | BTC-USD cierra en 67,236 o menos algún día antes del 28-ene-2027 | 0.40 | 28-ene-2027 |
| P0016 | macro | BTC-USD sobre su SMA200 el 28-dic-2026 | 0.67 | 28-dic-2026 |
| P0017 | analista cripto | BTC-USD > 84,084.40 el 28-dic-2026 | 0.55 | 28-dic-2026 |
| P0018 | cuantitativo | BTC-USD cae 20% o más desde su máximo acumulado antes del 28-ene-2027 | 0.70 | 28-ene-2027 |
| P0019 | geopolítico | Se promulga una ley de estructura de mercado cripto en EUA antes del 1-ene-2027 | 0.04 | 1-ene-2027 |

## Tamaño, stop, criterio de salida y boletas (gestor de riesgo, con veto)

**Veredicto: APRUEBA CON CAMBIOS.** Voto a favor, sin veto. Los seis cambios ya quedaron aplicados (ver abajo).

**Estado al decidir:** libro vacío (P&L 0, drawdown 0, sin rachas). Margen al tope: 5,000 MXN.

### Tamaño: 40% en BTC el lunes (4,000 MXN) y 6,000 MXN en MXN

Se toma el menor de tres métodos (`herramientas/riesgo.py`, cálculo propio):

| Método | Resultado |
|---|---|
| Por stop, con salida en SMA200 × 0.97 (≈68,970 USD) | Caben 5,644 MXN. 65% de golpe arriesga 11.5% y 100% arriesga 17.7%: los dos rebasan el 10% por operación |
| Volatilidad objetivo de 20% (Regla 18.4) | No limita. Con 40%, la cuenta combinada queda en 11.2% |
| Kelly con tope de 0.25 | 40% sobre la combinada (Sharpe 0.26) y 38-42% sobre la cuenta sola; con prima cero, 12%. **Es el que manda** |

- **Resultado simulado con 40%** (7 métodos): P(tocar −20%) de 0 a 8%; P(tocar −30%) de 1.7% o menos; P(tope) de 0.00%. En la peor trayectoria la cuenta queda en 6,891 MXN, con 1,891 de margen.
- **Aun con BTC en cero**, el tope no se toca: quedan 6,000 MXN.
- **Costo frente a entrar con 65% y filtro:** de 0 a 2 pp de P(quedar primero); 10 pp en el régimen de hoy, pero ese régimen solo tiene ~7 temporadas de historia.
- **Tramos 2 y 3** (+1,500 y +1,000 MXN, hasta 65%): los decide el comité, no antes del 30-oct y del 5-nov, y solo si se cumplen las cuatro condiciones:
  1. filtro encendido;
  2. sin cortacircuitos;
  3. volatilidad de 30 días ≤ 45%;
  4. la cuenta combinada va al menos 5 pp detrás del mejor rival.
  - Con los tramos: P(tocar −20%) de 3 a 17% y margen mínimo de 1,588 MXN.

### Filtro de tendencia: salida total con banda de ±3%

- **Dato:** cierre diario de BTC/USDT en Binance (00:00 UTC) contra la media de sus últimos 200 cierres.
- **Salida:** si el cierre queda **< SMA200 × 0.97** (≈68,970 el lunes; el nivel sube con la media), se vende el 100% al día siguiente, de 08:30 a 12:00 CDMX.
- **Reentrada:** con un cierre **> SMA200 × 1.03** (≈73,200).
- **Por qué la banda:** baja las salidas en falso de 36-51% a 16-31% con la misma P(tocar −20%). Pedir dos cierres de confirmación en vez de la banda las deja en 31-43%.
- **Vigilancia:** la rutina cripto de las 20:17 publica la boleta y la de las 08:17 la reconfirma. Los cortacircuitos se revisan cada 4 h.

### Stop: sin stop registrado; el stop es la regla de cierre

Un stop intradía en el mismo nivel:
- se dispara en 21-74% de las trayectorias;
- en 75-100% de esos casos el día cierra arriba del nivel;
- resta de 1 a 5 pp de P(quedar primero) y suma hasta 9.5 pp a P(tocar −20%).

Ejemplo del 10-oct-2025: un stop de −10% se disparó a las 21:19 UTC y el día cerró en −3.4%.

Además, el lado de compra del libro de BTC/MXN es delgado: 18,786 MXN a ±0.5% del precio medio (verificador).

### Ruta: BTC/MXN directo, con orden límite

- **Costo:** +0.10% a +0.29%, contra +0.20% por la ruta de USDT (verificador). A las 21:36 UTC el gestor midió un diferencial de 0.26%: +0.12% directo contra +0.22% por USDT.
- **Ventaja:** una sola operación y no hay que tener USDT.
- **Respaldo:** la ruta por USDT, si el diferencial de BTC/MXN pasa de 0.5%.

### Validaciones (`validar_orden`, clase cripto)

| Validación | Resultado |
|---|---|
| Tramo 1: cripto 40%, exposición bruta 0.40, riesgo 7.08% (708 MXN) | OK |
| Tramos 2 y 3: riesgo de 2.3% y 1.5% | OK |
| Límites de pérdida, tope y 8 operaciones al mes | OK |
| Costos: ~0.3% por temporada | OK |
| Fase 0 | Fallaba en lo documental; se resolvió con el cambio 3 |

### Escenarios de cola, con 40% en BTC

| Escenario | Efecto |
|---|---|
| Un día como el 10-oct-2025 | −181 MXN al cierre; −600 MXN en el mínimo del día |
| Un mes de −30% | −7.5% si es gradual; −12.2% si llega en un hueco de 2 días; −18.1% si se parece a marzo de 2020 (con 65% en BTC, −29.5%) |
| Retiros en MXN congelados | Se envía el BTC o el USDT on-chain a Bitso y se retira por SPEI desde ahí. **Un congelamiento total arriesga los 10,000 MXN: el tope no cubre el riesgo de contraparte.** |

### Cambios pedidos por el gestor, ya aplicados

1. **40% el lunes;** tramos 2 y 3 solo con las cuatro condiciones → `cripto_binance.exposicion`.
2. **Enmienda de stops** → `cripto_binance.stops` y `cripto_binance.filtro_tendencia`.
3. **Alcance de la excepción ampliado a `arena-claude-binance`** → `excepcion_cuenta_arena.alcance`, con la enmienda registrada.
4. **Kelly y límites de pérdida declarados en el perfil cripto:**
   - `kelly_fraccion_max` = 0.25;
   - `limites_perdida` de 5, 10 y 18%, provisionales del orquestador, porque el gestor pidió declararlos pero no dio cifras. Se calibran en el comité del 2-oct.
5. **Bitso verificada antes del 2-oct:** pendiente del dueño → `cripto_binance.contingencia_contraparte` y `PLAN.md`.
6. **Registro sombra en papel con la misma condición de validez:** ejecuta en la vela de 1 h de las 15:00 UTC del lunes → orden O0003.

### Boletas

- **Reales:** `bitacora/boletas/2026-09-28.md`, sección Binance (C0, C1, C1-R y la plantilla de venta S).
- **Sombra en papel:** O0003 en `bitacora/ordenes-pendientes.csv`, libro `bitacora/papel-binance/`.

## Verificación de cifras (verificador, 25-sep-2026, 21:16-21:40 UTC)

**Resultado:** de 21 afirmaciones, 16 se sostienen tal cual o con una precisión, 3 tenían una cifra imprecisa y a 1 le falta un dato: el costo del SPEI. **Ninguna corrección cambia la decisión.**

**Las precisiones que importan para ejecutar:**

| Tema | Hecho verificado | Tipo |
|---|---|---|
| Precio de BTC | 84,045.67 (20:29 UTC) y 84,084.40 (20:48 UTC) son fotos de 1 minuto, no cierres. Último cierre completo: 84,379.06 (24-sep). SMA200 con días completos: 70,850.90. La base de P0015 es la foto de las 20:29 y el pronóstico queda como se registró. | base estadística |
| Mínimo del ciclo | Cierre: 58,558.86 (30-jun-2026). Intradía: 57,747.77 (1-jul-2026). Los cortacircuitos y P0015 usan el de cierre; los stops, el intradía. | cálculo propio |
| Peor caída en 4 meses | −67.5% **en MXN** (dic-2017 a abr-2018); en USD, −66.0% de cierre a cierre | cálculo propio |
| Liquidez de BTCMXN | Diferencial de 0.19%, no 0.40%. 0.98 BTC al día. Del lado de compra del libro solo hay 18,786 MXN a ±0.5% del precio medio. | base estadística |
| Costo de comprar | BTCMXN con límite en el precio de compra: +0.10% si se llena. Por MXN→USDT→BTC: +0.20%. Tomando precio en BTCMXN: +0.29%. | cálculo propio |
| Pares y órdenes | BTCMXN, USDTMXN y ETHMXN en TRADING, con LIMIT, STOP_LOSS_LIMIT y OCO. Tick de BTCMXN: 1 MXN; paso: 0.000001 BTC; mínimo: 150 MXN. | base estadística |
| Comisión | 0.10%; con BNB, 0.075% (no vale la pena) | reporte narrativo |
| SPEI | Depósito en ≤30 min; retiro en 1-3 días hábiles; costo no verificado | reporte narrativo |
| Migración del 29-sep | De Funding a Spot; el anuncio no menciona MXN. Antes de ordenar, confirmar que los MXN estén en Spot. | reporte narrativo |
| CLARITY | Cloture rechazada 49-50 el 15-sep (votación nominal 234 del Senado) | filing regulatorio |
| Flujos a ETFs | BTC: +2,565 M USD del 1 al 24-sep. ETH: +746.7 M en 5 sesiones (SoSoValue) | base estadística |
| 10-oct-2025 | Mínimo de BTCUSDT de 102,000: −13.0% desde el máximo de las 20:44. Binance compensó ~283 M USD. Las pérdidas de paridad fueron en USDe, BNSOL y WBETH, no en USDT. | reporte narrativo y cálculo propio |

**Errores de nuestra base, corregidos en sitio y registrados en `conocimiento/registro-de-errores.md`:**
- el capítulo 24 negaba la votación de cloture, que sí ocurrió;
- la fila de BTC de `arena/investigacion/03-teoria-de-torneos-y-estrategia-competitiva.md` §6 usaba 252 días. Lo correcto es −32.5%, −30.7% y 42.3% con √365.

**Confiabilidad:** alta en datos de mercado y regulación; media en microestructura, que cambia con el tiempo.
