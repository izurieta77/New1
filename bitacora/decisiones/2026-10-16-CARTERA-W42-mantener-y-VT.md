# Decisión de cartera · comité semanal W42 · viernes 16-oct-2026

> Skill `comite-de-inversion`; el orquestador preside con el rol de `decisor`. Pasaron 10 días hábiles desde la decisión W40 del 2-oct (REGLAS §4). Fase 0, con la excepción de la cuenta arena vigente. Tesis y contexto: `bitacora/comite/2026-10-16-expediente.md` (copiado al repositorio el 17-oct por la revisión §1.2; antes apuntaba a un archivo temporal).

## Decisión
1. **Papel GBM: MANTENER (A).** Se quedan 5 SPYM, 1 QQQM, 2 UPRO (stop 135.76) y 1,072 MXN de efectivo. Sin órdenes nuevas. El stop y el filtro se aplican **sin discreción**.
2. **Real GBM: B2 en la versión del gestor de riesgo.** Comprar **1 VT** (Vanguard Total World Stock, ~2,898 MXN, 28.9% de la cuenta); el resto (~2,134 MXN) sigue en Smart Cash.
   - B2 en SPYM queda **VETADO**, porque rompe `etf_indice_max` = 60% por ETF.
   - Antes de ejecutar hay que **verificar que VT exista en GBM** y el **dueño debe firmar la boleta** (`bitacora/boletas/2026-10-19.md`).
3. **Real Binance: MANTENER (A).** BTC se queda en 40%. B3 se rechaza: el cierre de 81,616 no supera 87,396 y el calendario de tramos no permite antes del 30-oct. [Corregido 17-oct-2026, conciliación, `bitacora/arbitraje/2026-10-16.md` §5.1: al decidir, 81,616 era el precio en vivo de la vela 1d abierta del 16-oct, no un cierre; el último cierre era 82,245.93 (BTCUSDT 1d del 15-oct, Binance). La vela del 16-oct cerró a las 00:00 UTC del 17-oct en 81,615.64. Con cualquiera de las tres cifras B3 sigue fuera (< 87,396).]
4. **R12: se aprueba el pre-registro** de la condición de VIX, **solo para evaluación fuera de muestra**. El filtro vivo no cambia. Debe estar en git **antes del 23-oct** y antes de cualquier cierre del VIX ≥ 25.

## Tesis y cómo se refuta
- **Tesis (mantener):** ninguna regla pre-registrada se disparó. Recortar o rotar por noticias es discrecional y paga ~0.58% por vuelta. El stop y el filtro ya acotan la cola: −394 MXN, 1.95% del capital si salta el stop.
- **Refutación al 23-oct (abogado):** cualquiera de estos hechos refuta mantener:
  - VIX ≥ 25;
  - ^GSPC < 7,053;
  - UPRO < 135.76;
  - la cuenta de papel a −8% desde su pico.
- **Tesis de B2:** tener 50% de efectivo en la cuenta real contra rivales invertidos crea varianza relativa y cuesta ~2.5 pp al año. VT agrega exposición amplia sin sumar concentración en megatecnológicas.
- **Refutación de B2 (al 28-ene-2027):** que VT rinda menos que Smart Cash más los costos de ida y vuelta (~1%).

## Dictámenes (3 líneas cada uno)
- **Macro (62): A + B2 de 2,500.**
  - Régimen mixto con sesgo estanflacionario: 10a en 5.19%, tasa real 2.84% (percentil 99) y HY +54 pb en un mes.
  - El efectivo en MXN es una apuesta corta en USD contra rivales dolarizados, y el diferencial Fed-Banxico es el más delgado en una década.
  - Pasa a B1 si el VIX llega a 22 o más con el 10a en 5.25% o más.
- **Cuantitativo (60): A + B2 escalonado.**
  - Probabilidad de ~8% de tocar el stop antes del 23-oct.
  - R06 fuera de muestra da "solo protección" (DSR 0.84 < 0.95); el 3x no tiene un edge demostrado, pero recortarlo no está pre-registrado.
  - R12 se pre-registra con prueba fuera de muestra deflactada.
- **Geopolítico (60): B1, y B2 después del FOMC.**
  - El GPR diario llegó a 342, el máximo en 90 días. El AI-GPR petrolero está en el percentil 99.
  - Kalshi y Polymarket dan 13.5% a un alza en octubre y ~76% en diciembre.
  - Con el stop a 7.9%, un día de −2.7% del S&P lo dispara. [Corregido 17-oct-2026, conciliación, fallo §5.2: 7.9% es el precio sobre el stop (146.43 / 135.76 − 1). La caída que lo toca es 7.29% (1 − 135.76 / 146.43), o sea un S&P de ≈ −2.4% en un día con el 3x, no −2.7%.]
- **Cripto (75): A en Binance.**
  - Vol30 de 37.4% (≤ 45%, cumple), pero el cierre de 82,246 queda debajo de 87,396.
  - Pasar de 40% a 65% sube la vol de la cuenta de ~15% a ~24%.
  - El efectivo cripto se queda en MXN, no en USDT.
- **Abogado del diablo:**
  - A sobrevive con condiciones (60).
  - B1 no sobrevive como decisión discrecional (60).
  - B2 sobrevive con condiciones (65); encontró el error de que 2,500 en SPYM rompen el 60%.
  - B3 no sobrevive (80) y C no sobrevive (75).
  - Corrige al comité: **no hay modo torneo**, porque la ventaja es de ~1 pp contra una regla de 5 pp.

## Votos y confianzas
| Agente | Papel GBM | Real GBM | Binance | Confianza |
|---|---|---|---|---|
| analista-macro | A | B2 (2,500) | A | 62 |
| analista-cuantitativo | A | B2 escalonado | A | 60 |
| analista-geopolitico | B1 | B2 después del 28-oct | A | 60 |
| analista-cripto | — | B2 ≤ 2,500 o liquidez | A | 75 |
| abogado-del-diablo | A (con condiciones) | B2 con otro índice 1x | A | 60-65 |
| gestor-de-riesgo | A | B2 = 1 VT; **veto a SPYM** | A | 70 / 60 |

- **Papel:** 3 a 1 a favor de A, con confianza media de 60.7 entre los que votaron A. Aprobada. [Aclarado 17-oct-2026, conciliación, fallo §5.3: el conteo es correcto. Según `.claude/skills/comite-de-inversion/SKILL.md` pasos 2, 3 y 5, votan los dictámenes del paso 2 (macro, cuantitativo, geopolítico y abogado; el cripto no votó en papel). El gestor de riesgo dimensiona y puede vetar, pero no vota; su "A" de la tabla es su validación. Si se le contara, quedaría 4 a 1 con media de 63.0, y el resultado sería el mismo.]
- **Real GBM:** 5 de 5 a favor de B2. El instrumento lo fija el gestor de riesgo: el veto a SPYM manda y VT es la versión que cumple todo.
- **Binance:** unánime por A.

## Gestor de riesgo (resumen)
- **A en papel aprobada, sin veto.**
  - Pesos: SPYM 41.1%, QQQM 27.0%, UPRO 26.8%.
  - Pérdida con stop: 394 MXN, 1.95% del capital (el límite es 3%).
- **B2 en SPYM: VETO.**
  - 1 título deja SPYM en 66.3% y queda debajo de la orden mínima.
  - 2 títulos lo dejan en 82.8%.
- **B2 = 1 VT (156.82 USD × 18.479 = 2,897.88 MXN):**
  - VT queda en 28.9%; bruto 78.6%.
  - 2 de 8 operaciones del mes; rotación 0.79x.
- **Cola de la cuenta real con VT:**
  - un día tipo 16-mar-2020 cuesta −8.9%;
  - un peso +20% cuesta −13.1% y toca el cortacircuitos de −12%.
  - Ningún escenario se acerca al tope de 5,000 MXN.
- **Advertencia del gestor:** B2 se justifica por exposición, no por edge. El beneficio esperado (~40 MXN) apenas supera el costo (~29 MXN).

## Verificación (orquestador, 16-oct antes del commit `75726c2` de las 22:56 UTC) [Corregido 17-oct-2026, revisión §1.2: decía "~23:20 UTC", hora posterior al commit]
- **VT** = 156.82 USD (Yahoo). 1 VT = 2,897.88 MXN, que es 28.92% de 10,020.07.
- **SPYM +1** llevaría la posición a 66.27%.
- **Pérdida con stop:** 2 × (146.43 − 135.76) × 18.479 = 394.34 MXN.
- **Remanente:** 5,040.16 − 2,897.88 × 1.0029 = 2,133.88 MXN.
- **Brent:** el abogado dijo "~85.6"; **es incorrecto**. Yahoo BZ=F da 109.69 el 16-oct (+3.6%) y FRED DCOILBRENTEU (spot) 126.55 el 14-oct. La lectura estanflacionaria de la tesis se sostiene.

## Disenso (se conserva)
- **Geopolítico:** quería B1, bajar UPRO a 1 título. Su argumento es el régimen geopolítico alto y el stop a 7.9% (precio sobre el stop; la caída que lo toca es 7.29%, ≈ −2.4% del S&P; nota de conciliación del 17-oct). Con B1, la pérdida en un día tipo 16-mar-2020 sería −13.1% y no −17.9%. Se revisa el 23-oct con sus disparadores: VIX ≥ 22 con 10a ≥ 5.25%, o HY > 3.55%.
- **Momento de B2:** el geopolítico quería esperar al FOMC del 28-oct y el cuantitativo, escalonar. La boleta es una sola orden de ~2,898 MXN, con semáforo que la frena si el USD/MXN ≥ 18.81 o el VIX ≥ 25.
- **Modo torneo:** el abogado y el gestor corrigen la tesis. No se activa, porque la ventaja es de ~1 pp contra una regla de 5 pp.

## Pronósticos registrados
- **P0135:** índice del papel ≥ 100.92 al 23-oct (0.55).
- **P0136:** WTI CL=F ≥ 100 en algún cierre del 19 al 30-oct (0.70).
- **P0137 (agregado el 17-oct, revisión §1.1):** VT > 156.82 el 13-nov (0.56), pronóstico propio de la decisión B2.
- **Previos ligados:** P0127 (UPRO > 135.76 al 30-oct, 0.82) y P0131 (alza de la Fed el 28-oct, 0.13).

## Ejecución
- **Papel:** nada.
- **Real GBM:** boleta `bitacora/boletas/2026-10-19.md`, que el dueño debe confirmar.
- **Binance:** nada.
