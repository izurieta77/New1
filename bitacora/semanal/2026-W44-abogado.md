# Abogado del diablo · Auditoría semanal W44 · viernes 30-oct-2026

> Fase 0, solo papel. Informe del subagente `abogado-del-diablo`, guardado por el orquestador sin cambios de fondo. Recálculos en Python sobre los datos ya guardados (`laboratorio/replicas/R22b-datos`, `R22b.py`), con un script de borrador fuera del repo.

## Resumen
| # | Afirmación | Veredicto | Voto |
|---|---|---|---|
| 1 | R22b → plantilla §8: mediana de 4T y banda de UPA de ±4–5% | **Se sostiene con matiz.** La regla vale; la banda está mal calibrada | A favor de la regla, en contra de la banda |
| 2 | R20/R21 → B1 (1 UPRO) se sostiene; seguir con UPRO | **No se sostiene** como razón para mantener el UPRO. B1 solo gana frente a U27 | En contra |
| 3 | No vender dentro de Binance con los retiros en 0/990 | **Se sostiene con matiz.** Una de las dos razones es falsa y O0007 contradice la política | A favor, si se unifican las reglas |

## 1. R22b: mediana de 4 trimestres para la tasa efectiva
**Pre-mortem (marzo de 2027: la UPA estimada falla y la plantilla pierde credibilidad).**
1. El error de verdad es mucho mayor que ±4–5%. Ese número es el error *medio*, no una banda de cobertura, y la muestra ya excluye pérdidas y tasas fuera de 0–60%.
2. La significancia sin 4T dependía de 14 emisoras recuperadas después del fallo de R22.
3. Cuando la empresa da guía de tasa, una regla mecánica pierde contra ella.

**Tasa base.** En este laboratorio, 25 de 42 filas acabaron descartadas. En la literatura, los efectos que pasan p < 0.05 una sola vez se reducen mucho fuera de muestra (Harvey, Liu y Zhu 2016 piden t > 3; citado de memoria).

**El ataque más fuerte (selección de muestra / caminos que se bifurcan).** AC-29 §3.3: en las 29 emisoras originales de A el resultado es p = 0.135 y no se cumplen ni H1 ni H2. El p = 0.023 sale de las 14 emisoras recuperadas (grandes y de tasa estable), y la corrección se escribió conociendo el resultado de B. "Replicado" exagera. H2 pasa con 2.99999 contra 3.0: ruido. **La versión con el 4T sí es robusta:** p ≈ 1e−8, IC95 por emisora [0.85, 1.66] pp; esa versión justifica la regla.

**Reglas más simples** (mismos datos; n = 298 sin 4T / 616 con 4T):

| Regla | MAE sin 4T | MAE con 4T |
|---|---|---|
| **Mediana de 4** | **2.93** | **3.45** |
| Tasa de 12 meses (Σimpuesto / Σutilidad antes de impuestos) | 3.28 | 3.88 |
| Mismo trimestre del año anterior | 3.96 | 4.61 |
| Último trimestre | 3.45 | 4.64 |
| 21% estatutaria | 5.78 | 6.42 |

- Frente a la tasa de 12 meses, la mediana de 4 gana con el 4T por signos 334/282 (p = 0.040); IC por emisora de la diferencia [0.3, 0.6] pp. Sin el 4T no se distinguen (p = 0.77).
- **La guía de la empresa no se probó.** Bratten et al. (TAR 2017): la guía de la gerencia sobre la tasa es informativa.

**Banda recalculada.** Error de UPA de la mediana de 4 (con 4T): p50 2.5%, **p80 6.1%, p90 9.4%**; sin 4T: p80 5.5%, p90 8.3%. ±4–5% cubre ≈70% (estimación).

**Corrección propuesta para la plantilla §8.**
- Punto central: la guía de tasa de la empresa si existe y está fechada; si no, la mediana de 4 trimestres con el 4T reconstruido.
- Banda: **±6% (p80) o ±9% (p90)**.
- Emisoras con pérdida o tasa fuera de 0–60%: "sin pronóstico mecánico". No aplica a mexicanas (sin XBRL).
- Etiqueta: "Replicado (B no ciego; sin 4T frágil)".

**Falsabilidad.** Congelar la regla hoy y evaluarla con los 4T de 2026 de los 10-K (corte 15-mar-2027). Se refuta si el MAE de la mediana de 4 ≥ el del último trimestre, o si ±6% cubre < 75%.

## 2. R20/R21 → seguir con 1 UPRO
**Pre-mortem (abril de 2027: el papel pierde contra U0).**
1. El stop, a 4.0%, se dispara en ruido y la pérdida queda realizada (R16: el stop baja el Sharpe y empeora la MDD).
2. Con μ − r de 1–2%, el 3x pierde contra el 1x en esperanza.
3. El +0.73 pp de CAGR es dentro de muestra (1990–2026, S&P fuerte) y el filtro salió de minar variantes.

**Tasa base.** McLean y Pontiff (2016, citado de memoria): las anomalías publicadas pierden ~26% fuera de muestra y ~58% tras publicarse. +0.73 → ≈ +0.36 pp/año, contra +5.0 pp en P(−12%) y +3.2 pp en P(−20%).

**El ataque más fuerte.** R20 y R21 no prueban que el UPRO aporte; solo que la brecha no cambia las colas ("no es un respaldo del 3x", R21). Empate en μ ≈ 11.2% (r 3.8%, σ 17%); Vanguard estima ~4–5% anual a 10 años para EE. UU. (dic-2025, +~1 pp en abril). El filtro no corrige el arrastre (~4σ² ≈ 11.6 pp/año a 3x).

**P(cierre ≤ 135.76)** (UPRO 141.21, σ diaria = 3 × VIX/√252, corrección por cierres discretos):

| Supuesto de σ | 1 sesión | 5 sesiones | Al 20-nov (15) |
|---|---|---|---|
| VIX 19.42 | 14% | 46% | 67% |
| σ realizada 16 | 10% | 40% | 63% |
| VIX 23.93 (máx. intradía) | 19% | 52% | 71% |

**Corrección.** Votar **U0 contra U13.5**, no B1 contra A. No reentrar tras el stop sin un R23 pre-registrado (U0 vs U13.5 con μ 5/7/9/11%, r 3.8%, fuera de muestra 2009–2026 con UPRO real). Voto: U0 con la regla de la vela de 14:45 UTC del lunes (≈7.8 MXN de comisión).

**Falsabilidad.** Si en R23, con μ = 7%, U13.5 supera a U0 en ≥ 0.3 pp de CAGR sin sumar más de 3 pp a P(−12%), se retira la objeción.

## 3. Binance: no vender dentro con los retiros en 0/990
**Pre-mortem (noviembre: −30% en BTC).** Reapertura en semanas (mediana de solventes 8 días; ninguno de 7 reabrió en 48 h); rieles por fases sin plan por caso; O0007 vende dentro y registra una protección que no existe.

**Tasa base** (`conocimiento/cripto/fichas/2026-10-30-hackeos-exchanges-reapertura.md`, n = 11, sesgo de supervivencia): los solventes recuperaron 100% nominal; la pérdida de Binance ≈ 4.3% de reservas (Bybit 9.0%, Bitget 6.3%, pagaron todo).

**El ataque más fuerte.** "Precio deprimido por el pánico" es **falso con los datos propios** (Binance en línea con Deribit; E9 VERDE). La razón válida: vender BTC a MXN dentro no reduce contraparte; solo cambia la exposición de mercado. Mantener BTC conserva la opción del primer riel que abra. **La exposición de mercado la gobierna el filtro (encendido, +8.3%).** En juego: ≈1,910 MXN en BTC + 3,002 MXN (real).

**Contradicción.** O0007 vende dentro, justo lo que la política real descarta; el inicio del conteo cambió tres veces (21:50, 00:00, 02:10 UTC).

**Unificación propuesta.** Fuente única: `config/parametros.json`; la lista §3 y la decisión del 25-sep la citan.
- ROJA aislada = alerta operativa: no depositar, verificar cada 4 h, boleta armada.
- Contingencia: retiros BTC o MXN suspendidos > 24 h (desde la primera lectura **A** del endpoint), SPEI caído > 48 h, acción de autoridad, restricción a México o prueba de reservas no publicada.
- Respuesta por riel: (a) abre BTC → retirar en especie en la primera hora; (b) solo SPEI → vender con límite y retirar; (c) ambos → retirar ambos en especie; (d) todo cerrado → no convertir; vender solo por filtro o stop de mercado.
- Papel: anular O0007; marca de "congelado" (precio de mercado + escenarios de recuperación 100% / 95.7% / 68%).
- Si al 7-nov sigue todo cerrado: escalar (respaldo de saldos, ticket) y revisar solvencia contra E1 y P0207.

## Sesgos del comité
- **Anclaje:** 2.99999 celebrado como 3.0; el stop tratado como protección.
- **Confirmación:** "R18 sigue válido" leído como respaldo del UPRO; "Replicado" con B no ciego.
- **Statu quo / costo hundido:** se comparó B1 contra 2 UPRO, no contra 0.
- **Narrativa y recencia:** "el mayor hackeo de la historia" empuja a la urgencia.
- **Exceso de confianza:** "precio de pánico" sin contrastar.

## Condiciones mínimas
1. Plantilla §8 con banda p80/p90 y guía de la empresa primero; prueba fuera de muestra a marzo de 2027.
2. R23 pre-registrado antes de cualquier reentrada al UPRO.
3. Contingencia unificada por estado del riel; O0007 anulada.

## Fuentes
- [Bratten, Gleason, Larocque y Mills, TAR 2017](https://iro.uiowa.edu/esploro/outputs/journalArticle/Forecasting-Taxes-New-Evidence-from-Analysts/9984380541002771)
- [Vanguard VEMO](https://corporate.vanguard.com/content/corporatesite/us/en/corp/vemo/vemo-return-forecasts.html) · [Morningstar 2026](https://www.morningstar.com/markets/experts-forecast-stock-bond-returns-2026-edition)
- [Bloomberg, Bybit 21-feb-2025](https://www.bloomberg.com/news/articles/2025-02-21/crypto-prices-dip-after-1-5-billion-theft-from-bybit-exchange)
- McLean-Pontiff (2016) y Harvey-Liu-Zhu (2016): de memoria, sin consulta web.
- Internos: `laboratorio/auditorias/AC-29-R22/informe.md`, `laboratorio/replicas/R21-r18-con-brecha-r20.md`, `bitacora/cripto/2026-10-30.md`, `config/parametros.json`.
